"""Read-only GBIF API client helpers."""
from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx

from .config import USER_AGENT, settings


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable GBIF request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in params.items()
        if value is not None and value != ""
    }
    return dict(sorted(cleaned.items()))


def build_headers() -> dict[str, str]:
    """Build deterministic GBIF request headers."""
    return {"User-Agent": USER_AGENT}


def build_api_url(path: str) -> str:
    """Build a GBIF API URL from a path."""
    return f"{settings.gbif_api_base_url.rstrip('/')}/{path.lstrip('/')}"


def build_species_match_params(
    *,
    scientific_name: str,
    rank: str | None = None,
    kingdom: str | None = None,
) -> dict[str, str]:
    """Build deterministic GBIF species match parameters."""
    if not _string(scientific_name):
        raise ValueError("missing_scientific_name")
    return canonical_request_params(
        {
            "kingdom": kingdom,
            "name": scientific_name,
            "rank": rank,
        }
    )


def build_occurrence_search_params(
    *,
    taxon_key: str | int | None = None,
    country: str | None = None,
    geometry: str | None = None,
    limit: int | None = None,
    offset: int = 0,
    has_coordinate: bool | None = True,
) -> dict[str, str]:
    """Build deterministic GBIF occurrence search parameters."""
    if offset < 0:
        raise ValueError("invalid_offset")
    page_limit = settings.gbif_page_size if limit is None else limit
    if page_limit < 1 or page_limit > 300:
        raise ValueError("invalid_limit")
    return canonical_request_params(
        {
            "country": country,
            "geometry": geometry,
            "hasCoordinate": str(has_coordinate).lower() if has_coordinate is not None else None,
            "limit": page_limit,
            "offset": offset,
            "taxonKey": taxon_key,
        }
    )


def request_url(path: str, params: dict[str, Any] | None = None) -> str:
    """Build a replay/debug GBIF request URL."""
    clean = canonical_request_params(params or {})
    base = build_api_url(path)
    return f"{base}?{urlencode(clean)}" if clean else base


async def _get_json(
    path: str,
    *,
    params: dict[str, Any] | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    clean = canonical_request_params(params or {})
    url = build_api_url(path)
    if http_client is not None:
        response = await http_client.get(url, params=clean or None, headers=build_headers())
        response.raise_for_status()
        return response.json()
    async with httpx.AsyncClient(timeout=settings.gbif_fetch_timeout_seconds) as client:
        response = await client.get(url, params=clean or None, headers=build_headers())
        response.raise_for_status()
        return response.json()


async def species_match(
    scientific_name: str,
    *,
    rank: str | None = None,
    kingdom: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Call GBIF Species Match for one scientific name."""
    return await _get_json(
        "/species/match",
        params=build_species_match_params(
            scientific_name=scientific_name,
            rank=rank,
            kingdom=kingdom,
        ),
        http_client=http_client,
    )


async def fetch_species(
    taxon_key: str | int,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one GBIF species usage record."""
    if not _string(taxon_key):
        raise ValueError("missing_taxon_key")
    return await _get_json(f"/species/{taxon_key}", http_client=http_client)


async def search_occurrences(
    *,
    taxon_key: str | int | None = None,
    country: str | None = None,
    geometry: str | None = None,
    limit: int | None = None,
    offset: int = 0,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search GBIF occurrences for identity/place evidence."""
    return await _get_json(
        "/occurrence/search",
        params=build_occurrence_search_params(
            taxon_key=taxon_key,
            country=country,
            geometry=geometry,
            limit=limit,
            offset=offset,
        ),
        http_client=http_client,
    )


def extract_results(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Extract GBIF search results from a paged response."""
    if not isinstance(payload, dict):
        return []
    results = payload.get("results")
    return [item for item in results if isinstance(item, dict)] if isinstance(results, list) else []


def extract_count(payload: dict[str, Any] | None) -> int:
    """Extract GBIF total result count."""
    if not isinstance(payload, dict):
        return 0
    try:
        return int(payload.get("count") or 0)
    except (TypeError, ValueError):
        return 0

