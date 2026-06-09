from pathlib import Path

from workers.met_adapter.normalize import (
    canonical_json_hash,
    extract_record_id,
    mandatory_field_warnings,
    normalize_record,
)
from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

FIXTURES = Path("tests/fixtures/met")


def load_json(name: str) -> dict:
    import json

    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_normalize_record_extracts_met_sprint_2_fields() -> None:
    normalized = normalize_record(load_json("object_hokusai_public_domain.json"))

    assert normalized["record_id"] == "45434"
    assert normalized["title"] == "The Great Wave off Kanagawa"
    assert normalized["description"] == "Print"
    assert normalized["date"] == "ca. 1830-32"
    assert normalized["creator"] == "Katsushika Hokusai"
    assert normalized["rights_uri"] == CC0_URI
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True
    assert normalized["met_is_public_domain"] is True
    assert normalized["primary_image"].startswith("https://images.metmuseum.org/")
    assert normalized["additional_images"] == [
        "https://images.metmuseum.org/CRDImages/as/original/DP130156.jpg"
    ]
    assert normalized["preview_urls"] == [
        "https://images.metmuseum.org/CRDImages/as/original/DP130155.jpg",
        "https://images.metmuseum.org/CRDImages/as/original/DP130156.jpg",
    ]
    assert normalized["subject_terms"] == ["Waves", "Mount Fuji"]
    assert normalized["country"] == "Japan"
    assert normalized["artist_wikidata_url"] == "https://www.wikidata.org/wiki/Q5586"


def test_normalize_record_blocks_false_public_domain_flag() -> None:
    normalized = normalize_record(load_json("object_not_public_domain.json"))

    assert normalized["record_id"] == "90001"
    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["rights_uri"] is None
    assert normalized["met_rights_basis"] == "not_public_domain"


def test_normalize_record_blocks_missing_rights_field() -> None:
    normalized = normalize_record(load_json("object_missing_rights_field.json"))

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["met_rights_basis"] == "missing_rights_field"
    assert normalized["met_is_public_domain"] is None


def test_normalize_record_blocks_public_domain_without_primary_image() -> None:
    normalized = normalize_record(load_json("object_public_domain_no_image.json"))

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["met_rights_basis"] == "no_image_url"
    assert normalized["representative_media_url"] is None


def test_mandatory_field_warnings_report_blocked_media_gaps() -> None:
    normalized = normalize_record(load_json("object_public_domain_no_image.json"))

    assert mandatory_field_warnings(normalized) == [
        "missing_rights_uri",
        "missing_representative_media_url",
    ]


def test_record_id_and_hash_are_stable() -> None:
    left = load_json("object_hokusai_public_domain.json")
    right = dict(reversed(list(left.items())))

    assert extract_record_id(left) == "45434"
    assert canonical_json_hash(left) == canonical_json_hash(right)
    assert normalize_record(left)["raw_payload_hash"] == normalize_record(right)["raw_payload_hash"]

