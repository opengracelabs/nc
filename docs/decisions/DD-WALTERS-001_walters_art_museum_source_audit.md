# DD-WALTERS-001 — Walters Art Museum Open Data Source Audit

| Field | Value |
|---|---|
| **Decision ID** | DD-WALTERS-001 |
| **Type** | Source Audit |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-09 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first Walters governance document |
| **Governing Documents** | Institution Coverage Audit v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 · Institution Factory v1 · SA-14 (CSV Bulk Download Ingestion Protocol) |

---

## Background

The Walters Art Museum in Baltimore, Maryland holds approximately 36,000 works spanning
5,000 years across every inhabited continent. The museum's collections are distinguished
by extraordinary depth in illuminated manuscripts (medieval European, Byzantine, and
Islamic), Byzantine icons and metalwork, ancient Egyptian and Near Eastern material,
Islamic world art, Asian art, and arms and armour. These collecting areas represent
significant gaps in NC's current pipeline — no existing NC institution provides meaningful
illuminated manuscript content, Byzantine art, or pre-modern Islamic manuscript
illustration at any volume.

The Walters provides open data through a GitHub repository
(`github.com/WaltersArtMuseum/api-thewalters-org`) containing six CSV tables updated
periodically from the museum's collections management system. The institution's CC0
declaration is explicit and unconditional: *"The data and images are made available to the
public under a CC0 license that facilitates reuse, even for commercial purposes."*

