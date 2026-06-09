import json
from pathlib import Path

from workers.cma_adapter.normalize import normalize_record
from workers.cma_adapter.store import derive_anchor_type, write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path("tests/fixtures/cma")


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_derive_anchor_type_marks_cloudy_mountains_as_geographic() -> None:
    normalized = normalize_record(load_json("artwork_cloudy_mountains_cc0.json"))

    assert derive_anchor_type(normalized, "image") == "geographic"


def test_derive_anchor_type_marks_biological_subjects_as_biological() -> None:
    normalized = {"subject_terms": ["Birds", "Flowers"], "title": "Study"}

    assert derive_anchor_type(normalized, "image") == "biological"


def test_derive_anchor_type_marks_find_spot_as_geographic_after_biological() -> None:
    normalized = {"subject_terms": [], "title": "Study", "find_spot": "Cleveland"}

    assert derive_anchor_type(normalized, "image") == "geographic"


def test_derive_anchor_type_marks_culture_as_geographic_after_biological() -> None:
    assert derive_anchor_type({"culture": ["France"]}, "image") == "geographic"
    assert derive_anchor_type({"culture": "France"}, "image") == "geographic"


async def test_write_record_uses_shared_m36_write_path_for_cloudy_mountains() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("artwork_cloudy_mountains_cc0.json"),
        source_id="source-cma",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "113945"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "cma_openaccess_v1"
    assert conn.args_by_table["media_file"][3] == (
        "https://openaccess-cdn.clevelandart.org/1933.220/1933.220_print.jpg"
    )

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["cma_share_license_status"] == "CC0"
    assert normalized_payload["cma_copyright"] is None
    assert normalized_payload["cma_image_web_url"].endswith("1933.220_web.jpg")
    assert normalized_payload["cma_image_print_url"].endswith("1933.220_print.jpg")
    assert normalized_payload["cma_image_full_url"].endswith("1933.220_full.tif")


async def test_write_record_rejects_not_cc0_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("artwork_not_cc0.json"),
        source_id="source-cma",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "not_cc0",
        "record_id": "94979",
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_write_record_rejects_missing_delivery_image_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("artwork_cc0_no_web_image.json"),
        source_id="source-cma",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "no_image_url",
        "record_id": "94979",
        "writes": 0,
    }
    assert_no_writes(conn)
