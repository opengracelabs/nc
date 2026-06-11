"""NC-PRODUCT-001 product runtime APIs."""

import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from services.product.audit import build_audit_event
from services.product.export import build_product_snapshot_export
from services.product.provider.manual import (
    build_manual_export_manifest,
    build_manual_export_package,
)
from services.product.rights_gate import verify_candidate_gates
from services.product.state_machine import activation_actions, transition_activation_state

from ..dependencies import DB, Auth

router = APIRouter(prefix="/products", tags=["products"])

_LINE_COLS = """
    id, slug, title, status, anchor_slug, commercial_allowed,
    manual_provider_only, product_policy, provenance, created_at, updated_at
"""

_TEMPLATE_COLS = """
    id, product_line_id, slug, title, product_type, min_width_px, min_height_px,
    aspect_ratio, surface_spec, export_spec, provenance, created_at, updated_at
"""

_CANDIDATE_COLS = """
    id, product_line_id, product_template_id, candidate_key, title, status,
    source_anchor_slug, source, source_record_id, source_url, asset_snapshot,
    rights_snapshot, assembled_attribution, gate_result, provenance, created_at, updated_at
"""

_CANDIDATE_LIST_COLS = """
    pc.id, pc.product_line_id, pc.product_template_id, pc.candidate_key, pc.title, pc.status,
    pc.source_anchor_slug, pc.source, pc.source_record_id, pc.source_url, pc.asset_snapshot,
    pc.rights_snapshot, pc.assembled_attribution, pc.gate_result, pc.provenance,
    pc.created_at, pc.updated_at
"""

_PUBLICATION_COLS = """
    id, product_candidate_id, publication_version, publication_status, provider,
    snapshot, snapshot_sha256, manual_export_manifest, created_by, provenance,
    published_at, created_at, updated_at, activation_state
"""

_PACKAGE_COLS = """
    id, product_publication_id, package_version, package_status, provider,
    package_manifest, package_sha256, snapshot_export, generated_by, provenance,
    generated_at, updated_at
"""

_AUDIT_COLS = """
    id, product_publication_id, product_package_id, event_type, actor,
    previous_state, new_state, event, event_sha256, created_at
"""

_FIRST_SALE_COLS = """
    id, product_code, product_publication_id, product_package_id, activation_status,
    gate_e_session, snapshot_sha256, package_sha256, manual_provider_only,
    activated_by, activated_at, provenance, created_at, updated_at
"""

_JSON_FIELDS = {
    "product_policy",
    "provenance",
    "surface_spec",
    "export_spec",
    "asset_snapshot",
    "rights_snapshot",
    "assembled_attribution",
    "gate_result",
    "snapshot",
    "manual_export_manifest",
    "package_manifest",
    "snapshot_export",
    "previous_state",
    "new_state",
    "event",
    "gate_e_session",
}


class PublicationWorkflowAction(BaseModel):
    action: str = Field(pattern="^(verify|package|activate|pause|resume|retract)$")
    actor: str = Field(min_length=1)


def _decode(row) -> dict:
    item = dict(row)
    for field in _JSON_FIELDS:
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item


async def _get_line(conn: DB, line_slug: str) -> dict:
    row = await conn.fetchrow(f"SELECT {_LINE_COLS} FROM product_line WHERE slug = $1", line_slug)
    if not row:
        raise HTTPException(404, "Product line not found")
    return _decode(row)


async def _get_template(conn: DB, template_id: UUID | str) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_TEMPLATE_COLS} FROM product_template WHERE id = $1", template_id
    )
    if not row:
        raise HTTPException(404, "Product template not found")
    return _decode(row)


async def _get_candidate(conn: DB, candidate_id: UUID | str) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_CANDIDATE_COLS} FROM product_candidate WHERE id = $1", candidate_id
    )
    if not row:
        raise HTTPException(404, "Product candidate not found")
    return _decode(row)


async def _get_publication(conn: DB, publication_id: UUID | str) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_PUBLICATION_COLS} FROM product_publication WHERE id = $1", publication_id
    )
    if not row:
        raise HTTPException(404, "Product publication not found")
    return _decode(row)


async def _latest_package(conn: DB, publication_id: UUID | str) -> dict | None:
    row = await conn.fetchrow(
        f"SELECT {_PACKAGE_COLS} FROM product_manual_export_package "
        "WHERE product_publication_id = $1 ORDER BY generated_at DESC LIMIT 1",
        publication_id,
    )
    return _decode(row) if row else None


async def _write_audit(conn: DB, audit: dict, package_id: UUID | str | None = None) -> None:
    await conn.execute(
        """
        INSERT INTO product_audit_event (
            product_publication_id, product_package_id, event_type, actor,
            previous_state, new_state, event, event_sha256
        )
        VALUES ($1, $2, $3, $4, $5::jsonb, $6::jsonb, $7::jsonb, $8)
        ON CONFLICT (event_sha256) DO NOTHING
        """,
        audit["entity_id"],
        package_id,
        audit["event_type"],
        audit["actor"],
        json.dumps(audit["previous_state"]),
        json.dumps(audit["new_state"]),
        json.dumps(audit["event"]),
        audit["event_sha256"],
    )


@router.get("/lines")
async def list_product_lines(auth: Auth, conn: DB, status: str | None = Query(None)) -> list[dict]:
    if status:
        rows = await conn.fetch(
            f"SELECT {_LINE_COLS} FROM product_line WHERE status = $1 ORDER BY slug", status
        )
    else:
        rows = await conn.fetch(f"SELECT {_LINE_COLS} FROM product_line ORDER BY slug")
    return [_decode(row) for row in rows]


@router.get("/lines/{line_slug}")
async def get_product_line(line_slug: str, auth: Auth, conn: DB) -> dict:
    line = await _get_line(conn, line_slug)
    templates = await conn.fetch(
        f"SELECT {_TEMPLATE_COLS} FROM product_template WHERE product_line_id = $1 ORDER BY slug",
        line["id"],
    )
    candidates = await conn.fetch(
        f"SELECT {_CANDIDATE_COLS} FROM product_candidate WHERE product_line_id = $1 "
        "ORDER BY candidate_key",
        line["id"],
    )
    line["templates"] = [_decode(row) for row in templates]
    line["candidates"] = [_decode(row) for row in candidates]
    return line


@router.get("/candidates")
async def list_product_candidates(
    auth: Auth,
    conn: DB,
    line_slug: str | None = Query(None),
    status: str | None = Query(None),
) -> list[dict]:
    filters = []
    args: list = []
    join = ""
    if line_slug:
        join = "JOIN product_line pl ON pl.id = pc.product_line_id"
        args.append(line_slug)
        filters.append(f"pl.slug = ${len(args)}")
    if status:
        args.append(status)
        filters.append(f"pc.status = ${len(args)}")
    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    rows = await conn.fetch(
        f"SELECT {_CANDIDATE_LIST_COLS} FROM product_candidate pc {join} {where} "
        "ORDER BY pc.candidate_key",
        *args,
    )
    return [_decode(row) for row in rows]


@router.get("/candidates/{candidate_id}")
async def get_product_candidate(candidate_id: UUID, auth: Auth, conn: DB) -> dict:
    candidate = await _get_candidate(conn, candidate_id)
    template = await _get_template(conn, candidate["product_template_id"])
    candidate["verification"] = verify_candidate_gates(candidate, template)
    return candidate


@router.get("/candidates/{candidate_id}/verify")
async def verify_product_candidate(candidate_id: UUID, auth: Auth, conn: DB) -> dict:
    candidate = await _get_candidate(conn, candidate_id)
    template = await _get_template(conn, candidate["product_template_id"])
    return {"candidate_id": str(candidate_id), **verify_candidate_gates(candidate, template)}


@router.get("/publications")
async def list_product_publications(
    auth: Auth,
    conn: DB,
    provider: str | None = Query(None),
) -> list[dict]:
    if provider:
        rows = await conn.fetch(
            f"SELECT {_PUBLICATION_COLS} FROM product_publication "
            "WHERE provider = $1 ORDER BY created_at DESC",
            provider,
        )
    else:
        rows = await conn.fetch(
            f"SELECT {_PUBLICATION_COLS} FROM product_publication ORDER BY created_at DESC"
        )
    return [_decode(row) for row in rows]


@router.get("/publications/{publication_id}")
async def get_product_publication(publication_id: UUID, auth: Auth, conn: DB) -> dict:
    return await _get_publication(conn, publication_id)


@router.get("/publications/{publication_id}/manual-export")
async def get_manual_export_manifest(publication_id: UUID, auth: Auth, conn: DB) -> dict:
    publication = await _get_publication(conn, publication_id)
    if publication["provider"] != "manual":
        raise HTTPException(422, "Only manual provider is enabled for NC-PRODUCT-001 Sprint 1")
    return build_manual_export_manifest(publication)


@router.get("/publications/{publication_id}/snapshot-export")
async def get_product_snapshot_export(publication_id: UUID, auth: Auth, conn: DB) -> dict:
    publication = await _get_publication(conn, publication_id)
    return build_product_snapshot_export(publication)


@router.get("/publications/{publication_id}/packages")
async def list_manual_export_packages(publication_id: UUID, auth: Auth, conn: DB) -> list[dict]:
    await _get_publication(conn, publication_id)
    rows = await conn.fetch(
        f"SELECT {_PACKAGE_COLS} FROM product_manual_export_package "
        "WHERE product_publication_id = $1 ORDER BY generated_at DESC",
        publication_id,
    )
    return [_decode(row) for row in rows]


@router.get("/publications/{publication_id}/audit-events")
async def list_product_audit_events(publication_id: UUID, auth: Auth, conn: DB) -> list[dict]:
    await _get_publication(conn, publication_id)
    rows = await conn.fetch(
        f"SELECT {_AUDIT_COLS} FROM product_audit_event "
        "WHERE product_publication_id = $1 ORDER BY created_at DESC",
        publication_id,
    )
    return [_decode(row) for row in rows]


