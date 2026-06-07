# Europeana Adapter Build Plan

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Role | Lead Platform Engineer |
| Status | Ready for implementation |
| Scope | Europeana EDM adapter into Universal Media Substrate / M36 |
| API key | Validated |
| Constraint | No architecture redesign |

## Mission

Implement the Europeana adapter using Europeana EDM, the Media Substrate Constitution, and M36.

The adapter maps eligible Europeana records into:

```text
Europeana EDM
  -> source_item
  -> source_record
  -> media_rights
  -> media_technical_metadata
```

The adapter must ingest only records whose rights statement is explicitly one of:

- CC0
- Public Domain Mark
- NoC-US

All other records are skipped or recorded as rejected candidates. They must not create
`source_item`, `media_rights`, or activation records.

## Governance Boundary

Europeana is an aggregation source, not the default source of record.

Implementation rules:

1. Store the Europeana EDM payload verbatim as an immutable `source_record`.
2. Map `edm:ProvidedCHO` to `source_item`.
3. Map `ore:Aggregation` to `source_record`.
4. Map `edm:WebResource` to file/media references when a public media URL is available.
5. Create `media_rights` only for allowlisted rights.
6. Create `media_technical_metadata` from EDM and media probe data.
7. Do not create or approve `activation_target` solely from Europeana aggregation.
8. Do not bypass provider/source-of-record confirmation when a provider record is available.

This build plan stops at substrate ingestion and technical normalization.

## Rights Allowlist

Normalize Europeana rights values to canonical URIs before filtering.

| Accepted label | Accepted URI pattern | NC rights status |
|---|---|---|
| CC0 | `http://creativecommons.org/publicdomain/zero/1.0/` or `https://creativecommons.org/publicdomain/zero/1.0/` | `verified_cc0` |
| Public Domain Mark | `http://creativecommons.org/publicdomain/mark/1.0/` or `https://creativecommons.org/publicdomain/mark/1.0/` | `verified_pd` |
| NoC-US | `http://rightsstatements.org/vocab/NoC-US/1.0/` or `https://rightsstatements.org/vocab/NoC-US/1.0/` | `verified_pd` |

Hard filter:

```text
if normalized_rights_uri not in allowlist:
  reject candidate
  do not create source_item
  do not create source_record unless operating in audit-only discovery mode
```

Recommended implementation posture:

- Production ingest mode: skip non-allowlisted records before substrate writes.
- Audit mode: optionally record rejected search candidates in an adapter-specific run log, not in
  `source_item`.

## Media Type Scope

M36 activation-ready media types:

- `image`
- `map`
- `photography`
- `poster`

Europeana may return books, audio, video, 3D, and datasets. These should be handled as follows:

| Europeana type / signal | M36 mapping | Build action |
|---|---|---|
| Still image/object image | `image` | Ingest if rights allow and technical metadata passes. |
| Map/cartographic subject | `map` | Ingest if rights allow and image/media URL exists. |
| Photo/photograph subject | `photography` | Ingest if rights allow and image/media URL exists. |
| Poster subject/type | `poster` | Ingest if rights allow and image/media URL exists. |
| Book/text object | `book` | Reject for activation; optional discovery-only candidate until Phase 2. |
| Audio | `audio` | Reject for substrate ingest until Phase 3. |
| Video/film | `film` | Reject for substrate ingest until Phase 3. |
| 3D | `3d` | Reject for substrate ingest until Phase 4. |
| Dataset | `dataset` | Reject for substrate ingest until Phase 4. |

## EDM to M36 Mapping

### `source_item`

One `source_item` per Europeana `edm:ProvidedCHO`.

| NC field | Europeana/EDM source | Rule |
|---|---|---|
| `external_source` | `europeana` | Constant. |
| `external_id` | Europeana record ID / `about` | Stable dedupe key. |
| `source_institution_id` | `dataProvider` or provider institution mapping | Prefer `dataProvider`; preserve `provider`. |
| `media_type_id` | Europeana `type`, `dc:type`, subjects, format | Normalize to active M36 type only. |
| `title` | `dc:title` / `title` | Required for ingest. |
| `description` | `dc:description` | Optional but warning if missing. |
| `creator` | `dc:creator` | Preserve as raw string unless authority-resolved elsewhere. |
| `date_display` | `dc:date`, `year` | Preserve raw display; do not infer rights from date here. |
| `source_url` | `edm:isShownAt` | Required provider/object page when available. |
| `representative_media_url` | `edm:isShownBy` or `edm:object` or preview | Prefer `isShownBy`, then object, then preview. |
| `status` | adapter lifecycle | `proposed` or `acquired` after source_record/media_rights creation per M36 rules. |

