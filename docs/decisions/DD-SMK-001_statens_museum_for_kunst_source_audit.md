# DD-SMK-001 — Statens Museum for Kunst Open Access Source Audit

| Field | Value |
|---|---|
| **Decision ID** | DD-SMK-001 |
| **Type** | Source Audit |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-09 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first SMK governance document |
| **Governing Documents** | Institution Coverage Audit v1.0 · Europeana Rights Matrix v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 · Institution Factory v1 |
| **User designation** | Institution Candidate #9; pipeline sequence #11 following CMA (#9) and Paris Musées (#10) |

---

## Background

The Statens Museum for Kunst (SMK) — Denmark's National Gallery — holds approximately
260,000 objects spanning seven centuries of art. In 2016 SMK released its public domain
collection under CC0 via the SMK Open programme, making digital reproductions of all
public domain works freely available with no restriction on use. The SMK Open API
(`api.smk.dk/api/v1/`) provides programmatic access to approximately 70,000+ object
records, of which roughly 35,000–40,000 carry `public_domain: true`.

SMK is architecturally the closest institution to The Met and AIC among all institutions
audited in this pipeline: it uses a REST JSON API, requires no authentication, provides
a boolean public domain field, and offers confirmed IIIF. This makes SMK the most
tractable institution since AIC. However, four specific differences prevent direct
architecture inheritance and require a new SMK Rights Matrix v1.

**The governing answer to "Can SMK inherit Met/AIC architecture?":**

**Partial inheritance — at the shared substrate layer only.** SMK cannot reuse
Met Rights Matrix v1 (`met_rights_matrix_v1`) or AIC Rights Matrix v1
(`aic_rights_matrix_v1`). The rights field name is different from both (`public_domain`
vs `isPublicDomain` vs `is_public_domain`); the image check is different; and the
policy ID is institution-specific. A new **SMK Rights Matrix v1**
(`smk_rights_matrix_v1`) is required, following the boolean-form architecture pattern
established by Met and AIC. SMK Rights Matrix v1 will be the third boolean-form rights
matrix in the NC pipeline.

The shared write path (`write_normalized_record`, six M36 tables, `StoreRuntime`,
evidence structure) inherits unchanged.

This Decision presents four governance differences from AIC (the closest prior
institution):

1. **`public_domain` field — third boolean-form institution.** SMK uses
   `public_domain: boolean` at the top level of each object record. This is
   structurally identical to Met's `isPublicDomain` and AIC's `is_public_domain` in
   logic but differs in field name, requiring a new classifier. The `is not True`
   boolean-identity check applies directly once field name is corrected.

2. **Dual image delivery — direct URL and IIIF.** SMK provides both a direct image
   URL (`image_native`, a high-resolution JPEG from the IIP image server) and IIIF
   Image API access via `images[N].iiif_id`. Unlike AIC (IIIF-only via `image_id`
   construction) and Met (direct URL via `primaryImage`), SMK offers both. NC should
   use `image_native` as `representative_media_url` (direct URL, no construction
   required) and capture `images[0].iiif_id` for IIIF manifest linking. This is the
   simplest image delivery model of any IIIF-enabled institution.

3. **Confirmed IIIF Presentation API — manifest endpoint documented.** SMK provides
   IIIF Presentation manifests at
   `https://api.smk.dk/api/v1/iiif/manifest/?object_number={object_number}`. This is
   confirmed in the SMK API documentation, removes the IIIF uncertainty present in
   DD-MET-001 Gate 3, and differs from CMA (no IIIF) and Paris Musées (IIIF status
   unknown at audit time).

