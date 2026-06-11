"""GeoNames place resolver helpers."""
from __future__ import annotations

from typing import Any

from .client import (
    extract_first_geonames_id,
    fetch_hierarchy,
    fetch_place,
    normalize_geonames_id,
    search_places,
)
from .normalize import normalize_place_payload


async def resolve_geonames_id(
    query: str | int,
    *,
    country: str | None = None,
    feature_code: str | None = None,
    username: str | None = None,
    http_client: Any | None = None,
) -> str:
    """Resolve a GeoNames ID from an existing ID or place-name search."""
    geonames_id = normalize_geonames_id(query)
    if geonames_id:
        return geonames_id
    payload = await search_places(
        str(query),
        country=country,
        feature_code=feature_code,
        max_rows=1,
        username=username,
        http_client=http_client,
    )
    resolved = extract_first_geonames_id(payload)
    if not resolved:
        raise ValueError("geonames_id_not_resolved")
    return resolved


async def resolve_place(
    query: str | int,
    *,
    country: str | None = None,
    feature_code: str | None = None,
    include_hierarchy: bool = True,
    username: str | None = None,
    http_client: Any | None = None,
) -> dict[str, Any]:
    """Resolve a GeoNames place and normalize place identity evidence."""
    geonames_id = await resolve_geonames_id(
        query,
        country=country,
        feature_code=feature_code,
        username=username,
        http_client=http_client,
    )
    place_payload = await fetch_place(geonames_id, username=username, http_client=http_client)
    hierarchy_payload = (
        await fetch_hierarchy(geonames_id, username=username, http_client=http_client)
        if include_hierarchy
        else None
    )
    return normalize_place_payload(place_payload, hierarchy_payload=hierarchy_payload)

