import asyncio
import os
import sys
import logging
from dotenv import load_dotenv
from supabase import create_client

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bavarian_bypass import BavarianBypass

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BypassRunner")

async def run():
    # Load Environment
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
    
    url = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        logger.error("Missing Supabase Credentials")
        return

    supabase = create_client(url, key)
    

    # Initialize Fetcher
    from fetcher import ResilientFetcher
    fetcher = ResilientFetcher()
    
    engine = BavarianBypass(supabase, fetcher)
    
    # Test Coordinates (Rural area near Munich to simulate field)
    # 48.200, 11.600
    lat = 48.200
    lon = 11.600
    
    logger.info(f"Triggering Virtual Parcel Engine for {lat}, {lon}...")
    
    try:
        parcel_id = await engine.compute_virtual_parcel(lat, lon)
        if parcel_id:
            logger.info(f"SUCCESS: Created Parcel ID: {parcel_id}")
        else:
            logger.warning("FAILED: No parcel created.")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error: {e}")
    finally:
        await fetcher.close()


if __name__ == "__main__":
    asyncio.run(run())
