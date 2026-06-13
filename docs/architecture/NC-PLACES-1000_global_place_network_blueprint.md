# NC-PLACES-1000: Global Place Network Blueprint

| Field | Value |
|---|---|
| Document | NC-PLACES-1000 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | NC-GRAPH-002 · NC-ICH-001 · NC-PLACES-FACTORY-001 · NC-PRODUCT-001 · Strategic Direction v1 |
| Scale targets | 2,000 places (v1.0) → 10,000 places (v2.0) |
| Reference models | UNESCO Sites Navigator · Google Arts & Culture · National Geographic · Smithsonian · Rijksmuseum |

---

## Governing Doctrine

Nature & Culture is a Library of Commerce for public-domain heritage. At 10,000 places, the
platform becomes the definitive reference where geography, natural history, and cultural
heritage converge in a single traversable network. No equivalent system exists.

Five principles govern every decision in this document:

| Principle | Statement |
|---|---|
| Place is the axis of everything | Every entity — illustration, taxon, illustrator, expedition, ICH practice — ultimately connects to a place. The place page is the commerce unit. |
| Taxonomy precedes content | The taxonomic framework must be settled before content is created. Retroactive reclassification at scale destroys editorial consistency. |
| The graph is the discovery layer | At 10,000 places, hierarchical navigation is impossible. Relationship traversal is the only viable discovery mechanism. |
| Commerce is the outcome, not the goal | Place pages exist to tell true stories about heritage and natural history. Commerce is enabled, never forced. |
| Doctrine over precedent | When any reference model conflicts with NC doctrine (PD hard gate, FM-4, ICH-2), doctrine wins. |

---

## I. Global Place Taxonomy

### 1.1 Three-Level Structure

The NC place taxonomy has three levels. Every NC place carries one **primary type**, one
**primary subtype**, and zero or more **secondary subtypes**.

```
Domain (Level 0) — 4 domains
  └── Primary Type (Level 1) — 12 types
        └── Subtype (Level 2) — 44 subtypes
```

### 1.2 Domains

| Code | Domain | Definition |
|---|---|---|
| `N` | Natural | Places defined primarily by physical geography and ecology |
| `C` | Cultural | Places defined primarily by human history, architecture, and tradition |
| `M` | Mixed | Places recognized explicitly for both outstanding natural and cultural values |
| `X` | Cosmic | Places defined by their relationship to celestial phenomena (dark sky, space exploration) |

The `M` (Mixed) domain is the rarest and carries the highest editorial weight. UNESCO lists
fewer than 50 Mixed WH sites globally. These are NC's highest-priority places.

### 1.3 Primary Type and Subtype Taxonomy

```
N — NATURAL
├── N.PK  Protected Area
│   ├── N.PK.NP   National Park (IUCN II)
│   ├── N.PK.SR   Strict Nature Reserve (IUCN I)
│   ├── N.PK.WA   Wilderness Area (IUCN Ib)
│   ├── N.PK.NM   National Monument (IUCN III)
│   └── N.PK.PA   Protected Landscape (IUCN V)
├── N.MR  Marine Protected Area
│   ├── N.MR.RF   Coral Reef and Reef System
│   ├── N.MR.AT   Atoll and Archipelago
│   ├── N.MR.SM   Seamount and Hydrothermal Vent
│   ├── N.MR.SG   Seagrass and Kelp System
│   └── N.MR.MG   Mangrove Coast
├── N.WL  Wetland (Ramsar types)
│   ├── N.WL.DT   Delta and Estuary
│   ├── N.WL.LK   Lake and Lacustrine System
│   ├── N.WL.PT   Peatland and Bog
│   ├── N.WL.MN   Mangrove (wetland-classified)
│   └── N.WL.FP   Floodplain and Riparian
├── N.MT  Mountain and Alpine
│   ├── N.MT.VL   Volcanic Mountain
│   ├── N.MT.GL   Glacial and Ice System
│   ├── N.MT.AL   Alpine and Sub-alpine
│   └── N.MT.RG   Mountain Range
├── N.FR  Forest and Woodland
│   ├── N.FR.TR   Tropical Rainforest
│   ├── N.FR.TD   Tropical Dry Forest
│   ├── N.FR.TM   Temperate Forest
│   ├── N.FR.BL   Boreal and Taiga
│   └── N.FR.MN   Mangrove Forest
├── N.IS  Island and Oceanic
│   ├── N.IS.OC   Oceanic Island (volcanic)
│   ├── N.IS.CR   Coral Island and Atoll
│   ├── N.IS.SB   Sub-Antarctic Island
│   └── N.IS.AR   Archipelago System
├── N.GE  Geological
│   ├── N.GE.GP   Geopark (UNESCO)
│   ├── N.GE.CY   Canyon and Gorge
│   ├── N.GE.KS   Karst and Cave System
│   ├── N.GE.DS   Desert and Arid Landscape
│   └── N.GE.CS   Coastal and Cliff System
└── N.PL  Polar and Sub-polar
    ├── N.PL.AN   Antarctic
    ├── N.PL.AR   Arctic
    └── N.PL.SB   Sub-polar and Tundra

C — CULTURAL
├── C.SL  Sacred and Spiritual Landscape
│   ├── C.SL.IP   Indigenous Sacred Place
│   ├── C.SL.RL   Religious and Pilgrimage Site
│   └── C.SL.SM   Symbolic Mountain or Feature
├── C.CL  Cultural Landscape (UNESCO)
│   ├── C.CL.AG   Agrarian Landscape
│   ├── C.CL.HI   Historic Urban Landscape
│   ├── C.CL.IN   Industrial Heritage Landscape
│   └── C.CL.EV   Evolving Cultural Landscape
├── C.HU  Historic Urban
│   ├── C.HU.HC   Historic City Centre
│   ├── C.HU.PT   Port and Trading City
│   └── C.HU.RY   Royal and Imperial Capital
└── C.HR  Heritage Route
    ├── C.HR.TR   Trade and Pilgrimage Route
    └── C.HR.EX   Exploration Route

M — MIXED
└── M.MX  Mixed WH Site
    ├── M.MX.NC   Natural-Cultural (equal weight)
    ├── M.MX.NS   Natural-Sacred
    └── M.MX.NI   Natural-Indigenous

X — COSMIC
├── X.DS  Dark Sky Place
│   ├── X.DS.RV   Dark Sky Reserve (natural landscape)
│   ├── X.DS.PK   Dark Sky Park (protected area)
│   ├── X.DS.SY   Dark Sky Sanctuary (most remote)
│   └── X.DS.CM   Dark Sky Community (urban)
└── X.SP  Space Heritage
    └── X.SP.LO   Low Earth Orbit (Earthrise anchor)
```

### 1.4 Place Type Properties

Each primary type carries mandatory and optional fields:

| Property | N.PK | N.MR | N.WL | N.MT | N.IS | N.GE | C.CL | C.SL | M.MX | X.DS |
|---|---|---|---|---|---|---|---|---|---|---|
| `geonames_id` required | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `wdpa_id` expected | ✓ | ✓ | ✓ | ○ | ○ | ○ | ○ | ○ | ✓ | ○ |
| `ramsar_id` expected | — | — | ✓ | — | — | — | — | — | ○ | — |
| `iucn_category` required | ✓ | ✓ | — | — | — | — | — | — | ✓ | — |
| `wh_site_number` expected | ○ | ○ | ○ | ○ | ○ | ✓ | ✓ | ✓ | ✓ | — |
| `ich_elements` expected | — | — | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | — |
| `cultural_sensitivity_review` | — | — | ○ | ○ | ✓ | — | ✓ | ✓ | ✓ | — |

