# DD-RIJKSMUSEUM-001 — Rijksmuseum Production Activation

| Field | Value |
|---|---|
| **Decision ID** | DD-RIJKSMUSEUM-001 |
| **Type** | Source Activation |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-07 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first Rijksmuseum governance document |
| **Governing Amendments** | DD-RIJKSMUSEUM-001-A1 (Data Services Platform Amendment — ratified concurrently) |
| **Governing Documents** | Institution Coverage Audit v1.0 · MSC v1.2 · Standards Constitution v1.0 · M36 Engineering Specification v2 · Europeana Rights Matrix v1.0 |

---

## Background

The Rijksmuseum (Amsterdam, Netherlands) holds one of the world's premier collections
of Dutch Golden Age art, natural history illustration, cartography, and decorative arts.
It is rated Grade A in the Institution Coverage Audit v1.0: CC0-designated, high
commercial priority, excellent API quality, and identified as a Wave 3 onboarding target.

The Rijksmuseum is not currently registered in the NC `sources` table. No prior governance
document has authorized ingestion of Rijksmuseum content into the NC pipeline.

Unlike Europeana (an aggregator-source governed by DD-EUR-001), the Rijksmuseum is a
**direct content institution**. It holds, curates, and digitises its own collection.
Its API surfaces — Search API, OAI-PMH, IIIF Image API, IIIF Content State API —
are all first-party. There is no intermediary data provider; the Rijksmuseum is
simultaneously the holding institution and the API publisher.

The Rijksmuseum's Open Access programme, launched in 2011 and substantially expanded
since, designates high-resolution images of public domain works as CC0 1.0.
The `permitDownload` field in the Search API is the Rijksmuseum's machine-readable
attestation of CC0 status for a given object. As of 2026, over 700,000 objects
carry `permitDownload: true`.

Four prerequisites distinguish this Decision from DD-EUR-001:

| Distinction | Europeana | Rijksmuseum |
|---|---|---|
| Source role | Aggregator | Direct institution |
| `edm:dataProvider` routing | Required | Not applicable |
| Rights attestation | Rights Matrix URI vocabulary | `permitDownload` field + CC0 URI |
| Existing NC registration | `governance_state = 'active'` (Migration 17 backfill) | Not registered — INSERT required |
| IIIF delivery | Not primary delivery | First-class delivery mechanism |

Additionally, some Rijksmuseum objects may already be present in the NC pipeline via
the Europeana aggregator route (DD-EUR-001). This Decision establishes the
deduplication protocol for those objects.

---

## Findings

**F-1.** The Rijksmuseum is a Tier 1 Reference Institution under MSC v1.2 for
institution-direct ingestion via IIIF. Its API infrastructure — particularly the
Search API v4 and IIIF Image API v2.1 — meets or exceeds all MSC v1.2 Article 29
quality standards for Phase 1 media types.

**F-2.** The Rijksmuseum's `permitDownload: true` field constitutes a first-party
machine-readable CC0 attestation. It is the primary rights gate for NC ingestion.
No Rijksmuseum object with `permitDownload: false` is eligible for the NC pipeline
under any current or anticipated rights doctrine. This gate is simpler and more
authoritative than the multi-statement Europeana Rights Matrix vocabulary; a
separate Rights Matrix document is not required for this institution.

**F-3.** The Rijksmuseum Search API (`/api/{lang}/collection`) provides rights data,
image dimensions, creator provenance, and IIIF manifest links in a single response.
It is the authoritative source for `permitDownload` and is the designated ingest
surface for the pilot. The OAI-PMH endpoint is authorised for bulk metadata harvest
in Phase 2 but does not expose `permitDownload` and may not be used as the sole
ingest surface without Search API cross-reference.

**F-4.** The Rijksmuseum provides IIIF Image API v2.1 for all downloadable objects.
This is the designated mechanism for `media_file.source_url`. Full-resolution
IIIF delivery is available without additional authorisation. Thumbnail-only delivery
(`/full/!100,100/`) is not sufficient for NC; only full-resolution access
(`/full/full/0/default.jpg` or equivalent) satisfies the MSC v1.2 Article 29.2(d)
400px minimum.

