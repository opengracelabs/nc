# NC-PLACES-001: First 100-Place Expansion Plan

| Field | Value |
|---|---|
| Document | NC-PLACES-001 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | Principal Architect |
| Supersedes | None |
| Ratification gate | Two-human sign-off required before any new place enters production |

---

## I. Purpose and Scope

This document defines the first 100-place candidate list for the Nature & Culture platform. It
is a planning and prioritization instrument, not a production authorization. No place on this
list is authorized for production until it completes the standard place activation sequence:
GeoNames ID resolution → Wikidata confirmation → content fixture → Gate E sign-off.

Places already in the pilot (Tier 0) carry their existing governance status. All other places
are candidates. IDs are not ratified here unless the place has an existing NC-DATA-* fixture.

**Governing doctrine:** PostgreSQL is authority. PostGIS is spatial discovery. Neo4j is
relationship discovery. AI is storytelling. Products are commerce.

**Illustration Opportunity Doctrine applies:** The commercial object is an Illustration
Opportunity, not a taxon. Golden age 1750–1900. Priority illustrators: Audubon, Gould, Merian,
Redouté, Lear, Nodder, Haeckel, Wolf.

---

## II. Selection Criteria

A place qualifies if it meets ≥3 of the following 5 signals:

1. **Heritage designation** — UNESCO WH, Biosphere Reserve, Ramsar, Geopark, National Park,
   Marine Protected Area, Dark Sky designation
2. **Illustration opportunity** — confirmed PD illustration content exists from the golden age
   (1750–1900) or strong landscape/survey tradition
3. **Commerce potential** — giclée, digital download, or print product feasible at launch price
4. **Content institution coverage** — at least one ratified NC institution can serve assets
5. **Geographic gap priority** — fills Africa, Asia-Pacific, Latin America, or Pacific coverage

---

## III. Coverage Matrix

| Region | Places | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Gap priority |
|---|---|---|---|---|---|---|
| North America — USA | 19 | 2 | 8 | 7 | 2 | Low (well-covered) |
| North America — Canada/Mexico | 6 | 0 | 1 | 3 | 2 | Medium |
| Caribbean & Central America | 5 | 0 | 1 | 2 | 2 | Medium |
| South America | 10 | 1 | 3 | 4 | 2 | **HIGH** |
| Europe | 12 | 1 | 4 | 5 | 2 | Low |
| Africa | 14 | 0 | 3 | 5 | 6 | **CRITICAL** |
| Middle East & West Asia | 2 | 0 | 0 | 1 | 1 | High |
| South Asia | 5 | 0 | 1 | 2 | 2 | **HIGH** |
| East & Southeast Asia | 8 | 0 | 2 | 3 | 3 | **HIGH** |
| Pacific & Oceania | 10 | 2 | 2 | 3 | 3 | **CRITICAL** |
| Polar & Extreme | 5 | 0 | 2 | 2 | 1 | Medium |
| Marine & Freshwater Icons | 3 | 0 | 0 | 1 | 2 | Medium |
| Planetary Special | 1 | 1 | 0 | 0 | 0 | — |
| **TOTAL** | **100** | **7** | **27** | **38** | **28** | — |

---

## IV. Institution Availability by Tier

| Institution | Code | Status | Primary geographic coverage |
|---|---|---|---|
| NHM London | NHM | Active (DD-NHM-001) | Africa, Pacific, SE Asia, Beagle/Cook voyages |
| National Gallery of Art | NGA | Active (DD-NGA-001) | American landscape, Hudson River School |
| Metropolitan Museum | Met | Active (DD-MET-001) | Japan, China, Europe, Near East |
| Art Institute of Chicago | AIC | Active (DD-AIC-001) | France, Impressionism, Pacific |
| Cleveland Museum of Art | CMA | Active (DD-CMA-001) | China, East Asia, manuscripts |
| Statens Museum for Kunst | SMK | Active (DD-SMK-001) | Scandinavia, Northern Europe |
| Walters Art Museum | Walters | Active (DD-WALTERS-001) | Illuminated manuscripts, Byzantine |
| Yale YCBA + YUAG | Yale | Active (DD-YALE-001) | Dutch Golden Age, British landscape |
| Getty Museum | Getty | Active (DD-GETTY-001) | Dutch/Flemish, European drawing |
| Minneapolis Institute of Art | Mia | Active (DD-MIA-001) | World collection, limited full-res |
| National Archives | NARA | Active (DD-NARA-001) | USA federal photography, maps |
| NOAA | NOAA | Active (DD-NOAA-001) | Ocean, coastal, marine |
| DPLA | DPLA | Active (DD-DPLA-001) | USA history, natural history |
| Europeana | Europeana | Active (DD-EUR) | European aggregator |
| Trove (NLA) | Trove | **Must Add** — not yet onboarded | Australia, Pacific, Cook voyage |
| Wellcome Collection | Wellcome | **Must Add** — not yet onboarded | Tropical medicine, anthropology |
| V&A | V&A | Should Add — not yet onboarded | Travel posters, decorative arts |
| MNHN Paris | MNHN | Should Add — not yet onboarded | French natural history, Africa |

---

## V. Master Candidate Table

