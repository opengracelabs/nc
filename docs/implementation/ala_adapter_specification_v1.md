# ALA Adapter Specification v1

| Field | Value |
| --- | --- |
| Repository | `opengracelabs/nc` |
| Status | Engineering ROI assessment and adapter design |
| Adapter | `ala_adapter` |
| Source | Atlas of Living Australia |
| Official documentation | `https://docs.ala.org.au/` |
| API gateway | `https://api.ala.org.au` |
| Primary data surfaces | Occurrences / BioCache, Images, Metadata / Collectory, Common APIs |
| Bulk surface | Occurrence offline download |
| Schema standard | `ala_darwin_core_v1` |
| Rights policy | `ala_rights_matrix_v1` |
| GBIF posture | High compatibility; treat as GBIF/DwC evidence source, not primary commerce signal |
| Shared adapter target | `shared_media_adapter` for accepted image records only |

## Executive Decision

ALA is a strong evidence and biodiversity-context source, but a weaker direct media
adapter candidate than museum and library sources. Its core value is Darwin Core
occurrence, taxon, collection, and dataset metadata aligned with GBIF workflows. The v1
adapter should therefore be scoped as a governed occurrence-plus-image evidence adapter,
not a broad media ingestion adapter.

Proceed only if the first production goal is one of:

1. Biological anchor validation for Australian taxa and places.
2. Occurrence evidence enrichment for existing biological concepts.
3. Carefully filtered ALA-hosted image intake where license evidence is explicit and
   commercial reuse is allowed.

Do not use ALA occurrence counts as a commerce ranking signal. Existing NC governance
already treats GBIF-like occurrence frequency as a risk for popularity/frequency bias.

## Engineering ROI Assessment

| Area | Shared adapter reuse | New ALA code | Complexity | Notes |
| --- | ---: | ---: | --- | --- |
| M36 write path for accepted images | 85% | 15% | Low | Shared store can write accepted media once normalized. |
| Technical metadata | 75% | 25% | Low-Medium | ALA image derivatives are direct URLs, not IIIF. |
| Replay and compliance tests | 80% | 20% | Low | Existing fixture-driven adapter tests fit well. |
| Occurrence search/download client | 45% | 55% | Medium-High | BioCache query surface is broad and has many filters. |
| Image client | 60% | 40% | Medium | Image details and derivative endpoints are straightforward, but media provenance varies by data resource. |
| Metadata / Collectory client | 50% | 50% | Medium | Dataset, provider, license, attribution, GBIF fields require source-specific traversal. |
| Rights classification | 40% | 60% | High | ALA aggregates many providers and licenses; per-record and data-resource evidence must both pass. |
| Darwin Core normalization | 45% | 55% | Medium-High | DwC field coverage is strong but broader than current image adapters. |
| GBIF compatibility | 70% | 30% | Medium | DwC headers, GBIF registry keys, and GBIF-sharing metadata are strong reuse points. |
| Overall v1 adapter | 60% | 40% | Medium-High | High standards alignment, but lower media ROI and higher rights variability. |

**Shared adapter reuse:** 60%  
**New code:** 40%  
**Rights complexity:** High  
**Metadata complexity:** Medium-High  
**GBIF compatibility:** High

## Official Inputs Verified

Official ALA documentation reviewed:

- ALA API documentation hub at `https://docs.ala.org.au/`.
- API gateway root documented as `https://api.ala.org.au`.
- Documentation states most published read APIs do not require authentication, while
  protected, write, sensitive, private, or high-frequency common APIs require JWT or API
  key access.
- ALA documentation describes more than 100 million occurrence records and bulk downloads
  for offline use.
- Swagger initializer exposes OpenAPI specs for `images`, `occurrences`, `metadata`,
  `common`, `species`, `namematching`, and related services.
- Images OpenAPI exposes image details and derivatives such as original, thumbnail, and
  large image endpoints.
- Occurrences OpenAPI exposes BioCache search and asynchronous occurrence download,
  including Darwin Core header support.
- Metadata / Collectory OpenAPI exposes data resources, providers, license/citation
  fields, GBIF registry keys, and GBIF sharing indicators.
- Common OpenAPI exposes curated ALA APIs with API-key based access and name matching.

## Recommendation

Proceed to discovery/design, not immediate media production.

ALA should be classified as an identity/evidence adapter first and a media adapter
second. It is an excellent candidate for Australian biodiversity context, Darwin Core
evidence, and GBIF reconciliation. It is not the fastest high-yield direct image source
because rights are provider-dependent and the media surface is an aggregator image
service, not a single open-access collection.

Best v1:

- Build read-only occurrence, image, metadata, and GBIF-compatibility extraction.
- Add strict rights matrix before any M36 media write.
- Write only records with explicit accepted license evidence and usable image derivative.
- Store occurrence/DwC payloads as evidence for biological anchors where appropriate,
  not as public-facing collection assets by default.

## Reuse Boundary

Reuse from `shared_media_adapter`:

- M36 write path for accepted image records.
- Technical metadata envelope and image quality flags.
- Replay connection and M36 write-order assertions.
- Shared rights URI normalization for recognized Creative Commons and public-domain
  URI forms.
