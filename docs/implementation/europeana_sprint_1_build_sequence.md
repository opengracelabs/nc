# Europeana Sprint 1 Build Sequence

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Role | Lead Platform Engineer |
| Mission | Europeana Adapter Sprint 1 |
| Status | Ready for coding |
| Basis | `docs/implementation/europeana_week_1_execution.md` |
| Constraint | No redesign |

## Sprint Goal

Start coding `europeana_adapter` today and land the first deterministic path:

```text
Europeana fixture / full record
  -> rights filter
  -> EDM normalization
  -> media type classification
  -> source_item
  -> source_record
  -> media_rights
  -> media_technical_metadata
```

Only these rights may pass:

- CC0
- Public Domain Mark / PDM
- NoC-US

No `activation_target`, commerce, publication, Neo4j, pgvector, or frontend work in Sprint 1.

## The First Six

### 1. First File To Create

Create package marker first:

```text
workers/europeana_adapter/__init__.py
```

Command:

```bash
mkdir -p workers/europeana_adapter
touch workers/europeana_adapter/__init__.py
```

Why first:

- Establishes importable package path.
- Allows tests to import `workers.europeana_adapter.*`.
- Creates no behavioral risk.

Immediately after:

```text
workers/europeana_adapter/rights.py
```

`rights.py` is the first behavioral file because rights are the hard gate.

### 2. First Test To Write

Write:

```text
tests/unit/test_europeana_rights.py
```

First test:

```python
from workers.europeana_adapter.rights import classify_rights


def test_cc0_is_allowed() -> None:
    result = classify_rights("http://creativecommons.org/publicdomain/zero/1.0/")
    assert result["allowed"] is True
    assert result["rights_status"] == "verified_cc0"
    assert result["rights_basis"] == "cc0_statement"
    assert result["rights_statement_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
```

Command:

```bash
pytest tests/unit/test_europeana_rights.py
```

Expected first run:

- Fails until `workers/europeana_adapter/rights.py` exists and implements `classify_rights`.

Completion gate:

- CC0 passes.
- PDM passes.
- NoC-US passes.
- In Copyright fails.
- Missing rights fails.

### 3. First API Call To Implement

Implement search dry-run first:

```text
workers/europeana_adapter/client.py
```

First function:

```python
async def search_records(query: str, *, rows: int = 50, cursor: str | None = None) -> dict:
    ...
```

First command:

```bash
python -m workers.europeana_adapter.main dry-run --query Yellowstone --limit 50
```

Rules:

- This call is candidate discovery only.
- It must not write database rows.
- It must not call `ingest_record`.
- It must not treat search summary payloads as `source_record`.

Implementation order for API:

1. `config.py`
2. `client.py`
3. `main.py` with only `dry-run`
4. dry-run command

Do not implement `fetch_record(record_id)` until dry-run search works.

### 4. First EDM Mapping To Implement

Implement title + rights + stable ID first:

```text
workers/europeana_adapter/edm.py
```

First mapping:

```text
Europeana record ID -> normalized["europeana_record_id"]
dc:title/title      -> normalized["title"]
edm:rights/rights   -> normalized["edm_rights"]
```

First fixture:

```text
tests/fixtures/europeana/cc0_image.json
```

First EDM test:

```python
import json
from pathlib import Path

from workers.europeana_adapter.edm import normalize_edm_record


def test_normalize_minimum_identity_title_rights() -> None:
    raw = json.loads(Path("tests/fixtures/europeana/cc0_image.json").read_text())
    normalized = normalize_edm_record(raw)
    assert normalized["europeana_record_id"]
    assert normalized["title"]
    assert normalized["edm_rights"] == "https://creativecommons.org/publicdomain/zero/1.0/"
```

Command:

```bash
pytest tests/unit/test_europeana_edm.py
```

Completion gate:

- The adapter can identify the record.
- The adapter can read the title.
- The adapter can extract rights for the hard gate.

Only after that, add:

- provider
- dataProvider
- date
- description
- creator
- media URLs
- subjects
- raw payload hash
- mandatory warnings

### 5. First Database Write Path

Implement `source_item` first, but only after rights and EDM tests pass.

File:

```text
workers/europeana_adapter/store.py
```

First write function:

```python
async def upsert_source_item(conn, normalized: dict, media_type_id: str) -> str:
    ...
```

First database write path:

```text
normalized EDM
  -> rights accepted
  -> media_type_id = image
  -> source_item upsert
```

Why `source_item` first:

- It is the parent for the Week 1 substrate chain.
- `source_record`, `media_rights`, and `media_technical_metadata` all need `source_item_id`.

Do not write `source_item` if:

- rights are missing
- rights are not CC0/PDM/NoC-US
- title is missing
- media type is unsupported

First store test:

```python
import json
from pathlib import Path

from workers.europeana_adapter.store import ingest_record


def load_fixture(name: str) -> dict:
    return json.loads(Path(f"tests/fixtures/europeana/{name}").read_text())


async def test_disallowed_rights_rejected_before_writes(fake_conn) -> None:
    result = await ingest_record(fake_conn, load_fixture("in_copyright_image.json"))
    assert result["status"] == "rejected"
    assert result["reason"] == "rights_not_allowlisted"
```

Completion gate:

- Rejected rights cause zero database calls.
- Allowed rights can reach `upsert_source_item`.

Then implement the remaining write path in this order:

