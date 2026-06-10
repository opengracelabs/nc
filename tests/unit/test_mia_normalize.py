import json
from pathlib import Path

from workers.mia_adapter.normalize import (
    build_image_url,
    build_rights_evidence,
    build_source_record_uri,
    extract_object_id,
    iter_search_records,
    mandatory_field_warnings,
    normalize_record,
    normalize_records,
)
from workers.mia_adapter.rights import PUBLIC_DOMAIN_MARK_URI

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "mia"
REQUIRED_EVIDENCE_FIELDS = {
    "mia_object_id",
    "mia_rights_type",
    "mia_rights_uri",
    "mia_rights_image_display",
    "mia_image",
    "mia_public_access",
    "mia_restricted",
    "mia_primary_rendition_number",
    "mia_cache_location",
    "mia_image_width",
    "mia_image_height",
    "mia_accession_number",
    "mia_source_record_uri",
    "mia_image_url",
    "mia_iiif_manifest_url",
}


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_mia_identifier_source_and_image_url_helpers() -> None:
    record = fixture_json("object_public_domain_valid_image.json")

    assert extract_object_id(record) == "278"
    assert build_source_record_uri("278") == "https://collections.artsmia.org/art/278"
    assert build_image_url(record) == "https://5.api.artsmia.org/800/278.jpg"


def test_mia_image_url_uses_deterministic_sharded_800px_delivery_pattern() -> None:
    assert build_image_url({"id": 278}) == "https://5.api.artsmia.org/800/278.jpg"
    assert build_image_url({"id": 1013}) == "https://5.api.artsmia.org/800/1013.jpg"
    assert build_image_url({"id": "https://api.artsmia.org/objects/1003"}) == (
        "https://2.api.artsmia.org/800/1003.jpg"
    )
    assert build_image_url({"id": "not-numeric"}) is None


def test_mia_rights_evidence_contains_required_sprint2_fields() -> None:
    evidence = build_rights_evidence(fixture_json("object_public_domain_valid_image.json"))

    assert set(evidence) == REQUIRED_EVIDENCE_FIELDS
    assert evidence["mia_object_id"] == "278"
    assert evidence["mia_rights_type"] == "Public Domain"
    assert evidence["mia_rights_uri"] == PUBLIC_DOMAIN_MARK_URI
    assert evidence["mia_public_access"] == 1
    assert evidence["mia_restricted"] == 0
    assert evidence["mia_iiif_manifest_url"] is None


def test_mia_restricted_and_public_access_are_preserved_as_evidence_only() -> None:
    evidence = build_rights_evidence(fixture_json("object_restricted_zero_inc_edu.json"))

    assert evidence["mia_rights_type"] == "In Copyright–Educational Use"
    assert evidence["mia_restricted"] == 0
    assert evidence["mia_public_access"] == 1
    assert evidence["mia_rights_uri"] is None


def test_mia_normalize_record_emits_shared_shape_for_allowed_public_domain() -> None:
    normalized = normalize_record(fixture_json("object_public_domain_valid_image.json"))

    assert len(normalized) == 1
    item = normalized[0]
    assert item["record_id"] == "278"
    assert item["accession_num"] == "278.1"
    assert item["title"] == "Mia Fixture 278"
    assert item["rights_uri"] == PUBLIC_DOMAIN_MARK_URI
    assert item["rights_decision"] == "ALLOWED"
    assert item["rights_allowed"] is True
    assert item["provider"] == "Minneapolis Institute of Art"
    assert item["dataProvider"] == "Minneapolis Institute of Art"
    assert item["representative_media_url"] == "https://5.api.artsmia.org/800/278.jpg"
    assert item["preview_urls"] == [item["representative_media_url"]]
    assert item["width_px"] == 1200
    assert item["height_px"] == 900
    assert item["mia_metadata_license_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert mandatory_field_warnings(item) == []


def test_mia_normalize_record_emits_shared_shape_for_allowed_noc_us() -> None:
    normalized = normalize_record(fixture_json("object_noc_us_valid_image.json"))

    assert len(normalized) == 1
    item = normalized[0]
    assert item["record_id"] == "1013"
    assert item["mia_rights_type"] == "No Copyright–United States"
    assert item["rights_uri"] == "https://rightsstatements.org/vocab/NoC-US/1.0/"
    assert item["representative_media_url"] == "https://5.api.artsmia.org/800/1013.jpg"
    assert mandatory_field_warnings(item) == []


def test_mia_normalize_record_returns_no_candidate_for_blocked_rights() -> None:
    assert normalize_record(fixture_json("object_in_copyright.json")) == []
    assert normalize_record(fixture_json("object_restricted_zero_inc_edu.json")) == []


def test_mia_normalize_record_returns_no_candidate_for_missing_media_delivery() -> None:
    assert normalize_record(fixture_json("object_public_domain_missing_image.json")) == []


def test_mia_normalize_record_hash_is_replay_stable() -> None:
    left = normalize_record(fixture_json("object_public_domain_valid_image.json"))[0]
    right = normalize_record(fixture_json("object_public_domain_valid_image.json"))[0]

    assert left["raw_payload_hash"] == right["raw_payload_hash"]


def test_mia_search_payload_expansion_handles_hits_and_candidate_filtering() -> None:
    payload = fixture_json("search_mixed_rights_page.json")

    records = iter_search_records(payload)
    candidates = normalize_records(payload)

    assert [record["id"] for record in records] == [278, 1001, 1003, 279]
    assert [candidate["record_id"] for candidate in candidates] == ["278"]
