import json
from typing import List, Dict

# 70 Flagship Places Data (Simplified from flagship_portfolio_v1.md)
# Format: (Name, Category, Discovery, Collection, Commerce, Tourism)
PLACES_RAW = [
    ("Kyoto (Washoku)", "Intangible Heritage", 10, 10, 10, 10),
    ("Kerala (Yoga)", "Intangible Heritage", 10, 10, 10, 10),
    ("Oaxaca (Traditional Mexican Cuisine)", "Intangible Heritage", 9, 10, 10, 10),
    ("Raja Ampat", "Marine Protected Areas", 10, 10, 9, 10),
    ("Yellowstone", "UNESCO World Heritage", 10, 9, 9, 10),
    ("Great Barrier Reef", "UNESCO World Heritage", 10, 10, 8, 10),
    ("Serengeti", "UNESCO World Heritage", 9, 9, 10, 10),
    ("Machu Picchu", "UNESCO World Heritage", 10, 9, 9, 10),
    ("Yosemite", "UNESCO World Heritage", 9, 9, 10, 10),
    ("Pantanal", "Ramsar Wetlands", 10, 9, 9, 10),
    ("Namibrand", "Dark Sky Places", 10, 9, 9, 10),
    ("Andalusia (Flamenco)", "Intangible Heritage", 9, 9, 10, 10),
    ("Okavango Delta", "Ramsar Wetlands", 10, 9, 8, 10),
    ("Komodo", "Biosphere Reserves", 10, 9, 8, 10),
    ("Cape West Coast", "Biosphere Reserves", 9, 10, 9, 9),
    ("Ngorongoro Lengai", "UNESCO Global Geoparks", 10, 9, 8, 10),
    ("Aoraki Mackenzie", "Dark Sky Places", 10, 8, 9, 10),
    ("Marrakech (Falconry)", "Intangible Heritage", 9, 9, 9, 10),
    ("Bali (Wayang)", "Intangible Heritage", 9, 10, 8, 10),
    ("Palau", "Marine Protected Areas", 9, 9, 9, 10),
    ("Galápagos Islands", "UNESCO World Heritage", 10, 10, 7, 9),
    ("Monarch Butterfly BR", "Biosphere Reserves", 10, 9, 9, 8),
    ("Sian Ka'an", "Biosphere Reserves", 9, 9, 8, 10),
    ("Clayoquot Sound", "Biosphere Reserves", 9, 8, 9, 10),
    ("Reykjanes", "UNESCO Global Geoparks", 9, 8, 9, 10),
    ("Naples (Mediterranean Diet)", "Intangible Heritage", 8, 8, 10, 10),
    ("Kingston (Reggae)", "Intangible Heritage", 8, 8, 10, 10),
    ("Bahia (Capoeira)", "Intangible Heritage", 9, 8, 9, 10),
    ("Buenos Aires (Tango)", "Intangible Heritage", 8, 9, 9, 10),
    ("Kilimanjaro", "UNESCO World Heritage", 9, 8, 8, 10),
    ("Everglades", "Ramsar Wetlands", 9, 9, 8, 9),
    ("Mekong Delta", "Ramsar Wetlands", 9, 8, 8, 10),
    ("Nilgiri", "Biosphere Reserves", 8, 9, 9, 9),
    ("Arganeraie", "Biosphere Reserves", 8, 8, 10, 9),
    ("Katla", "UNESCO Global Geoparks", 9, 8, 8, 10),
    ("Pic du Midi", "Dark Sky Places", 8, 9, 8, 10),
    ("Kakadu", "UNESCO World Heritage", 9, 10, 7, 8),
    ("Ha Long Bay", "UNESCO World Heritage", 8, 8, 8, 10),
    ("Iguazu", "UNESCO World Heritage", 8, 8, 8, 10),
    ("Itoigawa", "UNESCO Global Geoparks", 8, 9, 9, 8),
    ("Batur", "UNESCO Global Geoparks", 8, 8, 8, 10),
    ("Central Idaho", "Dark Sky Places", 9, 8, 8, 9),
    ("Ross Sea", "Marine Protected Areas", 10, 9, 7, 8),
    ("Marae Moana", "Marine Protected Areas", 9, 9, 7, 9),
    ("Kerry", "Dark Sky Places", 8, 8, 7, 10),
    ("Brecon Beacons", "Dark Sky Places", 8, 7, 8, 10),
    ("Camargue", "Ramsar Wetlands", 7, 8, 9, 8),
    ("Doñana", "Ramsar Wetlands", 8, 8, 7, 9),
    ("Lake Baikal", "Ramsar Wetlands", 10, 9, 6, 7),
    ("Mount Kenya", "Biosphere Reserves", 8, 8, 7, 9),
    ("Dana", "Biosphere Reserves", 8, 8, 7, 9),
    ("Lesvos", "UNESCO Global Geoparks", 8, 9, 7, 8),
    ("Mont-Mégantic", "Dark Sky Places", 8, 8, 7, 9),
    ("Tubbataha", "Marine Protected Areas", 8, 8, 7, 9),
    ("Sundarbans", "Ramsar Wetlands", 9, 8, 7, 7),
    ("Wadden Sea", "Ramsar Wetlands", 7, 8, 7, 9),
    ("Danube Delta", "Ramsar Wetlands", 8, 8, 7, 8),
    ("Mudeungsan", "UNESCO Global Geoparks", 7, 8, 7, 9),
    ("Cherry Springs", "Dark Sky Places", 7, 7, 8, 9),
    ("Exmoor", "Dark Sky Places", 7, 7, 8, 9),
    ("Qeshm", "UNESCO Global Geoparks", 9, 8, 6, 7),
    ("Papahānaumokuākea", "Marine Protected Areas", 10, 9, 6, 5),
    ("Oki Islands", "UNESCO Global Geoparks", 7, 8, 7, 7),
    ("Marble Arch Caves", "UNESCO Global Geoparks", 7, 7, 7, 8),
    ("Zselic", "Dark Sky Places", 6, 7, 6, 8),
    ("Bañados del Este", "Biosphere Reserves", 6, 7, 6, 7),
    ("Chagos", "Marine Protected Areas", 9, 8, 5, 4),
    ("Kermadec", "Marine Protected Areas", 9, 8, 5, 4),
    ("Phoenix Islands", "Marine Protected Areas", 9, 8, 5, 3),
    ("Ascension Island", "Marine Protected Areas", 8, 7, 5, 5)
]

