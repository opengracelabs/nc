import json
from pathlib import Path

from workers.getty_adapter.client import CC0_URI
from workers.getty_adapter.normalize import (
    build_iiif_image_url,
    build_rights_evidence,
    extract_accession_number,
    extract_object_id,
    extract_title,
    mandatory_field_warnings,
    normalize_record,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "getty"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_getty_identifier_title_and_accession_extraction() -> None:
    record = fixture_json("object_cc0.json")

    assert extract_object_id(record) == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert extract_title(record) == "Irises"
    assert extract_accession_number(record) == "90.PA.20"


def test_getty_rights_evidence_contains_required_sprint2_fields() -> None:
    evidence = build_rights_evidence(
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
    )

    assert evidence == {
        "getty_object_id": "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb",
        "getty_rights_uri": CC0_URI,
        "getty_image_service": (
            "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
        ),
        "getty_manifest_uri": (
            "https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
        ),
        "getty_accession_number": "90.PA.20",
    }


def test_getty_normalize_record_emits_shared_shape_and_getty_evidence() -> None:
    normalized = normalize_record(
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
    )

    assert normalized["record_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert normalized["accession_num"] == "90.PA.20"
    assert normalized["title"] == "Irises"
    assert normalized["rights_uri"] == CC0_URI
    assert normalized["rights_decision"] == "ALLOWED"
    assert normalized["rights_allowed"] is True
    assert normalized["provider"] == "J. Paul Getty Museum"
    assert normalized["dataProvider"] == "J. Paul Getty Museum"
    assert normalized["source_url"] == (
        "https://data.getty.edu/museum/collection/object/"
        "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    )
    assert normalized["representative_media_url"] == (
        "https://media.getty.edu/iiif/image/"
        "7ff0a543-569a-4cb0-b92b-cd78877d4141/full/!1024,1024/0/default.jpg"
    )
    assert normalized["preview_urls"] == [normalized["representative_media_url"]]
    assert normalized["getty_rights_basis"] == "getty_cc0"
    assert normalized["getty_rights_policy_id"] == "getty_rights_matrix_v1"
    assert normalized["getty_schema_standard"] == "getty_linked_art_v1"
    assert mandatory_field_warnings(normalized) == []


def test_getty_normalize_record_preserves_blocked_rights_without_image_evidence() -> None:
    normalized = normalize_record(fixture_json("object_unknown_rights.json"))

    assert normalized["rights_decision"] == "BLOCKED"
    assert normalized["rights_allowed"] is False
    assert normalized["getty_rights_basis"] == "unknown_rights_uri"
    assert normalized["getty_rights_uri"] == "https://rightsstatements.org/vocab/InC/1.0/"
    assert normalized["getty_image_service"] is None
    assert normalized["getty_manifest_uri"] is None
    assert "missing_representative_media_url" in mandatory_field_warnings(normalized)


def test_getty_normalize_record_hash_is_replay_stable() -> None:
    left = normalize_record(
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
    )
    right = normalize_record(
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
    )

    assert left["raw_payload_hash"] == right["raw_payload_hash"]


def test_getty_build_iiif_image_url_rejects_blank_service() -> None:
    assert build_iiif_image_url("https://media.getty.edu/iiif/image/test", size="max") == (
        "https://media.getty.edu/iiif/image/test/full/max/0/default.jpg"
    )
    try:
        build_iiif_image_url("")
    except ValueError as exc:
        assert str(exc) == "missing_iiif_service"
    else:
        raise AssertionError("blank service accepted")

