"""Read-only Wikidata Action API client helpers."""
from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlencode

import httpx

from .config import USER_AGENT, settings

QID_RE = re.compile(r"^Q[1-9][0-9]*$")


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_qid(value: str | int | None) -> str | None:
    """Normalize a Wikidata QID or bare numeric ID."""
    text = _string(value)
    if not text:
        return None
    if text.isdigit():
        text = f"Q{text}"
    text = text.upper()
    return text if QID_RE.match(text) else None


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable Wikidata request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in params.items()
        if value is not None and value != ""
    }
    return dict(sorted(cleaned.items()))


def build_headers() -> dict[str, str]:
    """Build deterministic Wikidata request headers."""
    return {"User-Agent": settings.wikidata_user_agent or USER_AGENT}


def build_entity_params(
    qid: str | int,
    *,
    language: str | None = None,
) -> dict[str, str]:
    """Build Action API params for one entity lookup."""
    normalized_qid = normalize_qid(qid)
    if not normalized_qid:
        raise ValueError("missing_qid")
    lang = _string(language) or settings.wikidata_default_language
    return canonical_request_params(
        {
            "action": "wbgetentities",
            "format": "json",
            "ids": normalized_qid,
            "languages": lang,
            "props": "labels|descriptions|aliases|claims|sitelinks",
        }
    )


def build_search_params(
    query: str,
    *,
    language: str | None = None,
    limit: int = 5,
) -> dict[str, str]:
    """Build Action API params for QID search."""
    text = _string(query)
    if not text:
        raise ValueError("missing_query")
    if limit < 1 or limit > 50:
        raise ValueError("invalid_limit")
    lang = _string(language) or settings.wikidata_default_language
    return canonical_request_params(
        {
            "action": "wbsearchentities",
            "format": "json",
            "language": lang,
            "limit": limit,
            "search": text,
        }
    )


def request_url(params: dict[str, Any]) -> str:
    """Build a replay/debug Action API request URL."""
    clean = canonical_request_params(params)
    return f"{settings.wikidata_api_base_url}?{urlencode(clean)}"


async def _get_json(
    params: dict[str, Any],
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    clean = canonical_request_params(params)
    if http_client is not None:
        response = await http_client.get(
            settings.wikidata_api_base_url,
            params=clean,
            headers=build_headers(),
        )
        response.raise_for_status()
        return response.json()
    async with httpx.AsyncClient(timeout=settings.wikidata_fetch_timeout_seconds) as client:
        response = await client.get(
            settings.wikidata_api_base_url,
            params=clean,
            headers=build_headers(),
        )
        response.raise_for_status()
        return response.json()


async def search_entities(
    query: str,
    *,
    language: str | None = None,
    limit: int = 5,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search Wikidata entities by label."""
    return await _get_json(
        build_search_params(query, language=language, limit=limit),
        http_client=http_client,
    )


async def fetch_entity(
    qid: str | int,
    *,
    language: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one Wikidata entity by QID."""
    return await _get_json(
        build_entity_params(qid, language=language),
        http_client=http_client,
    )


def extract_entity(payload: dict[str, Any] | None, qid: str | int | None = None) -> dict[str, Any]:
    """Extract one entity object from a wbgetentities response."""
    if not isinstance(payload, dict):
        return {}
    entities = payload.get("entities")
    if not isinstance(entities, dict):
        return {}
    normalized_qid = normalize_qid(qid)
    if normalized_qid and isinstance(entities.get(normalized_qid), dict):
        return entities[normalized_qid]
    for entity in entities.values():
        if isinstance(entity, dict):
            return entity
    return {}


def extract_first_qid(payload: dict[str, Any] | None) -> str | None:
    """Extract the first QID from a wbsearchentities response."""
    if not isinstance(payload, dict):
        return None
    results = payload.get("search")
    if not isinstance(results, list):
        return None
    for item in results:
        if isinstance(item, dict):
            qid = normalize_qid(item.get("id"))
            if qid:
                return qid
    return None

