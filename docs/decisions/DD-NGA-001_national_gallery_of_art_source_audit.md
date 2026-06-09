# DD-NGA-001 — National Gallery of Art Open Access Source Audit

| Field | Value |
|---|---|
| **Decision ID** | DD-NGA-001 |
| **Type** | Source Audit |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-09 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first NGA governance document |
| **Governing Documents** | Institution Coverage Audit v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 · Institution Factory v1 |

---

## Background

The National Gallery of Art (NGA) in Washington, D.C. is a federal institution of the
United States government and one of the world's premier art museums. In January 2019 the
NGA launched its Open Access programme, releasing over 50,000 high-resolution digital
images of public domain works under Creative Commons Zero (CC0). The programme is declared
without commercial restriction: images with `openaccess = 1` carry no license fee, no
attribution requirement, and no commercial use restriction.

This Decision is initiated immediately following DD-GALLICA-003 (Gallica Commercial Reuse
Disqualification, 2026-06-09), which withdrew Gallica from NC's approved production sources
due to BnF's platform requirement that commercial re-use is subject to a license fee. NGA
presents the inverse situation: an explicit CC0 declaration with no commercial fee condition
at any layer. NGA passes NC's production-source commercial reuse test unconditionally.

This Decision documents four governance characteristics that materially differentiate NGA
from all prior institutions in NC's pipeline:

1. **CSV bulk download ingestion — new ingestion paradigm.** NGA does not provide a
   publicly documented REST collection API. Its primary open access data interface is a
   GitHub repository (`github.com/NationalGalleryOfArt/opendata`) providing 15 relational
   CSV tables updated daily from TMS (The Museum System). This is the first NC institution
   to require a CSV-based ingestion path. An NGA adapter must download and join multiple
   tables rather than paginating a REST endpoint. **SA-14 (CSV Bulk Download Ingestion
   Protocol) is required** to codify this new paradigm before Sprint 1.

2. **Image-record integer-flag rights — new rights class.** NGA's `openaccess` rights
   field is an integer (1 = allowed, 0 = restricted) on the **image record** in
   `published_images.csv`, not on the object record. This requires a join of the object
   record and image record before rights can be determined. NGA cannot inherit any prior
   rights matrix. It is the fifth distinct rights class in NC's pipeline (prior classes:
   URI-form, boolean-object-form, string-equality-form, API-tier-guarantee). A new **NGA
   Rights Matrix v1** (`nga_rights_matrix_v1`) is required.

3. **IIIF Image API v2 only — no Presentation manifests.** NGA provides IIIF Image API
   v2 Level 1 at `https://api.nga.gov/iiif/` using the image UUID from `published_images`.
   There are no IIIF Presentation manifests. SA-3 (IIIF 2.1 bridging) is **not required**.
   The `nga_manifest_url` field described in prior draft text does not apply.

4. **SA-9 remains critical.** The `build_rights_evidence` remap in
   `shared_media_adapter/store.py` covers `{"met", "aic", "cma", "smk"}`. NGA's
   `source_slug = "nga"` makes five institutions requiring institution-specific evidence
   injection branches. SA-9 must be drafted and ratified before NGA Sprint 3 — this is a
   constitutional maintenance liability.

**Governing answer to "Can NGA be approved as a production source?":** **Yes —
unconditionally.** The rights landscape is clean at every layer: copyright (CC0), platform
ToS (no commercial fee), federal copyright (17 U.S.C. § 105 eliminates reproduction rights
in federal employee digitizations), and institutional policy (no commercial licensing
programme for PD reproductions). The conflict that disqualified Gallica does not exist at NGA.

---

## Part I — Source Classification Audit

**Institution name:** National Gallery of Art (NGA)

**Location:** Washington, D.C., United States

**Institution type:** Independent federal agency, United States government

**Federal copyright status:** Works produced by U.S. federal government employees in scope
of employment are ineligible for copyright under 17 U.S.C. § 105. NGA digitizations created
by federal employees carry no reproduction rights claim independently of CC0. This is the
strongest PD foundation in NC's pipeline — no EU Article 14 / Bridgeman analysis layer is
required.

**Open access programme:** NGA Open Access (January 2019). CC0 1.0 Universal designation
for open access images. Platform policy: no permission required, no fee, no attribution
required, commercial use explicitly permitted.

**Commercial reuse status:** PERMITTED WITHOUT FEE — unconditionally.

**Collection size:**
- Total objects: 279,580
- Published images: 129,413
- Open access images (openaccess = 1): ~50,000+ (exact count requires live CSV query)

