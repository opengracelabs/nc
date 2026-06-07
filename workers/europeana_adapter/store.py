"""M36 substrate write path for Europeana records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .edm import normalize_edm_record
from .technical import (
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "europeana_adapter:sprint3"
SOURCE_SLUG = "europeana"
SCHEMA_STANDARD = "edm"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


_RUNTIME = StoreRuntime(
    worker_id=WORKER_ID,
    source_slug=SOURCE_SLUG,
    schema_standard=SCHEMA_STANDARD,
    technical_schema_version=TECHNICAL_SCHEMA_VERSION,
    validator_name=VALIDATOR_NAME,
    validator_version=VALIDATOR_VERSION,
    build_technical_metadata=_build_technical_metadata,
    validation_status=validation_status,
    workflow_record_id_key="europeana_record_id",
    anchor_type="mixed",
)


async def write_record(
    conn: Any,
    raw_payload: dict[str, Any],
    *,
    source_id: str,
    media_type_id: str,
) -> dict[str, Any]:
    """Write one non-blocked Europeana record into the M36 substrate tables."""
    normalized = normalize_edm_record(raw_payload)
    return await write_normalized_record(
        conn,
        runtime=_RUNTIME,
        raw_payload=raw_payload,
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )
