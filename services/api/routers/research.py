"""Research API: governed human-readable outputs backed by evidence."""

import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..dependencies import DB, Auth

router = APIRouter(prefix="/research", tags=["research"])

_OUTPUT_COLS = """
    id, place_id, output_type, output_version, title, summary, status,
    confidence_score, reviewed_by, reviewed_at, published_at,
    provenance, agent_notes, created_at, updated_at
"""

_STATEMENT_COLS = """
    id, output_id, place_id, sequence, statement_type, body, status,
    confidence_score, provenance, agent_notes, created_at, updated_at
"""

_EVIDENCE_COLS = """
    e.id, e.statement_id, e.asset_id, e.fact_id, e.relationship_id, e.evidence_role,
    e.provenance, e.created_at,
    a.raw_path AS asset_raw_path,
    a.normalized_path AS asset_normalized_path,
    a.checksum_sha256 AS asset_checksum_sha256,
    f.predicate AS fact_predicate,
    f.value AS fact_value,
    r.predicate AS relationship_predicate
"""

_JSON_DECODE = {"provenance", "agent_notes", "fact_value"}

_OUTPUT_TRANSITIONS = {
    "approve": ("approved", {"pending_review"}),
    "publish": ("published", {"approved"}),
    "reject": ("rejected", {"pending_review"}),
    "dispute": ("disputed", {"approved", "published"}),
    "retract": ("retracted", {"disputed"}),
}

_STATEMENT_STATUS_FOR_OUTPUT = {
    "approved": "approved",
    "published": "published",
    "rejected": "rejected",
    "disputed": "disputed",
    "retracted": "retracted",
}


class ResearchOutputAction(BaseModel):
    action: str
    reviewer: str
    reason: str | None = None


def _decode(row) -> dict:
    item = dict(row)
    for field in _JSON_DECODE:
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item


async def _output_detail(conn: DB, output_id: UUID) -> dict:
    output = await conn.fetchrow(
        f"SELECT {_OUTPUT_COLS} FROM research_outputs WHERE id = $1",
        output_id,
    )
    if not output:
        raise HTTPException(404, "Research output not found")

    statements = [_decode(r) for r in await conn.fetch(
        f"SELECT {_STATEMENT_COLS} FROM research_statements WHERE output_id = $1 ORDER BY sequence",
        output_id,
    )]
    if statements:
        evidence_rows = [_decode(r) for r in await conn.fetch(
            f"SELECT {_EVIDENCE_COLS} FROM research_statement_evidence e "
            f"JOIN assets a ON a.id = e.asset_id "
            f"JOIN facts f ON f.id = e.fact_id "
            f"JOIN relationships r ON r.id = e.relationship_id "
            f"WHERE e.statement_id = ANY($1::uuid[]) ORDER BY e.created_at, e.id",
            [s["id"] for s in statements],
        )]
    else:
        evidence_rows = []

    evidence_by_statement: dict[UUID, list[dict]] = {}
    for evidence in evidence_rows:
        evidence_by_statement.setdefault(evidence["statement_id"], []).append(evidence)

    for statement in statements:
        statement["evidence"] = evidence_by_statement.get(statement["id"], [])

    result = _decode(output)
    result["statements"] = statements
    return result


@router.get("/outputs")
async def list_research_outputs(
    auth: Auth,
    conn: DB,
    place_id: UUID | None = Query(None),
    status: str | None = Query(None),
    output_type: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    filters, args = [], []
    if place_id:
        args.append(place_id)
        filters.append(f"place_id = ${len(args)}")
    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")
    if output_type:
        args.append(output_type)
        filters.append(f"output_type = ${len(args)}")
    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]
    rows = await conn.fetch(
        f"SELECT {_OUTPUT_COLS} FROM research_outputs {where} ORDER BY updated_at DESC "
        f"LIMIT ${len(args) - 1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode(r) for r in rows]


@router.get("/outputs/{output_id}")
async def get_research_output(output_id: UUID, auth: Auth, conn: DB) -> dict:
    return await _output_detail(conn, output_id)


@router.patch("/outputs/{output_id}")
async def act_on_research_output(
    output_id: UUID,
    body: ResearchOutputAction,
    auth: Auth,
    conn: DB,
) -> dict:
    if not body.reviewer.strip():
        raise HTTPException(422, "reviewer is required")
    if body.action not in _OUTPUT_TRANSITIONS:
        raise HTTPException(422, f"action must be one of: {sorted(_OUTPUT_TRANSITIONS)}")
    if body.action in {"reject", "dispute", "retract"} and not body.reason:
        raise HTTPException(422, f"reason is required for {body.action}")

    new_status, allowed_from = _OUTPUT_TRANSITIONS[body.action]
    audit = {"action": body.action, "reviewer": body.reviewer, "reason": body.reason}
    statement_status = _STATEMENT_STATUS_FOR_OUTPUT[new_status]
    async with conn.transaction():
        row = await conn.fetchrow(
            "SELECT status FROM research_outputs WHERE id = $1 FOR UPDATE",
            output_id,
        )
        if not row:
            raise HTTPException(404, "Research output not found")
        if row["status"] not in allowed_from:
            raise HTTPException(
                422,
                f"Cannot '{body.action}' a research output with status '{row['status']}'. "
                f"Allowed from: {sorted(allowed_from)}",
            )

        await conn.execute(
            """
            UPDATE research_outputs
            SET status = $1,
                reviewed_by = $2,
                reviewed_at = NOW(),
                published_at = CASE WHEN $1 = 'published' THEN NOW() ELSE published_at END,
                agent_notes = agent_notes || $3::jsonb,
                updated_at = NOW()
            WHERE id = $4
            """,
            new_status,
            body.reviewer,
            json.dumps({"governance": audit}),
            output_id,
        )
        await conn.execute(
            """
            UPDATE research_statements
            SET status = $1,
                agent_notes = agent_notes || $2::jsonb,
                updated_at = NOW()
            WHERE output_id = $3
            """,
            statement_status,
            json.dumps({"governance": audit}),
            output_id,
        )

    return {"id": str(output_id), "status": new_status, "reviewed_by": body.reviewer}
