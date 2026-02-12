import os
import logging
from typing import List, Dict, Optional
from urllib.parse import quote
import httpx

logger = logging.getLogger("BraveSearchClient")

class BraveSearchClient:
    """
    Tier 2 Acquisition Engine using Brave Search API.
    
    Replaces deprecated Bing Search API (eingestellt am 11.08.2025).
    Provides stable, privacy-focused search for document discovery.
    
    Authentication: Requires BRAVE_API_KEY environment variable.
    
    Free Tier: 2,000 queries/month
    Paid Tier: $3 per 1,000 queries
    
    Sign up: https://brave.com/search/api/
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Brave Search Client.
        
        Args:
            api_key: Brave Search API key (or from BRAVE_API_KEY env)
        """
        self.api_key = api_key or os.getenv("BRAVE_API_KEY")
        self.endpoint = "https://api.search.brave.com/res/v1/web/search"
        
        if not self.api_key:
            logger.warning("BRAVE_API_KEY not set. API calls will fail.")
        else:
            logger.info("✅ Brave Search API initialized")
    
    def generate_search_query(self, site_domain: str, keywords: List[str], 
                             filetype: Optional[str] = "pdf", 
                             year: Optional[int] = None) -> str:
        """
        Constructs a targeted search query for document discovery.
        
        Example: site:muenchen.de filetype:pdf "Bebauungsplan" "2024"
        
        Args:
            site_domain: Domain to search within (e.g., 'muenchen.de')
            keywords: List of keywords to search for
            filetype: File type filter (default: pdf)
            year: Optional year filter
            
        Returns:
            Search query string optimized for Brave
        """
        query_parts = [f"site:{site_domain}"]
        
        if filetype:
            query_parts.append(f"filetype:{filetype}")
        
        # Add keywords - use quotes for exact phrases
        for keyword in keywords:
            if " " in keyword:
                query_parts.append(f'"{keyword}"')
            else:
                query_parts.append(keyword)
        
        if year:
            query_parts.append(str(year))
            
        return " ".join(query_parts)
    
    def get_manual_search_link(self, query: str) -> str:
        """
        Returns a clickable URL for manual verification in browser.
        """
        encoded = quote(query)
        return f"https://search.brave.com/search?q={encoded}"
    
    async def search(self, query: str, count: int = 20, offset: int = 0) -> List[Dict]:
        """
        Execute search via Brave Search API.
        
        Args:
            query: Search query string
            count: Number of results to return (max 20)
            offset: Offset for pagination
            
        Returns:
            List of search results with title, url, description
            
        Raises:
            ValueError: If API key is not configured
            httpx.HTTPError: If API request fails
        """
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY not configured. Set environment variable or pass to constructor.")
        
        # Prepare request
        headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json"
        }
        
        params = {
            "q": query,
            "count": min(count, 20),  # Brave allows max 20 per request
            "offset": offset
        }
        
        logger.info(f"Searching Brave: {query[:50]}...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.endpoint,
                    headers=headers,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Extract web results
                web_results = data.get("web", {}).get("results", [])
                
                results = []
                for item in web_results:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("description", ""),
                        "date": item.get("age", ""),
                        "display_url": item.get("profile", {}).get("name", "")
                    })
                
                logger.info(f"Found {len(results)} results")
                return results
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Brave API error: {e.response.status_code} - {e.response.text}")
                if e.response.status_code == 401:
                    raise ValueError("Invalid BRAVE_API_KEY")
                elif e.response.status_code == 429:
                    raise ValueError("Brave API rate limit exceeded")
                elif e.response.status_code == 403:
                    raise ValueError("Brave API quota exceeded or access denied")
                raise
            except httpx.RequestError as e:
                logger.error(f"Request error: {e}")
                raise
    
    async def search_pdfs(self, site_domain: str, keywords: List[str], 
                         year: Optional[int] = None, max_results: int = 20) -> List[Dict]:
        """
        Convenience method for searching PDFs on a specific site.
        
        Args:
            site_domain: Domain to search (e.g., 'stadt-muenster.de')
            keywords: Keywords to search for
            year: Optional year filter
            max_results: Maximum number of results
            
        Returns:
            List of PDF documents found
        """
        query = self.generate_search_query(site_domain, keywords, filetype="pdf", year=year)
        return await self.search(query, count=max_results)
    
    async def search_documents(self, site_domain: str, keywords: List[str],
                              filetypes: List[str] = None, 
                              year: Optional[int] = None,
                              max_results: int = 20) -> Dict[str, List[Dict]]:
        """
        Search for multiple document types at once.
        
        Args:
            site_domain: Domain to search
            keywords: Keywords to search for
            filetypes: List of file types (default: ['pdf', 'docx', 'doc'])
            year: Optional year filter
            max_results: Max results per file type
            
        Returns:
            Dict mapping filetype to list of results
        """
        if filetypes is None:
            filetypes = ["pdf", "docx", "doc"]
        
        all_results = {}
        
        for filetype in filetypes:
            query = self.generate_search_query(site_domain, keywords, filetype=filetype, year=year)
            try:
                results = await self.search(query, count=max_results)
                all_results[filetype] = results
            except Exception as e:
                logger.error(f"Error searching for {filetype}: {e}")
                all_results[filetype] = []
        
        return all_results


# Example Usage
if __name__ == "__main__":
    import asyncio
    
    async def test():
        # Initialize client (uses BRAVE_API_KEY from env)
        client = BraveSearchClient()
        
        # Generate search query
        query = client.generate_search_query(
            "muenchen.de", 
            ["Bebauungsplan", "Aufstellungsbeschluss"],
            year=2024
        )
        print(f"Search Query: {query}")
        print(f"Manual Link: {client.get_manual_search_link(query)}")
        
        # Execute search (requires API key)
        if os.getenv("BRAVE_API_KEY"):
            try:
                results = await client.search(query, count=5)
                print(f"\n--- Results ({len(results)}) ---")
                for i, r in enumerate(results, 1):
                    print(f"{i}. {r['title']}")
                    print(f"   URL: {r['url']}")
                    print()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("\n⚠️  BRAVE_API_KEY not set. Skipping API call.")
    
    asyncio.run(test())
