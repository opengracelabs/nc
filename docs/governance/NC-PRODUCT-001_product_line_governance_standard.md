# NC-PRODUCT-001: Product Line Governance Standard

| Field | Value |
|---|---|
| Document | NC-PRODUCT-001 |
| Version | 1.0 |
| Status | **DRAFT** — Pending Ratification |
| Date | 2026-06-11 |
| Authority | Strategic Directive · Illustration Opportunity Doctrine · IFC v1 · Product Routing Constitution v1.1 |
| Reference Documents | NC-PILOT-001 Launch Authorization · DD-NASA-001 (institutional knowledge) · DD-NOAA-001 · DD-NARA-001 · DD-MIA-001 · DD-GBIF-001 · DD-WIKIDATA-001 · SA-GEONAMES-001 · SA-OSM-001 · Product Routing Constitution v1.1 |
| Drafted By | NC Principal Architect |

---

## DECISION

**APPROVE WITH CONDITIONS**

Eighteen of the twenty requested product lines are approved for commercial activation subject to the conditions and gates defined in this standard. Two lines are reserved pending routing policy activation:

| Line | Product | Decision | Reason |
|---|---|---|---|
| 17 | Apparel | **RESERVED** | `fashion` family not routed in Product Routing Constitution v1.0; activation requires routing policy v2.0 |
| 18 | Tote bags | **RESERVED** | `fashion` family not routed in Product Routing Constitution v1.0; activation requires routing policy v2.0 |
| 1–16, 19–20 | All others | **APPROVED WITH CONDITIONS** | See per-line conditions and §VII gates |

All 20 lines are subject to IFC-1 (unconditional rights hard gate), FM-4 (foundation model inference prohibition), and the federal nonendorsement doctrine.

---

## Part I — Product Line Registry

### Article 1 — Mapping to Product Routing Constitution Families

The twenty commercial product lines map to the Product Routing Constitution v1.1 families and product types as follows. The routing constitution is the machine-level authority; this document is the commercial governance layer above it.

| # | Commercial Product Line | Routing Family | Routing Product Types | Min CSM Tier | Curator Always |
|---|---|---|---|---|---|
| 1 | Museum-grade wall prints | `museum_print` | `museum_giclée`, `archival_print` | MASTERWORK | ☑ |
| 2 | Framed prints | `wall_art` | `framed` | STANDARD | ☐ |
| 3 | Poster editions | `wall_art` | `poster` | STANDARD | ☐ |
| 4 | Canvas prints | `wall_art` | `canvas` | STANDARD | ☐ |
| 5 | Map prints | `wall_art` | `map_print` ¹ | STANDARD | ☐ |
| 6 | Archival plate collections | `museum_print` | `archival_print` (multi) ² | FLAGSHIP | ☑ |
| 7 | Place portfolios | `institutional_license` | `print_license` ³ | FLAGSHIP | ☑ |
| 8 | Digital downloads | `institutional_license` | `digital_license` | STANDARD | ☐ |
| 9 | PDF discovery guides | `educational` | `reference_sheet` (PDF) ⁴ | REFERENCE | ☐ |
| 10 | Educational lesson packs | `educational` | `classroom_poster`, `reference_sheet` | REFERENCE | ☐ |
| 11 | Tourism companion guides | `book` | `book_interior` | STANDARD | ☐ |
| 12 | Conservation story packs | `book` | `book_interior` | STANDARD | ☐ |
| 13 | Coffee-table book prototypes | `book` | `book_interior`, `cover_art` | FLAGSHIP | ☑ |
| 14 | Calendars | `calendar` | `wall_calendar`, `desk_calendar` | STANDARD | ☐ |
| 15 | Postcards / greeting cards | `card` | `greeting_card`, `notecard_set` | STANDARD | ☐ |
| 16 | Stickers | `card` | `sticker` ⁵ | STANDARD | ☐ |
| 17 | Apparel | `fashion` | — | — | RESERVED |
| 18 | Tote bags | `fashion` | — | — | RESERVED |
| 19 | Notebooks / journals | `home_decor` | `notebook_cover` ⁶ | STANDARD | ☐ |
| 20 | Premium collector bundles | `institutional_license` | `print_license` (bundle) ⁷ | MASTERWORK | ☑ |

**Product type notes:**

¹ `map_print` — new product type within `wall_art` family; authorized for Historic Maps Tier 1 assets (CI v1.2 `signal_substitutions`). NARA is the primary source. `map_print` is eligible at `eligible_wall_art_premium = TRUE`. No routing policy amendment required; `map_print` is a commerce-layer label routed within the existing `wall_art` family.

