"""NARA Catalog normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .client import (
    NaraDigitalObject,
    build_catalog_record_url,
    extract_digital_objects,
    extract_na_id,
    extract_use_restriction,
)
from .config import SCHEMA_STANDARD, SOURCE_SLUG
from .rights import NARA_RIGHTS_POLICY_ID, classify_rights

NARA_PROVIDER = "National Archives and Records Administration"


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash NARA source payloads for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def extract_local_identifier(record: dict[str, Any]) -> str | None:
    """Extract NARA local identifier evidence."""
    value = record.get("localIdentifier")
    if isinstance(value, list):
        for item in value:
            text = _string(item)
            if text:
                return text
        return None
    return _string(value)


def extract_title(record: dict[str, Any]) -> str | None:
    """Extract the NARA record title."""
    return _string(record.get("title"))


def extract_subject_terms(record: dict[str, Any]) -> list[str]:
    """Extract simple subject/type terms from a NARA record."""
    seen: set[str] = set()
    terms: list[str] = []
    for key in ("generalRecordsTypes", "subjects"):
        for value in _as_list(record.get(key)):
            label = None
            if isinstance(value, dict):
                label = _string(value.get("heading") or value.get("termName"))
            else:
                label = _string(value)
            if label and label not in seen:
                seen.add(label)
                terms.append(label)
    return terms


def _object_filename(digital_object: NaraDigitalObject) -> str | None:
    return digital_object.object_filename or digital_object.object_url.rstrip("/").split("/")[-1]


def build_rights_evidence(
    record: dict[str, Any] | None,
    *,
    digital_object: NaraDigitalObject | None = None,
) -> dict[str, str | None]:
    """Build NARA Sprint 2 evidence fields."""
    record_dict = record if isinstance(record, dict) else {}
    na_id = extract_na_id(record_dict)
    return {
        "nara_naid": na_id,
        "nara_use_restriction": extract_use_restriction(record_dict),
        "nara_object_url": digital_object.object_url if digital_object else None,
        "nara_catalog_url": build_catalog_record_url(na_id) if na_id else None,
        "nara_local_identifier": extract_local_identifier(record_dict),
    }


def normalize_record(record: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Normalize one NARA Catalog record into still-image media candidates."""
    record_dict = record if isinstance(record, dict) else {}
    rights = classify_rights(record)
    na_id = extract_na_id(record_dict)
    raw_payload_hash = canonical_json_hash({"record": record})
    title = extract_title(record_dict)
    subject_terms = extract_subject_terms(record_dict)

    normalized_records: list[dict[str, Any]] = []
    for digital_object in extract_digital_objects(record_dict):
        evidence = build_rights_evidence(record_dict, digital_object=digital_object)
        object_filename = _object_filename(digital_object)
        record_id = f"{na_id}:{digital_object.object_id}" if na_id else digital_object.object_id
        normalized_records.append(
            {
                "record_id": record_id,
                "source_record_id": na_id,
                "title": title,
                "description": digital_object.object_description,
                "date": None,
                "creator": None,
                "subject_terms": subject_terms,
                "rights_uri": rights["rights_statement_uri"],
                "provider": NARA_PROVIDER,
                "dataProvider": NARA_PROVIDER,
                "edm_type": "IMAGE",
                "source_url": evidence["nara_catalog_url"],
                "representative_media_url": digital_object.object_url,
                "preview_urls": [digital_object.object_url],
                "width_px": None,
                "height_px": None,
                "raw_payload_hash": raw_payload_hash,
                "rights_decision": rights["decision"],
                "rights_allowed": rights["allowed"],
                "nara_rights_basis": rights["rights_basis"],
                "nara_rights_policy_id": NARA_RIGHTS_POLICY_ID,
                "nara_source_slug": SOURCE_SLUG,
                "nara_schema_standard": SCHEMA_STANDARD,
                "nara_object_id": digital_object.object_id,
                "nara_object_type": digital_object.object_type,
                "nara_object_filename": object_filename,
                "nara_object_file_size": digital_object.object_file_size,
                **evidence,
            }
        )
    return normalized_records


def mandatory_field_warnings(normalized: dict[str, Any]) -> list[str]:
    """Return warnings for fields required by the shared media contract."""
    warnings: list[str] = []
    if not normalized.get("record_id"):
        warnings.append("missing_record_id")
    if not normalized.get("title"):
        warnings.append("missing_title")
    if not normalized.get("provider"):
        warnings.append("missing_provider")
    if not normalized.get("dataProvider"):
        warnings.append("missing_data_provider")
    if not normalized.get("representative_media_url"):
        warnings.append("missing_representative_media_url")
    if not normalized.get("nara_naid"):
        warnings.append("missing_nara_naid")
    return warnings
