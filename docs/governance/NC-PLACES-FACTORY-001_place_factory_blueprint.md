# NC-PLACES-FACTORY-001: Place Factory Blueprint

| Field | Value |
|---|---|
| Document | NC-PLACES-FACTORY-001 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | IFC v1 · NC-ICH-001 · NC-PLACES-001 · NC-GRAPH-002 · NC-AI-001 |
| Scale targets | 100 places (v0.5) → 1,000 places (v1.0) → 10,000 places (v2.0) |
| Stack | PostgreSQL · PostGIS · Neo4j · Grounded AI |

---

## Governing Doctrine

The Place Factory is the operational pipeline that scales NC from 7 pilot places to 10,000.
It applies the IFC v1 sequencing principle to places: **no place advances past Stage N until
its Stage N exit gate is cleared.** Gate violations are constitutional, not advisory.

The factory is mostly automated. Human judgment is reserved for four permanent gates:
- **Gate AR**: authority resolution conflict
- **Gate CS**: cultural sensitivity and ICH review
- **Gate E**: commerce activation (two-human, permanent)
- **Gate CP**: AI copy review before publish

Everything else runs unattended at scale.

---

## I. Architecture Overview

```
External Sources (9 systems)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Stage 1: SOURCE INGESTION                                                  │
│  Batch pull → normalize → deduplicate → nc_place_candidates                 │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Stage 2: CANDIDATE SCORING                                                 │
│  Heritage + PD + Gap + Commerce → composite score → tier assignment         │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Stage 3: AUTHORITY RESOLUTION                          ←── Gate AR (human) │
│  GeoNames + Wikidata + UNESCO IDs → canonical_identity record               │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Stage 4: PD PRODUCT POTENTIAL SCORING                                      │
│  Institution × expedition × subject scoring → illustration opportunity map  │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Stage 5: ICH CONNECTION                               ←── Gate CS (human)  │
│  ICH practice matching → cultural_sensitivity classification                │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Stage 6: SPATIAL LAYER                                                     │
│  Boundary import → PostGIS → WITHIN_BIOREGION / PROXIMATE_TO               │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Stage 7: GRAPH LAYER                                                       │
│  Neo4j projection → HAS_DESIGNATION / PRACTICED_AT / PROXIMATE_TO          │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Stage 8: AI CONTENT GENERATION                        ←── Gate CP (human)  │
│  Summary + collection headline + story thread + product copy                │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Stage 9: PUBLISHING                                   ←── Gate E (two-human)│
│  Tier assignment → page publish → commerce activation                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## II. Stage 1 — Source Ingestion

### 2.1 Source Systems

Nine source systems feed the factory. Each has a connector, a pull cadence, and a field
mapping to the NC candidate schema.

| Source | Authority | ID field | API / method | Pull cadence |
|---|---|---|---|---|
| UNESCO World Heritage | UNESCO WHC | `id_no` (4-digit) | JSON: `whc.unesco.org/en/list.json` | Monthly |
| UNESCO Biosphere Reserves | UNESCO MAB | MAB ID | Wikidata SPARQL (P2963) | Monthly |
| UNESCO Global Geoparks | UNESCO | Geopark ID | Wikidata SPARQL (P3425) | Monthly |
| Ramsar Sites | Ramsar Secretariat | RamsarID | RSIS JSON: `rsis.ramsar.org/api/sites` | Monthly |
| IDA Dark Sky Places | IDA / Wikidata | IDA ID | Wikidata SPARQL (P7694) | Quarterly |
| Marine Protected Areas | WDPA / MPAtlas | WDPA ID | WDPA API: `api.protectedplanet.net` | Monthly |
| UNESCO ICH Elements | UNESCO | element_id (5-digit) | ICH JSON: `ich.unesco.org` / Wikidata | Monthly |
| National Parks (IUCN II) | WDPA / IUCN | WDPA ID | WDPA API filtered `iucn_cat=II` | Monthly |
| Cultural Landscapes | UNESCO WHC (cultural) | `id_no` | WH JSON filtered `category=Cultural` | (via WH pull) |

### 2.2 Field Mapping Schema

Every source record normalizes to the `nc_candidate_source_records` schema:

```sql
-- Raw source record (one row per source per candidate)
CREATE TABLE nc_candidate_source_records (
  record_id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  source_system      TEXT         NOT NULL,
  -- 'UNESCO_WH' | 'UNESCO_Biosphere' | 'UNESCO_Geopark' | 'Ramsar'
  -- | 'IDA_DarkSky' | 'WDPA_MPA' | 'UNESCO_ICH' | 'WDPA_NP' | 'WDPA_CL'
  source_id          TEXT         NOT NULL,   -- ID within source system
  source_name        TEXT         NOT NULL,   -- official name from source
  source_country     TEXT[],                  -- ISO 3166-1 alpha-2 codes
  source_lat         NUMERIC(9,6),
  source_lon         NUMERIC(9,6),
  source_area_ha     NUMERIC(14,2),
  source_year        INTEGER,                 -- inscription / designation year
  source_status      TEXT,                    -- 'Active' | 'In_Danger' | 'Delisted'
  source_criteria    TEXT[],                  -- for WH sites: criteria used
  source_wh_type     TEXT,                    -- 'natural' | 'cultural' | 'mixed'
  source_raw         JSONB        NOT NULL,   -- full raw record from source
  pull_run_id        UUID         NOT NULL,   -- factory run this record came from
  pulled_at          TIMESTAMPTZ  NOT NULL DEFAULT now(),
  candidate_id       UUID         REFERENCES nc_place_candidates(candidate_id)
);
```

### 2.3 Ingestion Rules

**Rule I-1: Name normalization**
Strip diacritics for slug generation. Keep original `source_name` verbatim in
`source_raw`. Slug = lower(ascii(source_name)) with hyphens, max 80 chars.

**Rule I-2: Duplicate detection**
Before creating a new candidate, check:
1. Exact source ID match (same source system): reject as duplicate
2. Name similarity ≥85% within 50km: flag as probable duplicate, queue for merge review
3. WDPA ID cross-reference: if UNESCO WH and WDPA record point to same coordinates
   within 5km, merge into single candidate, union source system list

**Rule I-3: Delisted records**
UNESCO WH In Danger sites: ingest, score, flag `source_status = 'In_Danger'`.
Delisted sites (e.g., Arabian Oryx Sanctuary): ingest, score, set `pipeline_status = 'hold'`,
require Principal Architect decision before proceeding past Stage 2.

**Rule I-4: ICH-only records**
UNESCO ICH elements without a clear geographic anchor: ingest as `type = 'heritage_practice'`,
route to ICH connection layer directly (skip spatial and geography scoring).
These become `HeritagePractice` nodes, not `Place` nodes.

**Rule I-5: Exclusion list**
Before ingesting, check `nc_place_exclusion_list`. Matching records are silently rejected.
The exclusion list is the only permanent block at Stage 1.

**Rule I-6: Batch size**
Maximum 500 candidates per factory run at v0.5. Increase to 2,000 at v1.0, 10,000 at v2.0.

### 2.4 Source API Specifications

**UNESCO World Heritage (primary source)**
```
GET https://whc.unesco.org/en/list.json
Fields: id_no, site, states_parties, region, category, criteria_txt,
        longitude, latitude, date_inscribed, danger, area_hectares
Filter: date_inscribed IS NOT NULL (skip tentative list)
```

**Ramsar RSIS**
```
GET https://rsis.ramsar.org/api/sites?format=json&page=1&pageSize=100
Fields: RamsarID, Official_name, ISO3, Area_ha, date_of_designation,
        Longitude, Latitude, country
