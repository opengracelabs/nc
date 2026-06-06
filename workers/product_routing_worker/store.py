"""PostgreSQL operations for the Product Routing Worker."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from typing import Any

import asyncpg

from workers.commerce_opportunity_worker.score import canonical_json

from . import WORKER_VERSION
from .route import ProductRoute, route_product_families


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
        "product_surface_requirements": _jsonb(row["product_surface_requirements"]),
        "routing_formula_spec": _jsonb(row["routing_formula_spec"]),
        "family_caps": _jsonb(row["family_caps"]),
        "curator_gate_spec": _jsonb(row["curator_gate_spec"]),
    }


async def load_active_routing_policy(conn: asyncpg.Connection) -> dict[str, Any]:
    row = await conn.fetchrow(
        """
        SELECT id, version, product_surface_requirements, routing_formula_spec,
               family_caps, curator_gate_spec
        FROM product_routing_policy
        WHERE status = 'active'
        ORDER BY effective_from DESC NULLS LAST, created_at DESC
        LIMIT 1
        """
    )
    if row is None:
        raise RuntimeError("no active product_routing_policy found")
    return _decode_policy(row)


async def claim_routable_commerce_opportunities(
    conn: asyncpg.Connection,
    batch_size: int,
) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        """
        SELECT co.*
        FROM commerce_opportunities co
        WHERE co.curator_decision = 'approved'
          AND co.hard_gate_status = 'passed'
          AND co.policy_stale = FALSE
          AND co.commerce_tier <> 'blocked'
          AND NOT EXISTS (
              SELECT 1
              FROM product_recommendations pr
              WHERE pr.commerce_opportunity_id = co.id
                AND pr.status IN ('pending_curator_review','curator_approved','assigned','generated')
          )
        ORDER BY co.commerce_opportunity_score DESC, co.computed_at
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


def _route_checksum(
    commerce_record: dict[str, Any],
    route: ProductRoute,
    previous_checksum: str | None,
    event_at: datetime,
) -> str:
    surface = {
        "opportunity_id": str(commerce_record["opportunity_id"]),
        "event_type": "product_route_recommended",
        "event_at": event_at.isoformat(),
        "actor_id": WORKER_VERSION,
        "score_inputs": {
            "commerce_opportunity_id": str(commerce_record["id"]),
            "recommended_product_family": route.recommended_product_family,
            "routing_policy_id": route.provenance["routing_policy_id"],
        },
        "score_outputs": route.recommendation_basis,
        "previous_entry_checksum": previous_checksum,
    }
    return hashlib.sha256(canonical_json(surface).encode("utf-8")).hexdigest()


async def write_product_routes(
    conn: asyncpg.Connection,
    routing_policy: dict[str, Any],
    commerce_record: dict[str, Any],
    routes: list[ProductRoute],
    *,
    event_at: datetime | None = None,
) -> list[Any]:
    if not routes:
        return []

    now = event_at or datetime.now(UTC)
    opportunity_id = commerce_record["opportunity_id"]
    previous_checksum = await _previous_audit_checksum(conn, opportunity_id)
    recommendation_ids: list[Any] = []

    async with conn.transaction():
        for index, route in enumerate(routes):
            route_event_at = now + timedelta(microseconds=index)
            score_inputs = {
                "commerce_opportunity_id": str(commerce_record["id"]),
                "recommended_product_family": route.recommended_product_family,
                "routing_policy_id": str(routing_policy["id"]),
            }
            checksum = _route_checksum(commerce_record, route, previous_checksum, route_event_at)
            await conn.execute(
                """
                INSERT INTO score_audit_log (
                    opportunity_id, policy_version_id, event_type, event_at, actor_type,
                    actor_id, trigger, score_inputs, score_outputs, previous_state,
                    new_state, entry_checksum_sha256, previous_entry_checksum, reason,
                    generated_by
                ) VALUES (
                    $1, $2, 'product_route_recommended', $3, 'system_worker',
                    $4, 'initial', $5::jsonb, $6::jsonb, '{}'::jsonb,
                    $7::jsonb, $8, $9, $10, $11
                )
                """,
                opportunity_id,
                commerce_record["policy_version_id"],
                route_event_at,
                WORKER_VERSION,
                json.dumps(score_inputs, sort_keys=True),
                json.dumps(route.recommendation_basis, sort_keys=True),
                json.dumps(
                    {
                        "recommended_product_family": route.recommended_product_family,
                        "recommendation_confidence": route.recommendation_confidence,
                        "status": route.status,
                    },
                    sort_keys=True,
                ),
                checksum,
                previous_checksum,
                "Product route recommended",
                WORKER_VERSION,
            )
            row = await conn.fetchrow(
                """
                INSERT INTO product_recommendations (
                    opportunity_id, commerce_opportunity_id, policy_version_id,
                    recommended_product_family, recommended_product_types,
                    recommended_providers, recommendation_confidence,
                    recommendation_basis, status, provenance
                ) VALUES (
                    $1, $2, $3, $4, $5::jsonb, $6::jsonb, $7, $8::jsonb, $9, $10::jsonb
                )
                ON CONFLICT (opportunity_id, recommended_product_family) DO UPDATE SET
                    commerce_opportunity_id = EXCLUDED.commerce_opportunity_id,
                    policy_version_id = EXCLUDED.policy_version_id,
                    recommended_product_types = EXCLUDED.recommended_product_types,
                    recommended_providers = EXCLUDED.recommended_providers,
                    recommendation_confidence = EXCLUDED.recommendation_confidence,
                    recommendation_basis = EXCLUDED.recommendation_basis,
                    provenance = EXCLUDED.provenance,
                    updated_at = NOW()
                RETURNING id
                """,
                opportunity_id,
                commerce_record["id"],
                commerce_record["policy_version_id"],
                route.recommended_product_family,
                json.dumps(route.recommended_product_types, sort_keys=True),
                json.dumps(route.recommended_providers, sort_keys=True),
                route.recommendation_confidence,
                json.dumps(route.recommendation_basis, sort_keys=True),
                route.status,
                json.dumps(route.provenance, sort_keys=True),
            )
            recommendation_ids.append(row["id"])
            previous_checksum = checksum

    return recommendation_ids


async def route_commerce_opportunity(conn: asyncpg.Connection, routing_policy: dict[str, Any], commerce_record: dict[str, Any]) -> list[Any]:
    routes = route_product_families(routing_policy, commerce_record)
    return await write_product_routes(conn, routing_policy, commerce_record, routes)
