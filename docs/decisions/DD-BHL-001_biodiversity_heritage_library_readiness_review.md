# DD-BHL-001: Biodiversity Heritage Library — Readiness Review

| Field | Value |
|---|---|
| Document | DD-BHL-001 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Institution | Biodiversity Heritage Library (BHL) |
| Candidate rank | **#1 of 100** (NC-INSTITUTIONS-100) |
| Stage | Stage 2 — Governance (Institution Factory v1) |
| Authority | Institution Factory Constitution v1 · AF-8 (ToS separation) · Rights Class definitions · NC-ASSETS-1000000 · NC-PDPS |
| Reference Models | Europeana (DD-EUR-001) · Smithsonian Open Access · NHM London (DD-NHM-001) · GBIF Authority Standard (DD-GBIF-001) |

---

## Verdict

**APPROVE WITH CONDITIONS**

BHL is Nature & Culture's single most important institution. It holds all eight NC priority illustrators, provides a direct GBIF taxon bridge, and makes 60M+ pre-1928 public domain pages accessible under a documented license framework. No other institution comes close to BHL's combination of volume, illustrator depth, and taxonomic integration.

Activation is blocked on three conditions that must be resolved before any asset enters the commercial pipeline:

1. **SA-BHL-001 ratified** — BHL Protocol, Rights Matrix v1, and Member Library Tier Classification
2. **Member Library Tier Classification confirmed** for the 25 highest-volume BHL contributors
3. **Pilot completed** — 50 assets, Tier 1 member libraries only, 90 days, Sprint Compliance COMPLIANT

---

## 1. Institution Profile

**What BHL is:**
BHL is a consortium of ~100 member libraries (natural history museums, botanical gardens, universities) that have pooled their digitized natural history collections into a single open platform. As of 2026, BHL hosts approximately 60 million pages from ~250,000 volumes covering natural history literature from the 15th century onward.

**What BHL is not:**
BHL is not a single institution with a single rights policy. It is an aggregator. Each page traces back to a contributing member library whose rights assertion governs that item. BHL's platform license is a summary of the member library's assertion — not an independent grant.

**Why BHL is #1:**

| Factor | Detail |
|---|---|
| Priority illustrators | All 8: Audubon · Gould · Merian · Redouté · Lear · Nodder · Haeckel · Wolf |
| Volume | 60M pages → ~500K+ qualifying illustration candidates after PageType filter |
| Rights clarity | Majority pre-1928 = US public domain by date rule; many CC0 or CC BY contributions |
| Taxonomic integration | BHL Name Usage service provides GBIF taxon keys extracted from OCR — NC inherits directly |
| Collection coverage | All 7 NC discovery journeys (natural history, botanical, expedition, architectural, cultural, geographic, heritage) |
| Adapter class | AC-8 (BHL Page API) already classified in NC-ASSETS-1000000 |

---

## 2. Rights Architecture

### The Core Problem

BHL aggregates rights from ~100 member libraries. For NC, this means two independent gates must pass before any BHL illustration can enter the commercial pipeline:

- **Gate 1 — Copyright**: Is the underlying work in the public domain? (pre-1928 date rule, life+70 rule, or explicit CC0/CC BY)
- **Gate 2 — ToS**: Does the contributing member library's ToS permit commercial reuse of its digital file?

These gates are independent. AF-8 (Bridgeman + ToS separation) is the governing invariant. The Gallica precedent applies: BnF asserted PD content but imposed a commercial license fee via ToS. Any BHL member library could do the same.

The Bridgeman doctrine resolves Gate 1 for slavish scans: digitization of a flat 2D work creates no new copyright in the US. But Gate 2 (ToS) cannot be resolved by Bridgeman. It requires per-member-library review.

### Rights Class 10: Hierarchical Aggregate Rights

BHL is assigned **Rights Class 10**, a new classification requiring two inputs to produce a rights decision:

