import os

# Define the 70 places with their standards
places_data = [
    # Intangible Heritage
    {
        "name": "Kyoto (Washoku)",
        "unesco_criteria": "(iii), (v), (vi)",
        "iucn_category": "N/A",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Oryza, Camellia)",
    },
    {
        "name": "Kerala (Yoga)",
        "unesco_criteria": "(iii), (iv), (vi)",
        "iucn_category": "N/A",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Medicinal Herbs)",
    },
    {
        "name": "Oaxaca (Traditional Mexican Cuisine)",
        "unesco_criteria": "(ii), (v)",
        "iucn_category": "N/A",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Zea mays, Agave)",
    },
    {
        "name": "Raja Ampat",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "IV",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Anthozoa (Corals), Actinopterygii (Fish)",
    },
    {
        "name": "Yellowstone",
        "unesco_criteria": "(vii), (viii), (ix), (x)",
        "iucn_category": "II",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Mammalia (Canis lupus, Ursus arctos)",
    },
    {
        "name": "Great Barrier Reef",
        "unesco_criteria": "(vii), (viii), (ix), (x)",
        "iucn_category": "VI",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Anthozoa, Actinopterygii",
    },
    {
        "name": "Serengeti",
        "unesco_criteria": "(vii), (x)",
        "iucn_category": "II",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Mammalia (Connochaetes, Panthera)",
    },
    {
        "name": "Machu Picchu",
        "unesco_criteria": "(i), (iii), (vii), (ix)",
        "iucn_category": "V",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Orchidaceae), Aves",
    },
    {
        "name": "Yosemite",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "II",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Sequoiadendron), Mammalia",
    },
    {
        "name": "Pantanal",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "IV",
        "ramsar_type": "Inland",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Aves (Ciconiidae), Reptilia (Caiman)",
    },
    {
        "name": "Namibrand",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "Ib",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Welwitschia), Mammalia (Oryx)",
    },
    {
        "name": "Andalusia (Flamenco)",
        "unesco_criteria": "(iii), (vi)",
        "iucn_category": "N/A",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Olea europaea)",
    },
    {
        "name": "Okavango Delta",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "II",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Mammalia (Loxodonta), Aves",
    },
    {
        "name": "Komodo",
        "unesco_criteria": "(vii), (x)",
        "iucn_category": "II",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Reptilia (Varanus komodoensis)",
    },
    {
        "name": "Cape West Coast",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "IV",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "Buffer",
        "dwc_taxonomic_dominance": "Plantae (Proteaceae, Fynbos)",
    },
    {
        "name": "Ngorongoro Lengai",
        "unesco_criteria": "(vii), (viii), (ix), (x)",
        "iucn_category": "VI",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Mammalia (Ungulates)",
    },
    {
        "name": "Aoraki Mackenzie",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "II",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Alpine flora), Aves",
    },
    {
        "name": "Marrakech (Falconry)",
        "unesco_criteria": "(v), (vi)",
        "iucn_category": "N/A",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Aves (Falconidae)",
    },
    {
        "name": "Bali (Wayang)",
        "unesco_criteria": "(iii), (vi)",
        "iucn_category": "N/A",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Ficus, Oryza)",
    },
    {
        "name": "Palau",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "VI",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Anthozoa, Scyphozoa (Mastigias)",
    },
    {
        "name": "Galápagos Islands",
        "unesco_criteria": "(vii), (viii), (ix), (x)",
        "iucn_category": "Ia",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Reptilia (Chelonoidis), Aves (Fringillidae)",
    },
    {
        "name": "Monarch Butterfly BR",
        "unesco_criteria": "(vii)",
        "iucn_category": "IV",
        "ramsar_type": "N/A",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Insecta (Danaus plexippus)",
    },
    {
        "name": "Sian Ka'an",
        "unesco_criteria": "(vii), (x)",
        "iucn_category": "II",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Aves (Pelecanidae), Plantae (Mangroves)",
    },
    {
        "name": "Clayoquot Sound",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "IV",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "Transition",
        "dwc_taxonomic_dominance": "Plantae (Thuja, Tsuga), Mammalia",
    },
    {
        "name": "Reykjanes",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "III",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Lecanoromycetes (Lichens)",
    },
    {
        "name": "Naples (Mediterranean Diet)",
        "unesco_criteria": "(ii), (iv), (v)",
        "iucn_category": "N/A",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Olea, Vitis)",
    },
    {
        "name": "Kingston (Reggae)",
        "unesco_criteria": "(vi)",
        "iucn_category": "N/A",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Tropical flora)",
    },
    {
        "name": "Bahia (Capoeira)",
        "unesco_criteria": "(vi)",
        "iucn_category": "N/A",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Atlantic Forest)",
    },
    {
        "name": "Buenos Aires (Tango)",
        "unesco_criteria": "(vi)",
        "iucn_category": "N/A",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Pampas flora)",
    },
    {
        "name": "Kilimanjaro",
        "unesco_criteria": "(vii)",
        "iucn_category": "II",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Dendrosenecio), Mammalia",
    },
    {
        "name": "Everglades",
        "unesco_criteria": "(viii), (ix), (x)",
        "iucn_category": "II",
        "ramsar_type": "Inland",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Reptilia (Alligator), Aves",
    },
    {
        "name": "Mekong Delta",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "V",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Actinopterygii (Siluriformes), Plantae",
    },
    {
        "name": "Nilgiri",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "IV",
        "ramsar_type": "N/A",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Mammalia (Elephas, Panthera), Plantae",
    },
    {
        "name": "Arganeraie",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "VI",
        "ramsar_type": "N/A",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Plantae (Argania spinosa)",
    },
    {
        "name": "Katla",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "III",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Bryophyta (Mosses)",
    },
    {
        "name": "Pic du Midi",
        "unesco_criteria": "(vii)",
        "iucn_category": "V",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Alpine flora)",
    },
    {
        "name": "Kakadu",
        "unesco_criteria": "(i), (vi), (vii), (ix), (x)",
        "iucn_category": "II",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Reptilia (Crocodylus), Aves",
    },
    {
        "name": "Ha Long Bay",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "II",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Anthozoa, Plantae (Endemics)",
    },
    {
        "name": "Iguazu",
        "unesco_criteria": "(vii), (x)",
        "iucn_category": "II",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Aves (Apodidae), Mammalia",
    },
    {
        "name": "Itoigawa",
        "unesco_criteria": "(viii)",
        "iucn_category": "III",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Jadeite context)",
    },
    {
        "name": "Batur",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "V",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Volcanic flora)",
    },
    {
        "name": "Central Idaho",
        "unesco_criteria": "(vii)",
        "iucn_category": "II",
        "ramsar_type": "N/A",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Mammalia (Cervidae, Ursidae)",
    },
    {
        "name": "Ross Sea",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "Ia",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Aves (Spheniscidae), Mammalia (Pinnipedia)",
    },
    {
        "name": "Marae Moana",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "VI",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Anthozoa, Mammalia (Cetacea)",
    },
    {
        "name": "Kerry",
        "unesco_criteria": "(vii)",
        "iucn_category": "V",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Bryophytes), Aves",
    },
    {
        "name": "Brecon Beacons",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "V",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Upland flora)",
    },
    {
        "name": "Camargue",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "IV",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "Buffer",
        "dwc_taxonomic_dominance": "Aves (Phoenicopteridae), Mammalia (Equus)",
    },
    {
        "name": "Doñana",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "II",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Aves (Anatidae), Mammalia (Lynx pardinus)",
    },
    {
        "name": "Lake Baikal",
        "unesco_criteria": "(vii), (viii), (ix), (x)",
        "iucn_category": "II",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Mammalia (Pusa sibirica), Actinopterygii",
    },
    {
        "name": "Mount Kenya",
        "unesco_criteria": "(vii), (ix)",
        "iucn_category": "II",
        "ramsar_type": "N/A",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Plantae (Lobelia), Aves",
    },
    {
        "name": "Dana",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "IV",
        "ramsar_type": "N/A",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Plantae (Cupressus), Mammalia",
    },
    {
        "name": "Lesvos",
        "unesco_criteria": "(viii)",
        "iucn_category": "III",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Fossil Gymnospermae)",
    },
    {
        "name": "Mont-Mégantic",
        "unesco_criteria": "(vii)",
        "iucn_category": "V",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Aceraceae), Aves",
    },
    {
        "name": "Tubbataha",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "II",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Anthozoa, Cheloniidae (Turtles)",
    },
    {
        "name": "Sundarbans",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "II",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Rhizophoraceae), Mammalia (Panthera tigris)",
    },
    {
        "name": "Wadden Sea",
        "unesco_criteria": "(viii), (ix), (x)",
        "iucn_category": "IV",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Aves (Charadriiformes), Bivalvia",
    },
    {
        "name": "Danube Delta",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "II",
        "ramsar_type": "Inland",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Aves (Pelecanus), Actinopterygii",
    },
    {
        "name": "Mudeungsan",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "V",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Mountain flora)",
    },
    {
        "name": "Cherry Springs",
        "unesco_criteria": "(vii)",
        "iucn_category": "V",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Deciduous forest)",
    },
    {
        "name": "Exmoor",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "V",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Mammalia (Cervus elaphus), Plantae",
    },
    {
        "name": "Qeshm",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "VI",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Avicennia), Reptilia",
    },
    {
        "name": "Papahānaumokuākea",
        "unesco_criteria": "(iii), (vi), (viii), (ix), (x)",
        "iucn_category": "Ia",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Anthozoa, Aves (Diomedeidae)",
    },
    {
        "name": "Oki Islands",
        "unesco_criteria": "(vii), (viii)",
        "iucn_category": "V",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Subalpine-Temperate mix)",
    },
    {
        "name": "Marble Arch Caves",
        "unesco_criteria": "(viii)",
        "iucn_category": "III",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Plantae (Sphagnum), Invertebrata",
    },
    {
        "name": "Zselic",
        "unesco_criteria": "(vii)",
        "iucn_category": "V",
        "ramsar_type": "Inland",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Mammalia (Strigiformes context), Plantae",
    },
    {
        "name": "Bañados del Este",
        "unesco_criteria": "(ix), (x)",
        "iucn_category": "IV",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "Core",
        "dwc_taxonomic_dominance": "Plantae (Butia capitata), Aves",
    },
    {
        "name": "Chagos",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "Ia",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Anthozoa, Actinopterygii",
    },
    {
        "name": "Kermadec",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "Ia",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Actinopterygii, Mammalia (Cetacea)",
    },
    {
        "name": "Phoenix Islands",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "Ia",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Anthozoa, Aves",
    },
    {
        "name": "Ascension Island",
        "unesco_criteria": "(vii), (ix), (x)",
        "iucn_category": "VI",
        "ramsar_type": "Coastal/Marine",
        "mab_context": "N/A",
        "dwc_taxonomic_dominance": "Reptilia (Chelonia mydas), Aves",
    },
]

