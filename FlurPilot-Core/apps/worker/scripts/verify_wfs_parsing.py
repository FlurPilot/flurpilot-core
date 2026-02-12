
import asyncio
import sys
import os
from unittest.mock import MagicMock, AsyncMock

# Add parent directory to path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from bavarian_bypass import WFSClient
from fetcher import ResilientFetcher

# Sample GML Response (simplified WFS 2.0)
SAMPLE_GML = """
<?xml version="1.0" encoding="UTF-8"?>
<wfs:FeatureCollection xmlns:wfs="http://www.opengis.net/wfs/2.0" xmlns:gml="http://www.opengis.net/gml/3.2">
    <wfs:member>
        <flur:Feldblock>
            <flur:flik>BY_TEST_GML_123</flur:flik>
            <flur:geom>
                <gml:Polygon gml:id="P1" srsName="urn:ogc:def:crs:EPSG::4326">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>
                                48.1 11.5 48.2 11.5 48.2 11.6 48.1 11.6 48.1 11.5
                            </gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </flur:geom>
        </flur:Feldblock>
    </wfs:member>
</wfs:FeatureCollection>
"""

async def test_wfs_parsing():
    print("🧪 Testing WFS Client Parsing...")
    
    # Mock Fetcher
    mock_fetcher = MagicMock(spec=ResilientFetcher)
    mock_fetcher.get = AsyncMock()
    
    # 1. Test JSON (Success Case)
    print("\n[Test 1] JSON Response")
    
    mock_response_json = MagicMock()
    mock_response_json.status_code = 200
    mock_response_json.json.return_value = {
        "features": [{
            "type": "Feature",
            "properties": {"FLIK": "BY_JSON_123"},
            "geometry": {"type": "Polygon", "coordinates": []}
        }]
    }
    mock_fetcher.get.return_value = mock_response_json
    
    client = WFSClient(mock_fetcher)
    feat = await client.fetch_field_block(48.0, 11.0)
    
    if feat and feat['properties']['FLIK'] == "BY_JSON_123":
        print("✅ JSON Parsing: Passed")
    else:
        print(f"❌ JSON Parsing: Failed. Got {feat}")

    # 2. Test GML (Fallback Case)
    print("\n[Test 2] GML Response (Fallback)")
    
    import json
    mock_response_gml = MagicMock()
    mock_response_gml.status_code = 200
    mock_response_gml.json.side_effect = json.JSONDecodeError("Expecting value", "", 0) # Simulate JSON fail
    mock_response_gml.text = SAMPLE_GML
    
    mock_fetcher.get.return_value = mock_response_gml
    
    feat_gml = await client.fetch_field_block(48.0, 11.0)
    
    if feat_gml and feat_gml['geometry']['type'] == "Polygon":
        coords = feat_gml['geometry']['coordinates'][0]
        # Check swap (Input was Lat Lon 48.1 11.5 etc, expect Lon Lat in GeoJSON)
        # First point: 11.5, 48.1
        if coords[0][0] == 11.5 and coords[0][1] == 48.1:
             print("✅ GML Parsing: Passed (Coordinates swapped correctly)")
        else:
             print(f"❌ GML Parsing: Coordinates incorrect. Got {coords[0]}")
    else:
        print(f"❌ GML Parsing: Failed. Result: {feat_gml}")

if __name__ == "__main__":
    asyncio.run(test_wfs_parsing())
