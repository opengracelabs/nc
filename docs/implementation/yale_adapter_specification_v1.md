# Yale Adapter Specification v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Status | Engineering ROI assessment and adapter design |
| Adapter | `yale_adapter` |
| Source | Yale University Collections / LUX |
| Official data surface | LUX Linked Art JSON-LD records at `https://lux.collections.yale.edu/data/...` |
| Discovery/search surface | LUX search and advanced-search API configuration |
| Image delivery | IIIF and source media roots exposed through LUX records |
| Governing decision | `DD-YALE-001` draft required before production activation |
| Schema standard | `yale_lux_linked_art_v1` |
| Rights policy | `yale_lux_rights_matrix_v1` |
| Reuse target | Reuse `workers.shared_media_adapter` write, technical, rights URI, and replay infrastructure |

## Mission

Assess Yale as a candidate direct content institution and define the minimum adapter
contract for a first production path.

Yale is not a single homogeneous museum API. LUX is Yale's cross-collection discovery
layer for cultural heritage collections, backed by Linked Art JSON-LD records and
media records from several Yale units. The v1 adapter should therefore treat LUX as the
canonical discovery and metadata surface, but restrict writes to records with explicit
machine-readable rights and resolvable visual media.

## Official Inputs Verified

Live checks completed on 2026-06-10:

| Surface | Evidence | Adapter implication |
|---|---|---|
| LUX portal | `https://lux.collections.yale.edu/` identifies the service as "LUX: Yale Collections Discovery" and describes it as Yale University's cultural heritage collection search portal. | Source slug should be `yale_lux`, not a single museum unit. |
| Environment config | `https://lux.collections.yale.edu/env` exposes `dataApiBaseUrl` as `https://lux.collections.yale.edu/` and `cmsApiBaseUrl` as `https://lux-cms.collections.yale.edu/jsonapi/`. | Use the public LUX host as the data API root. CMS pages are documentation only, not ingest authority. |
| Data URI pattern | LUX advanced-search config describes record IDs as starting with `https://lux.collections.yale.edu/data/` followed by a URI path containing a UUID. | Client must fetch concrete `/data/{entity}/{uuid}` URIs, not `/view/...` routes. |
| Linked Art profile | The app emits `application/ld+json; profile='https://linked.art/ns/v1/linked-art.json'` links for entity pages. | Normalization should parse Linked Art JSON-LD directly. |
| Public-domain filter | Advanced-search config exposes `work.isPublicDomain`, with help text stating it applies to Yale University Art Gallery and Yale Center for British Art collections at this time. | Production rights allow path must be limited to explicit PD/Open Access evidence, initially YUAG/YCBA. |
| Digital media filters | Advanced-search config exposes `hasDigitalImage` and `isOnline` for objects, works, sets, agents, places, and concepts. | Discovery can seed visual candidates before per-record media validation. |
| Media roots | LUX frontend bundle references `ycba-lux.s3.amazonaws.com`, `images.peabody.yale.edu`, `media.art.yale.edu`, `linked-art.library.yale.edu`, `data.paul-mellon-centre.ac.uk`, and `paperbase.xyz`. | Media delivery varies by holding unit; adapter must not assume one IIIF template. |
| IIIF manifest support | LUX object views call a manifest ID when present and use source image fallback otherwise. | Store source IIIF manifest URL when exposed; fallback direct image only after rights pass. |

## Engineering Assessment

Yale has high strategic value and good standards alignment, but the adapter is more
complex than a single-museum REST API because LUX aggregates multiple Yale repositories
under one Linked Art model.

Estimated implementation split for a v1 still-visual adapter:

| Area | Shared adapter reuse | New code | Complexity |
|---|---:|---:|---|
| M36 write path | 90% | 10% | Low |
| Technical metadata | 75% | 25% | Low-Medium |
| Replay/compliance tests | 80% | 20% | Low |
| Client/data retrieval | 55% | 45% | Medium |
| Rights classification | 50% | 50% | Medium |
| Linked Art normalization | 45% | 55% | Medium-High |
| IIIF/image delivery | 65% | 35% | Medium |
| Source-specific evidence fields | 45% | 55% | Medium |
| Overall v1 adapter | 65% | 35% | Medium |

Engineering ROI: high, but not first among current next candidates if the goal is the
fastest new adapter. Yale should follow Trove/NHM/NARA only if the immediate priority is
high-quality art and manuscript media with strong Linked Art semantics. If the priority is
geographic gap closure, Trove and NHM remain better next candidates.

