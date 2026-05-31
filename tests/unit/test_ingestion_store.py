import hashlib

from workers.ingestion_worker.store import store_raw_evidence


class FakeMinio:
    def __init__(self) -> None:
        self.calls = []

    async def put_object(self, **kwargs):
        self.calls.append(kwargs)


async def test_store_raw_evidence_uses_place_id_path_and_checksum() -> None:
    minio = FakeMinio()
    raw = b'{"id": 31}'

    path, checksum = await store_raw_evidence(minio, raw, "place-1", "ingest-1")

    assert path == "ingestion/place-1/ingest-1/source_record.json"
    assert checksum == hashlib.sha256(raw).hexdigest()
    assert minio.calls[0]["object_name"] == path
    assert minio.calls[0]["length"] == len(raw)
