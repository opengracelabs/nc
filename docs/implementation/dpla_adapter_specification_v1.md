# DPLA Adapter Specification v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Status | Build plan only - ready for implementation after DD-DPLA-001 ratification |
| Adapter | `dpla_adapter` |
| Source | Digital Public Library of America |
| API key | Configured as `DPLA_API_KEY` |
| API surface | DPLA Items API only: `https://api.dp.la/v2/items` |
| Standards | DPLA MAP v5 mapped to M36 normalized media contract |
| Governance | DD-DPLA-001, MSC v1.2, Europeana Rights Matrix v1.0, Institution Factory Constitution v1.0 |
| Reuse target | Maximum reuse of `workers/shared_media_adapter` |

## Mission

Build `dpla_adapter` as a thin source-specific adapter over the frozen
`shared_media_adapter`.

The DPLA adapter must not create a parallel media ingestion path. It is responsible only
for DPLA API access, DPLA MAP v5 normalization, DPLA-specific rights pre-processing,
asset resolution state, and source-specific provenance fields. The shared adapter remains
the authority for:

- normalized record contract checks
- URI rights normalization and classification
- M36 write order
- media rights evidence baseline
- technical metadata hash and validation helpers
- replay connection and write-order assertions

The resulting flow is:

```text
DPLA Items API
  -> dpla_adapter.client
  -> dpla_adapter.normalize
  -> dpla_adapter.rights
  -> shared_media_adapter.store.write_normalized_record
  -> shared_media_adapter.replay assertions
```

## Reuse Boundary

`dpla_adapter` must import and reuse these shared modules:

| Shared module | DPLA usage |
|---|---|
| `workers.shared_media_adapter.contracts` | Enforce `NormalizedMediaRecord` field shape and mandatory warnings |
| `workers.shared_media_adapter.rights` | Normalize/classify URI-form `edm:rights` and classifiable rights URIs found in `sourceResource.rights` |
| `workers.shared_media_adapter.technical` | Build common visual technical metadata and quality flags |
| `workers.shared_media_adapter.store` | Use `StoreRuntime` and `write_normalized_record()` as the only M36 write path |
| `workers.shared_media_adapter.replay` | Reuse replay connection, write-order assertions, and rights evidence contract checks |

`dpla_adapter` may add DPLA-specific wrappers, but must not fork shared write SQL,
rights URI allowlists, technical content hashing, or replay write-order expectations.

## 1. API Client

Module: `workers/dpla_adapter/client.py`

The client is a deterministic wrapper around the DPLA Items API.

Required configuration:

| Setting | Value |
|---|---|
| `DPLA_API_KEY` | Required environment variable |
| `DPLA_API_BASE_URL` | Default `https://api.dp.la/v2` |
| `DPLA_ITEMS_PATH` | `/items` |
| `DPLA_RATE_LIMIT_RPS` | Default `2` |
| `DPLA_TIMEOUT_SECONDS` | Default `30` |
| `DPLA_PAGE_SIZE` | Default `100`, bounded by source policy |

Required client functions:

| Function | Responsibility |
|---|---|
| `search_items(query, *, page_size, page)` | Fetch one DPLA result page |
| `iter_items(query, *, max_records)` | Deterministically page through results |
| `fetch_item(record_id)` | Fetch one item by DPLA `@id` or API item id |
| `canonical_request_params(...)` | Return sorted request params for replay hashes/logs |

Pilot query shape from DD-DPLA-001:

```text
endpoint: https://api.dp.la/v2/items
q: yosemite
api_key: $DPLA_API_KEY
page_size: 100
sort_by: score
```

Rights filtering is local post-retrieval logic. The client must not rely on DPLA
server-side rights filtering for production eligibility.

The client must preserve the full raw item payload exactly as returned by DPLA. No
field normalization may occur in `client.py` beyond JSON decoding and deterministic
request logging.

## 2. Metadata Normalization

Module: `workers/dpla_adapter/normalize.py`