## Complexity Ratings

| Dimension | Rating | Reason |
|---|---|---|
| Rights complexity | Medium | Yale has an official Open Access posture, but LUX public-domain search help currently scopes `isPublicDomain` to YUAG and YCBA. Other Yale units require unit-specific evidence before commercial reuse. |
| Metadata complexity | Medium-High | LUX uses Linked Art JSON-LD with entity graphs for objects, works, agents, places, sets, events, and concepts. This is semantically strong but deeper than flat museum JSON. |
| Image complexity | Medium | IIIF manifests/images appear when available, but source media roots differ by unit. The adapter needs manifest detection plus direct-image fallback. |
| Store complexity | Low | Existing shared M36 write path is sufficient once Yale rights and evidence fields are injected. |
| Governance complexity | Medium | Direct integration must distinguish LUX as discovery/metadata authority from each Yale holding unit's rights and media authority. |

## Recommendation

Proceed to Discovery Report, not immediate production build.

Yale is a strong candidate for a later art/manuscript expansion sprint. It should not
displace Trove, NHM London, or NARA as the next adapter if the present roadmap is focused
on geographic and natural-history coverage. The best Yale entry point is a narrow
YUAG/YCBA visual-media pilot using explicit public-domain/Open Access evidence.

## Reuse Boundary

`yale_adapter` must reuse:

| Shared module | Yale use |
|---|---|
| `workers.shared_media_adapter.contracts` | Normalized record shape and mandatory field warnings |
| `workers.shared_media_adapter.store` | M36 write path for accepted visual records |
| `workers.shared_media_adapter.technical` | Baseline image metadata, content hash, quality flags |
| `workers.shared_media_adapter.replay` | Replay DB connection, write-order checks, no-write assertions |
| `workers.shared_media_adapter.rights` | CC0/PDM/RightsStatements.org URI decisions when explicit URIs are present |

Yale-specific modules own:

- LUX `/data/{entity}/{uuid}` retrieval
- LUX search/advanced-search request construction
- Linked Art JSON-LD graph traversal
- work/object/digital-object relationship resolution
- IIIF manifest and image-service extraction
- source-unit detection
- Yale-specific rights policy and evidence capture
- media root fallback handling
- source-specific provenance fields

## V1 Production Scope

Include:

- Human-made objects and visual works with `hasDigitalImage == true`
- Records with explicit public-domain/Open Access evidence
- Initial allow path limited to Yale University Art Gallery and Yale Center for British
  Art unless DD-YALE-001 expands the rights matrix
- Still visual media: image, photography, poster, map, drawing, print, manuscript leaf,
  and single-canvas visual object records
- IIIF manifests or image services when exposed
- Direct image fallback only when rights and media source are explicit

Exclude/defer:

- Peabody and other Yale unit records without explicit commercial reuse evidence
- Books and archives needing ordered multi-canvas activation
- Audio, video, born-digital files, and datasets
- Records with only human-readable or ambiguous rights text
- Records whose only image is a thumbnail or unauthorised derivative

## Client Design

Create `workers/yale_adapter/`:

- `__init__.py`
- `config.py`
- `client.py`
- `linked_art.py`
- `rights.py`
- `normalize.py`
- `technical.py`
- `store.py`

Client requirements:

| Function | Responsibility |
|---|---|
| `fetch_env(http_client=None)` | Fetch `/env` and confirm `dataApiBaseUrl`. |
| `fetch_advanced_search_config(http_client=None)` | Fetch `/api/advanced-search-config` for supported search terms. |
| `fetch_data_uri(uri, http_client=None)` | Fetch one Linked Art JSON-LD record by concrete `/data/...` URI. |
| `fetch_hal_link(uri, http_client=None)` | Fetch LUX HAL relationship pages when a record exposes `_links`. |
| `search_objects_with_images(...)` | Query objects with `hasDigitalImage == true` and optional YUAG/YCBA filters. |
| `search_public_domain_works(...)` | Query works with `isPublicDomain == true`; do not treat this as global Yale PD evidence. |
| `resolve_object_work_graph(object_record)` | Fetch carried/shown works needed for rights and title metadata. |
| `extract_manifest_url(record)` | Return source IIIF manifest URL when present. |
| `extract_media_candidates(record)` | Return IIIF image service, image URL, thumbnails, and source media root evidence. |

