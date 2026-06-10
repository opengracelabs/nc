# NHM Adapter Specification v1

| Field | Value |
| --- | --- |
| Repository | `opengracelabs/nc` |
| Status | Engineering ROI assessment and adapter design |
| Adapter | `nhm_adapter` |
| Source | Natural History Museum, London |
| Governing decision | `DD-NHM-001` |
| Official data surface | NHM Data Portal / CKAN API |
| Primary dataset | `collection-specimens` |
| Primary resource ID | `05ff2255-c38a-40c9-b657-4ccb55ab2feb` |
| Schema standard | `nhm_darwin_core_v1` |
| Rights policy | `nhm_rights_matrix_v1` |
| Image delivery | Direct Data Portal media URLs via `associatedMedia.identifier` |
| IIIF posture | Documented NHM capability; v1 must verify manifest derivation before using it |
| Shared adapter target | `shared_media_adapter` for accepted still-image records |

## Executive Decision

NHM is a strong medium-high ROI adapter candidate for natural-history specimen imagery.
The Data Portal exposes a machine-readable CKAN/DataStore surface, Darwin Core specimen
metadata, direct media URLs, per-media license evidence, dimensions, format, creator, and
rights-holder fields. This makes NHM more immediately writable than aggregator-style
biodiversity sources where media provenance is dispersed across many upstream providers.

Proceed with NHM under this ingestion model:

1. Use the official Data Portal CKAN API as the authoritative v1 source.
2. Harvest `collection-specimens` records with `associatedMedia` evidence.
3. Treat each associated still image as its own candidate media item.
4. Classify rights from the media object first, not the dataset license alone.
5. Write only records that pass NHM Rights Matrix v1.
6. Add IIIF lookup as a verified enhancement once manifest URL construction and
   Presentation API version are confirmed in Sprint 1.

Do not depend on browser image-viewer scraping, NHM Images, or Library and Archives
commercial picture-library surfaces for v1.

## Engineering ROI Assessment

| Area | Shared adapter reuse | New NHM code | Complexity | Notes |
| --- | ---: | ---: | --- | --- |
| M36 write path for accepted images | 85% | 15% | Low | Shared store can write accepted media once normalized. |
| Technical metadata | 80% | 20% | Low-Medium | Width, height, MIME format, and direct media URL are exposed on media entries. |
| Replay and compliance tests | 80% | 20% | Low | Existing fixture-driven adapter and blocked-record tests fit well. |
| CKAN package/DataStore client | 60% | 40% | Medium | New source class for NC, but simple HTTP JSON paging and package metadata. |
| Darwin Core normalization | 55% | 45% | Medium-High | Rich specimen fields, GBIF identifiers/issues, geospatial fields, and collection variation. |
| Associated media extraction | 65% | 35% | Medium | Media arrays can contain many images per specimen and need per-item evidence. |
| Rights classification | 55% | 45% | Medium | Dataset license, media license, rights holder, and package-level variation must be reconciled. |
| GBIF/DwC evidence | 65% | 35% | Medium | GBIF IDs and Darwin Core fields are strong evidence but should not become ranking signals. |
| IIIF integration | 35% | 65% | Medium-High | NHM IIIF is documented, but live v1 records must confirm manifest and service derivation. |
| Overall v1 adapter | 65% | 35% | Medium | High shared-store reuse; source-specific client, rights, and DwC/media normalization remain material. |

**Shared adapter reuse:** 65%  
**New code:** 35%  
**Rights complexity:** Medium  
**Metadata complexity:** Medium-High  
**IIIF support:** Documented but not a v1 dependency until Sprint 1 verifies manifest/service extraction.

## Official Inputs Verified

Official NHM surfaces used for this assessment:

- NHM Data Portal root: `https://data.nhm.ac.uk/`.
- CKAN API package metadata:
  `https://data.nhm.ac.uk/api/3/action/package_show?id=collection-specimens`.
- CKAN DataStore search:
  `https://data.nhm.ac.uk/api/3/action/datastore_search?resource_id=05ff2255-c38a-40c9-b657-4ccb55ab2feb`.
- Package search for image-bearing datasets:
  `https://data.nhm.ac.uk/api/3/action/package_search?q=image&rows=10`.
- Local source audit: `docs/decisions/DD-NHM-001_natural_history_museum_london_source_audit.md`.

Observed Data Portal facts:

- `collection-specimens` is a Darwin Core resource with active DataStore support.
- The resource advertises `_image_field: associatedMedia`.
- Sample DataStore responses expose Darwin Core specimen fields, `gbifID`, `gbifIssue`,
  and `associatedMediaCount`.
- Image-bearing records can expose many `associatedMedia` entries on one specimen.
- Media entries include `assetID`, `identifier`, `title`, `creator`, `type`,
  `license`, `rightsHolder`, `PixelXDimension`, `PixelYDimension`, and `format`.
- A sampled media record used `http://creativecommons.org/licenses/by/4.0/` and
  `The Trustees of the Natural History Museum, London` as rights holder.
