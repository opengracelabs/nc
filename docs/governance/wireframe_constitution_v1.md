# Nature & Culture Wireframe Constitution v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified |
| Repository | opengracelabs/nc |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |
| Governs | Information architecture — pages, hierarchies, navigation |

---

## Architecture Conflict — Flag Before Ratification

The mission brief lists Neo4j and pgvector as current architecture. Neither is present in
`infrastructure/postgres/init/00_extensions.sql` or any migration file. The Strategic
Direction v1 (2026-06-07) explicitly freezes the stack at PostgreSQL, MinIO, FastAPI,
and Docker Compose — excluding new databases, Neo4j, and vector databases.

**Ruling:** This constitution is designed against the frozen stack.

- Graph traversal (related places, creator networks): PostgreSQL recursive CTEs.
- Spatial discovery: PostGIS (present and confirmed in `00_extensions.sql`).
- Text search: `pg_trgm` trigram indexes (present) + faceted filters.
- Semantic similarity: Not available without pgvector. Discovery uses score-based
  similarity (PostgreSQL proximity on scoring signal vectors in `score_inputs JSONB`).
  Any amendment adding pgvector must pass Director approval and amend the Strategic
  Direction v1 frozen stack clause.

---

## Preamble

This Constitution governs the information architecture of the Nature & Culture platform.
It defines what information exists on each page, in what order, and with what relationships.
It does not govern visual design, layout, color, or typographic treatment.

NC is a place-centered public-domain heritage commerce platform. The governing identity:
**"The Library of Commerce for the world's public domain heritage."**

Every IA decision must answer: does this help users discover, understand, and purchase
the best public-domain heritage assets connected to a place?

NC's content types are governed by the Media Substrate Constitution v1.2. The fourteen
user-facing types — Places, Stories, Maps, Photography, Botanical Art, Fine Art, Posters,
Books, eBooks, Audiobooks, Audio, Film, 3D, Datasets — map to governed backend entities as
follows:

| User-facing type | Backend entity | Phase | Anchor type |
|---|---|---|---|
| Places | `places` table | Always | — |
| Stories | Editorial content (NC-authored) | Always | — |
| Maps | `source_item`, `media_type_id = 'map'` | Phase 1 | geographic |
| Photography | `source_item`, `media_type_id = 'photography'` | Phase 1 | geographic / cultural |
| Botanical Art | `source_item`, `media_type_id = 'image'`, `anchor_type = 'biological'`, botany subject | Phase 1 | biological |
| Fine Art | `source_item`, `media_type_id = 'image'`, `anchor_type = 'cultural'` | Phase 1 | cultural |
| Posters | `source_item`, `media_type_id = 'poster'` | Phase 1 | any |
| Books | `source_item`, `media_type_id = 'book'` | Phase 2 | any |
| eBooks | `source_item`, `media_type_id = 'ebook'` | Phase 2 | any |
| Audiobooks | `source_item`, `media_type_id = 'audiobook'` | Phase 2 | any |
| Audio | `source_item`, `media_type_id = 'audio'` | Phase 3 | any |
| Film | `source_item`, `media_type_id = 'film'` | Phase 3 | any |
| 3D | `source_item`, `media_type_id = '3d'` | Phase 4 | any |
| Datasets | `source_item`, `media_type_id = 'dataset'` | Phase 4 | any |

Botanical Art and Fine Art are content categories, not `media_type_id` values. They are
surfaced as user-facing labels through subject term classification and anchor_type. The
backend does not have a `botanical_art` media type.

Stories are NC-authored editorial content, not `source_item` records. They are not
governed by the Media Substrate Constitution. They link to `source_item`, `places`,
`collections`, and `creators`.

---

## Part I — Primary Navigation Hierarchy

### Article 1 — L1 Navigation (Global)

Five primary navigation destinations. All are persistent across all pages.

```
L1 PRIMARY NAV
├── Places
├── Discover
├── Stories
├── Collections
└── Shop
```

Utility navigation (persistent, not primary):

```
UTILITY NAV
├── Search  (global, always accessible)
├── Account
└── Cart
```

**Places** is listed first because it is NC's primary anchor and deepest moat.
**Discover** is the thematic/browse entry for users who are not place-led.
**Stories** is the editorial seduction layer (National Geographic reference).
**Collections** is the curated commercial destination.
**Shop** is the direct commerce entry for buyers who already know what they want.

### Article 2 — L2 Navigation (Per Primary Destination)

