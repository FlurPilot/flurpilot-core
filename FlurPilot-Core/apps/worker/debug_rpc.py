
import os
import json
from supabase import create_client
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Debugging RPC calculate_net_parcel...")

# 1. Define Sample GeoJSON (Square Field)
field_geojson = {
    "type": "Polygon",
    "coordinates": [[
        [11.573, 48.135],
        [11.577, 48.135],
        [11.577, 48.139],
        [11.573, 48.139],
        [11.573, 48.135]
    ]]
}

# 2. Define Sample Building (Small Square inside)
building_geojson = {
    "type": "Polygon",
    "coordinates": [[
        [11.574, 48.136],
        [11.575, 48.136],
        [11.575, 48.137],
        [11.574, 48.137],
        [11.574, 48.136]
    ]]
}

params = {
    "field_geom": field_geojson,
    "building_geoms": [building_geojson]
}

print(f"Params: {json.dumps(params)[:100]}...")

try:
    response = client.rpc("calculate_net_parcel", params).execute()
    data = response.data
    
    print("RPC Response:", data)
    
    if data:
        print(f"Area: {data[0].get('net_area')}")
    else:
        print("No data returned.")

except Exception as e:
    print(f"RPC Error: {e}")
