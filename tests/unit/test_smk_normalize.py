import json
from pathlib import Path

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision
from workers.smk_adapter.normalize import (
    build_collection_url,
    canonical_json_hash,
    extract_record_id,
    mandatory_field_warnings,
    normalize_record,
)

FIXTURES = Path("tests/fixtures/smk")


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_normalize_record_maps_smk_public_domain_object() -> None:
    raw = load("object_kms1_public_domain.json")
    normalized = normalize_record(raw)

    assert normalized["record_id"] == "KMS1"
    assert normalized["title"] == "The Fall of the Titans"
    assert normalized["creator"] == "Cornelis Cornelisz. van Haarlem"
    assert normalized["rights_uri"] == CC0_URI
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True
    assert normalized["smk_public_domain"] is True
    assert normalized["smk_image_rights"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert normalized["subject_terms"] == ["Titans", "Greek mythology"]
    assert normalized["smk_rights_basis"] == "smk_public_domain"
    assert normalized["smk_object_number"] == "KMS1"
    assert normalized["smk_image_native"].startswith("https://api.smk.dk/api/v1/download/")
    assert normalized["smk_image_iiif_id"].startswith("https://iip.smk.dk/iiif/")
    assert normalized["smk_manifest_url"] == (
        "https://api.smk.dk/api/v1/iiif/manifest?id=KMS1"
    )
    assert normalized["source_url"] == normalized["frontend_url"]
    assert normalized["representative_media_url"] == normalized["smk_image_native"]
    assert normalized["preview_urls"][0] == normalized["representative_media_url"]
    assert normalized["raw_payload_hash"] == canonical_json_hash(raw)
    assert mandatory_field_warnings(normalized) == []


def test_normalize_record_falls_back_to_iiif_image_and_constructed_manifest() -> None:
    raw = load("object_kms1_public_domain.json")
    record = raw["items"][0]
    record["image_native"] = ""
    record["iiif_manifest"] = ""

    normalized = normalize_record(raw)

    assert normalized["representative_media_url"] == record["images"][0]["url"]
    assert normalized["smk_manifest_url"] == (
        "https://api.smk.dk/api/v1/iiif/manifest?object_number=KMS1"
    )


def test_normalize_record_reports_blocked_rights() -> None:
    normalized = normalize_record(load("object_public_domain_no_image.json"))

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["rights_uri"] is None
    assert normalized["smk_rights_basis"] == "no_image_url"
    assert "missing_rights_uri" in mandatory_field_warnings(normalized)
    assert "missing_representative_media_url" in mandatory_field_warnings(normalized)


def test_helpers_extract_wrapped_record_id_and_collection_url() -> None:
    raw = load("object_kms1_public_domain.json")
    record = raw["items"][0]

    assert extract_record_id(raw) == "KMS1"
    assert build_collection_url(record) == record["frontend_url"]



def test_normalize_record_does_not_use_image_iiif_id_as_representative_fallback() -> None:
    raw = load("object_kms1_public_domain.json")
    record = raw["items"][0]
    record["image_native"] = ""
    record["images"] = []

    normalized = normalize_record(raw)

    assert normalized["representative_media_url"] is None
    assert normalized["smk_image_iiif_id"].startswith("https://iip.smk.dk/iiif/")
