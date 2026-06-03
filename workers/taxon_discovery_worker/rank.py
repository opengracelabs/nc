"""Deterministic public-domain illustration opportunity ranking.

This stage uses taxa as BHL search handles. It does not optimize for species,
does not verify BHL item/page rights, and must not approve assets for commerce.
Raw occurrence counts are capped so common species do not dominate illustration opportunity value.
"""
from __future__ import annotations

from math import log1p
from typing import Any

_SCORING_VERSION = "taxon_discovery:v1"

_VISUAL_GROUP_PRIORS = {
    "orchid": 1.00,
    "bird": 0.95,
    "butterfly": 0.94,
    "moth": 0.90,
    "shell": 0.90,
    "coral": 0.88,
    "fish": 0.86,
    "plant": 0.84,
    "mammal": 0.82,
    "reptile": 0.78,
    "amphibian": 0.72,
    "fungus": 0.70,
}

_RANK_PRIORS = {
    "species": 1.00,
    "subspecies": 0.92,
    "genus": 0.68,
    "family": 0.42,
}


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _round(value: float) -> float:
    return round(_clamp(value), 3)


def _presence(value: Any) -> float:
    return 1.0 if value else 0.0


def _visual_prior(candidate: dict[str, Any]) -> float:
    groups = [str(g).lower() for g in candidate.get("visual_groups", [])]
    if not groups:
        groups = [
            str(candidate.get("kingdom", "")).lower(),
            str(candidate.get("class", "")).lower(),
        ]
    return max((_VISUAL_GROUP_PRIORS.get(group, 0.45) for group in groups), default=0.45)


def _occurrence_signal(candidate: dict[str, Any]) -> float:
    count = max(int(candidate.get("gbif_occurrence_count") or 0), 0)
    datasets = max(int(candidate.get("gbif_dataset_count") or 0), 0)
    occurrence_component = min(log1p(count) / log1p(100), 1.0) * 0.25
    dataset_component = min(datasets / 6, 1.0) * 0.20
    return occurrence_component + dataset_component


def _place_relevance(candidate: dict[str, Any]) -> float:
    score = 0.0
    score += 0.30 * _presence(candidate.get("gbif_taxon_key"))
    score += 0.22 * _presence(candidate.get("wikidata_qid"))
    score += 0.16 * _presence(candidate.get("within_place_geometry"))
    score += 0.10 * _presence(candidate.get("wikidata_place_statement"))
    score += 0.08 * _presence(candidate.get("endemic_to_place"))
    score += 0.07 * _presence(candidate.get("threatened_status"))
    score += _occurrence_signal(candidate)
    return _round(score)


def _source_agreement(candidate: dict[str, Any]) -> float:
    has_gbif = bool(candidate.get("gbif_taxon_key"))
    has_wikidata = bool(candidate.get("wikidata_qid"))
    if has_gbif and has_wikidata:
        return 1.0
    if has_gbif or has_wikidata:
        return 0.55
    return 0.0


def _illustration_likelihood(candidate: dict[str, Any]) -> float:
    score = 0.0
    score += 0.35 * _visual_prior(candidate)
    score += 0.18 * _RANK_PRIORS.get(str(candidate.get("taxon_rank", "")).lower(), 0.35)
    score += 0.14 * _presence(candidate.get("historic_names"))
    score += 0.12 * _presence(candidate.get("common_names"))
    score += 0.11 * _presence(candidate.get("bhl_known_group"))
    score += 0.10 * _presence(candidate.get("pre_1931_literature_likelihood"))
    return _round(score)


def _public_domain_path(candidate: dict[str, Any]) -> float:
    score = 0.0
    score += 0.30 * _presence(candidate.get("pre_1931_literature_likelihood"))
    score += 0.24 * _presence(candidate.get("historic_names"))
    score += 0.20 * _presence(candidate.get("bhl_known_group"))
    score += 0.16 * _visual_prior(candidate)
    score += 0.10 * _presence(candidate.get("scientific_name"))
    return _round(score)


def _commercial_value(candidate: dict[str, Any]) -> float:
    score = 0.0
    score += 0.36 * _visual_prior(candidate)
    score += 0.18 * _presence(candidate.get("visually_distinctive"))
    score += 0.15 * _presence(candidate.get("endemic_to_place"))
    score += 0.12 * _presence(candidate.get("threatened_status"))
    score += 0.10 * _presence(candidate.get("common_names"))
    score += 0.09 * _presence(candidate.get("collection_theme_fit"))
    return _round(score)


