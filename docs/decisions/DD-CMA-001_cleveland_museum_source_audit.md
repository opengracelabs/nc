# DD-CMA-001 — Cleveland Museum of Art Open Access Source Audit

| Field | Value |
|---|---|
| **Decision ID** | DD-CMA-001 |
| **Type** | Source Audit |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-09 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first Cleveland Museum of Art governance document |
| **Governing Documents** | Institution Coverage Audit v1.0 · Europeana Rights Matrix v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 · Institution Factory v1 |

---

## Background

The Cleveland Museum of Art (CMA) is a major encyclopedic art museum holding
approximately 64,000 objects spanning 6,000 years and all world regions. In 2019,
the CMA released its open access collection — approximately 37,000 works with
images — under Creative Commons Zero (CC0-1.0), with no restriction on commercial
or non-commercial use and no attribution required. All CC0-designated works are
accessible via the CMA's Open Access API at
`https://openaccess-api.clevelandart.org/api/`.

The CMA's collection is commercially significant for NC primarily through its East
Asian holdings — Chinese paintings, bronzes, and ceramics; Japanese paintings and
prints; Korean celadons — which represent one of the strongest North American
museum collections for Asia-Pacific geographic coverage. NC currently has zero
content inventory for China, Korea, or the broader East Asian region. The CMA
pilot directly addresses this critical geographic gap identified in the Institution
Coverage Audit v1.0.

This Decision constitutes the formal Stage 1 Discovery Report and initiates Stage 2
Governance for the CMA as Institution #9.

This Decision presents five governance complexities that are distinct from prior DDs:

1. **String-form rights attestation — cannot inherit Met/AIC boolean architecture.**
   The CMA uses `share_license_status: "CC0"` (a string enum) rather than a boolean
   flag (`isPublicDomain: true` / `is_public_domain: true`). This is a fundamentally
   different rights field type. The Met Rights Matrix v1 and AIC Rights Matrix v1
   both govern boolean-identity checks (`field is True`); a CMA Rights Matrix v1
   must govern string-equality checks (`field == "CC0"`). The shared write path
   inherits correctly, but the institution-specific rights classifier is a new
   architectural form. This is the definitive answer to the question posed at audit
   initiation: **CMA cannot inherit Met or AIC rights architecture.**

2. **No IIIF — absent from the API contract.** Neither IIIF Image API nor IIIF
   Presentation API manifests are documented or available through the CMA Open
   Access API. Image delivery is via a direct CDN (`openaccess-cdn.clevelandart.org`)
   with three resolution tiers: `web` (900 px JPG), `print` (3400 px JPG), and
   `full` (TIFF archival). This is the first NC institution with no IIIF at any tier.
   No IIIF manifest URL appears in evidence or technical metadata for CMA records.

3. **Nested image object — multi-tier URL selection required.** The CMA API returns
   an `images` object containing `web`, `print`, and `full` sub-objects, each with
   a `url` field. Unlike Met's flat `primaryImage` string or AIC's UUID-based
   `image_id` construction, the CMA normalizer must traverse a nested structure and
   apply a priority tier selection rule. The `print` tier (3400 px) is the
   authorised representative media URL for NC commerce purposes; `web` is the
   fallback. The `full` TIFF tier is excluded from `representative_media_url` (not
   a web-deliverable format) but must be captured in technical metadata.

4. **Offset pagination — no cursor support.** The CMA API uses `skip`/`limit`
   offset pagination with no `next_url` cursor. This differs from both Met
   (all-IDs-at-once) and AIC (cursor-based `pagination.next_url`). The CMA client
   must compute the next `skip` value from the current `skip` + `limit`, terminating
   when `len(data) < limit` or `skip >= info.total`. Enumeration is deterministic
   by `?orderby=id` combined with `skip`.

5. **SA-9 urgency escalated.** The shared `store.py` boolean PD remap currently
   covers `source_slug in {"met", "aic"}`. CMA uses a string-form rights field but
   still routes through the CC0_URI path, causing the shared `classify_rights(CC0_URI)`
   to return `rights_status: "verified_cc0"`. The remap must extend to
   `source_slug in {"met", "aic", "cma"}`. Three institutions now require this
   extension. SA-9 (CC0 Adapter Profile generalising the remap via a `StoreRuntime`
   flag) is no longer merely recommended — it should be drafted before Institution #10
   is onboarded.

---

## Part I — Source Classification Audit

**Institution name:** Cleveland Museum of Art (CMA)

**Institution type:** Museum, nonprofit institution, independent

**Collection type:** Encyclopedic art museum — paintings, sculpture, prints and
drawings, decorative arts, arms and armor, textiles, Asian art (Chinese, Japanese,
Korean, Indian, Southeast Asian), African art, Islamic art, Medieval/Byzantine art,
pre-Columbian art, photography

