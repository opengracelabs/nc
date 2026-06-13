# NC-GRAPH-IMPLEMENTATION-001: World-Class Discovery Architecture

| Field | Value |
|---|---|
| Document | NC-GRAPH-IMPLEMENTATION-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-13 |
| Authority | neo4j_pgvector_runtime_architecture_v1 · NC-AI-001 · Wireframe Constitution v1 · Strategic Direction v1 |
| **Decision** | **APPROVE WITH CONDITIONS** |

---

## Purpose

Determine, from first principles via reference model analysis, which user experiences Nature & Culture
must deliver and which technology each experience genuinely requires: PostgreSQL, PostGIS, or Neo4j.

This document does not supersede the NC-AI-001 frozen stack ruling. It provides the evidence base
that either confirms the PostgreSQL CTE path is sufficient for Phase 0–1 or establishes the specific
scale threshold at which Neo4j becomes required — the condition needed to justify SD-AMEND-1.

---

## Part I: User Journeys First

NC-GRAPH-IMPLEMENTATION-001 starts from five visitor journeys. Database responsibilities are derived only after the visible experience is defined.

| Journey surface | User job | Primary reference model | Required experience | Architecture implication |
|---|---|---|---|---|
| Discover page | Choose a place, story, or collection without knowing the collection model | Airbnb + Google Arts & Culture | Map-first browsing, editorial cards, visible entry points | PostGIS powers viewport/proximity; PostgreSQL joins return cards |
| Recommendation panel | Understand why a record is being recommended | Spotify + Rijksmuseum | Explainable recommendation with reasons, not opaque ranking | PostgreSQL stores reason codes and provenance; Neo4j deferred until behavior graph exists |
| Related journeys | Continue from one record into story, edition, place, or maker paths | Google Arts & Culture | Every object leads somewhere meaningful | PostgreSQL CTEs handle 2-3 hop paths in Phase 0-1 |
| Nearby places | Move spatially from one place to another | Airbnb | Distance, bioregion, and route-aware place discovery | PostGIS is authoritative for distance, containment, and route geometry |
| Collection graph | See collection, work, story, place, and edition as one connected system | Spotify playlist + museum object graph | Collection behaves as a hub rather than a dead-end index | PostgreSQL is source of truth; Neo4j projection activates only past graph thresholds |

### 1.1 Journey A: Discover Page

The visitor lands on Discover and sees a place-led map with editorial entry points. The page must answer: where can I begin, what is live now, and what kind of journey is this? It should feel closer to Airbnb browsing than a database catalog.

Operational responsibilities:

- PostgreSQL returns published cards, journey counts, collection status, and provenance-safe summaries.
- PostGIS returns viewport membership, centroids, nearest places, and future polygon containment.
- Neo4j is not required for the first screen because no variable-depth traversal or behavior graph is involved.

### 1.2 Journey B: Recommendation Panel

The recommendation panel explains why Earthrise is the right first journey: it is live, source-traceable, connected to story and editions, and acts as a bridge to future planetary places. The panel must expose reasons in plain language.

Operational responsibilities:

- PostgreSQL stores deterministic recommendation reasons and eligibility gates.
- PostGIS may add spatial reasons when a recommendation is place-nearby.
- Neo4j becomes useful only when recommendations depend on user behavior such as saved, viewed, purchased, or co-explored paths.

### 1.3 Journey C: Related Journeys

From a collection or work, the visitor can continue into a story path, a work/detail path, or an edition path. This is the Google Arts & Culture behavior: one object opens several legitimate next moves.

Operational responsibilities:

- PostgreSQL CTEs handle collection -> work -> story, work -> artist -> works, and collection -> product paths.
- PostGIS is only involved when a related journey is spatial.
- Neo4j is deferred until related paths regularly exceed four hops or p95 CTE latency exceeds the threshold.

### 1.4 Journey D: Nearby Places

Nearby places must support more than naive distance. For Yellowstone it can mean Grand Teton by distance; for Galapagos it can mean the HMS Beagle route; for Great Barrier Reef it can mean reef-to-rainforest adjacency.

Operational responsibilities:

- PostGIS owns ST_DWithin, ST_Distance, ST_Within, ST_Intersects, route geometry, and bioregion containment.
- PostgreSQL stores editorial relationship types and display copy.
- Neo4j may later cache derived proximity edges, but PostGIS remains authoritative.

### 1.5 Journey E: Collection Graph

The collection graph shows the collection as a hub connecting source record, story, place, and editions. This is a visitor-facing model first and a graph database concern second.

Operational responsibilities:

- PostgreSQL remains the canonical store for collection membership, product derivation, publication status, and source rights.
- PostGIS contributes place anchors and spatial edges.
- Neo4j is a projection layer when relationship traversal depth and scale justify it.

---

## Part II: Reference Model Analysis

### 1.1 Google Arts & Culture

**UX Delivered**

Cross-institution art discovery. Users explore by color palette, time period, geographic origin, artist,
and movement. "Art Selfie" matches face to portrait. "Stories" link objects thematically across
institutions. Virtual tours traverse museum rooms. The central gesture: *any object leads to an
infinite network of connected objects.*

**Data Model**

```
Artwork → Artist → Movement → Period → Institution → Place
Artwork → Subject (Iconclass) → OtherArtwork
Artwork → ColorPalette → SimilarArtwork
Artist → Nationality → CountryPlace
```

**Graph Relationships Required**

| Relationship | Type | Hops |
|---|---|---|
| Artwork created by artist | Direct FK | 1 |
| Artwork part of movement | FK through join table | 2 |
| Artist contemporary with artist | Derived (overlapping periods) | 2 |
| Artist influenced by artist | Explicit editorial link | 2–5 |
| Artwork housed at institution in country | Chain | 3 |
| "People who viewed X also viewed Y" | Collaborative filtering | Variable |
| Color-similar artworks | Feature vector similarity | 1 (similarity space) |

**Spatial Queries Required**

- `ST_Within(artwork_origin, country_polygon)` — filter by country of origin
- `ST_Distance(institution_point, user_location)` — "art near me"
- Map clustering: aggregate artworks by bounding box tile for map display
- Institution location markers (point geometry only)

**Recommendation Engine**

- Content-based: color palette distance, subject overlap, period proximity
- Collaborative: "viewers of X also viewed Y" (session behavior graph)
- Editorial: curated movement/story traversal (manual graph, small)
- None of the content-based signals require Neo4j — they are feature similarity

**Technology Assessment**

| Capability | PostgreSQL CTE | PostGIS | Neo4j |
|---|---|---|---|
| Artwork → artist → works | ✓ simple join | — | — |
| Artwork → movement → related | ✓ 2-hop CTE | — | — |
| Color similarity | ✓ array distance (pg_trgm + jsonb) | — | — |
| Artwork by geographic origin | — | ✓ ST_Within | — |
| Artist influence chains (5+ hops) | ✗ slow at scale | — | ✓ required |
| Collaborative filtering at GAC scale (>10M sessions) | ✗ impractical | — | ✓ required |

**NC Adoption:** Artwork→Artist→Works pattern (CTE). Geographic origin filter (PostGIS). Influence
chains deferred to Phase 2+.

---

### 1.2 Airbnb

**UX Delivered**

