from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..dependencies import DB, Auth

router = APIRouter(prefix="/discovery/candidates", tags=["discovery"])

_VALID_TRANSITIONS = {
    "pending": {"approve", "reject", "flag"},
    "flagged": {"approve", "reject"},
}

_COLS = """
    id, source, source_id, wikidata_qid, unesco_ref_id,
    name, description, statement_of_ouv, justification,
    country_codes, heritage_type, ouv_criteria, transboundary,
    inscription_year, core_area_ha, buffer_area_ha, spatial_precision,
    confidence_score,
    status, discovered_at, reviewed_by, reviewed_at, rejection_reason,
    promoted_place_id
"""


class CandidateAction(BaseModel):
    action: str        # approve | reject | flag
    reviewer: str      # human identity — required for audit trail
    reason: str | None = None


@router.get("")
async def list_candidates(
    auth: Auth,
    conn: DB,
    status: str | None = Query(None),
    source: str | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    filters, args = [], []

    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")
    if source:
        args.append(source)
        filters.append(f"source = ${len(args)}")

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]

    rows = await conn.fetch(
        f"SELECT {_COLS} FROM discovery_candidates {where}"
        f" ORDER BY confidence_score DESC NULLS LAST"
        f" LIMIT ${len(args)-1} OFFSET ${len(args)}",
        *args,
    )
    return [dict(r) for r in rows]


@router.get("/{candidate_id}")
async def get_candidate(candidate_id: UUID, auth: Auth, conn: DB) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_COLS} FROM discovery_candidates WHERE id = $1", candidate_id
    )
    if not row:
        raise HTTPException(404, "Candidate not found")
    return dict(row)


@router.patch("/{candidate_id}")
async def act_on_candidate(
    candidate_id: UUID,
    body: CandidateAction,
    auth: Auth,
    conn: DB,
) -> dict:
    if not body.reviewer.strip():
        raise HTTPException(422, "reviewer is required")

    row = await conn.fetchrow(
        "SELECT status FROM discovery_candidates WHERE id = $1", candidate_id
    )
    if not row:
        raise HTTPException(404, "Candidate not found")

    allowed = _VALID_TRANSITIONS.get(row["status"], set())
    if body.action not in allowed:
        raise HTTPException(
            422,
            f"Cannot '{body.action}' a candidate with status '{row['status']}'. "
            f"Allowed actions: {sorted(allowed) or 'none'}",
        )

    new_status = {"approve": "approved", "reject": "rejected", "flag": "flagged"}[body.action]

    await conn.execute(
        """UPDATE discovery_candidates SET
               status          = $1,
               reviewed_by     = $2,
               reviewed_at     = NOW(),
               rejection_reason = $3,
               updated_at      = NOW()
           WHERE id = $4""",
        new_status, body.reviewer, body.reason, candidate_id,
    )
    return {"id": str(candidate_id), "status": new_status, "reviewed_by": body.reviewer}