# Asset Class Base Values (Collection, Educational, Commerce)
ASSET_CLASSES = {
    "Maps": (9, 10, 10),
    "Photography": (7, 9, 9),
    "Posters": (6, 7, 10),
    "Prints": (10, 9, 10),
    "Books": (8, 10, 6),
    "Manuscripts": (10, 9, 4),
    "Audio": (5, 10, 5),
    "Film": (6, 9, 7)
}

# Relevance Multipliers (Category x Asset Class)
RELEVANCE = {
    "Intangible Heritage": {"Maps": 0.6, "Photography": 0.9, "Posters": 0.9, "Prints": 1.0, "Books": 0.9, "Manuscripts": 1.0, "Audio": 1.0, "Film": 1.0},
    "Marine Protected Areas": {"Maps": 1.0, "Photography": 0.9, "Posters": 0.8, "Prints": 1.0, "Books": 0.9, "Manuscripts": 0.7, "Audio": 0.5, "Film": 0.8},
    "UNESCO World Heritage": {"Maps": 1.0, "Photography": 1.0, "Posters": 0.9, "Prints": 1.0, "Books": 1.0, "Manuscripts": 0.9, "Audio": 0.6, "Film": 0.8},
    "Ramsar Wetlands": {"Maps": 1.0, "Photography": 0.9, "Posters": 0.7, "Prints": 1.0, "Books": 0.9, "Manuscripts": 0.8, "Audio": 0.6, "Film": 0.8},
    "Dark Sky Places": {"Maps": 0.9, "Photography": 1.0, "Posters": 0.9, "Prints": 0.8, "Books": 0.8, "Manuscripts": 0.7, "Audio": 0.4, "Film": 0.7},
    "Biosphere Reserves": {"Maps": 1.0, "Photography": 0.9, "Posters": 0.8, "Prints": 1.0, "Books": 1.0, "Manuscripts": 0.8, "Audio": 0.6, "Film": 0.8},
    "UNESCO Global Geoparks": {"Maps": 1.0, "Photography": 0.8, "Posters": 0.7, "Prints": 0.9, "Books": 1.0, "Manuscripts": 0.9, "Audio": 0.5, "Film": 0.8}
}

