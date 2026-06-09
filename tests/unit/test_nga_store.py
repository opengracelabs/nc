import json
from pathlib import Path

from workers.nga_adapter.client import load_dataset
from workers.nga_adapter.store import derive_anchor_type, write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path("tests/fixtures/nga")


def dataset():
    return load_dataset(FIXTURES)


def test_derive_anchor_type_marks_asset_zero_as_geographic() -> None:
    normalized = {
        "subject_terms": ["Bridge", "France"],
        "title": "The Japanese Footbridge",
        "classification": "Painting",
    }

    assert derive_anchor_type(normalized, "image") == "geographic"


def test_derive_anchor_type_follows_dd_precedence_rules() -> None:
    assert derive_anchor_type({"title": "Atlas"}, "map") == "geographic"
    assert (
        derive_anchor_type({"place_executed": "France", "subject_terms": ["Birds"]}, "image")
        == "geographic"
    )
    assert (
        derive_anchor_type({"subject_terms": ["Birds", "Flowers"], "title": "Study"}, "image")
        == "biological"
    )
    assert derive_anchor_type({"school": "French"}, "image") == "geographic"
    assert derive_anchor_type({"creator_nationality": "French"}, "image") == "geographic"
    assert derive_anchor_type({"subject_terms": ["Bridge"]}, "image") == "geographic"
    assert derive_anchor_type({"subject_terms": ["Portrait"]}, "image") == "cultural"


async def test_write_record_uses_shared_m36_write_path_for_openaccess_object() -> None:
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
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "nga_openaccess_v1"
    assert conn.args_by_table["media_file"][3] == (
        "https://api.nga.gov/iiif/img-primary-2001/full/!1024,1024/0/default.jpg"
    )

    raw_payload = json.loads(conn.args_by_table["source_record"][4])
    assert raw_payload["object"]["objectid"] == "2001"
    assert raw_payload["selected_image"]["uuid"] == "img-primary-2001"
    assert [row["uuid"] for row in raw_payload["images"]] == [
        "img-primary-2001",
        "img-alt-2001",
    ]
    assert [row["term"] for row in raw_payload["terms"]] == ["Bridge", "France", "French"]
    assert raw_payload["constituents"][0]["constituentid"] == "501"

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["nga_openaccess"] == "1"
    assert normalized_payload["nga_image_uuid"] == "img-primary-2001"
    assert normalized_payload["nga_iiifurl"] == "https://api.nga.gov/iiif/img-primary-2001"
    assert normalized_payload["nga_objectid"] == "2001"
    assert normalized_payload["nga_accessionnum"] == "1942.9.97"


async def test_write_record_rejects_not_open_access_without_writes() -> None:
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