Place-first discovery with map as primary interface. Users browse listings by geography, zoom in on
a map to filter, apply attribute tags (amenity, price, type), and discover "Experiences" near a
destination. The central gesture: *where you are going determines what you see.*

**Data Model**

```
Listing → (lat/lng + polygon) → Neighborhood → City → Region
Listing → AmenityTag[]
Listing → AvailabilityCalendar
Experience → Host → Location → Listing proximity
```

**Graph Relationships Required**

| Relationship | Type | Hops |
|---|---|---|
| Listing contained in neighborhood | PostGIS point-in-polygon | 1 (spatial) |
| Neighborhood within city | Geographic hierarchy | 2 |
| Similar listings | Attribute overlap + collaborative | 1 |
| Experiences near a listing | ST_DWithin radius | 1 (spatial) |

**Spatial Queries Required**

- `ST_Within(listing_point, neighborhood_polygon)` — neighborhood containment
- `ST_DWithin(listing_point, search_point, radius)` — "within X km"
- `ST_MakeEnvelope(bbox)` — map pan/zoom viewport filter
- `ST_Distance(point_a, point_b)` — proximity ranking
- Point cluster aggregation by zoom level

**Recommendation Engine**

- Geographic proximity (pure PostGIS, no graph)
- "Guests who booked X also saved Y" (session-level collaborative filtering)
- Price/amenity clustering (simple attribute similarity)

**Technology Assessment**

| Capability | PostgreSQL CTE | PostGIS | Neo4j |
|---|---|---|---|
| Map viewport filter | — | ✓ ST_MakeEnvelope | — |
| Radius / proximity search | — | ✓ ST_DWithin | — |
| Geographic hierarchy traversal | ✓ simple FK chain | ✓ for polygon containment | — |
| "Guests also saved" at Airbnb scale | ✗ impractical | — | ✓ required |

**NC Adoption:** Map-first place browsing (PostGIS). Geographic containment (PostGIS). Proximity
ranking (PostGIS). No collaborative filtering needed at Phase 0 scale.

---

### 1.3 Spotify

**UX Delivered**

Taste-graph music discovery. Discover Weekly, artist radio, mood playlists. The central gesture:
*your listening history generates a personalized taste graph that surfaces new music.*

**Data Model**

```
Track → Artist → Genre → SubGenre
Artist → Collaborator[]
User → ListenEvent[] → Track
User → PlaylistMembership → Track
Artist → Influence → Artist (editorial)
```

**Graph Relationships Required**

| Relationship | Type | Hops |
|---|---|---|
| Artist→Genre→SubGenre | Taxonomy FK | 2 |
| Artist→Collaborators | Explicit link | 1 |
| "Fans also like" artist | Collaborative filter on user→listen→artist | 2 variable |
| Playlist co-occurrence | Derived: tracks in same playlists | 2 derived |
| User taste cluster | Matrix factorization on listen graph | n-hop |

**Spatial Queries Required**

- Minimal: "concerts near you" (ST_DWithin on venue points)

**Recommendation Engine**

- Collaborative filtering: the core Spotify recommendation is a user-item matrix factorization
  over a graph of billions of User→Track edges. This is the canonical use case for Neo4j or a
  dedicated ML graph system.
- Audio features: content-based similarity over acoustic feature vectors
- Graph traversal: "artists connected to artists you like through collaboration or influence chains"

**Technology Assessment**

| Capability | PostgreSQL CTE | PostGIS | Neo4j |
|---|---|---|---|
| Track→Artist→Genre | ✓ FK join | — | — |
| Artist radio (2-hop genre traversal) | ✓ CTE | — | — |
| "Fans also like" (collaborative filtering) | ✗ impractical | — | ✓ required |
| Discover Weekly (personalized, billions of edges) | ✗ impossible | — | ✓ required |

**NC Adoption at Phase 0:** No user listen history exists. "Related illustrations" via shared
subject/artist/period attributes (CTE). Full Spotify-style personalization requires user behavioral
data that NC will not have until significant scale.

**NC Adoption at Phase 2+:** If NC captures session behavior (viewed, saved, purchased), a
lightweight collaborative signal can be derived. This is the primary justification for Neo4j at scale.

---

### 1.4 Rijksmuseum

**UX Delivered**

Object-centered discovery organized around the maker. Users explore by color (visual palette picker),
material (bronze, oil, watercolor), period (1600s, 1700s), maker (Rembrandt, Vermeer), and
iconographic subject (Iconclass taxonomy). The central gesture: *every object connects to every other
object through the maker's hand, period, and iconographic vocabulary.*

**Data Model**

```
Object → Maker → Period → Technique → Material
Object → Iconclass subject → Subject hierarchy
Object → Provenance chain → Prior owner
Maker → Active period → City → Country
Collection → Object[]
```

**Graph Relationships Required**

| Relationship | Type | Hops |
|---|---|---|
| Object made by maker | Direct FK | 1 |
| Maker active in period | FK | 2 |
| Object uses technique | Join table | 1 |
| Object depicts subject (Iconclass) | Join table + taxonomy | 1–4 (taxonomy) |
| "By the same hand" (other works) | FK through maker | 2 |
| "From the same period" | FK through period | 2 |
| Maker contemporary with maker | Derived overlap | 2 |
| Provenance chain traversal | Recursive ownership | Variable |

**Spatial Queries Required**

- Geographic origin of objects and makers (point geometry, simple)
- Dutch East India trade routes (linestring, expedition pattern)
- Colonial provenance geography (point origin)

**Recommendation Engine**

- Maker-centric: "by the same hand" — simple 2-hop CTE
- Iconographic: shared Iconclass subject codes — 2-hop CTE through subject table
- Period + technique clustering — simple attribute filter
- No collaborative filtering documented

**Technology Assessment**

| Capability | PostgreSQL CTE | PostGIS | Neo4j |
|---|---|---|---|
| Object→Maker→Works | ✓ 2-hop CTE | — | — |
| Object→Subject→Related objects | ✓ 2-hop CTE | — | — |
| Iconclass taxonomy traversal | ✓ recursive CTE | — | — |
| Maker geographic origin | — | ✓ point | — |
| Trade route visualization | — | ✓ LineString | — |
| Provenance chain (variable depth) | ✓ at museum scale | — | ✓ at archive scale |

**NC Adoption:** This is NC's closest reference model. The 2-hop patterns (Illustration→Artist→Works,
Illustration→Subject→Related) are directly implementable in PostgreSQL CTEs. Period traversal: CTE.
Expedition routes: PostGIS LineString. No Neo4j required to match Rijksmuseum's actual recommendation
behavior.

---

### 1.5 Smithsonian

**UX Delivered**

Cross-disciplinary discovery across 19 museums. Objects from natural history, American history,
art, air and space, and archives surface together around a theme, person, or place. The central
gesture: *every object in the collection connects to every other through the fabric of human and
natural history.*

**Data Model**

```
Object → Collection → Unit → Topic/Theme
Object → Taxon (natural history)
Object → Person (historical figures)
Object → Event → Date → Period
Object → Expedition → Place → Specimen
Object → [cross-unit related objects]
```

**Graph Relationships Required**

