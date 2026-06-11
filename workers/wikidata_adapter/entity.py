"""Wikidata QID and entity resolver helpers."""
from __future__ import annotations

from typing import Any

from .client import extract_first_qid, fetch_entity, normalize_qid, search_entities
from .normalize import normalize_entity_payload


async def resolve_qid(
    query: str | int,
    *,
    language: str | None = None,
    http_client: Any | None = None,
) -> str:
    """Resolve a QID from an existing QID, numeric ID, or label search."""
    qid = normalize_qid(query)
    if qid:
        return qid
    payload = await search_entities(
        str(query),
        language=language,
        limit=1,
        http_client=http_client,
    )
    resolved = extract_first_qid(payload)
    if not resolved:
        raise ValueError("qid_not_resolved")
    return resolved


async def resolve_entity(
    query: str | int,
    *,
    language: str | None = None,
    http_client: Any | None = None,
) -> dict[str, Any]:
    """Resolve a Wikidata entity and normalize identity/context evidence."""
    qid = await resolve_qid(query, language=language, http_client=http_client)
    payload = await fetch_entity(qid, language=language, http_client=http_client)
    return normalize_entity_payload(payload, qid=qid, language=language or "en")


async def resolve_place(
    query: str | int,
    *,
    language: str | None = None,
    http_client: Any | None = None,
) -> dict[str, Any]:
    """Resolve a place entity as Wikidata context evidence."""
    return await resolve_entity(query, language=language, http_client=http_client)


async def resolve_person(
    query: str | int,
    *,
    language: str | None = None,
    http_client: Any | None = None,
) -> dict[str, Any]:
    """Resolve a person entity as Wikidata context evidence."""
    return await resolve_entity(query, language=language, http_client=http_client)


async def resolve_artwork(
    query: str | int,
    *,
    language: str | None = None,
    http_client: Any | None = None,
) -> dict[str, Any]:
    """Resolve an artwork/work entity as Wikidata context evidence."""
    return await resolve_entity(query, language=language, http_client=http_client)


async def resolve_species(
    query: str | int,
    *,
    language: str | None = None,
    http_client: Any | None = None,
) -> dict[str, Any]:
    """Resolve a taxon entity as Wikidata context evidence."""
    return await resolve_entity(query, language=language, http_client=http_client)

