import asyncio
import os
import random
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

# Niederkrüchten Coordinates (approx center)
BASE_LAT = 51.199
BASE_LNG = 6.220

def generate_random_polygon(lat_center, lng_center, radius=0.002):
    """Creates a small random quad polygon around a center point."""
    coords = []
    # Make a rough square/trapezoid (4 corners)
    offsets = [
        (-radius, -radius),
        (radius, -radius),
        (radius, radius),
        (-radius, radius)
    ]
    
    # Calculate corners with jitter
    corners = []
    for ox, oy in offsets:
        jitter_x = random.uniform(-0.0005, 0.0005)
        jitter_y = random.uniform(-0.0005, 0.0005)
        corners.append((lng_center + ox + jitter_x, lat_center + oy + jitter_y))
    
    # Close the loop: Append the first corner at the end
    corners.append(corners[0])
    
    # WKT Format: POLYGON((lng lat, lng lat, ...))
    wkt_coords = ", ".join([f"{lng} {lat}" for lng, lat in corners])
    return f"POLYGON(({wkt_coords}))"

async def seed_mock_data():
    print("Generating Synthetic Data for Neo-Trust Dashboard...")
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    parcels = []
    for i in range(50):
        # Random position shift
        shift_lat = random.uniform(-0.02, 0.02)
        shift_lng = random.uniform(-0.03, 0.03)
        
        geom = generate_random_polygon(BASE_LAT + shift_lat, BASE_LNG + shift_lng)
        
        parcel = {
            "alkis_id": f"MOCK-NDK-{1000+i}",
            "geom": geom,
            "area_sqm": random.randint(500, 50000),
            "properties": {
                "owner_type": random.choice(["Private", "Municipal", "Commercial", "Unknown"]),
                "land_use": random.choice(["Agriculture", "Forest", "Residential", "Industrial"]),
                "risk_score": random.randint(1, 100),
                "last_assessed": "2026-02-06"
            }
        }
        parcels.append(parcel)

    print(f"Injecting {len(parcels)} parcels into 'geo_parcels'...")
    
    try:
        data = client.table("geo_parcels").upsert(parcels, on_conflict="alkis_id").execute()
        print("✅ Success! Mock data active.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(seed_mock_data())