² Archival plate collections are multi-asset bundles of 4–12 `archival_print` units sold as a set. Each plate must individually pass IFC-1 and all gates. The bundle requires a single curator release approval covering all plates; individual plates are not separately activated after bundle approval.

³ Place portfolios are place-anchored print license bundles. Each must have a confirmed GeoNames ID (Invariant S-3) for the anchor place. Venice portfolios are deferred until Venice full-launch (requires DD-MET-001 ratification).

⁴ PDF discovery guides are delivered as `educational` → `reference_sheet` in `digital_license` envelope. They are governed as digital delivery products.

⁵ `sticker` is a new product type within the `card` family, at the lowest commerce tier threshold (tier_3). Sticker products use the `card` routing eligibility flag.

⁶ `notebook_cover` is a new product type within `home_decor`. Notebooks are governed as derived `home_decor` products: eligible when `eligible_wall_art_standard = TRUE AND csm_tier IN ('MASTERWORK','FLAGSHIP','STANDARD') AND commerce_tier IN ('tier_1','tier_2')`.

⁷ Premium collector bundles are multi-family bundles requiring MASTERWORK or FLAGSHIP tier assets for all included items. Governed as `institutional_license` with curator review always required. Bundle activation requires Principal Architect sign-off in addition to curator approval.

---

## Part II — Rights Class Eligibility

### Article 2 — Rights Class Admission Matrix

All product lines share the same rights admission logic. Rights classes are defined by their governing DD.

| Rights Class | Legal Basis | Source(s) | Eligible Product Lines |
|---|---|---|---|
| § 105 (federal statute PD) | 17 U.S.C. § 105 | NASA, NOAA, NARA | All 18 approved lines (1–16, 19–20) |
| CC0 | CC0 grant | BHL, Wikidata data | All 18 approved lines |
| Rights Class 3B — PDM / NoC-US | PDM / NoC-US | MIA (`rights_type="Public Domain"`, `"No Copyright–United States"`) | All 18 approved lines |
| Rights Class 3B — REVIEW REQUIRED | NoC-CR / NKC | MIA (`rights_type="No Copyright—Contractual Restrictions"`, `"No Known Copyright"`) | Lines 2–16, 19 (not museum_print / premium bundles); blocked from activation until human review complete |
| Rights Class 9 per-record | NARA `useRestriction.status == "Unrestricted"` | NARA | All 18 approved lines |
| Rights Class 9 per-record | NOAA Flickr `license ∈ {7,8,9,10}` | NOAA | All 18 approved lines; Sprint 3 write cap applies (§II.3) |

**2.1 NOAA Sprint 3 write cap.** NOAA assets with `license ∈ {7,8,9,10}` (ALLOWED) are limited to a maximum of 7 M36 writes in the current pilot sprint. REVIEW_REQUIRED NOAA assets (`license ∈ {1,2,3,4,5,6}`) produce zero writes in the pilot. These restrictions are sprint-specific governance controls under DD-NOAA-001 §VII and do not permanently limit NOAA product eligibility after sprint completion.

**2.2 MIA REVIEW_REQUIRED gating.** MIA `NoC-CR` and `NKC` records create a `workflow_item` and are written to M36 with `rights_status = "pending_verification"`. No commercial product may be activated from a REVIEW_REQUIRED record until the workflow_item is closed with `human_verdict = "verified_pd"`. Until that point, the asset is product-ineligible regardless of routing score.

### Article 3 — Permanent Exclusions (All Product Lines)

The following are permanently excluded from all 20 product lines and may not enter the product pipeline under any conditions:

| Category | Exclusion basis | Invariant |
|---|---|---|
| CC BY-NC licensed content | Non-commercial restriction; IFC-1 unsatisfiable at scale | IFC-1 |
| OSM-derived stored data | ODbL share-alike incompatible with NC commercial doctrine | OS-1–OS-5 (DD-OSM-001) |
| Wikidata Commons media (P18 referents and Wikimedia image URLs) | Commons boundary doctrine — Wikidata is an Identity Authority, not a content pipeline | W-6 (DD-WIKIDATA-001) |
| GBIF media (images from GBIF occurrence records) | Five-reason disqualification: wrong content type, mixed licenses, quality variance, occurrence data not illustration, `media_ingestion: "permanently_prohibited"` | DD-GBIF-001 §IV |
| Any asset with `rights_status = "blocked"` | IFC-1 hard gate failed | IFC-1 |
| Any asset with `hard_gate_status != "passed"` | Pre-routing gate PRG-1 failed | PRG-1 |
| Any asset with `commerce_tier = "blocked"` | Scoring verdict | PRG-3 |
| NOAA assets with personal name in credit line | Permanent hard block — individual credit indicates non-§105 origin | DD-NOAA-001 §III.3 |
| Apparel, Tote bags (lines 17, 18) | `fashion` routing family RESERVED in routing policy v1.0 | Product Routing Constitution v1.1 Art. 5 |

