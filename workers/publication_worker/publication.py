"""Deterministic Publication Intelligence decisions."""
from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from workers.commerce_opportunity_worker.score import canonical_json

from . import WORKER_VERSION


@dataclass(frozen=True)
class PublicationCandidateDraft:
    catalog_candidate_id: str
    catalog_variant_id: str
    publication_policy_id: str
    publication_channel_profile_id: str
    product_recommendation_id: str
    commerce_opportunity_id: str
    opportunity_id: str
    publication_status: str
    publication_priority: str
    readiness_score: float
    channel_fit_score: float
    risk_score: float
    publication_score: float
    decision: str
    decision_basis: dict[str, Any]
    input_snapshot: dict[str, Any]
    staleness_status: str
    provenance: dict[str, Any]



def _dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, str):
        return json.loads(value)
    return dict(value)

def _decimal(value: Any) -> Decimal:
    return Decimal(str(value if value is not None else 0))


def _float3(value: Decimal | float | int | None) -> float:
    dec = _decimal(value)
    if dec < 0:
        dec = Decimal("0")
    if dec > 1:
        dec = Decimal("1")
    return float(dec.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def _weighted(signals: dict[str, Any], weights: dict[str, Any]) -> float:
    total = Decimal("0")
    for key, weight in weights.items():
        total += _decimal(signals.get(key)) * _decimal(weight)
    return _float3(total)


def is_publication_stale(policy: dict[str, Any], catalog_candidate: dict[str, Any], catalog_variant: dict[str, Any], upstream: dict[str, Any] | None = None) -> bool:
    rules = policy.get("staleness_rules", {})
    if catalog_candidate.get("catalog_status") in rules.get("stale_parent_catalog_statuses", []):
        return True
    if catalog_variant.get("variant_status") in rules.get("stale_variant_statuses", []):
        return True
    if upstream and upstream.get("policy_stale") is True:
        return True
    return False


def _readiness(policy: dict[str, Any], catalog_candidate: dict[str, Any], catalog_variant: dict[str, Any]) -> tuple[float, dict[str, float]]:
    rights_snapshot = _dict(catalog_candidate.get("rights_snapshot"))
    media_requirements = _dict(catalog_candidate.get("media_requirements"))
    asset_requirements = _dict(catalog_variant.get("asset_requirements"))
    price_snapshot = _dict(catalog_variant.get("price_snapshot"))
    rights_conf = _float3(rights_snapshot.get("rights_confidence"))
    signals = {
        "metadata_complete": 1.0 if catalog_candidate.get("catalog_title") and catalog_candidate.get("catalog_description") else 0.0,
        "rights_confidence": rights_conf,
        "media_ready": 1.0 if media_requirements and asset_requirements else 0.0,
        "price_ready": 1.0 if price_snapshot else 0.0,
        "variant_complete": 1.0 if catalog_variant.get("variant_key") and catalog_variant.get("variant_title") else 0.0,
    }
    return _weighted(signals, policy["publication_readiness_rules"]["weights"]), signals


def _channel_fit(policy: dict[str, Any], channel_profile: dict[str, Any], catalog_candidate: dict[str, Any], catalog_variant: dict[str, Any], commerce: dict[str, Any]) -> tuple[float, dict[str, float]]:
    family = catalog_variant.get("product_family")
    allowed = channel_profile.get("allowed_product_families", [])
    quality = max(_decimal(commerce.get("commerce_opportunity_score")), _decimal(commerce.get("csm_score")))
    signals = {
        "family_allowed": 1.0 if family in allowed else 0.0,
        "quality_fit": _float3(quality),
        "commerce_fit": _float3(commerce.get("commerce_opportunity_score")),
        "variant_fit": 1.0 if catalog_candidate.get("product_family") == family else 0.0,
    }
    return _weighted(signals, policy["channel_fit_rules"]["weights"]), signals


def _risk(policy: dict[str, Any], catalog_candidate: dict[str, Any], catalog_variant: dict[str, Any]) -> tuple[float, dict[str, float]]:
    rights_snapshot = _dict(catalog_candidate.get("rights_snapshot"))
    media_requirements = _dict(catalog_candidate.get("media_requirements"))
    asset_requirements = _dict(catalog_variant.get("asset_requirements"))
    rights_conf = _float3(rights_snapshot.get("rights_confidence"))
    signals = {
        "rights_uncertainty": _float3(1 - rights_conf),
        "missing_media": 0.0 if media_requirements and asset_requirements else 1.0,
        "missing_metadata": 0.0 if catalog_candidate.get("catalog_title") and catalog_candidate.get("catalog_description") else 1.0,
    }
    return _weighted(signals, policy["risk_rules"]["weights"]), signals


def build_publication_candidate(policy: dict[str, Any], channel_profile: dict[str, Any], catalog_candidate: dict[str, Any], catalog_variant: dict[str, Any], commerce: dict[str, Any]) -> PublicationCandidateDraft:
    if is_publication_stale(policy, catalog_candidate, catalog_variant, commerce):
        staleness = "stale"
    else:
        staleness = "current"

    readiness_score, readiness_signals = _readiness(policy, catalog_candidate, catalog_variant)
    channel_fit_score, channel_signals = _channel_fit(policy, channel_profile, catalog_candidate, catalog_variant, commerce)
    risk_score, risk_signals = _risk(policy, catalog_candidate, catalog_variant)
    ranking = policy["ranking_rules"]
    publication_score = _weighted(
        {
            "readiness_score": readiness_score,
            "channel_fit_score": channel_fit_score,
            "inverse_risk_score": 1 - risk_score,
        },
        ranking["weights"],
    )
    if staleness == "stale" or risk_score >= _float3(policy["risk_rules"].get("block_if_risk_above", 1)):
        decision = "block"
    elif publication_score >= _float3(ranking["recommend_threshold"]) and risk_score <= _float3(ranking["risk_recommend_max"]):
        decision = "recommend"
    elif publication_score >= _float3(ranking["hold_threshold"]):
        decision = "hold"
    else:
        decision = "block"

    thresholds = ranking.get("priority_thresholds", {})
    if publication_score >= _float3(thresholds.get("high", 0.85)):
        priority = "high"
    elif publication_score >= _float3(thresholds.get("medium", 0.65)):
        priority = "medium"
    else:
        priority = "low"

    input_snapshot = {
        "catalog_candidate_id": str(catalog_candidate["id"]),
        "catalog_variant_id": str(catalog_variant["id"]),
        "channel_profile_key": channel_profile["profile_key"],
        "catalog_status": catalog_candidate.get("catalog_status"),
        "variant_status": catalog_variant.get("variant_status"),
        "product_family": catalog_variant.get("product_family"),
    }
    decision_basis = {
        "publication_policy_id": str(policy["id"]),
        "publication_policy_version": policy["version"],
        "channel_profile_key": channel_profile["profile_key"],
        "readiness_signals": readiness_signals,
        "channel_fit_signals": channel_signals,
        "risk_signals": risk_signals,
        "worker_version": WORKER_VERSION,
    }
    return PublicationCandidateDraft(
        catalog_candidate_id=str(catalog_candidate["id"]),
        catalog_variant_id=str(catalog_variant["id"]),
        publication_policy_id=str(policy["id"]),
        publication_channel_profile_id=str(channel_profile["id"]),
        product_recommendation_id=str(catalog_candidate["product_recommendation_id"]),
        commerce_opportunity_id=str(catalog_candidate["commerce_opportunity_id"]),
        opportunity_id=str(catalog_candidate["opportunity_id"]),
        publication_status="draft" if staleness == "current" else "stale",
        publication_priority=priority,
        readiness_score=readiness_score,
        channel_fit_score=channel_fit_score,
        risk_score=risk_score,
        publication_score=publication_score,
        decision=decision,
        decision_basis=decision_basis,
        input_snapshot=input_snapshot,
        staleness_status=staleness,
        provenance={"generated_by": WORKER_VERSION, "publication_policy_version": policy["version"]},
    )


def replay_publication_candidate(policy: dict[str, Any], channel_profile: dict[str, Any], catalog_candidate: dict[str, Any], catalog_variant: dict[str, Any], commerce: dict[str, Any], expected: dict[str, Any]) -> bool:
    actual = build_publication_candidate(policy, channel_profile, catalog_candidate, catalog_variant, commerce).__dict__
    return canonical_json(actual) == canonical_json(expected)
