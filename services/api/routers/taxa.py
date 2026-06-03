"""Taxon discovery API: ranked taxa and BHL search targets."""

import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..dependencies import DB, Auth

router = APIRouter(prefix="/taxa", tags=["taxa"])

_CANDIDATE_COLS = """
    id, run_id, place_id, concept_id, scientific_name, canonical_name, taxon_rank,
    gbif_taxon_key, wikidata_qid, common_names, status,
    place_relevance_score, source_agreement_score, illustration_likelihood_score,
    public_domain_path_score, commercial_value_score, searchability_score, total_score,
    score_components, provenance, agent_notes, created_at, updated_at
"""

_EVIDENCE_COLS = """
    id, candidate_id, source, evidence_type, source_record_id, source_url,
    payload, provenance, created_at
"""

_TARGET_COLS = """
    id, candidate_id, sequence, query, target_type, status, provenance, created_at
"""

_JSON_DECODE = {"score_components", "provenance", "agent_notes", "payload"}
_TRANSITIONS = {
    "approve": ("approved", {"candidate"}),
    "reject": ("rejected", {"candidate"}),
    "dispute": ("disputed", {"candidate", "approved"}),
    "retract": ("retracted", {"disputed"}),
}


class TaxonCandidateAction(BaseModel):
    action: str
    reviewer: str
    reason: str | None = None


def _decode(row) -> dict:
    item = dict(row)
    for field in _JSON_DECODE:
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item


async def _candidate_detail(conn: DB, candidate_id: UUID) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_CANDIDATE_COLS} FROM taxon_candidates WHERE id = $1",
        candidate_id,
    )
    if not row:
        raise HTTPException(404, "Taxon candidate not found")
    result = _decode(row)
    evidence = await conn.fetch(
        f"SELECT {_EVIDENCE_COLS} FROM taxon_candidate_evidence WHERE candidate_id = $1 "
        "ORDER BY source, evidence_type, created_at",
        candidate_id,
    )
    targets = await conn.fetch(
        f"SELECT {_TARGET_COLS} FROM bhl_search_targets WHERE candidate_id = $1 "
        "ORDER BY sequence",
        candidate_id,
    )
    result["evidence"] = [_decode(item) for item in evidence]
    result["bhl_search_targets"] = [_decode(item) for item in targets]
    return result


@router.get("/candidates")
async def list_taxon_candidates(
    auth: Auth,
    conn: DB,
    place_id: UUID | None = Query(None),
    status: str | None = Query(None),
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
    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]
    rows = await conn.fetch(
        f"SELECT {_CANDIDATE_COLS} FROM taxon_candidates {where} "
        f"ORDER BY total_score DESC, scientific_name LIMIT ${len(args) - 1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode(row) for row in rows]


@router.get("/candidates/{candidate_id}")
async def get_taxon_candidate(candidate_id: UUID, auth: Auth, conn: DB) -> dict:
    return await _candidate_detail(conn, candidate_id)


@router.get("/places/{place_id}/bhl-search-targets")
async def list_place_bhl_search_targets(
    place_id: UUID,
    auth: Auth,
    conn: DB,
    limit: int = Query(100, ge=1, le=500),
) -> list[dict]:
    rows = await conn.fetch(
        """
        SELECT c.id AS candidate_id, c.scientific_name, c.total_score,
               t.sequence, t.query, t.target_type, t.status, t.provenance
        FROM taxon_candidates c
        JOIN bhl_search_targets t ON t.candidate_id = c.id
        WHERE c.place_id = $1 AND c.status IN ('candidate','approved')
        ORDER BY c.total_score DESC, c.scientific_name, t.sequence
        LIMIT $2
        """,
        place_id,
        limit,
    )
    return [_decode(row) for row in rows]


@router.patch("/candidates/{candidate_id}")
async def act_on_taxon_candidate(
    candidate_id: UUID,
    body: TaxonCandidateAction,
    auth: Auth,
    conn: DB,
) -> dict:
    if not body.reviewer.strip():
        raise HTTPException(422, "reviewer is required")
    if body.action not in _TRANSITIONS:
        raise HTTPException(422, f"action must be one of: {sorted(_TRANSITIONS)}")
    if body.action in {"reject", "dispute", "retract"} and not body.reason:
        raise HTTPException(422, f"reason is required for {body.action}")

    new_status, allowed_from = _TRANSITIONS[body.action]
    audit = {"action": body.action, "reviewer": body.reviewer, "reason": body.reason}
    async with conn.transaction():
        row = await conn.fetchrow(
            "SELECT status FROM taxon_candidates WHERE id = $1 FOR UPDATE",
            candidate_id,
        )
        if not row:
            raise HTTPException(404, "Taxon candidate not found")
        if row["status"] not in allowed_from:
            raise HTTPException(
                422,
                f"Cannot '{body.action}' a taxon candidate with status '{row['status']}'. "
                f"Allowed from: {sorted(allowed_from)}",
            )
        await conn.execute(
            """
            UPDATE taxon_candidates
            SET status = $1,
                agent_notes = agent_notes || $2::jsonb,
                updated_at = NOW()
            WHERE id = $3
            """,
            new_status,
            json.dumps({"governance": audit}),
            candidate_id,
        )
    return {"id": str(candidate_id), "status": new_status, "reviewed_by": body.reviewer}