| Relationship | Type | Hops |
|---|---|---|
| Object→Collection→Unit | FK chain | 2 |
| Object→Topic→Related objects (cross-unit) | Join table traversal | 2–4 |
| Specimen→Taxon→Taxon hierarchy | Recursive taxonomy | Variable |
| Expedition→Place→Objects collected there | Chain through expedition | 3 |
| Illustration→depicted taxon→specimens of taxon | Cross-discipline link | 3 |

**Spatial Queries Required**

- Specimen collection locations (point geometry)
- Expedition routes (LineString)
- `ST_Within(collection_point, park_polygon)` — "objects collected in this park"
- Geographic origin of objects and makers

**Recommendation Engine**

- Topic + theme traversal (2-3 hop CTE)
- Cross-discipline links ("this fossil relates to this illustration") — 3-hop CTE
- "Often viewed together" collaborative filtering at Smithsonian scale (millions of sessions)

**Technology Assessment**

| Capability | PostgreSQL CTE | PostGIS | Neo4j |
|---|---|---|---|
| Object→Topic→Related | ✓ 2-3 hop CTE | — | — |
| Expedition→Place→Objects | ✓ 3-hop CTE | ✓ route LineString | — |
| Taxon hierarchy traversal | ✓ recursive CTE | — | — |
| Specimen origin within park | — | ✓ ST_Within | — |
| Cross-discipline discovery at Smithsonian scale (millions of objects) | ✗ slow | — | ✓ beneficial |

**NC Adoption:** NC is operating at a fraction of Smithsonian's object count. Cross-discipline
discovery (Illustration→Taxon→Place) is a 3-hop CTE today. At 10,000+ illustrations, the
relationship traversal becomes slow enough to justify Neo4j projection.

---

## Part III: Technology Responsibilities Matrix

### 2.1 Capability → Required Technology

| Capability | PostgreSQL | PostGIS | Neo4j | Phase |
|---|---|---|---|---|
| Illustration → artist → other works | ✓ required | — | — | Phase 0 |
| Illustration → subjects → related illustrations | ✓ required | — | — | Phase 0 |
| Place → subjects → illustrations | ✓ required (3-hop CTE) | — | — | Phase 0 |
| Collection → members | ✓ required | — | — | Phase 0 |
| Period → illustrations in period | ✓ required | — | — | Phase 0 |
| Full-text search (title, tags) | ✓ pg_trgm | — | — | Phase 0 |
| Map-first place browsing | — | ✓ required | — | Phase 0 |
| Place viewport filter (pan/zoom) | — | ✓ ST_MakeEnvelope | — | Phase 0 |
| Places within X km | — | ✓ ST_DWithin | — | Phase 0 |
| Species occurring within place polygon | — | ✓ ST_Within | — | Phase 0 |
| Expedition routes intersecting place | — | ✓ ST_Intersects | — | Phase 1 |
| Bioregion containment | — | ✓ ST_Within | — | Phase 1 |
| Artist visited place (geographic) | ✓ + PostGIS | ✓ point query | — | Phase 1 |
| Subject taxonomy traversal | ✓ recursive CTE | — | — | Phase 0 |
| Artist influence chains (2-3 hops) | ✓ CTE | — | — | Phase 1 |
| Artist influence chains (5+ hops, deep) | ✗ slow | — | ✓ required | Phase 2 |
| "Related to" at 1K+ illustration scale | ✓ CTE viable | — | — | Phase 1 |
| "Related to" at 10K+ illustration scale | ✗ slow | — | ✓ beneficial | Phase 2 |
| Personalized recommendations (session behavior) | ✗ impractical | — | ✓ required | Phase 3 |
| "Collectors also explored" (collaborative filtering) | ✗ impractical | — | ✓ required | Phase 3 |
| Variable-depth pattern matching | ✗ expensive | — | ✓ required | Phase 2 |
| Tourism path (place → nearby places → illustrations) | ✓ CTE + PostGIS | ✓ proximity | — | Phase 1 |
| Conservation path (taxon → status → places) | ✓ CTE | — | — | Phase 1 |

### 2.2 The Neo4j Threshold

Neo4j is not required until one of these conditions is met:

| Condition | Threshold | Current NC State |
|---|---|---|
| Total illustrations in graph | > 5,000 | 16 product-safe |
| Total places in graph | > 100 | 7 |
| Relationship traversal depth required | > 4 hops consistently | 3 hops max today |
| User session behavior records | > 10,000 sessions | 0 (pre-launch) |
| "Similar to" query latency via CTE | > 200ms at p95 | Not measurable yet |

**Verdict:** PostgreSQL CTE is the correct implementation for Phase 0 and Phase 1. Neo4j should be
fully designed now (schema, projection pipeline, rebuild protocol) and implemented when threshold is
crossed. The `neo4j_pgvector_runtime_architecture_v1.md` document defines that implementation path.

---

## Part IV: Wireframes

### 3.1 Map-First Place Discovery (Airbnb model)

```
┌─────────────────────────────────────────────────────────────────────┐
│  NATURE & CULTURE                                    [Search]  [☰]  │
├────────────────────────────────┬────────────────────────────────────┤
│                                │                                    │
│  Explore by place              │  ┌──────────────────────────────┐  │
│                                │  │                              │  │
│  ● National Parks              │  │                              │  │
│  ● Marine Ecosystems           │  │         [WORLD MAP]          │  │
│  ● Mountain Systems            │  │                              │  │
│  ● Island Ecosystems           │  │   ●Yellowstone  ●GrandCanyon │  │
│  ● River Systems               │  │                              │  │
│                                │  │  ●GreatBarrierReef           │  │
│  Sort by:                      │  │                              │  │
│  ● Most illustrations          │  └──────────────────────────────┘  │
│  ○ Alphabetical                │  PostGIS: ST_Within + centroid     │
│  ○ Recently added              │                                    │
├────────────────────────────────┴────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │              │  │              │  │              │             │
│  │ [Place img]  │  │ [Place img]  │  │ [Place img]  │             │
│  │              │  │              │  │              │             │
│  │ Yellowstone  │  │ Grand Canyon │  │ Great Barrier│             │
│  │ Wyoming · US │  │ Arizona · US │  │ Queensland AU│             │
│  │              │  │              │  │              │             │
│  │ 4 artists    │  │ 3 artists    │  │ 2 artists    │             │
│  │ 8 works      │  │ 5 works      │  │ 4 works      │             │
│  │ [Explore →]  │  │ [Explore →]  │  │ [Explore →]  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

PostGIS query: SELECT p.*, COUNT(DISTINCT a.artist_id), COUNT(DISTINCT i.illustration_id)
               FROM nc_places p LEFT JOIN nc_taxon_place tp ON ...
               WHERE ST_Within(p.centroid, $viewport_polygon)
               GROUP BY p.place_id ORDER BY illustration_count DESC
```

---

