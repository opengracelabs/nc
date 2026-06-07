# Yellowstone Prototype Specification v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified — implementation target |
| Repository | opengracelabs/nc |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |
| Branch | v0.4.0-collection-000001 |

---

## Preamble

The Yellowstone Prototype is the first public demonstration of the full NC platform
stack. It must prove five things in a single coherent place experience: Place, Map,
Photography, Story, and Commerce. It must not require Audio, Film, 3D, or Dataset.

The prototype is not a feature demonstration. It is a proof of the governance chain.
Every asset visible to a public user must have traversed the complete five-stage pipeline
(Ingest → Rights → Score → Activate → Route) and carry full provenance traceable to a
Library of Congress source record. Any asset that has not completed the chain is not
present in the prototype — it does not appear as "coming soon." It does not exist.

The Hayden Survey (1871) is the constitutional heart of this prototype. Ferdinand Hayden
mapped Yellowstone. William Henry Jackson photographed it. Their work convinced Congress
to create the world's first national park in 1872. The Library of Congress holds both
the maps and the photographs. Every asset in this prototype is from that expedition or
from the place it created.

**Governing constitutions in precedence order:**
1. Strategic Directive (doctrine layer)
2. Universal Media Substrate Constitution v1.2 (asset pipeline)
3. Asset Intelligence Constitution v1.1 (scoring signals)
4. Commerce Intelligence Constitution v1.2 (commerce scoring)
5. Product Routing Constitution v1.1 (product eligibility)
6. Catalog Constitution v1.1 (product variants)
7. Publication Constitution v1.1 (delivery)
8. Relationship & Semantic Intelligence Constitution v1.0 (discovery — Availability Invariant P-2 applies: prototype operates without Neo4j/pgvector)
9. Foundation Model Constitution v1.0 (AI advisory)
10. Wireframe Constitution v1 (information architecture)
11. Standards Constitution v1.0 (data layer interoperability)

---

## Part I — Prototype Identity

### Article 1 — What This Prototype Proves

This prototype must demonstrate:

| Capability | Expression | Constitution |
|---|---|---|
| **Place** | Yellowstone National Park as a canonical NC place with GeoNames ID, PostGIS geometry, and commerce-linked asset gallery | Wireframe v1, Standards v1.0 |
| **Map** | Hayden Survey maps (LOC, 1871) with IIIF viewer, rights badge, quality tier badge, and commerce module | Media Substrate v1.2, IIIF |
| **Photography** | William Henry Jackson photographs (LOC, 1871–1878) with IIIF viewer and commerce module | Media Substrate v1.2 |
| **Story** | NC-authored editorial: "The Survey That Made the First Park" linking place, maps, photographs, and commerce | Wireframe v1, FM v1.0 |
| **Commerce** | At least one active product (wall art) purchasable from the platform | Commerce Intelligence v1.2, Product Routing v1.1 |

### Article 2 — What This Prototype Does Not Prove

Explicitly absent and not required:

| Absent capability | Reason |
|---|---|
| Audio, Film, 3D, Dataset | Phase 2–4 media. Not permitted. No stubs on public pages. |
| Neo4j relationship traversal | SD-AMEND-1 pending. Availability Invariant (P-2) applies. |
| pgvector semantic similarity | SD-AMEND-1 pending. Availability Invariant (P-2) applies. |
| Multi-place asset discovery | Out of scope for v1. Yellowstone is the only place. |
| Creator authority page | Wireframe Constitution OQ-1 deferred to v1.1. |
| Biological-anchored illustration opportunities | BHL ingestion pipeline. Not required for geographic/photography prototype. |
| User accounts, purchasing pipeline | Commercial backend out of scope. "Add to cart" UI + product page is sufficient. |

### Article 3 — Existing Foundation (Migration 18)

The following exists in the database and must not be duplicated or contradicted:

| Entity | State | Location |
|---|---|---|
| LOC registered as source | `governance_state = 'proposed'` | M17 + M18 |
| Yellowstone geographic concept | `status = 'active'`, URI `nc:geo/yellowstone-national-park` | M18 |
| Hayden Survey map candidate | `loc_map_asset_candidates`, `source_record_id = 'loc:97683567'`, `status = 'active'` | M18 |
| Rights evidence for LOC:97683567 | `loc_map_rights_evidence`, `status = 'approved'`, `rights_status = 'Public Domain'` | M18 |
| Asset record | `assets` table, `ingest_id = 'loc_maps:97683567'`, `concept_id = Yellowstone concept` | M18 |

**Critical gap:** M18 uses the `loc_map_asset_candidates` staging table, bypassing the
full Media Substrate pipeline (`source_record` → `source_item` → `media_file` →
`media_rights` → `activation_target`). The prototype must complete this pipeline for
all assets — the staging table is proof-of-concept infrastructure, not production state.
See Article 31 (Launch Blockers).

---

## Part II — Place Specification

### Article 4 — The Yellowstone Place Record

**Canonical place:** Yellowstone National Park

