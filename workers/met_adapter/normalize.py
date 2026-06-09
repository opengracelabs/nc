"""Metropolitan Museum of Art Open Access normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .rights import classify_rights


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _image_list(value: Any) -> list[str]:
    return [str(item).strip() for item in _list(value) if str(item).strip()]


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash a raw Met API object for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def extract_record_id(raw: dict[str, Any]) -> str | None:
    """Extract the stable Met object identifier."""
    value = raw.get("objectID")
    if value is None or isinstance(value, bool):
        return None
    return _string(value)


def _subject_terms(raw: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    for tag in raw.get("tags") or []:
        if isinstance(tag, dict) and tag.get("term"):
            terms.append(str(tag["term"]))
    return terms


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize one Met object payload for rights and metadata replay."""
    rights = classify_rights(raw)
    primary_image = _string(raw.get("primaryImage"))
    additional_images = _image_list(raw.get("additionalImages"))

    return {
        "record_id": extract_record_id(raw),
        "title": _string(raw.get("title")),
        "description": _string(raw.get("objectName") or raw.get("classification")),
        "date": _string(raw.get("objectDate")),
        "creator": _string(raw.get("artistDisplayName")),
        "subject_terms": _subject_terms(raw),
        "rights_uri": rights["rights_statement_uri"],
        "provider": "Metropolitan Museum of Art",
        "dataProvider": (
            _string(raw.get("repository")) or "Metropolitan Museum of Art, New York, NY"
        ),
        "edm_type": _string(raw.get("objectName") or raw.get("classification")),
        "source_url": _string(raw.get("objectURL")),
        "representative_media_url": primary_image,
        "preview_urls": [primary_image, *additional_images] if primary_image else additional_images,
        "width_px": raw.get("width_px"),
        "height_px": raw.get("height_px"),
        "raw_payload_hash": canonical_json_hash(raw),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "met_is_public_domain": raw.get("isPublicDomain"),
        "met_rights_basis": rights["rights_basis"],
        "met_rights_policy_id": rights["rights_policy_id"],
        "met_object_id": extract_record_id(raw),
        "primary_image": primary_image,
        "additional_images": additional_images,
        "rights_and_reproduction": _string(raw.get("rightsAndReproduction")),
        "department": _string(raw.get("department")),
        "culture": _string(raw.get("culture")),
        "period": _string(raw.get("period")),
        "country": _string(raw.get("country")),
        "region": _string(raw.get("region")),
        "subregion": _string(raw.get("subregion")),
        "city": _string(raw.get("city")),
        "geography_type": _string(raw.get("geographyType")),
        "artist_wikidata_url": _string(raw.get("artistWikidata_URL")),
        "artist_ulan_url": _string(raw.get("artistULAN_URL")),
        "object_wikidata_url": _string(raw.get("objectWikidata_URL")),
        "tags": raw.get("tags") if isinstance(raw.get("tags"), list) else [],
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
    if not normalized.get("description"):
        warnings.append("missing_description")
    if not normalized.get("date"):
        warnings.append("missing_date")
    if not normalized.get("provider"):
        warnings.append("missing_provider")
    if not normalized.get("dataProvider"):
        warnings.append("missing_data_provider")
    if not normalized.get("representative_media_url"):
        warnings.append("missing_representative_media_url")
    return warnings

