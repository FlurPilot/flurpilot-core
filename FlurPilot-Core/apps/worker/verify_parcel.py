
import os
import time
from supabase import create_client
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Verifying Virtual Parcel Creation...")

# Query the latest parcel
try:
    response = client.table("virtual_parcels").select("*").order("last_calculated_at", desc=True).limit(1).execute()
    data = response.data
    
    if not data:
        print("❌ No virtual parcels found.")
        exit(1)
        
    parcel = data[0]
    print(f"✅ Found Parcel: {parcel['id']}")
    print(f"   Source Field: {parcel['source_field_id']}")
    print(f"   Net Area: {parcel['net_area_m2']} m²")
    
    if parcel['net_area_m2'] > 0:
        print("✅ SUCCESS: Area is positive.")
    else:
        print("⚠️ WARNING: Area is 0 or null.")
        
except Exception as e:
    print(f"❌ Error: {e}")
