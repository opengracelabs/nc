import json
from pathlib import Path

from workers.noaa_adapter.client import flickr_record_to_discovery_payload
from workers.noaa_adapter.normalize import normalize_record
from workers.noaa_adapter.rights import classify_rights
from workers.noaa_adapter.technical import build_technical_metadata, validation_status

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"
NOAA_ADAPTER = Path(__file__).resolve().parents[2] / "workers" / "noaa_adapter"
RETRIEVED_AT = "2026-06-11T00:00:00Z"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def fixture_record(name: str) -> dict:
    return flickr_record_to_discovery_payload(fixture_json(name))


def test_noaa_sprint2_read_only_module_boundary() -> None:
    assert (NOAA_ADAPTER / "config.py").exists()
    assert (NOAA_ADAPTER / "technical.py").exists()
    assert (NOAA_ADAPTER / "store.py").exists()


def test_noaa_sprint2_fixture_inventory_is_present() -> None:
    required = (
        "flickr_photo_usgov_clean_noaa.json",
        "flickr_photo_noaa_division_credit.json",
        "flickr_photo_personal_noaa_review.json",
        "flickr_photo_nasa_esa_review.json",
        "flickr_photo_getty_blocked.json",
        "flickr_photo_reuters_blocked.json",
        "flickr_photo_ap_blocked.json",
        "flickr_photo_maxar_blocked.json",
        "flickr_photo_planet_blocked.json",
    )

    assert all((FIXTURES / name).exists() for name in required)


def test_noaa_sprint2_rights_matrix_replay_decisions_are_stable() -> None:
    cases = (
        ("flickr_photo_usgov_clean_noaa.json", "ALLOWED"),
        ("flickr_photo_noaa_division_credit.json", "ALLOWED"),
        ("flickr_photo_personal_noaa_review.json", "BLOCKED"),
        ("flickr_photo_nasa_esa_review.json", "REVIEW_REQUIRED"),
        ("flickr_photo_getty_blocked.json", "BLOCKED"),
        ("flickr_photo_reuters_blocked.json", "BLOCKED"),
        ("flickr_photo_ap_blocked.json", "BLOCKED"),
        ("flickr_photo_maxar_blocked.json", "BLOCKED"),
        ("flickr_photo_planet_blocked.json", "BLOCKED"),
    )

    for name, decision in cases:
        assert classify_rights(fixture_record(name))["decision"] == decision


def test_noaa_sprint2_allowed_records_normalize_without_writes() -> None:
    normalized = normalize_record(
        fixture_record("flickr_photo_usgov_clean_noaa.json"),
        retrieved_at=RETRIEVED_AT,
    )
    review = normalize_record(
        fixture_record("flickr_photo_nasa_esa_review.json"),
        retrieved_at=RETRIEVED_AT,
    )
    blocked = normalize_record(
        fixture_record("flickr_photo_planet_blocked.json"),
        retrieved_at=RETRIEVED_AT,
    )

    assert len(normalized) == 1
    assert normalized[0]["noaa_rights_class"] == "rights_class_9"
    assert review == []
    assert blocked == []


def test_noaa_sprint2_technical_replay_is_discovery_only() -> None:
    normalized = normalize_record(
        fixture_record("flickr_photo_usgov_clean_noaa.json"),
        retrieved_at=RETRIEVED_AT,
    )[0]
    content = build_technical_metadata(normalized)

    assert validation_status(content) == "valid"
    assert content["source"] == "noaa"
    assert content["rights_policy_id"] == "noaa_rights_matrix_v1"
    assert "media_type_id" not in content

