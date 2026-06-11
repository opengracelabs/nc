import json
from pathlib import Path

from workers.noaa_adapter.client import flickr_record_to_discovery_payload
from workers.noaa_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def flickr_fixture(name: str) -> dict:
    return flickr_record_to_discovery_payload(fixture_json(name))


def test_noaa_rights_sprint2_allows_federal_agency_credits() -> None:
    for credit in (
        "NOAA",
        "NOAA/OMAO",
        "ESSA",
        "Weather Bureau",
        "USCGS",
        "Bureau of Commercial Fisheries",
        "NASA",
        "USGS",
        "USFWS",
        "NPS",
        "EPA",
        "NSF",
        "USACE",
        "NIST",
    ):
        rights = classify_rights({"credit": credit, "title": f"{credit} federal image"})
        assert rights["decision"] == "ALLOWED"
        assert rights["rights_basis"] == "noaa_federal_credit"


def test_noaa_rights_sprint2_reviews_nasa_esa_before_federal_allow() -> None:
    rights = classify_rights(flickr_fixture("flickr_photo_nasa_esa_review.json"))

    assert rights["decision"] == "REVIEW_REQUIRED"
    assert rights["rights_basis"] == "partner_or_contributor_marker"
    assert "NASA/ESA" in rights["partner_markers"]


def test_noaa_rights_sprint2_blocks_dedicated_maxar_and_planet_fixtures() -> None:
    for name, marker in (
        ("flickr_photo_maxar_blocked.json", "Maxar"),
        ("flickr_photo_planet_blocked.json", "Planet"),
    ):
        rights = classify_rights(flickr_fixture(name))
        assert rights["decision"] == "BLOCKED"
        assert rights["rights_basis"] == "blocked_partner_marker"
        assert rights["blocked_markers"] == [marker]