**F-5.** IIIF is not currently listed in the NC Standards Constitution v1.0. This
Decision authorises `iiif` in the `sources.standards` array for the Rijksmuseum
source record, but formal Standards Constitution amendment SA-4 is required before
IIIF Presentation API manifests may be used as `source_record.schema_standard`.
For the pilot, `schema_standard = 'rijksmuseum_json_v4'` is used for Search API
JSON records.

**F-6.** The Institution Coverage Audit v1.0 identified Western Europe (Netherlands,
UK, US) as well-covered by comparison to critical geographic gaps (Africa, Asia-Pacific,
Latin America). Rijksmuseum onboarding is therefore a Wave 3 priority — high commercial
value but not structurally blocking the geographic coverage gaps that matter most.
This Decision authorises a scoped pilot only; broad Rijksmuseum harvest requires
DD-RIJKSMUSEUM-002 after pilot review.

**F-7.** Deduplication with Europeana-routed Rijksmuseum objects is required.
The Europeana `edm:dataProvider` field identifies Rijksmuseum as the contributing
institution for some objects already in or potentially entering the NC pipeline via
DD-EUR-001. When a direct Rijksmuseum `source_item` is created, any existing
Europeana-routed `source_item` for the same object must be identified and governed
per the deduplication protocol in Article 2(d).

**F-8.** The NC `sources` table does not contain a Rijksmuseum row. This Decision
authorises a new source INSERT (not an UPDATE). The source begins with
`governance_state = 'active'` under the authority of this Decision — unlike
Migration 17's blanket backfill, this activation is formally governed from creation.

---

## Decision

### Article 1 — Production Authorization

The Rijksmuseum is formally authorized as an active NC production source for
content acquisition effective upon ratification of this Decision.

The `sources.governance_state = 'active'` designation for the Rijksmuseum source
record is hereby formally governed by this Decision. No prior backfill or blanket
activation applies. This Decision is the sole authority for Rijksmuseum ingestion.

---

### Article 2 — Source Classification

The Rijksmuseum is designated as a **direct content institution** in NC's source
taxonomy.

**(a)** The Rijksmuseum holds, curates, and digitises its own collection. It is not
an aggregator. `source_record.institution_id = 'rijksmuseum'` for all records
ingested via the Rijksmuseum API. There is no `edm:dataProvider` routing rule.
The aggregator provenance rule (DD-EUR-001 Article 2(b)) does not apply.

**(b)** The Rijksmuseum source role is `'institution'`. The Europeana source role
is `'aggregator'`. These classifications are mutually exclusive. An object that
arrives via Europeana and is later re-ingested from Rijksmuseum directly is
governed by the deduplication protocol in Article 2(d), not by both DDs simultaneously.

**(c)** The Rijksmuseum `objectNumber` field (e.g., `SK-A-1505`) is the stable
`source_identifier`. It must be stored verbatim. Normalisation or truncation is
not permitted.

**(d) Europeana deduplication protocol.** When a direct Rijksmuseum `source_item`
is created during ingestion, the worker must query the NC database for an existing
`source_item` where:
```
source_id = 'europeana'
AND provenance->'nc:raw_payload_hash' IS NOT NULL
AND (
    normalized_payload->>'dataProvider' ILIKE '%rijksmuseum%'
    OR normalized_payload->>'record_id' ILIKE '%rijksmuseum%'
)
```
If a matching Europeana `source_item` exists for the same object, the Rijksmuseum
`source_item` is the canonical record. The Europeana `source_item` is flagged
`status = 'superseded_by_direct_source'` (or equivalent governed status) via
a `workflow_item` opened for human review. No automated DELETE. The human reviewer
confirms identity match and completes the transition. This protocol is subject to
DD-DEDUP-001 when that Decision is issued; until then, this article governs.

---

### Article 3 — Rights Authority

The Rijksmuseum `permitDownload` field is the governing rights gate for all NC
Rijksmuseum ingestion.

**(a) ALLOWED:** `permitDownload: true` AND `copyrightHolder` field is empty or
absent. These objects carry the Rijksmuseum's CC0 attestation. After human
verification, they yield `rights_status = 'verified_cc0'`.

