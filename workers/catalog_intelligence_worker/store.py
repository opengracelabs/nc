"""PostgreSQL operations for Catalog Intelligence."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from typing import Any

import asyncpg

from workers.commerce_opportunity_worker.score import canonical_json

from . import WORKER_VERSION
from .catalog import CatalogCandidateDraft, CatalogVariantDraft, PricingProfileDraft, build_catalog_candidate, build_catalog_variants


def _jsonb(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, str):
        return json.loads(value)
    return dict(value)


def _decode_policy(row: Any) -> dict[str, Any]:
    return {
        "id": row["id"],
        "version": row["version"],
        "catalog_rules": _jsonb(row["catalog_rules"]),
        "variant_rules": _jsonb(row["variant_rules"]),
        "pricing_rules": _jsonb(row["pricing_rules"]),
        "eligibility_gates": _jsonb(row["eligibility_gates"]),
    }


async def load_active_catalog_policy(conn: asyncpg.Connection) -> dict[str, Any]:
    row = await conn.fetchrow(
        """
        SELECT id, version, catalog_rules, variant_rules, pricing_rules, eligibility_gates
        FROM catalog_policy
        WHERE status = 'active'
        ORDER BY effective_from DESC NULLS LAST, created_at DESC
        LIMIT 1
        """
    )
    if row is None:
        raise RuntimeError("no active catalog_policy found")
    return _decode_policy(row)


async def claim_catalog_recommendations(conn: asyncpg.Connection, batch_size: int) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        """
        SELECT
            pr.*,
            co.id AS co_id,
            co.opportunity_id AS co_opportunity_id,
            co.policy_version_id AS co_policy_version_id,
            co.curator_decision AS co_curator_decision,
            co.hard_gate_status AS co_hard_gate_status,
            co.policy_stale AS co_policy_stale,
            co.commerce_tier AS co_commerce_tier,
            co.rights_confidence AS co_rights_confidence,
            co.commerce_opportunity_score AS co_commerce_opportunity_score,
            co.csm_score AS co_csm_score
        FROM product_recommendations pr
        JOIN commerce_opportunities co ON co.id = pr.commerce_opportunity_id
        WHERE pr.status = 'curator_approved'
          AND co.curator_decision = 'approved'
          AND co.hard_gate_status = 'passed'
          AND co.policy_stale = FALSE
          AND co.commerce_tier <> 'blocked'
          AND NOT EXISTS (
              SELECT 1
              FROM catalog_candidates cc
              WHERE cc.product_recommendation_id = pr.id
                AND cc.catalog_status NOT IN ('retired','superseded')
          )
        ORDER BY pr.recommendation_confidence DESC NULLS LAST, pr.created_at
        LIMIT $1
        """,
        batch_size,
    )
    return [dict(row) for row in rows]


async def _previous_catalog_checksum(conn: asyncpg.Connection, candidate_id: Any | None, recommendation_id: Any | None, variant_id: Any | None) -> str | None:
    row = await conn.fetchrow(
        """
        SELECT entry_checksum_sha256
        FROM catalog_audit_log
        WHERE COALESCE(product_recommendation_id, catalog_candidate_id, catalog_variant_id)
              IS NOT DISTINCT FROM COALESCE($2::uuid, $1::uuid, $3::uuid)
        ORDER BY event_at DESC, created_at DESC, id DESC
        LIMIT 1
        """,
        candidate_id,
        recommendation_id,
        variant_id,
    )
    return row["entry_checksum_sha256"] if row else None


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if value.__class__.__name__ == "UUID":
        return str(value)
    return value


def _checksum(surface: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(_json_safe(surface)).encode("utf-8")).hexdigest()


def _audit_checksum(event_type: str, event_at: datetime, target: dict[str, Any], inputs: dict[str, Any], outputs: dict[str, Any], previous: str | None) -> str:
    return _checksum(
        {
            "event_type": event_type,
            "event_at": event_at.isoformat(),
            "actor_id": WORKER_VERSION,
            "target": target,
            "input_snapshot": inputs,
            "output_snapshot": outputs,
            "previous_entry_checksum": previous,
        }
    )


async def _write_audit(
    conn: asyncpg.Connection,
    *,
    event_type: str,
    catalog_policy_id: Any,
    product_recommendation_id: Any | None,
    catalog_candidate_id: Any | None,
    catalog_variant_id: Any | None,
    input_snapshot: dict[str, Any],
    output_snapshot: dict[str, Any],
    new_state: dict[str, Any],
    previous_checksum: str | None,
    event_at: datetime,
) -> str:
    target = {
        "product_recommendation_id": str(product_recommendation_id) if product_recommendation_id else None,
        "catalog_candidate_id": str(catalog_candidate_id) if catalog_candidate_id else None,
        "catalog_variant_id": str(catalog_variant_id) if catalog_variant_id else None,
    }
    checksum = _audit_checksum(event_type, event_at, target, input_snapshot, output_snapshot, previous_checksum)
    await conn.execute(
        """
        INSERT INTO catalog_audit_log (
            product_recommendation_id, catalog_candidate_id, catalog_variant_id,
            catalog_policy_id, event_type, event_at, actor_type, actor_id,
            trigger, input_snapshot, output_snapshot, previous_state, new_state,
            entry_checksum_sha256, previous_entry_checksum, reason, generated_by
        ) VALUES (
            $1, $2, $3, $4, $5, $6, 'system_worker', $7, 'initial',
            $8::jsonb, $9::jsonb, '{}'::jsonb, $10::jsonb, $11, $12, $13, $14
        )
        """,
        product_recommendation_id,
        catalog_candidate_id,
        catalog_variant_id,
        catalog_policy_id,
        event_type,
        event_at,
        WORKER_VERSION,
        json.dumps(input_snapshot, sort_keys=True, default=str),
        json.dumps(output_snapshot, sort_keys=True, default=str),
        json.dumps(new_state, sort_keys=True, default=str),
        checksum,
        previous_checksum,
        event_type.replace("_", " "),
        WORKER_VERSION,
    )
    return checksum


async def _upsert_pricing_profile(conn: asyncpg.Connection, policy: dict[str, Any], draft: PricingProfileDraft) -> Any:
    row = await conn.fetchrow(
        """
        INSERT INTO catalog_pricing_profiles (
            catalog_policy_id, profile_key, product_family, product_type, currency,
            base_price_cents, margin_floor_bps, complexity_multiplier,
            prestige_multiplier, size_multiplier_rules, rounding_rule, price_band,
            pricing_basis, status, provenance
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10::jsonb, $11::jsonb, $12,
            $13::jsonb, 'draft', $14::jsonb
        )
        ON CONFLICT (catalog_policy_id, profile_key) DO UPDATE SET
            base_price_cents = EXCLUDED.base_price_cents,
            margin_floor_bps = EXCLUDED.margin_floor_bps,
            complexity_multiplier = EXCLUDED.complexity_multiplier,
            prestige_multiplier = EXCLUDED.prestige_multiplier,
            size_multiplier_rules = EXCLUDED.size_multiplier_rules,
            rounding_rule = EXCLUDED.rounding_rule,
            price_band = EXCLUDED.price_band,
            pricing_basis = EXCLUDED.pricing_basis,
            updated_at = NOW()
        RETURNING id
        """,
        policy["id"],
        draft.profile_key,
        draft.product_family,
        draft.product_type,
        draft.currency,
        draft.base_price_cents,
        draft.margin_floor_bps,
        draft.complexity_multiplier,
        draft.prestige_multiplier,
        json.dumps(draft.size_multiplier_rules, sort_keys=True),
        json.dumps(draft.rounding_rule, sort_keys=True),
        draft.price_band,
        json.dumps(draft.pricing_basis, sort_keys=True),
        json.dumps({"generated_by": WORKER_VERSION}, sort_keys=True),
    )
    return row["id"]


async def write_catalog_candidate_and_variants(
    conn: asyncpg.Connection,
    policy: dict[str, Any],
    recommendation: dict[str, Any],
    commerce: dict[str, Any],
    *,
    event_at: datetime | None = None,
) -> tuple[Any, list[Any]]:
    now = event_at or datetime.now(UTC)
    candidate = build_catalog_candidate(policy, recommendation, commerce)
    variants = build_catalog_variants(policy, candidate, commerce)
    previous_checksum = await _previous_catalog_checksum(conn, None, recommendation["id"], None)

    async with conn.transaction():
        candidate_checksum = await _write_audit(
            conn,
            event_type="catalog_candidate_created",
            catalog_policy_id=policy["id"],
            product_recommendation_id=recommendation["id"],
            catalog_candidate_id=None,
            catalog_variant_id=None,
            input_snapshot={"recommendation": recommendation, "commerce": commerce},
            output_snapshot=candidate.__dict__,
            new_state={"catalog_slug": candidate.catalog_slug, "catalog_status": candidate.catalog_status},
            previous_checksum=previous_checksum,
            event_at=now,
        )
        row = await conn.fetchrow(
            """
            INSERT INTO catalog_candidates (
                product_recommendation_id, commerce_opportunity_id, opportunity_id,
                catalog_policy_id, product_family, catalog_title, catalog_description,
                catalog_slug, catalog_status, catalog_basis, source_snapshot,
                media_requirements, rights_snapshot, provenance
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10::jsonb, $11::jsonb,
                $12::jsonb, $13::jsonb, $14::jsonb
            )
            ON CONFLICT (product_recommendation_id) DO UPDATE SET
                catalog_policy_id = EXCLUDED.catalog_policy_id,
                product_family = EXCLUDED.product_family,
                catalog_title = EXCLUDED.catalog_title,
                catalog_description = EXCLUDED.catalog_description,
                catalog_slug = EXCLUDED.catalog_slug,
                catalog_basis = EXCLUDED.catalog_basis,
                source_snapshot = EXCLUDED.source_snapshot,
                media_requirements = EXCLUDED.media_requirements,
                rights_snapshot = EXCLUDED.rights_snapshot,
                provenance = EXCLUDED.provenance,
                updated_at = NOW()
            RETURNING id
            """,
            recommendation["id"],
            commerce["id"],
            commerce["opportunity_id"],
            policy["id"],
            candidate.product_family,
            candidate.catalog_title,
            candidate.catalog_description,
            candidate.catalog_slug,
            candidate.catalog_status,
            json.dumps(candidate.catalog_basis, sort_keys=True),
            json.dumps(candidate.source_snapshot, sort_keys=True, default=str),
            json.dumps(candidate.media_requirements, sort_keys=True),
            json.dumps(candidate.rights_snapshot, sort_keys=True, default=str),
            json.dumps(candidate.provenance, sort_keys=True),
        )
        candidate_id = row["id"]
        previous_checksum = candidate_checksum
        variant_ids: list[Any] = []
        for index, variant in enumerate(variants, start=1):
            pricing_profile_id = await _upsert_pricing_profile(conn, policy, variant.pricing_profile)
            event_time = now + timedelta(microseconds=index)
            previous_checksum = await _write_audit(
                conn,
                event_type="catalog_variant_created",
                catalog_policy_id=policy["id"],
                product_recommendation_id=recommendation["id"],
                catalog_candidate_id=candidate_id,
                catalog_variant_id=None,
                input_snapshot=candidate.__dict__,
                output_snapshot={key: value for key, value in variant.__dict__.items() if key != "pricing_profile"},
                new_state={"variant_key": variant.variant_key, "variant_status": variant.variant_status},
                previous_checksum=previous_checksum,
                event_at=event_time,
            )
            row = await conn.fetchrow(
                """
                INSERT INTO catalog_variants (
                    catalog_candidate_id, catalog_policy_id, pricing_profile_id,
                    variant_key, variant_title, product_family, product_type,
                    variant_options, surface_spec, format_spec, dimension_spec,
                    asset_requirements, price_snapshot, variant_status, provenance
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8::jsonb, $9::jsonb, $10::jsonb,
                    $11::jsonb, $12::jsonb, $13::jsonb, $14, $15::jsonb
                )
                ON CONFLICT (catalog_candidate_id, variant_key) DO UPDATE SET
                    pricing_profile_id = EXCLUDED.pricing_profile_id,
                    variant_title = EXCLUDED.variant_title,
                    variant_options = EXCLUDED.variant_options,
                    surface_spec = EXCLUDED.surface_spec,
                    format_spec = EXCLUDED.format_spec,
                    dimension_spec = EXCLUDED.dimension_spec,
                    asset_requirements = EXCLUDED.asset_requirements,
                    price_snapshot = EXCLUDED.price_snapshot,
                    provenance = EXCLUDED.provenance,
                    updated_at = NOW()
                RETURNING id
                """,
                candidate_id,
                policy["id"],
                pricing_profile_id,
                variant.variant_key,
                variant.variant_title,
                variant.product_family,
                variant.product_type,
                json.dumps(variant.variant_options, sort_keys=True),
                json.dumps(variant.surface_spec, sort_keys=True),
                json.dumps(variant.format_spec, sort_keys=True),
                json.dumps(variant.dimension_spec, sort_keys=True),
                json.dumps(variant.asset_requirements, sort_keys=True),
                json.dumps(variant.price_snapshot, sort_keys=True),
                variant.variant_status,
                json.dumps(variant.provenance, sort_keys=True),
            )
            variant_ids.append(row["id"])
    return candidate_id, variant_ids
