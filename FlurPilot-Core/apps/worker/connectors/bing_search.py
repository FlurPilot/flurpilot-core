"""
⚠️  DEPRECATED - DO NOT USE  ⚠️

Bing Search API wurde am 11. August 2025 eingestellt.
Dieses Modul existiert nur noch für Referenzzwecke.

Verwenden Sie stattdessen:
- connectors.brave_search (Empfohlen)
- connectors.search_index (Google Custom Search)

Migration:
    from connectors.brave_search import BraveSearchClient
    client = BraveSearchClient()
    
    # Oder
    from connectors.search_index import SearchIndexClient
    client = SearchIndexClient()
"""

import os
import logging
from typing import List, Dict, Optional
from urllib.parse import quote
import httpx

logger = logging.getLogger("BingSearchClient")

DEPRECATION_WARNING = """
⚠️  WARNUNG: Bing Search API wurde am 11. August 2025 eingestellt.
    Dieser Client funktioniert nicht mehr.
    
    Bitte migrieren Sie zu einer Alternative:
    - Brave Search API (empfohlen): connectors.brave_search
    - Google Custom Search: connectors.search_index
"""

class BingSearchClient:
    """
    ⚠️  DEPRECATED - API EINGESTELLT AM 11.08.2025  ⚠️
    
    Dieser Client wurde am 11. August 2025 obsolet, als Microsoft 
    die Bing Search APIs eingestellt hat.
    
    Siehe: https://learn.microsoft.com/en-us/bing/search-apis/overview
    
    Verwenden Sie stattdessen:
    - BraveSearchClient (empfohlen)
    - SearchIndexClient (Google)
    """
    
    def __init__(self, api_key: Optional[str] = None, custom_config_id: Optional[str] = None):
        logger.error(DEPRECATION_WARNING)
        raise RuntimeError(
            "Bing Search API wurde am 11. August 2025 eingestellt. "
            "Verwenden Sie BraveSearchClient oder SearchIndexClient."
        )
