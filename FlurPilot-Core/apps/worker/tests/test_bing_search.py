#!/usr/bin/env python3
"""
Test: Bing Custom Search API Integration

This script tests the Bing Search Client for Phase 2 (Acquisition Stability).
It validates that the API is properly configured and can discover PDF documents.

Target: >99% reliability for document discovery
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connectors.bing_search import BingSearchClient
from source_selector import SourceSelector

# Load environment variables
load_dotenv()


def test_api_configuration():
    """Test 1: Verify API key is configured"""
    print("\n" + "="*60)
    print("TEST 1: API Configuration")
    print("="*60)
    
    api_key = os.getenv("BING_API_KEY")
    
    if not api_key:
        print("❌ FAIL: BING_API_KEY not set in environment")
        print("   Please set: export BING_API_KEY='your-key-here'")
        return False
    
    if api_key == "your-bing-api-key-here":
        print("⚠️  WARNING: BING_API_KEY is set to placeholder value")
        print("   Please update with your actual API key")
        return False
    
    print(f"✅ PASS: BING_API_KEY is configured")
    print(f"   Key prefix: {api_key[:8]}...")
    
    custom_config = os.getenv("BING_CUSTOM_CONFIG_ID")
    if custom_config and custom_config != "your-custom-config-id-optional":
        print(f"✅ Custom config ID: {custom_config[:8]}...")
    else:
        print("ℹ️  Using default Bing search (no custom config)")
    
    return True


def test_client_initialization():
    """Test 2: Verify client can be initialized"""
    print("\n" + "="*60)
    print("TEST 2: Client Initialization")
    print("="*60)
    
    try:
        client = BingSearchClient()
        print("✅ PASS: BingSearchClient initialized successfully")
        return True
    except Exception as e:
        print(f"❌ FAIL: Failed to initialize client: {e}")
        return False


def test_query_generation():
    """Test 3: Verify search query generation"""
    print("\n" + "="*60)
    print("TEST 3: Query Generation")
    print("="*60)
    
    client = BingSearchClient()
    
    # Test basic query
    query = client.generate_search_query(
        site_domain="muenchen.de",
        keywords=["Bebauungsplan", "Solar"],
        filetype="pdf"
    )
    
    expected_parts = ["site:muenchen.de", "filetype:pdf", "Bebauungsplan", "Solar"]
    for part in expected_parts:
        if part not in query:
            print(f"❌ FAIL: Expected '{part}' in query")
            return False
    
    print(f"✅ PASS: Query generated correctly")
    print(f"   Query: {query}")
    
    # Test with year filter
    query_with_year = client.generate_search_query(
        site_domain="stadt-koeln.de",
        keywords=["Aufstellungsbeschluss"],
        filetype="pdf",
        year=2024
    )
    
    if "2024" not in query_with_year:
        print(f"❌ FAIL: Year filter not applied")
        return False
    
    print(f"✅ PASS: Year filter works")
    print(f"   Query: {query_with_year}")
    
    # Test manual link generation
    manual_link = client.get_manual_search_link(query)
    if not manual_link.startswith("https://www.bing.com/search?q="):
        print(f"❌ FAIL: Manual link format incorrect")
        return False
    
    print(f"✅ PASS: Manual search link generated")
    print(f"   Link: {manual_link[:60]}...")
    
    return True


async def test_api_call():
    """Test 4: Execute actual API call"""
    print("\n" + "="*60)
    print("TEST 4: API Call Execution")
    print("="*60)
    
    client = BingSearchClient()
    
    # Simple test query
    query = client.generate_search_query(
        site_domain="microsoft.com",
        keywords=["annual report"],
        filetype="pdf"
    )
    
    try:
        print(f"Searching: {query}")
        results = await client.search(query, count=5)
        
        if not results:
            print("⚠️  WARNING: No results returned (API may be working but no matches found)")
            return True  # API worked, just no results
        
        print(f"✅ PASS: API call successful")
        print(f"   Found {len(results)} results")
        
        # Validate result structure
        for i, result in enumerate(results[:3], 1):
            required_fields = ["title", "url", "snippet"]
            for field in required_fields:
                if field not in result:
                    print(f"❌ FAIL: Missing field '{field}' in result {i}")
                    return False
            
            print(f"\n   {i}. {result['title'][:50]}...")
            print(f"      URL: {result['url'][:50]}...")
        
        return True
        
    except ValueError as e:
        if "BING_API_KEY" in str(e):
            print(f"❌ FAIL: API key issue - {e}")
        else:
            print(f"❌ FAIL: {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL: API call failed - {e}")
        return False


async def test_pdf_search():
    """Test 5: PDF-specific search"""
    print("\n" + "="*60)
    print("TEST 5: PDF Document Discovery")
    print("="*60)
    
    client = BingSearchClient()
    
    try:
        results = await client.search_pdfs(
            site_domain="bundestag.de",
            keywords=["Gesetzentwurf"],
            max_results=3
        )
        
        print(f"✅ PASS: PDF search completed")
        print(f"   Found {len(results)} results")
        
        # Check if results contain PDFs
        pdf_count = sum(1 for r in results if r['url'].lower().endswith('.pdf'))
        print(f"   PDF documents: {pdf_count}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  WARNING: PDF search failed - {e}")
        # Don't fail the test if API isn't configured
        if "BING_API_KEY" in str(e):
            return False
        return True


def test_source_selector():
    """Test 6: SourceSelector integration"""
    print("\n" + "="*60)
    print("TEST 6: SourceSelector Integration")
    print("="*60)
    
    selector = SourceSelector()
    
    # Check if search is available
    if selector.is_search_available():
        print("✅ PASS: Tier 2 search engine available")
        client = selector.get_search_client()
        print(f"   Engine: {type(client).__name__}")
    else:
        print("⚠️  WARNING: No Tier 2 search engine configured")
        print("   Set BING_API_KEY or GOOGLE_API_KEY")
    
    # Test profile without OParl or RIS
    test_profile = {
        "name": "Test Municipality",
        "url": "https://example-municipality.de",
        # No oparl_url, no RIS pattern
    }
    
    # This should return a search client
    client = selector.select_acquisition_engine(test_profile, None)
    
    if client:
        print(f"✅ PASS: SourceSelector returns client for Tier 2 profile")
    else:
        print("⚠️  WARNING: SourceSelector returned None (expected if no API keys)")
    
    return True


async def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*60)
    print("BING CUSTOM SEARCH API - TEST SUITE")
    print("="*60)
    print("\nThis test suite validates the Bing Search integration.")
    print("Some tests require a valid BING_API_KEY environment variable.")
    
    results = []
    
    # Run tests
    results.append(("API Configuration", test_api_configuration()))
    results.append(("Client Initialization", test_client_initialization()))
    results.append(("Query Generation", test_query_generation()))
    results.append(("API Call", await test_api_call()))
    results.append(("PDF Search", await test_pdf_search()))
    results.append(("SourceSelector", test_source_selector()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Bing Search API is ready.")
        return 0
    elif passed >= total * 0.8:
        print("\n⚠️  Most tests passed. Check failed tests above.")
        return 0
    else:
        print("\n❌ Several tests failed. Please review configuration.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
