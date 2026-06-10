"""Mia collection JSON normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .config import METADATA_LICENSE_URI, SCHEMA_STANDARD, SOURCE_SLUG, settings
from .rights import MIA_RIGHTS_POLICY_ID, classify_rights

MIA_PROVIDER = "Minneapolis Institute of Art"


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash Mia source payloads for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def extract_object_id(record: dict[str, Any]) -> str | None:
    """Extract Mia numeric object id as a string."""
    object_id = _string(record.get("id"))
    if object_id and object_id.startswith("http"):
        return object_id.rstrip("/").split("/")[-1]
    return object_id


def build_source_record_uri(object_id: str | None) -> str | None:
    """Build Mia canonical collection object URL."""
    if not object_id:
        return None
    return f"https://collections.artsmia.org/art/{object_id}"


def build_image_url(record: dict[str, Any]) -> str | None:
    """Build Mia's deterministic sharded 800px reference image URL."""
    object_id = extract_object_id(record)
    if not object_id:
        return None
    try:
        numeric_id = int(object_id)
    except ValueError:
        return None
    return settings.mia_image_url_template.format(
        shard=numeric_id % 7,
        object_id=numeric_id,
    )


def _search_hit_source(item: Any) -> dict[str, Any] | None:
    if isinstance(item, dict) and isinstance(item.get("_source"), dict):
        return item["_source"]
    if isinstance(item, dict):
        return item
    return None


def iter_search_records(payload: dict[str, Any] | list[Any] | None) -> list[dict[str, Any]]:
    """Extract Mia object records from an object payload, search payload, or list."""
    if isinstance(payload, list):
        return [item for item in (_search_hit_source(value) for value in payload) if item]
    if not isinstance(payload, dict):
        return []
    hits = payload.get("hits")
    if isinstance(hits, dict) and isinstance(hits.get("hits"), list):
        return [item for item in (_search_hit_source(value) for value in hits["hits"]) if item]
    return [payload]


def build_rights_evidence(record: dict[str, Any] | None) -> dict[str, Any]:
    """Build Mia Sprint 2 evidence fields."""
    record_dict = record if isinstance(record, dict) else {}
    object_id = extract_object_id(record_dict)
    rights = classify_rights(record)
    image_url = build_image_url(record_dict) if object_id else None
    return {
        "mia_object_id": object_id,
        "mia_rights_type": _string(record_dict.get("rights_type")),
        "mia_rights_uri": rights["rights_statement_uri"],
        "mia_rights_image_display": _string(record_dict.get("Rights_Image_Display")),
        "mia_image": _string(record_dict.get("image")),
        "mia_public_access": record_dict.get("public_access"),
        "mia_restricted": record_dict.get("restricted"),
        "mia_primary_rendition_number": _string(record_dict.get("Primary_RenditionNumber")),
        "mia_cache_location": _string(record_dict.get("Cache_Location")),
        "mia_image_width": _int(record_dict.get("image_width")),
        "mia_image_height": _int(record_dict.get("image_height")),
        "mia_accession_number": _string(record_dict.get("accession_number")),
        "mia_source_record_uri": build_source_record_uri(object_id),
        "mia_image_url": image_url,
        "mia_iiif_manifest_url": None,
    }


def has_media_delivery(record: dict[str, Any]) -> bool:
    """Return true when a Mia record has enough media fields for a candidate."""
    evidence = build_rights_evidence(record)
    return all(
        (
            evidence["mia_image"] == "valid",
            bool(evidence["mia_primary_rendition_number"]),
            bool(evidence["mia_image_width"]),
            bool(evidence["mia_image_height"]),
            bool(evidence["mia_image_url"]),
        )
    )


def normalize_record(record: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Normalize one Mia object into zero or one media candidate."""
    record_dict = record if isinstance(record, dict) else {}
    rights = classify_rights(record)
    if not rights["allowed"] or not has_media_delivery(record_dict):
        return []

    evidence = build_rights_evidence(record_dict)
    raw_payload_hash = canonical_json_hash({"record": record})
    normalized = {
        "record_id": evidence["mia_object_id"],
        "source_record_id": evidence["mia_object_id"],
        "accession_num": evidence["mia_accession_number"],
        "title": _string(record_dict.get("title")),
        "description": _string(record_dict.get("text") or record_dict.get("description")),
        "date": _string(record_dict.get("dated")),
        "creator": _string(record_dict.get("artist")),
        "subject_terms": [
            value
            for value in (
                _string(record_dict.get("classification")),
                _string(record_dict.get("object_name")),
                _string(record_dict.get("department")),
            )
            if value
        ],
        "geographic_subjects": [
            value
            for value in (
                _string(record_dict.get("continent")),
                _string(record_dict.get("country")),
            )
            if value
        ],
        "rights_uri": rights["rights_statement_uri"],
        "provider": MIA_PROVIDER,
        "dataProvider": MIA_PROVIDER,
        "edm_type": _string(record_dict.get("classification")) or "IMAGE",
        "source_url": evidence["mia_source_record_uri"],
        "representative_media_url": evidence["mia_image_url"],
        "preview_urls": [evidence["mia_image_url"]],
        "width_px": evidence["mia_image_width"],
        "height_px": evidence["mia_image_height"],
        "raw_payload_hash": raw_payload_hash,
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "mia_rights_basis": rights["rights_basis"],
        "mia_rights_policy_id": MIA_RIGHTS_POLICY_ID,
        "mia_source_slug": SOURCE_SLUG,
        "mia_schema_standard": SCHEMA_STANDARD,
        "mia_metadata_license_uri": METADATA_LICENSE_URI,
        **evidence,
    }
    return [normalized]


def normalize_records(payload: dict[str, Any] | list[Any] | None) -> list[dict[str, Any]]:
    """Normalize a Mia search/object payload into media candidates."""
    candidates: list[dict[str, Any]] = []
    for record in iter_search_records(payload):
        candidates.extend(normalize_record(record))
    return candidates


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
    if not normalized.get("mia_object_id"):
        warnings.append("missing_mia_object_id")
    return warnings
