# NC-IO-001: Illustration Opportunity Factory Blueprint

| Field | Value |
|---|---|
| Document | NC-IO-001 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | Illustration Opportunity Doctrine · NC-TAXON-001 · NC-ASSETS-1000000 · NC-COMMERCE-2000 · NC-GRAPH-002 · NC-AI-001 |
| Reference Models | BHL · NHM · Rijksmuseum · Smithsonian Open Access · Getty Museum |
| Scope | Complete specification of the Illustration Opportunity as NC's canonical commercial entity. Defines the IO schema, three IO types, five-dimension scoring model, tier assignment, readiness state machine, deduplication, and all trigger conditions for collection, product, discovery, and educational outputs. |

---

## Governing Doctrine

The `illustration_opportunities` table is the primary commercial entity in Nature & Culture.

**Taxa are metadata. Taxa are semantic anchors. Taxa are search handles.**

The pipeline is:
```
Place → Illustration Opportunity → Public-Domain Asset → Collection → Product
```

An IO is not a species record, not an asset file, not a rights statement. It is the resolved combination of all four: a named person's documented observation, rendered in a specific medium, of a subject associated with a specific place, confirmed to be in the public domain, and judged to have commercial and editorial value.

**The IO Factory has one job:** transform four inputs (Taxon, Place, Institution, Asset) into four outputs (Collection trigger, Story enrichment, Product record, Education Pack) with a documented, auditable score for every decision.

---

## 1. Three IO Types

Every IO is classified as one of three types before scoring begins. The type governs which anchors are required and which scoring formula applies.

| Type | Code | Description | Taxon Required | ULAN Required | Examples |
|---|---|---|---|---|---|
| Natural History | `NH` | Biological illustration: botanical, zoological, entomological, marine, fungal | Yes | Yes | Audubon birds, Haeckel radiolarians, Redouté roses, Nodder Endeavour plates |
| Cultural-Architectural | `CL` | Architectural drawing, decorative art, cultural documentary, landscape | No | Yes (preferred) | Owen Jones ornament, Bierstadt landscapes, Hokusai prints, Church Andean paintings |
| Cartographic | `CT` | Maps, charts, surveys, expedition routes | No | Optional | Hayden Survey 1871, NARA USGS maps, Cook voyage charts, Humboldt topographic |

**IO type is set at intake and is immutable.** It cannot be changed without a human gate review and a new IO record.

**Type classification rules:**
- If the primary depicted subject is a living organism → `NH`
- If the primary subject is architecture, landscape, decorative art, or cultural scene with no biological focus → `CL`
- If the primary subject is geographic representation (map, chart, survey) → `CT`
- If ambiguous (e.g., a botanical garden plan): default `CL`; add taxon data as supplementary

---

## 2. IO Schema

The `illustration_opportunities` table is the canonical record. All other systems (graph, product, commerce) derive from it.