```
Places
├── By Continent
│   ├── Africa
│   ├── Americas
│   ├── Asia & Pacific
│   ├── Europe
│   └── Middle East
├── By Heritage Type
│   ├── Natural Heritage
│   ├── Cultural Heritage
│   └── Mixed Heritage
├── Featured Places
├── UNESCO World Heritage Sites
├── Endangered Sites
└── Map View  (PostGIS spatial browse)

Discover
├── By Media Type
│   ├── Historic Maps
│   ├── Photography
│   ├── Botanical Art
│   ├── Natural History Illustration
│   ├── Fine Art
│   ├── Posters
│   ├── Books & Documents
│   ├── Audio
│   ├── Film
│   ├── 3D Models
│   └── Datasets
├── By Creator
│   ├── Featured Illustrators
│   │   ├── John James Audubon
│   │   ├── John Gould
│   │   ├── Maria Sibylla Merian
│   │   ├── Pierre-Joseph Redouté
│   │   ├── Edward Lear
│   │   ├── Frederick Polydore Nodder
│   │   ├── Ernst Haeckel
│   │   └── Joseph Wolf
│   └── All Creators  (A–Z)
├── By Era
│   ├── Golden Age (1750–1900)  [constitutionally featured]
│   ├── Victorian (1837–1901)
│   ├── Edwardian (1901–1910)
│   ├── Early Modern (1500–1750)
│   └── All Eras
├── By Institution
│   ├── Biodiversity Heritage Library
│   ├── Library of Congress
│   ├── Smithsonian Institution
│   ├── Internet Archive
│   ├── British Library
│   └── All Institutions
└── By Theme
    ├── Expeditions & Exploration
    ├── Gardens & Botany
    ├── Oceans & Marine Life
    ├── Birds
    ├── Insects & Entomology
    ├── Heritage Architecture
    └── Natural Landscapes

Stories
├── Latest
├── Featured
├── By Theme
└── By Place

Collections
├── New Collections
├── Best Sellers
├── By Place
├── By Media Type
└── By Theme

Shop
├── Wall Art
│   ├── Premium Prints
│   └── Standard Prints
├── Calendars
├── Puzzles
├── Cards & Stationery
├── Books & Print
├── Educational License
└── Institutional License
```

### Article 3 — URL Hierarchy

```
/                           Homepage
/places                     Place browse root
/places/{continent}         Continent browse
/places/{continent}/{slug}  Place page
/discover                   Discovery root
/discover/media/{type}      Media type browse
/discover/creator/{slug}    Creator page
/discover/era/{label}       Era browse
/discover/institution/{id}  Institution page
/stories                    Stories root
/stories/{slug}             Story page
/collections                Collections root
/collections/{slug}         Collection page
/shop                       Shop root
/shop/{product-type}        Product type browse
/media/{id}                 Media item page (canonical)
/search                     Search results
```

---

## Part II — Seven Hierarchies

### Article 4 — Place Hierarchy

The place hierarchy has two axes: geographic and classificatory. Navigation uses geographic
as primary, with classificatory as filter.

**Geographic axis (primary navigation order):**

```
World
└── Continent  (Africa / Americas / Asia & Pacific / Europe / Middle East)
    └── Country / Region
        └── Place  (the governed `places` entity)
            └── Place Feature  (sub-area, section, named feature)
```

**Classificatory axis (filter layer):**

```
Heritage Type
├── Natural Heritage
├── Cultural Heritage
└── Mixed Heritage

UNESCO OUV Criteria  (i through x)
├── Criteria i–vi  (Cultural)
└── Criteria vii–x  (Natural)

Inscription Status
├── Inscribed
├── Inscribed (in danger)
└── Extended

Ecosystem / Built Type
├── Forest / Woodland
├── Marine / Coastal
├── Mountain / Alpine
├── Desert / Arid
├── Wetland / Freshwater
├── Urban Heritage
├── Archaeological Site
├── Religious Monument
├── Palace / Garden
└── Industrial Heritage

Time Period
├── Ancient (pre-500 CE)
├── Medieval (500–1500 CE)
├── Early Modern (1500–1750 CE)
├── Modern (1750–1900 CE)
└── Contemporary (1900–present)

Country / Sovereign Territory
├── By ISO 3166-1 alpha-2 code
└── Transboundary sites  (flag where applicable)
```

**Place relationship graph (PostgreSQL CTE traversal):**

```
Place → Related Places
    ├── Same country
    ├── Same UNESCO criteria
    ├── Same ecosystem type
    └── Geographically proximate  (PostGIS radius query)
```

### Article 5 — Media Hierarchy

The media hierarchy has two axes: format (what it is technically) and content category
(what it depicts). The IA surfaces content category first; format is a filter.

**Content category axis (user-facing primary):**

```
Natural History
├── Botanical Illustration  [image + biological + plant subject]
├── Zoological Illustration  [image + biological + animal subject]
│   ├── Birds (Ornithology)
│   ├── Insects (Entomology)
│   ├── Marine Life
│   ├── Mammals
│   └── Reptiles & Amphibians
├── Botanical Photography
└── Wildlife Photography

Geography & Cartography
├── Historic Maps  [map]
│   ├── World & Continental Maps
│   ├── Regional & Country Maps
│   ├── City Plans & Panoramas
│   ├── Sea Charts & Navigation
│   └── Expedition & Survey Maps
└── Topographic Views  [image + geographic]

Photography  [photography]
├── Heritage Site Photography
├── Expedition Photography
├── Architectural Photography
├── Portrait Photography
└── Documentary Photography

Fine Art  [image + cultural]
├── Landscape Painting
├── Architectural Rendering
├── Portraiture
└── Still Life & Interior

Ephemera  [poster]
├── Natural History Posters
├── Geographic & Travel Posters
├── Scientific Diagrams
└── Trade & Exhibition Labels

Books & Documents  [book / ebook]
├── Natural History Books
├── Travel & Expedition Journals
├── Scientific Journals
├── Field Guides & Monographs
└── Historical Atlases

Audio  [audiobook / audio]
├── Natural History Audiobooks
├── Field Recordings
├── Oral History
└── Historical Music (Archive)

Film & Moving Image  [film]
├── Nature Documentary (Archive)
├── Expedition Film
└── Heritage Site Film

Three-Dimensional  [3d]
├── Natural Specimens
├── Archaeological Objects
└── Architectural Models

Data  [dataset]
├── Species Occurrence Data
├── Geographic Heritage Data
└── Heritage Survey Data
```

