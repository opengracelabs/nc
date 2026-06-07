import json
from pathlib import Path

from workers.europeana_adapter import main

_FIXTURE = Path("tests/fixtures/europeana/yellowstone_launch_metadata_v1_record.json")


def _yellowstone_payload() -> dict:
    return json.loads(_FIXTURE.read_text())


async def test_fetch_live_asset_uses_record_api_client(monkeypatch) -> None:
    calls = []

    async def fake_fetch_record(record_id: str) -> dict:
        calls.append(record_id)
        return _yellowstone_payload()

    monkeypatch.setattr(main.client, "fetch_record", fake_fetch_record)

    result = await main.fetch_live_asset()

    assert calls == [main.YELLOWSTONE_RECORD_ID]
    assert result["object"]["id"] == "/9200518/ark__12148_btv1b530248434"


async def test_ingest_live_asset_dry_run_creates_expected_substrate_records(monkeypatch) -> None:
    async def fake_fetch_record(record_id: str) -> dict:
        assert record_id == main.YELLOWSTONE_RECORD_ID
        return _yellowstone_payload()

    monkeypatch.setattr(main.client, "fetch_record", fake_fetch_record)

    result = await main.ingest_live_asset(dry_run=True)

    assert result["mode"] == "dry_run"
    assert result["result"]["status"] == "written"
    assert result["result"]["record_id"] == "/9200518/ark__12148_btv1b530248434"
    assert result["result"]["source_item_id"] == "source_item-1"
    assert result["result"]["source_record_id"] == "source_record-2"
    assert result["result"]["media_file_id"] == "media_file-3"
    assert result["result"]["media_rights_id"] == "media_rights-4"
    assert result["result"]["technical_metadata_id"] == "media_technical_metadata-6"
    assert [event["table"] for event in result["events"] if event["table"]] == [
        "source_item",
        "source_record",
        "media_file",
        "media_rights",
        "preservation_event",
        "media_technical_metadata",
        "source_item",
    ]


async def test_ingest_live_asset_write_mode_uses_asyncpg_connection(monkeypatch) -> None:
    closed = []

    class FakeConn(main.DryRunConnection):
        async def close(self) -> None:
            closed.append(True)

    async def fake_connect(dsn: str) -> FakeConn:
        assert dsn
        return FakeConn()

    async def fake_fetch_record(record_id: str) -> dict:
        return _yellowstone_payload()

    monkeypatch.setattr(main.client, "fetch_record", fake_fetch_record)
    monkeypatch.setattr(main.asyncpg, "connect", fake_connect)

    result = await main.ingest_live_asset(dry_run=False)

    assert result["mode"] == "write"
    assert result["result"]["status"] == "written"
    assert closed == [True]