```sql
illustration_opportunities (
  -- Identity
  id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug                    TEXT UNIQUE NOT NULL,          -- url-safe: nc-bhl-nh-00001
  io_type                 TEXT NOT NULL                  -- NH | CL | CT
    CHECK (io_type IN ('NH', 'CL', 'CT')),
  title                   TEXT NOT NULL,                 -- editorial title
  subtitle                TEXT,

  -- Biological anchor (NH only; nullable for CL/CT)
  gbif_taxon_key          INTEGER,
  gbif_canonical_name     TEXT,
  gbif_vernacular_name    TEXT,
  gbif_family             TEXT,
  gbif_kingdom            TEXT,
  gbif_confidence         NUMERIC(4,3),

  -- Geographic anchor
  geonames_id             BIGINT NOT NULL,
  place_slug              TEXT NOT NULL,
  pac_class               SMALLINT CHECK (pac_class BETWEEN 1 AND 5),
  place_relevance_score   NUMERIC(4,3),

  -- Creator anchor
  ulan_id                 TEXT,                          -- ULAN person ID
  ulan_confidence         NUMERIC(4,3),
  illustrator_name        TEXT,
  illustration_date       TEXT,                          -- year or range: "1827" / "1827–1838"
  illustration_date_year  SMALLINT,                      -- sort key: first year of range
  illustration_date_confidence NUMERIC(4,3),
  in_golden_age           BOOLEAN GENERATED ALWAYS AS   -- 1750 ≤ year ≤ 1900
    (illustration_date_year BETWEEN 1750 AND 1900) STORED,

  -- Institutional anchor
  source_institution_slug TEXT NOT NULL,
  source_record_id        TEXT,                          -- institution's own ID
  rights_class            SMALLINT,                      -- 1–10
  bhl_page_id             INTEGER,                       -- Rights Class 10
  bhl_member_tier         SMALLINT,                      -- 1–4 (BHL only)

  -- Rights
  rights_status           TEXT NOT NULL
    CHECK (rights_status IN ('ALLOWED', 'REVIEW_REQUIRED', 'BLOCKED')),
  rights_uri              TEXT,
  rights_confidence       NUMERIC(4,3) NOT NULL,
  rights_method           TEXT,

  -- Scoring (all NUMERIC 4,3 = 0.000–1.000)
  ia_score                NUMERIC(4,3),   -- Illustrator Authority
  rc_score                NUMERIC(4,3),   -- Rights Confidence
  ps_score                NUMERIC(4,3),   -- Place Specificity
  iq_score                NUMERIC(4,3),   -- Image Quality
  nd_score                NUMERIC(4,3),   -- Narrative Depth
  io_composite_score      NUMERIC(4,3),   -- weighted composite (formula by io_type)

  -- Tier
  asset_tier              TEXT
    CHECK (asset_tier IN ('Tier 1', 'Tier 2', 'Tier 3', 'Tier 4')),

  -- Readiness state
  io_status               TEXT NOT NULL DEFAULT 'CANDIDATE'
    CHECK (io_status IN (
      'CANDIDATE', 'RIGHTS_REVIEW', 'ANCHORING', 'STAGED',
      'APPROVED', 'COLLECTION_ASSIGNED', 'PUBLISHED',
      'DEACTIVATED', 'ARCHIVED'
    )),

  -- Asset
  image_url               TEXT,
  image_width_px          INTEGER,
  image_height_px         INTEGER,
  image_dpi               INTEGER,
  iiif_manifest_url       TEXT,

  -- Edition
  edition_type            TEXT CHECK (edition_type IN ('OE', 'CE')),
  edition_size            INTEGER,         -- NULL for OE; locked at creation for CE
  ce_series               TEXT,            -- CE series slug

  -- Collection assignment
  collection_slug         TEXT,

  -- Darwin Core (NH and some CL)
  darwin_core_json        JSONB,

  -- Curator
  curator_slug            TEXT,
  curator_statement       TEXT,

  -- Deduplication
  primary_io_id           UUID,            -- NULL = this IS the primary record
  duplicate_of            UUID,            -- set if this is a secondary source record

  -- Audit
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  staged_at               TIMESTAMPTZ,
  approved_at             TIMESTAMPTZ,
  published_at            TIMESTAMPTZ,
  deactivated_at          TIMESTAMPTZ
)
```

---

## 3. IO Scoring

### Dimension Definitions

Five dimensions, each scored 0.000–1.000:

**Dimension 1 — Illustrator Authority (IA)**
How significant is the illustrator to NC's commercial and editorial mission?

| Condition | IA Score |
|---|---|
| Priority illustrator (doctrine-defined 8: Audubon · Gould · Merian · Redouté · Lear · Nodder · Haeckel · Wolf) | **1.000** |
| Named illustrator in ULAN, working within 1750–1900 golden age | **0.750** |
| Named illustrator in ULAN, working outside golden age | **0.600** |
| Named illustrator, no ULAN ID but date confirmed 1750–1900 | **0.450** |
| Named illustrator, no ULAN, outside golden age | **0.350** |
| Illustrator identified only as institutional (e.g., "Kew Gardens draughtsman") | **0.250** |
| Anonymous, cartographic (authorship convention; `CT` type only) | **0.200** |
| Anonymous, no type attribution | **0.100** |

**Dimension 2 — Rights Confidence (RC)**
How certain is the PD/CC0 determination? RC is the gate dimension: if RC = 0.000, the IO is Tier 4 regardless of all other scores.

| Condition | RC Score |
|---|---|
| CC0 institution-wide (Smithsonian, Rijksmuseum, Walters, Getty CC0 program) | **1.000** |
| CC0 per-record confirmed (Met `openaccess=1`, NGA `openaccess=1`) | **0.970** |
| Pre-1928 US PD + BHL Tier 1 CC0 member library | **0.960** |
| PDM (Public Domain Mark) + confirmed contributing institution | **0.940** |
| Pre-1928 US PD + BHL Tier 2 CC BY member library | **0.880** |
| § 105 federal PD (NASA, NARA, NOAA) confirmed | **0.960** |
| NoC-US + date rule pre-1928 + non-BHL institution | **0.850** |
| Life+70 rule confirmed (non-US, date-verified) | **0.820** |
| REVIEW_REQUIRED (Europeana NoC-CR, BHL Tier 3, unclassified member) | **0.500** |
| BLOCKED (InC, CC NC, CC ND, ToS restriction like Gallica) | **0.000** |