✓ = always required · ○ = required when present · — = not applicable

---

## II. Designation Taxonomy

### 2.1 Designation Frameworks

Designations are formal inscriptions by recognized international or national bodies.
A place may carry designations from multiple frameworks simultaneously.

| Code | Framework | Body | Max per place | Weight |
|---|---|---|---|---|
| `UNESCO_WH` | World Heritage | UNESCO WHC | 1 | 10 |
| `UNESCO_BS` | Biosphere Reserve | UNESCO MAB | 1 | 6 |
| `UNESCO_GP` | Global Geopark | UNESCO | 1 | 5 |
| `UNESCO_ICH` | Intangible CH | UNESCO ICH | unlimited | 8 per element |
| `RAMSAR` | Ramsar Wetland | Ramsar Secretariat | unlimited | 4 |
| `IUCN_PA` | Protected Area | IUCN / WDPA | 1 per unit | 3–4 |
| `IDA_DS` | Dark Sky Place | IDA | 1 | 4 |
| `MARINE_PA` | Marine MPA | Various | multiple | 3 |
| `NATIONAL` | National designation | Govt. body | multiple | 1–2 |

### 2.2 Designation Type Registry

```
UNESCO_WH
├── UNESCO_WH_N     Natural (WH criteria vii–x)
├── UNESCO_WH_C     Cultural (WH criteria i–vi)
├── UNESCO_WH_M     Mixed (both natural AND cultural)
└── UNESCO_WH_X     In Danger (modifier; applied alongside type above)

UNESCO_BS
├── UNESCO_BS_FULL  Full Biosphere Reserve (all three zones)
├── UNESCO_BS_CORE  Core zone designation (for sub-unit pages)
└── UNESCO_BS_TZ    Transition zone (for cultural landscape sub-pages)

UNESCO_GP
└── UNESCO_GP_FULL  UNESCO Global Geopark

UNESCO_ICH
├── UNESCO_ICH_RL   Representative List (most common)
├── UNESCO_ICH_US   Urgent Safeguarding List
├── UNESCO_ICH_GP   Good Practices Register
└── UNESCO_ICH_NA   National Inventory (recognized but not inscribed internationally)

RAMSAR
└── RAMSAR_FULL     Ramsar Site (wetlands of international importance)

IUCN_PA
├── IUCN_IA         Strict Nature Reserve
├── IUCN_IB         Wilderness Area
├── IUCN_II         National Park
├── IUCN_III        Natural Monument
├── IUCN_IV         Habitat/Species Management
├── IUCN_V          Protected Landscape/Seascape
└── IUCN_VI         Protected Area with Sustainable Use

IDA_DS
├── IDA_DS_RESERVE  Dark Sky Reserve (natural and buffer zones)
├── IDA_DS_PARK     Dark Sky Park (within IUCN-protected area)
├── IDA_DS_SANCT    Dark Sky Sanctuary (most remote, pristine)
└── IDA_DS_COMM     Dark Sky Community (populated area)

MARINE_PA
├── MPA_HS          High Seas MPA (no national jurisdiction)
├── MPA_EEZ         EEZ Marine Protected Area
└── MPA_CORAL       Coral Triangle Protected Area
```

### 2.3 Designation Stack Rules

The Designation Stack is the count of *active, unique* HeritageDesignation records for
a place. Each framework contributes at most once to the stack (a Biosphere Reserve with
three zones counts as 1, not 3).

```
stack_height = count of DISTINCT framework codes
               WHERE designation.status = 'Active'
```

| Stack height | Editorial tier | Discovery priority | Collection eligibility |
|---|---|---|---|
| 0 | — | — | — |
| 1 | Standard | Normal | Basic place collection |
| 2 | Notable | Elevated | Regional collection eligible |
| 3+ | **Priority** | **Top** | **All collection types eligible** |
| 5+ | **Exceptional** | **Featured** | DESIGNATION_BUNDLE mandatory |

Known high-stack places (stack ≥ 4):
- **Svalbard**: IUCN_IA + RAMSAR + UNESCO_WH_N + IDA_DS_RESERVE = stack 4
- **Wadden Sea**: UNESCO_WH_N + RAMSAR + IUCN_IA (tri-national) = stack 3
- **Great Barrier Reef**: UNESCO_WH_N + RAMSAR + IUCN_II + MPA_EEZ = stack 4
- **Tongariro**: UNESCO_WH_M + UNESCO_BS + IUCN_II = stack 3
- **Shiretoko**: UNESCO_WH_N + RAMSAR + IUCN_II = stack 3
- **Sundarbans**: UNESCO_WH_N + RAMSAR + IUCN_II (Bangladesh+India) = stack 3+

### 2.4 Designation Change Protocol

When a designation status changes post-activation:
1. `UNESCO_WH_X` (In Danger) added: flag for editorial review, reduce composite score by 3,
   add "Under Threat" editorial label. Do NOT delist place page.
2. Delisted (Arabian Oryx type): require Director Decision before page shows commerce.
   Add "Heritage Lost" editorial category. Historical context preserved.
3. Designation renewed / upgraded: trigger rescoring, notify editorial team.

---

## III. Place Family Taxonomy

### 3.1 Family Type Definitions

A Place Family is a named cluster of places that share a compelling narrative connection.
Families are the primary editorial super-structure above individual place pages.
At 10,000 places, families are also the primary browse layer (replacing category pages).

| Family type | Code | Definition | Typical size |
|---|---|---|---|
| Expedition | `FAM_EX` | All places documented by a named historical voyage/expedition | 8–30 places |
| Illustrator | `FAM_IL` | All places where a named NC Priority Illustrator worked | 5–20 places |
| Bioregion | `FAM_BR` | All places within a defined ecoregion (WWF biome classification) | 15–60 places |
| Designation | `FAM_DG` | All places sharing a specific designation type | 20–200+ places |
| Heritage Route | `FAM_HR` | Places linked by a historic road, voyage route, or pilgrimage path | 5–40 places |
| Ecological System | `FAM_EC` | Places connected by a shared ecological system (flyway, current, corridor) | 10–50 places |
| Cultural Sphere | `FAM_CS` | Places linked by a shared cultural/civilizational tradition | 10–80 places |
| Domain | `FAM_DO` | All places of a specific primary type within a geographic region | 20–200+ places |

### 3.2 Named Expedition Families

| Family slug | Name | Anchor illustrators | Place count (target) |
|---|---|---|---|
| `fam-cook-voyages` | Cook's Three Voyages | Parkinson, Hodges, Webber, Sydney Parkinson | 24 |
| `fam-beagle-voyage` | Darwin's Beagle Voyage | Conrad Martens, Robert FitzRoy | 16 |
| `fam-humboldt-expedition` | Humboldt's American Expedition | Turpin, Bonpland botanical illustrations | 12 |
| `fam-wallace-malay` | Wallace in the Malay Archipelago | Wallace field drawings; Bates contemporaneous | 14 |
| `fam-audubon-america` | Audubon's America | John James Audubon (Havell aquatints) | 18 |
| `fam-hooker-india` | Hooker's Himalayan Expeditions | W.H. Fitch illustrations for Hooker | 8 |
| `fam-challenger-expedition` | HMS Challenger Deep-Sea Voyage | Haeckel *Report*, Moseley illustrations | 20 |
| `fam-scott-shackleton` | Heroic Age Antarctic | Edward Wilson watercolours | 10 |
| `fam-levaillant-africa` | Le Vaillant's African Journeys | Barraband, Reinold (Oiseaux d'Afrique) | 10 |
| `fam-merian-suriname` | Merian's Surinam | Maria Sibylla Merian | 4 |
| `fam-ric-india` | East India Company Surveys | Roxburgh, Buchanan-Hamilton (EIC Floras) | 12 |
| `fam-gould-birds` | Gould's Global Ornithology | John Gould + H.C. Richter | 22 |