Pagination: iterate pages until empty
```

**WDPA (Protected Planet)**
```
GET https://api.protectedplanet.net/v3/protected_areas
    ?with_geometry=false&token={WDPA_TOKEN}
Fields: wdpaid, name, iucn_cat, status, marine, area_km2, iso3,
        latitude, longitude, designation_type
Filter: status = 'Designated' AND iucn_cat IN ('Ia','Ib','II','III','IV')
```

**UNESCO Biosphere Reserves (Wikidata SPARQL)**
```sparql
SELECT ?item ?name ?country ?mabId ?geonames ?lat ?lon WHERE {
  ?item wdt:P2963 ?mabId .
  ?item wdt:P17 ?country .
  OPTIONAL { ?item wdt:P1566 ?geonames }
  OPTIONAL { ?item p:P625/psv:P625 ?coords .
             ?coords wikibase:geoLatitude ?lat .
             ?coords wikibase:geoLongitude ?lon }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" .
                           ?item rdfs:label ?name }
}
```

**IDA Dark Sky Places (Wikidata SPARQL)**
```sparql
SELECT ?item ?name ?idaId ?country ?lat ?lon WHERE {
  ?item wdt:P7694 ?idaId .
  OPTIONAL { ?item wdt:P17 ?country }
  OPTIONAL { ?item p:P625/psv:P625 ?coords .
             ?coords wikibase:geoLatitude ?lat ;
                     wikibase:geoLongitude ?lon }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" .
                           ?item rdfs:label ?name }
}
```

---

## III. Stage 2 — Candidate Scoring

### 3.1 Composite Score Model

Every candidate receives a composite score (0–100) from four independent dimensions.
The composite score drives tier assignment and processing priority.

```
Composite Score = Heritage Score (0–30)
               + PD Score (0–40)
               + Gap Score (0–20)
               + Commerce Score (0–10)
```

### 3.2 Heritage Score (0–30)

Sum of designation type weights for all confirmed designations. Capped at 30.

| Designation | Points | Notes |
|---|---|---|
| UNESCO WH (any) | 10 | Applied once regardless of criteria count |
| UNESCO WH (mixed — both natural AND cultural) | +3 bonus | Added to the base 10 |
| UNESCO ICH element linked | 8 | Confirmed geographic link required |
| UNESCO Biosphere Reserve | 6 | |
| UNESCO Geopark | 5 | |
| Ramsar Wetland | 4 | |
| Dark Sky (IDA or NPS) | 4 | |
| IUCN I–II (strict protection) | 4 | |
| IUCN III–IV | 3 | |
| Marine Protected Area (high seas) | 3 | |
| WH In Danger modifier | −3 | Reduction, not rejection; flag for review |
| Delisted modifier | −8 | Sets hold flag; requires Director decision |

### 3.3 PD Score (0–40)

Three sub-dimensions.

**A. Institution Coverage (0–15)**

For each approved NC content institution, check if the place's centroid or country falls
within that institution's documented coverage geography.

```python
INSTITUTION_COVERAGE_REGIONS = {
    'nhm':       [(all_expedition_routes), 'ZA', 'TZ', 'KE', 'ID', 'MY', 'AU', 'NZ',
                  'PG', 'NC', 'FJ', 'AQ', 'NG', 'GH'],  # NHM strongest
    'met':       ['JP', 'CN', 'KR', 'IN', 'EG', 'TR', 'GR', 'FR', 'IT'],
    'nga':       ['US'],
    'aic':       ['FR', 'US', 'JP'],
    'cma':       ['CN', 'JP', 'KR'],
    'smk':       ['DK', 'NO', 'SE', 'FI', 'IS', 'DE', 'NL'],
    'walters':   ['JO', 'SA', 'IR', 'IQ', 'TR', 'SY', 'IL', 'MA', 'TN'],
    'yale':      ['NL', 'BE', 'GB', 'US'],
    'getty':     ['NL', 'BE', 'IT', 'FR', 'ES'],
    'mia':       ['*'],  # general collection
    'nara':      ['US'],
    'noaa':      ['US_coastal', 'marine'],
    'dpla':      ['US'],
    'europeana': ['EU_all'],
}

# Score: sum of matched institutions, capped at 15
# NHM match: +5 (strongest institution for gap fill)
# Met/CMA/NGA match: +4 each
# Others: +2–3 each
```

**B. Expedition Coverage (0–15)**

Check if any NC-tracked expedition passed within 500km of the candidate centroid.

| Expedition | Coverage region | Points |
|---|---|---|
| Cook Voyages (I, II, III) | Pacific, NZ, AU, AQ, S.America, Africa coast | 10 |
| Beagle / Darwin (1831–36) | S.America, Galápagos, Pacific, Cape | 10 |
| Humboldt Expedition (1799–1804) | S.America, Caribbean, Mexico | 9 |
| Wallace / Malay Arch. (1854–62) | SE Asia, Indonesia, Borneo, NG | 9 |
| Banks / Solander (1768–71) | Pacific, NZ, AU, S.America | 8 |
| Audubon Expeditions (1820–43) | E.USA, SE.USA, Caribbean, Labrador | 8 |
| J.D. Hooker Expeditions (1839–60) | AQ, India, Himalayas, Morocco, Atlas | 8 |
| EIC Botanical Surveys (1760–1857) | India, Sri Lanka, SE Asia, E.Africa | 7 |
| Cape Surveys (1772–1815) | S.Africa, Namibia, Mozambique | 6 |
| Russian Imperial Expeditions (1733–1845) | Siberia, C.Asia, Kamchatka, Alaska | 5 |
| Challenger Expedition (1872–76) | Global ocean transect | 4 |
| Scott / Shackleton (1901–17) | AQ, S.Georgia, Falklands | 4 |

Points awarded for nearest expedition: max 10, min 1 based on proximity.
Multiple expeditions: take highest + 50% of second highest.

**C. Illustration Subject Type (0–10)**

| Subject type | Points | Rationale |
|---|---|---|
| Island with high endemism | 10 | Unique species = unique illustrations |
| Tropical marine (coral reef, mangrove) | 9 | Colour-rich, high product appeal |
| Mountain / alpine (above treeline) | 8 | Strong landscape painting tradition |
| Tropical rainforest | 8 | Botanical illustration anchor |
| Wetland / delta | 7 | Waterbird illustration tradition |
| Desert / arid | 6 | Expedition illustration, geological |
| Polar / sub-polar | 6 | Expedition art, dramatic landscapes |
| Savanna / grassland | 5 | African wildlife illustration |
| Temperate forest | 5 | Botanical and bird illustration |
| Cultural landscape (urban/agricultural) | 4 | Art historical, less natural history |
| Cave / underground | 3 | Limited PD illustration tradition |

### 3.4 Gap Score (0–20)

Based on NC's geographic coverage deficit from the Institution Coverage Audit v1.

| Region | Points | Priority |
|---|---|---|
| Sub-Saharan Africa | 20 | CRITICAL — zero current coverage |
| Southeast Asia | 20 | CRITICAL — zero current coverage |
| Pacific / Oceania | 19 | CRITICAL — GBR only current coverage |
| Latin America | 18 | CRITICAL — Galápagos only |
| East Asia (China, Japan, Korea) | 16 | HIGH — Met/CMA active but no place pages |
| South Asia (India, Nepal, Sri Lanka) | 15 | HIGH |
| Central Asia / Middle East | 14 | HIGH |
| West Africa / Sahel | 18 | CRITICAL — no institution coverage |
| North Africa | 12 | MEDIUM |
| Eastern Europe | 10 | MEDIUM |
| Northern Europe (Scandinavia) | 8 | MEDIUM — SMK active |
| Western Europe | 5 | LOW — Europeana active |
| North America (non-USA) | 6 | MEDIUM |
| USA | 3 | LOW — multiple institutions active |

### 3.5 Commerce Score (0–10)

| Signal | Points | Rationale |
|---|---|---|
| Priority illustrator confirmed in coverage region | 10 | Audubon, Gould, Merian, Haeckel, etc. |
| Named in existing NC product pipeline | 9 | Cross-reference NC-COMMERCE-001 |
| Proven collector market (botanical, ornithological) | 8 | Sales evidence from comparable prints |
| High visual contrast subject (tropical, polar, volcanic) | 7 | |
| Strong ICH craft tradition (silk, weaving, lacquer) | 7 | ICH-PROD-01/02 path |
| Active tourism category (major NP) | 6 | Audience familiarity |
| Academic/scientific interest primarily | 4 | Niche, lower mass-market appeal |
| Remote or access-restricted | 2 | Limits audience and editorial story |

### 3.6 Tier Assignment

| Composite score | Tier | Processing priority |
|---|---|---|
| 70–100 | **Priority** | Activate next sprint |
| 50–69 | **Near-Ready** | Activate when institution coverage permits |
| 30–49 | **Pipeline** | Batch process at v1.0+ |
| 10–29 | **Low** | v2.0+ processing, re-score as institutions added |
| 0–9 | **Hold** | Requires Director decision to proceed |

---

## IV. Stage 3 — Authority Resolution

### 4.1 Resolution Sequence

Authority resolution produces one `canonical_identity` record per place.
The existing `canonical_identity` schema is extended with factory-specific fields.

```
For each scored candidate:
  Step A1: GeoNames resolution
  Step A2: Wikidata QID resolution
  Step A3: UNESCO / Ramsar / WDPA ID cross-link
  Step A4: Conflict detection
  Step A5: Confidence scoring
  → If confidence ≥ 0.90: AUTO-RESOLVE (no human required)
  → If confidence 0.60–0.89: CONFIRM (human review, 24hr SLA)
  → If confidence < 0.60: ESCALATE (Principal Architect review)
