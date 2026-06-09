"""Cleveland Museum of Art Open Access API client."""
from __future__ import annotations

from typing import Any

import httpx

from .config import settings

DEFAULT_FIELDS = (
    "id",
    "accession_number",
    "title",
    "share_license_status",
    "copyright",
    "images",
    "alternate_images",
    "is_highlight",
    "creation_date",
    "creation_date_earliest",
    "creation_date_latest",
    "creators",
    "culture",
    "type",
    "department",
    "collection",
    "technique",
    "find_spot",
    "description",
    "creditline",
    "url",
)


def _drop_none(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def _bool_int(value: bool | None) -> str | None:
    if value is None:
        return None
    return "1" if value else "0"


def _fields_value(fields: list[str] | tuple[str, ...] | str | None) -> str | None:
    if fields is None:
        return None
    if isinstance(fields, str):
        return fields.strip() or None
    cleaned = [str(field).strip() for field in fields if str(field).strip()]
    return ",".join(cleaned) if cleaned else None


def _validate_limit(limit: int) -> int:
    if limit < 1:
        raise ValueError("invalid_limit")
    if limit > settings.cma_max_limit:
        raise ValueError("limit_exceeds_cma_max")
    return limit


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in _drop_none(params).items()
        if value != ""
    }
    return dict(sorted(cleaned.items()))


def build_artwork_url(artwork_id: int | str) -> str:
    """Build the per-artwork API URL for a CMA artwork ID or accession number."""
    return f"{settings.cma_api_base_url}/artworks/{str(artwork_id).strip()}"


async def _get_json(
    path_or_url: str,
    *,
    params: dict[str, Any] | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    if path_or_url.startswith("http"):
        url = path_or_url
    else:
        url = f"{settings.cma_api_base_url}{path_or_url}"
    headers = {"User-Agent": settings.cma_user_agent}
    request_params = canonical_request_params(params or {})
    request_params_or_none = request_params or None

    if http_client is not None:
        response = await http_client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(timeout=settings.cma_fetch_timeout_seconds) as client:
        response = await client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()


async def fetch_artworks(
    *,
    q: str | None = None,
    skip: int = 0,
    limit: int | None = None,
    cc0: bool | None = True,
    has_image: bool | None = True,
    fields: list[str] | tuple[str, ...] | str | None = DEFAULT_FIELDS,
    sort: str | None = "id",
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one paginated CMA /artworks page."""
    if skip < 0:
        raise ValueError("invalid_skip")
    request_limit = _validate_limit(settings.cma_page_limit if limit is None else limit)
    cleaned_q = q.strip() if isinstance(q, str) else None

    return await _get_json(
        "/artworks",
        params={
            "q": cleaned_q or None,
            "skip": skip,
            "limit": request_limit,
            "cc0": _bool_int(cc0),
            "has_image": _bool_int(has_image),
            "select": _fields_value(fields),
            "orderby": sort,
        },
        http_client=http_client,
    )


async def fetch_artwork(
    artwork_id: int | str,
    *,
    fields: list[str] | tuple[str, ...] | str | None = DEFAULT_FIELDS,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one full CMA artwork payload by integer ID or accession number."""
    cleaned = str(artwork_id).strip()
    if not cleaned:
        raise ValueError("missing_artwork_id")
    return await _get_json(
        f"/artworks/{cleaned}",
        params={"select": _fields_value(fields)},
        http_client=http_client,
    )


def extract_artwork_records(response: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract artwork dictionaries from CMA list or single responses."""
    data = response.get("data")
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def extract_artwork_ids(response: dict[str, Any]) -> list[int]:
    """Extract integer artwork IDs from CMA list or single responses."""
    ids: list[int] = []
    for item in extract_artwork_records(response):
        value = item.get("id")
        if isinstance(value, bool):
            continue
        try:
            ids.append(int(value))
        except (TypeError, ValueError):
            continue
    return ids


def next_skip(response: dict[str, Any]) -> int | None:
    """Return the next skip offset, or None when the current page is terminal."""
    data = response.get("data")
    info = response.get("info")
    if not isinstance(data, list) or not isinstance(info, dict):
        return None
    params = info.get("parameters")
    if not isinstance(params, dict):
        return None
    try:
        skip = int(params.get("skip"))
        limit = int(params.get("limit"))
    except (TypeError, ValueError):
        return None
    if len(data) < limit:
        return None
    total = info.get("total")
    candidate = skip + limit
    if isinstance(total, int) and candidate >= total:
        return None
    return candidate