### 3.3 Named Ecological System Families

| Family slug | Name | Ecological basis | Place count (target) |
|---|---|---|---|
| `fam-coral-triangle` | Coral Triangle | Shared coral reef system, Indo-Pacific | 12 |
| `fam-east-atlantic-flyway` | East Atlantic Flyway | Migratory bird corridor, W. Africa coast | 16 |
| `fam-amazon-basin` | Amazon Basin | Watershed and drainage basin, S. America | 10 |
| `fam-african-rift-valley` | African Great Rift Valley | Rift geology + associated lakes | 12 |
| `fam-himalayan-arc` | Himalayan Arc | Elevation gradient from Terai to summit | 10 |
| `fam-kelp-highway` | Pacific Kelp Highway | Kelp forests, E. + W. Pacific coast | 8 |
| `fam-mediterranean-basin` | Mediterranean Basin | Shared climate + biodiversity hotspot | 20 |
| `fam-pacific-island-arc` | Pacific Island Arc | Volcanic island chain, Ring of Fire | 16 |

### 3.4 Named Cultural Sphere Families

| Family slug | Name | Cultural basis | Place count (target) |
|---|---|---|---|
| `fam-silk-road` | Silk Road Heritage | Trans-Eurasian trade routes | 30 |
| `fam-inca-road` | Qhapaq Ñan / Inca Road | Andean road network (WH 2014) | 12 |
| `fam-austronesian-voyaging` | Austronesian Voyaging Culture | Pacific navigation tradition | 14 |
| `fam-dutch-golden-age` | Dutch Golden Age Landscapes | 17th-c. Netherlands painting tradition | 8 |
| `fam-islamic-garden` | Islamic Garden Tradition | Chahar bagh garden heritage | 10 |
| `fam-buddhist-sacred-mountains` | Buddhist Sacred Mountain Network | Himalaya, Japan, SE Asia | 12 |
| `fam-indigenous-australia` | First Nations Australia | Songlines and Country | 15 |
| `fam-andean-heritage` | Andean Heritage Belt | Inca + pre-Inca highland cultures | 12 |

### 3.5 Family Membership Rules

- A place may belong to multiple families across types (Galápagos: `fam-beagle-voyage` + `fam-coral-triangle` + `fam-gould-birds`)
- Family membership is a graph edge (`MEMBER_OF_FAMILY`) derived from the PostgreSQL authority tables
- Expedition family membership requires: expedition passes within 300km of place centroid, OR named in primary source documentation
- Cultural sphere membership requires: UNESCO ICH element linked, OR WH cultural site designation, OR confirmed scholarly consensus in `nc_family_evidence` table
- Family pages are Tier 2+ places in the publishing model (not stubs)

---

## IV. Collection Family Taxonomy

### 4.1 Collection Hierarchy

Collections are the primary commerce unit above the individual product. At 10,000 places,
collections are organized in a four-level hierarchy:

```
Level 1: PLATFORM COLLECTION (1 per domain — 4 total)
  Level 2: REGIONAL COLLECTION (1 per bioregion — ~14 total)
    Level 3: FAMILY COLLECTION (1 per place family — ~60 total)
      Level 4: PLACE COLLECTION (1+ per place)
        └── THEMATIC SUB-COLLECTION (multiple per place, by subject)
```

All commerce flows through Level 4 (Place Collections). Higher levels are editorial
groupings that aggregate and cross-link Level 4 products.

### 4.2 Ten Collection Families

| Code | Family | Definition | Volume target |
|---|---|---|---|
| `CF-PLACE` | Place Anchor | All PD illustrations linked to a single place. Primary commerce unit. | 1 per place (10,000 at scale) |
| `CF-EXPEDITION` | Expedition Record | All illustrations produced during a named expedition, across all places visited | 12–30 per expedition |
| `CF-ILLUSTRATOR` | Illustrator Portfolio | Complete accessible PD output of a named NC Priority Illustrator | 8 per priority illustrator |
| `CF-DESIGNATION` | Designation Bundle | All illustrations from places sharing the same designation stack (stack ≥ 3) | 50–100 |
| `CF-BIOREGION` | Bioregion Survey | All illustrations from places within a named bioregion | 14 per bioregion |
| `CF-TAXON` | Taxon Study | All PD illustrations of a species or genus, across all places it occurs | By demand |
| `CF-ICH` | Heritage Practice | PD documentary illustrations connected to an ICH element or domain | 1 per ICH element |
| `CF-INSTITUTION` | Institution Portfolio | All PD illustrations from a single content institution | 1 per institution |
| `CF-ERA` | Historical Era | All illustrations from a defined historical period (e.g., "Golden Age 1770–1830") | 5–10 |
| `CF-THEME` | Editorial Theme | Curated cross-place collection around an editorial narrative | As needed |

### 4.3 Collection Activation Sequence

Not all collection families are available at all publishing tiers:

| Collection family | Min tier | Min illustrations | Gate required |
|---|---|---|---|
| CF-PLACE | Tier 2 | 3 | Gate CP |
| CF-EXPEDITION | Tier 2 | 5 | Gate CP |
| CF-ILLUSTRATOR | Tier 2 | 5 | Gate CP |
| CF-DESIGNATION | Tier 3 | 8 | Gate E (two-human) |
| CF-BIOREGION | Tier 3 | 10 | Gate E |
| CF-TAXON | Tier 3 | 5 | Gate E |
| CF-ICH | Tier 3 | 5 | Gate E + Gate CS |
| CF-INSTITUTION | Tier 3 | 10 | Gate E |
| CF-ERA | Tier 4 | 15 | Gate E + editorial review |
| CF-THEME | Tier 4 | 10 | Gate E + editorial review |

### 4.4 Collection Naming Convention

Consistent naming enables machine-readable collection IDs and coherent editorial voice.

| Collection family | Naming pattern | Example |
|---|---|---|
| CF-PLACE | `[Place Name] — [Primary Subject]` | "Galápagos Islands — Voyage of the Beagle" |
| CF-EXPEDITION | `[Illustrator/Artist]'s [Destination/Theme]` | "Audubon's Wilderness — Eastern Birds" |
| CF-ILLUSTRATOR | `The [Name] Collection` | "The Haeckel Collection" |
| CF-DESIGNATION | `[Designation] Heritage — [Region]` | "World Heritage — Pacific Islands" |
| CF-BIOREGION | `[Bioregion Name] — Natural History` | "Tropical Andes — Natural History" |
| CF-ICH | `[Practice Name] — Documentary Record` | "Noh Theatre — Documentary Record" |
| CF-THEME | `[Thematic Title]` | "Sacred Mountains of Asia" |

---

## V. Discovery Graph Taxonomy

### 5.1 Seven Traversal Axes

At 10,000 places, the NC discovery graph has an estimated 1.5–3M relationship edges.
Discovery is organized along seven traversal axes. Each axis has precomputed edges
(stored in Neo4j) and derived traversals (computed at query time from 2-hop paths).

