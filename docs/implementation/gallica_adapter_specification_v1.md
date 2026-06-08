# Gallica Adapter Specification v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Status | Connectivity audit and build plan only |
| Adapter | `gallica_adapter` |
| Source | Bibliotheque nationale de France / Gallica |
| Primary API surfaces | `OAIRecord`, `Pagination`, IIIF, OCR, audio, video |
| Standards | OAI-PMH, Dublin Core, Gallica Document API, IIIF Image/Presentation, ALTO OCR |
| Governance | MSC v1.2, Institution Coverage Audit v1, Standards Amendment SA-3 required |
| Reuse target | Maximize reuse of `workers/shared_media_adapter` for Phase 1 still visual media |

## Mission

Design `gallica_adapter` as a source-specific Gallica edge adapter that reuses the frozen
`shared_media_adapter` wherever the Gallica record can be represented as one current
visual media file with source metadata, rights evidence, and technical metadata.

Gallica has broader connectivity than the current shared adapter contract:

- `OAIRecord` supplies bibliographic metadata and technical media hints.
- `Pagination` supplies ordered page structure.
- IIIF supplies image delivery and document manifests.
- OCR supplies ALTO XML and plain text paths.
- Audio and video records expose time-based media files.

The v1 production path should therefore be narrow: still images, maps, illustrations,
photography, manuscript illuminations, and page crops that can map to one primary IIIF
image. Book/page/OCR, audio, and video should be discoverable and replayable in v1, but
not activated through the shared write path until the substrate has the corresponding
multi-file and time-based media gates.

## Connectivity Surfaces

| Surface | Gallica role | v1 adapter action | Shared reuse |
|---|---|---|---|
| `OAIRecord` | Bibliographic and technical metadata for one ARK | Normalize to shared media record | High |
| OAI-PMH harvest | Broad record discovery with resumption tokens | Reuse Rijksmuseum-style OAI client pattern | Medium |
| `Pagination` | Ordered pages/folios for books and periodicals | Build page manifest candidates; select page image for still-visual ingest | Medium |
| IIIF Image | Full-resolution image info and delivery | Primary retrieval path for Phase 1 visual media | High |
| IIIF Presentation | Document/page manifest | Store as optional source field; bridge to NC IIIF 3.0 later | Medium |
| OCR / ALTO | Page text, illustration boxes, captions | Discovery evidence only in v1 unless cropped image is selected | Low-Medium |
| Plain text | Whole-document or range text | Discovery/search evidence only | Low |
| Audio | MP3-like files referenced in `sounds` blocks | Detect and reject/defer as Phase 3 | Low |
| Video | Video files in video records | Detect and reject/defer as Phase 3 | Low |

## Reuse Estimate

### Recommended v1 Production Scope

Scope: still visual Gallica records and page-level visual extracts with resolvable IIIF
image URLs.

| Category | Reuse % | New code % | Complexity |
|---|---:|---:|---|
| API/write architecture | 70% | 30% | Medium |
| Metadata normalization | 55% | 45% | Medium |
| Rights handling | 45% | 55% | Medium-High |
| Asset retrieval | 65% | 35% | Medium |
| Replay strategy | 80% | 20% | Low-Medium |
| Source-specific fields | 40% | 60% | Medium |
| Overall v1 still-visual adapter | 65% | 35% | Medium |

### Full Gallica Connectivity Scope

Scope: still images, books/pages, OCR, audio, and video.

| Category | Reuse % | New code % | Complexity |
|---|---:|---:|---|
| Still visual media | 65% | 35% | Medium |
| Books and ordered pages | 45% | 55% | Medium-High |
| OCR and illustration extraction | 30% | 70% | High |
| Audio | 20% | 80% | High |
| Video | 15% | 85% | High |
| Overall full connectivity | 45% | 55% | High |

Conclusion: `shared_media_adapter` can carry most of the first production Gallica
still-visual adapter, but it cannot carry full Gallica coverage without new multi-file,
OCR, and time-based media support.

## Reuse Boundary

`gallica_adapter` must reuse these shared modules:

| Shared module | Gallica usage |
|---|---|
| `workers.shared_media_adapter.contracts` | Normalized record shape and mandatory field warnings |
| `workers.shared_media_adapter.store` | Only M36 write path for v1 still visual records |
| `workers.shared_media_adapter.technical` | Baseline visual technical metadata, quality flag, content hash |
| `workers.shared_media_adapter.replay` | Replay connection, write-order checks, no-write assertions |
| `workers.shared_media_adapter.rights` | Reuse only when Gallica rights normalize to CC0/PDM/NoC URI vocabulary |

Gallica-specific modules must own:

