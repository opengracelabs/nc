import json
from pathlib import Path

from workers.nasa_adapter.normalize import normalize_record
from workers.nasa_adapter.store import write_record
from workers.shared_media_adapter.replay import ReplayConn, assert_m36_write_order, assert_no_writes

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nasa"
REQUIRED_22_NASA_FIELDS = {
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


async def _write(
    record_fixture: str,
    manifest_fixture: str | None = None,
) -> tuple[dict, ReplayConn]:
    conn = ReplayConn()
    result = await write_record(
        conn,
        fixture_json(record_fixture),
        source_id="source-nasa",
        media_type_id="image",
        asset_manifest=fixture_json(manifest_fixture) if manifest_fixture else None,
    )
    return result, conn


async def test_nasa_sprint3_earthrise_writes_7_rows() -> None:
    result, conn = await _write("record_earthrise.json", "asset_as08_14_2383_manifest.json")

    assert result["status"] == "written"
    assert result["record_id"] == "AS08-14-2383"
    assert result["writes"] == 7
    assert_m36_write_order(conn)


async def test_nasa_sprint3_gsfc_federal_writes_7_rows() -> None:
    result, conn = await _write(
        "record_nasa_federal_image.json",
        "asset_gsfc_20171208_archive_manifest.json",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "GSFC_20171208_ARCHIVE"
    assert result["writes"] == 7
    assert_m36_write_order(conn)


async def test_nasa_sprint3_jpl_produces_zero_writes() -> None:
    result, conn = await _write("record_jpl_review_image.json", "asset_pia00001_manifest.json")

    assert result == {
        "status": "rejected",
        "reason": "review_required_pilot_exclusion",
        "record_id": "PIA00001",
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_nasa_sprint3_esa_partner_produces_zero_writes() -> None:
    result, conn = await _write("record_esa_review_image.json")

    assert result["reason"] == "review_required_pilot_exclusion"
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_nasa_sprint3_stsci_partner_produces_zero_writes() -> None:
    result, conn = await _write("record_stsci_review_image.json")

    assert result["reason"] == "review_required_pilot_exclusion"
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_nasa_sprint3_publicity_risk_produces_zero_writes() -> None:
    result, conn = await _write("record_publicity_risk_review_image.json")

    assert result["reason"] == "review_required_pilot_exclusion"
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_nasa_sprint3_getty_blocked_produces_zero_writes() -> None:
    result, conn = await _write("record_getty_blocked_image.json")

    assert result["status"] == "rejected"
    assert result["reason"] == "blocked_partner_marker"
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_nasa_sprint3_earthrise_evidence_contains_22_nasa_fields() -> None:
    _, conn = await _write("record_earthrise.json", "asset_as08_14_2383_manifest.json")

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert REQUIRED_22_NASA_FIELDS.issubset(evidence)
    assert len([key for key in evidence if key.startswith("nasa_")]) == 22


async def test_nasa_sprint3_delivery_url_is_orig_from_manifest() -> None:
    _, conn = await _write("record_earthrise.json", "asset_as08_14_2383_manifest.json")

    media_file_url = conn.args_by_table["media_file"][3]
    manifest = fixture_json("asset_as08_14_2383_manifest.json")
    manifest_urls = [item["href"] for item in manifest["collection"]["items"]]
    assert media_file_url in manifest_urls
    assert media_file_url.endswith("AS08-14-2383~orig.jpg")


async def test_nasa_sprint3_deterministic_write_stability() -> None:
    first, first_conn = await _write("record_earthrise.json", "asset_as08_14_2383_manifest.json")
    second, second_conn = await _write("record_earthrise.json", "asset_as08_14_2383_manifest.json")

    assert first["raw_payload_hash"] == second["raw_payload_hash"]
    assert first["technical_content_hash"] == second["technical_content_hash"]
    assert first_conn.sql_order == second_conn.sql_order
    assert first_conn.args_by_table["media_file"][3] == second_conn.args_by_table["media_file"][3]


def test_nasa_g7_asset_zero_earthrise_confirmed() -> None:
    candidates = normalize_record(
        fixture_json("record_earthrise.json"),
        asset_manifest=fixture_json("asset_as08_14_2383_manifest.json"),
    )

    assert len(candidates) == 1
    assert candidates[0]["record_id"] == "AS08-14-2383"
    assert candidates[0]["rights_decision"] == "ALLOWED"
    assert candidates[0]["representative_media_url"].endswith("~orig.jpg")