def _searchability(candidate: dict[str, Any]) -> float:
    score = 0.0
    score += 0.30 * _presence(candidate.get("scientific_name"))
    score += 0.18 * _presence(candidate.get("canonical_name"))
    score += 0.18 * _presence(candidate.get("historic_names"))
    score += 0.14 * _presence(candidate.get("common_names"))
    score += 0.10 * _presence(candidate.get("gbif_taxon_key"))
    score += 0.10 * _presence(candidate.get("wikidata_qid"))
    return _round(score)


def build_bhl_search_targets(candidate: dict[str, Any], *, limit: int = 8) -> list[dict[str, Any]]:
    names: list[tuple[str, str]] = []
    scientific_name = candidate.get("scientific_name")
    canonical_name = candidate.get("canonical_name")
    if scientific_name:
        names.append((str(scientific_name), "scientific_name"))
    if canonical_name and canonical_name != scientific_name:
        names.append((str(canonical_name), "canonical_name"))
    for name in candidate.get("historic_names", []) or []:
        names.append((str(name), "historic_synonym"))
    for name in candidate.get("common_names", []) or []:
        names.append((str(name), "common_name"))
    genus = candidate.get("genus")
    if genus:
        names.append((str(genus), "genus"))

    seen: set[str] = set()
    targets: list[dict[str, Any]] = []
    for name, target_type in names:
        query = name.strip()
        if not query or query.lower() in seen:
            continue
        seen.add(query.lower())
        targets.append({
            "sequence": len(targets) + 1,
            "query": query,
            "target_type": target_type,
            "provenance": {
                "prov:wasGeneratedBy": _SCORING_VERSION,
                "purpose": "bhl_public_domain_illustration_search",
            },
        })
        if len(targets) >= limit:
            break
    return targets


def rank_taxon_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    components = {
        "place_relevance": _place_relevance(candidate),
        "source_agreement": _round(_source_agreement(candidate)),
        "illustration_likelihood": _illustration_likelihood(candidate),
        "public_domain_path": _public_domain_path(candidate),
        "commercial_value": _commercial_value(candidate),
        "searchability": _searchability(candidate),
    }
    total = (
        0.26 * components["place_relevance"]
        + 0.16 * components["source_agreement"]
        + 0.20 * components["illustration_likelihood"]
        + 0.16 * components["public_domain_path"]
        + 0.16 * components["commercial_value"]
        + 0.06 * components["searchability"]
    )
    targets = build_bhl_search_targets(candidate)
    return {
        "scientific_name": candidate["scientific_name"],
        "canonical_name": candidate.get("canonical_name"),
        "taxon_rank": str(candidate.get("taxon_rank", "species")).lower(),
        "gbif_taxon_key": (
            str(candidate["gbif_taxon_key"]) if candidate.get("gbif_taxon_key") else None
        ),
        "wikidata_qid": candidate.get("wikidata_qid"),
        "common_names": candidate.get("common_names", []),
        "place_relevance_score": components["place_relevance"],
        "source_agreement_score": components["source_agreement"],
        "illustration_likelihood_score": components["illustration_likelihood"],
        "public_domain_path_score": components["public_domain_path"],
        "commercial_value_score": components["commercial_value"],
        "searchability_score": components["searchability"],
        "total_score": _round(total),
        "score_components": {
            **components,
            "gbif_occurrence_count_capped": min(
                int(candidate.get("gbif_occurrence_count") or 0), 100
            ),
            "scoring_note": (
                "Taxa are search handles; illustration opportunity is the ranking target. "
                "Raw occurrence counts are capped."
            ),
        },
        "bhl_search_targets": targets,
        "provenance": {
            "prov:wasGeneratedBy": _SCORING_VERSION,
            "sources": [
                source
                for source in (
                    "gbif" if candidate.get("gbif_taxon_key") else None,
                    "wikidata" if candidate.get("wikidata_qid") else None,
                )
                if source
            ],
            "rights_rule": "No BHL asset rights inferred at taxon discovery stage.",
        },
    }


def rank_taxa(candidates: list[dict[str, Any]], *, limit: int = 50) -> list[dict[str, Any]]:
    ranked = [rank_taxon_candidate(candidate) for candidate in candidates]
    ranked.sort(key=lambda item: (-item["total_score"], item["scientific_name"]))
    return ranked[:limit]
