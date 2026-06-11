"""Read-only NOAA image discovery client helpers.

Sprint 1 uses Flickr as the confirmed programmatic pilot surface while retaining
NOAA Photo Library extraction helpers for fixture-backed discovery. This module
does not write to NC storage.
"""
from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx

from .config import (
    DEFAULT_FLICKR_USER_ID,
    FLICKR_API_BASE_URL,
    FLICKR_PHOTO_PAGE_BASE_URL,
    PHOTOLIB_BASE_URL,
    USER_AGENT,
    settings,
)

FLICKR_LICENSE_LABELS = {
    "0": "All Rights Reserved",
    "1": "CC BY-NC-SA",
    "2": "CC BY-NC",
    "3": "CC BY-NC-ND",
    "4": "CC BY",
    "5": "CC BY-SA",
    "6": "CC BY-ND",
    "7": "No known copyright restrictions",
    "8": "United States Government Work",
    "9": "Public Domain Dedication",
    "10": "Public Domain Mark",
}


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in params.items()
        if value is not None and value != ""
    }
    return dict(sorted(cleaned.items()))


def build_headers() -> dict[str, str]:
    """Build deterministic request headers for NOAA discovery reads."""
    return {"User-Agent": USER_AGENT}


def build_flickr_rest_url(params: dict[str, Any] | None = None) -> str:
    """Build a Flickr REST URL for debugging, replay, and client requests."""
    clean = canonical_request_params(params or {})
    return f"{FLICKR_API_BASE_URL}?{urlencode(clean)}" if clean else FLICKR_API_BASE_URL


def build_public_photo_page_url(owner: str, photo_id: str | int) -> str:
    """Build the public Flickr photo page URL from API identifiers."""
    owner_text = _string(owner)
    photo_text = _string(photo_id)
    if not owner_text:
        raise ValueError("missing_owner")
    if not photo_text:
        raise ValueError("missing_photo_id")
    return f"{FLICKR_PHOTO_PAGE_BASE_URL}/{owner_text}/{photo_text}"


def build_people_get_public_photos_params(
    *,
    api_key: str,
    user_id: str = DEFAULT_FLICKR_USER_ID,
    page: int = 1,
    per_page: int = 100,
    tags: str | None = None,
    extras: str | None = None,
) -> dict[str, str]:
    """Build deterministic Flickr public-photo search params."""
    if page < 1:
        raise ValueError("invalid_page")
    if per_page < 1 or per_page > 500:
        raise ValueError("invalid_per_page")
    if not _string(api_key):
        raise ValueError("missing_api_key")
    return canonical_request_params(
        {
            "api_key": api_key,
            "extras": extras
            or (
                "description,license,date_upload,date_taken,owner_name,original_format,"
                "last_update,geo,tags,machine_tags,o_dims,views,media,path_alias,"
                "url_sq,url_t,url_s,url_q,url_n,url_z,url_c,url_l,url_o"
            ),
            "format": "json",
            "method": "flickr.people.getPublicPhotos",
            "nojsoncallback": "1",
            "page": page,
            "per_page": per_page,
            "safe_search": "1",
            "tags": tags,
            "user_id": user_id,
        }
    )


async def fetch_public_photos(
    *,
    api_key: str,
    user_id: str = DEFAULT_FLICKR_USER_ID,
    page: int = 1,
    per_page: int = 100,
    tags: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one page of public NOAA Flickr photos."""
    params = build_people_get_public_photos_params(
        api_key=api_key,
        user_id=user_id,
        page=page,
        per_page=per_page,
        tags=tags,
    )
    if http_client is not None:
        response = await http_client.get(
            FLICKR_API_BASE_URL,
            params=params,
            headers=build_headers(),
        )
        response.raise_for_status()
        return response.json()
    async with httpx.AsyncClient(timeout=settings.noaa_fetch_timeout_seconds) as client:
        response = await client.get(FLICKR_API_BASE_URL, params=params, headers=build_headers())
        response.raise_for_status()
        return response.json()


def extract_flickr_photos(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Extract Flickr photo objects from a public-photo response."""
    photos = _as_dict(_as_dict(payload).get("photos")).get("photo")
    return [item for item in photos if isinstance(item, dict)] if isinstance(photos, list) else []


def extract_total(payload: dict[str, Any] | None) -> int:
    """Extract Flickr total count for replay checks."""
    total = _as_dict(_as_dict(payload).get("photos")).get("total")
    try:
        return int(total)
    except (TypeError, ValueError):
        return 0


def choose_image_url(record: dict[str, Any] | None) -> str | None:
    """Choose the best available Flickr image URL without constructing one."""
    data = _as_dict(record)
    for key in ("url_o", "url_l", "url_c", "url_z"):
        value = _string(data.get(key))
        if value:
            return value
    return None


def extract_description(record: dict[str, Any] | None) -> str | None:
    """Extract Flickr's nested description content."""
    value = _as_dict(record).get("description")
    if isinstance(value, dict):
        return _string(value.get("_content"))
    return _string(value)


def extract_credit(record: dict[str, Any] | None) -> str | None:
    """Extract a NOAA credit line from known API/fixture fields."""
    data = _as_dict(record)
    explicit_credit = _string(data.get("credit"))
    if explicit_credit:
        return explicit_credit
    description = extract_description(data)
    if not description:
        return None
    for prefix in ("Credit:", "Photo credit:", "Image credit:", "Courtesy:"):
        marker_index = description.lower().find(prefix.lower())
        if marker_index >= 0:
            line = description[marker_index + len(prefix) :].splitlines()[0]
            return _string(line.strip(" .:-"))
    return None


def extract_license_label(record: dict[str, Any] | None) -> str | None:
    """Return Flickr's license label for fixture and API records."""
    data = _as_dict(record)
    explicit = _string(data.get("license_label"))
    if explicit:
        return explicit
    license_id = _string(data.get("license"))
    return FLICKR_LICENSE_LABELS.get(license_id or "")


def flickr_record_to_discovery_payload(record: dict[str, Any]) -> dict[str, Any]:
    """Convert a Flickr photo object into the adapter's source payload shape."""
    photo_id = _string(record.get("id"))
    owner = _string(record.get("owner"))
    source_url = None
    if photo_id and owner:
        source_url = build_public_photo_page_url(owner, photo_id)
    return {
        **record,
        "source_system": "flickr",
        "source_record_id": photo_id,
        "source_url": _string(record.get("source_url")) or source_url,
        "image_url": choose_image_url(record),
        "description": extract_description(record),
        "credit": extract_credit(record),
        "license_id": _string(record.get("license")),
        "license_label": extract_license_label(record),
    }


def photolib_record_to_discovery_payload(record: dict[str, Any]) -> dict[str, Any]:
    """Normalize a fixture-backed NOAA Photo Library record into source payload shape."""
    record_id = _string(record.get("id") or record.get("source_record_id"))
    source_url = _string(record.get("source_url") or record.get("url"))
    if record_id and source_url is None:
        source_url = f"{PHOTOLIB_BASE_URL.rstrip('/')}/{record_id.lstrip('/')}"
    return {
        **record,
        "source_system": "noaa_photolib",
        "source_record_id": record_id,
        "source_url": source_url,
        "image_url": _string(record.get("image_url")),
        "credit": _string(record.get("credit")),
        "license_id": _string(record.get("license_id")),
        "license_label": _string(record.get("license_label")),
    }