**Open access programme:** CMA Open Access Initiative (2019). CC0-1.0 for all
designated works. No authentication required. Official contact: openaccess@clevelandart.org.

**API type:** Custom REST JSON API
**API base URL:** `https://openaccess-api.clevelandart.org/api`
**API version:** No path versioning; single current API
**Pagination:** Offset-based `skip`/`limit` (default `limit=1000` for artworks)
**Authentication:** None required (open, unauthenticated access)
**Rate limiting:** Not documented; 5 req/s is NC convention for unauthenticated APIs

**Key endpoints:**
- `GET /api/artworks` — paginated artwork list with filter parameters
- `GET /api/artworks/{id}` — single artwork by integer ID
- `GET /api/artworks/{accession_number}` — single artwork by accession number
- `GET /api/creators/{creator_id}` — creator details

**CC0 collection size:** ≈ 37,000 artworks with images (all CC0 by API contract)

**Total API-accessible artworks:** ≈ 64,000 records

**Rights field:** `share_license_status` (string enum) — value `"CC0"` is the sole
ALLOWED designation

**Image delivery:** Direct CDN URLs, three resolution tiers, no IIIF

**IIIF:** None — absent from API contract

**NC institution tier:** Tier 1 Core — CC0, direct, no aggregator intermediary

**Institution onboarding wave:** Wave 4

**Proposed institution number:** #9

**Proposed source ID:** `cma`

**Proposed source priority:** 10

**Differentiating commercial strengths:**
- Chinese art (paintings, bronzes, ceramics) — NC's primary Asia-Pacific gap
- Japanese paintings (Kanō school, Rinpa) — supplemental and complementary to Met prints
- Korean art (celadons, paintings) — virtually unrepresented in NC pipeline
- Islamic art (carpets, metalwork, ceramics) — Middle East coverage gap
- Medieval and Byzantine art (European pre-Renaissance)
- Arms and armor (global coverage, commercial niche)
- Pre-Columbian art (Latin America supplemental to AIC holdings)

**Geographic coverage added:** China (critical — zero current coverage); Korea (new);
Islamic world/Middle East; Byzantium/Medieval Europe; supplemental Japan and Latin America

---

## Part II — Rights Strategy Audit

### II.1 — Can CMA Inherit Met/AIC Rights Architecture?

**Governing question:** Can the CMA adapter reuse Met Rights Matrix v1
(`met_rights_matrix_v1`) or AIC Rights Matrix v1 (`aic_rights_matrix_v1`)?

**Answer: No — for architectural reasons, not merely naming reasons.**

The Met Rights Matrix v1 and AIC Rights Matrix v1 both implement **boolean-form
rights determination**: the classifier checks whether a boolean field is strictly
`True` (`is True` in Python). The check is:

- Met: `record.get("isPublicDomain") is not True` → BLOCKED
- AIC: `record.get("is_public_domain") is not True` → BLOCKED

The CMA has no boolean public domain field. The rights attestation is:

- CMA: `record.get("share_license_status") != "CC0"` → BLOCKED

This is **string-equality-form rights determination** — a structurally different
classifier type. The boolean identity check (`is True`) does not apply because:
1. `"CC0" is True` evaluates to `False` in Python (a non-empty string is truthy but
   not `True`).
2. `"CC0" is not True` → BLOCKED — the Met/AIC gate would block every CMA record.

A new **CMA Rights Matrix v1** (`policy_id: "cma_rights_matrix_v1"`) is required.
It implements string-equality-form determination — a new constitutional rights class
for NC alongside boolean-form (Met/AIC) and URI-form (Europeana/Rijksmuseum/Gallica).

### II.2 — Can CMA Inherit Met/AIC at the Shared Write Path Level?

**Answer: Yes — with one required extension.**

The shared `write_normalized_record` function, the six M36 tables, the evidence
structure, and the `StoreRuntime` pattern all apply unchanged. The CMA adapter will
use `write_normalized_record` exactly as Met and AIC do.

The required extension: the `build_rights_evidence` terminal-value remap in
`shared_media_adapter/store.py` must cover `"cma"`:

```python
if runtime.source_slug in {"met", "aic", "cma"}:
    worker_classified_status = {
        "verified_cc0": "classified_cc0",
        "verified_pd": "classified_pd",
    }.get(str(worker_classified_status), worker_classified_status)
```

Because CMA records normalise to `rights_uri = CC0_URI`, the shared
`classify_rights(CC0_URI)` returns `rights_status: "verified_cc0"`. Without the
remap, this terminal value would propagate into `worker_classified_status` in rights
evidence — a CI-4 violation identical to Met V4 and the AIC Article 2.7 prerequisite.

### II.3 — CMA Rights Matrix v1 Classification Rules

