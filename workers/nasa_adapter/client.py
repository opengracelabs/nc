"""Client helpers for NASA Image and Video Library Sprint 1.

Sprint 1 is discovery-only. It uses images-api.nasa.gov exclusively and does
not construct asset URLs from NASA IDs.
"""
from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx

from . import config as _config

SOURCE_SLUG = _config.SOURCE_SLUG
SCHEMA_STANDARD = _config.SCHEMA_STANDARD
RIGHTS_POLICY_ID = _config.RIGHTS_POLICY_ID
API_BASE_URL = _config.API_BASE_URL
USER_AGENT = _config.USER_AGENT
IMAGES_API_HOST = _config.IMAGES_API_HOST
EXCLUDED_API_HOST = _config.EXCLUDED_API_HOST
settings = _config.settings


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _api_url(path: str) -> str:
    return f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def reject_api_nasa_url(url: str) -> None:
    """Reject api.nasa.gov family URLs for this adapter."""
    lowered = url.lower()
    if f"://{EXCLUDED_API_HOST}" in lowered or f".{EXCLUDED_API_HOST}" in lowered:
        raise ValueError("api_nasa_gov_excluded")


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in params.items()
        if value is not None and value != ""
    }
    return dict(sorted(cleaned.items()))


def build_search_url() -> str:
    """Build the official NASA Image and Video Library search URL."""
    return _api_url("/search")


def build_asset_url(nasa_id: str) -> str:
    """Build the official asset manifest endpoint URL."""
    cleaned = _string(nasa_id)
    if not cleaned:
        raise ValueError("missing_nasa_id")
    return _api_url(f"/asset/{cleaned}")


def build_metadata_url(nasa_id: str) -> str:
    """Build the official metadata location endpoint URL."""
    cleaned = _string(nasa_id)
    if not cleaned:
        raise ValueError("missing_nasa_id")
    return _api_url(f"/metadata/{cleaned}")


def build_search_params(
    *,
    query: str | None = None,
    center: str | None = None,
    media_type: str = "image",
    page: int = 1,
    page_size: int = 100,
    nasa_id: str | None = None,
    keywords: str | None = None,
    year_start: str | None = None,
    year_end: str | None = None,
) -> dict[str, str]:
    """Build deterministic NASA image search parameters."""
    if page < 1:
        raise ValueError("invalid_page")
    if page_size < 1:
        raise ValueError("invalid_page_size")
    return canonical_request_params(
        {
            "center": center,
            "keywords": keywords,
            "media_type": media_type,
            "nasa_id": nasa_id,
            "page": page,
            "page_size": page_size,
            "q": query,
            "year_end": year_end,
            "year_start": year_start,
        }
    )


def build_headers() -> dict[str, str]:
    """Build deterministic NASA Image API request headers."""
    return {"User-Agent": USER_AGENT}


async def _get_json(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    reject_api_nasa_url(url)
    request_params = canonical_request_params(params or {}) or None
    if http_client is not None:
        response = await http_client.get(url, params=request_params, headers=build_headers())
        response.raise_for_status()
        return response.json()
    async with httpx.AsyncClient(timeout=settings.nasa_images_fetch_timeout_seconds) as client:
        response = await client.get(url, params=request_params, headers=build_headers())
        response.raise_for_status()
        return response.json()


async def search_assets(
    *,
    query: str | None = None,
    center: str | None = None,
    media_type: str = "image",
    page: int = 1,
    page_size: int = 100,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search image assets through images-api.nasa.gov only."""
    return await _get_json(
        build_search_url(),
        params=build_search_params(
            query=query,
            center=center,
            media_type=media_type,
            page=page,
            page_size=page_size,
        ),
        http_client=http_client,
    )


async def fetch_asset_manifest(
    nasa_id: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one NASA asset manifest via /asset/{nasa_id}."""
    return await _get_json(build_asset_url(nasa_id), http_client=http_client)


async def fetch_metadata_location(
    nasa_id: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one NASA metadata location via /metadata/{nasa_id}."""
    return await _get_json(build_metadata_url(nasa_id), http_client=http_client)


def extract_collection_items(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Extract Collection+JSON items from a NASA API response."""
    if not isinstance(payload, dict):
        return []
    collection = payload.get("collection")
    if not isinstance(collection, dict):
        return []
    items = collection.get("items")
    return [item for item in items if isinstance(item, dict)] if isinstance(items, list) else []


def extract_item_data(item: dict[str, Any]) -> dict[str, Any]:
    """Extract the first data object from a Collection+JSON item."""
    data = item.get("data")
    if isinstance(data, list):
        for entry in data:
            if isinstance(entry, dict):
                return entry
    return {}


def extract_item_links(item: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract link objects from a Collection+JSON item."""
    links = item.get("links")
    return [link for link in links if isinstance(link, dict)] if isinstance(links, list) else []


def _https_asset_url(url: str) -> str:
    if url.startswith("http://images-assets.nasa.gov/"):
        return url.replace("http://", "https://", 1)
    return url


def extract_asset_urls(manifest: dict[str, Any] | None) -> list[str]:
    """Extract asset hrefs from a /asset/{nasa_id} response."""
    urls: list[str] = []
    for item in extract_collection_items(manifest):
        href = _string(item.get("href"))
        if href:
            urls.append(_https_asset_url(href))
    return urls


def choose_asset_url(asset_urls: list[str]) -> str | None:
    """Choose an image delivery URL from a NASA asset manifest without pattern construction."""
    image_exts = (".jpg", ".jpeg", ".png", ".tif", ".tiff")
    image_urls = [url for url in asset_urls if url.lower().endswith(image_exts)]
    for token in ("~orig", "~large", "~medium", "~small", "~thumb"):
        for url in image_urls:
            if token in url.lower():
                return url
    return image_urls[0] if image_urls else None


def choose_preview_url(item: dict[str, Any]) -> str | None:
    """Return preview URL from search-result links, if supplied by NASA."""
    for link in extract_item_links(item):
        if link.get("rel") == "preview" and _string(link.get("href")):
            return str(link["href"]).strip()
    for link in extract_item_links(item):
        if _string(link.get("href")):
            return str(link["href"]).strip()
    return None


def collection_query_url(params: dict[str, Any]) -> str:
    """Build a display/debug URL for a search query."""
    clean = canonical_request_params(params)
    return f"{build_search_url()}?{urlencode(clean)}" if clean else build_search_url()