### 3.2 Place Detail Page (Rijksmuseum + Smithsonian model)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Nature & Culture  /  Places  /  Yellowstone         [♡] [Share]   │
├──────────────────────────────────────┬──────────────────────────────┤
│                                      │                              │
│  ┌──────────────────────────────────┐│  Illustrations               │
│  │                                  ││  ────────────────────────    │
│  │                                  ││                              │
│  │       [PLACE HERO IMAGE]         ││  [img] [img] [img] [img]    │
│  │                                  ││  [img] [img] [img] [img]    │
│  │                                  ││                              │
│  └──────────────────────────────────┘│  [See all 8 illustrations →] │
│                                      │                              │
│  Yellowstone National Park           │  Artists                     │
│  ──────────────────────────          │  ────────────────────────    │
│  Wyoming, United States              │  Thomas Moran (1837–1926)    │
│  Established 1872 · 2.2M acres       │  William Henry Jackson       │
│  UNESCO World Heritage Site          │  Frederic Church             │
│  GeoNames 5843591 · Wikidata Q82070  │                              │
│                                      │  Related Places              │
│  Natural Subjects                    │  ────────────────────────    │
│  ────────────────────────            │  Grand Teton NP (85 km)      │
│  American Bison · Grizzly Bear       │  Glacier NP (428 km)         │
│  Trumpeter Swan · Gray Wolf          │  Yosemite NP (1,142 km)     │
│  Greater Yellowstone Ecosystem       │  [PostGIS: ST_Distance]      │
│  [GBIF: evidence layer only]         │                              │
├──────────────────────────────────────┴──────────────────────────────┤
│                                                                     │
│  The Expedition Record                                              │
│  ─────────────────────────────────────────────────────────────────  │
│  Hayden Geological Survey (1871) · Moran joined as expedition artist│
│  [Expedition route: PostGIS LineString]                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

Graph path: Place → [CTE] → Taxon → [CTE] → Illustration
            Place → [PostGIS ST_Distance] → Adjacent Places
            Place → [CTE] → Expedition → Artist
```

---

### 3.3 Illustration Detail (Google Arts & Culture model)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Nature & Culture  /  Yellowstone  /  Grand Prismatic Spring        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │                                                             │   │
│  │                 [FULL ILLUSTRATION]                         │   │
│  │                                                             │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                [Zoom] [Download] [Add to Cart →]   │
│                                                                     │
├──────────────────────────────┬──────────────────────────────────────┤
│                              │                                      │
│  Thomas Moran                │  Provenance                         │
│  Grand Prismatic Spring      │  ─────────────────────────────────  │
│  1872 · Oil on canvas        │  Source: Smithsonian American Art   │
│  Yellowstone, Wyoming        │  Rights: CC0 (Public Domain)        │
│                              │  Institution: Smithsonian           │
│  Subjects depicted           │  Asset ID: NC-ASSET-003             │
│  ─────────────────────────   │                                      │
│  Yellowstone Nat. Park       │  [Add to Cart — Giclée Print $299]  │
│  Geothermal landscape        │  [Add to Cart — Digital $29]        │
│  Hot spring ecosystem        │                                      │
│                              │                                      │
├──────────────────────────────┴──────────────────────────────────────┤
│                                                                     │
│  By Thomas Moran                                                    │
│  ─────────────────────────────────────────────────────────────────  │
│  [Chasm of Colorado]  [Mountain of the Holy Cross]  [Cliffs of the │
│  Upper Colorado]                                                    │
│  [CTE: illustration_id → artist_id → other illustrations]          │
│                                                                     │
│  More from Yellowstone                                              │
│  ─────────────────────────────────────────────────────────────────  │
│  [Jackson photo]  [Church landscape]  [Hayden survey illustration] │
│  [CTE: place_id → other illustrations, excluding current]          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 3.4 Artist Profile (Rijksmuseum model)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Nature & Culture  /  Artists  /  Thomas Moran                     │
├──────────────────────────────────┬──────────────────────────────────┤
│                                  │                                  │
│  ┌─────────────────────────────┐ │  Works in the Collection         │
│  │                             │ │  ────────────────────────────    │
│  │    [ARTIST PORTRAIT]        │ │                                  │
│  │                             │ │  [img] [img] [img] [img]        │
│  └─────────────────────────────┘ │  [img] [img]                    │
│                                  │                                  │
│  Thomas Moran                    │  [See all 6 works →]            │
│  ───────────────────────────     │                                  │
│  American · 1837–1926            │                                  │
│  Hudson River School             │  Places Visited                  │
│  Wikidata Q712574                │  ────────────────────────────    │
│                                  │  Yellowstone · Wyoming (1871)    │
│  Expeditions                     │  Grand Canyon · Arizona (1873)   │
│  ───────────────────────────     │  Yosemite · California (1872)    │
│  Hayden Survey (1871)            │  [PostGIS: artist points]        │
│  Wheeler Survey (1873)           │                                  │
│  [route LineString]              │  Contemporary Artists            │
│                                  │  ────────────────────────────    │
│                                  │  Albert Bierstadt (1830–1902)    │
│                                  │  Frederic Church (1826–1900)     │
│                                  │  [CTE: overlapping active years] │
│                                  │                                  │
└──────────────────────────────────┴──────────────────────────────────┘
```

---

### 3.5 Collection Page (Spotify playlist model)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Nature & Culture  /  Collections                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  EARTHRISE                                   [1 collection] │   │
│  │  The most reproduced photograph in history.                 │   │
│  │  NASA · 1968 · AS08-14-2383                                 │   │
│  │                                                             │   │
│  │  [img] [img] [img]     [Explore Collection →]              │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  DARWIN'S FINCHES                        [coming soon]      │   │
│  │  The illustrations that changed biology.                    │   │
│  │  John Gould · 1841 · HMS Beagle Voyage                      │   │
│  │                                                             │   │
│  │  [img] [img] [img] [img]   [Notify Me]                     │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  HAECKEL'S OCEAN                         [coming soon]      │   │
│  │  Victorian natural history as visual art.                   │   │
│  │  Ernst Haeckel · 1904 · Kunstformen der Natur               │   │
│  │                                                             │   │
│  │  [img] [img] [img] [img] [img]   [Notify Me]               │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part V: Expanded User Journey Logic

### 4.1 The Place Explorer (Airbnb entry)

```
User opens NC on mobile
        │
        ▼
[Homepage: map view]
PostGIS: featured places by centroid
        │
        ▼ taps "Yellowstone"
[Place Detail page]
CTE: place_id → taxa → illustrations (12 results)
PostGIS: ST_Distance → 3 adjacent places
        │
        ▼ taps illustration
[Illustration Detail]
CTE: artist_id → 3 other works
CTE: place_id → 3 more from same place
        │
        ▼ taps "Add to Cart"
[Product page: NC-PROD-001 Earthrise / NC-PROD-003 Moran]
Rights check: PostgreSQL canonical gate
        │
        ▼
[Checkout via Shopify]
```

Graph hops: 3 (Place → Taxon → Illustration). PostGIS: 1 spatial query. Neo4j: not required.

---

### 4.2 The Artist Devotee (Rijksmuseum entry)

```
User searches "Audubon"
        │
        ▼
[Search results]
pg_trgm: ILIKE '%audubon%' on artist names + illustration titles
        │
        ▼ selects John James Audubon
[Artist Profile]
CTE: artist_id → all illustrations (12 works)
CTE: artist.active_years → contemporary_artists (overlapping periods)
PostGIS: artist expedition points on map
        │
        ▼ taps "Birds of America — Great Blue Heron"
[Illustration Detail]
CTE: illustration → depicted_taxa → place occurrences
CTE: same artist → 3 related works
        │
        ▼ sees "Places where Great Blue Heron appears"
[Place Discovery: filtered by taxon]
CTE: taxon_id → taxon_place → place records
PostGIS: place centroids for map display
        │
        ▼ selects "Everglades National Park"
[Place Detail: Everglades]
```

