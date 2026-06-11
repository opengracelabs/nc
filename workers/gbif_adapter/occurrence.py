"""GBIF occurrence evidence helpers."""
from __future__ import annotations

from typing import Any

from .client import extract_count, extract_results, search_occurrences
from .config import OCCURRENCE_COUNT_CAP, settings
from .normalize import normalize_occurrence_payload
from .rights import classify_license


def cap_occurrence_count(count: int | None, *, cap: int = OCCURRENCE_COUNT_CAP) -> int:
    """Cap GBIF occurrence count so evidence cannot become a popularity signal."""
    raw = max(int(count or 0), 0)
    return min(raw, cap)


def normalize_occurrence(payload: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize one GBIF occurrence with license classification."""
    license_value = payload.get("license") if isinstance(payload, dict) else None
    return normalize_occurrence_payload(payload, rights=classify_license(license_value))


def normalize_occurrence_search_payload(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Normalize all occurrence results from a GBIF search response."""
    return [normalize_occurrence(item) for item in extract_results(payload)]


def summarize_place_relevance(payload: dict[str, Any] | None) -> dict[str, Any]:
    """Summarize bounded GBIF occurrence evidence for place/taxon validation."""
    raw_count = extract_count(payload)
    normalized = normalize_occurrence_search_payload(payload)
    return {
        "source": "gbif",
        "source_role": "validation_only",
        "occurrence_count": raw_count,
        "occurrence_count_cap": settings.gbif_occurrence_count_cap,
        "occurrence_count_capped": cap_occurrence_count(
            raw_count,
            cap=settings.gbif_occurrence_count_cap,
        ),
        "evidence_count": len(normalized),
        "taxon_keys": sorted(
            {
                item["gbif_taxon_key"]
                for item in normalized
                if item.get("gbif_taxon_key")
            }
        ),
    }


async def search_occurrence_evidence(
    *,
    taxon_key: str | int | None = None,
    country: str | None = None,
    geometry: str | None = None,
    limit: int | None = None,
    offset: int = 0,
    http_client: Any | None = None,
) -> list[dict[str, Any]]:
    """Search GBIF occurrences and return normalized evidence records."""
    payload = await search_occurrences(
        taxon_key=taxon_key,
        country=country,
        geometry=geometry,
        limit=limit,
        offset=offset,
        http_client=http_client,
    )
    return normalize_occurrence_search_payload(payload)