| Field | Value | Standard | Source |
|---|---|---|---|
| GeoNames ID | 5843591 | GeoNames (Adopted, Standards Art. 17) | GeoNames API |
| GeoNames feature code | `PRKA` (park) | GeoNames | GeoNames |
| GeoNames feature class | `L` (parks, areas) | GeoNames | GeoNames |
| Country code | `US` | ISO 3166-1 | GeoNames |
| Admin1 | `WY` (Wyoming) | GeoNames | GeoNames |
| WGS 84 centroid | 44.4280° N, 110.5885° W | RFC 7946 GeoJSON | GeoNames |
| Bounding box | 44.1319° N to 45.1023° N, 111.1570° W to 109.8205° W | RFC 7946 GeoJSON | NPS / PostGIS |
| Alternate names | "Yellowstone", "Parque Nacional Yellowstone", "黄石公园" | GeoNames | GeoNames |
| Wikidata QID | Q351 | Wikidata (Mapped, Standards Art. 16) | Wikidata |
| Schema.org type | `schema:TouristAttraction` + `schema:Place` | Schema.org (Extended, Standards Art. 14) | NC declaration |

**UNESCO World Heritage status:** Yellowstone is a UNESCO World Heritage Site (listed
1978, natural heritage). The `sources.source_id = 'unesco_whc'` already has this record
active in the NC database. The prototype must surface this connection on the place page.

**PostGIS geometry requirement:** Yellowstone's bounding polygon must be stored in the
`places` table with `geom` in SRID 4326. The GeoJSON output of `ST_AsGeoJSON()` must
be valid RFC 7946.

**Place page URL (Wireframe Constitution):**
`/places/north-america/united-states/wyoming/yellowstone`

### Article 5 — Place Page Mandatory Content Zones

Per Wireframe Constitution v1, the Yellowstone place page must contain:

| Zone | Content | Minimum requirement |
|---|---|---|
| Hero asset | Primary Hayden Survey map (LOC:97683567 or the most visually compelling activated map) | 1 asset with IIIF viewer |
| Asset gallery | All activated maps + photographs linked to Yellowstone | ≥ 5 assets |
| Place context | GeoNames feature description, UNESCO WHS status, founding year (1872) | Present |
| Golden Age banner | "Assets from the Golden Age (1750–1900)" with count | Present when applicable |
| Collection CTA | Link to "Yellowstone: The First Survey, 1871" collection | Present |
| Story CTA | Link to the Hayden Survey story | Present |
| Commerce module | Quick-buy for the highest-tier asset | Present |
| Rights badge | PD badge on every asset thumbnail | Mandatory on every appearance |
| Quality tier badge | MASTERWORK / FLAGSHIP / STANDARD / REFERENCE per asset | Mandatory on every appearance |

---

## Part III — Asset Set Specification

### Article 6 — Asset Source: Library of Congress

All prototype assets are sourced exclusively from the Library of Congress. No other
institution is required for the prototype. LOC is a Tier 1 institution
(Media Substrate Constitution v1.2, Part IX, Article 28).

**LOC source governance requirement:** Before any asset enters the production pipeline,
`sources.governance_state` for `source_id = 'loc'` must be advanced from `'proposed'`
to `'active'`. This is a human governance action requiring Director Decision. It is
currently a Launch Blocker (Article 31.1).

**LOC BagIt rule (Media Substrate Constitution v1.2, Article 29.1):** All bulk file
transfers from LOC must be documented with BagIt (RFC 8493) transfer manifests. This
applies to all photography files delivered in bulk.

### Article 7 — Map Assets (Mandatory)

**Asset class:** `map` / `historic_map`
**Anchor type:** `geographic`
**Era:** Golden Age (1871 = 1750–1900 range)
**Expected scoring formula:** `composite_geographic_v1.2` with CI v1.2 signal substitution
**Expected CSM tier:** MASTERWORK (target COS ≥ 0.844 per CI v1.2 historic maps analysis)

**Minimum required: 3 activated maps.**

| Priority | LOC Item | Title | Year | Status |
|---|---|---|---|---|
| P1 — Required | LOC:97683567 | Yellowstone National Park : 1871 | 1871 | M18 candidate — pipeline completion required |
| P2 — Required | TBD — Hayden Survey detail map | Geological and Geographical Survey of the Territories (Yellowstone detail sheet) | 1871–1872 | Sourcing required |
| P3 — Required | TBD — USGS Yellowstone | USGS topographic map, Yellowstone National Park | Pre-1928 | Sourcing required |

**Maps P2 and P3 must be sourced before prototype launch.** The sourcing team must
search LOC Geography and Map Division (`https://www.loc.gov/maps/`) for:
- Search terms: "Yellowstone National Park" + "survey" + date range 1860–1920
- Division filter: Geography and Map Division
- Rights filter: No known restrictions (LOC rights statement)
- Format preference: TIFF master file available; IIIF image service available

**Map pipeline requirements per asset:**
1. `source_record` created from LOC JSON API response
2. `source_item` derived from source_record with `anchor_type = 'geographic'`
3. `media_file` acquired (TIFF master from LOC storage service)
4. `media_rights` record: `rights_status = 'verified_pd'`, `rights_basis = 'publication_date_pre_1928'`, human-verified
5. `preservation_event` sequence: ingestion → fixity_check → format_identification → normalization (JPEG2000) → validation
6. `asset_delivery_manifest` (IIIF Presentation API 3.0)
7. `activation_target`: `status = 'activated'`, second-human approval recorded
8. `commerce_opportunities`: COS computed, CSM tier assigned, signal substitution applied