```

### 4.2 GeoNames Resolution Protocol

```python
# Priority feature class hierarchy for NC place types
FCODE_PRIORITY = {
    # National parks and protected areas
    'PRKA': 100,  # Park — highest priority for NPs
    'PRKN': 90,   # National park
    'PRKS': 85,   # State park
    # Natural features
    'RF':   95,   # Reef
    'LK':   80,   # Lake
    'LKNI': 78,   # Intermittent lake
    'MT':   80,   # Mountain
    'MTS':  75,   # Mountains
    'ISL':  85,   # Island
    'ISLS': 80,   # Islands
    'VLC':  75,   # Volcano
    'BAY':  70,   # Bay
    'FJD':  70,   # Fjord
    'WTLD': 65,   # Wetland
    # Administrative (fallback only)
    'ADM2': 40,
    'ADM1': 30,
    'PCLI': 10,
}

def resolve_geonames(name, country_code, lat, lon, area_ha):
    candidates = geonames_search(
        q=name,
        country=country_code,
        featureClass=['S', 'H', 'T', 'L'],  # spot, hydrography, mountain, parks
        maxRows=10,
    )
    scored = []
    for c in candidates:
        score = (
            name_similarity(name, c.name) * 0.4  # 40% weight
            + proximity_score(lat, lon, c.lat, c.lon) * 0.35  # 35% weight
            + FCODE_PRIORITY.get(c.fcode, 0) / 100 * 0.25     # 25% weight
        )
        scored.append((score, c))
    scored.sort(reverse=True)
    if len(scored) == 0:
        return RESOLUTION_FAILED
    if scored[0][0] >= 0.90:
        return AUTO_RESOLVED(scored[0][1])
    if scored[0][0] >= 0.70 and len(scored) > 1 and scored[1][0] < 0.60:
        return CONFIRM_REQUIRED(scored[0][1])
    return ESCALATE(scored)
```

### 4.3 Wikidata Resolution Protocol

```sparql
# Primary lookup: by P1566 (GeoNames ID) — most reliable cross-reference
SELECT ?item ?label ?p1566 ?p757 ?p3090 ?p2963 ?p3425 ?p7694 WHERE {
  ?item wdt:P1566 "%GEONAMES_ID%" .
  OPTIONAL { ?item wdt:P757 ?p757 }   # WHC site number
  OPTIONAL { ?item wdt:P3090 ?p3090 } # Ramsar site number
  OPTIONAL { ?item wdt:P2963 ?p2963 } # MAB Biosphere ID
  OPTIONAL { ?item wdt:P3425 ?p3425 } # UNESCO Geopark ID
  OPTIONAL { ?item wdt:P7694 ?p7694 } # IDA Dark Sky ID
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" .
                           ?item rdfs:label ?label }
}
```

Secondary lookup (when GeoNames not yet resolved):
```sparql
SELECT ?item ?label ?p1566 WHERE {
  ?item rdfs:label "%CANDIDATE_NAME%"@en .
  ?item wdt:P17 wd:%COUNTRY_QID% .
  OPTIONAL { ?item wdt:P1566 ?p1566 }
}
LIMIT 10
```

### 4.4 Cross-Border Resolution Rules

Cross-border sites (bi-national, tri-national, or Antarctic) require special handling.

| Scenario | Rule |
|---|---|
| Bi-national site (e.g., Iguazú Falls AR/BR) | Anchor to primary country NP slug; second country noted in `notes` field. Single `canonical_identity` for the shared natural feature. |
| Tri-national site (e.g., Wadden Sea NL/DE/DK) | Anchor to UNESCO WH site number as primary ID; GeoNames for centroid only; flag `is_transboundary = true`. |
| Antarctic sites | Apply S-3 equivalent: no GeoNames sovereign boundary. Use GeoNames geographic feature (bay, peninsula, mountain) as anchor. No country code required. |
| ICH multinational (e.g., Falconry) | Apply ICH-4: `ich_element_id` is identity authority. GeoNames for each practicing country separately. No single place anchor required. |

### 4.5 Conflict Detection and Resolution Queue

```sql
-- Items requiring human review
CREATE TABLE nc_authority_resolution_queue (
  queue_id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id      UUID         NOT NULL REFERENCES nc_place_candidates(candidate_id),
  conflict_type     TEXT         NOT NULL,
  -- 'geonames_ambiguous': multiple candidates, score gap < 0.20
  -- 'name_mismatch': official name differs from GeoNames name by > 20%
  -- 'cross_border': transboundary site requiring anchor decision
  -- 'no_geonames_match': zero GeoNames results
  -- 'delisted': designation status = 'Delisted'
  -- 'cultural_sensitivity': ICH practice with restricted flag suspected
  conflict_detail   JSONB        NOT NULL,   -- the conflicting candidates
  auto_suggestion   JSONB,                   -- system's best guess with confidence
  assigned_to       TEXT,                    -- reviewer
  sla_deadline      TIMESTAMPTZ,             -- 24h for CONFIRM, 72h for ESCALATE
  status            TEXT         NOT NULL DEFAULT 'open'
    CHECK (status IN ('open', 'resolved', 'escalated', 'rejected')),
  resolution        JSONB,                   -- final decision with rationale
  resolved_at       TIMESTAMPTZ,
  created_at        TIMESTAMPTZ  NOT NULL DEFAULT now()
);
```

---

## V. Stage 4 — PD Product Potential Scoring

### 5.1 Illustration Opportunity Map

Stage 4 produces an `illustration_opportunity_map` for each place: a structured prediction
of what PD content exists, from which institutions, and at what quality level.

```sql
CREATE TABLE nc_place_pd_scores (
  pd_score_id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id         UUID         NOT NULL REFERENCES nc_place_candidates(candidate_id),
  institution_coverage JSONB        NOT NULL,   -- per-institution coverage assessment
  -- {
  --   "nhm": {"score": 12, "confidence": 0.85, "content_type": ["natural_history","expedition"]},
  --   "met": {"score": 8, "confidence": 0.70, "content_type": ["woodblock","asian_art"]},
  --   ...
  -- }
  expedition_coverage  JSONB        NOT NULL,   -- matched expeditions
  -- [{"expedition": "cook-voyages", "proximity_km": 45, "points": 10}, ...]
  subject_type         TEXT         NOT NULL,   -- primary illustration subject category
  subject_score        INTEGER      NOT NULL,
  institution_score    INTEGER      NOT NULL,
  expedition_score     INTEGER      NOT NULL,
  pd_total             INTEGER      NOT NULL,   -- 0–40
  priority_illustrators TEXT[],                 -- Audubon, Gould, etc. identified
  priority_collections TEXT[],                 -- specific known collections
  predicted_asset_count_min INTEGER,           -- conservative estimate
  predicted_asset_count_max INTEGER,           -- optimistic estimate
  computed_at          TIMESTAMPTZ  NOT NULL DEFAULT now()
);
```

### 5.2 Institution × Geography Matrix

The scoring engine uses a pre-computed coverage polygon for each institution.
At Stage 4, the place centroid is tested against each institution's coverage polygon.

```python
# Coverage polygons loaded at engine startup
INSTITUTION_POLYGONS = {
    'nhm': load_multipolygon([
        'expedition:cook-voyage-1',
        'expedition:cook-voyage-2',
        'expedition:beagle',
        'expedition:challenger',
        'region:sub-saharan-africa',
        'region:southeast-asia',
        'region:pacific-oceania',
        'region:south-america-amazon',
    ]),
    'met': load_multipolygon([
        'region:japan',
        'region:china',
        'region:korea',
        'region:near-east',
        'region:ancient-egypt',
        'region:mediterranean-europe',
    ]),
    'nga': load_multipolygon(['region:north-america']),
    'cma': load_multipolygon(['region:east-asia']),
    'smk': load_multipolygon(['region:scandinavia', 'region:northern-europe']),
    'walters': load_multipolygon(['region:islamic-world', 'region:near-east', 'region:north-africa']),
    'yale': load_multipolygon(['region:dutch-golden-age', 'region:british-isles']),
    'getty': load_multipolygon(['region:dutch-golden-age', 'region:mediterranean-europe']),
}

