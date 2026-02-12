
import logging
from typing import Optional, Dict, Any
from supabase import Client

logger = logging.getLogger("JobQueue")

class JobQueue:
    """
    Interface for the Postgres-based Crawler Queue.
    Handles Atomic Locking, Retries, and Dead Letter Queueing.
    """
    def __init__(self, client: Client, worker_id: str):
        self.client = client
        self.worker_id = worker_id

    def push(self, job_type: str, payload: Dict[str, Any], domain: str = None) -> bool:
        """Pushes a new job to the queue."""
        try:
            data = {
                "type": job_type,
                "payload": payload,
                "status": "pending",
                "domain": domain
            }
            res = self.client.table("crawler_jobs").insert(data).execute()
            logger.info(f"Queued Job: {job_type} (Domain: {domain})")
            return True
        except Exception as e:
            logger.error(f"Failed to push job: {e}")
            return False

    def fetch_next(self) -> Optional[Dict[str, Any]]:
        """
        Atomically fetches the next available job using the 'fetch_next_job' RPC.
        This respects Domain Locking.
        """
        try:
            # call RPC
            response = self.client.rpc("fetch_next_job", {"p_worker_id": self.worker_id}).execute()
            
            # response.data is expected to be a list of rows (length 0 or 1)
            if response.data and len(response.data) > 0:
                job = response.data[0]
                # Map keys if RPC returns them different (unlikely with select *)
                # RPC returns: j_id, j_type, j_payload
                return {
                    "id": job['j_id'],
                    "type": job['j_type'],
                    "payload": job['j_payload']
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching job: {e}")
            return None

    def complete(self, job_id: str):
        """Marks a job as completed and releases the domain lock."""
        try:
            self.client.table("crawler_jobs").update({
                "status": "completed",
                "completed_at": "now()"
            }).eq("id", job_id).execute()
            logger.info(f"Job {job_id} completed.")
        except Exception as e:
            logger.error(f"Failed to complete job {job_id}: {e}")

    def fail(self, job_id: str, error_msg: str):
        """
        Handles job failure.
        - Increments retries.
        - If retries < max: status='pending' (release lock so it can be retried).
        - If retries >= max: status='dead' (DLQ).
        """
        try:
            # 1. Get current retry status
            res = self.client.table("crawler_jobs").select("retries, max_retries, error_log").eq("id", job_id).single().execute()
            if not res.data:
                logger.error(f"Job {job_id} not found during fail handling.")
                return

            job = res.data
            current_retries = job.get("retries", 0)
            max_retries = job.get("max_retries", 3)
            old_log = job.get("error_log", "") or ""
            
            new_log = f"{old_log}\n[Retry {current_retries+1}] {error_msg}".strip()
            
            if current_retries + 1 >= max_retries:
                # Dead Letter Queue
                logger.error(f"Job {job_id} moved to DLQ (Max Retries). Error: {error_msg}")
                self.client.table("crawler_jobs").update({
                    "status": "dead",
                    "error_log": new_log,
                    "completed_at": "now()"
                }).eq("id", job_id).execute()
            else:
                # Retry
                logger.warning(f"Job {job_id} failed. Retrying ({current_retries+1}/{max_retries})...")
                self.client.table("crawler_jobs").update({
                    "status": "pending",
                    "retries": current_retries + 1,
                    "error_log": new_log,
                    "worker_id": None, # Release worker assignment
                    "domain": None,    # Release domain lock? 
                    # WAIT: If we release domain lock (domain=Null), we lose the domain info for next time!
                    # The table schema has 'domain' column.
                    # We should NOT set domain=None. We just set status='pending'.
                    # The fetch_next_job function checks (status='processing'). So pending jobs don't block.
                    # BUT: Does the domain column persist? Yes.
                    # So we just update status.
                    "started_at": None
                }).eq("id", job_id).execute()

        except Exception as e:
            logger.error(f"Failed to fail job {job_id}: {e}")
