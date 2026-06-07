# Europeana Adapter Specification v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Role | Lead Platform Engineer |
| Status | Build plan only — ready for implementation |
| Adapter | `europeana_adapter` |
| API key | Validated |
| Standards | Europeana EDM, Rights Statements WG vocabulary |
| Governance | Media Substrate Constitution v1.2, M36 Universal Media Substrate |
| Scope | First production adapter, Yellowstone-first |

## Mission

Build the first production Europeana adapter.

The adapter ingests rights-cleared Europeana EDM records into the Universal Media Substrate:

```text
Europeana EDM
  -> source_item
  -> source_record
  -> media_rights
  -> media_technical_metadata
  -> activation_target
```

The adapter is production-oriented, but it is still governed by the Europeana aggregator boundary:

- Europeana EDM may create substrate records.
- Europeana rights statements may satisfy the first rights-cleared filter.
- Europeana aggregation alone must not auto-approve activation or commerce.
- `activation_target` may be created only as a reviewable target after source item, rights, and
  technical metadata gates pass.
- Approved activation still requires governed review and, where available, provider/source-of-record
  confirmation.

## Ingest Eligibility

The adapter must only ingest rights-cleared assets.

Accepted rights statements:

| Rights class | Canonical URI | `media_rights.rights_status` | `rights_basis` |
|---|---|---|---|
| CC0 | `https://creativecommons.org/publicdomain/zero/1.0/` | `verified_cc0` | `cc0_statement` |
| Public Domain Mark | `https://creativecommons.org/publicdomain/mark/1.0/` | `verified_pd` | `public_domain_mark` |
| NoC-US | `https://rightsstatements.org/vocab/NoC-US/1.0/` | `verified_pd` | `noc_us_statement` |

Normalize `http` and `https` variants to the canonical `https` URI before writing.

Hard rejection:

- Missing rights.
- Unknown rights.
- In Copyright.
- Copyright Not Evaluated.
- Educational Use Permitted.
- Non-commercial only.
- Any Creative Commons license other than CC0.
- Any record whose media type maps to a non-active M36 type.
- Any record without a usable representative media URL for active visual media.

## M36 Media Scope

Production v1 is restricted to M36 active Phase 1 media:

| Europeana signal | M36 media type | v1 action |
|---|---|---|
| `IMAGE` / still visual object | `image` | ingest |
| cartographic subject/type | `map` | ingest |
| photograph/photo subject/type | `photography` | ingest |
| poster subject/type | `poster` | ingest |
| book/text | `book` | skip, Phase 2 |
| audio | `audio` / `audiobook` | skip, Phase 2/3 |
| video/film | `film` | skip, Phase 3 |
| 3D | `3d` | skip, Phase 4 |
| dataset | `dataset` | skip, Phase 4 |

## EDM Mapping

### `source_item`

`source_item` represents the Europeana `edm:ProvidedCHO`.

| Field group | Mapping rule |
|---|---|
| Identity | `source = 'europeana'`; external key = Europeana record ID / `about`. |
| Provider | Preserve `provider` and `dataProvider`; prefer `dataProvider` as source institution label. |
| Title | Required from `dc:title` / Europeana `title`. |
| Description | From `dc:description`; warning if absent. |
| Type | Classify to active M36 media type only. |
| Creator/date | Preserve raw `dc:creator`, `dc:date`, `year`; do not authority-create in this worker. |
| URLs | Store Europeana API URL, `edm:isShownAt`, `edm:isShownBy`, `edm:object`, previews. |
| Lifecycle | Start as `acquired` after source record + rights + technical metadata exist. Move to `rights_verified` / `activation_eligible` only through substrate worker gates. |

### `source_record`

`source_record` represents the Europeana `ore:Aggregation` and full EDM payload.

Required:

- `schema_standard = 'edm'`
- raw payload stored verbatim
- normalized EDM payload stored separately
- SHA-256 hash of canonical raw payload
- Europeana record URL
- provider object URL if present
- fetch timestamp
- adapter version

Constitution v1.2 warnings:

- Missing `dc:title`
- Missing `dc:description`
- Missing `dc:date`
- Missing `edm:rights`

