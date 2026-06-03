"""MILESTONE-003 research replay tests.

Research outputs must be human-readable and fully supported by source evidence,
facts, relationships, provenance, governance, and replayable ordering.
"""
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from services.api.routers import research
from workers.research_worker.compose import build_research_output
from workers.research_worker.store import upsert_research_output

MIGRATION_15 = Path("infrastructure/postgres/init/15_research_outputs.sql")

_PLACE_ID = uuid4()
_ASSET_ID = uuid4()
_FACT_ID = uuid4()
_REL_ID = uuid4()
_OUTPUT_ID = uuid4()
_STATEMENT_ID = uuid4()


def _place() -> dict:
    return {
        "id": _PLACE_ID,
        "name": {"en": "Great Barrier Reef"},
        "source": "unesco_whc",
        "source_id": "31",
        "status": "active",
    }


def _fact(asset_id=_ASSET_ID) -> dict:
    return {
        "id": _FACT_ID,
        "place_id": _PLACE_ID,
        "predicate": "heritage_type",
        "value": {"text": "natural"},
        "value_type": "text",
        "language": None,
        "asset_id": asset_id,
        "source": "unesco_whc",
        "confidence_score": 0.95,
        "status": "active",
        "provenance": {"source_field": "places.heritage_type"},
        "agent_notes": {},
    }


def _relationship(asset_id=None) -> dict:
    return {
        "id": _REL_ID,
        "subject_id": _PLACE_ID,
        "subject_type": "place",
        "predicate": "classified_as",
        "object_id": uuid4(),
        "object_type": "concept",
        "confidence_score": 0.95,
        "status": "active",
        "asset_id": asset_id,
        "provenance": {"derived_from_predicate": "heritage_type"},
        "agent_notes": {},
    }


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

def test_research_migration_exists() -> None:
    assert MIGRATION_15.exists()


def test_research_schema_has_output_statement_evidence_tables() -> None:
    sql = MIGRATION_15.read_text()
    assert "CREATE TABLE research_outputs" in sql
    assert "CREATE TABLE research_statements" in sql
    assert "CREATE TABLE research_statement_evidence" in sql


def test_research_evidence_requires_asset_fact_and_relationship() -> None:
    sql = MIGRATION_15.read_text()
    assert "asset_id        UUID NOT NULL REFERENCES assets(id)" in sql
    assert "fact_id         UUID NOT NULL REFERENCES facts(id)" in sql
    assert "relationship_id UUID NOT NULL REFERENCES relationships(id)" in sql


def test_research_schema_rejects_unsupported_statements() -> None:
    sql = MIGRATION_15.read_text()
    assert "assert_research_statement_supported" in sql
    assert "DEFERRABLE INITIALLY DEFERRED" in sql
    assert "research statement % has no source evidence/fact/relationship support" in sql


def test_research_schema_requires_coherent_evidence_place() -> None:
    sql = MIGRATION_15.read_text()
    assert "assert_research_evidence_coherent" in sql
    assert "fact place does not match research statement place" in sql
    assert "relationship does not support research statement place" in sql
    assert "asset does not match supporting fact or relationship evidence" in sql


def test_research_schema_has_governance_lifecycle() -> None:
    sql = MIGRATION_15.read_text()
    for status in ("pending_review", "approved", "published", "rejected", "disputed", "retracted"):
        assert status in sql


def test_research_schema_requires_synchronized_published_statements() -> None:
    sql = MIGRATION_15.read_text()
    assert "cannot be % with unsynchronized statements" in sql
    assert "s.status <> NEW.status" in sql


# ---------------------------------------------------------------------------
# Worker composition
# ---------------------------------------------------------------------------

def test_build_research_output_emits_supported_statement() -> None:
    output = build_research_output(_place(), [_fact()], [_relationship()])

    assert output is not None
    assert output["title"] == "Great Barrier Reef"
    assert output["status"] == "pending_review"
    assert (
        output["statements"][0]["body"]
        == "Great Barrier Reef is classified as natural heritage."
    )
    evidence = output["statements"][0]["evidence"][0]
    assert evidence["asset_id"] == _ASSET_ID
    assert evidence["fact_id"] == _FACT_ID
    assert evidence["relationship_id"] == _REL_ID


def test_build_research_output_drops_fact_without_source_evidence() -> None:
    output = build_research_output(_place(), [_fact(asset_id=None)], [_relationship(asset_id=None)])
    assert output is None


def test_build_research_output_drops_relationship_without_supporting_fact() -> None:
    unsupported = _relationship()
    unsupported["provenance"] = {"derived_from_predicate": "missing_predicate"}
    output = build_research_output(_place(), [_fact()], [unsupported])
    assert output is None


def test_build_research_output_is_deterministic() -> None:
    first = build_research_output(_place(), [_fact()], [_relationship()])
    second = build_research_output(_place(), [_fact()], [_relationship()])
    assert first == second


class FakeStoreTx:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeStoreConn:
    def __init__(self) -> None:
        self.fetchrow_queries: list[str] = []
        self.execute_queries: list[str] = []

    def transaction(self):
        return FakeStoreTx()

    async def fetchrow(self, query: str, *args):
        self.fetchrow_queries.append(query)
        if "INSERT INTO research_outputs" in query:
            return {"id": _OUTPUT_ID}
        if "INSERT INTO research_statements" in query:
            return {"id": _STATEMENT_ID}
        return None

    async def execute(self, query: str, *args):
        self.execute_queries.append(query)
        return "INSERT 0 1"


