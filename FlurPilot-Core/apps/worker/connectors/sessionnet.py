import httpx
from bs4 import BeautifulSoup
import urllib.parse
from typing import List, Dict, Any
from datetime import datetime

class SessionNetClient:
    """
    Tier 1.5 Acquisition Engine.
    Scrapes 'SessionNet' (Somacos) RIS installations directly via HTML.
    Target: generic /bi/ URLs (Bürgerinformation).
    """

    def __init__(self, base_url: str):
        # Base URL should be the root of the RIS, e.g., "https://ris.stadt.de/bi"
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
            "Upgrade-Insecure-Requests": "1"
        }

    async def check_connectivity(self) -> bool:
        """
        Verifies if the SessionNet instance is reachable.
        Tries to hit the main page.
        """
        try:
            async with httpx.AsyncClient(headers=self.headers, verify=False, follow_redirects=True, http2=True) as client:
                res = await client.get(self.base_url)
                print(f"[SessionNet] Connectivity Check: {res.status_code} | {res.url}")
                return res.status_code == 200
        except Exception as e:
            print(f"[SessionNet] Connectivity Error: {e}")
            return False

    async def search_documents(self, keywords: List[str], days: int = 30) -> List[Dict[str, Any]]:
        """
        Performs a search on /bi/si0090.php (Generic Search Mask)
        Note: This is highly dependent on the specific version of SessionNet.
        We attempt a standard POST request simulation.
        """
        
        search_url = f"{self.base_url}/si0090.php"
        
        # Join keywords for simple text search
        query = " ".join(keywords)
        
        # Standard SessionNet POST fields (reverse engineered)
        # 'smc_query': search text
        # 'smc_doctype': often 100 for everything or specific IDs
        data = {
            "smc_query": query,
            "smc_doctype": "100" # All doc types
        }
        
        results = []
        
        try:
            async with httpx.AsyncClient(headers=self.headers, verify=False) as client:
                # 1. GET to get cookies/session if needed (skip for now)
                
                # 2. POST Search
                res = await client.post(search_url, data=data, timeout=10.0)
                if res.status_code != 200:
                    print(f"[SessionNet] Search failed: {res.status_code}")
                    return []
                
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Parse Result Table
                # Usually class "smc_table" or similar grid
                # This is fragile and needs testing against a real target
                rows = soup.select("table.smc_table tr")
                if not rows:
                    rows = soup.select("table.rismain tr")
                
                for row in rows:
                    # Heuristic parsing
                    cells = row.find_all("td")
                    if len(cells) < 3:
                        continue
                        
                    # Extract Link
                    link_tag = row.find("a")
                    if not link_tag:
                        continue
                        
                    href = link_tag.get("href")
                    title = link_tag.get_text(strip=True)
                    
                    if not href or not title:
                        continue
                        
                    # Filter: Only keep "Solar" relevant titles here if we want pre-filtering
                    # But we trust the Worker's filter function later.
                    
                    full_url = urllib.parse.urljoin(self.base_url + "/", href)
                    
                    # Create pseudo-document
                    doc = {
                        "id": full_url,
                        "name": title,
                        "date": datetime.now().isoformat(), # SessionNet tables often lack clear dates in search view
                        "type": "https://oparl.org/schema/1.0/Paper"
                    }
                    results.append(doc)
                    
        except Exception as e:
            print(f"[SessionNet] Error: {e}")
            
        return results
