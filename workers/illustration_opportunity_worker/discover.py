"""BHL-first illustration opportunity discovery.

BHL is the primary discovery source. GBIF validates place relevance only, and
Wikidata supplies context only. The output is an Illustration Opportunity.
"""
from __future__ import annotations

from typing import Any

from .rank import score_illustration_opportunity

_ALLOWED_RIGHTS = {"Public Domain", "CC0"}
_WORKER_ID = "illustration_opportunity_worker:v0.3.1"


def _first_text(*values: Any) -> str | None:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item.strip():
                    return item.strip()
                if isinstance(item, dict):
                    text = _first_text(
                        item.get("Name"),
                        item.get("FullName"),
                        item.get("CreatorName"),
                    )
                    if text:
                        return text
    return None


def _publication_year(record: dict[str, Any]) -> int | None:
    for key in ("Year", "PublicationYear", "Date", "VolumeInfo"):
        value = record.get(key)
        if value is None:
            continue
        text = str(value)
        for idx in range(0, max(len(text) - 3, 0)):
            part = text[idx : idx + 4]
            if part.isdigit():
                year = int(part)
                if 1400 <= year <= 2100:
                    return year
    return None


def _rights_status(record: dict[str, Any]) -> str | None:
    value = _first_text(
        record.get("Rights"),
        record.get("RightsStatus"),
        record.get("License"),
        record.get("CopyrightStatus"),
    )
    if not value:
        return None
    normalized = value.lower()
    if "cc0" in normalized:
        return "CC0"
    if "public domain" in normalized or normalized == "pd":
        return "Public Domain"
    return None


def _rights_url(record: dict[str, Any]) -> str | None:
    return _first_text(
        record.get("RightsUrl"),
        record.get("LicenseUrl"),
        record.get("SourceUrl"),
        record.get("PageUrl"),
        record.get("ItemUrl"),
    )


def _image_quality(record: dict[str, Any]) -> float:
    width = float(record.get("Width") or record.get("ImageWidth") or 0)
    height = float(record.get("Height") or record.get("ImageHeight") or 0)
    if width >= 2400 and height >= 2400:
        return 1.0
    if width >= 1600 and height >= 1600:
        return 0.85
    if width >= 1000 and height >= 1000:
        return 0.7
    return 0.55


def _historical_base(year: int | None) -> float:
    if year is None:
        return 0.45
    if 1750 <= year <= 1900:
        return 0.95
    if 1600 <= year < 1750 or 1900 < year <= 1930:
        return 0.65
    return 0.35


def build_illustration_opportunity(
    *,
    place_id: Any,
    concept_id: Any,
    taxon_name: str,
    bhl_record: dict[str, Any],
    gbif_validation: dict[str, Any] | None = None,
    wikidata_context: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    rights = _rights_status(bhl_record)
    rights_url = _rights_url(bhl_record)
    if rights not in _ALLOWED_RIGHTS:
        return None

    bhl_item_id = _first_text(
        bhl_record.get("ItemID"),
        bhl_record.get("ItemId"),
        bhl_record.get("item_id"),
    )
    bhl_page_id = _first_text(
        bhl_record.get("PageID"),
        bhl_record.get("PageId"),
        bhl_record.get("page_id"),
    )
    source_url = _first_text(
        bhl_record.get("PageUrl"),
        bhl_record.get("SourceUrl"),
        bhl_record.get("ItemUrl"),
    )
    publication_title = _first_text(bhl_record.get("Title"), bhl_record.get("ItemTitle"))
    if not bhl_item_id or not bhl_page_id or not publication_title:
        return None

    year = _publication_year(bhl_record)
    illustrator = _first_text(
        bhl_record.get("Illustrator"),
        bhl_record.get("Contributors"),
        bhl_record.get("Authors"),
        bhl_record.get("Creators"),
    )
    place_relevance = float((gbif_validation or {}).get("place_relevance_score", 0.72))
    commercial_value = float(bhl_record.get("CommercialValueScore") or 0.78)
    candidate = {
        "taxon_name": taxon_name,
        "publication_title": publication_title,
        "illustrator": illustrator,
        "publication_year": year,
        "source_url": source_url,
        "rights_status": rights,
        "rights_source_url": rights_url,
        "rights_verified_by": "bhl_metadata",
        "illustration_quality_score": _image_quality(bhl_record),
        "place_relevance_score": place_relevance,
        "historical_significance_score": _historical_base(year),
        "commercial_value_score": commercial_value,
    }
    scored = score_illustration_opportunity(candidate)
    if scored is None:
        return None

    source_record_id = f"item:{bhl_item_id}:page:{bhl_page_id}"
    scored.update({
        "concept_id": concept_id,
        "source": "bhl",
        "source_record_id": source_record_id,
        "source_url": source_url,
        "bhl_item_id": bhl_item_id,
        "bhl_page_id": bhl_page_id,
        "title": _first_text(bhl_record.get("PageTitle"), bhl_record.get("Title")),
        "rights_verified_by": "bhl_metadata",
        "evidence": [
            {
                "source": "bhl",
                "evidence_type": "rights",
                "source_url": rights_url,
                "payload": {"rights_status": rights},
            },
            {
                "source": "bhl",
                "evidence_type": "illustration",
                "source_url": source_url,
                "payload": bhl_record,
            },
        ],
        "place_link": {
            "place_id": place_id,
            "relevance_score": place_relevance,
            "evidence_summary": "GBIF validates place relevance; Wikidata supplies context only.",
            "provenance": {
                "prov:wasGeneratedBy": _WORKER_ID,
                "gbif_validation": gbif_validation or {},
                "wikidata_context": wikidata_context or {},
            },
        },
    })
    if gbif_validation:
        scored["evidence"].append({
            "source": "gbif",
            "evidence_type": "place_relevance",
            "source_url": gbif_validation.get("source_url") or "https://www.gbif.org",
            "payload": gbif_validation,
        })
    if wikidata_context:
        scored["evidence"].append({
            "source": "wikidata",
            "evidence_type": "taxonomic_context",
            "source_url": wikidata_context.get("source_url") or "https://www.wikidata.org",
            "payload": wikidata_context,
        })
    scored["provenance"] = {
        **scored["provenance"],
        "prov:wasGeneratedBy": _WORKER_ID,
        "source_roles": {
            "bhl": "primary_discovery",
            "gbif": "validation_only",
            "wikidata": "context_only",
        },
    }
    return scored