---

## Part III — Attribution and Disclaimer Standards

### Article 4 — Attribution Stack by Product Surface

Attribution requirements vary by surface type. The following is the governing matrix.

#### 4.1 Physical Print Products (lines 1–6, 14–16, 19)

Physical products (prints, cards, calendars, stickers, notebooks) have a label/packaging surface distinct from the digital listing.

| Attribution obligation | Physical label / packaging | Digital product listing |
|---|---|---|
| Asset credit (institution) | Required (brief form): e.g., `"Source: National Archives"` or `"Source: BHL/[Illustrator]"` | Required (full form per institution DD) |
| NASA nonendorsement | **Required**: exact text (§4.3) | **Required**: exact text (§4.3) |
| NOAA nonendorsement | Required if NOAA is named in product copy | **Required**: exact text (§4.3) |
| NARA credit | Preferred: `"Image from the National Archives (Record Group [n], Catalog ID [n])"` | Required as above |
| GeoNames CC BY 4.0 | **NOT required** on physical label alone (SA-GEONAMES-001 §III) | **Required**: full form if geo-anchored |
| OSM attribution | **NOT required** unless a map tile is printed on the physical product | **Required** if product listing displays map tiles |
| MIA credit | Not mandatory; `"Collection of the Minneapolis Institute of Art"` preferred | Required: `"Minneapolis Institute of Art, CC0"` |

#### 4.2 Digital Products (lines 8, 9, 10, 11, 12, 13)

Digital downloads, PDFs, guides, and book content carry the full attribution stack.

| Attribution obligation | In-document (PDF/digital file) | Product listing page |
|---|---|---|
| Asset credit | Required — full caption with institution, record ID, and rights basis | Required |
| NASA nonendorsement | **Required** in document credits section | **Required** |
| NOAA nonendorsement | **Required** in document credits section | **Required** |
| GeoNames CC BY 4.0 | **Required** in document credits: `Geographic data © GeoNames (geonames.org) — CC BY 4.0` | Required |
| OSM attribution | Required if document includes map imagery | Required if listing shows map tiles |
| Rights statement | `Public Domain` / `No Copyright` label per rights basis | `rights_statement_uri` linked |

#### 4.3 Museum-Grade and Collector Products (lines 1, 6, 7, 20)

Museum-grade products require full certificate of authenticity (COA) documentation containing:
- Asset title, date, and source institution
- Rights basis and `rights_statement_uri`
- NC edition number (for archival plate collections)
- Federal nonendorsement text (§5) if applicable
- GeoNames attribution if geo-anchored
- Curator approval reference (reviewer ID and approval date)

### Article 5 — Federal Nonendorsement Language (NASA / NOAA / NARA)

This article supersedes any general attribution rule for assets sourced from federal agencies. Federal nonendorsement language is **mandatory** and **immutable** for all products containing NASA, NOAA, or NARA imagery. Any product missing required nonendorsement text is product-unsafe and must not be activated.

#### 5.1 NASA

```
Image credit: NASA. NASA does not endorse this product.
```

- Required on: all digital product listings, all physical product labels, all COA documents, all digital download packages, all PDF documents containing NASA imagery
- Placement: directly beneath the NASA image or in the credits section — not buried in footer
- Prohibited: NASA meatball logo, NASA seal, any language implying NASA partnership or approval

#### 5.2 NOAA

```
Credit: NOAA/[Division]. NOAA does not endorse this product.
```

Replace `[Division]` with the applicable division from the NOAA federal allow-list: `NOAA`, `NOAA/NMFS`, `NOAA/NOS`, `NOAA/OAR`, `NOAA/NWS`, `NOAA/NESDIS`, `ESSA`, `USCGS`, `US Weather Bureau`, `Bureau of Commercial Fisheries`. The `credit_line` field from the NOAA source record governs which division appears.

- Required on: all digital product listings containing NOAA imagery; all physical product labels if NOAA is named in product copy
- Prohibited: NOAA circular seal, any language implying NOAA partnership, sponsor, or endorsement

