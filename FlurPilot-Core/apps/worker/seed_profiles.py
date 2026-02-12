import asyncio
import os
from dotenv import load_dotenv
from supabase import create_client

script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Use Service Role Key if available (for write access), else Anon Key
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

async def seed():
    print("Seeding Scout Profiles (with Admin privileges)...")
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Check if table exists by trying to select
    try:
        response = client.table("scout_profiles").select("*", count="exact").execute()
        print(f"Table exists. Found {response.count} profiles.")
        
        # Insert Niederkruechten
        data = {
            "name": "Niederkrüchten",
            "ags": "05166016",
            "oparl_url": "https://sdnetrim.kdvz-frechen.de/rim4390/api/oparl/1.0/system",
            "active": True
        }
        
        # Upsert (requires logic handling in code or conflict constraint in DB)
        # Using simple checks for now
        existing = client.table("scout_profiles").select("*").eq("ags", "05166016").execute()
        if len(existing.data) == 0:
            client.table("scout_profiles").insert(data).execute()
            print("Inserted Niederkrüchten.")
        else:
            print("Niederkrüchten already exists.")

    except Exception as e:
        print(f"Error: {e}")
        print("Did you run the CREATE TABLE SQL in the Supabase Dashboard?")

if __name__ == "__main__":
    asyncio.run(seed())