| Axis | Code | Basis | Edge type | Precomputed |
|---|---|---|---|---|
| Geographic proximity | AX-GEO | PostGIS centroid distance | `PROXIMATE_TO` | Yes (≤600km) |
| Ecological connection | AX-ECO | Bioregion, flyway, current | `WITHIN_BIOREGION`, `SHARES_ECOSYSTEM` | Yes |
| Historical / expedition | AX-HIS | Expedition route, dates | `PART_OF_VOYAGE`, `VISITED_BY` | Yes |
| Designation | AX-DES | Shared designation framework | `SHARES_DESIGNATION` | Yes |
| Cultural / ICH | AX-ICH | ICH practice co-location | `PRACTICED_AT`, `CO_PRACTICED_WITH` | Yes (direct), derived (co-) |
| Commercial signal | AX-COM | Product co-purchase, similar profile | `SIMILAR_PRODUCT_PROFILE` | Derived |
| Institutional | AX-INS | Content sourced from same institution | `SOURCED_FROM_INSTITUTION` | Yes |

### 5.2 Full Relationship Registry

All relationship types in the NC discovery graph. Grouped by axis.

**AX-GEO: Geographic**
| Relationship | Direction | Basis | G-8 registration |
|---|---|---|---|
| `PROXIMATE_TO` | Place↔Place | PostGIS: centroid ≤600km | Registered (NC-GRAPH-002) |
| `WITHIN_BIOREGION` | Place→Bioregion | PostGIS: ST_Within | Registered (NC-GRAPH-002) |
| `LOCATED_IN` | Place→Place | Admin hierarchy | Registered (NC-GRAPH-002) |
| `BORDERS` | Place↔Place | Shared boundary >5km | New — G-8 registration required |
| `PART_OF_SERIAL` | Place→Place | UNESCO serial site | New — G-8 registration required |

**AX-ECO: Ecological**
| Relationship | Direction | Basis | G-8 registration |
|---|---|---|---|
| `SHARES_ECOSYSTEM` | Place↔Place | Same ecosystem type (WWF L2) | New |
| `WITHIN_FLYWAY` | Place→Flyway | Migratory bird route overlay | New |
| `WITHIN_CURRENT` | Place→OceanCurrent | Ocean current system | New |
| `CONNECTED_BY_WATERSHED` | Place↔Place | Shared river basin | New |
| `CO_OCCURS_WITH` | Taxon↔Taxon | GBIF co-occurrence (≥500 records each) | Registered (NC-ICH-001) |
| `OCCURS_AT` | Taxon→Place | GBIF occurrence data | Registered (NC-GRAPH-002) |

**AX-HIS: Historical**
| Relationship | Direction | Basis | G-8 registration |
|---|---|---|---|
| `PART_OF_VOYAGE` | Place→Expedition | Expedition route record | Registered (NC-GRAPH-002) |
| `VISITED_BY` | Place→Person | Historical record | Registered (NC-GRAPH-002) |
| `CONTEMPORARY_WITH` | Person↔Person | Overlapping active years | Registered (NC-GRAPH-002) |
| `PRECEDED_BY` | Expedition→Expedition | Temporal sequence | New |
| `PART_OF_FAMILY` | Place→PlaceFamily | Family membership | New |

**AX-DES: Designation**
| Relationship | Direction | Basis | G-8 registration |
|---|---|---|---|
| `HAS_DESIGNATION` | Place→HeritageDesignation | PostgreSQL nc_place_designations | Registered (NC-ICH-001) |
| `SHARES_DESIGNATION` | Place↔Place | Same designation framework | Derived |
| `PART_OF_BIOSPHERE` | Place→BiosphereReserve | UNESCO MAB zone | New |
| `CONNECTED_BY_CORRIDOR` | Place↔Place | Ecological corridor between WH sites | New |

**AX-ICH: Cultural/ICH**
| Relationship | Direction | Basis | G-8 registration |
|---|---|---|---|
| `PRACTICED_AT` | HeritagePractice→Place | nc_practice_place_anchors | Registered (NC-ICH-001) |
| `DOCUMENTED_BY` | HeritagePractice→Illustration | nc_practice_illustrations | Registered (NC-ICH-001) |
| `CO_PRACTICED_WITH` | HeritagePractice↔HeritagePractice | Shared place evidence | Registered (NC-ICH-001) |
| `EVOLVED_INTO` | HeritagePractice→HeritagePractice | Historical lineage | Registered (NC-ICH-001) |
| `CULTURALLY_CONNECTED` | Place↔Place | Shared ICH domain, same cultural sphere | Derived |
| `MEMBER_OF_FAMILY` | Place→PlaceFamily | nc_place_family_members | New |

**AX-COM: Commercial**
| Relationship | Direction | Basis | G-8 registration |
|---|---|---|---|
| `SIMILAR_PRODUCT_PROFILE` | Place↔Place | Shared product category + illustrator style | Derived (no FM writes — G-5) |
| `APPEARS_IN_COLLECTION` | Illustration→Collection | nc_collection_items | Registered (NC-GRAPH-002) |
| `ASSOCIATED_WITH` | Illustration→Place | Asset provenance | Registered (NC-GRAPH-002) |
| `CREATED_BY` | Illustration→Artist | Attribution record | Registered (NC-GRAPH-002) |
| `PART_OF_EXPEDITION` | Illustration→Expedition | Provenance | Registered (NC-GRAPH-002) |
| `SOURCED_FROM` | Illustration→Institution | Rights chain | Registered (NC-GRAPH-002) |

### 5.3 Discovery Journey Map

Seven canonical discovery journeys that users traverse. Each journey is a named
multi-hop graph path with a defined entry node type.

| Journey | Entry | Traversal | Exit |
|---|---|---|---|
| **Expedition Trail** | Expedition node | PART_OF_VOYAGE → Place → PROXIMATE_TO → adjacent places | Place collection |
| **Illustrator's World** | Artist node | CREATED_BY (reverse) → Illustration → ASSOCIATED_WITH → Place | Place page |
| **Designation Network** | HeritageDesignation → Place | SHARES_DESIGNATION → related places → PRACTICED_AT → ICH | Heritage collection |
| **Ecological Corridor** | Bioregion node | WITHIN_BIOREGION (reverse) → Places → SHARES_ECOSYSTEM → family | Bioregion collection |
| **ICH Thread** | HeritagePractice → DOCUMENTED_BY → Illustration | ASSOCIATED_WITH → Place → PRACTICED_AT (other practices) | ICH collection |
| **Taxon Trail** | Taxon node | OCCURS_AT → Place → CO_OCCURS_WITH → related taxa | Place + taxon collection |
| **Cultural Sphere** | PlaceFamily → places | MEMBER_OF_FAMILY (reverse) → Places → CULTURALLY_CONNECTED | Cultural collection |

### 5.4 Graph Scale Parameters

| Parameter | 1,000 places | 5,000 places | 10,000 places |
|---|---|---|---|
| Estimated nodes | ~400,000 | ~2,000,000 | ~4,000,000 |
| Estimated relationships | ~2,500,000 | ~12,000,000 | ~25,000,000 |
| Precomputed PROXIMATE_TO pairs | ~50,000 | ~1,200,000 | ~5,000,000 |
| Recommended Neo4j deployment | AuraDB Professional | AuraDB Enterprise or self-hosted 3-node | Self-hosted 5-node cluster |
| Full rebuild time target | <60 min | <4 hours | <12 hours |
| Incremental sync lag target | <15 min | <15 min | <15 min |