**Format axis (technical filter — maps to `media_type_id`):**

```
Images
Maps
Photography
Posters
Books
eBooks
Audiobooks
Audio
Film
3D Models
Datasets
```

**Quality axis (filter — maps to `csm_tier`):**

```
MASTERWORK  (CSM 90–100)
FLAGSHIP    (CSM 75–89)
STANDARD    (CSM 60–74)
REFERENCE   (CSM 40–59)
```

**Era axis (filter — maps to `publication_year`):**

```
Golden Age (1750–1900)  [constitutionally featured — primary era filter]
Early Modern (1500–1750)
Victorian (1837–1901)
Edwardian (1901–1910)
Pre-1900 (all public domain)
```

### Article 6 — Discovery Hierarchy

Discovery governs how users find assets they did not know they were looking for. Five
entry modes are supported; each has its own traversal path.

**Entry Mode 1: Editorial (curated seduction)**

```
Homepage feature → Story → embedded media → Collection → individual asset → product
Homepage feature → Featured Place → place page → media browse → asset → product
```

**Entry Mode 2: Geographic (place-led)**

```
Map View (PostGIS) OR continent browse
  → Country/Region browse
    → Place page
      → media type filter
        → media item (source_item)
          → product options
```

**Entry Mode 3: Subject/Theme (thematic)**

```
Discover / By Theme
  → Theme landing (e.g., Expeditions & Exploration)
    → filtered media grid (score-ranked)
      → media item
        → product options
```

**Entry Mode 4: Creator-led**

```
Discover / By Creator
  → Creator page (Audubon, Gould, etc.)
    → creator's works (all media types, score-ranked)
      → media item
        → product options
```

**Entry Mode 5: Search**

```
Global search (pg_trgm trigram match on: title, taxon_name, place names,
               publication_title, illustrator, subject_terms, era)
  → Ranked results list (grouped by: Places / Media / Collections / Stories)
    → Faceted filter refinement
      → media item or place page
        → product options
```

**Faceted filter vocabulary (universal across all browse contexts):**

```
Filters
├── Media Type  (format axis values)
├── Content Category  (content axis values)
├── Place  (linked place)
├── Continent  (derived from place.country_codes)
├── Heritage Type  (place.heritage_type)
├── Creator  (illustrator)
├── Institution  (source institution)
├── Era  (publication year range)
├── Quality Tier  (csm_tier)
└── Rights Statement  (media_rights.rights_statement_uri — all are PD/CC0; filter by specific statement)
```

**Sort vocabulary (universal across all browse contexts):**

```
Sort
├── Best Match  (relevance score, default for search)
├── Highest Scored  (csm_score DESC, default for browse)
├── Newest to Platform  (activated_at DESC)
├── Oldest Era  (publication_year ASC)
├── Newest Era  (publication_year DESC)
└── Alphabetical  (title ASC)
```

### Article 7 — Commerce Hierarchy

Commerce appears at three levels: individual asset, collection, and licensing.
It is embedded contextually on every relevant page, not siloed to a Shop section.

**Product type hierarchy:**

```
Commerce Products
├── Wall Art
│   ├── Museum Premium Print  (MASTERWORK / FLAGSHIP)
│   ├── Standard Print  (STANDARD and above)
│   └── Digital Download
├── Home & Gift
│   ├── Calendar  (12-asset collection or single)
│   ├── Puzzle  (FLAGSHIP and above)
│   └── Cards & Stationery
├── Publishing & Editorial
│   ├── Book Illustration License
│   └── Editorial License
├── Institutional
│   ├── Museum Print License
│   └── Institutional Use License
└── Educational
    └── Educational License  (REFERENCE tier and above)
```

**Commerce eligibility by tier (from `commerce_opportunities`):**

```
MASTERWORK   → Wall Art (museum premium) + All home & gift + All publishing + All institutional + Educational
FLAGSHIP     → Wall Art (standard) + Puzzle + Cards + Publishing + Institutional + Educational
STANDARD     → Wall Art (standard) + Cards + Editorial + Educational
REFERENCE    → Educational only + Digital Download
BLOCKED      → No commerce
```

**Commerce hierarchy per page:**

```
Media Page  → "Available as" block → primary product CTA → License option
Place Page  → "Shop this Place" rail → top-scored assets with buy CTAs
Collection Page  → Collection bundle CTA + individual asset CTAs
Institution Page  → "License from this institution" inquiry CTA
Story Page  → commerce rail on linked media and collections
```

**Licensing hierarchy (B2B — Era 2 stub):**

```
Licensing
├── Single Asset License
│   ├── Editorial Use
│   ├── Commercial Use
│   ├── Educational Use
│   └── Institutional Use (museum / exhibition)
└── Collection License
    ├── Thematic Bundle
    ├── Place Bundle
    └── Institutional Catalog Access
```

### Article 8 — Tourism Hierarchy

Tourism is a signal layer, not a platform. NC does not build travel booking, itinerary
tools, or destination guides. Tourism surfaces as contextual enrichment on place pages and
as a commerce category for destination-oriented products.

**Tourism intelligence hierarchy:**

