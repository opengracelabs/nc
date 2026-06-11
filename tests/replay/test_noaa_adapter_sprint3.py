import json
from pathlib import Path

from workers.noaa_adapter.client import flickr_record_to_discovery_payload
from workers.noaa_adapter.store import REVIEW_REQUIRED_PILOT_EXCLUSION, write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"
NOAA_ADAPTER = Path(__file__).resolve().parents[2] / "workers" / "noaa_adapter"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def fixture_record(name: str) -> dict:
    return flickr_record_to_discovery_payload(fixture_json(name))


async def test_noaa_sprint3_allowed_replay_writes_m36_without_workflow() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_record("federal_agency_usgs_credit.json"),
        source_id="source-noaa",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert "workflow_items" not in conn.sql_order


async def test_noaa_sprint3_review_required_replay_is_pilot_excluded() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_record("flickr_photo_university_review.json"),
        source_id="source-noaa",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == REVIEW_REQUIRED_PILOT_EXCLUSION
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_noaa_sprint3_blocked_replay_has_zero_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_record("flickr_photo_getty_blocked.json"),
        source_id="source-noaa",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == "blocked_partner_marker"
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_noaa_sprint3_evidence_extension_survives_replay() -> None:
    conn = ReplayConn()

    await write_record(
        conn,
        fixture_record("federal_agency_nasa_credit.json"),
        source_id="source-noaa",
        media_type_id="image",
    )

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["noaa_source_system"] == "flickr"
    assert evidence["noaa_source_record_id"] == "1017"
    assert evidence["noaa_credit"] == "NASA"
    assert evidence["noaa_license_label"] == "United States Government Work"
    assert evidence["noaa_partner_markers"] == []
    assert evidence["noaa_blocked_markers"] == []


def test_noaa_sprint3_store_boundary_is_adapter_only() -> None:
    assert (NOAA_ADAPTER / "store.py").exists()
    assert not (NOAA_ADAPTER / "workflow.py").exists()

