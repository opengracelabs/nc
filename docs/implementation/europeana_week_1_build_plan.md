# Europeana Week 1 Build Plan

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Role | Lead Platform Engineer |
| Mission | Europeana Adapter Execution Plan |
| Scope | Week 1 implementation tasks only |
| Adapter | `europeana_adapter` |
| Status | Build plan — no redesign |

## Objective

Build the Week 1 foundation for `europeana_adapter`.

Week 1 must implement the code and tests needed to ingest only rights-cleared Europeana records
into the first four M36 substrate targets:

```text
Europeana EDM
  -> source_item
  -> source_record
  -> media_rights
  -> media_technical_metadata
```

Allowed rights only:

- CC0
- Public Domain Mark / PDM
- NoC-US

Week 1 does not implement `activation_target`, commerce, publication, provider routing, Neo4j,
pgvector, or frontend behavior.

## Files

Create the worker package:

```text
workers/europeana_adapter/
  __init__.py
  config.py
  client.py
  rights.py
  edm.py
  media_type.py
  technical.py
  store.py
  main.py
```

Create fixtures:

```text
tests/fixtures/europeana/
  cc0_image.json
  pdm_image.json
  noc_us_image.json
  in_copyright_image.json
  missing_rights_image.json
  missing_title_image.json
  unsupported_audio.json
```

Create tests:

```text
tests/unit/test_europeana_rights.py
tests/unit/test_europeana_edm.py
tests/unit/test_europeana_media_type.py
tests/unit/test_europeana_technical.py
tests/unit/test_europeana_store.py
tests/replay/test_europeana_adapter_week1.py
```

Create SQL migration only if M36 substrate tables are not already present:

```text
infrastructure/postgres/init/36_universal_media_substrate.sql
```

Do not create a separate Europeana-specific schema unless unavoidable. The adapter should write to
the M36 substrate tables, not to a parallel model.

## Workers

### `config.py`

Add settings:

```text
EUROPEANA_API_KEY
EUROPEANA_API_BASE_URL=https://api.europeana.eu/record/v2
EUROPEANA_REQUESTS_PER_SECOND=2
EUROPEANA_MAX_CONCURRENCY=2
EUROPEANA_FETCH_TIMEOUT_SECONDS=30
EUROPEANA_DRY_RUN=true
POSTGRES_DSN
```

Implementation tasks:

1. Use `pydantic_settings.BaseSettings`, matching existing worker config style.
2. Default dry-run to true.
3. Require `EUROPEANA_API_KEY` for non-dry-run.

### `client.py`

Responsibilities:

- search Europeana
- fetch full record by Europeana record ID
- apply timeout
- expose deterministic response object

Functions:

```python
async def search_records(query: str, *, rows: int, cursor: str | None = None) -> dict:
    ...

async def fetch_record(record_id: str) -> dict:
    ...
```

Rules:

- Search results are candidates only.
- Substrate writes must use full record fetch, never search summaries alone.
- Week 1 uses conservative paging: `rows=50`.

### `rights.py`

Responsibilities:

- normalize rights URI
- classify allowed rights
- reject everything else

Constants:

```python
CC0_URI = "https://creativecommons.org/publicdomain/zero/1.0/"
PDM_URI = "https://creativecommons.org/publicdomain/mark/1.0/"
NOC_US_URI = "https://rightsstatements.org/vocab/NoC-US/1.0/"
```

Functions:

```python
def normalize_rights_uri(value: str | None) -> str | None:
    ...

def classify_rights(value: str | None) -> dict:
    ...

def is_allowed_rights(value: str | None) -> bool:
    ...
```

Expected classification:

| Input | Output |
|---|---|
| CC0 URI | `rights_status = verified_cc0`, `rights_basis = cc0_statement` |
| Public Domain Mark URI | `rights_status = verified_pd`, `rights_basis = public_domain_mark` |
| NoC-US URI | `rights_status = verified_pd`, `rights_basis = noc_us_statement` |
| any other URI | reject |
| missing URI | reject |

### `edm.py`

Responsibilities:

- parse Europeana EDM payload
- extract required fields
- preserve raw and normalized payload separately
- produce warning list

Functions:

```python
def canonical_json_hash(payload: dict) -> str:
    ...

def normalize_edm_record(raw: dict) -> dict:
    ...

def mandatory_field_warnings(normalized: dict) -> list[str]:
    ...
```

Required normalized keys:

```text
europeana_record_id
provider
data_provider
title
description
date
creator
edm_rights
edm_type
dc_type
subjects
language
country
is_shown_at
is_shown_by
object_url
preview_urls
all_media_urls
raw_payload_hash
```

Mandatory warning fields:

- `dc:title`
- `dc:description`
- `dc:date`
- `edm:rights`

Missing `edm:rights` is both a warning and hard rejection.

### `media_type.py`

Responsibilities:

- map Europeana record type to active M36 Phase 1 media type
- reject pending media types

Function:

```python
def classify_media_type(normalized: dict) -> dict:
    ...
```

Allowed outputs:

- `image`
- `map`
- `photography`
- `poster`

Rejected outputs:

- `book`
- `ebook`
- `audiobook`
- `audio`
- `film`
- `3d`
- `dataset`
- `unknown`

Rules:

- Europeana `type = IMAGE` defaults to `image`.
- If title/type/subject contains cartographic/map signals, classify as `map`.
- If title/type/subject contains photograph/photo signals, classify as `photography`.
- If title/type/subject contains poster signals, classify as `poster`.
- No Phase 2-4 type can be written in Week 1.

### `technical.py`

Responsibilities:

- build `media_technical_metadata.content`
- select representative media URL
- flag image quality if dimensions are known

Functions:

```python
def select_representative_media_url(normalized: dict) -> str | None:
    ...

def build_technical_metadata(normalized: dict, media_type_id: str) -> dict:
    ...
```

Required content keys:

```text
source_schema = edm
media_type_id
edm_type
title
description
creator
date
provider
data_provider
country
language
subject_terms
media_urls
representative_media_url
quality_flag
mandatory_field_warnings
```

Week 1 quality flag:

- `below_minimum` only when dimensions are present and longest edge is less than 400px.
- `unknown_dimensions` when dimensions are absent.
- Do not fetch remote media binaries in Week 1.

### `store.py`

Responsibilities:

- write M36 substrate records transactionally
- reject non-cleared rights before writes
- avoid duplicate `source_item`

Functions:

```python
async def upsert_source_item(conn, normalized: dict, media_type_id: str) -> str:
    ...

async def insert_source_record(conn, source_item_id: str, raw: dict, normalized: dict) -> str:
    ...

async def insert_media_rights(conn, source_item_id: str, rights: dict, normalized: dict) -> str:
    ...

async def insert_media_technical_metadata(
    conn,
    source_item_id: str,
    media_type_id: str,
    content: dict,
) -> str:
    ...

async def ingest_record(conn, raw: dict) -> dict:
    ...
```

Transaction rule:

- `ingest_record` runs in one transaction.
- If `source_record`, `media_rights`, or `media_technical_metadata` fails, roll back all writes for
  that record.
- Non-allowlisted rights must return rejected status before any write.

Week 1 output:

```json
{
  "status": "ingested|rejected|quarantined",
  "reason": "...",
  "source_item_id": "...",
  "source_record_id": "...",
  "media_rights_id": "...",
  "media_technical_metadata_id": "..."
}
```

### `main.py`

Responsibilities:

- run dry-run search
- run explicit record ingest
- emit summary

CLI modes:

```text
python -m workers.europeana_adapter.main dry-run --query Yellowstone --limit 50
python -m workers.europeana_adapter.main ingest-record --record-id {europeana_record_id}
python -m workers.europeana_adapter.main ingest-fixture tests/fixtures/europeana/cc0_image.json
```

## Migrations

Week 1 migration requirement depends on M36 state.

### If M36 Exists

No migration.

Use existing M36 tables:

- `source_item`
- `source_record`
- `media_rights`
- `media_technical_metadata`
- `media_type_registry`

### If M36 Does Not Exist

Implement only the required M36 subset in:

```text
infrastructure/postgres/init/36_universal_media_substrate.sql
```

Minimum Week 1 tables:

- `media_type_registry`
- `source_item`
- `source_record`
- `media_rights`
- `media_technical_metadata`

Required constraints:

- `source_record.raw_payload` immutable by policy/test.
- `media_rights.rights_status IN ('verified_pd','verified_cc0','blocked')`.
- `media_rights.rights_statement_uri` not null.
- `media_technical_metadata.content` not empty.
- unique Europeana identity on source item, via source/external ID or equivalent.

Seed active M36 media types:

```text
image
map
photography
poster
```

Do not add activation target in Week 1.

## Tests

### Unit Tests

`tests/unit/test_europeana_rights.py`

- CC0 accepted.
- PDM accepted.
- NoC-US accepted.
- `http` variants normalize to `https`.
- In Copyright rejected.
- missing rights rejected.
- non-CC0 Creative Commons rejected.

`tests/unit/test_europeana_edm.py`

- complete EDM fixture normalizes expected fields.
- missing description emits warning.
- missing date emits warning.
- missing title quarantines or rejects per store policy.
- raw payload hash is deterministic.

`tests/unit/test_europeana_media_type.py`

- IMAGE defaults to `image`.
- map subject/title classifies as `map`.
- photograph subject/title classifies as `photography`.
- poster subject/title classifies as `poster`.
- audio/video/book are rejected in Week 1.

`tests/unit/test_europeana_technical.py`

- representative URL prefers `isShownBy`.
- falls back to `object`.
- falls back to preview.
- absent media URL rejects.
- dimensions below 400px produce `below_minimum`.
- absent dimensions produce `unknown_dimensions`.

`tests/unit/test_europeana_store.py`

- allowed fixture writes all four target records.
- disallowed rights writes no substrate rows.
- duplicate Europeana ID does not duplicate source item.
- failed technical metadata insert rolls back source item/source record/rights writes.

### Replay Test

`tests/replay/test_europeana_adapter_week1.py`

- same fixture produces same payload hash.
- same rights URI produces same rights status.
- same fixture produces same media type classification.
- refetch with changed payload creates a new source record, not mutation.
- output chain is complete:
  `source_item -> source_record -> media_rights -> media_technical_metadata`.

## Commands

Syntax checks:

```bash
python3 --version
bash -n infrastructure/postgres/init/36_universal_media_substrate.sql
```

Unit tests:

```bash
pytest tests/unit/test_europeana_rights.py
pytest tests/unit/test_europeana_edm.py
pytest tests/unit/test_europeana_media_type.py
pytest tests/unit/test_europeana_technical.py
pytest tests/unit/test_europeana_store.py
```

Replay test:

```bash
pytest tests/replay/test_europeana_adapter_week1.py
```

Full targeted run:

```bash
pytest tests/unit/test_europeana_rights.py tests/unit/test_europeana_edm.py tests/unit/test_europeana_media_type.py tests/unit/test_europeana_technical.py tests/unit/test_europeana_store.py tests/replay/test_europeana_adapter_week1.py
```

Dry-run command:

```bash
python -m workers.europeana_adapter.main dry-run --query Yellowstone --limit 50
```

Fixture ingest command:

```bash
python -m workers.europeana_adapter.main ingest-fixture tests/fixtures/europeana/cc0_image.json
```

Single-record ingest command:

```bash
python -m workers.europeana_adapter.main ingest-record --record-id {europeana_record_id}
```

Database checks:

```bash
make schema-check
make replay-test
```

## Week 1 Exact Task Order

1. Create `workers/europeana_adapter/` package.
2. Add `config.py`.
3. Add fixture directory and seven fixtures.
4. Implement `rights.py`.
5. Implement `test_europeana_rights.py`.
6. Implement `edm.py`.
7. Implement `test_europeana_edm.py`.
8. Implement `media_type.py`.
9. Implement `test_europeana_media_type.py`.
10. Implement `technical.py`.
11. Implement `test_europeana_technical.py`.
12. Inspect M36 table availability.
13. Add `36_universal_media_substrate.sql` only if required.
14. Implement `store.py`.
15. Implement `test_europeana_store.py`.
16. Implement `client.py`.
17. Implement `main.py`.
18. Implement `test_europeana_adapter_week1.py`.
19. Run all targeted tests.
20. Run dry-run Yellowstone search.
21. Ingest one CC0/PDM/NoC-US fixture into local DB.
22. Verify row chain in PostgreSQL.

## Week 1 Exit Criteria

Week 1 is complete only when:

- CC0, PDM, and NoC-US are accepted.
- All other rights are rejected before substrate writes.
- A valid fixture creates:
  - `source_item`
  - `source_record`
  - `media_rights`
  - `media_technical_metadata`
- Unsupported media types are rejected.
- Search summaries cannot write substrate records.
- Full record fetch or fixture payload is required before ingest.
- Targeted unit and replay tests pass.
- No activation target or commerce records are created.

## Non-Goals

Do not implement in Week 1:

- `activation_target`
- provider confirmation workflow
- downstream `illustration_opportunities` links
- Commerce scoring
- Catalog
- Publication
- Neo4j projection
- pgvector
- frontend routes
- broad Europeana batch ingest
