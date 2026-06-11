"""Read-only GeoNames API client helpers."""
from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx

from .config import settings


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_geonames_id(value: str | int | None) -> str | None:
    """Normalize a GeoNames identifier."""
    text = _string(value)
    if not text:
        return None
    return text if text.isdigit() else None


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable GeoNames request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in params.items()
        if value is not None and value != ""
    }
    return dict(sorted(cleaned.items()))


def build_api_url(path: str) -> str:
    """Build a GeoNames API URL from a path."""
    return f"{settings.geonames_api_base_url.rstrip('/')}/{path.lstrip('/')}"


def build_lookup_params(
    geonames_id: str | int,
    *,
    username: str | None = None,
) -> dict[str, str]:
    """Build deterministic getJSON parameters."""
    normalized_id = normalize_geonames_id(geonames_id)
    if not normalized_id:
        raise ValueError("missing_geonames_id")
    user = _string(username) or settings.geonames_username
    return canonical_request_params({"geonameId": normalized_id, "username": user})


def build_search_params(
    query: str,
    *,
    country: str | None = None,
    feature_code: str | None = None,
    max_rows: int | None = None,
    username: str | None = None,
) -> dict[str, str]:
    """Build deterministic searchJSON parameters."""
    text = _string(query)
    if not text:
        raise ValueError("missing_query")
    rows = settings.geonames_page_size if max_rows is None else max_rows
    if rows < 1 or rows > 1000:
        raise ValueError("invalid_max_rows")
    user = _string(username) or settings.geonames_username
    return canonical_request_params(
        {
            "country": country,
            "fcode": feature_code,
            "maxRows": rows,
            "q": text,
            "username": user,
        }
    )


def build_hierarchy_params(
    geonames_id: str | int,
    *,
    username: str | None = None,
) -> dict[str, str]:
    """Build deterministic hierarchyJSON parameters."""
    return build_lookup_params(geonames_id, username=username)


def request_url(path: str, params: dict[str, Any]) -> str:
    """Build a replay/debug GeoNames request URL."""
    clean = canonical_request_params(params)
    return f"{build_api_url(path)}?{urlencode(clean)}" if clean else build_api_url(path)


async def _get_json(
    path: str,
    *,
    params: dict[str, Any],
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    clean = canonical_request_params(params)
    url = build_api_url(path)
    if http_client is not None:
        response = await http_client.get(url, params=clean or None)
        response.raise_for_status()
        return response.json()
    async with httpx.AsyncClient(timeout=settings.geonames_fetch_timeout_seconds) as client:
        response = await client.get(url, params=clean or None)
        response.raise_for_status()
        return response.json()


async def search_places(
    query: str,
    *,
    country: str | None = None,
    feature_code: str | None = None,
    max_rows: int | None = None,
    username: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search GeoNames places by name."""
    return await _get_json(
        "/searchJSON",
        params=build_search_params(
            query,
            country=country,
            feature_code=feature_code,
            max_rows=max_rows,
            username=username,
        ),
        http_client=http_client,
    )


async def fetch_place(
    geonames_id: str | int,
    *,
    username: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one GeoNames place by geonameId."""
    return await _get_json(
        "/getJSON",
        params=build_lookup_params(geonames_id, username=username),
        http_client=http_client,
    )


async def fetch_hierarchy(
    geonames_id: str | int,
    *,
    username: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch the GeoNames hierarchy for one place."""
    return await _get_json(
        "/hierarchyJSON",
        params=build_hierarchy_params(geonames_id, username=username),
        http_client=http_client,
    )


def extract_results(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Extract GeoNames search results."""
    if not isinstance(payload, dict):
        return []
    results = payload.get("geonames")
    return [item for item in results if isinstance(item, dict)] if isinstance(results, list) else []


def extract_first_geonames_id(payload: dict[str, Any] | None) -> str | None:
    """Extract the first GeoNames ID from a search response."""
    for item in extract_results(payload):
        geonames_id = normalize_geonames_id(item.get("geonameId"))
        if geonames_id:
            return geonames_id
    return None

