"""MILESTONE-2.6 Knowledge Hardening tests.

Verifies all blockers identified in the MILESTONE-2.5 scale review:
  B1 — GIN index dropped, redundant indexes dropped, fillfactor set
  B2 — build_co_inscribed_relationships bounded to batch place_ids
  B3 — PATCH /relationships/{id} governance endpoint
  B4 — process_places wrapped in a transaction

Also covers H1–H5 (HIGH) fixes:
  H1 — knowledge_score computed in release_places
  H2 — stale facts trigger resets last_knowledge_extracted_at
  H3 — relationship governance error handling
  H4 — co_inscribed_with retraction trigger on inscription_year supersede
  H5 — draft status removed from facts lifecycle
"""
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from services.api.routers import knowledge

MIGRATION_09 = Path("infrastructure/postgres/init/09_knowledge_facts.sql")
MIGRATION_14 = Path("infrastructure/postgres/init/14_knowledge_hardening.sql")
MIGRATION_08 = Path("infrastructure/postgres/init/08_knowledge_concepts.sql")

_REL_ID = uuid4()
_PLACE_ID = uuid4()
_CONCEPT_ID = uuid4()


# ---------------------------------------------------------------------------
# B1 — Schema: dropped indexes and fillfactor
# ---------------------------------------------------------------------------

def test_migration_14_exists() -> None:
    assert MIGRATION_14.exists(), "Migration 14 not found"


def test_migration_14_drops_gin_provenance_index() -> None:
    sql = MIGRATION_14.read_text()
    assert "DROP INDEX IF EXISTS idx_facts_provenance" in sql


def test_migration_14_drops_place_pred_index() -> None:
    sql = MIGRATION_14.read_text()
    assert "DROP INDEX IF EXISTS idx_facts_place_pred" in sql


def test_migration_14_drops_redundant_rel_indexes() -> None:
    sql = MIGRATION_14.read_text()
    assert "DROP INDEX IF EXISTS idx_rel_subject" in sql
    assert "DROP INDEX IF EXISTS idx_rel_predicate" in sql
    assert "DROP INDEX IF EXISTS idx_rel_status" in sql


def test_migration_14_drops_superseded_queue_index() -> None:
    sql = MIGRATION_14.read_text()
    assert "DROP INDEX IF EXISTS idx_places_knowledge_queue" in sql


def test_migration_14_sets_fillfactor_on_facts() -> None:
    sql = MIGRATION_14.read_text()
    assert "facts" in sql and "fillfactor = 70" in sql


def test_migration_14_sets_fillfactor_on_relationships() -> None:
    sql = MIGRATION_14.read_text()
    assert "relationships" in sql and "fillfactor = 70" in sql


def test_migration_09_no_gin_provenance_index() -> None:
    sql = MIGRATION_09.read_text()
    assert "idx_facts_provenance" not in sql


def test_migration_09_no_place_pred_index() -> None:
    sql = MIGRATION_09.read_text()
    assert "idx_facts_place_pred" not in sql


# ---------------------------------------------------------------------------
# H5 — Draft status removed from facts lifecycle
# ---------------------------------------------------------------------------

def test_migration_09_default_status_is_active() -> None:
    sql = MIGRATION_09.read_text()
    assert "DEFAULT 'active'" in sql
    assert "DEFAULT 'draft'" not in sql


def test_migration_09_no_draft_in_check_constraint() -> None:
    sql = MIGRATION_09.read_text()
    assert "'draft'" not in sql


def test_migration_14_removes_draft_from_constraint() -> None:
    sql = MIGRATION_14.read_text()
    assert "chk_fact_status" in sql
    # The ADD CONSTRAINT block must not include 'draft' as a valid status value
    constraint_block = sql[sql.index("ADD CONSTRAINT chk_fact_status"):]
    constraint_block = constraint_block[: constraint_block.index(";")]
    assert "'draft'" not in constraint_block


def test_fact_dispute_transition_only_from_active() -> None:
    _, allowed_from = knowledge._FACT_TRANSITIONS["dispute"]
    assert allowed_from == {"active"}
    assert "draft" not in allowed_from


