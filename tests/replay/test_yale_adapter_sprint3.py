import json
from pathlib import Path

from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)
from workers.yale_adapter.store import write_record

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "yale"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_yale_sprint3_replay_writes_ycba_full_m36_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("ycba_object_cc0.json"),
        manifest=fixture_json("manifest_ycba_12345_v3.json"),
        source_id="source-ycba",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "12345"
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
    assert evidence["source"] == "ycba"
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["ycba_rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert evidence["ycba_attribution"] == "Yale Center for British Art"
    assert evidence["yale_object_id"] == "12345"
    assert evidence["yale_iiif_manifest"] == "https://manifests.collections.yale.edu/ycba/obj/12345"
    assert evidence["yale_image_service"] == "https://media.collections.yale.edu/iiif/2/ycba-12345"

    technical_args = conn.args_by_table["media_technical_metadata"]
    technical_content = json.loads(technical_args[3])
    assert technical_content["source"] == "ycba"
    assert technical_content["schema_standard"] == "yale_lux_linked_art_v1"
    assert technical_content["yale_object_id"] == "12345"
    assert technical_content["yale_image_service"] == (
        "https://media.collections.yale.edu/iiif/2/ycba-12345"
    )


async def test_yale_sprint3_replay_writes_yuag_full_m36_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("yuag_object_noc_us.json"),
        manifest=fixture_json("manifest_yuag_98765_v3.json"),
        source_id="source-yuag",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "98765"
    assert result["writes"] == 7
    assert_m36_write_order(conn)

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["source"] == "yuag"
    assert evidence["worker_classified_status"] == "classified_pd"
    assert evidence["yuag_rights_uri"] == "http://rightsstatements.org/vocab/NoC-US/1.0/"
    assert evidence["yale_object_id"] == "98765"
    assert evidence["yale_iiif_manifest"] == "https://manifests.collections.yale.edu/yuag/obj/98765"
    assert evidence["yale_image_service"] == "https://media.collections.yale.edu/iiif/2/yuag-98765"


async def test_yale_sprint3_replay_blocks_unknown_rights_without_store_write_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("ycba_object_restricted.json"),
        source_id="source-ycba",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "unknown_rights_uri",
        "record_id": "55555",
        "writes": 0,
    }
    assert_no_writes(conn)