#### 5.3 NARA

```
Image from the National Archives (Record Group [n], Catalog ID [n]).
```

NARA does not require an active nonendorsement disclaimer (unlike NASA/NOAA), but the credit format above is required. `Record Group` and `Catalog ID` (`naId`) are extracted from the NARA source record.

#### 5.4 Federal Endorsement Zero-Tolerance

A single confirmed endorsement violation on any federal-sourced product triggers immediate deactivation of ALL products sourced from that federal agency across the entire NC catalog. This zero-tolerance rule is unconditional (established in NC-PILOT-001 Launch Authorization, Decision Article 8).

---

## Part IV — GeoNames and OSM Attribution for Place/Map Products

### Article 6 — GeoNames Attribution Rules

Governed by SA-GEONAMES-001. Summary of product-specific rules:

| Product context | GeoNames attribution required? | Form |
|---|---|---|
| Digital product listing (any geo-anchored product) | **Yes** | Full: `Geographic data © GeoNames (geonames.org) — CC BY 4.0` |
| Physical print label or packaging | **No** | Not required on physical label alone |
| PDF discovery guide or educational PDF | **Yes** | Full form in document credits |
| Digital download package (zip/metadata) | **Yes** | `nc:geonames_attribution` JSON in metadata manifest |
| Place portfolio | **Yes** | Full form on portfolio cover/credits page |
| Museum COA | **Yes** | Full form in COA |
| Calendar (print product) | **No** on physical calendar | **Yes** on digital listing |
| Sticker, postcard, greeting card (physical) | **No** | **Yes** on digital listing |
| Earthrise product (any) | **Exempt** | S-3 cosmic anchor exception; `geonames_exemption: "cosmic_anchor_S3_provisional"` |

### Article 7 — OSM Attribution Rules

Governed by SA-OSM-001. OSM attribution is required ONLY when OSM tiles are rendered and visible to the purchaser.

