import asyncio
from connectors.sessionnet import SessionNetClient

async def test_sessionnet():
    # Target: Stadt Crailsheim (Hosted by KRZ)
    # URL: https://sessionnet.krz.de/crailsheim/bi/
    url = "https://sessionnet.krz.de/crailsheim/bi" 
    
    print(f"Testing SessionNet Connector with: {url}")
    
    client = SessionNetClient(url)
    
    # 1. Connectivity
    alive = await client.check_connectivity()
    print(f"Connectivity Check: {'ALIVE' if alive else 'DEAD'}")
    
    if not alive:
        return

    # 2. Search
    keywords = ["PV", "Solar", "Anlage"]
    print(f"Searching for: {keywords} ...")
    
    results = await client.search_documents(keywords)
    
    print(f"Found {len(results)} items.")
    for res in results[:5]:
        print(f" - {res['name']} ({res['id']})")
        
    if len(results) > 0:
        print("SUCCESS: Tier 1.5 Scraper Verified!")

if __name__ == "__main__":
    asyncio.run(test_sessionnet())