def calculate_opportunities():
    collection_opps = []
    commerce_opps = []
    educational_opps = []

    for name, cat, disc, coll, comm, tour in PLACES_RAW:
        place_total = disc + coll + comm + tour
        place_factor = place_total / 40.0
        
        for ac, (base_coll, base_edu, base_comm) in ASSET_CLASSES.items():
            rel = RELEVANCE[cat].get(ac, 1.0)
            
            # Scores
            s_coll = round(base_coll * rel * place_factor, 2)
            s_edu = round(base_edu * rel * place_factor, 2)
            s_comm = round(base_comm * rel * place_factor, 2)
            
            collection_opps.append({"Place": name, "Asset Class": ac, "Score": s_coll})
            commerce_opps.append({"Place": name, "Asset Class": ac, "Score": s_comm})
            educational_opps.append({"Place": name, "Asset Class": ac, "Score": s_edu})

    # Sort and get Top 20
    collection_opps.sort(key=lambda x: x["Score"], reverse=True)
    commerce_opps.sort(key=lambda x: x["Score"], reverse=True)
    educational_opps.sort(key=lambda x: x["Score"], reverse=True)
    
    return collection_opps[:20], commerce_opps[:20], educational_opps[:20]

def print_matrix():
    print("### LOC Opportunity Matrix (Base Values)")
    print("| Asset Class | Collection | Educational | Commerce | Rationale |")
    print("| :--- | :---: | :---: | :---: | :--- |")
    rationales = {
        "Maps": "Foundational for place identity; high demand for wall art; essential for historical context.",
        "Photography": "Authentic heritage visuals; strong emotional resonance; high commercial appeal for prints/books.",
        "Posters": "Visual impact; designed for public consumption; perfect for modern decor/branding.",
        "Prints": "'Golden Age' lithographs/engravings; highest aesthetic refinement; ideal for premium products.",
        "Books": "Dense historical/scientific data; source material for collections; lower standalone commercial value.",
        "Manuscripts": "Extremely rare/unique; high prestige; difficult to commercialize beyond niche publications.",
        "Audio": "Vital for Intangible Heritage (music/language); high educational power; limited visual commerce.",
        "Film": "Dynamic historical record; high engagement; licensing potential but limited physical commerce."
    }
    for ac, scores in ASSET_CLASSES.items():
        print(f"| {ac} | {scores[0]} | {scores[1]} | {scores[2]} | {rationales[ac]} |")
    print("\n")

def print_top_20(title, opps):
    print(f"### {title}")
    print("| Rank | Place | Asset Class | Score |")
    print("| :--- | :--- | :--- | :---: |")
    for i, opp in enumerate(opps):
        print(f"| {i+1} | {opp['Place']} | {opp['Asset Class']} | {opp['Score']} |")
    print("\n")

if __name__ == "__main__":
    top_coll, top_comm, top_edu = calculate_opportunities()
    
    print_matrix()
    print_top_20("Top 20 Collection Opportunities", top_coll)
    print_top_20("Top 20 Commerce Opportunities", top_comm)
    print_top_20("Top 20 Educational Opportunities", top_edu)