**(b) REVIEW REQUIRED:** `permitDownload: true` AND `copyrightHolder` field is
non-empty. The Rijksmuseum attests download permission but asserts a copyright
holder. Human review is required to determine whether NC's PD hard gate is
satisfied. These objects enter the pipeline with `rights_status = 'pending_verification'`
and a `workflow_item` of `capability = 'rights_review'`.

**(c) BLOCKED:** `permitDownload: false`. No Rijksmuseum object with
`permitDownload: false` may enter the NC pipeline at any stage. Pre-ingestion
rejection is mandatory. Every rejection must be logged.

**(d)** The `rights_statement_uri` for ALLOWED objects is
`http://creativecommons.org/publicdomain/zero/1.0/`. No other rights URI may be
used for Rijksmuseum ALLOWED objects.

**(e)** The FM exclusion (FM Constitution v1.0 Invariant FM-4) applies permanently
to all Rijksmuseum-sourced assets, identical to DD-EUR-001 Article 3(c). No FM
output may influence any `media_rights` record for any Rijksmuseum-sourced asset.

**(f) Required evidence for ALLOWED objects:**
The `media_rights.rights_evidence` dict must include:

```json
{
  "source": "rijksmuseum",
  "source_record_id": "<uuid>",
  "permit_download_attested": true,
  "copyright_holder_field": "",
  "cc0_declaration_url": "https://www.rijksmuseum.nl/en/open-access-policy",
  "applying_institution": "Rijksmuseum Amsterdam",
  "raw_payload_hash": "<hash>",
  "worker_classified_status": "verified_cc0",
  "evidence_status": "pending_human_review"
}
```

`verified_by` and `verified_at` on `media_rights` remain NULL until a human
reviewer sets them. `commercial_reuse_permitted` and `modification_permitted`
remain FALSE until human verification. The worker may not set terminal rights
status. This invariant is identical to V1 (store.py remediation) and is
permanently enforced.

---

### Article 4 — API Governance

Four API surfaces are authorised. Each has a distinct role and governance posture.

#### 4.1 — Search API v4 (Pilot: Primary Ingest Surface)

```
Endpoint:    https://www.rijksmuseum.nl/api/{lang}/collection
Auth:        ?key=$RIJKSMUSEUM_API_KEY
Version:     v4
Format:      JSON
Rate limit:  10 requests/second; burst 50
```

**Authorised use:**
- Primary ingest surface for the pilot
- Rights determination (sole surface exposing `permitDownload`)
- Image dimension and URL discovery
- IIIF manifest link resolution
- Incremental update detection via `q` + date parameters

**Governance rules:**
- Worker must pass `imgonly=True` to exclude non-visual objects
- Worker must inspect `permitDownload` from the API response and gate on it
  before creating `source_record` (pre-ingestion filter, not post-ingestion)
- `ps` (page size) must not exceed 100 per request
- Language parameter defaults to `en` for metadata fields; `nl` records may
  supplement but must not replace English metadata for NC display fields

**Prohibited:**
- Ingestion of objects without an accessible `webImage.url`
- Any inference of rights from `dating.yearLate` alone without `permitDownload: true`
- Ignoring `copyrightHolder` field in rights classification

#### 4.2 — OAI-PMH (Phase 2: Bulk Metadata Harvest)

```
Endpoint:    https://www.rijksmuseum.nl/api/oai/$RIJKSMUSEUM_API_KEY
Formats:     oai_dc (Dublin Core), ese (Europeana Semantic Elements)
Harvest:     Full (ListRecords) + incremental (from/until parameters)
```

**Authorised use:**
- Bulk metadata harvest for comprehensive collection coverage
- Incremental harvest for changed-record detection
- `oai_dc` metadata prefix for maximum portability

**NOT authorised for pilot.** OAI-PMH does not expose `permitDownload`. Any
OAI-PMH-sourced record entering the NC pipeline MUST be cross-referenced against
the Search API before `source_record` creation to retrieve `permitDownload` status.
An OAI-PMH record that cannot be resolved via Search API must be BLOCKED pending
resolution. This cross-reference requirement makes OAI-PMH unsuitable for the pilot
without a dedicated resolver worker; its activation requires DD-RIJKSMUSEUM-002.