```
Input 1: BHL item-level license string
  → bhl_item.License (e.g., "CC BY 4.0", "CC0 1.0", "Not in Copyright", "Public Domain")
  → bhl_item.LicenseUrl (URI form)

Input 2: Contributing member library Tier Classification
  → bhl_source_institution_slug (derived from bhl_item.HoldingInstitution)
  → member_library_tier (BHL_TIER_1 / BHL_TIER_2 / BHL_TIER_3 / BHL_TIER_4)

Rights decision:
  IF bhl_member_tier = BHL_TIER_1 (CC0) AND date_rule = pre_1928 → ALLOWED (confidence: 0.97)
  IF bhl_member_tier = BHL_TIER_1 (CC0) AND license = CC0 → ALLOWED (confidence: 0.97)
  IF bhl_member_tier = BHL_TIER_2 (CC BY) AND date_rule = pre_1928 → ALLOWED_ATTRIBUTION (confidence: 0.93)
  IF bhl_member_tier = BHL_TIER_3 AND date_rule = pre_1928 → REVIEW_REQUIRED (confidence: 0.75)
  IF bhl_member_tier = BHL_TIER_4 → BLOCKED (confidence: 1.00)
  IF bhl_member_tier = UNCLASSIFIED → REVIEW_REQUIRED (confidence: 0.50)
```

### BHL Rights Matrix v1

| BHL License String | Member Tier | Date Rule | NC Decision | Confidence |
|---|---|---|---|---|
| `CC0 1.0` | Tier 1 | any | ALLOWED | 0.97 |
| `Public Domain` | Tier 1 | pre-1928 | ALLOWED | 0.97 |
| `Not in Copyright` | Tier 1 | pre-1928 | ALLOWED | 0.95 |
| `CC BY 4.0` / `CC BY 3.0` | Tier 2 | any | ALLOWED_ATTRIBUTION | 0.93 |
| `Not in Copyright` | Tier 3 | pre-1928 | REVIEW_REQUIRED | 0.75 |
| `Public Domain` | Tier 3 | pre-1928 | REVIEW_REQUIRED | 0.72 |
| `Public Domain` | UNCLASSIFIED | pre-1928 | REVIEW_REQUIRED | 0.50 |
| Any InC / CC NC / CC ND | any | any | BLOCKED | 1.00 |
| `In Copyright` | any | any | BLOCKED | 1.00 |
| `Undetermined` | any | any | REVIEW_REQUIRED | 0.30 |

**SA-BHL-001 is required to encode this matrix in rights.py.**

### BHL Member Library Tier Classification v1

Four tiers, based on their rights assertions and confirmed ToS status:

**BHL Tier 1 — CC0 confirmed, commercial use permitted:**

| Institution | BHL Holding Slug | Confirmed Via |
|---|---|---|
| Smithsonian Institution Libraries | `smithsonian` | DD-SMITHSONIAN-001 (pending) |
| NHM London (Data Portal) | `nhm-london` | DD-NHM-001 |
| New York Botanical Garden | `nybg` | DD-NYBG-001 (pending) |
| Missouri Botanical Garden | `mobot` | DD-MBG-001 (pending) |
| California Academy of Sciences | `calacad` | DD-CALACAD-001 (pending) |
| Biodiversity Heritage Library (platform CC0) | `bhl-platform` | BHL open data policy |

**BHL Tier 2 — CC BY confirmed, attribution required, commercial use permitted:**

| Institution | BHL Holding Slug | Confirmed Via |
|---|---|---|
| Wellcome Collection | `wellcome` | DD-WELLCOME-001 (pending) |
| Harvard MCZ / MCZ Library | `harvard-mcz` | DD-HARVARD-001 (pending) |

**BHL Tier 3 — Pre-1928 PD applies, ToS requires confirmation (REVIEW_REQUIRED in pilot):**

| Institution | Notes |
|---|---|
| Royal Botanic Gardens Kew | DD-KEW-001 pending |
| Natural History Museum Vienna | DD-NHM-WIEN pending |
| New York Public Library (older contributions) | Some BHL holdings predate NYPL CC0 policy |
| University of Toronto | Canadian institution; separate ToS audit needed |
| Staatsbibliothek Berlin | German institution; see BSB digitization ToS |

