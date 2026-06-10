import json
from pathlib import Path

from workers.getty_adapter.store import write_record
from workers.shared_media_adapter.replay import ReplayConn, assert_m36_write_order, assert_no_writes

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "getty"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_getty_sprint3_compliance_allowed_record_writes_all_m36_tables_and_pins() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
        source_id="source-getty",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["writes"] == 7
    assert_m36_write_order(conn)
    assert set(conn.args_by_table) >= {
        "source_item",
        "source_record",
        "media_file",
        "media_rights",
        "preservation_event",
        "media_technical_metadata",
        "execute:source_item",
    }
    assert conn.args_by_table["execute:source_item"] == (
        "source_item-1",
        "source_record-2",
        "media_rights-4",
        "media_technical_metadata-6",
    )


async def test_getty_sprint3_compliance_blocked_record_has_zero_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_unknown_rights.json"),
        source_id="source-getty",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_getty_sprint3_compliance_missing_object_has_zero_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        None,
        source_id="source-getty",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "missing_object",
        "record_id": None,
        "writes": 0,
    }
    assert_no_writes(conn)

