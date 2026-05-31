import json

import workers.ingestion_worker.main as ingestion


class FakeConn:
    def __init__(self) -> None:
        self.status_updates = []
        self.source_errors = []

    async def fetchrow(self, query: str, *args):
        if "FROM discovery_candidates" in query:
            return {
                "id": "candidate-1",
                "source": "unesco_whc",
                "source_id": "31",
                "wikidata_qid": None,
                "unesco_ref_id": "31",
                "name": {"en": "Great Barrier Reef"},
                "description": {},
                "statement_of_ouv": {},
                "justification": {},
                "country_codes": ["AU"],
                "heritage_type": "natural",
                "transboundary": False,
                "ouv_criteria": ["vii"],
                "inscription_year": 1981,
                "centroid": json.dumps({"type": "Point", "coordinates": [147.7, -18.2]}),
                "core_area_ha": 34800000.0,
                "buffer_area_ha": None,
                "spatial_precision": "surveyed",
                "confidence_score": 0.9,
                "status": "ingesting",
                "promoted_place_id": None,
            }
        if "FROM sources" in query:
            return {"config": {"api_base": "https://example.test/api/v2"}}
        raise AssertionError(query)

    async def execute(self, query: str, *args):
        if "UPDATE discovery_candidates" in query:
            self.status_updates.append((query, args))
        if "UPDATE sources" in query:
            self.source_errors.append((query, args))
        return "UPDATE 1"


class FakeMinio:
    pass


async def test_unesco_ingestion_replay_promotes_to_place(monkeypatch) -> None:
    calls = {}

    async def fake_fetch_raw(source, source_id, config):
        calls["fetch"] = (source, source_id, config)
        return b'{"site":"Great Barrier Reef"}', "https://example.test/api/v2/sites/31/?format=json"

    async def fake_store_raw_evidence(minio, raw_bytes, place_id, ingest_id):
        calls["store"] = (raw_bytes, place_id, ingest_id)
        return f"ingestion/{place_id}/{ingest_id}/source_record.json", "checksum"

    async def fake_insert_place(
        conn, candidate, ingest_id, place_id, raw_path, checksum, source_url, size_bytes
    ):
        calls["insert"] = {
            "candidate": candidate,
            "ingest_id": ingest_id,
            "place_id": place_id,
            "raw_path": raw_path,
            "checksum": checksum,
            "source_url": source_url,
            "size_bytes": size_bytes,
        }
        return place_id

    monkeypatch.setattr(ingestion, "fetch_raw", fake_fetch_raw)
    monkeypatch.setattr(ingestion, "store_raw_evidence", fake_store_raw_evidence)
    monkeypatch.setattr(ingestion, "insert_place", fake_insert_place)

    conn = FakeConn()
    place_id = await ingestion.ingest_candidate(conn, FakeMinio(), "candidate-1")

    assert place_id == calls["insert"]["place_id"]
    assert calls["fetch"] == (
        "unesco_whc",
        "31",
        {"api_base": "https://example.test/api/v2"},
    )
    assert calls["insert"]["raw_path"].startswith(f"ingestion/{place_id}/")
    assert calls["insert"]["size_bytes"] == len(b'{"site":"Great Barrier Reef"}')
    assert conn.status_updates == []
    assert conn.source_errors == []
