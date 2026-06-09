"""Art Institute of Chicago public API client."""
from __future__ import annotations

from typing import Any

import httpx

from .config import settings

DEFAULT_FIELDS = (
    "id",
    "title",
    "is_public_domain",
    "image_id",
    "alt_image_ids",
    "date_display",
    "date_start",
    "date_end",
    "artist_display",
    "artist_title",
    "place_of_origin",
    "department_title",
    "department_id",
    "artwork_type_title",
    "medium_display",
    "subject_titles",
    "classification_titles",
    "style_titles",
    "copyright_notice",
    "main_reference_number",
    "api_link",
    "thumbnail",
)


def _drop_none(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def _fields_value(fields: list[str] | tuple[str, ...] | str | None) -> str | None:
    if fields is None:
        return None
    if isinstance(fields, str):
        return fields.strip() or None
    cleaned = [str(field).strip() for field in fields if str(field).strip()]
    return ",".join(cleaned) if cleaned else None


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in _drop_none(params).items()
        if value != ""
    }
    return dict(sorted(cleaned.items()))


def build_artwork_url(artwork_id: int | str) -> str:
    """Build the per-artwork API URL for an AIC artwork ID."""
    return f"{settings.aic_api_base_url}/artworks/{str(artwork_id).strip()}"


def build_manifest_url(artwork_id: int | str) -> str:
    """Build the IIIF Presentation manifest URL for an AIC artwork ID."""
    return f"{build_artwork_url(artwork_id)}/manifest.json"


async def _get_json(
    path_or_url: str,
    *,
    params: dict[str, Any] | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    if path_or_url.startswith("http"):
        url = path_or_url
    else:
        url = f"{settings.aic_api_base_url}{path_or_url}"
    headers = {"User-Agent": settings.aic_user_agent}
    request_params = canonical_request_params(params or {})
    request_params_or_none = request_params or None

    if http_client is not None:
        response = await http_client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(timeout=settings.aic_fetch_timeout_seconds) as client:
        response = await client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()


async def fetch_artworks(
    *,
    page: int = 1,
    limit: int | None = None,
    fields: list[str] | tuple[str, ...] | str | None = DEFAULT_FIELDS,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one paginated /artworks page."""
    return await _get_json(
        "/artworks",
        params={
            "page": page,
            "limit": limit or settings.aic_page_limit,
            "fields": _fields_value(fields),
        },
        http_client=http_client,
    )


async def fetch_artwork(
    artwork_id: int | str,
    *,
    fields: list[str] | tuple[str, ...] | str | None = DEFAULT_FIELDS,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one full AIC artwork payload by integer artwork ID."""
    cleaned = str(artwork_id).strip()
    if not cleaned:
        raise ValueError("missing_artwork_id")
    return await _get_json(
        f"/artworks/{cleaned}",
        params={"fields": _fields_value(fields)},
        http_client=http_client,
    )


async def search_artworks(
    *,
    query: str | None = None,
    public_domain: bool = True,
    page: int = 1,
    limit: int | None = None,
    fields: list[str] | tuple[str, ...] | str | None = DEFAULT_FIELDS,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search AIC artworks, defaulting to the public-domain filter."""
    params: dict[str, Any] = {
        "page": page,
        "limit": limit or settings.aic_page_limit,
        "fields": _fields_value(fields),
    }
    if query is not None and query.strip():
        params["q"] = query.strip()
    if public_domain:
        params["query[term][is_public_domain]"] = "true"

    return await _get_json("/artworks/search", params=params, http_client=http_client)


async def fetch_manifest(
    artwork_id: int | str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one AIC IIIF Presentation manifest by artwork ID."""
    cleaned = str(artwork_id).strip()
    if not cleaned:
        raise ValueError("missing_artwork_id")
    return await _get_json(f"/artworks/{cleaned}/manifest.json", http_client=http_client)


async def fetch_next_page(
    response: dict[str, Any],
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any] | None:
    """Fetch `pagination.next_url` from a prior AIC response, when present."""
    next_url = next_page_url(response)
    if not next_url:
        return None
    return await _get_json(next_url, http_client=http_client)


def next_page_url(response: dict[str, Any]) -> str | None:
    """Return the AIC pagination.next_url cursor."""
    pagination = response.get("pagination")
    if not isinstance(pagination, dict):
        return None
    value = pagination.get("next_url")
    if not isinstance(value, str):
        return None
    return value.strip() or None


def extract_artwork_ids(response: dict[str, Any]) -> list[int]:
    """Extract integer artwork IDs from /artworks or /artworks/search responses."""
    data = response.get("data")
    if not isinstance(data, list):
        return []

    ids: list[int] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        value = item.get("id")
        if isinstance(value, bool):
            continue
        try:
            ids.append(int(value))
        except (TypeError, ValueError):
            continue
    return ids