**Primary data access:** GitHub repository `github.com/NationalGalleryOfArt/opendata` —
15 CSV tables, updated daily from TMS SQL Server, CC0 licensed. Raw file base URL:
`https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/`

**Key tables:**
- `objects.csv` — 279,580 object records (primary metadata)
- `published_images.csv` — 129,413 image records (including IIIF URL and openaccess flag)
- `objects_terms.csv` — keyword/subject/style/school terms (many-to-many)
- `objects_constituents.csv` — object-to-artist relationships
- `constituents.csv` — artist records (including nationality)

**IIIF:** Image API v2 Level 1 at `https://api.nga.gov/iiif/`. No IIIF Presentation API.
No manifest endpoint. No SA-3 analogue required.

**REST API status:** An undocumented `dataServices` REST API exists (SpringBoot, read-only)
but has no published endpoints or documentation. NC's ingestion pipeline MUST NOT rely on
undocumented endpoints. CSV bulk download is the authorised primary ingestion path.

**Authentication:** None required. CSV downloads are publicly accessible. IIIF server
is publicly accessible. Gate 3 must confirm whether production-volume IIIF requests
require rate-limit registration.

**NC institution tier:** Tier 1 Core — CC0, direct, no aggregator intermediary

**Proposed institution number:** #12

**Proposed source ID:** `nga`

**Proposed source priority:** 13