```
Tourism Context (on Place Pages)
├── UNESCO WHC status badge  (inscription year, heritage type)
├── Outstanding Universal Value summary  (abbreviated OUV statement)
├── Tourism Attractiveness Signal  (TAS — derived from scoring, not displayed as raw score)
│   ├── "Iconic Heritage Site"  (TAS ≥ 0.85)
│   ├── "Major Heritage Site"   (TAS 0.70–0.84)
│   ├── "Notable Heritage Site" (TAS 0.50–0.69)
│   └── [no tourism label]     (TAS < 0.50)
├── Geographic context  (PostGIS — country, region, nearby sites)
└── Seasonal context  (winter/summer collections where applicable)

Tourism Commerce (product framing)
├── "Art of [Place]" — place-anchored wall art collections
├── "Journey Through [Region]" — curated route collections
├── Travel Posters  (poster media type + geographic anchor)
└── Destination Calendars  (12 assets × 1 place or region)

Tourism B2B (licensing destination)
└── "License for Tourism Use"  (institutional licensing inquiry form)
```

**Tourism browse entry (under Discover):**

```
Discover / By Theme / Heritage Travel
├── By Destination  → links to place pages
├── Iconic World Heritage Sites  (TAS ≥ 0.85)
├── Natural World Heritage  (heritage_type = 'natural')
├── Cultural World Heritage  (heritage_type = 'cultural')
└── Endangered Heritage Sites
```

### Article 9 — Education Hierarchy

Education is a licensing category and content framing, not a platform. NC does not build
an LMS, curriculum tools, or student accounts. Education surfaces as a license type on
REFERENCE tier assets and as a content framing for research and scholarly use.

**Educational content hierarchy:**

```
Educational Content Categories
├── Natural Sciences
│   ├── Botany  (botanical art + botanical books + field guides)
│   ├── Zoology  (natural history illustration + zoological books)
│   ├── Marine Biology
│   ├── Entomology
│   └── Ecology & Geography
├── Earth Sciences
│   ├── Cartography & Maps  (historic maps + survey maps)
│   ├── Geology & Landscape
│   └── Oceanography
├── History & Culture
│   ├── Art History  (fine art + posters + illustration history)
│   ├── Exploration History  (expedition photography + maps + journals)
│   └── Heritage Architecture
└── Data & Research
    ├── Species Occurrence Datasets
    ├── Heritage Survey Data
    └── Cartographic Data

Educational License Types
├── Single Asset — Educational Use (perpetual, non-exclusive)
├── Classroom Bundle (≤30 assets, one institution)
└── Institutional License (unlimited use, one academic institution)

Educational Browse Entry
└── Shop / Educational License
    ├── By Subject  (maps to educational content categories above)
    ├── By Format  (image / map / book / dataset)
    ├── CC0 Only  (unrestricted reuse — no license required)
    └── Downloadable  (assets with digital download enabled)
```

**Educational commerce eligibility:** All assets with `csm_tier != 'BLOCKED'` and
`media_rights.rights_status IN ('verified_pd', 'verified_cc0')` are eligible for
educational licensing. CC0 assets are explicitly marked as requiring no license.

---

## Part III — Page Information Architecture

### Article 10 — Homepage

```
URL: /

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: GLOBAL NAVIGATION
  BLOCK: Primary Nav
    • Places
    • Discover
    • Stories
    • Collections
    • Shop
  BLOCK: Utility Nav
    • Search
    • Account
    • Cart

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: IDENTITY
  BLOCK: Platform Statement
    • One-sentence mission: "The Library of Commerce for the world's public domain heritage."
    • Tagline (optional editorial)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: HERO
  DATA SOURCE: Editorially selected. One featured asset at a time.
  Rotating. Selection governed by: csm_tier = MASTERWORK AND anchor_type is any.
  BLOCK: Hero Media
    • Primary media asset (IIIF delivery — zoomable)
    • Asset title
    • Creator name
    • Place connection  (linked)
    • Era / Year
    • Rights statement badge
  BLOCK: Hero Context
    • Short editorial sentence (one line)
    • CTA: "Explore this Place"
    • CTA: "View Collection"
    • CTA: "Shop this Piece"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: SEARCH
  BLOCK: Global Search
    • Search input (pg_trgm — title, place, creator, subject)
    • Placeholder text: "Search by place, artist, subject, or era"
    • Autocomplete: Place names + Creator names + Subject terms
    • No filters on homepage — filters appear on results page

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: FEATURED COLLECTIONS
  DATA SOURCE: collections WHERE status = 'published', ordered by editorial priority.
  Max 4 items.
  BLOCK: Collection Card × 4
    • Collection title
    • Collection type (place_theme / taxon_theme / seasonal / curated_set)
    • Primary place name (if place_theme)
    • Asset count
    • Thumbnail (highest-scored asset in collection)
    • CTA: "View Collection"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: EXPLORE BY PLACE
  DATA SOURCE: places WHERE status = 'active', ordered by TAS DESC. Max 8 items.
  BLOCK: Place Grid
    • For each place:
      • Place name
      • Country flag / code
      • Heritage type badge (Natural / Cultural / Mixed)
      • Top-scored asset thumbnail (from illustration_opportunities/source_items)
      • Asset count for this place
    • CTA: "Explore all Places"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: EXPLORE BY MEDIA
  DATA SOURCE: media_type_registry WHERE status = 'active'. Static content labels
  supplement pending types as "Coming Soon."
  BLOCK: Media Type Grid
    • For each content category (user-facing label, not media_type_id):
      • Category label (Maps / Botanical Art / Photography / Fine Art / Posters / Books / etc.)
      • Representative thumbnail
      • Asset count (active source_items in this category)
      • Phase badge for pending types: "Coming Soon"
    • All 14 user-facing types listed; Phase 2–4 show Coming Soon state

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: FEATURED CREATORS
  DATA SOURCE: creator_prestige_registry WHERE applies_to_anchor_types covers Phase 1
  active types. Priority order from Illustration Opportunity Doctrine.
  BLOCK: Creator Cards × 8 (priority illustrators)
    • For each creator:
      • Creator name
      • Era / active dates
      • Prestige label (if applicable)
      • Representative work thumbnail
      • Work count
      • CTA: "View Works"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: ERA SPOTLIGHT
  DATA SOURCE: Editorially configured. Default: Golden Age 1750–1900.
  BLOCK: Era Feature
    • Era name: "The Golden Age of Natural History (1750–1900)"
    • Editorial one-paragraph context (NC-authored)
    • Asset count from this era
    • 6 representative assets (score-ranked, diverse media types)
    • CTA: "Explore the Golden Age"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: STORIES
  DATA SOURCE: NC-authored editorial stories. Max 3 featured.
  BLOCK: Story Cards × 3
    • Story title
    • Subtitle / hook sentence
    • Hero image (linked source_item)
    • Place connection
    • Read time estimate
    • CTA: "Read Story"
  BLOCK: Stories Entry
    • CTA: "All Stories"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: INSTITUTIONS
  DATA SOURCE: sources WHERE governance_state = 'active', ordered by priority ASC.
  Max 6 items.
  BLOCK: Institution Strip
    • Institution name
    • Asset count from this institution
    • CTA: "Browse [Institution]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COMMERCE ENTRY
  BLOCK: Commerce Pathways
    • "Shop the Collection" → /collections
    • "License for Commercial Use" → /shop/institutional-license
    • "Educational License" → /shop/educational-license

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: FOOTER
  BLOCK: Navigation
    • Places / Discover / Stories / Collections / Shop
  BLOCK: Institution Links
    • Links to all active source institution pages
  BLOCK: Legal
    • Rights statement: all assets are public domain or CC0
    • Rights vocabulary citations (rightsstatements.org)
    • Privacy, Terms, DMCA contact
  BLOCK: About
    • About NC
    • How assets are verified
    • Licensing FAQ
    • API / B2B inquiry
```