Graph hops: 4 (Artist → Illustration → Taxon → Place). All CTE. No PostGIS required until map display.

---

### 4.3 The Collection Navigator (Spotify entry)

```
User arrives via editorial link "The NASA Photography That Changed History"
        │
        ▼
[Earthrise Collection page]
CTE: collection_id → illustration_members → product_records
        │
        ▼ sees "Earthrise — Giclée Print"
[Product detail: NC-PROD-001]
PostgreSQL: rights check, availability
        │
        ▼ purchases
[Post-purchase: "You might also explore"]
CTE: collection.anchor_place_id → adjacent_places → collections anchored there
PostGIS: ST_Distance — nearest place with a collection
        │
        ▼ "Darwin's Finches — coming soon"
[Collection preview + notify me]
```

Graph hops: 3 (Collection → Place → Adjacent Place → Collection). CTE + PostGIS proximity.

---

## Part VI: Graph Schema

### 5.1 Node Types

All nodes carry `pg_id`, `pg_table`, `schema_version`, `projection_run_id`, `projected_at` per the
`neo4j_pgvector_runtime_architecture_v1.md` contract.

```cypher
-- Place node
(:Place {
  place_id:         UUID,          -- PostgreSQL pk
  geonames_id:      INTEGER,       -- canonical spatial authority
  wikidata_qid:     TEXT,          -- identity authority
  name:             TEXT,
  canonical_name:   TEXT,
  fcode:            TEXT,          -- GeoNames feature code: PRKA, RF, MT, ISL
  country_code:     TEXT,
  admin1_code:      TEXT,
  centroid_lat:     FLOAT,         -- derived from PostGIS, stored for graph display
  centroid_lng:     FLOAT,
  area_km2:         FLOAT,
  established_year: INTEGER,
  place_type:       TEXT           -- 'national_park', 'reef', 'mountain', 'island'
})

-- Illustration node (maps to SourceItem in v1 ontology)
(:Illustration {
  illustration_id:  UUID,
  nc_asset_id:      TEXT,          -- NC-ASSET-001 etc.
  title:            TEXT,
  year:             INTEGER,
  year_circa:       BOOLEAN,
  rights:           TEXT,          -- CC0, PDM, NoC-US
  institution_slug: TEXT,
  product_safe:     BOOLEAN,
  resolution_mp:    FLOAT,         -- megapixels
  color_primary:    TEXT,          -- dominant hex
  color_palette:    TEXT[]         -- top 5 hex colors
})

-- Artist (maps to Creator in v1 ontology)
(:Artist {
  artist_id:        UUID,
  wikidata_qid:     TEXT,
  name:             TEXT,
  birth_year:       INTEGER,
  death_year:       INTEGER,
  nationality:      TEXT,
  active_start:     INTEGER,
  active_end:       INTEGER,
  nc_priority:      BOOLEAN,       -- Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel, Wolf
  priority_rank:    INTEGER        -- 1–8
})

-- Taxon (maps to Concept in v1 ontology)
(:Taxon {
  taxon_id:         UUID,
  gbif_taxon_key:   INTEGER,       -- GBIF biological anchor (evidence only)
  wikidata_qid:     TEXT,
  scientific_name:  TEXT,
  common_name:      TEXT,
  rank:             TEXT,          -- species, genus, family, order
  kingdom:          TEXT,
  phylum:           TEXT,
  class:            TEXT,
  order:            TEXT,
  family:           TEXT,
  iucn_status:      TEXT           -- evidence layer, not commerce gate
})

-- Institution (maps to Institution in v1 ontology)
(:Institution {
  institution_id:   UUID,
  slug:             TEXT,          -- 'nasa', 'smithsonian', 'met', 'nhm'
  name:             TEXT,
  wikidata_qid:     TEXT,
  country_code:     TEXT,
  adapter_class:    TEXT,          -- boolean, csv, linked_art, ckan, etc.
  source_role:      TEXT           -- 'content', 'identity', 'evidence', 'validation_only'
})

-- Collection
(:Collection {
  collection_id:    UUID,
  slug:             TEXT,          -- 'earthrise', 'darwin-finches'
  name:             TEXT,
  anchor_place_id:  UUID,
  launch_phase:     INTEGER,
  status:           TEXT           -- 'live', 'coming_soon', 'reserved'
})

-- Expedition (maps to Event in v1 ontology)
(:Expedition {
  expedition_id:    UUID,
  name:             TEXT,          -- 'Hayden Survey', 'HMS Beagle', 'Cook Voyage I'
  start_year:       INTEGER,
  end_year:         INTEGER,
  lead_naturalist:  TEXT,
  vessel_name:      TEXT
})

-- Period
(:Period {
  period_id:        UUID,
  name:             TEXT,          -- 'Golden Age Natural History 1750-1900'
  start_year:       INTEGER,
  end_year:         INTEGER
})

-- Product
(:Product {
  product_id:       UUID,
  nc_product_id:    TEXT,          -- NC-PROD-001
  name:             TEXT,
  product_line:     INTEGER,       -- 1–20 per NC-PRODUCT-001
  status:           TEXT           -- 'active', 'deferred', 'reserved'
})

-- Bioregion (spatial grouping for Neo4j proximity edges)
(:Bioregion {
  bioregion_id:     UUID,
  name:             TEXT,          -- 'Indo-Pacific', 'Rocky Mountain West'
  region_type:      TEXT           -- 'marine', 'terrestrial', 'freshwater'
})
```

---

### 5.2 Relationship Types

All relationships carry `derivation`, `pg_source`, `pg_source_id`, `schema_version`,
`projection_run_id`, `projected_at` per the v1 ontology contract.

```cypher
-- Illustration authorship
(i:Illustration)-[:CREATED_BY {year: INT, confirmed: BOOL}]->(a:Artist)

-- Illustration subject
(i:Illustration)-[:DEPICTS {primary: BOOL, confidence: FLOAT}]->(t:Taxon)

-- Illustration geography (editorial link, not PostGIS authority)
(i:Illustration)-[:ASSOCIATED_WITH {evidence_type: TEXT}]->(p:Place)

-- Illustration provenance
(i:Illustration)-[:SOURCED_FROM {asset_id: TEXT, rights: TEXT}]->(inst:Institution)

-- Illustration collection membership
(i:Illustration)-[:PART_OF {display_order: INT}]->(c:Collection)

-- Illustration temporal period
(i:Illustration)-[:CREATED_IN]->(per:Period)

-- Artist place visits (editorial + expedition-derived)
(a:Artist)-[:VISITED {year: INT}]->(p:Place)

-- Artist expedition participation
(a:Artist)-[:PART_OF_EXPEDITION]->(e:Expedition)

-- Artist active period
(a:Artist)-[:ACTIVE_IN]->(per:Period)

-- Artist contemporaries (derived: overlapping active years, ≤20 year gap)
(a:Artist)-[:CONTEMPORARY_WITH {overlap_years: INT}]->(a2:Artist)

-- Taxon place occurrence (GBIF evidence layer)
(t:Taxon)-[:OCCURS_AT {occurrence_count: INT, gbif_confirmed: BOOL}]->(p:Place)

-- Taxon hierarchy
(t:Taxon)-[:CHILD_OF]->(t2:Taxon)

-- Place geographic hierarchy
(p:Place)-[:LOCATED_IN {hierarchy_type: TEXT}]->(p2:Place)

-- Place bioregion containment (PostGIS-derived, stored as graph edge)
(p:Place)-[:WITHIN_BIOREGION]->(b:Bioregion)

-- Place proximity (PostGIS-derived: ≤500km, stored as traversal aid)
(p:Place)-[:PROXIMATE_TO {distance_km: FLOAT}]->(p2:Place)

-- Expedition place passage
(e:Expedition)-[:PASSED_THROUGH {year: INT}]->(p:Place)

-- Collection anchor place
(c:Collection)-[:ANCHORED_AT]->(p:Place)

-- Product provenance
(prod:Product)-[:DERIVED_FROM]->(i:Illustration)

-- External identity
(p:Place)-[:SAME_AS {authority: TEXT}]->(external_id)
(a:Artist)-[:SAME_AS {authority: TEXT}]->(external_id)
(t:Taxon)-[:SAME_AS {authority: TEXT}]->(external_id)
```

