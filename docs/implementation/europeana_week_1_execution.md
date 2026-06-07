# Europeana Week 1 Execution

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Role | Lead Platform Engineer |
| Mission | Europeana Week 1 Execution |
| Scope | Exact files, commands, and worker skeletons |
| Status | Ready for coding |

## Execution Goal

Create the Week 1 `europeana_adapter` implementation skeleton and tests.

Week 1 writes only:

```text
source_item
source_record
media_rights
media_technical_metadata
```

Allowed rights only:

```text
CC0
Public Domain Mark / PDM
NoC-US
```

No redesign. No activation target. No commerce. No publication.

## Exact File Tree

Create:

```text
workers/europeana_adapter/__init__.py
workers/europeana_adapter/config.py
workers/europeana_adapter/client.py
workers/europeana_adapter/rights.py
workers/europeana_adapter/edm.py
workers/europeana_adapter/media_type.py
workers/europeana_adapter/technical.py
workers/europeana_adapter/store.py
workers/europeana_adapter/main.py

tests/fixtures/europeana/cc0_image.json
tests/fixtures/europeana/pdm_image.json
tests/fixtures/europeana/noc_us_image.json
tests/fixtures/europeana/in_copyright_image.json
tests/fixtures/europeana/missing_rights_image.json
tests/fixtures/europeana/missing_title_image.json
tests/fixtures/europeana/unsupported_audio.json

tests/unit/test_europeana_rights.py
tests/unit/test_europeana_edm.py
tests/unit/test_europeana_media_type.py
tests/unit/test_europeana_technical.py
tests/unit/test_europeana_store.py
tests/replay/test_europeana_adapter_week1.py
```

Conditional:

```text
infrastructure/postgres/init/36_universal_media_substrate.sql
```

Only create the SQL file if the M36 substrate tables are not already present.

## Exact Commands

Create directories:

```bash
mkdir -p workers/europeana_adapter
mkdir -p tests/fixtures/europeana
```

Create worker files:

```bash
touch workers/europeana_adapter/__init__.py
touch workers/europeana_adapter/config.py
touch workers/europeana_adapter/client.py
touch workers/europeana_adapter/rights.py
touch workers/europeana_adapter/edm.py
touch workers/europeana_adapter/media_type.py
touch workers/europeana_adapter/technical.py
touch workers/europeana_adapter/store.py
touch workers/europeana_adapter/main.py
```

Create fixture files:

```bash
touch tests/fixtures/europeana/cc0_image.json
touch tests/fixtures/europeana/pdm_image.json
touch tests/fixtures/europeana/noc_us_image.json
touch tests/fixtures/europeana/in_copyright_image.json
touch tests/fixtures/europeana/missing_rights_image.json
touch tests/fixtures/europeana/missing_title_image.json
touch tests/fixtures/europeana/unsupported_audio.json
```

Create test files:

```bash
touch tests/unit/test_europeana_rights.py
touch tests/unit/test_europeana_edm.py
touch tests/unit/test_europeana_media_type.py
touch tests/unit/test_europeana_technical.py
touch tests/unit/test_europeana_store.py
touch tests/replay/test_europeana_adapter_week1.py
```

Check whether M36 tables exist:

```bash
rg -n "CREATE TABLE source_item|CREATE TABLE source_record|CREATE TABLE media_rights|CREATE TABLE media_technical_metadata" infrastructure/postgres/init
```

Create Week 1 SQL only if missing:

```bash
touch infrastructure/postgres/init/36_universal_media_substrate.sql
```

Syntax checks:

```bash
python3 --version
bash -n infrastructure/postgres/init/36_universal_media_substrate.sql
```

Run tests:

```bash
pytest tests/unit/test_europeana_rights.py
pytest tests/unit/test_europeana_edm.py
pytest tests/unit/test_europeana_media_type.py
pytest tests/unit/test_europeana_technical.py
pytest tests/unit/test_europeana_store.py
pytest tests/replay/test_europeana_adapter_week1.py
```

Targeted combined run:

```bash
pytest tests/unit/test_europeana_rights.py tests/unit/test_europeana_edm.py tests/unit/test_europeana_media_type.py tests/unit/test_europeana_technical.py tests/unit/test_europeana_store.py tests/replay/test_europeana_adapter_week1.py
```

Dry-run:

```bash
python -m workers.europeana_adapter.main dry-run --query Yellowstone --limit 50
```

