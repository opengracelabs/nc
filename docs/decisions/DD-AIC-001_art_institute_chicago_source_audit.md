# DD-AIC-001 — Art Institute of Chicago Open Access Source Audit

| Field | Value |
|---|---|
| **Decision ID** | DD-AIC-001 |
| **Type** | Source Audit |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-09 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first Art Institute of Chicago governance document |
| **Governing Documents** | Institution Coverage Audit v1.0 · Europeana Rights Matrix v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 · Institution Factory v1 |

---

## Background

The Art Institute of Chicago (AIC) is one of the oldest and largest art museums in the
United States, holding a permanent collection of approximately 300,000 objects spanning
five thousand years of art history across all world regions. The AIC's Open Access
programme, which pre-dates and complements its CC0 image release, makes all images of
public domain works in the collection freely available with no restrictions on use.
The `is_public_domain` field in the AIC's public API is the governing attestation.
As of 2024, more than 60,000 works carry `is_public_domain: true` — a volume that
is smaller than The Met's 492,000 but concentrated in high-commercial-value categories:
French Impressionism, Japanese woodblock prints, European Old Masters, and Prints and
Drawings. The AIC's Impressionist and Post-Impressionist holdings are among the finest
outside France, creating a uniquely strong pipeline for NC's France and Western Europe
place pages.

The Institution Coverage Audit v1.0 placed the AIC in Wave 4 onboarding alongside
The Met, the Getty, and the British Library. DD-MET-001 (2026-06-09) onboarded The Met
as Institution #7. This Decision constitutes the formal Stage 1 Discovery Report and
initiates Stage 2 Governance for the AIC as Institution #8.

This Decision presents five governance complexities that are distinct from or absent
in DD-MET-001:

1. **Image URL construction — no `primaryImage` field.** The AIC API does not return
   a direct image URL. Image delivery requires IIIF URL construction from the
   `image_id` field (a UUID string). Rights checks, normalize.py representative
   media URL assignment, and the image presence gate in the AIC rights classifier
   must all use `image_id` rather than a direct URL string. This is the first NC
   institution where `representative_media_url` is derived rather than copied.

2. **Cannot reuse Met Rights Matrix v1.** The Met Rights Matrix v1 governs
   `isPublicDomain` (camelCase) and `primaryImage` (direct URL). The AIC uses
   `is_public_domain` (snake_case) and `image_id` (IIIF UUID). The governing field
   names are different, the image presence check is different, and the policy
   instrument is institution-specific. A new AIC Rights Matrix v1 is required,
   structurally equivalent to Met Rights Matrix v1 but with AIC-specific field
   bindings. This is the governing answer to the question posed at audit initiation:
   **AIC cannot reuse Met Rights Matrix v1.**

3. **Standard REST pagination — no all-IDs-at-once response.** The Met returns all
   public-domain object IDs in a single API response for cursor-then-iterate
   enumeration. The AIC uses standard paginated REST (`page`, `limit`, `next_url`
   in a `pagination` block), supplemented by an Elasticsearch-based search endpoint
   for filtered enumeration. The AIC client will use the search endpoint with
   `query[term][is_public_domain]=true` as the primary enumeration path.

4. **Confirmed IIIF Presentation API — manifests available.** Unlike The Met, where
   IIIF manifest availability required a Gate 3 verification gate, the AIC provides
   confirmed IIIF Presentation API manifests at
   `https://api.artic.edu/api/v1/artworks/{id}/manifest.json`. This removes one
   activation uncertainty present in DD-MET-001. However, the IIIF Image API URL
   pattern (`/iiif/2/`) indicates Image API 2.x, and the Presentation API manifest
   version (2.1 vs 3.0) requires live verification at Gate 3.

5. **Shared store.py boolean PD remap — requires extension.** DD-MET-001 Sprint 3
   introduced a source-slug-specific remap in `shared_media_adapter/store.py` to
   prevent terminal value attestation (`"verified_cc0"`) in rights evidence for
   the Met. The AIC uses the same boolean PD → CC0 path and will encounter the
   identical V4 class violation unless the remap is extended to cover
   `source_slug == "aic"`. This is a required Sprint 3 prerequisite for AIC.

---

## Part I — Source Classification Audit

**Institution name:** Art Institute of Chicago (AIC)

**Institution type:** Museum, nonprofit institution, independent

**Collection type:** Encyclopedic art museum — paintings, sculpture, prints and
drawings, photography, textiles, decorative arts, architectural drawings, Asian art,
African and Amerindian art, arms and armor

**Open access programme:** AIC Open Access. CC0 designation for all works where
`is_public_domain: true`. No separate application required. No authentication
required for the AIC public API.

**API type:** Custom REST JSON API
**API base URL:** `https://api.artic.edu/api/v1`
**API version:** v1 (path-versioned, no published deprecation schedule)
**Pagination:** Standard page/limit REST with `pagination.next_url` cursor
**Authentication:** None required (open, unauthenticated access)
**Rate limiting:** No published limit; 5 req/s is the accepted NC convention for
unauthenticated public APIs

