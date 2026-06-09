import json
from pathlib import Path

from workers.met_adapter.store import write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path("tests/fixtures/met")


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_met_sprint3_replay_writes_great_wave_full_m36_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("object_hokusai_public_domain.json"),
        source_id="source-met",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "45434"
    assert result["source_item_id"] == "source_item-1"
    assert result["source_record_id"] == "source_record-2"
    assert result["media_file_id"] == "media_file-3"
    assert result["media_rights_id"] == "media_rights-4"
    assert result["technical_metadata_id"] == "media_technical_metadata-6"
    assert result["workflow_item_id"] is None
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)

    preservation_args = conn.args_by_table["preservation_event"]
    assert preservation_args[4] == "rights_verification"
    assert preservation_args[5] == "pending_human_review"

    media_rights_args = conn.args_by_table["media_rights"]
    evidence = json.loads(media_rights_args[2])
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["met_is_public_domain"] is True


async def test_met_sprint3_replay_blocks_no_image_without_store_write_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("object_public_domain_no_image.json"),
        source_id="source-met",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "no_image_url",
        "record_id": "90003",
        "writes": 0,
    }
    assert_no_writes(conn)
