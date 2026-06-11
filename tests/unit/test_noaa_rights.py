import json
from pathlib import Path

from workers.noaa_adapter.client import (
    flickr_record_to_discovery_payload,
    photolib_record_to_discovery_payload,
)
from workers.noaa_adapter.rights import NO_COPYRIGHT_US_URI, classify_rights, is_allowed_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def flickr_fixture(name: str) -> dict:
    return flickr_record_to_discovery_payload(fixture_json(name))


def test_noaa_rights_allows_flickr_license_8_us_government_work() -> None:
    rights = classify_rights(flickr_fixture("flickr_photo_usgov_clean_noaa.json"))

    assert rights["decision"] == "ALLOWED"
    assert rights["allowed"] is True
    assert rights["rights_statement_uri"] == NO_COPYRIGHT_US_URI
    assert rights["rights_basis"] == "flickr_us_government_work"
    assert is_allowed_rights(flickr_fixture("flickr_photo_usgov_clean_noaa.json")) is True


def test_noaa_rights_allows_noaa_division_credit() -> None:
    rights = classify_rights(flickr_fixture("flickr_photo_noaa_division_credit.json"))

    assert rights["decision"] == "ALLOWED"
    assert rights["rights_basis"] == "flickr_us_government_work"

    photolib = photolib_record_to_discovery_payload(fixture_json("photolib_record_clean_noaa.json"))
    photolib_rights = classify_rights(photolib)
    assert photolib_rights["decision"] == "ALLOWED"
    assert photolib_rights["rights_basis"] == "noaa_federal_credit"


def test_noaa_rights_reviews_contributor_and_partner_markers() -> None:
    cases = (
        ("flickr_photo_university_review.json", "partner_or_contributor_marker"),
        ("flickr_photo_ngo_review.json", "partner_or_contributor_marker"),
        ("flickr_photo_foreign_agency_review.json", "partner_or_contributor_marker"),
        ("flickr_photo_contractor_review.json", "partner_or_contributor_marker"),
    )
    for name, basis in cases:
        rights = classify_rights(flickr_fixture(name))
        assert rights["decision"] == "REVIEW_REQUIRED"
        assert rights["allowed"] is False
        assert rights["rights_basis"] == basis


def test_noaa_rights_blocks_commercial_markers() -> None:
    cases = (
        ("flickr_photo_getty_blocked.json", "Getty"),
        ("flickr_photo_reuters_blocked.json", "Reuters"),
        ("flickr_photo_ap_blocked.json", "AP"),
    )
    for name, marker in cases:
        rights = classify_rights(flickr_fixture(name))
        assert rights["decision"] == "BLOCKED"
        assert rights["rights_basis"] == "blocked_partner_marker"
        assert marker in rights["blocked_markers"]


def test_noaa_rights_blocks_satellite_markers() -> None:
    rights = classify_rights(flickr_fixture("flickr_photo_satellite_blocked.json"))

    assert rights["decision"] == "BLOCKED"
    assert rights["rights_basis"] == "blocked_partner_marker"
    assert rights["blocked_markers"] == ["Maxar", "DigitalGlobe", "Planet", "GeoEye"]


def test_noaa_rights_blocks_license_zero_and_missing_evidence() -> None:
    license_zero = classify_rights(flickr_fixture("flickr_photo_all_rights_reserved_blocked.json"))
    missing = classify_rights(flickr_fixture("flickr_photo_missing_rights_blocked.json"))

    assert license_zero["decision"] == "BLOCKED"
    assert license_zero["rights_basis"] == "flickr_all_rights_reserved"
    assert missing["decision"] == "BLOCKED"
    assert missing["rights_basis"] == "missing_rights_evidence"
    assert classify_rights(None)["rights_basis"] == "missing_object"

