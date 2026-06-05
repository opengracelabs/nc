import json
import os
from pathlib import Path

# Nature & Culture Flagship Portfolio v1 - Curated Data
PORTFOLIO_RECORDS = [
    # Category 1: UNESCO World Heritage
    {
        "name": "Yellowstone",
        "category": "UNESCO World Heritage",
        "why_flagship": "World's first national park; unmatched geothermal concentration and intact megafauna ecosystems.",
        "bhl_opportunities": ["19th-century geological survey illustrations", "Early Rocky Mountain botanical sketches"],
        "smithsonian_opportunities": ["Thomas Moran landscape watercolors", "William Henry Jackson expedition photography"],
        "collection_potential": "High demand for 'American Frontier' and early conservation aesthetics.",
        "commerce_potential": "Fine art prints, heritage-themed apparel, and high-end photographic journals.",
        "tourism_potential": "Primary global destination for geothermal tourism and wolf-watching.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Great Barrier Reef",
        "category": "UNESCO World Heritage",
        "why_flagship": "Largest coral reef system on Earth; critical biodiversity hotspot for marine life.",
        "bhl_opportunities": ["18th-century hydrographic charts", "Victorian-era ichthyological color plates"],
        "smithsonian_opportunities": ["U.S. Exploring Expedition coral specimens", "Early scientific maritime records"],
        "collection_potential": "Vibrant marine aesthetics; high educational and scientific appeal.",
        "commerce_potential": "Sustainable fashion collaborations, digital underwater art galleries.",
        "tourism_potential": "World-leading destination for diving and reef-based eco-education.",
        "discovery_value": 10, "collection_value": 10, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Galápagos Islands",
        "category": "UNESCO World Heritage",
        "why_flagship": "Living laboratory of evolution; unique endemic species and historical scientific significance.",
        "bhl_opportunities": ["Charles Darwin's HMS Beagle sketches", "Early reptilian anatomical engravings"],
        "smithsonian_opportunities": ["Albatross expedition specimens", "Early 20th-century natural history photography"],
        "collection_potential": "Niche appeal for evolutionary biology and scientific history enthusiasts.",
        "commerce_potential": "Educational media, heritage travel gear, high-quality wildlife replicas.",
        "tourism_potential": "Top-tier destination for high-end, research-led eco-tourism.",
        "discovery_value": 10, "collection_value": 10, "commerce_value": 7, "tourism_value": 9
    },
    {
        "name": "Kakadu",
        "category": "UNESCO World Heritage",
        "why_flagship": "Continuous human habitation for 65,000 years; world-class rock art and wetland biodiversity.",
        "bhl_opportunities": ["Australian tropical flora illustrations", "Early anthropological field journals"],
        "smithsonian_opportunities": ["Indigenous material culture artifacts", "Herbert Basedow expedition records"],
        "collection_potential": "Unique intersection of deep time, indigenous culture, and unique fauna.",
        "commerce_potential": "Ethical indigenous art collaborations, premium cultural heritage books.",
        "tourism_potential": "Exceptional for cultural-natural immersive travel experiences.",
        "discovery_value": 9, "collection_value": 10, "commerce_value": 7, "tourism_value": 8
    },
    {
        "name": "Serengeti",
        "category": "UNESCO World Heritage",
        "why_flagship": "Hosts the largest terrestrial mammal migration; quintessential African savannah ecosystem.",
        "bhl_opportunities": ["19th-century big game lithographs", "East African botanical studies"],
        "smithsonian_opportunities": ["Roosevelt African Expedition specimens", "Early savanna habitat photography"],
        "collection_potential": "Iconic wildlife imagery with massive global recognition.",
        "commerce_potential": "Luxury safari branding, wildlife photography workshops, high-end décor.",
        "tourism_potential": "The global gold standard for terrestrial wildlife viewing.",
        "discovery_value": 9, "collection_value": 9, "commerce_value": 10, "tourism_value": 10
    },
    {
        "name": "Machu Picchu",
        "category": "UNESCO World Heritage",
        "why_flagship": "Masterpiece of Andean architecture and landscape engineering; symbolic of Inca civilization.",
        "bhl_opportunities": ["Andean ethnobotany records", "19th-century mountain terrain surveys"],
        "smithsonian_opportunities": ["Hiram Bingham expedition artifacts", "Early Peruvian archaeological photography"],
        "collection_potential": "Extreme cultural prestige and aesthetic mystery.",
        "commerce_potential": "Historical travel accessories, architecture-inspired design collections.",
        "tourism_potential": "One of the most visited and desired bucket-list sites globally.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Ha Long Bay",
        "category": "UNESCO World Heritage",
        "why_flagship": "Stunning karst seascape; iconic limestone pillars and rich maritime cultural history.",
        "bhl_opportunities": ["French colonial botanical surveys", "Gulf of Tonkin maritime charts"],
        "smithsonian_opportunities": ["Southeast Asian marine biodiversity records", "Early regional ethnography"],
        "collection_potential": "High visual impact; poetic and serene landscape aesthetics.",
        "commerce_potential": "Hospitality design, luxury cruise branding, landscape art prints.",
        "tourism_potential": "South East Asia's premier maritime natural attraction.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Yosemite",
        "category": "UNESCO World Heritage",
        "why_flagship": "Iconic granitic landforms and giant sequoias; birth of the modern national park idea.",
        "bhl_opportunities": ["John Muir's botanical sketches", "Early Sierra Nevada geological maps"],
        "smithsonian_opportunities": ["Ansel Adams heritage photography", "Carleton Watkins mammoth plates"],
        "collection_potential": "Gold standard for American wilderness aesthetics.",
        "commerce_potential": "Outdoor gear branding, fine art photography, conservation-themed media.",
        "tourism_potential": "Central pillar of North American mountain tourism.",
        "discovery_value": 9, "collection_value": 9, "commerce_value": 10, "tourism_value": 10
    },
    {
        "name": "Iguazu",
        "category": "UNESCO World Heritage",
        "why_flagship": "One of the world's largest and most spectacular waterfall systems; subtropical rainforest setting.",
        "bhl_opportunities": ["Atlantic Forest lepidoptera illustrations", "Early riverine exploration logs"],
        "smithsonian_opportunities": ["South American bird specimens", "Boundary survey expedition photos"],
        "collection_potential": "Dynamic and powerful nature imagery; high sensory appeal.",
        "commerce_potential": "Environmental awareness campaigns, wellness/nature sound branding.",
        "tourism_potential": "Primary destination for South American water-based eco-tourism.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Kilimanjaro",
        "category": "UNESCO World Heritage",
        "why_flagship": "Africa's highest peak and world's tallest free-standing mountain; diverse ecological zones.",
        "bhl_opportunities": ["Afro-alpine flora studies", "Early glacial mapping records"],
        "smithsonian_opportunities": ["East African montane mammal records", "Abbott expedition specimens"],
        "collection_potential": "Symbolic of adventure, climate change awareness, and African majesty.",
        "commerce_potential": "Adventure travel gear, climate science educational content.",
        "tourism_potential": "Global magnet for mountaineering and ecological trekking.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 8, "tourism_value": 10
    },

    # Category 2: Ramsar Wetlands
    {
        "name": "Okavango Delta",
        "category": "Ramsar Wetlands",
        "why_flagship": "Unique endorheic delta in the Kalahari; world-class concentration of wetland-dependent wildlife.",
        "bhl_opportunities": ["Southern African avian color plates", "Early river system navigation charts"],
        "smithsonian_opportunities": ["Smithsonian-Chrysler Expedition mammal records", "African freshwater ecology studies"],
        "collection_potential": "High-end wildlife art; rare and charismatic species focus.",
        "commerce_potential": "Exclusive eco-lodge design, high-end safari photography gear.",
        "tourism_potential": "The ultimate destination for water-based African safaris.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Everglades",
        "category": "Ramsar Wetlands",
        "why_flagship": "Subtropical sawgrass prairie; critical habitat for North American aquatic species.",
        "bhl_opportunities": ["Audubon's water bird engravings", "Seminole War-era landscape sketches"],
        "smithsonian_opportunities": ["Abbott expedition specimens", "Early Florida botanical surveys"],
        "collection_potential": "Rich heritage of American natural history and conservation struggle.",
        "commerce_potential": "Birding guides, eco-friendly apparel, swamp-exploration media.",
        "tourism_potential": "Critical hub for North American eco-tourism and birdwatching.",
        "discovery_value": 9, "collection_value": 9, "commerce_value": 8, "tourism_value": 9
    },
    {
        "name": "Pantanal",
        "category": "Ramsar Wetlands",
        "why_flagship": "World's largest tropical wetland; highest concentration of wildlife in South America.",
        "bhl_opportunities": ["19th-century Brazilian herpetology plates", "Early Amazonian border surveys"],
        "smithsonian_opportunities": ["Roosevelt-Rondon Expedition records", "Neotropical bird specimens"],
        "collection_potential": "Vibrant and dense wildlife imagery; incredible biodiversity focus.",
        "commerce_potential": "Wildlife documentary partnerships, high-end eco-tourism branding.",
        "tourism_potential": "South America's premier wildlife viewing and photography destination.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Camargue",
        "category": "Ramsar Wetlands",
        "why_flagship": "Rhône River delta; famous for wild white horses, black bulls, and flamingos.",
        "bhl_opportunities": ["French Mediterranean botanical studies", "18th-century wetland drainage maps"],
        "smithsonian_opportunities": ["European waterfowl records", "Early Provençal ethnographic notes"],
        "collection_potential": "Strong regional character and poetic animal imagery.",
        "commerce_potential": "Lifestyle branding, regional artisanal products, photography books.",
        "tourism_potential": "Top destination for European birding and horse-based tourism.",
        "discovery_value": 7, "collection_value": 8, "commerce_value": 9, "tourism_value": 8
    },
    {
        "name": "Sundarbans",
        "category": "Ramsar Wetlands",
        "why_flagship": "Largest mangrove forest in the world; critical tiger habitat and storm barrier.",
        "bhl_opportunities": ["British Raj botanical illustrations", "Bengal maritime charts"],
        "smithsonian_opportunities": ["South Asian mammal specimens", "Early mangrove ecology research"],
        "collection_potential": "Mysterious and high-stakes nature narratives (tigers and tides).",
        "commerce_potential": "Environmental resilience media, educational conservation campaigns.",
        "tourism_potential": "Niche destination for adventurous wildlife seekers.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 7, "tourism_value": 7
    },
    {
        "name": "Doñana",
        "category": "Ramsar Wetlands",
        "why_flagship": "Critical stopover for migratory birds; refuge for the Iberian Lynx.",
        "bhl_opportunities": ["Spanish ornithological catalogs", "Andalusia land-use maps"],
        "smithsonian_opportunities": ["Mediterranean ecosystem records", "Migratory bird tracking history"],
        "collection_potential": "European conservation flagship with rare species appeal.",
        "commerce_potential": "Sustainable agriculture branding, birding equipment.",
        "tourism_potential": "Major hub for European birdwatchers.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 7, "tourism_value": 9
    },
    {
        "name": "Lake Baikal",
        "category": "Ramsar Wetlands",
        "why_flagship": "Deepest and oldest lake on Earth; contains 20% of world's unfrozen surface freshwater.",
        "bhl_opportunities": ["Russian imperial scientific surveys", "Endemic nerpa seal sketches"],
        "smithsonian_opportunities": ["Siberian ethnology artifacts", "Freshwater biology records"],
        "collection_potential": "Extreme environment appeal; unique endemic biodiversity.",
        "commerce_potential": "Scientific media, pure water branding, cold-weather gear.",
        "tourism_potential": "Adventure travel destination for geologists and winter tourists.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 6, "tourism_value": 7
    },
    {
        "name": "Wadden Sea",
        "category": "Ramsar Wetlands",
        "why_flagship": "Largest unbroken system of intertidal sand and mud flats in the world.",
        "bhl_opportunities": ["North Sea malacology (shells) plates", "Coastal geomorphology maps"],
        "smithsonian_opportunities": ["Marine invertebrate collections", "European coastal history"],
        "collection_potential": "Subtle, minimalist coastal aesthetics; high scientific value.",
        "commerce_potential": "Eco-design, sustainable seafood branding, coastal education.",
        "tourism_potential": "Leading European destination for 'mudflat hiking' and nature study.",
        "discovery_value": 7, "collection_value": 8, "commerce_value": 7, "tourism_value": 9
    },
    {
        "name": "Danube Delta",
        "category": "Ramsar Wetlands",
        "why_flagship": "Best preserved European delta; major reed bed and pelican habitat.",
        "bhl_opportunities": ["Central European fish illustrations", "River navigation logs"],
        "smithsonian_opportunities": ["Balkan bird collections", "Early 20th-century wetland photography"],
        "collection_potential": "Lush, intricate riverine aesthetics.",
        "commerce_potential": "Eco-cruising, wildlife photography retreats.",
        "tourism_potential": "Premier European destination for birdwatching and boating.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 7, "tourism_value": 8
    },
    {
        "name": "Mekong Delta",
        "category": "Ramsar Wetlands",
        "why_flagship": "Biological treasure trove; critical for regional food security and aquatic culture.",
        "bhl_opportunities": ["Indochina botanical surveys", "Freshwater stingray sketches"],
        "smithsonian_opportunities": ["Southeast Asian fish specimens", "Agricultural heritage records"],
        "collection_potential": "Vibrant intersection of nature and human riverine life.",
        "commerce_potential": "Sustainable aquaculture branding, cultural travel media.",
        "tourism_potential": "Global destination for river culture and floating market experiences.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 8, "tourism_value": 10
    },

    # Category 3: Biosphere Reserves
    {
        "name": "Mount Kenya",
        "category": "Biosphere Reserves",
        "why_flagship": "Straddles the equator with glaciers; unique high-altitude afro-alpine flora.",
        "bhl_opportunities": ["Lobelia and Senecio botanical plates", "Early montane survey maps"],
        "smithsonian_opportunities": ["Mearns expedition bird specimens", "Equatorial mountain photography"],
        "collection_potential": "Stark, surreal mountain plant imagery.",
        "commerce_potential": "Mountaineering gear, high-altitude agriculture branding.",
        "tourism_potential": "Top destination for African peak-bagging and unique botany.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 7, "tourism_value": 9
    },
    {
        "name": "Monarch Butterfly BR",
        "category": "Biosphere Reserves",
        "why_flagship": "Site of one of nature's most spectacular insect migrations.",
        "bhl_opportunities": ["Lepidoptera life-cycle illustrations", "Early migration mapping"],
        "smithsonian_opportunities": ["Mexican insect collections", "Migration research records"],
        "collection_potential": "Extremely high visual appeal and emotional resonance.",
        "commerce_potential": "Educational kits, nature-inspired jewelry, garden products.",
        "tourism_potential": "Highly seasonal but massive density of nature tourism.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 9, "tourism_value": 8
    },
    {
        "name": "Bañados del Este",
        "category": "Biosphere Reserves",
        "why_flagship": "Extensive coastal wetlands and lagoons in Uruguay; critical for birds and ombu forests.",
        "bhl_opportunities": ["Pampas grass and ombu sketches", "Coastal avian illustrations"],
        "smithsonian_opportunities": ["Uruguayan bird specimens", "Wetland ecology studies"],
        "collection_potential": "Quiet, poetic South American coastal aesthetics.",
        "commerce_potential": "Sustainable wool/leather branding, eco-lodges.",
        "tourism_potential": "Emerging destination for South American birding.",
        "discovery_value": 6, "collection_value": 7, "commerce_value": 6, "tourism_value": 7
    },
    {
        "name": "Dana",
        "category": "Biosphere Reserves",
        "why_flagship": "Jordan's most diverse nature reserve; dramatic sandstone canyons and ancient history.",
        "bhl_opportunities": ["Middle Eastern desert flora studies", "Early archaeological site maps"],
        "smithsonian_opportunities": ["Levantine mammal records", "Biblical era archaeology photos"],
        "collection_potential": "Rich earth tones and desert-adapted life forms.",
        "commerce_potential": "Cultural heritage travel, desert-resilient product design.",
        "tourism_potential": "Premier trekking and community tourism hub in the Middle East.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 7, "tourism_value": 9
    },
    {
        "name": "Komodo",
        "category": "Biosphere Reserves",
        "why_flagship": "Home to the world's largest lizard; unique island ecosystem and marine wealth.",
        "bhl_opportunities": ["Varanus komodoensis anatomical sketches", "Sunda Islands marine charts"],
        "smithsonian_opportunities": ["Indonesian reptile specimens", "Early expedition journals"],
        "collection_potential": "High 'creature' appeal and dramatic island landscapes.",
        "commerce_potential": "Adventure media, conservation-led luxury travel.",
        "tourism_potential": "World-famous destination for wildlife and diving.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Cape West Coast",
        "category": "Biosphere Reserves",
        "why_flagship": "Part of the hyper-diverse Cape Floral Region; incredible seasonal wildflower blooms.",
        "bhl_opportunities": ["Fynbos botanical color plates", "Early Cape Colony maritime maps"],
        "smithsonian_opportunities": ["South African plant collections", "Heritage coastal photography"],
        "collection_potential": "Exquisite floral aesthetics; high design applicability.",
        "commerce_potential": "Botanical skincare, fine art prints, floral-themed luxury goods.",
        "tourism_potential": "Major seasonal hub for flower tourism and birding.",
        "discovery_value": 9, "collection_value": 10, "commerce_value": 9, "tourism_value": 9
    },
    {
        "name": "Sian Ka'an",
        "category": "Biosphere Reserves",
        "why_flagship": "Vast coastal reserve in Mexico; includes Mayan ruins, coral reefs, and tropical forests.",
        "bhl_opportunities": ["Yucatan Peninsula botanical surveys", "Caribbean reef illustrations"],
        "smithsonian_opportunities": ["Mayan archaeological records", "Tropical bird specimens"],
        "collection_potential": "Tropical lushness and ancient history combined.",
        "commerce_potential": "Sustainable beachwear, heritage-led hospitality.",
        "tourism_potential": "Top eco-destination for the Riviera Maya.",
        "discovery_value": 9, "collection_value": 9, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Clayoquot Sound",
        "category": "Biosphere Reserves",
        "why_flagship": "Iconic temperate rainforest of the Pacific Northwest; focus of major conservation battles.",
        "bhl_opportunities": ["Conifer botanical illustrations", "Marine mammal survey records"],
        "smithsonian_opportunities": ["Northwest Coast indigenous artifacts", "Pacific ecology studies"],
        "collection_potential": "High 'Old Growth' forest aesthetic; misty, deep-green themes.",
        "commerce_potential": "Outdoor gear, forest-bathing wellness products.",
        "tourism_potential": "Global center for whale watching and rainforest trekking.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Nilgiri",
        "category": "Biosphere Reserves",
        "why_flagship": "India's first biosphere reserve; critical for elephants, tigers, and diverse forest types.",
        "bhl_opportunities": ["Western Ghats floral studies", "Early tea plantation maps"],
        "smithsonian_opportunities": ["Indian mammal specimens", "Tribal ethnography records"],
        "collection_potential": "Rich forest biodiversity and cultural-agricultural heritage.",
        "commerce_potential": "Premium tea/coffee branding, forest-friendly textiles.",
        "tourism_potential": "Primary hub for South Indian wildlife and hill-station tourism.",
        "discovery_value": 8, "collection_value": 9, "commerce_value": 9, "tourism_value": 9
    },
    {
        "name": "Arganeraie",
        "category": "Biosphere Reserves",
        "why_flagship": "Unique argan forest ecosystem in Morocco; vital for local economy and desertification control.",
        "bhl_opportunities": ["Argan tree botanical sketches", "Moroccan semi-arid land surveys"],
        "smithsonian_opportunities": ["North African cultural artifacts", "Arid zone ecology studies"],
        "collection_potential": "Strong 'Tree of Life' motif; goats-in-trees visual appeal.",
        "commerce_potential": "Cosmetic branding (Argan oil), sustainable culinary products.",
        "tourism_potential": "Cultural and ecological tourism hub in Southern Morocco.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 10, "tourism_value": 9
    },

    # Category 4: UNESCO Global Geoparks
    {
        "name": "Katla",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "Dynamic volcanic landscape in Iceland; home to glaciers and active volcanoes.",
        "bhl_opportunities": ["19th-century Icelandic geological sketches", "Glacial movement records"],
        "smithsonian_opportunities": ["Volcanology specimens", "Arctic expedition photography"],
        "collection_potential": "High-contrast, dramatic earth-process imagery.",
        "commerce_potential": "Outdoor adventure media, geothermal technology branding.",
        "tourism_potential": "Core attraction for Icelandic geology and glacier tours.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Lesvos",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "Contains one of the world's most impressive petrified forests.",
        "bhl_opportunities": ["Paleobotanical fossil illustrations", "Aegean geological maps"],
        "smithsonian_opportunities": ["Petrified wood specimens", "Greek archaeological records"],
        "collection_potential": "Fascinating 'deep time' visuals; stone trees.",
        "commerce_potential": "Educational geology kits, Mediterranean travel media.",
        "tourism_potential": "Premier Greek destination for natural history.",
        "discovery_value": 8, "collection_value": 9, "commerce_value": 7, "tourism_value": 8
    },
    {
        "name": "Ngorongoro Lengai",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "Only geopark in Sub-Saharan Africa; massive caldera and the 'Mountain of God' volcano.",
        "bhl_opportunities": ["Volcanic ash soil studies", "Early Tanzanian rift maps"],
        "smithsonian_opportunities": ["African geological specimens", "Masai cultural records"],
        "collection_potential": "Combination of epic scale and unique geological chemistry.",
        "commerce_potential": "High-end geological tourism, documentary films.",
        "tourism_potential": "Global wildlife and geology superstar.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Reykjanes",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "Where the Mid-Atlantic Ridge rises above sea level; extreme rift valley geology.",
        "bhl_opportunities": ["Mid-ocean ridge geological diagrams", "Icelandic lichen studies"],
        "smithsonian_opportunities": ["Tectonic research records", "Early geothermal surveys"],
        "collection_potential": "Raw, primal earth-creation imagery.",
        "commerce_potential": "Renewable energy branding, extreme environment gear.",
        "tourism_potential": "First stop for most visitors to Iceland (Blue Lagoon nearby).",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Oki Islands",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "Unique evolution in the Sea of Japan; dramatic sea cliffs and ritual culture.",
        "bhl_opportunities": ["Japanese maritime botany", "Coastal erosion sketches"],
        "smithsonian_opportunities": ["Japanese mineral collections", "Local folklore/ethnography"],
        "collection_potential": "Serene and dramatic Japanese island aesthetics.",
        "commerce_potential": "Cultural-nature travel, marine-based wellness.",
        "tourism_potential": "High potential for slow-tourism and geological study.",
        "discovery_value": 7, "collection_value": 8, "commerce_value": 7, "tourism_value": 7
    },
    {
        "name": "Itoigawa",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "The jade capital of Japan; located on a major tectonic fault line.",
        "bhl_opportunities": ["Jadeite mineralogical plates", "Alpine flora of the Chubu region"],
        "smithsonian_opportunities": ["Japanese jade specimens", "Tectonic fault research"],
        "collection_potential": "High prestige material (jade) and tectonic drama.",
        "commerce_potential": "Jewelry branding, geological education, mountain tourism.",
        "tourism_potential": "Unique niche for mineral lovers and hikers.",
        "discovery_value": 8, "collection_value": 9, "commerce_value": 9, "tourism_value": 8
    },
    {
        "name": "Mudeungsan",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "Massive columnar jointing at high altitude; sacred mountain in South Korea.",
        "bhl_opportunities": ["Basalt columnar jointing diagrams", "Korean mountain flora"],
        "smithsonian_opportunities": ["Korean geological records", "Early Buddhist temple photography"],
        "collection_potential": "Geometric nature patterns and spiritual landscapes.",
        "commerce_potential": "Outdoor lifestyle, mindfulness/nature apps.",
        "tourism_potential": "Major hub for Korean mountain culture.",
        "discovery_value": 7, "collection_value": 8, "commerce_value": 7, "tourism_value": 9
    },
    {
        "name": "Marble Arch Caves",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "Classic karst landscape in Ireland/UK; stunning cave systems and boglands.",
        "bhl_opportunities": ["Speleological maps and sketches", "Peatland botanical studies"],
        "smithsonian_opportunities": ["Irish geological collections", "Early cave exploration photos"],
        "collection_potential": "Subterranean mystery and lush green surface landscapes.",
        "commerce_potential": "Subterranean tourism, environmental education.",
        "tourism_potential": "Key attraction for cross-border Irish tourism.",
        "discovery_value": 7, "collection_value": 7, "commerce_value": 7, "tourism_value": 8
    },
    {
        "name": "Batur",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "Double caldera volcano in Bali; center of sacred landscape and water management.",
        "bhl_opportunities": ["Balinese volcanic soil studies", "Tropical montane sketches"],
        "smithsonian_opportunities": ["Balinese cultural artifacts", "Early volcanic survey photos"],
        "collection_potential": "High-impact volcanic beauty and deep cultural integration.",
        "commerce_potential": "Spiritual travel, volcanic-grown agricultural products.",
        "tourism_potential": "Central to Bali's inland natural attractions.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Qeshm",
        "category": "UNESCO Global Geoparks",
        "why_flagship": "Largest island in the Persian Gulf; incredible salt caves and eroded 'Star Valley'.",
        "bhl_opportunities": ["Mangrove (Hara Forest) botanical sketches", "Persian Gulf marine charts"],
        "smithsonian_opportunities": ["Iranian mineral specimens", "Maritime cultural artifacts"],
        "collection_potential": "Surreal, arid-landscape aesthetics and unique maritime culture.",
        "commerce_potential": "Artisanal crafts, desert-island eco-tourism.",
        "tourism_potential": "Emerging destination for Middle Eastern nature travel.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 6, "tourism_value": 7
    },

    # Category 5: Dark Sky Places
    {
        "name": "Aoraki Mackenzie",
        "category": "Dark Sky Places",
        "why_flagship": "Premier southern hemisphere stargazing; spectacular alpine backdrop in New Zealand.",
        "bhl_opportunities": ["Southern sky star charts", "Alpine botanical illustrations"],
        "smithsonian_opportunities": ["Astrophotography heritage", "New Zealand expedition records"],
        "collection_potential": "High visual drama; stars over mountains.",
        "commerce_potential": "Astrophotography gear, luxury star-watching retreats.",
        "tourism_potential": "World leader in astro-tourism.",
        "discovery_value": 10, "collection_value": 8, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Cherry Springs",
        "category": "Dark Sky Places",
        "why_flagship": "One of the darkest spots in the US Eastern Seaboard.",
        "bhl_opportunities": ["Early American astronomical journals", "Appalachian forest surveys"],
        "smithsonian_opportunities": ["Early telescope history", "Pennsylvania wilderness photography"],
        "collection_potential": "Nostalgic 'dark night' appeal for urban populations.",
        "commerce_potential": "Camping gear, educational space content.",
        "tourism_potential": "Major regional hub for amateur astronomers.",
        "discovery_value": 7, "collection_value": 7, "commerce_value": 8, "tourism_value": 9
    },
    {
        "name": "Pic du Midi",
        "category": "Dark Sky Places",
        "why_flagship": "Historic observatory in the French Pyrenees; iconic 'frontier of science'.",
        "bhl_opportunities": ["Pyrenean mountain flora", "Early moon surface sketches"],
        "smithsonian_opportunities": ["Astronomical instrument collections", "Scientific expedition photos"],
        "collection_potential": "Scientific prestige and high mountain aesthetics.",
        "commerce_potential": "Precision optics, heritage travel branding.",
        "tourism_potential": "Top European destination for science-based tourism.",
        "discovery_value": 8, "collection_value": 9, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Kerry",
        "category": "Dark Sky Places",
        "why_flagship": "Gold tier reserve on the edge of Europe; rugged Atlantic coast scenery.",
        "bhl_opportunities": ["Irish coastal mosses and liverworts", "Early Atlantic weather logs"],
        "smithsonian_opportunities": ["Celtic archaeological records", "Early Irish photography"],
        "collection_potential": "Moody, evocative nightscapes and coastal wildness.",
        "commerce_potential": "Cultural-nature travel, moody landscape art.",
        "tourism_potential": "Central to Ireland's 'Wild Atlantic Way'.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 7, "tourism_value": 10
    },
    {
        "name": "Exmoor",
        "category": "Dark Sky Places",
        "why_flagship": "First Dark Sky Reserve in Europe; ancient moorland and dramatic sea cliffs.",
        "bhl_opportunities": ["Devonshire heathland botanical studies", "Red deer anatomical sketches"],
        "smithsonian_opportunities": ["British land-use history", "Heritage landscape photos"],
        "collection_potential": "Classic English wildness; pastoral but rugged.",
        "commerce_potential": "Outdoor apparel, regional heritage products.",
        "tourism_potential": "Major UK destination for walking and stargazing.",
        "discovery_value": 7, "collection_value": 7, "commerce_value": 8, "tourism_value": 9
    },
    {
        "name": "Mont-Mégantic",
        "category": "Dark Sky Places",
        "why_flagship": "First International Dark Sky Reserve; innovative light pollution control.",
        "bhl_opportunities": ["Quebec forest ecology surveys", "Northern sky maps"],
        "smithsonian_opportunities": ["Canadian scientific records", "Light pollution research data"],
        "collection_potential": "Science-conservation success story visuals.",
        "commerce_potential": "Smart lighting technology, eco-tourism media.",
        "tourism_potential": "Leading science-nature hub in Eastern Canada.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 7, "tourism_value": 9
    },
    {
        "name": "Zselic",
        "category": "Dark Sky Places",
        "why_flagship": "One of the best places for pristine starry skies in Central Europe.",
        "bhl_opportunities": ["Hungarian forest flora", "Central European owl studies"],
        "smithsonian_opportunities": ["Eastern European ethnography", "Forestry history"],
        "collection_potential": "Deep forest night mystery.",
        "commerce_potential": "Nature-themed hospitality, educational content.",
        "tourism_potential": "Key destination for Hungarian nature lovers.",
        "discovery_value": 6, "collection_value": 7, "commerce_value": 6, "tourism_value": 8
    },
    {
        "name": "Brecon Beacons",
        "category": "Dark Sky Places",
        "why_flagship": "Welsh mountain massif with dark, star-filled skies.",
        "bhl_opportunities": ["Welsh upland botanical surveys", "Early geological maps of Wales"],
        "smithsonian_opportunities": ["Welsh cultural history", "Industrial heritage records"],
        "collection_potential": "Powerful mountain silhouettes and ancient legends.",
        "commerce_potential": "Adventure travel, regional food branding.",
        "tourism_potential": "Premier Welsh destination for hiking and stargazing.",
        "discovery_value": 8, "collection_value": 7, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Namibrand",
        "category": "Dark Sky Places",
        "why_flagship": "One of the darkest places on earth; located in the ancient Namib desert.",
        "bhl_opportunities": ["Welwitschia mirabilis botanical plates", "Desert insect illustrations"],
        "smithsonian_opportunities": ["Namibian mineral collections", "Early desert photography"],
        "collection_potential": "Unearthly, high-concept desert-and-star visuals.",
        "commerce_potential": "Ultra-luxury eco-tourism, high-end photography.",
        "tourism_potential": "Top-tier destination for high-end wilderness seekers.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Central Idaho",
        "category": "Dark Sky Places",
        "why_flagship": "First Gold-Tier Dark Sky Reserve in the United States; rugged wilderness.",
        "bhl_opportunities": ["Rocky Mountain mammal sketches", "Wildfire ecology records"],
        "smithsonian_opportunities": ["American West expedition photos", "Nez Perce cultural records"],
        "collection_potential": "Pristine 'Old West' wilderness aesthetics.",
        "commerce_potential": "Premium outdoor gear, conservation media.",
        "tourism_potential": "Elite destination for North American wilderness fans.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 8, "tourism_value": 9
    },

    # Category 6: Intangible Heritage (Places)
    {
        "name": "Andalusia (Flamenco)",
        "category": "Intangible Heritage",
        "why_flagship": "Flamenco is deeply rooted in the landscape and history of Southern Spain.",
        "bhl_opportunities": ["Mediterranean aromatic plant studies", "Early agricultural maps"],
        "smithsonian_opportunities": ["Spanish folk music recordings", "Traditional costume artifacts"],
        "collection_potential": "High emotional intensity and vibrant cultural colors.",
        "commerce_potential": "Cultural travel, music/dance media, fashion.",
        "tourism_potential": "Global magnet for cultural tourism.",
        "discovery_value": 9, "collection_value": 9, "commerce_value": 10, "tourism_value": 10
    },
    {
        "name": "Oaxaca (Traditional Mexican Cuisine)",
        "category": "Intangible Heritage",
        "why_flagship": "Ancestral foodways integrated with biodiversity (maize, agaves).",
        "bhl_opportunities": ["Maize and Agave botanical varieties", "Cochineal dye history"],
        "smithsonian_opportunities": ["Pre-Columbian agricultural tools", "Traditional pottery"],
        "collection_potential": "Vibrant, 'earthy' aesthetics; food-culture focus.",
        "commerce_potential": "Culinary products, food-tourism branding.",
        "tourism_potential": "World-leading culinary destination.",
        "discovery_value": 9, "collection_value": 10, "commerce_value": 10, "tourism_value": 10
    },
    {
        "name": "Kyoto (Washoku)",
        "category": "Intangible Heritage",
        "why_flagship": "Japanese traditional dietary cultures; deep respect for nature and seasons.",
        "bhl_opportunities": ["Seasonal Japanese plant catalogs", "Seaweed/Algae illustrations"],
        "smithsonian_opportunities": ["Japanese culinary utensils", "Edo-period food prints"],
        "collection_potential": "Extreme refinement and aesthetic precision.",
        "commerce_potential": "High-end kitchenware, seasonal wellness products.",
        "tourism_potential": "Ultimate destination for cultural and culinary refinement.",
        "discovery_value": 10, "collection_value": 10, "commerce_value": 10, "tourism_value": 10
    },
    {
        "name": "Naples (Mediterranean Diet)",
        "category": "Intangible Heritage",
        "why_flagship": "A lifestyle based on local landscape and sustainable eating habits.",
        "bhl_opportunities": ["Vesuvius-region soil/flora surveys", "Early olive/vine sketches"],
        "smithsonian_opportunities": ["Italian maritime history", "Traditional farming tools"],
        "collection_potential": "Sun-drenched, health-focused Mediterranean visuals.",
        "commerce_potential": "Wellness apps, sustainable food brands.",
        "tourism_potential": "Global hub for lifestyle and culinary travel.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 10, "tourism_value": 10
    },
    {
        "name": "Marrakech (Falconry)",
        "category": "Intangible Heritage",
        "why_flagship": "Living human heritage; deep connection between birds of prey and desert landscapes.",
        "bhl_opportunities": ["Raptor anatomical plates", "North African desert ecology"],
        "smithsonian_opportunities": ["Berber cultural artifacts", "History of falconry equipment"],
        "collection_potential": "Dramatic, ancient-style desert-heritage visuals.",
        "commerce_potential": "Luxury travel, heritage leather goods.",
        "tourism_potential": "Iconic Moroccan cultural experience.",
        "discovery_value": 9, "collection_value": 9, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Kingston (Reggae)",
        "category": "Intangible Heritage",
        "why_flagship": "Music as a voice for social justice and cultural identity, born from the island's history.",
        "bhl_opportunities": ["Jamaican tropical flora", "Early Caribbean maritime charts"],
        "smithsonian_opportunities": ["Lomax folk music collections", "Jamaican social history records"],
        "collection_potential": "Vibrant, high-energy cultural icons.",
        "commerce_potential": "Music festivals, apparel, lifestyle media.",
        "tourism_potential": "Central to Jamaica's cultural identity and tourism.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 10, "tourism_value": 10
    },
    {
        "name": "Bahia (Capoeira)",
        "category": "Intangible Heritage",
        "why_flagship": "Afro-Brazilian martial art, dance, and music; symbol of resistance and grace.",
        "bhl_opportunities": ["Atlantic Forest botanical surveys", "Sugar plantation maps"],
        "smithsonian_opportunities": ["Afro-Brazilian artifacts", "Folk musical instruments (Berimbau)"],
        "collection_potential": "Dynamic human movement and powerful historical narrative.",
        "commerce_potential": "Fitness/wellness branding, cultural media.",
        "tourism_potential": "Key cultural draw for Salvador da Bahia.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Buenos Aires (Tango)",
        "category": "Intangible Heritage",
        "why_flagship": "An urban art form born from the fusion of cultures in the Rio de la Plata.",
        "bhl_opportunities": ["Pampas grasslands ecology", "Early port navigation charts"],
        "smithsonian_opportunities": ["Latin American music archives", "Early 20th-century urban photography"],
        "collection_potential": "Sophisticated, urban, and romantic aesthetics.",
        "commerce_potential": "Evening-wear fashion, luxury urban travel.",
        "tourism_potential": "Primary cultural attraction for Buenos Aires.",
        "discovery_value": 8, "collection_value": 9, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Bali (Wayang)",
        "category": "Intangible Heritage",
        "why_flagship": "Shadow puppetry reflecting deep philosophical and mythological traditions.",
        "bhl_opportunities": ["Balinese rice-paddy ecology", "Early tropical forest surveys"],
        "smithsonian_opportunities": ["Indonesian puppet collections", "Mythological scroll paintings"],
        "collection_potential": "Intricate, graphic-style shadow aesthetics.",
        "commerce_potential": "Home décor, high-end cultural storytelling media.",
        "tourism_potential": "Cornerstone of Balinese cultural tourism.",
        "discovery_value": 9, "collection_value": 10, "commerce_value": 8, "tourism_value": 10
    },
    {
        "name": "Kerala (Yoga)",
        "category": "Intangible Heritage",
        "why_flagship": "Ancient physical and spiritual practice deeply linked to the Indian landscape.",
        "bhl_opportunities": ["Ayurvedic medicinal plant plates", "Tropical backwater surveys"],
        "smithsonian_opportunities": ["South Asian spiritual artifacts", "History of science records"],
        "collection_potential": "Serene, health-focused, and ancient-wisdom visuals.",
        "commerce_potential": "Global wellness industry leader, sustainable apparel.",
        "tourism_potential": "World epicenter for wellness and spiritual tourism.",
        "discovery_value": 10, "collection_value": 10, "commerce_value": 10, "tourism_value": 10
    },

    # Category 7: Marine Protected Areas
    {
        "name": "Papahānaumokuākea",
        "category": "Marine Protected Areas",
        "why_flagship": "One of the largest MPAs in the world; sacred site for Native Hawaiians.",
        "bhl_opportunities": ["Pacific seabird illustrations", "Deep-sea coral sketches"],
        "smithsonian_opportunities": ["Albatross expedition marine records", "Hawaiian cultural artifacts"],
        "collection_potential": "High-purity ocean aesthetics; rare and remote species.",
        "commerce_potential": "Ocean conservation branding, scientific media.",
        "tourism_potential": "Extremely limited, enhancing its 'pristine' prestige.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 6, "tourism_value": 5
    },
    {
        "name": "Chagos",
        "category": "Marine Protected Areas",
        "why_flagship": "Contains some of the world's cleanest coral reefs and exceptional biodiversity.",
        "bhl_opportunities": ["Indian Ocean malacology (shells)", "Early nautical charts"],
        "smithsonian_opportunities": ["Tropical fish collections", "Oceanic research logs"],
        "collection_potential": "Vibrant and healthy reef imagery; conservation hope stories.",
        "commerce_potential": "Scientific research partnerships, high-end media.",
        "tourism_potential": "Primarily for researchers and explorers.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 5, "tourism_value": 4
    },
    {
        "name": "Phoenix Islands",
        "category": "Marine Protected Areas",
        "why_flagship": "First large, deep-water MPA to be established; critical climate research site.",
        "bhl_opportunities": ["Equatorial Pacific algae studies", "Deep-water fish plates"],
        "smithsonian_opportunities": ["Deep-sea biology records", "Early Pacific explorations"],
        "collection_potential": "Hidden depths and climate resilience themes.",
        "commerce_potential": "Sustainability-focused corporate partnerships.",
        "tourism_potential": "Minimal, high-exclusivity exploration.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 5, "tourism_value": 3
    },
    {
        "name": "Ross Sea",
        "category": "Marine Protected Areas",
        "why_flagship": "The 'Last Ocean'; most pristine marine ecosystem on Earth.",
        "bhl_opportunities": ["Antarctic penguin sketches", "Early ice-breaker journals"],
        "smithsonian_opportunities": ["Antarctic expedition specimens", "Polar research photography"],
        "collection_potential": "Dramatic ice-and-ocean aesthetics; extreme life.",
        "commerce_potential": "Extreme adventure branding, climate awareness.",
        "tourism_potential": "Top-tier destination for high-end Antarctic cruises.",
        "discovery_value": 10, "collection_value": 9, "commerce_value": 7, "tourism_value": 8
    },
    {
        "name": "Palau",
        "category": "Marine Protected Areas",
        "why_flagship": "Pioneer in marine conservation (the 'Palau Pledge'); world-famous Jellyfish Lake.",
        "bhl_opportunities": ["Micronesian coral reef surveys", "Invertebrate anatomical sketches"],
        "smithsonian_opportunities": ["Palauan cultural artifacts", "Early marine ecology studies"],
        "collection_potential": "Vibrant, friendly marine life imagery; high public appeal.",
        "commerce_potential": "Eco-tourism branding, sustainable swimwear.",
        "tourism_potential": "Global leader in high-value, low-impact diving tourism.",
        "discovery_value": 9, "collection_value": 9, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Raja Ampat",
        "category": "Marine Protected Areas",
        "why_flagship": "Global epicenter of marine biodiversity; the 'Crown Jewel' of the Coral Triangle.",
        "bhl_opportunities": ["Alfred Russel Wallace's specimen sketches", "Early Dutch East Indies charts"],
        "smithsonian_opportunities": ["Indo-Pacific fish collections", "Early expedition journals"],
        "collection_potential": "Incredible density and variety of marine visuals.",
        "commerce_potential": "Luxury diving gear, high-end nature photography.",
        "tourism_potential": "The ultimate global destination for marine biodiversity.",
        "discovery_value": 10, "collection_value": 10, "commerce_value": 9, "tourism_value": 10
    },
    {
        "name": "Tubbataha",
        "category": "Marine Protected Areas",
        "why_flagship": "Pristine coral reef in the Sulu Sea; example of successful remote reef management.",
        "bhl_opportunities": ["Philippines marine flora", "Turtle nesting site maps"],
        "smithsonian_opportunities": ["South East Asian marine records", "Early regional surveys"],
        "collection_potential": "High clarity and vibrant reef community visuals.",
        "commerce_potential": "Conservation-led travel gear, maritime media.",
        "tourism_potential": "World-class seasonal diving destination.",
        "discovery_value": 8, "collection_value": 8, "commerce_value": 7, "tourism_value": 9
    },
    {
        "name": "Ascension Island",
        "category": "Marine Protected Areas",
        "why_flagship": "Critical green turtle nesting site and unique Atlantic marine biodiversity.",
        "bhl_opportunities": ["Atlantic green turtle anatomical sketches", "Early volcanic island charts"],
        "smithsonian_opportunities": ["Ascension Island specimens", "Darwin-era records"],
        "collection_potential": "Remote Atlantic wildness; focal species appeal (turtles).",
        "commerce_potential": "Ocean conservation awareness, niche adventure media.",
        "tourism_potential": "Highly niche, focused on conservation and angling.",
        "discovery_value": 8, "collection_value": 7, "commerce_value": 5, "tourism_value": 5
    },
    {
        "name": "Marae Moana",
        "category": "Marine Protected Areas",
        "why_flagship": "Vast Cook Islands MPA; integrates traditional Polynesian conservation (Rā'ui).",
        "bhl_opportunities": ["Polynesian botanical surveys", "Canoe navigation charts"],
        "smithsonian_opportunities": ["Cook Islands cultural artifacts", "Early Pacific ethnography"],
        "collection_potential": "Integration of deep ocean and ancient maritime culture.",
        "commerce_potential": "Ethical jewelry, sustainable Pacific products.",
        "tourism_potential": "High-value cultural and marine tourism.",
        "discovery_value": 9, "collection_value": 9, "commerce_value": 7, "tourism_value": 9
    },
    {
        "name": "Kermadec",
        "category": "Marine Protected Areas",
        "why_flagship": "One of the few remaining large-scale pristine temperate marine environments.",
        "bhl_opportunities": ["Southern Pacific whale records", "Subtropical island botany"],
        "smithsonian_opportunities": ["Kermadec expedition specimens", "Deep-sea research records"],
        "collection_potential": "Dramatic, stormy southern ocean aesthetics.",
        "commerce_potential": "Research and scientific branding, extreme environment gear.",
        "tourism_potential": "Very limited; high scientific and prestige value.",
        "discovery_value": 9, "collection_value": 8, "commerce_value": 5, "tourism_value": 4
    }
]