**This Decision is not responding to a Must Add mandate** from the Institution Coverage
Audit v1.0 (which listed NHM London, BnF/Gallica, Wellcome, Trove, HathiTrust). It
responds to an opportunity identified in the audit session: the Walters fills a manuscript
illustration gap — a product category NC cannot address from any currently approved or
in-pipeline institution — with a clean CC0 commercial posture, no platform fee, and a
CSV-based ingestion architecture directly analogous to NGA (Institution #12).

**The governing answer to "Can Walters be approved as a production source?":**

**Yes — unconditionally.** The CC0 designation is explicit and institution-wide. The
policy text specifically invokes commercial reuse. There is no per-asset fee, no platform
ToS commercial restriction, and no license agreement requirement. Walters passes NC's
production-source commercial reuse requirement at every layer.

This Decision presents five governance characteristics that differentiate Walters from all
prior institutions:

1. **Institution-wide CC0 — new rights class.** Walters' CC0 designation applies to the
   entire dataset, not to individual records via a per-record flag. There is no
   `openaccess`, `isPublicDomain`, or `share_license_status` field. All 21,877 object
   records in the CSV dataset are CC0 by institutional declaration. Rights classification
   reduces to: does the record exist and does it have a usable image URL? This is the
   **sixth distinct rights class** in NC's pipeline.

2. **CSV bulk download — inherits SA-14.** Like NGA, Walters has no publicly accessible
   REST collection API (the v1 API retired in 2023; v2 is under development with no
   release timeline). The authorised ingestion path is CSV bulk download from GitHub.
   SA-14 (CSV Bulk Download Ingestion Protocol, drafted for NGA) governs the generic
   parameters; Walters-specific schema bindings are in SA-15.

3. **No IIIF — direct JPEG delivery.** Walters provides no IIIF Image API and no IIIF
   Presentation manifests. Images are direct JPEG URLs in `media.csv.ImageURL`. No SA-3
   analogue is required. `representative_media_url` equals the ImageURL directly.

4. **Primary image via `IsPrimary` integer flag.** Primary image selection uses
   `media.csv.IsPrimary = 1` (integer flag on the image record), falling back to `Rank ASC`
   if multiple IsPrimary = 1 records exist or if no primary is marked. This is distinct
   from NGA's `viewtype = "primary"` + sequence sort and does not inherit NGA's client.

5. **Pipe-delimited sub-fields.** Several `art.csv` fields contain pipe-delimited
   (`|`) lists: `Images` (image filenames), `CollectionID` (3-letter collection codes),
   `CollectionName` (collection display names), `Creators` (creator IDs). The adapter must
   split these before use. The `media.csv` join is authorised over the `art.csv.Images`
   field for image URL retrieval (media.csv provides the full `ImageURL` directly).

---

## Part I — Source Classification Audit

**Institution name:** Walters Art Museum

**Location:** Baltimore, Maryland, United States

**Institution type:** Private non-profit art museum (city-museum partnership)

**Open access programme:** CC0 1.0 Universal via GitHub open data repository. Policy
text: *"The data and images are made available to the public under a CC0 license that
facilitates reuse, even for commercial purposes."*

**Commercial reuse status:** PERMITTED WITHOUT FEE — explicitly.

**API status:** API v1 retired 2023 (server end-of-life; GitHub issue "API v1 is offline"
open). API v2 under development, no public release timeline. The GitHub CSV repository
is the sole publicly available, maintained data interface.

**Primary data access:** GitHub repository `github.com/WaltersArtMuseum/api-thewalters-org`
— six CSV tables, periodically updated from TMS. Raw file base URL:
`https://raw.githubusercontent.com/WaltersArtMuseum/api-thewalters-org/main/`

**Key tables:**

| Table | Records | Purpose |
|---|---|---|
| `art.csv` | 21,877 | Primary object metadata |
| `media.csv` | 46,371 | Image records with direct URLs |
| `collections.csv` | 24 | Collection category definitions |
| `creators.csv` | — | Artist/maker records |
| `exhibitions.csv` | — | Exhibition records |
| `relationships.csv` | — | Multi-object relationship pairs |

**IIIF:** Not provided. No IIIF Image API. No Presentation manifests. No SA-3 analogue
required.

**Authentication:** None required for CSV download or image URLs. Public access.

**NC institution tier:** Tier 1 Core — CC0, direct, no aggregator intermediary.

**Proposed institution number:** #13

**Proposed source ID:** `walters`

**Proposed source priority:** 14

**Differentiating commercial strengths:**
- **Illuminated manuscripts** — NC's first manuscript illustration content. Medieval
  European, Byzantine, and Islamic manuscripts with figurative scenes, decorated borders,
  zoological and botanical marginalia. No other NC institution provides this category.
- **Byzantine art** — Icons, metalwork, manuscript illumination from Byzantium and Early
  Russia. NC's first Byzantine content. Fills Constantinople/Istanbul place pages.
- **Islamic manuscripts** — Quranic manuscripts, scientific illustrations, botanical
  manuscript pages. Fills NC's Islamic world gap.
- **Ancient Egypt** — Statuary, papyri, decorated objects. Supplemental to Met;
  different objects.
- **Medieval European metalwork and arms** — Religious objects, armour, metalwork.
  Fills NC's medieval European gap.
- **Asian art** — China, Japan/Korea, India, Southeast Asia collections supplemental to
  Met/SMK/NGA (different physical objects).

**Primary commercial gap addressed:** Illuminated manuscript illustration pipeline —
a product category unavailable from any current or in-pipeline NC institution.

---

## Part II — Rights Strategy Audit

### II.1 — Commercial Reuse Qualification

| Layer | Walters Position | Compatible? |
|---|---|---|
| Copyright | CC0 1.0 — all rights waived | YES |
| Platform policy | "facilitates reuse, even for commercial purposes" | YES |
| Per-asset fee | None | YES |
| License agreement | None required | YES |
| Attribution requirement | None (CC0; museum requests citation as best practice only) | YES |
| Platform ToS commercial restriction | None | YES |

**Walters is approved as a production source.**

### II.2 — Can Walters Inherit Any Prior Rights Matrix?

**Answer: No.**

Walters' rights architecture is distinct from all five prior rights classes:

| Class | Institution(s) | Rights field |
|---|---|---|
| URI-form | Europeana, Rijksmuseum | Compare field to allowlist URI |
| Boolean-object-form | Met, AIC, SMK | `field is True` on object record |
| String-equality-form | CMA | `field == "CC0"` on object record |
| API-tier-guarantee | Paris Musées | API-level rights promise |
| Image-record integer-flag | NGA | `image_record["openaccess"] == 1` |
| **Institution-wide CC0** | **Walters** | **No per-record field; entire dataset is CC0** |

Walters introduces the **sixth distinct rights class**: institution-wide CC0. There is no
rights field to check on any record. All records in the CSV dataset carry CC0 by
institutional declaration. Rights classification is purely a data completeness check: does
a valid object record exist, and does it have a usable image URL?

A new **Walters Rights Matrix v1** (`policy_id: "walters_rights_matrix_v1"`) is required.

### II.3 — Walters Rights Matrix v1 Classification Rules

Rights classification is performed on the joined row (object record + primary image record),
where the join condition is `media.ObjectID = art.ObjectID` and `media.IsPrimary = "1"`.

| Rule ID | Condition | Outcome | rights_basis |
|---|---|---|---|
| WLT-R-1 | `object_row` is not a dict | BLOCKED | `missing_object_record` |
| WLT-R-2 | `image_row` is None (no image record for this object) | BLOCKED | `no_image_record` |
| WLT-R-3 | `image_row.get("ImageURL")` is None or empty | BLOCKED | `missing_image_url` |
| WLT-R-4 | All prior rules pass | ALLOWED | `walters_institution_cc0` |

**ALLOWED outcome:**
- `decision`: ALLOWED
- `rights_statement_uri`: CC0_URI
- `rights_status`: `"pending_verification"` (CI-4 ceiling)
- `rights_policy_id`: `"walters_rights_matrix_v1"`

**No REVIEW_REQUIRED class.** Every record is ALLOWED or BLOCKED.

### II.4 — Rights Evidence Requirements (SC-7)

Additional fields in `media_rights.rights_evidence` for all Walters records:
- `walters_object_id` (str) — verbatim `art_row["ObjectID"]`
- `walters_object_number` (str) — verbatim `art_row.get("ObjectNumber")`
- `walters_media_xref_id` (str) — verbatim `media_row["MediaXrefID"]`
- `walters_image_url` (str) — verbatim `media_row["ImageURL"]`
- `walters_is_primary` (str) — verbatim `media_row.get("IsPrimary")`

### II.5 — Shared Store Extension (Sprint 3 Prerequisite)

`build_rights_evidence` in `shared_media_adapter/store.py` must extend the remap set to
include `"walters"` before Walters Sprint 3. The remap set currently covers
`{"met", "aic", "cma", "smk", "nga"}`. Adding `"walters"` makes six institutions.
SA-9 must be updated to cover Walters before Sprint 3 begins.

---

## Part III — Data Access Audit

### III.1 — Ingestion Architecture Overview

Walters ingestion follows the SA-14 CSV bulk download paradigm established for NGA:

```
1. Download CSV tables from GitHub (periodic full refresh)
2. Build in-memory join: art + media + creators
3. Filter: media.IsPrimary = 1 (one primary image per object)
4. Sort: by art.ObjectID ASC (CI-8 determinism)
5. For each joined row: classify rights, normalize, write to M36
6. Fetch image directly via media.ImageURL
```

**Key difference from NGA:** Image delivery is a direct JPEG HTTP GET, not IIIF URL
construction. `representative_media_url = media_row["ImageURL"]` verbatim.

SA-14 governs the generic CSV bulk download protocol. Walters-specific schema bindings
(field names, join keys, primary image selection, collection code parsing) are in SA-15.

### III.2 — CSV Table Reference URLs

| Table | Raw URL |
|---|---|
| `art.csv` | `.../main/art.csv` |
| `media.csv` | `.../main/media.csv` |
| `collections.csv` | `.../main/collections.csv` |
| `creators.csv` | `.../main/creators.csv` |
| `exhibitions.csv` | `.../main/exhibitions.csv` |
| `relationships.csv` | `.../main/relationships.csv` |

Base URL: `https://raw.githubusercontent.com/WaltersArtMuseum/api-thewalters-org/main/`

Required tables for Sprint 1: `art.csv`, `media.csv`, `creators.csv`. The remaining three
tables (`collections.csv`, `exhibitions.csv`, `relationships.csv`) are optional enrichment.

### III.3 — Field Names (Exact CSV Headers)

**`art.csv`** (camelCase — Walters CSV uses camelCase unlike NGA's all-lowercase):

| Field | Type | Notes |
|---|---|---|
| `ObjectID` | integer | Primary key; persistent unique identifier |
| `ObjectNumber` | string | Accession number (e.g., "37.677", "W.854") |
| `ObjectName` | string | Object type (sword, painting, mummy, etc.) |
| `Title` | string | Object title |
| `DateBeginYear` | integer | Creation start year; negative = BCE |
| `DateEndYear` | integer | Creation end year; negative = BCE |
| `DateText` | string | Human-readable period (e.g., "late 5th century BCE") |
| `Medium` | string | Materials and process |
| `Style` | string | Art style, historical period, movement |
| `Culture` | string | Civilization of origin |
| `Classification` | string | Broad type (Metal, Ceramics, Manuscripts, etc.) |
| `Description` | string | Plaintext description |
| `Provenance` | string | Ownership/custody chronology |
| `CreditLine` | string | Acquisition credit |
| `Dynasty` | string | Historical dynasty (ancient objects) |
| `GeographyID` | integer | FK to geography data (not in current CSV files) |
| `ResourceURL` | string | Museum page URL |
| `Images` | string | **Pipe-delimited** image filenames (use `media.csv` instead) |
| `CollectionID` | string | **Pipe-delimited** 3-letter collection codes |
| `CollectionName` | string | **Pipe-delimited** collection display names |
| `Creators` | string | **Pipe-delimited** creator IDs (join to `creators.csv`) |
| `RelatedObjects` | string | Pipe-delimited related ObjectIDs |

**`media.csv`:**

| Field | Type | Notes |
|---|---|---|
| `ObjectID` | integer | FK to `art.csv`; join key |
| `MediaXrefID` | integer | Unique image identifier |
| `ImageURL` | string | Full direct HTTP URL to JPEG image |
| `Filename` | string | Image filename only |
| `MediaType` | string | "Image" (filter to this value) |
| `MediaView` | string | View code (Front, Back, Fnt, Rev, Det, etc.) |
| `Rank` | integer | Display order; lower = higher priority |
| `IsPrimary` | integer | 1 = primary/thumbnail image; 0 = alternate |

**`creators.csv`:**

| Field | Type | Notes |
|---|---|---|
| `id` | integer | Creator ID; matches values in `art.csv.Creators` |
| `name` | string | Display name |
| `sort_name` | string | Surname-first format |
| `date` | string | Birth–death years |
| `nationality` | string | Creator nationality (if present) |

### III.4 — Join Strategy

**Primary join (required):**
`media.ObjectID = art.ObjectID` WHERE `media.MediaType = "Image"`

**Primary image selection:**
1. Among matching media rows for one object: filter `IsPrimary = "1"`
2. If multiple IsPrimary = "1" rows: take the one with lowest `Rank` (ascending integer)
3. If no IsPrimary = "1" row: take the row with lowest `Rank` among all `MediaType = "Image"` rows
4. If no media row at all: BLOCKED by WLT-R-2

**Creator join (required for anchor type and creator field):**
1. Split `art.Creators` on `|` to get creator ID list
2. For each ID: look up `creators.csv` by `id`
3. Take first matched creator for `creator` field; take all nationalities for anchor type

**Collection code parsing:**
Split `art.CollectionID` on `|` to get a list of 3-letter codes. These are used for
anchor type derivation (see Article 5).

### III.5 — Enumeration and Replay Determinism

Primary enumeration: filter `art.csv` rows that have at least one `MediaType = "Image"`
row in `media.csv`. Sort by `art.ObjectID ASC` (integer, ascending). One M36 record per
`ObjectID`. Required for CI-8 replay determinism.

### III.6 — CSV Freshness and Update Cadence

The GitHub repository does not update on a daily cadence (unlike NGA). The last
substantive data update was 2025-07-07 (~11 months before this Decision). The adapter
must:
- Log download timestamp in `preservation_event`
- Apply a staleness guard of **30 days** (vs NGA's 7 days) reflecting Walters' slower
  update cadence
- Refuse ingestion if any required CSV has a `Last-Modified` older than 30 days

Gate 3 must confirm the actual update frequency and adjust the staleness guard if needed.

### III.7 — API v2 Risk

The Walters is developing API v2 (no release timeline). If v2 launches during NC's
Walters adapter lifecycle, it may supersede the CSV-based path. The Sprint 1 adapter
must be designed to allow a future REST-based override without full rewrite. A DD-WALTERS-002
should be triggered when v2 becomes available.

---

## Part IV — Image Delivery Governance

### IV.1 — Image Delivery

| Component | Status |
|---|---|
| Direct JPEG URL | Confirmed — `media.csv.ImageURL` field |
| IIIF Image API | **Not provided** |
| IIIF Presentation API | **Not provided** |
| Manifest endpoint | **Does not exist** |
| SA-3 analogue | **Not required** |

`representative_media_url` is `media_row["ImageURL"]` verbatim. No URL construction
is required. No IIIF size parameter. Gate 3 must confirm that image URLs remain accessible
without authentication and that image resolutions are adequate for NC's product pipeline.

### IV.2 — Image URL Pattern

```
https://art.thewalters.org/images/raw/{filename}
```

Where `filename` is the `Filename` field from `media.csv`. The `ImageURL` field in
`media.csv` provides the complete ready-to-use URL and is the authorised source.

### IV.3 — Resolution Governance

Image resolution is not documented in the CSV schema. Walters does not provide resolution
tiers, IIIF zoom, or a `width`/`height` field (unlike NGA's `published_images.csv`).
Gate 3 must sample image resolutions across object types. Minimum acceptable:
1200 × 900 px for manuscript content (detailed marginalia), 800 × 600 px for
decorative arts and three-dimensional objects. If sampled resolutions are inadequate,
DD-WALTERS-002 must evaluate The Digital Walters (`thedigitalwalters.org`) as an
alternative high-resolution image source for the manuscript tier.

### IV.4 — The Digital Walters (Manuscript Tier)

`thedigitalwalters.org` hosts high-resolution archival images of the Walters manuscript
collection separately from the main CSV dataset. This system's IIIF status and rights
terms are not confirmed by this Decision. Gate 3 must evaluate whether Digital Walters
images (potentially IIIF-capable at higher resolution) should supersede `media.csv` image
URLs for manuscript records. If Digital Walters provides IIIF, a supplemental
SA-3 analogue may be required for manuscript records only.

---

## Part V — Commercial Opportunity Assessment

### V.1 — Primary Commercial Tier: Illuminated Manuscripts (NC's Gap Category)

Walters holds one of the world's great illuminated manuscript collections:
- **Medieval European**: Books of Hours, Psalters, Bibles, Apocalypse manuscripts —
  elaborate figurative scenes, historiated initials, decorated borders
- **Byzantine**: Gospel books, lectionaries, psalters — gold-ground miniatures, formal
  portrait miniatures
- **Islamic**: Quranic manuscripts, scientific texts, Persian poetry — calligraphic
  illumination, botanical and zoological illustration

NC currently has zero illuminated manuscript content. Walters fills this category entirely.
Manuscript illustration pages are high-value print products — detailed, framed, with
clear cultural provenance and visual distinctiveness.

### V.2 — Secondary Commercial Tier: Byzantine and Ancient Mediterranean

**Byzantine** (BYZ collection): Icons, enamels, metalwork, ivory carvings. NC has no
Byzantine content. Directly anchors Constantinople/Istanbul place pages and Eastern
Orthodox world context.

**Ancient Egyptian** (EGY collection): Statuary, amulets, papyri. Supplemental to Met;
different objects with different provenance.

**Ancient Near Eastern and Greek**: Fills additional ancient world gaps.

### V.3 — Geographic Gap Coverage

| Gap | Walters Coverage |
|---|---|
| Byzantine world / Istanbul | **Primary fill** — BYZ collection |
| Islamic world manuscripts | **Primary fill** — ISL collection |
| Medieval European scriptoria | **Primary fill** — manuscript collection |
| Ancient Egypt (supplemental) | Supplemental to Met |
| Ancient Near East | Partial fill |
| South Arabia / Ethiopia | Fills Africa gap partially (EGY, Ethiopia collections) |

### V.4 — Estimated NC-Eligible Inventory

| Category | Estimated Objects | Estimated Images |
|---|---|---|
| Total objects with images | ~10,000–15,000 | 46,371 |
| Illuminated manuscripts (pre-1500) | ~2,000–4,000 | ~8,000–16,000 |
| Byzantine art | ~1,000–2,000 | ~3,000–6,000 |
| Islamic manuscripts and objects | ~1,500–3,000 | ~4,000–9,000 |
| Ancient Egyptian | ~1,000–2,000 | ~3,000–6,000 |
| MASTERWORK tier | ~500–1,500 | — |

Note: NC eligibility requires `media.csv` image coverage; objects without images are
BLOCKED by WLT-R-2. Exact counts require live CSV filtering at Gate 3.

---

## Decision

### Article 1 — Source Classification and Production Approval

**1.1** The Walters Art Museum is classified as a **Tier 1 Core** content institution
for NC's commercial pipeline. Walters passes NC's production-source commercial reuse
requirement without qualification. See Part II.1.

**1.2** Walters is assigned institution number **#13**.

**1.3** Walters' CC0 Open Access policy, institution-wide with explicit commercial
reuse authorization in the policy text, is unambiguous. No text-path analysis,
REVIEW_REQUIRED tier, or language-specific doctrine is required.

**1.4** The source identifier is `walters`. Permanent once written.

**1.5** Current Institution Factory stage: **Stage 1 (Discovery) complete; Stage 2
(Governance) initiated by this Decision.**

### Article 2 — Walters Rights Matrix v1

**2.1** A new institution-specific rights matrix is required: **Walters Rights Matrix v1**
(`policy_id: "walters_rights_matrix_v1"`).

**2.2** Walters Rights Matrix v1 introduces the **sixth distinct rights class** to NC's
pipeline: **institution-wide CC0**. There is no per-record rights field. All records
in the Walters CSV dataset are CC0 by institutional declaration. Classification is a
data completeness check, not a rights determination.

**2.3** Walters Rights Matrix v1 cannot inherit any prior rights matrix.

**2.4** Classification rules: per Part II.3 (WLT-R-1 through WLT-R-4).

**2.5** `rights_status` in the ALLOWED outcome: `"pending_verification"` (CI-4 ceiling).

**2.6** No REVIEW_REQUIRED class.

**2.7** Rights evidence additional fields per Part II.4: `walters_object_id`,
`walters_object_number`, `walters_media_xref_id`, `walters_image_url`,
`walters_is_primary`.

**2.8** `shared_media_adapter/store.py` remap set must extend to include `"walters"`
before Sprint 3. SA-9 must be updated accordingly.

### Article 3 — Ingestion Architecture

**3.1** The authorised primary ingestion path is **CSV bulk download** from
`github.com/WaltersArtMuseum/api-thewalters-org`. The retired API v1 must not be used.
API v2, when available, must be evaluated via DD-WALTERS-002 before adoption.

**3.2** Required tables for Sprint 1: `art.csv`, `media.csv`, `creators.csv`.

**3.3** Join strategy per Article III.4. One M36 record per unique `ObjectID`.

**3.4** Pipe-delimited sub-fields (`CollectionID`, `CollectionName`, `Creators`,
`Images`) must be parsed by splitting on `|` before use.

**3.5** `art.csv.Images` field must not be used for image URL retrieval. `media.csv`
`ImageURL` is the authorised image URL source.

**3.6** CSV freshness guard: 30-day staleness threshold (vs NGA's 7-day). Download
timestamps logged in `preservation_event`.

**3.7** `walters_dry_run = True` is the mandatory default in `config.py`. Production
activation requires explicit override and two-human sign-off.

**3.8** Enumeration order: `art.ObjectID ASC` (integer, ascending). Required for CI-8
replay determinism.

### Article 4 — Image Delivery Governance

**4.1** `representative_media_url` = `media_row["ImageURL"]` verbatim. No URL construction.
No IIIF size parameter.

**4.2** There are no IIIF Presentation manifests. No `walters_manifest_url` field.
No SA-3 analogue required.

**4.3** Primary image selection: `IsPrimary = "1"` with `Rank ASC` tiebreaker.
Fallback: lowest `Rank` among all `MediaType = "Image"` rows if no primary marked.

**4.4** Image resolution gate: Gate 3 must sample image resolutions. Minimum thresholds
per Article IV.3. If inadequate, evaluate The Digital Walters as a supplemental
high-resolution source before Sprint development begins.

**4.5** `MediaType = "Image"` filter applied in media join. Non-image media types (PDF,
video) excluded from ingestion in this Decision.

### Article 5 — Metadata Field Mapping

| CSV Field | Source Table | NC Substrate Field | Transformation |
|---|---|---|---|
| `ObjectID` | art | `record_id` | `str(ObjectID)` |
| `ObjectNumber` | art | `accession_num` | Strip |
| `Title` | art | `title` | Strip |
| `DateText` | art | `date` | Strip |
| `DateBeginYear` | art | `date_start` | Integer; negative = BCE |
| `DateEndYear` | art | `date_end` | Integer; negative = BCE |
| `Medium` | art | `technique` | Strip |
| `Description` | art | `description` | Strip; fallback to `Medium` |
| `Provenance` | art | `provenance` | Strip |
| `Culture` | art | `culture` | Strip |
| `Style` | art | `style` | Strip |
| `Classification` | art | `edm_type` | Strip |
| `CreditLine` | art | `credit_line` | Strip |
| `Dynasty` | art | `dynasty` | Strip |
| `ObjectName` | art | `sub_type` | Strip |
| `CollectionID` | art | `collection_codes` | Split on `\|`; list |
| `CollectionName` | art | `collection_names` | Split on `\|`; list |
| `ResourceURL` | art | `source_url` | Strip; prefer PURL |
| `name` | creators (via Creators join) | `creator` | First matched creator name |
| `nationality` | creators (via join) | `creator_nationality` | Collect all |
| `ImageURL` | media | `representative_media_url` | Verbatim (IsPrimary = 1) |
| `MediaXrefID` | media | `walters_media_xref_id` | `str(MediaXrefID)` |
| `IsPrimary` | media | `walters_is_primary` | Raw string |
| SHA256(canonical JSON) | — | `raw_payload_hash` | Sort keys, no separators |

**Preferred `source_url`:** `https://purl.thewalters.org/art/{ObjectNumber}` — the
PURL is more stable than `ResourceURL`. Gate 3 must confirm the PURL pattern is live.
Fallback: `ResourceURL` verbatim from `art.csv`.

**Anchor type derivation rules (ordered, first match wins):**

1. `Classification` contains "manuscript" or "book" (case-insensitive) → `"geographic"`
   (manuscript content is always place-attributable to its scriptoria/culture of origin)
2. Any `creator_nationality` or `Culture` non-null → `"geographic"`
3. Biological keywords in `Description`, `ObjectName`, or `CollectionName`
   (bird, botanical, plant, animal, insect, fish, flower, zoological) → `"biological"`
4. Any `CollectionID` code in geographic set
   (BYZ, EGY, GRK, ISL, CHN, IND, ANE, ETH, AME, JAP, SEA) → `"geographic"`
5. Default → `"cultural"`

### Article 6 — Pilot Scope

**6.1** The Walters pilot is authorised for **Illuminated Manuscripts / Medieval Europe**
as the primary target place context. This addresses NC's most significant content gap and
has the highest commercial differentiation from any other pipeline institution.

**6.2** Pilot target: **75 assets** with `ImageURL` confirmed accessible.

**6.3** Primary batch (50): Illuminated manuscripts — medieval European Books of Hours,
Psalters, and Gospel books. Filter: `Classification` contains "Manuscripts" AND
`DateEndYear ≤ 1500`.

**6.4** Secondary batch (25): Byzantine collection (BYZ `CollectionID`). Icons,
enameled metalwork, manuscript illumination from Byzantine world.

**6.5** Pilot duration: 90 days. Two-human sign-off required for activation.

### Article 7 — Asset Zero Requirements

**7.1** Asset Zero must satisfy:
- `media.IsPrimary = "1"` and `ImageURL` non-null; HTTP 200 confirmed
- Pre-1500 subject matter
- Clear figurative or decorative illustration (manuscript page preferred)
- MASTERWORK tier (widely reproduced, historically documented)

**7.2** Recommended Asset Zero: A **medieval illuminated manuscript page** from the
Walters' Book of Hours holdings or Byzantine Gospel book — a full-page miniature or
historiated initial with figurative content. Walters W.174 (Psalter) or similar canonical
manuscript objects are strong candidates. Specific `ObjectID` must be confirmed via live
`art.csv` + `media.csv` query at Gate 7.

**7.3** Alternative: Byzantine icon or enamel plaque — strongly associated with the
Walters brand and fills a gap no other NC institution addresses.

**7.4** Asset Zero checklist:
- [ ] `ObjectID` confirmed in `art.csv` with `IsPrimary = "1"` in `media.csv`
- [ ] `ImageURL` confirmed HTTP 200; image resolution meets thresholds (Article IV.3)
- [ ] Walters Rights Matrix v1 classifies as ALLOWED (WLT-R-1 through WLT-R-4)
- [ ] `normalize_record()` produces no mandatory field warnings
- [ ] `write_record()` returns `status: "written"`, `writes: 7`
- [ ] `media_rights.rights_status = "pending_verification"` in DB
- [ ] All five SC-7 evidence fields present in rights_evidence
- [ ] Two-human sign-off

### Article 8 — Success Criteria

**SC-1 (Asset Zero):** Written with `rights_status = "pending_verification"`. Image URL
resolves HTTP 200. Two-human sign-off.

**SC-2 (CSV freshness):** All required tables downloaded within 30 days of pilot run.
Download timestamps logged in `preservation_event`.

**SC-3 (Pilot volume):** 75 assets written. BLOCKED rate ≤ 10% (higher threshold than
NGA/SMK reflects possible image availability gaps in older CSV data).

**SC-4 (FM-4):** Zero violations. Non-waivable.

**SC-5 (No terminal attestation):** Zero `"verified_cc0"` in `worker_classified_status`.

**SC-6 (Anchor type fidelity):** Correct for ≥ 90% of pilot assets. At least one
`"biological"` (botanical/zoological manuscript marginalia), one `"geographic"` (manuscript
or Byzantine record), and one `"cultural"` record.

**SC-7 (Walters evidence completeness):** `walters_object_id`, `walters_object_number`,
`walters_media_xref_id`, `walters_image_url`, `walters_is_primary` present in all ALLOWED
records. Zero exceptions.

**SC-8 (Image resolution):** `representative_media_url` resolves HTTP 200 and meets
minimum resolution thresholds (Article IV.3) for ≥ 90% of written records.

**SC-9 (Join consistency):** No two M36 records carry the same `walters_object_id`. One
substrate record per object enforced.

**SC-10 (Human review gate):** Two-human sign-off on pilot completion report before
DD-WALTERS-002.

### Article 9 — Source Registry Authorization

| Parameter | Value |
|---|---|
| `source_id` | `walters` |
| `source_name` | `Walters Art Museum` |
| `source_type` | `museum_open_data` |
| `institution_number` | `13` |
| `priority` | `14` |
| `auth_type` | `none` |
| `rate_limit_rps` | `5` |
| `burst` | `10` |
| `rights_policy_id` | `walters_rights_matrix_v1` |
| `data_base_url` | `https://raw.githubusercontent.com/WaltersArtMuseum/api-thewalters-org/main` |
| `collection_page_template` | `https://purl.thewalters.org/art/{ObjectNumber}` |
| `schema_standard` | `walters_opendata_v1` |
| `governance_state` | `pending_activation` |
| `onboarding_stage` | `stage_1_discovery` |
| `governing_dd` | `DD-WALTERS-001` |

### Article 10 — Standards Amendments

**SA-15 (Required — blocks Sprint 1):** Walters Open Data Adapter Profile. Defines:
`walters_opendata_v1` schema standard, `walters_rights_matrix_v1` policy ID, CSV field
names (camelCase schema), join keys (`ObjectID`), primary image selection (`IsPrimary = 1`,
`Rank ASC`), pipe-delimiter parsing rules, source registry parameters, evidence fields
(`walters_object_id`, `walters_object_number`, `walters_media_xref_id`,
`walters_image_url`, `walters_is_primary`), staleness guard (30-day threshold), PURL
collection page template. Must be ratified before Sprint 1.

**SA-9 update (Required — blocks Sprint 3):** Extend `build_rights_evidence` remap set
to include `"walters"`. Current set: `{"met", "aic", "cma", "smk", "nga"}`. Must include
`"walters"` before Walters Sprint 3. Add Walters evidence injection block to shared store.

**SA-14 (Applies — no new amendment):** CSV Bulk Download Ingestion Protocol (drafted for
NGA) governs generic parameters. Walters-specific parameters are in SA-15.

**SA-3 analogue: Not required.** Walters has no IIIF.

### Article 11 — Activation Prerequisites

**Constitutional (CI-class, non-waivable):**
- [ ] SA-15 (Walters Open Data Adapter Profile) ratified before Sprint 1
- [ ] SA-9 updated to include `"walters"` before Sprint 3
- [ ] `walters_dry_run = True` default in `config.py`

**Gate 3 (must resolve before Sprint development):**
- [ ] Image resolution confirmed adequate (Article IV.3 thresholds)
- [ ] PURL pattern `purl.thewalters.org/art/{ObjectNumber}` confirmed live
- [ ] CSV freshness cadence confirmed (adjust staleness guard if needed)
- [ ] The Digital Walters evaluated for manuscript-tier high-resolution images (Article IV.4)
- [ ] API v2 status confirmed (affects timeline risk; Article III.7)
- [ ] `MediaType = "Image"` confirmed as correct filter (no other type serves images)
- [ ] Rate-limit or access restriction confirmed absent for ImageURL fetches

**Sprint prerequisites:**
- [ ] `workers/walters_adapter/config.py` — GitHub base URL, freshness guard, dry_run
- [ ] `workers/walters_adapter/client.py` — CSV download, three-table join, pipe parsing,
      primary image selection (`IsPrimary = 1`, `Rank ASC`), `ObjectID ASC` enumeration
- [ ] `workers/walters_adapter/rights.py` — Walters Rights Matrix v1
      (institution-wide CC0; WLT-R-1 through WLT-R-4)
- [ ] `workers/walters_adapter/normalize.py` — camelCase field mapping, pipe-field parsing,
      creator join, culture/collection anchor signals, PURL source_url construction
- [ ] `workers/walters_adapter/technical.py` — `walters_opendata_v1` schema standard
- [ ] `workers/walters_adapter/store.py` — `derive_anchor_type` via manuscript/culture/
      collection code rules, `StoreRuntime` with `source_slug="walters"`,
      join-consistency guard

### Article 12 — Subsequent Decisions

**DD-WALTERS-002** (Walters Production Activation): Drafted upon Asset Zero completion,
pilot completion, and SC-1 through SC-10 passing.

**DD-WALTERS-002 trigger event:** API v2 launch — if Walters releases a documented REST
API before DD-WALTERS-002 is filed, the v2 path must be evaluated and may supersede the
CSV-based adapter before production activation.

---

## Risk Register

| ID | Risk | Probability | Severity | Mitigation |
|---|---|---|---|---|
| R-1 | Image resolution inadequate for NC product pipeline (no metadata on resolution) | Medium | High | Gate 3 resolution audit; Article IV.4 Digital Walters fallback |
| R-2 | API v2 launches mid-sprint, superseding CSV adapter before activation | Low | Medium | DD-WALTERS-002 trigger on v2 launch; design adapter for modular replacement |
| R-3 | CSV schema breaking change (2024–2025 pattern of changes continues) | Medium | Medium | Pin to known-good schema version; test against live CSV at Gate 3 |
| R-4 | SA-9 not updated to include `"walters"` before Sprint 3 — remap gap | Medium | High | SA-9 must be updated as explicit Sprint 3 blocking condition |
| R-5 | PURL pattern not live or ObjectNumber format incompatible with PURL | Low | Low | Gate 3 confirmation; fallback to `ResourceURL` field |
| R-6 | Digital Walters manuscripts require separate IIIF infrastructure | Medium | Medium | Gate 3 evaluation; treat as Phase 2 if IIIF adds complexity |
| R-7 | 30-day freshness guard too strict for Walters' actual update cadence | Low | Low | Gate 3 cadence confirmation; amend SA-15 if needed |
| R-8 | Pipe-delimited field parsing edge cases (empty fields, malformed values) | Low | Low | Defensive parsing with empty-string guard; unit-tested fixture |
| R-9 | Anchor type misclassification — arms/armour classified "geographic" via Culture | Low | Low | Acceptable; medieval armour with culture attribution is geographic by DD rule 2 |
| R-10 | Must Add institutions (NHM London, Wellcome, Trove, HathiTrust) not addressed | Certain | Info | Walters fills a non-overlapping gap; Must Add institutions remain outstanding |

---

## Ratification

This Decision is in Draft status. Both parties must review:

- **Part II.1** (Commercial Reuse Qualification — production approval finding)
- **Article 2.2** (new rights class: institution-wide CC0)
- **Article 4.4** (image resolution gate — may gate Sprint development)
- **Article 10** (SA-15 as Sprint 1 blocker; SA-9 update as Sprint 3 blocker)
- **Article 11** (Activation Prerequisites)

Upon ratification: SA-15 must be drafted immediately (blocks Sprint 1); SA-9 must be
updated to include `"walters"` before Sprint 3 begins.

| Role | Name | Date |
|---|---|---|
| Director | opengracelabs | — |
| Second Human | — | — |
