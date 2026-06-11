import json
from pathlib import Path

from workers.noaa_adapter.client import choose_image_url, flickr_record_to_discovery_payload
from workers.noaa_adapter.normalize import normalize_record
from workers.noaa_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"
RETRIEVED_AT = "2026-06-11T00:00:00Z"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def fixture_record(name: str) -> dict:
    return flickr_record_to_discovery_payload(fixture_json(name))


def test_noaa_remediation_blocks_personal_name_noaa_credit() -> None:
    rights = classify_rights(fixture_record("personal_name_noaa_blocked.json"))

    assert rights["decision"] == "BLOCKED"
    assert rights["allowed"] is False
    assert rights["rights_statement_uri"] is None
    assert rights["rights_status"] == "blocked"
    assert rights["rights_basis"] == "personal_name_noaa_credit"
    assert rights["contributor_markers"] == ["Jane Smith/NOAA"]
    assert normalize_record(
        fixture_record("personal_name_noaa_blocked.json"),
        retrieved_at=RETRIEVED_AT,
    ) == []


def test_noaa_remediation_allows_federal_partner_agency_credits() -> None:
    for name, agency in (
        ("federal_agency_nasa_credit.json", "NASA"),
        ("federal_agency_usgs_credit.json", "USGS"),
    ):
        record = fixture_record(name)
        rights = classify_rights(record)
        normalized = normalize_record(record, retrieved_at=RETRIEVED_AT)

        assert record["credit"] == agency
        assert rights["decision"] == "ALLOWED"
        assert rights["rights_basis"] == "flickr_us_government_work"
        assert len(normalized) == 1
        assert normalized[0]["image_url"].endswith("_z.jpg")


def test_noaa_remediation_noaa_prefix_credit_allows_division_variants() -> None:
    for credit in ("NOAA", "NOAA Office of Ocean Exploration", "NOAA/OMAO"):
        rights = classify_rights({"credit": credit, "title": "NOAA federal image"})
        assert rights["decision"] == "ALLOWED"
        assert rights["rights_basis"] == "noaa_federal_credit"


def test_noaa_remediation_url_z_is_minimum_image_tier() -> None:
    assert choose_image_url({"url_z": "https://example.test/z.jpg"}) == "https://example.test/z.jpg"
    assert choose_image_url({"url_m": "https://example.test/m.jpg"}) is None
    assert choose_image_url(
        {
            "url_m": "https://example.test/m.jpg",
            "url_z": "https://example.test/z.jpg",
        }
    ) == "https://example.test/z.jpg"

