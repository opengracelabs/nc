"""Candidate-only asset factory runtime for NC-ASSETS-1000000."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any, TypedDict

from services.data.place_seed import normalize_place_slug

ASSET_SOURCES_DIR = Path("data/curated/asset_sources")
ASSET_CANDIDATES_DIR = Path("data/curated/asset_candidates")
ASSET_FACTORY_VERSION = "NC-ASSETS-1000000-v1"

SUPPORTED_ASSET_SOURCES = (
    "Europeana",
    "Smithsonian",
    "Rijksmuseum",
    "NHM",
    "BHL",
    "NASA",
    "NOAA",
    "NARA",
)

SUPPORTED_SOURCE_KEYS = {source.lower(): source for source in SUPPORTED_ASSET_SOURCES}

REQUIRED_ASSET_FIELDS = (
    "asset_candidate_id",
    "candidate_status",
    "source_system",
    "source_institution",
    "source_record_id",
    "source_url",
    "title",
    "creator",
    "date",
    "media_type",
    "asset_url",
    "thumbnail_url",
    "iiif_manifest_url",
    "rights_status",
    "rights_statement_uri",
    "place_slug",
    "collection_hints",
    "product_hints",
    "species_hints",
    "theme_hints",
    "asset_readiness",
    "asset_collection_mapping",
    "asset_product_mapping",
    "canonical_publication_created",
)

FORBIDDEN_CANONICAL_FIELDS = {
    "canonical_asset_id",
    "canonical_identity",
    "canonical_publication_id",
    "canonical_product_id",
    "published_asset_id",
    "product_page_slug",
    "edition_registry_id",
    "certificate_id",
    "neo4j_node_id",
    "asset_id",
}

VALID_CANDIDATE_STATUS = {"candidate", "unverified", "needs_review", "rejected"}
ALLOWED_RIGHTS = {"verified_pd", "verified_cc0", "open_access", "public_domain"}
REVIEW_RIGHTS = {"pending_verification", "unknown", "source_observed"}

SOURCE_DEFAULTS = {
    "Europeana": {"institution": "Europeana", "collection_bias": "europeana_open_culture"},
    "Smithsonian": {"institution": "Smithsonian", "collection_bias": "smithsonian_open_access"},
    "Rijksmuseum": {"institution": "Rijksmuseum", "collection_bias": "rijksmuseum_open_data"},
    "NHM": {"institution": "Natural History Museum", "collection_bias": "natural_history_collection"},
    "BHL": {"institution": "Biodiversity Heritage Library", "collection_bias": "biodiversity_library"},
    "NASA": {"institution": "NASA", "collection_bias": "space_earth_observation"},
    "NOAA": {"institution": "NOAA", "collection_bias": "ocean_atmosphere"},
    "NARA": {"institution": "National Archives and Records Administration", "collection_bias": "federal_archive"},
}

PRODUCT_HINT_WEIGHTS = {
    "fine_art_print": 14,
    "framed_print": 14,
    "canvas": 12,
    "metal": 10,
    "acrylic": 10,
    "postcard": 8,
    "calendar": 8,
    "book": 9,
    "educational_pack": 12,
    "digital_download": 10,
}

MEDIA_TYPE_PRODUCT_HINTS = {
    "image": ["fine_art_print", "framed_print", "canvas", "postcard", "digital_download"],
    "map": ["fine_art_print", "framed_print", "book", "educational_pack", "digital_download"],
    "illustration": ["fine_art_print", "framed_print", "calendar", "educational_pack", "digital_download"],
    "book_page": ["book", "educational_pack", "digital_download"],
    "specimen": ["educational_pack", "book", "digital_download"],
    "satellite": ["metal", "acrylic", "fine_art_print", "educational_pack", "digital_download"],
}


class AssetFactoryError(ValueError):
    """Raised when an asset source violates candidate-only factory rules."""


class AssetCandidate(TypedDict):
    asset_candidate_id: str
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
    asset_readiness: dict[str, Any]
    asset_collection_mapping: list[dict[str, Any]]
    asset_product_mapping: list[dict[str, Any]]
    canonical_publication_created: bool


def _as_string(value: Any, field: str, default: str | None = None) -> str:
    if value in (None, "") and default is not None:
        return default
    if not isinstance(value, str) or not value.strip():
        raise AssetFactoryError(f"{field} must be a non-empty string")
    return value.strip()


def _as_optional_string(value: Any) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else ""


def _as_string_list(value: Any, field: str) -> list[str]:
    if value in (None, ""):
        return []
    if not isinstance(value, list):
        raise AssetFactoryError(f"{field} must be a list")
    result = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise AssetFactoryError(f"{field} must contain strings")
        result.append(item.strip())
    return result


def _as_int(value: Any, default: int = 0) -> int:
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: int) -> int:
    return max(0, min(100, value))


def normalize_source_system(value: Any) -> str:
    source = _as_string(value, "source_system")
    normalized = SUPPORTED_SOURCE_KEYS.get(source.lower())
    if not normalized:
        raise AssetFactoryError(f"source_system must be one of {SUPPORTED_ASSET_SOURCES}")
    return normalized


def validate_candidate_only(record: dict[str, Any]) -> None:
    forbidden = set(record) & FORBIDDEN_CANONICAL_FIELDS
    if forbidden:
        raise AssetFactoryError(f"canonical publication fields are not allowed: {sorted(forbidden)}")
    status = record.get("candidate_status", "candidate")
    if status not in VALID_CANDIDATE_STATUS:
        raise AssetFactoryError(f"candidate_status must be one of {sorted(VALID_CANDIDATE_STATUS)}")


def _candidate_id(source_system: str, source_record_id: str, title: str) -> str:
    return f"{source_system.lower()}-{normalize_place_slug(source_record_id or title)}"


def infer_product_hints(media_type: str, explicit_hints: list[str]) -> list[str]:
    hints = explicit_hints or MEDIA_TYPE_PRODUCT_HINTS.get(media_type, ["educational_pack", "digital_download"])
    return sorted(dict.fromkeys(hints))


def score_asset_candidate(raw: dict[str, Any]) -> dict[str, int]:
    rights = str(raw.get("rights_status") or "").lower()
    asset_url = raw.get("asset_url")
    iiif = raw.get("iiif_manifest_url")
    width = _as_int(raw.get("width_px"))
    height = _as_int(raw.get("height_px"))
    product_hints = _as_string_list(raw.get("product_hints"), "product_hints")
    collection_hints = _as_string_list(raw.get("collection_hints"), "collection_hints")

    rights_score = 100 if rights in ALLOWED_RIGHTS else 50 if rights in REVIEW_RIGHTS else 0
    media_score = 20
    if asset_url:
        media_score += 35
    if iiif:
        media_score += 20
    if width >= 3000 and height >= 3000:
        media_score += 25
    elif width >= 1600 and height >= 1600:
        media_score += 15
    metadata_score = 30
    for field in ("title", "source_record_id", "source_url", "source_institution"):
        if raw.get(field):
            metadata_score += 12
    if raw.get("creator"):
        metadata_score += 8
    collection_score = _clamp(30 + len(collection_hints) * 12 + (20 if raw.get("place_slug") else 0))
    product_score = _clamp(20 + sum(PRODUCT_HINT_WEIGHTS.get(hint, 4) for hint in product_hints))

    return {
        "rights_score": _clamp(rights_score),
        "media_score": _clamp(media_score),
        "metadata_score": _clamp(metadata_score),
        "collection_score": collection_score,
        "product_score": product_score,
    }


def build_asset_readiness(raw: dict[str, Any]) -> dict[str, Any]:
    scores = score_asset_candidate(raw)
    missing = []
    if scores["rights_score"] < 100:
        missing.append("verified_open_rights")
    if not raw.get("asset_url"):
        missing.append("asset_url")
    if scores["media_score"] < 70:
        missing.append("production_media_quality")
    if scores["metadata_score"] < 70:
        missing.append("required_source_metadata")

    overall = round(
        scores["rights_score"] * 0.35
        + scores["media_score"] * 0.25
        + scores["metadata_score"] * 0.2
        + scores["collection_score"] * 0.1
        + scores["product_score"] * 0.1,
        2,
    )
    state = "ready" if overall >= 80 and not missing else "review" if overall >= 55 else "hold"
    return {
        "state": state,
        "overall_score": overall,
        **scores,
        "missing": missing,
        "candidate_only": True,
    }


def build_asset_collection_mapping(raw: dict[str, Any]) -> list[dict[str, Any]]:
    hints = _as_string_list(raw.get("collection_hints"), "collection_hints")
    if not hints and raw.get("place_slug"):
        hints = [f"{raw['place_slug']}_collection"]
    return [
        {
            "mapping_status": "candidate",
            "collection_slug": normalize_place_slug(hint),
            "fit_score": _clamp(58 + index * 7 + (10 if raw.get("place_slug") else 0)),
            "evidence": ["source_metadata", "place_hint" if raw.get("place_slug") else "theme_hint"],
        }
        for index, hint in enumerate(hints[:5])
    ]


def build_asset_product_mapping(raw: dict[str, Any]) -> list[dict[str, Any]]:
    product_hints = infer_product_hints(
        str(raw.get("media_type") or "image"),
        _as_string_list(raw.get("product_hints"), "product_hints"),
    )
    readiness = build_asset_readiness(raw)
    return [
        {
            "mapping_status": "candidate",
            "product_type": hint,
            "fit_score": _clamp(readiness["product_score"] + PRODUCT_HINT_WEIGHTS.get(hint, 4)),
            "requires_review": readiness["state"] != "ready",
        }
        for hint in product_hints
    ]


def normalize_asset_candidate(raw: dict[str, Any], source_system: str | None = None) -> AssetCandidate:
    if not isinstance(raw, dict):
        raise AssetFactoryError("asset source record must be an object")
    validate_candidate_only(raw)
    source = normalize_source_system(raw.get("source_system") or source_system)
    defaults = SOURCE_DEFAULTS[source]
    title = _as_string(raw.get("title") or raw.get("name"), "title")
    source_record_id = _as_string(
        raw.get("source_record_id") or raw.get("identifier") or raw.get("id"),
        "source_record_id",
    )
    media_type = _as_string(raw.get("media_type") or raw.get("type"), "media_type", "image")
    product_hints = infer_product_hints(
        media_type,
        _as_string_list(raw.get("product_hints"), "product_hints"),
    )
    working: dict[str, Any] = {
        "asset_candidate_id": raw.get("asset_candidate_id")
        or _candidate_id(source, source_record_id, title),
        "candidate_status": _as_string(raw.get("candidate_status"), "candidate_status", "candidate"),
        "source_system": source,
        "source_institution": _as_string(
            raw.get("source_institution"),
            "source_institution",
            defaults["institution"],
        ),
        "source_record_id": source_record_id,
        "source_url": _as_string(raw.get("source_url"), "source_url"),
        "title": title,
        "creator": _as_optional_string(raw.get("creator") or raw.get("artist")),
        "date": _as_optional_string(raw.get("date") or raw.get("created")),
        "media_type": media_type,
        "asset_url": _as_optional_string(raw.get("asset_url") or raw.get("image_url")),
        "thumbnail_url": _as_optional_string(raw.get("thumbnail_url")),
        "iiif_manifest_url": _as_optional_string(raw.get("iiif_manifest_url")),
        "rights_status": _as_string(raw.get("rights_status"), "rights_status", "pending_verification"),
        "rights_statement_uri": _as_optional_string(raw.get("rights_statement_uri")),
        "place_slug": normalize_place_slug(str(raw.get("place_slug") or raw.get("place") or "global")),
        "collection_hints": _as_string_list(raw.get("collection_hints"), "collection_hints")
        or [defaults["collection_bias"]],
        "product_hints": product_hints,
        "species_hints": _as_string_list(raw.get("species_hints"), "species_hints"),
        "theme_hints": _as_string_list(raw.get("theme_hints"), "theme_hints"),
        "width_px": _as_int(raw.get("width_px")),
        "height_px": _as_int(raw.get("height_px")),
    }
    validate_candidate_only(working)
    working["asset_readiness"] = build_asset_readiness(working)
    working["asset_collection_mapping"] = build_asset_collection_mapping(working)
    working["asset_product_mapping"] = build_asset_product_mapping(working)
    working["canonical_publication_created"] = False
    for transient in ("width_px", "height_px"):
        working.pop(transient, None)
    missing = set(REQUIRED_ASSET_FIELDS) - set(working)
    if missing:
        raise AssetFactoryError(f"asset candidate missing required fields: {sorted(missing)}")
    return AssetCandidate(**working)


def ingest_asset_source(path: Path | str) -> list[AssetCandidate]:
    source_path = Path(path)
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        source_system = payload.get("source_system") or payload.get("source_list") or source_path.stem
        records = payload.get("records")
    else:
        source_system = source_path.stem
        records = payload
    if not isinstance(records, list):
        raise AssetFactoryError("asset source must be a list or an object with records")
    candidates = [normalize_asset_candidate(record, str(source_system)) for record in records]
    duplicate_ids = sorted(
        candidate_id
        for candidate_id, count in Counter(c["asset_candidate_id"] for c in candidates).items()
        if count > 1
    )
    if duplicate_ids:
        raise AssetFactoryError(f"duplicate asset candidates in source: {duplicate_ids}")
    return candidates


def asset_ingestion_pipeline(paths: Iterable[Path | str]) -> dict[str, Any]:
    candidates: list[AssetCandidate] = []
    seen: set[str] = set()
    for path in paths:
        for candidate in ingest_asset_source(path):
            candidate_id = candidate["asset_candidate_id"]
            if candidate_id in seen:
                raise AssetFactoryError(f"duplicate asset candidate across pipeline: {candidate_id}")
            seen.add(candidate_id)
            candidates.append(candidate)
    return {
        "runtime_version": ASSET_FACTORY_VERSION,
        "asset_candidates": candidates,
        "asset_readiness": {c["asset_candidate_id"]: c["asset_readiness"] for c in candidates},
        "asset_collection_mapping": {
            c["asset_candidate_id"]: c["asset_collection_mapping"] for c in candidates
        },
        "asset_product_mapping": {
            c["asset_candidate_id"]: c["asset_product_mapping"] for c in candidates
        },
        "canonical_publication_created": False,
        "summary": summarize_asset_factory(candidates),
    }


def export_asset_candidates(
    candidates: Iterable[AssetCandidate],
    batch_name: str,
    output_dir: Path | str = ASSET_CANDIDATES_DIR,
) -> Path:
    materialized = sorted(list(candidates), key=lambda item: item["asset_candidate_id"])
    if not materialized:
        raise AssetFactoryError("cannot export an empty asset candidate batch")
    for candidate in materialized:
        validate_candidate_only(candidate)
        if candidate.get("canonical_publication_created") is not False:
            raise AssetFactoryError("canonical publication is not allowed in asset factory")
        missing = set(REQUIRED_ASSET_FIELDS) - set(candidate)
        if missing:
            raise AssetFactoryError(f"asset candidate missing required fields: {sorted(missing)}")
    output_path = Path(output_dir) / f"{normalize_place_slug(batch_name)}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(materialized, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def summarize_asset_factory(candidates: Iterable[AssetCandidate]) -> dict[str, Any]:
    materialized = list(candidates)
    readiness_states = [c["asset_readiness"]["state"] for c in materialized]
    return {
        "runtime_version": ASSET_FACTORY_VERSION,
        "total_candidates": len(materialized),
        "supported_sources": list(SUPPORTED_ASSET_SOURCES),
        "source_system_counts": dict(sorted(Counter(c["source_system"] for c in materialized).items())),
        "media_type_counts": dict(sorted(Counter(c["media_type"] for c in materialized).items())),
        "rights_status_counts": dict(sorted(Counter(c["rights_status"] for c in materialized).items())),
        "asset_readiness_counts": dict(sorted(Counter(readiness_states).items())),
        "collection_mapping_count": sum(len(c["asset_collection_mapping"]) for c in materialized),
        "product_mapping_count": sum(len(c["asset_product_mapping"]) for c in materialized),
        "canonical_publication_created": False,
        "scale_target": 1000000,
    }