---

### Article 11 — Place Page

```
URL: /places/{continent}/{slug}
DATA SOURCE: places table + illustration_opportunities/source_items + collections

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: BREADCRUMB
  BLOCK: Place Hierarchy
    • World → {Continent} → {Country} → {Place Name}
    • Each level is a linked browse destination

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: PLACE IDENTITY
  BLOCK: Primary Identity
    • Place name  (places.name — English primary)
    • UNESCO World Heritage Site badge  (if applicable — inscription year)
    • Heritage type badge  (Natural / Cultural / Mixed)
    • Country / countries  (places.country_codes)
    • Continent
    • Inscription year
    • Endangerment status  (if endangered_since IS NOT NULL)
  BLOCK: Place Signals
    • Tourism attractiveness label  (derived from TAS tier — not raw score)
    • Total asset count by type  (image / map / photography / poster / etc.)
    • Collection count
    • OUV criteria badges  (i through x, where applicable)
  BLOCK: Primary Media
    • Best-scored asset for this place  (csm_score DESC, anchor_type matching place)
    • Asset title, creator, era
    • "View this piece" link

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: PLACE STATEMENT
  BLOCK: Outstanding Universal Value
    • OUV statement  (places.statement_of_ouv — abbreviated, max 200 words)
    • Criteria listed
    • "Learn More" → source institution / UNESCO link

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: PLACE GEOGRAPHY
  BLOCK: Spatial Context
    • Geographic coordinates  (places.centroid — PostGIS)
    • Area  (places.area_ha, core_area_ha)
    • Spatial map view  (PostGIS boundary rendering)
    • Nearby UNESCO sites  (PostGIS radius query, linked)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: MEDIA BY TYPE
  One sub-zone per active media type that has assets for this place.
  Rendered in constitutional activation order (Phase 1 first).
  Empty types are not shown.

  SUB-ZONE: Maps  [media_type_id = 'map', place-linked]
    BLOCK: Map Grid
      • Score-ranked source_items (csm_score DESC)
      • For each: thumbnail, title, creator, era, institution badge
      • Max 6 shown on page load; "View all Maps of {Place}" link
      • Era filter: Golden Age / Pre-1900 / All

  SUB-ZONE: Illustrations  [image, anchor_type = 'biological', place-linked]
    BLOCK: Illustration Grid
      • Score-ranked source_items
      • For each: thumbnail, title, taxon name, creator, era, institution badge
      • Subcategory filter: Botanical / Zoological / Marine / Birds / All
      • Max 6 shown; "View all Illustrations of {Place}" link

  SUB-ZONE: Photography  [photography, place-linked]
    BLOCK: Photography Grid
      • Score-ranked source_items
      • For each: thumbnail, title, creator, era, institution badge
      • Max 6 shown; "View all Photography of {Place}" link

  SUB-ZONE: Fine Art & Landscape  [image, anchor_type = 'cultural' / 'geographic', place-linked]
    BLOCK: Fine Art Grid
      • As above

  SUB-ZONE: Posters  [poster, place-linked]
    BLOCK: Poster Grid
      • As above

  SUB-ZONE: Books & Documents  [book / ebook, place-linked — Phase 2 stub]
    BLOCK: Coming Soon state  (if no active assets; shown when Phase 2 activates)

  SUB-ZONE: Audio  [audiobook / audio, place-linked — Phase 3 stub]
    BLOCK: Coming Soon state

  SUB-ZONE: Film  [film, place-linked — Phase 3 stub]
    BLOCK: Coming Soon state

  SUB-ZONE: 3D Models  [3d, place-linked — Phase 4 stub]
    BLOCK: Coming Soon state

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COLLECTIONS
  DATA SOURCE: collections linked to this place via collection_places
  BLOCK: Place Collections Grid
    • Collection title, type, asset count
    • Thumbnail
    • CTA: "View Collection"
  BLOCK: Empty state if no collections
    • "No collections yet — check back soon"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: STORIES
  DATA SOURCE: NC-authored stories linking to this place
  BLOCK: Story Cards
    • Story title, hook, thumbnail, CTA
  BLOCK: Empty state if no stories

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: RELATED PLACES
  DATA SOURCE: PostGIS proximity query + shared OUV criteria + same heritage type
  BLOCK: Related Place Cards × 4–6
    • Place name, heritage type, country
    • Best-scored thumbnail
    • Asset count
    • Relationship label: "Nearby" / "Same ecosystem" / "Same criteria"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: INSTITUTIONS
  DATA SOURCE: sources contributing assets to this place
  BLOCK: Contributing Institutions Strip
    • Institution name
    • Asset count from this institution for this place
    • "Browse [Institution]" link

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COMMERCE RAIL  (persistent, contextual)
  BLOCK: Shop This Place
    • "Shop the Art of {Place Name}"
    • Top 3 products (highest-scored, MASTERWORK/FLAGSHIP preferred)
    • CTA: "View all products for {Place}"
    • CTA: "License for Commercial Use"
```

