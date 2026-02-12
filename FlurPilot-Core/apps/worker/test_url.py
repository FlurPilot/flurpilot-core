import asyncio
import httpx
import json

async def check():
    candidates = [
        "https://ris.niederkruechten.de/webservice/oparl/v1.1/body", # Known disabled
        "https://session.bochum.de/bi/oparl/1.1/system",
        "https://session.bochum.de/bi/oparl/1.0/system",
        "https://ris.moers.de/webservice/oparl/v1.1/system",
        "https://oparl.bonn.de/oparl/v1.0/system",
        "https://ratsinformation.stadt-koeln.de/oparl/v1.0/system",
        "https://ris.leipzig.de/oparl/1.0/system"
    ]

    async with httpx.AsyncClient() as client:
        for url in candidates:
            print(f"Testing: {url} ...")
            try:
                response = await client.get(url, follow_redirects=True, timeout=5.0)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"✅ SUCCESS! {url}")
                        print(json.dumps(data, indent=2)[:200] + "...")
                        return # Stop after first success
                    except:
                        print("❌ Invalid JSON")
                else:
                    print(f"❌ Status {response.status_code}")
            except Exception as e:
                print(f"❌ Error: {e}")
            print("-" * 20)

if __name__ == "__main__":
    asyncio.run(check())
