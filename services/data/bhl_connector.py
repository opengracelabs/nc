"""BHL connector runtime for candidate-only Asset Factory feeds."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, TypedDict

from services.data.asset_factory import (
    ASSET_FACTORY_VERSION,
    ASSET_SOURCES_DIR,
    AssetCandidate,
    normalize_asset_candidate,
    summarize_asset_factory,
)
from services.data.place_seed import normalize_place_slug
from workers.gbif_adapter.identity import normalize_taxon_identity

BHL_RUNTIME_VERSION = "NC-BHL-001-v1"
DEFAULT_BHL_SOURCE = ASSET_SOURCES_DIR / "bhl_connector_seed.json"
BHL_INSTITUTION = "Biodiversity Heritage Library"


class BhlConnectorError(ValueError):
    """Raised when BHL connector input cannot feed candidate-only assets."""


class BhlIllustrationCandidate(TypedDict):
    candidate_status: str
    source_system: str
    source_institution: str
    source_record_id: str
    source_url: str
    title: str
    creator: str
    date: str
    media_type: str
    asset_url: str
    thumbnail_url: str
    iiif_manifest_url: str
    rights_status: str
    rights_statement_uri: str
    place_slug: str
    collection_hints: list[str]
    product_hints: list[str]
    species_hints: list[str]
    theme_hints: list[str]
    width_px: int
    height_px: int
    bhl_title_id: str
    bhl_item_id: str
    bhl_page_id: str
    gbif_mapping: dict[str, Any]
    taxonomic_enrichment: dict[str, Any]


def _string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BhlConnectorError(f"{field} must be a non-empty string")
    return value.strip()


def _string_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if not isinstance(value, list):
        raise BhlConnectorError("expected a list")
    return [str(item).strip() for item in value if str(item).strip()]


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def load_bhl_source(path: Path | str = DEFAULT_BHL_SOURCE) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise BhlConnectorError("BHL source must be an object")
    if payload.get("source_system") != "BHL":
        raise BhlConnectorError("BHL source must declare source_system=BHL")
    return payload


def ingest_bhl_titles(payload: dict[str, Any]) -> list[dict[str, Any]]:
    titles = payload.get("titles")
    if not isinstance(titles, list):
        raise BhlConnectorError("BHL source must contain titles")
    normalized = []
    seen: set[str] = set()
    for raw in titles:
        if not isinstance(raw, dict):
            raise BhlConnectorError("BHL title records must be objects")
        title = {
            "title_id": _string(raw.get("title_id"), "title_id"),
            "item_id": _string(raw.get("item_id"), "item_id"),
            "title": _string(raw.get("title"), "title"),
            "creator": str(raw.get("creator") or "").strip(),
            "publication_year": str(raw.get("publication_year") or "").strip(),
            "source_url": _string(raw.get("source_url"), "source_url"),
            "rights_status": str(raw.get("rights_status") or "pending_verification").strip(),
            "rights_statement_uri": str(raw.get("rights_statement_uri") or "").strip(),
            "collection_hints": _string_list(raw.get("collection_hints")),
            "theme_hints": _string_list(raw.get("theme_hints")),
        }
        if title["item_id"] in seen:
            raise BhlConnectorError(f"duplicate BHL item_id: {title['item_id']}")
        seen.add(title["item_id"])
        normalized.append(title)
    return normalized


def ingest_bhl_pages(payload: dict[str, Any]) -> list[dict[str, Any]]:
    pages = payload.get("pages")
    if not isinstance(pages, list):
        raise BhlConnectorError("BHL source must contain pages")
    normalized = []
    seen: set[str] = set()
    for raw in pages:
        if not isinstance(raw, dict):
            raise BhlConnectorError("BHL page records must be objects")
        page = {
            "page_id": _string(raw.get("page_id"), "page_id"),
            "item_id": _string(raw.get("item_id"), "item_id"),
            "page_number": str(raw.get("page_number") or "").strip(),
            "page_type": str(raw.get("page_type") or "").strip(),
            "caption": str(raw.get("caption") or "").strip(),
            "has_illustration": bool(raw.get("has_illustration")),
            "illustration_type": str(raw.get("illustration_type") or "").strip(),
            "scientific_names": _string_list(raw.get("scientific_names")),
            "common_names": _string_list(raw.get("common_names")),
            "place_slug": normalize_place_slug(str(raw.get("place_slug") or "global")),
            "width_px": _int(raw.get("width_px")),
            "height_px": _int(raw.get("height_px")),
            "page_url": _string(raw.get("page_url"), "page_url"),
            "image_url": str(raw.get("image_url") or "").strip(),
            "thumbnail_url": str(raw.get("thumbnail_url") or "").strip(),
            "iiif_manifest_url": str(raw.get("iiif_manifest_url") or "").strip(),
            "gbif_match": raw.get("gbif_match") if isinstance(raw.get("gbif_match"), dict) else {},
        }
        if page["page_id"] in seen:
            raise BhlConnectorError(f"duplicate BHL page_id: {page['page_id']}")
        seen.add(page["page_id"])
        normalized.append(page)
    return normalized


def build_gbif_mapping(page: dict[str, Any]) -> dict[str, Any]:
    evidence = normalize_taxon_identity(page.get("gbif_match") or {})
    scientific_names = page.get("scientific_names") or []
    return {
        "mapping_status": "candidate",
        "source": "GBIF",
        "scientific_name": scientific_names[0] if scientific_names else evidence.get("canonical_name"),
        "gbif_taxon_key": evidence.get("gbif_taxon_key"),
        "accepted_taxon_key": evidence.get("accepted_taxon_key"),
        "source_url": evidence.get("source_url"),
        "darwin_core_mapping": evidence.get("darwin_core_mapping"),
        "candidate_only": True,
    }


def build_taxonomic_enrichment(page: dict[str, Any]) -> dict[str, Any]:
    evidence = normalize_taxon_identity(page.get("gbif_match") or {})
    return {
        "enrichment_status": "candidate",
        "taxonomic_source": "GBIF",
        "scientific_name": evidence.get("scientific_name"),
        "canonical_name": evidence.get("canonical_name"),
        "accepted_scientific_name": evidence.get("accepted_scientific_name"),
        "taxon_rank": evidence.get("taxon_rank"),
        "kingdom": evidence.get("kingdom"),
        "phylum": evidence.get("phylum"),
        "class": evidence.get("class"),
        "order": evidence.get("order"),
        "family": evidence.get("family"),
        "genus": evidence.get("genus"),
        "species": evidence.get("species"),
        "raw_payload_hash": evidence.get("raw_payload_hash"),
        "candidate_only": True,
    }


def extract_illustration_candidates(
    titles: list[dict[str, Any]], pages: list[dict[str, Any]]
) -> list[BhlIllustrationCandidate]:
    by_item = {title["item_id"]: title for title in titles}
    candidates: list[BhlIllustrationCandidate] = []
    for page in pages:
        if not page["has_illustration"] or not page["image_url"]:
            continue
        title = by_item.get(page["item_id"])
        if title is None:
            raise BhlConnectorError(f"BHL page has no title item: {page['item_id']}")
        species_hints = page["scientific_names"] + page["common_names"]
        record_title = page["caption"] or f"{title['title']} {page['page_number']}".strip()
        candidates.append(
            {
                "candidate_status": "candidate",
                "source_system": "BHL",
                "source_institution": BHL_INSTITUTION,
                "source_record_id": f"{page['item_id']}:page:{page['page_id']}",
                "source_url": page["page_url"],
                "title": record_title,
                "creator": title["creator"],
                "date": title["publication_year"],
                "media_type": "illustration",
                "asset_url": page["image_url"],
                "thumbnail_url": page["thumbnail_url"],
                "iiif_manifest_url": page["iiif_manifest_url"],
                "rights_status": title["rights_status"],
                "rights_statement_uri": title["rights_statement_uri"],
                "place_slug": page["place_slug"],
                "collection_hints": sorted(dict.fromkeys(title["collection_hints"] + [page["place_slug"]])),
                "product_hints": [
                    "fine_art_print",
                    "framed_print",
                    "calendar",
                    "educational_pack",
                    "digital_download",
                ],
                "species_hints": species_hints,
                "theme_hints": sorted(dict.fromkeys(title["theme_hints"] + ["bhl-illustration"])),
                "width_px": page["width_px"],
                "height_px": page["height_px"],
                "bhl_title_id": title["title_id"],
                "bhl_item_id": page["item_id"],
                "bhl_page_id": page["page_id"],
                "gbif_mapping": build_gbif_mapping(page),
                "taxonomic_enrichment": build_taxonomic_enrichment(page),
            }
        )
    return candidates


def feed_asset_factory(candidates: list[BhlIllustrationCandidate]) -> list[AssetCandidate]:
    assets = [normalize_asset_candidate(candidate, "BHL") for candidate in candidates]
    duplicate_ids = [
        candidate_id
        for candidate_id, count in Counter(asset["asset_candidate_id"] for asset in assets).items()
        if count > 1
    ]
    if duplicate_ids:
        raise BhlConnectorError(f"duplicate BHL asset candidates: {sorted(duplicate_ids)}")
    return assets


def build_bhl_runtime(path: Path | str = DEFAULT_BHL_SOURCE) -> dict[str, Any]:
    payload = load_bhl_source(path)
    titles = ingest_bhl_titles(payload)
    pages = ingest_bhl_pages(payload)
    illustration_candidates = extract_illustration_candidates(titles, pages)
    asset_candidates = feed_asset_factory(illustration_candidates)
    return {
        "runtime_version": BHL_RUNTIME_VERSION,
        "asset_factory_version": ASSET_FACTORY_VERSION,
        "title_ingestion": titles,
        "page_ingestion": pages,
        "illustration_candidate_extraction": illustration_candidates,
        "gbif_mapping": {
            candidate["source_record_id"]: candidate["gbif_mapping"]
            for candidate in illustration_candidates
        },
        "taxonomic_enrichment": {
            candidate["source_record_id"]: candidate["taxonomic_enrichment"]
            for candidate in illustration_candidates
        },
        "asset_factory_feed": {
            "asset_candidates": asset_candidates,
            "summary": summarize_asset_factory(asset_candidates),
        },
        "canonical_publication_created": False,
        "summary": {
            "title_count": len(titles),
            "page_count": len(pages),
            "illustration_candidate_count": len(illustration_candidates),
            "asset_candidate_count": len(asset_candidates),
            "gbif_mapping_count": sum(
                1 for candidate in illustration_candidates if candidate["gbif_mapping"].get("gbif_taxon_key")
            ),
            "taxonomic_enrichment_count": sum(
                1
                for candidate in illustration_candidates
                if candidate["taxonomic_enrichment"].get("canonical_name")
            ),
            "candidate_only": True,
            "canonical_publication_created": False,
        },
    }