Fixture ingest:

```bash
python -m workers.europeana_adapter.main ingest-fixture tests/fixtures/europeana/cc0_image.json
```

Single record ingest:

```bash
python -m workers.europeana_adapter.main ingest-record --record-id RECORD_ID
```

Repository checks:

```bash
make schema-check
make replay-test
```

## Worker Skeletons

### `workers/europeana_adapter/config.py`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_dsn: str
    europeana_api_key: str = ""
    europeana_api_base_url: str = "https://api.europeana.eu/record/v2"
    europeana_requests_per_second: int = 2
    europeana_max_concurrency: int = 2
    europeana_fetch_timeout_seconds: int = 30
    europeana_dry_run: bool = True


settings = Settings()
```

### `workers/europeana_adapter/rights.py`

```python
from __future__ import annotations

from typing import Any

CC0_URI = "https://creativecommons.org/publicdomain/zero/1.0/"
PDM_URI = "https://creativecommons.org/publicdomain/mark/1.0/"
NOC_US_URI = "https://rightsstatements.org/vocab/NoC-US/1.0/"

_ALLOWED = {
    CC0_URI: {"rights_status": "verified_cc0", "rights_basis": "cc0_statement"},
    PDM_URI: {"rights_status": "verified_pd", "rights_basis": "public_domain_mark"},
    NOC_US_URI: {"rights_status": "verified_pd", "rights_basis": "noc_us_statement"},
}


def normalize_rights_uri(value: str | None) -> str | None:
    if not value:
        return None
    uri = value.strip()
    if not uri:
        return None
    uri = uri.replace("http://", "https://", 1)
    if not uri.endswith("/"):
        uri = f"{uri}/"
    return uri


def classify_rights(value: str | None) -> dict[str, Any]:
    uri = normalize_rights_uri(value)
    if uri not in _ALLOWED:
        return {
            "allowed": False,
            "rights_statement_uri": uri,
            "rights_status": "blocked",
            "rights_basis": "not_allowlisted",
        }
    return {
        "allowed": True,
        "rights_statement_uri": uri,
        **_ALLOWED[uri],
    }


def is_allowed_rights(value: str | None) -> bool:
    return bool(classify_rights(value)["allowed"])
```

### `workers/europeana_adapter/edm.py`

```python
from __future__ import annotations

import hashlib
import json
from typing import Any


def _first(value: Any) -> Any:
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def canonical_json_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def normalize_edm_record(raw: dict[str, Any]) -> dict[str, Any]:
    item = raw.get("object") or raw
    title = _first(item.get("title") or item.get("dcTitle"))
    description = _first(item.get("dcDescription") or item.get("description"))
    date = _first(item.get("year") or item.get("dcDate"))
    rights = _first(item.get("rights") or item.get("edmRights"))
    is_shown_by = _first(item.get("edmIsShownBy") or item.get("isShownBy"))
    is_shown_at = _first(item.get("edmIsShownAt") or item.get("isShownAt"))
    object_url = _first(item.get("edmObject") or item.get("object"))
    previews = _list(item.get("edmPreview") or item.get("preview"))
    media_urls = [url for url in [is_shown_by, object_url, *previews] if url]

    return {
        "europeana_record_id": item.get("id") or item.get("about") or raw.get("id"),
        "provider": item.get("provider"),
        "data_provider": item.get("dataProvider"),
        "title": title,
        "description": description,
        "date": date,
        "creator": item.get("dcCreator") or item.get("creator"),
        "edm_rights": rights,
        "edm_type": item.get("type"),
        "dc_type": item.get("dcType"),
        "subjects": _list(item.get("dcSubject") or item.get("subject")),
        "language": item.get("language"),
        "country": item.get("country"),
        "is_shown_at": is_shown_at,
        "is_shown_by": is_shown_by,
        "object_url": object_url,
        "preview_urls": previews,
        "all_media_urls": media_urls,
        "raw_payload_hash": canonical_json_hash(raw),
    }


