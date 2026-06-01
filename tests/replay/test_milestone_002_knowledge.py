"""MILESTONE-002 knowledge API and schema replay tests.

Tests the knowledge router (concepts, facts, relationships) using fake
connections — no live database required.
"""
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from services.api.routers import knowledge
from workers.discovery_worker.normalize import normalize_unesco_whc
from workers.discovery_worker.sources.base import RawRecord
from workers.knowledge_worker.extract import build_place_concept_relationships, extract_facts
from workers.knowledge_worker.store import upsert_facts, upsert_relationships

FIXTURE = Path("tests/fixtures/unesco_whc_50_sites.json")

_CONCEPT_ID = uuid4()
_FACT_ID = uuid4()
_PLACE_ID = uuid4()


def _gbr_place() -> dict:
    site = next(s for s in json.loads(FIXTURE.read_text()) if s["id_number"] == 31)
    rec = normalize_unesco_whc(RawRecord(source_id=str(site["id_number"]), payload=site))
    rec["id"] = uuid4()
    rec["source"] = "unesco_whc"
    return rec


# ---------------------------------------------------------------------------
# Schema file sanity
# ---------------------------------------------------------------------------

def test_knowledge_schema_files_exist() -> None:
    init = Path("infrastructure/postgres/init")
    for fname in (
        "08_knowledge_concepts.sql",
        "09_knowledge_facts.sql",
        "10_knowledge_relationships.sql",
        "11_knowledge_seed.sql",
        "12_knowledge_place_fields.sql",
    ):
        assert (init / fname).exists(), f"Missing migration: {fname}"


def test_concepts_migration_creates_concepts_table() -> None:
    ddl = Path("infrastructure/postgres/init/08_knowledge_concepts.sql").read_text()
    assert "CREATE TABLE concepts" in ddl
    assert "CREATE TABLE concept_aliases" in ddl
    assert "check_concept_no_cycle" in ddl


def test_facts_migration_has_controlled_predicate_vocabulary() -> None:
    ddl = Path("infrastructure/postgres/init/09_knowledge_facts.sql").read_text()
    for predicate in ("inscription_year", "ouv_criterion", "country_code", "heritage_type"):
        assert predicate in ddl
    assert "chk_fact_predicate" in ddl
    assert "uniq_facts_slot" in ddl


def test_relationships_migration_has_self_ref_guard() -> None:
    ddl = Path("infrastructure/postgres/init/10_knowledge_relationships.sql").read_text()
    assert "chk_rel_no_self_ref" in ddl
    assert "co_inscribed_with" in ddl
    assert "exemplifies" in ddl
    assert "classified_as" in ddl


def test_seed_migration_has_all_ten_criteria() -> None:
    sql = Path("infrastructure/postgres/init/11_knowledge_seed.sql").read_text()
    for crit in ("whc:criterion/i", "whc:criterion/v", "whc:criterion/x"):
        assert crit in sql


def test_seed_migration_has_heritage_types() -> None:
    sql = Path("infrastructure/postgres/init/11_knowledge_seed.sql").read_text()
    for ht in ("whc:type/natural", "whc:type/cultural", "whc:type/mixed"):
        assert ht in sql


def test_place_fields_migration_adds_knowledge_columns() -> None:
    ddl = Path("infrastructure/postgres/init/12_knowledge_place_fields.sql").read_text()
    assert "knowledge_extracting" in ddl
    assert "last_knowledge_extracted_at" in ddl
    assert "knowledge_score" in ddl


# ---------------------------------------------------------------------------
# Fake connections for API router tests
# ---------------------------------------------------------------------------

class FakeConceptsConn:
    async def fetch(self, query: str, *args):
        return [
            {
                "id": _CONCEPT_ID,
                "uri": "whc:criterion/vii",
                "label": json.dumps({"en": "Superlative Natural Phenomena"}),
                "description": json.dumps({}),
                "type": "criterion",
                "status": "active",
                "broader_id": None,
                "provenance": json.dumps({}),
                "created_at": "2026-05-31T00:00:00Z",
                "updated_at": "2026-05-31T00:00:00Z",
            }
        ]

    async def fetchrow(self, query: str, *args):
        rows = await self.fetch(query, *args)
        return rows[0] if rows else None


