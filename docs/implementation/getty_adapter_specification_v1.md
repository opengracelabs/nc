# Getty Adapter Specification v1

| Field | Value |
| --- | --- |
| Repository | `opengracelabs/nc` |
| Status | Engineering ROI assessment and adapter design |
| Adapter | `getty_adapter` |
| Source | J. Paul Getty Museum |
| Official content policy | Getty Open Content Program |
| Official data surface | Getty Museum Linked Open Data / Linked Art JSON-LD |
| Bulk harvest surface | ActivityStreams 2.0 ordered collection |
| Image delivery | IIIF Image API plus IIIF Presentation API v2 |
| Governing decision | `DD-GETTY-001` |
| Schema standard | `getty_linked_art_v1` |
| Rights policy | `getty_rights_matrix_v1` |
| Shared adapter target | `shared_media_adapter` |

## Executive Decision

Getty is a viable medium-ROI source if "bulk download surfaces only" includes Getty's official ActivityStreams bulk-harvest/change-feed surface. A flat static CSV or JSON dump was not confirmed in the official Getty surfaces reviewed for this assessment.

Proceed with Getty only under this ingestion model:

1. Traverse the official ActivityStreams ordered collection.
2. Resolve each activity object to its Linked Art JSON-LD record.
3. Accept only records that pass the Getty Rights Matrix v1.
4. Resolve IIIF manifest and image service evidence before any M36 write.

If policy requires a flat static bulk dump only, Getty should be deferred until Getty publishes such a dump or explicitly documents one.

## Engineering ROI Assessment

| Area | Shared adapter reuse | New Getty code | Complexity | Notes |
| --- | ---: | ---: | --- | --- |
| M36 write path | 90% | 10% | Low | Reuse `shared_media_adapter.store`; add Getty evidence fields and source slug mapping. |
| Technical metadata | 75% | 25% | Low-Medium | Reuse shared IIIF/media probing where possible; Getty needs IIIF v2 extraction. |
| Replay and compliance tests | 80% | 20% | Low | Existing adapter test shape is reusable with Getty fixtures. |
| ActivityStreams harvest client | 45% | 55% | Medium-High | Getty-specific paging, activity filtering, record URI extraction, and tombstone handling. |
| Linked Art record retrieval | 55% | 45% | Medium | Yale Linked Art patterns help, but Getty record shapes and IDs differ. |
| Rights classification | 55% | 45% | Medium | CC0 is simple; nested Linked Art rights evidence traversal is source-specific. |
| Linked Art normalization | 50% | 50% | Medium-High | Rich Linked Art graph, multiple identifiers, creators, dates, and representation paths. |
| IIIF manifest and service extraction | 70% | 30% | Medium | IIIF concepts reusable; Getty is primarily IIIF Presentation v2. |
| Source-specific evidence | 45% | 55% | Medium | Getty object URI, UUID, accession number, activity event, manifest, and service evidence. |
| Overall v1 adapter | 65% | 35% | Medium | Good shared-store reuse; client and normalization remain Getty-specific. |

**Shared adapter reuse:** 65%  
**New code:** 35%  
**Rights complexity:** Medium  
**Metadata complexity:** Medium-High

## Official Inputs Verified

Official Getty surfaces used for this assessment:

- Getty Open Content Program and FAQ.
- Getty Open Data and API documentation.
- Getty Museum collection Linked Art JSON-LD documentation shell.
- Getty Museum ActivityStreams ordered collection page 1.
- Getty IIIF image and presentation URLs present in collection records.

The official ActivityStreams endpoint returned an ActivityStreams JSON document with an ordered collection page, `next` paging, and ordered activity items. This confirms a bulk-harvest/change-feed path, not a flat static bulk-download file.

## Scope

### In Scope

- J. Paul Getty Museum collection records.
- Open Content records classified as CC0.
- Linked Art JSON-LD object records.
- ActivityStreams create/update harvesting.
- IIIF Presentation v2 manifest lookup.
- IIIF Image API service extraction.
- Still-image media records suitable for the M36 media pipeline.

### Out of Scope