def mandatory_field_warnings(normalized: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if not normalized.get("title"):
        warnings.append("missing_dc_title")
    if not normalized.get("description"):
        warnings.append("missing_dc_description")
    if not normalized.get("date"):
        warnings.append("missing_dc_date")
    if not normalized.get("edm_rights"):
        warnings.append("missing_edm_rights")
    return warnings
```

### `workers/europeana_adapter/media_type.py`

```python
from __future__ import annotations

from typing import Any

ACTIVE_TYPES = {"image", "map", "photography", "poster"}


def _haystack(normalized: dict[str, Any]) -> str:
    parts = [
        normalized.get("title"),
        normalized.get("description"),
        normalized.get("edm_type"),
        normalized.get("dc_type"),
        " ".join(str(v) for v in normalized.get("subjects") or []),
    ]
    return " ".join(str(p).lower() for p in parts if p)


def classify_media_type(normalized: dict[str, Any]) -> dict[str, Any]:
    text = _haystack(normalized)
    edm_type = str(normalized.get("edm_type") or "").upper()

    if any(token in text for token in ("audio", "sound", "recording")):
        return {"allowed": False, "media_type_id": "audio", "reason": "phase_3_pending"}
    if any(token in text for token in ("film", "video", "moving image")):
        return {"allowed": False, "media_type_id": "film", "reason": "phase_3_pending"}
    if any(token in text for token in ("book", "text", "manuscript")) and edm_type != "IMAGE":
        return {"allowed": False, "media_type_id": "book", "reason": "phase_2_pending"}
    if "map" in text or "cartographic" in text:
        return {"allowed": True, "media_type_id": "map"}
    if "poster" in text:
        return {"allowed": True, "media_type_id": "poster"}
    if "photo" in text or "photograph" in text:
        return {"allowed": True, "media_type_id": "photography"}
    if edm_type == "IMAGE":
        return {"allowed": True, "media_type_id": "image"}
    return {"allowed": False, "media_type_id": "unknown", "reason": "unsupported_media_type"}
```

### `workers/europeana_adapter/technical.py`

```python
from __future__ import annotations

from typing import Any

from .edm import mandatory_field_warnings


def select_representative_media_url(normalized: dict[str, Any]) -> str | None:
    return (
        normalized.get("is_shown_by")
        or normalized.get("object_url")
        or next(iter(normalized.get("preview_urls") or []), None)
    )


def build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    width = normalized.get("width")
    height = normalized.get("height")
    quality_flag = "unknown_dimensions"
    if isinstance(width, int) and isinstance(height, int):
        quality_flag = "below_minimum" if max(width, height) < 400 else "meets_minimum"

    return {
        "source_schema": "edm",
        "media_type_id": media_type_id,
        "edm_type": normalized.get("edm_type"),
        "title": normalized.get("title"),
        "description": normalized.get("description"),
        "creator": normalized.get("creator"),
        "date": normalized.get("date"),
        "provider": normalized.get("provider"),
        "data_provider": normalized.get("data_provider"),
        "country": normalized.get("country"),
        "language": normalized.get("language"),
        "subject_terms": normalized.get("subjects") or [],
        "media_urls": normalized.get("all_media_urls") or [],
        "representative_media_url": select_representative_media_url(normalized),
        "quality_flag": quality_flag,
        "mandatory_field_warnings": mandatory_field_warnings(normalized),
    }
```

### `workers/europeana_adapter/client.py`

```python
from __future__ import annotations

import httpx

from .config import settings


async def search_records(query: str, *, rows: int = 50, cursor: str | None = None) -> dict:
    params = {
        "wskey": settings.europeana_api_key,
        "query": query,
        "rows": rows,
    }
    if cursor:
        params["cursor"] = cursor
    async with httpx.AsyncClient(timeout=settings.europeana_fetch_timeout_seconds) as client:
        response = await client.get(f"{settings.europeana_api_base_url}/search.json", params=params)
        response.raise_for_status()
        return response.json()


async def fetch_record(record_id: str) -> dict:
    cleaned = record_id.strip("/")
    url = f"{settings.europeana_api_base_url}/{cleaned}.json"
    async with httpx.AsyncClient(timeout=settings.europeana_fetch_timeout_seconds) as client:
        response = await client.get(url, params={"wskey": settings.europeana_api_key})
        response.raise_for_status()
        return response.json()
```

### `workers/europeana_adapter/store.py`

```python
from __future__ import annotations

import json
from typing import Any

import asyncpg

from .edm import normalize_edm_record
from .media_type import classify_media_type
from .rights import classify_rights
from .technical import build_technical_metadata, select_representative_media_url

WORKER_ID = "europeana_adapter:v1-week1"


async def upsert_source_item(
    conn: asyncpg.Connection,
    normalized: dict[str, Any],
    media_type_id: str,
) -> str:
    row = await conn.fetchrow(
        """
        INSERT INTO source_item (
            external_source, external_id, media_type_id, title, source_url, status
        ) VALUES (
            'europeana', $1, $2, $3, $4, 'acquired'
        )
        ON CONFLICT (external_source, external_id)
        DO UPDATE SET
            media_type_id = EXCLUDED.media_type_id,
            title = EXCLUDED.title,
            source_url = EXCLUDED.source_url,
            updated_at = NOW()
        RETURNING id
        """,
        normalized["europeana_record_id"],
        media_type_id,
        normalized["title"],
        normalized.get("is_shown_at"),
    )
    return str(row["id"])


async def insert_source_record(
    conn: asyncpg.Connection,
    source_item_id: str,
    raw: dict[str, Any],
    normalized: dict[str, Any],
) -> str:
    row = await conn.fetchrow(
        """
        INSERT INTO source_record (
            source_item_id, schema_standard, source_url, raw_payload,
            normalized_payload, raw_payload_hash
        ) VALUES (
            $1, 'edm', $2, $3::jsonb, $4::jsonb, $5
        )
        RETURNING id
        """,
        source_item_id,
        normalized.get("is_shown_at"),
        json.dumps(raw, sort_keys=True),
        json.dumps(normalized, sort_keys=True),
        normalized["raw_payload_hash"],
    )
    return str(row["id"])


async def insert_media_rights(
    conn: asyncpg.Connection,
    source_item_id: str,
    rights: dict[str, Any],
    normalized: dict[str, Any],
) -> str:
    evidence = {
        "worker_id": WORKER_ID,
        "europeana_record_id": normalized.get("europeana_record_id"),
        "provider": normalized.get("provider"),
        "data_provider": normalized.get("data_provider"),
        "source_url": normalized.get("is_shown_at"),
        "raw_rights": normalized.get("edm_rights"),
    }
    row = await conn.fetchrow(
        """
        INSERT INTO media_rights (
            source_item_id, rights_status, rights_statement_uri,
            rights_basis, rights_evidence, verified_by, verified_at
        ) VALUES (
            $1, $2, $3, $4, $5::jsonb, $6, NOW()
        )
        RETURNING id
        """,
        source_item_id,
        rights["rights_status"],
        rights["rights_statement_uri"],
        rights["rights_basis"],
        json.dumps(evidence, sort_keys=True),
        WORKER_ID,
    )
    return str(row["id"])


async def insert_media_technical_metadata(
    conn: asyncpg.Connection,
    source_item_id: str,
    media_type_id: str,
    content: dict[str, Any],
) -> str:
    row = await conn.fetchrow(
        """
        INSERT INTO media_technical_metadata (
            source_item_id, media_type_id, content, schema_version, generated_by
        ) VALUES (
            $1, $2, $3::jsonb, 'europeana_edm_week1_v1', $4
        )
        RETURNING id
        """,
        source_item_id,
        media_type_id,
        json.dumps(content, sort_keys=True),
        WORKER_ID,
    )
    return str(row["id"])


async def ingest_record(conn: asyncpg.Connection, raw: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_edm_record(raw)

    if not normalized.get("title"):
        return {"status": "quarantined", "reason": "missing_title"}

    rights = classify_rights(normalized.get("edm_rights"))
    if not rights["allowed"]:
        return {"status": "rejected", "reason": "rights_not_allowlisted"}

    media_type = classify_media_type(normalized)
    if not media_type["allowed"]:
        return {"status": "rejected", "reason": media_type.get("reason", "unsupported_media_type")}

    if not select_representative_media_url(normalized):
        return {"status": "rejected", "reason": "missing_representative_media_url"}

    async with conn.transaction():
        source_item_id = await upsert_source_item(conn, normalized, media_type["media_type_id"])
        source_record_id = await insert_source_record(conn, source_item_id, raw, normalized)
        media_rights_id = await insert_media_rights(conn, source_item_id, rights, normalized)
        technical_content = build_technical_metadata(normalized, media_type["media_type_id"])
        media_technical_metadata_id = await insert_media_technical_metadata(
            conn,
            source_item_id,
            media_type["media_type_id"],
            technical_content,
        )

    return {
        "status": "ingested",
        "source_item_id": source_item_id,
        "source_record_id": source_record_id,
        "media_rights_id": media_rights_id,
        "media_technical_metadata_id": media_technical_metadata_id,
    }
```

### `workers/europeana_adapter/main.py`

```python
from __future__ import annotations

import argparse
import asyncio
import json
import logging
from pathlib import Path

import asyncpg

from .client import fetch_record, search_records
from .config import settings
from .store import ingest_record

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("europeana_adapter")


async def run_dry_run(query: str, limit: int) -> None:
    result = await search_records(query, rows=limit)
    items = result.get("items") or []
    print(json.dumps({"mode": "dry_run", "query": query, "records_fetched": len(items)}, indent=2))


async def run_ingest_fixture(path: str) -> None:
    raw = json.loads(Path(path).read_text())
    conn = await asyncpg.connect(settings.postgres_dsn)
    try:
        result = await ingest_record(conn, raw)
        print(json.dumps(result, indent=2, sort_keys=True))
    finally:
        await conn.close()


async def run_ingest_record(record_id: str) -> None:
    raw = await fetch_record(record_id)
    conn = await asyncpg.connect(settings.postgres_dsn)
    try:
        result = await ingest_record(conn, raw)
        print(json.dumps(result, indent=2, sort_keys=True))
    finally:
        await conn.close()


async def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    dry_run = sub.add_parser("dry-run")
    dry_run.add_argument("--query", required=True)
    dry_run.add_argument("--limit", type=int, default=50)

    fixture = sub.add_parser("ingest-fixture")
    fixture.add_argument("path")

    record = sub.add_parser("ingest-record")
    record.add_argument("--record-id", required=True)

    args = parser.parse_args()
    if args.command == "dry-run":
        await run_dry_run(args.query, args.limit)
    elif args.command == "ingest-fixture":
        await run_ingest_fixture(args.path)
    elif args.command == "ingest-record":
        await run_ingest_record(args.record_id)


if __name__ == "__main__":
    asyncio.run(main())
```

## Fixture Skeletons

Use this shape for `cc0_image.json`, changing `id`, `rights`, and title per fixture:

```json
{
  "object": {
    "id": "/123/test-cc0-image",
    "type": "IMAGE",
    "title": ["Yellowstone test image"],
    "dcDescription": ["Fixture description."],
    "year": ["1900"],
    "dcCreator": ["Fixture Creator"],
    "rights": ["https://creativecommons.org/publicdomain/zero/1.0/"],
    "provider": ["Europeana"],
    "dataProvider": ["Fixture Museum"],
    "country": ["Netherlands"],
    "language": ["en"],
    "dcSubject": ["Yellowstone", "Landscape"],
    "edmIsShownAt": ["https://example.org/object/cc0"],
    "edmIsShownBy": ["https://example.org/media/cc0.jpg"],
    "edmPreview": ["https://example.org/media/cc0-preview.jpg"]
  }
}
```

Rights fixture changes:

```text
pdm_image.json: rights = https://creativecommons.org/publicdomain/mark/1.0/
noc_us_image.json: rights = https://rightsstatements.org/vocab/NoC-US/1.0/
in_copyright_image.json: rights = https://rightsstatements.org/vocab/InC/1.0/
missing_rights_image.json: remove rights
missing_title_image.json: remove title
unsupported_audio.json: type = SOUND, title includes audio
```

## Test Skeletons

### `tests/unit/test_europeana_rights.py`

```python
from workers.europeana_adapter.rights import classify_rights, normalize_rights_uri


def test_cc0_is_allowed() -> None:
    result = classify_rights("http://creativecommons.org/publicdomain/zero/1.0/")
    assert result["allowed"] is True
    assert result["rights_status"] == "verified_cc0"


def test_pdm_is_allowed() -> None:
    result = classify_rights("https://creativecommons.org/publicdomain/mark/1.0/")
    assert result["allowed"] is True
    assert result["rights_status"] == "verified_pd"


def test_noc_us_is_allowed() -> None:
    result = classify_rights("http://rightsstatements.org/vocab/NoC-US/1.0/")
    assert result["allowed"] is True
    assert result["rights_basis"] == "noc_us_statement"


def test_non_allowlisted_rights_rejected() -> None:
    result = classify_rights("https://rightsstatements.org/vocab/InC/1.0/")
    assert result["allowed"] is False


def test_missing_rights_rejected() -> None:
    assert classify_rights(None)["allowed"] is False


def test_http_normalizes_to_https() -> None:
    assert normalize_rights_uri("http://rightsstatements.org/vocab/NoC-US/1.0/").startswith("https://")
```

### `tests/unit/test_europeana_edm.py`

```python
import json
from pathlib import Path

from workers.europeana_adapter.edm import canonical_json_hash, mandatory_field_warnings, normalize_edm_record


def load_fixture(name: str) -> dict:
    return json.loads(Path(f"tests/fixtures/europeana/{name}").read_text())


def test_normalize_complete_record() -> None:
    normalized = normalize_edm_record(load_fixture("cc0_image.json"))
    assert normalized["title"]
    assert normalized["edm_rights"]
    assert normalized["is_shown_by"]


def test_hash_is_deterministic() -> None:
    raw = load_fixture("cc0_image.json")
    assert canonical_json_hash(raw) == canonical_json_hash(raw)


def test_missing_title_warning() -> None:
    normalized = normalize_edm_record(load_fixture("missing_title_image.json"))
    assert "missing_dc_title" in mandatory_field_warnings(normalized)
```

### `tests/unit/test_europeana_media_type.py`

```python
from workers.europeana_adapter.media_type import classify_media_type


def test_image_defaults_to_image() -> None:
    assert classify_media_type({"edm_type": "IMAGE", "subjects": []})["media_type_id"] == "image"


def test_map_signal_classifies_map() -> None:
    result = classify_media_type({"edm_type": "IMAGE", "title": "Yellowstone map"})
    assert result["allowed"] is True
    assert result["media_type_id"] == "map"


def test_audio_rejected() -> None:
    result = classify_media_type({"edm_type": "SOUND", "title": "Yellowstone audio"})
    assert result["allowed"] is False
```

### `tests/unit/test_europeana_technical.py`

```python
from workers.europeana_adapter.technical import build_technical_metadata, select_representative_media_url


def test_selects_is_shown_by_first() -> None:
    normalized = {"is_shown_by": "a", "object_url": "b", "preview_urls": ["c"]}
    assert select_representative_media_url(normalized) == "a"


def test_unknown_dimensions_flag() -> None:
    content = build_technical_metadata({"title": "x"}, "image")
    assert content["quality_flag"] == "unknown_dimensions"


def test_below_minimum_flag() -> None:
    content = build_technical_metadata({"width": 300, "height": 399}, "image")
    assert content["quality_flag"] == "below_minimum"
```

### `tests/unit/test_europeana_store.py`

Start with mocked or fake connection tests if M36 tables are not available. Once M36 exists, convert
to integration-style DB tests.

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


async def test_missing_title_quarantined(fake_conn) -> None:
    result = await ingest_record(fake_conn, load_fixture("missing_title_image.json"))
    assert result["status"] == "quarantined"
```

### `tests/replay/test_europeana_adapter_week1.py`

```python
import json
from pathlib import Path

from workers.europeana_adapter.edm import normalize_edm_record
from workers.europeana_adapter.media_type import classify_media_type
from workers.europeana_adapter.rights import classify_rights


def load_fixture(name: str) -> dict:
    return json.loads(Path(f"tests/fixtures/europeana/{name}").read_text())


def test_fixture_replay_is_stable() -> None:
    raw = load_fixture("cc0_image.json")
    first = normalize_edm_record(raw)
    second = normalize_edm_record(raw)
    assert first["raw_payload_hash"] == second["raw_payload_hash"]
    assert classify_rights(first["edm_rights"]) == classify_rights(second["edm_rights"])
    assert classify_media_type(first) == classify_media_type(second)
```

## Coding Order

1. Create directories and files.
2. Add fixtures.
3. Implement `rights.py`.
4. Add and pass `test_europeana_rights.py`.
5. Implement `edm.py`.
6. Add and pass `test_europeana_edm.py`.
7. Implement `media_type.py`.
8. Add and pass `test_europeana_media_type.py`.
9. Implement `technical.py`.
10. Add and pass `test_europeana_technical.py`.
11. Inspect M36 tables.
12. Add conditional SQL only if required.
13. Implement `store.py`.
14. Add `test_europeana_store.py`.
15. Implement `client.py`.
16. Implement `main.py`.
17. Add replay test.
18. Run targeted tests.
19. Run dry-run.
20. Run one fixture ingest.

## Completion Gate

Ready for Week 2 only when:

- target tests pass
- CC0/PDM/NoC-US accepted
- non-allowlisted rights rejected before DB writes
- fixture can create all four Week 1 substrate records
- replay fixture output is stable
- no `activation_target` code exists