- Mandatory field warnings and normalized media contract shape.

ALA adapter owns:

- BioCache occurrence query construction.
- Asynchronous occurrence download request/status handling.
- Darwin Core field selection and normalization.
- Image service lookup and derivative URL construction.
- Metadata / Collectory data resource lookup.
- Provider, data resource, citation, and attribution extraction.
- GBIF registry key and shareability extraction.
- ALA Rights Matrix v1.
- Sensitive/generalized occurrence handling.
- API key/JWT optional transport configuration for protected endpoints.

## Proposed Files

```text
workers/ala_adapter/
  __init__.py
  config.py
  client.py
  rights.py
  normalize.py
  gbif.py
  technical.py
  store.py
```

## V1 Scope

### In Scope

- Public, non-sensitive occurrence records.
- Occurrence records with image evidence.
- ALA image details and image derivative URLs.
- Metadata / Collectory data resource records for rights, citation, provider, and GBIF
  fields.
- Darwin Core field export/download support.
- GBIF registry and shareability evidence.
- Still image media only where rights are explicit and allowed.

### Out of Scope

- Sensitive/private occurrence records.
- Occurrence records requiring authenticated sensitive-data access.
- Write/update APIs.
- ALA upload APIs.
- Raw occurrence count ranking for commerce.
- Audio/video media in v1.
- Records with missing, unknown, non-commercial, or provider-ambiguous rights.
- Records with only thumbnail images.

## Client Design

`config.py` should define:

- `SOURCE_SLUG = "ala"`
- `SCHEMA_STANDARD = "ala_darwin_core_v1"`
- `RIGHTS_POLICY_ID = "ala_rights_matrix_v1"`
- `ALA_API_BASE_URL = "https://api.ala.org.au"`
- `ALA_OCCURRENCES_BASE_PATH = "occurrences"`
- `ALA_IMAGES_BASE_PATH = "images"`
- `ALA_METADATA_BASE_PATH = "metadata"`
- optional `ALA_API_KEY`
- optional JWT settings for protected APIs
- request timeout and user agent

`client.py` should implement:

- `search_occurrences(...)`
- `fetch_occurrence(record_id)`
- `request_occurrence_download(...)`
- `fetch_image_details(image_id)`
- `build_image_derivative_url(image_id, derivative)`
- `fetch_data_resource(uid)`
- `fetch_data_provider(uid)`
- `fetch_collection(uid)`
- `fetch_indexed_fields(is_dwc=True)`
- `canonical_request_params(params)`

Transport rules:

- Use unauthenticated public reads whenever possible.
- Do not require API key for the default v1 replay/client tests.
- Support API key for Common APIs and higher-frequency endpoints as optional config.
- Never request sensitive/private records in v1.

## Rights Matrix v1

Module: `workers/ala_adapter/rights.py`

Policy ID: `ala_rights_matrix_v1`

| Condition | Decision | Basis |
| --- | --- | --- |
| Missing occurrence/image object | `BLOCKED` | `missing_object` |
| Missing image ID or derivative URL | `BLOCKED` | `missing_image` |
| Missing data resource metadata | `BLOCKED` | `missing_data_resource` |
| Missing license / rights fields | `BLOCKED` | `missing_rights_evidence` |
| CC0 URI | `ALLOWED` | `cc0` |
| CC BY URI | `ALLOWED` | `cc_by` |
| Public Domain Mark URI | `ALLOWED` | `public_domain_mark` |
| CC BY-SA URI | `REVIEW_REQUIRED` | `share_alike_review` |
| Non-commercial URI/text | `BLOCKED` | `non_commercial` |
| No-derivatives URI/text | `BLOCKED` | `no_derivatives` |
| In-copyright / permission / all-rights-reserved text | `BLOCKED` | `restricted_rights` |
| Unknown rights URI/text | `BLOCKED` | `unknown_rights_uri` |

V1 should not write `REVIEW_REQUIRED` records. The review classification can be retained
as discovery evidence only until governance authorizes an escalation path.

Rights evidence fields:

- `ala_occurrence_id`
- `ala_image_id`
- `ala_data_resource_uid`
- `ala_data_provider_uid`
- `ala_license`
- `ala_rights`
- `ala_rights_holder`
- `ala_citation`
- `ala_image_url`
- `ala_gbif_dataset_key`
- `ala_gbif_registry_key`

## Normalization Design

`normalize.py` should produce two shapes:

1. `normalize_occurrence_evidence(...)` for biological evidence records.
2. `normalize_media_record(...)` for records that pass image and rights gates.

Canonical media mapping:

| Normalized field | ALA source | Rule |
| --- | --- | --- |
| `record_id` | occurrence UUID / record ID | Prefer stable occurrence ID. |
| `title` | scientific name + image/data resource label | Required; deterministic fallback. |
| `description` | occurrence remarks / image metadata description | Optional, sanitized. |
| `date` | event date | Preserve display string. |
| `creator` | image creator / occurrence recordedBy | Prefer image creator. |
| `subject_terms` | scientific name, taxon rank, taxon ID, dataset terms | Deduplicate stable order. |
| `geographic_subjects` | state, locality, decimal lat/lon, country | Generalized only; avoid sensitive detail. |
| `rights_uri` | image license / data resource license | Required for media write. |
| `provider` | ALA / data provider | Required. |
| `dataProvider` | Collectory provider or data resource | Required. |
| `edm_type` | image / occurrence media type | `image` for v1 writes. |
| `source_url` | ALA occurrence or image page/API URL | Required. |
| `representative_media_url` | image derivative/original URL | Required and not thumbnail-only. |
| `preview_urls` | thumbnail and large derivative URLs | Deduplicate. |
| `raw_payload_hash` | occurrence + image + data resource payload | Required for replay. |

Darwin Core evidence fields:

- `dwc_occurrence_id`
- `dwc_taxon_id`
- `dwc_scientific_name`
- `dwc_event_date`
- `dwc_decimal_latitude`
- `dwc_decimal_longitude`
- `dwc_basis_of_record`
- `dwc_dataset_id`
- `dwc_institution_code`
- `dwc_collection_code`
- `dwc_catalog_number`

## GBIF Compatibility

ALA has high GBIF compatibility for three reasons:

1. Occurrence downloads can use Darwin Core headers.
2. Collectory data resources expose GBIF-related fields such as registry keys, GBIF DOI,
   GBIF dataset flags, and shareability indicators.
3. ALA has metadata workflows for GBIF synchronization and data-resource scanning.

GBIF compatibility rating: **High**.

Adapter rules:

- Preserve ALA occurrence IDs and DwC occurrence IDs separately when both exist.
- Preserve GBIF dataset/registry keys when exposed by Collectory metadata.
- Treat GBIF fields as reconciliation/evidence, not ownership or rights authority.
- Do not infer media rights from GBIF compatibility.
- Do not use occurrence counts as commercial opportunity rank signals.
- Prefer DwC terms for biological anchor evidence.

## Technical Metadata

`technical.py` should reuse `shared_media_adapter.technical`.

ALA-specific additions:

- `ala_occurrence_id`
- `ala_image_id`
- `ala_data_resource_uid`
- `ala_data_provider_uid`
- `ala_license`
- `ala_rights`
- `ala_rights_holder`
- `ala_image_url`
- `ala_gbif_dataset_key`
- `ala_gbif_registry_key`
- `dwc_occurrence_id`
- `dwc_taxon_id`
- `dwc_scientific_name`

No IIIF assumptions should be made in v1.

## Store Design

`store.py` should be a thin wrapper around `shared_media_adapter.store` for media writes.

Pre-write gates:

1. Rights decision must be `ALLOWED`.
2. Image evidence must include a usable original or large derivative URL.
3. Data resource metadata must be present.
4. Sensitive/private occurrence indicators must be absent.
5. Required ALA evidence fields must be populated.

Blocked records produce zero writes.

Write path for allowed image records:

- `source_item`
- `source_record`
- `media_file`
- `media_rights`
- `preservation_event`
- `media_technical_metadata`
- source item pin

Occurrence-only records should not enter M36 media writes in v1. They should be retained
only as discovery/evidence fixtures unless a separate biodiversity evidence substrate is
authorized.

## Sprint Plan

### Sprint 1

Create `__init__.py`, `config.py`, and `client.py`.

Deliver:

- Occurrence search request builder.
- Occurrence lookup.
- Occurrence download request builder.
- Image details lookup.
- Image derivative URL builder.
- Collectory data resource lookup.
- Indexed DwC field lookup.
- Unit and replay fixtures.
- No store writes.

### Sprint 2

Create `rights.py`, `normalize.py`, and `gbif.py`.

Deliver:

- ALA Rights Matrix v1.
- Darwin Core evidence extraction.
- GBIF compatibility evidence extraction.
- Image/media normalization.
- Occurrence-only evidence normalization.
- Unit and replay tests.
- No store writes.

### Sprint 3

Create `technical.py` and `store.py`.

Deliver:

- Reuse shared technical metadata.
- Reuse shared M36 store path for allowed image records.
- Add ALA evidence passthrough to media rights.
- Blocked records produce zero writes.
- Unit, compliance, and replay tests.

## Acceptance Criteria

- Adapter can parse public ALA occurrence, image, and data resource fixtures.
- Adapter can identify Darwin Core fields and preserve DwC evidence.
- Adapter can preserve GBIF dataset/registry evidence when available.
- Adapter blocks missing/unknown/non-commercial/no-derivatives rights.
- Adapter does not infer rights from ALA/GBIF presence.
- Adapter writes only image records with explicit allowed rights and usable image URL.
- Occurrence-only records produce zero M36 media writes.
- Full replay is deterministic.

## Final Recommendation

ALA should be pursued as a biodiversity evidence and GBIF-compatible standards adapter,
not as the next high-yield image ingestion source.

Estimated implementation split:

- Shared adapter reuse: 60%
- New ALA code: 40%
- Rights complexity: High
- Metadata complexity: Medium-High
- GBIF compatibility: High