---

### Article 12 — Media Page

```
URL: /media/{id}
DATA SOURCE: source_item + commerce_opportunities + asset_delivery_manifest +
             media_technical_metadata + media_rights + places + creator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: BREADCRUMB
  BLOCK: Context Trail
    • {Continent} → {Country} → {Place} → {Media type category} → {Asset title}
    • Each level linked

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: PRIMARY MEDIA
  BLOCK: Media Viewer
    • IIIF viewer for image / map / photography / poster
    • IIIF Presentation API 3.0 manifest (from asset_delivery_manifest.manifest_payload)
    • Controls: zoom in / zoom out / full screen / download (if licensed)
    • For Phase 2–4 types: format-appropriate viewer (epub-js / html5-audio / hls / model-viewer)
  BLOCK: Media Identity
    • Title  (source_item title or derived from source_record)
    • Media type badge  (Maps / Botanical Art / Photography / Fine Art / Poster / etc.)
    • Quality tier badge  (MASTERWORK / FLAGSHIP / STANDARD / REFERENCE)
    • Rights statement badge  (plain-language: "Public Domain" / "CC0")
    • Rights statement URI  (linked to rightsstatements.org)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: CREATOR & PROVENANCE
  BLOCK: Creator
    • Creator name  (linked to creator page)
    • Creator prestige label  (from creator_prestige_registry — if applicable)
    • Creator era / active dates
  BLOCK: Source Institution
    • Institution name  (linked to institution page)
    • Institution tier badge  (Tier 1 Constitutional / Tier 2 Operational)
  BLOCK: Publication Context
    • Publication title  (BHL title or source_record derived)
    • Publication year / era label
    • Volume, page reference  (if applicable)
    • Source URL  (linked to source institution record)
  BLOCK: Rights Provenance
    • Rights status  (media_rights.rights_status, plain language)
    • Rights evidence summary  (abbreviated — full detail available on expand)
    • Verified by / Verified at  (media_rights.verified_by, verified_at)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: SUBJECT & TAXONOMY
  BLOCK: Subject Terms
    • TGM subject terms  (linked — each links to a subject browse)
    • Subject category (Botanical / Zoological / Cartographic / etc.)
  BLOCK: Taxon Connection  (if anchor_type = 'biological')
    • Scientific name  (linked to concept)
    • Common name
    • Taxon rank
    • GBIF / Wikidata link (where available)
  BLOCK: Place Connections
    • All linked places  (from illustration_opportunity_places)
    • Each: place name, relevance score (shown as signal — "Primary Location" / "Related")
    • Linked to place pages

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: TECHNICAL DETAILS
  BLOCK: Technical Metadata
    • Media type (format label)
    • Dimensions (pixels, if applicable — from media_technical_metadata.content)
    • Resolution tier (from commerce_opportunities.resolution_tier)
    • Archival format
    • Quality flag (from media_technical_metadata.content.quality_flag — shown only if flagged)
  BLOCK: Substrate Record
    • Activated at (activation_target.approved_at)
    • Source institution record ID (linked)
    • "Full technical details" expandable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COMMERCE
  DATA SOURCE: commerce_opportunities for this source_item
  BLOCK: Commerce Tier
    • CSM tier badge (MASTERWORK / FLAGSHIP / STANDARD / REFERENCE)
    • Commerce tier label (from commerce_tier)
  BLOCK: Available Products
    • For each eligible product type (from eligible_* flags on commerce_opportunities):
      • Product name
      • Product format options (sizes, etc.)
      • Price
      • "Add to Cart" CTA
    • Primary CTA highlighted (highest-value eligible product)
  BLOCK: License Options
    • "License for Editorial Use"
    • "License for Commercial Use"
    • "Educational License"
    • "Institutional License"
    • Each: short description + "Inquire" or "Buy License" CTA
  BLOCK: Save / Wishlist
    • "Save this piece"
    • "Add to Lightbox"  (for institutional/B2B users)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: RELATED CONTENT
  BLOCK: More from this Creator
    • 4–6 assets from same creator, score-ranked
    • Each: thumbnail, title, place, era
  BLOCK: More from this Place
    • 4–6 assets from same primary place, score-ranked, different creator
    • Each: thumbnail, title, creator, media type
  BLOCK: More from this Institution
    • 4–6 assets from same source institution, score-ranked
    • Each: thumbnail, title, place, creator
  BLOCK: In These Collections
    • Collections containing this asset
    • Each: collection title, type, asset count, CTA
```

