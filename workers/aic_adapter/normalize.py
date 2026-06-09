"""Art Institute of Chicago Open Access normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .client import build_manifest_url
from .rights import classify_rights

AIC_IIIF_IMAGE_BASE_URL = "https://www.artic.edu/iiif/2"
AIC_COLLECTION_BASE_URL = "https://www.artic.edu/artworks"


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


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash a raw AIC API payload for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def extract_record_id(raw: dict[str, Any]) -> str | None:
    """Extract the stable AIC artwork identifier."""
    item = _record_object(raw)
    value = item.get("id")
    if value is None or isinstance(value, bool):
        return None
    return _string(value)


def build_collection_url(record_id: str | None) -> str | None:
    """Build the public AIC collection page URL for an artwork."""
    cleaned = _string(record_id)
    if cleaned is None:
        return None
    return f"{AIC_COLLECTION_BASE_URL}/{cleaned}"


def build_iiif_image_url(
    image_id: str | None,
    *,
    size: str = "843,",
) -> str | None:
    """Build the governed AIC IIIF Image API URL from an image_id."""
    cleaned = _string(image_id)
    if cleaned is None:
        return None
    return f"{AIC_IIIF_IMAGE_BASE_URL}/{cleaned}/full/{size}/0/default.jpg"


def _additional_image_urls(raw: dict[str, Any]) -> list[str]:
    urls: list[str] = []
    for image_id in _string_list(raw.get("alt_image_ids")):
        url = build_iiif_image_url(image_id)
        if url:
            urls.append(url)
    return urls


def _description(raw: dict[str, Any]) -> str | None:
    classifications = _string_list(raw.get("classification_titles"))
    if classifications:
        return ", ".join(classifications)
    return _string(raw.get("artwork_type_title") or raw.get("medium_display"))


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize one AIC artwork payload for rights and metadata replay."""
    item = _record_object(raw)
    rights = classify_rights(item)
    record_id = extract_record_id(item)
    image_id = _string(item.get("image_id"))
    representative_media_url = build_iiif_image_url(image_id)
    additional_images = _additional_image_urls(item)
    aic_manifest_url = build_manifest_url(record_id) if record_id else None

    return {
        "record_id": record_id,
        "title": _string(item.get("title")),
        "description": _description(item),
        "date": _string(item.get("date_display")),
        "creator": _string(item.get("artist_display") or item.get("artist_title")),
        "subject_terms": _string_list(item.get("subject_titles")),
        "rights_uri": rights["rights_statement_uri"],
        "provider": "Art Institute of Chicago",
        "dataProvider": "Art Institute of Chicago",
        "edm_type": _string(item.get("artwork_type_title")),
        "source_url": build_collection_url(record_id),
        "representative_media_url": representative_media_url,
        "preview_urls": (
            [representative_media_url, *additional_images]
            if representative_media_url
            else additional_images
        ),
        "width_px": None,
        "height_px": None,
        "raw_payload_hash": canonical_json_hash(raw),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "aic_is_public_domain": item.get("is_public_domain"),
        "aic_rights_basis": rights["rights_basis"],
        "aic_rights_policy_id": rights["rights_policy_id"],
        "aic_image_id": image_id,
        "aic_manifest_url": aic_manifest_url,
        "aic_api_link": _string(item.get("api_link")),
        "aic_copyright_notice": _string(item.get("copyright_notice")),
        "additional_images": additional_images,
        "alt_image_ids": _string_list(item.get("alt_image_ids")),
        "date_start": item.get("date_start"),
        "date_end": item.get("date_end"),
        "artist_title": _string(item.get("artist_title")),
        "place_of_origin": _string(item.get("place_of_origin")),
        "department": _string(item.get("department_title")),
        "department_id": _string(item.get("department_id")),
        "medium": _string(item.get("medium_display")),
        "style_titles": _string_list(item.get("style_titles")),
        "classification_titles": _string_list(item.get("classification_titles")),
        "accession_number": _string(item.get("main_reference_number")),
        "thumbnail": item.get("thumbnail") if isinstance(item.get("thumbnail"), dict) else None,
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

