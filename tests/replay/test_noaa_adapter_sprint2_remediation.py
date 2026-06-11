import json
from pathlib import Path

from workers.noaa_adapter.client import flickr_record_to_discovery_payload
from workers.noaa_adapter.normalize import normalize_record
from workers.noaa_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"
NOAA_ADAPTER = Path(__file__).resolve().parents[2] / "workers" / "noaa_adapter"
RETRIEVED_AT = "2026-06-11T00:00:00Z"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def fixture_record(name: str) -> dict:
    return flickr_record_to_discovery_payload(fixture_json(name))


def test_noaa_sprint2_remediation_fixture_inventory_is_present() -> None:
    for name in (
        "federal_agency_nasa_credit.json",
        "federal_agency_usgs_credit.json",
        "personal_name_noaa_blocked.json",
    ):
        assert (FIXTURES / name).exists()


def test_noaa_sprint2_remediation_rights_decisions_are_stable() -> None:
    cases = (
        ("federal_agency_nasa_credit.json", "ALLOWED"),
        ("federal_agency_usgs_credit.json", "ALLOWED"),
        ("personal_name_noaa_blocked.json", "BLOCKED"),
    )

    for name, decision in cases:
        assert classify_rights(fixture_record(name))["decision"] == decision


def test_noaa_sprint2_remediation_normalization_stays_read_only() -> None:
    allowed = normalize_record(
        fixture_record("federal_agency_nasa_credit.json"),
        retrieved_at=RETRIEVED_AT,
    )
    blocked = normalize_record(
        fixture_record("personal_name_noaa_blocked.json"),
        retrieved_at=RETRIEVED_AT,
    )

    assert len(allowed) == 1
    assert allowed[0]["representative_media_url"].endswith("_z.jpg")
    assert blocked == []
    assert (NOAA_ADAPTER / "store.py").exists()