Warnings must be visible before rights verification. Missing `edm:rights` also fails the ingest
rights gate.

### `media_rights`

Create one current rights record for each ingested source item.

Required evidence:

- normalized `edm:rights`
- raw rights value
- Europeana record URL
- provider page URL if present
- provider/dataProvider values
- adapter rule: `europeana_rights_allowlist_v1`
- API response hash

The adapter may set:

- `verified_cc0` for CC0
- `verified_pd` for Public Domain Mark / NoC-US

This is substrate rights clearance. It does not approve commerce activation.

### `media_technical_metadata`

Create one active technical metadata record for each ingested source item.

Required content:

- `source_schema = 'edm'`
- M36 `media_type_id`
- Europeana `type`
- title, description, creator, date
- provider and dataProvider
- country/language if present
- subject terms from `dc:subject`, concepts, agents, places
- all candidate media URLs
- selected representative media URL
- width/height if available or probeable
- MIME type if available or probeable
- Europeana quality baseline result

Image quality baseline:

- For Phase 1 visual media, longest edge must be evaluated against 400px.
- If longest edge is below 400px, set `quality_flag = 'below_minimum'`.
- This flag does not block substrate ingestion, but it blocks automatic commerce readiness.

### `activation_target`

Create an `activation_target` only when all are true:

1. `source_item` exists.
2. current `source_record` exists.
3. current `media_rights.rights_status IN ('verified_pd', 'verified_cc0')`.
4. current `media_technical_metadata` exists and validates for the active M36 media type.
5. media type is Phase 1 active.
6. representative media URL exists.
7. provider/source page exists, or the record is explicitly marked `provider_unavailable`.

Initial status:

- `proposed` / `pending_review` / equivalent existing lifecycle value.

Forbidden:

- Do not mark approved.
- Do not create downstream commerce records.
- Do not link to `illustration_opportunities` automatically.
- Do not activate if provider URL is missing unless Director-approved Europeana-only strategy
  exists.

Approval must pin:

- `source_record_id_at_approval`
- `media_rights_id_at_approval`
- `media_technical_metadata_id_at_approval`

## Worker Sequence

### Production Worker Chain

1. `europeana_search_worker`
   - Executes scoped Europeana API searches.
   - Writes run metrics and candidate IDs.

2. `europeana_record_fetch_worker`
   - Fetches full record payloads by Europeana record ID.
   - Computes raw payload hash.

3. `europeana_rights_filter_worker`
   - Normalizes rights.
   - Applies hard allowlist.
   - Rejects non-cleared records before substrate writes.

4. `europeana_edm_normalization_worker`
   - Builds normalized EDM payload.
   - Extracts ProvidedCHO, Aggregation, WebResource signals.
   - Records mandatory-field warnings.

5. `europeana_media_type_worker`
   - Maps EDM type/subjects/format to active M36 media type.
   - Rejects Phase 2–4 types.

6. `europeana_dedupe_worker`
   - Checks Europeana record ID, provider URL, media URL, title/date/provider tuple.
   - Routes to update/refetch path when existing `source_item` exists.

7. `europeana_source_item_worker`
   - Creates or updates current linkage on `source_item`.

8. `europeana_source_record_worker`
   - Inserts immutable `source_record`.
   - Updates `source_item.current_source_record_id` under M36 rules.

9. `europeana_media_rights_worker`
   - Inserts `media_rights`.
   - Updates `source_item.current_media_rights_id`.

10. `europeana_technical_metadata_worker`
    - Probes media if needed.
    - Inserts `media_technical_metadata`.
    - Updates `source_item.current_media_technical_metadata_id`.

11. `europeana_activation_target_worker`
    - Creates reviewable activation target only after M36 gates pass.
    - Does not approve activation.

12. `europeana_replay_audit_worker`
    - Verifies source_item -> source_record -> rights -> technical metadata -> activation target
      chain completeness.

## API Strategy

Use two modes:

### Search Mode

Purpose: discover candidate records.

Recommended initial parameters:

