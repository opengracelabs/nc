from workers.discovery_worker.store import upsert_candidate


class FakeConn:
    def __init__(self) -> None:
        self.query = ""
        self.args = ()

    async def fetchrow(self, query: str, *args):
        self.query = query
        self.args = args
        return {"id": "candidate-id", "created": True}


async def test_upsert_candidate_uses_on_conflict() -> None:
    conn = FakeConn()

    candidate_id, created = await upsert_candidate(
        conn,
        {
            "source": "unesco_whc",
            "source_id": "31",
            "wikidata_qid": None,
            "name": {"en": "Example"},
            "description": {},
            "country_codes": ["AU"],
            "heritage_type": "mixed",
            "ouv_criteria": ["i"],
            "inscription_year": 1981,
            "centroid": {"type": "Point", "coordinates": [151.2, -33.8]},
            "confidence_score": 0.9,
            "provenance": {},
        },
    )

    assert candidate_id == "candidate-id"
    assert created is True
    assert "ON CONFLICT (source, source_id) DO UPDATE" in conn.query