1. `insert_source_record`
2. `insert_media_rights`
3. `insert_media_technical_metadata`
4. `ingest_record` transaction wrapper

### 6. First Replay Test

Write:

```text
tests/replay/test_europeana_adapter_week1.py
```

First replay test:

```python
import json
from pathlib import Path

from workers.europeana_adapter.edm import normalize_edm_record
from workers.europeana_adapter.rights import classify_rights


def load_fixture(name: str) -> dict:
    return json.loads(Path(f"tests/fixtures/europeana/{name}").read_text())


def test_rights_and_payload_hash_replay_are_stable() -> None:
    raw = load_fixture("cc0_image.json")
    first = normalize_edm_record(raw)
    second = normalize_edm_record(raw)

    assert first["raw_payload_hash"] == second["raw_payload_hash"]
    assert classify_rights(first["edm_rights"]) == classify_rights(second["edm_rights"])
```

Command:

```bash
pytest tests/replay/test_europeana_adapter_week1.py
```

Completion gate:

- Same raw fixture produces same payload hash.
- Same rights URI produces same rights classification.
- No live API dependency is required for replay.

## Exact Implementation Order

### Phase 0: Create Skeleton

Commands:

```bash
mkdir -p workers/europeana_adapter
mkdir -p tests/fixtures/europeana
touch workers/europeana_adapter/__init__.py
touch workers/europeana_adapter/rights.py
touch tests/unit/test_europeana_rights.py
```

Run:

```bash
pytest tests/unit/test_europeana_rights.py
```

Expected:

- Fail first, then pass after `rights.py`.

### Phase 1: Rights Gate

Implement:

```text
workers/europeana_adapter/rights.py
tests/unit/test_europeana_rights.py
```

Commands:

```bash
pytest tests/unit/test_europeana_rights.py
```

Gate:

- CC0/PDM/NoC-US accepted.
- Everything else rejected.

### Phase 2: Minimal EDM Mapping

Create:

```text
workers/europeana_adapter/edm.py
tests/fixtures/europeana/cc0_image.json
tests/unit/test_europeana_edm.py
```

Run:

```bash
pytest tests/unit/test_europeana_edm.py
```

Gate:

- record ID, title, rights, hash normalize.

### Phase 3: Phase 1 Media Type

Create:

```text
workers/europeana_adapter/media_type.py
tests/unit/test_europeana_media_type.py
```

Run:

```bash
pytest tests/unit/test_europeana_media_type.py
```

Gate:

- `IMAGE` -> `image`.
- `map` signal -> `map`.
- `photograph` signal -> `photography`.
- `poster` signal -> `poster`.
- audio/book/film rejected.

### Phase 4: Technical Metadata

Create:

```text
workers/europeana_adapter/technical.py
tests/unit/test_europeana_technical.py
```

Run:

```bash
pytest tests/unit/test_europeana_technical.py
```

Gate:

- representative media URL chosen.
- unknown dimensions flagged.
- below-400px dimensions flagged.

### Phase 5: Store Path

Create:

```text
workers/europeana_adapter/store.py
tests/unit/test_europeana_store.py
```

Run:

```bash
pytest tests/unit/test_europeana_store.py
```

Gate:

- rejected rights write nothing.
- accepted fixture can produce all four IDs.
- transaction wrapper exists.

### Phase 6: Replay

Create:

```text
tests/replay/test_europeana_adapter_week1.py
```

Run:

```bash
pytest tests/replay/test_europeana_adapter_week1.py
```

Gate:

- raw payload hash stable.
- rights classification stable.
- media type classification stable.

### Phase 7: API Dry Run

Create:

```text
workers/europeana_adapter/config.py
workers/europeana_adapter/client.py
workers/europeana_adapter/main.py
```

Run:

```bash
python -m workers.europeana_adapter.main dry-run --query Yellowstone --limit 50
```

Gate:

- Calls Europeana search endpoint.
- Prints summary.
- Writes no database rows.

## Today’s Coding Queue

Do this today, in order:

1. Create package directory.
2. Write `test_europeana_rights.py`.
3. Implement `rights.py`.
4. Write `cc0_image.json`.
5. Write `test_europeana_edm.py`.
6. Implement `edm.py`.
7. Write `test_europeana_media_type.py`.
8. Implement `media_type.py`.
9. Write `test_europeana_technical.py`.
10. Implement `technical.py`.
11. Write first `test_europeana_store.py` rejection test.
12. Implement first `store.py` rejection path.
13. Write first replay test.
14. Implement enough hash/rights replay to pass.
15. Add `config.py`, `client.py`, `main.py` dry-run.
16. Run targeted tests.
17. Run dry-run if API key is present.

## Stop Conditions

Stop and fix before moving on if:

- any non-allowlisted rights reaches a DB write path
- search result summaries are used as `source_record`
- media types outside Phase 1 become ingestable
- replay depends on live Europeana API
- `activation_target` appears in Sprint 1 code

## Sprint 1 Exit Criteria

Sprint 1 is ready for Week 2 when:

- `pytest tests/unit/test_europeana_rights.py` passes
- `pytest tests/unit/test_europeana_edm.py` passes
- `pytest tests/unit/test_europeana_media_type.py` passes
- `pytest tests/unit/test_europeana_technical.py` passes
- first store-path test passes
- first replay test passes
- dry-run command works or is blocked only by missing runtime API env
- no redesign or downstream activation code was added
