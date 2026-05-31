"""Knowledge API: concepts, facts, relationships.

Every fact is traceable to its source evidence via provenance.source_field.
Governance endpoints (PATCH /facts/{id}, PATCH /relationships/{id}) require a
reviewer and follow the same state-machine pattern as /discovery/candidates.
"""
import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..dependencies import DB, Auth

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

_CONCEPT_COLS = """
    id, uri, label, description, type, status,
    broader_id, provenance, created_at, updated_at
"""

_FACT_COLS = """
    id, place_id, predicate, value, value_type, language,
    concept_id, asset_id, source, confidence_score,
    status, provenance, agent_notes, created_at, updated_at
"""

_REL_COLS = """
    id, subject_id, subject_type, predicate, object_id, object_type,
    confidence_score, status, asset_id, provenance, agent_notes,
    created_at, updated_at
"""

_FACT_TRANSITIONS = {
    "dispute": ("disputed", {"active"}),
    "retract": ("retracted", {"disputed"}),
}

_REL_TRANSITIONS = {
    "activate": ("active",    {"proposed"}),
    "dispute":  ("disputed",  {"active", "proposed"}),
    "retract":  ("retracted", {"disputed"}),
}

_JSON_DECODE = {"label", "description", "value", "provenance", "agent_notes"}

_VALID_CONCEPT_TYPES = {
    "criterion", "heritage_type", "ecosystem", "biome",
    "geographic", "thematic", "actor",
}


def _decode(row) -> dict:
    item = dict(row)
    for f in _JSON_DECODE:
        if isinstance(item.get(f), str):
            item[f] = json.loads(item[f])
    return item


# ---------------------------------------------------------------------------
# Concepts
# ---------------------------------------------------------------------------

class ConceptCreate(BaseModel):
    uri: str
    label: dict
    description: dict = {}
    type: str
    broader_id: UUID | None = None


@router.get("/concepts")
async def list_concepts(
    auth: Auth,
    conn: DB,
    type: str | None = Query(None),
    status: str | None = Query(None),
    q: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    filters, args = [], []
    if type:
        args.append(type)
        filters.append(f"type = ${len(args)}")
    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")
    if q:
        args.append(f"%{q}%")
        n = len(args)
        filters.append(f"(uri ILIKE ${n} OR label::text ILIKE ${n})")

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]
    rows = await conn.fetch(
        f"SELECT {_CONCEPT_COLS} FROM concepts {where}"
        f" ORDER BY type, uri"
        f" LIMIT ${len(args) - 1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode(r) for r in rows]


@router.get("/concepts/{concept_id}")
async def get_concept(concept_id: UUID, auth: Auth, conn: DB) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_CONCEPT_COLS} FROM concepts WHERE id = $1", concept_id
    )
    if not row:
        raise HTTPException(404, "Concept not found")
    concept = _decode(row)
    aliases = await conn.fetch(
        """SELECT id, alias, language, source, confidence_score
           FROM concept_aliases WHERE concept_id = $1 ORDER BY language, alias""",
        concept_id,
    )
    concept["aliases"] = [dict(a) for a in aliases]
    return concept


@router.post("/concepts", status_code=201)
async def create_concept(body: ConceptCreate, auth: Auth, conn: DB) -> dict:
    if body.type not in _VALID_CONCEPT_TYPES:
        raise HTTPException(422, f"type must be one of: {sorted(_VALID_CONCEPT_TYPES)}")
    if not body.label.get("en"):
        raise HTTPException(422, "label.en is required")

    row = await conn.fetchrow(
        """INSERT INTO concepts (uri, label, description, type, broader_id)
           VALUES ($1, $2::jsonb, $3::jsonb, $4, $5)
           RETURNING id""",
        body.uri,
        json.dumps(body.label),
        json.dumps(body.description),
        body.type,
        body.broader_id,
    )
    return {"id": str(row["id"]), "uri": body.uri, "type": body.type}


# ---------------------------------------------------------------------------
# Facts
# ---------------------------------------------------------------------------

class FactAction(BaseModel):
    action: str       # dispute | retract
    reviewer: str
    reason: str | None = None


@router.get("/facts")
async def list_facts(
    auth: Auth,
    conn: DB,
    place_id: UUID | None = Query(None),
    predicate: str | None = Query(None),
    status: str | None = Query(None),
    concept_id: UUID | None = Query(None),
    source: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    filters, args = [], []
    if place_id:
        args.append(place_id)
        filters.append(f"place_id = ${len(args)}")
    if predicate:
        args.append(predicate)
        filters.append(f"predicate = ${len(args)}")
    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")
    if concept_id:
        args.append(concept_id)
        filters.append(f"concept_id = ${len(args)}")
    if source:
        args.append(source)
        filters.append(f"source = ${len(args)}")

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]
    rows = await conn.fetch(
        f"SELECT {_FACT_COLS} FROM facts {where}"
        f" ORDER BY predicate, language, created_at DESC"
        f" LIMIT ${len(args) - 1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode(r) for r in rows]


@router.get("/facts/{fact_id}")
async def get_fact(fact_id: UUID, auth: Auth, conn: DB) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_FACT_COLS} FROM facts WHERE id = $1", fact_id
    )
    if not row:
        raise HTTPException(404, "Fact not found")
    return _decode(row)


