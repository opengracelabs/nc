import pytest

from workers.ingestion_worker.fetch import _source_url
from workers.ingestion_worker.validate import validate_candidate


def test_wikidata_source_url_requires_qid() -> None:
    assert _source_url("wikidata", "Q123", {}) == (
        "https://www.wikidata.org/wiki/Special:EntityData/Q123.json"
    )
    with pytest.raises(ValueError, match="must be a QID"):
        _source_url("wikidata", "31", {})


def test_validate_candidate_allows_claimed_ingesting_status() -> None:
    errors = validate_candidate(
        {
            "id": "candidate-1",
            "source": "unesco_whc",
            "source_id": "31",
            "name": {"en": "Example"},
            "status": "ingesting",
            "country_codes": ["AU"],
            "centroid": {"type": "Point", "coordinates": [151.2, -33.8]},
            "ouv_criteria": ["i", "vii"],
        }
    )

    assert errors == []


class FakeExecuteConn:
    def __init__(self) -> None:
        self.query = ""
        self.args = ()

    async def execute(self, query: str, *args):
        self.query = query
        self.args = args
        return "UPDATE 2"


async def test_reset_stale_ingesting_uses_integer_interval() -> None:
    from workers.ingestion_worker.main import reset_stale_ingesting

    conn = FakeExecuteConn()

    updated = await reset_stale_ingesting(conn, timeout_seconds=900)

    assert updated == 2
    assert conn.args == (900,)
    assert "$1::int * interval '1 second'" in conn.query