**Dimension 3 — Place Specificity (PS)**
How precisely is the IO anchored to an NC place? (Mapped directly to NC-TAXON-001 PAC classes)

| PAC Class | PS Score |
|---|---|
| PAC-1 (Explicit: caption or plate title names the place) | **1.000** |
| PAC-2 (Biographical: illustrator documented at place in the period) | **0.800** |
| PAC-3 (Ecological: GBIF ≥3 occurrences within place boundary) | **0.650** |
| PAC-4 (Range: native range polygon intersects place) | **0.450** |
| PAC-5 (Editorial: curator decision) | **0.300** |
| No place association yet | **0.000** |

**Dimension 4 — Image Quality (IQ)**
Technical quality of the available image file.

| Condition | IQ Score |
|---|---|
| 600+ dpi original scan, full color, no visible damage | **1.000** |
| 300–600 dpi scan, good color accuracy, minor edge artifacts | **0.850** |
| 150–300 dpi scan, acceptable color, moderate age artifacts | **0.650** |
| 96–150 dpi screen-resolution, usable for digital but not print | **0.450** |
| Below 96 dpi or significant physical damage (tears, foxing, staining) | **0.250** |
| Insufficient (thumbnail only or visually corrupted) | **0.000** |

**Dimension 5 — Narrative Depth (ND)**
How much supporting editorial context exists for this IO? ND has low weight but distinguishes print-ready from editorially thin IOs.

| Condition | ND Score |
|---|---|
| Expedition documented + illustrator biography complete + place story published | **1.000** |
| Any two of the three above | **0.700** |
| Any one of the three above | **0.400** |
| None of the three above (blank editorial context) | **0.200** |

### Scoring Formulas by IO Type

**Natural History (NH):**
```
io_composite = (RC × 0.30) + (IA × 0.30) + (PS × 0.20) + (IQ × 0.15) + (ND × 0.05)
```

**Cultural-Architectural (CL):**
```
io_composite = (RC × 0.30) + (IA × 0.30) + (PS × 0.25) + (IQ × 0.15) + (ND × 0.00)
```
*(ND weight zero: CL narrative comes from the place story, not taxon biology. PS weight +0.05 compensates.)*

**Cartographic (CT):**
```
io_composite = (RC × 0.35) + (PS × 0.35) + (IQ × 0.25) + (IA × 0.05) + (ND × 0.00)
```
*(Maps: place content and rights dominate. Image quality critical for print. Illustrator is secondary.)*

---

## 4. IO Tier Assignment

Tier assignment uses hard gate rules evaluated in strict order. The first matching rule determines the tier; lower rules are not evaluated.

```
Rule 1 (BLOCK): IF rc_score = 0.000 → Tier 4
Rule 2 (BLOCK): IF iq_score < 0.250 → Tier 4
Rule 3 (BLOCK): IF io_composite < 0.300 → Tier 4

Rule 4 (TIER 1): IF
  rc_score ≥ 0.850
  AND ps_score ≥ 0.450     (PAC ≤ 3 confirmed)
  AND iq_score ≥ 0.600
  AND ulan_id IS NOT NULL  (named illustrator, except CT type)
  AND (
    io_composite ≥ 0.700
    OR (ia_score = 1.000 AND io_composite ≥ 0.650)  -- priority illustrator allowance
  )
  → Tier 1

Rule 5 (TIER 2): IF
  rc_score ≥ 0.750
  AND iq_score ≥ 0.600
  AND (ulan_id IS NOT NULL OR geonames_id IS NOT NULL)
  AND io_composite ≥ 0.500
  → Tier 2

Rule 6 (TIER 3): IF
  rc_score ≥ 0.750
  AND iq_score ≥ 0.300
  AND io_composite ≥ 0.300
  → Tier 3

Default → Tier 4
```

**Priority illustrator allowance (Rule 4):** An IO by Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel, or Wolf reaches Tier 1 at composite ≥ 0.650 rather than 0.700. The doctrine establishes these eight illustrators as having presumptive commercial value; the lower threshold reflects that. Rights and image quality gates remain unchanged.

**CT type exception for ULAN:** Cartographic IOs may reach Tier 1 without a confirmed ULAN ID if `geonames_id` is confirmed and all other Rule 4 conditions are met. Survey maps produced by federal agencies (NARA, USGS) have no individual illustrator and should not be penalized for this.

---

## 5. IO Readiness State Machine

Nine states, six transitions requiring automated logic, three transitions requiring human action:

