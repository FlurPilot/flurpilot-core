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

def debug_search():
    query = "München"
    print(f"Searching for '{query}'...")

    # 1. Check Profiles
    print("\n--- Scout Profiles ---")
    res_prof = client.table("scout_profiles").select("name").ilike("name", f"%{query}%").execute()
    print(f"Profiles Found: {len(res_prof.data)}")
    for p in res_prof.data:
        print(p)

    # 2. Check Parcels (ALKIS ID)
    print("\n--- Parcels (ALKIS ID) ---")
    res_alkis = client.table("geo_parcels").select("alkis_id, properties").ilike("alkis_id", f"%{query}%").execute()
    print(f"By ID Found: {len(res_alkis.data)}")

    # 3. Check Parcels (Municipality Prop)
    # Note: supabase-py doesn't always support complex filter syntax easily in one go, 
    # but let's try the text search or a raw filter if possible, or just the property selector.
    # Using 'ilike' on a json arrow accessor might be tricky via the python client's simple methods 
    # if not explicitly supported, but let's try standard PostgREST syntax logic.
    # Actually, for debugging, let's just fetch the mock parcel and see what it has.
    
    print("\n--- Check Mock Parcel ---")
    res_mock = client.table("geo_parcels").select("*").eq("alkis_id", "MOCK-MUC-001").execute()
    for row in res_mock.data:
        print(row)

if __name__ == "__main__":
    debug_search()