---

## VI. Commerce Family Taxonomy

### 6.1 Eight Commerce Families

At 10,000 places, the product catalogue reaches an estimated 150,000–500,000 SKUs.
Commerce families are the navigable structure that makes this manageable.

| Code | Commerce Family | Description | Product types |
|---|---|---|---|
| `CMF-NAT` | Natural History | Botanical, ornithological, zoological, entomological, marine prints | Print, digital, framed |
| `CMF-EXP` | Expedition Document | Voyage plates, field studies, coastal surveys, navigation charts | Print, digital |
| `CMF-LND` | Landscape Art | Oil reproduction, watercolour landscape, panoramic view | Print, canvas, framed |
| `CMF-MAP` | Cartographic | Historic maps, charts, expedition surveys, coastal surveys | Print, digital |
| `CMF-ETH` | Ethnographic | Costume, craft documentation, ceremonial object, material culture | Print, digital |
| `CMF-ICH` | Heritage Practice | ICH documentary illustration: craft, maritime, ethnobotanical | Print, digital |
| `CMF-SCI` | Scientific Illustration | Anatomical, geological, astronomical, oceanographic | Print, digital |
| `CMF-EDI` | Editorial / Limited | Curated collections, collector editions, bespoke prints | Print, edition |

### 6.2 Product Type Registry (per NC-PRODUCT-001)

| Product code | Type name | Commerce family | Min tier | Edition model |
|---|---|---|---|---|
| NC-PROD-001 | Giclée Fine Art Print | CMF-NAT / CMF-LND | Tier 3 | Open edition |
| NC-PROD-002 | Digital Download | All families | Tier 3 | Unlimited |
| NC-PROD-003 | Framed Print | CMF-NAT / CMF-LND | Tier 3 | Open edition |
| NC-PROD-004 | Canvas Print | CMF-LND | Tier 3 | Open edition |
| NC-PROD-005 | Archival Print | CMF-EXP / CMF-NAT | Tier 3 | Open edition |
| NC-PROD-006 | Study Print | CMF-SCI | Tier 3 | Open edition |
| NC-PROD-007 | Portfolio Set | All families | Tier 4 | Limited |
| NC-PROD-008 | Digital Collection | All families | Tier 3 | Unlimited |
| NC-PROD-009 | Art Book | CMF-EDI | Tier 4 | Limited |
| NC-PROD-010 | Collector Edition | CMF-EDI | Tier 4 | Strictly limited |
| NC-PROD-ICH-01 | Craft Documentation Print | CMF-ICH | Tier 3 | Open (Gate CS required) |
| NC-PROD-ICH-02 | Ceremonial Object Study | CMF-ICH | Tier 3 | Open (Gate CS required) |
| NC-PROD-ICH-03 | Ethnobotanical Plate | CMF-ICH | Tier 3 | Open (Gate CS required) |
| NC-PROD-ICH-04 | Maritime Heritage Chart | CMF-ICH | Tier 3 | Open (Gate CS required) |
| NC-PROD-ICH-05 | Performance Costume Plate | CMF-ICH | Tier 3 | Open (Gate CS required) |
| NC-PROD-MAP-01 | Historic Map Print | CMF-MAP | Tier 3 | Open edition |
| NC-PROD-MAP-02 | Expedition Survey | CMF-MAP | Tier 3 | Open edition |

### 6.3 Commerce Path Governance

Every product activation follows the NC-PRODUCT-001 eight-gate sequence. ICH products
carry an additional gate (Gate CS) before Gate E.

```
Standard product path:
  Rights verification → PD confirmation → Attribution stack → Gate E

ICH product path:
  Rights verification → PD confirmation → Attribution stack → Gate CS → Gate E

Federal / government image path (NASA/NARA):
  Rights verification (§105) → Nonendorsement check → Gate E
```

### 6.4 Commerce Density Targets

| Publishing tier | Places | Products per place (avg) | Total SKUs (estimate) |
|---|---|---|---|
| Tier 3 (1,000 places) | 1,000 | 3 | ~3,000 |
| Tier 3 (5,000 places) | 5,000 | 5 | ~25,000 |
| Tier 4 (10,000 places) | 10,000 | 8 | ~80,000 |
| Collections across all tiers | — | — | ~15,000–50,000 |

---

## VII. ICH Integration Model

### 7.1 ICH as a Cross-Network Layer

ICH is not a property of individual places — it is a layer connecting places through shared
cultural traditions. At 10,000 places, the ICH layer has five integration patterns.

```
Pattern 1: PLACE ANCHOR
  A single place is the primary cultural home of a practice.
  Example: Noh Theatre → Kyoto / Japan
  Graph: HeritagePractice -[PRACTICED_AT]-> Place

Pattern 2: DISTRIBUTED PRACTICE
  A practice is associated with multiple places in a cultural sphere.
  Example: Falconry → UAE, Saudi Arabia, Morocco, Belgium, Spain, etc. (18 countries)
  Graph: HeritagePractice -[PRACTICED_AT]-> [multiple Places]
         Places -[CULTURALLY_CONNECTED]-> (derived from shared PRACTICED_AT)

Pattern 3: NATURAL-CULTURAL BRIDGE
  An ICH practice connects a natural place to human culture.
  Example: Pacific Navigation -[PRACTICED_AT]-> Papahānaumokuākea
           Pacific Navigation -[USES_TAXON]-> Star paths (conceptual) / Frigate Bird (navigation marker)
  Graph: HeritagePractice -[PRACTICED_AT]-> Place -[WITHIN_BIOREGION]-> OceanicBioregion
         HeritagePractice -[USES_TAXON]-> Taxon -[OCCURS_AT]-> Place

Pattern 4: EXPEDITION DOCUMENTATION
  A historical expedition documented an ICH practice as primary content.
  Example: Cook voyages documented Pacific navigation and Hawaiian ceremony
  Graph: Expedition -[VISITED_BY]-> Place
         HeritagePractice -[DOCUMENTED_CULTURE]-> Expedition
         Expedition -[PART_OF_VOYAGE]-> Place (Cook route places)

Pattern 5: MATERIAL CONNECTION
  Practices across different places share a material tradition.
  Example: Silk weaving (Japan) → Silk weaving (Uzbekistan) → Silk weaving (Thailand)
  These are NOT the same practice but share material domain (ICH-6: evidence-based only)
  Graph: HeritagePractice -[SHARES_MATERIAL]-> Material -[SHARES_MATERIAL (reverse)]-> HeritagePractice
         Material node is new (add to registry via G-8)
```

### 7.2 ICH × Commerce Eligibility Matrix

| ICH UNESCO domain | Code | Commerce path | Sensitivity default | Notes |
|---|---|---|---|---|
| Oral traditions and expressions | OT | Indirect only (no direct ICH product) | consult | Story context only; the oral tradition is never the product |
| Performing arts | PA | Indirect (costume, instrument illustration) | consult | Documentary illustration only |
| Social practices, rituals, festive events | SP | Indirect (ceremonial object illustration) | restricted or consult | Case-by-case Gate CS |
| Knowledge about nature | NK | **Direct** — ethnobotanical, zoological | none | Strongest ICH-commerce connection |
| Traditional craftsmanship | TC | **Direct** — craft documentation illustration | none | NC-PROD-ICH-01 through 05 |