```
CANDIDATE ──(auto: rights screen)──────→ RIGHTS_REVIEW
CANDIDATE ──(auto: rights clear)───────→ ANCHORING
RIGHTS_REVIEW ──(human: review passed)─→ ANCHORING
RIGHTS_REVIEW ──(human: review failed)─→ DEACTIVATED
ANCHORING ──(auto: anchors complete)───→ STAGED
STAGED ──(human: curator review)───────→ APPROVED
STAGED ──(human: curator reject)───────→ DEACTIVATED
APPROVED ──(auto: tier 1 + trigger)────→ COLLECTION_ASSIGNED
APPROVED ──(auto: tier 2–3)────────────→ PUBLISHED (editorial/discovery)
COLLECTION_ASSIGNED ──(Gate E/human)───→ PUBLISHED
PUBLISHED ──(rights retraction/auto)───→ DEACTIVATED
DEACTIVATED ──(curator restore)────────→ ANCHORING
PUBLISHED ──(long-term, curator)───────→ ARCHIVED
```

**State definitions:**

| State | Meaning | Human action possible |
|---|---|---|
| `CANDIDATE` | Asset identified; intake processing underway | No |
| `RIGHTS_REVIEW` | Rights screen returned REVIEW_REQUIRED; workflow item open | Yes — reviewer approves or rejects |
| `ANCHORING` | Rights cleared; ULAN + GeoNames resolution in progress | No (automated) |
| `STAGED` | All required anchors present; awaiting curator review | Yes — curator approves, rejects, or requests changes |
| `APPROVED` | Curator confirmed; eligible for collection and product triggers | No — triggers fire automatically |
| `COLLECTION_ASSIGNED` | Collection trigger fired; IO assigned to collection; pending publication gate | Yes — Gate E (for CE) or curator (for OE) |
| `PUBLISHED` | Live on NC site; collection and discovery active | Yes — curator may deactivate or archive |
| `DEACTIVATED` | Removed from public surfaces; record retained | Yes — curator may restore to ANCHORING |
| `ARCHIVED` | Permanently retained for audit; no longer publicly visible | No |

**SLA requirements:**

| Transition | Maximum time |
|---|---|
| CANDIDATE → RIGHTS_REVIEW or ANCHORING | 24 hours |
| RIGHTS_REVIEW → ANCHORING | 30 days (human SLA) |
| ANCHORING → STAGED | 72 hours (automated) |
| STAGED → APPROVED | 14 days (curator SLA) |
| rights retraction → DEACTIVATED | 5 minutes (priority 1 per NC-GRAPH-002) |

---

## 6. IO Deduplication

The same physical illustration may appear in two institutions (e.g., an Audubon plate held by both the Smithsonian and digitized by NYPL for BHL). CI-9 governs: flag, don't delete.

**Deduplication key:**

For `NH` type:
```
dedup_key = hash(ulan_id || ':' || illustration_date_year || ':' || gbif_taxon_key)
```

For `CL` type:
```
dedup_key = hash(ulan_id || ':' || illustration_date_year || ':' || title_normalized)
```

For `CT` type:
```
dedup_key = hash(geonames_id || ':' || illustration_date_year || ':' || title_normalized)
```

**Deduplication resolution:**
When two records share a `dedup_key`:
1. The record with the higher `io_composite_score` becomes primary (`primary_io_id = NULL`)
2. The lower-scoring record is marked `duplicate_of = primary_io_id`
3. Both records are retained in the database
4. Only the primary record is visible to the product and discovery pipelines
5. A human can reverse the designation (curator gate) if the lower-scoring record has a specific editorial reason for priority (e.g., the duplicate has higher-resolution image)

If the two records have identical composite scores, prefer: CC0 institution-wide > CC0 per-record > pre-1928 + Tier 1 BHL > all others.

---

## 7. IO Nomenclature

NC-internal IO identifiers follow a canonical format. This scheme is applied to all IOs created after DD-BHL-001 activation. Existing pilot IO identifiers (NC-NASA-002, BHL-GOULD-FINCHES, etc.) from NC-COMMERCE-001 are grandfathered and do not change.

```
{SOURCE_CODE}-{TYPE}-{SEQ5}

SOURCE_CODE:  institution code (UPPER, max 12 chars)
              BHL, SMITHSONIAN, RIJKS, NHM, MET, NGA, NARA, NOAA, NASA,
              WALTERS, YALE, GETTY, CMA, SMK, AIC, NATURALIS, NYBG, ...

TYPE:         NH | CL | CT

SEQ5:         5-digit zero-padded sequence per source+type combination
              BHL-NH-00001, BHL-NH-00002, ..., BHL-NH-99999

Full example: NC-BHL-NH-00001
              NC-RIJKS-CL-00001
              NC-NARA-CT-00001
```