---

### 5.3 Discovery Path Queries

**Path 1: Place → Subjects → Illustrations (primary discovery)**

```cypher
-- Neo4j
MATCH (p:Place {place_id: $place_id})
      -[:OCCURS_AT|ASSOCIATED_WITH*1..2]-(t:Taxon)
      -[:DEPICTS*1]-(i:Illustration)
WHERE i.product_safe = true
  AND i.rights IN ['CC0', 'PDM', 'NoC-US']
RETURN i ORDER BY i.year DESC LIMIT 12

-- PostgreSQL CTE equivalent (operative for Phase 0-1)
WITH place_taxa AS (
  SELECT tp.taxon_id, tp.occurrence_count
  FROM nc_taxon_place tp
  WHERE tp.place_id = $place_id
    AND tp.gbif_confirmed = true
),
place_illustrations AS (
  SELECT i.*, pt.occurrence_count,
         ROW_NUMBER() OVER (ORDER BY pt.occurrence_count DESC, i.year DESC) AS rank
  FROM nc_illustrations i
  JOIN nc_illustration_taxon it ON i.illustration_id = it.illustration_id
  JOIN place_taxa pt ON it.taxon_id = pt.taxon_id
  WHERE i.product_safe = true
    AND i.rights IN ('CC0', 'PDM', 'NoC-US')
)
SELECT * FROM place_illustrations ORDER BY rank LIMIT 12;
```

**Path 2: Illustration → Artist → Related Works (maker path)**

```cypher
-- Neo4j
MATCH (i:Illustration {illustration_id: $illus_id})
      -[:CREATED_BY]->(a:Artist)
      <-[:CREATED_BY]-(i2:Illustration)
WHERE i2.illustration_id <> $illus_id
  AND i2.product_safe = true
RETURN i2, a LIMIT 8

-- PostgreSQL CTE equivalent
SELECT i2.*, a.name AS artist_name
FROM nc_illustrations i1
JOIN nc_illustration_artist ia1 ON i1.illustration_id = ia1.illustration_id
JOIN nc_artists a ON ia1.artist_id = a.artist_id
JOIN nc_illustration_artist ia2 ON a.artist_id = ia2.artist_id
JOIN nc_illustrations i2 ON ia2.illustration_id = i2.illustration_id
WHERE i1.illustration_id = $illus_id
  AND i2.illustration_id <> $illus_id
  AND i2.product_safe = true
LIMIT 8;
```

**Path 3: Place → Adjacent Places (tourism path)**

```cypher
-- Neo4j (uses stored PROXIMATE_TO edges derived from PostGIS)
MATCH (p:Place {place_id: $place_id})-[r:PROXIMATE_TO]->(p2:Place)
RETURN p2, r.distance_km ORDER BY r.distance_km LIMIT 5

-- PostGIS (authoritative — Neo4j edge is a derived copy)
SELECT p2.place_id, p2.name,
       ST_Distance(p1.centroid::geography, p2.centroid::geography) / 1000 AS dist_km
FROM nc_places p1, nc_places p2
WHERE p1.place_id = $place_id
  AND p2.place_id <> $place_id
  AND ST_DWithin(p1.centroid::geography, p2.centroid::geography, 600000)
ORDER BY dist_km LIMIT 5;
```

**Path 4: Artist → Contemporary Artists (provenance path)**

```cypher
-- Neo4j
MATCH (a:Artist {artist_id: $artist_id})
      -[:CONTEMPORARY_WITH]->(a2:Artist)
RETURN a2 ORDER BY a2.nc_priority DESC, a.birth_year

-- PostgreSQL CTE equivalent
SELECT a2.*, ABS(a2.active_start - a1.active_start) AS year_overlap
FROM nc_artists a1
JOIN nc_artists a2 ON a2.artist_id <> a1.artist_id
WHERE a1.artist_id = $artist_id
  AND a2.active_start <= a1.active_end
  AND a2.active_end >= a1.active_start
  AND ABS(a2.active_start - a1.active_start) <= 30
ORDER BY a2.nc_priority DESC, year_overlap ASC
LIMIT 6;
```

**Path 5: Collection → Place → Nearby Collections (commerce path)**

```cypher
-- Neo4j
MATCH (c:Collection {collection_id: $coll_id})
      -[:ANCHORED_AT]->(p:Place)
      -[:PROXIMATE_TO]->(p2:Place)
      <-[:ANCHORED_AT]-(c2:Collection)
WHERE c2.collection_id <> $coll_id
  AND c2.status IN ['live', 'coming_soon']
RETURN c2, p2 LIMIT 4

-- PostgreSQL CTE + PostGIS equivalent
WITH anchor AS (
  SELECT c.anchor_place_id
  FROM nc_collections c WHERE c.collection_id = $coll_id
),
nearby_places AS (
  SELECT p2.place_id,
         ST_Distance(p1.centroid::geography, p2.centroid::geography)/1000 AS dist_km
  FROM nc_places p1, nc_places p2, anchor a
  WHERE p1.place_id = a.anchor_place_id
    AND p2.place_id <> p1.place_id
    AND ST_DWithin(p1.centroid::geography, p2.centroid::geography, 2000000)
)
SELECT c2.*, np.dist_km
FROM nc_collections c2
JOIN nearby_places np ON c2.anchor_place_id = np.place_id
WHERE c2.collection_id <> $coll_id
  AND c2.status IN ('live', 'coming_soon')
ORDER BY np.dist_km LIMIT 4;
```

---

## Part VII: Spatial Schema (PostGIS)

### 6.1 Core Spatial Tables