def test_fact_retract_transition_only_from_disputed() -> None:
    _, allowed_from = knowledge._FACT_TRANSITIONS["retract"]
    assert allowed_from == {"disputed"}


def test_fact_transitions_does_not_include_draft_action() -> None:
    assert "draft" not in knowledge._FACT_TRANSITIONS


# ---------------------------------------------------------------------------
# H2 — Stale facts trigger forces re-queue
# ---------------------------------------------------------------------------

def test_migration_09_stale_trigger_resets_last_extracted_at() -> None:
    sql = MIGRATION_09.read_text()
    assert "last_knowledge_extracted_at = NULL" in sql
    assert "knowledge_extracting = FALSE" in sql


def test_migration_14_stale_trigger_resets_last_extracted_at() -> None:
    sql = MIGRATION_14.read_text()
    assert "last_knowledge_extracted_at = NULL" in sql
    assert "knowledge_extracting = FALSE" in sql


# ---------------------------------------------------------------------------
# H4 — Co-inscribed retraction trigger
# ---------------------------------------------------------------------------

def test_migration_09_has_retract_co_inscribed_trigger() -> None:
    sql = MIGRATION_09.read_text()
    assert "retract_stale_co_inscribed" in sql
    assert "trg_facts_retract_co_inscribed" in sql
    assert "inscription_year_superseded" in sql


def test_migration_14_has_retract_co_inscribed_trigger() -> None:
    sql = MIGRATION_14.read_text()
    assert "retract_stale_co_inscribed" in sql
    assert "trg_facts_retract_co_inscribed" in sql


def test_retract_co_inscribed_trigger_fires_on_supersede() -> None:
    sql = MIGRATION_14.read_text()
    assert "OLD.status = 'active'" in sql
    assert "NEW.status = 'superseded'" in sql
    assert "co_inscribed_with" in sql


# ---------------------------------------------------------------------------
# M2 — concept_aliases updated_at
# ---------------------------------------------------------------------------

def test_migration_08_concept_aliases_has_updated_at() -> None:
    sql = MIGRATION_08.read_text()
    assert "updated_at" in sql
    assert "trg_concept_aliases_updated_at" in sql


def test_migration_14_adds_updated_at_to_concept_aliases() -> None:
    sql = MIGRATION_14.read_text()
    assert "concept_aliases" in sql
    assert "updated_at" in sql


# ---------------------------------------------------------------------------
# B2 — build_co_inscribed_relationships is bounded to place_ids
# ---------------------------------------------------------------------------

def test_build_co_inscribed_takes_place_ids_parameter() -> None:
    import inspect

    from workers.knowledge_worker.store import build_co_inscribed_relationships
    sig = inspect.signature(build_co_inscribed_relationships)
    assert "place_ids" in sig.parameters


async def test_build_co_inscribed_returns_zero_for_empty_batch() -> None:
    from workers.knowledge_worker.store import build_co_inscribed_relationships

    class FakeConn:
        async def execute(self, *a, **kw):
            raise AssertionError("execute should not be called for empty batch")

    result = await build_co_inscribed_relationships(FakeConn(), [])
    assert result == 0


def test_store_imports_worker_id_constant() -> None:
    from workers.knowledge_worker import store
    assert hasattr(store, "_WORKER_ID")


# ---------------------------------------------------------------------------
# B3 — PATCH /relationships/{id} governance endpoint
# ---------------------------------------------------------------------------

class FakeRelConn:
    def __init__(self, current_status: str = "proposed") -> None:
        self.current_status = current_status
        self.executed_query = ""
        self.executed_args: tuple = ()

    async def fetchrow(self, query: str, *args):
        return {"status": self.current_status}

    async def execute(self, query: str, *args):
        self.executed_query = query
        self.executed_args = args
        return "UPDATE 1"


class FakeRelConnNotFound:
    async def fetchrow(self, query: str, *args):
        return None

    async def execute(self, query: str, *args):
        return "UPDATE 0"