**slug** (URL-safe):
```
nc-bhl-nh-00001
nc-rijks-cl-00001
```

**The `NC-` prefix is always present** in the slug; it is dropped in the short internal identifier (BHL-NH-00001) for readability in lists and logs.

---

## 8. Collection Triggers

Six triggers, extending NC-TAXON-001's T1–T4 with two non-biological types:

| ID | Name | Condition | Result |
|---|---|---|---|
| **T1** | Illustrator-Family | `IA ≥ 0.750` AND `io_type = NH` AND same `gbif_family`, count ≥ 3 Tier 1 IOs | Priority illustrator family collection candidate |
| **T2** | Place-Ecology | `pac_class ≤ 3` AND same `place_slug`, count ≥ 5 IOs (Tier 1 or 2) | Place natural history series candidate |
| **T3** | Designation-Endemic | `endemism_score ≥ 0.80` AND `designation = D`, count ≥ 3 taxa | Designation endemic series candidate |
| **T4** | Family-Atlas | `io_type = NH` AND same `gbif_family`, count ≥ 10 Tier 1 IOs AND distinct illustrators ≥ 2 | Family atlas candidate |
| **T5** | Cultural-Place | `io_type = CL` AND same `place_slug`, count ≥ 3 Tier 1 IOs AND distinct `ulan_id` ≥ 1 | Place cultural heritage collection |
| **T6** | Expedition-Thread | same `expedition_slug`, count ≥ 5 IOs AND distinct `place_slug` ≥ 2 | Expedition natural history / cultural collection |

**Trigger priority scoring:**

When multiple triggers fire from the same IO batch, collection candidates are ranked:

```
collection_priority =
  (T1_or_T6 ? 1.0 : 0.6)                      * 0.30  -- Illustrator/Expedition > Place > Family
  + (illustrator_in_priority_8 ? 1.0 : 0.5)    * 0.25
  + (all_ios_tier_1 ? 1.0 : 0.7)               * 0.20
  + (designation_depth_score)                   * 0.15  -- WH=1.0, Biosphere=0.8, Geopark=0.6
  + (nc_place_page_published ? 1.0 : 0.3)       * 0.10
```

**No collection advances past CANDIDATE without curator review.** Trigger fires open a queue item. The curator confirms, modifies, or rejects the candidate. Collection goes live only after a human approval gate.

---

## 9. Product Triggers

### Product Trigger Matrix

Minimum dimension scores required for each product family. All require `rights_status = ALLOWED`:

| Family | Product Type | RC | IA | PS | IQ | Additional Requirements |
|---|---|---|---|---|---|---|
| **A** | Museum Giclée (archival print) | 0.97 | 0.75 | 0.45 | 0.90 | Specialist studio order; curator + PA review; edition_size locked |
| **B** | Wall Art (framed/canvas/poster) | 0.85 | 0.40 | 0.45 | 0.60 | Gelato routing confirmed |
| **C** | Educational Context Card | 0.75 | any | any | 0.30 | Free (EDU-0); gbif_taxon_key for NH type |
| **C+** | Curriculum Module (EDU-1–4) | 0.85 | 0.40 | 0.45 | 0.60 | darwin_core_json complete for NH |
| **D** | Book / Monograph | 0.85 | 0.40 | 0.45 | 0.60 | Collection ≥ 5 Tier 1 IOs; distinct places ≥ 2 |
| **E** | Paper Goods (cards, stationery) | 0.85 | 0.40 | 0.45 | 0.60 | — |
| **F** | Digital Study Edition (DDS) | 0.85 | 0.40 | any | 0.60 | — |
| **F+** | Digital Research Edition (DDR) | 0.95 | 0.60 | 0.45 | 0.80 | darwin_core_json complete |
| **G** | Collector Edition (CE) | 0.95 | 0.75 | 0.65 | 0.80 | CE Allocation available; curator signature |
| **H** | Subscription (Explorer/Collector) | (any Tier 1 IO in collection) | — | — | — | S1/S2/S3 activation |

**CE Allocation Register** is checked before any Family G trigger fires (see §10 below).

**Federal nonendorsement check (all products with NASA/NARA/NOAA source):**
Before any product trigger finalizes, the prohibited phrases validator (NC-AI-001 C-5) must confirm the product copy contains no language implying government endorsement. This check is mandatory and cannot be bypassed.

### CE Allocation Register

The CE Allocation Register governs edition scarcity at scale. It is an append-only ledger; entries are never modified.

**Maximum active CE editions at any time:**

| Constraint | Limit |
|---|---|
| Per curator | 3 active CE editions simultaneously |
| Per illustrator | 5 active CE editions simultaneously |
| Per place | 3 active CE editions simultaneously |
| New CE editions per calendar year | 20 |

