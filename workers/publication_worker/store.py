"""PostgreSQL operations for Publication Intelligence."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

import asyncpg

from workers.commerce_opportunity_worker.score import canonical_json

from . import WORKER_VERSION
from .publication import PublicationCandidateDraft, build_publication_candidate


def _jsonb(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, str):
        return json.loads(value)
    return dict(value)


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if value.__class__.__name__ == "UUID":
        return str(value)
    return value


def _decode_policy(row: Any) -> dict[str, Any]:
    return {
        "id": row["id"],
        "version": row["version"],
        "eligibility_gates": _jsonb(row["eligibility_gates"]),
        "channel_fit_rules": _jsonb(row["channel_fit_rules"]),
        "publication_readiness_rules": _jsonb(row["publication_readiness_rules"]),
        "risk_rules": _jsonb(row["risk_rules"]),
        "ranking_rules": _jsonb(row["ranking_rules"]),
        "staleness_rules": _jsonb(row["staleness_rules"]),
    }


async def load_active_publication_policy(conn: asyncpg.Connection) -> dict[str, Any]:
    row = await conn.fetchrow(
        """
        SELECT id, version, eligibility_gates, channel_fit_rules,
               publication_readiness_rules, risk_rules, ranking_rules, staleness_rules
        FROM publication_policy
        WHERE status = 'active'
        ORDER BY effective_from DESC NULLS LAST, created_at DESC
        LIMIT 1
        """
    )
    if row is None:
        raise RuntimeError("no active publication_policy found")
    return _decode_policy(row)


async def load_active_channel_profiles(conn: asyncpg.Connection, publication_policy_id: Any) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        """
        SELECT *
        FROM publication_channel_profiles
        WHERE publication_policy_id = $1
          AND status IN ('draft','approved')
        ORDER BY sort_order, profile_key
        """,
        publication_policy_id,
    )
    return [dict(row) for row in rows]


async def claim_publication_inputs(conn: asyncpg.Connection, batch_size: int) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        """
        SELECT