async def test_act_on_relationship_activate_from_proposed() -> None:
    conn = FakeRelConn(current_status="proposed")
    result = await knowledge.act_on_relationship(
        rel_id=UUID(str(_REL_ID)),
        body=knowledge.RelationshipAction(action="activate", reviewer="curator"),
        auth="dev-secret",
        conn=conn,
    )
    assert result["status"] == "active"
    assert result["reviewed_by"] == "curator"


async def test_act_on_relationship_dispute_from_active() -> None:
    conn = FakeRelConn(current_status="active")
    result = await knowledge.act_on_relationship(
        rel_id=UUID(str(_REL_ID)),
        body=knowledge.RelationshipAction(
            action="dispute", reviewer="auditor", reason="Incorrect pairing"
        ),
        auth="dev-secret",
        conn=conn,
    )
    assert result["status"] == "disputed"
    assert result["reviewed_by"] == "auditor"


async def test_act_on_relationship_dispute_from_proposed() -> None:
    conn = FakeRelConn(current_status="proposed")
    result = await knowledge.act_on_relationship(
        rel_id=UUID(str(_REL_ID)),
        body=knowledge.RelationshipAction(action="dispute", reviewer="auditor"),
        auth="dev-secret",
        conn=conn,
    )
    assert result["status"] == "disputed"


async def test_act_on_relationship_retract_from_disputed() -> None:
    conn = FakeRelConn(current_status="disputed")
    result = await knowledge.act_on_relationship(
        rel_id=UUID(str(_REL_ID)),
        body=knowledge.RelationshipAction(
            action="retract", reviewer="auditor", reason="Confirmed incorrect"
        ),
        auth="dev-secret",
        conn=conn,
    )
    assert result["status"] == "retracted"
    assert result["reviewed_by"] == "auditor"


async def test_act_on_relationship_retract_requires_reason() -> None:
    from fastapi import HTTPException
    conn = FakeRelConn(current_status="disputed")
    with pytest.raises(HTTPException) as exc_info:
        await knowledge.act_on_relationship(
            rel_id=UUID(str(_REL_ID)),
            body=knowledge.RelationshipAction(action="retract", reviewer="auditor", reason=None),
            auth="dev-secret",
            conn=conn,
        )
    assert exc_info.value.status_code == 422


async def test_act_on_relationship_requires_reviewer() -> None:
    from fastapi import HTTPException
    conn = FakeRelConn(current_status="proposed")
    with pytest.raises(HTTPException) as exc_info:
        await knowledge.act_on_relationship(
            rel_id=UUID(str(_REL_ID)),
            body=knowledge.RelationshipAction(action="activate", reviewer="  "),
            auth="dev-secret",
            conn=conn,
        )
    assert exc_info.value.status_code == 422


async def test_act_on_relationship_invalid_action_rejected() -> None:
    from fastapi import HTTPException
    conn = FakeRelConn(current_status="active")
    with pytest.raises(HTTPException) as exc_info:
        await knowledge.act_on_relationship(
            rel_id=UUID(str(_REL_ID)),
            body=knowledge.RelationshipAction(action="delete", reviewer="auditor"),
            auth="dev-secret",
            conn=conn,
        )
    assert exc_info.value.status_code == 422


async def test_act_on_relationship_wrong_status_rejected() -> None:
    from fastapi import HTTPException
    conn = FakeRelConn(current_status="retracted")
    with pytest.raises(HTTPException) as exc_info:
        await knowledge.act_on_relationship(
            rel_id=UUID(str(_REL_ID)),
            body=knowledge.RelationshipAction(action="activate", reviewer="curator"),
            auth="dev-secret",
            conn=conn,
        )
    assert exc_info.value.status_code == 422


async def test_act_on_relationship_not_found_returns_404() -> None:
    from fastapi import HTTPException
    conn = FakeRelConnNotFound()
    with pytest.raises(HTTPException) as exc_info:
        await knowledge.act_on_relationship(
            rel_id=UUID(str(_REL_ID)),
            body=knowledge.RelationshipAction(action="activate", reviewer="curator"),
            auth="dev-secret",
            conn=conn,
        )
    assert exc_info.value.status_code == 404


