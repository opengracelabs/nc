import json
from pathlib import Path

from workers.nasa_adapter import store as nasa_store
from workers.nasa_adapter.store import write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nasa"
REQUIRED_NASA_EVIDENCE_FIELDS = {
    "nasa_id",
    "nasa_center",
    "nasa_media_type",
    "nasa_rights_uri",
    "nasa_rights_basis",
    "nasa_asset_manifest_url",
    "nasa_metadata_url",
    "nasa_original_url",
    "nasa_large_url",
    "nasa_preview_url",
    "nasa_selected_asset_url",
    "nasa_photographer",
    "nasa_secondary_creator",
    "nasa_keywords",
    "nasa_album",
    "nasa_partner_markers",
    "nasa_copyright_detected",
    "nasa_publicity_risk_detected",
    "nasa_source_api",
    "nasa_rights_policy_id",
    "nasa_schema_standard",
    "nasa_source_slug",
}


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_write_record_uses_shared_m36_write_path_for_allowed_earthrise() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("record_earthrise.json"),
        source_id="source-nasa",
        media_type_id="image",
        asset_manifest=fixture_json("asset_as08_14_2383_manifest.json"),
    )

    assert result["status"] == "written"
    assert result["record_id"] == "AS08-14-2383"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "nasa_images_collection_json_v1"
    assert conn.args_by_table["media_file"][3].endswith("AS08-14-2383~orig.jpg")

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert REQUIRED_NASA_EVIDENCE_FIELDS.issubset(evidence)
    assert evidence["source"] == "nasa_images"
    assert evidence["worker_classified_status"] == "classified_pd"
    assert evidence["rights_matrix_classification"] == "allowed"
    assert evidence["nasa_id"] == "AS08-14-2383"
    assert evidence["nasa_rights_basis"] == "federal_center_clean_rights"


async def test_write_record_rejects_review_required_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("record_jpl_review_image.json"),
        source_id="source-nasa",
        media_type_id="image",
        asset_manifest=fixture_json("asset_pia00001_manifest.json"),
    )

    assert result == {
        "status": "rejected",
        "reason": "review_required_pilot_exclusion",
        "record_id": "PIA00001",
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_write_record_rejects_blocked_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("record_getty_blocked_image.json"),
        source_id="source-nasa",
        media_type_id="image",
        asset_manifest=fixture_json("asset_jsc2007e034221_manifest.json"),
    )

    assert result["status"] == "rejected"
    assert result["reason"] == "blocked_partner_marker"
    assert result["writes"] == 0
    assert_no_writes(conn)


def test_nasa_store_runtime_configuration_and_callable_extension() -> None:
    runtime = nasa_store._runtime()

    assert runtime.worker_id == "nasa_adapter:sprint3"
    assert runtime.source_slug == "nasa_images"
    assert runtime.schema_standard == "nasa_images_collection_json_v1"
    assert runtime.rights_policy_id == "nasa_images_rights_class_10_v1"
    assert runtime.anchor_type == "geographic"
    assert callable(runtime.build_evidence_extension)


def test_nasa_evidence_extension_returns_all_normalized_nasa_fields() -> None:
    normalized = {
        "record_id": "AS08-14-2383",
        "nasa_id": "AS08-14-2383",
        "nasa_center": "JSC",
        "not_nasa": "ignored",
    }

    assert nasa_store._build_evidence_extension(normalized) == {
        "nasa_id": "AS08-14-2383",
        "nasa_center": "JSC",
    }
