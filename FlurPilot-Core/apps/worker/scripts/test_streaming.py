import asyncio
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_client import generate_stream
from dotenv import load_dotenv

async def test_streaming():
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
    
    print("Testing Streaming Response from Claude 4.6...")
    print("-" * 30)
    
    prompt = "Explain in 3 short bullet points why the 'Bavarian Bypass' for Virtual Parcels is clever."
    
    async for chunk in generate_stream(prompt):
        print(chunk, end="", flush=True)
        
    print("\n" + "-" * 30)
    print("\n✅ Streaming complete.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_streaming())