**"Active" definition:** A CE edition is active from its publication date until the edition is sold out AND all physical prints have been delivered. An edition is not "inactive" merely because it is sold out; it remains active until delivery is complete.

**CE Allocation check logic:**
```
BEFORE triggering Family G:
  curator_active = COUNT(ce_editions WHERE curator_slug = X AND status = 'active')
  illustrator_active = COUNT(ce_editions WHERE ulan_id = Y AND status = 'active')
  place_active = COUNT(ce_editions WHERE place_slug = Z AND status = 'active')
  annual_new = COUNT(ce_editions WHERE year(published_at) = CURRENT_YEAR)

  IF curator_active ≥ 3 → BLOCK
  IF illustrator_active ≥ 5 → BLOCK
  IF place_active ≥ 3 → BLOCK
  IF annual_new ≥ 20 → BLOCK
  ELSE → CE trigger proceeds to curator review queue
```

**CE edition size:** Must be declared at time of curator approval and is **immutable once published.** No retrospective edition size changes. No "we'll expand it later." The Internet Archive deposit confirms the historical scarcity claim (per NC-ERS standard).

---

## 10. Discovery Triggers

Seven discovery triggers, mapped to NC-GRAPH-002's seven discovery journeys. Each trigger fires when an IO is published and activates the corresponding graph edge.

**T-DISC-1: Place Grid Activation**
```
On IO published:
  MERGE (io)-[:DISPLAYED_IN]->(place)
  Increment place.io_count
  If place.io_count == 1: fire PLACE_PAGE_SEEDABLE notification
  If place.io_count == 5: fire PLACE_PAGE_PUBLISHABLE notification
  If place.io_count == 20: fire PLACE_PAGE_FEATURED notification
```

**T-DISC-2: Illustration Connected (Related IOs)**
```
On IO published:
  Find all published IOs WHERE:
    same illustrator (ulan_id) → edge strength: HIGH
    same place (place_slug) → edge strength: HIGH
    same taxon family (gbif_family) → edge strength: MEDIUM
    same period (within 25 years) → edge strength: LOW
  MERGE (io)-[:RELATED_TO {strength}]->(related_io)
  (bidirectional: also MERGE (related_io)-[:RELATED_TO]->(io))
```

**T-DISC-3: Artist Radio**
```
On IO published:
  Increment artist.io_count WHERE ulan_id = this.ulan_id
  If artist.io_count == 3:  fire ARTIST_RADIO_ENABLED notification (minimum for journey)
  If artist.io_count == 10: fire ARTIST_FEATURED notification
```

**T-DISC-4: Nearby Places (PostGIS)**
```
On place_page published (driven by T-DISC-1):
  PostGIS spatial query: places within 500km of this place centroid
  → MERGE (place)-[:NEAR]->(neighbour_place) for top 5 by distance
  → Journey: "Other places nearby" sidebar
```

**T-DISC-5: Expedition Thread**
```
On IO published WHERE expedition_slug IS NOT NULL:
  MERGE (io)-[:PART_OF]->(expedition)
  If expedition.io_count ≥ 5 AND expedition.distinct_places ≥ 2:
    fire EXPEDITION_THREAD_ACTIVE notification
    → Journey: "Follow the expedition route"
```

**T-DISC-6: Topic Bridge**
```
On IO published:
  Assign topic nodes from gbif_kingdom, gbif_class, designation_type, io_type
  MERGE (io)-[:TAGGED_WITH]->(topic) for each assigned topic
  → Journey: "More from [Botanical Illustration / Dutch Golden Age / UNESCO World Heritage]"
```

**T-DISC-7: Knowledge Panel (Schema.org)**
```
On IO published:
  Generate Schema.org JSON-LD:
    @type: CreativeWork (NH/CL) OR Map (CT)
    name: io.title
    creator: {name: illustrator_name, url: nc.art/illustrators/{ulan_id}}
    about: {name: gbif_canonical_name, taxonKey: gbif_taxon_key} (NH only)
    locationCreated: {name: place_name, geonamesId: geonames_id}
    license: rights_uri
    dateCreated: illustration_date
    isPartOf: {url: nc.art/collections/{collection_slug}}
  → Published in page <head> for SEO and Google Knowledge Graph
```

---

## 11. Story Output

Every published IO enriches three story objects in NC-GRAPH-002:

**Place Story enrichment:**
When an IO is published for a place, the place's editorial narrative gains:
- A new illustration context entry: "{illustrator_name} depicted {gbif_vernacular_name or title} at {place_name} in {illustration_date}"
- If ND ≥ 0.70: the expedition or biographical narrative becomes available for the place story module
- AI may draft the editorial copy (NC-AI-001 category: "place story") under human review

