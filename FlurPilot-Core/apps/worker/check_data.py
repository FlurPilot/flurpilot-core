import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Missing credentials")
    exit(1)

client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_data():
    print("Checking geo_parcels...")
    res = client.table("geo_parcels").select("*").limit(5).execute()
    for row in res.data:
        print(f"ID: {row['id']}")
        print(f"ALKIS: {row['alkis_id']}")
        print(f"Props: {row['properties']}")
        print("-" * 20)
        
    print("\nChecking scout_profiles (top 5)...")
    res2 = client.table("scout_profiles").select("name, active").limit(5).execute()
    for row in res2.data:
        print(row)

if __name__ == "__main__":
    check_data()
