import json
from pathlib import Path

from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)
from workers.walters_adapter.client import load_dataset
from workers.walters_adapter.store import derive_anchor_type, write_record

FIXTURES = Path("tests/fixtures/walters")


def dataset():
    return load_dataset(FIXTURES)


def test_derive_anchor_type_marks_asset_zero_as_geographic() -> None:
    normalized = {
        "classification": "Manuscripts & Rare Books",
        "object_name": "book of hours",
        "title": "Leaf from a Book of Hours",
    }

    assert derive_anchor_type(normalized, "image") == "geographic"


def test_derive_anchor_type_marks_biological_subjects_as_biological() -> None:
    normalized = {
        "subject_terms": ["Flowers"],
        "title": "Marginal Botanical Study",
        "classification": "Drawing",
    }

    assert derive_anchor_type(normalized, "image") == "biological"


async def test_write_record_uses_shared_m36_write_path_for_allowed_object() -> None:
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
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "walters_opendata_v1"
    assert conn.args_by_table["media_file"][3] == (
        "https://art.thewalters.org/images/raw/W174_fnt.jpg"
    )

    raw_payload = json.loads(conn.args_by_table["source_record"][4])
    assert raw_payload["object"]["ObjectID"] == "1001"
    assert raw_payload["selected_image"]["MediaXrefID"] == "2001"
    assert [row["MediaXrefID"] for row in raw_payload["images"]] == ["2001", "2002"]
    assert [row["id"] for row in raw_payload["creators"]] == ["501", "502"]

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["walters_object_id"] == "1001"
    assert normalized_payload["walters_object_number"] == "W.174"
    assert normalized_payload["walters_image_url"] == (
        "https://art.thewalters.org/images/raw/W174_fnt.jpg"
    )
    assert normalized_payload["walters_media_xref_id"] == "2001"
    assert normalized_payload["walters_is_primary"] == "1"


async def test_write_record_rejects_missing_primary_image_without_writes() -> None:
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