async def test_act_on_relationship_writes_governance_audit_trail() -> None:
    conn = FakeRelConn(current_status="proposed")
    await knowledge.act_on_relationship(
        rel_id=UUID(str(_REL_ID)),
        body=knowledge.RelationshipAction(
            action="activate", reviewer="curator", reason="Verified correct"
        ),
        auth="dev-secret",
        conn=conn,
    )
    assert "agent_notes" in conn.executed_query
    audit = json.loads(conn.executed_args[1])
    assert audit["governance"]["action"] == "activate"
    assert audit["governance"]["reviewer"] == "curator"


async def test_activate_not_allowed_from_active() -> None:
    from fastapi import HTTPException
    conn = FakeRelConn(current_status="active")
    with pytest.raises(HTTPException) as exc_info:
        await knowledge.act_on_relationship(
            rel_id=UUID(str(_REL_ID)),
            body=knowledge.RelationshipAction(action="activate", reviewer="curator"),
            auth="dev-secret",
            conn=conn,
        )
    assert exc_info.value.status_code == 422


# ---------------------------------------------------------------------------
# GET /relationships/{rel_id}
# ---------------------------------------------------------------------------

class FakeGetRelConn:
    async def fetchrow(self, query: str, *args):
        return {
            "id": _REL_ID,
            "subject_id": _PLACE_ID,
            "subject_type": "place",
            "predicate": "co_inscribed_with",
            "object_id": uuid4(),
            "object_type": "place",
            "confidence_score": 0.85,
            "status": "active",
            "asset_id": None,
            "provenance": json.dumps({"prov:wasGeneratedBy": "knowledge_worker:v0.2.0"}),
            "agent_notes": json.dumps({}),
            "created_at": "2026-05-31T00:00:00Z",
            "updated_at": "2026-05-31T00:00:00Z",
        }


async def test_get_relationship_returns_decoded_provenance() -> None:
    rel = await knowledge.get_relationship(
        rel_id=UUID(str(_REL_ID)),
        auth="dev-secret",
        conn=FakeGetRelConn(),
    )
    assert rel["predicate"] == "co_inscribed_with"
    assert isinstance(rel["provenance"], dict)
    assert rel["provenance"]["prov:wasGeneratedBy"] == "knowledge_worker:v0.2.0"


async def test_get_relationship_not_found_returns_404() -> None:
    from fastapi import HTTPException

    class FakeNotFound:
        async def fetchrow(self, *a, **kw):
            return None

    with pytest.raises(HTTPException) as exc_info:
        await knowledge.get_relationship(
            rel_id=UUID(str(_REL_ID)),
            auth="dev-secret",
            conn=FakeNotFound(),
        )
    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# B3 — _REL_COLS includes agent_notes
# ---------------------------------------------------------------------------

def test_rel_cols_includes_agent_notes() -> None:
    assert "agent_notes" in knowledge._REL_COLS


# ---------------------------------------------------------------------------
# Object-side relationships in get_place_knowledge
# ---------------------------------------------------------------------------

class FakeKnowledgeConnQueryCapture:
    """Records both fetch queries to verify subject and object sides."""

    def __init__(self) -> None:
        self.queries: list[str] = []

    async def fetch(self, query: str, *args):
        self.queries.append(query)
        return []


async def test_get_place_knowledge_query_includes_object_id_condition() -> None:
    conn = FakeKnowledgeConnQueryCapture()
    await knowledge.get_place_knowledge(
        place_id=UUID(str(_PLACE_ID)),
        auth="dev-secret",
        conn=conn,
    )
    rel_query = next(q for q in conn.queries if "relationships" in q)
    assert "object_id" in rel_query, "get_place_knowledge must query object-side relationships"


async def test_get_place_knowledge_query_includes_subject_id_condition() -> None:
    conn = FakeKnowledgeConnQueryCapture()
    await knowledge.get_place_knowledge(
        place_id=UUID(str(_PLACE_ID)),
        auth="dev-secret",
        conn=conn,
    )
    rel_query = next(q for q in conn.queries if "relationships" in q)
    assert "subject_id" in rel_query


