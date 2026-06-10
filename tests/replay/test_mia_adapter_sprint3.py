import json
from pathlib import Path

from workers.mia_adapter.store import write_record
from workers.shared_media_adapter.replay import ReplayConn, assert_m36_write_order, assert_no_writes

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "mia"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_public_domain_valid_image_writes_once() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_public_domain_valid_image.json"),
        source_id="source-mia",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["writes"] == 7
    assert len([event for event in conn.events if event[1] == "media_file"]) == 1
    assert_m36_write_order(conn)


async def test_mia_sprint3_replay_noc_us_valid_image_writes_once() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_noc_us_valid_image.json"),
        source_id="source-mia",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "1013"
    assert result["writes"] == 7
    assert len([event for event in conn.events if event[1] == "media_file"]) == 1
    assert_m36_write_order(conn)

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["rights_statement_uri"] == "https://rightsstatements.org/vocab/NoC-US/1.0/"
    assert evidence["mia_rights_uri"] == "https://rightsstatements.org/vocab/NoC-US/1.0/"
    assert evidence["mia_rights_type"] == "No Copyright–United States"
    assert evidence["worker_classified_status"] == "classified_pd"

    assert conn.args_by_table["media_file"][3] == "https://5.api.artsmia.org/800/1013.jpg"


async def test_restricted_zero_inc_edu_produces_zero_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_restricted_zero_inc_edu.json"),
        source_id="source-mia",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == "blocked_observed_rights_type"
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_deterministic_public_domain_write() -> None:
    left_conn = ReplayConn()
    right_conn = ReplayConn()
    record = fixture_json("object_public_domain_valid_image.json")

    left = await write_record(left_conn, record, source_id="source-mia", media_type_id="image")
    right = await write_record(right_conn, record, source_id="source-mia", media_type_id="image")

    assert left["status"] == "written"
    assert right["status"] == "written"
    assert left["raw_payload_hash"] == right["raw_payload_hash"]
    assert left["technical_content_hash"] == right["technical_content_hash"]
    assert left_conn.sql_order == right_conn.sql_order
    assert left_conn.args_by_table["media_file"][:4] == right_conn.args_by_table["media_file"][:4]
    assert json.loads(left_conn.args_by_table["media_rights"][2]) == json.loads(
        right_conn.args_by_table["media_rights"][2]
    )