Do not create a new creator, place, or concept authority record from Europeana strings in this
adapter. Preserve strings in `source_record` and `media_technical_metadata`; separate authority
resolution can run later.

### `source_record`

One immutable `source_record` per fetched Europeana record payload.

| NC field | Value |
|---|---|
| `source_item_id` | Created/linked `source_item.id`. |
| `schema_standard` | `edm`. |
| `source_url` | Europeana record API URL and provider `edm:isShownAt` in normalized payload. |
| `raw_payload` | Full Europeana record response, verbatim. |
| `normalized_payload` | EDM crosswalk used by the adapter. |
| `raw_payload_hash` | SHA-256 of canonical JSON serialization. |
| `fetched_at` | Adapter fetch timestamp. |
| `source_record_status` | `active` unless superseded by refetch. |

Minimum-field warning behavior:

- Missing `dc:title`
- Missing `dc:description`
- Missing `dc:date`
- Missing `edm:rights`

Missing fields should create warning metadata and/or preservation/provenance warning events, but
the hard ingest gate is rights allowlist plus usable media/type constraints.

### `media_rights`

One current `media_rights` record per ingested `source_item`.

| NC field | Europeana source | Rule |
|---|---|---|
| `source_item_id` | Linked source item | Required. |
| `rights_status` | normalized `edm:rights` | `verified_cc0` for CC0; `verified_pd` for PDM/NoC-US. |
| `rights_statement_uri` | `edm:rights` | Store normalized canonical URI. |
| `rights_basis` | rights URI class | `cc0_statement`, `public_domain_mark`, or `noc_us_statement`. |
| `rights_evidence` | EDM rights, provider URL, Europeana record URL | JSONB evidence. |
| `verified_by` | adapter identity for automated allowlist verification | Use governed worker ID. |
| `verified_at` | ingest timestamp | Required. |
| `verification_method` | adapter rule | `europeana_rights_allowlist_v1`. |

Important:

- `verified_pd` here means the record passes the governed Europeana rights allowlist. It does not
  authorize commerce activation by itself.
- Activation remains blocked until source-of-record/provider confirmation or Director-approved
  Europeana-only strategy exists.

### `media_technical_metadata`

One current `media_technical_metadata` record per ingested `source_item`.

| Content key | Europeana/source | Rule |
|---|---|---|
| `media_type_id` | normalized type | Must be active M36 type for ingest. |
| `edm_type` | Europeana `type` | Preserve original. |
| `title` | `dc:title` | Required. |
| `description` | `dc:description` | Preserve if present. |
| `creator` | `dc:creator` | Preserve as list/string. |
| `date` | `dc:date` / `year` | Preserve raw. |
| `provider` | `provider` | Preserve. |
| `data_provider` | `dataProvider` | Preserve. |
| `country` | `country` | Preserve. |
| `language` | `language` | Preserve. |
| `subject_terms` | `dc:subject`, `concepts`, `places`, `agents` labels | Preserve as source terms. |
| `media_urls` | `edm:isShownBy`, `edm:object`, `edm:preview` | Preserve all candidates. |
| `width` / `height` | media probe or Europeana technical fields | Probe where possible. |
| `quality_flag` | derived | `below_minimum` if longest edge < 400px for still visual types. |
| `source_schema` | constant | `edm`. |

Europeana image baseline:

- For `image`, `map`, `photography`, and `poster`, evaluate a 400px minimum longest-edge baseline.
- Below-baseline records may still be preserved as substrate records if rights allow, but must be
  flagged and must not be auto-activated for commerce.

## Adapter Modules

Implement as small modules with deterministic boundaries:

| Module | Responsibility |
|---|---|
| `europeana_client` | Search/fetch records using validated API key. |
| `rights_normalizer` | Normalize and filter CC0/PDM/NoC-US rights URIs. |
| `edm_parser` | Extract ProvidedCHO, Aggregation, WebResource, metadata fields. |
| `media_type_classifier` | Map Europeana type/subjects/formats to M36 media type. |
| `source_item_writer` | Upsert/link source item by Europeana external ID. |
| `source_record_writer` | Insert immutable EDM source record snapshots. |
| `media_rights_writer` | Insert allowlisted rights records. |
| `technical_metadata_writer` | Insert technical metadata and quality flags. |
| `dedupe_checker` | Detect existing source item/source record by Europeana ID/provider URL/media URL. |
| `run_logger` | Record adapter run metrics and rejected rights counts. |