**Illustrator Story enrichment:**
When an IO is published for an illustrator:
- The illustrator's NC profile gains a new work entry
- If artist.io_count reaches 3, 10, 20: the illustrator profile is promoted to a new prominence tier

**Expedition Story enrichment:**
When ≥5 IOs in the same expedition are published:
- Expedition timeline becomes available as a standalone editorial object
- Places visited by the expedition become linked in geographic sequence
- The expedition story is usable as a collection editorial introduction

---

## 12. Education Pack Output

The IO Factory generates four education outputs, triggered at different readiness states:

| Output | Trigger | Contents | Product Tier |
|---|---|---|---|
| **Species Context Card** | IO published (NH, any tier) | gbif_vernacular_name + illustrator + place + 3 sentences | EDU-0 (free) |
| **Illustrator Context Module** | IO approved (any type, Tier 1/2) | Illustrator biography + this IO's narrative context + 3 discussion prompts | EDU-1 (£12–18) |
| **Expedition Module** | Expedition trigger T-DISC-5 fires (≥5 IOs) | Timeline + 5 species or cultural modules + teaching guide PDF | EDU-2 (£45–65) |
| **Darwin Core Research Pack** | IO published (NH, Tier 1, darwin_core_json complete) | Full Darwin Core XML/JSON + IIIF manifest + provenance chain | EDU-4 / S3 Institutional |

**AI content governance for education outputs (NC-AI-001):**
- AI may draft: context card body text, discussion prompts, expedition summary
- AI may not write: attribution strings, rights statements, Darwin Core field values, scientific name determinations (AI-ATT-1 permanent)
- All AI-drafted educational copy requires human review before any product activation

---

## 13. Factory Pipeline (End-to-End)

```
INTAKE
  └─ Asset enters from Asset Factory (Stage 8: Product Routing)
  └─ io_type assigned from asset classification
  └─ io_status = CANDIDATE

RIGHTS SCREEN (Stage 1)
  └─ rights_screen(source_institution_slug, rights_class, raw_rights_metadata)
  └─ rc_score assigned
  └─ If REVIEW_REQUIRED: io_status = RIGHTS_REVIEW, workflow item opened
  └─ If BLOCKED: io_status = DEACTIVATED
  └─ If ALLOWED: continue to Anchoring

ANCHOR RESOLUTION (Stage 2)
  └─ io_status = ANCHORING
  └─ Run in parallel:
       ULAN resolution → ia_score
       GBIF resolution (NH only) → gbif_taxon_key (from NC-TAXON-001 factory)
       GeoNames resolution → geonames_id + pac_class + ps_score
       Image quality assessment → iq_score
       Date validation → illustration_date_year, in_golden_age
  └─ nd_score calculated from existing editorial context

SCORING (Stage 3)
  └─ io_composite_score = formula(io_type, ia, rc, ps, iq, nd)
  └─ asset_tier = tier_assignment_rules(all dimension scores)

DEDUPLICATION CHECK (Stage 4)
  └─ dedup_key generated
  └─ Check against existing records
  └─ If duplicate: flag, set duplicate_of, do not advance primary

STAGED (Stage 5)
  └─ io_status = STAGED
  └─ Curator queue item opened with full score breakdown
  └─ SLA: 14 days

CURATOR REVIEW (Stage 6) [HUMAN GATE]
  └─ Curator reviews: tier, place association, illustrator identity, rights confidence
  └─ Curator may: approve, reject, or request score adjustment
  └─ If approved: io_status = APPROVED
  └─ curator_slug recorded

TRIGGER EVALUATION (Stage 7)
  └─ Evaluate collection triggers T1–T6
  └─ If trigger fires: io_status = COLLECTION_ASSIGNED, collection candidate created
  └─ Evaluate product triggers (product trigger matrix)
  └─ CE check (CE Allocation Register query)
  └─ Evaluate discovery triggers T-DISC-1 through T-DISC-7

PUBLICATION GATE (Stage 8) [HUMAN GATE for CE; automated for OE Tier 1]
  └─ CE: Gate E — two named humans, never automated
  └─ OE Tier 1: curator approval sufficient (from Stage 6)
  └─ OE Tier 2–3: auto-publish on APPROVED status
  └─ io_status = PUBLISHED on confirmation

GRAPH SYNC (Stage 9)
  └─ PostgreSQL trigger → nc_graph_change_queue
  └─ projection_worker → Neo4j node upsert + all edges
  └─ Rights retraction wire: if io_status → DEACTIVATED, remove from graph < 5 min
```