async def test_get_place_knowledge_includes_object_side_relationship() -> None:
    """A co_inscribed_with where this place is the object must appear in the result."""
    other_place_id = uuid4()

    class FakeObjectSideConn:
        async def fetch(self, query: str, *args):
            if "facts" in query:
                return []
            return [
                {
                    "id": uuid4(),
                    "subject_id": other_place_id,
                    "subject_type": "place",
                    "predicate": "co_inscribed_with",
                    "object_id": _PLACE_ID,
                    "object_type": "place",
                    "confidence_score": 0.85,
                    "status": "active",
                    "asset_id": None,
                    "provenance": json.dumps({}),
                    "agent_notes": json.dumps({}),
                    "created_at": "2026-05-31T00:00:00Z",
                    "updated_at": "2026-05-31T00:00:00Z",
                }
            ]

    result = await knowledge.get_place_knowledge(
        place_id=UUID(str(_PLACE_ID)),
        auth="dev-secret",
        conn=FakeObjectSideConn(),
    )
    assert len(result["relationships"]) == 1
    assert result["relationships"][0]["predicate"] == "co_inscribed_with"
    assert result["relationships"][0]["object_id"] == _PLACE_ID


# ---------------------------------------------------------------------------
# H1 — knowledge_score computed in release_places
# ---------------------------------------------------------------------------

class FakeReleaseConn:
    def __init__(self) -> None:
        self.executed: list[str] = []

    async def execute(self, query: str, *args):
        self.executed.append(query)
        return "UPDATE 1"


async def test_release_places_computes_knowledge_score() -> None:
    from workers.knowledge_worker.store import release_places

    conn = FakeReleaseConn()
    place_ids = [uuid4(), uuid4()]
    await release_places(conn, place_ids)

    assert conn.executed, "release_places must execute at least one statement"
    query = conn.executed[0]
    assert "knowledge_score" in query, (
        "release_places must compute knowledge_score as AVG(confidence_score)"
    )
    assert "AVG" in query.upper()


async def test_release_places_skips_empty_batch() -> None:
    from workers.knowledge_worker.store import release_places

    conn = FakeReleaseConn()
    await release_places(conn, [])
    assert not conn.executed, "release_places must not execute for empty place_ids"


# ---------------------------------------------------------------------------
# B4 — process_places is wrapped in a transaction (structural check)
# ---------------------------------------------------------------------------

def test_process_places_uses_transaction() -> None:
    import inspect

    from workers.knowledge_worker import main as kw_main
    src = inspect.getsource(kw_main.process_places)
    assert "conn.transaction()" in src, (
        "process_places must wrap writes in conn.transaction() to prevent partial writes"
    )


def test_poll_active_places_passes_place_ids_to_co_inscribed() -> None:
    import inspect

    from workers.knowledge_worker import main as kw_main
    src = inspect.getsource(kw_main.poll_active_places)
    assert "build_co_inscribed_relationships" in src
    assert "place_ids" in src


# ---------------------------------------------------------------------------
# Relationship governance state machine completeness
# ---------------------------------------------------------------------------

def test_rel_transitions_has_activate() -> None:
    assert "activate" in knowledge._REL_TRANSITIONS
    new_status, allowed_from = knowledge._REL_TRANSITIONS["activate"]
    assert new_status == "active"
    assert "proposed" in allowed_from


def test_rel_transitions_has_dispute() -> None:
    assert "dispute" in knowledge._REL_TRANSITIONS
    new_status, allowed_from = knowledge._REL_TRANSITIONS["dispute"]
    assert new_status == "disputed"
    assert "active" in allowed_from
    assert "proposed" in allowed_from


def test_rel_transitions_has_retract() -> None:
    assert "retract" in knowledge._REL_TRANSITIONS
    new_status, allowed_from = knowledge._REL_TRANSITIONS["retract"]
    assert new_status == "retracted"
    assert allowed_from == {"disputed"}


def test_rel_transitions_no_direct_retract_from_active() -> None:
    _, allowed_from = knowledge._REL_TRANSITIONS["retract"]
    assert "active" not in allowed_from