**Schema standard:** `source_record.schema_standard = 'dc'` for OAI-PMH records.

#### 4.3 — IIIF Image API v2.1 (Pilot: Media File Delivery)

```
Pattern:     https://www.rijksmuseum.nl/api/iiif/{objectNumber}/{region}/{size}/{rotation}/{quality}.{format}
Full res:    https://www.rijksmuseum.nl/api/iiif/{objectNumber}/full/full/0/default.jpg
Info:        https://www.rijksmuseum.nl/api/iiif/{objectNumber}/info.json
```

**Authorised use:**
- `media_file.source_url` = IIIF Image API base URI for the object
- Full-resolution image retrieval for MinIO ingestion
- Dimension discovery via `info.json`

**Governance rules:**
- Only full-resolution delivery is authorised for `media_file` ingestion
- `info.json` must be retrieved to populate `media_file.width_px` / `height_px`
  and to verify the MSC v1.2 Article 29.2(d) 400px minimum on the longest edge
- The IIIF Image API URI is constructed from `objectNumber` per the pattern above
  and from `webImage.url` as returned by the Search API

**Note on Standards Constitution:** `iiif` is added to `sources.standards` for
the Rijksmuseum source row by this Decision. Formal Standards Constitution amendment
SA-4 is required before IIIF Presentation API manifests may be used as
`source_record.schema_standard`. Until SA-4 is ratified, use `rijksmuseum_json_v4`.

#### 4.4 — IIIF Content State API (Phase 3: Deferred)

The Rijksmuseum IIIF Content State API is noted for future use. It is not
authorised for pilot ingestion. Its activation requires DD-RIJKSMUSEUM-002 and
Standards Constitution amendment SA-4.

---

### Article 5 — Metadata Standards Mapping

**`source_record.schema_standard`:** `rijksmuseum_json_v4` for Search API records.

The following mapping defines how Rijksmuseum Search API JSON fields map to NC
M36 substrate fields. The mapping is normative. Workers must implement it exactly.

#### 5.1 — Mandatory Fields

All 6 fields must be present. A Search API object missing any mandatory field
is **BLOCKED** at pre-ingestion and logged.

| NC field | Rijksmuseum API field | Notes |
|---|---|---|
| `source_identifier` | `objectNumber` | Verbatim. No normalisation. |
| `title` | `title` | Fallback: `longTitle` if `title` absent |
| `canonical_source_url` | `links.web` | Rijksmuseum website URL |
| `representative_media_url` | `webImage.url` | BLOCKED if absent |
| `rights_gate` | `permitDownload` | BLOCKED if `false` |
| `raw_payload_hash` | SHA-256 of canonical JSON | Computed by worker |

#### 5.2 — Standard Fields

Populated when present; NULL if absent.

| NC field | Rijksmuseum API field | Notes |
|---|---|---|
| `description` | `description` + `longTitle` | Combine if both present |
| `date` | `dating.presentingDate` | Fallback: `{yearEarly}–{yearLate}` |
| `creator` | `principalMakers[0].name` | First maker only for M36 |
| `creator_role` | `principalMakers[0].occupation[0]` | First occupation only |
| `width_px` | `webImage.width` | From Search API or IIIF `info.json` |
| `height_px` | `webImage.height` | From Search API or IIIF `info.json` |
| `rights_statement_uri` | `http://creativecommons.org/publicdomain/zero/1.0/` | Constant for ALLOWED objects |
| `copyright_holder` | `copyrightHolder` | Empty string treated as absent |
| `data_provider` | `'Rijksmuseum Amsterdam'` | Static constant; not from API |
| `iiif_manifest_url` | `https://www.rijksmuseum.nl/api/iiif/{objectNumber}/manifest.json` | Constructed from `objectNumber` |

#### 5.3 — Subject and Classification Fields

| NC field | Rijksmuseum API field | Notes |
|---|---|---|
| `subject_terms` | `classification.iconClasses[]` | Primary controlled vocabulary |
| `subject_terms` (append) | `materials[]` + `techniques[]` | Tagged `controlled_vocabulary: false` |
| `object_types` | `objectTypes[]` | Dutch-language values; pass through |

#### 5.4 — anchor_type Derivation

`anchor_type` must be set at ingest time using the following rule, applied in order:

