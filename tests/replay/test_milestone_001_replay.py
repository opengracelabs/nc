import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from services.api.routers import discovery, places
from workers.discovery_worker import normalize
from workers.discovery_worker.score import score
from workers.discovery_worker.sources.unesco_whc import UnescoWHCSource
from workers.ingestion_worker import fetch as ingestion_fetch
from workers.preservation_worker.main import (
    VerificationResult,
    claim_fetched_assets,
    verify_asset_object,
)

FIXTURE = Path("tests/fixtures/unesco_whc_50_sites.json")
FIXTURE_BYTES = FIXTURE.read_bytes()


class FakeApprovalConn:
    def __init__(self) -> None:
        self.candidate_id = uuid4()
        self.executed = []

    async def fetchrow(self, query: str, *args):
        return {"status": "pending"}

    async def execute(self, query: str, *args):
        self.executed.append((query, args))
        return "UPDATE 1"


class FakeSearchConn:
    def __init__(self) -> None:
        self.query = ""
        self.args = ()
        self.place_id = uuid4()

    async def fetch(self, query: str, *args):
        self.query = query
        self.args = args
        return [
            {
                "id": self.place_id,
                "wikidata_qid": None,
                "geonames_id": None,
                "osm_relation_id": None,
                "source_id": "31",
                "source": "unesco_whc",
                "unesco_ref_id": "31",
                "name": json.dumps({"en": "Great Barrier Reef"}),
                "description": json.dumps({"en": "A globally significant coral reef ecosystem."}),
                "statement_of_ouv": json.dumps({}),
                "justification": json.dumps({}),
                "heritage_type": "natural",
                "ouv_criteria": ["vii", "viii", "ix", "x"],
                "category_skos": [],
                "transboundary": False,
                "country_codes": ["AU"],
                "continent": None,
                "centroid": json.dumps({"type": "Point", "coordinates": [147.6992, -18.2871]}),
                "boundary": None,
                "area_ha": None,
                "core_area_ha": 34800000.0,
                "buffer_area_ha": None,
                "spatial_precision": "surveyed",
                "inscription_year": 1981,
                "inscription_date": None,
                "endangered_since": None,
                "status": "candidate",
                "confidence_score": 0.95,
                "agent_notes": json.dumps({}),
                "provenance": json.dumps({"source": "replay"}),
                "created_at": "2026-05-31T00:00:00Z",
                "updated_at": "2026-05-31T00:00:00Z",
            }
        ]

    async def fetchrow(self, query: str, *args):
        rows = await self.fetch(query, *args)
        return rows[0] if rows else None


class FakeClaimConn:
    def __init__(self) -> None:
        self.query = ""
        self.args = ()

    async def fetch(self, query: str, *args):
        self.query = query
        self.args = args
        return []


class FakeObject:
    def __init__(self, size: int) -> None:
        self.size = size


class FakeResponse:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw_bytes = raw_bytes
        self.released = False

    async def read(self) -> bytes:
        return self.raw_bytes

    async def release(self) -> None:
        self.released = True


class FakeMinio:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw_bytes = raw_bytes
        self.response = FakeResponse(raw_bytes)

    async def stat_object(self, bucket_name: str, object_name: str):
        return FakeObject(len(self.raw_bytes))

    async def get_object(self, bucket_name: str, object_name: str):
        return self.response


async def test_discovery_replay_reads_great_barrier_reef(monkeypatch) -> None:
    from workers.discovery_worker import config

    monkeypatch.setattr(config.settings, "unesco_replay_fixture", str(FIXTURE))

    result = await UnescoWHCSource().fetch({}, "run-1")

    assert result.total == 50
    assert len(result.records) == 50
    assert any(
        r.source_id == "31" and r.payload["site"] == "Great Barrier Reef"
        for r in result.records
    )


async def test_approval_replay_promotes_pending_candidate_to_approved() -> None:
    conn = FakeApprovalConn()

    result = await discovery.act_on_candidate(
        candidate_id=conn.candidate_id,
        body=discovery.CandidateAction(action="approve", reviewer="replay"),
        auth="dev-secret",
        conn=conn,
    )

    assert result == {
        "id": str(conn.candidate_id),
        "status": "approved",
        "reviewed_by": "replay",
    }
    assert conn.executed[0][1][0] == "approved"


