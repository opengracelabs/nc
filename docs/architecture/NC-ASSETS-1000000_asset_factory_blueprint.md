# NC-ASSETS-1000000: Asset Factory Blueprint

| Field | Value |
|---|---|
| Document | NC-ASSETS-1000000 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | Asset Intelligence Constitution v1 · NC-GRAPH-002 · NC-COMMERCE-2000 · Institution Factory Constitution v1 · IFC v1 |
| Scope | Architecture for scaling NC from thousands of assets to 1,000,000. Covers asset factory, taxonomy, collection generation, product generation, trust preservation, rights verification, AI content generation, and discovery graph integration at scale. |
| Reference Models | Europeana · Smithsonian Open Access · Rijksmuseum · DPLA · NHM · BHL |
| Pending DD | DD-BHL-001 (required — BHL is the primary 1M source; no governance document exists) |

---

## Why 1,000,000

The current asset database contains approximately 20 Illustration Opportunities. NC-COMMERCE-2000 projects ~15,000 IOs at 2,000 places. Neither number approaches the scale of the heritage institutions NC draws from.

BHL has 60 million pages. Europeana has 50 million records. The Smithsonian Open Access program has 4.7 million objects. The NHM holds 80 million specimens. The limiting factor at those institutions is curation, not content. NC's limiting factor is the same.

1,000,000 assets in NC's database does not mean 1,000,000 products. It means 1,000,000 records in a governed hierarchy where:
- ~100,000–200,000 are commerce-ready Illustration Opportunities
- ~300,000–400,000 are editorial assets (confirmed PD, illustration type confirmed, not yet commerce-routed)
- ~500,000–700,000 are discovery assets (in the graph for place and taxon context)

The system that routes, classifies, and governs those records is what this document designs.

---

## Source Institution Contribution Estimate

| Source | Protocol | Estimated qualifying assets | Rights basis |
|---|---|---|---|
| **BHL** (new — DD-BHL-001 required) | Page API + image classifier | 500,000+ | Pre-1928 NoC-US; CC0 where published |
| **Europeana** (DD-EUR-001) | OAI-PMH / REST | 200,000+ | CC0, PDM, NoC-US after rights filter |
| **Smithsonian Open Access** (DD-SMITHSONIAN pending) | CSV bulk / API | 100,000+ | CC0 |
| **Getty Open Content** (DD-GETTY-001) | ActivityStreams | 88,000 | CC0 per-record |
| **Metropolitan Museum** (DD-MET-001) | REST cursor | 50,000+ | CC0 boolean |
| **NHM Data Portal** (DD-NHM-001) | CKAN Datastore | 50,000+ | CC0 dataset-level |
| **Mia** (DD-MIA-001) | REST | 64,000+ | Rights Class 3B (rights_type gate) |
| **Walters** (DD-WALTERS-001) | CSV bulk | 36,000+ | CC0 institution-wide |
| **DPLA** (DD-DPLA-001) | Two-tier aggregator | 30,000+ | Aggregator-sourced CC0/PDM |
| **NGA** (DD-NGA-001) | CSV bulk | 20,000+ | CC0 integer flag |
| **Yale YCBA + YUAG** (DD-YALE-001) | Linked Art | 20,000+ | Rights Class 7 subject_to |
| **AIC** (DD-AIC-001) | REST | 20,000+ | Rights Class 3 string |
| **CMA** (DD-CMA-001) | REST | 15,000+ | Rights Class 3 string |
| **NOAA** (DD-NOAA-001) | Flickr API | 10,000+ | § 105 license filter |
| **NARA** (DD-NARA-001) | REST | 10,000+ | Rights Class 9 Unrestricted |
| **SMK** (DD-SMK-001) | REST | 5,000+ | Boolean `public_domain` |
| Future institutions (IFC pipeline) | Various | +100,000 | Per-DD |

**Total estimated qualifying assets at full institution coverage: ~1,000,000–1,200,000**

---

## Part I — Asset Factory

### 1.1 Pipeline Overview

The Asset Factory is the automated system that takes raw records from source institutions and routes them to their correct position in NC's asset hierarchy. It is not a batch job. It is a continuous pipeline with nine stages and four mandatory human gates.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ASSET FACTORY                               │
│                                                                     │
│  SOURCE INSTITUTIONS                                                │
│  BHL · Europeana · Smithsonian · NHM · NGA · Walters · Getty ···   │
│       │                                                             │
│  Stage 1: HARVEST ──────────────────── per-adapter protocol        │
│       │                                                             │
│  Stage 2: NORMALISE ────────────────── → NC canonical record       │
│       │                                                             │
│  Stage 3: RIGHTS SCREEN ───────────── → rights_class + confidence  │
│       │                              ┌─ BLOCKED → discard          │
│       │                              ├─ ALLOWED → continue         │
│       │                              └─ REVIEW → [Gate AR]         │
│       │                                                             │
│  Stage 4: ILLUSTRATION FILTER ──────── → is this an illustration?  │
│       │                              ┌─ NO → discovery_asset only  │
│       │                              └─ YES → continue             │
│       │                                                             │
│  Stage 5: QUALITY SCREEN ──────────── → resolution + completeness  │
│       │                              ┌─ BELOW THRESHOLD → Tier 3   │
│       │                              └─ ABOVE THRESHOLD → continue │
│       │                                                             │
│  Stage 6: IO CANDIDATE GENERATION ──── → attempt IO construction  │
│       │    Illustrator → ULAN lookup                               │
│       │    Place → GeoNames lookup                                 │
│       │    Taxon → GBIF lookup (if natural history)               │
│       │                              ┌─ FULL IO → Tier 1 candidate │
│       │                              ├─ PARTIAL → Tier 2 candidate │
│       │                              └─ NONE → Tier 3             │
│       │                                                             │
│  Stage 7: M36 WRITE ───────────────── → canonical asset record     │
│       │    asset_tier assigned                                      │
│       │    source_institution recorded                              │
│       │    rights_class assigned                                    │
│       │    confidence_score recorded                                │
│       │                                                             │
│  Stage 8: GRAPH INTEGRATION ───────── → nodes + edges written      │
│       │                                                             │
│  Stage 9: PRODUCT ROUTING ─────────── → if Tier 1: route to       │
│           [Gate CP] ─────────────────── curator pre-screen        │
│           [Gate E] ──────────────────── two-human activation      │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Stage 1 — Harvest

Each source institution uses one of eight adapter protocols. The adapter is responsible for fetching records and delivering a raw payload to Stage 2. Adapters run on schedule (daily or weekly depending on source).

| Adapter Class | Protocol | Institutions |
|---|---|---|
| **AC-1: OAI-PMH** | OAI-PMH XML harvest (Dublin Core or EDM) | Europeana; future Tier 1 direct institutions |
| **AC-2: REST cursor** | Paginated JSON REST with cursor/offset | Met · AIC · CMA · SMK |
| **AC-3: CSV bulk** | GitHub or direct bulk download, 15-table schema | NGA · Walters · Smithsonian |
| **AC-4: Linked Art JSON-LD** | Linked Art `@context` traversal | Yale (YCBA + YUAG) |
| **AC-5: ActivityStreams harvest** | ActivityStreams ordered collection pages | Getty |
| **AC-6: CKAN Datastore API** | CKAN `datastore_search` endpoint | NHM |
| **AC-7: Flickr API** | Flickr photo search + license filter | NOAA |
| **AC-8: BHL Page API** | BHL API v3 `GetPageMetadata` + Internet Archive image delivery | BHL (DD-BHL-001 required) |
| **AC-9: DPLA two-tier** | DPLA API → hub institution deref | DPLA |