1. If `objectTypes[]` contains any of: `kaart`, `atlas`, `globus`, `globe`, `map`
   → `anchor_type = 'geographic'`
2. Else if `classification.iconClasses[]` contains any of: `plants`, `animals`,
   `birds`, `fish`, `insects`, `botanical`, `zoological`, `fauna`, `flora`
   OR `objectTypes[]` contains: `natural history`, `naturalia`
   → `anchor_type = 'biological'`
3. Else if multiple categories from rules 1 and 2 are present simultaneously
   → `anchor_type = 'mixed'`
4. Default: `anchor_type = 'cultural'`

This derivation replaces the `'mixed'` default used for Europeana. Rijksmuseum
objects carry sufficient classification metadata to derive a meaningful anchor type
at ingest time.

---

### Article 6 — Source Registry Amendment

The following INSERT is authorised by this Decision and **must be applied before
the first production ingestion run.**

**Pre-INSERT verification:**
```sql
SELECT COUNT(*) FROM sources WHERE source_id = 'rijksmuseum';
-- Expected: 0 rows. If 1 row, do not INSERT — investigate.
```

**Amendment RU-SR-1 — Insert Rijksmuseum source record:**

```sql
-- DD-RIJKSMUSEUM-001 Article 6 — Source Registry Amendment RU-SR-1
-- Authorised by: DD-RIJKSMUSEUM-001
-- Ratification date: <insert date>
-- Applied by: <insert name>
-- Applied at: <insert timestamp>

INSERT INTO sources (
    source_id,
    name,
    description,
    institution,
    base_url,
    fetch_strategy,
    auth_type,
    priority,
    entity_types,
    standards,
    governance_state,
    operational_status,
    status,
    config,
    provenance,
    created_at,
    updated_at
) VALUES (
    'rijksmuseum',
    'Rijksmuseum',
    'Royal Museum of the Netherlands. Dutch Golden Age art, natural history illustration, cartography, and decorative arts. CC0 Open Access programme.',
    'Rijksmuseum Amsterdam',
    'https://www.rijksmuseum.nl/api',
    'api',
    'key',
    3,
    ARRAY['image', 'photography', 'map'],
    ARRAY['cidoc_crm', 'skos', 'prov_o', 'premis', 'dc', 'iiif'],
    'active',
    'unavailable',
    'active',
    '{
        "search_api_endpoint":      "https://www.rijksmuseum.nl/api/en/collection",
        "search_api_version":       "v4",
        "oai_pmh_endpoint":         "https://www.rijksmuseum.nl/api/oai",
        "iiif_image_api_pattern":   "https://www.rijksmuseum.nl/api/iiif/{object_number}",
        "iiif_manifest_pattern":    "https://www.rijksmuseum.nl/api/iiif/{object_number}/manifest.json",
        "auth_key_env":             "RIJKSMUSEUM_API_KEY",
        "rate_limit":               {"requests_per_second": 10, "burst": 50},
        "rights_strategy":          "permit_download_gate",
        "source_role":              "institution",
        "oai_pmh_formats":          ["oai_dc", "ese"],
        "iiif_delivery":            true,
        "completeness_minimum":     6,
        "rights_filter": {
            "mode":                 "pre_ingestion",
            "authority":            "dd_rijksmuseum_001",
            "require_permit_download": true,
            "allowed_rights_uris":  ["http://creativecommons.org/publicdomain/zero/1.0/"],
            "review_required_conditions": ["permit_download_true_copyright_holder_present"],
            "filter_mode":          "strict"
        }
    }'::jsonb,
    '{"nc:authority": "DD-RIJKSMUSEUM-001", "nc:activation_date": "<insert date>"}'::jsonb,
    NOW(),
    NOW()
);
```

**Note on `governance_state` / `operational_status` columns:** These columns are
added by Migration 17 (`17_source_governance.sql`). If Migration 17 has not been
applied to the target database, remove `governance_state` and `operational_status`
from the INSERT above. Apply Migration 17 first.

