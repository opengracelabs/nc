import json
from pathlib import Path

from workers.nasa_adapter.normalize import build_rights_evidence, normalize_record
from workers.nasa_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nasa"
def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_nasa_sprint2_jpl_replay_is_review_required() -> None:
    rights = classify_rights(fixture_json("record_jpl_review_image.json"))

    assert rights["decision"] == "REVIEW_REQUIRED"
    assert rights["rights_basis"] == "review_center_jpl"


def test_nasa_sprint2_esa_replay_is_review_required() -> None:
    rights = classify_rights(fixture_json("record_esa_review_image.json"))

    assert rights["decision"] == "REVIEW_REQUIRED"
    assert rights["rights_basis"] == "review_partner_marker"
    assert rights["partner_markers"] == ["ESA"]


def test_nasa_sprint2_ap_reuters_replay_are_blocked() -> None:
    for fixture, marker in (
        ("record_ap_blocked_image.json", "AP"),
        ("record_reuters_blocked_image.json", "Reuters"),
    ):
        rights = classify_rights(fixture_json(fixture))
        assert rights["decision"] == "BLOCKED"
        assert rights["rights_basis"] == "blocked_partner_marker"
        assert marker in rights["partner_markers"]


def test_nasa_sprint2_clean_federal_image_normalizes_once() -> None:
    candidates = normalize_record(
        fixture_json("record_nasa_federal_image.json"),
        asset_manifest=fixture_json("asset_gsfc_20171208_archive_manifest.json"),
    )

    assert len(candidates) == 1
    assert candidates[0]["record_id"] == "GSFC_20171208_ARCHIVE"
    assert candidates[0]["nasa_rights_basis"] == "federal_center_clean_rights"


def test_nasa_sprint2_earthrise_and_blue_marble_are_allowed_candidates() -> None:
    cases = (
        ("record_earthrise.json", "asset_as08_14_2383_manifest.json", "AS08-14-2383"),
        ("record_blue_marble.json", "asset_as17_148_22727_manifest.json", "AS17-148-22727"),
    )

    for record_fixture, manifest_fixture, nasa_id in cases:
        candidates = normalize_record(
            fixture_json(record_fixture),
            asset_manifest=fixture_json(manifest_fixture),
        )
        assert len(candidates) == 1
        assert candidates[0]["record_id"] == nasa_id
        assert candidates[0]["rights_decision"] == "ALLOWED"
        assert candidates[0]["representative_media_url"].endswith("~orig.jpg")


def test_nasa_sprint2_required_evidence_fields_are_present() -> None:
    evidence = build_rights_evidence(
        fixture_json("record_nasa_federal_image.json"),
        asset_manifest=fixture_json("asset_gsfc_20171208_archive_manifest.json"),
    )

    assert set(evidence) == {
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
    }
    assert evidence["nasa_source_api"] == "images-api.nasa.gov"
    assert evidence["nasa_publicity_risk_detected"] is False