def derive_commerce_data(place):
    """Derive product families and rationale based on standards."""
    criteria = place["unesco_criteria"]
    dominance = place["dwc_taxonomic_dominance"]
    category = place["iucn_category"]
    ramsar = place["ramsar_type"]

    products = []
    rationale = ""

    # Logic for Products and Rationale
    if "Cultural" in dominance or "(i)" in criteria or "(iii)" in criteria or "(vi)" in criteria:
        products = ["Books", "Cards", "Home Decor"]
        rationale = f"Cultural criteria {criteria} support high-end heritage publishing and artisan-inspired home collections."
    elif "Anthozoa" in dominance or "Marine" in ramsar:
        products = ["Wall Art", "Fashion", "Education"]
        rationale = f"Exceptional marine biodiversity ({dominance}) lends itself to vibrant wall art and sustainable apparel lines."
    elif "Mammalia" in dominance or "Aves" in dominance:
        products = ["Calendars", "Wall Art", "Puzzles"]
        rationale = f"Charismatic megafauna and avian dominance ({dominance}) drive demand for high-visual-impact prints and interactive puzzles."
    elif "Plantae" in dominance:
        products = ["Books", "Home Decor", "Education"]
        rationale = f"Botanical dominance ({dominance}) facilitates educational resources and aesthetically refined lifestyle products."
    elif "vii" in criteria or "viii" in criteria:
        products = ["Wall Art", "Books", "Calendars"]
        rationale = f"Iconic geological and landscape criteria ({criteria}) favor large-format visual media and commemorative gifts."
    else:
        products = ["Wall Art", "Cards", "Education"]
        rationale = "Universal appeal of global significance supports diverse visual and educational product categories."

    return products, rationale

