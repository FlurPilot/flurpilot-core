import asyncio
import os
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
from ai_client import get_client
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    print("Testing OpenRouter Connection...")
    
    try:
        client, model = get_client()
        print(f"Client initialized with model: {model}")
        
        print(f"Sending request to {model}...")
        completion = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Are you online? Reply with 'Yes, I am online as FlurPilot AI'."
                }
            ]
        )
        
        print("\n--- Response ---")
        print(completion.choices[0].message.content)
        print("----------------")
        print("\n✅ Connection Successful!")
        
    except Exception as e:
        import traceback
        print(f"\n❌ Connection Failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