**Key endpoints:**
- `GET /artworks?page=N&limit=100&fields=…` — paginated full collection
- `GET /artworks/{id}` — single artwork by integer ID
- `GET /artworks/search` — Elasticsearch-based filtered search
- `GET /artworks/{id}/manifest.json` — IIIF Presentation manifest (confirmed)

**PD collection size:** ≥ 60,000 works (is_public_domain: true as of 2024)

**Total collection size:** ≈ 300,000 objects

**Rights field:** `is_public_domain` (boolean) — the sole governing attestation

**Secondary rights field:** `copyright_notice` (string, often null for PD works)

**IIIF:** Confirmed — Image API 2.x, Presentation API manifests available

**OECD taxonomy:** Museum / Visual Art / Open Access / Public Domain

**NC institution tier:** Tier 1 Core — CC0, direct, no aggregator intermediary

**Institution onboarding wave:** Wave 4 (alongside The Met, Getty, British Library)

**Proposed institution number:** #8

**Proposed source ID:** `aic`

**Proposed source priority:** 9

**Differentiating commercial strengths:**
- French Impressionism and Post-Impressionism (Seurat, Monet, Caillebotte, Toulouse-Lautrec,
  Renoir, Cézanne, Degas) — world-class for France, Paris, and Île-de-France place pages
- Japanese woodblock prints (Hiroshige, Hokusai, Utamaro, Kuniyoshi) — supplemental
  to Met Japan pilot; different impressions, distinct Illustration Opportunities
- European Old Master prints and drawings — strong natural history illustration pipeline
- American art (Chicago School, American Modernism) — North America place pages
- African and pre-Columbian art — critical for NC's geographic gap (Africa, Latin America)
- Architectural drawings (Art Institute is also home to the Ryerson and Burnham Libraries)

**Geographic coverage added:** France (primary); Japan (supplemental); sub-Saharan Africa;
Mesoamerica and South America; United States Midwest

---

## Part II — Rights Strategy Audit

### II.1 — Can AIC Reuse Met Rights Matrix v1?

**Governing question:** The audit initiating message asked whether AIC can reuse the
Met Rights Matrix v1 (`policy_id: "met_rights_matrix_v1"`, governed by DD-MET-001
Article 2).

**Answer: No.**

The Met Rights Matrix v1 is bound to three Met-specific field names:
1. `isPublicDomain` (camelCase boolean) — the sole PD attestation field
2. `primaryImage` (direct JPEG URL string) — the image presence gate
3. `rightsAndReproduction` (string) — secondary rights annotation

The AIC uses:
1. `is_public_domain` (snake_case boolean) — same logical function, different field name
2. `image_id` (UUID string) — requires IIIF URL construction; not a direct image URL
3. `copyright_notice` (string) — secondary annotation, different field name

The image presence gate is architecturally different: Met's `_present_image(primaryImage)`
checks for a non-empty string URL. AIC's gate must check for a non-null, non-empty
`image_id` UUID. A Met classifier applied to an AIC record would test for `"isPublicDomain"`
in `record` and block every AIC record as `missing_rights_field`, since AIC's field is
`"is_public_domain"`. This is a hard functional incompatibility, not merely a naming
inconvenience.

The policy ID `"met_rights_matrix_v1"` is also institution-specific. It should never
appear in the rights evidence of a non-Met record.

**Ruling:** A new **AIC Rights Matrix v1** (`policy_id: "aic_rights_matrix_v1"`) is
required. It is structurally equivalent to the Met Rights Matrix v1 — same boolean
architecture, same three classification outcomes (ALLOWED / BLOCKED / no REVIEW_REQUIRED
class), same CC0_URI as the authorised rights URI — but all field bindings are
AIC-specific.

### II.2 — AIC Rights Matrix v1 Classification Rules

| Rule ID | Condition | Outcome | rights_basis |
|---|---|---|---|
| AIC-R-1 | `record` is not a dict (None or other) | BLOCKED | `missing_rights_field` |
| AIC-R-2 | `"is_public_domain"` not in `record` | BLOCKED | `missing_rights_field` |
| AIC-R-3 | `record["is_public_domain"] is not True` | BLOCKED | `not_public_domain` |
| AIC-R-4 | `image_id` is null, empty, or not a string | BLOCKED | `no_image_id` |
| AIC-R-5 | All prior rules pass | ALLOWED | `aic_is_public_domain` |

**ALLOWED outcome:**
- `decision`: ALLOWED
- `rights_statement_uri`: CC0_URI (`"https://creativecommons.org/publicdomain/zero/1.0/"`)
- `rights_status`: `"pending_verification"` (worker ceiling, CI-4)
- `rights_policy_id`: `"aic_rights_matrix_v1"`

**REVIEW_REQUIRED class:** Not applicable. AIC Rights Matrix v1 has no review path.
Any record that does not satisfy AIC-R-1 through AIC-R-4 is BLOCKED. This mirrors
Met Rights Matrix v1 exactly.

**Secondary field `copyright_notice`:** This field is informational only. It is
extracted into `media_technical_metadata.content` for audit purposes and into
`media_rights.rights_evidence` as `aic_copyright_notice`. It does not alter the
classification outcome. A non-null `copyright_notice` on a `is_public_domain: true`
record is not a conflict — AIC applies this pattern for provenance annotation.

