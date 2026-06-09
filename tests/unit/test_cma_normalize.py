import json
from pathlib import Path

from workers.cma_adapter.normalize import (
    build_collection_url,
    canonical_json_hash,
    extract_record_id,
    mandatory_field_warnings,
    normalize_record,
    representative_media_url,
)
from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

FIXTURES = Path("tests/fixtures/cma")


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_normalize_record_maps_cma_cc0_object() -> None:
    raw = load("artwork_94979_cc0.json")
    normalized = normalize_record(raw)

    assert normalized["record_id"] == "94979"
    assert normalized["title"] == "Nathaniel Hurd"
    assert normalized["rights_uri"] == CC0_URI
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True
    assert normalized["cma_share_license_status"] == "CC0"
    assert normalized["cma_copyright"] is None
    assert normalized["accession_number"] == "1915.534"
    assert normalized["source_url"] == "https://clevelandart.org/art/1915.534"
    assert normalized["representative_media_url"] == normalized["cma_image_print_url"]
    assert normalized["cma_image_web_url"].endswith("_web.jpg")
    assert normalized["cma_image_print_url"].endswith("_print.jpg")
    assert normalized["cma_image_full_url"].endswith("_full.tif")
    assert normalized["width_px"] == 2849
    assert normalized["height_px"] == 3400
    assert normalized["raw_payload_hash"] == canonical_json_hash(raw)
    assert mandatory_field_warnings(normalized) == []


def test_normalize_record_falls_back_to_web_representative_image() -> None:
    raw = load("artwork_94979_cc0.json")
    raw["data"]["images"]["print"]["url"] = ""

    normalized = normalize_record(raw)

    assert normalized["representative_media_url"] == normalized["cma_image_web_url"]
    assert representative_media_url(raw["data"]) == normalized["cma_image_web_url"]


def test_normalize_record_reports_blocked_rights() -> None:
    normalized = normalize_record(load("artwork_cc0_no_web_image.json"))

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["rights_uri"] is None
    assert normalized["cma_rights_basis"] == "no_image_url"
    assert "missing_rights_uri" in mandatory_field_warnings(normalized)
    assert "missing_representative_media_url" in mandatory_field_warnings(normalized)


def test_helpers_extract_record_id_and_collection_url() -> None:
    raw = load("artwork_94979_cc0.json")

    assert extract_record_id(raw) == "94979"
    assert build_collection_url("1915.534") == "https://clevelandart.org/art/1915.534"



def test_normalize_record_alternate_images_use_print_then_web_then_skip() -> None:
    raw = load("artwork_94979_cc0.json")
    raw["data"]["alternate_images"] = [
        {
            "print": {"url": "https://example.test/alt-print.jpg"},
            "web": {"url": "https://example.test/alt-web.jpg"},
        },
        {"print": {"url": ""}, "web": {"url": "https://example.test/alt-web-only.jpg"}},
        {"print": {"url": ""}, "web": {"url": ""}},
    ]

    normalized = normalize_record(raw)

    assert normalized["additional_images"] == [
        "https://example.test/alt-print.jpg",
        "https://example.test/alt-web-only.jpg",
    ]
