import asyncio
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

async def test_geo():
    print("Testing PostGIS Engine...")
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Define a simple polygon (A square near Munich)
    # WKT Format: POLYGON((lng lat, lng lat, ...))
    wkt_polygon = "POLYGON((11.5 48.1, 11.6 48.1, 11.6 48.2, 11.5 48.2, 11.5 48.1))"
    
    data = {
        "alkis_id": "TEST-PARCEL-001",
        "geom": wkt_polygon,
        "area_sqm": 1000,
        "properties": {"type": "test_parcel"}
    }
    
    try:
        # 1. Insert
        print(f"Inserting Parcel: {data['alkis_id']}...")
        client.table("geo_parcels").upsert(data, on_conflict="alkis_id").execute()
        print("✅ Insert Successful.")
        
        # 2. Query (using PostGIS function via RPC is ideal, but for now just select)
        # Note: Supabase JS/Python client usually returns GeoJSON for geometry columns if PostGIS is enabled correctly
        response = client.table("geo_parcels").select("id, geom").eq("alkis_id", "TEST-PARCEL-001").execute()
        print(f"Retrieved: {response.data}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Did you run the CREATE EXTENSION postgis SQL?")

if __name__ == "__main__":
    asyncio.run(test_geo())