**BHL Tier 4 — BLOCKED pending explicit license:**

| Institution | Disqualification Reason |
|---|---|
| Bibliothèque nationale de France | DD-GALLICA-003: ToS requires commercial license fee |
| Any institution whose ToS explicitly prohibits commercial reuse | Per AF-8 |

**UNCLASSIFIED:** All other BHL member libraries. These institutions' content is REVIEW_REQUIRED until their DD is drafted and their Tier confirmed.

---

## 3. Technical Architecture

### AC-8: BHL Page API Adapter

BHL exposes a documented REST API at `api.biodiversitylibrary.org`. The NC BHL adapter (AC-8) operates at page level, not item level.

**Key API endpoints:**

```
GET /api3?op=GetPageMetadata&pageid={pageid}&ocr=f&names=t&format=json
  → Returns: PageType, PageUrl, ThumbnailUrl, Names (taxonomic names extracted)

GET /api3?op=GetItemMetadata&itemid={itemid}&idtype=BHL&format=json
  → Returns: Source, TitleID, License, LicenseUrl, HoldingInstitution, Rights

GET /api3?op=GetTitleMetadata&titleid={titleid}&format=json
  → Returns: Authors, FullTitle, PublicationDate, SubjectTags

GET /api3?op=GetPageNames&pageid={pageid}&format=json
  → Returns: NameFound (list), NameConfidenceRating, GBIFUsageKey
```

**Illustration filter (PageType):**

BHL's `PageType` field is NC's primary filter. Target values:
- `"Illustration"` — primary target
- `"Map"` — secondary target (Historic Maps Tier 1)
- `"Plate"` — included
- `"Figure"` — included

Excluded: `"Text"`, `"Index"`, `"Table"`, `"Title Page"` (unless image content confirmed by secondary classifier)

**Estimated pipeline reduction:**

| Stage | Volume |
|---|---|
| Total BHL pages | 60,000,000 |
| After PageType filter | ~2,000,000 |
| After image quality classifier | ~500,000 |
| After rights screen (Tier 1+2 only, pilot) | ~200,000 |
| After place association | ~80,000 |
| Commerce-ready IOs (Tier 1 assets) | ~15,000–25,000 |

### Image Delivery

BHL does not provide IIIF. Image delivery is direct URL:

```
https://www.biodiversitylibrary.org/pageimage/{pageid}
```

This matches the Walters and NARA delivery model (no IIIF). NC stores the BHL page URL as `source_url` and downloads the image to NC's own storage. **SA-BHL-001 must specify the BHL direct delivery protocol as a variant of SA-23 (NARA direct delivery).**

**Resolution tiers:**
BHL provides two resolutions:
- Thumbnail: `bhl_item.ThumbnailUrl` (low resolution, suitable for discovery only)
- Full page: `biodiversitylibrary.org/pageimage/{pageid}` (300–600 dpi from microfilm/flatbed scans)

Quality varies by digitizing institution and original print quality. A quality threshold filter (minimum 150 dpi equivalent) is required before Tier 1 classification.

### BHL Bulk Download (Batch Harvest)

Beyond the API, BHL provides a bulk data export:

```
https://www.biodiversitylibrary.org/data/data.nhtml
```

This includes structured exports of titles, items, pages, and names in TSV format. The NC batch harvester should use the bulk download for initial population and the API for incremental updates.

---

## 4. Taxonomic Integration

### The BHL-GBIF Bridge

BHL operates its own Name Usage service, which applies automated taxonomic name recognition (TNR) to OCR text from every page. The output includes extracted scientific names with associated GBIF Backbone taxon keys.

**This bridge is the single most important technical feature of BHL for NC.** It means that for a BHL page showing a Haeckel radiolarian, BHL has already extracted the scientific name and linked it to a GBIF taxon key. NC inherits this work directly.

**How NC uses the BHL-GBIF bridge:**