def generate_portfolio():
    # 1. Calculate scores and add to records
    for record in PORTFOLIO_RECORDS:
        record["total_score"] = (
            record["discovery_value"] +
            record["collection_value"] +
            record["commerce_value"] +
            record["tourism_value"]
        )

    # 2. Rank records by total score
    ranked_portfolio = sorted(PORTFOLIO_RECORDS, key=lambda x: x["total_score"], reverse=True)

    # Ensure output directories exist
    output_dir = Path("data/curated")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3. Generate Markdown Report
    md_content = "# Nature & Culture Flagship Portfolio v1\n\n"
    md_content += "## Overview\n"
    md_content += "This portfolio curates 70 globally significant places and cultural practices, "
    md_content += "ranked by their potential for discovery, collection, commerce, and tourism within the Nature & Culture ecosystem.\n\n"
    
    md_content += "| Rank | Name | Category | Total Score | Discovery | Collection | Commerce | Tourism |\n"
    md_content += "|------|------|----------|-------------|-----------|------------|----------|---------|\n"
    
    for i, record in enumerate(ranked_portfolio, 1):
        md_content += f"| {i} | {record['name']} | {record['category']} | **{record['total_score']}** | {record['discovery_value']} | {record['collection_value']} | {record['commerce_value']} | {record['tourism_value']} |\n"
    
    md_content += "\n## Detailed Records\n\n"
    for i, record in enumerate(ranked_portfolio, 1):
        md_content += f"### {i}. {record['name']}\n"
        md_content += f"- **Category:** {record['category']}\n"
        md_content += f"- **Why it belongs:** {record['why_flagship']}\n"
        md_content += f"- **BHL Opportunities:** {', '.join(record['bhl_opportunities'])}\n"
        md_content += f"- **Smithsonian Opportunities:** {', '.join(record['smithsonian_opportunities'])}\n"
        md_content += f"- **Collection Potential:** {record['collection_potential']}\n"
        md_content += f"- **Commerce Potential:** {record['commerce_potential']}\n"
        md_content += f"- **Tourism Potential:** {record['tourism_potential']}\n"
        md_content += f"- **Scores:** Discovery: {record['discovery_value']}, Collection: {record['collection_value']}, Commerce: {record['commerce_value']}, Tourism: {record['tourism_value']}\n\n"

    with open(output_dir / "flagship_portfolio_v1.md", "w") as f:
        f.write(md_content)

    # 4. Generate JSON Payload
    json_data = {
        "version": "1.0.0",
        "total_records": len(ranked_portfolio),
        "records": ranked_portfolio
    }
    
    with open(output_dir / "flagship_portfolio_v1.json", "w") as f:
        json.dump(json_data, f, indent=2)

    print(f"Generated flagship_portfolio_v1.md and flagship_portfolio_v1.json in {output_dir}")

if __name__ == "__main__":
    generate_portfolio()