### II.3 — Rights Evidence Requirements (CI-8)

Constitutional Invariant CI-8 requires nine fields in `media_rights.rights_evidence`.
For AIC records, the following additional field must also appear:

- `aic_is_public_domain` (boolean) — the raw value of `record["is_public_domain"]`

This is the direct analogue of `met_is_public_domain` (DD-MET-001 Article 2.4).
It provides the human reviewer with the verbatim source attestation alongside the
NC matrix classification.

### II.4 — Shared Store Remap Requirement

The shared `media_adapter/store.py` `build_rights_evidence` function currently remaps
terminal status values for `source_slug == "met"`:

```python
if runtime.source_slug == "met":
    worker_classified_status = {
        "verified_cc0": "classified_cc0",
        "verified_pd": "classified_pd",
    }.get(str(worker_classified_status), worker_classified_status)
```

Because AIC uses the same boolean PD → CC0_URI path, the shared
`classify_rights(CC0_URI)` call in `write_normalized_record` will return
`rights_status: "verified_cc0"`. Without extension, this terminal value would appear
as `worker_classified_status` in the rights evidence — a V4-class violation (CI-4).

**Required modification (Sprint 3 prerequisite):** Extend the remap condition to
`if runtime.source_slug in {"met", "aic"}:`. Injection of `aic_is_public_domain` into
evidence must also be added under the same condition, symmetrically with the Met branch.

**Architectural note:** The branching accumulation on `source_slug` is a code smell.
A future standards amendment (SA-9 candidate) should introduce a `boolean_pd_mode`
flag in `StoreRuntime` that generalises this behaviour for all boolean-PD institutions
without source-slug branching.

---

## Part III — API Surface Audit

### III.1 — Enumeration Strategy

**Primary path:** Elasticsearch search with PD filter

```
GET /artworks/search?query[term][is_public_domain]=true&limit=100&page=1&fields=id,is_public_domain,image_id,title
```

Response:
```json
{
    "data": [...],
    "pagination": {
        "total": 60000,
        "limit": 100,
        "total_pages": 600,
        "current_page": 1,
        "next_url": "https://api.artic.edu/api/v1/artworks/search?..."
    }
}
```

The `pagination.next_url` field is the cursor. When `next_url` is absent or null,
enumeration is complete.

**Secondary path:** Full paginated scan with client-side PD filter

```
GET /artworks?page=N&limit=100&fields=id,is_public_domain,image_id,...
```

The search path is preferred for production because it reduces network load by
returning only PD records. The full scan path is preferred for replay and audit
because it provides a stable, deterministic enumeration order (by integer `id`).

**Comparison to Met:** The Met's all-IDs-at-once response (`GET /objects?departmentIds=…`)
allowed the client to build a complete enumeration list in a single request, then
iterate individually. AIC requires iterating page-by-page. This affects the client
architecture: there is no equivalent of Met's `extract_object_ids()` bulk function.

### III.2 — Single-Record Fetch

```
GET /artworks/{id}?fields=id,title,is_public_domain,image_id,...
```

The `fields` query parameter controls which fields appear in the response. For NC
intake, the required fields are documented in Article 5 of this Decision. Omitting
`fields` returns all available fields, which is acceptable for initial sprint development
and replay fidelity.

### III.3 — Rate Limiting

The AIC API has no published rate limit. NC shall apply the convention of 5 req/s
with burst 10, matching the Met configuration. The AIC API is unauthenticated and
publicly documented; it is architecturally appropriate to treat it identically to the
Met for rate limiting purposes.

### III.4 — Field Selection (fields= parameter)

The AIC API supports a `fields` query parameter that restricts the response to named
fields. For production enumeration, the following field set is authorised for the
initial sprint. Additions require a Standards Amendment:

Required for rights classification:
- `id`, `is_public_domain`, `image_id`

Required for normalization:
- `title`, `date_display`, `date_start`, `date_end`
- `artist_display`, `artist_title`
- `place_of_origin`, `department_title`, `department_id`
- `artwork_type_title`, `medium_display`
- `subject_titles`, `classification_titles`, `style_titles`
- `copyright_notice`, `main_reference_number`
- `alt_image_ids`, `api_link`, `thumbnail`

Required for IIIF delivery:
- `image_id`, `alt_image_ids`

---

## Part IV — IIIF Governance Audit

### IV.1 — IIIF Status

Unlike The Met — where IIIF manifest availability was classified as uncertain and
required a Gate 3 verification gate — the AIC has confirmed, documented IIIF support:

| Component | Status | URL Pattern |
|---|---|---|
| IIIF Image API | Confirmed | `https://www.artic.edu/iiif/2/{image_id}/` |
| IIIF Image level | Level 2 (assumed) | Full region/size/rotation/quality/format |
| IIIF Presentation | Confirmed | `https://api.artic.edu/api/v1/artworks/{id}/manifest.json` |
| IIIF Image API version | 2.x (URL path `/2/`) | Requires live version confirmation |
| IIIF Presentation version | Unknown — 2.1 or 3.0 | Requires live manifest verification at Gate 3 |

### IV.2 — IIIF Image URL Construction

