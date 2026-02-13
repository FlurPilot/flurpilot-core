
import asyncio
import logging
import os
import sys
import time
from urllib.parse import urlparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from supabase import create_client, Client

# Custom Modules
from connectors.oparl import OParlClient
from fetcher import ResilientFetcher
from job_queue import JobQueue
from privacy import PrivacyEngine
from bavarian_bypass import BavarianBypass
from source_selector import SourceSelector
from audit_logger import AuditLogger

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WorkerCluster")

# Load Environment
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Must be Service Role for Worker

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("Missing Supabase Credentials. Please check .env")
    sys.exit(1)

# Initialize Global Clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
fetcher = ResilientFetcher()
worker_id = os.getenv("WORKER_ID", f"worker_{int(time.time())}")
queue = JobQueue(supabase, worker_id)
privacy_engine = PrivacyEngine()
virtual_parcel_engine = BavarianBypass(supabase, fetcher)
audit = AuditLogger(supabase)

# --- CONFIG ---
KEYWORDS = ["Solar", "Photovoltaik", "Freiflächen", "Sondergebiet", "Aufstellungsbeschluss"]

async def process_crawl_profile(profile):
    """
    Executes the crawling logic for a single profile (City).
    """
    logger.info(f"Processing Profile: {profile.get('name')} ({profile.get('url')})")
    
    url = profile.get("url") or profile.get("oparl_url")
    if not url: 
        logger.warning(f"Profile {profile.get('name')} has no URL.")
        return

    # TIER 1: Hybrid Engine Selection
    # The Selector chooses OParl, SessionNet, or Tier 2 based on profile data
    client = SourceSelector.select_client(profile, fetcher)
    
    if not client:
        logger.warning(f"No suitable client found for {profile.get('name')}")
        return

    try:
        # Unified Interface Check
        # Ideally all clients should share a base interface (fetch_recent_papers)
        # For now, we check type or duck-type
        
        # OParl Specific Path
        if isinstance(client, OParlClient):
            sys_info = await client.get_system_info()
            if not sys_info:
                logger.warning(f"OParl System Unreachable: {url}")
                return

            # Fetch Papers
            papers = await client.fetch_recent_papers(days=7)
            logger.info(f"Found {len(papers)} papers for {profile.get('name')}")

            # Papers fetched. Proceed to processing loop below.
            pass 

        # SessionNet / Tier 2 Placeholder
        else:
             logger.info(f"Client {type(client).__name__} not yet fully integrated in main loop.")
             return

        # --- REUSED PROCESSING LOGIC (Indented for OParl only right now) ---
        # NOTE: To make this truly polymorphic, we'd need a common 'fetch_papers' return type.
        # OParl returns dicts with 'id', 'name'. SessionNet returns similar.
        # Let's assume OParl for now and Refactor loop later or just copy logic.
        
        # Actually, let's just restore the OParl logic but acting on 'client' variable
        # assuming it is OParlClient.
        
        # The Loop:
        for paper in papers:
            title = paper.get("name", "Untitled")
            
            # Simple Keyword Check (Pre-Filter)
            is_relevant = any(k.lower() in title.lower() for k in KEYWORDS)
            
            if is_relevant:
                score = 80 # Base score for Title Match
                
                # F-01: Deep Analysis (Download PDF)
                # Only OParlClient has fetch_full_text right now
                if hasattr(client, 'fetch_full_text'):
                    logger.info(f"   > [DEEP DIVE] Downloading PDF for: {title[:30]}...")
                    paper = await client.fetch_full_text(paper)
                
                summary_text = f"Detected keywords in title: {title}"
                if paper.get('full_text'):
                    summary_text = paper.get('full_text')[:500] + "..."
                    # Check text relevance again? (Optional)
                    score = 90
                
                # F-03: Privacy Pipeline
                title_result = privacy_engine.clean_text(title)
                summary_result = privacy_engine.clean_text(summary_text)

                # Audit: Log PII redactions
                total_redactions = title_result.redaction_count + summary_result.redaction_count
                if total_redactions > 0:
                    try:
                        audit.log_action(
                            action="pii_redaction",
                            resource=paper.get("id", "unknown"),
                            actor_id=worker_id,
                            details={
                                "title_redactions": title_result.redaction_count,
                                "summary_redactions": summary_result.redaction_count,
                                "entity_types": list(set(
                                    e.entity_type for e in
                                    title_result.redacted_entities + summary_result.redacted_entities
                                )),
                            }
                        )
                    except Exception as audit_err:
                        logger.warning(f"Audit log failed (non-blocking): {audit_err}")

                doc = {
                    "external_id": paper.get("id"), 
                    "title": title_result.sanitized_text,
                    "doc_type": paper.get("type", "unknown").split("/")[-1],
                    "published_date": paper.get("date"),
                    "url": paper.get("id"),
                    "region_id": profile.get("id"),
                    "relevant": True,
                    "risk_score": score,
                    "summary": summary_result.sanitized_text,
                    "content_hash": paper.get("content_hash")
                }
                
                # Dedup Check: Content Hash
                content_hash = paper.get("content_hash")
                if content_hash:
                    # Check if this hash already exists (Global Dedup)
                    # We only care if it's the SAME content.
                    existing_hash = supabase.table("evidence_docs").select("id").eq("content_hash", content_hash).execute()
                    if existing_hash.data:
                        logger.info(f"   > [DEDUP] Skipping {title[:20]}... (Hash match)")
                        continue

                # Upsert Evidence
                try:
                    supabase.table("evidence_docs").upsert(doc, on_conflict="external_id").execute()
                    logger.info(f"   > Indexed Evidence: {title_result.sanitized_text[:50]}...")
                except Exception as db_err:
                    logger.error(f"DB Error: {db_err}")

    except Exception as e:
        logger.error(f"Error crawling {profile.get('name')}: {e}")
        raise e # Re-raise to trigger job failure/retry
    finally:
        if hasattr(client, 'close'):
            await client.close()

    # Create dummy Geometry (F-02) if needed
    # (Leaving this out for now to focus on F-01)
    
    # Update last_scout_at
    supabase.table("scout_profiles").update({"last_scout_at": "now()"}).eq("id", profile["id"]).execute()