### Article 8 — Photography Assets (Mandatory)

**Asset class:** `photography` / `historic_photography`
**Anchor type:** `geographic` (landscape/thermal/geological features) OR `biological` (wildlife)
**Primary anchor type for this prototype:** `geographic` — Yellowstone's thermal features,
canyons, and landscapes are the commercial priority. Wildlife photography (bison, elk)
may be included as `anchor_type = 'biological'` but is not required.
**Era:** Golden Age (1871–1878)
**Expected CSM tier:** FLAGSHIP minimum (COS ≥ 0.600)

**Minimum required: 5 activated photographs.**

**Photographer:** William Henry Jackson (1843–1942). Jackson was the official
photographer on Ferdinand Hayden's 1871 United States Geological Survey of
Yellowstone. He is not on NC's Priority Illustrator Registry (that list governs
natural history illustrators, not survey photographers), but his Yellowstone work is
of exceptional historical significance and commercial demand.

**Recommended photography subjects for the prototype:**

| Priority | Subject | Rationale |
|---|---|---|
| P1 | Old Faithful geyser eruption | Highest commercial demand; iconic |
| P2 | Grand Canyon of the Yellowstone | Second most iconic; dramatic landscape |
| P3 | Mammoth Hot Springs terraces | Strong thermal feature; color potential |
| P4 | Lower Falls, Yellowstone | Classic scenic; strong wall art candidate |
| P5 | Grand Prismatic Spring area | Color; thermal feature; contemporary resonance |

**Photography sourcing:** LOC Prints & Photographs Online Catalog
(`https://www.loc.gov/pictures/`). Search terms: "Jackson" + "Yellowstone" + date
range 1870–1910. Also: Detroit Publishing Company collection (post-1895 Jackson
Yellowstone photographs). All items must show "No known restrictions" or equivalent
LOC rights statement.

**Photography pipeline requirements:** Same eight-step pipeline as Article 7. JPEG2000
archival conversion required. IIIF Image API service required for viewer delivery.

### Article 9 — Story Asset (Mandatory)

**Type:** NC-authored editorial content
**Title:** "The Survey That Made the First Park"
**URL:** `/stories/hayden-survey-made-the-first-park`

**Story requirements:**

| Requirement | Rule | Constitution |
|---|---|---|
| Human authorship | NC-authored; FM may generate draft but human editor must substantially revise | FM Constitution v1.0, Art. 11.9 |
| Asset references | Must link to ≥ 2 maps and ≥ 3 photographs by their `/media/{id}` URLs | Wireframe v1 |
| Place reference | Must link to `/places/.../yellowstone` | Wireframe v1 |
| Collection reference | Must link to the "Yellowstone First Survey 1871" collection | Wireframe v1 |
| Commerce contextual | Each asset reference must include a commerce CTA (not just a viewer link) | Wireframe v1, Art. 12 |
| Editorial quality | National Geographic standard (Strategic Direction v1 editorial benchmark) | Strategic Direction v1 |
| JSON-LD | `schema:Article` + `schema:mainEntity` linking to each referenced asset | Standards v1.0, Art. 13.2 |

**Story narrative guidance** (not constitutional — editorial only):
The story recounts the 1871 Hayden Survey: Congress authorized the survey, Hayden
assembled the team including Jackson, the expedition produced the maps and photographs
that documented a wilderness no one in Washington had seen, and in 1872 Congress created
Yellowstone as the world's first national park. The narrative connects every referenced
asset to a specific moment in that story.

### Article 10 — Collection Specification (Mandatory)

**Collection:** "Yellowstone: The First Survey, 1871"
**URL:** `/collections/yellowstone-first-survey-1871`
**Collection type:** `place_collection` + `era_collection`

| Requirement | Value |
|---|---|
| Minimum assets | 5 activated assets (≥ 2 maps + ≥ 3 photographs) |
| Maximum assets (prototype) | 15 |
| Sequence order | Maps first (geographic scope), then photography (ground-level views) |
| Featured asset | Hayden Survey map LOC:97683567 as collection hero |
| CSM tier floor | STANDARD minimum for all included assets (no REFERENCE-only collection) |
| Commerce | Shop CTA visible in collection header and on each asset card |
| Rights | PD badge on every asset card |
| JSON-LD | `schema:Collection` with `schema:hasPart` for each included asset | Standards v1.0 |

---

## Part IV — Mandatory Pages

### Article 11 — Page Inventory

Five page types are mandatory for public launch. These map directly to the Wireframe
Constitution v1 canonical page set (Article 6 of Wireframe Constitution).