- Package search shows license variation across NHM datasets, including `cc-zero`,
  `cc-by`, and `cc-by-sa`.
- Browser image-viewer pages were not a reliable machine-ingestion surface from this
  environment.

## Scope

### In Scope

- Public `collection-specimens` records.
- Darwin Core specimen metadata.
- Still-image media in `associatedMedia`.
- Direct media URLs from `associatedMedia.identifier`.
- Media-level rights evidence from `associatedMedia.license` and `rightsHolder`.
- GBIF IDs and issue flags as evidence fields.
- Optional IIIF manifest probing after Sprint 1 confirms exact URL and version behavior.

### Out of Scope

- NHM Images commercial picture-library records.
- Library and Archives commercial/non-commercial licensing surfaces.
- Browser image-viewer scraping.
- Records without associated media.
- Media without explicit license evidence.
- Unknown, non-commercial, no-derivatives, or all-rights-reserved media.
- Audio, video, Sketchfab, 3D, and non-still-image media in v1.
- Sensitive/private specimen records or restricted geodata workflows.
- Raw occurrence frequency as a commerce ranking signal.

## Reuse Boundary

Reuse from `shared_media_adapter`:

- M36 write path helpers for `source_item`, `source_record`, `media_file`,
  `media_rights`, `preservation_event`, `media_technical_metadata`, and source item
  pinning.
- Technical metadata envelope and image dimension/format handling.
- Shared rights URI normalization for Creative Commons and public-domain URI forms.
- Replay fixture conventions.
- Compliance test structure.
- Terminal rights semantics: `ALLOWED`, `BLOCKED`, and non-writing `REVIEW_REQUIRED`.

NHM adapter owns:

- CKAN package lookup.
- DataStore pagination and request canonicalization.
- Dataset/resource metadata validation.
- Darwin Core specimen normalization.
- Associated media parsing and one-specimen-many-media expansion.
- Per-media rights evidence extraction.
- NHM Rights Matrix v1.
- GBIF evidence capture.
- Optional IIIF manifest/service verification.

## Proposed Files