@router.post("/publications/{publication_id}/workflow")
async def run_product_publication_workflow(
    publication_id: UUID, body: PublicationWorkflowAction, auth: Auth, conn: DB
) -> dict:
    publication = await _get_publication(conn, publication_id)
    previous_state = publication.get("activation_state") or "ready"
    action = body.action

    if action == "verify":
        new_state = (
            transition_activation_state("draft", "verify")
            if previous_state == "draft"
            else previous_state
        )
    else:
        new_state = transition_activation_state(previous_state, action)

    package = await _latest_package(conn, publication_id)
    if action in {"activate", "pause", "resume", "retract"} and not package:
        raise HTTPException(422, "Manual export package must exist before this workflow action")

    async with conn.transaction():
        package_id = package["id"] if package else None
        event_type = "publication_verified"
        event_payload = {"action": action, "allowed_next_actions": activation_actions(new_state)}

        if action == "package":
            publication_for_package = {**publication, "activation_state": new_state}
            package_payload = build_manual_export_package(publication_for_package)
            package_row = await conn.fetchrow(
                f"""
                INSERT INTO product_manual_export_package (
                    product_publication_id, package_version, package_status, provider,
                    package_manifest, package_sha256, snapshot_export, generated_by, provenance
                )
                VALUES ($1, 'nc-commerce-002-api-v1', 'generated', 'manual',
                        $2::jsonb, $3, $4::jsonb, $5, $6::jsonb)
                ON CONFLICT (product_publication_id, package_version) DO UPDATE SET
                    package_manifest = EXCLUDED.package_manifest,
                    package_sha256 = EXCLUDED.package_sha256,
                    snapshot_export = EXCLUDED.snapshot_export,
                    generated_by = EXCLUDED.generated_by,
                    provenance = product_manual_export_package.provenance || EXCLUDED.provenance,
                    updated_at = NOW()
                RETURNING {_PACKAGE_COLS}
                """,
                publication_id,
                json.dumps(package_payload),
                package_payload["package_sha256"],
                json.dumps(build_product_snapshot_export(publication)),
                body.actor,
                json.dumps({"authority": "NC-COMMERCE-002", "api_generated": True}),
            )
            package = _decode(package_row)
            package_id = package["id"]
            event_type = "manual_package_generated"
            event_payload["package_sha256"] = package["package_sha256"]
        elif action == "activate":
            await conn.execute(
                "UPDATE product_manual_export_package "
                "SET package_status = 'activated', updated_at = NOW() "
                "WHERE id = $1",
                package_id,
            )
            event_type = "manual_package_activated"
        elif action == "pause":
            await conn.execute(
                "UPDATE product_manual_export_package "
                "SET package_status = 'paused', updated_at = NOW() "
                "WHERE id = $1",
                package_id,
            )
            event_type = "manual_package_paused"
        elif action == "retract":
            if package_id:
                await conn.execute(
                    "UPDATE product_manual_export_package "
                    "SET package_status = 'retracted', updated_at = NOW() "
                    "WHERE id = $1",
                    package_id,
                )
            event_type = "manual_package_retracted"

        row = await conn.fetchrow(
            f"""
            UPDATE product_publication
               SET activation_state = $2, updated_at = NOW()
             WHERE id = $1
            RETURNING {_PUBLICATION_COLS}
            """,
            publication_id,
            new_state,
        )
        updated = _decode(row)
        audit = build_audit_event(
            entity_type="product_publication",
            entity_id=str(publication_id),
            event_type=event_type,
            actor=body.actor,
            previous_state={"activation_state": previous_state},
            new_state={"activation_state": new_state},
            event=event_payload,
        )
        await _write_audit(conn, audit, package_id)

    updated["package"] = package
    updated["allowed_next_actions"] = activation_actions(updated["activation_state"])
    return updated


@router.get("/first-sale-activations")
async def list_first_sale_activations(
    auth: Auth, conn: DB, product_code: str | None = Query(None)
) -> list[dict]:
    if product_code:
        rows = await conn.fetch(
            f"SELECT {_FIRST_SALE_COLS} FROM product_first_sale_activation "
            "WHERE product_code = $1 ORDER BY activated_at DESC",
            product_code,
        )
    else:
        rows = await conn.fetch(
            f"SELECT {_FIRST_SALE_COLS} FROM product_first_sale_activation "
            "ORDER BY activated_at DESC"
        )
    return [_decode(row) for row in rows]


@router.get("/health")
async def get_product_runtime_health(auth: Auth, conn: DB) -> dict:
    line_count = await conn.fetchval("SELECT COUNT(*) FROM product_line")
    candidate_count = await conn.fetchval("SELECT COUNT(*) FROM product_candidate")
    publication_count = await conn.fetchval("SELECT COUNT(*) FROM product_publication")
    blocked_count = await conn.fetchval(
        "SELECT COUNT(*) FROM product_candidate WHERE gate_result->>'passed' <> 'true'"
    )
    return {
        "runtime": "NC-PRODUCT-001 Sprint 1",
        "provider": "manual",
        "status": "healthy" if not blocked_count else "degraded",
        "product_lines": line_count or 0,
        "product_candidates": candidate_count or 0,
        "product_publications": publication_count or 0,
        "blocked_candidates": blocked_count or 0,
    }