class FakeFactsConn:
    def __init__(self) -> None:
        self.query = ""
        self.args: tuple = ()

    async def fetch(self, query: str, *args):
        self.query = query
        self.args = args
        return [
            {
                "id": _FACT_ID,
                "place_id": _PLACE_ID,
                "predicate": "heritage_type",
                "value": json.dumps({"text": "natural"}),
                "value_type": "text",
                "language": None,
                "concept_id": _CONCEPT_ID,
                "asset_id": None,
                "source": "unesco_whc",
                "confidence_score": 0.95,
                "status": "active",
                "provenance": json.dumps({
                    "prov:wasGeneratedBy": "knowledge_worker:v0.2.0",
                    "extraction_method": "field_mapping",
                    "source_field": "places.heritage_type",
                }),
                "agent_notes": json.dumps({}),
                "created_at": "2026-05-31T00:00:00Z",
                "updated_at": "2026-05-31T00:00:00Z",
            }
        ]

    async def fetchrow(self, query: str, *args):
        return {"status": "active"}

    async def execute(self, query: str, *args):
        self.query = query
        self.args = args
        return "UPDATE 1"


class FakeKnowledgeConn:
    async def fetch(self, query: str, *args):
        return []


# ---------------------------------------------------------------------------
# Concepts API
# ---------------------------------------------------------------------------

async def test_list_concepts_returns_decoded_labels() -> None:
    rows = await knowledge.list_concepts(
        auth="dev-secret",
        conn=FakeConceptsConn(),
        type=None,
        status=None,
        q=None,
        limit=50,
        offset=0,
    )
    assert rows[0]["label"] == {"en": "Superlative Natural Phenomena"}
    assert rows[0]["uri"] == "whc:criterion/vii"


async def test_get_concept_returns_with_aliases() -> None:
    class FakeWithAliases(FakeConceptsConn):
        async def fetch(self, query: str, *args):
            if "concept_aliases" in query:
                return []
            return await super().fetch(query, *args)

    concept = await knowledge.get_concept(
        concept_id=UUID(str(_CONCEPT_ID)),
        auth="dev-secret",
        conn=FakeWithAliases(),
    )
    assert concept["uri"] == "whc:criterion/vii"
    assert "aliases" in concept
    assert isinstance(concept["aliases"], list)


# ---------------------------------------------------------------------------
# Facts API
# ---------------------------------------------------------------------------

async def test_list_facts_decodes_value_from_jsonb() -> None:
    rows = await knowledge.list_facts(
        auth="dev-secret",
        conn=FakeFactsConn(),
        place_id=None,
        predicate=None,
        status=None,
        concept_id=None,
        source=None,
        limit=50,
        offset=0,
    )
    assert rows[0]["value"] == {"text": "natural"}
    assert rows[0]["predicate"] == "heritage_type"


async def test_list_facts_provenance_is_decoded() -> None:
    rows = await knowledge.list_facts(
        auth="dev-secret",
        conn=FakeFactsConn(),
        place_id=None,
        predicate=None,
        status=None,
        concept_id=None,
        source=None,
        limit=50,
        offset=0,
    )
    prov = rows[0]["provenance"]
    assert isinstance(prov, dict)
    assert prov["extraction_method"] == "field_mapping"
    assert prov["source_field"] == "places.heritage_type"


async def test_list_facts_filters_by_place_id() -> None:
    conn = FakeFactsConn()
    await knowledge.list_facts(
        auth="dev-secret",
        conn=conn,
        place_id=_PLACE_ID,
        predicate=None,
        status=None,
        concept_id=None,
        source=None,
        limit=50,
        offset=0,
    )
    assert "place_id" in conn.query