---

### Article 13 — Collection Page

```
URL: /collections/{slug}
DATA SOURCE: collections + collection_assets + illustration_opportunities/source_items +
             collection_places + places

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COLLECTION IDENTITY
  BLOCK: Header
    • Collection title
    • Collection type badge  (Place Theme / Natural History / Seasonal / Curated Set)
    • Publication date (collections.published_at)
    • Curator / Editorial attribution  (collections.reviewed_by — human label)
  BLOCK: Primary Place Connection  (if place_theme)
    • Place name, heritage type, country  (linked to place page)
    • Place thumbnail
  BLOCK: Collection Summary
    • Editorial description (collections.summary — multi-sentence)
    • Asset count
    • Media types represented (icons/labels for each type present)
    • Era range (min / max publication year across assets)
    • Institutions contributing (source institutions)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COLLECTION COMMERCE HEADER
  BLOCK: Collection Buy Options
    • "Buy the Collection" CTA (if collection product available)
    • Price range label
    • "License this Collection" CTA (institutional)
  BLOCK: Collection Stats
    • MASTERWORK / FLAGSHIP asset count
    • Available product types in this collection

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COLLECTION BROWSER
  BLOCK: Filter Controls
    • Filter by: Media type / Creator / Era / Quality tier
    • Sort by: Collection sequence / Score / Era
  BLOCK: Asset Grid
    • For each collection_assets entry (ordered by collection sequence):
      • Thumbnail (IIIF delivery)
      • Asset title
      • Creator name (linked)
      • Era / Year
      • Quality tier badge
      • Media type badge
      • Place connection (if different from collection primary place)
      • Primary product CTA ("Buy Print" / "License" / etc.)
      • "View details" link → media page

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COLLECTION CONTEXT
  BLOCK: Places in this Collection
    • All places linked via collection_places (with role: primary / supporting)
    • Each: place name, heritage type, thumbnail
  BLOCK: Creators in this Collection
    • All creators appearing in collection_assets
    • Each: creator name, work count in this collection
  BLOCK: Institutions Contributing
    • All source institutions for assets in this collection
    • Each: institution name, asset count

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: STORIES
  BLOCK: Featured In
    • NC-authored stories that reference this collection
    • Each: story title, hook, CTA

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: RELATED COLLECTIONS
  DATA SOURCE: Collections sharing places, themes, or creators. Score-ranked.
  BLOCK: Related Collection Cards × 3–4
    • Collection title, type, asset count, thumbnail
    • Relationship label: "Same place" / "Same theme" / "Same era"
    • CTA: "View Collection"
```

---

### Article 14 — Institution Page

```
URL: /discover/institution/{source_id}
DATA SOURCE: sources + media_rights + source_items/illustration_opportunities +
             collections + creator_authority_registry

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: INSTITUTION IDENTITY
  BLOCK: Header
    • Institution name  (sources.name)
    • Country of origin
    • Institution type  (Library / Museum / Archive / Digital Repository)
  BLOCK: Constitutional Standing
    • Tier badge: "Tier 1 — Constitutional Governance" OR "Tier 2 — Operational Reference"
      (from Wireframe Constitution Part I / Media Substrate Constitution v1.2, Article 28)
    • Governance state badge: proposed / approved / active / suspended / deprecated / retired
    • Governance domains (for Tier 1): e.g., "Metadata Standards · Rights Vocabulary · PREMIS"
  BLOCK: Institutional Description
    • 2–3 sentence description of institution's mission and relevance to NC
    • Homepage link (external)
    • Standards declared (from sources.standards array)
  BLOCK: Rights Strategy
    • Rights strategy label (from sources.config.rights_strategy)
      Plain-language: "Date-based: US works published before 1928" /
                      "Institutional CC0 dedication" / "Human verification required"
    • Rights statement URIs applicable (linked to rightsstatements.org)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COLLECTION SUMMARY
  BLOCK: Asset Counts
    • Total activated source_items from this institution
    • Breakdown by media type (for each active media_type_id)
    • Breakdown by quality tier (MASTERWORK / FLAGSHIP / STANDARD / REFERENCE)
  BLOCK: Coverage
    • Unique places covered (count, linked to place browse filtered by institution)
    • Unique creators / illustrators represented
    • Era range: earliest and latest publication year in collection
  BLOCK: Publication Year Distribution
    • Era bands: pre-1750 / 1750–1900 (Golden Age) / 1900–1928 / 1928–present
    • Asset count per band

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: FEATURED ASSETS
  DATA SOURCE: source_items from this institution, csm_score DESC, max 12
  BLOCK: Top Assets Grid
    • Thumbnail, title, creator, place, era, quality tier badge
    • "View" link → media page

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: BROWSE THIS INSTITUTION
  BLOCK: Browse Controls
    • Filter by: Media type / Content category / Place / Era / Quality tier
    • Sort by: Score / Era / Alphabetical
  BLOCK: Asset Grid (paginated)
    • As featured assets grid, full browseable set

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: COLLECTIONS FROM THIS INSTITUTION
  DATA SOURCE: Collections where contributing institution = this source
  BLOCK: Collection Cards × max 6
    • Collection title, type, asset count, thumbnail
    • CTA: "View Collection"
  BLOCK: "View all collections from {Institution}" link

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: PLACES COVERED
  DATA SOURCE: places linked to source_items from this institution
  BLOCK: Place Grid × max 8
    • Place name, heritage type, country
    • Asset count from this institution for this place
    • CTA: "View {Place} assets from {Institution}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: CREATORS FROM THIS INSTITUTION
  DATA SOURCE: creators appearing in source_items from this institution
  BLOCK: Creator Strip
    • Creator name, era, work count from this institution
    • Priority illustrators (from creator_prestige_registry) shown first

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: GOVERNANCE REFERENCE  (visible to institutional/B2B users)
  BLOCK: Metadata Standards
    • schema_standard values used by this institution
    • Plain-language description of each standard
  BLOCK: Governance Rules Adopted from This Institution
    • From Media Substrate Constitution v1.2, Article 29
    • Displayed as: "NC adopts {rule name} from {institution}"
  BLOCK: Excluded Governance Patterns
    • From Media Substrate Constitution v1.2, Article 30
    • Displayed as: "NC does not adopt {pattern name} from {institution}"
    • Intent: transparency for B2B and scholarly users

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZONE: LICENSING
  BLOCK: License from this Institution
    • "License assets from {Institution}"
    • License types available (based on rights_strategy)
    • "Inquire about institutional licensing" → B2B contact form
```

