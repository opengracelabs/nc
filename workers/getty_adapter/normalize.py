"""Getty Linked Art normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .client import (
    build_object_url,
    extract_iiif_image_service,
    extract_manifest_url,
)
from .config import SCHEMA_STANDARD, SOURCE_SLUG
from .rights import GETTY_RIGHTS_POLICY_ID, classify_rights

GETTY_PROVIDER = "J. Paul Getty Museum"


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


def _id_value(node: dict[str, Any]) -> str | None:
    return _string(node.get("id") or node.get("@id"))


def _label(value: Any) -> str | None:
    if isinstance(value, str):
        return _string(value)
    if isinstance(value, dict):
        for key in ("_label", "label", "content", "name"):
            text = _string(value.get(key))
            if text:
                return text
    return None


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash Getty source payloads for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def extract_object_uri(record: dict[str, Any]) -> str | None:
    """Return the Getty Linked Art object URI."""
    return _id_value(record)


def extract_object_id(record: dict[str, Any]) -> str | None:
    """Return the Getty object UUID or identifier from the Linked Art URI."""
    object_uri = extract_object_uri(record)
    if object_uri:
        return object_uri.rstrip("/").split("/")[-1]
    return None


def _classified_labels(entry: dict[str, Any]) -> str:
    parts = [_string(entry.get("type")) or "", _label(entry) or ""]
    for classification in _as_list(entry.get("classified_as")):
        label = _label(classification)
        uri = _id_value(classification) if isinstance(classification, dict) else None
        if label:
            parts.append(label)
        if uri:
            parts.append(uri)
    return " ".join(parts).lower()


def _identified_by_value(record: dict[str, Any], wanted_tokens: tuple[str, ...]) -> str | None:
    wanted = tuple(token.lower() for token in wanted_tokens)
    for entry in _as_list(record.get("identified_by")):
        if not isinstance(entry, dict):
            continue
        haystack = _classified_labels(entry)
        if any(token in haystack for token in wanted):
            content = _string(entry.get("content"))
            if content:
                return content
    return None


def extract_accession_number(record: dict[str, Any]) -> str | None:
    """Extract Getty accession number from Linked Art identifiers."""
    return _identified_by_value(record, ("accession", "300312355"))


def extract_title(record: dict[str, Any]) -> str | None:
    """Extract the preferred Getty title/name."""
    return _identified_by_value(record, ("title", "name", "300404670")) or _label(record)


def extract_creator(record: dict[str, Any]) -> str | None:
    produced_by = record.get("produced_by")
    if not isinstance(produced_by, dict):
        return None
    for agent in _as_list(produced_by.get("carried_out_by")):
        label = _label(agent)
        if label:
            return label
    return None


def _parse_year(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(str(value).strip()[:4])
    except (TypeError, ValueError):
        return None


def extract_dates(record: dict[str, Any]) -> tuple[int | None, int | None, str | None]:
    produced_by = record.get("produced_by")
    if not isinstance(produced_by, dict):
        return None, None, None
    timespan = produced_by.get("timespan")
    if not isinstance(timespan, dict):
        return None, None, None
    return (
        _parse_year(timespan.get("begin_of_the_begin")),
        _parse_year(timespan.get("end_of_the_end")),
        _string(timespan.get("_label") or timespan.get("label")),
    )


def extract_edm_type(record: dict[str, Any]) -> str | None:
    for entry in _as_list(record.get("classified_as")):
        label = _label(entry)
        if label:
            return label
    return _string(record.get("type"))


def extract_subject_terms(record: dict[str, Any]) -> list[str]:
    seen: set[str] = set()
    terms: list[str] = []
    for key in ("about", "classified_as"):
        for entry in _as_list(record.get(key)):
            label = _label(entry)
            if label and label not in seen:
                seen.add(label)
                terms.append(label)
    return terms


def build_iiif_image_url(
    image_service: str,
    *,
    size: str = "!1024,1024",
) -> str:
    """Build a deterministic IIIF Image API URL from a Getty service base."""
    cleaned = image_service.strip().rstrip("/")
    if not cleaned:
        raise ValueError("missing_iiif_service")
    cleaned_size = size.strip() or "!1024,1024"
    return f"{cleaned}/full/{cleaned_size}/0/default.jpg"


def build_rights_evidence(
    record: dict[str, Any] | None,
    *,
    manifest: dict[str, Any] | None = None,
) -> dict[str, str | None]:
    """Build Getty Sprint 2 evidence fields."""
    record_dict = record if isinstance(record, dict) else {}
    rights = classify_rights(record)
    manifest_uri = extract_manifest_url(record_dict) if record_dict else None
    image_service = extract_iiif_image_service(manifest) if isinstance(manifest, dict) else None

    return {
        "getty_object_id": extract_object_id(record_dict),
        "getty_rights_uri": rights["rights_statement_uri"],
        "getty_image_service": image_service,
        "getty_manifest_uri": manifest_uri,
        "getty_accession_number": extract_accession_number(record_dict),
    }


def normalize_record(
    record: dict[str, Any] | None,
    *,
    manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize one Getty Linked Art object plus optional IIIF manifest evidence."""
    record_dict = record if isinstance(record, dict) else {}
    raw_payload = {"object": record, "iiif_manifest": manifest}
    rights = classify_rights(record)
    evidence = build_rights_evidence(record, manifest=manifest)
    image_service = evidence["getty_image_service"]
    representative_media_url = (
        build_iiif_image_url(image_service) if isinstance(image_service, str) else None
    )
    date_start, date_end, date_display = extract_dates(record_dict)
    object_uri = extract_object_uri(record_dict)

    return {
        "record_id": evidence["getty_object_id"],
        "accession_num": evidence["getty_accession_number"],
        "title": extract_title(record_dict),
        "description": None,
        "date": date_display,
        "date_start": date_start,
        "date_end": date_end,
        "creator": extract_creator(record_dict),
        "subject_terms": extract_subject_terms(record_dict),
        "geographic_subjects": [],
        "rights_uri": rights["rights_statement_uri"],
        "provider": GETTY_PROVIDER,
        "dataProvider": GETTY_PROVIDER,
        "edm_type": extract_edm_type(record_dict),
        "source_url": object_uri or (
            build_object_url(evidence["getty_object_id"])
            if isinstance(evidence["getty_object_id"], str)
            else None
        ),
        "representative_media_url": representative_media_url,
        "preview_urls": [representative_media_url] if representative_media_url else [],
        "width_px": None,
        "height_px": None,
        "raw_payload_hash": canonical_json_hash(raw_payload),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "getty_rights_basis": rights["rights_basis"],
        "getty_rights_policy_id": GETTY_RIGHTS_POLICY_ID,
        "getty_source_slug": SOURCE_SLUG,
        "getty_schema_standard": SCHEMA_STANDARD,
        **evidence,
    }


def mandatory_field_warnings(normalized: dict[str, Any]) -> list[str]:
    """Return warnings for fields required by the shared media contract."""
    warnings: list[str] = []
    if not normalized.get("record_id"):
        warnings.append("missing_record_id")
    if not normalized.get("title"):
        warnings.append("missing_title")
    if not normalized.get("rights_uri"):
        warnings.append("missing_rights_uri")
    if not normalized.get("provider"):
        warnings.append("missing_provider")
    if not normalized.get("dataProvider"):
        warnings.append("missing_data_provider")
    if not normalized.get("representative_media_url"):
        warnings.append("missing_representative_media_url")
    return warnings

