
import os
import time
from supabase import create_client
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Seeding Virtual Parcel Job (Bavaria)...")

# Sample Point in Bavaria (Near Munich)
payload = {
    "lat": 48.137,
    "lon": 11.575
}

job = {
    "type": "calculate_parcel",
    "payload": payload,
    "status": "pending",
    "worker_id": None
}

try:
    data = client.table("crawler_jobs").insert(job).execute()
    print(f"Job Queued: {data.data[0]['id']}")
except Exception as e:
    print(f"Error: {e}")