4. **Search-based API with `keys=*` enumeration.** The SMK API's primary enumeration
   endpoint is a search/filter interface:
   `GET /api/v1/art/search?keys=*&public_domain=true&offset=0&rows=100`. This uses
   `offset`/`rows` parameters (analogous to CMA's `skip`/`limit`) rather than AIC's
   cursor `next_url` or Met's all-IDs pattern. Termination is by
   `len(items) < rows` or `offset >= found`.

---

## Part I — Source Classification Audit

**Institution name:** Statens Museum for Kunst (SMK) — Denmark's National Gallery

**Institution type:** National museum, public institution, Danish state

**Collection focus:** Dutch and Flemish Golden Age (Rembrandt, Hals, Ruisdael,
Jordaens), Danish Golden Age (Eckersberg, Kobke, Hammershøi), French art (Matisse,
Picasso — 20th century), German/Northern European Renaissance, prints and drawings,
photography

**Open access programme:** SMK Open (2016). CC0 designation for all public domain
works. No authentication required.

**API type:** REST JSON, search-based
**API base URL:** `https://api.smk.dk/api/v1`
**Key endpoints:**
- `GET /api/v1/art/search?keys=*&public_domain=true&offset=N&rows=100` — paginated
  enumeration
- `GET /api/v1/art/?object_number={id}` — single artwork fetch
- `GET /api/v1/iiif/manifest/?object_number={id}` — IIIF Presentation manifest

**Authentication:** None required (open, unauthenticated access)

**Pagination:** Offset/rows. Response includes `found` (total count), `offset`,
`rows`, `items` array. Termination: `len(items) < rows` or `offset + rows >= found`.

**Sort requirement:** `sort=id` or equivalent stable sort must be applied for replay
determinism. Unstable sort causes CI-8 replay inconsistency.

**Rate limiting:** Not documented; NC convention 5 req/s applies.

**PD collection size:** ~35,000–40,000 works (public_domain: true, has_image: true)

**IIIF:** Confirmed — Image API 2.x and Presentation API manifests

**NC institution tier:** Tier 1 Core — CC0, direct, no aggregator intermediary

**Proposed institution number:** #11 (user designation: Candidate #9)

**Proposed source ID:** `smk`

**Proposed source priority:** 12

**Differentiating commercial strengths:**
- Danish Golden Age (Eckersberg, Hammershøi, Kobke) — NC's first and only
  Scandinavia/Copenhagen content
- Dutch/Flemish Golden Age (Rembrandt school, Hals, landscape painters) —
  supplemental Netherlands coverage
- Northern European prints and drawings — natural history illustration pipeline
- Hammershøi interiors — unique architectural/cultural anchor for Copenhagen
  place pages

**Geographic coverage added:** Denmark (new — zero current coverage); Copenhagen
(city-level); supplemental Netherlands and Northern Europe

---

## Part II — Rights Strategy Audit

### II.1 — Can SMK Inherit Met/AIC Rights Architecture?

**Answer: No — for the same architectural reason as AIC cannot inherit Met.**

The field bindings are institution-specific. Met Rights Matrix v1 checks
`"isPublicDomain" not in record` and `record.get("isPublicDomain") is not True`.
AIC Rights Matrix v1 checks `"is_public_domain" not in record` and
`record.get("is_public_domain") is not True`. SMK's field is `"public_domain"` —
applying either prior matrix to an SMK record would block it under
`missing_rights_field`.

The three boolean-form rights matrices form a constitutional class:
**boolean-form rights determination**. All three implement `field is True` identity
checks with institution-specific field names. They are structurally equivalent but
institutionally distinct. Each requires its own policy ID. No cross-institution
reuse is permitted.

**Ruling:** A new **SMK Rights Matrix v1** (`policy_id: "smk_rights_matrix_v1"`) is
required. It is the third boolean-form rights matrix in the NC pipeline.

### II.2 — SMK Rights Matrix v1 Classification Rules

| Rule ID | Condition | Outcome | rights_basis |
|---|---|---|---|
| SMK-R-1 | `record` is not a dict (None or other) | BLOCKED | `missing_rights_field` |
| SMK-R-2 | `"public_domain"` not in `record` | BLOCKED | `missing_rights_field` |
| SMK-R-3 | `record.get("public_domain") is not True` | BLOCKED | `not_public_domain` |
| SMK-R-4 | No usable image URL (`image_native` absent/empty AND `images` empty/null) | BLOCKED | `no_image_url` |
| SMK-R-5 | All prior rules pass | ALLOWED | `smk_public_domain` |

**ALLOWED outcome:**
- `decision`: ALLOWED
- `rights_statement_uri`: CC0_URI
- `rights_status`: `"pending_verification"` (CI-4 worker ceiling)
- `rights_policy_id`: `"smk_rights_matrix_v1"`

**REVIEW_REQUIRED class:** Not applicable. SMK Rights Matrix v1 has no review path.
Every record is ALLOWED or BLOCKED. This matches Met and AIC matrix structure.

**Secondary rights field:** `image_rights.rights` (string, e.g., `"Public Domain"`).
This field provides a verbatim source rights attestation and must appear in rights
evidence as `smk_image_rights`. It supplements but does not replace the
`public_domain` boolean gate.

### II.3 — Rights Evidence Requirements (CI-8)

Additional fields in `media_rights.rights_evidence` for all SMK records:
- `smk_public_domain` (boolean) — verbatim `record["public_domain"]`
- `smk_image_rights` (string or null) — verbatim
  `record.get("image_rights", {}).get("rights")`
- `smk_object_number` (string) — verbatim `record["object_number"]`
- `smk_manifest_url` (string or null) — constructed IIIF manifest URL

### II.4 — Shared Store Extension (Sprint 3 Prerequisite)

The `build_rights_evidence` remap must extend to
`source_slug in {"met", "aic", "cma", "smk"}`. Injection of `smk_public_domain`,
`smk_image_rights`, `smk_object_number`, and `smk_manifest_url` into evidence must
be added for `source_slug == "smk"`.

**SA-9 is now overdue.** Four institutions require this branch. SA-9 must be
drafted before SMK Sprint 3.

---

## Part III — API Surface Audit

### III.1 — Enumeration Strategy

```
GET https://api.smk.dk/api/v1/art/search?keys=*&public_domain=true&has_image=true&offset=0&rows=100&lang=en&sort=id
```

Response:
```json
{
  "found": 37000,
  "offset": 0,
  "rows": 100,
  "items": [...]
}
```

Termination: `len(items) < rows`. The `found` field is used only for progress
tracking, not for loop control — loop control is by response `items` count, same
as CMA convention.

The `has_image=true` filter restricts to records with available images, eliminating
BLOCKED records before fetch. The `sort=id` (or `sort=object_number`) parameter is
required for replay determinism.

### III.2 — Single-Record Fetch

```
GET https://api.smk.dk/api/v1/art/?object_number={object_number}&lang=en
```

Response wraps the record in an `items` array even for single-record requests:
`{"found": 1, "items": [{...}]}`. The normalizer must unwrap `items[0]`.

### III.3 — IIIF Manifest Fetch

```
GET https://api.smk.dk/api/v1/iiif/manifest/?object_number={object_number}
```

Returns a IIIF Presentation API manifest. The manifest URL must be stored in
`smk_manifest_url` in both rights evidence and technical metadata.

### III.4 — Rate Limiting

No documented rate limit. NC convention: 5 req/s, burst 10. SMK user-agent:
`NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)`.

### III.5 — No Authentication

The SMK API is fully unauthenticated. No credentials, API keys, or Bearer tokens.
This matches Met, AIC, and CMA. SMK config must not contain any credential fields.

---

## Part IV — IIIF Governance

### IV.1 — IIIF Status

| Component | Status | URL Pattern |
|---|---|---|
| IIIF Image API | Confirmed | `https://iip.smk.dk/iiif/jp2/{image_id}.tif/full/!1024,1024/0/default.jpg` |
| IIIF Presentation API | Confirmed | `https://api.smk.dk/api/v1/iiif/manifest/?object_number={id}` |
| Image API version | 2.x | Requires live `info.json` confirmation |
| Presentation version | TBV at Gate 3 | Live manifest inspection required |

IIIF is confirmed, unlike Met (uncertain) and CMA (absent). Unlike Paris Musées
(unknown at audit time), SMK has documented IIIF support in the API specification.

### IV.2 — Image Delivery Strategy

SMK provides two image delivery paths. NC should use:

**Primary:** `image_native` (direct JPEG from IIP server, high resolution) as
`representative_media_url`. This is the simplest path — a complete URL present
directly in the API response, no construction required. Analogous to Met's
`primaryImage`.

**Secondary:** IIIF URL constructed from `images[0].iiif_id` for IIIF-aware
consumers. Not used for `representative_media_url` in Sprint 1 — captured in
technical metadata only.

**Fallback:** `images[0].url` if `image_native` is absent.

**Priority rule in normalize.py:**
1. Use `image_native` if non-null and non-empty
2. Else use `images[0].url` if `images` is non-empty list and `images[0].url`
   is non-null
3. Else `representative_media_url = None` → BLOCKED by SMK-R-4

### IV.3 — IIIF Manifest URL

`smk_manifest_url` =
`f"https://api.smk.dk/api/v1/iiif/manifest/?object_number={object_number}"`.
Must be stored in rights evidence (Article II.3) and technical metadata.

### IV.4 — IIIF Version Gate

IIIF Presentation API version requires live verification at Gate 3. If Presentation
2.1 → SA-3 analogue required. If 3.0 → no bridging. This is the same gate that
appears in DD-AIC-001 Article 4.5. The SMK IIIF Image API uses IIP server
(`iip.smk.dk`) which indicates version 2.x image delivery.

---

## Part V — Commercial Opportunity Assessment

### V.1 — Primary Commercial Tier: Danish Golden Age

SMK is the defining institution for Danish Golden Age painting — Christoffer Wilhelm
Eckersberg (1783–1853), Christen Kobke (1810–1848), and Vilhelm Hammershøi
(1864–1916). These artists are globally recognized, pre-1900, and unrepresented in
any other NC institution. Hammershøi's Copenhagen interiors directly provide
city-level anchor content for Copenhagen place pages. Eckersberg's Italian views
(Rome, Pompeii, the Bay of Naples) provide Mediterranean geographic anchors from a
Nordic perspective. NC has zero Scandinavia coverage in its current pipeline. SMK
uniquely fills this gap.

### V.2 — Secondary Tier: Dutch/Flemish Golden Age

SMK holds a significant collection of 17th-century Dutch and Flemish paintings —
landscapes, portraits, still lifes. These supplement Netherlands coverage already
begun via the Rijksmuseum adapter. Different physical objects; distinct Illustration
Opportunities. No deduplication required at the object level; source priority
convention (Rijksmuseum primary for Dutch works, SMK supplemental) should be
documented.

### V.3 — Geographic Gap Coverage

SMK fills NC's Scandinavia gap — the only critical gap from the Institution Coverage
Audit v1.0 not addressed by any prior institution. Denmark (Copenhagen), Greenland
(SMK holds Greenlandic art), the Nordic region broadly. Secondary: Mediterranean
Europe via Eckersberg's Italian vedute.

### V.4 — Deduplication Assessment

- SMK vs Rijksmuseum: Dutch/Flemish works. Different physical objects. Rijksmuseum
  priority for Dutch masters.
- SMK vs Europeana: SMK contributes to Europeana. Deduplication protocol from
  DD-EUR-001 applies. Direct SMK record takes precedence over aggregator-mediated
  Europeana record.
- SMK vs AIC: Minimal overlap. Both have some French works but different objects.

### V.5 — Volume Estimate

| Classification | Estimated Count |
|---|---|
| public_domain: true, has_image: true | ~35,000–40,000 |
| Danish Golden Age (pre-1900) | ~3,000–5,000 |
| Dutch/Flemish (pre-1700) | ~4,000–6,000 |
| Prints and drawings (pre-1900) | ~8,000–12,000 |
| MASTERWORK tier (major artist, clear provenance) | ~2,000–4,000 |

---

## Decision

### Article 1 — Source Classification

**1.1** SMK is classified as a **Tier 1 Core** content institution for NC's
commercial pipeline.

**1.2** SMK is assigned institution number **#11** (pipeline sequence). User
designation: Candidate #9. Where these differ, pipeline sequence governs for
governance documents.

**1.3** The governing onboarding instrument is the Institution Factory v1 and
Institution Factory Constitution v1.0.

**1.4** SMK's Open programme is a direct CC0 release. SMK is the `dataProvider`
and `provider` in all NC substrate records.

**1.5** The source identifier is `smk`. Permanent once written.

**1.6** Current Institution Factory stage: **Stage 1 (Discovery) complete; Stage 2
(Governance) initiated by this Decision.** No connectivity blockers. Stage 3
(Connectivity) is straightforward — unauthenticated, no private API required.

### Article 2 — SMK Rights Matrix v1

**2.1** A new institution-specific rights matrix is required: **SMK Rights Matrix v1**
(`policy_id: "smk_rights_matrix_v1"`).

**2.2** Neither Met Rights Matrix v1 nor AIC Rights Matrix v1 governs SMK records.
SMK's rights field is `public_domain` (not `isPublicDomain` or `is_public_domain`).
Applying either prior matrix to SMK records produces `missing_rights_field` BLOCKED
for every record.

**2.3** SMK Rights Matrix v1 implements boolean-form determination (identical logic
to Met and AIC) with SMK-specific field bindings. It is the third member of the
boolean-form rights matrix constitutional class.

**2.4** Classification rules: per Part II.2 above (SMK-R-1 through SMK-R-5).

**2.5** `rights_status` in the ALLOWED outcome is `"pending_verification"` (CI-4).

**2.6** No REVIEW_REQUIRED class. Every record is ALLOWED or BLOCKED.

**2.7** Rights evidence additional fields per Part II.3: `smk_public_domain`,
`smk_image_rights`, `smk_object_number`, `smk_manifest_url`.

**2.8** `shared_media_adapter/store.py` must extend the remap to
`source_slug in {"met", "aic", "cma", "smk"}` before Sprint 3. SA-9 should
replace this branching — see Article 10.

### Article 3 — API Governance

**3.1** Authorised API base URL: `https://api.smk.dk/api/v1`. HTTPS only.

**3.2** Primary enumeration:
`GET /api/v1/art/search?keys=*&public_domain=true&has_image=true&sort=id&offset={n}&rows=100&lang=en`.
The `sort=id` parameter is required for replay determinism.

**3.3** Enumeration termination: `len(items) < rows`. Do not use `found` for loop
control.

**3.4** Single-record fetch:
`GET /api/v1/art/?object_number={id}&lang=en`. Response is
`{"found": 1, "items": [{...}]}` — normalizer must unwrap `items[0]`.

**3.5** Rate limit: 5 req/s, burst 10. User-Agent:
`NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)`.

**3.6** No authentication. No credential fields in SMK config.

**3.7** `smk_dry_run = True` is mandatory default. Production activation requires
explicit override and two-human sign-off.

### Article 4 — IIIF Governance

**4.1** IIIF is confirmed for SMK. No IIIF gate is required analogous to DD-MET-001.

**4.2** `representative_media_url` priority rule:
`image_native` → `images[0].url` → `None`. No IIIF URL construction is required
for `representative_media_url` — direct URL is available.

**4.3** `smk_manifest_url` =
`f"https://api.smk.dk/api/v1/iiif/manifest/?object_number={object_number}"` when
`object_number` is non-null. Must be stored in rights evidence and technical metadata.

**4.4** IIIF Image API IIIF IDs are captured from `images[N].iiif_id` into technical
metadata as `smk_iiif_ids`. Not used for `representative_media_url` in Sprint 1 —
captured in technical metadata only.

**4.5** IIIF Presentation manifest version requires live verification at Gate 3.
If 2.1 → SA-3 analogue required. If 3.0 → no bridging.

### Article 5 — Metadata Field Mapping

| SMK API Field | NC Substrate Field | Rule |
|---|---|---|
| `object_number` (str) | `record_id` | Direct string; None if absent |
| `f"…smk.dk/en/artwork/?object_number={id}"` | `source_url` | Constructed from `object_number` |
| `titles[0].title` (str) | `title` | First title; strip; None if empty |
| `artist[0].name` joined | `creator` | Join all `artist[N].name` with ", " |
| `production_date[0].period` (str) | `date` | First production period; strip |
| `production_date[0].start` (int) | `date_start` | Integer; None if absent |
| `production_date[0].end` (int) | `date_end` | Integer; None if absent |
| `content_subject` (list) | `subject_terms` | List of subject strings |
| `image_native` priority | `representative_media_url` | Article 4.2 priority rule |
| `alternative_images` → urls | `additional_images` | List of image URLs |
| `object_names[0].name` (str) | `edm_type` | First object name; strip |
| `collection` (list) | `collection` | List of collection strings |
| `techniques` (list) | `technique` | List |
| `public_domain` (bool) | `smk_public_domain` | Raw boolean |
| `image_rights.rights` (str/null) | `smk_image_rights` | Strip; None if absent |
| `images[N].iiif_id` (str) | `smk_iiif_ids` | List of IIIF IDs |
| Constructed | `smk_manifest_url` | IIIF manifest URL |
| `object_number` | `smk_object_number` | Same as record_id |
| SHA256(canonical JSON) | `raw_payload_hash` | Sort keys, no separators |

**Anchor type derivation:**
1. `media_type_id == "map"` → `"geographic"`
2. Biological keywords in `content_subject` or `object_names` → `"biological"`
3. `artist[0].nationality` non-null → `"geographic"` (artist nationality as
   geographic proxy)
4. Default → `"cultural"`

Note: SMK lacks an explicit `place_of_origin` or `find_spot` field at the top
level. Geographic anchor derivation relies on `content_subject` keywords and artist
nationality. This is less direct than CMA (`culture` field) or AIC
(`place_of_origin`). Wave 2 enrichment may use `content_subject` place-name parsing.

### Article 6 — Pilot Scope

**6.1** The SMK pilot is authorised for **Denmark / Copenhagen** as the target
place context. This is SMK's primary commercial differentiator and fills NC's
Scandinavia coverage gap.

**6.2** Pilot target: **75 assets**, pre-1900, `public_domain: true`,
`has_image: true`. Filter: `responsible_museum` or `collection` indicates SMK
Danish collections, or `artist[0].nationality: "Danish"`.

**6.3** Primary batch (50): Danish Golden Age works — Eckersberg, Kobke, Hammershøi,
or contemporaries. Filter: `public_domain=true`, `artist[0].nationality=Danish` or
equivalent, `production_date[0].end ≤ 1900`.

**6.4** Secondary batch (25): Dutch/Flemish Golden Age (Rembrandt school, Hals,
landscape painters), pre-1700. Supplemental Netherlands coverage.

**6.5** Pilot duration: 90 days. Two-human sign-off required for activation.

### Article 7 — Asset Zero Requirements

**7.1** Asset Zero must satisfy:
- `public_domain: true`
- `image_native` non-null, HTTP 200 confirmed
- Artist: Danish (Eckersberg, Kobke, or Hammershøi preferred)
- `production_date[0].end ≤ 1900`
- MASTERWORK tier (recognised work, major Danish artist)

**7.2** Recommended Asset Zero: A Vilhelm Hammershøi work from SMK's collection —
ideally a Copenhagen interior or Danish landscape scene. Hammershøi is iconic,
globally recognized, and directly anchors Copenhagen place pages. Specific
`object_number` must be selected via live API query at Gate 7.

**7.3** Alternative: Christoffer Wilhelm Eckersberg — if Hammershøi is unavailable
with image. Eckersberg's Italian views (pre-1820) also serve as geographic anchors
for Mediterranean Europe.

**7.4** Asset Zero checklist:
- [ ] `GET /api/v1/art/?object_number={id}` returns HTTP 200 with
      `"public_domain": true`
- [ ] `image_native` non-null and HTTP 200 confirmed
- [ ] IIIF manifest URL confirmed HTTP 200
- [ ] SMK Rights Matrix v1 classifies as ALLOWED
- [ ] `normalize_record()` produces no mandatory field warnings
- [ ] `write_record()` returns `status: "written"`, `writes: 7`
- [ ] `media_rights.rights_status = "pending_verification"` in DB
- [ ] `smk_public_domain: true` in rights evidence
- [ ] `smk_manifest_url` non-null in rights evidence
- [ ] Two-human sign-off

### Article 8 — Success Criteria

**SC-1 (Asset Zero):** Written with `rights_status = "pending_verification"`.
Image resolves HTTP 200. IIIF manifest confirmed. Two-human sign-off.

**SC-2 (IIIF version):** Presentation API version confirmed. SA-3 analogue raised
or waived.

**SC-3 (Pilot volume):** 75 assets written. BLOCKED rate ≤ 5%.

**SC-4 (FM-4):** Zero violations. Non-waivable.

**SC-5 (No terminal attestation):** Zero `"verified_cc0"` in
`worker_classified_status`.

**SC-6 (Anchor type fidelity):** Correct for ≥ 95% of pilot assets. At least one
biological, one geographic, one cultural record.

**SC-7 (SMK evidence completeness):** `smk_public_domain`, `smk_image_rights`,
`smk_object_number`, `smk_manifest_url` present in all ALLOWED records. Zero
exceptions.

**SC-8 (Image resolution):** `representative_media_url` resolves HTTP 200 for ≥ 95%
of written records.

**SC-9 (Human review gate):** Two-human sign-off on pilot completion report before
DD-SMK-002.

### Article 9 — Source Registry Authorization

| Parameter | Value |
|---|---|
| `source_id` | `smk` |
| `source_name` | `Statens Museum for Kunst` |
| `source_type` | `national_gallery_open_access` |
| `institution_number` | `11` |
| `priority` | `12` |
| `auth_type` | `none` |
| `rate_limit_rps` | `5` |
| `burst` | `10` |
| `rights_policy_id` | `smk_rights_matrix_v1` |
| `api_base_url` | `https://api.smk.dk/api/v1` |
| `iiif_manifest_template` | `https://api.smk.dk/api/v1/iiif/manifest/?object_number={id}` |
| `collection_page_template` | `https://www.smk.dk/en/artwork/?object_number={id}` |
| `schema_standard` | `smk_openaccess_v1` |
| `governance_state` | `pending_activation` |
| `onboarding_stage` | `stage_1_discovery` |
| `governing_dd` | `DD-SMK-001` |

### Article 10 — Standards Amendments

**SA-12 (Required):** SMK Open Access Adapter Profile. Defines `smk_openaccess_v1`
schema standard, `smk_rights_matrix_v1` policy ID, `image_native` priority image
selection, IIIF manifest URL template, offset/rows pagination, source registry
parameters, `smk_iiif_ids` technical metadata field. Must be ratified before Sprint
development begins.

**SA-9 (Now overdue — four institutions require it):** The
`build_rights_evidence` source_slug branch now covers `{"met", "aic", "cma"}` and
must extend to `"smk"`. Four institutions requiring this branch is the threshold
past which the branching becomes a maintenance liability. SA-9 (CC0 Adapter Profile
/ `StoreRuntime.cc0_adapter_mode` flag) must be drafted and ratified before SMK
Sprint 3, and ideally before SMK Sprint 1.

**SA-3 analogue (Conditional):** Required if Gate 3 confirms IIIF Presentation 2.1
manifests. Waived if 3.0 confirmed.

### Article 11 — Activation Prerequisites

**Constitutional (CI-class, non-waivable):**
- [ ] SA-12 (SMK Open Access Adapter Profile) ratified
- [ ] SA-9 ratified OR `shared_media_adapter/store.py` extended to
      `{"met", "aic", "cma", "smk"}`
- [ ] `smk_dry_run = True` default in config

**Gate 3 (must resolve before DD-SMK-002):**
- [ ] IIIF Presentation API version confirmed live
- [ ] `image_native` URL confirmed resolving HTTP 200 for sample records
- [ ] Europeana overlap confirmed; deduplication protocol in place
- [ ] Collection page URL `smk.dk/en/artwork/?object_number=` confirmed
- [ ] `sort=id` enumeration parameter supported (fallback: `sort=object_number`)

**Sprint prerequisites:**
- [ ] `workers/smk_adapter/config.py`
- [ ] `workers/smk_adapter/client.py` — offset/rows pagination, single-record fetch,
      manifest fetch
- [ ] `workers/smk_adapter/rights.py` — SMK Rights Matrix v1 (boolean-form)
- [ ] `workers/smk_adapter/normalize.py` — `items[0]` unwrap, `image_native`
      priority, `object_number`-based URLs
- [ ] `workers/smk_adapter/technical.py` — SMK-specific fields including
      `smk_iiif_ids`
- [ ] `workers/smk_adapter/store.py` — `derive_anchor_type` via `content_subject`
      + artist nationality, `StoreRuntime` with `source_slug="smk"`

### Article 12 — Subsequent Decisions

**DD-SMK-002** (SMK Production Activation): Drafted upon Asset Zero completion,
pilot completion, and all SC-1 through SC-9 passing.

---

## Risk Register

| ID | Risk | Probability | Severity | Mitigation |
|---|---|---|---|---|
| R-1 | IIIF Presentation API version is 2.1, requiring SA-3 analogue | Medium | Medium | Gate 3 live check; raise SA immediately if confirmed |
| R-2 | `image_native` absent for a significant fraction of PD records | Low | Medium | `images[0].url` fallback; SMK-R-4 blocks imageless records |
| R-3 | SMK `sort=id` parameter not supported — enumeration non-deterministic | Medium | Medium | Test sort parameter at Gate 3; use `sort=object_number` as fallback |
| R-4 | Europeana duplicate records for Dutch/Flemish works | High | Medium | Apply DD-EUR-001 deduplication; direct SMK record takes precedence |
| R-5 | `artist[0].nationality` absent for anonymous/workshop works | High | Low | Anchor type defaults to `"cultural"` — correct for anonymous works |
| R-6 | SA-9 not ratified before Sprint 3 — fourth source_slug branch required | High | Medium | SA-9 drafting must begin immediately; treat as blocking for SMK Sprint 3 |
| R-7 | SMK API changes to `keys=*` parameter behaviour | Low | Medium | Monitor SMK Open API changelog; test enumeration at Gate 3 |
| R-8 | `image_rights.rights` field structure varies across records | Low | Low | Guarded by `record.get("image_rights", {}).get("rights")` — None if absent |

---

## Ratification

This Decision is in Draft status. Requires Director sign-off (`opengracelabs`) and
second-human approval. Both parties must review Part II (Rights Strategy, including
Met/AIC inheritance ruling) and Article 11 (Activation Prerequisites) before signing.

Upon ratification: source registry entry (Article 9) may be written; SA-12 drafting
may begin; SA-9 drafting must begin immediately.

| Role | Name | Date |
|---|---|---|
| Director | opengracelabs | — |
| Second Human | — | — |
