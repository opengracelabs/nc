import json
from pathlib import Path

from workers.nara_adapter.normalize import (
    build_rights_evidence,
    canonical_json_hash,
    extract_local_identifier,
    mandatory_field_warnings,
    normalize_record,
)
from workers.nara_adapter.rights import PUBLIC_DOMAIN_MARK_URI

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nara"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_build_rights_evidence_contains_required_nara_fields() -> None:
    record = fixture_json("record_unrestricted.json")
    normalized = normalize_record(record)

    evidence = build_rights_evidence(record, digital_object=None)

    assert evidence == {
        "nara_naid": "1667751",
        "nara_use_restriction": "Unrestricted",
        "nara_object_url": None,
        "nara_catalog_url": "https://catalog.archives.gov/id/1667751",
        "nara_local_identifier": "00303",
    }
    assert normalized[0]["nara_object_url"].endswith("00303_2003_001_AC.jpg")


def test_normalize_record_expands_each_still_image_object() -> None:
    record = fixture_json("record_unrestricted.json")
    normalized = normalize_record(record)

    assert len(normalized) == 2
    assert [item["record_id"] for item in normalized] == [
        "1667751:14721029",
        "1667751:14721030",
    ]
    first = normalized[0]
    assert first["rights_decision"] == "ALLOWED"
    assert first["rights_allowed"] is True
    assert first["rights_uri"] == PUBLIC_DOMAIN_MARK_URI
    assert first["source_url"] == "https://catalog.archives.gov/id/1667751"
    assert first["representative_media_url"].endswith("00303_2003_001_AC.jpg")
    assert first["preview_urls"] == [first["representative_media_url"]]
    assert first["nara_naid"] == "1667751"
    assert first["nara_use_restriction"] == "Unrestricted"
    assert first["nara_catalog_url"] == "https://catalog.archives.gov/id/1667751"
    assert first["nara_local_identifier"] == "00303"
    assert first["nara_object_id"] == "14721029"
    assert first["nara_object_type"] == "Image (JPG)"
    assert first["nara_object_filename"] == "00303_2003_001_AC.jpg"
    assert first["nara_object_file_size"] == 62296840
    assert first["raw_payload_hash"] == canonical_json_hash({"record": record})
    assert mandatory_field_warnings(first) == []


def test_normalize_record_preserves_blocked_decision_without_filtering_candidate() -> None:
    record = fixture_json("record_restricted.json")
    normalized = normalize_record(record)

    assert len(normalized) == 1
    assert normalized[0]["rights_decision"] == "BLOCKED"
    assert normalized[0]["rights_allowed"] is False
    assert normalized[0]["rights_uri"] is None
    assert normalized[0]["nara_use_restriction"] == "Restricted - Possibly Copyright"
    assert normalized[0]["nara_local_identifier"] is None


def test_normalize_missing_or_non_image_records_return_no_candidates() -> None:
    assert normalize_record({}) == []
    no_images = {
        "naId": 1,
        "title": "No images",
        "useRestriction": {"status": "Unrestricted"},
    }
    assert normalize_record(no_images) == []


def test_extract_local_identifier_accepts_list_and_missing_values() -> None:
    assert extract_local_identifier({"localIdentifier": ["", "ABC"]}) == "ABC"
    assert extract_local_identifier({}) is None
