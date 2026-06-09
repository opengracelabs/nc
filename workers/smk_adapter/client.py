"""Statens Museum for Kunst Open API client."""
from __future__ import annotations

from typing import Any

import httpx

from .config import settings

DEFAULT_FIELDS = (
    "object_number",
    "titles",
    "public_domain",
    "rights",
    "content_subject",
    "has_image",
    "image_thumbnail",
    "image_native",
    "image_iiif_id",
    "image_hq",
    "image_mime_type",
    "image_width",
    "image_height",
    "iiif_manifest",
    "frontend_url",
    "object_url",
    "production",
    "production_date",
    "production_dates_notes",
    "artist",
    "object_names",
    "materials",
    "techniques",
    "dimensions",
    "images",
)


def _drop_none(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def _bool(value: bool | None) -> str | None:
    if value is None:
        return None
    return str(value).lower()


def _fields_value(fields: list[str] | tuple[str, ...] | str | None) -> str | None:
    if fields is None:
        return None
    if isinstance(fields, str):
        return fields.strip() or None
    cleaned = [str(field).strip() for field in fields if str(field).strip()]
    return ",".join(cleaned) if cleaned else None


def _filters_value(
    *,
    public_domain: bool | None = None,
    has_image: bool | None = None,
    extra_filters: list[str] | tuple[str, ...] | str | None = None,
) -> str | None:
    filters: list[str] = []
    if has_image is not None:
        filters.append(f"[has_image:{_bool(has_image)}]")
    if public_domain is not None:
        filters.append(f"[public_domain:{_bool(public_domain)}]")
    if isinstance(extra_filters, str):
        if extra_filters.strip():
            filters.append(extra_filters.strip())
    elif extra_filters:
        filters.extend(str(value).strip() for value in extra_filters if str(value).strip())
    return ",".join(filters) if filters else None


def _validate_rows(rows: int) -> int:
    if rows < 1:
        raise ValueError("invalid_rows")
    if rows > settings.smk_max_rows:
        raise ValueError("rows_exceeds_smk_max")
    return rows


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in _drop_none(params).items()
        if value != ""
    }
    return dict(sorted(cleaned.items()))


def build_object_url(object_number: int | str) -> str:
    """Build the per-object API URL for an SMK object number."""
    return f"{settings.smk_api_base_url}/art/?object_number={str(object_number).strip()}"


def build_manifest_url(object_number: int | str) -> str:
    """Build the IIIF Presentation manifest URL for an SMK object number."""
    return f"{settings.smk_api_base_url}/iiif/manifest?object_number={str(object_number).strip()}"


async def _get_json(
    path_or_url: str,
    *,
    params: dict[str, Any] | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    if path_or_url.startswith("http"):
        url = path_or_url
    else:
        url = f"{settings.smk_api_base_url}{path_or_url}"
    headers = {"User-Agent": settings.smk_user_agent}
    request_params = canonical_request_params(params or {})
    request_params_or_none = request_params or None

    if http_client is not None:
        response = await http_client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(timeout=settings.smk_fetch_timeout_seconds) as client:
        response = await client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()


async def search_artworks(
    *,
    keys: str = "*",
    public_domain: bool | None = True,
    has_image: bool | None = True,
    offset: int = 0,
    rows: int | None = None,
    fields: list[str] | tuple[str, ...] | str | None = DEFAULT_FIELDS,
    lang: str | None = None,
    sort: str | None = "id",
    extra_filters: list[str] | tuple[str, ...] | str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search SMK artworks, defaulting to public-domain records with images."""
    cleaned_keys = keys.strip()
    if not cleaned_keys:
        raise ValueError("missing_keys")
    if offset < 0:
        raise ValueError("invalid_offset")
    request_rows = _validate_rows(settings.smk_page_limit if rows is None else rows)

    return await _get_json(
        "/art/search/",
        params={
            "keys": cleaned_keys,
            "filters": _filters_value(
                public_domain=public_domain,
                has_image=has_image,
                extra_filters=extra_filters,
            ),
            "offset": offset,
            "rows": request_rows,
            "fields": _fields_value(fields),
            "lang": lang or settings.smk_default_lang,
            "sort": sort,
        },
        http_client=http_client,
    )


async def fetch_object(
    object_number: int | str,
    *,
    lang: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one full SMK artwork payload by object_number."""
    cleaned = str(object_number).strip()
    if not cleaned:
        raise ValueError("missing_object_number")
    return await _get_json(
        "/art/",
        params={"object_number": cleaned, "lang": lang or settings.smk_default_lang},
        http_client=http_client,
    )


async def fetch_manifest(
    object_number: int | str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one SMK IIIF Presentation manifest by object_number."""
    cleaned = str(object_number).strip()
    if not cleaned:
        raise ValueError("missing_object_number")
    return await _get_json(
        "/iiif/manifest",
        params={"object_number": cleaned},
        http_client=http_client,
    )


def extract_items(response: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract item dictionaries from SMK search or object responses."""
    items = response.get("items")
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def extract_object_numbers(response: dict[str, Any]) -> list[str]:
    """Extract SMK object numbers from search or object responses."""
    numbers: list[str] = []
    for item in extract_items(response):
        value = item.get("object_number")
        if isinstance(value, str) and value.strip():
            numbers.append(value.strip())
    return numbers


def next_offset(response: dict[str, Any]) -> int | None:
    """Return the next search offset, or None when the current page is terminal."""
    items = response.get("items")
    offset = response.get("offset")
    rows = response.get("rows")
    if not isinstance(items, list) or not isinstance(offset, int) or not isinstance(rows, int):
        return None
    if len(items) < rows:
        return None
    found = response.get("found")
    candidate = offset + rows
    if isinstance(found, int) and candidate >= found:
        return None
    return candidate

