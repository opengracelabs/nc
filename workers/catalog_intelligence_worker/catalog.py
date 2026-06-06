"""Deterministic Catalog Intelligence generation."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from workers.commerce_opportunity_worker.score import canonical_json

from . import WORKER_VERSION


@dataclass(frozen=True)
class CatalogCandidateDraft:
    product_recommendation_id: str
    commerce_opportunity_id: str
    opportunity_id: str
    catalog_policy_id: str
    product_family: str
    catalog_title: str
    catalog_description: str
    catalog_slug: str
    catalog_status: str
    catalog_basis: dict[str, Any]
    source_snapshot: dict[str, Any]
    media_requirements: dict[str, Any]
    rights_snapshot: dict[str, Any]
    provenance: dict[str, Any]


@dataclass(frozen=True)
class PricingProfileDraft:
    profile_key: str
    product_family: str
    product_type: str
    currency: str
    base_price_cents: int
    margin_floor_bps: int
    complexity_multiplier: float
    prestige_multiplier: float
    size_multiplier_rules: dict[str, Any]
    rounding_rule: dict[str, Any]
    price_band: str
    pricing_basis: dict[str, Any]


@dataclass(frozen=True)
class CatalogVariantDraft:
    variant_key: str
    variant_title: str
    product_family: str
    product_type: str
    variant_options: dict[str, Any]
    surface_spec: dict[str, Any]
    format_spec: dict[str, Any]
    dimension_spec: dict[str, Any]
    asset_requirements: dict[str, Any]
    price_snapshot: dict[str, Any]
    variant_status: str
    pricing_profile: PricingProfileDraft
    provenance: dict[str, Any]


def _slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "catalog-candidate"


def _label(value: str) -> str:
    return value.replace("_", " ").title()


def _decimal(value: Any) -> Decimal:
    return Decimal(str(value or 0))


def _round_price(cents: Decimal, rounding: dict[str, Any]) -> int:
    nearest = Decimal(str(rounding.get("nearest_cents", 100)))
    minus = Decimal(str(rounding.get("minus_cents", 1)))
    rounded = (cents / nearest).to_integral_value(rounding=ROUND_HALF_UP) * nearest
    return int(max(Decimal("1"), rounded - minus))


def _family_media_requirements(policy: dict[str, Any], family: str) -> dict[str, Any]:
    return dict(policy["catalog_rules"].get("media_requirements_by_family", {}).get(family, {"required_assets": ["source_image"]}))


def build_catalog_candidate(policy: dict[str, Any], recommendation: dict[str, Any], commerce: dict[str, Any]) -> CatalogCandidateDraft:
    if recommendation.get("status") != policy["eligibility_gates"].get("requires_product_recommendation_status", "curator_approved"):
        raise ValueError("product recommendation is not curator approved")
    if commerce.get("curator_decision") != "approved" or commerce.get("hard_gate_status") != "passed":
        raise ValueError("commerce opportunity is not approved and passed")
    if commerce.get("policy_stale") is True or commerce.get("commerce_tier") == "blocked":
        raise ValueError("commerce opportunity is stale or blocked")

    family = recommendation["recommended_product_family"]
    title_base = recommendation.get("title") or recommendation.get("catalog_title") or recommendation.get("source_title") or f"{_label(family)} Candidate"
    title = policy["catalog_rules"].get("title_template", "{asset_title} - {product_family_label}").format(
        asset_title=title_base,
        product_family_label=_label(family),
    )
    description = policy["catalog_rules"].get("description_template", "Internal catalog candidate generated from {source_title}.").format(
        source_title=title_base,
        product_family_label=_label(family),
    )
    slug_seed = f"{recommendation['id']}-{family}-{title}"
    slug = f"{_slug(title)}-{hashlib.sha1(slug_seed.encode('utf-8')).hexdigest()[:10]}"
    media_requirements = _family_media_requirements(policy, family)
    rights_snapshot = {
        "rights_confidence": commerce.get("rights_confidence"),
        "hard_gate_status": commerce.get("hard_gate_status"),
        "rights_basis": "approved_commerce_opportunity",
    }
    source_snapshot = {
        "product_recommendation_id": str(recommendation["id"]),
        "commerce_opportunity_id": str(commerce["id"]),
        "opportunity_id": str(commerce["opportunity_id"]),
        "recommended_product_family": family,
        "recommended_product_types": recommendation.get("recommended_product_types", {}),
        "recommendation_confidence": recommendation.get("recommendation_confidence"),
        "commerce_opportunity_score": commerce.get("commerce_opportunity_score"),
        "csm_score": commerce.get("csm_score"),
    }
    basis = {
        "catalog_policy_id": str(policy["id"]),
        "catalog_policy_version": policy["version"],
        "source_recommendation_status": recommendation.get("status"),
        "worker_version": WORKER_VERSION,
    }
    return CatalogCandidateDraft(
        product_recommendation_id=str(recommendation["id"]),
        commerce_opportunity_id=str(commerce["id"]),
        opportunity_id=str(commerce["opportunity_id"]),
        catalog_policy_id=str(policy["id"]),
        product_family=family,
        catalog_title=title,
        catalog_description=description,
        catalog_slug=slug,
        catalog_status="draft",
        catalog_basis=basis,
        source_snapshot=source_snapshot,
        media_requirements=media_requirements,
        rights_snapshot=rights_snapshot,
        provenance={"generated_by": WORKER_VERSION, "catalog_policy_version": policy["version"]},
    )


def build_pricing_profile(policy: dict[str, Any], family: str, product_type: str, commerce: dict[str, Any]) -> PricingProfileDraft:
    pricing = policy["pricing_rules"]
    profile = dict(pricing["profiles"][product_type])
    prestige = Decimal("1.15") if _decimal(commerce.get("csm_score")) >= Decimal("0.90") else Decimal("1.00")
    complexity = Decimal("1.10") if family in {"museum_print", "institutional_license"} else Decimal("1.00")
    return PricingProfileDraft(
        profile_key=f"{family}_{product_type}_v{policy['version']}",
        product_family=family,
        product_type=product_type,
        currency=pricing.get("currency", "USD"),
        base_price_cents=int(profile["base_price_cents"]),
        margin_floor_bps=int(profile["margin_floor_bps"]),
        complexity_multiplier=float(complexity),
        prestige_multiplier=float(prestige),
        size_multiplier_rules={"csm_masterwork_multiplier": float(prestige)},
        rounding_rule=dict(pricing.get("rounding", {"nearest_cents": 100, "minus_cents": 1})),
        price_band=profile["price_band"],
        pricing_basis={
            "catalog_policy_id": str(policy["id"]),
            "catalog_policy_version": policy["version"],
            "pricing_rule": "base_x_complexity_x_prestige_v1",
            "worker_version": WORKER_VERSION,
        },
    )


def _price_snapshot(profile: PricingProfileDraft) -> dict[str, Any]:
    cents = _decimal(profile.base_price_cents) * _decimal(profile.complexity_multiplier) * _decimal(profile.prestige_multiplier)
    final_cents = _round_price(cents, profile.rounding_rule)
    return {
        "currency": profile.currency,
        "base_price_cents": profile.base_price_cents,
        "final_price_cents": final_cents,
        "price_band": profile.price_band,
        "pricing_profile_key": profile.profile_key,
        "pricing_rule": profile.pricing_basis["pricing_rule"],
    }


def build_catalog_variants(policy: dict[str, Any], candidate: CatalogCandidateDraft, commerce: dict[str, Any]) -> list[CatalogVariantDraft]:
    family = candidate.product_family
    variants: list[CatalogVariantDraft] = []
    for rule in policy["variant_rules"].get(family, []):
        rule = dict(rule)
        product_type = rule["product_type"]
        pricing_profile = build_pricing_profile(policy, family, product_type, commerce)
        variant_key = rule["variant_key"]
        variants.append(
            CatalogVariantDraft(
                variant_key=variant_key,
                variant_title=f"{candidate.catalog_title} - {rule['title_suffix']}",
                product_family=family,
                product_type=product_type,
                variant_options={"variant_key": variant_key, "title_suffix": rule["title_suffix"]},
                surface_spec={"product_family": family, "product_type": product_type},
                format_spec={"internal_format": product_type},
                dimension_spec=dict(rule["dimensions"]),
                asset_requirements=dict(candidate.media_requirements),
                price_snapshot=_price_snapshot(pricing_profile),
                variant_status="draft",
                pricing_profile=pricing_profile,
                provenance={"generated_by": WORKER_VERSION, "catalog_policy_version": policy["version"]},
            )
        )
    variants.sort(key=lambda item: item.variant_key)
    return variants


def replay_catalog_generation(policy: dict[str, Any], recommendation: dict[str, Any], commerce: dict[str, Any], expected: dict[str, Any]) -> bool:
    candidate = build_catalog_candidate(policy, recommendation, commerce)
    variants = build_catalog_variants(policy, candidate, commerce)
    actual = {
        "candidate": candidate.__dict__,
        "variants": [
            {key: value for key, value in variant.__dict__.items() if key != "pricing_profile"}
            for variant in variants
        ],
    }
    return canonical_json(actual) == canonical_json(expected)
