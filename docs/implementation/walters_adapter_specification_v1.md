# Walters Adapter Specification v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Status | Engineering assessment and adapter design |
| Adapter | `walters_adapter` |
| Source | Walters Art Museum |
| Official data surface | Static CSV files in `WaltersArtMuseum/api-thewalters-org` |
| Governing decision | `DD-WALTERS-001` draft |
| Schema standard | `walters_opendata_v1` |
| Rights policy | `walters_rights_matrix_v1` |
| Reuse target | Reuse `workers.shared_media_adapter` write, technical, rights URI, and replay infrastructure |

## Engineering Assessment

Walters can inherit the current shared media architecture, but it cannot inherit any prior
institution-specific client or rights matrix unchanged.

The official Walters API v1 closed in 2023. Until v2 is available, Walters publishes
official static data files through its GitHub repository. This makes Walters closest to
NGA architecturally: both are deterministic CSV-bulk sources, not paginated REST APIs.
The image delivery model is simpler than NGA because Walters provides direct JPEG URLs in
`media.csv.ImageURL`; no IIIF URL construction is required.

Estimated implementation split:

| Area | Shared adapter reuse | New code | Complexity |
|---|---:|---:|---|
| M36 write path | 90% | 10% | Low |
| Technical metadata | 80% | 20% | Low |
| Replay/compliance tests | 80% | 20% | Low |
| Client/data loading | 35% | 65% | Medium |
| Rights classification | 55% | 45% | Low-Medium |
| Normalization | 55% | 45% | Medium |
| Image delivery | 75% | 25% | Low |
| Overall adapter | 70% | 30% | Medium-Low |

Engineering ROI: high. Walters has a clean CC0 posture, direct image URLs, no
authentication, and a deterministic CSV ingestion path. New work is mostly field binding,
CSV joins, pipe-delimited parsing, and source-specific evidence fields.

## Complexity Ratings

| Dimension | Rating | Reason |
|---|---|---|
| Rights complexity | Low-Medium | Institution-wide CC0, but no per-record rights field. Classifier must validate joined object/image completeness and cite the institutional CC0 basis. |
| Metadata complexity | Medium | Rich object records with camelCase CSV headers, pipe-delimited fields, creator joins, collection codes, and HTML descriptions. |
| Image complexity | Low | Direct JPEG URL from `media.csv.ImageURL`; no IIIF, no manifest, no size parameter construction. |
| Store complexity | Low | Existing shared M36 write path is sufficient after adding Walters rights evidence in shared store. |

## Authoritative Official Inputs

Required official files:

| File | Purpose |
|---|---|
| `art.csv` | Primary object metadata |
| `media.csv` | Image records and direct image URLs |
| `creators.csv` | Creator name and nationality joins |

Optional enrichment files:

| File | Purpose |
|---|---|
| `collections.csv` | Collection labels/code enrichment |
| `relationships.csv` | Multi-object relationships |
| `exhibitions.csv` | Exhibition evidence |

Base URL:

```text
https://raw.githubusercontent.com/WaltersArtMuseum/api-thewalters-org/main/
```

Do not use retired v1 REST endpoints for production implementation. If Walters API v2
becomes public, evaluate it through a follow-up decision before replacing the CSV path.

## Reuse Boundary

`walters_adapter` must reuse:

| Shared module | Walters use |
|---|---|
| `workers.shared_media_adapter.store` | `StoreRuntime` and `write_normalized_record()` only; no SQL fork |
| `workers.shared_media_adapter.technical` | Baseline content, quality flag, validation status, content hash |
| `workers.shared_media_adapter.replay` | Replay connection, write-order assertions, blocked-record assertions |
| `workers.shared_media_adapter.rights` | CC0 URI constants and shared terminal/non-terminal wording conventions |

Walters-specific modules own:

- CSV download/loading and deterministic indexing
- `art.csv` + `media.csv` + `creators.csv` joins
- primary image selection from `IsPrimary` and `Rank`
- pipe-delimited parsing for `Images`, `CollectionID`, `CollectionName`, `Creators`
- institution-wide CC0 rights matrix
- Walters-specific normalization and evidence fields
- anchor type derivation

## Sprint 1 Client Design

Create `workers/walters_adapter/`:

- `__init__.py`
- `config.py`
- `client.py`

Client requirements:

| Function | Responsibility |
|---|---|
| `csv_url(filename)` | Build official raw GitHub CSV URL |
| `load_csv_text(text)` | Parse UTF-8 CSV deterministically |
| `load_csv_file(path)` | Load replay fixtures |
| `fetch_csv(filename, http_client=None)` | Fetch one official CSV |
| `load_dataset(directory)` | Load required CSV fixtures |
| `get_object(dataset, object_id)` | Lookup one `art.csv` row |
| `get_media_for_object(dataset, object_id)` | Return `MediaType == "Image"` rows sorted by primary/rank/id |
| `select_primary_image(rows)` | Prefer `IsPrimary == "1"`, then lowest `Rank` |
| `get_creators_for_object(dataset, object_id)` | Split `art.Creators`, join to `creators.csv` |
| `search_objects(...)` | Deterministic local search over loaded CSV rows |

Determinism:

- enumerate objects by integer `ObjectID ASC`
- sort media by `(primary desc, Rank asc, MediaXrefID asc, Filename asc)`
- split pipe-delimited values while dropping empty strings
- no store writes in Sprint 1

## Walters Rights Matrix v1

Module: `workers/walters_adapter/rights.py`

Policy ID: `walters_rights_matrix_v1`

Classification input is the joined pair: `object_row`, `image_row`.

| Rule | Condition | Outcome | `rights_basis` |
|---|---|---|---|
| WLT-R-1 | `object_row` is not a dict | BLOCKED | `missing_object_record` |
| WLT-R-2 | `image_row` is not a dict | BLOCKED | `no_image_record` |
| WLT-R-3 | `ImageURL` missing or blank | BLOCKED | `missing_image_url` |
| WLT-R-4 | prior rules pass | ALLOWED | `walters_institution_cc0` |

Allowed output:

- `decision = ALLOWED`
- `rights_statement_uri = CC0_URI`
- `rights_status = "pending_verification"`
- `rights_policy_id = "walters_rights_matrix_v1"`

There is no `REVIEW_REQUIRED` class. Blocked records produce zero writes.

## Normalization Design

Module: `workers/walters_adapter/normalize.py`

Canonical mapping:

| Source | Normalized field | Rule |
|---|---|---|
| `art.ObjectID` | `record_id` | string |
| `art.ObjectNumber` | `accession_number`, `walters_object_number` | strip |
| `art.Title` | `title` | strip |
| `art.DateText` | `date` | strip |
| `art.DateBeginYear` | `date_start` | optional integer |
| `art.DateEndYear` | `date_end` | optional integer |
| `art.Description` | `description` | strip HTML or preserve text safely; fallback to `Medium` |
| `art.Medium` | `medium` | strip |
| `art.Culture` | `culture` | strip |
| `art.Style` | `style` | strip |
| `art.Classification` | `classification`, `edm_type` | strip |
| `art.ObjectName` | `object_name` | strip |
| `art.CollectionID` | `collection_codes` | split on `\|` |
| `art.CollectionName` | `collection_names` | split on `\|` |
| `art.ResourceURL` | `source_url` | prefer provided URL |
| joined creator rows | `creator`, `creator_nationality` | join names/nationalities with `; ` |
| `media.ImageURL` | `representative_media_url` | verbatim |
| all image URLs | `preview_urls` | primary first, deduplicated |
| joined payload | `raw_payload_hash` | canonical JSON SHA-256 |

Walters evidence fields in normalized payload:

- `walters_object_id`
- `walters_object_number`
- `walters_media_xref_id`
- `walters_image_url`
- `walters_filename`
- `walters_media_view`
- `walters_rank`
- `walters_is_primary`

## Image Delivery

Image source:

```text
media.csv.ImageURL
```

Expected pattern:

```text
https://art.thewalters.org/images/raw/{Filename}
```

No IIIF support is assumed. Do not create `walters_manifest_url`. Do not construct
alternate image sizes unless a future official API documents them.

Primary image selection:

1. Filter `MediaType == "Image"`.
2. Prefer rows with `IsPrimary == "1"`.
3. Tiebreak by lowest integer `Rank`.
4. Tiebreak by lowest integer `MediaXrefID`.
5. If no primary exists, use lowest-rank image row.

## Store Design

Module: `workers/walters_adapter/store.py`

Reuse `workers.shared_media_adapter.store.write_normalized_record()`.

Runtime:

| Field | Value |
|---|---|
| `source_slug` | `walters` |
| `schema_standard` | `walters_opendata_v1` |
| `rights_policy_id` | `walters_rights_matrix_v1` |
| `workflow_record_id_key` | `walters_object_id` |
| `worker_id` | `walters_adapter:sprint3` |

Raw payload must include actual joined records:

```json
{
  "object": "<art.csv row>",
  "selected_image": "<primary media.csv row>",
  "images": ["<all image rows for object>"],
  "creators": ["<joined creator rows>"]
}
```

Shared-store prerequisite before Sprint 3:

- include `"walters"` in the non-terminal `worker_classified_status` remap set
- inject Walters evidence fields into `build_rights_evidence()`

Required rights evidence:

- `walters_object_id`
- `walters_object_number`
- `walters_media_xref_id`
- `walters_image_url`
- `walters_is_primary`

## Anchor Type Rules

Implement ordered rules in `store.py::derive_anchor_type()`:

1. manuscript/book classification or object name -> `geographic`
2. culture present -> `geographic`
3. creator nationality present -> `geographic`
4. biological keyword in title/description/object name/collection name -> `biological`
5. collection code in `BYZ`, `EGY`, `GRK`, `ISL`, `CHN`, `IND`, `ANE`, `ETH`, `AME`, `JAP`, `SEA` -> `geographic`
6. keyword fallback for place/culture terms -> `geographic`
7. otherwise -> `cultural`

## Test Plan

Unit tests:

- CSV URL construction and unsupported file rejection
- CSV parsing with Walters camelCase headers
- object lookup
- media lookup and primary image selection
- creator join
- pipe-delimited parsing
- rights matrix allowed/blocked cases
- normalization mapping and evidence fields
- technical metadata content/hash
- blocked records produce zero writes

Replay tests:

- fixture load for `art.csv`, `media.csv`, `creators.csv`
- deterministic search/enumeration
- allowed joined record writes full M36 path
- blocked missing image and missing `ImageURL` records write nothing
- raw payload contains actual joined object/media/creator rows

Compliance tests:

- no AIC/Met/NGA/SMK SQL fork
- shared M36 write order
- rights evidence completeness
- `worker_classified_status` uses non-terminal wording

## Sprint Build Sequence

1. Sprint 1: `config.py`, `client.py`, fixtures, client/replay tests. No store writes.
2. Sprint 2: `rights.py`, `normalize.py`, Walters Rights Matrix v1, replay coverage.
3. Sprint 3: `technical.py`, `store.py`, shared-store Walters evidence extension, full M36 path.
4. Sprint 3B if audit requires: evidence field or anchor-type corrections only.

## Assessment Result

Walters is a strong adapter candidate. It should proceed after `DD-WALTERS-001` and the
Walters adapter profile are ratified. The adapter should inherit NGA's CSV-bulk posture
and the shared M36 write path, while implementing a source-specific institution-wide CC0
rights matrix and direct-JPEG image model.