| Page | URL | Wireframe Constitution mapping |
|---|---|---|
| **Homepage** | `/` | Homepage spec (Article 7) |
| **Place Page** | `/places/north-america/united-states/wyoming/yellowstone` | Place Page spec (Article 8) |
| **Media Page** (×N) | `/media/{id}` — one per activated asset | Media Page spec (Article 9) |
| **Collection Page** | `/collections/yellowstone-first-survey-1871` | Collection Page spec (Article 10) |
| **Story Page** | `/stories/hayden-survey-made-the-first-park` | Editorial — Wireframe Art. 11 |

An Institution Page for the Library of Congress (`/discover/institution/loc`) is
recommended but not required for public launch. It may be a stub page with: institution
name, description, link to LOC, count of NC assets from LOC.

### Article 12 — Homepage Minimum Requirements

The homepage is the prototype's first impression. For the Yellowstone prototype,
the homepage is Yellowstone-focused. Minimum requirements:

| Zone | Content | Rule |
|---|---|---|
| Featured place | Yellowstone National Park with hero asset | 1 |
| Featured collection | "Yellowstone: The First Survey, 1871" | 1 |
| Featured story | "The Survey That Made the First Park" | 1 |
| Commerce CTA | "Shop Yellowstone" or equivalent | Present |
| L1 Navigation | Places / Discover / Stories / Collections / Shop | Per Wireframe v1 |
| Search | Functional search returning at least place and asset results | Present |
| Rights signal | PD badge visible on every featured asset | Mandatory |
| JSON-LD | `schema:WebSite` + `schema:hasPart` (place, collection, story) | Standards v1.0 |

**Homepage must not:** Show Phase 2–4 media types. Show "coming soon" stubs. Show
raw COS scores or technical scoring data. Show Wikidata QIDs, GeoNames IDs, or other
internal identifiers.

### Article 13 — Media Page Minimum Requirements

Each activated asset has its own `/media/{id}` page. Minimum requirements per page:

| Zone | Content | Rule |
|---|---|---|
| IIIF viewer | Full-screen IIIF viewer (Presentation API 3.0) | Media Substrate v1.2 |
| Rights badge | "Public Domain" badge — prominent, always visible | Wireframe v1, mandatory |
| Quality tier badge | MASTERWORK / FLAGSHIP / STANDARD / REFERENCE | Wireframe v1, mandatory |
| Golden Age badge | Present if publication_year in 1750–1900 | Wireframe v1 |
| Asset metadata | Title, year, creator (Jackson / Hayden Survey), institution (LOC) | DCTERMS (Standards v1.0) |
| Place link | Link to `/places/.../yellowstone` | Wireframe v1 |
| Commerce module | Product variants with pricing and "Add to Cart" | Commerce required |
| Collection link | Link to parent collection if asset is in one | Wireframe v1 |
| Story link | Link to related story if present | Wireframe v1 |
| JSON-LD | `schema:ImageObject` or `schema:Map` + `nc:` heritage extensions | Standards v1.0 |
| IIIF manifest link | `seeAlso` link to resolvable IIIF manifest URL | Standards v1.0 |

**Media page must not:** Show raw COS score. Show `fm_candidate_record` data. Show
`media_rights_id` or internal UUIDs. Show `source_record_id` as a visible identifier.

---

## Part V — Mandatory User Journeys

### Article 14 — Journey 1: Place Discovery

*Entry point: Homepage or external link to place page.*

```
Step 1: Homepage
  → Hero: Yellowstone National Park featured with Hayden Survey map
  → Click: "Explore Yellowstone" CTA or place card

Step 2: Yellowstone Place Page
  → Hero asset: Primary Hayden Survey map (IIIF viewer)
  → PD badge visible ✓
  → MASTERWORK/FLAGSHIP quality tier badge visible ✓
  → Asset gallery: ≥ 5 assets (maps + photographs)
  → Click: A map asset in the gallery

Step 3: Map Media Page
  → IIIF viewer opens at full resolution
  → Rights badge: "Public Domain" ✓
  → Quality tier: "MASTERWORK" (or FLAGSHIP) ✓
  → Golden Age badge: "1871" ✓
  → Commerce module visible: "Buy as Wall Art" option
  → Click: "View Collection"

Step 4: Collection Page
  → "Yellowstone: The First Survey, 1871"
  → Sequence: maps first, then photographs
  → Commerce CTA in header ✓
  → Click: Photography asset

Step 5: Photography Media Page
  → IIIF viewer: Jackson photograph
  → Rights badge, quality badge ✓
  → Commerce module: wall art option
  → Click: "Add to Cart" (or reach product page)

Step 6: Product Page / Cart
  → Size variant selection
  → Price visible
  → Cart functionality (add item)
  → [Journey complete — purchase pipeline out of scope]
```

**Journey 1 success gate:** User can navigate from Homepage to a product page for any
asset in fewer than 5 clicks. Every step shows a rights badge. No dead ends.

### Article 15 — Journey 2: Editorial Discovery

*Entry point: Story page (direct link or discovery through Stories L1 nav).*

```
Step 1: Story page — "The Survey That Made the First Park"
  → NC-authored editorial text
  → Inline asset references with thumbnails (maps + photographs)
  → PD badge on every thumbnail ✓

Step 2: Click inline asset (map or photograph)
  → Media page for that asset
  → IIIF viewer
  → Rights badge + quality tier ✓

Step 3: Commerce module on media page
  → "Buy as Wall Art" visible
  → Click: Product page

Step 4: Product page
  → Add to cart
  → [Journey complete]
```