**Post-INSERT verification:**
```sql
SELECT
    source_id,
    config->>'source_role'                              AS source_role,
    config->>'rights_strategy'                         AS rights_strategy,
    (config->'rights_filter'->>'require_permit_download')::boolean AS permit_download_gate,
    'iiif' = ANY(standards)                            AS iiif_in_standards,
    'dc' = ANY(standards)                              AS dc_in_standards,
    'image' = ANY(entity_types)                        AS image_active
FROM sources
WHERE source_id = 'rijksmuseum';
-- All boolean columns must return true.
```

---

### Article 7 — Pilot Scope

This Decision authorises a **scoped pilot** only. Production ingestion is limited
to the following parameters.

**(a) Content category.** The pilot targets **natural history illustration**:
zoological and botanical prints, etchings, and drawings where the subject matter
is fauna or flora. This category maps to `anchor_type = 'biological'`, aligns with
NC's illustration opportunity doctrine, and represents the highest-priority
Rijksmuseum content for the NC commerce platform.

**(b) Search API query parameters.**
```
api         = Rijksmuseum Search API v4
endpoint    = https://www.rijksmuseum.nl/api/en/collection
key         = $RIJKSMUSEUM_API_KEY
imgonly     = True
type        = print
q           = fauna OR flora OR botanical OR zoological OR bird OR fish OR insect
ps          = 100
p           = 1  (paginate as needed up to asset cap)
```

Pre-ingestion filter applied by worker (not query parameter):
```
permitDownload = true   (inspect each object in response; reject if false)
```

**(c) Asset cap.** The pilot is capped at **100 assets** that pass the pre-ingestion
gate (`permitDownload: true`, all 6 mandatory fields present). Objects rejected at
the pre-ingestion gate do not count toward the cap.

**(d) Place association.** Rijksmuseum content is not geographically queryable at
the same specificity as Europeana's Yellowstone query. Place association is
**not required at ingestion time** for Rijksmuseum assets. It is required before
`activation_eligible`. The activation review workflow must include a place
association step: the human reviewer assigns at least one NC `places` record
before the asset may advance. Assets without a place association may not reach
`activation_eligible`.

**(e) Anchor type.** The derivation rule in Article 5.4 applies at ingest time.
For the natural history pilot, the expected outcome is predominantly
`anchor_type = 'biological'`. Mixed outcomes are permitted.

**(f) Query scope lock.** Only assets matching the Article 7(b) query scope may
be ingested under DD-RIJKSMUSEUM-001. Any expansion of subject, type, language,
or rights scope requires DD-RIJKSMUSEUM-002.

**(g) Pilot window.** 90 calendar days from the date of first production ingestion
run, or when the 100-asset cap is reached — whichever comes first. Pilot review
within 14 calendar days of pilot end.

---

### Article 8 — Pilot Success Criteria

The pilot is evaluated at the conclusion of the pilot window. Success on all
criteria triggers the DD-RIJKSMUSEUM-002 decision process for scope expansion.

| # | Criterion | Threshold | Metric |
|---|---|---|---|
| SC-1 | Activated assets | ≥ 10 assets reach `activation_target` with second-human approval | `COUNT(activation_targets) WHERE source = 'rijksmuseum'` |
| SC-2 | Rights verification completeness | 100% of `activation_eligible` assets have complete evidence in `media_rights.rights_evidence` | No `verified_cc0` record missing required evidence fields per Article 3(f) |
| SC-3 | BLOCKED filter accuracy | 100% of `permitDownload: false` objects rejected at pre-ingestion gate | Zero `permitDownload: false` objects in `source_record` |
| SC-4 | Place association | 100% of activated assets have at least one `places` record assigned | No `activation_target` missing `place_id` for Rijksmuseum assets |
| SC-5 | FM exclusion | Zero FM output connected to any rights determination | No `fm_candidate_record` referenced in any Rijksmuseum `workflow_item` or `media_rights` preservation event |
| SC-6 | IIIF image quality | 100% of ingested assets meet the 400px minimum on longest edge | No `media_technical_metadata` with `quality_flag = 'below_minimum'` for Rijksmuseum assets |
| SC-7 | anchor_type derivation accuracy | ≥ 90% of pilot assets have `anchor_type != 'mixed'` (Article 5.4 rule fires correctly) | Operator review of `anchor_type` distribution |
| SC-8 | Pipeline completion rate | ≥ 80% of ingested assets complete pre-activation gates without worker error | Ingestion error rate ≤ 20% |