# Generate Matrices
standards_matrix = "| Name | UNESCO Criteria | IUCN | Ramsar | MAB | DwC Taxonomic Dominance |\n"
standards_matrix += "|------|-----------------|------|--------|-----|--------------------------|\n"

commerce_matrix = "| Name | Top Product Families | Commerce Rationale |\n"
commerce_matrix += "|------|----------------------|--------------------|\n"

for place in places_data:
    products, rationale = derive_commerce_data(place)
    
    standards_matrix += f"| {place['name']} | {place['unesco_criteria']} | {place['iucn_category']} | {place['ramsar_type']} | {place['mab_context']} | {place['dwc_taxonomic_dominance']} |\n"
    commerce_matrix += f"| {place['name']} | {', '.join(products)} | {rationale} |\n"

# Ensure directories exist
os.makedirs("docs/curation", exist_ok=True)
os.makedirs("docs/commerce", exist_ok=True)

# Write files
with open("docs/curation/70_place_standards_matrix.md", "w") as f:
    f.write("# 70 Place Standards Matrix\n\n")
    f.write(standards_matrix)

with open("docs/commerce/70_place_commerce_matrix.md", "w") as f:
    f.write("# 70 Place Commerce Matrix\n\n")
    f.write(commerce_matrix)

print("Matrices generated successfully.")