NK and TC are the two ICH domains with direct commerce paths. All others produce
contextual narrative (story threads) but not primary ICH products.

### 7.3 Global ICH Coverage Targets

| Region | ICH UNESCO elements (approx.) | NC target coverage (v2.0) | Primary institution |
|---|---|---|---|
| East Asia | ~120 | 60 | Met, CMA, SMK |
| South/SE Asia | ~90 | 40 | NHM, Wellcome (pending) |
| Arab States / Middle East | ~70 | 35 | Walters |
| Latin America / Caribbean | ~60 | 25 | NHM (expeditions) |
| Sub-Saharan Africa | ~55 | 20 | Smithsonian NMAFA (pending) |
| Europe / North America | ~80 | 30 | NGA, Europeana |
| Pacific / Oceania | ~25 | 15 | NHM, Trove (pending) |
| Central Asia | ~40 | 15 | Walters, Getty |

### 7.4 ICH Sensitivity Cascade

At 10,000 places, ICH sensitivity decisions must be trackable and reproducible.
The cascade defines the precedence order for sensitivity classification:

```
1. UNESCO ICH element lists 'urgent safeguarding':
   → classification = consult (minimum), review required for commerce
   
2. Practice domain = 'Social practices, rituals, festive events':
   → classification = consult or restricted; never auto-classified 'none'
   
3. Practice has Indigenous community identified in nc_heritage_practices.community_contact:
   → classification = consult; Gate CS mandatory; community_review_status must = 'approved'
   
4. Practice domain = 'Oral traditions':
   → classification = consult; only contextual narrative, no ICH products
   
5. Practice domain = 'Knowledge about nature' OR 'Traditional craftsmanship':
   → classification = none (default); Gate CS advisory only
   
6. Illustrator is from the practicing culture (not European observer):
   → Apply ICH-1 invariant: classification may be upgraded to 'consult' if
     illustration depicts ceremony, ritual, or sacred element
```

---

## VIII. Publishing Tiers

### 8.1 Five-Tier Model — Content Requirements

| Tier | Status | Public | URL active | Min content | Products | Collections | Gate |
|---|---|---|---|---|---|---|---|
| **0 SEED** | `internal_only` | No | No | Slug + canonical ID confirmed | None | None | Gate AR |
| **1 STUB** | `coming_soon` | Yes | Yes | Summary + designation stack + map | None | None | Gate CP (summary) |
| **2 ILLUSTRATED** | `illustrated` | Yes | Yes | Tier 1 + ≥3 illustrations + story thread + family connection | None | ≥1 CF-PLACE | Gate CP (story + headline) |
| **3 COMMERCE** | `live` | Yes | Yes | Tier 2 + full attribution + related places | ≥1 product | ≥1 CF-PLACE, ≥1 eligible family collection | Gate E (two-human) |
| **4 PREMIUM** | `premium` | Yes | Yes | Tier 3 + editorial feature + full discovery paths | ≥3 products | ≥3 collections incl. ≥1 CF-DESIGNATION or CF-EXPEDITION | Gate E re-confirm for new products |

### 8.2 Tier Content Specifications

**Tier 1 STUB — minimum page specification:**
- Place name (official + common name)
- 2-sentence place summary (Gate CP approved)
- Designation stack display (all active HeritageDesignation records)
- Map (PostGIS centroid + boundary if available)
- Place type and domain badge
- Place family memberships (editorial text only, no product link)
- No illustrations, no products, no commerce CTA

**Tier 2 ILLUSTRATED — additions:**
- ≥3 product-safe illustrations with full attribution (artist + institution + year + expedition if applicable)
- Collection headline (Gate CP approved)
- Story thread / editorial feature (2–3 paragraphs, Gate CP approved)
- ICH element cards (if applicable; cultural sensitivity class must = none or approved consult)
- Related places (≥2 PROXIMATE_TO neighbors at Tier 1+)
- "Follow Collection" CTA (no purchase yet)

**Tier 3 COMMERCE — additions:**
- ≥1 active product from NC-PRODUCT-001 registry
- Full attribution stack display (artist + institution + rights statement + GeoNames credit)
- Federal nonendorsement statement (if NASA/NARA sourced)
- Buy CTA + price
- CF-PLACE collection activated with all eligible illustrations
- Related collections navigation (cross-family discovery)
- Breadcrumb: Region → Bioregion → Place Family → Place

**Tier 4 PREMIUM — additions:**
- ≥3 active products
- DESIGNATION_BUNDLE collection (if stack ≥ 3)
- Expedition family collection (if expedition connection confirmed)
- Full graph-driven "Discover next" panel (AX-GEO + AX-HIS + AX-DES traversals)
- ICH collection (if applicable; Gate CS confirmed)
- Editorial feature with AI-generated story thread (Gate CP approved)
- "About this heritage" deep-dive section

### 8.3 Tier Advancement Gates

Tier advancement is irreversible except under:
- Designation status change (In Danger, Delisted) → demote to previous tier pending review
- Rights retraction → demote to Tier 1 or Tier 0 within 15 minutes (G-4)
- ICH sensitivity reclassification to `restricted` → remove ICH products, review all others

```sql
-- Tier advancement is gated at the database level
-- (see nc_place_pipeline_state.gate_e_cleared trigger in NC-PLACES-FACTORY-001)

-- Tier demotion on rights retraction (G-4 compliance)
CREATE OR REPLACE FUNCTION nc_retract_place_commerce()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.rights_status = 'retracted' AND OLD.rights_status <> 'retracted' THEN
    UPDATE nc_place_pipeline_state
    SET tier = LEAST(tier, 1),
        pipeline_status = 'rights_retracted',
        gate_e_cleared = false
    WHERE place_id = NEW.place_id;
    -- Queue Neo4j removal (G-4: within 15 minutes)
    INSERT INTO nc_graph_priority_queue (entity_type, entity_id, action, queued_at)
    VALUES ('place', NEW.place_id, 'REMOVE_COMMERCE_NODES', now());
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 8.4 Tier Distribution Targets

| Version | Total places | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|---|---|
| v0.5 | 100 | 30 | 40 | 20 | 8 | 2 |
| v1.0 | 1,000 | 200 | 400 | 250 | 120 | 30 |
| v1.5 | 2,500 | 400 | 900 | 700 | 400 | 100 |
| v2.0 | 10,000 | 2,000 | 4,000 | 2,500 | 1,200 | 300 |

---

## IX. Governance Tiers

### 9.1 Three Governance Tiers

As the place network scales, governance overhead must scale sublinearly. Three governance
tiers provide appropriate oversight without requiring N×linear human effort.

| Tier | Code | Places covered | Review model | Change cadence |
|---|---|---|---|---|
| Foundation | GOV-F | Tier 0 pilot (≤20 places) | Principal Architect reviews every change | As needed |
| Standard | GOV-S | Tier 1–3 operational (20–2,000 places) | Institutional review; batch approval; exception-flagged | Weekly batch |
| Scale | GOV-SC | Tier 1–2 at bulk (2,000–10,000 places) | Exception-flagging only; auto-approve within bounds | Daily automated |

### 9.2 Governance Tier by Place Classification

| Place condition | Governance tier | Review cadence |
|---|---|---|
| Pilot places (Yellowstone, GBR, Grand Canyon, etc.) | GOV-F | Every change reviewed |
| Mixed WH site (UNESCO_WH_M) | GOV-F | Every change reviewed |
| ICH practice with `consult` sensitivity linked | GOV-S | Change reviewed within 48h |
| UNESCO WH In Danger | GOV-S | Flagged for review within 24h |
| Standard Tier 3 place (no special flags) | GOV-S | Weekly batch approval |
| Tier 1–2 place with no ICH, no sensitivity | GOV-SC | Exception only |

### 9.3 Change Classification Matrix

| Change type | Governance tier required | Gate required | Approval SLA |
|---|---|---|---|
| New place activated (any tier) | ≥ GOV-S | Gate AR + Gate CP | 72h |
| Commerce activation | ≥ GOV-S | Gate E (two-human) | 1 week |
| ICH product added | ≥ GOV-S | Gate CS + Gate E | 72h |
| Cultural sensitivity reclassification | GOV-F | Principal Architect | 24h |
| Designation status change | ≥ GOV-S | Editorial review | 24h |
| Illustration removed (rights retraction) | Any | Automated (G-4) | 15 min |
| Place summary updated (copy change) | ≥ GOV-S | Gate CP | 48h |
| New place family membership | GOV-SC | None (evidence-based) | Automated |
| New PROXIMATE_TO edge | GOV-SC | None (PostGIS derived) | Automated |

### 9.4 Principal Architect Reserves

The following decisions are permanently reserved for Principal Architect or Director Decision.
They cannot be delegated to batch review or automated approval at any scale.

1. Reclassification of any `restricted` ICH practice to `consult` or `none`
2. Commerce activation for any Delisted WH site
3. Commerce activation for any place classified `C.SL.IP` (Indigenous Sacred Place)
4. Addition of a new designation framework to the registry
5. Architectural changes to the place taxonomy (adding types or subtypes)
6. Whitelist expansion for NC-PLACES-FACTORY-001 exclusion overrides
7. Any dispute over canonical GeoNames ID where Wikidata claim conflicts

---

## X. Scale Architecture

### 10.1 Database Architecture

**PostgreSQL partitioning strategy at 10,000 places:**

```sql
-- Place geometry partitioned by region (PostGIS BRIN index for spatial queries)
CREATE TABLE place_geometry (
  -- existing schema
  region_slug TEXT NOT NULL
) PARTITION BY LIST (region_slug);

