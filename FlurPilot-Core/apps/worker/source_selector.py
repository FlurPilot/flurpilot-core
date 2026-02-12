
import logging
import os
from typing import Optional, Any
from urllib.parse import urlparse

# Connectors
from connectors.oparl import OParlClient
from connectors.sessionnet import SessionNetClient
from connectors.search_index import SearchIndexClient as GoogleSearchClient
from connectors.brave_search import BraveSearchClient
from connectors.bing_search import BingSearchClient

logger = logging.getLogger("SourceSelector")

class SourceSelector:
    """
    Implements F-01 Hybrid Strategy.
    Routes a profile to the correct Acquisition Engine.
    
    Tier 1: OParl (Gold Standard) - Structured API access
    Tier 1.5: RIS Scraper (SessionNet/Somacos) - HTML scraping for known systems
    Tier 2: Search APIs - Brave Search (Primary) or Google Custom Search (Fallback)
    
    ⚠️  NOTE: Bing Search API wurde am 11.08.2025 eingestellt und ist nicht mehr verfügbar.
    """
    
    def __init__(self):
        # Initialize Tier 2 search clients with priority: Brave > Google
        self.brave_client = None
        self.google_client = None
        
        # Try to initialize Brave (preferred - replaces deprecated Bing)
        if os.getenv("BRAVE_API_KEY"):
            try:
                self.brave_client = BraveSearchClient()
                logger.info("✅ Brave Search API initialized (Primary Tier 2)")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Brave Search: {e}")
        
        # Fallback to Google if Brave not available
        if not self.brave_client and os.getenv("GOOGLE_API_KEY"):
            try:
                self.google_client = GoogleSearchClient()
                logger.info("✅ Google Custom Search API initialized (Fallback Tier 2)")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Google Search: {e}")
    
    @staticmethod
    def select_client(profile: dict, fetcher: Any) -> Any:
        """
        Determines the best client for the given profile.
        Returns an instance of the client (or None if no match).
        
        DEPRECATED: Use select_acquisition_engine() instead for full Tier 2 support.
        """
        selector = SourceSelector()
        return selector.select_acquisition_engine(profile, fetcher)
    
    def select_acquisition_engine(self, profile: dict, fetcher: Any) -> Any:
        """
        Determines the best acquisition engine for the given profile.
        
        Priority:
        1. Tier 1: OParl API
        2. Tier 1.5: RIS Scraper (SessionNet/Somacos)
        3. Tier 2: Search API (Brave or Google)
        
        Args:
            profile: Municipality profile with metadata
            fetcher: ResilientFetcher instance for HTTP requests
            
        Returns:
            Client instance or None if no suitable engine found
        """
        name = profile.get("name", "Unknown")
        oparl_url = profile.get("oparl_url")
        url = profile.get("url")
        
        # 1. Tier 1: OParl (Gold Standard)
        # If we have an explicit OParl URL, use it.
        if oparl_url:
            logger.info(f"🥇 Selected Engine: OParl (Tier 1) for {name}")
            return OParlClient(oparl_url, fetcher=fetcher)
            
        # 2. Tier 1.5: RIS Scraper (SessionNet / Somacos)
        # Heuristic: URL contains typical RIS patterns
        if url:
            if "sessionnet" in url.lower() or "/bi/" in url.lower() or "ris" in url.lower():
                logger.info(f"🥈 Selected Engine: SessionNet (Tier 1.5) for {name}")
                # SessionNetClient currently doesn't accept fetcher, needs refactor or wrapper
                # For now we instantiate it directly, but ideally it should use the fetcher.
                # TODO: Upgrade SessionNetClient to use ResilientFetcher
                return SessionNetClient(url)

        # 3. Tier 2: Search API (Brave preferred, Google fallback)
        # If no direct interface, use Search API to discover documents
        if self.brave_client:
            logger.info(f"🔍 Selected Engine: Brave Search (Tier 2) for {name}")
            return self.brave_client
        elif self.google_client:
            logger.info(f"🔍 Selected Engine: Google Custom Search (Tier 2) for {name}")
            return self.google_client
        else:
            logger.warning(f"⚠️ No Tier 2 search engine available for {name}")
            logger.warning("   Set BRAVE_API_KEY or GOOGLE_API_KEY environment variable")
            logger.warning("   ⚠️  NOTE: Bing Search API wurde am 11.08.2025 eingestellt!")
            return None
    
    def get_search_client(self) -> Optional[Any]:
        """
        Returns the preferred search client (Brave or Google) for general use.
        
        Returns:
            BraveSearchClient or GoogleSearchClient instance, or None
        """
        return self.brave_client or self.google_client
    
    def is_search_available(self) -> bool:
        """
        Check if any Tier 2 search engine is available.
        
        Returns:
            True if Brave or Google search is configured
        """
        return self.brave_client is not None or self.google_client is not None