```text
workers/nhm_adapter/
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

- `SOURCE_SLUG = "nhm"`
- `SCHEMA_STANDARD = "nhm_darwin_core_v1"`
- `RIGHTS_POLICY_ID = "nhm_rights_matrix_v1"`
- `NHM_API_BASE_URL = "https://data.nhm.ac.uk/api/3"`
- `COLLECTION_SPECIMENS_PACKAGE_ID = "collection-specimens"`
- `COLLECTION_SPECIMENS_RESOURCE_ID = "05ff2255-c38a-40c9-b657-4ccb55ab2feb"`
- `REQUEST_TIMEOUT_SECONDS`
- `USER_AGENT`
- conservative page size and request delay settings

`client.py` should implement:

- `fetch_package(package_id)`
- `fetch_resource_page(resource_id, limit, offset, sort=None)`
- `fetch_record(resource_id, record_id)`
- `iter_records_with_media(resource_id, limit, start_offset=0)`
- `extract_associated_media(record)`
- `canonical_request_params(params)`
- `build_datastore_url(action, params)`

Transport rules:

- Use public unauthenticated reads.
- Use `datastore_search` for v1 replay tests.
- Avoid relying on SQL search for v1 because Cloudflare/browser controls can interfere
  with query-like traffic.
- Rate limit requests and cache package/resource metadata.
- Never fetch or write restricted records in v1.

## NHM Rights Matrix v1

Module: `workers/nhm_adapter/rights.py`

Policy ID: `nhm_rights_matrix_v1`

| Condition | Decision | Basis |
| --- | --- | --- |
| Missing specimen object | `BLOCKED` | `missing_object` |
| Missing associated media object | `BLOCKED` | `missing_media` |
| Missing media URL | `BLOCKED` | `missing_media_url` |
| Missing media license | `BLOCKED` | `missing_media_license` |
| CC0 URI | `ALLOWED` | `cc0` |
| CC BY URI | `ALLOWED` | `cc_by` |
| Public Domain Mark URI | `ALLOWED` | `public_domain_mark` |
| CC BY-SA URI | `REVIEW_REQUIRED` | `share_alike_review` |
| Non-commercial URI/text | `BLOCKED` | `non_commercial` |
| No-derivatives URI/text | `BLOCKED` | `no_derivatives` |
| All-rights-reserved or permission text | `BLOCKED` | `restricted_rights` |
| Unknown rights URI/text | `BLOCKED` | `unknown_rights_uri` |

V1 must not write `REVIEW_REQUIRED` records. Review classifications may be retained as
discovery evidence until governance authorizes an escalation path.

Rights evidence fields:

- `nhm_record_id`
- `nhm_occurrence_id`
- `nhm_catalog_number`
- `nhm_collection_code`
- `nhm_institution_code`
- `nhm_asset_id`
- `nhm_media_url`
- `nhm_media_license`
- `nhm_rights_holder`
- `nhm_media_creator`
- `nhm_package_license_id`
- `nhm_resource_id`
- `nhm_doi`
- `nhm_gbif_id`
- `nhm_gbif_issue`

## Normalization Design

`normalize.py` should expand each accepted specimen/media pair into a canonical adapter
object with:

- `source_slug`
- `source_record_id`
- `source_item_id`
- `source_record_uri`
- `title`
- `creator_display`
- `scientific_name`
- `catalog_number`
- `collection_code`
- `institution_code`
- `basis_of_record`
- `occurrence_id`
- `gbif_id`
- `gbif_issue`
- `rights_uri`
- `rights_holder`
- `media_url`
- `media_format`
- `media_width`
- `media_height`
- `raw_record`
- `raw_media`

Recommended identifiers:

- `source_record_id`: specimen `_id` when present, with `occurrenceID` fallback.
- `source_item_id`: media `assetID` when present, with media `identifier` hash fallback.
- M36 source item key: `nhm:{source_record_id}:{source_item_id}`.

Title preference:

1. Media `title`.
2. `scientificName` plus `catalogNumber`.
3. `scientificName`.
4. `catalogNumber`.
5. `source_item_id`.

Creator preference:

1. Media `creator`.
2. Darwin Core `recordedBy`.
3. NHM institutional fallback only as contributor/rights holder, not creator.

Rights preference:

1. Media `license`.
2. Record-level license fields if confirmed.
3. Dataset/package license only as fallback evidence; do not allow writes from fallback
   alone unless Sprint 1 proves there are no per-media overrides for the target surface.

## IIIF Design

NHM IIIF support is documented in the local source audit, including a v3 image server and
CKAN IIIF extension. The live DataStore payloads checked for this assessment exposed
direct media identifiers and dimensions but did not expose a ready-to-use manifest or
image-service field.

V1 posture:

- Direct media URLs are the default write path.
- IIIF manifest lookup is optional until Sprint 1 confirms exact manifest URL
  construction and Presentation API version.
- Do not derive a manifest URL silently during writes unless a replay fixture proves the
  pattern against live Data Portal records.

Sprint 1 IIIF verification should test:

- `resource_id`
- DataStore record `_id`
- media `assetID`
- manifest URL pattern documented in `DD-NHM-001`
- Presentation API version
- first canvas image service ID
- parity between `associatedMedia.identifier` and IIIF image service output

## Store Design

`store.py` should reuse `shared_media_adapter.store` and implement the full M36 write
path only for `ALLOWED` normalized media records:

1. `source_item`
2. `source_record`
3. `media_file`
4. `media_rights`
5. `preservation_event`
6. `media_technical_metadata`
7. `source_item` pin

Blocked and review-required records must perform zero writes. They should emit replayable
decision evidence only.

## Test Plan

Unit tests:

- CKAN package parsing.
- DataStore record parsing.
- Associated media extraction.
- One specimen with many media entries expands into many candidate media objects.
- Rights matrix decisions for CC0, CC BY, CC BY-SA, non-commercial, no-derivatives,
  missing license, and unknown URI.
- Normalization identifiers and evidence fields.
- Direct media technical metadata extraction.
- Optional IIIF manifest parser once Sprint 1 fixture exists.

Replay tests:

- Package metadata replay for `collection-specimens`.
- DataStore page replay with no media.
- DataStore page replay with many associated media entries.
- Allowed CC BY media record replay.
- Blocked missing-license media replay.
- Review-required CC BY-SA dataset/media replay if fixture is available.

Compliance tests:

- Blocked records perform zero writes.
- `REVIEW_REQUIRED` records perform zero writes.
- Allowed records write the full M36 path in order.
- Required NHM evidence fields are present on rights and source records.
- Source item pin is written only after all dependent writes succeed.

## Sprint Recommendation

Sprint 1 should build the read-only adapter:

- `__init__.py`
- `config.py`
- `client.py`
- package lookup
- DataStore pagination
- associated media extraction
- direct media URL extraction
- no store writes
- unit and replay fixtures

Sprint 2 should build governance:

- `rights.py`
- `normalize.py`
- NHM Rights Matrix v1
- evidence field completeness
- blocked/review-required replay tests

Sprint 3 should build writes:

- `technical.py`
- `store.py`
- shared technical/store reuse
- full M36 write path
- compliance tests proving blocked records produce zero writes

## Acceptance Criteria

NHM adapter v1 is ready for production consideration when:

- CKAN package/resource metadata is fetched and cached.
- Records with `associatedMedia` are extracted deterministically.
- Each media item receives an independent rights decision.
- CC BY media writes preserve attribution and rights-holder evidence.
- Missing/unknown/restricted rights produce zero writes.
- Darwin Core and GBIF evidence fields survive normalization.
- Direct media URL technical metadata is recorded.
- IIIF is either verified by fixture and implemented, or explicitly disabled without
  blocking direct media ingestion.
- Replay and compliance tests pass without network access.