async def test_list_facts_filters_by_predicate() -> None:
    conn = FakeFactsConn()
    await knowledge.list_facts(
        auth="dev-secret",
        conn=conn,
        place_id=None,
        predicate="heritage_type",
        status=None,
        concept_id=None,
        source=None,
        limit=50,
        offset=0,
    )
    assert "predicate" in conn.query
    assert "heritage_type" in conn.args


async def test_act_on_fact_dispute_transitions_to_disputed() -> None:
    conn = FakeFactsConn()
    result = await knowledge.act_on_fact(
        fact_id=UUID(str(_FACT_ID)),
        body=knowledge.FactAction(action="dispute", reviewer="auditor", reason="Source conflict"),
        auth="dev-secret",
        conn=conn,
    )
    assert result["status"] == "disputed"
    assert result["reviewed_by"] == "auditor"


async def test_act_on_fact_requires_reviewer() -> None:
    from fastapi import HTTPException
    conn = FakeFactsConn()
    with pytest.raises(HTTPException) as exc_info:
        await knowledge.act_on_fact(
            fact_id=UUID(str(_FACT_ID)),
            body=knowledge.FactAction(action="dispute", reviewer="   ", reason=None),
            auth="dev-secret",
            conn=conn,
        )
    assert exc_info.value.status_code == 422


async def test_act_on_fact_retract_requires_reason() -> None:
    from fastapi import HTTPException

    class FakeDisputedConn(FakeFactsConn):
        async def fetchrow(self, query, *args):
            return {"status": "disputed"}

    conn = FakeDisputedConn()
    with pytest.raises(HTTPException) as exc_info:
        await knowledge.act_on_fact(
            fact_id=UUID(str(_FACT_ID)),
            body=knowledge.FactAction(action="retract", reviewer="auditor", reason=None),
            auth="dev-secret",
            conn=conn,
        )
    assert exc_info.value.status_code == 422


async def test_act_on_fact_retracts_disputed_fact_with_reason() -> None:
    class FakeDisputedConn(FakeFactsConn):
        async def fetchrow(self, query, *args):
            return {"status": "disputed"}

    conn = FakeDisputedConn()
    result = await knowledge.act_on_fact(
        fact_id=UUID(str(_FACT_ID)),
        body=knowledge.FactAction(
            action="retract",
            reviewer="auditor",
            reason="Source evidence was withdrawn",
        ),
        auth="dev-secret",
        conn=conn,
    )

    assert result["status"] == "retracted"
    assert "Source evidence was withdrawn" in conn.args[1]


async def test_act_on_fact_invalid_action_rejected() -> None:
    from fastapi import HTTPException
    conn = FakeFactsConn()
    with pytest.raises(HTTPException) as exc_info:
        await knowledge.act_on_fact(
            fact_id=UUID(str(_FACT_ID)),
            body=knowledge.FactAction(action="delete", reviewer="auditor"),
            auth="dev-secret",
            conn=conn,
        )
    assert exc_info.value.status_code == 422


# ---------------------------------------------------------------------------
# Place knowledge aggregate
# ---------------------------------------------------------------------------

async def test_get_place_knowledge_returns_facts_and_relationships() -> None:
    result = await knowledge.get_place_knowledge(
        place_id=UUID(str(_PLACE_ID)),
        auth="dev-secret",
        conn=FakeKnowledgeConn(),
    )
    assert "place_id" in result
    assert "facts" in result
    assert "relationships" in result
    assert result["place_id"] == str(_PLACE_ID)


# ---------------------------------------------------------------------------
# Extraction produces facts traceable to source
# ---------------------------------------------------------------------------

def test_gbr_facts_source_fields_all_reference_places_columns() -> None:
    place = _gbr_place()
    for fact in extract_facts(place):
        sf = fact["provenance"]["source_field"]
        assert sf.startswith("places.") or sf.startswith("field:"), (
            f"predicate={fact['predicate']} has unexpected source_field={sf!r}"
        )


