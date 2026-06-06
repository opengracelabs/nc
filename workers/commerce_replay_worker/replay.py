"""Replay verification for Commerce Intelligence audit entries."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import asyncpg

from workers.commerce_opportunity_worker.score import canonical_json, compute_scores, replay_score
from workers.commerce_opportunity_worker.store import _decode_policy

from . import WORKER_VERSION


@dataclass(frozen=True)
class ReplayResult:
    audit_id: Any
    opportunity_id: Any
    verified: bool
    expected_event_type: str
    reason: str


def _jsonb(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, str):
        return json.loads(value)
    return dict(value)


def verify_audit_entry(policy: dict[str, Any], audit_entry: dict[str, Any]) -> ReplayResult:
    score_inputs = _jsonb(audit_entry["score_inputs"])
    score_outputs = _jsonb(audit_entry["score_outputs"])
    verified = replay_score(policy, score_inputs, score_outputs)
    return ReplayResult(
        audit_id=audit_entry["id"],
        opportunity_id=audit_entry["opportunity_id"],
        verified=verified,
        expected_event_type="replay_verified" if verified else "replay_failure",
        reason="Replay verified deterministic score outputs" if verified else "Replay failed deterministic score output verification",
    )


async def load_policy_for_audit(conn: asyncpg.Connection, policy_version_id: Any) -> dict[str, Any]:
    row = await conn.fetchrow(
        """
        SELECT id, version, formula_spec, tier_thresholds, hard_gate_values,
               product_surface_requirements
        FROM commerce_policy
        WHERE id = $1
        """,
        policy_version_id,
    )
    if row is None:
        raise RuntimeError(f"commerce_policy {policy_version_id} not found")
    return _decode_policy(row)


async def claim_replay_entries(conn: asyncpg.Connection, batch_size: int) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        """
        SELECT sal.id, sal.opportunity_id, sal.policy_version_id, sal.event_type,
               sal.event_at, sal.actor_id, sal.score_inputs, sal.score_outputs,
               sal.entry_checksum_sha256
        FROM score_audit_log sal
        WHERE sal.event_type IN ('score_computed','hard_gate_blocked')
          AND NOT EXISTS (
              SELECT 1
              FROM score_audit_log replay
              WHERE replay.opportunity_id = sal.opportunity_id
                AND replay.previous_entry_checksum = sal.entry_checksum_sha256
                AND replay.event_type IN ('replay_verified','replay_failure')
          )
        ORDER BY sal.event_at, sal.created_at
        LIMIT $1
        """,
        batch_size,
    )
    return [dict(row) for row in rows]


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


def _replay_checksum(opportunity_id: Any, event_type: str, event_at: datetime, score_inputs: dict[str, Any], score_outputs: dict[str, Any]) -> str:
    surface = {
        "opportunity_id": str(opportunity_id),
        "event_type": event_type,
        "event_at": event_at.isoformat(),
        "actor_id": WORKER_VERSION,
        "score_inputs": score_inputs,
        "score_outputs": score_outputs,
    }
    return hashlib.sha256(canonical_json(surface).encode("utf-8")).hexdigest()


async def write_replay_result(conn: asyncpg.Connection, policy: dict[str, Any], audit_entry: dict[str, Any], result: ReplayResult) -> None:
    now = datetime.now(UTC)
    score_inputs = _jsonb(audit_entry["score_inputs"])
    score_outputs = {
        "replay_verified": result.verified,
        "replayed_audit_id": str(audit_entry["id"]),
        "replayed_event_type": audit_entry["event_type"],
    }
    previous_checksum = await _previous_audit_checksum(conn, audit_entry["opportunity_id"])
    checksum = _replay_checksum(audit_entry["opportunity_id"], result.expected_event_type, now, score_inputs, score_outputs)

    async with conn.transaction():
        await conn.execute(
            """
            INSERT INTO score_audit_log (
                opportunity_id, policy_version_id, event_type, event_at, actor_type,
                actor_id, trigger, score_inputs, score_outputs, previous_state,
                new_state, entry_checksum_sha256, previous_entry_checksum, reason,
                generated_by
            ) VALUES (
                $1, $2, $3, $4, 'system_worker', $5, 'manual_recompute', $6::jsonb,
                $7::jsonb, '{}'::jsonb, '{}'::jsonb, $8, $9, $10, $11
            )
            """,
            audit_entry["opportunity_id"],
            policy["id"],
            result.expected_event_type,
            now,
            WORKER_VERSION,
            json.dumps(score_inputs, sort_keys=True),
            json.dumps(score_outputs, sort_keys=True),
            checksum,
            previous_checksum,
            result.reason,
            WORKER_VERSION,
        )
        if not result.verified:
            await conn.execute(
                """
                UPDATE commerce_opportunities
                SET status = 'integrity_suspect', updated_at = NOW()
                WHERE opportunity_id = $1
                """,
                audit_entry["opportunity_id"],
            )


async def replay_entry(conn: asyncpg.Connection, audit_entry: dict[str, Any]) -> ReplayResult:
    policy = await load_policy_for_audit(conn, audit_entry["policy_version_id"])
    result = verify_audit_entry(policy, audit_entry)
    await write_replay_result(conn, policy, audit_entry, result)
    return result


async def run_once(conn: asyncpg.Connection, batch_size: int) -> int:
    entries = await claim_replay_entries(conn, batch_size)
    for entry in entries:
        await replay_entry(conn, entry)
    return len(entries)
