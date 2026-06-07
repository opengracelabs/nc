"""Rijksmuseum Search API client."""
from __future__ import annotations

from typing import Any

import httpx

from .config import settings


def _drop_none(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


async def search_collection(
    *,
    about_actor: str | None = None,
    creator: str | None = None,
    creation_date: str | None = None,
    description: str | None = None,
    image_available: bool | None = None,
    material: str | None = None,
    member_of_set_id: str | None = None,
    object_number: str | None = None,
    page_token: str | None = None,
    technique: str | None = None,
    title: str | None = None,
    type_: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search Rijksmuseum collection objects using the Linked Art Search endpoint."""
    params = _drop_none(
        {
            "aboutActor": about_actor,
            "creator": creator,
            "creationDate": creation_date,
            "description": description,
            "imageAvailable": str(image_available).lower() if image_available is not None else None,
            "material": material,
            "memberOfSetId": member_of_set_id,
            "objectNumber": object_number,
            "pageToken": page_token,
            "technique": technique,
            "title": title,
            "type": type_,
        }
    )

    if http_client is not None:
        response = await http_client.get(settings.rijksmuseum_search_base_url, params=params)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(timeout=settings.rijksmuseum_fetch_timeout_seconds) as client:
        response = await client.get(settings.rijksmuseum_search_base_url, params=params)
        response.raise_for_status()
        return response.json()


def extract_lod_ids(search_response: dict[str, Any]) -> list[str]:
    """Extract Rijksmuseum Linked Open Data IDs from a Search response."""
    ids: list[str] = []
    for item in search_response.get("orderedItems", []):
        if isinstance(item, dict) and item.get("id"):
            ids.append(str(item["id"]))
    return ids


def next_page_token(search_response: dict[str, Any]) -> str | None:
    """Extract the opaque Search page token from the next page URL, when present."""
    next_page = search_response.get("next")
    if not isinstance(next_page, dict) or not next_page.get("id"):
        return None
    url = httpx.URL(str(next_page["id"]))
    return url.params.get("pageToken")