- Gallica Document API client calls
- OAI-PMH pagination/resumption handling
- XML parsing for `OAIRecord`, `Pagination`, OCR, audio, and video blocks
- IIIF URL derivation from ARK/page/crop coordinates
- Gallica rights phrase classification and provenance text capture
- multi-page/page-crop candidate selection
- audio/video deferral logic

## 1. API Client

Module: `workers/gallica_adapter/client.py`

Required endpoints:

| Function | Endpoint | Responsibility |
|---|---|---|
| `fetch_oai_record(ark)` | `/services/OAIRecord?ark={ark}` | Fetch one Gallica document record |
| `fetch_pagination(ark)` | `/services/Pagination?ark={ark}` | Fetch page/folio sequence |
| `fetch_iiif_info(ark, page)` | `/iiif/{ark}/f{page}/info.json` | Probe image dimensions and IIIF availability |
| `build_iiif_image_url(ark, page, region)` | `/iiif/{ark}/f{page}/{region}/full/0/native.jpg` | Build representative image/crop URL |
| `fetch_iiif_manifest(ark)` | `/iiif/{ark}/manifest.json` | Fetch source IIIF manifest when available |
| `fetch_ocr_alto(ark, page)` | `/RequestDigitalElement?O={id}&E=ALTO&Deb={page}` | Fetch page OCR evidence |
| `fetch_plain_text(ark, range)` | `/{ark}.texteBrut` or page range qualifier | Fetch document text evidence |

OAI-PMH harvest support:

- Use the Rijksmuseum OAI client shape as the implementation precedent.
- Support `Identify`, `ListMetadataFormats`, `ListSets`, `ListIdentifiers`,
  `ListRecords`, and `GetRecord`.
- Support `resumptionToken` exactly as OAI-PMH exposes it.
- Preserve deleted-record headers as audit events; do not write deleted records.
- Store `responseDate`, OAI identifier, set specs, and datestamp in raw payload.

The client must not normalize metadata. It returns raw XML or parsed transport envelopes
only. Normalization belongs in `normalize.py`.

## 2. Metadata Normalization

Module: `workers/gallica_adapter/normalize.py`

The normalizer maps a Gallica `OAIRecord` plus optional `Pagination` and IIIF info into
the shared normalized media record shape.

| Normalized field | Gallica source | Rule |
|---|---|---|
| `record_id` | ARK or OAI header identifier | Required; prefer canonical ARK without page suffix |
| `title` | `dc:title` / notice title | Required |
| `description` | `dc:description`, notice summary, OCR caption context | Warning if absent |
| `date` | `dc:date` / notice date | Preserve display value; parse year only as optional evidence |
| `creator` | `dc:creator` | Join repeated values with `; ` |
| `subject_terms` | `dc:subject`, `dc:coverage`, OCR illustration context | Flatten to stable ordered strings |
| `rights_uri` | Gallica rights normalization result | URI if possible; otherwise governed Gallica rights sentinel only after SA-3 |
| `provider` | `Bibliotheque nationale de France` | Holding/source institution |
| `dataProvider` | `Gallica` or collection partner when exposed | Preserve partner if record is not pure BnF |
| `edm_type` | `dc:type`, `setSpec`, media blocks | Map to image/map/photography/poster/book/audio/film |
| `source_url` | `https://gallica.bnf.fr/ark:/...` | Human source page |
| `representative_media_url` | IIIF image URL or selected page crop | Required for shared write |
| `preview_urls` | thumbnail/precalculated image/IIIF thumbnail | Deduplicated list |
| `width_px` / `height_px` | IIIF `info.json` | Required for activation; optional for initial review |
| `raw_payload_hash` | canonical raw payload hash | Include OAIRecord plus Pagination/IIIF evidence used |
| `rights_decision` | Gallica rights module | Mirror adapter rights decision |
| `rights_allowed` | Gallica rights module | Mirror adapter rights allowed flag |

Phase 1 media mapping:

| Gallica signal | M36 media type | v1 action |
|---|---|---|
| still image / estampe / photographie | `image` or `photography` | ingest if rights and IIIF pass |
| carte / plan | `map` | ingest if rights and IIIF pass |
| poster / affiche | `poster` | ingest if rights and IIIF pass |
| manuscript page or illumination crop | `image` | ingest selected crop/page only |
| printed book page illustration | `image` | ingest selected page/crop only; book remains provenance |
| full book / periodical issue | `book` | defer as first-class source item |
| OCR text only | none | evidence only |
| sound recording | `audio` | defer |
| video | `film` | defer |

## 3. Rights Handling

Module: `workers/gallica_adapter/rights.py`