Normalization maps DPLA MAP v5 records into the shared normalized media record shape
defined by `workers.shared_media_adapter.contracts.REQUIRED_NORMALIZED_FIELDS`.

Canonical normalized fields:

| Normalized field | DPLA source | Rule |
|---|---|---|
| `record_id` | `@id` | Required; canonical DPLA item identifier |
| `title` | `sourceResource.title` | Required; first value if array |
| `description` | `sourceResource.description` | First value if array; warning if absent |
| `date` | `sourceResource.date.displayDate`, `.begin`, `.end` | Prefer display date; fall back to begin/end |
| `creator` | `sourceResource.creator` | Join arrays with `; ` |
| `subject_terms` | `sourceResource.subject[].name`, strings in `sourceResource.subject` | Flatten to strings; preserve order |
| `rights_uri` | `edm:rights` or classifiable URI in `sourceResource.rights` | DPLA rights shim selects value |
| `provider` | `provider.name` or `provider` | Service Hub; required for provenance when available |
| `dataProvider` | `dataProvider` | Contributing institution; required |
| `edm_type` | `sourceResource.type` | Normalize Phase 1 visual signals only |
| `source_url` | `isShownAt` | Contributing institution item page |
| `representative_media_url` | `object`, then best `hasView[].@id` | Stage 1 preview unless full-resolution verified |
| `preview_urls` | `object`, thumbnails, `hasView` previews | Deduplicate while preserving order |
| `width_px` / `height_px` | DPLA image fields if present; probe result if available | Optional at initial ingest |
| `raw_payload_hash` | canonical raw JSON hash | SHA-256, stable key order |
| `rights_decision` | DPLA rights shim | Mirror shared rights decision |
| `rights_allowed` | DPLA rights shim | Mirror shared rights allowed flag |

Quality floor before shared write:

- reject if `sourceResource.title` is absent
- reject if `dataProvider` is absent
- reject if `object` is absent
- reject if both `edm:rights` and `sourceResource.rights` are absent
- reject non-Phase-1 media types: book, audio, film, 3D, dataset

The normalized record should include DPLA-specific optional fields under stable keys,
but those fields must not be required by the shared adapter:

| Optional field | Meaning |
|---|---|
| `dpla_id` | Same as `@id`, retained for explicit source-specific evidence |
| `dpla_api_url` | API URL used to fetch the record |
| `provider_hub_id` | Hub identifier if DPLA exposes one |
| `provider_hub_name` | Service Hub name |
| `contributing_institution` | Alias of `dataProvider` for evidence readability |
| `provenance_chain` | `[dataProvider, provider, "dpla", "nc"]` |
| `source_resource_rights_raw` | Exact raw `sourceResource.rights` value |
| `edm_rights_raw` | Exact raw `edm:rights` value |
| `has_view_urls` | Candidate image URLs from `hasView` |
| `delivery_tier` | `preview`, `full_resolution`, or `preview_only` |
| `delivery_status` | `pending_resolution`, `resolved`, or `unresolvable` |
| `date_confidence` | `display`, `parsed`, or `absent` |

## 3. Rights Handling

Module: `workers/dpla_adapter/rights.py`

DPLA rights handling has two stages:

1. Select and classify the best rights signal.
2. Pass URI-form classifications to the shared rights classifier wherever possible.

URI path:

- Prefer `edm:rights` when it contains a URI.
- If `edm:rights` is absent, scan `sourceResource.rights` for a single classifiable URI.
- Normalize and classify the URI with `workers.shared_media_adapter.rights.classify_rights()`.
- BLOCKED classifications are rejected before `write_normalized_record()`.
- REVIEW_REQUIRED classifications may be written and must create a rights review workflow item through the shared store path.

Free-text path:

| Free-text pattern | DPLA classification | Shared write behavior |
|---|---|---|
| `public domain` | NKC-equivalent | Write as review-required only with DPLA evidence extension |
| `no known copyright` | NKC-equivalent | Write as review-required only with DPLA evidence extension |
| `no copyright restrictions` | NKC-equivalent | Write as review-required only with DPLA evidence extension |
| `copyright not evaluated` | CNE-equivalent | Reject before shared write |
| absent rights text | Absent | Reject before shared write |
| unknown text | Unknown | Reject before shared write |

Because the shared store currently rejects missing `rights_uri`, free-text NKC-equivalent
records need a DPLA-specific review URI sentinel only if approved by governance. Until
that sentinel is approved, v1 implementation should log free-text NKC-equivalent
records as `review_candidate_not_written` and not call the shared store. This preserves
the frozen shared adapter contract.

Required DPLA evidence extension for free-text review candidates:

```json
{
  "rights_source": "dpla_freetext",
  "original_text": "<exact sourceResource.rights text>",
  "classification": "nkc_equivalent",
  "review_rule": "HR-2c"
}
```

DPLA NoC-US enhanced review:

For URI records classified as NoC-US, the DPLA adapter must add a source-specific
evidence extension to the normalized payload or review context:

```json
{
  "dpla_nocus_enhanced_check": true,
  "contributing_institution": "<dataProvider>",
  "hub": "<provider>",
  "publication_year_verified": false,
  "publication_year": null,
  "pd_basis": "us_publication_before_1928",
  "hub_rights_enrichment_level": "unknown"
}
```

No Foundation Model output may participate in any DPLA rights decision.

## 4. Asset Retrieval Path

Module: `workers/dpla_adapter/assets.py`

DPLA does not provide a reliable full-resolution media API. The adapter must treat
retrieval as a two-stage process.

Stage 1: Preview ingest

- Use `object` as the initial `representative_media_url`.
- Set `delivery_tier = "preview"`.
- Set `delivery_status = "pending_resolution"`.
- Write via shared store only if all rights and metadata gates pass.
- Do not mark the asset activation eligible from preview delivery alone.

Stage 2: Full-resolution resolution

- Fetch `isShownAt`, the contributing institution item page.
- Locate a full-resolution image URL from the page or from better `hasView` candidates.
- Probe image dimensions.
- Require at least 400px on the shortest side before activation eligibility.
- Update media delivery metadata to `delivery_tier = "full_resolution"` and `delivery_status = "resolved"` when confirmed.

Failure path:

- If no full-resolution URL is available, keep the item at `delivery_status = "pending_resolution"` for up to 30 days.
- After 30 days, mark `delivery_status = "unresolvable"`.
- `preview_only` or `unresolvable` assets are excluded from activation.

The shared adapter writes the initial `media_file` row. Any later full-resolution update
must be a separate DPLA asset-resolution worker or follow-up store function; it must not
change the frozen initial write order.

## 5. Replay Strategy

Replay must prove that DPLA-specific logic remains thin and deterministic.

Required fixture classes:

| Fixture | Expected result |
|---|---|
| `dpla_uri_cc0_image.json` | Written through shared store; no workflow item |
| `dpla_uri_pdm_image.json` | Written through shared store; no workflow item |
| `dpla_uri_nocus_image.json` | Written through shared store; DPLA NoC-US evidence extension present |
| `dpla_uri_nkc_image.json` | Written through shared store; rights review workflow item |
| `dpla_freetext_public_domain.json` | Not written until freetext sentinel/evidence path is approved; logged as review candidate |
| `dpla_blocked_incopyright.json` | Rejected before shared write; no SQL events |
| `dpla_missing_object.json` | Rejected by quality floor; no SQL events |
| `dpla_non_visual_book.json` | Rejected by media scope; no SQL events |

Replay assertions:

- use `workers.shared_media_adapter.replay.ReplayConn`
- use `assert_m36_write_order()` for written URI records
- use `assert_no_writes()` for blocked, missing-quality, and unsupported-media records
- use `assert_rights_evidence_contract(evidence, source="dpla")`
- assert `schema_standard == "dpla_map_v5"` after SA-5 ratification; use a temporary non-production test value only before SA-5
- assert `provider` and `dataProvider` are both present in normalized payloads that reach shared write
- assert raw payload hash is stable for reordered JSON keys
- assert `object` starts as preview delivery and never implies activation eligibility