- query: Yellowstone scoped terms first
- media: image
- rights filters: CC0, Public Domain Mark, NoC-US where API supports filtering
- profile: rich enough to include rights, title, provider, dataProvider, media URLs
- page size: conservative fixed size
- cursor or pagination token stored per run

Search mode may over-return. The adapter must still apply local rights filtering.

### Record Mode

Purpose: fetch full payload for a specific Europeana record ID before substrate writes.

Rules:

- Never write substrate records from search result summaries alone.
- Always fetch full record payload.
- Hash and store full payload.
- Treat search results as candidates, not source records.

## Rate Limiting

Use conservative client-side throttling even if the API key allows higher throughput.

Recommended defaults:

| Setting | Value |
|---|---|
| max requests per second | 2 |
| max concurrent requests | 2 |
| page size | 50 |
| retry attempts | 3 |
| retry backoff | exponential: 1s, 2s, 4s plus jitter |
| 429 handling | pause worker queue for 60s, then resume |
| daily batch cap for v1 | 1,000 full records |
| Yellowstone pilot cap | 100 full records |

Persist:

- run ID
- query
- page/cursor
- request count
- response status counts
- retry count
- rate-limit pauses

## Replay Requirements

Every ingested record must be replayable.

Replay evidence:

| Evidence | Required |
|---|---|
| adapter version | yes |
| API endpoint | yes |
| query parameters | yes for search |
| Europeana record ID | yes |
| full raw payload | yes |
| raw payload hash | yes |
| normalized payload hash | yes |
| rights normalizer version | yes |
| media type classifier version | yes |
| technical metadata extractor version | yes |
| selected media URL | yes |
| provider URL | yes if present |
| source_item ID | yes |
| source_record ID | yes |
| media_rights ID | yes |
| media_technical_metadata ID | yes |
| activation_target ID | if created |

Replay tests:

1. Same raw payload produces same normalized payload.
2. Same rights URI produces same rights status.
3. Same EDM type/subjects produce same M36 media type.
4. Same technical metadata input produces same quality flag.
5. Refetch with changed payload creates a new `source_record`, not mutation.
6. Rights change from allowlisted to restricted blocks new activation eligibility.
7. Activation target pins exact rights/source/technical metadata IDs.

## Error Handling

| Error | Handling |
|---|---|
| API 401/403 | Stop run; mark `auth_failure`; do not retry endlessly. |
| API 429 | Pause queue; retry with backoff; preserve cursor. |
| API 5xx | Retry up to limit; mark failed after max attempts. |
| malformed JSON | Record fetch failure; no substrate write. |
| missing rights | Reject candidate; no substrate write. |
| disallowed rights | Reject candidate; no substrate write. |
| missing title | Quarantine candidate; no public/source item write. |
| missing description/date | Write warning if all hard gates pass. |
| unsupported media type | Reject candidate; no substrate write. |
| no media URL | Reject candidate; no substrate write. |
| media probe failure | Ingest with `technical_probe_status = failed` only if metadata otherwise sufficient; do not create activation target. |
| duplicate record | Route to refetch/update path; do not duplicate `source_item`. |
| database constraint failure | Roll back current record transaction; continue run after logging. |

Transaction rule:

- Each Europeana record is processed in its own transaction.
- Failed records must not poison the full batch.
- Partial substrate chains are not allowed. If any of the four core writes fail, roll back the
  record transaction.

## Rights Filtering

Rights filtering is the first hard gate after full record fetch.

Sequence:

```text
extract edm:rights
  -> normalize URI
  -> match allowlist
  -> assign NC rights status
  -> build rights evidence
  -> proceed to substrate writes
```

Never infer public-domain status from date, creator death date, provider text, country, or
Europeana snippets in this adapter. Those may be future advisory evidence, but not v1 rights
clearance.

## Yellowstone-First Implementation Path

Purpose:

- Prove production adapter behavior against a narrow, place-centered prototype path.
- Avoid broad Europeana ingestion before dedupe, provider confirmation, and activation review
  flows are proven.

Search targets:

```text
Yellowstone
Yellowstone National Park
Old Faithful
Grand Canyon of the Yellowstone
Hayden Yellowstone
Yellowstone map
Yellowstone photograph
```