**Journey 2 success gate:** User reading the story can reach a product page in 2 clicks
from any inline asset reference.

### Article 16 — Journey 3: Commerce Direct

*Entry point: Any media page (direct URL, search result, or referral).*

```
Step 1: Any media page (/media/{id})
  → IIIF viewer loaded
  → Rights badge: "Public Domain" ✓
  → Quality tier badge visible ✓
  → Commerce module: product options visible

Step 2: Commerce module
  → At least 1 product type available: Wall Art
  → Size options: minimum 3 variants (e.g., 8"×10", 16"×20", 24"×30")
  → Price displayed
  → Click: "Add to Cart"

Step 3: Cart confirmation
  → Asset image, title, size, price in cart
  → [Journey complete]
```

**Journey 3 success gate:** User landing directly on a media page can add a product to
cart in 1 click. No navigation through the place or collection is required.

### Article 17 — Journey 4: Search Discovery

*Entry point: Search bar from any page.*

```
Step 1: Search input
  → Query: "Yellowstone" or "Hayden Survey" or "Old Faithful"

Step 2: Search results
  → Place result: Yellowstone National Park ✓
  → Asset results: maps and photographs ✓
  → Collection result: "Yellowstone: The First Survey, 1871" ✓
  → Story result: "The Survey That Made the First Park" ✓

Step 3: Click any result
  → Navigates to the correct page type
  → [Journey merges with Journeys 1–3 from that page]
```

**Journey 4 success gate:** Search for "Yellowstone" returns at least one result from
each of: place, asset, collection, story. Search infrastructure requirement: pg_trgm
(already in `00_extensions.sql`). No Neo4j or pgvector required.

---

## Part VI — Governance Requirements

### Article 18 — Media Substrate Constitution v1.2 Requirements

Every activated asset must have completed all pipeline stages. No exceptions.

| Requirement | Constitutional basis | Applies to |
|---|---|---|
| `source_record` from LOC JSON API | Art. 5.2 | All assets |
| `source_item` derived from source_record | Art. 5.3 | All assets |
| `media_file` acquired (TIFF master from LOC storage service) | Art. 6 | All assets |
| BagIt transfer manifest for bulk file delivery | Art. 29.1 (LOC institution rule) | Photography batch |
| `media_rights.rights_status = 'verified_pd'` | Art. 7, Invariant R-2 | All assets |
| `media_rights.rights_basis = 'publication_date_pre_1928'` | Art. 7.3 | All 1871–1878 assets |
| Human rights verifier recorded in `media_rights.verified_by` | Art. 7.5 | All assets |
| `preservation_event` sequence: ingestion → fixity → format_identification → normalization → validation | Art. 13 | All assets |
| TGM subject terms in `media_technical_metadata.content.subject_terms` | Art. 29.1 (LOC TGM rule) | All assets |
| `asset_delivery_manifest` (IIIF Presentation API 3.0) | Art. 10 | All activated assets |
| `activation_target.status = 'activated'` | Art. 14 | All public assets |
| Second-human approval for activation | Art. 25.2 (Media Substrate) | All activations |
| `activation_target.media_rights_id_at_approval` captured at approval | Art. 14.9 | All activations |

### Article 19 — Asset Intelligence Constitution v1.1 Requirements

| Requirement | Constitutional basis |
|---|---|
| `anchor_type = 'geographic'` for all maps and landscape photography | M32 schema + CI v1.2 |
| `anchor_type_verified_by` and `anchor_type_verified_at` set | M32 constraint |
| `illustration_opportunity_places` link: all assets → Yellowstone, `relevance_score = 1.00` | Asset Intelligence |
| `place_relevance_score` in `commerce_opportunities` computed from the place link | Commerce Intelligence v1.2 |
| LOC `institutional_credit` factor recorded in `commerce_opportunities` | Asset Intelligence v1.1 |
| `golden_age_factor` = 1.0 for all 1871 assets | Asset Intelligence v1.1 |

### Article 20 — Commerce Intelligence Constitution v1.2 Requirements

| Requirement | Constitutional basis |
|---|---|
| `signal_substitutions: {"taxon_commercial_tier_score": "place_relevance_score"}` active in `anchor_weight_spec.geographic` | CI v1.2, Amendment G-3 |
| `commerce_opportunity_score` computed for all activated assets | CI v1.2 |
| `csm_tier` assigned for all activated assets | CI v1.2 |
| Maps must achieve minimum `csm_tier = 'flagship'` (COS ≥ 0.600) | Prototype gate |
| `hard_gate_status = 'pass'` for all activated assets | CI v1.2, Art. 4 (rights gate) |
| `score_audit_log` entries for all score computations | CI v1.2 |

### Article 21 — Product Routing and Catalog Requirements

| Requirement | Constitutional basis |
|---|---|
| At least 1 product route active per activated asset | Product Routing v1.1 |
| `product_type = 'wall_art'` available for all MASTERWORK/FLAGSHIP assets | Product Routing v1.1 |
| Minimum 3 size variants per wall art product | Catalog v1.1 |
| Pricing published for all active products | Catalog v1.1 |
| Product page accessible at `/shop/...` or equivalent | Wireframe v1, Commerce layer |