def score_institution_coverage(centroid, country_code):
    score = 0
    coverage = {}
    for inst, polygon in INSTITUTION_POLYGONS.items():
        if ST_Within(centroid, polygon) or country_code in INSTITUTION_COUNTRIES[inst]:
            pts = INSTITUTION_BASE_SCORES[inst]
            score += pts
            coverage[inst] = pts
    return min(score, 15), coverage
```

### 5.3 Known High-Priority Institution × Place Pairs

These pairs have confirmed or near-confirmed PD content and are pre-scored at maximum:

| Place slug | Institution | Known content | Pre-score |
|---|---|---|---|
| `galapagos-islands` | NHM | Gould *Zoology of the Beagle* (finches, tortoises) | 38/40 |
| `tierra-del-fuego` | NHM | Beagle voyage: Martens watercolours, FitzRoy charts | 36/40 |
| `fiordland-national-park` | NHM | Parkinson *Banks Florilegium*, Cook voyage NZ | 37/40 |
| `everglades-national-park` | NHM | Audubon *Birds of America* (Havell aquatints) | 38/40 |
| `yosemite-national-park` | NGA | Bierstadt / Moran landscape oils | 36/40 |
| `mount-fuji` | Met | Hokusai / Hiroshige ukiyo-e (CC0 confirmed) | 39/40 |
| `himalayas-sagarmatha` | NHM | Hooker *Rhododendrons of Sikkim-Himalaya* | 35/40 |
| `borneo-kinabatangan` | NHM | Wallace *Malay Archipelago* plates | 34/40 |
| `cape-of-good-hope` | NHM | Levaillant *Oiseaux d'Afrique*, Masson botanicals | 36/40 |
| `antactic-peninsula` | NHM | Edward Wilson watercolours (Scott expeditions) | 33/40 |

---

## VI. Stage 5 — ICH Connection Layer

### 6.1 Automated ICH Matching

For each place passing Stage 4, the ICH matching engine queries the NC ICH registry
for practices geographically associated with the place.

```sql
-- ICH matching query
-- Finds practices practiced within 300km of place centroid
-- or in the same country
WITH place_centroid AS (
  SELECT
    c.candidate_id,
    pg.centroid AS geom,
    c.primary_country_code
  FROM nc_place_candidates c
  JOIN place_geometry pg ON pg.slug = c.slug_candidate
  WHERE c.candidate_id = $candidate_id
)
SELECT
  hp.practice_id,
  hp.slug,
  hp.display_name,
  hp.unesco_domain,
  hp.cultural_sensitivity,
  hp.countries,
  ST_Distance(
    pa.centroid::geography,
    pc.geom::geography
  ) / 1000 AS distance_km,
  CASE
    WHEN pc.primary_country_code = ANY(hp.countries) THEN 'country_match'
    WHEN ST_DWithin(pa.centroid::geography, pc.geom::geography, 300000) THEN 'proximity'
    ELSE 'none'
  END AS match_reason
FROM nc_heritage_practices hp
JOIN nc_practice_place_anchors ppa ON ppa.practice_id = hp.practice_id
JOIN place_geometry pa ON pa.slug = (
  SELECT pg2.slug FROM place_geometry pg2
  JOIN nc_place_candidates nc2 ON nc2.slug_candidate = pg2.slug
  WHERE nc2.candidate_id IN (
    SELECT candidate_id FROM nc_place_candidates
    WHERE candidate_id = ppa.place_id
  )
  LIMIT 1
)
CROSS JOIN place_centroid pc
WHERE (
  pc.primary_country_code = ANY(hp.countries)
  OR ST_DWithin(pa.centroid::geography, pc.geom::geography, 300000)
)
ORDER BY distance_km ASC;
```

### 6.2 Cultural Sensitivity Classification

Every ICH match generates a `cultural_sensitivity` record. The sensitivity gate (Gate CS)
is **always human-reviewed** — no auto-approval for cultural sensitivity.

| Condition | Classification | Action |
|---|---|---|
| Practice involves sacred ceremony or restricted knowledge | `restricted` | Block ALL commerce paths. Flag on place page. No override. |
| Practice involves Indigenous community (non-sacred) | `consult` | Queue for community review. Commerce blocked pending `community_review_status = 'approved'`. |
| Practice is a craft, agricultural, or maritime tradition | `none` | Standard commerce path available. Human review advisory only. |
| Practice is multinational with no specific Indigenous claim | `none` | Standard path. |

### 6.3 Gate CS: Cultural Sensitivity Review Queue

```sql
CREATE TABLE nc_cultural_sensitivity_review (
  review_id           UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id        UUID         NOT NULL REFERENCES nc_place_candidates(candidate_id),
  practice_id         UUID         NOT NULL REFERENCES nc_heritage_practices(practice_id),
  proposed_sensitivity TEXT        NOT NULL,
  reason              TEXT,
  reviewer            TEXT,
  decision            TEXT         CHECK (decision IN ('approved', 'declined', 'restricted', 'consult')),
  community_consulted BOOLEAN      NOT NULL DEFAULT false,
  community_contact   TEXT,        -- contact record for consult path
  decision_notes      TEXT,
  decided_at          TIMESTAMPTZ,
  status              TEXT         NOT NULL DEFAULT 'open',
  created_at          TIMESTAMPTZ  NOT NULL DEFAULT now()
);
```

---

## VII. Stage 6 — PostGIS Spatial Layer

### 7.1 Boundary Import Protocol

For each place passing Gate CS, import spatial data into the existing PostGIS tables.

**Priority boundary sources (in order):**
1. WDPA boundary polygon (if WDPA ID confirmed) — most accurate for protected areas
2. UNESCO WHC boundary (for WH sites) — available as KML from WHC
3. GeoNames bounding box → converted to envelope polygon (fallback)
4. Manual boundary (for places with no digital boundary) — human-digitized, flag `precision = 'manual'`

```sql
-- Boundary import function (extends existing place_geometry table)
INSERT INTO place_geometry (
  slug, name, place_type, region_slug, geom, provenance
)
VALUES (
  $slug,
  $display_name,
  $place_type,
  (SELECT slug FROM region_geometry WHERE ST_Within(ST_MakePoint($lon, $lat)::geometry, geom) LIMIT 1),
  ST_GeomFromGeoJSON($boundary_geojson),
  jsonb_build_object(
    'source', $boundary_source,      -- 'WDPA' | 'WHC' | 'GeoNames_bbox' | 'manual'
    'wdpa_id', $wdpa_id,
    'precision', $precision,         -- 'polygon' | 'bbox' | 'point_buffer'
    'factory_run_id', $run_id,
    'imported_at', now()
  )
);
```

### 7.2 Spatial Enrichment Queries

After boundary import, run the full spatial enrichment suite:

```sql
-- 1. WITHIN_BIOREGION assignment
UPDATE nc_places p
SET bioregion_id = (
  SELECT bioregion_id FROM nc_bioregions b
  WHERE ST_Within(
    (SELECT centroid FROM place_geometry WHERE slug = p.slug),
    b.geom
  )
  ORDER BY ST_Area(b.geom) ASC  -- smallest containing bioregion
  LIMIT 1
)
WHERE p.slug = $slug;