The client must keep network retrieval separate from normalization. Parsed transport
envelopes and raw JSON must remain available for replay fixtures.

## Rights Matrix v1

Module: `workers/yale_adapter/rights.py`

Policy ID: `yale_lux_rights_matrix_v1`

Classification input:

- LUX object record
- related work record(s), when present
- digital object/media record(s), when present
- detected holding unit
- extracted rights URI/text
- IIIF manifest rights/license fields, when present

Rules:

| Rule | Condition | Outcome | `rights_basis` |
|---|---|---|---|
| YAL-R-1 | Missing object/work record | BLOCKED | `missing_lux_record` |
| YAL-R-2 | No digital image or no online media | BLOCKED | `missing_digital_media` |
| YAL-R-3 | Explicit non-commercial, restricted, in-copyright, or permission-required statement | BLOCKED | `restricted_rights` |
| YAL-R-4 | Rights field absent from object, work, digital object, and manifest | BLOCKED | `missing_rights_evidence` |
| YAL-R-5 | Recognized CC0, Public Domain Mark, or No Copyright URI | ALLOWED | `recognized_public_domain_uri` |
| YAL-R-6 | LUX public-domain signal is true and holding unit is YUAG or YCBA | ALLOWED | `yale_yuag_ycba_public_domain_signal` |
| YAL-R-7 | Yale Open Access text is present but source unit is not YUAG/YCBA | REVIEW_REQUIRED | `unit_specific_open_access_review` |
| YAL-R-8 | Rights text is public-domain-like but lacks a governed URI or LUX boolean evidence | REVIEW_REQUIRED | `unmapped_public_domain_text` |

Allowed output:

- `decision = ALLOWED`
- `rights_statement_uri = CC0_URI`, `PDM_URI`, or source URI if recognized
- `rights_status = "terminal"`
- `rights_policy_id = "yale_lux_rights_matrix_v1"`

There is no write path for `REVIEW_REQUIRED` in v1. Review candidates may be stored only
as discovery evidence until DD-YALE-001 authorizes a specific escalation path.

## Normalization Design

Module: `workers/yale_adapter/normalize.py`

Canonical mapping:

| Normalized field | LUX / Linked Art source | Rule |
|---|---|---|
| `record_id` | `/data/object/{uuid}` or `/data/work/{uuid}` | Prefer object UUID for physical/digital object writes. |
| `title` | primary name/title | Required; fallback to related work title. |
| `description` | notes, descriptions, exhibition text | Strip unsafe markup; preserve concise text. |
| `date` | production/creation/publication event timespan | Preserve display string; parse year only as optional evidence. |
| `creator` | production/creation carried_out_by agents | Join primary agents with `; `. |
| `subject_terms` | classified_as, about, materials, techniques | Flatten labels and IDs in stable order. |
| `provider` | holding unit / owning collection | Required. |
| `dataProvider` | Yale University / specific unit | Preserve both LUX and unit provenance. |
| `edm_type` | Linked Art entity type + classification | Map to image/map/photography/poster/book/deferred media. |
| `source_url` | LUX `/view/...` or source homepage | Prefer human LUX route; preserve source museum URL if present. |
| `representative_media_url` | IIIF image URL or direct source image | Required for shared write. |
| `iiif_manifest_url` | manifest field or viewer manifest ID | Optional but preferred. |
| `preview_urls` | thumbnails and lower-resolution images | Deduplicate; representative first. |
| `width_px` / `height_px` | IIIF `info.json` or image metadata | Required for activation when available. |
| `raw_payload_hash` | canonical JSON hash | Include all object/work/media records used. |
| `rights_decision` | Yale rights module | Mirror adapter rights decision. |
| `rights_allowed` | Yale rights module | Mirror adapter rights allowed flag. |

Yale evidence fields:

- `yale_lux_object_uri`
- `yale_lux_work_uri`
- `yale_lux_digital_object_uri`
- `yale_holding_unit`
- `yale_collection_uri`
- `yale_source_media_root`
- `yale_rights_text_raw`
- `yale_rights_uri`
- `yale_public_domain_signal`
- `yale_iiif_manifest_url`
- `yale_iiif_image_service`
- `linked_art_profile`

## IIIF and Image Delivery

Preferred path:

1. Fetch object/work record from LUX data URI.
2. Extract IIIF manifest URL if present.
3. Fetch manifest and verify license/rights plus canvas image service.
4. Extract Image API service and dimensions from `info.json`.
5. Build representative `full/full/0/default.jpg` or service-native equivalent.

Fallback path:

1. Use direct source image URL only after rights pass.
2. Preserve source media root and source unit evidence.
3. Mark `iiif_manifest_url` absent and `delivery_protocol = direct_image`.

Do not assume a single Yale IIIF URL template. LUX records may point to source-specific
media infrastructure.

## Store Design

Module: `workers/yale_adapter/store.py`

Reuse `workers.shared_media_adapter.store.write_normalized_record()`.

Runtime:

| Field | Value |
|---|---|
| `source_slug` | `yale_lux` |
| `schema_standard` | `yale_lux_linked_art_v1` |
| `rights_policy_id` | `yale_lux_rights_matrix_v1` |
| `workflow_record_id_key` | `yale_lux_object_uri` |
| `worker_id` | `yale_adapter:sprint3` |

Raw payload must include all fetched graph records:

```json
{
  "object": "<LUX object JSON-LD>",
  "works": ["<related work JSON-LD>"],
  "digital_objects": ["<digital object/media JSON-LD>"],
  "iiif_manifest": "<manifest JSON when fetched>",
  "advanced_search_config_version": "<hash or fetch timestamp>"
}
```

Shared-store prerequisite before Sprint 3:

- include `yale_lux` in non-terminal `worker_classified_status` remap rules
- inject Yale evidence fields into `build_rights_evidence()`
- allow `yale_lux_linked_art_v1` as a schema standard in source governance records

## Sprint Plan

### Sprint 1 — Connectivity and Fixtures

Deliverables:

- client functions for `/env`, `/api/advanced-search-config`, and concrete `/data/...`
  records
- fixtures for one YUAG object, one YCBA object, one non-YUAG/YCBA review candidate,
  and one no-image blocked record
- no DB writes

Exit criteria:

- all fixture fetches replay deterministically
- concrete LUX data URIs resolve
- public-domain and digital-image search terms are captured from advanced-search config

### Sprint 2 — Rights and Normalization

Deliverables:

- `rights.py` with YAL-R-1 through YAL-R-8
- `linked_art.py` graph traversal helpers
- `normalize.py` canonical mapping
- unit tests for allowed, review, and blocked paths

Exit criteria:

- absent rights never writes
- non-YUAG/YCBA Open Access-like text becomes `REVIEW_REQUIRED`
- YUAG/YCBA public-domain evidence can produce terminal allowed records

### Sprint 3 — M36 Write Integration

Deliverables:

- shared-store integration
- technical metadata integration
- replay tests covering write and no-write cases
- compliance verdict

Exit criteria:

- allowed fixture writes through all six M36 tables
- blocked/review fixtures produce zero writes
- rights evidence includes Yale source unit and exact evidence fields

## Acceptance Criteria

| ID | Criterion |
|---|---|
| YAL-AC-1 | Adapter fetches LUX `/env` and verifies the production data API base URL. |
| YAL-AC-2 | Adapter fetches advanced-search config and confirms `hasDigitalImage`, `isOnline`, and `work.isPublicDomain` terms. |
| YAL-AC-3 | Adapter fetches concrete LUX `/data/...` records and parses Linked Art JSON-LD without using `/view/...` HTML routes. |
| YAL-AC-4 | Adapter blocks absent, ambiguous, restricted, or non-commercial rights before shared write. |
| YAL-AC-5 | Adapter allows only explicit CC0/PDM/NoC URI records or YUAG/YCBA public-domain signal records. |
| YAL-AC-6 | Adapter extracts IIIF manifest/image service when available and records direct-image fallback evidence otherwise. |
| YAL-AC-7 | Adapter writes only still visual records in v1. |
| YAL-AC-8 | Replay fixtures prove allowed, review, blocked, and missing-media paths. |

## ROI Summary

| Question | Answer |
|---|---|
| Shared Adapter reuse % | 65% overall for v1 still-visual adapter |
| New code % | 35% overall; concentrated in Linked Art graph traversal, Yale rights, and LUX client logic |
| Rights complexity | Medium |
| Metadata complexity | Medium-High |
| Engineering ROI | High strategic ROI; medium near-term ROI |
| Recommended next action | Discovery Report and DD-YALE-001 draft, not immediate build unless art/manuscript depth is the next roadmap priority |