| Product context | OSM attribution required? |
|---|---|
| Product listing page with map tile displayed | **Yes** — `© OpenStreetMap contributors` overlaid on map tile |
| Map print (product line #5) — the product IS a rendered map | **Yes** — attribution embedded in map image or printed caption |
| Any product where no map tile is rendered | **No** |
| Physical print or packaging (no map rendered) | **No** |
| PDF containing an embedded map image | **Yes** — caption on the map image |
| Digital download without map rendering | **No** |

For Mapbox-served tile listings: `© OpenStreetMap contributors | Map data provided by Mapbox` — OSM attribution appears first.

---

## Part V — Exclusions Register

### Article 8 — REVIEW_REQUIRED Asset Controls

Assets in REVIEW_REQUIRED status (`rights_type IN {"No Copyright—Contractual Restrictions", "No Known Copyright"}` at MIA; or manual review-queue at any institution) are subject to these controls:

1. REVIEW_REQUIRED assets MAY NOT activate to any product line until `workflow_item.human_verdict = "verified_pd"` is set by an authorized human reviewer
2. REVIEW_REQUIRED assets MAY be routed (a `product_recommendation` record may be created) but must have `status = "pending_curator_review"` with a block note indicating rights review dependency
3. REVIEW_REQUIRED assets MUST NOT appear on any public-facing product listing
4. A routing worker that creates a product_recommendation for a REVIEW_REQUIRED asset must set `recommendation_basis.derivation_note` to `"rights_review_dependency: workflow_item_required"` to ensure the dependency is visible in the routing audit trail

### Article 9 — BLOCKED Asset Controls

Assets with `rights_status = "blocked"` are completely excluded from the product pipeline. Blocked assets:
- Produce no product_recommendation records (PRG-1 gate failure)
- Must not appear in any product listing, bundle, or collection
- Must not be referenced in any COA, PDF, or digital download
- May not be unblocked without a formal governance review and IFC-1 re-evaluation

### Article 10 — Source-Specific Permanent Exclusions

| Source | Excluded content | Basis |
|---|---|---|
| All sources | CC BY-NC licensed content | IFC-1 (non-commercial restriction) |
| GBIF | All GBIF-hosted media (images attached to occurrence records) | DD-GBIF-001 `media_ingestion: "permanently_prohibited"` |
| Wikidata | All P18 (image) field referents; all Wikimedia Commons image URLs | DD-WIKIDATA-001 Invariant W-6 |
| OSM | Any data derived from OSM tags, relations, or coordinates stored in NC tables | OS-1–OS-5 |
| NOAA | Personal name credit lines | DD-NOAA-001 §III.3 — permanent hard block |
| NOAA | REVIEW_REQUIRED (Flickr `license ∈ {1–6}`) in pilot phase | DD-NOAA-001 §VII — 0 pilot writes |
| Any institution without a ratified DD | All content | Institution Factory Constitution IFC-1 |

---

## Part VI — Product Approval Gates

### Article 11 — Gate Sequence

Every product recommendation must clear gates in sequence. A failure at any gate terminates the product activation workflow for that asset at that product line.

**Gate 0 — Source Activation Gate (IFC institutional gate)**

The source institution must have:
- A ratified Decision Document (DD) in `docs/decisions/`
- `governance_state: "active"` or equivalent in the sources table
- All required Standards Amendments (SAs) ratified

No asset from an unratified institution may enter any product line. Violation is IFC-12 constitutional breach.

**Gate 1 — IFC-1 Rights Hard Gate (unconditional)**

```
media_rights.rights_status = 'verified_pd'
AND media_rights.human_verified = TRUE
AND commerce_opportunities.hard_gate_status = 'passed'
```

This gate is unconditionally permanent. No exception, no bypass. FM-4 reinforces: foundation model inference alone may never set `rights_status = 'verified_pd'`. Human review must set `human_verified = TRUE`.

**Gate 2 — Pre-Routing Gates (PRG-0 through PRG-3)**

From Product Routing Constitution v1.1 Article 7:
- PRG-0: `commerce_opportunities.curator_decision = 'approved'`
- PRG-1: `commerce_opportunities.hard_gate_status = 'passed'`
- PRG-2: `commerce_opportunities.policy_stale = FALSE`
- PRG-3: `commerce_opportunities.commerce_tier NOT IN ('blocked')`

**Gate 3 — Product Family Routing Gate**

From Product Routing Constitution v1.1 Article 8:
- Flag gate (any/all/derived per family)
- Commerce tier gate (min_commerce_tier threshold)
- CSM tier gate (min_csm_tier threshold)
- Score gates (min_commerce_score, min_csm_score)

**Gate 4 — Federal Nonendorsement Verification Gate**

For any asset sourced from NASA, NOAA, or NARA:
- Required nonendorsement text must be present in the product template
- Text must match exactly (§5)
- No prohibited items (seals, logos, endorsement language) present in product copy

This gate is evaluated at the product template level, not the asset level. A template that passes once covers all assets of that source in that product type.

**Gate 5 — Attribution Completeness Gate**

Before product listing goes live:
- SA-GEONAMES-001 gate items confirmed (if geo-anchored)
- SA-OSM-001 gate items confirmed (if map tiles displayed)
- Institution credit present per institution DD

**Gate 6 — Quality Threshold Gate**

Image file must meet minimum resolution and quality requirements (Article 13).

**Gate 7 — Curator Approval Gate (conditional)**

Required when any of the following hold:
- `routing_rules[family].curator_always_required = true` (museum_print, institutional_license, and per Article 1 for lines 1, 6, 7, 13, 20)
- `commerce_opportunities.requires_curator_review = TRUE`
- `commerce_opportunities.csm_tier = 'MASTERWORK'`
- Asset source is NOAA and it is within the pilot sprint (review all NOAA assets regardless of license tier during Sprint 3)

**Gate 8 — Activation Gate (two-human)**

Governed by IFC-11 (second-human activation). `activation_target.status` transitions to `'activated'` only after two distinct human approvals (curator + Principal Architect sign-off).

For Premium Collector Bundles (line 20): Principal Architect sign-off is mandatory (not just curator). Bundle activation requires explicit decision record.

---

## Part VII — Product-Safe Metadata Fields

### Article 12 — Required Fields on product_recommendation Before Activation

Every `product_recommendation` record must carry the following metadata in `recommendation_basis` before it may activate to a commercial product:

```json
{
  "routing_policy_id": "<UUID>",
  "routing_policy_version": "<semver>",
  "routed_at": "<ISO 8601 UTC>",
  "rights_evidence": {
    "rights_class": "<§105|cc0|3B_pdm|3B_noc_us|3B_review_required|9_nara|9_noaa>",
    "rights_basis": "<mia_public_domain|§105_nasa|§105_noaa|§105_nara|bhl_cc0|...>",
    "rights_statement_uri": "<URI or null>",
    "source_slug": "<nasa|noaa|nara|mia|bhl|...>",
    "human_verified": true,
    "rights_policy_id": "<nara_rights_matrix_v1|mia_rights_matrix_v1|...>"
  },
  "attribution": {
    "federal_nonendorsement_required": true | false,
    "federal_source": "<nasa|noaa|nara|null>",
    "geonames_attribution_required": true | false,
    "osm_attribution_required": true | false,
    "geonames_id": "<integer or null>",
    "geonames_exemption": "<null or 'cosmic_anchor_S3_provisional'>"
  },
  "place_anchor": {
    "place_id": "<UUID or null>",
    "geonames_id": "<integer or null>",
    "wikidata_qid": "<Qnnnn or null>"
  },
  "exclusion_flags": {
    "gbif_media_excluded": false,
    "wikidata_commons_excluded": false,
    "osm_data_excluded": false,
    "cc_by_nc_excluded": false
  }
}
```

All boolean exclusion flags must be explicitly `false` (not null) for an activation-eligible product recommendation. A `true` value on any exclusion flag means the asset must not activate.

---

## Part VIII — Print-File Quality Thresholds

### Article 13 — Minimum Image Resolution Requirements

Quality thresholds are evaluated at the source image file level before routing. An image that fails its threshold must not be written to a product recommendation for the affected product line. Thresholds are minimum gates, not ideal targets.

| Product line | Min pixel dimension (long edge) | Min effective DPI at product size | Min file size guidance |
|---|---|---|---|
| Museum-grade wall prints (#1) | 6000 px | 300 DPI at 20"×24" | 20 MB+ uncompressed recommended |
| Framed prints (#2) | 3600 px | 300 DPI at 12"×16" | — |
| Poster editions (#3) | 3000 px | 150 DPI at 20"×30" | — |
| Canvas prints (#4) | 3600 px | 150 DPI at 24"×36" | — |
| Map prints (#5) | 4000 px | 200 DPI at 20"×24" | — |
| Archival plate collections (#6) | 5000 px | 300 DPI at 16"×20" | — |
| Place portfolios (#7) | 3000 px | 300 DPI at 8"×10" per plate | — |
| Digital downloads (#8) | 3000 px | 300 DPI at 10"×8" effective | — |
| PDF discovery guides (#9) | 1200 px | 150 DPI for body illustrations | — |
| Educational lesson packs (#10) | 1200 px | 150 DPI for body; 300 DPI for classroom poster export | — |
| Tourism companion guides (#11) | 1200 px | 150 DPI for body | — |
| Conservation story packs (#12) | 1200 px | 150 DPI for body | — |
| Coffee-table book prototypes (#13) | 3600 px | 300 DPI for full-page spread | — |
| Calendars (#14) | 2400 px | 200 DPI at 11"×8.5" per month | — |
| Postcards / greeting cards (#15) | 1200 px | 300 DPI at 4"×6" | — |
| Stickers (#16) | 800 px | 300 DPI at 2"×2" | — |
| Apparel (#17) | RESERVED | RESERVED | — |
| Tote bags (#18) | RESERVED | RESERVED | — |
| Notebooks / journals (#19) | 1200 px | 200 DPI at 6"×9" cover | — |
| Premium collector bundles (#20) | 6000 px | 300 DPI at 20"×24" per plate | — |

**Quality source note:** MIA CDN delivers images at 800px maximum (via `800/` path). MIA assets do not qualify for museum-grade wall prints (#1), archival plate collections (#6), or premium collector bundles (#20) based on CDN resolution alone. Sprint 1 must confirm whether full-resolution MIA images are available via API or alternative path. Until confirmed, MIA is restricted to lines #2–16 and #19.

**NARA resolution variability:** NARA digitized items range from 400px thumbnails to 10,000px+ map scans. The NARA adapter must extract `objectFileSize` and construct the highest-resolution `objectUrl` available per record. Sprint 2 must confirm maximum resolution per `objectType`.

---

## Part IX — Commercial Release Checklist

### Article 14 — Per-Product Release Gate (Pre-Activation)

Before any product recommendation transitions to `status = 'activated'`, the following checklist must be completed and signed off by the responsible curator and the Principal Architect (where required).

```
PRODUCT RELEASE CHECKLIST — NC-PRODUCT-001

Asset Identification:
[ ] source_item.id confirmed
[ ] institution confirmed with ratified DD
[ ] source slug confirmed (nasa|noaa|nara|mia|bhl|...)
[ ] product line and routing family confirmed

Rights Verification (IFC-1):
[ ] rights_status = 'verified_pd' confirmed
[ ] human_verified = TRUE confirmed
[ ] hard_gate_status = 'passed' confirmed
[ ] rights_policy_id confirmed and matching institution DD
[ ] REVIEW_REQUIRED workflow_item closed (if applicable)

Federal Assets (if applicable):
[ ] NASA nonendorsement text present and exact (if NASA source)
[ ] NOAA nonendorsement text present with correct division (if NOAA source)
[ ] NARA credit format present with Record Group and Catalog ID (if NARA source)
[ ] No prohibited federal seals, logos, or endorsement language in product copy

Attribution (SA-GEONAMES-001, SA-OSM-001):
[ ] GeoNames attribution present on digital listing (if geo-anchored)
[ ] GeoNames ID confirmed valid (Invariant S-3) or Earthrise exemption recorded
[ ] OSM attribution present (if map tiles displayed)
[ ] Co-attribution ordering correct (asset credit → GeoNames → OSM → institutional)

Exclusion Verification:
[ ] No GBIF media included
[ ] No Wikidata Commons media (P18 referents) included
[ ] No OSM-derived stored data in product metadata
[ ] No CC BY-NC licensed assets
[ ] exclusion_flags all confirmed FALSE

Quality Threshold:
[ ] Source image meets minimum pixel dimension for product line (Article 13)
[ ] Image file confirmed accessible (URL or CDN confirmed live)

Curator Gate (if required):
[ ] curator_reviewed_by IS NOT NULL
[ ] curator_reviewed_at IS NOT NULL
[ ] curator_reviewed_by IS DISTINCT FROM routing worker author (self-approval prohibited)

Collector / Bundle (lines 1, 6, 7, 20 only):
[ ] All bundle plates individually IFC-1 cleared
[ ] COA document prepared with full attribution
[ ] Edition number assigned (archival collections)
[ ] Principal Architect sign-off obtained

Post-Checklist:
[ ] activation_target.status = 'activated' set in same transaction as final approval
[ ] product_recommendation.status = 'assigned' (or 'curator_approved') set
```

---

## Part X — Post-Sale Audit and Takedown Process

### Article 15 — Ongoing Compliance Monitoring

**15.1 Attribution compliance audit.** All active product listings are subject to quarterly attribution spot-checks. Each audit must confirm: federal nonendorsement text exact, GeoNames attribution present where required, OSM attribution present where required. Any detected omission triggers immediate product suspension pending correction.

**15.2 Rights status re-verification.** Any asset with `rights_status = 'verified_pd'` that is subsequently found to carry a valid copyright claim triggers the takedown protocol (Article 16). This includes cases where source institution governance is later found to be deficient, a new rights holder comes forward, or NC receives a DMCA notice.

**15.3 Source institution re-audit trigger.** If a source institution's DD is amended to add exclusions, new rights traps, or compliance conditions, all existing activated products from that source must be re-evaluated within 30 days.

**15.4 NOAA division re-verification.** NOAA Flickr accounts are subject to periodic re-audit. If a NOAA account is found to have changed license terms on previously ingested assets, affected products must be reviewed within 14 days.

### Article 16 — Takedown Protocol

Immediate-suspension triggers (any one is sufficient):
- Rights complaint or DMCA notice received for any activated asset
- Asset found to carry a personal name credit line (NOAA hard block, DD-NOAA-001 §III.3)
- Federal endorsement language found in product copy (zero-tolerance per Launch Authorization Article 8)
- GeoNames attribution absent from a required surface
- Source institution DD revoked (e.g., Gallica-style disqualification)

**16.1 Suspension sequence.**
1. `activation_target.status` set to `'suspended'` (within 1 business hour of discovery)
2. Product listing removed from public view (within 1 business hour)
3. Curator review initiated, Principal Architect notified
4. Determination within 5 business days: remediate or permanently retire
5. If permanent retirement: `product_recommendation.status = 'retired'`; `activation_target.status = 'retired'`

**16.2 Federal agency zero-tolerance cascade.** If a federal endorsement violation is confirmed: all products from that federal source are suspended (not just the violating product) until a full attribution audit confirms all products are clean. This cascade applies to NASA, NOAA, and NARA independently. Suspension of one federal source does not affect others.

**16.3 Affected buyers.** When a product is permanently retired after sale (verified rights failure, not attribution correction), affected buyer records must be flagged for the customer operations team within 24 hours of permanent retirement decision. This document does not govern customer communication — that is an operations responsibility.

**16.4 Post-incident review.** Every takedown that results in permanent retirement requires a post-incident governance review within 30 days. The review produces a lesson-learned addendum to the governing institution DD or SA.

---

## Part XI — Reserved Lines: Apparel and Tote Bags

### Article 17 — Fashion Family Activation Requirements

Product lines 17 (Apparel) and 18 (Tote bags) are assigned to the `fashion` routing family. The `fashion` family is explicitly reserved in Product Routing Constitution v1.1 Article 5 and Article 5.2: "Reserved families (e.g., `fashion`) are intentionally absent from `routing_rules`."

**17.1 Activation path.** Lines 17 and 18 are activated when a new `product_routing_policy` version (v2.0 or later) adds `fashion` to `routing_rules` with defined eligibility flags, tier thresholds, and curator requirements. That version requires second-human approval per the activation protocol.

**17.2 Pre-activation governance.** This standard defines the following preliminary governance for fashion when activated:
- Min CSM tier: STANDARD
- Min commerce tier: tier_2
- Curator always required: false (unless MASTERWORK)
- Additional restriction: fashion products may only use natural history illustration assets (ornithological, botanical, marine) as primary artwork; cultural/figure/portrait subjects require additional review
- Physical product label: institution credit required; NASA nonendorsement required if NASA-sourced; GeoNames attribution NOT required on garment label
- Quality threshold (preliminary): print area image minimum 3000px at intended print size, 200 DPI

**17.3 Timing.** No activation timeline is set. Lines 17 and 18 are ineligible for the NC-PILOT-001 commercial pilot launch.

---

## Part XII — Conditions and Ratification

### Article 18 — Conditions for Full Ratification

| Condition | Description | Blocking |
|---|---|---|
| C-1 | SA-GEONAMES-001 must be ratified by Principal Architect before any geo-anchored product goes live | BLOCKS public launch for all geo-anchored products |
| C-2 | SA-OSM-001 must be ratified by Principal Architect before any product listing displays map tiles | BLOCKS map tile display in listings |
| C-3 | DD-NASA-001 must be formally filed as a ratified document (`docs/decisions/DD-NASA-001_*.md`); until then, NASA assets may enter pipeline under existing institutional knowledge but no new NASA product types may be added without the filed DD | BLOCKS new NASA product type additions |
| C-4 | MIA quality path (full-resolution image availability) must be confirmed in Sprint 1 before MIA assets route to museum_print, archival plate collections, or premium collector bundles | BLOCKS lines 1, 6, 20 for MIA source until Sprint 1 confirms |
| C-5 | Apparel and tote bags (lines 17, 18) require Product Routing Constitution v2.0 activation — no timeline set | BLOCKS lines 17, 18 |

### Article 19 — Decision

**NC-PRODUCT-001 is APPROVED WITH CONDITIONS.** The product line governance framework defined in this document is ratified as of the date of Principal Architect signature. Lines 17 and 18 remain RESERVED. All 18 approved lines are authorized to enter the commercial release pipeline subject to the gates, exclusions, and attribution requirements defined herein.

### Article 20 — Relationship to Other Governing Documents

This document is subordinate to:
```
Strategic Directive
  └─ Illustration Opportunity Doctrine
       └─ IFC v1 (Institution Factory Constitution)
            └─ Product Routing Constitution v1.1
                 └─ NC-PRODUCT-001 (this document)
                      └─ Per-product commerce policy records
```

Any provision of NC-PRODUCT-001 that conflicts with the Product Routing Constitution v1.1 or IFC v1 is void. The routing constitution governs the machine-level routing process; this document governs the commercial activation layer above it.

---

## Ratification Table

| Role | Decision | Date |
|---|---|---|
| Principal Architect | ☐ PENDING | — |
| Governance Review | ☐ PENDING | — |

**Conditions for ratification:**
1. All 5 Article 18 conditions noted
2. Product line registry (Article 1) accepted as canonical mapping to routing families
3. Federal nonendorsement texts (Article 5) accepted as immutable
4. Quality thresholds (Article 13) accepted as minimum gates
5. Takedown protocol (Article 16) accepted as operations-binding

---

*NC-PRODUCT-001 drafted 2026-06-11 under authority of Institution Factory Constitution v1, Product Routing Constitution v1.1, and NC-PILOT-001 Launch Authorization.*
*Reference documents: NC-PILOT-001-LA · DD-NOAA-001 · DD-NARA-001 · DD-MIA-001 · DD-GBIF-001 · DD-WIKIDATA-001 · SA-GEONAMES-001 · SA-OSM-001 · Product Routing Constitution v1.1*
