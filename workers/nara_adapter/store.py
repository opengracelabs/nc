"""M36 runtime helpers for NARA Catalog records.

Sprint 2 remains read-only. This module defines the source-owned evidence extension
that Sprint 3 can pass into the shared M36 write path without editing shared code.
"""
from __future__ import annotations

from typing import Any

from workers.shared_media_adapter.store import StoreRuntime

from .config import RIGHTS_POLICY_ID, SCHEMA_STANDARD, SOURCE_SLUG

WORKER_ID = "nara_adapter:sprint2"
TECHNICAL_SCHEMA_VERSION = "nara_technical_metadata_v1"
VALIDATOR_NAME = "nara_adapter.technical"
VALIDATOR_VERSION = "v1"


def _build_technical_metadata(normalized: dict[str, Any], media_type_id: str) -> dict[str, Any]:
    return {
        "record_id": normalized.get("record_id"),
        "media_type_id": media_type_id,
        "representative_media_url": normalized.get("representative_media_url"),
    }


def _validation_status(content: dict[str, Any]) -> str:
    if not content.get("record_id"):
        return "invalid"
    if not content.get("representative_media_url"):
        return "invalid"
    return "valid"


def _build_evidence_extension(normalized: dict[str, Any]) -> dict[str, Any]:
    return {
        "nara_naid": normalized.get("nara_naid"),
        "nara_use_restriction": normalized.get("nara_use_restriction"),
        "nara_object_url": normalized.get("nara_object_url"),
        "nara_catalog_url": normalized.get("nara_catalog_url"),
        "nara_local_identifier": normalized.get("nara_local_identifier"),
    }


def _runtime(anchor_type: str = "cultural") -> StoreRuntime:
    return StoreRuntime(
        worker_id=WORKER_ID,
        source_slug=SOURCE_SLUG,
        schema_standard=SCHEMA_STANDARD,
        technical_schema_version=TECHNICAL_SCHEMA_VERSION,
        validator_name=VALIDATOR_NAME,
        validator_version=VALIDATOR_VERSION,
        build_technical_metadata=_build_technical_metadata,
        validation_status=_validation_status,
        build_evidence_extension=_build_evidence_extension,
        rights_policy_id=RIGHTS_POLICY_ID,
        workflow_record_id_key="nara_naid",
        anchor_type=anchor_type,
    )
