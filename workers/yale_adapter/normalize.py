"""Yale LUX Linked Art normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .client import (
    INSTITUTION_LABELS,
    build_iiif_image_url,
    derive_manifest_candidate,
    detect_source_slug,
    extract_iiif_image_services,
    extract_object_id,
    extract_record_id,
)
from .rights import YALE_RIGHTS_POLICY_ID, classify_rights

YALE_PROVIDER = "Yale University Collections"


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
    """Hash Yale source payloads for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _identified_by_value(record: dict[str, Any], wanted_type: str) -> str | None:
    wanted = wanted_type.lower()
    for entry in _as_list(record.get("identified_by")):
        if not isinstance(entry, dict):
            continue
        entry_type = _string(entry.get("type")) or ""
        entry_label = _label(entry) or ""
        if wanted in entry_type.lower() or wanted in entry_label.lower():
            content = _string(entry.get("content"))
            if content:
                return content
    return None


def extract_accession_number(record: dict[str, Any]) -> str | None:
    return _identified_by_value(record, "identifier")


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
    except (ValueError, TypeError):
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
        _string(timespan.get("_label")),
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
    for entry in _as_list(record.get("about")):
        label = _label(entry)
        if label and label not in seen:
            seen.add(label)
            terms.append(label)
    for entry in _as_list(record.get("classified_as")):
        label = _label(entry)
        if label and label not in seen:
            seen.add(label)
            terms.append(label)
    return terms


def extract_geographic_subjects(record: dict[str, Any]) -> list[str]:
    places: list[str] = []
    for entry in _as_list(record.get("about")):
        if isinstance(entry, dict):
            entry_type = _string(entry.get("type")) or ""
            if "place" in entry_type.lower():
                label = _label(entry)
                if label:
                    places.append(label)
    return places


def extract_title(record: dict[str, Any]) -> str | None:
    """Extract the preferred Yale title/name."""
    return _identified_by_value(record, "name") or _label(record)


def extract_collection(record: dict[str, Any]) -> str | None:
    """Extract the Yale holding collection/institution label."""
    source_slug = detect_source_slug(record)
    if source_slug in INSTITUTION_LABELS:
        return INSTITUTION_LABELS[source_slug]
    for entry in _as_list(record.get("member_of")):
        label = _label(entry)
        if label:
            return label
    return None


def extract_manifest_url(record: dict[str, Any]) -> str | None:
    """Return the IIIF manifest URL for a Yale object when derivable."""
    candidate = derive_manifest_candidate(record)
    return candidate.url if candidate is not None else None


def extract_image_service(manifest: dict[str, Any] | None) -> str | None:
    """Return the first IIIF Image API service from a v3 manifest."""
    if not isinstance(manifest, dict):
        return None
    services = extract_iiif_image_services(manifest)
    return services[0] if services else None


def build_rights_evidence(
    record: dict[str, Any] | None,
    *,
    manifest: dict[str, Any] | None = None,
) -> dict[str, str | None]:
    """Build Yale rights evidence per DD-YALE-001 Article II.4."""
    record_dict = record if isinstance(record, dict) else {}
    rights = classify_rights(record)
    source_slug = rights["source_slug"] or detect_source_slug(record_dict)
    manifest_url = extract_manifest_url(record_dict) if record_dict else None
    image_service = extract_image_service(manifest)
    record_id = extract_record_id(record_dict) or None
    object_id = extract_object_id(record_dict)
    rights_uri = rights["rights_statement_uri"]

    slug = source_slug if source_slug in ("ycba", "yuag") else "yale"
    evidence: dict[str, str | None] = {
        f"{slug}_subject_to_uri": rights_uri,
        f"{slug}_record_id": record_id,
        f"{slug}_object_id": object_id,
        f"{slug}_iiif_manifest": manifest_url,
        "yale_object_id": object_id,
        "yale_rights_uri": rights_uri,
        "yale_collection": extract_collection(record_dict),
        "yale_iiif_manifest": manifest_url,
        "yale_image_service": image_service,
    }
    if source_slug == "ycba":
        evidence["ycba_attribution"] = "Yale Center for British Art"
    return evidence


def normalize_record(
    record: dict[str, Any] | None,
    *,
    manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize one Yale LUX object plus optional IIIF manifest evidence."""
    record_dict = record if isinstance(record, dict) else {}
    raw_payload = {"object": record, "iiif_manifest": manifest}
    rights = classify_rights(record)
    evidence = build_rights_evidence(record, manifest=manifest)
    image_service = evidence["yale_image_service"]
    representative_media_url = (
        build_iiif_image_url(image_service) if isinstance(image_service, str) else None
    )
    source_slug = rights["source_slug"] or detect_source_slug(record_dict)
    collection = extract_collection(record_dict)
    ycba_rights_uri = rights["rights_statement_uri"] if source_slug == "ycba" else None
    yuag_rights_uri = rights["rights_statement_uri"] if source_slug == "yuag" else None
    ycba_attribution = "Yale Center for British Art" if source_slug == "ycba" else None
    date_start, date_end, date_display = extract_dates(record_dict)

    return {
        "record_id": evidence["yale_object_id"],
        "accession_num": extract_accession_number(record_dict),
        "title": extract_title(record_dict),
        "description": None,
        "date": date_display,
        "date_start": date_start,
        "date_end": date_end,
        "creator": extract_creator(record_dict),
        "subject_terms": extract_subject_terms(record_dict),
        "geographic_subjects": extract_geographic_subjects(record_dict),
        "rights_uri": rights["rights_statement_uri"],
        "provider": collection or YALE_PROVIDER,
        "dataProvider": collection or YALE_PROVIDER,
        "edm_type": extract_edm_type(record_dict),
        "source_url": extract_record_id(record_dict) or None,
        "representative_media_url": representative_media_url,
        "preview_urls": [representative_media_url] if representative_media_url else [],
        "width_px": None,
        "height_px": None,
        "raw_payload_hash": canonical_json_hash(raw_payload),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "yale_rights_basis": rights["rights_basis"],
        "yale_rights_policy_id": YALE_RIGHTS_POLICY_ID,
        "yale_source_slug": source_slug,
        "ycba_rights_uri": ycba_rights_uri,
        "ycba_attribution": ycba_attribution,
        "yuag_rights_uri": yuag_rights_uri,
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