async def process_job(job):
    """
    Dispatcher for job types.
    """
    job_type = job.get('type')
    payload = job.get('payload')
    
    if job_type == 'crawl_profile':
        await process_crawl_profile(payload)
    elif job_type == 'calculate_parcel':
        # F-02 Payload: {lat: float, lon: float}
        lat = payload.get('lat')
        lon = payload.get('lon')
        if lat and lon:
            await virtual_parcel_engine.compute_virtual_parcel(lat, lon)
        else:
            logger.warning("Job payload missing lat/lon")
    else:
        logger.warning(f"Unknown Job Type: {job_type}")


async def run_producer():
    """
    Scans for stale profiles and pushes them to the queue.
    """
    logger.info("Producer: Scanning for stale profiles...")
    
    # 1. Fetch Active Profiles
    res = supabase.table("scout_profiles").select("*").eq("active", True).execute()
    profiles = res.data or []
    
    queued_count = 0
    for p in profiles:
        # 2. Check Frequency
        last_scout = p.get('last_scout_at')
        should_queue = False
        
        if not last_scout:
            should_queue = True # Never scouted
        else:
            # Parse and check if > 24h old
            try:
                # Assuming ISO format. Simplified check: 
                # For demo purposes, we might just queue if not currently running?
                # Let's check DB for pending jobs to avoid duplicates
                pass
            except:
                pass
        
        # 3. Dedup Check (Don't queue if already in pipe)
        # Check if there is a pending or processing job for this profile
        # using @> JSON containment operator
        existing = supabase.table("crawler_jobs") \
            .select("id") \
            .in_("status", ["pending", "processing"]) \
            .contains("payload", {"id": p["id"]}) \
            .execute()
            
        if not existing.data:
            # Domain Lock Preparation
            domain = None
            p_url = p.get('url') or p.get('oparl_url')
            if p_url:
                try:
                    domain = urlparse(p_url).netloc
                except:
                    pass
            
            # PUSH
            if queue.push("crawl_profile", p, domain=domain):
                queued_count += 1
        
    if queued_count > 0:
        logger.info(f"Producer: Queued {queued_count} new profiles.")


async def worker_loop():
    logger.info(f"Worker Cluster {worker_id} Starting...")
    
    # Force Producer run on start
    await run_producer()
    last_producer_run = time.time()
    
    while True:
        # 1. Producer Tick (every 60s)
        if time.time() - last_producer_run > 60:
            try:
                await run_producer()
            except Exception as e:
                logger.error(f"Producer Error: {e}")
            last_producer_run = time.time()
            
        # 2. Consumer Tick
        try:
            job = queue.fetch_next()
            if job:
                start_time = time.time()
                await process_job(job)
                duration = time.time() - start_time
                
                queue.complete(job['id'])
                logger.info(f"Job {job['id']} finished in {duration:.2f}s")
            else:
                # Idle
                await asyncio.sleep(2)
                
        except Exception as e:
            logger.error(f"Critical Worker Loop Error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(worker_loop())
    except KeyboardInterrupt:
        logger.info("Worker Stopped.")
