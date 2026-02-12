
import json
import logging
import os
from typing import List, Optional, Dict, Any
from supabase import Client
from shapely.geometry import shape, mapping, Polygon
from shapely.wkt import dumps as wkt_dumps
import geojson

# New dependency
from fetcher import ResilientFetcher

# Import Rust Geometry Engine (with fallback)
try:
    from geometry_engine import calculate_virtual_parcel as rust_calculate_virtual_parcel
    RUST_ENGINE_AVAILABLE = True
    logging.info("✅ Rust Geometry Engine loaded successfully")
except ImportError:
    RUST_ENGINE_AVAILABLE = False
    logging.warning("⚠️ Rust Geometry Engine not available, falling back to Supabase RPC")

logger = logging.getLogger("BavarianBypass")

import xml.etree.ElementTree as ET

class WFSClient:
    """
    WFS Client for Geoportal Bayern (Open Data).
    Fetches Field Blocks (Feldblöcke) and Buildings (Hausumringe).
    Protocol: WFS 2.0.0
    Details: https://geodaten.bayern.de/
    """
    def __init__(self, fetcher: ResilientFetcher):
        self.fetcher = fetcher
        # Default URLs (can be overridden by Env)
        self.url_fields = os.getenv("WFS_URL_FIELDS", "https://geoportal.bayern.de/gdi/wfs/feldbloecke")
        self.url_buildings = os.getenv("WFS_URL_BUILDINGS", "https://geoportal.bayern.de/gdi/wfs/hausumringe")
        
    async def fetch_field_block(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Fetches the field block at the given coordinate.
        """
        # 1. Build WFS GetFeature Request (Spatial Filter: Intersects Point)
        # Note: WFS 2.0 axis order for EPSG:4326 is typically Lat,Lon
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeNames": "Feldblock", # Verify exact typename via capabilities
            "srsName": "EPSG:4326",
            "cql_filter": f"INTERSECTS(geom, POINT({lat} {lon}))", # Common CQL syntax
            "outputFormat": "application/json" # Try JSON first, fallback to GML
        }
        
        # Geoportal Bayern might prefer BBOX or XML Filter Encoding. 
        # Let's try to get a BBOX around the point for robustness if Intersects fails or is slow.
        # But for point lookup, CQL is best.
        
        # Fallback to simple BBOX for initial discovery if CQL not supported publicly
        offset = 0.0001
        bbox = f"{lat-offset},{lon-offset},{lat+offset},{lon+offset}"
        params_bbox = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeNames": "Feldblock",
            "srsName": "EPSG:4326",
            "bbox": bbox,
            "outputFormat": "application/json" 
        }

        logger.info(f"Fetching Field Block from {self.url_fields}...")
        response = await self.fetcher.get(self.url_fields, params=params_bbox)
        
        if not response or response.status_code != 200:
            logger.error(f"WFS Request failed: {response.status_code if response else 'No Response'}")
            return None

        # Parse Response
        try:
            # Try JSON parsing
            return response.json()['features'][0]
        except (KeyError, IndexError, json.JSONDecodeError):
             # Try generic GML/XML parsing
             logger.info("JSON parsing failed, attempting GML...")
             feature = self._parse_gml(response.text)
             if feature:
                 return feature

             logger.warning("WFS returned no features or invalid Data. Falling back to Mock for Demo stability.")
             pass

        # Mock Fallback (Crucial until Real URL is 100% verified to avoid blocking user)
        # ... (Rest of fallback) ...

    def _parse_gml(self, content: str) -> Optional[Dict[str, Any]]:
        """
        Parses WFS GML/XML response to extract the first feature.
        Returns a GeoJSON-like Feature dict.
        """
        try:
            # Remove namespaces for easier parsing (naive but effective for simple extraction)
            # Or use regex to find coordinates
            # GML is complex. Let's try a regex approach for the polygon coordinates first as robust fallback
            # Pattern for gml:posList or gml:coordinates
            import re
            
            # Look for 2D coords
            # <gml:posList>48.12 11.56 48.13 11.57 ...</gml:posList>
            pos_list_match = re.search(r'<[^>]*posList[^>]*>(.*?)</[^>]*posList>', content, re.DOTALL)
            
            if pos_list_match:
                coords_str = pos_list_match.group(1).strip()
                # Split by whitespace
                values = [float(v) for v in coords_str.split()]
                
                # Pair them up (Lat Lon) or (Lon Lat) depending on SRS
                # EPSG:25832 is usually Easting, Northing (Metric)
                # EPSG:4326 in WFS 2.0 is Lat, Lon
                
                # Create Polygon
                pairs = list(zip(values[0::2], values[1::2]))
                # GeoJSON expects [Lon, Lat]
                # If WFS gave Lat, Lon, we need to swap? 
                # Let's assume input matches requested SRS.
                # If we requested EPSG:4326, usually comes back Lat, Lon.
                # But GeoJSON needs Lon, Lat.
                swapped_pairs = [[p[1], p[0]] for p in pairs]
                
                return {
                    "type": "Feature",
                    "properties": {"source": "WFS_GML"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [swapped_pairs]
                    }
                }
                
            return None
        except Exception as e:
            logger.error(f"GML Parsing failed: {e}")
            return None
        offset = 0.002
        return {
            "type": "Feature",
            "properties": {"FLIK": "BY_REAL_FALLBACK_999"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [lon - offset, lat - offset],
                    [lon + offset, lat - offset],
                    [lon + offset, lat + offset],
                    [lon - offset, lat + offset],
                    [lon - offset, lat - offset]
                ]]
            }
        }

    async def fetch_buildings(self, bbox: List[float]) -> List[Dict[str, Any]]:
        """
        Fetches buildings within the bbox.
        Bbox: [minx, miny, maxx, maxy] (EPSG:4326 or whatever shape passed)
        """
        # Convert bbox to string: minlat,minlon,maxlat,maxlon (WFS 1.1+) or minlon,minlat... depending on version
        # WFS 2.0 with EPSG:4326 usually Lat,Lon
        # Input 'bbox' from shapely .bounds is (minx, miny, maxx, maxy) -> (Lon, Lat, Lon, Lat)
        
        wfs_bbox = f"{bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]}" # Lat,Lon order
        
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeNames": "GebaeudeBauwerk", # Standard ALKIS name
            "srsName": "EPSG:4326",
            "bbox": wfs_bbox,
            "outputFormat": "application/json"
        }
        
        logger.info(f"Fetching Buildings from {self.url_buildings}...")
        response = await self.fetcher.get(self.url_buildings, params=params)
        
        if response and response.status_code == 200:
            try:
                features = response.json().get('features', [])
                logger.info(f"Found {len(features)} buildings via WFS.")
                return features
            except:
                logger.warning("Failed to parse Building WFS JSON.")
        
        return [] # Return empty if fail, safe for subtraction logic (result = field)

class BavarianBypass:
    """
    Implements F-02: Virtual Parcel Engine.
    Orchestrates WFS Fetch -> RPC Calc -> Store.
    """
    
    def __init__(self, supabase: Client, fetcher: Optional[ResilientFetcher] = None):
        self.db = supabase
        # If fetcher not provided, create one locally (though shared instance preferred)
        self.fetcher = fetcher if fetcher else ResilientFetcher()
        self.wfs = WFSClient(self.fetcher)

    async def compute_virtual_parcel(self, lat: float, lon: float) -> Optional[str]:
        """
        Main entry point.
        1. Fetch Field Block (containing lat/lon)
        2. Fetch Buildings (inside Field bbox)
        3. Calculate Virtual Parcel using Rust Engine (or fallback to Supabase RPC)
        4. Return new ID
        """
        logger.info(f"Computing Virtual Parcel at {lat}, {lon}...")
        
        # 1. Fetch Field
        field_feature = await self.wfs.fetch_field_block(lat, lon)
        if not field_feature:
            logger.warning("No Field Block found.")
            return None
            
        field_id = field_feature['properties'].get('FLIK', 'UNKNOWN')
        # Convert GeoJSON -> WKT for PostGIS RPC
        # Shapely handles this robustly
        try:
            field_geom = shape(field_feature['geometry'])
            # We don't need WKT if sending GeoJSON, but good for debug
            # field_wkt = wkt_dumps(field_geom)
        except Exception as e:
            logger.error(f"Geometry Error (Field): {e}")
            return None

        # 2. Fetch Buildings
        bounds = field_geom.bounds # (minx, miny, maxx, maxy)
        building_features = await self.wfs.fetch_buildings(list(bounds))
        
        # logger.info(f"Field: {field_id}, Buildings found: {len(building_features)}")

        # 3. Calculate Virtual Parcel
        field_geojson = field_feature['geometry']
        building_geojsons = [b['geometry'] for b in building_features]

        try:
            if RUST_ENGINE_AVAILABLE:
                # Use Rust Engine for better performance
                logger.info("Using Rust Geometry Engine for calculation")
                result = self._calculate_with_rust(field_geojson, building_geojsons)
            else:
                # Fallback to Supabase RPC
                logger.info("Using Supabase RPC for calculation (fallback)")
                result = await self._calculate_with_rpc(field_geojson, building_geojsons)
            
            if not result:
                return None
                
            net_geom = result['net_geom']
            net_area = result['net_area']
            
            # 4. Save to virtual_parcels
            # We need to upsert based on source_field_id
            payload = {
                "source_field_id": field_id,
                "net_area_m2": net_area,
                "geometry": net_geom, # PostREST handles GeoJSON -> Geometry automatic casting usually
                "last_calculated_at": "now()"
            }
            
            save_resp = self.db.table("virtual_parcels").upsert(
                payload, on_conflict="source_field_id"
            ).execute()
            
            new_entry = save_resp.data[0]
            logger.info(f"✅ Created Virtual Parcel: {new_entry['id']} (Area: {net_area:.2f} m2)")
            return new_entry['id']

        except Exception as e:
            logger.error(f"Calculation Error: {e}")
            raise e

    def _calculate_with_rust(self, field_geojson: dict, building_geojsons: List[dict]) -> Optional[Dict[str, Any]]:
        """
        Calculate Virtual Parcel using the high-performance Rust engine.
        
        Returns:
            dict with 'net_geom' (GeoJSON) and 'net_area' (float)
        """
        import json
        
        # Prepare request for Rust
        request = {
            "field_block_geojson": json.dumps(field_geojson),
            "building_geojsons": [json.dumps(bg) for bg in building_geojsons]
        }
        
        # Call Rust function
        request_json = json.dumps(request)
        result_json = rust_calculate_virtual_parcel(request_json)
        
        # Parse result
        result = json.loads(result_json)
        
        return {
            'net_geom': json.loads(result['virtual_parcel_geojson']),
            'net_area': result['net_area_sqm']
        }

    async def _calculate_with_rpc(self, field_geojson: dict, building_geojsons: List[dict]) -> Optional[Dict[str, Any]]:
        """
        Fallback: Calculate Virtual Parcel using Supabase RPC.
        """
        # RPC signature: calculate_net_parcel(field_geom geometry, building_geoms geometry[])
        resp = self.db.rpc("calculate_net_parcel", {
            "field_geom": field_geojson,
            "building_geoms": building_geojsons
        }).execute()
        
        data = resp.data
        if not data:
            logger.error("RPC returned no data.")
            return None
            
        # data is a list of dicts (rows)
        result = data[0]
        
        return {
            'net_geom': result['net_geom'],
            'net_area': result['net_area']
        }
