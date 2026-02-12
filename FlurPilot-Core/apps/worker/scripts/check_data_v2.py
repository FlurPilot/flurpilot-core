import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check():
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
    
    url = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        print("Missing Supabase Credentials")
        return

    supabase = create_client(url, key)
    
    try:
        # Simple select
        print("Querying virtual_parcels...")
        resp = supabase.table("virtual_parcels").select("*").limit(1).execute()
        print(f"Bavarian Bypass Results: {len(resp.data)} rows found.")
        if resp.data:
            print(f"First Row ID: {resp.data[0].get('id')}")

    except Exception as e:
        print("ERROR DETAILS:")
        if hasattr(e, 'message'): print(f"Message: {e.message}")
        if hasattr(e, 'code'): print(f"Code: {e.code}")
        if hasattr(e, 'details'): print(f"Details: {e.details}")
        print(f"Full Error: {e}")

if __name__ == "__main__":
    check()