**Pilot failure definition:** SC-3 and SC-5 are constitutional. Failure on either
suspends the pilot immediately. SC-1, SC-2, SC-4, SC-6, SC-7, SC-8 are
performance criteria; failure triggers remediation without suspension.

---

### Article 9 — Required Actions Before First Ingestion Run

All items must be complete before the first ingestion run begins. No partial
completion is acceptable.

| # | Action | Gate |
|---|---|---|
| 9.1 | DD-RIJKSMUSEUM-001 ratified (Director signature + second-human approval) | Gate 1 |
| 9.2 | Source registry amendment RU-SR-1 applied and verified | Gate 2 |
| 9.3 | `RIJKSMUSEUM_API_KEY` set in `.env` and validated (test query returns ≥ 1 result) | Gate 3 |
| 9.4 | Rijksmuseum ingestion worker implemented with pre-ingestion `permitDownload` gate | Gate 3 |
| 9.5 | Article 5.4 `anchor_type` derivation logic implemented and unit-tested | Gate 3 |
| 9.6 | At least one human reviewer authorized for `rights_review` workflow items (may be same person as DD-EUR-001 rights reviewer) | Gate 3 |
| 9.7 | FM exclusion confirmed in writing for Rijksmuseum pipeline | Gate 3 |

---

### Article 10 — Explicit Exclusions

This Decision does not authorise:

**(a)** Ingestion of objects with `permitDownload: false`, regardless of creation
date, creator, or any other signal.

**(b)** OAI-PMH as a standalone ingest surface without Search API cross-reference
for `permitDownload`. OAI-PMH-only ingestion requires DD-RIJKSMUSEUM-002.

**(c)** IIIF Presentation API manifests as `source_record.schema_standard`.
Requires Standards Constitution amendment SA-4.

**(d)** IIIF Content State API ingestion. Requires DD-RIJKSMUSEUM-002 and SA-4.

**(e)** Ingestion of `objectTypes` outside the pilot scope defined in Article 7(b)
(paintings, furniture, jewellery, ceramics, coins, weapons, textiles, etc.
are excluded from this Decision).

**(f)** Ingestion of Rijksmuseum map holdings (`anchor_type = 'geographic'`).
Maps require a separate geographic pilot scope in DD-RIJKSMUSEUM-002.

**(g)** Phase 2–4 media types (`book`, `ebook`, `audio`, `film`, `dataset`, `3d`).
Phase 1 only: `image`, `photography`. (`map` deferred per (f) above.)

**(h)** Date-based PD determination as a standalone rights gate. `permitDownload`
is mandatory. Creation date alone does not satisfy the NC PD hard gate for
Rijksmuseum content.

**(i)** Increasing the `completeness_minimum` below 6 without a new Director
Decision. The floor may be raised by configuration update; it may not be lowered.

**(j)** Any use of the Rijksmuseum Linked Data API or SPARQL endpoint. Only
the four surfaces listed in Article 4 are authorised.

---

### Article 11 — Subsequent Decisions

| ID | Trigger | Scope |
|---|---|---|
| **DD-RIJKSMUSEUM-002** | Pilot success (SC-1 through SC-8 met) | Scope expansion: maps, paintings, OAI-PMH bulk harvest, cap removal |
| **SA-4** | Required for IIIF manifest as `schema_standard` | Standards Constitution amendment: add IIIF Presentation API v3 |
| **DD-DEDUP-001** | Growing overlap between direct sources and Europeana-routed objects | Deduplication governance: `source_item` identity merge protocol |

DD-RIJKSMUSEUM-002 is not automatically triggered by pilot success. It requires
a Director review of pilot results, a Principal Architect recommendation, and
a new Decision document.

---

## Ratification

This Decision requires:

1. **Director signature** — opengracelabs (the Director)
2. **Second-human approval** — a second person with authority over NC governance decisions

| Role | Name | Date |
|---|---|---|
| Director | — | — |
| Second Human Approver | — | — |

---

*DD-RIJKSMUSEUM-001 Draft — 2026-06-07*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending ratification by: Director (opengracelabs)*
