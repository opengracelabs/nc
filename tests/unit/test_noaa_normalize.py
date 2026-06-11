import json
from pathlib import Path

from workers.noaa_adapter.client import (
    flickr_record_to_discovery_payload,
    photolib_record_to_discovery_payload,
)
from workers.noaa_adapter.normalize import (
    REQUIRED_EVIDENCE_FIELDS,
    build_rights_evidence,
    mandatory_evidence_warnings,
    normalize_flickr_search_payload,
    normalize_record,
)
from workers.noaa_adapter.rights import NO_COPYRIGHT_US_URI

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"
RETRIEVED_AT = "2026-06-11T00:00:00Z"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def flickr_fixture(name: str) -> dict:
    return flickr_record_to_discovery_payload(fixture_json(name))


def test_noaa_normalize_allowed_flickr_record_preserves_required_evidence() -> None:
    normalized = normalize_record(
        flickr_fixture("flickr_photo_usgov_clean_noaa.json"),
        retrieved_at=RETRIEVED_AT,
    )

    assert len(normalized) == 1
    item = normalized[0]
    assert item["record_id"] == "1001"
    assert item["source_slug"] == "noaa"
    assert item["source_system"] == "flickr"
    assert item["image_url"].endswith("1001_clean_o.jpg")
    assert item["rights_uri"] == NO_COPYRIGHT_US_URI
    assert item["rights_decision"] == "ALLOWED"
    assert item["rights_basis"] == "flickr_us_government_work"
    assert item["credit"] == "NOAA/NOS"
    assert item["retrieved_at"] == RETRIEVED_AT
    assert mandatory_evidence_warnings(item) == []
    assert set(REQUIRED_EVIDENCE_FIELDS).issubset(item)


def test_noaa_normalize_review_and_blocked_records_emit_no_candidates() -> None:
    assert normalize_record(
        flickr_fixture("flickr_photo_personal_noaa_review.json"),
        retrieved_at=RETRIEVED_AT,
    ) == []
    assert normalize_record(
        flickr_fixture("flickr_photo_getty_blocked.json"),
        retrieved_at=RETRIEVED_AT,
    ) == []


def test_noaa_rights_evidence_preserves_markers_and_hash() -> None:
    evidence = build_rights_evidence(
        flickr_fixture("flickr_photo_personal_noaa_review.json"),
        retrieved_at=RETRIEVED_AT,
    )

    assert evidence["rights_decision"] == "BLOCKED"
    assert evidence["rights_basis"] == "personal_name_noaa_credit"
    assert evidence["contributor_markers"] == ["Jane Smith/NOAA"]
    assert evidence["partner_markers"] == []
    assert len(evidence["raw_payload_hash"]) == 64
    assert mandatory_evidence_warnings(evidence) == []


def test_noaa_normalize_flickr_search_payload_only_allows_clean_records() -> None:
    candidates = normalize_flickr_search_payload(
        fixture_json("flickr_search_page_mixed.json"),
        retrieved_at=RETRIEVED_AT,
    )

    assert [candidate["record_id"] for candidate in candidates] == ["1001"]
    assert candidates[0]["source_url"] == "https://www.flickr.com/photos/usoceangov/1001"


def test_noaa_normalize_photolib_record_uses_credit_gate() -> None:
    normalized = normalize_record(
        photolib_record_to_discovery_payload(fixture_json("photolib_record_clean_noaa.json")),
        retrieved_at=RETRIEVED_AT,
    )

    assert len(normalized) == 1
    assert normalized[0]["source_system"] == "noaa_photolib"
    assert normalized[0]["rights_basis"] == "noaa_federal_credit"

