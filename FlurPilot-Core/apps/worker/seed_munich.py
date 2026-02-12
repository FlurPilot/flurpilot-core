import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    print("No Creds")
    exit(1)

client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Munich Marienplatz approx
# Polygon around it
wkt_polygon = "POLYGON((11.575 48.137, 11.576 48.137, 11.576 48.138, 11.575 48.138, 11.575 48.137))"

data = {
    "alkis_id": "MOCK-MUC-001",
    "geom": wkt_polygon, # Supabase needs PostGIS raw or text insert usually works if setup. 
    # Actually, the Edge Function or standard insert might fail on WKT if column is Geometry type and we use REST.
    # But supabase-js often helps. Let's try raw string.
    # If this fails, we might need a custom RPC or use the worker's logic.
    "properties": {
        "land_use": "Sondergebiet Solar",
        "area_sqm": 4500,
        "owner": "Landeshauptstadt München",
        "municipality": "München Transparent"  # Match OParl Name for Smart Jump
    }
}

# NOTE: Direct insert of WKT into Geometry column via JS/Python Client often fails without a converter (like ST_GeomFromText).
# I will use a raw SQL call via rpc or just try text and hope PostGIS casts it.
# Actually, the best way for Supabase is often GeoJSON or just text if the caster is implicit.
# Let's try inserting via RPC or standard helper. 
# Worker used `db_client.table("geo_parcels").insert(parcel_data).execute()`
# But worker converted WKT? No, checking worker code... 
# Worker code used `wkt` string. Let's assume it works.

print("Upserting Munich Parcel...")
try:
    res = client.table("geo_parcels").upsert(data, on_conflict="alkis_id").execute()
    print("Success:", res)
except Exception as e:
    print("Failed:", e)
