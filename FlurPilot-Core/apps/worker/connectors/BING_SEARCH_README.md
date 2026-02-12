# Bing Custom Search API Connector

This module provides a robust interface to the Bing Custom Search API for document discovery in the FlurPilot acquisition engine.

## Overview

Replaces fragile HTML scraping with a stable API-based approach for discovering municipal documents (PDFs, etc.).

**Priority**: Bing > Google (if both configured, Bing is preferred)

## Setup

### 1. Get API Key

1. Go to [Bing Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)
2. Sign up for an Azure account (if needed)
3. Create a Bing Search resource
4. Copy the API key

### 2. Configuration

Add to your `.env` file:

```bash
# Required
BING_API_KEY=your-api-key-here

# Optional (for custom search configurations)
BING_CUSTOM_CONFIG_ID=your-custom-config-id
```

### 3. Test

```bash
cd apps/worker
python tests/test_bing_search.py
```

## Usage

### Basic Search

```python
from connectors.bing_search import BingSearchClient

client = BingSearchClient()

# Simple search
results = await client.search(
    "site:stadt-muenchen.de filetype:pdf Bebauungsplan",
    count=10
)

for result in results:
    print(f"{result['title']}: {result['url']}")
```

### PDF Discovery

```python
# Search for PDFs on a specific site
results = await client.search_pdfs(
    site_domain="stadt-koeln.de",
    keywords=["Aufstellungsbeschluss", "Solar"],
    year=2024,
    max_results=20
)
```

### Multiple Document Types

```python
# Search for PDFs, DOCX, and DOC files
results = await client.search_documents(
    site_domain="muenchen.de",
    keywords=["Bebauungsplan"],
    filetypes=["pdf", "docx", "doc"],
    year=2024
)

# Results are grouped by filetype
pdfs = results["pdf"]
docxs = results["docx"]
```

### With SourceSelector

```python
from source_selector import SourceSelector

selector = SourceSelector()

# For a profile without OParl or RIS
profile = {
    "name": "Example City",
    "url": "https://example-city.de"
}

# Automatically selects Bing if configured
client = selector.select_acquisition_engine(profile, fetcher)
```

## API Methods

### `generate_search_query(site_domain, keywords, filetype=None, year=None)`

Constructs an optimized search query.

**Example**:
```python
query = client.generate_search_query(
    "stadt-muenchen.de",
    ["Bebauungsplan", "Solar"],
    filetype="pdf",
    year=2024
)
# Result: "site:stadt-muenchen.de filetype:pdf Bebauungsplan Solar 2024"
```

### `search(query, count=20, offset=0)`

Executes search and returns structured results.

**Returns**:
```python
[
    {
        "title": "Document Title",
        "url": "https://...",
        "snippet": "Description...",
        "date": "2024-01-15T10:30:00",
        "display_url": "stadt-muenchen.de/..."
    }
]
```

### `search_pdfs(site_domain, keywords, year=None, max_results=20)`

Convenience method for PDF discovery.

### `search_documents(site_domain, keywords, filetypes=None, year=None, max_results=20)`

Search multiple file types in one call.

## Query Syntax

The connector generates Bing-compatible search queries:

- `site:domain.de` - Restrict to specific domain
- `filetype:pdf` - Filter by file type
- `"exact phrase"` - Exact match for multi-word terms
- `2024` - Year filter

**Examples**:
```
site:stadt-muenchen.de filetype:pdf "Bebauungsplan" Solar 2024
site:bundestag.de filetype:pdf Gesetzentwurf
```

## Error Handling

The client handles common errors:

- **401 Unauthorized**: Invalid API key
- **403 Forbidden**: Quota exceeded or access denied
- **Rate Limiting**: Automatic retry via httpx
- **Network Errors**: Clear error messages

```python
try:
    results = await client.search("query")
except ValueError as e:
    print(f"Configuration error: {e}")
except httpx.HTTPStatusError as e:
    print(f"API error: {e}")
```

## Testing

Run the test suite:

```bash
# All tests
python tests/test_bing_search.py

# Individual test categories:
# 1. API Configuration
# 2. Client Initialization  
# 3. Query Generation
# 4. API Call Execution
# 5. PDF Search
# 6. SourceSelector Integration
```

## Comparison: Bing vs Google

| Feature | Bing | Google |
|---------|------|--------|
| Free Tier | 1,000 req/month | 100 req/day |
| Paid Tier | $7/1,000 req | $5/1,000 req |
| Setup Complexity | Medium | High (Custom Search Engine) |
| Result Quality | Good | Excellent |
| API Stability | Very Good | Good |

**Recommendation**: Use Bing as primary (better free tier), Google as fallback.

## Migration from Scraping

Before (fragile):
```python
# HTML scraping - breaks when site changes
response = await fetcher.get(url)
soup = BeautifulSoup(response.text)
pdfs = soup.find_all('a', href=re.compile(r'\.pdf$'))
```

After (stable):
```python
# API-based - consistent interface
results = await client.search_pdfs(
    site_domain="stadt-muenchen.de",
    keywords=["Bebauungsplan"]
)
```

## Cost Estimation

For typical usage (~500 queries/month):
- **Free Tier**: Sufficient for development/small deployments
- **Production**: ~$3.50/month (500 queries)

Monitor usage in Azure Portal.

## Troubleshooting

### "BING_API_KEY not set"
- Check `.env` file
- Verify key is loaded: `echo $BING_API_KEY`
- Restart your application

### "Invalid BING_API_KEY"
- Verify key in Azure Portal
- Ensure key is active (not revoked)
- Check subscription status

### No results returned
- Check query syntax: `site:domain.de` must be valid domain
- Try simpler keywords first
- Verify Bing can index the site

### Rate limiting (429 errors)
- Implement exponential backoff
- Reduce request frequency
- Consider upgrading plan

## Resources

- [Bing Search API Docs](https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/)
- [API Pricing](https://www.microsoft.com/en-us/bing/apis/pricing)
- [Azure Portal](https://portal.azure.com/)

## License

MIT - Part of FlurPilot Core