### 1.3 Stage 2 — Normalise

Every raw payload, regardless of adapter class, is normalised to NC's canonical record schema before any further processing. Normalisation does not interpret or classify — it maps fields.

**NC Canonical Asset Record (normalised):**

```python
{
  # Identity
  "nc_id":                str,     # NC-generated UUID
  "source_institution":   str,     # institution slug (e.g., "nhm", "europeana")
  "source_id":            str,     # institution's own object/image ID
  "source_url":           str,     # direct URL to institution's record page
  "adapter_class":        str,     # AC-1 through AC-9

  # Description
  "title":                str,     # normalised title
  "description":          str,     # normalised description (may be empty)
  "date_raw":             str,     # date string as received
  "date_year":            int,     # parsed year (null if unparseable)
  "creator_raw":          str,     # creator string as received (may be empty)
  "subject_tags":         list,    # normalised subject/tag list

  # Image delivery
  "image_url":            str,     # primary image URL
  "iiif_manifest_url":    str,     # IIIF manifest URL (null if no IIIF)
  "thumbnail_url":        str,     # thumbnail URL

  # Rights (pre-resolution — raw as received)
  "rights_raw":           str,     # rights string as received from institution
  "rights_uri":           str,     # URI if institution provides one
  "rights_class_raw":     str,     # unparsed rights class before Stage 3

  # Metadata completeness
  "has_creator":          bool,
  "has_date":             bool,
  "has_image":            bool,
  "has_iiif":             bool,
  "metadata_completeness": float,  # 0.0–1.0 score
}
```

### 1.4 Stage 3 — Rights Screen

The rights screen is the first gate the asset must pass. It applies the Rights Verification Engine (see Part VI) to produce a `rights_class` and `confidence_score`. Three outcomes:

| Outcome | Meaning | Next stage |
|---|---|---|
| `ALLOWED` | Rights class confirmed, confidence ≥ 0.85 | Stage 4 |
| `REVIEW` | Rights uncertain or confidence < 0.85 | Human gate AR (Authority Review) |
| `BLOCKED` | Rights class is InC, NC, or any permanently excluded class | Discard — do not write to M36 |

**Human Gate AR (Authority Review):**
- Triggered by REVIEW outcome
- Reviewer is the Collection Curator or Institutional Director
- Reviewer sets `human_rights_verdict` to `verified_pd`, `verified_review`, or `blocked`
- Verdict is written to M36 as `rights_status` and `human_verdict` fields
- No commercial product may be activated from a `verified_review` record until a second reviewer confirms

### 1.5 Stage 4 — Illustration Filter

Not every record that passes rights screening is an illustration. At BHL scale especially, most records are text pages, not plates. The illustration filter determines:

1. **Is this an illustration?** (binary classifier)
2. **If yes, what type?** (multiclass classifier)

**Illustration type taxonomy** (see Part II for full taxonomy):

| Code | Type | Description |
|---|---|---|
| `IT-NAT` | Natural history plate | Botanical, zoological, mycological, geological |
| `IT-ARCH` | Architectural drawing | Plans, elevations, ornamental detail, reconstruction |
| `IT-CART` | Cartographic | Map, chart, topographic survey |
| `IT-EXPD` | Expedition field illustration | Field watercolour, expedition drawing |
| `IT-DOCU` | Documentary illustration | Cultural, ethnographic, portrait, costume |
| `IT-ASTR` | Astronomical illustration | Celestial map, star chart, telescope observation |
| `IT-MARI` | Marine illustration | Marine natural history, oceanographic |
| `IT-UNKN` | Unknown illustration type | Passes filter; type resolved in Stage 6 |

Assets that fail the illustration filter (text pages, photographs, specimen records, museum objects that are not illustrations) are classified as **Tier 4 Reference Assets** and written to the graph as context nodes. They do not proceed to Stage 6 IO candidate generation but may contribute to discovery.