| Rule ID | Condition | Outcome | rights_basis |
|---|---|---|---|
| CMA-R-1 | `record` is not a dict (None or other) | BLOCKED | `missing_rights_field` |
| CMA-R-2 | `"share_license_status"` not in `record` | BLOCKED | `missing_rights_field` |
| CMA-R-3 | `record["share_license_status"] != "CC0"` | BLOCKED | `not_cc0` |
| CMA-R-4 | No usable image URL in `images.web.url` or `images.print.url` | BLOCKED | `no_image_url` |
| CMA-R-5 | All prior rules pass | ALLOWED | `cma_share_license_status_cc0` |

**ALLOWED outcome:**
- `decision`: ALLOWED
- `rights_statement_uri`: CC0_URI
- `rights_status`: `"pending_verification"` (CI-4 worker ceiling)
- `rights_policy_id`: `"cma_rights_matrix_v1"`

**REVIEW_REQUIRED class:** Not applicable. CMA Rights Matrix v1 has no review path.
Every record is either ALLOWED or BLOCKED. This matches the Met and AIC matrices
in outcome structure, despite the different input form.

**CMA-R-4 image check:** The check must traverse the nested `images` object. A
record is image-present if `images` is a non-empty dict AND at least one of
`images.web.url` or `images.print.url` is a non-empty string. The `full` TIFF URL
is not sufficient alone (not web-deliverable). The `images` object can be null or
absent for some records — this must be guarded.

### II.4 — Rights Evidence Requirements (CI-8)

Constitutional Invariant CI-8 requires nine fields in `media_rights.rights_evidence`.
For CMA records, the following additional fields must also appear:

- `cma_share_license_status` (string) — verbatim value of `record["share_license_status"]`
- `cma_copyright` (string or null) — verbatim value of `record.get("copyright")`
- `cma_accession_number` (string) — the CMA accession number (provenance anchor)

No IIIF manifest URL appears in CMA evidence (no IIIF available). This distinguishes
CMA's evidence schema from AIC's (which has `aic_manifest_url`).

### II.5 — Shared Store Extension (Sprint 3 Prerequisite)

Before any CMA record is written to the M36 substrate:

1. `build_rights_evidence` remap extended to `source_slug in {"met", "aic", "cma"}`
2. CMA evidence fields injected:
   ```python
   if runtime.source_slug == "cma":
       evidence["cma_share_license_status"] = normalized.get("cma_share_license_status")
       evidence["cma_copyright"] = normalized.get("cma_copyright")
       evidence["cma_accession_number"] = normalized.get("accession_number")
   ```
3. SA-9 (CC0 Adapter Profile) should be drafted before Institution #10 to replace
   accumulating `source_slug` branches with a `StoreRuntime` flag mechanism.

---

## Part III — API Surface Audit

### III.1 — Enumeration Strategy

**Primary path:** CC0 + has_image filtered scan

```
GET /api/artworks?cc0=1&has_image=1&skip=0&limit=100&orderby=id
```

Response structure:
```json
{
    "info": {
        "total": 37000,
        "parameters": {"skip": 0, "limit": 100}
    },
    "data": [...]
}
```

Termination condition: `len(response["data"]) < limit` OR `skip + limit >= info.total`.

The `orderby=id` parameter ensures deterministic enumeration order for replay.
Without it, order is undefined and replay hashes may differ across runs.

**Comparison to prior institutions:**
- Met: single all-IDs response → iterate per record
- AIC: cursor via `pagination.next_url`
- CMA: manual offset (`skip += limit`) — new pattern, no cursor field to follow

### III.2 — Single-Record Fetch

```
GET /api/artworks/{id}
```
or
```
GET /api/artworks/{accession_number}
```

The integer `id` is the preferred primary key for single-record fetch (stable,
unambiguous). The `accession_number` form is useful for human-initiated lookups.

### III.3 — Field Selection

The CMA API supports a `select` parameter to restrict response fields. For production
ingestion, the authorised field set includes:

Required for rights classification:
- `share_license_status`, `images`, `copyright`

Required for normalization:
- `id`, `accession_number`, `title`, `creation_date`, `creation_date_earliest`,
  `creation_date_latest`, `creators`, `culture`, `type`, `department`, `collection`,
  `technique`, `find_spot`, `description`, `creditline`

Additional for technical metadata:
- `date_added_to_oa`, `is_highlight`, `citations`, `exhibitions`, `related_works`,
  `external_resources`

### III.4 — Rate Limiting

No published rate limit. NC applies 5 req/s with burst 10 (standard convention for
unauthenticated public APIs). The CMA API default `limit` for artworks is 1,000 —
production ingestion should use `limit=100` to reduce per-request payload size and
improve retry granularity.

---

## Part IV — Image Delivery Governance

### IV.1 — Image Tier Architecture

