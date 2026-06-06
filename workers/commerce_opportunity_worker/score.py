"""Deterministic Commerce Intelligence scoring."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from . import WORKER_VERSION


COS_SUBSCORES = (
    "museum_score",
    "retail_score",
    "publishing_score",
    "tourism_score",
    "reference_score",
)
PRODUCT_ELIGIBILITY_FIELDS = {
    "wall_art_premium": "eligible_wall_art_premium",
    "wall_art_standard": "eligible_wall_art_standard",
    "calendar": "eligible_calendar",
    "puzzle": "eligible_puzzle",
    "card": "eligible_card",
    "book_illustration": "eligible_book_illustration",
    "educational": "eligible_educational",
    "museum_print": "eligible_museum_print",
    "institutional_license": "eligible_institutional_license",
}


@dataclass(frozen=True)
class ScoreComputation:
    score_inputs: dict[str, Any]
    score_outputs: dict[str, Any]
    commerce_record: dict[str, Any]
    input_hash_sha256: str
    audit_checksum_sha256: str
    event_at: datetime
    hard_gate_failure: str | None = None


def _decimal(value: Any) -> Decimal:
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


def _quantize(value: Decimal, places: str = "0.001") -> Decimal:
    if value < 0:
        value = Decimal("0")
    if value > 1:
        value = Decimal("1")
    return value.quantize(Decimal(places), rounding=ROUND_HALF_UP)


def _float3(value: Decimal | float | int | None) -> float:
    return float(_quantize(_decimal(value)))


def _canonicalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _canonicalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_canonicalize(item) for item in value]
    if isinstance(value, float):
        return format(_quantize(Decimal(str(value)), "0.000001"), "f")
    if isinstance(value, Decimal):
        return format(_quantize(value, "0.000001"), "f")
    return value


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(_canonicalize(value), sort_keys=True, separators=(",", ":"))


def hash_json(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def weighted_sum(inputs: dict[str, Any], spec: dict[str, Any]) -> float:
    total = Decimal("0")
    for item in spec.get("inputs", []):
        signal = item["signal"]
        weight = _decimal(item["weight"])
        total += _decimal(inputs.get(signal)) * weight
    return _float3(total)


def assign_threshold_tier(score: float, thresholds: dict[str, Any], order: tuple[str, ...]) -> str:
    value = _decimal(score)
    for tier in order:
        if value >= _decimal(thresholds[tier]):
            return tier
    return order[-1]


def _apply_signal_defaults(inputs: dict[str, Any], formula_spec: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(inputs)
    for key, value in formula_spec.get("signal_defaults", {}).items():
        normalized.setdefault(key, value)
    return normalized


def _resolution_tier(image_width_px: int | None, formula_spec: dict[str, Any]) -> tuple[str, float]:
    width = int(image_width_px or 0)
    tiers = formula_spec.get("resolution_tier_map", {})
    for name in ("premium", "standard", "marginal"):
        tier = tiers.get(name, {})
        if width >= int(tier.get("min_width_px") or 0):
            return name, _float3(tier.get("score", 0))
    return "blocked", _float3(tiers.get("blocked", {}).get("score", 0))


def evaluate_hard_gates(inputs: dict[str, Any], hard_gate_values: dict[str, Any]) -> str | None:
    gate_0 = hard_gate_values.get("gate_0_rights_record_exists", {})
    if gate_0.get("required") and not inputs.get("rights_record_exists", False):
        return gate_0.get("blocked_status", "blocked_rights")

    gate_3 = hard_gate_values.get("gate_3_legal_hold", {})
    legal_value = gate_3.get("rights_confidence_equals")
    if legal_value is not None and _decimal(inputs.get("rights_confidence")) == _decimal(legal_value):
        return gate_3.get("blocked_status", "blocked_legal")

    gate_1 = hard_gate_values.get("gate_1_min_rights_confidence", {})
    if _decimal(inputs.get("rights_confidence")) < _decimal(gate_1.get("min_rights_confidence", 0)):
        return gate_1.get("blocked_status", "blocked_rights")

    gate_2 = hard_gate_values.get("gate_2_min_image_width_px", {})
    if int(inputs.get("image_width_px") or 0) < int(gate_2.get("min_image_width_px", 0)):
        return gate_2.get("blocked_status", "blocked_resolution")

    gate_4 = hard_gate_values.get("gate_4_min_quality_score", {})
    quality = inputs.get("image_quality_score")
    if quality is None and gate_4.get("null_blocks", False):
        return gate_4.get("blocked_status", "blocked_quality")
    if _decimal(quality) < _decimal(gate_4.get("min_quality_score", 0)):
        return gate_4.get("blocked_status", "blocked_quality")

    return None


def _eligibility(record: dict[str, Any], policy: dict[str, Any]) -> dict[str, bool]:
    requirements = policy.get("product_surface_requirements", {})
    result = {field: False for field in PRODUCT_ELIGIBILITY_FIELDS.values()}
    if record["hard_gate_status"] != "passed":
        return result

    for surface, field in PRODUCT_ELIGIBILITY_FIELDS.items():
        req = requirements.get(surface, {})
        eligible = True
        checks = {
            "min_cos": record.get("commerce_opportunity_score"),
            "min_image_width_px": record.get("image_width_px"),
            "min_quality_score": record.get("image_quality_score"),
            "min_composition_fit": record.get("composition_fit"),
            "min_publishing_score": record.get("publishing_score"),
            "min_identification_confidence": record.get("identification_confidence"),
            "min_reference_score": record.get("reference_score"),
            "min_museum_score": record.get("museum_score"),
            "min_rights_confidence": record.get("rights_confidence"),
        }
        for requirement, actual in checks.items():
            if requirement in req and _decimal(actual) < _decimal(req[requirement]):
                eligible = False
        if "illustrator_prestige" in req and _decimal(record.get("illustrator_prestige")) < _decimal(req["illustrator_prestige"]):
            eligible = False
        result[field] = eligible
    return result


def compute_scores(
    policy: dict[str, Any],
    raw_inputs: dict[str, Any],
    *,
    opportunity_id: str,
    previous_entry_checksum: str | None = None,
    event_at: datetime | None = None,
    actor_id: str = WORKER_VERSION,
) -> ScoreComputation:
    formula_spec = policy["formula_spec"]
    inputs = _apply_signal_defaults(raw_inputs, formula_spec)
    resolution_tier, resolution_tier_score = _resolution_tier(inputs.get("image_width_px"), formula_spec)
    inputs["resolution_tier"] = resolution_tier
    inputs["resolution_tier_score"] = resolution_tier_score

    hard_gate_failure = evaluate_hard_gates(inputs, policy["hard_gate_values"])
    hard_gate_status = hard_gate_failure or "passed"

    subscores: dict[str, float] = {}
    if hard_gate_failure is None:
        for name in COS_SUBSCORES:
            subscores[name] = weighted_sum(inputs, formula_spec["subscores"][name])
        cos = weighted_sum(subscores, formula_spec["composite"])
        commerce_tier = assign_threshold_tier(
            cos,
            policy["tier_thresholds"],
            ("tier_1", "tier_2", "tier_3", "blocked"),
        )
    else:
        subscores = {name: 0.0 for name in COS_SUBSCORES}
        cos = 0.0
        commerce_tier = "blocked"

    csm_spec = formula_spec["csm_dimension_map"]
    csm_dimensions: dict[str, float] = {}
    if hard_gate_failure is None:
        for name, spec in csm_spec["dimensions"].items():
            csm_dimensions[name] = weighted_sum(inputs, spec)
        csm_score = weighted_sum(csm_dimensions, csm_spec["composite"])
        csm_tier = assign_threshold_tier(
            csm_score,
            csm_spec["tier_thresholds"],
            ("MASTERWORK", "FLAGSHIP", "STANDARD", "REFERENCE", "BLOCKED"),
        )
        rcs_gate = csm_spec.get("rcs_gate", {})
        rcs_signal = rcs_gate.get("signal", "rights_confidence")
        rcs_min_value = rcs_gate.get("min_value")
        if rcs_min_value is not None and _decimal(inputs.get(rcs_signal)) < _decimal(rcs_min_value):
            csm_tier = rcs_gate.get("blocked_tier", "BLOCKED")
    else:
        csm_dimensions = {name: 0.0 for name in csm_spec["dimensions"]}
        csm_score = 0.0
        csm_tier = "BLOCKED"

    score_outputs = {
        **subscores,
        "commerce_opportunity_score": cos,
        "commerce_tier": commerce_tier,
        "hard_gate_status": hard_gate_status,
        "csm_dimensions": csm_dimensions,
        "csm_score": csm_score,
        "csm_tier": csm_tier,
        "scorer_version": formula_spec.get("scorer_version"),
        "csm_scorer_version": csm_spec.get("scorer_version"),
    }
    input_hash = hash_json(inputs)
    now = event_at or datetime.now(UTC)
    audit_surface = {
        "opportunity_id": str(opportunity_id),
        "event_type": "score_computed" if hard_gate_failure is None else "hard_gate_blocked",
        "event_at": now.isoformat(),
        "actor_id": actor_id,
        "score_inputs": inputs,
        "score_outputs": score_outputs,
    }
    audit_checksum = hashlib.sha256(canonical_json(audit_surface).encode("utf-8")).hexdigest()

    record = {
        **{name: subscores[name] for name in COS_SUBSCORES},
        "commerce_opportunity_score": cos,
        "commerce_tier": commerce_tier,
        "csm_score": csm_score,
        "csm_tier": csm_tier,
        "hard_gate_status": hard_gate_status,
        "rights_confidence": _float3(inputs.get("rights_confidence")),
        "golden_age_factor": _float3(inputs.get("golden_age_factor")),
        "institutional_credit": _float3(inputs.get("institutional_credit")),
        "provenance_completeness": _float3(inputs.get("provenance_completeness")),
        "resolution_tier_score": _float3(inputs.get("resolution_tier_score")),
        "place_relevance_score": _float3(inputs.get("place_relevance_score")),
        "place_tier_score": _float3(inputs.get("place_tier_score")),
        "illustrator_prestige": _float3(inputs.get("illustrator_prestige")),
        "taxon_commercial_tier": inputs.get("taxon_commercial_tier"),
        "taxon_commercial_tier_score": _float3(inputs.get("taxon_commercial_tier_score")),
        "taxon_place_iconic": _float3(inputs.get("taxon_place_iconic")),
        "image_quality_score": _float3(inputs.get("image_quality_score")),
        "composition_fit": _float3(inputs.get("composition_fit")),
        "identification_confidence": _float3(inputs.get("identification_confidence")),
        "color_profile": inputs.get("color_profile"),
        "color_score": _float3(inputs.get("color_score")),
        "image_width_px": int(inputs.get("image_width_px") or 0),
        "resolution_tier": resolution_tier,
        "score_inputs": inputs,
        "input_hash_sha256": input_hash,
        "policy_stale": False,
        "requires_curator_review": bool(inputs.get("requires_curator_review", False)),
        "curator_review_reason": inputs.get("curator_review_reason"),
        "status": "active" if hard_gate_failure is None else "blocked",
    }
    record.update(_eligibility(record, policy))

    return ScoreComputation(
        score_inputs=inputs,
        score_outputs=score_outputs,
        commerce_record=record,
        input_hash_sha256=input_hash,
        audit_checksum_sha256=audit_checksum,
        event_at=now,
        hard_gate_failure=hard_gate_failure,
    )


def replay_score(policy: dict[str, Any], score_inputs: dict[str, Any], score_outputs: dict[str, Any]) -> bool:
    computed = compute_scores(policy, score_inputs, opportunity_id="replay").score_outputs
    for key, value in score_outputs.items():
        if key in {"scorer_version", "csm_scorer_version"}:
            if computed.get(key) != value:
                return False
        elif isinstance(value, dict):
            for nested_key, nested_value in value.items():
                if _float3(computed[key][nested_key]) != _float3(nested_value):
                    return False
        elif isinstance(value, (float, int)):
            if _float3(computed[key]) != _float3(value):
                return False
        elif computed.get(key) != value:
            return False
    return True