```sql
-- Canonical place geometry
CREATE TABLE nc_places (
  place_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  geonames_id      INTEGER UNIQUE NOT NULL,
  wikidata_qid     TEXT,
  name             TEXT NOT NULL,
  canonical_name   TEXT NOT NULL,
  fcode            TEXT NOT NULL,         -- PRKA, RF, MT, ISL, LK, OCN
  country_code     CHAR(2),
  admin1_code      TEXT,
  geom             GEOMETRY(GEOMETRY, 4326) NOT NULL,  -- polygon preferred, point fallback
  centroid         GEOMETRY(POINT, 4326) GENERATED ALWAYS AS (ST_Centroid(geom)) STORED,
  area_km2         FLOAT,
  established_year INTEGER,
  place_type       TEXT                  -- 'national_park', 'reef', 'mountain', 'island'
);

CREATE INDEX nc_places_geom_idx     ON nc_places USING GIST (geom);
CREATE INDEX nc_places_centroid_idx ON nc_places USING GIST (centroid);
CREATE INDEX nc_places_fcode_idx    ON nc_places (fcode);
CREATE INDEX nc_places_country_idx  ON nc_places (country_code);

-- Taxon occurrences within place (PostGIS-confirmed)
CREATE TABLE nc_taxon_place (
  taxon_id         UUID NOT NULL REFERENCES nc_taxa (taxon_id),
  place_id         UUID NOT NULL REFERENCES nc_places (place_id),
  occurrence_count INTEGER DEFAULT 0,
  gbif_confirmed   BOOLEAN DEFAULT false,
  occurrence_geom  GEOMETRY(MULTIPOINT, 4326),  -- GBIF occurrence point cloud
  last_synced_at   TIMESTAMPTZ,
  PRIMARY KEY (taxon_id, place_id)
);

CREATE INDEX nc_taxon_place_geom_idx ON nc_taxon_place USING GIST (occurrence_geom);
CREATE INDEX nc_taxon_place_place_idx ON nc_taxon_place (place_id);

-- Expedition routes
CREATE TABLE nc_expeditions (
  expedition_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name             TEXT NOT NULL,
  slug             TEXT UNIQUE NOT NULL,
  start_year       INTEGER,
  end_year         INTEGER,
  lead_naturalist  TEXT,
  vessel_name      TEXT,
  route            GEOMETRY(LINESTRING, 4326)
);

CREATE INDEX nc_expeditions_route_idx ON nc_expeditions USING GIST (route);

-- Bioregions for place grouping
CREATE TABLE nc_bioregions (
  bioregion_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name             TEXT NOT NULL,
  region_type      TEXT NOT NULL,   -- 'marine', 'terrestrial', 'freshwater'
  geom             GEOMETRY(MULTIPOLYGON, 4326) NOT NULL
);

CREATE INDEX nc_bioregions_geom_idx ON nc_bioregions USING GIST (geom);

-- Artist location history (expedition waypoints)
CREATE TABLE nc_artist_places (
  artist_id        UUID NOT NULL REFERENCES nc_artists (artist_id),
  place_id         UUID NOT NULL REFERENCES nc_places (place_id),
  visit_year       INTEGER,
  expedition_id    UUID REFERENCES nc_expeditions (expedition_id),
  point            GEOMETRY(POINT, 4326),
  PRIMARY KEY (artist_id, place_id)
);

CREATE INDEX nc_artist_places_point_idx ON nc_artist_places USING GIST (point);
```

### 6.2 Core Spatial Queries

```sql
-- Q1: Places within map viewport (homepage map)
SELECT p.place_id, p.name, p.fcode, p.centroid,
       COUNT(DISTINCT it.illustration_id) AS illustration_count
FROM nc_places p
LEFT JOIN nc_taxon_place tp ON p.place_id = tp.place_id
LEFT JOIN nc_illustration_taxon it ON tp.taxon_id = it.taxon_id
LEFT JOIN nc_illustrations i ON it.illustration_id = i.illustration_id
  AND i.product_safe = true
WHERE ST_Within(p.centroid, ST_MakeEnvelope($west, $south, $east, $north, 4326))
GROUP BY p.place_id
ORDER BY illustration_count DESC;

-- Q2: Adjacent places (tourism path)
SELECT p2.place_id, p2.name, p2.fcode,
       ST_Distance(p1.centroid::geography, p2.centroid::geography) / 1000 AS dist_km
FROM nc_places p1
JOIN nc_places p2 ON p1.place_id <> p2.place_id
WHERE p1.place_id = $place_id
  AND ST_DWithin(p1.centroid::geography, p2.centroid::geography, 600000)
ORDER BY dist_km
LIMIT 5;

-- Q3: Taxa confirmed within place polygon (species occurrence gate)
SELECT DISTINCT t.taxon_id, t.scientific_name, t.common_name,
                tp.occurrence_count
FROM nc_taxa t
JOIN nc_taxon_place tp ON t.taxon_id = tp.taxon_id
WHERE tp.place_id = $place_id
  AND tp.gbif_confirmed = true
  AND tp.occurrence_count > 0
ORDER BY tp.occurrence_count DESC
LIMIT 50;

-- Q4: Expeditions intersecting a place
SELECT e.expedition_id, e.name, e.start_year, e.end_year, e.lead_naturalist
FROM nc_expeditions e
JOIN nc_places p ON ST_Intersects(e.route, p.geom)
WHERE p.place_id = $place_id
  AND e.route IS NOT NULL;

-- Q5: Places within a bioregion
SELECT p.place_id, p.name, p.centroid
FROM nc_places p
JOIN nc_bioregions b ON ST_Within(p.centroid, b.geom)
WHERE b.name = $bioregion_name;

-- Q6: Artist place visits on map
SELECT ap.artist_id, ap.place_id, ap.visit_year,
       p.name AS place_name, ap.point
FROM nc_artist_places ap
JOIN nc_places p ON ap.place_id = p.place_id
WHERE ap.artist_id = $artist_id
  AND ap.point IS NOT NULL
ORDER BY ap.visit_year;

-- Q7: Nearest place with a published collection (commerce path)
SELECT c.collection_id, c.name, c.slug, c.status,
       ST_Distance(p1.centroid::geography, p2.centroid::geography)/1000 AS dist_km
FROM nc_places p1
JOIN nc_places p2 ON p1.place_id <> p2.place_id
JOIN nc_collections c ON c.anchor_place_id = p2.place_id
WHERE p1.place_id = $place_id
  AND c.status IN ('live', 'coming_soon')
  AND ST_DWithin(p1.centroid::geography, p2.centroid::geography, 5000000)
ORDER BY dist_km
LIMIT 3;
```

---

## Part VIII: Architecture Verdict

### 7.1 Technology Assignment by Phase

| Technology | Role | Phase 0 (now) | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|---|---|
| **PostgreSQL** | Canonical authority | ✓ all writes | ✓ all writes | ✓ all writes | ✓ all writes |
| **PostGIS** | Spatial authority | ✓ activate now | ✓ | ✓ | ✓ |
| **pg_trgm** | Text search | ✓ activate now | ✓ | ✓ | ✓ |
| **PostgreSQL CTE** | Graph traversal (≤4 hops) | ✓ sufficient | ✓ sufficient | ✓ primary | ✓ fallback |
| **Neo4j** | Derived graph projection | ✗ not authorized | ✗ below threshold | ✓ when >5K illustrations | ✓ full |
| **pgvector** | Semantic similarity | ✗ not authorized | ✗ below threshold | ✓ when captions exist | ✓ full |

### 7.2 What Each Reference Model Actually Requires at NC's Current Scale

