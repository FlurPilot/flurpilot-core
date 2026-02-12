
import asyncio
import logging
import time
import random
import os
from typing import Dict, Optional, Any

from urllib.parse import urlparse
import httpx
import urllib.robotparser
from urllib.parse import urlparse, urljoin


logger = logging.getLogger("ResilientFetcher")

# Common User Agents (Modern, Desktop)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

class CircuitBreaker:
    """
    Tracks failures for a domain.
    State: CLOSED (Normal) -> OPEN (Failures > threshold) -> HALF-OPEN (Test)
    """
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED" 

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit Breaker OPENED. Too many failures.")

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def can_request(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
                return True # Allow one test request
            return False
        if self.state == "HALF-OPEN":
            return False # Already one test in progress (simplification)
        return True

class ResilientFetcher:
    """
    HTTP Client with:
    - User-Agent Rotation
    - Circuit Breaker per Domain
    - Rate Limiting (Token Bucket - Conceptual)
    """
    def __init__(self):
        self.breakers: Dict[str, CircuitBreaker] = {}
        self.robots_parsers: Dict[str, urllib.robotparser.RobotFileParser] = {}
        self.robots_checked: Dict[str, float] = {} # Timestamp of last check
        self.last_request_time: Dict[str, float] = {} # For Crawl-Delay
        
        # Proxy Configuration
        proxies = None
        http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
        https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
        
        if http_proxy or https_proxy:
            proxies = {
                "http://": http_proxy,
                "https://": https_proxy
            }
            logger.info(f"Using Proxies: {proxies}")
            
        self.client = httpx.AsyncClient(
            timeout=30.0, 
            follow_redirects=True,
            trust_env=True # Explicitly enable env var support
        )

    async def _check_robots(self, url: str) -> bool:
        """
        Checks if the URL is allowed by robots.txt.
        Async fetch, synchronous parse.
        """
        domain = urlparse(url).netloc
        scheme = urlparse(url).scheme
        if not domain or not scheme:
             return True # Can't check
             
        robots_url = f"{scheme}://{domain}/robots.txt"
        
        # Check Cache (TTL 24h)
        now = time.time()
        if domain in self.robots_checked:
            if now - self.robots_checked[domain] < 86400:
                parser = self.robots_parsers.get(domain)
                if parser:
                    return parser.can_fetch("*", url)
                return True # Default allow if parser failed previously but cached?
        
        # Fetch robots.txt
        logger.info(f"Checking robots.txt for {domain}...")
        try:
            # Create Parser
            parser = urllib.robotparser.RobotFileParser()
            parser.set_url(robots_url)
            
            # Fetch content manually to keep it async
            # Use a separate client or the same one but careful with recursion?
            # Safe to use self.client.get because _check_robots is internal and doesn't call .get() recursively if we are careful
            # But .get() calls _check_robots! Infinite Loop Risk.
            # Fix: Use self.client.get directly, bypassing self.get() wrapper.
            
            resp = await self.client.get(robots_url, timeout=10.0)
            
            if resp.status_code == 200:
                # Provide lines to parser
                lines = resp.text.splitlines()
                parser.parse(lines)
                self.robots_parsers[domain] = parser
            elif resp.status_code in [401, 403]:
                # Strict: If robots.txt is forbidden, assume disallow all? 
                # Standard says: If 403, do not crawl.
                logger.warning(f"robots.txt Forbidden for {domain}. Blocking.")
                self.robots_checked[domain] = now
                self.robots_parsers[domain] = None # Marker for block
                return False
            else:
                # 404 etc -> Allow all
                parser.allow_all = True
                self.robots_parsers[domain] = parser

            self.robots_checked[domain] = now
            return parser.can_fetch("*", url)
            
        except Exception as e:
            logger.warning(f"Failed to fetch robots.txt for {domain}: {e}. Defaulting to Allow.")
            return True



    def _get_breaker(self, url: str) -> CircuitBreaker:
        domain = urlparse(url).netloc
        if domain not in self.breakers:
            self.breakers[domain] = CircuitBreaker()
        return self.breakers[domain]

    def _get_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
        }

    async def get(self, url: str, **kwargs) -> Optional[httpx.Response]:
        breaker = self._get_breaker(url)
        if not breaker.can_request():
            logger.warning(f"Circuit OPEN for {url}. Skipping request.")
            return None

        # Robots.txt Check
        # Optimization: Only check for HTML/API calls, maybe skip for PDF assets if we extracted them from allowed page?
        # But safest is to check.
        if not await self._check_robots(url):
            logger.warning(f"Blocked by robots.txt: {url}")
            return None

        # Crawl-Delay Implementation
        # We need to check if there is a delay set for this domain
        domain = urlparse(url).netloc
        parser = self.robots_parsers.get(domain)
        if parser:
            crawl_delay = parser.crawl_delay("*")
            if crawl_delay:
                last_req = self.last_request_time.get(domain, 0)
                elapsed = time.time() - last_req
                if elapsed < crawl_delay:
                    wait_time = crawl_delay - elapsed
                    if wait_time > 0:
                        logger.info(f"Respecting Crawl-Delay for {domain}: Sleeping {wait_time:.2f}s")
                        await asyncio.sleep(wait_time)
        
        self.last_request_time[domain] = time.time()

        try:
            # Merge headers
            headers = self._get_headers()
            if 'headers' in kwargs:
                headers.update(kwargs['headers'])
                del kwargs['headers']

            response = await self.client.get(url, headers=headers, **kwargs)
            
            if response.status_code >= 500:
                breaker.record_failure()
            elif response.status_code == 429: # Too Many Requests
                breaker.record_failure()
            else:
                breaker.record_success()
            
            return response

        except Exception as e:
            logger.error(f"Request failed {url}: {e}")
            breaker.record_failure()
            return None

    async def stream(self, method: str, url: str, **kwargs):
        """
        Wraps httpx stream context manager
        """
        breaker = self._get_breaker(url)
        # Note: We can't easily block here if it's a context manager generator without being async generator
        # For simplicity, we assume caller checks or we just let it fail if open
        # Real implementation would be more complex.
        
        # Merge headers
        headers = self._get_headers()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
            del kwargs['headers']

        return self.client.stream(method, url, headers=headers, **kwargs)

    async def close(self):
        await self.client.aclose()