Because AIC does not return a direct image URL, `representative_media_url` must be
constructed from `image_id`. The authorised construction pattern is:

```
https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg
```

Where `843,` is the IIIF Image API size parameter requesting 843 pixels wide with
proportional height. This is consistent with AIC's standard preview delivery size.

For full-resolution delivery:
```
https://www.artic.edu/iiif/2/{image_id}/full/full/0/default.jpg
```

**Implications for normalize.py:**
1. `representative_media_url` cannot be copied from a raw API field.
   It must be constructed: `f"https://www.artic.edu/iiif/2/{raw['image_id']}/full/843,/0/default.jpg"`
   when `image_id` is non-null and non-empty.
2. `representative_media_url` must be `None` when `image_id` is absent or empty.
3. `additional_images` must be constructed from `alt_image_ids` using the same pattern.

**Implications for media_file.source_url:**
The `source_url` column in `media_file` stores the image delivery URL (not the
collection page URL). For AIC, this is the constructed IIIF URL. The collection
page URL (`https://www.artic.edu/artworks/{id}`) maps to `source_item.canonical_source_url`
(via `normalized["source_url"]`), following the convention established in
`contracts.py` and confirmed in DD-MET-001.

### IV.3 — IIIF Presentation API Version Gate

If live verification at Gate 3 confirms that AIC's Presentation manifests are IIIF
Presentation API 2.1, a Standards Amendment analogous to SA-3 (Gallica IIIF 2.1
bridging) will be required before activation. If manifests are confirmed 3.0, no
bridging is needed.

This gate is classified Tier 2 (exit gate) — it does not block DD-AIC-001 ratification
but it does block DD-AIC-002 (production activation).

### IV.4 — IIIF Manifest as Secondary Evidence Asset

The IIIF Presentation manifest URL (`https://api.artic.edu/api/v1/artworks/{id}/manifest.json`)
provides a machine-readable provenance record for each work. The rights evidence
must include `aic_manifest_url` to enable downstream reviewers to inspect the
institutional IIIF manifest. This is analogous to the Gallica IIIF manifest requirement
in DD-GALLICA-001.

---

## Part V — Commercial Opportunity Assessment

### V.1 — Primary Commercial Tier: French Impressionism

The AIC holds what is widely considered the finest collection of French Impressionist
and Post-Impressionist works outside France. Key holdings include works by Seurat
(two), Monet (33+), Caillebotte (8), Renoir, Degas, and Toulouse-Lautrec. These
works are Illustration Opportunities bound to France, Paris, Île-de-France, Normandy,
Provence, and the Côte d'Azur. No other NC institution currently in pipeline has
equivalent depth for French place pages. This is AIC's primary commercial differentiator.

### V.2 — Secondary Tier: Japanese Prints

The AIC holds thousands of Japanese woodblock prints, including major series by
Hiroshige, Hokusai, Utamaro, and Kuniyoshi. These provide supplemental content for
NC's Japan place pages. However, this tier overlaps with the Met Japan pilot
(DD-MET-001 Article 6). AIC and Met hold different physical impressions — they are
distinct Illustration Opportunities — but a source priority convention should be
established. The Met pilot runs first; AIC Japanese prints are Wave 2 at minimum.

### V.3 — Geographic Gap Coverage

The AIC's collections of African art, Oceanic art, and pre-Columbian art address
three of the four critical geographic gaps identified in the Institution Coverage
Audit v1.0 (Africa, Pacific, Latin America). These are anchor_type: cultural/geographic
and represent a long-term pipeline for commercial tiers that NC currently has no
inventory for. Pilot inclusion is deferred to Wave 2 pending place-page infrastructure
for these regions.

### V.4 — Deduplication Assessment

**AIC vs Met:** Both hold Japanese prints. Objects are physically distinct (different
impressions, different accession numbers). No object-level deduplication is required.
Artist/series-level priority convention: Met records take precedence for the initial
Japan build; AIC records supplement where Met has gaps.

**AIC vs Europeana/DPLA:** AIC is not known to contribute records to Europeana or
DPLA through a digital hub. Live verification required at Gate 2 (Connectivity).
If AIC records appear in either aggregator, the deduplication protocol from
DD-EUR-001 and DD-DPLA-001 applies.

### V.5 — Volume Estimate

| Classification | Estimated Count |
|---|---|
| Total AIC collection | ~300,000 |
| is_public_domain: true | ≥60,000 |
| is_public_domain: true AND image_id non-null | ~55,000 (estimated) |
| Estimated MASTERWORK tier (≥1850, major artist, place-associated) | ~5,000–8,000 |
| French Impressionist/Post-Impressionist, PD, image present | ~2,000–3,000 |
| Japanese woodblock prints, PD, image present | ~4,000–6,000 |

---

## Decision

### Article 1 — Source Classification

**1.1** The Art Institute of Chicago is classified as a **Tier 1 Core** content
institution for NC's commercial pipeline.