| Reference model pattern | NC adoption | Required tech |
|---|---|---|
| Airbnb: map-first place browsing | Homepage + Place pages | PostGIS |
| Airbnb: proximity discovery | Related places on Place page | PostGIS |
| Rijksmuseum: maker traversal | Artist profile, "by same artist" | PostgreSQL CTE |
| Rijksmuseum: subject traversal | "More from this place" | PostgreSQL CTE |
| Rijksmuseum: period grouping | Period filter, contemporary artists | PostgreSQL CTE |
| Rijksmuseum: expedition routes | Artist profile map layer | PostGIS LineString |
| Google Arts & Culture: cross-institution | Multi-institution illustrations per place | PostgreSQL CTE |
| Google Arts & Culture: color discovery | Color palette filter | PostgreSQL JSONB array |
| Smithsonian: cross-discipline | Illustration → Taxon → Place | PostgreSQL 3-hop CTE |
| Smithsonian: specimen origin | Species occurrence within place | PostGIS ST_Within |
| Spotify: "fans also like" | NOT YET — requires session behavior graph | Neo4j (Phase 3) |
| Spotify: artist influence chains (5+ hops) | NOT YET — too few artists today | Neo4j (Phase 2) |
| Google Arts & Culture: collaborative filtering | NOT YET — no user behavioral data | Neo4j (Phase 3) |

### 7.3 Conditions for Neo4j Authorization (SD-AMEND-1 prerequisites)

Neo4j activation requires all three of:

1. **Scale threshold**: ≥ 5,000 product-safe illustrations OR ≥ 100 places in the canonical graph
2. **Performance evidence**: PostgreSQL CTE p95 latency for Place→Taxon→Illustration path exceeds
   200ms on production traffic with genuine query volume
3. **Behavioral data**: ≥ 10,000 user session records enabling meaningful collaborative filtering

Until these are met, the operative architecture is PostgreSQL CTE + PostGIS per NC-AI-001 Section I.2.

### 7.4 The Discovery Graph Design Is Not Wasted

Designing the full graph schema now (Part V) is not premature. It:

- Defines the PostgreSQL table structure that CTEs will traverse (same entities, same relationships
  expressed as FK columns and join tables)
- Defines exactly what the Neo4j projection worker will extract from PostgreSQL when activated
- Enables the projection pipeline from `neo4j_pgvector_runtime_architecture_v1.md` to be implemented
  without redesign
- Provides the wireframe target and UX vocabulary for product, editorial, and engineering

The graph schema IS the PostgreSQL schema. The difference is only in the query mechanism.

---

## Part IX: Implementation Sequence

### Phase 0 (immediate)

```
1. PostGIS extension confirmed active (nc_places geometry populated)
2. pg_trgm extension confirmed active (full-text search on title, name, tags)
3. nc_places: add geom GEOMETRY column, centroid GENERATED column, GIST indexes
4. nc_taxon_place: create with occurrence_geom, GIST index
5. nc_expeditions: create with route LINESTRING, GIST index
6. nc_artist_places: create with point geometry
7. nc_bioregions: create with MULTIPOLYGON, seed 4 pilot bioregions
8. Seed canonical place records: 7 pilot places with polygon geometry from GeoNames
9. Seed taxon_place records: GBIF occurrence data for pilot taxa at pilot places
10. Verify Q1–Q7 spatial queries against pilot data
```

### Phase 1 (Sprint 2–3)

```
11. nc_collections: add anchor_place_id FK
12. nc_illustration_taxon: create join table
13. nc_illustration_artist: create join table
14. Populate artist visit records from expedition research
15. Expedition routes: seed HMS Beagle, Hayden Survey, Cook Voyage I geometries
16. Enable Place Detail page spatial queries (Q2 adjacent, Q3 taxa, Q4 expeditions)
17. Enable Artist Profile map layer (Q6)
```

### Phase 2 (when Neo4j threshold is met)

```
18. Director Decision SD-AMEND-1: amend Strategic Direction v1 frozen stack clause
19. Second-human approval per neo4j_pgvector_runtime_architecture_v1 protocol
20. Deploy Neo4j service (projection-only, no public write path)
21. Seed projection_schema_registry from Part V node/relationship vocabulary
22. Run relationship_snapshot_worker full build from PostgreSQL
23. Run neo4j_validation_worker: orphan checks, count validation, source hash checks
24. Enable hybrid discovery API in degraded-safe mode
25. Enable Neo4j-backed discovery behind feature flag
26. Monitor: projection staleness, CTE vs Neo4j latency comparison, drift audit
```

---

## Appendix A: Recommendation Paths Summary

| Path | Name | Hops | Technology | Phase |
|---|---|---|---|---|
| R-1 | Place → Taxon → Illustration | 3 | PostgreSQL CTE | Phase 0 |
| R-2 | Illustration → Artist → Works | 2 | PostgreSQL CTE | Phase 0 |
| R-3 | Place → Adjacent Places | 1 (spatial) | PostGIS ST_DWithin | Phase 0 |
| R-4 | Collection → Place → Collections | 3 | CTE + PostGIS | Phase 1 |
| R-5 | Artist → Contemporary Artists | 2 (derived) | PostgreSQL CTE | Phase 1 |
| R-6 | Illustration → Period → Related | 2 | PostgreSQL CTE | Phase 1 |
| R-7 | Taxon → Place → Illustrations | 2 | PostgreSQL CTE | Phase 1 |
| R-8 | Artist → Expedition → Places | 2 | CTE + PostGIS | Phase 1 |
| R-9 | Artist → Influence → Artist (deep) | 5+ | Neo4j | Phase 2 |
| R-10 | "Collectors also explored" | Variable | Neo4j | Phase 3 |
| R-11 | Personalized discovery | Behavioral | Neo4j | Phase 3 |

---

## Appendix B: Tourism Paths

| Path | Entry | Steps | Output |
|---|---|---|---|
| T-1 | Place page | Place → ST_DWithin → 5 nearest places | Related places widget |
| T-2 | Place page | Place → Bioregion → Bioregion places | Regional discovery |
| T-3 | Artist page | Artist → Expeditions → Places visited | Artist journey map |
| T-4 | Collection page | Collection anchor → nearby collections | "You might also explore" |
| T-5 | Place page | Place → Expedition routes → Other route stops | Expedition thread |

---

## Appendix C: Conservation Paths

| Path | Entry | Steps | Technology |
|---|---|---|---|
| C-1 | Taxon page | Taxon → IUCN status → alert copy | PostgreSQL (evidence layer) |
| C-2 | Taxon page | Taxon → NC Places where depicted | CTE via taxon_place |
| C-3 | Place page | Place → Taxa with IUCN EN/CR | PostgreSQL join |
| C-4 | Illustration page | Illustration → Depicted taxon → IUCN status | CTE 2-hop |
| C-5 | Conservation is evidence layer only | Never a commerce gate | FM-4 permanent |

Conservation status is read from GBIF evidence data. It informs editorial copy but never gates
product activation or pricing. FM-4 is unconditionally permanent.

---

## Appendix D: Collection Paths

| Path | Entry | Steps | Technology |
|---|---|---|---|
| CL-1 | Collections homepage | Collection → Members → Product availability | PostgreSQL join |
| CL-2 | Illustration page | Illustration → Collections it belongs to | PostgreSQL join |
| CL-3 | Place page | Place → Collections anchored here | PostgreSQL CTE |
| CL-4 | Collection page | Collection anchor → adjacent collections | CTE + PostGIS |
| CL-5 | Artist page | Artist → Illustrations → Collections containing them | CTE 3-hop |

---

*NC-GRAPH-IMPLEMENTATION-001 · v1.0 · 2026-06-13 · DRAFT*
