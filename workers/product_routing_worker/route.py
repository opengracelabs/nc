"""Deterministic product routing logic."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from . import WORKER_VERSION


@dataclass(frozen=True)
class ProductRoute:
    recommended_product_family: str
    recommended_product_types: dict[str, Any]
    recommended_providers: dict[str, Any]
    recommendation_confidence: float
    recommendation_basis: dict[str, Any]
    status: str
    provenance: dict[str, Any]


def _decimal(value: Any) -> Decimal:
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


def _float3(value: Decimal | float | int | None) -> float:
    decimal = _decimal(value)
    if decimal < 0:
        decimal = Decimal("0")
    if decimal > 1:
        decimal = Decimal("1")
    return float(decimal.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def _json_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    return dict(value)


def _passes_thresholds(record: dict[str, Any], requirement: dict[str, Any]) -> bool:
    checks = {
        "min_cos": record.get("commerce_opportunity_score"),
        "min_csm_score": record.get("csm_score"),
        "min_image_width_px": record.get("image_width_px"),
        "min_quality_score": record.get("image_quality_score"),
        "min_composition_fit": record.get("composition_fit"),
        "min_publishing_score": record.get("publishing_score"),
        "min_identification_confidence": record.get("identification_confidence"),
        "min_reference_score": record.get("reference_score"),
        "min_museum_score": record.get("museum_score"),
    }
    for threshold, actual in checks.items():
        if threshold in requirement and _decimal(actual) < _decimal(requirement[threshold]):
            return False
    return True


def _passes_flags(record: dict[str, Any], requirement: dict[str, Any]) -> bool:
    return all(bool(record.get(flag)) for flag in requirement.get("required_flags", []))


def _confidence(record: dict[str, Any], requirement: dict[str, Any], formula_spec: dict[str, Any]) -> float:
    weights = formula_spec.get("confidence_weights", {})
    basis_signal = requirement.get("basis_model", "commerce_opportunity_score")
    total = (
        _decimal(record.get("commerce_opportunity_score")) * _decimal(weights.get("commerce_opportunity_score", 0))
        + _decimal(record.get(basis_signal)) * _decimal(weights.get("basis_model_score", 0))
        + _decimal(record.get("csm_score")) * _decimal(weights.get("csm_score", 0))
    )
    return _float3(total)


def route_product_families(policy: dict[str, Any], commerce_record: dict[str, Any]) -> list[ProductRoute]:
    if commerce_record.get("hard_gate_status") != "passed":
        return []
    if commerce_record.get("commerce_tier") == "blocked":
        return []
    if commerce_record.get("policy_stale") is True:
        return []
    if commerce_record.get("curator_decision") != "approved":
        return []

    requirements = _json_dict(policy.get("product_surface_requirements"))
    formula_spec = _json_dict(policy.get("routing_formula_spec"))
    family_caps = _json_dict(policy.get("family_caps"))
    max_routes = int(family_caps.get("max_recommendations_per_opportunity") or len(requirements))
    status = formula_spec.get("status_on_create", "pending_curator_review")

    routes: list[ProductRoute] = []
    for family, requirement in requirements.items():
        requirement = _json_dict(requirement)
        if not _passes_flags(commerce_record, requirement):
            continue
        if not _passes_thresholds(commerce_record, requirement):
            continue

        basis_model = requirement.get("basis_model", "commerce_opportunity_score")
        confidence = _confidence(commerce_record, requirement, formula_spec)
        recommendation_basis = {
            "routing_policy_id": str(policy.get("id")),
            "routing_policy_version": policy.get("version"),
            "routing_scorer_version": formula_spec.get("routing_scorer_version"),
            "basis_model": basis_model,
            "basis_model_score": _float3(commerce_record.get(basis_model)),
            "commerce_opportunity_score": _float3(commerce_record.get("commerce_opportunity_score")),
            "csm_score": _float3(commerce_record.get("csm_score")),
            "thresholds_applied": {
                key: requirement[key]
                for key in sorted(requirement)
                if key.startswith("min_") or key == "required_flags"
            },
            "worker_version": WORKER_VERSION,
        }
        routes.append(
            ProductRoute(
                recommended_product_family=family,
                recommended_product_types={"types": list(requirement.get("recommended_product_types", []))},
                recommended_providers={},
                recommendation_confidence=confidence,
                recommendation_basis=recommendation_basis,
                status=status,
                provenance={
                    "routing_policy_id": str(policy.get("id")),
                    "routing_policy_version": policy.get("version"),
                    "generated_by": WORKER_VERSION,
                },
            )
        )

    routes.sort(key=lambda route: (-route.recommendation_confidence, route.recommended_product_family))
    return routes[:max_routes]
