import os
import httpx
import json
import asyncio
from typing import List, Dict, Any

API_KEY = os.getenv("SMITHSONIAN_API_KEY")
BASE_URL = "https://api.si.edu/openaccess/api/v1.0/search"

PLACES = [
    "Yellowstone",
    "Great Barrier Reef",
    "Galápagos",
    "Kakadu"
]

async def fetch_smithsonian_assets(query: str, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
    params = {
        "q": query,
        "api_key": API_KEY,
        "rows": 100  # Fetch a good sample for each place
    }
    try:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("response", {}).get("rows", [])
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

def score_asset(asset: Dict[str, Any], place: str) -> Dict[str, Any]:
    content = asset.get("content", {})
    metadata = content.get("descriptiveNonRepeating", {})
    
    # Rights Hard Gate
    usage = metadata.get("metadata_usage", {}).get("access", "").upper()
    if usage != "CC0":
        return None
    
    title = asset.get("title", "Untitled")
    unit = metadata.get("unit_code", "Unknown")
    
    # 1. Place Relevance (0.25)
    place_score = 1.0 if place.lower() in title.lower() else 0.7
    
    # 2. Public Domain Confidence (0.15) - Already Gated
    pd_score = 1.0
    
    # 3. Visual Quality (0.20)
    # Check for online media
    media = content.get("online_media", {}).get("media", [])
    visual_score = 0.5
    if media:
        visual_score = 1.0 if any(m.get("type") == "Images" for m in media) else 0.8
    
    # 4. Commercial Value (0.20)
    obj_type = content.get("freetext", {}).get("objectType", [{}])[0].get("content", "").lower()
    comm_value = 0.6
    if any(k in obj_type for k in ["painting", "print", "illustration", "map", "specimen"]):
        comm_value = 1.0
    elif "photograph" in obj_type:
        comm_value = 0.9
    
    # 5. Collection Fit (0.20)
    fit_score = 0.8
    if unit in ["NMNH", "NMAI", "SAAM", "NPG"]: # Natural History, Am. Indian, Am. Art, Portrait Gallery
        fit_score = 1.0

    total_score = (place_score * 0.25) + (pd_score * 0.15) + (visual_score * 0.20) + (comm_value * 0.20) + (fit_score * 0.20)
    
    why_valuable = f"High-quality {obj_type or 'object'} from {unit} with strong {place} relevance."
    if comm_value == 1.0:
        why_valuable += " Excellent commercial potential as an illustration or specimen."

    return {
        "Smithsonian ID": asset.get("id"),
        "Title": title,
        "Collection": unit,
        "Media Type": "Image" if visual_score == 1.0 else "Other",
        "Rights": usage,
        "Place": place,
        "Opportunity Score": round(total_score, 3),
        "Why Valuable": why_valuable
    }

async def main():
    if not API_KEY:
        print("Error: SMITHSONIAN_API_KEY not found in environment.")
        return

    all_candidates = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [fetch_smithsonian_assets(place, client) for place in PLACES]
        results = await asyncio.gather(*tasks)
        
        for idx, place_assets in enumerate(results):
            place = PLACES[idx]
            for asset in place_assets:
                scored = score_asset(asset, place)
                if scored:
                    all_candidates.append(scored)

    # Rank by score
    all_candidates.sort(key=lambda x: x["Opportunity Score"], reverse=True)
    top_100 = all_candidates[:100]

    # Output as Markdown Table
    print(f"| Smithsonian ID | Title | Collection | Media Type | Rights | Place | Score | Why Valuable |")
    print(f"| --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in top_100:
        # Clean title for MD
        clean_title = c["Title"].replace("|", "\\|")[:50] + ("..." if len(c["Title"]) > 50 else "")
        print(f"| {c['Smithsonian ID']} | {clean_title} | {c['Collection']} | {c['Media Type']} | {c['Rights']} | {c['Place']} | {c['Opportunity Score']} | {c['Why Valuable']} |")

    # Also save to JSON
    os.makedirs("data/exports", exist_ok=True)
    with open("data/exports/smithsonian_top_100.json", "w") as f:
        json.dump(top_100, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
