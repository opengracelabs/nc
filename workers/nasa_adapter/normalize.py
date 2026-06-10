"""NASA Image and Video Library normalization for Sprint 1."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .client import (
    build_asset_url,
    build_metadata_url,
    choose_asset_url,
    choose_preview_url,
    extract_asset_urls,
    extract_collection_items,
    extract_item_data,
    extract_item_links,
)
from .config import SCHEMA_STANDARD, SOURCE_SLUG
from .rights import NASA_RIGHTS_POLICY_ID, classify_rights

NASA_PROVIDER = "NASA"


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


def _int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash NASA source payloads for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def extract_search_records(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Extract search-result records with item/data/links preserved."""
    records: list[dict[str, Any]] = []
    for item in extract_collection_items(payload):
        data = extract_item_data(item)
        if data:
            records.append({"item": item, "data": data, "links": extract_item_links(item)})
    return records


def _link_dimension(item: dict[str, Any], key: str) -> int | None:
    best: int | None = None
    for link in extract_item_links(item):
        value = _int(link.get(key))
        if value is not None:
            best = value if best is None else max(best, value)
    return best


def build_rights_evidence(
    record: dict[str, Any] | None,
    *,
    asset_manifest: dict[str, Any] | None = None,
    metadata_location: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build NASA Sprint 1 evidence fields."""
    record_dict = record if isinstance(record, dict) else {}
    rights = classify_rights(record_dict)
    nasa_id = _string(record_dict.get("nasa_id"))
    asset_urls = extract_asset_urls(asset_manifest)
    original_url = next((url for url in asset_urls if "~orig" in url.lower()), None)
    large_url = next((url for url in asset_urls if "~large" in url.lower()), None)
    selected_url = choose_asset_url(asset_urls)
    metadata_url = None
    if isinstance(metadata_location, dict):
        metadata_url = _string(metadata_location.get("location"))
    return {
        "nasa_id": nasa_id,
        "nasa_center": _string(record_dict.get("center")),
        "nasa_media_type": _string(record_dict.get("media_type")),
        "nasa_rights_uri": rights["rights_statement_uri"],
        "nasa_rights_basis": rights["rights_basis"],
        "nasa_asset_manifest_url": build_asset_url(nasa_id) if nasa_id else None,
        "nasa_metadata_url": metadata_url or (build_metadata_url(nasa_id) if nasa_id else None),
        "nasa_original_url": original_url,
        "nasa_large_url": large_url,
        "nasa_preview_url": _string(record_dict.get("preview_url")),
        "nasa_selected_asset_url": selected_url,
        "nasa_photographer": _string(record_dict.get("photographer")),
        "nasa_secondary_creator": _string(record_dict.get("secondary_creator")),
        "nasa_keywords": [str(value) for value in _as_list(record_dict.get("keywords"))],
        "nasa_album": [str(value) for value in _as_list(record_dict.get("album"))],
        "nasa_partner_markers": rights.get("partner_markers") or [],
        "nasa_copyright_detected": bool(rights.get("copyright_markers")),
        "nasa_publicity_risk_detected": bool(rights.get("publicity_risk_markers")),
        "nasa_source_api": "images-api.nasa.gov",
    }


def normalize_record(
    record: dict[str, Any] | None,
    *,
    asset_manifest: dict[str, Any] | None = None,
    metadata_location: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Normalize one NASA image record into zero or one discovery candidate."""
    record_dict = record if isinstance(record, dict) else {}
    rights = classify_rights(record_dict)
    evidence = build_rights_evidence(
        record_dict,
        asset_manifest=asset_manifest,
        metadata_location=metadata_location,
    )
    representative_media_url = evidence["nasa_selected_asset_url"]
    if not rights["allowed"] or not representative_media_url:
        return []

    raw_payload = {
        "record": record,
        "asset_manifest": asset_manifest,
        "metadata_location": metadata_location,
    }
    preview_url = evidence["nasa_preview_url"]
    normalized = {
        "record_id": evidence["nasa_id"],
        "source_record_id": evidence["nasa_id"],
        "title": _string(record_dict.get("title")),
        "description": _string(record_dict.get("description")),
        "date": _string(record_dict.get("date_created")),
        "creator": _string(record_dict.get("photographer") or record_dict.get("secondary_creator")),
        "subject_terms": evidence["nasa_keywords"],
        "geographic_subjects": [_string(record_dict.get("location"))]
        if _string(record_dict.get("location"))
        else [],
        "rights_uri": rights["rights_statement_uri"],
        "provider": NASA_PROVIDER,
        "dataProvider": evidence["nasa_center"] or NASA_PROVIDER,
        "edm_type": evidence["nasa_media_type"],
        "source_url": evidence["nasa_asset_manifest_url"],
        "representative_media_url": representative_media_url,
        "preview_urls": [preview_url] if preview_url else [],
        "width_px": _int(record_dict.get("width")),
        "height_px": _int(record_dict.get("height")),
        "raw_payload_hash": canonical_json_hash(raw_payload),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "nasa_rights_policy_id": NASA_RIGHTS_POLICY_ID,
        "nasa_schema_standard": SCHEMA_STANDARD,
        "nasa_source_slug": SOURCE_SLUG,
        **evidence,
    }
    return [normalized]


def normalize_search_payload(
    payload: dict[str, Any] | None,
    *,
    manifests_by_nasa_id: dict[str, dict[str, Any]] | None = None,
    metadata_by_nasa_id: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Normalize NASA search results with externally fetched asset manifests."""
    manifests = manifests_by_nasa_id or {}
    metadata_locations = metadata_by_nasa_id or {}
    candidates: list[dict[str, Any]] = []
    for search_record in extract_search_records(payload):
        data = dict(search_record["data"])
        preview_url = choose_preview_url(search_record["item"])
        if preview_url:
            data["preview_url"] = preview_url
        nasa_id = _string(data.get("nasa_id"))
        candidates.extend(
            normalize_record(
                data,
                asset_manifest=manifests.get(nasa_id or ""),
                metadata_location=metadata_locations.get(nasa_id or ""),
            )
        )
    return candidates


def enrich_search_data_with_dimensions(item: dict[str, Any]) -> dict[str, Any]:
    """Extract first data record and add best link dimensions for tests/replay."""
    data = dict(extract_item_data(item))
    width = _link_dimension(item, "width")
    height = _link_dimension(item, "height")
    if width is not None:
        data["width"] = width
    if height is not None:
        data["height"] = height
    preview_url = choose_preview_url(item)
    if preview_url:
        data["preview_url"] = preview_url
    return data


def mandatory_field_warnings(normalized: dict[str, Any]) -> list[str]:
    """Return missing-field warnings for NASA discovery candidates."""
    required = (
        "record_id",
        "title",
        "rights_uri",
        "source_url",
        "representative_media_url",
        "nasa_id",
        "nasa_center",
        "nasa_rights_basis",
    )
    return [field for field in required if not normalized.get(field)]
