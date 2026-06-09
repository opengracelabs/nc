"""Cleveland Museum of Art Open Access normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .rights import classify_rights

CMA_PROVIDER = "Cleveland Museum of Art"
CMA_COLLECTION_BASE_URL = "https://clevelandart.org/art"


def _record_object(raw: dict[str, Any]) -> dict[str, Any]:
    data = raw.get("data")
    if isinstance(data, dict):
        return data
    return raw


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        value = [value]
    return [str(item).strip() for item in value if str(item).strip()]


def _image_tier(record: dict[str, Any], tier: str) -> dict[str, Any] | None:
    images = record.get("images")
    if not isinstance(images, dict):
        return None
    image = images.get(tier)
    return image if isinstance(image, dict) else None


def _image_url(record: dict[str, Any], tier: str) -> str | None:
    image = _image_tier(record, tier)
    if image is None:
        return None
    return _string(image.get("url"))


def _image_int(record: dict[str, Any], tier: str, key: str) -> int | None:
    image = _image_tier(record, tier)
    if image is None:
        return None
    value = image.get(key)
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def representative_media_url(record: dict[str, Any]) -> str | None:
    """Select the web-deliverable representative image tier."""
    return _image_url(record, "print") or _image_url(record, "web")


def _additional_image_urls(record: dict[str, Any]) -> list[str]:
    alternate_images = record.get("alternate_images")
    if not isinstance(alternate_images, list):
        return []
    urls: list[str] = []
    for item in alternate_images:
        if not isinstance(item, dict):
            continue
        images = item.get("images")
        if not isinstance(images, dict):
            images = item
        image = images.get("print")
        if not isinstance(image, dict) or not _string(image.get("url")):
            image = images.get("web")
        if not isinstance(image, dict):
            continue
        url = _string(image.get("url"))
        if url:
            urls.append(url)
    return urls


def _creators(record: dict[str, Any]) -> list[str]:
    creators = record.get("creators")
    if not isinstance(creators, list):
        return []
    values: list[str] = []
    for item in creators:
        if not isinstance(item, dict):
            continue
        value = _string(item.get("description") or item.get("name"))
        if value:
            values.append(value)
    return values


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash a raw CMA API payload for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def extract_record_id(raw: dict[str, Any]) -> str | None:
    """Extract the stable CMA integer artwork identifier."""
    value = _record_object(raw).get("id")
    if value is None or isinstance(value, bool):
        return None
    return _string(value)


def build_collection_url(accession_number: str | None) -> str | None:
    """Build the public CMA collection page URL from accession_number."""
    cleaned = _string(accession_number)
    if cleaned is None:
        return None
    return f"{CMA_COLLECTION_BASE_URL}/{cleaned}"


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize one CMA artwork payload for rights and metadata replay."""
    record = _record_object(raw)
    rights = classify_rights(record)
    record_id = extract_record_id(record)
    accession_number = _string(record.get("accession_number"))
    rep_url = representative_media_url(record)
    additional_images = _additional_image_urls(record)
    creators = _creators(record)

    return {
        "record_id": record_id,
        "title": _string(record.get("title")),
        "description": _string(record.get("description") or record.get("tombstone")),
        "date": _string(record.get("creation_date")),
        "creator": "; ".join(creators) if creators else None,
        "subject_terms": _string_list(
            [
                record.get("culture"),
                record.get("type"),
                record.get("department"),
                record.get("collection"),
            ]
        ),
        "rights_uri": rights["rights_statement_uri"],
        "provider": CMA_PROVIDER,
        "dataProvider": CMA_PROVIDER,
        "edm_type": _string(record.get("type")),
        "source_url": _string(record.get("url")) or build_collection_url(accession_number),
        "representative_media_url": rep_url,
        "preview_urls": [
            url for url in [rep_url, _image_url(record, "web"), *additional_images] if url
        ],
        "width_px": _image_int(record, "print", "width") or _image_int(record, "web", "width"),
        "height_px": _image_int(record, "print", "height") or _image_int(record, "web", "height"),
        "raw_payload_hash": canonical_json_hash(raw),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "cma_share_license_status": _string(record.get("share_license_status")),
        "cma_copyright": _string(record.get("copyright")),
        "cma_rights_basis": rights["rights_basis"],
        "cma_rights_policy_id": rights["rights_policy_id"],
        "accession_number": accession_number,
        "cma_image_web_url": _image_url(record, "web"),
        "cma_image_print_url": _image_url(record, "print"),
        "cma_image_full_url": _image_url(record, "full"),
        "images": record.get("images") if isinstance(record.get("images"), dict) else {},
        "additional_images": additional_images,
        "alternate_images": (
            record.get("alternate_images")
            if isinstance(record.get("alternate_images"), list)
            else []
        ),
        "creation_date_earliest": record.get("creation_date_earliest"),
        "creation_date_latest": record.get("creation_date_latest"),
        "creators": creators,
        "culture": _string(record.get("culture")),
        "department": _string(record.get("department")),
        "collection": _string(record.get("collection")),
        "technique": _string(record.get("technique")),
        "find_spot": _string(record.get("find_spot")),
        "creditline": _string(record.get("creditline")),
        "is_highlight": record.get("is_highlight"),
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

