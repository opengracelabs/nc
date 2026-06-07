"""M36 substrate write path for Rijksmuseum records."""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record

from .edm import normalize_search_getrecord
from .technical import (
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

WORKER_ID = "rijksmuseum_adapter:sprint4"
SOURCE_SLUG = "rijksmuseum"
SCHEMA_STANDARD = "edm"
PILOT_BIOLOGICAL_SET_SPEC = "261222"


def build_raw_payload(search_response: dict[str, Any], oai_xml: str) -> dict[str, Any]:
    """Preserve both sides of the Search -> GetRecord workflow for replay."""
    return {
        "search_response": search_response,
        "oai_getrecord_xml": oai_xml,
    }


def derive_anchor_type(normalized: dict[str, Any]) -> str:
    """Derive the governed source_item anchor type from OAI-PMH set membership."""
    if PILOT_BIOLOGICAL_SET_SPEC in (normalized.get("set_specs") or []):
        return "biological"
    return "cultural"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return build_technical_metadata(normalized, media_type_id=media_type_id)


def _runtime(anchor_type: str) -> StoreRuntime:
    return StoreRuntime(
        worker_id=WORKER_ID,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        technical_schema_version=TECHNICAL_SCHEMA_VERSION,
        validator_name=VALIDATOR_NAME,
        validator_version=VALIDATOR_VERSION,
        build_technical_metadata=_build_technical_metadata,
        validation_status=validation_status,
        workflow_record_id_key="rijksmuseum_record_id",
        anchor_type=anchor_type,
        parameterize_anchor_type=True,
        reject_missing_rights=True,
    )


async def write_record(
    conn: Any,
    search_response: dict[str, Any],
    oai_xml: str,
    *,
    source_id: str,
    media_type_id: str,
    anchor_type: str | None = None,
) -> dict[str, Any]:
    """Write one non-blocked Rijksmuseum Search/GetRecord record into M36 tables."""
    normalized = normalize_search_getrecord(search_response, oai_xml)
    raw_payload = build_raw_payload(search_response, oai_xml)
    derived_anchor_type = anchor_type if anchor_type is not None else derive_anchor_type(normalized)
    return await write_normalized_record(
        conn,
        runtime=_runtime(derived_anchor_type),
        raw_payload=raw_payload,
        normalized=normalized,
        source_id=source_id,
        media_type_id=media_type_id,
    )
