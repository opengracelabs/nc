"""GBIF taxon identity evidence helpers."""
from __future__ import annotations

from typing import Any

from .client import fetch_species, species_match
from .normalize import normalize_taxon_payload


async def resolve_taxon_name(
    scientific_name: str,
    *,
    rank: str | None = None,
    kingdom: str | None = None,
    http_client: Any | None = None,
) -> dict[str, Any]:
    """Resolve a scientific name with GBIF Species Match and normalize evidence."""
    payload = await species_match(
        scientific_name,
        rank=rank,
        kingdom=kingdom,
        http_client=http_client,
    )
    return normalize_taxon_identity(payload)


async def fetch_taxon_identity(
    taxon_key: str | int,
    *,
    http_client: Any | None = None,
) -> dict[str, Any]:
    """Fetch one GBIF taxon usage and normalize identity evidence."""
    payload = await fetch_species(taxon_key, http_client=http_client)
    return normalize_taxon_identity(payload)


def normalize_taxon_identity(payload: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize GBIF taxon identity evidence."""
    return normalize_taxon_payload(payload)


def build_taxon_identity_evidence(payload: dict[str, Any] | None) -> dict[str, Any]:
    """Build replay-stable taxon identity evidence from a GBIF payload."""
    return normalize_taxon_identity(payload)