@router.patch("/facts/{fact_id}")
async def act_on_fact(fact_id: UUID, body: FactAction, auth: Auth, conn: DB) -> dict:
    if not body.reviewer.strip():
        raise HTTPException(422, "reviewer is required")
    if body.action not in _FACT_TRANSITIONS:
        raise HTTPException(422, f"action must be one of: {sorted(_FACT_TRANSITIONS)}")
    if body.action == "retract" and not body.reason:
        raise HTTPException(422, "reason is required for retract")

    row = await conn.fetchrow("SELECT status FROM facts WHERE id = $1", fact_id)
    if not row:
        raise HTTPException(404, "Fact not found")

    new_status, allowed_from = _FACT_TRANSITIONS[body.action]
    if row["status"] not in allowed_from:
        raise HTTPException(
            422,
            f"Cannot '{body.action}' a fact with status '{row['status']}'. "
            f"Allowed from: {sorted(allowed_from)}",
        )

    audit = {"action": body.action, "reviewer": body.reviewer, "reason": body.reason}
    await conn.execute(
        """UPDATE facts
           SET status = $1,
               agent_notes = agent_notes || $2::jsonb,
               updated_at = NOW()
           WHERE id = $3""",
        new_status,
        json.dumps({"governance": audit}),
        fact_id,
    )
    return {"id": str(fact_id), "status": new_status, "reviewed_by": body.reviewer}


# ---------------------------------------------------------------------------
# Relationships
# ---------------------------------------------------------------------------

class RelationshipAction(BaseModel):
    action: str       # activate | dispute | retract
    reviewer: str
    reason: str | None = None


@router.get("/relationships")
async def list_relationships(
    auth: Auth,
    conn: DB,
    subject_id: UUID | None = Query(None),
    object_id: UUID | None = Query(None),
    predicate: str | None = Query(None),
    subject_type: str | None = Query(None),
    object_type: str | None = Query(None),
    status: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    filters, args = [], []
    if subject_id:
        args.append(subject_id)
        filters.append(f"subject_id = ${len(args)}")
    if object_id:
        args.append(object_id)
        filters.append(f"object_id = ${len(args)}")
    if predicate:
        args.append(predicate)
        filters.append(f"predicate = ${len(args)}")
    if subject_type:
        args.append(subject_type)
        filters.append(f"subject_type = ${len(args)}")
    if object_type:
        args.append(object_type)
        filters.append(f"object_type = ${len(args)}")
    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    args += [limit, offset]
    rows = await conn.fetch(
        f"SELECT {_REL_COLS} FROM relationships {where}"
        f" ORDER BY predicate, created_at DESC"
        f" LIMIT ${len(args) - 1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode(r) for r in rows]


@router.get("/relationships/{rel_id}")
async def get_relationship(rel_id: UUID, auth: Auth, conn: DB) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_REL_COLS} FROM relationships WHERE id = $1", rel_id
    )
    if not row:
        raise HTTPException(404, "Relationship not found")
    return _decode(row)


@router.patch("/relationships/{rel_id}")
async def act_on_relationship(
    rel_id: UUID, body: RelationshipAction, auth: Auth, conn: DB
) -> dict:
    if not body.reviewer.strip():
        raise HTTPException(422, "reviewer is required")
    if body.action not in _REL_TRANSITIONS:
        raise HTTPException(422, f"action must be one of: {sorted(_REL_TRANSITIONS)}")
    if body.action == "retract" and not body.reason:
        raise HTTPException(422, "reason is required for retract")

    row = await conn.fetchrow("SELECT status FROM relationships WHERE id = $1", rel_id)
    if not row:
        raise HTTPException(404, "Relationship not found")

    new_status, allowed_from = _REL_TRANSITIONS[body.action]
    if row["status"] not in allowed_from:
        raise HTTPException(
            422,
            f"Cannot '{body.action}' a relationship with status '{row['status']}'. "
            f"Allowed from: {sorted(allowed_from)}",
        )

    audit = {"action": body.action, "reviewer": body.reviewer, "reason": body.reason}
    await conn.execute(
        """UPDATE relationships
           SET status = $1,
               agent_notes = agent_notes || $2::jsonb,
               updated_at = NOW()
           WHERE id = $3""",
        new_status,
        json.dumps({"governance": audit}),
        rel_id,
    )
    return {"id": str(rel_id), "status": new_status, "reviewed_by": body.reviewer}


# ---------------------------------------------------------------------------
# Place knowledge aggregate
# ---------------------------------------------------------------------------

@router.get("/places/{place_id}/knowledge")
async def get_place_knowledge(place_id: UUID, auth: Auth, conn: DB) -> dict:
    """All active facts and relationships for a place in one call.

    Relationships are returned for both subject and object sides so that
    co_inscribed_with edges (where this place may be the object) are included.
    """
    facts = await conn.fetch(
        f"SELECT {_FACT_COLS} FROM facts"
        f" WHERE place_id = $1 AND status = 'active'"
        f" ORDER BY predicate, language",
        place_id,
    )
    rels = await conn.fetch(
        f"SELECT {_REL_COLS} FROM relationships"
        f" WHERE status = 'active'"
        f"   AND ("
        f"       (subject_id = $1 AND subject_type = 'place')"
        f"    OR (object_id  = $1 AND object_type  = 'place')"
        f"   )"
        f" ORDER BY predicate",
        place_id,
    )
    return {
        "place_id": str(place_id),
        "facts": [_decode(r) for r in facts],
        "relationships": [_decode(r) for r in rels],
    }