async def test_ingestion_replay_fetch_reads_fixture(monkeypatch) -> None:
    monkeypatch.setattr(ingestion_fetch.settings, "unesco_replay_fixture", str(FIXTURE))

    raw_bytes, source_url = await ingestion_fetch.fetch_raw("unesco_whc", "31", {})

    assert source_url == f"{FIXTURE}#31"
    assert b"Great Barrier Reef" in raw_bytes
    assert b"Galapagos Islands" not in raw_bytes


async def test_preservation_replay_marks_valid_for_matching_object() -> None:
    raw_bytes = FIXTURE_BYTES
    asset = {
        "id": uuid4(),
        "raw_path": "ingestion/place/ingest/source_record.json",
        "checksum_sha256": __import__("hashlib").sha256(raw_bytes).hexdigest(),
        "size_bytes": len(raw_bytes),
    }

    result = await verify_asset_object(FakeMinio(raw_bytes), asset)

    assert result == VerificationResult("valid", [])


async def test_preservation_replay_quarantines_checksum_mismatch() -> None:
    raw_bytes = FIXTURE_BYTES
    asset = {
        "id": uuid4(),
        "raw_path": "ingestion/place/ingest/source_record.json",
        "checksum_sha256": "bad",
        "size_bytes": len(raw_bytes),
    }

    result = await verify_asset_object(FakeMinio(raw_bytes), asset)

    assert result.status == "quarantined"
    assert result.warnings == ["checksum_sha256 mismatch"]


async def test_preservation_replay_claim_qualifies_returning_columns() -> None:
    conn = FakeClaimConn()

    await claim_fetched_assets(conn, 5)

    assert "FOR UPDATE SKIP LOCKED" in conn.query
    assert "RETURNING" in conn.query
    assert "a.id" in conn.query
    assert conn.args == (5,)


async def test_search_replay_uses_postgres_filters() -> None:
    conn = FakeSearchConn()

    rows = await places.search_places(
        auth="dev-secret",
        conn=conn,
        q="reef",
        country="AU",
        heritage_type="natural",
        criterion="vii",
    )

    assert rows[0]["name"] == {"en": "Great Barrier Reef"}
    assert rows[0]["centroid"] == {"type": "Point", "coordinates": [147.6992, -18.2871]}
    assert "name::text ILIKE" in conn.query
    assert conn.args[:4] == ("natural", "AU", "vii", "%reef%")


async def test_get_place_replay_decodes_json_fields() -> None:
    conn = FakeSearchConn()

    row = await places.get_place(UUID(str(conn.place_id)), auth="dev-secret", conn=conn)

    assert row["name"]["en"] == "Great Barrier Reef"
    assert row["description"]["en"].startswith("A globally significant")


def test_unesco_replay_fixture_contains_50_sites() -> None:
    sites = json.loads(FIXTURE.read_text())

    assert len(sites) == 50
    assert len({str(site["id_number"]) for site in sites}) == 50
    assert any(site["site"] == "Great Barrier Reef" for site in sites)


def test_great_barrier_reef_end_to_end_replay_record() -> None:
    site = next(
        item for item in json.loads(FIXTURE.read_text())
        if item["site"] == "Great Barrier Reef"
    )
    record = normalize.normalize_unesco_whc(
        __import__("workers.discovery_worker.sources.base", fromlist=["RawRecord"]).RawRecord(
            source_id=str(site["id_number"]),
            payload=site,
        )
    )
    record["confidence_score"] = score(record)

    assert record["source"] == "unesco_whc"
    assert record["source_id"] == "31"
    assert record["name"]["en"] == "Great Barrier Reef"
    assert record["country_codes"] == ["AU"]
    assert record["heritage_type"] == "natural"
    assert record["ouv_criteria"] == ["vii", "viii", "ix", "x"]
    assert record["confidence_score"] >= 0.8


@pytest.mark.parametrize(
    ("params", "expected_arg"),
    [
        ({"country": "AU"}, "AU"),
        ({"criterion": "vii"}, "vii"),
        ({"heritage_type": "natural"}, "natural"),
    ],
)
async def test_list_places_replay_filters(params, expected_arg) -> None:
    conn = FakeSearchConn()

    await places.list_places(
        auth="dev-secret",
        conn=conn,
        status=None,
        heritage_type=params.get("heritage_type"),
        country=params.get("country"),
        country_code=None,
        criterion=params.get("criterion"),
        ouv_criterion=None,
        inscription_year=None,
        limit=50,
        offset=0,
    )

    assert expected_arg in conn.args