-- Major region partitions
CREATE TABLE place_geometry_americas   PARTITION OF place_geometry FOR VALUES IN ('north-america', 'south-america', 'caribbean');
CREATE TABLE place_geometry_europe     PARTITION OF place_geometry FOR VALUES IN ('western-europe', 'northern-europe', 'eastern-europe', 'mediterranean');
CREATE TABLE place_geometry_africa     PARTITION OF place_geometry FOR VALUES IN ('sub-saharan-africa', 'north-africa');
CREATE TABLE place_geometry_asia       PARTITION OF place_geometry FOR VALUES IN ('east-asia', 'south-asia', 'southeast-asia', 'central-asia');
CREATE TABLE place_geometry_pacific    PARTITION OF place_geometry FOR VALUES IN ('oceania', 'pacific-islands');
CREATE TABLE place_geometry_polar      PARTITION OF place_geometry FOR VALUES IN ('arctic', 'antarctic');

-- Candidate scoring partitioned by tier for query efficiency
CREATE TABLE nc_place_candidates (
  -- existing schema
  tier_assignment SMALLINT
) PARTITION BY RANGE (tier_assignment);
```

**Indexing strategy at 10,000 places:**

| Table | Index type | Columns | Rationale |
|---|---|---|---|
| `place_geometry` | GiST | `geom` | Spatial queries (ST_Within, ST_DWithin) |
| `place_geometry` | BRIN | `region_slug, centroid` | Range scans by region |
| `nc_places` | GIN | `place_type, designation_types` | Array containment queries |
| `nc_place_candidates` | B-tree | `composite_score DESC` | Score-ordered pagination |
| `nc_heritage_practices` | GIN | `countries` | Country-array containment |
| `nc_place_pipeline_state` | B-tree | `pipeline_status, tier` | Queue processing |
| `canonical_identity` | B-tree | `geonames_id, wikidata_qid` | Authority lookup |

### 10.2 Graph Architecture

**Neo4j cluster topology at 10,000 places:**

```
v1.0 (1,000 places):    AuraDB Professional — 1 primary + 1 read replica
v1.5 (2,500 places):    AuraDB Enterprise or self-hosted 3-node
                        Primary: writes + heavy traversals
                        Replica 1: discovery API reads
                        Replica 2: recommendation engine
v2.0 (10,000 places):   Self-hosted 5-node cluster
                        Primary (1): writes, projection pipeline
                        Secondaries (2): discovery API (load-balanced)
                        Analytics (1): recommendation engine, batch jobs
                        Backup (1): hot standby for G-7 rebuild
```

**Precomputed vs. on-demand traversals:**

| Query type | Strategy | Rationale |
|---|---|---|
| PROXIMATE_TO (place → neighbors) | Precomputed, stored edges | 5M pairs at 10K places; too slow on-demand |
| WITHIN_BIOREGION | Precomputed, stored edges | Stable, changes only when bioregion boundaries update |
| SHARES_DESIGNATION | Derived (2-hop via HeritageDesignation) | <50ms; not precomputed |
| CO_PRACTICED_WITH | Precomputed for top 1000 pairs | Long tail derived on demand |
| SIMILAR_PRODUCT_PROFILE | Derived (no FM writes per G-5) | Commerce scoring never touches graph |
| Discovery journey (full traversal) | On-demand, 3-hop cap | Bounded query time |

### 10.3 Search Architecture

| Scale | Search engine | Strategy | Notes |
|---|---|---|---|
| ≤1,000 places | `pg_trgm` | Trigram similarity on `nc_places.name` + `nc_places.summary` | Existing approach; sufficient |
| 1,000–5,000 places | `pg_trgm` + tsvector | Full-text search on PostgreSQL; combined with trigram | `GIN tsvector index` on `name || ' ' || summary` |
| 5,000–10,000 places | Meilisearch or Typesense | Dedicated search service; synced from PostgreSQL via CDC | Instant as-you-type; faceted by type, region, designation |
| Enterprise (>10,000) | Elasticsearch | Full-document indexing with geo filtering | Defer until warranted |

**Search facets at 10,000 places:**
- Place type (taxonomy Level 1: N.PK, N.MR, C.CL, M.MX, X.DS, etc.)
- Domain (Natural, Cultural, Mixed, Cosmic)
- Designation (UNESCO WH, Biosphere, Geopark, Ramsar, Dark Sky)
- Region (14 regions)
- Place family (50+ named families)
- Commerce tier (Stub / Illustrated / Commerce / Premium)
- ICH domain (5 UNESCO domains)

### 10.4 Image Delivery Architecture

NC PD images at 10,000 places, 5–50 illustrations per place: estimated 150,000–500,000
source images managed through the NC asset pipeline.

| Scale | Delivery model | CDN | Image proxy |
|---|---|---|---|
| ≤1,000 places | Shopify CDN + institution direct | Shopify | imgix or Cloudflare Images |
| 1,000–5,000 places | NC-managed S3 + CloudFront | CloudFront | Cloudflare Images |
| 5,000–10,000 places | Multi-region S3 + CloudFront | CloudFront (multi-edge) | Cloudflare Images + lazy-load |

**Image resolution tiers:**
- Thumbnail (400px): place grid, collection grid — served from NC CDN
- Preview (1200px): place page hero, illustration detail — served from NC CDN
- Full-res (max): digital download product — served from signed S3 URL, time-limited
- Print-ready (TIF/max DPI): fulfilled per order — never publicly cached

### 10.5 API Architecture

```
Public Discovery API (read-only, no auth):
  GET /api/places/{slug}          — place page data
  GET /api/places/{slug}/graph    — neighborhood graph (3-hop cap)
  GET /api/places/{slug}/collection — place collection
  GET /api/families/{slug}        — family page data
  GET /api/search?q=&type=&region= — full-text + faceted search
  Rate limit: 60 req/min per IP

