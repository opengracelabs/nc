"""Deterministic Asset Intelligence registry resolution."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from workers.commerce_opportunity_worker.score import canonical_json

from . import WORKER_VERSION


@dataclass(frozen=True)
class CreatorAuthorityResolution:
    registry_id: str | None
    registry_version: str | None
    canonical_creator_key: str | None
    display_name: str | None
    authority_confidence: float
    attribution_risk: str
    matched_alias: str | None


@dataclass(frozen=True)
class CreatorPrestigeResolution:
    registry_id: str | None
    registry_version: str | None
    prestige_score: float
    prestige_tier: str
    prestige_rationale_hash: str | None


@dataclass(frozen=True)
class PlaceIconicTaxaResolution:
    registry_id: str | None
    registry_version: str | None
    place_key: str | None
    taxon_key: str | None
    scientific_name: str | None
    iconic_score: float


@dataclass(frozen=True)
class AssetIntelligenceResolution:
    anchor_type: str
    creator_authority: CreatorAuthorityResolution
    creator_prestige: CreatorPrestigeResolution
    place_iconic_taxa: PlaceIconicTaxaResolution
    resolved_signals: dict[str, Any]
    registry_version_set: dict[str, str]
    input_hash_sha256: str


def normalize_name(value: str | None) -> str:
    if not value:
        return ""
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_text = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", ascii_text.lower()).strip()


def _active(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("status") == "active"]


def _float(value: Any) -> float:
    return float(value or 0.0)


def _hash_text(value: str | None) -> str | None:
    if value is None:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def resolve_creator_authority(
    creator_name: str | None,
    authority_rows: list[dict[str, Any]],
    alias_rows: list[dict[str, Any]],
) -> CreatorAuthorityResolution:
    normalized = normalize_name(creator_name)
    if not normalized:
        return CreatorAuthorityResolution(None, None, None, None, 0.0, "unknown", None)

    authority_by_id = {str(row["id"]): row for row in _active(authority_rows)}
    candidates: list[tuple[float, dict[str, Any], dict[str, Any]]] = []
    for alias in alias_rows:
        authority = authority_by_id.get(str(alias.get("creator_authority_id")))
        if authority is None:
            continue
        alias_norm = normalize_name(alias.get("normalized_alias") or alias.get("alias"))
        if not alias_norm:
            continue
        if normalized == alias_norm or alias_norm in normalized or normalized in alias_norm:
            score = _float(alias.get("confidence_score")) * _float(
                authority.get("authority_confidence")
            )
            candidates.append((score, authority, alias))

    if not candidates:
        return CreatorAuthorityResolution(None, None, None, None, 0.0, "unknown", None)

    candidates.sort(key=lambda item: (-item[0], item[1].get("canonical_creator_key", "")))
    _, authority, alias = candidates[0]
    return CreatorAuthorityResolution(
        registry_id=str(authority["id"]),
        registry_version=authority.get("registry_version"),
        canonical_creator_key=authority.get("canonical_creator_key"),
        display_name=authority.get("display_name"),
        authority_confidence=_float(authority.get("authority_confidence")),
        attribution_risk=authority.get("attribution_risk") or "unknown",
        matched_alias=alias.get("alias"),
    )


def resolve_creator_prestige(
    authority: CreatorAuthorityResolution,
    anchor_type: str,
    prestige_rows: list[dict[str, Any]],
) -> CreatorPrestigeResolution:
    if authority.registry_id is None:
        return CreatorPrestigeResolution(None, None, 0.0, "none", None)

    matches = []
    for row in _active(prestige_rows):
        if str(row.get("creator_authority_id")) != authority.registry_id:
            continue
        applies = row.get("applies_to_anchor_types") or []
        if anchor_type not in applies:
            continue
        matches.append(row)

    if not matches:
        return CreatorPrestigeResolution(None, None, 0.0, "none", None)

    matches.sort(
        key=lambda row: (-_float(row.get("prestige_score")), row.get("registry_version", ""))
    )
    row = matches[0]
    return CreatorPrestigeResolution(
        registry_id=str(row["id"]),
        registry_version=row.get("registry_version"),
        prestige_score=_float(row.get("prestige_score")),
        prestige_tier=row.get("prestige_tier") or "none",
        prestige_rationale_hash=_hash_text(row.get("prestige_rationale")),
    )


def resolve_place_iconic_taxa(
    *,
    place_key: str | None,
    taxon_name: str | None,
    taxon_key: str | None,
    registry_rows: list[dict[str, Any]],
) -> PlaceIconicTaxaResolution:
    normalized_taxon = normalize_name(taxon_key or taxon_name)
    normalized_place = normalize_name(place_key)
    if not normalized_taxon or not normalized_place:
        return PlaceIconicTaxaResolution(None, None, None, None, None, 0.0)

    matches = []
    for row in _active(registry_rows):
        row_place = normalize_name(row.get("place_key") or row.get("place_label"))
        row_taxon = normalize_name(row.get("taxon_key") or row.get("scientific_name"))
        taxon_matches = (
            row_taxon == normalized_taxon
            or row_taxon in normalized_taxon
            or normalized_taxon in row_taxon
        )
        if row_place == normalized_place and taxon_matches:
            matches.append(row)

    if not matches:
        return PlaceIconicTaxaResolution(None, None, None, None, None, 0.0)

    matches.sort(key=lambda row: (-_float(row.get("iconic_score")), row.get("taxon_key", "")))
    row = matches[0]
    return PlaceIconicTaxaResolution(
        registry_id=str(row["id"]),
        registry_version=row.get("registry_version"),
        place_key=row.get("place_key"),
        taxon_key=row.get("taxon_key"),
        scientific_name=row.get("scientific_name"),
        iconic_score=_float(row.get("iconic_score")),
    )


def resolve_asset_intelligence(
    opportunity: dict[str, Any],
    *,
    authority_rows: list[dict[str, Any]],
    alias_rows: list[dict[str, Any]],
    prestige_rows: list[dict[str, Any]],
    iconic_taxa_rows: list[dict[str, Any]],
) -> AssetIntelligenceResolution:
    anchor_type = opportunity.get("anchor_type") or (
        "biological" if opportunity.get("source") == "bhl" else "geographic"
    )
    authority = resolve_creator_authority(
        opportunity.get("illustrator") or opportunity.get("creator"),
        authority_rows,
        alias_rows,
    )
    prestige = resolve_creator_prestige(authority, anchor_type, prestige_rows)
    iconic = resolve_place_iconic_taxa(
        place_key=opportunity.get("place_key"),
        taxon_name=opportunity.get("taxon_name"),
        taxon_key=opportunity.get("taxon_key"),
        registry_rows=iconic_taxa_rows,
    )
    requires_review = (
        prestige.prestige_score >= 1.0
        or authority.attribution_risk in {"medium", "high"}
        or anchor_type in {"geographic", "cultural"}
    )
    if prestige.prestige_score >= 1.0:
        review_reason = "priority_illustrator"
    elif requires_review:
        review_reason = "manual_flag"
    else:
        review_reason = None
    registry_version_set = {
        "commerce_anchor_type_vocabulary": "1.0.0",
        "creator_authority_registry": authority.registry_version or "unresolved",
        "creator_prestige_registry": prestige.registry_version or "unresolved",
        "place_iconic_taxa_registry": iconic.registry_version or "unresolved",
    }
    resolved_signals = {
        "anchor_type": anchor_type,
        "creator_authority": authority.__dict__,
        "creator_prestige": prestige.__dict__,
        "place_iconic_taxa": iconic.__dict__,
        "illustrator_prestige": prestige.prestige_score,
        "taxon_place_iconic": iconic.iconic_score,
        "requires_curator_review": requires_review,
        "curator_review_reason": review_reason,
        "resolved_by": WORKER_VERSION,
    }
    surface = {
        "opportunity": {
            "source": opportunity.get("source"),
            "source_record_id": opportunity.get("source_record_id"),
            "anchor_type": anchor_type,
            "creator": opportunity.get("illustrator") or opportunity.get("creator"),
            "taxon_name": opportunity.get("taxon_name"),
            "place_key": opportunity.get("place_key"),
        },
        "registry_version_set": registry_version_set,
        "resolved_signals": resolved_signals,
    }
    return AssetIntelligenceResolution(
        anchor_type=anchor_type,
        creator_authority=authority,
        creator_prestige=prestige,
        place_iconic_taxa=iconic,
        resolved_signals=resolved_signals,
        registry_version_set=registry_version_set,
        input_hash_sha256=hashlib.sha256(canonical_json(surface).encode("utf-8")).hexdigest(),
    )


def apply_asset_intelligence_to_score_inputs(
    score_inputs: dict[str, Any],
    resolution: AssetIntelligenceResolution,
) -> dict[str, Any]:
    enriched = dict(score_inputs)
    enriched["anchor_type"] = resolution.anchor_type
    enriched["illustrator_prestige"] = resolution.resolved_signals["illustrator_prestige"]
    enriched["taxon_place_iconic"] = resolution.resolved_signals["taxon_place_iconic"]
    enriched["requires_curator_review"] = resolution.resolved_signals["requires_curator_review"]
    enriched["curator_review_reason"] = resolution.resolved_signals["curator_review_reason"]
    enriched["asset_intelligence"] = {
        "registry_version_set": resolution.registry_version_set,
        "input_hash_sha256": resolution.input_hash_sha256,
        "resolved_signals": json.loads(json.dumps(resolution.resolved_signals, sort_keys=True)),
    }
    return enriched


def recompute_after_activation(
    score_inputs: dict[str, Any],
    resolution: AssetIntelligenceResolution,
) -> dict[str, Any]:
    return apply_asset_intelligence_to_score_inputs(score_inputs, resolution)
