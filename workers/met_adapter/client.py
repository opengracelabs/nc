"""Metropolitan Museum of Art Open Access API client."""
from __future__ import annotations

from typing import Any

import httpx

from .config import settings


def _drop_none(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def _bool(value: bool | None) -> str | None:
    if value is None:
        return None
    return str(value).lower()


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in _drop_none(params).items()
        if value != ""
    }
    return dict(sorted(cleaned.items()))


def build_object_url(object_id: int | str) -> str:
    """Build the per-object API URL for a Met object ID."""
    return f"{settings.met_api_base_url}/objects/{str(object_id).strip()}"


async def _get_json(
    path: str,
    *,
    params: dict[str, Any] | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    url = f"{settings.met_api_base_url}{path}"
    headers = {"User-Agent": settings.met_user_agent}
    request_params = canonical_request_params(params or {})

    if http_client is not None:
        response = await http_client.get(url, params=request_params, headers=headers)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(timeout=settings.met_fetch_timeout_seconds) as client:
        response = await client.get(url, params=request_params, headers=headers)
        response.raise_for_status()
        return response.json()


async def fetch_objects(
    *,
    department_ids: int | str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch object IDs from the Met /objects endpoint.

    Department-scoped enumeration is authorized for Sprint 1 connectivity.
    Full-collection enumeration remains a caller decision; this client only wraps
    the endpoint and performs no persistence.
    """
    return await _get_json(
        "/objects",
        params={"departmentIds": department_ids},
        http_client=http_client,
    )


async def fetch_object(
    object_id: int | str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one full Met object payload by objectID."""
    cleaned = str(object_id).strip()
    if not cleaned:
        raise ValueError("missing_object_id")
    return await _get_json(f"/objects/{cleaned}", http_client=http_client)


async def search_objects(
    query: str,
    *,
    is_public_domain: bool | None = None,
    department_id: int | str | None = None,
    title: bool | None = None,
    tags: bool | None = None,
    medium: str | None = None,
    has_images: bool | None = None,
    geo_location: str | None = None,
    date_begin: int | None = None,
    date_end: int | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search Met object IDs using the /search endpoint."""
    cleaned_query = query.strip()
    if not cleaned_query:
        raise ValueError("missing_query")

    return await _get_json(
        "/search",
        params={
            "q": cleaned_query,
            "isPublicDomain": _bool(is_public_domain),
            "departmentId": department_id,
            "title": _bool(title),
            "tags": _bool(tags),
            "medium": medium,
            "hasImages": _bool(has_images),
            "geoLocation": geo_location,
            "dateBegin": date_begin,
            "dateEnd": date_end,
        },
        http_client=http_client,
    )


def extract_object_ids(response: dict[str, Any]) -> list[int]:
    """Extract integer object IDs from /objects or /search responses."""
    ids = response.get("objectIDs")
    if not isinstance(ids, list):
        return []

    extracted: list[int] = []
    for value in ids:
        if isinstance(value, bool):
            continue
        try:
            extracted.append(int(value))
        except (TypeError, ValueError):
            continue
    return extracted