### Article 22 — Standards Constitution v1.0 Requirements

| Requirement | Standard | Rule |
|---|---|---|
| GeoNames ID (5843591) recorded for Yellowstone place | GeoNames (Adopted) | Art. 17 |
| PostGIS geometry (bounding polygon) stored for Yellowstone | GeoJSON (Adopted) | Art. 12 |
| GeoJSON output from place API endpoint valid per RFC 7946 | GeoJSON | Art. 12 |
| Schema.org/TouristAttraction structured data on place page | Schema.org (Extended) | Art. 14 |
| Schema.org/ImageObject or Map structured data on all media pages | Schema.org | Art. 14 |
| `schema:Product` + `schema:Offer` structured data on all product pages | Schema.org | Art. 14 |
| JSON-LD `@context` on all entity API responses | JSON-LD (Adopted) | Art. 13 |
| IIIF manifests well-formed and resolvable | IIIF (Extended) | Art. 10 |
| DCTERMS metadata complete for all source_items | Dublin Core (Adopted) | Art. 7 |
| Wikidata QID recorded for Yellowstone place (Q351) | Wikidata (Mapped) | Art. 16 |
| `nc:commerce_context` extension present in all IIIF manifests | IIIF Extension v1.0 | Part IV Art. 19 |

### Article 23 — Foundation Model Constitution v1.0 Requirements

Foundation Models are permitted in the prototype preparation workflow for the following
governed use cases only:

| Use case | Purpose | Promotion path |
|---|---|---|
| `subject_term_classification` | Suggest TGM subject terms for LOC assets | Auto-apply at confidence ≥ 0.92, or human review queue |
| `anchor_type_classification` | Confirm `anchor_type = 'geographic'` for maps and landscape photography | Auto-apply at confidence ≥ 0.96 |
| `editorial_content_assistance` | Draft text for the Hayden Survey story | Human editor must substantially revise. FM draft is NOT publishable. |

**FM requirements:**
- All FM calls produce `fm_inference_record` entries
- `rights_analysis_advisory` may be used as advisory context for human rights verifier — FM output must be labeled "Advisory only" and may not set `media_rights.rights_status`
- No FM output directly enters `commerce_opportunities` scoring fields (FM-5 Score Gate)

---

## Part VII — Commerce Requirements

### Article 24 — Commerce Minimum Viable Set

**Minimum viable commerce for public launch:**

| Product | Asset | Variants | Required |
|---|---|---|---|
| Wall Art — Hayden Survey Map | LOC:97683567 (primary Hayden map) | 3 sizes minimum | Required |
| Wall Art — Hayden Survey map (2nd) | Second map asset (P2 from Article 7) | 3 sizes minimum | Required |
| Wall Art — Jackson photograph | Best-scoring Jackson photograph | 3 sizes minimum | Required |

**Total minimum:** 3 products × 3 size variants = 9 active product variants.

**Price structure (from Catalog v1.1):** The catalog constitution governs pricing tiers.
Pricing is set per CSM tier. For MASTERWORK assets: premium tier. For FLAGSHIP: standard
tier. Specific prices are a Director Decision not subject to this Constitution.

### Article 25 — Commerce Scoring Targets

The following COS targets are based on CI v1.2 historic maps analysis (Signal
Substitution G-3):

| Asset type | Expected COS | Expected CSM tier | Launch gate |
|---|---|---|---|
| Hayden Survey map (1871, LOC, geographic anchor) | ≥ 0.80 | MASTERWORK | Minimum FLAGSHIP (0.60) |
| Jackson photograph (1871–1878, LOC, geographic anchor) | ≥ 0.60 | FLAGSHIP | Minimum FLAGSHIP (0.60) |
| Secondary map / USGS (pre-1928, LOC, geographic anchor) | ≥ 0.60 | FLAGSHIP | Minimum STANDARD (0.40) |

**Commerce hard gate:** No asset enters any product page with `hard_gate_status != 'pass'`.
The hard gate requires `media_rights.rights_status = 'verified_pd'` AND
`activation_target.status = 'activated'`. These are non-negotiable.

### Article 26 — Commerce UI Requirements

Per Wireframe Constitution v1:

| Requirement | Rule |
|---|---|
| Commerce contextual on every page | Not siloed to /shop only |
| Raw COS score never shown | Wireframe v1, Art. 17 |
| Quality tier shown as badge label only (MASTERWORK/FLAGSHIP/STANDARD/REFERENCE) | Wireframe v1 |
| Rights badge always accompanies every commercial asset presentation | Wireframe v1, mandatory |
| Product price displayed before checkout | Wireframe v1, Commerce hierarchy |
| "Add to Cart" reachable in ≤ 2 clicks from any media page | Journey 3 gate |

---

## Part VIII — Minimum Success Criteria

### Article 27 — Functional Criteria (must pass all)