- Getty Research Institute records.
- Non-CC0 records.
- Records missing rights evidence.
- Records missing IIIF manifest or image service evidence.
- Deletes, tombstones, or withdrawals as write records; these should be logged and skipped in v1.
- Time-based media and complex multi-canvas books as first-class media objects.

## Reuse Boundary

Reuse from `shared_media_adapter`:

- M36 write path helpers for `source_item`, `source_record`, `media_file`, `media_rights`, `preservation_event`, `media_technical_metadata`, and source item pinning.
- Technical metadata envelope and image service probing.
- Replay fixture conventions.
- Compliance test structure.
- Terminal rights classification semantics: `ALLOWED` and `BLOCKED`.

Getty adapter owns:

- ActivityStreams traversal.
- Activity item filtering and record URI extraction.
- Linked Art JSON-LD record fetch.
- Getty object ID, UUID, accession number, and collection page extraction.
- Recursive rights evidence extraction.
- Getty Rights Matrix v1.
- Linked Art object normalization.
- IIIF Presentation v2 manifest parsing.
- Getty-specific evidence field assembly.

## Proposed Files

```text
workers/getty_adapter/
  __init__.py
  config.py
  client.py
  rights.py
  normalize.py
  technical.py
  store.py
```

## Client Design

`config.py` should define:

- `SOURCE_SLUG = "getty"`
- `SCHEMA_STANDARD = "getty_linked_art_v1"`
- `RIGHTS_POLICY_ID = "getty_rights_matrix_v1"`
- `ACTIVITY_STREAM_START_URL`
- `REQUEST_TIMEOUT_SECONDS`
- `USER_AGENT`

`client.py` should implement:

- `fetch_activity_stream_page(page_or_url)`
- `next_activity_stream_page(page)`
- `extract_activity_record_uris(page, include_types=("Create", "Update"))`
- `fetch_linked_art_record(record_uri)`
- `fetch_iiif_manifest(manifest_uri)`
- `extract_manifest_url(record)`
- `extract_iiif_image_service(manifest)`

SPARQL or search endpoints may be useful for diagnostics, but they should not be the primary v1 ingestion path.

## Getty Rights Matrix v1

| Condition | Decision | Basis |
| --- | --- | --- |
| Missing object | `BLOCKED` | No source evidence. |
| Missing `subject_to` | `BLOCKED` | No machine-verifiable rights evidence. |
| CC0 URI | `ALLOWED` | Getty Open Content / CC0. |
| Unknown rights URI | `BLOCKED` | Not eligible for automatic open-content ingestion. |
| Non-CC0 URI | `BLOCKED` | Not eligible for v1. |

Rights extraction must recursively inspect Linked Art JSON-LD for:

- `subject_to[].id`
- `subject_to[].classified_as[].id`
- `referred_to_by[].subject_to[]`
- equivalent nested `@id` keys when present

Every decision should emit:

- `rights_status`
- `policy_id`
- `decision`
- `basis`
- `getty_rights_uri`
- `getty_object_uri`

Allowed records should use a terminal pending-verification status compatible with the shared M36 rights flow.

## Normalization Design

`normalize.py` should convert a Getty Linked Art object into a canonical adapter object with:

- `source_slug`
- `source_record_id`
- `source_record_uri`
- `title`
- `accession_number`
- `creator_display`
- `date_display`
- `classification`
- `collection_page_url`
- `rights_uri`
- `iiif_manifest`
- `iiif_image_service`
- `activity_stream_event_id`
- `raw_record`

Getty evidence fields:

- `getty_object_uri`
- `getty_object_uuid`
- `getty_accession_number`
- `getty_collection_page_url`
- `getty_rights_uri`
- `getty_iiif_manifest`
- `getty_image_service`
- `getty_activity_stream_event_id`

Normalization should prefer structured Linked Art fields over string parsing:

- Title from `identified_by` entries classified as title, with fallback to `_label`.
- Accession number from `identified_by` entries classified as accession number.
- Creator from `produced_by.carried_out_by`.
- Date from `produced_by.timespan` display fields.
- Classification from `classified_as` or object type fields.
- Human URL from equivalent page references when available.