---

## 14. Governance Invariants

| # | Invariant |
|---|---|
| IO-1 | The `illustration_opportunities` table is the canonical commercial entity. No product, collection, or story may exist without an associated IO record. |
| IO-2 | IO type (`io_type`) is set at intake and is immutable. Type change requires a human gate review and a new record. |
| IO-3 | RC = 0.000 (BLOCKED) produces Tier 4 unconditionally. No other dimension score can override a blocked rights status. (IFC-1) |
| IO-4 | CE edition size is declared at curator approval and locked immediately on publication. Retrospective edition expansion is permanently prohibited. |
| IO-5 | The CE Allocation Register is an append-only ledger. No entry may be modified or deleted. Constraints (3/curator, 5/illustrator, 3/place, 20/year) are unconditional. |
| IO-6 | Gate E (CE publication) is always two named humans. Never automated. Never single-person. Never delegated to an AI output. (IFC-2) |
| IO-7 | Darwin Core field values are retrieved from authoritative sources (GBIF, BHL, ULAN, GeoNames). AI may draft surrounding educational copy; AI never writes Darwin Core values. (AI-ATT-1) |
| IO-8 | Deduplication: when two records share a dedup_key, the lower-scoring record is flagged and retained — never deleted. (CI-9) |
| IO-9 | The deduplication key uses `gbif_taxon_key` (not `gbif_canonical_name`) because synonym resolution may change the name but not the taxon key. Keys are stable; names are not. |
| IO-10 | GBIF occurrence count is capped at 100 in the PS scoring formula. Raw occurrence count is never used anywhere. (CI Constitution) |
| IO-11 | PAC-4 (range) and PAC-5 (editorial) place associations produce Tier 2 maximum. No CE product may be triggered from an IO whose only place association is PAC-4 or PAC-5. |
| IO-12 | The prohibited phrases validator (NC-AI-001 C-5) runs on all product copy before any product trigger finalizes. Federal nonendorsement and false provenance phrases are unconditional blocks. |
| IO-13 | Rights retraction SLA: 5 minutes from rights_status → BLOCKED to io_status → DEACTIVATED and removal from Neo4j graph. This is a priority-1 operation, not a batch job. |
| IO-14 | Pilot IOs (NC-PROD-001 through NC-PROD-010 from NC-COMMERCE-001) are grandfathered. Their identifiers do not change to the new nomenclature scheme. |

---

## 15. Open Actions

| # | Action | Priority | Depends On |
|---|---|---|---|
| OA-1 | Implement IO scoring engine (5 dimensions × 3 formulas) | HIGH | — |
| OA-2 | Implement tier assignment logic (hard rules §4) | HIGH | OA-1 |
| OA-3 | Implement IO readiness state machine + SLA tracking | HIGH | — |
| OA-4 | Implement CE Allocation Register as append-only table | HIGH | — |
| OA-5 | Implement deduplication key generation and matching | HIGH | — |
| OA-6 | Implement collection trigger evaluation (T1–T6) as post-publish hook | MEDIUM | NC-GRAPH-002 live |
| OA-7 | Implement product trigger matrix as per-family activation checklist | MEDIUM | OA-1 + OA-2 |
| OA-8 | Implement discovery triggers T-DISC-1 through T-DISC-7 as graph edge writers | MEDIUM | NC-GRAPH-002 live |
| OA-9 | Implement Schema.org JSON-LD generator for Knowledge Panel (T-DISC-7) | MEDIUM | — |
| OA-10 | Curator queue UI: score breakdown, tier justification, APPROVE / REJECT / ADJUST actions | HIGH | OA-1 + OA-2 + OA-3 |
| OA-11 | Add `io_type`, `ia_score`, `rc_score`, `ps_score`, `iq_score`, `nd_score`, `io_composite_score`, `io_status`, `edition_type`, `ce_series` columns to M36 migration | HIGH | NC-ASSETS-1000000 M36 |
| OA-12 | Prohibited phrases validator integration (NC-AI-001 C-5) on product trigger finalization | HIGH | NC-AI-001 C-5 |
| OA-13 | Education pack generation pipeline (Species Context Card EDU-0 as first output) | MEDIUM | IO_PUBLISHED event |
| OA-14 | darwin_core_json serializer and `nc:` namespace registration at `nc.art/data/terms/` | MEDIUM | NC-TAXON-001 OA-7 |

---

*NC-IO-001 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
*Priority ratification dependencies: NC-TAXON-001 · NC-ASSETS-1000000 · NC-GRAPH-002 · DD-BHL-001 · NC-AI-001 (C-5)*
