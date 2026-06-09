import json
from pathlib import Path

from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)
from workers.walters_adapter.client import load_dataset
from workers.walters_adapter.store import write_record

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "walters"


def dataset():
    return load_dataset(FIXTURES)


async def test_walters_sprint3_replay_writes_allowed_object_full_m36_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        dataset(),
        "1001",
        source_id="source-walters",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "1001"
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

    source_record_args = conn.args_by_table["source_record"]
    assert source_record_args[3] == "walters_opendata_v1"
    raw_payload = json.loads(source_record_args[4])
    assert raw_payload["object"]["ObjectID"] == "1001"
    assert raw_payload["selected_image"]["MediaXrefID"] == "2001"

    technical_args = conn.args_by_table["media_technical_metadata"]
    technical_content = json.loads(technical_args[3])
    assert technical_content["schema_standard"] == "walters_opendata_v1"
    assert technical_content["walters_object_id"] == "1001"
    assert technical_content["walters_image_url"] == (
        "https://art.thewalters.org/images/raw/W174_fnt.jpg"
    )

    media_rights_args = conn.args_by_table["media_rights"]
    evidence = json.loads(media_rights_args[2])
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["walters_object_id"] == "1001"
    assert evidence["walters_object_number"] == "W.174"
    assert evidence["walters_image_url"] == "https://art.thewalters.org/images/raw/W174_fnt.jpg"
    assert evidence["walters_media_xref_id"] == "2001"
    assert evidence["walters_is_primary"] == "1"
    assert evidence["walters_collection_ids"] == ["MAN", "MED"]
    assert evidence["walters_collection_names"] == ["Manuscripts", "Medieval"]


async def test_walters_sprint3_replay_blocks_no_primary_image_without_store_write_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        dataset(),
        "1003",
        source_id="source-walters",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "no_primary_image",
        "record_id": "1003",
        "writes": 0,
    }
    assert_no_writes(conn)