**1.2** The AIC is assigned institution number **#8**, following The Metropolitan
Museum of Art (#7, DD-MET-001).

**1.3** The governing onboarding instrument is the Institution Factory v1 and the
Institution Factory Constitution v1.0. The AIC must complete all nine stages and
pass all mandatory exit gates before operational status is granted.

**1.4** The AIC's Open Access programme is a direct CC0 release. No aggregator
intermediary exists between the AIC and NC. The AIC is the `dataProvider` and
the `provider` in all NC substrate records.

**1.5** The source identifier is `aic`. This identifier is permanent once written
to the source registry and must not be changed after Asset Zero is written. Source
registry parameters are defined in Article 9.

### Article 2 — AIC Rights Matrix v1

**2.1** The Art Institute of Chicago requires a new institution-specific rights
matrix: **AIC Rights Matrix v1** (`policy_id: "aic_rights_matrix_v1"`).

**2.2** The Met Rights Matrix v1 (`policy_id: "met_rights_matrix_v1"`, governed
by DD-MET-001 Article 2) does not govern AIC records and must never be applied to
them. The field name `isPublicDomain` is not present in AIC API responses. The
image presence check in Met Rights Matrix v1 (`primaryImage` string URL) is
incompatible with AIC's `image_id` UUID pattern.

**2.3** AIC Rights Matrix v1 governs the following classification logic:

- **BLOCKED (missing_rights_field):** record is not a dict; or `"is_public_domain"`
  is absent from record
- **BLOCKED (not_public_domain):** `record["is_public_domain"] is not True`
- **BLOCKED (no_image_id):** `image_id` is null, empty string, or not a string
- **ALLOWED:** all prior conditions pass — `rights_statement_uri = CC0_URI`,
  `rights_status = "pending_verification"`

**2.4** AIC Rights Matrix v1 has **no REVIEW_REQUIRED class**. Every record is
either ALLOWED or BLOCKED. This is identical in structure to Met Rights Matrix v1.

**2.5** `rights_status` in the ALLOWED outcome is `"pending_verification"`. The
worker never sets a terminal rights status (CI-4, FM Constitution Article 12).

**2.6** The following fields must appear in `media_rights.rights_evidence` for all
AIC records, in addition to the nine CI-8 required fields:

- `aic_is_public_domain` (boolean) — verbatim value of `record["is_public_domain"]`
- `aic_copyright_notice` (string or null) — verbatim value of `record.get("copyright_notice")`
- `aic_manifest_url` (string or null) — constructed IIIF manifest URL,
  `f"https://api.artic.edu/api/v1/artworks/{id}/manifest.json"`

**2.7** The shared `media_adapter/store.py` boolean PD remap must be extended to
cover `source_slug == "aic"` before any AIC record is written to the substrate.
The `build_rights_evidence` function must also inject `aic_is_public_domain` when
`runtime.source_slug == "aic"`, following the precedent of the Met branch. This
extension is a Sprint 3 prerequisite for the AIC adapter.

### Article 3 — API Governance

**3.1** The authorised AIC API base URL is `https://api.artic.edu/api/v1`. All
requests must use HTTPS. HTTP requests are not permitted.

**3.2** The primary enumeration path for production ingestion is the Elasticsearch
search endpoint with `query[term][is_public_domain]=true`. The paginated full-scan
path is authorised for replay and audit runs.

**3.3** Enumeration is cursor-driven via `pagination.next_url`. When `pagination.next_url`
is absent or null, enumeration is complete. Enumeration must not rely on
`pagination.total` for loop termination.

**3.4** The rate limit for AIC API requests is **5 req/s** with **burst 10**.
This matches the Met configuration. The AIC API user-agent must identify NC:
`NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)`.

**3.5** The `fields` query parameter must be specified for production enumeration
requests to limit response size. The authorised field set for sprint development
is documented in Part III.4. Changes to the field set require a sprint audit review.

**3.6** AIC API does not require authentication. No API key, token, or credential
is stored for the AIC in NC configuration. If the AIC introduces authentication in
a future API version, this Decision must be amended before the new version is adopted.

**3.7** Dry-run mode (`aic_dry_run = True`) must be the default configuration value
in `workers/aic_adapter/config.py`. Production activation requires explicit
override and two-human sign-off (CI-2, IFC-9).

### Article 4 — IIIF Governance

**4.1** The AIC provides confirmed IIIF support. Image delivery is via IIIF Image
API with the base URL `https://www.artic.edu/iiif/2/{image_id}/`.

**4.2** The `representative_media_url` field in the normalized record must be
**constructed** from `image_id` using the pattern:
```
https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg
```
It must be `None` when `image_id` is null, empty, or not a string.

**4.3** The collection page URL for `source_item.canonical_source_url` (set via
`normalized["source_url"]`) must be constructed as:
```
https://www.artic.edu/artworks/{id}
```
where `{id}` is the integer artwork ID from the API response.

**4.4** IIIF Presentation manifest URL: `https://api.artic.edu/api/v1/artworks/{id}/manifest.json`.
This URL must be stored in `aic_manifest_url` within `media_rights.rights_evidence`
as required by Article 2.6.

**4.5** IIIF Presentation API version must be verified at Gate 3 (Connectivity).
If manifests are confirmed IIIF Presentation 3.0: no bridging required. If manifests
are IIIF Presentation 2.1: a Standards Amendment is required (see Article 10).
This is a Gate 3 exit-gate condition for DD-AIC-002.

**4.6** IIIF Image API version is indicated by the `/2/` path segment. This
implies Image API 2.x. Live verification of the `info.json` response is required
at Gate 3 to confirm the exact version and supported level.

### Article 5 — Metadata Field Mapping

The following table governs the normalization contract for AIC records. All mappings
are expressed as: AIC API field → NC substrate field → normalization rule.

| AIC API Field | NC Substrate Field | Rule |
|---|---|---|
| `id` (int) | `record_id` | `str(raw["id"])` — stringify; None if absent or falsy |
| `f"…/artworks/{id}"` | `source_url` | Constructed from `id` — not a direct field |
| `title` (str) | `title` | Strip whitespace; None if empty |
| `date_display` (str) | `date` | Strip; None if empty |
| `date_start` (int) | `date_start` | Integer; None if absent |
| `date_end` (int) | `date_end` | Integer; None if absent |
| `artist_display` (str) | `creator` | Strip; None if empty |
| `subject_titles` (list) | `subject_terms` | List of strings; empty list if absent |
| `classification_titles` (list) | `description` | Join with ", " as fallback description |
| `artwork_type_title` (str) | `edm_type` | Strip; None if empty |
| `place_of_origin` (str) | `place_of_origin` | Strip; None if empty |
| `department_title` (str) | `department` | Strip; None if empty |
| `medium_display` (str) | `medium` | Strip; None if empty |
| `style_titles` (list) | `style_titles` | List of strings |
| `copyright_notice` (str/null) | `copyright_notice` | Strip; None if null/empty |
| `main_reference_number` (str) | `accession_number` | Strip; None if empty |
| `is_public_domain` (bool) | `aic_is_public_domain` | Raw boolean value |
| `image_id` (str/null) | `aic_image_id` | UUID string; None if absent |
| Constructed | `representative_media_url` | IIIF URL from `image_id`; None if no `image_id` |
| `alt_image_ids` (list) | `additional_images` | List of constructed IIIF URLs |
| Constructed | `aic_manifest_url` | `f"…/{id}/manifest.json"`; None if no `id` |
| `api_link` (str) | `aic_api_link` | Canonical API URL for this record |
| `thumbnail` (obj/null) | `thumbnail` | Pass through as-is; None if absent |
| SHA256(canonical JSON) | `raw_payload_hash` | Sort keys, no separators |
| Classified | `rights_uri` | CC0_URI if ALLOWED; None if BLOCKED |
| Classified | `rights_decision` | AIC Rights Matrix v1 outcome string |

**Anchor type derivation (Article 5.2):** The `derive_anchor_type` function in
`workers/aic_adapter/store.py` must evaluate in the following precedence order:
1. `media_type_id == "map"` → `"geographic"`
2. `subject_terms` contains any biological keyword → `"biological"`
   (keyword set mirrors Met: "bird", "fish", "flower", "botanical", "plant", "animal",
   "insect", "mammal", "reptile", "amphibian")
3. `place_of_origin` is non-null → `"geographic"`
4. Default → `"cultural"`

### Article 6 — Pilot Scope

**6.1** The AIC pilot is authorised for **France** as the target place context.
This differentiates the AIC pilot from the Met pilot (Japan), tests the
`place_of_origin`→place-association path, and exercises NC's highest-commercial-value
AIC tier (French Impressionism).

**6.2** The pilot target is **75 assets** with a secondary sub-cap of 25 from
outside the French Impressionist tier (Japanese prints or Prints and Drawings)
to verify anchor_type derivation across multiple departments.

**6.3** Pilot filter criteria:
- Primary batch (50 assets): `is_public_domain: true`, `place_of_origin` contains
  "France", `date_end ≤ 1900`, `image_id` non-null
- Secondary batch (25 assets): `is_public_domain: true`, `department_title` contains
  "Prints and Drawings" OR "Asian Art", `date_end ≤ 1900`, `image_id` non-null

**6.4** Pilot duration: 90 days from Asset Zero write date.

**6.5** Pilot activation requires two-human sign-off (CI-2). One signatory must be
the Director (`opengracelabs`). The second may be any authorised reviewer.

**6.6** No production traffic or commercial serving may be enabled for AIC assets
until the pilot completes and DD-AIC-002 is ratified.

### Article 7 — Asset Zero Requirements

**7.1** Asset Zero is the first AIC record written to the M36 substrate. It must
satisfy all of the following:

- `is_public_domain: true`
- `image_id` non-null and resolvable to a IIIF image URL that returns HTTP 200
- `place_of_origin: "France"` (for France pilot alignment)
- `date_end ≤ 1900`
- Clear artist attribution (non-anonymous, known artist with established provenance)
- MASTERWORK tier (globally recognised work, major artist, institution-defining holding)

**7.2** Recommended Asset Zero candidate: Georges-Pierre Seurat, *A Sunday on La
Grande Jatte — 1884* (1884–86). AIC accession: 1926.224. Place of origin: France.
Subject: The Île de la Grande Jatte, Asnières-sur-Seine (northwest of Paris).
Expected anchor_type: `geographic` (France / Île-de-France place page). Commercial
tier: MASTERWORK. This work is universally recognised, directly associated with the
France/Paris/Île-de-France place hierarchy, and represents the AIC's most iconic
single holding.

**7.3** Alternative Asset Zero candidates (if Seurat fails image resolution):
- Claude Monet, any water lilies or Argenteuil study, France, pre-1900
- Gustave Caillebotte, any Paris street scene, France, pre-1890
- Any pre-1900 European natural history print from Prints and Drawings with
  confirmed IIIF image_id

**7.4** Asset Zero checklist:
- [ ] Live API fetch: `GET /artworks/{id}` returns HTTP 200
- [ ] `is_public_domain: true` confirmed in response
- [ ] `image_id` non-null, non-empty in response
- [ ] IIIF image URL constructed and HTTP 200 confirmed
- [ ] IIIF Presentation manifest URL confirmed (HTTP 200)
- [ ] IIIF Presentation manifest version recorded
- [ ] AIC Rights Matrix v1 classifies as ALLOWED
- [ ] `normalize_record()` produces no mandatory field warnings
- [ ] `write_record()` returns `status: "written"`, `writes: 7`
- [ ] `media_rights.rights_status = "pending_verification"` in DB
- [ ] `media_rights.rights_evidence.aic_is_public_domain` = True in DB
- [ ] `media_rights.rights_evidence.aic_manifest_url` non-null in DB
- [ ] Two-human sign-off on Asset Zero record

### Article 8 — Success Criteria

**SC-1 (Asset Zero):** Asset Zero is written to the M36 substrate with
`rights_status = "pending_verification"`. The IIIF manifest URL resolves with
HTTP 200. Two-human sign-off is complete.

**SC-2 (IIIF confirmation):** The IIIF Presentation manifest version is determined
and documented. If 2.1, SA-3 analogue is raised before pilot activation. If 3.0,
bridging exemption is recorded.

**SC-3 (Pilot volume):** 75 pilot assets are written. BLOCKED rate ≤ 5%.
Of BLOCKED records, ≥ 90% have `rights_basis: "not_public_domain"` or
`"no_image_id"` (expected). Unexpected block reasons must be investigated.

**SC-4 (FM-4 — permanent):** Zero FM-4 violations across all 75 pilot writes.
No foundation model output appears in any `media_rights` column. This criterion
is non-waivable (IFC-3).

**SC-5 (No terminal attestation):** Zero records with `worker_classified_status`
set to `"verified_cc0"` or `"verified_pd"` in `media_rights.rights_evidence`.
All must show `"classified_cc0"` or `"classified_pd"` (worker-classification labels).

**SC-6 (Anchor type fidelity):** Anchor type derivation is correct for ≥ 95% of
pilot assets. At least one biological, one geographic, and one cultural record is
present in the pilot set. Manual spot-check of 10% sample.

**SC-7 (AIC evidence completeness):** `aic_is_public_domain`, `aic_copyright_notice`,
and `aic_manifest_url` are present in `media_rights.rights_evidence` for all
ALLOWED records. SC-7 admits zero exceptions.

**SC-8 (IIIF URL resolution):** `representative_media_url` resolves to HTTP 200
for ≥ 95% of written records. Failures must be logged with the affected `image_id`
values for remediation before production activation.

**SC-9 (Human review gate):** Two-human sign-off on the pilot completion report
before DD-AIC-002 is initiated. One signatory must be the Director.

### Article 9 — Source Registry Authorization

Upon ratification of this Decision, the following entry may be written to the NC
source registry:

| Parameter | Value |
|---|---|
| `source_id` | `aic` |
| `source_name` | `Art Institute of Chicago` |
| `source_type` | `museum_open_access` |
| `institution_number` | `8` |
| `priority` | `9` |
| `auth_type` | `none` |
| `rate_limit_rps` | `5` |
| `burst` | `10` |
| `rights_policy_id` | `aic_rights_matrix_v1` |
| `api_base_url` | `https://api.artic.edu/api/v1` |
| `iiif_image_base_url` | `https://www.artic.edu/iiif/2/` |
| `iiif_manifest_template` | `https://api.artic.edu/api/v1/artworks/{id}/manifest.json` |
| `collection_page_template` | `https://www.artic.edu/artworks/{id}` |
| `schema_standard` | `aic_openaccess_v1` |
| `governance_state` | `pending_activation` |
| `onboarding_stage` | `stage_1_discovery` |
| `governing_dd` | `DD-AIC-001` |

### Article 10 — Standards Amendments

**SA-8 (Required):** AIC Open Access Adapter Profile. Defines the AIC-specific
adapter contract: `aic_openaccess_v1` schema standard, `aic_rights_matrix_v1`
policy ID, IIIF URL construction pattern, source registry parameters, and the
`fields` parameter field set. Analogous to SA-7 (Met Open Access Adapter Profile).
Must be ratified before AIC adapter sprint development begins.

**SA-3 analogue (Conditional):** Required only if Gate 3 IIIF version verification
confirms AIC Presentation API manifests are version 2.1. If manifests are 3.0,
this SA is waived. The SA-3 analogue would define AIC IIIF 2.1 → 3.0 bridging
requirements. Blocking gate for DD-AIC-002.

**SA-9 (Recommended, future):** Boolean PD Adapter Profile. Generalises the
`build_rights_evidence` boolean PD remap in `shared_media_adapter/store.py` from
`source_slug` branching to a `StoreRuntime.boolean_pd_mode` flag. This removes
accumulating source-slug conditions as additional boolean PD institutions are
onboarded. SA-9 is not required for AIC pilot but is recommended before a third
boolean PD institution is onboarded.

### Article 11 — Activation Prerequisites

The following must be satisfied before any AIC record is written to the M36 substrate:

**Constitutional prerequisites (CI-class, non-waivable):**
- [ ] SA-8 (AIC Open Access Adapter Profile) ratified
- [ ] `shared_media_adapter/store.py` boolean PD remap extended to `source_slug in {"met", "aic"}`
- [ ] `aic_is_public_domain` injection added to `build_rights_evidence` for AIC records
- [ ] `aic_dry_run = True` is the default configuration; explicit override required for production

**Gate 3 prerequisites (exit gate, must resolve before DD-AIC-002):**
- [ ] IIIF Presentation API version confirmed via live manifest fetch
- [ ] SA-3 analogue decision recorded (required or waived) based on version confirmation
- [ ] IIIF Image API `info.json` fetched and level confirmed

**Sprint prerequisites (adapter code):**
- [ ] `workers/aic_adapter/config.py` — configuration with dry-run default
- [ ] `workers/aic_adapter/client.py` — pagination cursor client with Elasticsearch search
- [ ] `workers/aic_adapter/rights.py` — AIC Rights Matrix v1 classifier
- [ ] `workers/aic_adapter/normalize.py` — IIIF URL construction, source_url construction
- [ ] `workers/aic_adapter/technical.py` — AIC-specific technical metadata schema
- [ ] `workers/aic_adapter/store.py` — `derive_anchor_type` with `place_of_origin` path,
      `StoreRuntime` with `source_slug="aic"`, `rights_policy_id="aic_rights_matrix_v1"`

### Article 12 — Subsequent Decisions

**DD-AIC-002** (AIC Production Activation) shall be drafted upon:
1. All Article 11 prerequisites satisfied
2. Asset Zero checklist complete with two-human sign-off
3. Pilot completion report approved with two-human sign-off (SC-9)
4. SC-1 through SC-9 all passing

DD-AIC-002 is the governing document for AIC production activation and governs
the transition from `governance_state: pending_activation` to `governance_state: active`.

---

## Risk Register

| ID | Risk | Probability | Severity | Mitigation |
|---|---|---|---|---|
| R-1 | IIIF Presentation manifest version is 2.1, requiring SA-3 analogue | Medium | Medium | Verify at Gate 3 before sprint completion; raise SA immediately if 2.1 confirmed |
| R-2 | `image_id` absent for a significant fraction of is_public_domain:true records | Medium | High | Pilot will characterise actual rate; BLOCKED (no_image_id) is an expected outcome |
| R-3 | AIC API versioning change or endpoint deprecation | Low | High | Pin to `api/v1`; monitor AIC API announcements; `api_link` in each record provides canonical reference |
| R-4 | Undocumented rate limiting causes 429 responses at 5 req/s | Medium | Medium | Implement exponential backoff; reduce to 3 req/s if 429s observed |
| R-5 | AIC Japanese print records duplicate Met Japan pilot Illustration Opportunities | Low | Low | Different physical objects; artist/series priority convention (Met first) is sufficient |
| R-6 | `place_of_origin` is too coarse for NC place hierarchy (country-only, no city/region) | High | Medium | AIC provides single `place_of_origin` string (e.g., "France", not "Paris"). NC place association will use country-level match; sub-country enrichment is Wave 2 |
| R-7 | Elasticsearch search query format changes between AIC API deployments | Low | Medium | Maintain full paginated scan as fallback; do not depend exclusively on search path |
| R-8 | AIC records appear in DPLA or Europeana aggregators, creating duplicate substrate entries | Unknown | Medium | Verify at Gate 2; apply existing deduplication protocols if duplicates found |
| R-9 | `build_rights_evidence` source_slug branching accumulates into unmaintainable code | Medium (long-term) | Low (now) | SA-9 (Boolean PD Adapter Profile) recommended before third boolean PD institution |
| R-10 | IIIF image resolution (843,) insufficient for NC print commerce quality standards | Low | Medium | Verify image quality at Asset Zero; switch to `full/full` for production if required |

---

## Ratification

This Decision is in Draft status. It requires:

1. Director sign-off (`opengracelabs`)
2. Second-human approval (any authorised reviewer)
3. Both parties must review Part II (Rights Strategy Audit), Article 2 (AIC Rights Matrix v1),
   and Article 11 (Activation Prerequisites) before signing.

Upon ratification:
- This Decision's status changes to Ratified
- The AIC source registry entry (Article 9) may be written
- SA-8 drafting may begin
- Sprint development may begin (blocked only by SA-8 ratification and Article 11 prerequisites)

| Role | Name | Date |
|---|---|---|
| Director | opengracelabs | — |
| Second Human | — | — |
