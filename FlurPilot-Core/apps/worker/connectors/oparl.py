import httpx
import asyncio
from typing import Optional, Dict, Any, List
import sys
import os
# Allow importing from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pdf_processor import PDFProcessor

class OParlClient:
    """
    A robust client for interacting with OParl APIs (v1.0/1.1).
    Implements the Hybrid Acquisition Strategy (Tier 1).
    """
    
    def __init__(self, base_url: str, fetcher):
        self.base_url = base_url.rstrip('/')
        self.fetcher = fetcher
        self.pdf_processor = PDFProcessor(fetcher=fetcher)

    async def get_system_info(self) -> Optional[Dict[str, Any]]:
        """
        Handshake: Fetches the OParl System Entry Point.
        Verifies if the API is reachable and OParl compliant.
        """
        try:
            print(f"[OParl] Connecting to {self.base_url}...")
            response = await self.fetcher.get(self.base_url)
            
            if response and response.status_code == 200:
                data = response.json()
                print(f"[OParl] Connected! System Name: {data.get('name', 'Unknown')}")
                return data
            else:
                print(f"[OParl] Error: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"[OParl] Connection Failed: {e}")
            return None

    async def fetch_recent_papers(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Fetches 'Papers' (Drucksachen) modified in the last X days.
        Traverses: System -> Body -> Papers
        """
        try:
            # 1. Get System Info to find Body
            system_info = await self.get_system_info()
            if not system_info:
                return []
            
            # 2. Extract Body URL (Taking the first body if list, or direct link)
            bodies = system_info.get('body', [])
            if not bodies:
                print("[OParl] No Body URL found in System Info.")
                return []
            
            # Handle list of URLs or list of Objects
            body_url = bodies[0] if isinstance(bodies, list) else bodies
            if isinstance(body_url, dict):
                body_url = body_url.get('id')

            print(f"[OParl] Fetching Body: {body_url}")
            print(f"[OParl] Fetching Body: {body_url}")
            body_res = await self.fetcher.get(body_url)
            if not body_res or body_res.status_code != 200:
                print(f"[OParl] Failed to fetch Body: {body_res.status_code if body_res else 'No Response'}")
                return []
            
            raw_body = body_res.json()
            # Handle OParl List Wrapper
            if 'data' in raw_body:
                body_data = raw_body['data']
                # If it's a list (which it likely is for /body endpoint), take first
                if isinstance(body_data, list):
                    if not body_data: 
                        print("[OParl] Body list is empty.")
                        return []
                    body_data = body_data[0]
            else:
                body_data = raw_body

            print(f"[DEBUG] Body Info: {body_data.get('name', 'Unknown')}")
            
            # 3. Get Papers URL
            papers_url = body_data.get('paper')
            if not papers_url:
                print("[OParl] No 'paper' endpoint in Body.")
                return []
            
            # 4. Fetch Papers (with limit/filter)
            # Standard OParl supports 'modified_since' or just pagination.
            # For this MVP we just fetch the list (often paginated).
            print(f"[OParl] Fetching Papers from: {papers_url}")
            
            # We append query params manually or use params dict
            # We append query params manually or use params dict
            papers_res = await self.fetcher.get(papers_url) 
            
            if not papers_res or papers_res.status_code != 200:
                print(f"[OParl] Failed to fetch Papers: {papers_res.status_code if papers_res else 'No Response'}")
                return []
            
            papers_data = papers_res.json()
            
            # OParl lists are often wrapped in { "data": [...] } or are direct lists
            items = papers_data.get('data', []) if isinstance(papers_data, dict) else papers_data
            
            print(f"[OParl] Found {len(items)} papers.")
            return items

        except Exception as e:
            print(f"[OParl] Fetch Error: {e}")
            return []

    async def fetch_full_text(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriches a paper object with full text and hash from its PDF.
        Finds the primary file (accessUrl or downloadUrl).
        """
        # Finds file list
        files = paper.get('file', [])
        if not files:
            files = paper.get('auxiliaryFile', [])
            
        if not files:
            return paper

        # Handle list or single obj
        target_file = files[0] if isinstance(files, list) else files
        if isinstance(target_file, str):
            # If it's just a URL string (rare in Oparl but possible)
            file_url = target_file
        else:
            file_url = target_file.get('accessUrl') or target_file.get('downloadUrl')

        if file_url:
            print(f"[OParl] Processing PDF: {file_url}")
            content_hash, _, text = await self.pdf_processor.process_url(file_url)
            
            if text:
                paper['full_text'] = text
                paper['content_hash'] = content_hash
                print(f"[OParl] Added {len(text)} chars of text.")
            
        return paper

    async def close(self):
        # We don't close the shared fetcher here
        pass
