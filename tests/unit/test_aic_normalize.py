from pathlib import Path

from workers.aic_adapter.normalize import (
    build_iiif_image_url,
    canonical_json_hash,
    extract_record_id,
    mandatory_field_warnings,
    normalize_record,
)
from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

FIXTURES = Path("tests/fixtures/aic")


def load_json(name: str) -> dict:
    import json

    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_build_iiif_image_url_constructs_aic_delivery_url() -> None:
    assert build_iiif_image_url(" image-id ") == (
        "https://www.artic.edu/iiif/2/image-id/full/843,/0/default.jpg"
    )
    assert build_iiif_image_url("image-id", size="full") == (
        "https://www.artic.edu/iiif/2/image-id/full/full/0/default.jpg"
    )
    assert build_iiif_image_url(None) is None


def test_normalize_record_extracts_aic_sprint_2_fields() -> None:
    normalized = normalize_record(load_json("artwork_seurat_public_domain.json"))

    assert normalized["record_id"] == "27992"
    assert normalized["title"] == "A Sunday on La Grande Jatte -- 1884"
    assert normalized["description"] == "painting"
    assert normalized["date"] == "1884-86"
    assert normalized["creator"] == "Georges Seurat\\nFrench, 1859-1891"
    assert normalized["rights_uri"] == CC0_URI
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True
    assert normalized["aic_is_public_domain"] is True
    assert normalized["aic_image_id"] == "12345678-aaaa-bbbb-cccc-123456789abc"
    assert normalized["representative_media_url"] == (
        "https://www.artic.edu/iiif/2/"
        "12345678-aaaa-bbbb-cccc-123456789abc/full/843,/0/default.jpg"
    )
    assert normalized["additional_images"] == [
        "https://www.artic.edu/iiif/2/"
        "22222222-aaaa-bbbb-cccc-123456789abc/full/843,/0/default.jpg"
    ]
    assert normalized["preview_urls"] == [
        "https://www.artic.edu/iiif/2/"
        "12345678-aaaa-bbbb-cccc-123456789abc/full/843,/0/default.jpg",
        "https://www.artic.edu/iiif/2/"
        "22222222-aaaa-bbbb-cccc-123456789abc/full/843,/0/default.jpg",
    ]
    assert normalized["source_url"] == "https://www.artic.edu/artworks/27992"
    assert normalized["aic_manifest_url"] == (
        "https://api.artic.edu/api/v1/artworks/27992/manifest.json"
    )
    assert normalized["subject_terms"] == ["France", "Leisure"]
    assert normalized["place_of_origin"] == "France"
    assert normalized["accession_number"] == "1926.224"


def test_normalize_record_accepts_top_level_artwork_shape() -> None:
    payload = load_json("artwork_seurat_public_domain.json")["data"]

    assert normalize_record(payload)["record_id"] == "27992"


def test_normalize_record_blocks_false_public_domain_flag() -> None:
    normalized = normalize_record(load_json("artwork_not_public_domain.json"))

    assert normalized["record_id"] == "90001"
    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["rights_uri"] is None
    assert normalized["aic_rights_basis"] == "not_public_domain"


def test_normalize_record_blocks_missing_rights_field() -> None:
    normalized = normalize_record(load_json("artwork_missing_rights_field.json"))

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["aic_rights_basis"] == "missing_rights_field"
    assert normalized["aic_is_public_domain"] is None


def test_normalize_record_blocks_public_domain_without_image_id() -> None:
    normalized = normalize_record(load_json("artwork_public_domain_no_image_id.json"))

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["aic_rights_basis"] == "no_image_id"
    assert normalized["representative_media_url"] is None


def test_mandatory_field_warnings_report_blocked_media_gaps() -> None:
    normalized = normalize_record(load_json("artwork_public_domain_no_image_id.json"))

    assert mandatory_field_warnings(normalized) == [
        "missing_rights_uri",
        "missing_representative_media_url",
    ]


def test_record_id_and_hash_are_stable() -> None:
    left = load_json("artwork_seurat_public_domain.json")
    right = {"data": dict(reversed(list(left["data"].items())))}

    assert extract_record_id(left) == "27992"
    assert canonical_json_hash(left) == canonical_json_hash(right)
    assert normalize_record(left)["raw_payload_hash"] == normalize_record(right)["raw_payload_hash"]

