
import os
from supabase import create_client
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Clearing Crawler Jobs...")
try:
    driver = client.table("crawler_jobs").delete().gt("created_at", "2000-01-01T00:00:00Z").execute()
    print("Jobs Cleared.")
except Exception as e:
    print(f"Error: {e}")