## Implementation Sequence

1. Confirm Europeana API key environment variable and client config.
2. Define canonical rights allowlist and URI normalizer.
3. Implement record fetch by Europeana record ID.
4. Implement search fetch with query, media type filters, and paging.
5. Implement EDM parser and normalized payload builder.
6. Implement hard rights filter before substrate writes.
7. Implement M36 media type classifier for active Phase 1 visual types.
8. Implement dedupe by Europeana record ID, provider page URL, and media URL.
9. Implement `source_item` writer.
10. Implement immutable `source_record` writer with `schema_standard = 'edm'`.
11. Implement `media_rights` writer.
12. Implement `media_technical_metadata` writer.
13. Add run summary output: fetched, skipped-rights, skipped-type, skipped-media, ingested,
    warnings.
14. Add fixtures for CC0, PDM, NoC-US, restricted, and missing-rights records.
15. Add tests for mapping, rights filtering, dedupe, immutable source record behavior, and warning
    generation.
16. Run dry-run mode against validated API key.
17. Run small ingest batch with explicit record IDs.
18. Verify database completeness:
    `source_item -> source_record -> media_rights -> media_technical_metadata`.

## Required Tests

### Rights Tests

| Case | Expected |
|---|---|
| CC0 URI | Ingest; `media_rights.rights_status = verified_cc0`. |
| Public Domain Mark URI | Ingest; `media_rights.rights_status = verified_pd`. |
| NoC-US URI | Ingest; `media_rights.rights_status = verified_pd`. |
| In Copyright | Reject before substrate writes. |
| No rights URI | Reject before substrate writes. |
| Unknown rights URI | Reject before substrate writes. |

### EDM Mapping Tests

| Case | Expected |
|---|---|
| Complete image EDM record | Creates all four target records. |
| Missing `dc:description` | Creates warning; still ingests if rights/type/media pass. |
| Missing `dc:title` | Reject or quarantine per implementation policy; do not create public candidate. |
| Multiple media URLs | Preserves all; selects best representative. |
| Provider URL present | Stored in normalized source record and rights evidence. |
| Provider URL missing | Ingest allowed only as aggregation record; activation remains blocked. |

### M36 Integrity Tests

| Case | Expected |
|---|---|
| Duplicate Europeana record ID | Does not create duplicate source item. |
| Refetched changed payload | Inserts new immutable source record; updates current FK only. |
| Changed rights from allowed to restricted | New rights record; source item becomes non-activation-eligible. |
| Below 400px image | `quality_flag = below_minimum`. |
| Non-Phase-1 media type | Skipped or recorded discovery-only; no active substrate ingest. |

## Dry-Run Output Contract

Dry-run should emit:

```json
{
  "run_id": "...",
  "mode": "dry_run",
  "records_fetched": 0,
  "records_allowed_by_rights": 0,
  "records_rejected_by_rights": 0,
  "records_rejected_by_type": 0,
  "records_rejected_by_media": 0,
  "records_warnings": 0,
  "would_create": {
    "source_item": 0,
    "source_record": 0,
    "media_rights": 0,
    "media_technical_metadata": 0
  }
}
```

## GO / NO-GO

GO for implementation when:

- Europeana API key is available in runtime config.
- M36 target tables exist.
- Rights allowlist tests pass.
- Adapter dry-run produces deterministic counts.
- Fixtures cover CC0, Public Domain Mark, NoC-US, restricted rights, missing rights, missing
  metadata, duplicate record, and changed payload.

NO-GO if:

- Any non-allowlisted rights record creates a `source_item`.
- The adapter creates activation targets from Europeana aggregation alone.
- Raw EDM payloads are not stored immutably.
- Source/provider URLs are discarded.
- Technical metadata lacks rights/type/media quality warnings.

## Ready-for-Implementation Summary

Build the adapter as a rights-first EDM normalizer:

```text
fetch Europeana record
  -> normalize rights
  -> hard allowlist filter
  -> classify active M36 media type
  -> dedupe
  -> source_item
  -> immutable source_record(schema_standard='edm')
  -> media_rights
  -> media_technical_metadata
```

The adapter is ready to implement as a substrate ingestion worker. It must not activate commerce
or publication outputs until separate source-of-record and activation governance is satisfied.