The CMA provides three image tiers per artwork record. All are direct CDN URLs —
no IIIF construction required.

| Tier | Key path | Resolution | Format | NC use |
|---|---|---|---|---|
| `web` | `images.web.url` | 900 px | JPG | Fallback representative media |
| `print` | `images.print.url` | 3,400 px | JPG | **Primary representative media** |
| `full` | `images.full.url` | Archival | TIFF | Technical metadata only — not web-deliverable |

**URL pattern:** `https://openaccess-cdn.clevelandart.org/{accession}/{accession}_print.jpg`

### IV.2 — Representative Media URL Selection

`representative_media_url` must be selected by the following priority rule:

1. Use `images["print"]["url"]` if present and non-empty string
2. Else use `images["web"]["url"]` if present and non-empty string
3. Else: `representative_media_url = None` (record will be BLOCKED by CMA-R-4 in rights.py)

This selection must happen in `normalize.py`, not in `rights.py`. The rights
classifier checks only for URL presence; the normalizer selects the tier.

### IV.3 — Alternate Images

The `alternate_images` field (array) contains additional views of the same work.
Each entry follows the same three-tier structure as `images`. All non-empty
`print.url` values from `alternate_images` must be collected into `additional_images`
in the normalized record, following the Met/AIC `additional_images` convention.

### IV.4 — No IIIF

The CMA Open Access API provides no IIIF Image API endpoint and no IIIF Presentation
API manifests. The following fields that appear in Met/AIC records do not exist for
CMA and must not be populated:

- `aic_manifest_url` — does not exist for CMA
- Any IIIF Image API URL construction — not applicable

The absence of IIIF is not a constitutional defect. NC's image delivery contract
requires a `representative_media_url` that resolves to an image. The CMA CDN URL
satisfies this contract. No SA is required for absent IIIF.

### IV.5 — Collection Page URL

CMA collection page URLs follow the pattern:

```
https://clevelandart.org/art/{accession_number}
```

This is the `source_url` / `source_item.canonical_source_url` value. It must be
constructed from the `accession_number` field, not the `id` integer. Live
verification of this URL pattern is required at Gate 3. If the pattern uses `id`
rather than `accession_number`, this Article must be amended before Sprint 2.

---

## Part V — Commercial Opportunity Assessment

### V.1 — Primary Commercial Tier: East Asian Art

The CMA holds one of the finest East Asian art collections in North America, with
particular depth in:
- Chinese paintings (Song, Yuan, Ming, Qing dynasties) — landscape, bird-and-flower,
  figure subjects — all `anchor_type: geographic` (China place pages)
- Chinese bronzes, ceramics, jades — cultural/geographic
- Japanese paintings (Kanō, Rinpa, Maruyama-Shijō schools) — supplemental to
  Met ukiyo-e pilot; different art forms, distinct Illustration Opportunities
- Korean celadons and paintings — NC has zero current Korea coverage

This tier is CMA's primary commercial differentiator. No other NC institution
currently in pipeline provides significant Chinese painting inventory.

### V.2 — Secondary Tier: Islamic and Medieval Art

CMA holds significant Islamic metalwork, carpets, and ceramics (Ottoman, Persian,
Mughal) and Medieval/Byzantine art (icons, ivories, enamels). These provide content
for Middle Eastern and European medieval place pages — geographic areas with no
current NC inventory.

### V.3 — Geographic Gap Coverage

CMA directly addresses three of four critical geographic gaps from the Institution
Coverage Audit v1.0:
- **China** (primary): not covered by any existing or in-pipeline NC institution
- **Korea**: not covered anywhere in pipeline
- **Islamic world/Middle East**: not covered anywhere in pipeline

### V.4 — Deduplication Assessment

**CMA vs Met:** Met pilot covers Japanese prints (Hiroshige, Hokusai). CMA's Japanese
holdings are primarily paintings (Kanō school) — different art form, distinct objects.
Minimal deduplication risk.

**CMA vs AIC:** AIC has some East Asian works; CMA's Chinese collection is stronger.
Different physical objects throughout.

**CMA vs Europeana/DPLA:** CMA is not known to contribute to either aggregator.
Verify at Gate 2.

### V.5 — Volume Estimate

| Classification | Estimated Count |
|---|---|
| Total CC0 works with images | ≈37,000 |
| Chinese art, CC0, has_image | ≈3,000–5,000 |
| Japanese art, CC0, has_image | ≈2,000–3,000 |
| Korean art, CC0, has_image | ≈500–1,000 |
| Islamic art, CC0, has_image | ≈1,000–2,000 |
| MASTERWORK tier (major work, clear attribution, pre-1900) | ≈3,000–5,000 |

---

## Decision

### Article 1 — Source Classification

**1.1** The Cleveland Museum of Art is classified as a **Tier 1 Core** content
institution for NC's commercial pipeline.