Allowed v1 result classes:

- images
- maps
- photography
- posters

Pilot caps:

- 100 full records fetched.
- 25 substrate ingests maximum.
- 5 activation targets maximum.

Yellowstone acceptance:

1. At least one eligible Yellowstone visual asset ingests into the full substrate chain.
2. At least one map or photograph candidate is rejected or accepted deterministically by rights.
3. All non-allowlisted rights records are rejected before substrate writes.
4. Activation targets are created only as reviewable targets.
5. No downstream commerce records are created.

## Week 1

Goal: deterministic client, rights filter, and EDM parser.

Exact order:

1. Confirm API key environment variable and runtime config name.
2. Create adapter run configuration for Yellowstone pilot.
3. Implement API client contract for search and record fetch.
4. Implement rate limiter and retry policy.
5. Implement rights URI normalizer.
6. Implement hard allowlist filter.
7. Implement EDM parser and normalized payload builder.
8. Implement media URL selection.
9. Implement Phase 1 media type classifier.
10. Build fixtures:
    - CC0
    - Public Domain Mark
    - NoC-US
    - In Copyright
    - missing rights
    - missing title
    - non-visual media
11. Add unit tests for rights, parsing, classifier, and media URL selection.
12. Run dry-run search against Yellowstone terms.

Exit criteria:

- Dry run fetches candidates and writes no substrate rows.
- Rights filter rejects all non-allowlisted rights.
- Full record fetch is required before any candidate is marked ingestable.

## Week 2

Goal: substrate writes for `source_item`, `source_record`, `media_rights`,
`media_technical_metadata`.

Exact order:

1. Implement dedupe checks.
2. Implement per-record transaction wrapper.
3. Implement `source_item` writer.
4. Implement immutable `source_record` writer.
5. Implement mandatory-field warnings.
6. Implement `media_rights` writer.
7. Implement technical metadata extractor.
8. Implement media probe and 400px quality baseline.
9. Implement `media_technical_metadata` writer.
10. Implement refetch behavior for changed payloads.
11. Add database integration tests for complete chain and rollback behavior.
12. Run Yellowstone ingest in limited batch mode.

Exit criteria:

- Every ingested record has complete chain:
  `source_item -> source_record -> media_rights -> media_technical_metadata`.
- Duplicate Europeana records do not create duplicate source items.
- Changed payload creates a new source record.
- Below-minimum images carry quality flag.

## Week 3

Goal: activation target proposal, replay audit, production readiness.

Exact order:

1. Implement activation eligibility check.
2. Implement `activation_target` proposal writer.
3. Ensure activation target pins current source/rights/technical metadata references.
4. Block activation target creation on missing provider URL unless Director-approved strategy flag
   is set.
5. Implement replay audit worker.
6. Implement run summary reporting.
7. Add replay tests for rights, source record immutability, classifier, and activation target pins.
8. Run Yellowstone pilot:
   - 100 full records max
   - 25 ingests max
   - 5 activation targets max
9. Produce pilot report with accepted, rejected, warning, and proposed activation counts.
10. Mark adapter ready for production batch review.

Exit criteria:

- Activation targets are proposed only, never approved.
- No downstream commerce/publication records are created.
- Replay audit can reconstruct every ingested record's decision path.
- Yellowstone pilot report is deterministic and reviewable.

## GO / NO-GO

GO for implementation:

- API key validated.
- Rights allowlist is explicit.
- EDM to M36 mapping is constitutionally defined.
- Yellowstone-first scope limits production risk.

NO-GO conditions:

- Non-allowlisted rights create substrate rows.
- Search summaries write substrate rows without full record fetch.
- `source_record.raw_payload` is mutated.
- `activation_target` is approved automatically.
- Europeana aggregation creates downstream commerce records.
- Replay cannot identify raw payload, rights normalizer, classifier, and target record IDs.

## Final Implementation Rule

`europeana_adapter` is a rights-first substrate ingestion worker.

It may create a complete M36 substrate chain and proposed activation targets. It may not approve
activation, commerce, catalog, publication, or provider routing outputs.
