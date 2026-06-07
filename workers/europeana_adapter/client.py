"""Europeana Record API client."""
from __future__ import annotations

from typing import Any

import httpx

from .config import settings


async def search_records(
    query: str,
    *,
    rows: int = 50,
    cursor: str | None = None,
) -> dict[str, Any]:
    """Search Europeana records.

    Search responses are candidate discovery only. Substrate writes must use
    `fetch_record` so the full payload can be hashed and replayed.
    """
    params: dict[str, Any] = {
        "wskey": settings.europeana_api_key,
        "query": query,
        "rows": rows,
    }
    if cursor:
        params["cursor"] = cursor

    async with httpx.AsyncClient(timeout=settings.europeana_fetch_timeout_seconds) as client:
        response = await client.get(
            f"{settings.europeana_api_base_url}/search.json",
            params=params,
        )
        response.raise_for_status()
        return response.json()


async def fetch_record(record_id: str) -> dict[str, Any]:
    """Fetch a full Europeana record payload by record ID."""
    cleaned = record_id.strip("/")
    async with httpx.AsyncClient(timeout=settings.europeana_fetch_timeout_seconds) as client:
        response = await client.get(
            f"{settings.europeana_api_base_url}/{cleaned}.json",
            params={"wskey": settings.europeana_api_key},
        )
        response.raise_for_status()
        return response.json()