Commerce API (auth: Shopify session or API key):
  GET /api/products/{id}          — product data
  POST /api/cart                  — add to cart (Shopify integration)
  Rate limit: standard Shopify

Internal Factory API (auth: service account):
  POST /api/factory/candidates    — ingest new candidates
  POST /api/factory/score         — trigger composite scoring
  POST /api/factory/authority     — trigger authority resolution
  PUT  /api/places/{slug}/tier    — tier advancement (gated by Gate E)
```

### 10.6 Sync Architecture (PostgreSQL → Neo4j)

At 10,000 places, the sync architecture from NC-GRAPH-002 is extended:

```
Tier 1: Real-time (< 5 min)
  — Rights retraction (G-4: within 15 min)
  — Product activation/deactivation
  Mechanism: PostgreSQL trigger → nc_graph_priority_queue → priority worker

Tier 2: Near-real-time (< 15 min)
  — New illustration added to place
  — Designation status change
  — ICH sensitivity reclassification
  Mechanism: PostgreSQL trigger → nc_graph_change_queue → standard worker

Tier 3: Batch (hourly or nightly)
  — PROXIMATE_TO recomputation (only when new places added)
  — CO_PRACTICED_WITH recomputation
  — Designation stack height update
  — Composite score refresh (when institutions added)
  Mechanism: Scheduled job → bulk projection worker

Tier 4: Full rebuild (G-7: always available)
  — Triggered manually or after schema change (G-8)
  — Drops and rebuilds all Neo4j nodes and relationships from PostgreSQL
  — Target rebuild time: < 12 hours at 10,000 places
  Mechanism: Admin command → full projection worker
```

---

## XI. Reference Model Analysis

### 11.1 What Each Model Contributes

| Reference model | Primary lesson | NC application |
|---|---|---|
| **UNESCO Sites Navigator** | Designation-first navigation; serial site handling; multi-country display; In Danger status display | Designation Stack as primary editorial signal; serial site PART_OF_SERIAL relationship |
| **Google Arts & Culture** | Entity as hub (place, artist, artwork, movement, era all equally traversable); story-layer above the image; mobile-first image browsing | Every entity type is a traversal hub (G-2 equivalent for UX); Story thread as primary editorial layer |
| **National Geographic** | Quality as the non-negotiable; every place is a story, not a data entry; expedition narrative as engagement hook; Maps as primary orientation layer | Family narrative approach; expedition families as the emotional hook for place pages |
| **Smithsonian** | Topic-based cross-disciplinary navigation; institutional depth; "behind the collection" editorial approach | CF-INSTITUTION as a browsable collection; institution provenance as storytelling element |
| **Rijksmuseum** | Artist biography as discovery path; full provenance depth as commerce differentiator; "rijksstudio" downloadable collections | Illustrator families (FAM_IL) as primary artist discovery; full CREATED_BY chain as commerce narrative |

### 11.2 What NC Does Differently

None of these five reference models combines all of:
- **Illustration Opportunity Doctrine** — commerce object is the PD illustration, not the place itself
- **ICH layer** — heritage practices as a first-class discovery and narrative layer
- **Graph-native discovery** — traversal across Expedition → Illustrator → Taxon → Place
- **Rights-constitutional architecture** — PD hard gate, G-4 retraction, FM-4 permanent
- **Designation Stack** — multiple heritage frameworks as a single editorial priority signal

The combination makes NC irreproducible by any existing model. The closest analogy is
the Rijksmuseum's provenance-depth model crossed with NatGeo's place-as-story model,
extended to natural history illustration and intangible heritage.

---

## XII. Governance Invariants

| Code | Invariant |
|---|---|
| **GPN-1** | Every place carries exactly one primary type code and one primary subtype code from the taxonomy defined in Section I. No freeform place types. |
| **GPN-2** | Designation Stack height is computed automatically from `nc_place_designations`. No manual override of stack height. |
| **GPN-3** | Place family membership is derived from evidence (expedition records, proximity, ICH links). Families are not editorially assigned without a supporting evidence record. |
| **GPN-4** | Collection family CF-PLACE is activated at Tier 2. No commerce CTA appears on any CF-PLACE collection below Tier 3. |
| **GPN-5** | ICH products (CMF-ICH) require Gate CS (cultural sensitivity) and Gate E (two-human). No ICH product may be activated by a single approver. |
| **GPN-6** | New relationship types in the discovery graph require G-8 schema registration before deployment. The relationship registry is the authoritative schema. |
| **GPN-7** | `M.MX` (Mixed WH domain) places are permanently in GOV-F (Foundation governance). They may not be delegated to batch review at any scale. |
| **GPN-8** | Rights retraction propagates from PostgreSQL to Neo4j within 15 minutes. Commerce pages for retracted assets are taken offline automatically. |
| **GPN-9** | The global place taxonomy (Section I) may not be modified without a Director Decision and a ratified amendment. Taxonomy stability at 10,000-place scale is architectural. |
| **GPN-10** | The Illustration Opportunity Doctrine applies at every scale. The commercial object is always a PD illustration, never a place, a taxon, a practice, or a designation. |

---

## XIII. Implementation Sequence

### Phase GPN-1: Taxonomy Foundation (prerequisite: NC-PLACES-FACTORY-001 PF-1)
1. Ratify this document
2. Deploy place taxonomy codes to `nc_places.place_type_primary` and `nc_places.place_subtype`
3. Deploy designation taxonomy to `nc_heritage_designations.designation_code`
4. Deploy place family tables (`nc_place_families`, `nc_place_family_members`)
5. Register all new relationship types (G-8) for graph schema

### Phase GPN-2: Family and Collection Layer (v0.5 → v1.0)
1. Classify all 100 places from NC-PLACES-001 into taxonomy codes
2. Assign expedition family memberships for known Cook/Darwin/Audubon places
3. Activate first 5 named expedition families in the graph
4. Activate CF-EXPEDITION and CF-ILLUSTRATOR collection types
5. Launch first DESIGNATION_BUNDLE collection (GBR stack-4 bundle)

### Phase GPN-3: Full Discovery Graph (v1.0)
1. Deploy BORDERS, PART_OF_SERIAL, SHARES_ECOSYSTEM relationship types
2. Deploy MEMBER_OF_FAMILY, CULTURALLY_CONNECTED, PRECEDED_BY types
3. Deploy WITHIN_FLYWAY, WITHIN_CURRENT, CONNECTED_BY_WATERSHED types
4. Run full graph projection for all 1,000 places
5. Activate search facets (type, designation, family, region)

### Phase GPN-4: Scale Architecture (v1.5 → v2.0)
1. Deploy PostgreSQL partitioning by region
2. Upgrade Neo4j to 3-node cluster (AuraDB Enterprise)
3. Deploy Meilisearch sync from PostgreSQL (at 5,000 places)
4. Activate all 10 collection families
5. Target: 10,000-place taxonomy fully populated

---

*NC-PLACES-1000 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