| # | slug | Display Name | Country | Type | Tier | Risk |
|---|---|---|---|---|---|---|
| 01 | `earthrise` | Earthrise | — | Planetary / Cosmic viewpoint | 0 | Low |
| 02 | `yellowstone-national-park` | Yellowstone National Park | USA | National Park · UNESCO WH | 0 | Low |
| 03 | `grand-canyon-national-park` | Grand Canyon National Park | USA | National Park · UNESCO WH | 0 | Low |
| 04 | `great-barrier-reef` | Great Barrier Reef | Australia | Marine Park · UNESCO WH | 0 | Low |
| 05 | `papahanaumokuakea` | Papahānaumokuākea MNM | USA | Marine National Monument | 0 | Low |
| 06 | `venice` | Venice | Italy | Cultural Landscape · UNESCO WH | 0 | Low |
| 07 | `galapagos-islands` | Galápagos Islands | Ecuador | Archipelago · NP · UNESCO WH | 0 | Low |
| 08 | `yosemite-national-park` | Yosemite National Park | USA | National Park · UNESCO WH | 1 | Low |
| 09 | `everglades-national-park` | Everglades National Park | USA | National Park · Ramsar · UNESCO WH | 1 | Low |
| 10 | `tierra-del-fuego` | Tierra del Fuego | Argentina / Chile | National Park · Biosphere Reserve | 1 | Medium |
| 11 | `cape-of-good-hope` | Cape of Good Hope | South Africa | Nature Reserve | 1 | Low |
| 12 | `mount-fuji` | Mount Fuji | Japan | Cultural Landscape · UNESCO WH | 1 | Low |
| 13 | `fiordland-national-park` | Fiordland National Park | New Zealand | National Park · UNESCO WH | 1 | Low |
| 14 | `scottish-highlands` | Scottish Highlands | United Kingdom | Cultural Landscape / Region | 1 | Medium |
| 15 | `wadden-sea` | Wadden Sea | Netherlands / Germany / Denmark | UNESCO WH · Ramsar | 1 | Medium |
| 16 | `svalbard-archipelago` | Svalbard Archipelago | Norway | Archipelago / National Parks | 1 | Low |
| 17 | `serengeti-national-park` | Serengeti National Park | Tanzania | National Park · UNESCO WH | 1 | Low |
| 18 | `amazon-national-park` | Amazônia National Park | Brazil | National Park | 1 | Medium |
| 19 | `masoala-national-park` | Masoala National Park | Madagascar | National Park · UNESCO WH | 1 | Medium |
| 20 | `borneo-kinabatangan` | Kinabatangan Wildlife Sanctuary | Malaysia | Wildlife Sanctuary · Ramsar | 1 | Medium |
| 21 | `antarctic-peninsula` | Antarctic Peninsula | Antarctica | UNESCO / Treaty Zone | 1 | Low |
| 22 | `cape-floral-region` | Cape Floristic Region | South Africa | UNESCO WH · Biosphere Reserve | 1 | Low |
| 23 | `banff-national-park` | Banff National Park | Canada | National Park · UNESCO WH | 1 | Low |
| 24 | `okavango-delta` | Okavango Delta | Botswana | Ramsar · UNESCO WH | 1 | Low |
| 25 | `himalayas-sagarmatha` | Sagarmatha / Mount Everest | Nepal | National Park · UNESCO WH | 1 | Medium |
| 26 | `lake-baikal` | Lake Baikal | Russia | UNESCO WH | 1 | Low |
| 27 | `vatnajokull-national-park` | Vatnajökull National Park | Iceland | National Park · UNESCO WH | 1 | Low |
| 28 | `olympic-national-park` | Olympic National Park | USA | National Park · UNESCO WH | 2 | Low |
| 29 | `denali-national-park` | Denali National Park | USA | National Park | 2 | Low |
| 30 | `great-smoky-mountains-national-park` | Great Smoky Mountains NP | USA | National Park · UNESCO WH · Biosphere | 2 | Low |
| 31 | `redwood-national-park` | Redwood National and State Parks | USA | National Park · UNESCO WH | 2 | Low |
| 32 | `hawaii-volcanoes-national-park` | Hawaiʻi Volcanoes National Park | USA | National Park · UNESCO WH | 2 | Low |
| 33 | `channel-islands-national-park` | Channel Islands National Park | USA | National Park | 2 | Low |
| 34 | `acadia-national-park` | Acadia National Park | USA | National Park | 2 | Low |
| 35 | `death-valley-national-park` | Death Valley National Park | USA | National Park · Dark Sky | 2 | Low |
| 36 | `big-bend-national-park` | Big Bend National Park | USA | National Park · Dark Sky | 2 | Low |
| 37 | `glacier-national-park` | Glacier National Park | USA | National Park | 2 | Low |
| 38 | `florida-keys-national-marine-sanctuary` | Florida Keys NMS | USA | National Marine Sanctuary | 2 | Low |
| 39 | `okefenokee-national-wildlife-refuge` | Okefenokee NWR | USA | National Wildlife Refuge · Ramsar | 2 | Low |
| 40 | `cape-hatteras-national-seashore` | Cape Hatteras National Seashore | USA | National Seashore | 2 | Low |
| 41 | `monterey-bay-national-marine-sanctuary` | Monterey Bay NMS | USA | National Marine Sanctuary | 2 | Low |
| 42 | `boundary-waters-canoe-area` | Boundary Waters Canoe Area Wilderness | USA | Wilderness Area | 2 | Low |
| 43 | `banff-national-park` | (see #23) | — | — | — | — |
| 44 | `pacific-rim-national-park-reserve` | Pacific Rim National Park Reserve | Canada | National Park Reserve | 2 | Low |
| 45 | `nahanni-national-park-reserve` | Nahanni National Park Reserve | Canada | National Park · UNESCO WH | 2 | Low |
| 46 | `sian-kaan-biosphere-reserve` | Sian Ka'an Biosphere Reserve | Mexico | Biosphere Reserve · UNESCO WH | 2 | Medium |
| 47 | `monarch-butterfly-biosphere-reserve` | Monarch Butterfly Biosphere Reserve | Mexico | Biosphere Reserve · UNESCO WH | 2 | Low |
| 48 | `copper-canyon` | Copper Canyon (Barrancas del Cobre) | Mexico | Natural Region | 2 | Medium |
| 49 | `belize-barrier-reef-reserve-system` | Belize Barrier Reef Reserve System | Belize | Marine Reserve · UNESCO WH | 2 | Low |
| 50 | `blue-mountains-jamaica` | Blue and John Crow Mountains | Jamaica | National Park · UNESCO WH · Biosphere | 2 | Low |
| 51 | `cocos-island-national-park` | Cocos Island National Park | Costa Rica | National Park · UNESCO WH | 2 | Low |
| 52 | `monteverde-cloud-forest` | Monteverde Cloud Forest | Costa Rica | Biological Reserve | 2 | Low |
| 53 | `asa-wright-nature-centre` | Asa Wright Nature Centre | Trinidad & Tobago | Nature Reserve | 3 | Low |
| 54 | `pantanal` | Pantanal Conservation Area | Brazil / Bolivia / Paraguay | UNESCO WH · Ramsar | 2 | Medium |
| 55 | `iguazu-falls` | Iguazú / Iguaçu Falls | Argentina / Brazil | National Parks · UNESCO WH | 2 | Low |
| 56 | `torres-del-paine-national-park` | Torres del Paine National Park | Chile | National Park · Biosphere Reserve | 2 | Low |
| 57 | `atacama-desert` | Atacama Desert | Chile | Natural Region | 2 | Medium |
| 58 | `machu-picchu` | Machu Picchu | Peru | Cultural Landscape · UNESCO WH | 2 | Low |
| 59 | `manu-national-park` | Manu National Park | Peru | National Park · UNESCO WH · Biosphere | 2 | Low |
| 60 | `los-glaciares-national-park` | Los Glaciares National Park | Argentina | National Park · UNESCO WH | 2 | Low |
| 61 | `lake-district-national-park` | Lake District National Park | United Kingdom | National Park · UNESCO WH | 2 | Low |
| 62 | `camargue` | Camargue | France | Regional Nature Park · Ramsar | 2 | Low |
| 63 | `donana-national-park` | Doñana National Park | Spain | National Park · UNESCO WH · Ramsar | 2 | Low |
| 64 | `dolomites` | Dolomites | Italy | UNESCO WH | 2 | Low |
| 65 | `bialowieza-forest` | Białowieża Forest | Poland / Belarus | UNESCO WH · Biosphere Reserve | 2 | High |
| 66 | `danube-delta-biosphere-reserve` | Danube Delta | Romania / Ukraine | UNESCO WH · Ramsar · Biosphere | 2 | Medium |
| 67 | `plitvice-lakes-national-park` | Plitvice Lakes National Park | Croatia | National Park · UNESCO WH | 2 | Low |
| 68 | `jungfrau-aletsch` | Jungfrau-Aletsch | Switzerland | UNESCO WH | 2 | Low |
| 69 | `cairngorms-national-park` | Cairngorms National Park | United Kingdom | National Park | 2 | Low |
| 70 | `ngorongoro-conservation-area` | Ngorongoro Conservation Area | Tanzania | UNESCO WH | 2 | Low |
| 71 | `kruger-national-park` | Kruger National Park | South Africa | National Park | 2 | Low |
| 72 | `victoria-falls` | Victoria Falls | Zimbabwe / Zambia | UNESCO WH | 2 | Low |
| 73 | `virunga-national-park` | Virunga National Park | DRC | National Park · UNESCO WH | 3 | High |
| 74 | `bwindi-impenetrable-national-park` | Bwindi Impenetrable NP | Uganda | National Park · UNESCO WH | 3 | Medium |
| 75 | `namib-naukluft-national-park` | Namib-Naukluft National Park | Namibia | National Park · UNESCO WH | 3 | Low |
| 76 | `socotra-archipelago` | Socotra Archipelago | Yemen | Archipelago · UNESCO WH | 3 | High |
| 77 | `mount-kilimanjaro` | Mount Kilimanjaro | Tanzania | National Park · UNESCO WH | 3 | Low |
| 78 | `ahaggar-national-park` | Ahaggar National Park | Algeria | National Park | 3 | Medium |
| 79 | `wadi-rum` | Wadi Rum Protected Area | Jordan | Protected Area · UNESCO WH | 2 | Low |
| 80 | `arabian-oryx-sanctuary` | Arabian Oryx Sanctuary | Oman | Sanctuary · UNESCO WH | 3 | Low |
| 81 | `sundarbans` | Sundarbans | Bangladesh / India | National Park · UNESCO WH · Ramsar | 3 | Medium |
| 82 | `kaziranga-national-park` | Kaziranga National Park | India | National Park · UNESCO WH | 3 | Low |
| 83 | `manas-national-park` | Manas National Park | India / Bhutan | National Park · UNESCO WH | 3 | Medium |
| 84 | `royal-chitwan-national-park` | Chitwan National Park | Nepal | National Park · UNESCO WH | 3 | Low |
| 85 | `mount-fuji` | (see #12) | — | — | — | — |
| 86 | `shiretoko-national-park` | Shiretoko National Park | Japan | National Park · UNESCO WH | 2 | Low |
| 87 | `zhangjiajie-national-forest-park` | Zhangjiajie National Forest Park | China | National Forest Park | 3 | Medium |
| 88 | `jiuzhaigou-valley` | Jiuzhaigou Valley | China | Scenic Area · UNESCO WH | 3 | Medium |
| 89 | `komodo-national-park` | Komodo National Park | Indonesia | National Park · UNESCO WH | 3 | Low |
| 90 | `raja-ampat` | Raja Ampat | Indonesia | Marine Protected Area | 3 | Low |
| 91 | `ha-long-bay` | Hạ Long Bay | Vietnam | UNESCO WH | 3 | Low |
| 92 | `lord-howe-island` | Lord Howe Island | Australia | UNESCO WH | 3 | Low |
| 93 | `kakadu-national-park` | Kakadu National Park | Australia | National Park · UNESCO WH · Ramsar | 3 | Low |
| 94 | `daintree-national-park` | Daintree National Park | Australia | National Park · UNESCO WH | 3 | Low |
| 95 | `palau-national-marine-sanctuary` | Palau National Marine Sanctuary | Palau | Marine Sanctuary | 3 | Low |
| 96 | `easter-island-rapa-nui` | Easter Island / Rapa Nui | Chile | National Park · UNESCO WH | 2 | Low |
| 97 | `new-caledonia` | New Caledonia Lagoons | France | UNESCO WH | 3 | Medium |
| 98 | `ningaloo-reef` | Ningaloo Reef | Australia | Marine Park · UNESCO WH | 3 | Low |
| 99 | `lake-tanganyika` | Lake Tanganyika | Tanzania / DRC / Zambia / Burundi | Ramsar | 3 | Medium |
| 100 | `lake-titicaca` | Lake Titicaca | Peru / Bolivia | Ramsar | 3 | Medium |

*Note: Row 43 and Row 85 are duplicate references — Banff is #23, Mount Fuji is #12. These
rows are placeholders in the sequential numbering; the master count is 98 unique place slugs
plus 2 carry-forward references. Final slug list in §VIII resolves this to exactly 98 unique
places with #43 and #85 to be filled before ratification.*

---

## VI. Tier 0 — Pilot Active (7 places)

These places carry existing governance authorization. No new action required here.

| # | slug | GeoNames status | Wikidata status | Commerce status |
|---|---|---|---|---|
| 01 | `earthrise` | S-3 exempt | — | AUTHORIZED — NC-PROD-001/008 live |
| 02 | `yellowstone-national-park` | **RATIFIED** (5843591, PRKA) — NC-DATA-001 | Confirmed | Commerce-ready |
| 03 | `grand-canyon-national-park` | **RATIFIED** (5296401, PRKA) — NC-DATA-002/003 | Q220289 confirmed | Commerce-ready |
| 04 | `great-barrier-reef` | **RATIFIED** (2164628, H.RF) — NC-DATA-004/005 | Q7343 confirmed | Commerce-ready |
| 05 | `papahanaumokuakea` | Confirmation needed | Confirmation needed | Pilot phase |
| 06 | `venice` | Confirmation needed | Q641 (likely) | Pilot phase — Canaletto deferred |
| 07 | `galapagos-islands` | Confirmation needed | Q34425 (likely) | Pilot phase |

---

## VII. Detailed Entries — Tier 1 (27 places, #08–#27)

---

### 08 · Yosemite National Park

| | |
|---|---|
| **slug** | `yosemite-national-park` |
| **place_type** | National Park · UNESCO World Heritage |
| **country** | USA |
| **region** | Sierra Nevada, California |
| **collection_theme** | The American Sublime — Valley, Rock, and Wilderness Light |
| **why** | Anchor of Hudson River School landscape painting tradition. Bierstadt's monumental Yosemite canvases are held at NGA. Carleton Watkins' 1861 survey photographs (DPLA) established the photographic landscape canon. John Muir's conservation voice. NARA holds USGS survey maps. |
| **content_sources** | NGA (Bierstadt, Moran — landscape oil), DPLA (Carleton Watkins survey photography, early conservation pamphlets), NARA (USGS Yosemite survey maps, 1860s–) |
| **product_potential** | **High** — large-format giclée of Bierstadt oil paintings; survey photography archival prints |
| **authority_checks** | GeoNames PRKA confirmation required · Wikidata Q23919 confirmation required |
| **risk** | Low |

---

### 09 · Everglades National Park

| | |
|---|---|
| **slug** | `everglades-national-park` |
| **place_type** | National Park · Ramsar Wetland · UNESCO World Heritage |
| **country** | USA |
| **region** | South Florida |
| **collection_theme** | Audubon's Wilderness — Wading Birds and River of Grass |
| **why** | Audubon painted Florida wading birds in the Everglades region; plates from *The Birds of America* (1827–1838) are the defining illustration set. NHM holds original Havell aquatints. DPLA has Florida natural history records. NARA holds early National Park Service documentation. |
| **content_sources** | NHM (Audubon *Birds of America* aquatints), DPLA (Florida natural history), NARA (NPS survey photography, 1940s–) |
| **product_potential** | **High** — Audubon wading bird plates (Roseate Spoonbill, Great Blue Heron, Snowy Egret) are flagship commerce assets |
| **authority_checks** | GeoNames PRKA confirmation required · Wikidata Q193540 confirmation required |
| **risk** | Low |

---

### 10 · Tierra del Fuego

| | |
|---|---|
| **slug** | `tierra-del-fuego` |
| **place_type** | National Park · Biosphere Reserve · Archipelago |
| **country** | Argentina / Chile (bi-national) |
| **region** | Southern Cone |
| **collection_theme** | The Uttermost Part of the Earth — Beagle Voyage and Sub-Antarctic Wilderness |
| **why** | FitzRoy and Darwin's second Beagle voyage (1831–36) spent months charting Tierra del Fuego. NHM holds the primary Beagle voyage natural history illustrations. Conrad Martens produced watercolour landscapes from the voyage. This is one of NHM's highest-priority illustration sets for NC. |
| **content_sources** | NHM (Beagle voyage plates, Conrad Martens watercolours, FitzRoy survey charts), Europeana (expedition records) |
| **product_potential** | **High** — Beagle voyage botanical and zoological plates; Martens sub-Antarctic landscapes |
| **authority_checks** | Scope required: anchor to Tierra del Fuego National Park (Argentine side) · GeoNames PRKA/ADM1 disambiguation · Cross-border: Chilean sector separate slug or unified? Decision needed before ratification |
| **risk** | Medium (cross-border scope) |

---

### 11 · Cape of Good Hope

| | |
|---|---|
| **slug** | `cape-of-good-hope` |
| **place_type** | Nature Reserve · UNESCO WH component (Cape Floral Region) |
| **country** | South Africa |
| **region** | Western Cape |
| **collection_theme** | The Tip of Africa — Cape Botanicals and Sea Routes |
| **why** | The Cape was a primary stopping point for 18th-century naturalists en route to the East Indies and Pacific. Levaillant, Sparrman, Masson, and Thunberg all worked the Cape flora. NHM holds Cape botanical illustration sets of extraordinary quality. The Cape Floral Region is the most species-rich temperate flora on Earth. |
| **content_sources** | NHM (Levaillant *Oiseaux d'Afrique*, Cape botanical surveys, Masson drawings), Europeana (Dutch East India Company natural history) |
| **product_potential** | **High** — Cape protea and fynbos botanical illustration; Levaillant African bird plates |
| **authority_checks** | GeoNames: Cape of Good Hope Nature Reserve vs. Cape Point disambiguation required · Wikidata Q148784 confirmation required · Relationship to Cape Floral Region (#22) must be defined |
| **risk** | Low |

---

### 12 · Mount Fuji

| | |
|---|---|
| **slug** | `mount-fuji` |
| **place_type** | Cultural Landscape · UNESCO World Heritage |
| **country** | Japan |
| **region** | Honshu |
| **collection_theme** | Thirty-Six Views — Hokusai, Hiroshige, and the Mountain |
| **why** | Met Museum holds the world's finest public-domain collection of Hokusai and Hiroshige ukiyo-e woodblock prints depicting Fuji. The *Thirty-Six Views of Mount Fuji* series (Hokusai, c. 1831) is NC's highest-value Japan illustration set. CMA and Mia also hold prints. |
| **content_sources** | Met (Hokusai, Hiroshige ukiyo-e woodblocks — CC0 confirmed), CMA (East Asian prints), Mia (Japanese woodblock) |
| **product_potential** | **High** — Hokusai's *The Great Wave* and Fuji views are among the most commercially proven public-domain images globally |
| **authority_checks** | GeoNames MT/VLC confirmation required · Wikidata Q39231 confirmation required |
| **risk** | Low |

---

### 13 · Fiordland National Park

| | |
|---|---|
| **slug** | `fiordland-national-park` |
| **place_type** | National Park · UNESCO World Heritage |
| **country** | New Zealand |
| **region** | Southland / Te Anau |
| **collection_theme** | Cook's South Seas — Parkinson, Banks, and the Voyage to Aotearoa |
| **why** | Joseph Banks and Sydney Parkinson's botanical illustrations from Cook's first voyage (1769–70) include the earliest European natural history documentation of New Zealand. NHM holds the Parkinson originals. The fiordlands are among the most dramatic landscapes in the southern hemisphere. Fills Pacific gap. |
| **content_sources** | NHM (Parkinson botanical drawings — Cook voyage, Banks Florilegium plates), Europeana (Royal Society voyage records) |
| **product_potential** | **High** — Parkinson *New Zealand flora* plates are museum-quality giclée candidates |
| **authority_checks** | GeoNames PRKA confirmation required · Wikidata Q901648 confirmation required · Boundary: Te Wahipounamu UNESCO site vs. Fiordland NP alone — clarify scope |
| **risk** | Low |

---

### 14 · Scottish Highlands

| | |
|---|---|
| **slug** | `scottish-highlands` |
| **place_type** | Cultural Landscape / Region |
| **country** | United Kingdom |
| **region** | Scotland |
| **collection_theme** | The Romantic Wilderness — Highland Nature and Victorian Natural History |
| **why** | Victorian British natural history publishing is heavily anchored in the Highlands. Gould's *Birds of Great Britain* includes Highland species. SMK, Yale, and Getty hold European landscape painting. Europeana has extensive British natural history illustration from this period. Strong Romantic landscape tradition (Landseer, Turner). |
| **content_sources** | Europeana (Victorian natural history, Gould British birds), SMK (Northern European landscape), Yale (British landscape tradition), NHM (British natural history illustration) |
| **product_potential** | **High** — Highland stag and Victorian nature art; Gould British bird plates |
| **authority_checks** | Scope required: "Scottish Highlands" is a cultural region, not an administrative unit. Anchor to Highland Council area or use Cairngorms NP (#69) as the bounded component. GeoNames ADM2 disambiguation needed. |
| **risk** | Medium (scope ambiguity — region vs. bounded unit) |

---

### 15 · Wadden Sea

| | |
|---|---|
| **slug** | `wadden-sea` |
| **place_type** | UNESCO World Heritage · Ramsar Wetland |
| **country** | Netherlands / Germany / Denmark |
| **region** | North Sea coast |
| **collection_theme** | Dutch Golden Age Coast — Tidal Flats, Seabirds, and Maritime Painting |
| **why** | The Wadden Sea is the heartland of the Dutch Golden Age coastal painting tradition. SMK holds Danish sea paintings. Getty and Yale hold Dutch Golden Age seascapes. Ecological importance as the world's largest intertidal mudflat system makes it a strong conservation story. |
| **content_sources** | SMK (Danish coastal/seabird painting), Getty (Dutch Golden Age seascapes), Yale (Dutch marine tradition), Europeana (natural history of North Sea) |
| **product_potential** | **High** — Dutch Golden Age seascape paintings are proven commerce assets |
| **authority_checks** | Cross-border UNESCO site: GeoNames ID for the trinational site area — authority disambiguation required. Three separate national components or unified international slug? Recommend unified slug anchored to the UNESCO nomination boundary. |
| **risk** | Medium (tri-national boundary) |

---

### 16 · Svalbard Archipelago

| | |
|---|---|
| **slug** | `svalbard-archipelago` |
| **place_type** | Archipelago / National Parks |
| **country** | Norway |
| **region** | Arctic Ocean |
| **collection_theme** | Arctic Wilderness — Expedition Art and the Far North |
| **why** | Svalbard is a primary site for Arctic expedition illustration (17th–19th century). Walrus and polar bear hunting voyages produced natural history records. William Scoresby's *Account of the Arctic Regions* (1820) illustrations are in European collections. NHM holds Arctic expedition material. SMK has Scandinavian Arctic tradition. Dark Sky reserve. |
| **content_sources** | NHM (Arctic expedition plates, walrus/polar bear natural history), SMK (Norwegian Arctic painting), Europeana (Dutch/British Arctic expedition records) |
| **product_potential** | **High** — Arctic expedition illustrations, polar bear and walrus plates |
| **authority_checks** | GeoNames ADM1 (Svalbard as Norwegian territory) · Wikidata Q25230 confirmation required · Distinct from Spitsbergen island — scope should be archipelago-level |
| **risk** | Low |

---

### 17 · Serengeti National Park

| | |
|---|---|
| **slug** | `serengeti-national-park` |
| **place_type** | National Park · UNESCO World Heritage |
| **country** | Tanzania |
| **region** | East Africa |
| **collection_theme** | African Plains — Migration, Predators, and Early Exploration |
| **why** | NHM holds significant East African natural history illustration from 19th-century exploration (Sclater, Hartlaub, Reichenow). Fills critical Africa gap. The Serengeti-Mara ecosystem is the planet's most iconic wildlife landscape. Haeckel's East African plates extend coverage. |
| **content_sources** | NHM (East African natural history, Haeckel East Africa plates, exploration records), Europeana (German East Africa expedition material) |
| **product_potential** | **High** — African bird and mammal illustration plates; landscape tradition |
| **authority_checks** | GeoNames PRKA confirmation required · Wikidata Q43267 confirmation required · Boundary: distinct from Ngorongoro (#70) and Masai Mara (Kenya) — confirm NP boundary only |
| **risk** | Low |

---

### 18 · Amazônia National Park

| | |
|---|---|
| **slug** | `amazon-national-park` |
| **place_type** | National Park |
| **country** | Brazil |
| **region** | Pará state, Amazon Basin |
| **collection_theme** | The Green Continent — Humboldt, Wallace, and Amazonian Natural History |
| **why** | Humboldt's expedition illustrations (1799–1804) and Wallace's Amazon travels (1848–52) produced the defining visual record of Amazonian biodiversity. NHM holds Wallace originals. Europeana has Humboldt expedition plates. Anchoring to Amazônia NP (oldest national park in Brazil, 1974) provides a governable boundary. |
| **content_sources** | NHM (Wallace *Palm Trees of the Amazon*, Amazon natural history), Europeana (Humboldt expedition plates, Spruce botanical drawings) |
| **product_potential** | **High** — Humboldt illustration plates; Wallace botanical drawings; tropical bird and mammal plates |
| **authority_checks** | GeoNames PRKA for Amazônia NP (Brazil) · Wikidata Q193291 · Note: "Amazon" is too broad — slug anchored to the national park, not the basin. Basin-level is a separate scope decision. |
| **risk** | Medium (scope: NP vs. basin) |

---

### 19 · Masoala National Park

| | |
|---|---|
| **slug** | `masoala-national-park` |
| **place_type** | National Park · UNESCO World Heritage (Rainforests of Atsinanana) |
| **country** | Madagascar |
| **region** | Toamasina Province |
| **collection_theme** | The Island at the End of the World — Lemurs, Chameleons, and Commerson's Botany |
| **why** | Madagascar has the highest endemic species rate in the world. Philibert Commerson and Pierre Sonnerat produced 18th-century illustration records. Buffon's *Histoire Naturelle* includes Madagascar plates (Gallica RESEARCH ONLY — Gallica disqualified from production, DD-GALLICA-003). NHM fills the institution gap here. Fills Africa gap. |
| **content_sources** | NHM (Madagascar natural history illustration, Commerson/Sonnerat records), Europeana (French colonial natural history — rights check required per item) |
| **product_potential** | **High** — lemur plates, chameleon illustration, Commerson botanical drawings |
| **authority_checks** | GeoNames PRKA confirmation required · Wikidata Q1033099 · Rights check: Europeana items need per-item Europeana Rights Matrix v1 screening |
| **risk** | Medium (Gallica production blocked — Europeana path only) |

---

### 20 · Kinabatangan Wildlife Sanctuary

| | |
|---|---|
| **slug** | `borneo-kinabatangan` |
| **place_type** | Wildlife Sanctuary · Ramsar Wetland |
| **country** | Malaysia (Sabah) |
| **region** | Borneo / Southeast Asia |
| **collection_theme** | Wallace's Malay Archipelago — Orang-utans, Proboscis Monkeys, and Evolution's Edge |
| **why** | Alfred Russel Wallace spent years in Borneo documenting species that independently led him to natural selection. NHM holds Wallace's original specimens and illustration references. *The Malay Archipelago* (1869) is a primary NC illustration source. Fills critical Asia-Pacific gap. |
| **content_sources** | NHM (Wallace Malay Archipelago illustrations, Borneo natural history), Europeana (Dutch colonial Borneo natural history) |
| **product_potential** | **High** — orang-utan and proboscis monkey illustration; Wallace botanical plates; bird-of-paradise from Aru Islands adjacent collection |
| **authority_checks** | GeoNames confirmation required · Wikidata Q1470074 · Scope: Kinabatangan floodplain vs. Danum Valley — clarify NC anchor point |
| **risk** | Medium (scope: several distinct protected areas in Sabah) |

---

### 21 · Antarctic Peninsula

| | |
|---|---|
| **slug** | `antarctic-peninsula` |
| **place_type** | Antarctic Treaty Zone / Protected Area |
| **country** | Antarctica (international) |
| **region** | Southern Ocean |
| **collection_theme** | The Last Continent — Expedition Art and the Age of Antarctic Exploration |
| **why** | The Heroic Age of Antarctic Exploration (1897–1922) produced the most extraordinary expedition illustration record of any region. Edward Wilson's watercolours from Scott's expeditions. NHM holds primary expedition records. Haeckel's Radiolaria and medusa illustrations originate from Southern Ocean expeditions. |
| **content_sources** | NHM (Edward Wilson watercolours, Scott expedition records, Challenger expedition plates), Europeana (Shackleton/Amundsen expedition records) |
| **product_potential** | **High** — Wilson penguin and ice-shelf watercolours are museum-quality giclée candidates |
| **authority_checks** | No GeoNames sovereign boundary (Antarctic Treaty). Scope as geographic region rather than political unit. S-3 equivalent exception may apply. Wikidata Q21590 (Antarctic Peninsula) confirmation. |
| **risk** | Low (no sovereignty dispute over the peninsula itself for content purposes) |

---

### 22 · Cape Floristic Region

| | |
|---|---|
| **slug** | `cape-floral-region` |
| **place_type** | UNESCO World Heritage · Biosphere Reserve |
| **country** | South Africa |
| **region** | Western Cape |
| **collection_theme** | Fynbos — The Most Species-Rich Temperate Flora on Earth |
| **why** | The Cape Floristic Region is home to over 9,000 plant species, the highest density outside of tropical forest. Francis Masson (Kew, 1772–75) and Carl Peter Thunberg produced the primary 18th-century botanical record. NHM holds extensive Cape botanical illustration from this period. Proteas and ericas are among the most commercially striking botanical illustration subjects. |
| **content_sources** | NHM (Masson Cape botanical drawings, Thunberg records), Europeana (Kew Gardens Cape correspondence) |
| **product_potential** | **High** — Cape protea, sugarbush, and leucadendron botanical prints are high-value commerce assets |
| **authority_checks** | GeoNames: Cape Floristic Region is a UNESCO WH site — confirm specific GeoNames ID vs. component reserves · Wikidata Q218296 · Relationship to Cape of Good Hope (#11) must be defined in graph |
| **risk** | Low |

---

### 23 · Banff National Park

| | |
|---|---|
| **slug** | `banff-national-park` |
| **place_type** | National Park · UNESCO World Heritage |
| **country** | Canada |
| **region** | Alberta, Canadian Rockies |
| **collection_theme** | The Canadian Sublime — Rocky Mountain Survey and Wilderness Photography |
| **why** | Canadian Pacific Railway survey photography (1880s–90s) produced a defining visual record of the Rockies. DPLA and NARA hold early Canadian Rockies survey material. Banff is the oldest Canadian national park (1885). Lucius O'Brien and the Canadian Rockies painters are in Europeana. |
| **content_sources** | DPLA (Canadian Rockies survey photography), NARA (US border survey maps), Europeana (O'Brien and Canadian landscape painting) |
| **product_potential** | **High** — Rocky Mountain survey photography; Canadian landscape oil paintings |
| **authority_checks** | GeoNames PRKA confirmation required · Wikidata Q131625 confirmation required |
| **risk** | Low |

---

### 24 · Okavango Delta

| | |
|---|---|
| **slug** | `okavango-delta` |
| **place_type** | UNESCO World Heritage · Ramsar Wetland |
| **country** | Botswana |
| **region** | Southern Africa |
| **collection_theme** | The River that Never Reaches the Sea — Africa's Inland Delta |
| **why** | The Okavango is Africa's largest inland delta and a critical biodiversity refuge. 19th-century Southern African exploration illustrations (Livingstone, Baldwin) passed through the region. NHM holds Southern African natural history illustration. Fills critical Africa gap. |
| **content_sources** | NHM (Southern African natural history, bird plates, Livingstone expedition records), Europeana (Southern Africa exploration) |
| **product_potential** | **Medium** — African bird plates tied to the delta ecosystem; landscape illustration secondary |
| **authority_checks** | GeoNames: Okavango Delta — waterway system vs. Moremi GR disambiguation required · Wikidata Q179654 · Not a National Park: Moremi is the bounded NP component |
| **risk** | Low |

---

### 25 · Sagarmatha National Park (Mount Everest region)

| | |
|---|---|
| **slug** | `himalayas-sagarmatha` |
| **place_type** | National Park · UNESCO World Heritage |
| **country** | Nepal |
| **region** | Khumbu, Eastern Nepal |
| **collection_theme** | The Roof of the World — Himalayan Botanical Survey and Alpine Illustration |
| **why** | Joseph Hooker's *Himalayan Journals* and *Rhododendrons of Sikkim-Himalaya* (1849–51) are among the most important 19th-century botanical illustration works. NHM holds the Hooker originals. The Himalayas are the most biodiverse mountain system on Earth. Fills Asia-Pacific gap. |
| **content_sources** | NHM (Hooker Himalayan rhododendron plates, *Flora of British India* illustrations), Europeana (Survey of India botanical records) |
| **product_potential** | **High** — Hooker rhododendron plates are museum-quality commerce assets; Himalayan alpine botanical illustration |
| **authority_checks** | GeoNames PRKA for Sagarmatha NP confirmation required · Wikidata Q27394 · Slug disambiguation: "himalayas" is too broad — Sagarmatha NP is the governable anchor |
| **risk** | Medium (scope: NP vs. broader Himalayan range) |

---

### 26 · Lake Baikal

| | |
|---|---|
| **slug** | `lake-baikal` |
| **place_type** | UNESCO World Heritage |
| **country** | Russia |
| **region** | Siberia |
| **collection_theme** | The Sacred Sea — Russian Imperial Natural History and the World's Oldest Lake |
| **why** | Lake Baikal contains 20% of the world's freshwater and the highest freshwater biodiversity density on Earth. Russian Imperial expeditions (Gmelin, Pallas) produced detailed 18th-century natural history records now in Europeana. |
| **content_sources** | Europeana (Russian Imperial natural history expedition plates, Pallas Siberian botanical illustrations) |
| **product_potential** | **Medium** — Pallas Siberian flora and fauna plates; Baikal seal (*nerpa*) illustration |
| **authority_checks** | GeoNames LK confirmation required · Wikidata Q5513 confirmation required |
| **risk** | Low |

---

### 27 · Vatnajökull National Park

| | |
|---|---|
| **slug** | `vatnajokull-national-park` |
| **place_type** | National Park · UNESCO World Heritage |
| **country** | Iceland |
| **region** | Southeast Iceland |
| **collection_theme** | Fire and Ice — Iceland's Volcanic Wilderness and the Norse Natural Imagination |
| **why** | Iceland's volcanic and glacial landscape attracted European scientific expedition from the 18th century. SMK holds Scandinavian natural illustration. Vatnajökull is Europe's largest glacier. Sir Joseph Banks visited Iceland in 1772 and produced botanical records now in NHM. |
| **content_sources** | NHM (Banks Iceland botanical 1772), SMK (Scandinavian natural landscape), Europeana (Danish-era Iceland illustration) |
| **product_potential** | **Medium** — Icelandic flora illustration; volcanic landscape tradition; SMK Northern landscape |
| **authority_checks** | GeoNames PRKA confirmation required · Wikidata Q245016 confirmation required |
| **risk** | Low |

---

## VIII. Tier 2 Entries — Selected Detail (places #28–#100)

Tier 2 entries follow the same authority requirements. Key details only.

| # | slug | Collection theme | Primary content source | Product potential | Authority note |
|---|---|---|---|---|---|
| 28 | `olympic-national-park` | Temperate Rainforest and Pacific Rim Wilderness | DPLA, NARA | Medium | GeoNames PRKA |
| 29 | `denali-national-park` | The Great Land — Alaskan Wilderness Survey | DPLA, NARA | Medium | GeoNames PRKA |
| 30 | `great-smoky-mountains-national-park` | Appalachian Spring — Cherokee Heritage and Eastern Wilderness | DPLA, NHM (eastern US flora) | Medium | GeoNames PRKA |
| 31 | `redwood-national-park` | Ancient Giants — Coast Redwood and California Natural History | DPLA, NHM | Medium | GeoNames PRKA |
| 32 | `hawaii-volcanoes-national-park` | Pele's Landscape — Hawaiian Lava, Flora, and Polynesian Natural History | NHM (Cook voyage Hawaii), NOAA, NARA | High | GeoNames PRKA |
| 33 | `channel-islands-national-park` | California's Galápagos — Island Endemism and Maritime Survey | NHM, DPLA | Medium | GeoNames PRKA · Scope: 5 islands unified or per-island? |
| 34 | `acadia-national-park` | The Rock Coast — New England Landscape Painting Tradition | NGA (East Coast landscape), DPLA | High | GeoNames PRKA |
| 35 | `death-valley-national-park` | Basin and Range — Desert Survey and Geological Illustration | NARA (USGS survey), DPLA | Medium | GeoNames PRKA · Dark Sky reserve |
| 36 | `big-bend-national-park` | The Great Bend — Chihuahuan Desert and Texas Natural History | NARA, DPLA | Medium | GeoNames PRKA · Dark Sky reserve |
| 37 | `glacier-national-park` | Going-to-the-Sun — Rocky Mountain Survey and Northern Wilderness | NGA, DPLA, NARA | High | GeoNames PRKA |
| 38 | `florida-keys-national-marine-sanctuary` | Audubon's Reef — Florida Keys Natural History and Coral Illustration | NHM (Audubon), NOAA | High | GeoNames NMS boundary |
| 39 | `okefenokee-national-wildlife-refuge` | Audubon's Swamp — Southern Wetlands and Bird Illustration | NHM (Audubon southeastern plates), DPLA | High | GeoNames NWR confirmation |
| 40 | `cape-hatteras-national-seashore` | Outer Banks — Coastal Survey and Atlantic Bird Migration | NARA (Coast Survey charts), DPLA, NHM | Medium | GeoNames NS confirmation |
| 41 | `monterey-bay-national-marine-sanctuary` | The Kelp Forest — Pacific Coast Natural History | NOAA, NHM | Medium | GeoNames NMS boundary |
| 42 | `boundary-waters-canoe-area` | The Boreal Interior — Canadian Shield and Northern Wilderness | DPLA, NARA | Medium | GeoNames WA confirmation |
| 44 | `pacific-rim-national-park-reserve` | Northwest Coast — Haida Maritime Landscape and Rain Forest | NHM (Cook/Banks Pacific), Europeana | Medium | GeoNames PRKA · Indigenous cultural layer — consult |
| 45 | `nahanni-national-park-reserve` | Wild Rivers — Canada's Northern Wilderness and Cave Systems | DPLA, NARA | Low | GeoNames PRKA |
| 46 | `sian-kaan-biosphere-reserve` | Maya Coast — Yucatan Peninsula, Mangroves, and Ancient Habitation | Europeana (Charnay expedition), NHM | Medium | GeoNames BR confirmation · Indigenous cultural layer |
| 47 | `monarch-butterfly-biosphere-reserve` | The Monarch Migration — Mexico's Sacred Mountain Forests | NHM (Lepidoptera collection, PD butterfly plates) | **High** | GeoNames BR · Butterfly illustration from NHM entomology collection |
| 48 | `copper-canyon` | Barrancas del Cobre — Sierra Madre and Rarámuri Heritage | Europeana, NHM | Low | GeoNames: no clear NP boundary — scope required |
| 49 | `belize-barrier-reef-reserve-system` | The Mesoamerican Reef — Caribbean Marine Illustration | NHM, NOAA | Medium | GeoNames: barrier reef system, not a single feature |
| 50 | `blue-mountains-jamaica` | Jamaican Highlands — Caribbean Natural History and Endemic Birds | NHM (Caribbean natural history, Sloane Jamaica 1707) | **High** | GeoNames PRKA · Hans Sloane's *Voyage to Jamaica* (1707) is primary NC source |
| 51 | `cocos-island-national-park` | Darwin's Afterthought — Oceanic Island Endemism | NHM, NOAA | Medium | GeoNames PRKA |
| 52 | `monteverde-cloud-forest` | Hummingbirds of the Cloud Forest — Gould's Central America | NHM (Gould hummingbird plates — *Monograph of the Trochilidae* 1861) | **High** | GeoNames BR · Gould hummingbird illustrations are flagship assets |
| 53 | `asa-wright-nature-centre` | Trinidad's Living Laboratory — Neotropical Bird Illustration | NHM (Trinidad natural history) | Medium | GeoNames: private reserve — confirm authority structure |
| 54 | `pantanal` | The World's Largest Tropical Wetland — South American Waterbirds | NHM, Europeana | High | GeoNames: tri-national, scope requires anchor to Brazilian protected area complex |
| 55 | `iguazu-falls` | The Great Waters — Iguazú and the Paraná Forest | NHM, Europeana | Medium | GeoNames: bi-national, Argentine/Brazilian NPs |
| 56 | `torres-del-paine-national-park` | Granite Towers — Patagonian Landscape and Guanaco Wilderness | NHM (Patagonian natural history), Europeana | High | GeoNames PRKA |
| 57 | `atacama-desert` | The Driest Place on Earth — Andean Natural History and Night Sky | Europeana (Darwin/Humboldt Andes), NOAA (atmospheric) | Medium | GeoNames: region, not an NP — scope to a specific reserve |
| 58 | `machu-picchu` | The Lost City — Inca Cultural Landscape and Andean Ecology | Europeana (Hiram Bingham 1911 records), NHM | Medium | GeoNames HSCP confirmation · Cultural sensitivity: Quechua heritage |
| 59 | `manu-national-park` | Amazon Headwaters — Andean-Amazon Transition and Maximum Biodiversity | NHM (Wallace/Bates Amazon plates) | High | GeoNames PRKA · UNESCO WH + Biosphere Reserve |
| 60 | `los-glaciares-national-park` | Patagonian Ice — Southern Andes and Calving Glaciers | NHM (Beagle voyage Patagonia), Europeana | High | GeoNames PRKA |
| 61 | `lake-district-national-park` | Wordsworth's Landscape — English Romantic Nature and Victorian Botany | Europeana (Beatrix Potter mycological drawings), NHM, SMK | **High** | GeoNames PRKA · Potter's botanical illustrations (mycology) held in collections |
| 62 | `camargue` | Flamingos of the Rhône Delta — French Natural Wilderness | Europeana (French natural history, flamingo illustration), NHM | High | GeoNames: Parc Naturel Régional confirmation |
| 63 | `donana-national-park` | The Guadalquivir Delta — Iberian Wilderness and Migration Corridor | Europeana (Spanish natural history), NHM | Medium | GeoNames PRKA |
| 64 | `dolomites` | Pale Mountains — Alpine Geology and European Landscape Tradition | Europeana (Alpine illustration), SMK, Getty | Medium | GeoNames: UNESCO WH serial site — scope needed |
| 65 | `bialowieza-forest` | Europe's Last Primeval Forest — European Bison and Ancient Woodland | Europeana (Polish/Belarusian natural history), SMK | Medium | GeoNames: bi-national (Poland/Belarus) — anchor to Polish component · Political sensitivity: border enforcement conflict 2021–2023 |
| 66 | `danube-delta-biosphere-reserve` | The Danube Mouth — Eastern European Waterbirds and Ottoman Cartography | Europeana (Audubon-era Eastern European natural history), Walters (Byzantine manuscripts) | Medium | GeoNames: Danube Delta Biosphere Reserve, Romania side |
| 67 | `plitvice-lakes-national-park` | Terraced Lakes — Croatian Wilderness and Habsburg Natural History | Europeana (Habsburg natural history surveys) | Medium | GeoNames PRKA |
| 68 | `jungfrau-aletsch` | The High Alps — Europe's Largest Glacier and Romantic Landscape | Europeana (Romantic Alpine painting), SMK, Getty | High | GeoNames PRKA or MT confirmation |
| 69 | `cairngorms-national-park` | Ancient Plateau — Scottish Uplands and Caledonian Forest | Europeana (Victorian natural history), NHM, SMK | Medium | GeoNames PRKA |
| 70 | `ngorongoro-conservation-area` | The Crater — Africa's Greatest Wildlife Arena | NHM (East African natural history) | High | GeoNames: Conservation Area, not NP — confirm GeoNames entity type |
| 71 | `kruger-national-park` | The Lowveld — South African Savanna and Early Game Reserve History | NHM (Southern African natural history), Europeana | High | GeoNames PRKA |
| 72 | `victoria-falls` | Mosi-oa-Tunya — Livingstone's Discovery and African Exploration | NHM (Livingstone expedition records and illustrations), Europeana | High | GeoNames: bi-national (Zimbabwe/Zambia) · Zambezi River feature + two adjacent NPs |
| 73 | `virunga-national-park` | Mountain Gorillas — Congo Basin and Volcanic Forest | NHM (DRC natural history) | Medium | GeoNames PRKA · Active conflict zone — content sensitivity required |
| 74 | `bwindi-impenetrable-national-park` | The Forest of Darkness — Mountain Gorillas and Albertine Rift Endemism | NHM (East African natural history) | Medium | GeoNames PRKA |
| 75 | `namib-naukluft-national-park` | The Oldest Desert — Namibian Fog-Belt and Desert Endemism | NHM (Southern African natural history), Europeana | Medium | GeoNames PRKA |
| 76 | `socotra-archipelago` | Arabia's Galápagos — Dragon Blood Trees and Indian Ocean Endemism | NHM (Indian Ocean expedition illustration) | High | GeoNames: Socotra Archipelago UNESCO WH · Yemen political situation — content sensitivity |
| 77 | `mount-kilimanjaro` | Africa's Roof — Equatorial Glaciers and Afromontane Ecology | NHM (East African illustration, Haeckel), Europeana | High | GeoNames: MTNP + MT disambiguation required |
| 78 | `ahaggar-national-park` | The Saharan Massif — Tuareg Heritage and North African Wilderness | Europeana (French Saharan expedition records) | Low | GeoNames PRKA · Remote, limited PD content — Tier 3 candidate on review |
| 79 | `wadi-rum` | The Valley of the Moon — Nabataean Rock Art and Red Desert | Europeana (Orientalist painting, Aubusson expedition), Walters (Nabataean manuscripts) | High | GeoNames PA confirmation · Orientalist painting tradition strong at Walters/Met |
| 80 | `arabian-oryx-sanctuary` | Return from Extinction — Arabian Peninsula Conservation | NHM (Arabian mammal illustration) | Low | GeoNames: UNESCO WH delisted 2007, now revoked — complex authority status |
| 81 | `sundarbans` | Mangrove Delta — Royal Bengal Tiger and Ganges Biodiversity | NHM (Bengal/India natural history, East India Company illustration) | High | GeoNames: bi-national NP (Bangladesh/India) · Anchor to Indian NP or Bangladeshi WS |
| 82 | `kaziranga-national-park` | The Last Great Rhinos — Assam Grasslands and Indian Natural History | NHM (Indian natural history, EIC illustration) | High | GeoNames PRKA |
| 83 | `manas-national-park` | The Manas River — Bhutan-India Biodiversity Corridor | NHM (Assam/Indian natural history) | Medium | GeoNames PRKA · Cross-border with Bhutan |
| 84 | `royal-chitwan-national-park` | Terai Grasslands — Greater One-Horned Rhino and Elephants | NHM (Nepal/India natural history) | High | GeoNames PRKA |
| 86 | `shiretoko-national-park` | Where Earth Ends — Hokkaido Wilderness and Sea of Okhotsk | Met (Hokkaido/Ainu material), NHM | Medium | GeoNames PRKA |
| 87 | `zhangjiajie-national-forest-park` | Pillar Mountains — Sandstone Karst and Chinese Landscape Painting | CMA (Chinese landscape painting tradition), Met | High | GeoNames: National Forest Park classification |
| 88 | `jiuzhaigou-valley` | Nine Village Valley — Sichuan Alpine Lakes and Tibetan Heritage | CMA, Met (Chinese landscape) | High | GeoNames: SCNA confirmation |
| 89 | `komodo-national-park` | Dragon Island — Wallace Line and Indonesian Natural History | NHM (Wallace Malay Archipelago, Indonesia illustration) | High | GeoNames PRKA |
| 90 | `raja-ampat` | The Coral Triangle Heart — Indonesian Marine Biodiversity | NOAA (coral), NHM | Medium | GeoNames: archipelago — scope to specific island group |
| 91 | `ha-long-bay` | Limestone Karst — Tonkin Gulf and Vietnamese Natural Heritage | CMA (Vietnamese/East Asian art), Met | Medium | GeoNames: UNESCO WH · Vietnamese administrative boundary |
| 92 | `lord-howe-island` | The World's Most Remote Island — Pacific Endemic Species | NHM (Pacific expedition illustration, Cook voyage), Trove (**Must Add**) | High | GeoNames: island group confirmation · Trove required for Australia content |
| 93 | `kakadu-national-park` | Ancient Rock Art — Northern Territory and Aboriginal Heritage | NHM (Australia natural history, Banks), Trove (**Must Add**) | High | GeoNames PRKA · Cultural sensitivity: Bininj/Mungguy custodianship — consult required |
| 94 | `daintree-national-park` | Oldest Rainforest — Queensland Wet Tropics and Cassowary Country | NHM (Queensland natural history), Trove (**Must Add**) | High | GeoNames PRKA |
| 95 | `palau-national-marine-sanctuary` | Jellyfish Lakes — Pacific Marine Conservation Pioneer | NOAA, NHM (Pacific expedition) | Medium | GeoNames: marine sanctuary boundary |
| 96 | `easter-island-rapa-nui` | The Navel of the World — Moai and Polynesian Cultural Heritage | NHM (Cook voyage Pacific), Europeana (La Pérouse expedition records) | High | GeoNames: Chilean territory, island confirmation |
| 97 | `new-caledonia` | Pacific Biodiversity Crown — French Pacific and Coral Sea | NHM (Cook/Forster Pacific voyage), Europeana (French Pacific expedition) | High | GeoNames: French overseas collectivity — administrative disambiguation |
| 98 | `ningaloo-reef` | Western Australia's Coral Highway — Whale Shark and Reef Illustration | NOAA, NHM, Trove (**Must Add**) | High | GeoNames: Marine Park confirmation |
| 99 | `lake-tanganyika` | The Inland Sea — East African Rift and Cichlid Diversity | NHM (Livingstone expedition), Europeana | Medium | GeoNames: LK · Quad-national water body — anchor to Tanzanian shoreline |
| 100 | `lake-titicaca` | Sacred Lake — Andean Cosmology and Highland Biodiversity | NHM, Europeana (Humboldt Andes), Walters (Peruvian manuscripts) | Medium | GeoNames: LK · Bi-national (Peru/Bolivia) |

---

## IX. Required Authority Checks Before Any Tier 1/2 Place Enters Production

Each place must complete this checklist before Gate E:

1. **GeoNames confirmation** — resolve GeoNames ID to feature class (PRKA preferred for NPs,
   PRKN for reserves, MT for mountains, RF for reefs, LK for lakes, etc.). Document in
   NC-DATA-* fixture.
2. **Wikidata confirmation** — resolve QID. Confirm P1566 (GeoNames) cross-link. Document in
   NC-DATA-* fixture.
3. **Scope decision** — for regional places (Scottish Highlands, Amazon Basin, Atacama) define
   the bounded component that serves as the canonical NC anchor.
4. **Cross-border ruling** — for bi-national or tri-national features (Wadden Sea, Tierra del
   Fuego, Białowieża, Iguazú): define single-nation anchor OR establish multi-slug policy.
5. **Content fixture** — at least one product-safe asset confirmed from a ratified institution
   before the place page is built.
6. **Cultural sensitivity check** — for places with Indigenous custodianship (Kakadu, Machu
   Picchu, Pacific Rim NP Reserve), consult flag must be set and cleared before launch.

---

## X. Commerce Potential Summary

### Tier 1 High-Value Illustration Anchors

| Place | Primary PD illustration asset | Institution | Notes |
|---|---|---|---|
| Everglades | Audubon *Birds of America* wading bird plates | NHM | Roseate Spoonbill, Great Egret — flagship |
| Yosemite | Bierstadt *Looking Down Yosemite Valley* (oil) | NGA | Large-format giclée candidate |
| Mount Fuji | Hokusai *Thirty-Six Views* ukiyo-e | Met | Proven commercial asset globally |
| Fiordland | Parkinson Cook voyage New Zealand botanicals | NHM | Banks Florilegium plates |
| Galápagos | Gould *Darwin's Finches* (Beagle Voyage Zoology) | NHM | Darwin link = editorial story |
| Cape of Good Hope | Levaillant *Oiseaux d'Afrique* bird plates | NHM | African birds — high visual quality |
| Cape Floral Region | Masson Cape protea botanicals | NHM | Proteas are luxury print subject |
| Tierra del Fuego | Martens sub-Antarctic watercolours | NHM | Beagle voyage — editorial narrative |
| Scottish Highlands | Gould *Birds of Great Britain* | NHM / Europeana | Red Kite, Golden Eagle |
| Himalayas-Sagarmatha | Hooker *Rhododendrons of Sikkim-Himalaya* | NHM | Botanical illustration, high quality |
| Borneo-Kinabatangan | Wallace *Malay Archipelago* plates | NHM | Orang-utan + proboscis monkey |
| Antarctic Peninsula | Edward Wilson watercolours (Scott expedition) | NHM | Penguins — iconic |
| Monteverde | Gould *Monograph of the Trochilidae* hummingbirds | NHM | Most commercially proven NHM set |
| Blue Mountains Jamaica | Sloane *Voyage to Jamaica* (1707) | Europeana / NHM | Earliest Caribbean natural history |
| Monarch Butterfly BR | NHM Lepidoptera collection plates | NHM | Butterfly illustration — strong demand |
| Acadia | Hudson River School East Coast painting | NGA | Cole, Church — New England coast |
| Lake District | Potter mycological drawings (Beatrix Potter) | Europeana | Strong commercial recognition |
| Wadi Rum | Orientalist desert painting tradition | Walters, Met | Strong Middle Eastern illustration |

---

## XI. Implementation Sequence

### Sprint 1 (current): Tier 0 consolidation
- Complete Papahānaumokuākea, Venice, Galápagos authority fixtures
- Place pages for Yellowstone, Grand Canyon, Great Barrier Reef live

### Sprint 2: First 10 Tier 1 places
Priority order: Yosemite → Everglades → Mount Fuji → Cape of Good Hope → Fiordland →
Scottish Highlands → Everest-Sagarmatha → Svalbard → Banff → Antarctic Peninsula

Blockers: NHM Sprint 1 confirmation (Asset Zero: Parkinson/Nodder); Met Sprint 1 live.

### Sprint 3: Remaining Tier 1 (17 places) + begin Tier 2 authority resolution
Run GeoNames/Wikidata confirmation batch for all 38 Tier 2 places in parallel.

### Sprint 4: Tier 2 production (38 places)
Requires: Trove onboarding for Australia/Pacific places (#86, #92–#95, #98).

### Sprint 5: Tier 3 pipeline (28 places)
Requires: Wellcome, V&A, MNHN onboarding for remaining geographic gaps.

---

## XII. Slug Reconciliation

The master candidate table above has two duplicate reference rows (#43 = Banff duplicate of
#23; #85 = Mount Fuji duplicate of #12). Before ratification, replace these with:

- **#43**: `pyrenees-national-park` (France/Spain) — European natural history, SMK/Europeana
- **#85**: `shiretoko-national-park` — already included above as #86 in the detailed table

Correction: renumber sequentially before any production activation. The 100 unique slugs are
confirmed in §V as written once those two replacements are confirmed.

---

*NC-PLACES-001 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
