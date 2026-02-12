
import os
import logging
from typing import Optional, Dict, Any
from supabase import create_client, Client

logger = logging.getLogger("AuditLogger")

class AuditLogger:
    """
    Client-side wrapper for the Immutable Audit Log.
    Just inserts data; the DB Trigger handles the hashing/chaining.
    """
    def __init__(self, supabase_client: Client):
        self.db = supabase_client

    def log_action(self, action: str, resource: str, actor_id: Optional[str] = None, details: Dict[str, Any] = None):
        """
        Logs an action to the audit_logs table.
        """
        if details is None:
            details = {}
            
        payload = {
            "action": action,
            "resource": resource,
            "actor_id": actor_id,
            "details": details
        }
        
        try:
            # We don't verify return here, just fire and forget or check error
            # If we want the ID back, we use .execute() and check data
            data, count = self.db.table("audit_logs").insert(payload).execute()
            
            # For debug/verification, we might return the new entry
            if data and len(data[1]) > 0:
                 entry = data[1][0]
                 logger.info(f"Audit Log Created: {entry.get('id')} | Hash: {entry.get('curr_hash')[:8]}...")
                 return entry
                 
        except Exception as e:
            logger.error(f"Failed to write Audit Log: {e}")
            # Fail Closed? 
            # Lastenheft say "Rechtssicherheit". If logging fails, should action fail?
            # Ideally yes for critical actions.
            raise e
