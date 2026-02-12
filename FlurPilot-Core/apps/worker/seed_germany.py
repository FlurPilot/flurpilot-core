import asyncio
import httpx
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    print("Missing Supabase credentials")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def seed_germany():
    # Official OParl Directory
    BASE_URL = "https://dev.oparl.org/api/endpoints"
    print(f"Fetching Germany-wide list from {BASE_URL}...")
    
    async with httpx.AsyncClient() as client:
        try:
            next_url = BASE_URL
            total_imported = 0
            
            while next_url:
                print(f"Fetching page: {next_url}")
                resp = await client.get(next_url)
                
                if resp.status_code != 200:
                    print(f"Failed to fetch: {resp.status_code}")
                    break
                
                payload = resp.json()
                items = payload.get('data', [])
                meta = payload.get('meta', {})
                
                print(f" - Found {len(items)} items on this page.")
                
                for ep in items:
                    sys_url = ep.get('url')
                    # 'title' seems to be the name in this API
                    name = ep.get('title') or ep.get('system', {}).get('name') or "Unknown Body"
                    
                    if not sys_url: 
                        continue
                        
                    # print(f"   Importing: {name}...")
                    
                    try:
                        data = {
                            "name": name,
                            "oparl_url": sys_url,
                            "active": True
                        }
                        
                        exists = supabase.table("scout_profiles").select("id").eq("oparl_url", sys_url).execute()
                        if not exists.data:
                             supabase.table("scout_profiles").insert(data).execute()
                             total_imported += 1
                             print(f"   [+] Added {name}")
                        else:
                            # print(f"   [.] Skipped {name}")
                            pass
                            
                    except Exception as e:
                        print(f"   [!] Error importing {name}: {e}")
                
                # Next Page
                next_url = meta.get('next')
            
            print(f"\n✅ SUCCESSFULLY IMPORTED {total_imported} NEW MUNICIPALITIES.")
            print("Restart the worker to stat harvesting Germany-wide.")
            
        except Exception as e:
            print(f"Critical Error: {e}")

if __name__ == "__main__":
    asyncio.run(seed_germany())