**The BHL exception:** BHL page images are ambiguous — a single BHL volume page may be text, a plate, or mixed. BHL pages that fail the illustration filter are retained as text-indexed discovery nodes (BHL's taxonomic name index makes them valuable for graph traversal even without an image).

### 1.6 Stage 5 — Quality Screen

Resolution and metadata completeness check. Thresholds per NC-PRODUCT-001 Article 13:

| Asset class | Minimum pixel dimension | Minimum metadata completeness | Outcome if fails |
|---|---|---|---|
| Museum Print candidate (R1) | 6000px long edge | 0.80 | Demote to R2 candidate |
| Standard Print candidate (R2) | 3000px long edge | 0.60 | Demote to R3 candidate |
| Digital/Educational (R3) | 1200px long edge | 0.40 | Tier 3 only |
| Below all thresholds | < 1200px long edge | Any | Tier 4 only (discovery context) |

**IIIF resolution flag:** If an asset has a IIIF Image API endpoint, resolution is confirmed by querying the `/info.json` endpoint rather than downloading the full image. This is the efficient path at scale.

### 1.7 Stage 6 — IO Candidate Generation

The most important stage. An Illustration Opportunity is not a raw asset — it is an asset with three confirmed anchors: an illustrator (ULAN), a place (GeoNames), and a rights status. Stage 6 attempts to build these anchors automatically.

**Illustrator resolution:**

```python
def resolve_illustrator(creator_raw: str) -> IllustratorResolution:
    # Step 1: Exact match against NC known illustrators (fast path)
    if creator_raw in NC_KNOWN_ILLUSTRATORS:
        return IllustratorResolution(
            ulan_id=NC_KNOWN_ILLUSTRATORS[creator_raw].ulan_id,
            confidence=1.0,
            method="exact_match"
        )

    # Step 2: ULAN API fuzzy lookup
    ulan_result = ulan_api.search(creator_raw, fuzzy=True)
    if ulan_result.best_match_score > 0.85:
        return IllustratorResolution(
            ulan_id=ulan_result.best_match.ulan_id,
            confidence=ulan_result.best_match_score,
            method="ulan_fuzzy"
        )

    # Step 3: Wikidata lookup (DD-WIKIDATA-001: identity layer only)
    wikidata_result = wikidata_api.search_person(creator_raw)
    if wikidata_result.found and wikidata_result.has_ulan_statement:
        return IllustratorResolution(
            ulan_id=wikidata_result.ulan_id,
            confidence=0.80,
            method="wikidata_ulan_claim"
        )

    # Step 4: Unresolved — flag for human review
    return IllustratorResolution(
        ulan_id=None,
        confidence=0.0,
        method="unresolved",
        human_review_required=True
    )
```

**Place resolution:**

```python
def resolve_place(asset: NormalisedAsset) -> PlaceResolution:
    # Extract place candidates from title, description, subject_tags
    candidates = extract_place_candidates(asset)

    for candidate in candidates:
        # GeoNames lookup (authoritative per DD-GEONAMES-001)
        result = geonames_api.search(candidate.text, feature_class=candidate.expected_fclass)
        if result.confidence > 0.80:
            return PlaceResolution(
                geonames_id=result.geonames_id,
                place_name=result.name,
                confidence=result.confidence,
                method="geonames_text_extract"
            )

    # Check Darwin Core locality field (for natural history assets)
    if asset.has_dwc_locality:
        result = geonames_api.search(asset.dwc_locality)
        if result.confidence > 0.70:
            return PlaceResolution(geonames_id=result.geonames_id, confidence=0.70)

    return PlaceResolution(geonames_id=None, confidence=0.0, human_review_required=True)
```

**Taxon resolution (natural history assets only):**

```python
def resolve_taxon(asset: NormalisedAsset) -> TaxonResolution:
    # BHL taxonomic name service (pre-extracted — most reliable)
    if asset.has_bhl_taxon_names:
        gbif_result = gbif_api.match_name(asset.bhl_taxon_names[0])
        if gbif_result.matchType == "EXACT":
            return TaxonResolution(gbif_key=gbif_result.usageKey, confidence=1.0)

    # Extract from title/description using taxonomic pattern matcher
    taxon_candidates = extract_taxon_names(asset.title, asset.description)
    for candidate in taxon_candidates:
        gbif_result = gbif_api.match_name(candidate)
        if gbif_result.confidence > 0.90:
            return TaxonResolution(gbif_key=gbif_result.usageKey, confidence=gbif_result.confidence)

    return TaxonResolution(gbif_key=None, confidence=0.0)
```

**IO tier assignment:**

| Anchors confirmed | Tier | Label |
|---|---|---|
| ULAN + GeoNames + Rights (confidence ≥ 0.85) | **Tier 1** | Commerce-ready IO |
| Rights + one of (ULAN or GeoNames) | **Tier 2** | Editorial asset |
| Rights confirmed, no anchors | **Tier 3** | Discovery asset |
| Rights uncertain or below resolution threshold | **Tier 4** | Reference / context |

### 1.8 Stage 7 — M36 Write

Every asset that passes Stage 3 (rights screen = ALLOWED or REVIEW) is written to the M36 master record table, regardless of tier. The tier is a routing classification, not an admission gate.

**M36 asset record (additions beyond normalised schema):**

```sql
-- New fields written at Stage 7
asset_tier          SMALLINT,    -- 1 / 2 / 3 / 4
illustration_type   TEXT,        -- IT-NAT / IT-ARCH / IT-CART / etc.
rights_class        TEXT,        -- rights class slug
rights_confidence   FLOAT,       -- 0.0–1.0
human_verdict       TEXT,        -- null / 'verified_pd' / 'blocked'
ulan_id             TEXT,        -- null if unresolved
ulan_confidence     FLOAT,
geonames_id         BIGINT,      -- null if unresolved
geonames_confidence FLOAT,
gbif_taxon_key      BIGINT,      -- null if not natural history / unresolved
gbif_confidence     FLOAT,
resolution_method   TEXT,        -- JSON record of how each anchor was resolved
io_status           TEXT,        -- 'candidate' / 'active' / 'deferred' / 'blocked'
created_at          TIMESTAMPTZ,
updated_at          TIMESTAMPTZ
```

**Immutability rule:** Once a `human_verdict` field is written, it may not be overwritten by the automated pipeline. Human verdicts are only modified by a named human using the governance interface.

### 1.9 Stage 8 — Graph Integration

After M36 write, nodes and edges are created in the discovery graph (NC-GRAPH-002). The graph write is the mechanism by which an asset becomes discoverable across places, illustrators, taxa, and collections.

**Nodes created at Stage 8:**

```cypher
// Asset node
CREATE (a:Asset {
  ncId: $nc_id,
  title: $title,
  illustrationType: $illustration_type,
  tier: $asset_tier,
  sourceInstitution: $source_institution,
  rightsClass: $rights_class,
  dateYear: $date_year,
  imageUrl: $image_url
})

// Edges created if anchors resolved:
MATCH (i:Illustrator {ulanId: $ulan_id})
CREATE (a)-[:CREATED_BY]->(i)

MATCH (p:Place {geonamesId: $geonames_id})
CREATE (a)-[:DEPICTS_PLACE]->(p)

MATCH (t:Taxon {gbifKey: $gbif_taxon_key})
CREATE (a)-[:DEPICTS_TAXON]->(t)
```

### 1.10 Stage 9 — Product Routing

Tier 1 assets enter the product routing pipeline (NC-PRODUCT-001 product routing constitution). This stage is not automated end-to-end — it triggers human gate CP (Curator Pre-screen) before any product is created.

**Gate CP (Curator Pre-screen):**
The curator reviews the IO candidate, confirms the ULAN and GeoNames assignments, and approves the asset for product routing. This is a lightweight review, not a full curatorial process — the system has done the research; the curator confirms it.

Gate CP is the human intelligence layer that prevents the automated pipeline from creating bad products at scale. It is intentionally kept lightweight — it should take 2–5 minutes per IO for a well-prepared candidate — so it can operate at volume.

**Gate E (Product Activation):**
Always two named humans. Never automated. The constitutional invariant.

---

## Part II — Asset Taxonomy

### 2.1 Taxonomy Principles

The asset taxonomy must be:
1. **Derivable from metadata** — classification can be determined algorithmically from existing fields
2. **Cross-institution consistent** — a botanical plate from NHM and one from Europeana are the same type
3. **Commerce-informative** — the taxonomy directly drives product routing decisions
4. **CIDOC CRM aligned** — types map to CRM entity types where applicable

### 2.2 Top-Level Classification

```
NC Asset
├── Illustration (IT-*) — the commercial tier
│   ├── Natural History (IT-NAT)
│   │   ├── IT-NAT-BOT  Botanical illustration
│   │   ├── IT-NAT-ZOO  Zoological illustration
│   │   ├── IT-NAT-MYC  Mycological illustration
│   │   ├── IT-NAT-MAR  Marine illustration
│   │   ├── IT-NAT-GEO  Geological / mineralogical illustration
│   │   └── IT-NAT-ECO  Ecological scene (landscape + natural history)
│   ├── Architectural (IT-ARCH)
│   │   ├── IT-ARCH-PLN  Plan / section / elevation
│   │   ├── IT-ARCH-DET  Ornamental detail
│   │   ├── IT-ARCH-PAT  Pattern / tile / geometry
│   │   └── IT-ARCH-REC  Archaeological reconstruction
│   ├── Cartographic (IT-CART)
│   │   ├── IT-CART-MAP  General map
│   │   ├── IT-CART-NAV  Nautical chart
│   │   ├── IT-CART-TOP  Topographic survey
│   │   └── IT-CART-CEL  Celestial / astronomical chart
│   ├── Expedition (IT-EXPD)
│   │   ├── IT-EXPD-FLD  Field watercolour
│   │   ├── IT-EXPD-POR  Expedition portrait
│   │   └── IT-EXPD-LND  Expedition landscape
│   ├── Documentary (IT-DOCU)
│   │   ├── IT-DOCU-CUL  Cultural / ethnographic
│   │   ├── IT-DOCU-COS  Costume / dress
│   │   └── IT-DOCU-ICH  ICH documentary (TC element type)
│   └── Astronomical (IT-ASTR)
│       ├── IT-ASTR-CEL  Celestial observation
│       └── IT-ASTR-CHT  Star chart / atlas
│
├── Context Asset (CA-*) — editorial and discovery use
│   ├── CA-PHO  Historical photograph
│   ├── CA-OBJ  Museum object (not illustration)
│   ├── CA-TXT  Text page (BHL OCR-indexed)
│   └── CA-SPC  Specimen record
│
└── Reference Asset (RA-*) — graph context only
    ├── RA-MAP  Modern map (OSM tile — display only)
    └── RA-DOC  Archival document
```

### 2.3 Classification Model

The illustration type classifier is a three-stage model:

1. **Title/subject-tag keyword classifier** (fast path, ~70% of records): Pattern matching on title and subject tags. "botanical plate", "Haeckel", "Audubon", "plan of the temple" → high confidence without image analysis.

2. **Image visual classifier** (required for ambiguous BHL pages and low-metadata records): CNN-based binary classifier (illustration vs. not), followed by multiclass type classifier. Trained on labeled examples from known collections.

3. **Human confirmation** (for new illustration types or low-confidence results): Curator confirms at Gate CP.

### 2.4 Metadata Completeness Scoring

```python
def metadata_completeness(asset: NormalisedAsset) -> float:
    score = 0.0
    if asset.has_title:          score += 0.15
    if asset.has_creator:        score += 0.25   # most important field
    if asset.has_date:           score += 0.20
    if asset.has_image:          score += 0.20
    if asset.has_description:    score += 0.10
    if asset.has_iiif:           score += 0.05
    if asset.has_subject_tags:   score += 0.05
    return min(score, 1.0)
```

The creator field carries 0.25 of the score because illustrator identity is the primary commercial differentiator. An unattributed botanical plate is a Tier 2 asset at best. The same plate attributed to Redouté is a Tier 1 IO.

---

## Part III — Collection Generation

### 3.1 The Collection Candidate Problem

At pilot scale, collections are built manually: curator selects illustrations, writes copy, publishes. At 1M assets, manual collection building cannot keep pace with ingestion.

The solution is not to automate collection publishing. It is to automate collection *candidacy* — identifying when a set of assets reaches the threshold where a collection is worth a curator's attention — and then routing that candidate to a human for the decisions that require human judgment.

### 3.2 Collection Trigger Rules

A collection candidate is generated when a graph query returns a result set above threshold:

```cypher
// Trigger Rule CT-1: Place + Illustrator density
MATCH (p:Place)-[:DEPICTS_PLACE]-(a:Asset)-[:CREATED_BY]->(i:Illustrator)
WHERE a.tier IN [1, 2]
  AND NOT (a)-[:PART_OF]->(:Collection)
WITH p, i, collect(a) as assets, count(a) as asset_count
WHERE asset_count >= 5
RETURN p.name, i.name, asset_count
ORDER BY asset_count DESC
```

```cypher
// Trigger Rule CT-2: Designation stack + illustration density
MATCH (p:Place)-[:HAS_DESIGNATION]->(d:Designation),
      (p)-[:DEPICTS_PLACE]-(a:Asset)
WHERE a.tier IN [1, 2]
  AND a.dateYear BETWEEN 1750 AND 1900
WITH p, count(DISTINCT d) as desig_count, count(a) as asset_count
WHERE desig_count >= 3 AND asset_count >= 10
  AND NOT EXISTS { MATCH (p)-[:ANCHOR_OF]->(:Collection) }
RETURN p.name, desig_count, asset_count
ORDER BY desig_count DESC, asset_count DESC
```

```cypher
// Trigger Rule CT-3: Illustrator retrospective (illustrator + 10+ places)
MATCH (i:Illustrator)-[:CREATED]->(a:Asset)-[:DEPICTS_PLACE]->(p:Place)
WHERE a.tier = 1
WITH i, count(DISTINCT p) as place_count, count(a) as total_assets
WHERE place_count >= 10 AND total_assets >= 30
RETURN i.name, place_count, total_assets
```

### 3.3 Collection Candidate Record

When a trigger rule fires, a `collection_candidate` record is created:

```sql
CREATE TABLE collection_candidates (
  id              UUID PRIMARY KEY,
  trigger_rule    TEXT,         -- 'CT-1' / 'CT-2' / 'CT-3'
  place_id        BIGINT,       -- GeoNames ID
  illustrator_id  TEXT,         -- ULAN ID (null for CT-2)
  asset_ids       UUID[],       -- qualifying asset IDs
  asset_count     INT,
  tier_1_count    INT,
  tier_2_count    INT,
  designation_stack JSONB,      -- designations for the place
  composite_score FLOAT,        -- 0–100 (from NC-PLACES-FACTORY-001)
  status          TEXT,         -- 'pending' / 'approved' / 'deferred' / 'rejected'
  curator_id      TEXT,         -- curator who reviewed (null until reviewed)
  reviewed_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ
);
```

### 3.4 Gate CS (Curator Selection)

The Curator Selection gate is the human decision on a collection candidate. The curator reviews:
1. The asset set (thumbnail grid of all qualifying assets)
2. The designation stack for the place
3. The existing collections for the place (to avoid duplication)
4. The illustrator's ULAN record and publication history
5. The place's current commerce tier

The curator makes one of four decisions:
- **Approve** → collection is created with `status: active`
- **Defer** → collection candidate held pending more assets (threshold raised)
- **Merge** → merge with an existing collection at the same place
- **Reject** → assets are Tier 2/3 only; no collection warranted

### 3.5 AI-Assisted Collection Copy Generation

When a collection candidate is approved, an AI model generates draft collection copy. This is strictly advisory — the draft is never published without curator review and approval.

**AI drafts:**
- Collection title (3 candidates)
- Collection introduction (300–500 words, 3 candidates)
- Curatorial statement (150 words, 3 candidates, first person for curator to adapt)
- Place description (200 words)
- Illustrator biography (150 words, sourced from ULAN + Wikidata)

**What AI never writes:**
- Signed curatorial statements (curator writes in their own voice)
- Rights determinations
- Certificate content
- Any text that will appear attributed to a named person without that person's review and approval

The AI draft is labeled `draft: true` in the CMS until the curator edits and approves it. The published version is labeled with the curator's name and approval date.

---

## Part IV — Product Generation

### 4.1 Automated Product Routing

Tier 1 IOs that pass Gate CP are automatically routed through the NC-PRODUCT-001 product routing constitution. The routing engine produces a `product_recommendation` record for each eligible product line.

```python
def route_to_products(io: IllustrationOpportunity) -> list[ProductRecommendation]:
    recommendations = []

    for product_line in APPROVED_PRODUCT_LINES:
        eligibility = check_eligibility(io, product_line)

        if eligibility.eligible:
            recommendations.append(ProductRecommendation(
                io_id=io.nc_id,
                product_line=product_line.id,
                routing_family=product_line.routing_family,
                csm_tier=io.csm_tier,
                curator_required=product_line.curator_always,
                confidence=eligibility.confidence,
                blocking_conditions=eligibility.conditions
            ))

    return sorted(recommendations, key=lambda r: r.confidence, reverse=True)
```

### 4.2 CE Edition Allocation at Scale

At 1M assets, CE allocation requires governance to prevent inflation. The CE system must remain scarce at scale — otherwise the edition architecture loses its value.

**CE allocation rules at 2,000 places:**

| Metric | Rule |
|---|---|
| Total active CE editions | Maximum 3 per active curator at any time |
| CE per illustrator | Maximum 5 open CE editions per illustrator across all collections |
| CE per place | Maximum 3 open CE editions per place at any time |
| CE per year | Maximum 20 new CE editions opened per calendar year |
| CE edition size | Always locked at Gate E; default 100; signature collections may request 25 or 50 |

**The scarcity principle from Rijksmuseum:** Rijksmuseum's limited editions maintain value because the museum controls the number. Getty's Open Content prints are not limited — they are open access. NC's CE editions are not Getty prints. The governance system that limits CE at scale is what makes the CE system meaningful at scale.

### 4.3 Product Generation Triggers

Products are never generated automatically. They are *recommended* automatically and *created* by a human after Gate CP + Gate E. The distinction is the entire trust architecture.

**Product recommendation trigger:**
- IO moves to `tier = 1`
- Gate CP completed by named curator
- `product_recommendation` records created by routing engine

**Product activation trigger:**
- Gate E: two named humans confirm
- `product` record created with `status: active`
- NC-ERS edition record created
- NC-COAS certificate record created

---

## Part V — Trust Preservation at Scale

### 5.1 The Scale Trust Problem

At pilot scale, every asset has been personally reviewed by the Founding Curator. At 1M assets, that is impossible. Trust at scale requires a different architecture: not manual review of everything, but systematic evidence of how decisions were made and by whom.

The trust model at 1M assets is:
- **Automated decisions are documented** (which algorithm, which data, which confidence score)
- **Human decisions are attributed** (which named person, at which gate, at what time)
- **Confidence scores are public** (the verify page shows whether a provenance link was automated or human-confirmed)
- **Uncertainty is disclosed** (a Tier 2 asset is not presented as a Tier 1 IO)

### 5.2 Confidence Scoring Model

Every field in an IO record carries a confidence score. The product page displays a composite confidence:

```python
class IllustrationOpportunityConfidence:
    ulan_confidence:     float   # How certain is the illustrator attribution?
    geonames_confidence: float   # How certain is the place association?
    rights_confidence:   float   # How certain is the rights determination?
    date_confidence:     float   # How certain is the date?
    image_confidence:    float   # How certain is this an illustration?

    @property
    def composite(self) -> float:
        # Rights is unconditional — any uncertainty reduces composite significantly
        if self.rights_confidence < 0.85:
            return 0.0  # not commerce-eligible with uncertain rights
        weights = {
            "ulan": 0.30,
            "geonames": 0.25,
            "rights": 0.30,
            "date": 0.10,
            "image": 0.05
        }
        return sum(
            getattr(self, f"{k}_confidence") * v
            for k, v in weights.items()
        )
```

**Public display:** The verify page (`/verify/[certificate]`) shows:

| Provenance link | Confidence | Method |
|---|---|---|
| Illustrator attribution | 97% | ULAN exact match |
| Place association | 91% | GeoNames lookup |
| Rights status | 100% | Institution CC0 confirmed |

A visitor can see that the place association was algorithmically determined (91%) while the rights status was institution-confirmed (100%). This is the Getty model: show the research, not just the conclusion.

### 5.3 Human Gate Audit Trail

Every human gate produces an immutable audit record:

```sql
CREATE TABLE gate_events (
  id              UUID PRIMARY KEY,
  gate_type       TEXT,         -- 'AR' / 'CS' / 'CP' / 'E'
  asset_id        UUID,         -- or collection_id, or product_id
  actor_name      TEXT,         -- named human (not role — name)
  actor_role      TEXT,
  decision        TEXT,         -- 'approved' / 'rejected' / 'deferred'
  decision_notes  TEXT,
  created_at      TIMESTAMPTZ
);
```

This table is append-only. No record may be updated or deleted. It is the institutional accountability layer.

### 5.4 Provenance Chain Integrity at Scale

The NC-PDPS 6-link chain must be maintained for every IO, not just for Earthrise. At 1M assets, the chain must be generated automatically where possible and flagged for human completion where not.

**Chain completeness by tier:**

| Link | Tier 1 (required) | Tier 2 (required) | Tier 3 (optional) |
|---|---|---|---|
| L1: Creator | ULAN resolved | Creator named | Raw string only |
| L2: Creation Event | Year + source confirmed | Year or range | Raw date string |
| L3: Custody History | Source institution + ROR | Institution named | — |
| L4: Rights Status | Full statutory text | RightsStatements.org URI | URI only |
| L5: Source Access | IIIF or URL confirmed | URL recorded | — |
| L6: Commercial Activation | Curator named + Gate E timestamp | — | — |

L6 (Commercial Activation) is the one link that is always human — it records who activated the product and when. This link cannot be generated automatically.

---

## Part VI — Rights Verification Engine

### 6.1 Design Principle

Rights classes 1–9 cover NC's existing institutions. At 1M assets from hundreds of sources, a general rights engine is required — one that can determine rights class for any asset without a pre-written institution-specific adapter.

The general engine is a decision tree that produces a rights class, a confidence score, and a human-review flag. It never makes a commercial activation decision — it informs the curator, who makes the decision.

### 6.2 Allowed URI Registry

The canonical list of rights URIs that are immediately ALLOWED (confidence 1.0, no human review required):

```python
ALLOWED_URIS = {
    # CC0 / PDM
    "http://creativecommons.org/publicdomain/zero/1.0/",
    "https://creativecommons.org/publicdomain/zero/1.0/",
    "http://creativecommons.org/publicdomain/mark/1.0/",
    "https://creativecommons.org/publicdomain/mark/1.0/",
    # NoC-US
    "http://rightsstatements.org/vocab/NoC-US/1.0/",
    "https://rightsstatements.org/vocab/NoC-US/1.0/",
    # Europeana-ratified
    "http://rightsstatements.org/vocab/NKC/1.0/",     # requires second-pass human
    "http://rightsstatements.org/vocab/NoC-OKLR/1.0/",# requires second-pass human
}

REVIEW_URIS = {
    "http://rightsstatements.org/vocab/NoC-CR/1.0/",
    "http://rightsstatements.org/vocab/NKC/1.0/",
    # CC BY variants — attribution obligation, commercially usable but not preferred
    "http://creativecommons.org/licenses/by/4.0/",
    "http://creativecommons.org/licenses/by/3.0/",
}

BLOCKED_URIS = {
    # All InC variants
    "http://rightsstatements.org/vocab/InC/1.0/",
    "http://rightsstatements.org/vocab/InC-EDU/1.0/",
    "http://rightsstatements.org/vocab/InC-NC/1.0/",
    "http://rightsstatements.org/vocab/InC-RUU/1.0/",
    "http://rightsstatements.org/vocab/InC-OW-EU/1.0/",
    # All CC-NC variants
    "http://creativecommons.org/licenses/by-nc/4.0/",
    "http://creativecommons.org/licenses/by-nc-sa/4.0/",
    "http://creativecommons.org/licenses/by-nc-nd/4.0/",
    # All CC-ND variants
    "http://creativecommons.org/licenses/by-nd/4.0/",
    # UND, CNE
    "http://rightsstatements.org/vocab/UND/1.0/",
    "http://rightsstatements.org/vocab/CNE/1.0/",
}
```

### 6.3 General Decision Tree

```
INPUT: asset record with {pub_date, creator_death_date, country, rights_uri, institution_rights_statement}

IF rights_uri IN BLOCKED_URIS:
    → BLOCKED, confidence=1.0

ELIF rights_uri IN ALLOWED_URIS:
    → ALLOWED, rights_class=map[rights_uri], confidence=1.0

ELIF rights_uri IN REVIEW_URIS:
    → REVIEW, confidence=0.50, human_review=True

# No URI — use date-based determination
ELIF pub_date IS NOT NULL AND pub_date.year < 1928 AND country == "US":
    # Hirtle chart: US publication before 1928 = public domain
    → ALLOWED, rights_class="NoC-US", confidence=0.95

ELIF creator_death_date IS NOT NULL AND (current_year - creator_death_date.year) > 100:
    # Life + 100 years (conservative — most jurisdictions)
    → ALLOWED, rights_class="life_plus_100", confidence=0.85

ELIF pub_date IS NOT NULL AND pub_date.year < 1800:
    # Pre-1800 — virtually all jurisdictions: PD
    → ALLOWED, rights_class="pre_1800_pd", confidence=0.90

ELIF pub_date IS NOT NULL AND pub_date.year < 1875 AND creator_death_date IS NULL:
    # 1800-1875, author death unknown — likely PD but not certain
    → REVIEW, confidence=0.65, human_review=True

ELSE:
    → BLOCKED (pending review), confidence=0.0, human_review=True
    # Cannot activate for commerce until human resolves
```

### 6.4 The Bridgeman Doctrine (applied at scale)

*Bridgeman Art Library v. Corel Corp. (1999)*: A photograph of a public-domain two-dimensional work of art lacks sufficient originality for copyright protection. Faithful reproductions of PD flat works are themselves PD.

At 1M assets, many source institution records are IIIF images of PD illustrations. The rights determination is on the *original illustration*, not on the IIIF image. If the original illustration is PD, the IIIF image of it is PD. This is the principle NC's entire rights architecture rests on.

**Application at scale:** When an institution supplies a IIIF image of an illustration where the *original* meets the date/life+100/CC0 criteria, the rights determination applies to the original. The IIIF image delivery is not a copyright barrier.

**Exception (Gallica disqualification precedent):** If an institution's terms of service impose a commercial license fee for reuse regardless of the underlying copyright status, the Bridgeman doctrine resolves copyright but not the contractual ToS barrier. Rights class determination is copyright; ToS is a separate gate. BnF/Gallica is the canonical case: EU Article 14 and Bridgeman both confirm PD, but BnF's ToS requires a license fee. The institution is blocked regardless of rights class. (DD-GALLICA-003)

---

## Part VII — AI Content Generation

### 7.1 The Model

NC-AI-001 established the governing principle: **Graph = truth. Models = advisory.** At 1M assets this principle becomes more important, not less.

The risk at scale is editorial collapse — the platform fills with AI-generated content that is technically accurate but lacks the voice, judgment, and accountability that make an institution trustworthy. The asset factory must scale without the editorial layer degrading.

The governance mechanism is a strict separation between what AI generates and what AI publishes. AI generates candidates. Humans publish.

### 7.2 What AI Does at 1M Scale

| Task | AI action | Human gate | Output state until approved |
|---|---|---|---|
| Illustration type classification | Classifies asset as IT-NAT, IT-ARCH, etc. | Gate CP confirmation | `ai_draft: true` |
| Illustrator name resolution | ULAN fuzzy match | Gate CP confirmation | `confidence: float` |
| Place name extraction | GeoNames lookup from text | Gate CP confirmation | `confidence: float` |
| Taxon name extraction | GBIF match from BHL/text | Gate CP confirmation | `confidence: float` |
| Collection title generation | 3 candidate titles | Curator selection + edit | `draft: true, published: false` |
| Collection introduction | 3 candidate drafts (300–500 words) | Curator review + edit + approval | `draft: true, published: false` |
| Illustrator biography | Draft from ULAN + Wikidata sources | Curator review + edit | `draft: true, published: false` |
| Place description | Draft from GeoNames + designation records | Curator review + edit | `draft: true, published: false` |
| Curatorial statement template | Structural prompt for curator to adapt | Curator writes own version | Discarded — not published |
| Rights class suggestion | Decision tree output | Human gate AR if REVIEW outcome | `confidence: float, human_review: bool` |
| Product routing | Recommendation record | Gate CP + Gate E | `recommendation: true, active: false` |

### 7.3 What AI Never Does

| Prohibited action | Reason |
|---|---|
| Publish editorial content without curator approval | Unnamed content is the trust failure the institution was built to avoid |
| Write signed curatorial statements | Named statements require the named person's authorship |
| Make rights determinations | Rights confidence score ≠ rights determination; human verdict is the gate |
| Activate a product (Gate E) | Constitutional invariant — always two humans |
| Write certificate content | NC-COAS requires named curator statement |
| Modify a human_verdict field | Gate records are immutable |
| Generate illustrator credentials it cannot verify | Hallucinated credentials are worse than no credentials |
| Use Qwen or DeepSeek models on non-local infrastructure | China jurisdiction rule (NC-AI-001) |

### 7.4 BHL Illustration Extraction — the AI-native pipeline

BHL is the largest single source for NC at scale. The BHL extraction pipeline is the most AI-intensive component of the Asset Factory — because most BHL records are text pages, not illustrations, and the illustration is embedded in a book-level record rather than being a standalone asset.

```
BHL API: search titles (date: 1750–1900, has_illustrations: true)
    ↓ ~50,000 illustrated titles
BHL API: get items (volumes, issues) per title
    ↓ page-level metadata for ~10M pages
FILTER: pages with known plate markers (BHL PageType = "Plate" or "Illustration")
    ↓ ~500,000 candidate illustration pages
Internet Archive: fetch page images (JPEG, via IA item URL)
    ↓
Image classifier: is this a plate or a text page?
    ├── YES (confidence > 0.80) → proceed
    └── NO / LOW → discard or Tier 4
    ↓
OCR caption extraction: parse caption beneath/above plate
    ├── extract illustrator name → ULAN lookup
    ├── extract species name → BHL name services → GBIF
    └── extract place reference → GeoNames
    ↓
Resolution check: BHL/IA JPEG quality
    ├── >= 6000px → R1 candidate
    ├── >= 3000px → R2 candidate
    └── < 3000px → R3 or Tier 3
    ↓
Rights assignment: all pre-1928 US publication → NoC-US (confidence 0.95)
Post-1927: check DPLA/HathiTrust for copyright renewal status
    ↓
IO candidate generation (if illustrator + place resolved)
    ↓
M36 write → graph integration → Gate CP queue
```

**BHL PageType filter:** BHL provides a `PageType` field per page. Values include "Plate", "Illustration", "Map", "Text". Filtering on `PageType IN ["Plate", "Illustration", "Map"]` reduces the page set from 60M to ~2M before image classification runs. This is a 30x efficiency gain.

**The BHL-GBIF bridge:** BHL's Name Usage service has already identified taxonomic names in 60M+ pages. For any page with a confirmed GBIF taxon match, NC inherits that match directly — no re-extraction needed. This makes BHL natural history illustrations the easiest IO candidates to generate at scale.

### 7.5 AI Model Selection by Task

Per NC-AI-001 governance:

| Task | Model family | Rationale |
|---|---|---|
| Illustration classification | CV model (local or cloud) | Visual task; no text generation risk |
| ULAN/GeoNames/GBIF resolution | Embedding + retrieval (local) | Structured lookup; no generation |
| Collection title candidates | Claude (Anthropic) | Creative, bounded, curator-reviewed |
| Collection introduction draft | Claude (Anthropic) | Long-form editorial, curator-reviewed |
| Illustrator biography draft | Claude (Anthropic) | Factual synthesis, curator-reviewed |
| OCR caption parsing | GPT-4o or Claude (parsing task) | Text extraction, high accuracy required |
| Rights class suggestion | Deterministic rules engine | No AI needed — use the decision tree |

---

## Part VIII — Discovery Graph Integration

### 8.1 Graph Scale Parameters at 1M Assets

| Entity | Count at pilot | Count at 1M assets | Node type |
|---|---|---|---|
| Assets | ~20 | 1,000,000 | `:Asset` |
| Places | 7 | 2,000 | `:Place` |
| Illustrators | 5 | ~5,000 | `:Illustrator` |
| Taxa | ~20 | ~80,000 | `:Taxon` |
| Collections | 6 | ~1,400 | `:Collection` |
| Source institutions | 3 | ~50 | `:Institution` |
| Editions | 2 | ~2,100 | `:Edition` |
| Products | 2 | ~40,000 | `:Product` |
| Designations | 5 | ~8,000 | `:Designation` |
| **Total nodes** | ~70 | **~1,130,000** | |
| **Total edges** | ~100 | **~15,000,000** | |

Neo4j handles billions of nodes; 15M edges is well within its operating range. The scale concern is not capacity but query design — traversals must be bounded.

### 8.2 Core Edge Types at Scale

| Edge | From → To | Count estimate | Indexed |
|---|---|---|---|
| `DEPICTS_PLACE` | Asset → Place | 3M | Yes |
| `DEPICTS_TAXON` | Asset → Taxon | 5M | Yes |
| `CREATED_BY` | Asset → Illustrator | 500K | Yes |
| `PART_OF` | Asset → Collection | 1.4M | Yes |
| `ANCHORED_TO` | Collection → Place | 3K | Yes |
| `HAS_DESIGNATION` | Place → Designation | 8K | Yes |
| `DERIVED_FROM` | Product → Asset | 40K | Yes |
| `SOURCED_FROM` | Asset → Institution | 1M | Yes |
| `DEPICTS_ERA` | Asset → TimeSpan | 1M | No (scan) |
| `RELATED_TO` | Asset → Asset | ~500K | Selective |

### 8.3 Discovery Query Patterns at Scale

Seven discovery journeys, each expressed as a bounded graph query:

```cypher
// Journey 1: Place → Illustrations (place page primary content)
MATCH (p:Place {geonamesId: $id})<-[:DEPICTS_PLACE]-(a:Asset)
WHERE a.tier IN [1, 2] AND a.dateYear BETWEEN 1750 AND 1900
RETURN a ORDER BY a.tier ASC, a.ulanConfidence DESC LIMIT 50

// Journey 2: Illustrator retrospective
MATCH (i:Illustrator {ulanId: $ulan})-[:CREATED]->(a:Asset)-[:DEPICTS_PLACE]->(p:Place)
WHERE a.tier = 1
RETURN a, p ORDER BY a.dateYear ASC LIMIT 100

// Journey 3: Designation cross-section
MATCH (p:Place)-[:HAS_DESIGNATION]->(d:Designation {type: 'UNESCO_BIOSPHERE'}),
      (p)<-[:DEPICTS_PLACE]-(a:Asset)-[:CREATED_BY]->(i:Illustrator)
WHERE a.tier = 1
RETURN p.name, i.name, count(a) as count
ORDER BY count DESC LIMIT 20

// Journey 4: Taxon across places
MATCH (t:Taxon {gbifKey: $key})<-[:DEPICTS_TAXON]-(a:Asset)-[:DEPICTS_PLACE]->(p:Place)
WHERE a.tier IN [1, 2]
RETURN a, p ORDER BY a.tier ASC LIMIT 30

// Journey 5: Date range expedition
MATCH (a:Asset)
WHERE a.dateYear BETWEEN $from AND $to
  AND a.illustrationType STARTS WITH 'IT-EXPD'
  AND a.tier = 1
MATCH (a)-[:DEPICTS_PLACE]->(p:Place)
RETURN a, p LIMIT 50

// Journey 6: ICH place cluster
MATCH (p:Place)-[:HAS_DESIGNATION]->(d:Designation {type: 'ICH'}),
      (p)<-[:DEPICTS_PLACE]-(a:Asset {illustrationType: 'IT-DOCU-ICH'})
WHERE a.tier IN [1, 2]
RETURN p.name, collect(a)[..6] as preview_assets

// Journey 7: Collection recommendation for subscriber
// (given subscriber's held editions, find related places/illustrators)
MATCH (e:Edition {subscriberId: $sub_id})-[:DERIVED_FROM]->(a:Asset)
MATCH (a)-[:DEPICTS_PLACE]->(p:Place)<-[:DEPICTS_PLACE]-(related:Asset)
WHERE NOT (related)-[:PART_OF]->(:Collection)
  AND related.tier = 1
RETURN related, p LIMIT 20
```

### 8.4 Collection Generation Triggers at Graph Scale

Beyond the Cypher trigger rules in Part III, the graph enables three additional collection types that are only possible at scale:

**Cross-place illustrator collection** (triggered when an illustrator has Tier 1 assets at 5+ places):
One collection for the illustrator across all their places. Example: Haeckel Collection — assets across Great Barrier Reef, Galapagos, Red Sea, Maldives.

**Designation-family collection** (triggered when 20+ places within a designation family have Tier 1 assets):
One meta-collection for a designation type. Example: UNESCO Biosphere Collection — the finest natural history illustrations from Biosphere Reserves worldwide.

**Era-and-expedition collection** (triggered by date cluster + expedition connection):
One collection for a specific expedition. Example: HMS Beagle Collection — all Darwin's Finches plates, Galápagos landscapes, Patagonian specimens from the 1831–1836 voyage.

---

## Part IX — BHL Institutional Governance

### 9.1 DD-BHL-001 Requirement

BHL is the largest single source for NC at 1M assets but has no governance document. This is the highest-priority institutional gap in the 1M architecture. Until DD-BHL-001 is ratified, BHL assets may not enter the commercial pipeline.

**DD-BHL-001 must address:**
1. BHL's legal status (501(c)(3) consortium; content is PD by selection policy)
2. Rights class for BHL assets (pre-1928 US publication → NoC-US; institutional confirmation required)
3. Internet Archive image delivery terms (IA's Open Content Alliance terms apply)
4. BHL PageType taxonomy as the illustration filter
5. BHL Name Usage service as the GBIF bridge
6. Attribution requirements (BHL standard citation format)
7. Resolution confirmation protocol (per-volume scan quality verification)
8. Pilot scope (suggested: 500 pages from 10 known high-quality illustrated volumes)
9. SA required: SA-BHL-001 (BHL Protocol and Rights Matrix v1)

**Estimated BHL contribution post-DD-BHL-001 ratification:**
- Phase 1 (Sprint 1): 5,000 pages from priority volumes (Haeckel, Audubon, Gould, Redouté)
- Phase 2 (Sprint 2): 50,000 pages from expanded volume set
- Phase 3 (Sprint 3): 500,000+ pages via automated pipeline

---

## Part X — Asset Factory Invariants

| # | Invariant | Rule |
|---|---|---|
| AF-1 | **Rights gate precedes all other processing** | No asset enters Stage 4 or beyond if Stage 3 = BLOCKED |
| AF-2 | **Confidence scores are public** | Every IO provenance link displays its confidence score and resolution method on the verify page |
| AF-3 | **Human verdicts are immutable** | `human_verdict` and `gate_events` records cannot be overwritten by the automated pipeline |
| AF-4 | **AI drafts are never published without human approval** | `draft: true` content cannot be displayed publicly |
| AF-5 | **Gate E is always two humans** | The product activation gate cannot be reduced, bypassed, or single-personned under any conditions |
| AF-6 | **CE allocation is governed at scale** | The CE allocation rules (max 3 per curator, max 5 per illustrator, max 3 per place) apply regardless of asset volume |
| AF-7 | **BHL requires DD-BHL-001 before commercial activation** | No BHL-sourced asset may be activated for commerce until DD-BHL-001 is ratified |
| AF-8 | **Bridgeman doctrine applies; ToS is a separate gate** | Rights class confirms copyright status. ToS must be separately confirmed for each institution. Gallica is the canonical blocked case. |
| AF-9 | **GBIF media is permanently prohibited** | DD-GBIF-001 disqualification applies at all scales. GBIF occurrence images may not enter the commercial pipeline. |
| AF-10 | **IFC-1 is unconditional** | At 1M assets, no exception path exists for non-PD/CC0 content regardless of volume or commercial potential |
| AF-11 | **Named curator required for L6** | The sixth link of the NC-PDPS chain (Commercial Activation) requires a named curator. Automated pipelines may fill links 1–5; link 6 is always human. |
| AF-12 | **Qwen + DeepSeek: local only** | China jurisdiction rule applies at all scales (NC-AI-001). |

---

## Part XI — Scale Roadmap

| Phase | Target | New assets | New IOs | Key action |
|---|---|---|---|---|
| **Pilot** (now) | 20 assets | — | 16 IOs | Gate E confirmed; Earthrise + 5 signature |
| **Sprint 1** | 5,000 | +4,980 | +300 | BHL Phase 1 (5K pages from priority volumes) after DD-BHL-001; Europeana pilot extended |
| **Sprint 2** | 50,000 | +45,000 | +3,000 | BHL Phase 2 (50K); NHM + Smithsonian activated; IIIF manifests live |
| **Sprint 3** | 200,000 | +150,000 | +15,000 | All current institutions at full ingestion; BHL Phase 3 begins |
| **Sprint 4** | 500,000 | +300,000 | +50,000 | BHL automated pipeline at full scale; DPLA two-tier activated |
| **Target** | 1,000,000 | +500,000 | +100,000 | Full institution set; IFC pipeline for next 10 institutions |

---

## Part XII — Reference Model Lessons Applied

**Europeana → EDM as the interoperability model.**
Europeana's Europeana Data Model is built on Dublin Core + CIDOC CRM and is the reason 50M records from 3,000 institutions interoperate. NC's CIDOC CRM layer is the equivalent: any institution that can speak CRM can contribute to NC without a custom adapter.

**Smithsonian Open Access → Bulk-first, API-second.**
The Smithsonian's GitHub CSV export is more reliable at scale than the API. Bulk download prevents rate-limit failures and allows reproducible ingestion. NC's AC-3 adapter (CSV bulk) follows this for NGA, Walters, and Smithsonian.

**Rijksmuseum → Quality over quantity in the commercial tier.**
Rijksmuseum has 1.1M objects but maintains a curated set of commercial products. Quantity in the database does not mean quantity in the shop. NC's asset tier model (Tier 1 commerce → Tier 4 reference) applies this principle: 1M assets in the database, ~100K commerce-ready.

**DPLA → Two-tier aggregation expands coverage without direct institution work.**
DPLA aggregates from hubs. NC's AC-9 adapter uses this to reach US state and regional institutions without individual DD documents for each one. The DPLA aggregator becomes a gateway to hundreds of smaller institutions.

**NHM → Dataset-level rights + precision filtering.**
NHM's Data Portal is CC BY on the dataset level — Rights Class 8. But NHM's Library/Archives are blocked (non-commercial government licence). The lesson: large institutions have mixed rights regimes, and precision filtering (which collection, not which institution) is required.

**BHL → Literature as an illustration source.**
BHL treats books as the unit of ingestion; NC treats illustrations as the unit of commerce. The BHL extraction pipeline is NC's contribution: the mechanism by which 60M text pages yield 500K+ commercial illustration candidates. This is the scale architecture no other platform has built.

---

## Open Actions

| # | Action | Priority | Blocking |
|---|---|---|---|
| OA-1 | **Draft DD-BHL-001** — BHL institutional governance | Critical | Sprint 1 BHL ingestion |
| OA-2 | **SA-BHL-001** — BHL Protocol and Rights Matrix v1 | Critical | Follows DD-BHL-001 |
| OA-3 | Build illustration type classifier (ML model, training data from NHM/NGA labeled set) | High | Stage 4 of pipeline |
| OA-4 | Build ULAN fuzzy lookup service (wrap ULAN API with caching layer) | High | Stage 6 |
| OA-5 | Extend M36 table with asset_tier, rights_confidence, ulan_id, geonames_id, gbif_taxon_key | High | Stage 7 |
| OA-6 | Build `gate_events` table (append-only audit log) | High | Trust preservation |
| OA-7 | Build collection_candidates table + trigger rule scheduler | Medium | Collection generation |
| OA-8 | Implement BHL Page API client (AC-8 adapter) | High | BHL ingestion (post DD-BHL-001) |
| OA-9 | Build rights verification engine (decision tree + ALLOWED/REVIEW/BLOCKED registries) | High | General rights at scale |
| OA-10 | Design AI content generation queue (draft → curator review → publish workflow) | Medium | Collection generation |
| OA-11 | Graph schema migration for 1M asset scale (indexes on DEPICTS_PLACE, CREATED_BY, DEPICTS_TAXON) | Medium | Graph at scale |
| OA-12 | DD-SMITHSONIAN-001 (Smithsonian Open Access governance) | High | Sprint 1 Smithsonian ingestion |

---

*NC-ASSETS-1000000 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
