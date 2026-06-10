import json
from pathlib import Path

from workers.yale_adapter.client import CC0_URI
from workers.yale_adapter.normalize import (
    build_rights_evidence,
    canonical_json_hash,
    extract_collection,
    extract_image_service,
    extract_manifest_url,
    extract_title,
    mandatory_field_warnings,
    normalize_record,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "yale"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_extract_title_collection_manifest_and_image_service() -> None:
    record = fixture_json("ycba_object_cc0.json")
    manifest = fixture_json("manifest_ycba_12345_v3.json")

    assert extract_title(record) == "A View of Snowdon"
    assert extract_collection(record) == "Yale Center for British Art"
    assert extract_manifest_url(record) == "https://manifests.collections.yale.edu/ycba/obj/12345"
    assert extract_image_service(manifest) == "https://media.collections.yale.edu/iiif/2/ycba-12345"


def test_build_rights_evidence_has_required_yale_fields() -> None:
    record = fixture_json("ycba_object_cc0.json")
    manifest = fixture_json("manifest_ycba_12345_v3.json")

    evidence = build_rights_evidence(record, manifest=manifest)

    assert evidence["ycba_subject_to_uri"] == CC0_URI
    assert evidence["ycba_record_id"] == "https://lux.collections.yale.edu/data/object/ycba-obj-12345"
    assert evidence["ycba_object_id"] == "12345"
    assert evidence["ycba_iiif_manifest"] == "https://manifests.collections.yale.edu/ycba/obj/12345"
    assert evidence["ycba_attribution"] == "Yale Center for British Art"
    assert evidence["yale_object_id"] == "12345"
    assert evidence["yale_rights_uri"] == CC0_URI
    assert evidence["yale_collection"] == "Yale Center for British Art"
    assert evidence["yale_iiif_manifest"] == "https://manifests.collections.yale.edu/ycba/obj/12345"
    assert evidence["yale_image_service"] == "https://media.collections.yale.edu/iiif/2/ycba-12345"


def test_normalize_allowed_record_includes_rights_and_media_evidence() -> None:
    record = fixture_json("ycba_object_cc0.json")
    manifest = fixture_json("manifest_ycba_12345_v3.json")

    normalized = normalize_record(record, manifest=manifest)

    assert normalized["record_id"] == "12345"
    assert normalized["title"] == "A View of Snowdon"
    assert normalized["rights_decision"] == "ALLOWED"
    assert normalized["rights_allowed"] is True
    assert normalized["rights_uri"] == CC0_URI
    assert normalized["yale_rights_basis"] == "ycba_cc0"
    assert normalized["yale_source_slug"] == "ycba"
    assert normalized["yale_object_id"] == "12345"
    assert normalized["ycba_subject_to_uri"] == CC0_URI
    assert normalized["ycba_object_id"] == "12345"
    assert normalized["ycba_iiif_manifest"] == (
        "https://manifests.collections.yale.edu/ycba/obj/12345"
    )
    assert normalized["ycba_attribution"] == "Yale Center for British Art"
    assert normalized["yale_image_service"] == (
        "https://media.collections.yale.edu/iiif/2/ycba-12345"
    )
    assert normalized["representative_media_url"] == (
        "https://media.collections.yale.edu/iiif/2/ycba-12345/full/!1024,1024/0/default.jpg"
    )
    assert mandatory_field_warnings(normalized) == []


def test_normalize_blocked_record_preserves_evidence_without_representative_media() -> None:
    normalized = normalize_record(fixture_json("ycba_object_restricted.json"))

    assert normalized["rights_decision"] == "BLOCKED"
    assert normalized["rights_allowed"] is False
    assert normalized["rights_uri"] == "https://rightsstatements.org/vocab/UND/1.0/"
    assert normalized["yale_rights_basis"] == "unknown_rights_uri"
    assert normalized["yale_image_service"] is None
    assert "missing_representative_media_url" in mandatory_field_warnings(normalized)


def test_canonical_json_hash_is_stable() -> None:
    left = canonical_json_hash({"b": 2, "a": 1})
    right = canonical_json_hash({"a": 1, "b": 2})

    assert left == right
    assert len(left) == 64

