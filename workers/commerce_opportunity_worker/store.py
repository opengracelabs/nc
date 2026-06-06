"""PostgreSQL operations for the Commerce Opportunity Worker."""
from __future__ import annotations

import json
from typing import Any

import asyncpg

from . import WORKER_VERSION
from .score import ScoreComputation, compute_scores


_OPPORTUNITY_INPUT_COLS = """
    io.id AS opportunity_id,
    io.source,
    io.source_record_id,
    io.taxon_name,
    io.title,
    io.publication_title,
    io.illustrator,
    io.publication_year,
    io.rights_status,
    io.rights_verified_by,
    io.illustration_quality_score,
    io.historical_significance_score,
    io.provenance_score,
    io.opportunity_score,
    io.score_components,
    COALESCE(MAX(iop.relevance_score), 0) AS place_relevance_score,
    COALESCE(MAX(a.size_bytes), 0) AS asset_size_bytes,
    COALESCE(MAX(CASE WHEN a.checksum_sha256 IS NOT NULL THEN 1 ELSE 0 END), 0) AS has_asset_checksum,
    COALESCE(MAX(CASE WHEN ar.asset_id IS NOT NULL THEN 1 ELSE 0 END), 0) AS asset_rights_record_exists,
    COALESCE(MAX(CASE WHEN ar.rights_status IN ('Public Domain','CC0') THEN 1 ELSE 0 END), 0) AS asset_rights_public_domain,
    COALESCE(MAX(CASE WHEN ioe.evidence_type = 'rights' THEN 1 ELSE 0 END), 0) AS rights_evidence_exists,
    MAX(tctv.value) AS taxon_commercial_tier,
    COALESCE(MAX(tctv.score), 0) AS taxon_commercial_tier_score
"""


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
        "formula_spec": _jsonb(row["formula_spec"]),
        "tier_thresholds": _jsonb(row["tier_thresholds"]),
        "hard_gate_values": _jsonb(row["hard_gate_values"]),
        "product_surface_requirements": _jsonb(row["product_surface_requirements"]),
    }


async def load_active_policy(conn: asyncpg.Connection) -> dict[str, Any]:
    row = await conn.fetchrow(
        """
        SELECT id, version, formula_spec, tier_thresholds, hard_gate_values,
               product_surface_requirements
        FROM commerce_policy
        WHERE status = 'active'
        ORDER BY effective_from DESC NULLS LAST, created_at DESC
        LIMIT 1
        """
    )
    if row is None:
        raise RuntimeError("no active commerce_policy found")
    return _decode_policy(row)


async def claim_approved_opportunities(
    conn: asyncpg.Connection,
    batch_size: int,
) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        f"""
        SELECT {_OPPORTUNITY_INPUT_COLS}
        FROM illustration_opportunities io
        LEFT JOIN illustration_opportunity_places iop ON iop.opportunity_id = io.id
        LEFT JOIN illustration_opportunity_assets ioa ON ioa.opportunity_id = io.id
        LEFT JOIN assets a ON a.id = ioa.asset_id
        LEFT JOIN asset_rights ar ON ar.asset_id = a.id
        LEFT JOIN illustration_opportunity_evidence ioe ON ioe.opportunity_id = io.id
        LEFT JOIN taxon_commercial_tier_vocabulary tctv
               ON tctv.value = io.score_components->>'taxon_commercial_tier'
              AND tctv.status = 'active'
              AND tctv.approved_by IS NOT NULL
              AND tctv.approved_at IS NOT NULL
        WHERE io.status = 'approved'
          AND NOT EXISTS (
              SELECT 1
              FROM commerce_opportunities co
              WHERE co.opportunity_id = io.id
                AND co.policy_stale = FALSE
                AND co.status IN ('active','blocked')
          )
        GROUP BY io.id
        ORDER BY io.opportunity_score DESC, io.created_at
        LIMIT $1
        """,  # noqa: S608
        batch_size,
    )
    return [dict(row) for row in rows]


def _priority_illustrator_score(name: Any) -> float:
    if not name:
        return 0.0
    normalized = str(name).lower()
    priority_names = ("audubon", "gould", "merian", "redoute", "redouté", "lear", "nodder", "haeckel", "wolf")
    return 1.0 if any(item in normalized for item in priority_names) else 0.0