def test_all_50_sites_facts_are_traceable() -> None:
    sites = json.loads(FIXTURE.read_text())
    for site in sites:
        rec = normalize_unesco_whc(RawRecord(source_id=str(site["id_number"]), payload=site))
        rec["id"] = uuid4()
        rec["source"] = "unesco_whc"
        for fact in extract_facts(rec):
            prov = fact["provenance"]
            assert "prov:wasGeneratedBy" in prov
            assert "source_field" in prov
            assert "extraction_version" in prov



async def test_upsert_facts_keeps_multi_value_predicates_active() -> None:
    class FakeStoreConn:
        def __init__(self) -> None:
            self.queries: list[str] = []

        async def fetchval(self, query: str, *args):
            self.queries.append(query)
            if "INSERT INTO facts" in query:
                return 2
            return 0

    conn = FakeStoreConn()
    facts = [
        {
            "place_id": _PLACE_ID,
            "predicate": "country_code",
            "value": {"text": "AU"},
            "value_type": "text",
            "language": None,
            "asset_id": None,
            "source": "unesco_whc",
            "confidence_score": 0.95,
            "provenance": {"source_field": "places.country_codes"},
        },
        {
            "place_id": _PLACE_ID,
            "predicate": "country_code",
            "value": {"text": "PG"},
            "value_type": "text",
            "language": None,
            "asset_id": None,
            "source": "unesco_whc",
            "confidence_score": 0.95,
            "provenance": {"source_field": "places.country_codes"},
        },
    ]

    written, superseded = await upsert_facts(conn, facts)

    supersede_queries = [q for q in conn.queries if "UPDATE facts" in q]
    assert written == 2
    assert superseded == 0
    assert supersede_queries
    assert "predicate <> ALL" in supersede_queries[0]


async def test_upsert_relationships_uses_set_based_replay_insert() -> None:
    class FakeRelationshipConn:
        def __init__(self) -> None:
            self.query = ""

        async def fetchval(self, query: str, *args):
            self.query = query
            return 2

    rels = [
        {
            "subject_id": _PLACE_ID,
            "subject_type": "place",
            "predicate": "exemplifies",
            "object_id": _CONCEPT_ID,
            "object_type": "concept",
            "confidence_score": 0.95,
            "status": "active",
            "asset_id": None,
            "provenance": {"derived_from_predicate": "ouv_criterion"},
        },
        {
            "subject_id": _PLACE_ID,
            "subject_type": "place",
            "predicate": "classified_as",
            "object_id": _CONCEPT_ID,
            "object_type": "concept",
            "confidence_score": 0.95,
            "status": "active",
            "asset_id": None,
            "provenance": {"derived_from_predicate": "heritage_type"},
        },
    ]

    written = await upsert_relationships(FakeRelationshipConn(), rels)

    assert written == 2


def test_relationship_replay_is_deterministic_for_great_barrier_reef() -> None:
    place = _gbr_place()
    facts = extract_facts(place)
    first = build_place_concept_relationships(place["id"], facts, place["source"])
    second = build_place_concept_relationships(place["id"], facts, place["source"])

    first_keys = [(r["subject_id"], r["predicate"], r.get("concept_uri")) for r in first]
    second_keys = [(r["subject_id"], r["predicate"], r.get("concept_uri")) for r in second]
    assert first_keys == second_keys
    assert {r["predicate"] for r in first} >= {"classified_as", "exemplifies"}


def test_knowledge_performance_migration_contains_search_indexes() -> None:
    sql = Path("infrastructure/postgres/init/13_knowledge_performance_indexes.sql").read_text()
    for index_name in (
        "idx_facts_active_predicate_created_at",
        "idx_relationships_active_place_co_inscribed",
        "idx_places_description_trgm",
        "idx_places_active_updated_at_desc",
    ):
        assert index_name in sql