async def test_upsert_research_output_writes_statement_evidence() -> None:
    conn = FakeStoreConn()
    output = build_research_output(_place(), [_fact()], [_relationship()])

    output_id = await upsert_research_output(conn, output)

    assert output_id == _OUTPUT_ID
    assert any("INSERT INTO research_outputs" in query for query in conn.fetchrow_queries)
    assert any("INSERT INTO research_statements" in query for query in conn.fetchrow_queries)
    assert any("INSERT INTO research_statement_evidence" in query for query in conn.execute_queries)


# ---------------------------------------------------------------------------
# API and governance
# ---------------------------------------------------------------------------

class FakeTx:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeResearchConn:
    def __init__(self, status: str = "pending_review") -> None:
        self.status = status
        self.executed: list[tuple[str, tuple]] = []
        self.fetchrow_queries: list[str] = []

    def transaction(self):
        return FakeTx()

    async def fetchrow(self, query: str, *args):
        self.fetchrow_queries.append(query)
        if "SELECT status FROM research_outputs" in query:
            return {"status": self.status}
        if "FROM research_outputs" in query:
            return {
                "id": _OUTPUT_ID,
                "place_id": _PLACE_ID,
                "output_type": "place_brief",
                "output_version": "1",
                "title": "Great Barrier Reef",
                "summary": "Research brief",
                "status": self.status,
                "confidence_score": 0.95,
                "reviewed_by": None,
                "reviewed_at": None,
                "published_at": None,
                "provenance": json.dumps({"prov:wasGeneratedBy": "research_worker:v0.3.0"}),
                "agent_notes": json.dumps({}),
                "created_at": "2026-06-01T00:00:00Z",
                "updated_at": "2026-06-01T00:00:00Z",
            }
        return None

    async def fetch(self, query: str, *args):
        if "FROM research_statements" in query:
            return [
                {
                    "id": _STATEMENT_ID,
                    "output_id": _OUTPUT_ID,
                    "place_id": _PLACE_ID,
                    "sequence": 1,
                    "statement_type": "classification",
                    "body": "Great Barrier Reef is classified as natural heritage.",
                    "status": self.status,
                    "confidence_score": 0.95,
                    "provenance": json.dumps({}),
                    "agent_notes": json.dumps({}),
                    "created_at": "2026-06-01T00:00:00Z",
                    "updated_at": "2026-06-01T00:00:00Z",
                }
            ]
        if "FROM research_statement_evidence" in query:
            return [
                {
                    "id": uuid4(),
                    "statement_id": _STATEMENT_ID,
                    "asset_id": _ASSET_ID,
                    "fact_id": _FACT_ID,
                    "relationship_id": _REL_ID,
                    "evidence_role": "supporting",
                    "provenance": json.dumps({}),
                    "created_at": "2026-06-01T00:00:00Z",
                    "asset_raw_path": "raw/ingestion/place/ingest/source.json",
                    "asset_normalized_path": "normalized/ingestion/place/ingest/source.json",
                    "asset_checksum_sha256": "abc123",
                    "fact_predicate": "heritage_type",
                    "fact_value": json.dumps({"text": "natural"}),
                    "relationship_predicate": "classified_as",
                }
            ]
        return []

    async def execute(self, query: str, *args):
        self.executed.append((query, args))
        return "UPDATE 1"


async def test_get_research_output_returns_statements_with_evidence() -> None:
    result = await research.get_research_output(
        output_id=UUID(str(_OUTPUT_ID)),
        auth="dev-secret",
        conn=FakeResearchConn(),
    )

    assert result["title"] == "Great Barrier Reef"
    assert result["statements"][0]["evidence"][0]["asset_id"] == _ASSET_ID
    assert result["statements"][0]["evidence"][0]["fact_id"] == _FACT_ID
    evidence = result["statements"][0]["evidence"][0]
    assert evidence["relationship_id"] == _REL_ID
    assert evidence["asset_raw_path"] == "raw/ingestion/place/ingest/source.json"
    assert evidence["fact_predicate"] == "heritage_type"
    assert evidence["fact_value"] == {"text": "natural"}
    assert evidence["relationship_predicate"] == "classified_as"


async def test_research_output_approval_updates_output_and_statements() -> None:
    conn = FakeResearchConn(status="pending_review")
    result = await research.act_on_research_output(
        output_id=UUID(str(_OUTPUT_ID)),
        body=research.ResearchOutputAction(action="approve", reviewer="curator"),
        auth="dev-secret",
        conn=conn,
    )

    assert result["status"] == "approved"
    assert result["reviewed_by"] == "curator"
    assert any("UPDATE research_outputs" in query for query, _ in conn.executed)
    assert any("UPDATE research_statements" in query for query, _ in conn.executed)
    assert any("FOR UPDATE" in query for query in conn.fetchrow_queries)


async def test_research_retract_requires_reason() -> None:
    with pytest.raises(Exception) as exc_info:
        await research.act_on_research_output(
            output_id=UUID(str(_OUTPUT_ID)),
            body=research.ResearchOutputAction(action="retract", reviewer="curator"),
            auth="dev-secret",
            conn=FakeResearchConn(status="disputed"),
        )
    assert getattr(exc_info.value, "status_code", None) == 422


async def test_research_publish_only_from_approved() -> None:
    with pytest.raises(Exception) as exc_info:
        await research.act_on_research_output(
            output_id=UUID(str(_OUTPUT_ID)),
            body=research.ResearchOutputAction(action="publish", reviewer="curator"),
            auth="dev-secret",
            conn=FakeResearchConn(status="pending_review"),
        )
    assert getattr(exc_info.value, "status_code", None) == 422