-- 2. PROXIMATE_TO pairs (≤ 600km between centroids)
INSERT INTO nc_place_proximity (place_slug_a, place_slug_b, distance_km)
SELECT
  $slug AS place_slug_a,
  pg2.slug AS place_slug_b,
  ST_Distance(pg1.centroid::geography, pg2.centroid::geography) / 1000 AS distance_km
FROM place_geometry pg1
JOIN place_geometry pg2 ON pg2.slug <> $slug
WHERE pg1.slug = $slug
  AND ST_DWithin(pg1.centroid::geography, pg2.centroid::geography, 600000)
ON CONFLICT (place_slug_a, place_slug_b) DO UPDATE
  SET distance_km = EXCLUDED.distance_km;

-- 3. Marine territory detection
UPDATE nc_places
SET is_marine = true
WHERE slug = $slug
  AND ST_Intersects(
    (SELECT geom FROM place_geometry WHERE slug = $slug),
    (SELECT geom FROM region_geometry WHERE slug = 'global-ocean')
  );

-- 4. Elevation zone classification
-- (Uses SRTM data loaded into elevation_raster table)
UPDATE nc_places
SET elevation_zone = CASE
  WHEN avg_elevation_m > 3500 THEN 'alpine'
  WHEN avg_elevation_m > 1500 THEN 'montane'
  WHEN avg_elevation_m < 0    THEN 'marine'
  ELSE 'lowland'
END
WHERE slug = $slug;
```

### 7.3 Spatial Overlap Detection

Detect spatial overlap with existing NC places to prevent duplicate place pages.

```sql
-- Overlap detection (>50% area overlap = probable duplicate)
SELECT
  pg_new.slug AS new_candidate,
  pg_exist.slug AS existing_place,
  ST_Area(ST_Intersection(pg_new.geom, pg_exist.geom)::geography) /
  ST_Area(pg_new.geom::geography) AS overlap_fraction
FROM place_geometry pg_new
CROSS JOIN place_geometry pg_exist
WHERE pg_new.slug = $candidate_slug
  AND pg_exist.slug <> $candidate_slug
  AND ST_Intersects(pg_new.geom, pg_exist.geom)
HAVING overlap_fraction > 0.50;
-- Result > 0.50: flag for merge review before activating new place
-- Result 0.10–0.50: flag as related places (component/sub-place relationship)
-- Result < 0.10: no overlap concern
```

---

## VIII. Stage 7 — Neo4j Discovery Layer

### 8.1 Graph Enrichment Sequence

After spatial enrichment, each new place is projected into Neo4j. The projection worker
follows the G-1 through G-8 invariants from NC-GRAPH-002. New ICH relationships
follow ICH-1 through ICH-6.

```python
def project_new_place(place_slug: str, run_id: str) -> None:
    """Full graph enrichment for a newly activated place."""
    with neo4j_session() as session:
        # 1. Create / update Place node (G-2: provenance block required)
        session.execute_write(_upsert_place_node, place_slug, run_id)

        # 2. Project HAS_DESIGNATION edges from nc_place_designations
        session.execute_write(_project_has_designation, place_slug, run_id)

        # 3. Project PRACTICED_AT edges from nc_practice_place_anchors
        session.execute_write(_project_practiced_at, place_slug, run_id)

        # 4. Project WITHIN_BIOREGION from nc_place_bioregion
        session.execute_write(_project_within_bioregion, place_slug, run_id)

        # 5. Project PROXIMATE_TO from nc_place_proximity (PostGIS derived)
        session.execute_write(_project_proximate_to, place_slug, run_id)

        # 6. Project LOCATED_IN (admin hierarchy)
        session.execute_write(_project_located_in, place_slug, run_id)

        # 7. Compute CONTEMPORARY_WITH for artists connected to this place
        session.execute_write(_compute_contemporary_with, place_slug, run_id)

        # 8. Compute CO_OCCURS_WITH for taxa at this place
        session.execute_write(_compute_co_occurs_with, place_slug, run_id)

        # 9. Compute CO_PRACTICED_WITH for connected ICH practices
        session.execute_write(_compute_co_practiced_with, place_slug, run_id)

        # 10. Update designation_stack_height on Place node
        session.execute_write(_update_stack_height, place_slug)

        # Log completion
        log_projection_event(place_slug, run_id, 'PLACE_PROJECTION_COMPLETE')
```

### 8.2 Discovery Path Verification

After projection, run a suite of smoke tests to verify the place is discoverable:

```cypher
// Smoke test 1: Place is reachable from the discovery grid
MATCH (p:Place {slug: $slug})
OPTIONAL MATCH (p)-[:WITHIN_BIOREGION]->(b:Bioregion)
OPTIONAL MATCH (p)-[:HAS_DESIGNATION]->(hd:HeritageDesignation)
OPTIONAL MATCH (p)<-[:ASSOCIATED_WITH]-(i:Illustration)
  WHERE i.product_safe = true
RETURN
  p.name AS place,
  count(DISTINCT b) AS bioregion_count,  -- should be 1
  count(DISTINCT hd) AS designation_count,
  count(DISTINCT i) AS product_safe_illustrations
// PASS: bioregion_count = 1, designation_count ≥ 1

// Smoke test 2: Place has at least one PROXIMATE_TO neighbor
MATCH (p:Place {slug: $slug})-[:PROXIMATE_TO]->(neighbor:Place)
RETURN count(neighbor) AS neighbors
// PASS: neighbors ≥ 1 (fail = isolated place, check spatial data)

// Smoke test 3: ICH connections intact
MATCH (p:Place {slug: $slug})<-[:PRACTICED_AT]-(hp:HeritagePractice)
OPTIONAL MATCH (hp)-[:DOCUMENTED_BY]->(i:Illustration)
  WHERE i.product_safe = true