Replay command target:

```text
pytest tests/unit/test_dpla_client.py \
       tests/unit/test_dpla_normalize.py \
       tests/unit/test_dpla_rights.py \
       tests/unit/test_dpla_assets.py \
       tests/replay/test_dpla_adapter_sprint1.py
```

## 6. Source-Specific Fields

DPLA source-specific fields belong in normalized payload extensions and rights evidence,
not in new database tables.

Required source-specific fields:

| Field | Required before write? | Purpose |
|---|---:|---|
| `dpla_id` | Yes | Canonical DPLA identifier and dedupe key |
| `dpla_api_url` | Yes | Replayable source API URL |
| `provider_hub_name` | Yes | Service Hub provenance |
| `contributing_institution` | Yes | Original contributing institution |
| `provenance_chain` | Yes | Preserve institution -> hub -> DPLA -> NC chain |
| `edm_rights_raw` | When present | Raw URI rights evidence |
| `source_resource_rights_raw` | When present | Raw free-text or URI rights evidence |
| `rights_signal_source` | Yes | `edm:rights`, `sourceResource.rights_uri`, or `sourceResource.rights_text` |
| `dpla_rights_extension` | Conditional | Free-text or NoC-US enhanced evidence |
| `delivery_tier` | Yes | Preview/full-resolution status |
| `delivery_status` | Yes | Resolution lifecycle |
| `has_view_urls` | No | Alternative image candidates |
| `date_confidence` | No | Date quality indicator |

These fields must be serialized inside `source_record.normalized_payload` and, where
rights-related, copied into `media_rights.rights_evidence` by a DPLA wrapper when the
shared evidence contract does not already include them.

## Proposed Package Layout

```text
workers/dpla_adapter/
  __init__.py
  config.py
  client.py
  normalize.py
  rights.py
  media_type.py
  technical.py
  assets.py
  store.py
  main.py
```

`store.py` should mirror the existing Europeana/Rijksmuseum pattern:

```text
normalize raw payload
derive DPLA runtime
call shared_media_adapter.store.write_normalized_record()
```

Runtime configuration:

| `StoreRuntime` field | DPLA value |
|---|---|
| `worker_id` | `dpla_adapter:v1` |
| `source_slug` | `dpla` |
| `schema_standard` | `dpla_map_v5` after SA-5 |
| `technical_schema_version` | `dpla-technical-v1` |
| `validator_name` | `dpla_adapter.technical.validation_status` |
| `validator_version` | `v1` |
| `workflow_record_id_key` | `dpla_record_id` |
| `anchor_type` | `mixed` by default; may derive `geographic` for maps/place-specific records |

## Implementation Gates

The adapter is ready for first production run only after:

1. DD-DPLA-001 is ratified.
2. DPLA source registry INSERT is complete.
3. Standards Amendment SA-5 registers `dpla_map_v5`.
4. URI rights fixtures prove shared rights reuse.
5. BLOCKED and unknown free-text fixtures prove zero writes.
6. Hub provenance is present for every written record.
7. Asset resolution logic proves preview-only assets cannot become activation eligible.
8. Replay tests prove the shared M36 write order is unchanged.

## Summary

`dpla_adapter` is a DPLA MAP v5 edge adapter, not a new substrate implementation.

Maximum reuse means:

- DPLA owns API access, MAP v5 normalization, hub provenance, free-text rights handling,
  and image resolution lifecycle.
- `shared_media_adapter` owns URI rights policy, M36 writes, technical metadata baseline,
  and replay write-order guarantees.
- No source-specific schema is introduced for v1.
- Full-resolution retrieval is a second-stage resolution path and must not weaken the
  initial shared ingest contract.