Gallica rights are not as directly reusable as Europeana EDM URI rights. The shared
rights classifier can be reused only after Gallica rights text has been mapped to a
recognized URI or a governed source-specific decision.

Required v1 policy:

- If a Gallica record exposes a recognized CC0, PDM, or RightsStatements.org URI, pass it
  to `shared_media_adapter.rights.classify_rights()`.
- If a record exposes only Gallica conditions/provenance text, classify it with a
  Gallica-specific ruleset and write only REVIEW_REQUIRED candidates unless SA-3
  explicitly authorizes an allow path.
- Treat absent rights as rejected before shared write.
- Treat non-commercial, restricted, access-limited, or unclear reuse statements as
  BLOCKED before shared write.
- Preserve the exact Gallica notice/provenance text in normalized payload and rights
  evidence.

Minimum evidence fields:

| Field | Meaning |
|---|---|
| `gallica_rights_text_raw` | Exact source rights/conditions text |
| `gallica_notice_text` | Notice/provenance text required by SA-3 |
| `gallica_ark` | Source ARK |
| `bnf_response_date` | OAI response date when available |
| `metadata_license` | BnF metadata license evidence |
| `digital_content_terms_url` | Gallica content terms URL when present |
| `rights_signal_source` | `dc:rights`, notice field, IIIF metadata, or API terms |

Rights complexity: Medium-High. The current shared classifier is URI-first. Gallica v1
needs new source-specific text classification and should bias toward human review unless
the record has an explicit governed URI path.

## 4. Asset Retrieval Path

Module: `workers/gallica_adapter/assets.py`

Still visual path:

1. Use `OAIRecord` to identify the ARK, title, type, and source page.
2. Use `Pagination` when the selected asset is page-level.
3. Use IIIF `info.json` to confirm dimensions.
4. Use IIIF Image API to build the representative media URL.
5. Pass the normalized record to `shared_media_adapter.store.write_normalized_record()`.

Page crop path:

1. Use ALTO OCR `Illustration` boxes when a page illustration, map inset, or captioned
   region is the target.
2. Convert ALTO `HPOS`, `VPOS`, `WIDTH`, and `HEIGHT` to the IIIF region.
3. Build a crop URL with the IIIF Image API.
4. Store the parent ARK, page number, OCR block id, and crop coordinates as source-specific
   fields.

Book/OCR path:

- Do not create a first-class `book` source item in v1.
- Store OCR as discovery evidence only.
- Page-level visual extracts may be ingested as still visual records when rights,
  source page, and IIIF image quality pass.

Audio/video path:

- Detect `sounds` and video media blocks in `OAIRecord`.
- Preserve file URLs and track/page ordering in the raw payload.
- Reject/defer before shared write with reason `unsupported_time_based_media`.
- Do not call the shared store for audio/video in v1; the shared technical metadata and
  write path are visual/single-file oriented.

## 5. Replay Strategy

Replay must prove both reuse and deferral boundaries.

Required fixtures:

| Fixture | Expected result |
|---|---|
| `gallica_oairecord_image_pd.xml` | Normalizes and writes through shared store |
| `gallica_pagination_map_page.xml` | Selects page IIIF image and writes through shared store |
| `gallica_iiif_info_dimensions.json` | Produces width/height and `meets_minimum` quality flag |
| `gallica_ocr_illustration_alto.xml` | Builds deterministic IIIF crop candidate; no write unless selected |
| `gallica_missing_rights.xml` | Rejected before shared write |
| `gallica_restricted_rights.xml` | Rejected before shared write |
| `gallica_audio_oairecord.xml` | Deferred; `assert_no_writes()` |
| `gallica_video_oairecord.xml` | Deferred; `assert_no_writes()` |
| `gallica_oai_resumption.xml` | Parses next token deterministically |

Shared replay assertions:

- Use `ReplayConn`.
- Use `assert_m36_write_order()` for still visual records that reach shared write.
- Use `assert_no_writes()` for missing rights, restricted rights, audio, video, and
  unsupported full-book records.
- Use `assert_rights_evidence_contract(evidence, source="gallica")` where a URI path
  reaches the shared rights evidence builder.
- Assert `schema_standard == "gallica_api_profile_v1"` after SA-3.
- Assert IIIF dimensions produce stable technical content hashes.
- Assert ALTO crop coordinates produce stable IIIF region URLs.

Replay command target:

```text
pytest tests/unit/test_gallica_client.py \
       tests/unit/test_gallica_normalize.py \
       tests/unit/test_gallica_rights.py \
       tests/unit/test_gallica_assets.py \
       tests/replay/test_gallica_adapter_sprint1.py
```