## IIIF Design

Getty v1 should treat IIIF Presentation v2 as the default manifest shape.

Manifest extraction:

- Read manifest URI from Linked Art digital object references when present.
- Do not derive manifest URLs from object IDs unless an official field confirms the mapping.
- Fetch the manifest before store writes.

Image service extraction:

- Traverse `sequences[].canvases[].images[].resource.service`.
- Accept service `@id` or `id`.
- Require a concrete IIIF image service URL before M36 writes.
- Preserve the manifest URL and image service URL as evidence.

## Store Design

`store.py` should be a thin Getty wrapper around `shared_media_adapter.store`.

Write path:

1. Validate normalized object exists.
2. Evaluate Getty Rights Matrix v1.
3. Block record if decision is not `ALLOWED`.
4. Validate IIIF manifest and image service evidence.
5. Build shared media payload.
6. Write:
   - `source_item`
   - `source_record`
   - `media_file`
   - `media_rights`
   - `preservation_event`
   - `media_technical_metadata`
   - source item pin

Blocked records must produce zero writes.

Runtime source fields:

- `source_slug = "getty"`
- `schema_standard = "getty_linked_art_v1"`
- `rights_policy_id = "getty_rights_matrix_v1"`
- workflow key: `getty_object_uuid` when available, otherwise stable hash of `getty_object_uri`

## Test Plan

Unit tests:

- ActivityStreams page parsing.
- Next-page extraction.
- Activity item URI extraction.
- Linked Art manifest URL extraction.
- IIIF v2 image service extraction.
- CC0 allowed rights decision.
- Missing object blocked.
- Missing `subject_to` blocked.
- Unknown URI blocked.
- Normalization of title, accession number, creator, date, and evidence fields.

Replay tests:

- One CC0 Getty object with manifest and image service.
- One missing-rights object blocked.
- One unknown-rights object blocked.
- One activity item without resolvable object skipped.

Compliance tests:

- Allowed record creates the complete M36 write set.
- Blocked records create zero writes.
- Required Getty evidence appears in `media_rights`, `source_record`, and technical metadata payloads.
- Replay output is deterministic.

## Sprint Plan

### Sprint 1

Create `workers/getty_adapter/__init__.py`, `config.py`, and `client.py`.

Deliver:

- ActivityStreams page fetch and paging.
- Activity record URI extraction.
- Linked Art JSON-LD fetch.
- IIIF manifest fetch.
- IIIF v2 image service extraction.
- Unit and replay fixtures.
- No store writes.

### Sprint 2

Create `rights.py` and `normalize.py`.

Deliver:

- Getty Rights Matrix v1.
- Recursive rights URI extraction.
- Linked Art normalization.
- Getty evidence field assembly.
- Unit and replay tests.
- No store writes.

### Sprint 3

Create `technical.py` and `store.py`.

Deliver:

- Reuse `shared_media_adapter.technical`.
- Reuse `shared_media_adapter.store`.
- Full M36 write path.
- Blocked records produce zero writes.
- Unit, compliance, and replay tests.

## Acceptance Criteria

- Getty adapter accepts only CC0 Open Content records.
- Every accepted record has `getty_object_uri`, `getty_rights_uri`, `getty_iiif_manifest`, and `getty_image_service`.
- Missing or unknown rights evidence blocks ingestion.
- Missing IIIF evidence blocks ingestion.
- ActivityStreams traversal is deterministic under replay fixtures.
- Store writes reuse the shared M36 path.
- Blocked records produce zero writes.

## Final Recommendation

Getty should proceed after Yale if ActivityStreams is accepted as a bulk-harvest surface. The adapter has strong shared-store reuse and a manageable rights model, but the metadata path is more complex than static CSV-style sources because each harvested activity must resolve to rich Linked Art JSON-LD and IIIF v2 evidence.

Estimated implementation split:

- Shared adapter reuse: 65%
- New Getty code: 35%
- Rights complexity: Medium
- Metadata complexity: Medium-High