def _golden_age_factor(year: Any) -> float:
    if year is None:
        return 0.0
    try:
        value = int(year)
    except (TypeError, ValueError):
        return 0.0
    if 1750 <= value <= 1900:
        return 1.0
    if 1600 <= value < 1750 or 1900 < value <= 1930:
        return 0.45
    return 0.0


def build_input_snapshot(opportunity: dict[str, Any]) -> dict[str, Any]:
    components = opportunity.get("score_components") or {}
    if isinstance(components, str):
        components = json.loads(components)
    image_quality = float(opportunity.get("illustration_quality_score") or 0)
    publication_year = opportunity.get("publication_year")
    source = opportunity.get("source")
    source_is_loc = source == "loc"
    source_is_bhl = source == "bhl"
    illustrator_prestige = max(
        float(components.get("priority_illustrator_score") or 0),
        _priority_illustrator_score(opportunity.get("illustrator")),
    )
    golden_age = max(
        float(components.get("golden_age_priority_score") or 0),
        _golden_age_factor(publication_year),
    )
    rights_record_exists = bool(opportunity.get("asset_rights_record_exists")) or bool(opportunity.get("rights_evidence_exists"))
    rights_confidence = 1.0 if opportunity.get("rights_status") in {"Public Domain", "CC0"} and rights_record_exists else 0.0
    image_width_px = int(
        opportunity.get("image_width_px")
        or opportunity.get("width")
        or components.get("image_width_px")
        or 0
    )

    return {
        "rights_record_exists": rights_record_exists,
        "rights_confidence": rights_confidence,
        "golden_age_factor": golden_age,
        "institutional_credit": 1.0 if source_is_loc else 0.9 if source_is_bhl else 0.7,
        "provenance_completeness": float(opportunity.get("provenance_score") or 0.8),
        "place_relevance_score": float(opportunity.get("place_relevance_score") or 0),
        "place_tier_score": 1.0 if source_is_loc else 0.85,
        "illustrator_prestige": illustrator_prestige,
        "taxon_commercial_tier": opportunity.get("taxon_commercial_tier"),
        "taxon_commercial_tier_score": float(opportunity.get("taxon_commercial_tier_score") or 0),
        "taxon_place_iconic": float(opportunity.get("taxon_place_iconic") or opportunity.get("place_relevance_score") or 0),
        "image_quality_score": image_quality,
        "composition_fit": float(opportunity.get("composition_fit") or image_quality),
        "identification_confidence": 0.95 if opportunity.get("taxon_name") else 0.7,
        "color_profile": "chromolithograph" if illustrator_prestige >= 1.0 else "unknown",
        "color_score": float(opportunity.get("color_score") or (0.9 if illustrator_prestige >= 1.0 else 0.65)),
        "image_width_px": image_width_px,
        "requires_curator_review": illustrator_prestige >= 1.0 or source_is_loc,
        "curator_review_reason": "priority_illustrator" if illustrator_prestige >= 1.0 else "manual_flag" if source_is_loc else None,
    }


async def _previous_commerce_state(conn: asyncpg.Connection, opportunity_id: Any) -> dict[str, Any]:
    row = await conn.fetchrow(
        """
        SELECT id, policy_version_id, hard_gate_status, commerce_opportunity_score,
               commerce_tier, csm_score, csm_tier, input_hash_sha256, status
        FROM commerce_opportunities
        WHERE opportunity_id = $1
        """,
        opportunity_id,
    )
    return dict(row) if row else {}


async def _previous_audit_checksum(conn: asyncpg.Connection, opportunity_id: Any) -> str | None:
    row = await conn.fetchrow(
        """
        SELECT entry_checksum_sha256
        FROM score_audit_log
        WHERE opportunity_id = $1
        ORDER BY event_at DESC, created_at DESC, id DESC
        LIMIT 1
        """,
        opportunity_id,
    )
    return row["entry_checksum_sha256"] if row else None


