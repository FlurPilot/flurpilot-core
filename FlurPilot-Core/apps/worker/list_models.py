import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def list_models():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("No API Key")
        return

    url = "https://openrouter.ai/api/v1/models"
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            data = resp.json().get('data', [])
            for m in data:
                mid = m.get('id')
                if 'opus' in mid.lower():
                    print(mid)
        else:
            print(f"Error: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    asyncio.run(list_models())