```
BHL page → PageNames API → NameFound[].GBIFUsageKey
  → resolution_method = "bhl_names_service"
  → gbif_taxon_key = GBIFUsageKey
  → gbif_confidence = NameConfidenceRating / 100
  → cross-validate: GET gbif.org/species/{taxon_key}
    → confirm scientificName, kingdom, class matches caption OCR
```

**GBIF governance constraints apply (SA-GBIF-001):**
- GBIF taxon key is the biological anchor; BHL is the discovery source
- GBIF occurrence count capped at 100 per CI Constitution
- GBIF media permanently prohibited; only GBIF taxon key is used
- Source role remains `"validation_only"` for GBIF regardless of how taxon key was discovered

**When BHL name resolution fails:**
If `PageNames` returns empty or low-confidence results, the fallback sequence is:
1. Caption OCR → spaCy NER → GBIF fuzzy species lookup
2. Illustrator + date → likely genera inference (e.g., Audubon plates = North American birds)
3. Record as `gbif_confidence = 0.0`, `gbif_taxon_key = null`, asset tier downgrades to Tier 2

### Illustrator Resolution via BHL

BHL item metadata includes `Authors` with BHL-internal person IDs. The NC pipeline maps BHL author IDs to ULAN IDs:

```
bhl_item.Authors[].Name → fuzzy match → ULAN person search
  → if priority illustrator match: ulan_id confirmed, confidence = 0.95
  → if match by name only: ulan_id proposed, requires human gate
```

**Priority illustrators with high BHL-ULAN match confidence:**

| Illustrator | BHL Coverage | ULAN ID | Notes |
|---|---|---|---|
| John James Audubon | Extensive (Birds + Quadrupeds) | 500013195 | Major volumes from Smithsonian + NYPL |
| John Gould | Extensive (birds series) | 500009325 | Multiple BHL volumes from NHM |
| Maria Sibylla Merian | Core works | 500028462 | Insecten-Werk, Metamorphosis Insectorum |
| Pierre-Joseph Redouté | Extensive (botanical) | 500003600 | Les Liliacées, Les Roses — some MNHN contributions |
| Edward Lear | Illustrated works | 500022973 | Parrots + Tortoises |
| Frederick Nodder | Selected plates | 500037547 | Naturalist's Miscellany; NHM primary |
| Ernst Haeckel | Full Kunstformen + scientific plates | 500023445 | Multiple Tier 1 member contributions |
| Joseph Wolf | Selected plates | 500037213 | NHM primary archive; limited BHL presence |

---

## 5. NC-PDPS: Provenance Chain for BHL Illustrations

BHL introduces a more complex provenance chain than previous institutions. Every BHL illustration requires 7 NC-PDPS links (standard is 6):

```
L1 — Creator: [Illustrator name], [ULAN ID], [birth–death dates]
     e.g.: "John James Audubon, ULAN:500013195, 1785–1851"

L2 — Creation Event: [Title], [publication date], [plate number if applicable]
     e.g.: "The Birds of America, 1827–1838, Plate I: Wild Turkey"

L3 — Physical Custody: [Contributing member library], [holding institution], [acquisition record if known]
     e.g.: "Smithsonian Institution Libraries, Washington DC. Digitized 2014."

L4 — Digitization: [Contributing library], [digitization date/program], [resolution], [member tier]
     e.g.: "Smithsonian Institution Libraries. BHL Digitization Program. CC0 1.0. BHL Tier 1."

L5 — Rights Status: [Rights class] + [rights decision] + [confidence]
     e.g.: "Rights Class 10. ALLOWED. Pre-1928 US PD + CC0 member library. Confidence: 0.97."

L6 — Platform Record: [BHL page URL], [BHL item ID], [BHL title ID], [access date]
     e.g.: "biodiversitylibrary.org/page/[pageid]. Item [itemid]. Accessed 2026-06-13."

L7 — Commercial Activation: [NC curator name], [date], [edition size if CE]
     e.g.: "Nathan Holderhead, Founding Curator. Activated 2026-[date]. Open edition."
```

**L7 is always a named human. This is NC-PDPS permanent invariant (AF-12).**

