import json
from pathlib import Path

from workers.noaa_adapter import store as noaa_store
from workers.noaa_adapter.client import flickr_record_to_discovery_payload
from workers.noaa_adapter.store import REVIEW_REQUIRED_PILOT_EXCLUSION, write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def fixture_record(name: str) -> dict:
    return flickr_record_to_discovery_payload(fixture_json(name))


async def test_noaa_write_record_uses_shared_m36_path_for_allowed_record() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_record("federal_agency_nasa_credit.json"),
        source_id="source-noaa",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "1017"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "noaa_discovery_v1"
    assert conn.args_by_table["media_file"][3].endswith("1017_nasa_z.jpg")

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["source"] == "noaa"
    assert evidence["applying_policy"] == "noaa_rights_matrix_v1"
    assert evidence["rights_matrix_classification"] == "allowed"
    assert evidence["noaa_source_system"] == "flickr"
    assert evidence["noaa_credit"] == "NASA"
    assert evidence["noaa_license_id"] == "8"
    assert evidence["noaa_rights_class"] == "rights_class_9"
    assert evidence["noaa_source_slug"] == "noaa"


async def test_noaa_write_record_rejects_review_required_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_record("flickr_photo_nasa_esa_review.json"),
        source_id="source-noaa",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": REVIEW_REQUIRED_PILOT_EXCLUSION,
        "record_id": "1014",
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_noaa_write_record_rejects_blocked_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_record("personal_name_noaa_blocked.json"),
        source_id="source-noaa",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "personal_name_noaa_credit",
        "record_id": "1019",
        "writes": 0,
    }
    assert_no_writes(conn)


def test_noaa_store_runtime_configuration_and_callable_extension() -> None:
    runtime = noaa_store._runtime()

    assert runtime.worker_id == "noaa_adapter:sprint3"
    assert runtime.source_slug == "noaa"
    assert runtime.schema_standard == "noaa_discovery_v1"
    assert runtime.rights_policy_id == "noaa_rights_matrix_v1"
    assert runtime.anchor_type == "geographic"
    assert callable(runtime.build_evidence_extension)


def test_noaa_evidence_extension_is_adapter_owned() -> None:
    extension = noaa_store._build_evidence_extension(
        {
            "source_system": "flickr",
            "credit": "NOAA/NOS",
            "license_id": "8",
            "noaa_rights_class": "rights_class_9",
            "not_noaa": "ignored",
        }
    )

    assert extension["noaa_source_system"] == "flickr"
    assert extension["noaa_credit"] == "NOAA/NOS"
    assert extension["noaa_license_id"] == "8"
    assert extension["noaa_rights_class"] == "rights_class_9"
    assert "not_noaa" not in extension

