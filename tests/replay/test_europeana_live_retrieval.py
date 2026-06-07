import json
from pathlib import Path

from workers.europeana_adapter import main

_FIXTURE = Path("tests/fixtures/europeana/yellowstone_launch_metadata_v1_record.json")


def _yellowstone_payload() -> dict:
    return json.loads(_FIXTURE.read_text())


async def test_live_yellowstone_dry_run_replay_is_stable(monkeypatch) -> None:
    async def fake_fetch_record(record_id: str) -> dict:
        assert record_id == main.YELLOWSTONE_RECORD_ID
        return _yellowstone_payload()

    monkeypatch.setattr(main.client, "fetch_record", fake_fetch_record)

    first = await main.ingest_live_asset(dry_run=True)
    second = await main.ingest_live_asset(dry_run=True)

    assert first["result"]["raw_payload_hash"] == second["result"]["raw_payload_hash"]
    assert first["result"]["technical_content_hash"] == second["result"]["technical_content_hash"]
    assert first["events"] == second["events"]
    assert first["result"]["writes"] == 7