The addition of L4 (Digitization) separates the physical custody from the digitization rights decision. This is required for BHL because the digitizing library and the physical holding institution are sometimes different entities.

---

## 6. Collection Generation

BHL enables collection types not available from any single institution.

### Collections directly unlocked by BHL activation:

**Priority Illustrator Collections** (blocked without BHL):
- *Audubon: Birds of America* — requires NYPL/Smithsonian Tier 1 BHL contributions + GBIF taxon keys for all plates
- *Haeckel: Kunstformen der Natur* — requires Tier 1 BHL contributions + radiolarian / medusa GBIF taxon keys
- *Gould: A Monograph of the Trochilidae* (hummingbirds) — requires NHM/Smithsonian BHL contributions

**Expedition Collections** (anchored to place):
- *Cook Voyage Natural History* — Parkinson + Nodder plates from NHM BHL contributions; place: Pacific islands
- *Humboldt Expedition* — Botanical illustration from BHL; place: Andes + Amazon
- *Banks/Parkinson Endeavour* — NHM BHL contributions; place: Great Barrier Reef, New Zealand, Tahiti

**Designation-Series Collections** (enabled at scale):
- *UNESCO Biosphere Reserve: Natural History Series* — BHL botanical + zoological illustration for all 738 biosphere reserves
- *Geopark Expedition Series* — BHL geological natural history; fills SA-GEOPARK-001 gap

### Overlap with Existing Collections

BHL contributions do not conflict with existing NC collections. The Earthrise collection (NASA) has no BHL overlap. Islamic architecture collections (Alhambra, Petra, Fez) have limited BHL content; the primary BHL value is natural history, not architectural illustration.

---

## 7. Product Generation

BHL enables NC product lines that cannot be activated from any other single source.

**Immediately activatable (Tier 1 member libraries):**

| Product Line | Product Family | Example SKU | Prerequisite |
|---|---|---|---|
| Natural History Print | B (Wall Art) | Audubon Wild Turkey, A3 | DD-BHL-001 + SA-BHL-001 |
| Botanical Study Print | B | Redouté Rose Plate XII, A3 | DD-BHL-001 + MNHN confirmation |
| Expedition Folio | G (Collector) | Haeckel Kunstformen CE, 100 prints | DD-BHL-001 + SA-BHL-001 |
| Digital Study Edition | F (Digital) | Gould Hummingbird DDS | DD-BHL-001 |
| Natural History Digital Pack | F | Cook Voyage Pacific Plates | NHM + BHL joint activation |
| Educational Context Card | C (Educational) | Audubon Bird Biology EDU-1 | DD-BHL-001 + EDU platform |

**Darwin Core mandatory fields for all BHL natural history products:**

```
dwc:scientificName        ← from BHL Names service (GBIF-confirmed)
gbif:taxonKey             ← from BHL-GBIF bridge
dwc:recordedBy            ← illustrator (ULAN anchor)
dwc:basisOfRecord         ← "HumanObservation" (illustrated observation)
dwc:institutionCode       ← contributing member library slug
dc:bibliographicCitation  ← full BHL citation (title, author, page URL)
```

---

## 8. Unique Risks vs Existing Institutions

Ten risks specific to BHL not encountered in prior DD documents:

| Risk | Severity | Mitigation |
|---|---|---|
| **R-1** Member library ToS variation (~100 institutions) | HIGH | Member library Tier Classification; pilot restricted to Tier 1 only |
| **R-2** Rights metadata reliability (crowd-sourced from members) | HIGH | Two-field confirmation: BHL license string + date rule; confidence score required |
| **R-3** Non-US member EU digitization copyright claims | MEDIUM | Bridgeman doctrine applies in US; NC products sold via US commerce; monitor for UK/EU specific claims |
| **R-4** OCR quality: name extraction accuracy varies by volume age and scan quality | MEDIUM | BHL name confidence rating threshold (≥0.70); human gate for priority illustrator attribution |
| **R-5** No IIIF: image resolution and stability uncertainty | MEDIUM | Direct delivery protocol (SA-BHL-001 per SA-23 variant); NC caches images to own CDN |
| **R-6** Competing institution primacy: for priority illustrators, originating institution (e.g., NHM for Nodder originals) should take precedence over BHL aggregation | LOW | IFC routing: if specific institution has confirmed CC0 + higher resolution, prefer that institution's DD over BHL |
| **R-7** Attribution chain complexity (7 links vs 6 for standard IOs) | LOW | NC-PDPS extended to 7 links for BHL type; documented in SA-BHL-001 |
| **R-8** Scale: 60M pages → automated decisions carry residual error rate | HIGH | Confidence thresholds per rights decision; REVIEW_REQUIRED threshold at 0.75; human gate for Tier 1 CEs |
| **R-9** BHL API rate limits | LOW | API key required; bulk download for initial harvest reduces API dependency |
| **R-10** Member library disqualification cascades: if a Tier 1 library is later reclassified (ToS change), all their BHL contributions must be immediately suspended | MEDIUM | Quarterly member library Tier audit; suspension trigger armed per CI-6 equivalence |

---

## 9. Pilot Specification

| Parameter | Value |
|---|---|
| Asset count | 50 illustrations |
| Duration | 90 days from Asset Zero confirmation |
| Member library restriction | **Tier 1 only** (no Tier 2 or Tier 3 contributions in pilot) |
| Priority illustrators | Audubon + Haeckel (2 of 8; both confirmed in Tier 1 member libraries) |
| Target places | Everglades (Audubon) · Atlantic/Pacific (Haeckel radiolarians) |
| Rights screen | Pre-1928 + CC0 member library; confidence ≥ 0.90 required |
| GBIF validation | gbif_taxon_key confirmed for all 50 assets via BHL Names API |
| ULAN validation | ulan_id confirmed for all Audubon and Haeckel assets |
| Image quality | Minimum 150 dpi equivalent; no missing plates |
| Sprint compliance | Sprint 1 compliance required before Asset Zero confirmation |
| Suspension triggers | Rights confidence drops below 0.85 on any batch; member library ToS change; stop harvest immediately |

**Asset Zero (proposed):**
**Audubon — Wild Turkey (Plate I, The Birds of America, 1827)**
- BHL holding: Smithsonian Institution Libraries (BHL Tier 1, CC0)
- GBIF taxon key: *Meleagris gallopavo* (GBIF:5228050)
- ULAN: 500013195 (Audubon confirmed)
- GeoNames: connects to Everglades (GeoNames TBD per NC-DATA routing)
- NC Rights Class 10: ALLOWED, confidence 0.97
- NC-PDPS: 7-link chain complete

Asset Zero must be confirmed by two named humans per Gate E.

---

## 10. Standards Amendments Required

| SA | Title | Blocks |
|---|---|---|
| **SA-BHL-001** | BHL Protocol, Rights Matrix v1, and Member Library Tier Classification | All BHL commercial activation |
| **SA-BHL-002** | BHL-GBIF Bridge Protocol (NC-PDPS L4 + 7-link provenance chain) | All BHL natural history IOs |
| **SA-9 extension** | Add `bhl` slug to known source slugs (now 13th slug in SA-9) | Sprint 1 compliance |

**SA-BHL-001 must define:**
1. AC-8 BHL Page API adapter specification (endpoint, pagination, PageType filter values)
2. BHL Rights Matrix v1 (above table, encoded as rights.py)
3. BHL Member Library Tier Classification v1 (living document, quarterly update cycle)
4. Direct image delivery protocol (no IIIF variant of SA-23)
5. Attribution standard: BHL citation format for NC-PDPS L6
6. Bulk download harvest protocol (supplementary to API)
7. Member library disqualification cascade procedure

**SA-BHL-002 must define:**
1. NC-PDPS extended 7-link chain for BHL illustrations
2. BHL Names API integration spec (pageid → GBIFUsageKey resolution)
3. Fallback name resolution sequence (OCR → spaCy → GBIF fuzzy)
4. Minimum GBIF confidence threshold for Tier 1 classification (0.70)
5. Darwin Core mandatory fields for BHL natural history products