**1.2** The CMA is assigned institution number **#9**, following the Art Institute
of Chicago (#8, DD-AIC-001).

**1.3** The governing onboarding instrument is the Institution Factory v1 and
Institution Factory Constitution v1.0. The CMA must complete all nine stages and
pass all mandatory exit gates before operational status is granted.

**1.4** The CMA's Open Access Initiative is a direct CC0 release. The CMA is the
`dataProvider` and `provider` in all NC substrate records.

**1.5** The source identifier is `cma`. Permanent once written.

### Article 2 — CMA Rights Matrix v1

**2.1** The Cleveland Museum of Art requires a new institution-specific rights
matrix: **CMA Rights Matrix v1** (`policy_id: "cma_rights_matrix_v1"`).

**2.2** Neither Met Rights Matrix v1 nor AIC Rights Matrix v1 governs CMA records.
Both implement boolean-form PD detection (`field is True`). The CMA uses
`share_license_status: "CC0"` (string-equality form). Applying a boolean-form
matrix to CMA records would classify every CMA record as BLOCKED under the
`missing_rights_field` or `not_public_domain` rule.

**2.3** CMA Rights Matrix v1 implements string-equality-form determination. The
sole ALLOWED condition is `share_license_status == "CC0"` (exact string equality,
case-sensitive) combined with at least one usable image URL.

**2.4** CMA Rights Matrix v1 has **no REVIEW_REQUIRED class**. Every record is
ALLOWED or BLOCKED. This outcome structure matches Met and AIC matrices despite the
different input form.

**2.5** `rights_status` in the ALLOWED outcome is `"pending_verification"` (CI-4).

**2.6** The following fields must appear in `media_rights.rights_evidence` for all
CMA records, in addition to the nine CI-8 required fields:

- `cma_share_license_status` (string) — verbatim `record["share_license_status"]`
- `cma_copyright` (string or null) — verbatim `record.get("copyright")`
- `cma_accession_number` (string) — verbatim `record["accession_number"]`

No IIIF manifest URL is required (no IIIF available). This is a deliberate absence,
not an omission.

**2.7** The shared `media_adapter/store.py` `build_rights_evidence` function must be
extended to `source_slug in {"met", "aic", "cma"}` before any CMA record is written.
The three Article 2.6 evidence fields must be injected when `source_slug == "cma"`.
This is a Sprint 3 prerequisite and constitutes a constitutional activation gate (CI-4).

**2.8** SA-9 (CC0 Adapter Profile) must be drafted before Institution #10 is
onboarded. Three institutions now require `source_slug` branching in
`build_rights_evidence`. SA-9 will replace branching with a `StoreRuntime` flag.

### Article 3 — API Governance

**3.1** The authorised CMA API base URL is `https://openaccess-api.clevelandart.org/api`.
All requests must use HTTPS.

**3.2** The primary enumeration path is:
`GET /api/artworks?cc0=1&has_image=1&orderby=id&skip={n}&limit=100`

The `orderby=id` parameter is **required** for replay determinism. Enumeration
without a stable sort order is a CI-8 violation (evidence completeness cannot be
guaranteed across re-runs).

**3.3** Enumeration terminates when `len(response["data"]) < limit` or when
`info.parameters.skip + limit >= info.total`. Both conditions must be checked.
The client must not rely on either condition alone.

**3.4** Rate limit: 5 req/s, burst 10. CMA user-agent:
`NC-OpenGrace-Pipeline/1.0 (+https://opengrace.com)`.

**3.5** `limit=100` is the authorised page size for production ingestion. The API
default of `limit=1000` is not used in production — it increases per-request payload
and retry blast radius.

**3.6** No authentication credentials are stored for CMA. If the CMA API introduces
authentication in a future version, this Decision must be amended.

**3.7** `cma_dry_run = True` is the mandatory default configuration. Production
activation requires explicit override and two-human sign-off (CI-2, IFC-9).

### Article 4 — Image Delivery Governance

**4.1** Image delivery is via the CMA CDN (`openaccess-cdn.clevelandart.org`).
No IIIF construction is required or supported. No IIIF manifest URL exists.

**4.2** `representative_media_url` must be selected by tier priority:
1. `images["print"]["url"]` if non-null and non-empty string
2. Else `images["web"]["url"]` if non-null and non-empty string
3. Else `None`

**4.3** This selection must occur in `normalize.py`. The rights classifier
(`rights.py`) checks only for URL presence (CMA-R-4) — it does not select a tier.

**4.4** The `full` TIFF URL must be captured in `media_technical_metadata.content`
as `cma_image_full_url`. It must not be used as `representative_media_url`.

**4.5** `additional_images` must be constructed from `alternate_images[N].print.url`
values (fallback to `web.url`), following the same priority rule as Article 4.2.

**4.6** The collection page URL (`source_url`) must be constructed as:
`https://clevelandart.org/art/{accession_number}`
Live verification of this URL pattern is required at Gate 3. If the pattern differs,
this Article must be amended before Sprint 2 begins.

### Article 5 — Metadata Field Mapping

| CMA API Field | NC Substrate Field | Rule |
|---|---|---|
| `id` (int) | `record_id` | `str(raw["id"])` — stringify; None if absent |
| `f"…/art/{accession_number}"` | `source_url` | Constructed from `accession_number` (verify pattern at Gate 3) |
| `title` (str) | `title` | Strip; None if empty |
| `creation_date` (str) | `date` | Strip; None if empty |
| `creation_date_earliest` (int) | `date_start` | Integer; None if absent |
| `creation_date_latest` (int) | `date_end` | Integer; None if absent |
| `creators[N].name` joined | `creator` | Join with ", " for primary attribution |
| `creators` (array) | `creators_detail` | Full array for provenance |
| `type` (str) | `edm_type` | Strip; None if empty |
| `culture` (array) | `culture` | List of strings; primary culture as `culture_primary` |
| `department` (str) | `department` | Strip; None if empty |
| `collection` (str) | `collection` | Strip; None if empty |
| `technique` (array) | `technique` | List of strings |
| `find_spot` (str) | `find_spot` | Strip; None if empty |
| `description` (str) | `description` | Strip; None if empty; fallback `type` |
| `accession_number` (str) | `accession_number` | Strip; None if empty |
| `share_license_status` (str) | `cma_share_license_status` | Raw value |
| `copyright` (str/null) | `cma_copyright` | Strip; None if null/empty |
| Tier-selected | `representative_media_url` | Article 4.2 priority rule |
| `images["web"]["url"]` | `cma_image_web_url` | Pass through; None if absent |
| `images["print"]["url"]` | `cma_image_print_url` | Pass through; None if absent |
| `images["full"]["url"]` | `cma_image_full_url` | Pass through; None if absent |
| `alternate_images` → urls | `additional_images` | Constructed per Article 4.5 |
| `creditline` (str) | `credit_line` | Strip; None if empty |
| `is_highlight` (bool) | `is_highlight` | Boolean; None if absent |
| SHA256(canonical JSON) | `raw_payload_hash` | Sort keys, no separators |
| Classified | `rights_uri` | CC0_URI if ALLOWED; None if BLOCKED |
| Classified | `rights_decision` | CMA Rights Matrix v1 outcome string |

**Anchor type derivation (Article 5.2):**
Precedence order in `derive_anchor_type`:
1. `media_type_id == "map"` → `"geographic"`
2. Biological keyword in `type` field or flattened subject terms → `"biological"`
   (keyword set: "bird", "fish", "flower", "botanical", "plant", "animal",
   "insect", "mammal", "reptile", "amphibian")
3. `find_spot` non-null → `"geographic"` (archaeological provenance)
4. `culture` list non-empty → `"geographic"` (cultural origin = place association)
5. Default → `"cultural"`

**`creator` derivation:** `creators` is an array of objects with `name` and `role`
fields. The primary `creator` string must be constructed by joining `c["name"]` for
each creator where `c.get("name")` is non-empty. Role is not appended to the primary
`creator` string but is preserved in `creators_detail`.

### Article 6 — Pilot Scope

**6.1** The CMA pilot is authorised for **China** as the target place context.
This differentiates the CMA pilot from the Met pilot (Japan), the AIC pilot (France),
and directly addresses NC's most critical geographic gap (zero China coverage).

**6.2** The pilot target is **75 assets** with a secondary sub-cap of 25 from outside
the Chinese art tier (Islamic or Korean art) to verify anchor_type derivation and
department diversity.

**6.3** Pilot filter criteria:
- Primary batch (50 assets): `cc0=1`, `has_image=1`, `department` contains
  "Chinese" OR `culture` contains "Chinese", `creation_date_latest ≤ 1900`
- Secondary batch (25 assets): `cc0=1`, `has_image=1`, `department` contains
  "Islamic" OR `department` contains "Korean", `creation_date_latest ≤ 1900`

**6.4** Pilot duration: 90 days from Asset Zero write date.

**6.5** Pilot activation requires two-human sign-off (CI-2).

**6.6** No production traffic for CMA assets until DD-CMA-002 is ratified.

### Article 7 — Asset Zero Requirements

**7.1** Asset Zero must satisfy:
- `share_license_status: "CC0"`
- `images.print.url` non-null and resolves HTTP 200
- `culture` contains `"Chinese"` OR `department` contains "Chinese Art" (China pilot)
- `creation_date_latest ≤ 1900`
- Clear creator attribution (known artist or workshop/dynasty attribution)
- MASTERWORK tier (significant work, major holding)

**7.2** Recommended Asset Zero category: A Chinese landscape painting or bird-and-flower
painting (pre-1900, Qing or Ming dynasty preferred) from CMA's East Asian collection.
For highest commercial value: a Song or Yuan dynasty landscape scroll with confirmed
`images.print.url` and identifiable provenance. The specific accession number must be
selected and verified live at Gate 7 via API fetch.

**7.3** Alternative Asset Zero: A Chinese bronze vessel (Zhou or Han dynasty) or
Korean celadon (Goryeo dynasty) — if Chinese painting selection fails image resolution.

**7.4** Asset Zero checklist:
- [ ] Live API fetch: `GET /api/artworks/{id}` returns HTTP 200
- [ ] `share_license_status: "CC0"` confirmed in response
- [ ] `images.print.url` non-null and non-empty in response
- [ ] `images.print.url` resolves to HTTP 200 (CDN live check)
- [ ] CMA Rights Matrix v1 classifies as ALLOWED
- [ ] `normalize_record()` produces no mandatory field warnings
- [ ] Collection page URL (`clevelandart.org/art/{accession_number}`) resolves HTTP 200
- [ ] `write_record()` returns `status: "written"`, `writes: 7`
- [ ] `media_rights.rights_status = "pending_verification"` in DB
- [ ] `media_rights.rights_evidence.cma_share_license_status = "CC0"` in DB
- [ ] `media_rights.rights_evidence.cma_accession_number` non-null in DB
- [ ] Two-human sign-off on Asset Zero record

### Article 8 — Success Criteria

**SC-1 (Asset Zero):** Asset Zero written with `rights_status = "pending_verification"`.
CDN image URL resolves HTTP 200. Two-human sign-off complete.

**SC-2 (Collection page URL):** Gate 3 verification confirms `clevelandart.org/art/{accession_number}`
URL pattern is correct. If incorrect, amended URL pattern is documented before
Sprint 2 begins.

**SC-3 (Pilot volume):** 75 pilot assets written. BLOCKED rate ≤ 5%. Of BLOCKED
records, ≥ 90% have `rights_basis: "not_cc0"` or `"no_image_url"` (expected).

**SC-4 (FM-4 — permanent):** Zero FM-4 violations. Non-waivable.

**SC-5 (No terminal attestation):** Zero records with `worker_classified_status`
set to `"verified_cc0"` in `media_rights.rights_evidence`. Must show
`"classified_cc0"` for all ALLOWED records.

**SC-6 (Anchor type fidelity):** Anchor type correct for ≥ 95% of pilot assets.
At least one biological (type contains animal/bird/botanical keyword), one geographic
(culture non-empty), and one cultural (no culture, no find_spot) record present.

**SC-7 (CMA evidence completeness):** `cma_share_license_status`, `cma_copyright`,
and `cma_accession_number` present in `media_rights.rights_evidence` for all ALLOWED
records. SC-7 admits zero exceptions.

**SC-8 (CDN URL resolution):** `representative_media_url` resolves HTTP 200 for
≥ 95% of written records.

**SC-9 (Human review gate):** Two-human sign-off on pilot completion report before
DD-CMA-002 is initiated.

### Article 9 — Source Registry Authorization

| Parameter | Value |
|---|---|
| `source_id` | `cma` |
| `source_name` | `Cleveland Museum of Art` |
| `source_type` | `museum_open_access` |
| `institution_number` | `9` |
| `priority` | `10` |
| `auth_type` | `none` |
| `rate_limit_rps` | `5` |
| `burst` | `10` |
| `rights_policy_id` | `cma_rights_matrix_v1` |
| `api_base_url` | `https://openaccess-api.clevelandart.org/api` |
| `cdn_base_url` | `https://openaccess-cdn.clevelandart.org` |
| `collection_page_template` | `https://clevelandart.org/art/{accession_number}` |
| `schema_standard` | `cma_openaccess_v1` |
| `governance_state` | `pending_activation` |
| `onboarding_stage` | `stage_1_discovery` |
| `governing_dd` | `DD-CMA-001` |

### Article 10 — Standards Amendments

**SA-10 (Required):** CMA Open Access Adapter Profile. Defines the CMA-specific
adapter contract: `cma_openaccess_v1` schema standard, `cma_rights_matrix_v1`
policy ID, CDN image tier selection rule, offset pagination pattern, source registry
parameters, and the `select` parameter field set. Analogous to SA-7 (Met) and SA-8
(AIC). Must be ratified before CMA adapter sprint development begins.

**SA-9 (Now required, not merely recommended):** CC0 Adapter Profile. Replaces
accumulating `source_slug in {"met", "aic", "cma"}` branching in
`build_rights_evidence` with a `StoreRuntime.cc0_adapter_mode` flag. Three
institutions now require the branch. SA-9 must be drafted and ratified before
Institution #10 onboarding begins. Any further delay makes the shared store a
maintenance liability.

### Article 11 — Activation Prerequisites

**Constitutional prerequisites (CI-class, non-waivable):**
- [ ] SA-10 (CMA Open Access Adapter Profile) ratified
- [ ] `shared_media_adapter/store.py` remap extended to `{"met", "aic", "cma"}`
- [ ] CMA evidence fields (`cma_share_license_status`, `cma_copyright`, `cma_accession_number`) injected
- [ ] `cma_dry_run = True` is default; explicit override required for production

**Gate 3 prerequisites (exit gate — must resolve before DD-CMA-002):**
- [ ] Collection page URL pattern verified live (`clevelandart.org/art/{accession_number}`)
- [ ] CDN URL availability confirmed (HTTP 200 for `images.print.url` sample)
- [ ] Confirmed absence of IIIF (no remediation required; documented as deliberate)

**Sprint prerequisites (adapter code):**
- [ ] `workers/cma_adapter/config.py` — configuration with dry-run default
- [ ] `workers/cma_adapter/client.py` — offset pagination client with `cc0=1&has_image=1&orderby=id`
- [ ] `workers/cma_adapter/rights.py` — CMA Rights Matrix v1 (string-equality form)
- [ ] `workers/cma_adapter/normalize.py` — tier selection, `creators` array flattening, `source_url` construction
- [ ] `workers/cma_adapter/technical.py` — CMA-specific technical metadata schema
- [ ] `workers/cma_adapter/store.py` — `derive_anchor_type` using `culture` + `find_spot`, `StoreRuntime` with `source_slug="cma"`

### Article 12 — Subsequent Decisions

**DD-CMA-002** (CMA Production Activation) shall be drafted upon:
1. All Article 11 prerequisites satisfied
2. Asset Zero checklist complete with two-human sign-off
3. Pilot completion report approved with two-human sign-off (SC-9)
4. SC-1 through SC-9 all passing

**SA-9** should be drafted concurrently with CMA Sprint 1 — not after Sprint 3.
Delaying SA-9 means a fourth institution's Sprint 3 will require yet another
`source_slug` branch.

---

## Risk Register

| ID | Risk | Probability | Severity | Mitigation |
|---|---|---|---|---|
| R-1 | Collection page URL pattern is not `clevelandart.org/art/{accession_number}` | Medium | Medium | Gate 3 live verification required; Article 4.6 must be amended if pattern differs |
| R-2 | `images.print.url` absent for a significant fraction of CC0 records | Medium | Medium | `web.url` fallback covers most cases; CMA-R-4 blocks records with no usable URL |
| R-3 | CMA CDN availability degrades for archival records | Low | Medium | CDN URL resolution checked at Asset Zero and sampled in pilot |
| R-4 | `share_license_status` takes values other than "CC0" or null in practice | Low | Low | CMA-R-3 blocks any non-"CC0" value; filter `cc0=1` pre-filters these |
| R-5 | `creators` array is empty or anonymous for a significant fraction of China works | High | Low | Normaliser handles empty array; `creator: null` is acceptable for ancient works |
| R-6 | `culture` field granularity insufficient for sub-country place hierarchy | Medium | Medium | `culture: ["Chinese"]` maps to country-level; sub-region enrichment deferred to Wave 2 |
| R-7 | Offset pagination becomes inconsistent if new records are added during enumeration | Low | Low | `orderby=id` with stable integer IDs minimises this; replay uses raw payload hash for deduplication |
| R-8 | CMA API versioning — no path versioning means breaking changes are undiscovered | Medium | High | Monitor `openaccess@clevelandart.org` announcements; pin to live API with hash-based change detection |
| R-9 | SA-9 delay causes Institution #10 to add a fourth `source_slug` branch | High (if not drafted) | Medium | SA-9 drafting should begin before CMA Sprint 1 completes |
| R-10 | CMA vs DPLA/Europeana duplication (unknown status) | Unknown | Medium | Verify at Gate 2; apply existing deduplication protocols if found |

---

## Ratification

This Decision is in Draft status. It requires:

1. Director sign-off (`opengracelabs`)
2. Second-human approval (any authorised reviewer)
3. Both parties must review Part II (Rights Strategy Audit, including the
   Met/AIC inheritance ruling), Article 2 (CMA Rights Matrix v1), and
   Article 11 (Activation Prerequisites) before signing.

Upon ratification:
- CMA source registry entry (Article 9) may be written
- SA-10 drafting may begin
- SA-9 drafting should begin concurrently
- Sprint development may begin (blocked only by SA-10 ratification and
  Article 11 prerequisites)

| Role | Name | Date |
|---|---|---|
| Director | opengracelabs | — |
| Second Human | — | — |
