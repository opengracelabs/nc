import json
from pathlib import Path

from workers.nga_adapter.client import load_dataset
from workers.nga_adapter.store import write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nga"


def dataset():
    return load_dataset(FIXTURES)


async def test_nga_sprint3_replay_writes_openaccess_object_full_m36_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        dataset(),
        "2001",
        source_id="source-nga",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "2001"
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
    assert source_record_args[3] == "nga_openaccess_v1"
    raw_payload = json.loads(source_record_args[4])
    assert raw_payload["object"]["objectid"] == "2001"
    assert raw_payload["selected_image"]["uuid"] == "img-primary-2001"
    assert [row["term"] for row in raw_payload["terms"]] == ["Bridge", "France", "French"]

    technical_args = conn.args_by_table["media_technical_metadata"]
    technical_content = json.loads(technical_args[3])
    assert technical_content["schema_standard"] == "nga_openaccess_v1"
    assert technical_content["school"] == "French"
    assert technical_content["place_executed"] == "France"
    assert technical_content["creator_nationality"] == "French"

    media_rights_args = conn.args_by_table["media_rights"]
    evidence = json.loads(media_rights_args[2])
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["nga_openaccess"] == "1"
    assert evidence["nga_iiifurl"] == "https://api.nga.gov/iiif/img-primary-2001"
    assert evidence["nga_objectid"] == "2001"
    assert evidence["nga_accessionnum"] == "1942.9.97"


async def test_nga_sprint3_replay_blocks_restricted_object_without_store_write_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        dataset(),
        "2002",
        source_id="source-nga",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "no_published_image",
        "record_id": "2002",
        "writes": 0,
    }
    assert_no_writes(conn)
