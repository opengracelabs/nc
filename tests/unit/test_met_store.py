import json
from pathlib import Path

from workers.met_adapter.normalize import normalize_record
from workers.met_adapter.store import derive_anchor_type, write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path("tests/fixtures/met")


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_derive_anchor_type_marks_great_wave_as_geographic() -> None:
    normalized = normalize_record(load_json("object_hokusai_public_domain.json"))

    assert derive_anchor_type(normalized, "image") == "geographic"


async def test_write_record_uses_shared_m36_write_path_for_great_wave() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("object_hokusai_public_domain.json"),
        source_id="source-met",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "45434"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "met_openaccess_v1"
    assert conn.args_by_table["media_file"][3] == (
        "https://images.metmuseum.org/CRDImages/as/original/DP130155.jpg"
    )

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["met_object_id"] == "45434"
    assert normalized_payload["met_is_public_domain"] is True
    assert normalized_payload["additional_images"] == [
        "https://images.metmuseum.org/CRDImages/as/original/DP130156.jpg"
    ]


async def test_write_record_rejects_not_public_domain_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("object_not_public_domain.json"),
        source_id="source-met",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "not_public_domain",
        "record_id": "90001",
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_write_record_rejects_missing_rights_field_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("object_missing_rights_field.json"),
        source_id="source-met",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "missing_rights_field",
        "record_id": "90002",
        "writes": 0,
    }
    assert_no_writes(conn)

