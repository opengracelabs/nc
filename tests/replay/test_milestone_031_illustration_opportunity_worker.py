"""v0.3.1 Illustration Opportunity Discovery replay tests."""
from uuid import uuid4

from workers.illustration_opportunity_worker.discover import build_illustration_opportunity
from workers.illustration_opportunity_worker.store import upsert_illustration_opportunity

_PLACE_ID = uuid4()
_CONCEPT_ID = uuid4()
_OPPORTUNITY_ID = uuid4()


def _bhl_record() -> dict:
    return {
        "ItemID": "12345",
        "PageID": "67890",
        "Title": "Naturalist's Miscellany",
        "PageTitle": "Acanthaster planci plate",
        "Illustrator": "Nodder",
        "Year": "1789",
        "Rights": "Public Domain",
        "RightsUrl": "https://www.biodiversitylibrary.org/page/67890",
        "PageUrl": "https://www.biodiversitylibrary.org/page/67890",
        "Width": 2400,
        "Height": 2600,
        "CommercialValueScore": 0.92,
    }


def _opportunity() -> dict:
    result = build_illustration_opportunity(
        place_id=_PLACE_ID,
        concept_id=_CONCEPT_ID,
        taxon_name="Acanthaster planci",
        bhl_record=_bhl_record(),
        gbif_validation={
            "source_url": "https://www.gbif.org/species/2270935",
            "gbif_taxon_key": "2270935",
            "place_relevance_score": 0.91,
            "role": "validation_only",
        },
        wikidata_context={
            "source_url": "https://www.wikidata.org/wiki/Q203929",
            "wikidata_qid": "Q203929",
            "role": "context_only",
        },
    )
    assert result is not None
    return result


def test_worker_builds_required_illustration_opportunity_fields() -> None:
    result = _opportunity()

    assert "place_id" not in result
    assert result["place_link"]["place_id"] == _PLACE_ID
    assert result["concept_id"] == _CONCEPT_ID
    assert result["bhl_item_id"] == "12345"
    assert result["bhl_page_id"] == "67890"
    assert result["publication_year"] == 1789
    assert result["illustrator"] == "Nodder"
    assert result["rights_status"] == "Public Domain"
    assert result["opportunity_score"] > 0.9


def test_worker_uses_bhl_as_primary_discovery_source() -> None:
    result = _opportunity()

    assert result["source"] == "bhl"
    assert result["source_record_id"] == "item:12345:page:67890"
    assert result["provenance"]["source_roles"]["bhl"] == "primary_discovery"
    assert any(
        e["source"] == "bhl" and e["evidence_type"] == "illustration"
        for e in result["evidence"]
    )


def test_worker_uses_gbif_validation_and_wikidata_context_only() -> None:
    result = _opportunity()

    assert result["provenance"]["source_roles"]["gbif"] == "validation_only"
    assert result["provenance"]["source_roles"]["wikidata"] == "context_only"
    assert any(
        e["source"] == "gbif" and e["evidence_type"] == "place_relevance"
        for e in result["evidence"]
    )
    assert any(
        e["source"] == "wikidata" and e["evidence_type"] == "taxonomic_context"
        for e in result["evidence"]
    )


def test_worker_rejects_unverified_or_ambiguous_rights() -> None:
    record = _bhl_record()
    record["Rights"] = "No known copyright restrictions"

    result = build_illustration_opportunity(
        place_id=_PLACE_ID,
        concept_id=_CONCEPT_ID,
        taxon_name="Acanthaster planci",
        bhl_record=record,
    )

    assert result is None


class FakeTx:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeOpportunityConn:
    def __init__(self) -> None:
        self.fetchrow_queries: list[tuple[str, tuple]] = []
        self.execute_queries: list[tuple[str, tuple]] = []

    def transaction(self):
        return FakeTx()

    async def fetchrow(self, query: str, *args):
        self.fetchrow_queries.append((query, args))
        if "INSERT INTO illustration_opportunities" in query:
            return {"id": _OPPORTUNITY_ID}
        return None

    async def execute(self, query: str, *args):
        self.execute_queries.append((query, args))
        return "OK"


async def test_store_writes_opportunity_place_link_and_evidence() -> None:
    conn = FakeOpportunityConn()
    opportunity_id = await upsert_illustration_opportunity(conn, _opportunity())

    assert opportunity_id == _OPPORTUNITY_ID
    insert_query, insert_args = conn.fetchrow_queries[0]
    assert "INSERT INTO illustration_opportunities" in insert_query
    assert _PLACE_ID not in insert_args
    assert _CONCEPT_ID in insert_args
    assert "12345" in insert_args
    assert "67890" in insert_args
    assert any(
        "INSERT INTO illustration_opportunity_places" in q for q, _ in conn.execute_queries
    )
    assert any(
        "INSERT INTO illustration_opportunity_evidence" in q for q, _ in conn.execute_queries
    )