## 6. Source-Specific Fields

Gallica-specific fields should live inside `source_record.normalized_payload` and rights
evidence extensions, not in new source-specific database tables.

| Field | Required before write? | Purpose |
|---|---:|---|
| `gallica_ark` | Yes | Canonical digital object identifier |
| `oai_identifier` | Yes | OAI-PMH provenance |
| `oai_datestamp` | Yes | Replay and change tracking |
| `oai_set_specs` | No | Type/theme filtering |
| `bnf_response_date` | Yes when OAI-PMH used | Required OAI provenance |
| `gallica_source_url` | Yes | Human source page |
| `iiif_manifest_url` | When available | Source IIIF document manifest |
| `iiif_image_service_url` | Yes for still visual write | Image service provenance |
| `pagination_pages` | For page-level assets | Page/folio sequence summary |
| `selected_page_num` | For page-level assets | Representative page |
| `ocr_alto_url` | For OCR-backed extracts | OCR evidence path |
| `ocr_illustration_id` | For crop extracts | ALTO block provenance |
| `iiif_region` | For crop extracts | Region coordinates |
| `gallica_rights_text_raw` | Yes | Exact source rights text |
| `gallica_notice_text` | When present | SA-3 provenance text |
| `audio_files` | Audio records only | Deferral evidence |
| `video_files` | Video records only | Deferral evidence |
| `deferred_reason` | Deferred records only | `book_pipeline_pending`, `unsupported_time_based_media`, etc. |

## Proposed Package Layout

```text
workers/gallica_adapter/
  __init__.py
  config.py
  client.py
  oai.py
  normalize.py
  rights.py
  media_type.py
  assets.py
  ocr.py
  technical.py
  store.py
  main.py
```

`store.py` should mirror the existing Europeana and Rijksmuseum shared-store pattern:

```text
parse OAIRecord/Pagination/IIIF evidence
normalize raw payload
derive Gallica runtime
call shared_media_adapter.store.write_normalized_record()
```

Runtime configuration:

| `StoreRuntime` field | Gallica value |
|---|---|
| `worker_id` | `gallica_adapter:v1` |
| `source_slug` | `gallica` |
| `schema_standard` | `gallica_api_profile_v1` after SA-3 |
| `technical_schema_version` | `gallica-technical-v1` |
| `validator_name` | `gallica_adapter.technical.validation_status` |
| `validator_version` | `v1` |
| `workflow_record_id_key` | `gallica_record_id` |
| `anchor_type` | `mixed`, with `geographic` for maps and place-first records |

## Complexity Assessment

| Dimension | Assessment |
|---|---|
| API connectivity | Medium: several endpoints, but stable XML/IIIF surfaces |
| OAI harvest | Medium: resumption tokens and deleted headers; pattern already exists |
| Metadata mapping | Medium: DC is simple but Gallica notice/type conventions are source-specific |
| Rights | Medium-High: Gallica text/conditions require governed source-specific rules |
| IIIF visual retrieval | Low-Medium: strong reuse of image delivery assumptions |
| Pagination | Medium: page-level records require ordered page state |
| OCR | High: ALTO parsing and crop extraction are new source intelligence |
| Audio/video | High: current shared adapter should defer, not ingest |
| Overall v1 still visual | Medium |
| Overall full Gallica | High |

## Implementation Gates

The adapter is ready for first production visual run only after:

1. Standards Amendment SA-3 ratifies `gallica_api_profile_v1`.
2. Gallica source registry entry exists.
3. OAIRecord, Pagination, IIIF info, and IIIF image fixtures replay deterministically.
4. Gallica rights text policy is ratified or limited to explicit URI records.
5. Audio/video fixtures prove deferral with zero shared writes.
6. OCR fixtures prove crop extraction without creating first-class book/OCR records.
7. Shared M36 write order remains unchanged for still visual records.

## Summary

For Gallica v1, reuse is high only if the production scope is disciplined.

- Still visual adapter: about 65% shared reuse, 35% new code, medium complexity.
- Full Gallica connectivity: about 45% shared reuse, 55% new code, high complexity.
- `shared_media_adapter` should remain the write-path authority for eligible visual
  assets.
- New Gallica code is required for OAIRecord/Pagination XML parsing, IIIF derivation,
  Gallica rights text, OCR/ALTO extraction, and audio/video deferral.

## External References

- BnF Gallica Document API: `https://api.bnf.fr/fr/api-document-de-gallica`
- BnF Gallica IIIF API: `https://api.bnf.fr/fr/api-iiif-de-recuperation-des-images-de-gallica`
- BnF Gallica OAI-PMH: `https://api.bnf.fr/fr/oai-num`