**Differentiating commercial strengths:**
- American art (Homer, Cole, Sargent, Cassatt, Copley) — NC's first North American art content
- French Impressionism (Monet, Renoir, Degas, Manet, Cézanne) — distinct objects from AIC
- European Old Masters (Leonardo Ginevra de' Benci, Vermeer, Raphael, El Greco, Goya)
- Spanish masters — fills Spain/Iberian Peninsula gap (zero current NC coverage)
- Dutch Golden Age — supplemental to Rijksmuseum and SMK (different physical objects)
- Prints and drawings — natural history illustration pipeline (Hudson River School watercolors)
- Index of American Design — historical American design and decorative arts (4,840+ objects)

---

## Part II — Rights Strategy Audit

### II.1 — Commercial Reuse Qualification

| Layer | NGA Position | Compatible? |
|---|---|---|
| Copyright | CC0 1.0 — all rights waived for metadata; images CC0 (openaccess=1) | YES |
| Platform ToS | No commercial fee, no permission required | YES |
| Federal copyright | 17 U.S.C. § 105 — digitizations by federal employees ineligible for copyright | YES |
| Per-asset fee | None | YES |
| Attribution requirement | None (CC0) | YES |
| License agreement | None required | YES |

**NGA is approved as a production source.** There is no ToS commercial restriction at any
layer. Contrast with DD-GALLICA-003: BnF's "commercial re-use subject to license fee" is a
contractual platform condition absent at NGA. NGA's public policy statement is the opposite.

### II.2 — Can NGA Inherit Prior Rights Matrix Architecture?

**Answer: No.**

NGA's rights check is structurally distinct from all prior institutions:

1. The rights field (`openaccess`) is on the **image record** (`published_images.csv`), not
   the object record. Met, AIC, SMK, and CMA all carry the rights field on the object record.
2. The field type is an **integer** (1 or 0), not a Python boolean. Boolean-identity check
   `field is True` does not apply; integer-equality check `field == 1` is required.
3. Rights determination requires a **join** between the object record and the image record.
   No prior institution requires a multi-table join as part of the rights classification step.

NGA Rights Matrix v1 is the **fifth distinct rights class** in NC's pipeline:
- URI-form: Europeana, Rijksmuseum (compare field value to allowlist URI set)
- Boolean-object-form: Met, AIC, SMK (field on object record, `field is True`)
- String-equality-form: CMA (`field == "CC0"` on object record)
- API-tier-guarantee: Paris Musées (blocked Stage 3; API-level rights promise)
- **Image-record integer-flag-form: NGA** (`image_record["openaccess"] == 1`, join required)

### II.3 — NGA Rights Matrix v1 Classification Rules

Rights classification is performed on the **joined row** (object record + primary image
record), where the join condition is `published_images.depictstmsobjectid = objects.objectid`
and `published_images.viewtype = "primary"`. If no primary image exists, use the image with
the lowest `sequence` value.

| Rule ID | Condition | Outcome | rights_basis |
|---|---|---|---|
| NGA-R-1 | `object_record` is not a dict | BLOCKED | `missing_object_record` |
| NGA-R-2 | `image_record` is None (no published image for this object) | BLOCKED | `no_published_image` |
| NGA-R-3 | `image_record.get("openaccess") != 1` | BLOCKED | `not_open_access` |
| NGA-R-4 | `image_record.get("iiifurl")` is None or empty | BLOCKED | `no_iiif_url` |
| NGA-R-5 | All prior rules pass | ALLOWED | `nga_open_access_cc0` |

**ALLOWED outcome:**
- `decision`: ALLOWED
- `rights_statement_uri`: CC0_URI
- `rights_status`: `"pending_verification"` (CI-4 ceiling)
- `rights_policy_id`: `"nga_rights_matrix_v1"`

**REVIEW_REQUIRED class:** Not applicable. Every record is ALLOWED or BLOCKED.

### II.4 — Rights Evidence Requirements (SC-7)

Additional fields in `media_rights.rights_evidence` for all NGA records:
- `nga_openaccess` (int) — verbatim `image_record["openaccess"]`
- `nga_accessionnum` (str) — verbatim `object_record.get("accessionnum")`
- `nga_image_uuid` (str) — verbatim `image_record["uuid"]` (IIIF image identifier)
- `nga_iiifurl` (str) — verbatim `image_record["iiifurl"]` (IIIF base URL)
- `nga_objectid` (int) — verbatim `object_record["objectid"]`

### II.5 — Shared Store Extension (Sprint 3 Prerequisite)

`build_rights_evidence` in `shared_media_adapter/store.py` must extend the remap to
`source_slug in {"met", "aic", "cma", "smk", "nga"}` before NGA Sprint 3. SA-9 must be
drafted and ratified before Sprint 3 — five institutions in this branch is a constitutional
maintenance liability. This is not a recommendation; it is a blocking condition.

---

## Part III — Data Access Audit

### III.1 — Ingestion Architecture Overview

NGA's ingestion architecture is fundamentally different from all prior NC institutions.
There is no REST collection API suitable for production pagination. The correct path is:

```
1. Download CSV tables from GitHub (daily full refresh or incremental diff)
2. Build in-memory join: objects + published_images + objects_terms + objects_constituents + constituents
3. Filter: published_images.openaccess = 1
4. Sort: by objects.objectid ASC (CI-8 determinism)
5. For each joined row: classify rights, normalize, write to M36
6. Fetch IIIF image via api.nga.gov for representative_media_url
```

This is the first NC institution to use a CSV-bulk ingestion path. SA-14 (CSV Bulk Download
Ingestion Protocol) must be drafted and ratified before Sprint 1 to codify this paradigm.

### III.2 — CSV Table Reference URLs

| Table | GitHub Raw URL | Key fields |
|---|---|---|
| `objects.csv` | `.../data/objects.csv` | objectid, uuid, accessionnum, title, displaydate, beginyear, endyear, medium, attribution, attributioninverted, classification, subclassification, provenancetext, departmentabbr, wikidataid |
| `published_images.csv` | `.../data/published_images.csv` | uuid, iiifurl, iiifthumburl, viewtype, sequence, width, height, maxpixels, openaccess, depictstmsobjectid |
| `objects_terms.csv` | `.../data/objects_terms.csv` | termid, objectid, termtype, term |
| `objects_constituents.csv` | `.../data/objects_constituents.csv` | objectid, constituentid, roletype, role |
| `constituents.csv` | `.../data/constituents.csv` | constituentid, preferreddisplayname, nationality, beginyear, endyear |

Base URL: `https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/`

### III.3 — Enumeration and Replay Determinism

Primary enumeration: Download all five tables. Filter `published_images` where
`openaccess = 1`. Join to `objects` on `depictstmsobjectid = objectid`. Sort by
`objectid ASC` for CI-8 replay determinism. No pagination cursor — a complete ordered
pass through the open access image set.

The `published_images` join may yield multiple images per object (primary + alternates).
The authorised join strategy is:
1. One primary image per object: `viewtype = "primary"`, or lowest `sequence` if no primary
2. Additional images via `viewtype = "alternate"` — stored in `additional_images` in
   technical metadata, not as separate substrate records
3. Exactly one M36 record per `objectid`; the primary image record provides the rights
   evidence and IIIF URL

### III.4 — CSV Freshness and Caching

The GitHub repository updates daily (automated cron job, commit message format
`YYYY-MM-DD data export`). The NGA adapter must:
- Check the `Last-Modified` header (or GitHub API commit timestamp) before re-downloading
- Cache downloaded CSV files locally with the date suffix
- Log the download timestamp in `preservation_event` metadata
- Refuse to ingest if a CSV's modification date is more than 7 days old (staleness guard)

### III.5 — Rate Limiting

CSV GitHub downloads: public GitHub rate limits apply (60 req/hr unauthenticated; not a
concern for bulk CSV). IIIF image server (`api.nga.gov`): no documented rate limit. NC
convention: 5 req/s, burst 10. Gate 3 must confirm whether production-volume IIIF image
requests require rate-limit registration with NGA.

### III.6 — `maxpixels` Field Governance

`published_images.csv` contains a `maxpixels` field described as a "fair use resolution
cap." Gate 3 must determine whether this cap applies to `openaccess = 1` images. If
`maxpixels` caps even CC0 images, the IIIF request must not exceed `maxpixels` in any
dimension. The adapter must respect this cap in IIIF URL construction when non-null.

---

## Part IV — Image Delivery and IIIF Governance

### IV.1 — IIIF Status

| Component | Status |
|---|---|
| IIIF Image API | Confirmed — v2 Level 1 at `https://api.nga.gov/iiif/` |
| IIIF Presentation API | **Not implemented** — no manifests |
| Manifest endpoint | **Does not exist** — not a gate item |
| SA-3 analogue | **Not required** |

The `iiifurl` field in `published_images.csv` contains the IIIF Image API base URL for
each image (format: `https://api.nga.gov/iiif/{uuid}`). This is the authorised image
identifier and the basis for all IIIF URL construction.

### IV.2 — IIIF Image URL Construction

Standard size for `representative_media_url`:
```
{iiifurl}/full/!1024,1024/0/default.jpg
```

Thumbnail:
```
{iiifurl}/full/!200,200/0/default.jpg
```
(The `iiifthumburl` field from `published_images.csv` provides a pre-computed
200×200 thumbnail — it may be used directly instead of constructing the URL.)

Full resolution (for preservation):
```
{iiifurl}/full/max/0/default.jpg
```

**`representative_media_url` priority rule:**
1. `{iiifurl}/full/!1024,1024/0/default.jpg` where `iiifurl` is non-null and
   `openaccess = 1` — HTTP 200 confirmed
2. `None` → BLOCKED by NGA-R-4

There is no direct CDN file URL fallback. All image delivery is IIIF-based.

### IV.3 — IIIF Image API Capabilities (Verified)

- Format: JPEG only
- Qualities: native, color, gray
- Rotation: 90° increments
- Region: percentage and square regions supported
- Size: forced WH, proportional, above-full
- Tile size: 256×256, scale factors 1–64
- Pre-computed sizes: 52, 105, 210, 420, 841, 1682 px wide (6 tiers)
- Maximum resolution: per image (up to ~12M pixels); see `maxpixels` caveat (Article IV.3
  Gate 3 item)

---

## Part V — Commercial Opportunity Assessment

### V.1 — Primary Commercial Tier: American Art (NC's Current Zero-Coverage Gap)

NGA holds one of the world's finest American art collections. NC currently has zero North
American art content. Key inventory for NC's pipeline:

- **Hudson River School**: Thomas Cole, Frederic Church, Albert Bierstadt — American landscape
  painting directly anchors U.S. regional place pages (New England, Hudson Valley, Appalachian)
- **Winslow Homer**: Marine paintings and outdoor scenes — globally recognized, high-value
  print products, coastal and maritime place pages
- **John Singer Sargent**: Portraits and watercolors — exceptional commercial value for
  portrait-format products
- **Mary Cassatt**: Impressionist scenes — fills NC's first American Impressionist inventory
- **Index of American Design**: 4,840+ historical American design and craft objects

### V.2 — Secondary Tier: European Old Masters and Impressionism

- **Leonardo da Vinci** — Ginevra de' Benci (only Leonardo in the Americas) — high-anchor
  institutional value for Italy place pages
- **Vermeer** — Girl with the Red Hat — Dutch Golden Age supplement to Rijksmuseum/SMK
- **French Impressionism** — Monet, Renoir, Degas, Cézanne, Gauguin — distinct objects
  from AIC's holdings; supplemental French coverage (partially addresses Gallica gap)
- **Spanish masters** — El Greco, Goya, Velázquez — fills Spain/Iberian Peninsula gap
  (zero current NC coverage for pre-1900 Spanish painting)

### V.3 — Geographic Gap Coverage

| Gap | NGA Coverage |
|---|---|
| United States / North America | **Primary fill** — American art anchor content |
| Spain / Iberian Peninsula | **Primary fill** — El Greco, Goya, Velázquez |
| Washington D.C. / Federal Mall | **Institution anchor** for D.C. place page |
| France (post-Gallica) | **Partial** — Impressionism (not Buffon/Redouté natural history) |

### V.4 — Estimated Open Access Inventory

| Category | Estimated Count |
|---|---|
| Total open access images | ~50,000+ |
| American art (pre-1900) | ~8,000–12,000 |
| European Old Masters (pre-1800) | ~10,000–15,000 |
| French Impressionism | ~3,000–5,000 |
| Prints, drawings, watercolors | ~10,000–15,000 |
| MASTERWORK tier | ~3,000–6,000 |

Note: Exact counts require filtering `published_images.csv` on `openaccess = 1` and joining
with `objects` to apply date/classification filters. Gate 3 establishes actuals.

---

## Decision

### Article 1 — Source Classification and Production Approval

**1.1** The National Gallery of Art is classified as a **Tier 1 Core** content institution
for NC's commercial pipeline. NGA passes NC's production-source commercial reuse requirement
without qualification. See Part II.1.

**1.2** NGA is assigned institution number **#12**.

**1.3** NGA's CC0 Open Access programme, combined with federal government § 105 copyright
status for NGA digitizations, constitutes the strongest rights foundation in NC's portfolio.
No text-path rights analysis, REVIEW_REQUIRED tier, or language-specific doctrine is required.

**1.4** The source identifier is `nga`. Permanent once written.

**1.5** Current Institution Factory stage: **Stage 1 (Discovery) complete; Stage 2
(Governance) initiated by this Decision.**

### Article 2 — NGA Rights Matrix v1

**2.1** A new institution-specific rights matrix is required: **NGA Rights Matrix v1**
(`policy_id: "nga_rights_matrix_v1"`).

**2.2** NGA Rights Matrix v1 introduces a new rights class to NC's pipeline:
**image-record integer-flag-form**. The rights field `openaccess` (integer 1/0) resides on
the image record in `published_images.csv`, not the object record. Rights classification
requires a join of the object record and image record before any rule is applied.

**2.3** NGA Rights Matrix v1 cannot inherit any prior rights matrix. The join requirement,
field location, and field type are all distinct from Met/AIC/SMK (boolean-object-form),
CMA (string-equality-form), Europeana/Rijksmuseum (URI-form), and Paris Musées
(API-tier-guarantee).

**2.4** Classification rules: per Part II.3 (NGA-R-1 through NGA-R-5).

**2.5** `rights_status` in the ALLOWED outcome: `"pending_verification"` (CI-4 ceiling).
`"verified_cc0"` is never written by the worker (FM-4).

**2.6** No REVIEW_REQUIRED class.

**2.7** Rights evidence additional fields per Part II.4: `nga_openaccess`, `nga_accessionnum`,
`nga_image_uuid`, `nga_iiifurl`, `nga_objectid`.

**2.8** `shared_media_adapter/store.py` remap must extend to
`source_slug in {"met", "aic", "cma", "smk", "nga"}` before Sprint 3. SA-9 must be drafted
and ratified as a blocking condition.

### Article 3 — Ingestion Architecture

**3.1** The authorised primary ingestion path is **CSV bulk download** from
`github.com/NationalGalleryOfArt/opendata`. REST API endpoints are not authorised as a
primary ingestion path until documented and verified by NGA.

**3.2** The undocumented `dataServices` REST API must not be relied upon in any adapter
code. Any use of undocumented endpoints is a constitutional violation under SC-7 (evidence
completeness requires reproducible provenance).

**3.3** Five tables are required: `objects.csv`, `published_images.csv`, `objects_terms.csv`,
`objects_constituents.csv`, `constituents.csv`. All five must be downloaded in the same
ingestion run to maintain join consistency.

**3.4** Enumeration order: `objectid ASC`. One M36 record per unique `objectid` in the
open access image set. Required for CI-8 replay determinism.

**3.5** CSV freshness guard: refuse ingestion if any required CSV has `Last-Modified` older
than 7 days. Log download timestamps in `preservation_event`.

**3.6** `nga_dry_run = True` is the mandatory default in `config.py`. Production activation
requires explicit override and two-human sign-off.

### Article 4 — IIIF and Image Delivery Governance

**4.1** IIIF Image API v2 Level 1 at `https://api.nga.gov/iiif/` is the authorised image
delivery path.

**4.2** There are no IIIF Presentation manifests. No `nga_manifest_url` field. No SA-3
analogue required.

**4.3** `representative_media_url`: `{iiifurl}/full/!1024,1024/0/default.jpg`. Article
IV.2 priority rule applies.

**4.4** `maxpixels` governance: Gate 3 must determine whether `maxpixels` caps IIIF image
delivery for open access images. If non-null and applicable, IIIF URL must not request a
resolution exceeding `maxpixels`. The adapter must implement this cap check.

### Article 5 — Metadata Field Mapping

| CSV Field | Source Table | NC Substrate Field | Transformation |
|---|---|---|---|
| `objectid` | objects | `record_id` | `str(objectid)` |
| `accessionnum` | objects | `accession_num` | Strip |
| `title` | objects | `title` | Strip |
| `displaydate` | objects | `date` | Strip |
| `beginyear` | objects | `date_start` | Integer |
| `endyear` | objects | `date_end` | Integer |
| `attributioninverted` | objects | `creator` | Strip; fall back to `attribution` |
| `attribution` | objects | `creator_display` | Strip |
| `classification` | objects | `edm_type` | Strip |
| `subclassification` | objects | `sub_type` | Strip |
| `medium` | objects | `technique` | Strip |
| `provenancetext` | objects | `provenance` | Strip |
| `departmentabbr` | objects | `department` | Strip |
| `wikidataid` | objects | `wikidata_id` | Strip |
| `iiifurl` | published_images | `nga_iiifurl` | Raw |
| `openaccess` | published_images | `nga_openaccess` | Integer |
| `uuid` | published_images | `nga_image_uuid` | Raw |
| `width` | published_images | `width_px` | Integer |
| `height` | published_images | `height_px` | Integer |
| `maxpixels` | published_images | `nga_maxpixels` | Integer or None |
| `term` (School) | objects_terms | `school` | Collect all terms where termtype="School" |
| `term` (Keyword/Theme) | objects_terms | `subject_terms` | Collect; termtype in ("Keyword","Theme","Style") |
| `term` (Place Executed) | objects_terms | `place_executed` | Collect; termtype="Place Executed" |
| `nationality` | constituents | `creator_nationality` | Via objects_constituents join; roletype="artist" |
| SHA256(canonical JSON) | — | `raw_payload_hash` | Sort keys, no separators, on joined row |
| Constructed | — | `source_url` | `https://www.nga.gov/collection/art-object-page.{objectid}.html` (verify at Gate 3) |
| Constructed | — | `representative_media_url` | `{iiifurl}/full/!1024,1024/0/default.jpg` |

**Anchor type derivation rules (ordered, first match wins):**

1. `termtype = "Place Executed"` term is non-empty AND subject matter has geographic content
   → `"geographic"`
2. Any Keyword/Theme term matching biological vocabulary (bird, botanical, flower, plant,
   animal, fish, insect) → `"biological"`
3. `school` non-empty (school = place of artistic tradition) → `"geographic"`
4. `classification` or `subclassification` contains "map" → `"geographic"`
5. `creator_nationality` is non-null → `"geographic"` (nationality provides place anchor)
6. Default → `"cultural"`

### Article 6 — Pilot Scope

**6.1** The NGA pilot is authorised for **American Art / United States** as the target place
context. American art is NGA's primary commercial differentiator and fills NC's North
American gap.

**6.2** Pilot target: **75 assets**, `openaccess = 1`, subject matter pre-1900.

**6.3** Primary batch (50): American art — Hudson River School, Winslow Homer, John Singer
Sargent, Mary Cassatt. Filter: `school` term = "American" OR constituent nationality
= "American" with `beginyear < 1870`.

**6.4** Secondary batch (25): European — Spanish masters (El Greco, Goya) or French
Impressionism (Monet, Degas). Verification of Spanish gap coverage via `school = "Spanish"`.

**6.5** Pilot duration: 90 days. Two-human sign-off required for activation.

### Article 7 — Asset Zero Requirements

**7.1** Asset Zero must satisfy:
- `image_record.openaccess = 1`
- `iiifurl` non-null; `{iiifurl}/full/!1024,1024/0/default.jpg` returns HTTP 200
- American subject or American artist, pre-1900
- MASTERWORK tier (globally recognized work)

**7.2** Recommended Asset Zero: **Winslow Homer** — a major marine painting or outdoor
scene from his mature period (1880s–1890s). Homer is globally recognized, commercially
strong for prints, and directly anchors United States/coastal place pages. "Breezing Up
(A Fair Wind)" (c.1873–76) is a strong candidate if its `published_images` record carries
`openaccess = 1`. Specific `objectid` must be confirmed via live CSV query at Gate 7.

**7.3** Alternative: Thomas Cole (Hudson River School landscape) or Mary Cassatt (garden
or mother-child scene). Both pre-1900, both MASTERWORK tier, both strong commercial works.

**7.4** Asset Zero checklist:
- [ ] `objectid` confirmed in `objects.csv` with `openaccess = 1` in `published_images`
- [ ] `{iiifurl}/full/!1024,1024/0/default.jpg` confirmed HTTP 200
- [ ] NGA Rights Matrix v1 classifies as ALLOWED (NGA-R-1 through NGA-R-5)
- [ ] `normalize_record()` produces no mandatory field warnings
- [ ] `write_record()` returns `status: "written"`, `writes: 7`
- [ ] `media_rights.rights_status = "pending_verification"` in DB
- [ ] `nga_openaccess: 1` in rights evidence
- [ ] `nga_iiifurl` non-null in rights evidence
- [ ] `nga_image_uuid` non-null in rights evidence
- [ ] Two-human sign-off

### Article 8 — Success Criteria

**SC-1 (Asset Zero):** Written with `rights_status = "pending_verification"`. IIIF image
resolves HTTP 200. Two-human sign-off.

**SC-2 (CSV freshness):** All five tables downloaded within 24 hours of pilot run.
Download timestamps logged in `preservation_event`.

**SC-3 (Pilot volume):** 75 assets written. BLOCKED rate ≤ 5%.

**SC-4 (FM-4):** Zero violations. Non-waivable.

**SC-5 (No terminal attestation):** Zero `"verified_cc0"` in `worker_classified_status`.

**SC-6 (Anchor type fidelity):** Correct for ≥ 95% of pilot assets. At least one biological
(bird/botanical), one geographic (American landscape with school term), one cultural record.

**SC-7 (NGA evidence completeness):** `nga_openaccess`, `nga_accessionnum`, `nga_image_uuid`,
`nga_iiifurl`, `nga_objectid` present in all ALLOWED records. Zero exceptions.

**SC-8 (Image resolution):** `representative_media_url` resolves HTTP 200 for ≥ 95% of
written records.

**SC-9 (Join consistency):** No two M36 records carry the same `nga_objectid`. One
substrate record per object enforced.

**SC-10 (Human review gate):** Two-human sign-off on pilot completion report before
DD-NGA-002.

### Article 9 — Source Registry Authorization

| Parameter | Value |
|---|---|
| `source_id` | `nga` |
| `source_name` | `National Gallery of Art` |
| `source_type` | `federal_museum_open_access` |
| `institution_number` | `12` |
| `priority` | `13` |
| `auth_type` | `none` |
| `rate_limit_rps` | `5` |
| `burst` | `10` |
| `rights_policy_id` | `nga_rights_matrix_v1` |
| `api_base_url` | `https://api.nga.gov/iiif` |
| `data_base_url` | `https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data` |
| `collection_page_template` | `https://www.nga.gov/collection/art-object-page.{objectid}.html` |
| `schema_standard` | `nga_openaccess_v1` |
| `governance_state` | `pending_activation` |
| `onboarding_stage` | `stage_1_discovery` |
| `governing_dd` | `DD-NGA-001` |

### Article 10 — Standards Amendments

**SA-14 (Required — new paradigm, blocks Sprint 1):** CSV Bulk Download Ingestion Protocol.
Codifies: GitHub raw CSV URL format, required tables and join keys, local caching strategy,
daily freshness check, staleness guard (7-day), download-timestamp logging in
`preservation_event`, deterministic sort (objectid ASC) for CI-8, join strategy for primary
image selection. Must be ratified before any NGA adapter code is written.

**SA-13 (Required — blocks Sprint 1):** NGA Open Access Adapter Profile. Defines:
`nga_openaccess_v1` schema standard, `nga_rights_matrix_v1` policy ID, IIIF Image API v2
URL construction, source registry parameters, evidence fields (`nga_openaccess`,
`nga_accessionnum`, `nga_image_uuid`, `nga_iiifurl`, `nga_objectid`), `maxpixels` cap rule.

**SA-9 (Critical — blocking for Sprint 3):** CC0 Adapter Profile / `StoreRuntime.cc0_adapter_mode`.
The `build_rights_evidence` source_slug remap now requires five branches. SA-9 must be drafted
and ratified before NGA Sprint 3. This is a constitutional maintenance liability.

**SA-3 analogue:** **Not required.** NGA has no IIIF Presentation manifests.

### Article 11 — Activation Prerequisites

**Constitutional (CI-class, non-waivable):**
- [ ] SA-14 (CSV Bulk Download Protocol) ratified before Sprint 1
- [ ] SA-13 (NGA Open Access Adapter Profile) ratified before Sprint 1
- [ ] SA-9 ratified before Sprint 3
- [ ] `nga_dry_run = True` default in `config.py`

**Gate 3 (must resolve before DD-NGA-002):**
- [ ] `maxpixels` cap confirmed for open access images (does it apply or not?)
- [ ] Rate-limit registration confirmed for production-volume IIIF requests
- [ ] Collection page URL template confirmed (`art-object-page.{objectid}.html`)
- [ ] Exact open access image count confirmed (CSV `openaccess = 1` filter result)
- [ ] `dataServices` REST API status confirmed (document or formally excluded)

**Sprint prerequisites:**
- [ ] `workers/nga_adapter/config.py` — GitHub CSV URLs, IIIF base, rate limits, dry_run
- [ ] `workers/nga_adapter/client.py` — CSV download, five-table join, image primary
      selection, freshness guard, enumeration with `objectid ASC` sort
- [ ] `workers/nga_adapter/rights.py` — NGA Rights Matrix v1 (image-record integer-flag)
- [ ] `workers/nga_adapter/normalize.py` — field mapping per Article 5, IIIF URL
      construction, anchor type derivation
- [ ] `workers/nga_adapter/technical.py` — `nga_openaccess_v1` schema standard
- [ ] `workers/nga_adapter/store.py` — `derive_anchor_type` via school/nationality/
      classification rules, `StoreRuntime` with `source_slug="nga"`, join-consistency guard

### Article 12 — Subsequent Decisions

**DD-NGA-002** (NGA Production Activation): Drafted upon Asset Zero completion, pilot
completion, and SC-1 through SC-10 passing.

---

## Risk Register

| ID | Risk | Probability | Severity | Mitigation |
|---|---|---|---|---|
| R-1 | `dataServices` REST API used unofficially; endpoints change without notice | Medium | High | SA-14 enforces CSV-only primary path; dataServices explicitly excluded in Article 3.2 |
| R-2 | `maxpixels` caps open access image resolution below 1024px on some records | Medium | Medium | Gate 3 confirmation; adapter implements cap check per Article 4.4 |
| R-3 | GitHub CSV download rate limit hit during large pilot run (five files) | Low | Low | Retry with backoff; cache files locally; single batch download |
| R-4 | SA-9 not ratified before Sprint 3 — five-institution remap branch | High | High | SA-9 must be drafted immediately; treat as Sprint 3 blocking condition |
| R-5 | SA-14 not ratified before Sprint 1 — CSV ingestion paradigm undefined | High | High | SA-14 is listed as blocking for Sprint 1; must be drafted first |
| R-6 | `openaccess` integer field parsing: empty string or None in CSV row | Medium | Medium | `int(row.get("openaccess", 0) or 0) == 1` guard in client.py |
| R-7 | Multiple primary images per object (viewtype = "primary" > 1) | Low | Low | Select lowest `sequence` among primaries; log and continue |
| R-8 | Collection page URL pattern differs from `art-object-page.{objectid}.html` | Low | Low | Gate 3 confirmation; amend Article 9 template if pattern differs |
| R-9 | Anchor type misclassification for American art with no school/nationality terms | Medium | Medium | Sprint 2 anchor-type audit; fallback `"cultural"` acceptable if no evidence |
| R-10 | Priority illustrator gap (Redouté, Buffon) not addressed by NGA holdings | Certain | Info | NGA fills American/Spanish gap; BnF/natural history gap remains unaddressed per DD-GALLICA-003 §5.3 |

---

## Ratification

This Decision is in Draft status. Requires Director sign-off (`opengracelabs`) and
second-human approval. Both parties must review:

- **Part II.1** (Commercial Reuse Qualification — the production approval finding)
- **Article 3.2** (prohibition on `dataServices` undocumented API)
- **Article 10** (SA-14 and SA-13 as Sprint 1 blockers; SA-9 as Sprint 3 blocking condition)
- **Article 11** (Activation Prerequisites)

Upon ratification: SA-14 must be drafted immediately (blocks Sprint 1); SA-13 may be
drafted concurrently; SA-9 must be drafted and ratified before Sprint 3 begins.

| Role | Name | Date |
|---|---|---|
| Director | opengracelabs | — |
| Second Human | — | — |