RETURN
  count(DISTINCT hp) AS ich_elements,
  count(DISTINCT i)  AS commerce_eligible_illustrations
// PASS if ich_elements ≥ 1 (or 0 if no ICH match confirmed at Stage 5)
```

---

## IX. Stage 8 — AI Content Generation Layer

### 9.1 Content Generation Schema

The AI layer generates four content types per place. All four are grounded by the
graph context assembled at Stages 6–7. The AI cannot assert facts absent from the
structured context (NC-AI-001 invariant AI-ATT-1).

| Content type | Max length | Source grounding | Human review required |
|---|---|---|---|
| Place summary | 2 sentences | Place node + Designation nodes + Bioregion | Yes — Gate CP |
| Collection headline | 8 words | Place + primary illustration + Expedition | Yes — Gate CP |
| Story thread | 3 paragraphs | Full graph subgraph (Place + Illustration + Artist + Expedition + ICH) | Yes — Gate CP |
| Product copy | 40 words per product | Illustration + Artist + Institution + HeritagePractice | Yes — Gate CP |

### 9.2 Context Assembly (AI-G1 from NC-AI-001)

```python
def assemble_place_context(place_slug: str) -> dict:
    """
    Build the grounded context for AI content generation.
    Returns a structured dict — AI receives ONLY this, not raw graph.
    """
    with neo4j_session() as session:
        result = session.run("""
            MATCH (p:Place {slug: $slug})
            OPTIONAL MATCH (p)-[:HAS_DESIGNATION]->(hd:HeritageDesignation)
            OPTIONAL MATCH (p)-[:WITHIN_BIOREGION]->(b:Bioregion)
            OPTIONAL MATCH (p)<-[:ASSOCIATED_WITH]-(i:Illustration)
              WHERE i.product_safe = true
            OPTIONAL MATCH (i)-[:CREATED_BY]->(a:Artist)
            OPTIONAL MATCH (i)-[:PART_OF_EXPEDITION]->(e:Expedition)
            OPTIONAL MATCH (i)-[:SOURCED_FROM]->(inst:Institution)
            OPTIONAL MATCH (p)<-[:PRACTICED_AT]-(hp:HeritagePractice)
              WHERE hp.cultural_sensitivity <> 'restricted'
            RETURN p,
                   collect(DISTINCT {type: hd.designation_type, year: hd.inscription_year,
                                     criteria: hd.wh_criteria}) AS designations,
                   b.name AS bioregion,
                   collect(DISTINCT {title: i.display_title, year: i.year,
                                     artist: a.name, expedition: e.name,
                                     institution: inst.display_name}) AS illustrations,
                   collect(DISTINCT {practice: hp.display_name,
                                     domain: hp.unesco_domain}) AS ich_elements
        """, slug=place_slug).single()

    return {
        "place_name":    result["p"]["name"],
        "country":       result["p"]["country_code"],
        "bioregion":     result["bioregion"],
        "designations":  result["designations"],
        "illustrations": result["illustrations"][:10],  # cap at 10 for context window
        "ich_elements":  result["ich_elements"],
        # The AI sees ONLY the above. Not the full graph. Not raw DB.
        "__grounded":    True,
        "__source":      "NC-PLACES-FACTORY-001 Stage 8 context assembly",
    }
```

### 9.3 Generation Prompts

**Place Summary prompt:**
```
You are the editorial voice of Nature & Culture, a commerce platform that connects
public-domain natural history illustration to the world's most significant places.

Context (grounded):
{context_json}

Write a 2-sentence summary of {place_name} for the NC place page.
Rules:
- Assert only facts present in the context above
- Do not invent or infer expedition connections not listed
- Use present tense for the place, past tense for historical events
- Tone: authoritative, precise, evocative — NatGeo quality
- Do not mention NC, the platform, or the commerce context
- Do not include any flags, emoji, or markdown
```

**Collection Headline prompt:**
```
Context (grounded):
{context_json}

Write an 8-word-maximum collection headline for {place_name}.
The headline names the most significant illustration opportunity at this place.
Examples of good headlines:
- "Darwin's Archipelago — Voyage of the Beagle"
- "Hokusai's Mountain — Thirty-Six Views of Fuji"
- "Audubon's Wilderness — Wading Birds and River of Grass"
Rules:
- Use the name of the artist or expedition if present in context
- Do not invent names
- Format: [possessive/evocative phrase] — [short descriptor]
```

### 9.4 Gate CP: Copy Review Queue

```sql
CREATE TABLE nc_place_copy_review (
  review_id        UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id     UUID         NOT NULL REFERENCES nc_place_candidates(candidate_id),
  content_type     TEXT         NOT NULL,  -- 'summary' | 'headline' | 'story' | 'product_copy'
  generated_copy   TEXT         NOT NULL,
  context_used     JSONB        NOT NULL,  -- the grounded context assembled at generation time
  reviewer         TEXT,
  status           TEXT         NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'approved', 'rejected', 'revised')),
  reviewer_notes   TEXT,
  approved_copy    TEXT,                   -- final approved version (may differ from generated)
  reviewed_at      TIMESTAMPTZ,
  created_at       TIMESTAMPTZ  NOT NULL DEFAULT now()
);
```

**Copy review checklist (Gate CP):**
- [ ] Every factual claim can be traced to the grounded context
- [ ] No invented expedition connections, artist attributions, or historical claims
- [ ] Cultural sensitivity language is appropriate for ICH-connected places
- [ ] Attribution lines for GeoNames (CC BY 4.0) are present in the provenance record
- [ ] No NC platform self-reference in editorial copy
- [ ] Tone matches NC voice guidelines

---

## X. Stage 9 — Publishing Tiers

### 10.1 Five-Tier Publication Model

Each place is published at one of five tiers. Tier advancement is sequential.
No place skips a tier. Commerce activation (Gate E) is required for Tier 3+.

```
Tier 0: SEED
  Status: internal_only
  Conditions: slug reserved, canonical_identity confirmed (GeoNames + Wikidata)
  Public: No
  URL: none (slug reserved in nc_places but no web route)

Tier 1: STUB
  Status: coming_soon
  Conditions: Tier 0 + designation stack populated + PostGIS boundary imported + Gate CP (summary)
  Public: Yes (public URL active)
  Content: place name, summary, designation stack cards, map
  Products: None
  Collections: None

Tier 2: ILLUSTRATED
  Status: illustrated
  Conditions: Tier 1 + ≥3 product-safe illustrations in collection + ICH connections visible
              + Gate CP (collection headline + story thread)
  Public: Yes
  Content: all Tier 1 + illustration grid + editorial story + ICH element cards
  Products: None
  Collections: ≥1 collection (PLACE_ANCHOR type)

Tier 3: COMMERCE
  Status: live
  Conditions: Tier 2 + ≥1 active product + Gate E (two-human commerce activation)
              + attribution stack complete (GeoNames + institution + nonendorsement)
  Public: Yes
  Content: all Tier 2 + active product listings
  Products: ≥1 active product
  Collections: ≥1 commerce-enabled collection

Tier 4: PREMIUM
  Status: premium
  Conditions: Tier 3 + ≥3 active products + DESIGNATION_BUNDLE collection (if stack ≥3)
              + recommendation paths active + AI story reviewed
              + related places shown (≥2 PROXIMATE_TO neighbors at Tier 1+)
  Public: Yes
  Content: all Tier 3 + full editorial treatment + discovery collections
  Products: ≥3 active products
  Collections: ≥3 collections including ≥1 ICH collection (if applicable)