| # | Criterion | Measurement |
|---|---|---|
| F-1 | Yellowstone Place Page loads with ≥ 1 hero asset | Manual verification |
| F-2 | ≥ 2 maps have functioning IIIF viewers (zoom, pan, full-screen) | Manual verification |
| F-3 | ≥ 3 photographs have functioning IIIF viewers | Manual verification |
| F-4 | Collection page displays ≥ 5 assets with correct sequence (maps first) | Manual verification |
| F-5 | Story page is accessible and links to ≥ 2 maps + ≥ 3 photographs | Manual verification |
| F-6 | Search "Yellowstone" returns ≥ 1 result from each of: place, asset, collection, story | Manual verification |
| F-7 | Every asset on every page shows a rights badge (PD) — zero exceptions | Manual QA sweep |
| F-8 | Every media page shows a quality tier badge — zero exceptions | Manual QA sweep |
| F-9 | At least 1 product can reach "Add to Cart" state from a media page | Manual verification |
| F-10 | Phase 2–4 stubs are absent from all public pages | Manual QA sweep |

### Article 28 — Commerce Criteria (must pass all)

| # | Criterion | Measurement |
|---|---|---|
| C-1 | ≥ 3 activated assets have `csm_tier` ≥ FLAGSHIP | Database query |
| C-2 | Signal substitution `taxon_commercial_tier_score → place_relevance_score` active for all geographic-anchor assets | Database query: `commerce_opportunities.score_inputs.signal_substitutions` |
| C-3 | No product page shows an asset with `hard_gate_status != 'pass'` | Database query |
| C-4 | All active products have pricing published | Catalog query |
| C-5 | Raw COS scores are not exposed on any public page | Frontend audit |

### Article 29 — Governance Criteria (must pass all)

| # | Criterion | Measurement |
|---|---|---|
| G-1 | Every activated asset has a complete provenance chain: source_record → source_item → media_file → media_rights → activation_target | Database query: left join completeness check |
| G-2 | Every activated asset has `media_rights.rights_status = 'verified_pd'` with a human verifier recorded | Database query |
| G-3 | Every activated asset has `activation_target` with second-human approval recorded | Database query |
| G-4 | Every activated asset has ≥ 5 `preservation_event` entries (ingestion, fixity, format_id, normalization, validation) | Database query |
| G-5 | LOC `governance_state = 'active'` (upgraded from 'proposed') | Database query |
| G-6 | Replay is possible for all governance decisions: provenance chain traceable end-to-end | Director audit |

### Article 30 — Technical Criteria (must pass all)

| # | Criterion | Measurement |
|---|---|---|
| T-1 | All IIIF manifests validate against IIIF Presentation API 3.0 | IIIF Validator |
| T-2 | JSON-LD present and valid on all 5 page types | JSON-LD Validator + Chrome DevTools |
| T-3 | Schema.org `schema:Product` + `schema:Offer` markup present on all product pages | Google Rich Results Test |
| T-4 | `schema:TouristAttraction` markup present on Yellowstone place page | Google Rich Results Test |
| T-5 | GeoJSON from place API endpoint validates per RFC 7946 | GeoJSON validator |
| T-6 | NC IIIF commerce extension (`nc:commerce_context`) present in all activated manifests | Manifest audit |
| T-7 | No 404s or broken links in any of the 4 mandatory user journeys | Link checker |

---

## Part IX — Launch Blockers

### Article 31 — Blockers That Must Be Resolved Before Public Launch

Any unresolved blocker is a constitutional violation of the relevant constitution. There
is no waiver process. The prototype does not launch with an unresolved blocker.

**Blocker 31.1 — LOC Source Governance Gate (Media Substrate v1.2)**
`sources.governance_state = 'proposed'` for `source_id = 'loc'`. LOC must be advanced
to `governance_state = 'active'` via a Director Decision before any LOC asset can enter
the production pipeline. This is the most upstream blocker.
*Action: Director Decision DD-LOC-001 required.*

**Blocker 31.2 — M18 Pipeline Gap (Media Substrate v1.2)**
The Hayden Survey map in `loc_map_asset_candidates` was created via the M18 staging
table, bypassing the full Media Substrate pipeline (source_record → source_item →
media_file → media_rights → activation_target). The full pipeline must be completed
for LOC:97683567 and all prototype assets before launch.
*Action: Migration 36 (Media Substrate pipeline completion) + worker pipeline run.*

**Blocker 31.3 — Photography Assets Not Sourced (Article 8)**
Minimum 5 William Henry Jackson photographs must be identified, sourced, and ingested.
Sourcing research has not yet been completed.
*Action: Research LOC Prints & Photographs collection. Identify ≥ 5 items. Ingest.*

**Blocker 31.4 — Map Assets P2 and P3 Not Sourced (Article 7)**
Only 1 of the 3 required maps has been identified (LOC:97683567). Two additional maps
are required.
*Action: Source 2 additional Hayden Survey or USGS Yellowstone maps from LOC.*

**Blocker 31.5 — Yellowstone Place Record Not in `places` Table**
The current `places` table (via `01_tables.sql`) may not have a Yellowstone record with
GeoNames ID, PostGIS geometry, and Wikidata QID. The concept `nc:geo/yellowstone-national-park`
exists in `concepts` (M18) but the `places` table is the canonical entity for the
Wireframe Constitution place page.
*Action: Insert Yellowstone into `places` with GeoNames ID 5843591, geometry (bounding
polygon from NPS or GeoNames), Wikidata QID Q351.*

