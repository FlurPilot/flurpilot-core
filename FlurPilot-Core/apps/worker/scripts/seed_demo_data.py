
import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
    sys.exit(1)

def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def seed_scout_profile(client: Client):
    print("Seeding 'Gemeinde Niederkrüchten' profile...")
    try:
        # Check if exists
        res = client.table("scout_profiles").select("id").eq("name", "Gemeinde Niederkrüchten").execute()
        if not res.data:
            client.table("scout_profiles").insert({
                "name": "Gemeinde Niederkrüchten",
                "oparl_url": "https://niederkruechten.ris-portal.de/oparl/v1/system", # Example URL, might need adjustment
                "active": True,
                "lat": 51.199,
                "lon": 6.220
            }).execute()
            print("✅ Profile Created.")
        else:
            print("⚠️ Profile already exists.")
    except Exception as e:
        print(f"❌ Failed to seed profile: {e}")

def seed_field_blocks(client: Client):
    print("Seeding Mock Field Blocks (Agricultural Land)...")
    # Coordinates around Niederkrüchten (Approx)
    # A large field block
    field_geom = {
        "type": "Polygon",
        "coordinates": [[
            [6.218, 51.198],
            [6.222, 51.198],
            [6.222, 51.196],
            [6.218, 51.196],
            [6.218, 51.198]
        ]]
    }
    
    try:
        # Check count (naive idempotent check)
        res = client.table("field_blocks").select("id", count="exact").execute()
        if res.count == 0:
            client.table("field_blocks").insert({
                "code": "FLIK-DE-NW-12345",
                "year": 2024,
                "geom": field_geom
            }).execute()
            print("✅ Field Block Created.")
        else:
             print("⚠️ Field Blocks already exist.")
    except Exception as e:
        print(f"❌ Failed to seed field block: {e}")

def seed_buildings(client: Client):
    print("Seeding Mock Building Footprints (Barns)...")
    # A small barn inside the field block above
    barn_geom = {
        "type": "Polygon",
        "coordinates": [[
            [6.220, 51.197],
            [6.2205, 51.197],
            [6.2205, 51.1965],
            [6.220, 51.1965],
            [6.220, 51.197]
        ]]
    }

    try:
        res = client.table("building_footprints").select("id", count="exact").execute()
        if res.count == 0:
            client.table("building_footprints").insert({
                "geom": barn_geom
            }).execute()
            print("✅ Building Footprint Created.")
        else:
             print("⚠️ Building Footprints already exist.")
    except Exception as e:
        print(f"❌ Failed to seed buildings: {e}")

if __name__ == "__main__":
    print("--- FlurPilot Seeder v0.1 ---")
    client = init_supabase()
    seed_scout_profile(client)
    seed_field_blocks(client)
    seed_buildings(client)
    print("--- Seeding Complete ---")