```

### 10.2 Publishing State Machine

```sql
CREATE TABLE nc_place_pipeline_state (
  place_id          UUID         PRIMARY KEY REFERENCES nc_places(place_id),
  slug              TEXT         NOT NULL UNIQUE,
  pipeline_status   TEXT         NOT NULL DEFAULT 'ingested'
    CHECK (pipeline_status IN (
      'ingested',           -- Stage 1: source record exists
      'scored',             -- Stage 2: composite score computed
      'authority_pending',  -- Stage 3: awaiting GeoNames/Wikidata resolution
      'authority_resolved', -- Stage 3: canonical_identity confirmed
      'pd_scored',          -- Stage 4: illustration opportunity map computed
      'ich_connected',      -- Stage 5: ICH matches confirmed, sensitivity gate cleared
      'spatially_enriched', -- Stage 6: PostGIS boundary, bioregion, proximity
      'graph_enriched',     -- Stage 7: Neo4j nodes and edges projected
      'copy_generated',     -- Stage 8: AI copy generated, awaiting review
      'copy_approved',      -- Stage 8: Gate CP cleared
      'tier_0',             -- Stage 9: SEED
      'tier_1',             -- Stage 9: STUB
      'tier_2',             -- Stage 9: ILLUSTRATED
      'tier_3',             -- Stage 9: COMMERCE (Gate E cleared)
      'tier_4',             -- Stage 9: PREMIUM
      -- Hold / failure states
      'hold_authority',     -- authority ambiguity, in review queue
      'hold_cultural',      -- cultural sensitivity review in progress
      'hold_commerce',      -- awaiting Gate E sign-offs
      'hold_director',      -- requires Principal Architect decision
      'rejected'            -- failed ingestion or exclusion list match
    )),
  composite_score   INTEGER,
  tier              SMALLINT     CHECK (tier BETWEEN 0 AND 4),
  stage_timestamps  JSONB        NOT NULL DEFAULT '{}',
  -- {"scored": "2026-06-13T...", "authority_resolved": "...", ...}
  gate_ar_cleared   BOOLEAN      NOT NULL DEFAULT false,
  gate_cs_cleared   BOOLEAN      NOT NULL DEFAULT false,
  gate_cp_cleared   BOOLEAN      NOT NULL DEFAULT false,
  gate_e_cleared    BOOLEAN      NOT NULL DEFAULT false,
  gate_e_approver_1 TEXT,
  gate_e_approver_2 TEXT,
  factory_run_id    UUID,
  created_at        TIMESTAMPTZ  NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ  NOT NULL DEFAULT now()
);
```

### 10.3 Gate E: Commerce Activation (Two-Human)

Gate E is unconditional and permanent. No automation may clear Gate E.

```sql
-- Gate E enforcement: two distinct humans required
-- gate_e_approver_1 and gate_e_approver_2 must be different users
-- Neither approver may be the AI content generator

CREATE OR REPLACE FUNCTION enforce_gate_e_two_human()
RETURNS TRIGGER AS $$
BEGIN
  -- Prevent same person approving twice
  IF NEW.gate_e_approver_1 IS NOT NULL
    AND NEW.gate_e_approver_2 IS NOT NULL
    AND NEW.gate_e_approver_1 = NEW.gate_e_approver_2
  THEN
    RAISE EXCEPTION 'Gate E violation: gate_e_approver_1 and gate_e_approver_2 must be different humans';
  END IF;

  -- Prevent clearing gate_e before gate_cp
  IF NEW.gate_e_cleared = true AND NEW.gate_cp_cleared = false THEN
    RAISE EXCEPTION 'Gate E violation: Gate CP (copy review) must be cleared before Gate E';
  END IF;

  -- Enforce that commerce activation requires tier_2 minimum
  IF NEW.gate_e_cleared = true AND COALESCE(NEW.tier, 0) < 2 THEN
    RAISE EXCEPTION 'Gate E violation: place must be at tier_2 (ILLUSTRATED) before commerce activation';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_enforce_gate_e
BEFORE UPDATE ON nc_place_pipeline_state
FOR EACH ROW
WHEN (NEW.gate_e_cleared = true AND OLD.gate_e_cleared = false)
EXECUTE FUNCTION enforce_gate_e_two_human();
```

---

## XI. Throughput Model

### 11.1 Scale Parameters

| Parameter | v0.5 (100 places) | v1.0 (1,000 places) | v2.0 (10,000 places) |
|---|---|---|---|
| Batch size per factory run | 50 | 200 | 1,000 |
| Factory run cadence | Weekly | Daily | Continuous |
| Target throughput (new places/week) | 10 | 50 | 500 |
| Auto-resolve rate (Stage 3) | 70% | 85% | 90% |
| Human review queue depth | ≤10 | ≤40 | ≤100 |
| Gate AR SLA (auto → human) | 48 hours | 24 hours | 12 hours |
| Gate CS SLA | 72 hours | 48 hours | 48 hours |
| Gate CP SLA | 48 hours | 24 hours | 12 hours |
| Gate E SLA | 1 week | 72 hours | 48 hours |
| Stages 1–7 (automated): | ~2 hours | ~30 min | ~5 min |
| Stage 8 (AI generation): | ~5 min | ~2 min | ~30 sec |
| Stage 9 (human gates): | 2–7 days | 1–3 days | 1–2 days |

### 11.2 Bottleneck Analysis

**Primary bottleneck at all scales:** Human review gates (Gate CP always required, Gate E always
two-human). The automated pipeline can produce 1,000 Stage-7-complete places per day at v2.0
scale, but publishing rate is constrained by human review capacity.

**Mitigation strategies:**
- **Batch Gate CP review**: AI generates copy for 20 places in a session; reviewer approves/edits
  in one sitting (1 hour = 15–20 places)
- **Tiered Gate E**: Gate E required only for Tier 3 (commerce activation). Tier 1–2 places can
  publish without Gate E — only commerce adds the two-human gate
- **Auto-renew**: If a place's designation status changes (e.g., WH In Danger), auto-flag for
  re-review rather than auto-demotion
- **Pre-approval queues**: Institution teams can pre-approve standard ICH sensitivity
  classifications for entire practice categories (e.g., "All Japanese craft practices from
  domain TC are classified `none`")

---

## XII. PostgreSQL Schema — Factory Tables

```sql
-- Master candidate registry
CREATE TABLE nc_place_candidates (
  candidate_id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  slug_candidate        TEXT         NOT NULL UNIQUE,  -- proposed NC slug
  official_name         TEXT         NOT NULL,
  source_systems        TEXT[]       NOT NULL,  -- which source systems this candidate came from
  primary_country_code  TEXT,                   -- ISO 3166-1 alpha-2
  all_country_codes     TEXT[],                 -- for transboundary candidates
  source_lat            NUMERIC(9,6),
  source_lon            NUMERIC(9,6),
  composite_score       INTEGER,                -- final composite score (0–100)
  heritage_score        SMALLINT,
  pd_score              SMALLINT,
  gap_score             SMALLINT,
  commerce_score        SMALLINT,
  tier_assignment       SMALLINT,               -- 1–4 or NULL if unscored
  place_type_primary    TEXT,                   -- UNESCO_WH | Biosphere | Geopark | Ramsar | etc.
  is_transboundary      BOOLEAN      NOT NULL DEFAULT false,
  has_cultural_flag     BOOLEAN      NOT NULL DEFAULT false,
  pipeline_status       TEXT         NOT NULL DEFAULT 'ingested',
  factory_run_id        UUID,
  promoted_to_place_id  UUID,                   -- FK to nc_places once activated
  exclusion_reason      TEXT,                   -- if rejected
  created_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),
  updated_at            TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Source records (one per source system per candidate)