---

## Part IV — Cross-Cutting IA Rules

### Article 15 — Content State Rules

Phase 2–4 media types have a defined state on all pages during Phase 1 activation:

```
Active type   → full content zone with data
Pending type  → "Coming Soon" stub zone, no data exposed
               Stub shows: type name, brief description, "Notify me" CTA
               Stub does NOT show: asset counts, thumbnails, pricing
Retired type  → zone removed entirely
```

The homepage media type grid shows all 14 user-facing types. Phase 2–4 types show
"Coming Soon" state, not placeholder counts.

### Article 16 — Rights Visibility Rules

Rights information is visible on every page that displays a source_item. No asset appears
without its rights badge. The rights display hierarchy:

```
Rights Badge (always visible on all asset appearances)
├── "Public Domain"   (rights_status = 'verified_pd')
└── "CC0"             (rights_status = 'verified_cc0')

Rights detail (expanded on media page)
├── Plain-language statement
├── Rights statement URI (linked)
├── Evidence summary (abbreviated)
└── "Full provenance" expandable
```

### Article 17 — Quality Signal Rules

Quality tier is shown as a badge on every source_item appearance. The tier vocabulary
is displayed in plain language, not as a score:

```
MASTERWORK  → "Masterwork"  badge
FLAGSHIP    → "Flagship"    badge
STANDARD    → (no badge — default quality)
REFERENCE   → "Reference"   badge
BLOCKED     → not shown to users (not activated)
```

Raw numeric scores (csm_score, commerce_opportunity_score) are not shown to end users.
They are internal governance signals.

### Article 18 — Creator Page Stub

The Creator page (`/discover/creator/{slug}`) is architecturally defined here but not
listed in the primary page deliverables. It follows the Institution page structure with:
creator identity, all works, places covered, institutions holding works, era, prestige label,
and commerce rail. It must be implemented before the Golden Age era feature can link
creators as first-class entities.

### Article 19 — Story Page Stub

The Story page (`/stories/{slug}`) is NC-authored editorial content. It is not governed
by the Media Substrate Constitution. Its information architecture:

```
Story Page
├── ZONE: Story Identity
│   • Title, subtitle, author, date
│   • Hero media (linked source_item — IIIF)
│   • Estimated read time
├── ZONE: Story Body
│   • Narrative text (NC-authored)
│   • Inline media embeds (linked source_items — IIIF inline)
│   • Place references (linked to place pages)
├── ZONE: Related Assets
│   • Curated media grid (story-linked source_items, score-ranked)
├── ZONE: Related Collections
│   • Collections referenced in story
└── ZONE: Commerce Rail
    • Top products from story-linked assets
    • "Shop the Story" CTA
```

---

## Open Questions

| OQ | Question | Recommended resolution |
|---|---|---|
| OQ-1 | Should Creator pages be listed as a primary page deliverable in v1.1? | Yes — Creators are first-class entities per the Illustration Opportunity Doctrine. Creator pages should be added to the five-page canonical set in v1.1. |
| OQ-2 | Should the Discover entry mode include a map-based view (PostGIS)? | Yes — PostGIS is confirmed in the stack. An interactive map is the most natural entry mode for a place-centered platform. Requires front-end map rendering (Leaflet or equivalent). This is a UX implementation decision outside the IA scope but should be noted. |
| OQ-3 | How should the "Coming Soon" state for Phase 2–4 media handle notification capture? | An email capture CTA ("Notify me when Books are available") is appropriate. Requires a notification preference table not currently in the schema — minor future migration. |
| OQ-4 | The Governance Reference zone on the Institution page exposes constitutional doctrine (Article 29/30 rules). Is this appropriate for public display? | Yes — NC's PD verification process and governance transparency are a commercial differentiator, not a liability. Displaying governance rules adopted from LOC, Europeana, etc. builds institutional trust with B2B buyers. |