**Blocker 31.6 — Commerce Scoring Not Computed**
No `commerce_opportunities` records exist for LOC map assets. Signal substitution G-3
(CI v1.2) must be active and scoring must be run before commerce UI can be rendered.
*Action: Run scoring worker against all activated map/photography illustration_opportunities.*

**Blocker 31.7 — Rights Verification Not Completed by Human Verifier**
M18 created `loc_map_rights_evidence` records with `requires_human_review = TRUE` and
`status = 'approved'` — but the approval was done programmatically, not by a human
verifier. The Media Substrate Constitution requires a human rights verifier for
`media_rights.rights_status = 'verified_pd'`.
*Action: Human rights verifier must review and approve all prototype assets. Records
`media_rights.verified_by` must be populated with a human identity.*

**Blocker 31.8 — Second-Human Activation Approval Not Recorded**
No activation_target records exist for LOC assets (the pipeline was not completed — see
31.2). When the pipeline is completed, each activation_target requires second-human
approval.
*Action: After pipeline completion, Director plus second human must approve each
activation_target.*

**Blocker 31.9 — Story Not Written**
The Hayden Survey story ("The Survey That Made the First Park") has not been written.
It requires human authorship after assets are activated.
*Action: Human editor writes story. FM advisory may generate a draft. Human must
substantially revise before publication.*

**Blocker 31.10 — Collection Not Created**
"Yellowstone: The First Survey, 1871" collection has not been created. Collection
requires activated assets before it can be published.
*Action: After assets are activated, human curator creates collection with editorial
sequence.*

---

## Part X — Out of Scope

### Article 32 — Explicitly Excluded from the Prototype

| Item | Why excluded | When to add |
|---|---|---|
| Audio, Film, 3D, Dataset assets | Phase 2–4 per Media Substrate Constitution v1.2 | P2-1 / P3-1 / P4-1 amendments |
| Neo4j relationship traversal | SD-AMEND-1 required. Availability Invariant P-2 applies. | After SD-AMEND-1 |
| pgvector "More like this" discovery | SD-AMEND-1 required. | After SD-AMEND-1 |
| Creator authority page (William Henry Jackson) | Wireframe Constitution OQ-1 deferred | Wireframe v1.1 |
| Thomas Moran fine art (Smithsonian source) | Smithsonian ingestion pipeline not built | Future milestone |
| Biological-anchored illustration opportunities | BHL pipeline; different anchor type | Future biological prototype |
| User authentication, purchase pipeline | Out of scope for prototype | v0.6.x Products milestone |
| Multi-place routing (Grand Teton as related place) | Out of scope; single-place prototype | After R&SI Constitution SD-AMEND-1 |
| B2B licensing tier | Era 2 commerce; not prototype scope | Strategic Direction v1, Era 2 |
| Tourism attraction score computation | TAS scoring not yet implemented | Future milestone |
| Mobile application | Not in scope | Future milestone |

---

## Open Questions

| OQ | Question | Recommended resolution |
|---|---|---|
| OQ-1 | Should William Henry Jackson be added to the Priority Illustrator Registry? | Jackson is a photographer, not a natural history illustrator. The Priority Illustrator Registry (Audubon, Gould, et al.) governs scientific illustration. Jackson's commercial prestige in the photography domain warrants a parallel "Priority Photographer Registry" — proposed as an Asset Intelligence Constitution v1.2 amendment rather than modifying the existing list. |
| OQ-2 | Should the Yellowstone concept in `concepts` table be migrated to the `places` table, or should both records coexist? | The `concepts` record (`nc:geo/yellowstone-national-park`) anchors existing illustration_opportunities. The `places` record is needed for the Wireframe place page. Both must exist and be linked. A `concept_place_link` table or a `concept_id` FK on `places` is required. This is a schema design decision for Migration 36 or a standalone migration. |
| OQ-3 | Should the LOC Institution Page be required for launch? | Recommended: required as a stub. LOC is the sole source institution for the prototype. The Institution page is constitutionally defined in Wireframe v1. A stub with institution name, description, LOC URL, and asset count satisfies the requirement. Full institution page (editorial content, source governance history) deferred. |
| OQ-4 | Should the prototype include USGS Yellowstone maps (post-1871, pre-1928) as a third map tier alongside the Hayden Survey maps? | Recommended: Yes. USGS Yellowstone topographic surveys from 1878–1920 are at LOC. They provide geographic detail the 1871 Hayden map doesn't have. They extend the collection's spatial completeness and provide additional commerce-ready assets. Same LOC ingestion pipeline applies. |
| OQ-5 | What is the minimum viable search implementation? | pg_trgm trigram search over `source_item.title`, `places.name`, `collections.title`, `stories.title`. No Neo4j/pgvector required. GIN index on relevant text columns (`06_search.sql` already in migrations). The search must return results from all four entity types. A single PostgreSQL UNION query is sufficient for the prototype. |