CREATE TABLE nc_candidate_source_records (
  record_id             UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id          UUID         NOT NULL REFERENCES nc_place_candidates(candidate_id),
  source_system         TEXT         NOT NULL,
  source_id             TEXT         NOT NULL,
  source_name           TEXT         NOT NULL,
  source_country        TEXT[],
  source_lat            NUMERIC(9,6),
  source_lon            NUMERIC(9,6),
  source_area_ha        NUMERIC(14,2),
  source_year           INTEGER,
  source_status         TEXT,
  source_criteria       TEXT[],
  source_wh_type        TEXT,
  source_raw            JSONB        NOT NULL,
  pull_run_id           UUID         NOT NULL,
  pulled_at             TIMESTAMPTZ  NOT NULL DEFAULT now(),
  UNIQUE (source_system, source_id)
);

-- Factory run log
CREATE TABLE nc_factory_run_log (
  run_id                UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  run_type              TEXT         NOT NULL,  -- 'full' | 'incremental' | 'rescore' | 'reauthorize'
  started_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),
  completed_at          TIMESTAMPTZ,
  sources_pulled        TEXT[],
  candidates_ingested   INTEGER,
  candidates_scored     INTEGER,
  candidates_resolved   INTEGER,
  candidates_blocked    INTEGER,
  new_places_activated  INTEGER,
  review_items_created  INTEGER,
  status                TEXT         NOT NULL DEFAULT 'running'
    CHECK (status IN ('running', 'completed', 'failed', 'aborted')),
  error_summary         TEXT
);

-- Permanent exclusion list
CREATE TABLE nc_place_exclusion_list (
  exclusion_id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  exclusion_type        TEXT         NOT NULL,
  -- 'slug': block a specific slug
  -- 'geonames_id': block a specific GeoNames ID
  -- 'source_id': block a specific source system ID
  -- 'name_pattern': block all candidates matching pattern (for generic exclusions)
  exclusion_value       TEXT         NOT NULL,
  reason                TEXT         NOT NULL,
  added_by              TEXT         NOT NULL,
  added_at              TIMESTAMPTZ  NOT NULL DEFAULT now(),
  expires_at            TIMESTAMPTZ,            -- NULL = permanent
  UNIQUE (exclusion_type, exclusion_value)
);

-- Human review indexes
CREATE INDEX nc_place_candidates_pipeline_status ON nc_place_candidates (pipeline_status);
CREATE INDEX nc_place_candidates_tier ON nc_place_candidates (tier_assignment) WHERE tier_assignment IS NOT NULL;
CREATE INDEX nc_place_candidates_score ON nc_place_candidates (composite_score DESC);
CREATE INDEX nc_authority_resolution_queue_status ON nc_authority_resolution_queue (status) WHERE status = 'open';
CREATE INDEX nc_cultural_sensitivity_review_status ON nc_cultural_sensitivity_review (status) WHERE status = 'open';
CREATE INDEX nc_place_copy_review_status ON nc_place_copy_review (status) WHERE status = 'pending';
```

---

## XIII. Failure Modes and Mitigations

| Failure mode | Detection | Mitigation |
|---|---|---|
| GeoNames API rate limit | HTTP 429 from api.geonames.org | Exponential backoff; max 1,000 req/hour on free tier; upgrade to premium at v1.0 |
| Wikidata SPARQL timeout | Query > 60s | Chunk by country; cache QID lookups; retry once before escalate |
| WDPA API unavailable | HTTP 5xx | Fall back to WDPA monthly bulk download (CSV); queue affected candidates |
| Source name mismatch | Name similarity < 70% | Route to Gate AR queue; do not auto-reject (official names vary significantly) |
| Cross-border anchor conflict | Two or more NPs match same coordinates | IFC sequencing principle applies: hold at Stage 3 until anchor decision |
| Cultural sensitivity false negative | Practice marked `none` but community objects | Revocation path: `community_review_status` can be updated to `declined` post-activation; triggers rights retraction within 15 minutes (G-4) |
| Duplicate place detection | Spatial overlap > 50% | Flag merge candidates; existing place takes precedence unless new candidate has higher score |
| AI hallucination in copy | Factual claim not in grounded context | Gate CP reviewer must reject; regenerate with tighter context; log `context_used` for audit |
| Designation delisted post-activation | UNESCO In Danger or delisted notification | Auto-flag in `nc_heritage_designations.status`; reduce `designation_stack_height`; trigger editorial review notification (do not auto-delist place page) |
| WDPA boundary error | Geometry self-intersection, invalid polygon | `ST_IsValid()` check on import; fall back to GeoNames bounding box; log precision as 'bbox_fallback' |
| Gate E timeout | Two approvals not received within SLA | Escalation notification to Principal Architect; no auto-approval ever |

---

## XIV. Governance Invariants

| Code | Invariant |
|---|---|
| PF-1 | No place advances to Stage N+1 until its Stage N exit gate is cleared. Gate violations are constitutional. |
| PF-2 | Gate E (commerce activation) requires two distinct human approvers. No automation, no override, no single-person bypass. |
| PF-3 | Gate CS (cultural sensitivity) is always human-reviewed. No automation may classify a practice as `none` without a human record. |
| PF-4 | Gate CP (AI copy) is always human-reviewed before publish. AI-generated copy that has not cleared Gate CP must not appear on any public surface. |
| PF-5 | `canonical_identity` is the sole authority for a place's GeoNames ID and Wikidata QID. The factory may propose but not write canonical IDs without Gate AR clearance. |
| PF-6 | Cultural sensitivity `restricted` is a permanent production block. No upgrade path without a new Gate CS record with `community_consulted = true` and a named community contact. |
| PF-7 | A place with `designation_status = 'Delisted'` may not be activated for commerce without a Principal Architect Director Decision. The delisted status must be prominently disclosed on the place page. |
| PF-8 | The `nc_place_exclusion_list` is permanent unless an explicit expiry is set and has passed. Exclusion bypass requires a new Director Decision. |

---

## XV. Implementation Sequence

### Phase PF-1: Infrastructure (prerequisite: NC-ICH-001 Sprint ICH-1)
1. Ratify this document
2. Deploy factory PostgreSQL tables (12 new tables)
3. Deploy source connectors for UNESCO WH, Ramsar, WDPA (3 sources minimum)
4. Deploy composite scoring engine
5. Deploy Gate AR review queue UI (simple admin table view)
6. Seed `nc_place_exclusion_list` with known exclusions (Paris Musées equivalent)

### Phase PF-2: Authority automation (v0.5 — 100 places)
1. Deploy GeoNames resolution worker
2. Deploy Wikidata SPARQL resolution worker
3. Deploy Gate CS review queue UI
4. Run first factory batch: UNESCO WH natural sites only (220 sites), score all, resolve top 50
5. Activate 10 new Tier 1 (STUB) places
6. Run Gate CP review for first 5 place summaries

### Phase PF-3: Full pipeline (v1.0 — 1,000 places)
1. Add remaining 6 source connectors (Biosphere, Geopark, Dark Sky, ICH, MPA, NP)
2. Deploy PostGIS boundary import worker
3. Deploy Neo4j projection worker (extends NC-GRAPH-002 projection_worker)
4. Deploy AI content generation pipeline (extends NC-AI-001)
5. Target: 1,000 Tier 0–1 places within 90 days of Phase PF-3 launch
6. Target: 100 Tier 3 (COMMERCE) places within 180 days

### Phase PF-4: Scale (v2.0 — 10,000 places)
1. Onboard Trove → unlocks ~400 Australian/Pacific candidates
2. Onboard Wellcome → unlocks South Asian, African candidates
3. Run continuous factory (daily batches)
4. Target: 10,000 Tier 0–1 places in the NC registry
5. Target: 1,000 Tier 3+ (COMMERCE) places

---

*NC-PLACES-FACTORY-001 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