---

## 11. Governance Invariants

| # | Invariant |
|---|---|
| BHL-1 | No BHL illustration enters the commercial pipeline before SA-BHL-001 and SA-BHL-002 are ratified |
| BHL-2 | The pilot is restricted to Tier 1 member libraries. No Tier 3 or UNCLASSIFIED library contributions may enter any pipeline stage during the pilot |
| BHL-3 | BHL rights metadata (item-level license string) is necessary but not sufficient. The contributing member library's Tier Classification is always required as the second input to the Rights Class 10 decision |
| BHL-4 | AF-8 applies unconditionally: a pre-1928 public domain ruling does not override a contributing library's ToS commercial restriction |
| BHL-5 | The BHL-GBIF bridge provides GBIF taxon keys. GBIF media is permanently prohibited per DD-GBIF-001 regardless of how the taxon key was discovered |
| BHL-6 | For any priority illustrator whose originating institution has a confirmed CC0 + higher-resolution source (e.g., NHM Nodder originals), that institution's DD takes precedence over BHL aggregation for CE products |
| BHL-7 | NC-PDPS for BHL illustrations requires 7 links (L1–L7), not 6. L7 remains always a named human |
| BHL-8 | Member library Tier Classification is reviewed quarterly. Any downgrade from Tier 1 to Tier 4 triggers immediate suspension of all affected contributions |
| BHL-9 | IFC-1 is unconditional. Any BHL item whose member library is BLOCKED (Tier 4) cannot enter any NC pipeline stage regardless of BHL's platform rights assertion |
| BHL-10 | At scale (>50K BHL assets in pipeline), the REVIEW_REQUIRED queue requires a dedicated human review workflow. Automated REVIEW_REQUIRED records must not age more than 30 days without action |

---

## 12. Open Actions

| # | Action | Priority | Owner |
|---|---|---|---|
| OA-1 | Draft and ratify SA-BHL-001 | CRITICAL | Architecture |
| OA-2 | Draft and ratify SA-BHL-002 | CRITICAL | Architecture |
| OA-3 | Complete Member Library Tier Classification for top 25 BHL contributors | CRITICAL | Governance |
| OA-4 | Extend SA-9 to add `bhl` slug (13th source slug) | HIGH | Engineering |
| OA-5 | Implement AC-8 BHL Page API adapter | HIGH | Engineering |
| OA-6 | Implement BHL-GBIF bridge (Names API → GBIF taxon key resolution) | HIGH | Engineering |
| OA-7 | Encode Rights Class 10 in rights.py | HIGH | Engineering |
| OA-8 | Asset Zero confirmation: Wild Turkey Plate I (two-human Gate E) | HIGH | Curator |
| OA-9 | Initiate pilot harvest: 50 Tier 1 assets, Audubon + Haeckel | HIGH | Engineering + Curator |
| OA-10 | Draft DD-SMITHSONIAN-001 to confirm Smithsonian BHL Tier 1 status | HIGH | Architecture |
| OA-11 | Image quality classifier training data (BHL illustration samples) | MEDIUM | AI/ML |
| OA-12 | ULAN fuzzy lookup service for BHL author name resolution | MEDIUM | Engineering |
| OA-13 | BHL direct delivery CDN caching layer | MEDIUM | Infrastructure |
| OA-14 | Member library Tier audit calendar (quarterly) | LOW | Governance |

---

## Ratification Package

Before DD-BHL-001 can be ratified and BHL can advance to Stage 3 (Connectivity):

- [ ] SA-BHL-001 drafted and circulated
- [ ] SA-BHL-002 drafted and circulated
- [ ] Member Library Tier Classification v1 (top 25 contributors) attached as Appendix A
- [ ] BHL API access confirmed (api key registered, rate limit documented)
- [ ] SA-9 extension (bhl slug) drafted
- [ ] Two-human ratification: named humans and signatures

---

*DD-BHL-001 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
*Next stage upon ratification: Stage 3 (Connectivity) — BHL source record in DB, API smoke tests, SC-1 verified*