+            cc.id AS catalog_candidate_id,
+            cv.id AS catalog_variant_id,
+            cc.*, cv.*,
+            co.id AS co_id,
+            co.curator_decision AS co_curator_decision,
+            co.hard_gate_status AS co_hard_gate_status,
+            co.policy_stale AS co_policy_stale,
+            co.commerce_tier AS co_commerce_tier,
+            co.commerce_opportunity_score AS co_commerce_opportunity_score,
+            co.csm_score AS co_csm_score
        FROM catalog_candidates cc
        JOIN catalog_variants cv ON cv.catalog_candidate_id = cc.id
        JOIN product_recommendations pr ON pr.id = cc.product_recommendation_id
        JOIN commerce_opportunities co ON co.id = cc.commerce_opportunity_id
        WHERE cc.catalog_status IN ('draft','approved')
          AND cv.variant_status IN ('draft','approved')
          AND pr.status = 'curator_approved'
          AND co.curator_decision = 'approved'
          AND co.hard_gate_status = 'passed'
          AND co.policy_stale = FALSE
          AND co.commerce_tier <> 'blocked'
          AND NOT EXISTS (
              SELECT 1 FROM publication_candidates pc
              WHERE pc.catalog_variant_id = cv.id
                AND pc.publication_status NOT IN ('retired','superseded','stale')
          )
        ORDER BY cc.created_at, cv.variant_key
        LIMIT $1
        """.replace('+            ', '            '),
        batch_size,
    )
    return [dict(row) for row in rows]


def _checksum(surface: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(_json_safe(surface)).encode("utf-8")).hexdigest()


async def _previous_checksum(conn: asyncpg.Connection, publication_candidate_id: Any | None, catalog_variant_id: Any | None, catalog_candidate_id: Any | None) -> str | None:
    row = await conn.fetchrow(
        """
        SELECT entry_checksum_sha256
        FROM publication_audit_log
        WHERE COALESCE(publication_candidate_id, catalog_variant_id, catalog_candidate_id)
              IS NOT DISTINCT FROM COALESCE($1::uuid, $2::uuid, $3::uuid)
        ORDER BY event_at DESC, created_at DESC, id DESC
        LIMIT 1
        """,
        publication_candidate_id,
        catalog_variant_id,
        catalog_candidate_id,
    )
    return row["entry_checksum_sha256"] if row else None


async def _write_audit(conn: asyncpg.Connection, policy_id: Any, draft: PublicationCandidateDraft, event_type: str, previous: str | None, event_at: datetime) -> str:
    surface = {
        "event_type": event_type,
        "event_at": event_at.isoformat(),
        "actor_id": WORKER_VERSION,
        "catalog_variant_id": draft.catalog_variant_id,
        "input_snapshot": draft.input_snapshot,
        "output_snapshot": draft.decision_basis,
        "previous_entry_checksum": previous,
    }
    checksum = _checksum(surface)
    await conn.execute(
        """
        INSERT INTO publication_audit_log (
            publication_candidate_id, catalog_candidate_id, catalog_variant_id,
            publication_policy_id, event_type, event_at, actor_type, actor_id,
            trigger, input_snapshot, output_snapshot, previous_state, new_state,
            entry_checksum_sha256, previous_entry_checksum, reason, generated_by
        ) VALUES (
            NULL, $1, $2, $3, $4, $5, 'system_worker', $6, 'initial',
            $7::jsonb, $8::jsonb, '{}'::jsonb, $9::jsonb, $10, $11, $12, $13
        )
        """,
        draft.catalog_candidate_id,
        draft.catalog_variant_id,
        policy_id,
        event_type,
        event_at,
        WORKER_VERSION,
        json.dumps(draft.input_snapshot, sort_keys=True),
        json.dumps(draft.decision_basis, sort_keys=True),
        json.dumps({"decision": draft.decision, "publication_score": draft.publication_score}, sort_keys=True),
        checksum,
        previous,
        event_type.replace("_", " "),
        WORKER_VERSION,
    )
    return checksum


async def write_publication_candidate(conn: asyncpg.Connection, policy: dict[str, Any], channel_profile: dict[str, Any], catalog_candidate: dict[str, Any], catalog_variant: dict[str, Any], commerce: dict[str, Any], *, event_at: datetime | None = None) -> Any:
    now = event_at or datetime.now(UTC)
    draft = build_publication_candidate(policy, channel_profile, catalog_candidate, catalog_variant, commerce)
    previous = await _previous_checksum(conn, None, catalog_variant["id"], catalog_candidate["id"])
    async with conn.transaction():
        await _write_audit(conn, policy["id"], draft, "publication_candidate_created", previous, now)
        row = await conn.fetchrow(
            """
            INSERT INTO publication_candidates (
                catalog_candidate_id, catalog_variant_id, publication_policy_id,
                publication_channel_profile_id, product_recommendation_id,
                commerce_opportunity_id, opportunity_id, publication_status,
                publication_priority, readiness_score, channel_fit_score, risk_score,
                publication_score, decision, decision_basis, input_snapshot,
                staleness_status, provenance
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
                $13, $14, $15::jsonb, $16::jsonb, $17, $18::jsonb
            )
            ON CONFLICT (catalog_variant_id, publication_channel_profile_id) DO UPDATE SET
                publication_policy_id = EXCLUDED.publication_policy_id,
                publication_status = EXCLUDED.publication_status,
                publication_priority = EXCLUDED.publication_priority,
                readiness_score = EXCLUDED.readiness_score,
                channel_fit_score = EXCLUDED.channel_fit_score,
                risk_score = EXCLUDED.risk_score,
                publication_score = EXCLUDED.publication_score,
                decision = EXCLUDED.decision,
                decision_basis = EXCLUDED.decision_basis,
                input_snapshot = EXCLUDED.input_snapshot,
                staleness_status = EXCLUDED.staleness_status,
                provenance = EXCLUDED.provenance,
                updated_at = NOW()
            RETURNING id
            """,
            draft.catalog_candidate_id,
            draft.catalog_variant_id,
            policy["id"],
            channel_profile["id"],
            draft.product_recommendation_id,
            draft.commerce_opportunity_id,
            draft.opportunity_id,
            draft.publication_status,
            draft.publication_priority,
            draft.readiness_score,
            draft.channel_fit_score,
            draft.risk_score,
            draft.publication_score,
            draft.decision,
            json.dumps(draft.decision_basis, sort_keys=True),
            json.dumps(draft.input_snapshot, sort_keys=True),
            draft.staleness_status,
            json.dumps(draft.provenance, sort_keys=True),
        )
    return row["id"]
