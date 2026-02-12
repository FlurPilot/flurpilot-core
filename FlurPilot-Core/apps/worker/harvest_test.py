import asyncio
import json
from connectors.oparl import OParlClient

async def harvest():
    # Moers (Verified Working)
    url = "https://ris.moers.de/webservice/oparl/v1.1/system"
    print(f"HARVESTING FROM: {url}")
    
    client = OParlClient(url)
    
    # Fetch Papers
    papers = await client.fetch_recent_papers()
    
    print(f"\n--- HARVEST RESULTS ({len(papers)} items) ---")
    for paper in papers[:10]: # Validating first 10
        name = paper.get('name', 'Untitled')
        date = paper.get('date', 'No-Date')
        print(f"[{date}] {name}")
        
        # Check files/auxiliaryFile
        files = paper.get('auxiliaryFile', [])
        if files:
            print(f"   > {len(files)} Attachments found.")
            
    await client.close()

if __name__ == "__main__":
    asyncio.run(harvest())