async def write_score_and_opportunity(
    conn: asyncpg.Connection,
    policy: dict[str, Any],
    opportunity_id: Any,
    computation: ScoreComputation,
) -> Any:
    record = computation.commerce_record
    previous_state = await _previous_commerce_state(conn, opportunity_id)
    previous_checksum = await _previous_audit_checksum(conn, opportunity_id)
    recomputed = compute_scores(
        policy,
        computation.score_inputs,
        opportunity_id=str(opportunity_id),
        previous_entry_checksum=previous_checksum,
        event_at=computation.event_at,
    )

    async with conn.transaction():
        await conn.execute(
            """
            INSERT INTO score_audit_log (
                opportunity_id, policy_version_id, event_type, event_at, actor_type,
                actor_id, trigger, score_inputs, score_outputs, previous_state,
                new_state, entry_checksum_sha256, previous_entry_checksum, reason,
                generated_by
            ) VALUES (
                $1, $2, $3, $4, 'system_worker', $5, 'initial', $6::jsonb,
                $7::jsonb, $8::jsonb, $9::jsonb, $10, $11, $12, $13
            )
            """,
            opportunity_id,
            policy["id"],
            "score_computed" if recomputed.hard_gate_failure is None else "hard_gate_blocked",
            recomputed.event_at,
            WORKER_VERSION,
            json.dumps(recomputed.score_inputs, sort_keys=True),
            json.dumps(recomputed.score_outputs, sort_keys=True),
            json.dumps(previous_state, sort_keys=True, default=str),
            json.dumps(recomputed.commerce_record, sort_keys=True, default=str),
            recomputed.audit_checksum_sha256,
            previous_checksum,
            "Commerce opportunity score computed" if recomputed.hard_gate_failure is None else "Commerce opportunity blocked by hard gate",
            WORKER_VERSION,
        )
        row = await conn.fetchrow(
            """
            INSERT INTO commerce_opportunities (
                opportunity_id, policy_version_id, computed_at, computed_by,
                computation_trigger, policy_stale, last_scored_at, hard_gate_status,
                rights_confidence, golden_age_factor, institutional_credit,
                provenance_completeness, resolution_tier_score, place_relevance_score,
                place_tier_score, illustrator_prestige, taxon_commercial_tier,
                taxon_commercial_tier_score, taxon_place_iconic, image_quality_score,
                composition_fit, identification_confidence, color_profile, color_score,
                image_width_px, resolution_tier, museum_score, retail_score,
                publishing_score, tourism_score, reference_score,
                commerce_opportunity_score, commerce_tier, csm_score, csm_tier,
                eligible_wall_art_premium, eligible_wall_art_standard, eligible_calendar,
                eligible_puzzle, eligible_card, eligible_book_illustration,
                eligible_educational, eligible_museum_print,
                eligible_institutional_license, requires_curator_review,
                curator_review_reason, score_inputs, input_hash_sha256, status,
                provenance
            ) VALUES (
                $1, $2, $3, $4, 'initial', $5, $3, $6,
                $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17,
                $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28,
                $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39,
                $40, $41, $42, $43, $44, $45::jsonb, $46, $47, $48::jsonb
            )
            ON CONFLICT (opportunity_id) DO UPDATE SET
                policy_version_id = EXCLUDED.policy_version_id,
                computed_at = EXCLUDED.computed_at,
                computed_by = EXCLUDED.computed_by,
                computation_trigger = EXCLUDED.computation_trigger,
                policy_stale = EXCLUDED.policy_stale,
                last_scored_at = EXCLUDED.last_scored_at,
                hard_gate_status = EXCLUDED.hard_gate_status,
                rights_confidence = EXCLUDED.rights_confidence,
                golden_age_factor = EXCLUDED.golden_age_factor,
                institutional_credit = EXCLUDED.institutional_credit,
                provenance_completeness = EXCLUDED.provenance_completeness,
                resolution_tier_score = EXCLUDED.resolution_tier_score,
                place_relevance_score = EXCLUDED.place_relevance_score,
                place_tier_score = EXCLUDED.place_tier_score,
                illustrator_prestige = EXCLUDED.illustrator_prestige,
                taxon_commercial_tier = EXCLUDED.taxon_commercial_tier,
                taxon_commercial_tier_score = EXCLUDED.taxon_commercial_tier_score,
                taxon_place_iconic = EXCLUDED.taxon_place_iconic,
                image_quality_score = EXCLUDED.image_quality_score,
                composition_fit = EXCLUDED.composition_fit,
                identification_confidence = EXCLUDED.identification_confidence,
                color_profile = EXCLUDED.color_profile,
                color_score = EXCLUDED.color_score,
                image_width_px = EXCLUDED.image_width_px,
                resolution_tier = EXCLUDED.resolution_tier,
                museum_score = EXCLUDED.museum_score,
                retail_score = EXCLUDED.retail_score,
                publishing_score = EXCLUDED.publishing_score,
                tourism_score = EXCLUDED.tourism_score,
                reference_score = EXCLUDED.reference_score,
                commerce_opportunity_score = EXCLUDED.commerce_opportunity_score,
                commerce_tier = EXCLUDED.commerce_tier,
                csm_score = EXCLUDED.csm_score,
                csm_tier = EXCLUDED.csm_tier,
                eligible_wall_art_premium = EXCLUDED.eligible_wall_art_premium,
                eligible_wall_art_standard = EXCLUDED.eligible_wall_art_standard,
                eligible_calendar = EXCLUDED.eligible_calendar,
                eligible_puzzle = EXCLUDED.eligible_puzzle,
                eligible_card = EXCLUDED.eligible_card,
                eligible_book_illustration = EXCLUDED.eligible_book_illustration,
                eligible_educational = EXCLUDED.eligible_educational,
                eligible_museum_print = EXCLUDED.eligible_museum_print,
                eligible_institutional_license = EXCLUDED.eligible_institutional_license,
                requires_curator_review = EXCLUDED.requires_curator_review,
                curator_review_reason = EXCLUDED.curator_review_reason,
                score_inputs = EXCLUDED.score_inputs,
                input_hash_sha256 = EXCLUDED.input_hash_sha256,
                status = EXCLUDED.status,
                provenance = EXCLUDED.provenance,
                updated_at = NOW()
            RETURNING id
            """,
            opportunity_id,
            policy["id"],
            recomputed.event_at,
            WORKER_VERSION,
            record["policy_stale"],
            record["hard_gate_status"],
            record["rights_confidence"],
            record["golden_age_factor"],
            record["institutional_credit"],
            record["provenance_completeness"],
            record["resolution_tier_score"],
            record["place_relevance_score"],
            record["place_tier_score"],
            record["illustrator_prestige"],
            record["taxon_commercial_tier"],
            record["taxon_commercial_tier_score"],
            record["taxon_place_iconic"],
            record["image_quality_score"],
            record["composition_fit"],
            record["identification_confidence"],
            record["color_profile"],
            record["color_score"],
            record["image_width_px"],
            record["resolution_tier"],
            record["museum_score"],
            record["retail_score"],
            record["publishing_score"],
            record["tourism_score"],
            record["reference_score"],
            record["commerce_opportunity_score"],
            record["commerce_tier"],
            record["csm_score"],
            record["csm_tier"],
            record["eligible_wall_art_premium"],
            record["eligible_wall_art_standard"],
            record["eligible_calendar"],
            record["eligible_puzzle"],
            record["eligible_card"],
            record["eligible_book_illustration"],
            record["eligible_educational"],
            record["eligible_museum_print"],
            record["eligible_institutional_license"],
            record["requires_curator_review"],
            record["curator_review_reason"],
            json.dumps(record["score_inputs"], sort_keys=True),
            record["input_hash_sha256"],
            record["status"],
            json.dumps({"prov:wasGeneratedBy": WORKER_VERSION}, sort_keys=True),
        )
    return row["id"]


async def score_opportunity(conn: asyncpg.Connection, opportunity: dict[str, Any]) -> Any:
    policy = await load_active_policy(conn)
    inputs = build_input_snapshot(opportunity)
    computation = compute_scores(policy, inputs, opportunity_id=str(opportunity["opportunity_id"]))
    return await write_score_and_opportunity(conn, policy, opportunity["opportunity_id"], computation)
