"""Statens Museum for Kunst Open API normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .client import build_manifest_url
from .rights import classify_rights

SMK_PROVIDER = "Statens Museum for Kunst"


def _record_object(raw: dict[str, Any]) -> dict[str, Any]:
    items = raw.get("items")
    if isinstance(items, list) and items and isinstance(items[0], dict):
        return items[0]
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


def _first_title(record: dict[str, Any]) -> str | None:
    titles = record.get("titles")
    if not isinstance(titles, list):
        return _string(record.get("title"))

    fallback: str | None = None
    for item in titles:
        if not isinstance(item, dict):
            continue
        title = _string(item.get("title"))
        if title is None:
            continue
        if fallback is None:
            fallback = title
        language = _string(item.get("language"))
        if language and language.lower() in {"engelsk", "english", "en"}:
            return title
    return fallback


def _creator(record: dict[str, Any]) -> str | None:
    artists = _string_list(record.get("artist"))
    if artists:
        return "; ".join(artists)

    production = record.get("production")
    if isinstance(production, list):
        creators = [
            creator
            for item in production
            if isinstance(item, dict)
            for creator in [_string(item.get("creator"))]
            if creator
        ]
        if creators:
            return "; ".join(creators)
    return None


def _object_names(record: dict[str, Any]) -> list[str]:
    names = record.get("object_names")
    if not isinstance(names, list):
        return []
    values: list[str] = []
    for item in names:
        if isinstance(item, dict):
            value = _string(item.get("name"))
            if value:
                values.append(value)
    return values


def _description(record: dict[str, Any]) -> str | None:
    object_names = _object_names(record)
    techniques = _string_list(record.get("techniques"))
    materials = _string_list(record.get("materials"))
    parts = [*object_names, *techniques, *materials]
    return ", ".join(parts) if parts else None


def _first_image_url(record: dict[str, Any]) -> str | None:
    images = record.get("images")
    if not isinstance(images, list) or not images or not isinstance(images[0], dict):
        return None
    return _string(images[0].get("url"))


def _representative_media_url(record: dict[str, Any]) -> str | None:
    return _string(record.get("image_native")) or _first_image_url(record)


def _preview_urls(record: dict[str, Any], representative_media_url: str | None) -> list[str]:
    urls: list[str] = []
    for value in (
        representative_media_url,
        record.get("image_thumbnail"),
        record.get("image_iiif_id"),
    ):
        url = _string(value)
        if url and url not in urls:
            urls.append(url)
    return urls


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash a raw SMK API payload for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def extract_record_id(raw: dict[str, Any]) -> str | None:
    """Extract the stable SMK object_number identifier."""
    return _string(_record_object(raw).get("object_number"))


def build_collection_url(record: dict[str, Any]) -> str | None:
    """Return the public SMK collection page URL from the API record."""
    return _string(record.get("frontend_url")) or _string(record.get("object_url"))


def _image_rights(record: dict[str, Any]) -> str | None:
    image_rights = record.get("image_rights")
    if isinstance(image_rights, dict):
        return _string(image_rights.get("rights"))
    return None


def _content_subject_terms(record: dict[str, Any]) -> list[str]:
    subjects = record.get("content_subject")
    if not isinstance(subjects, list):
        return []
    terms: list[str] = []
    for item in subjects:
        if isinstance(item, dict):
            value = _string(item.get("name") or item.get("title") or item.get("label"))
        else:
            value = _string(item)
        if value:
            terms.append(value)
    return terms


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize one SMK artwork payload for rights and metadata replay."""
    record = _record_object(raw)
    rights = classify_rights(record)
    record_id = extract_record_id(record)
    representative_media_url = _representative_media_url(record)
    manifest_url = _string(record.get("iiif_manifest")) or (
        build_manifest_url(record_id) if record_id else None
    )

    return {
        "record_id": record_id,
        "title": _first_title(record),
        "description": _description(record),
        "date": _string(record.get("production_date") or record.get("production_dates_notes")),
        "creator": _creator(record),
        "subject_terms": _content_subject_terms(record),
        "rights_uri": rights["rights_statement_uri"],
        "provider": SMK_PROVIDER,
        "dataProvider": SMK_PROVIDER,
        "edm_type": _object_names(record)[0] if _object_names(record) else None,
        "source_url": build_collection_url(record),
        "representative_media_url": representative_media_url,
        "preview_urls": _preview_urls(record, representative_media_url),
        "width_px": record.get("image_width"),
        "height_px": record.get("image_height"),
        "raw_payload_hash": canonical_json_hash(raw),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "smk_public_domain": record.get("public_domain"),
        "smk_image_rights": _image_rights(record),
        "smk_rights_basis": rights["rights_basis"],
        "smk_rights_policy_id": rights["rights_policy_id"],
        "smk_object_number": record_id,
        "smk_image_native": _string(record.get("image_native")),
        "smk_image_iiif_id": _string(record.get("image_iiif_id")),
        "smk_manifest_url": manifest_url,
        "smk_image_thumbnail": _string(record.get("image_thumbnail")),
        "image_mime_type": _string(record.get("image_mime_type")),
        "image_hq": record.get("image_hq"),
        "artist": _string_list(record.get("artist")),
        "production": (
            record.get("production") if isinstance(record.get("production"), list) else []
        ),
        "object_names": _object_names(record),
        "materials": _string_list(record.get("materials")),
        "techniques": _string_list(record.get("techniques")),
        "dimensions": (
            record.get("dimensions") if isinstance(record.get("dimensions"), list) else []
        ),
        "images": record.get("images") if isinstance(record.get("images"), list) else [],
        "content_subject": (
            record.get("content_subject")
            if isinstance(record.get("content_subject"), list)
            else []
        ),
        "frontend_url": _string(record.get("frontend_url")),
        "object_url": _string(record.get("object_url")),
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

