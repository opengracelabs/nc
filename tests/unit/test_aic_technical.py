from pathlib import Path

from workers.aic_adapter.normalize import normalize_record
from workers.aic_adapter.technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path("tests/fixtures/aic")


def load_json(name: str) -> dict:
    import json

    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_aic_technical_constants_are_sprint3_values() -> None:
    assert TECHNICAL_SCHEMA_VERSION == "aic-technical-v1"
    assert VALIDATOR_NAME == "aic_adapter.technical"
    assert VALIDATOR_VERSION == "v1"
    assert SCHEMA_STANDARD == "aic_openaccess_v1"


def test_build_technical_metadata_reuses_shared_visual_contract_with_aic_fields() -> None:
    normalized = normalize_record(load_json("artwork_seurat_public_domain.json"))

    content = build_technical_metadata(normalized, media_type_id="image")

    assert content["source"] == "aic"
    assert content["schema_standard"] == "aic_openaccess_v1"
    assert content["record_id"] == "27992"
    assert content["media_type_id"] == "image"
    assert content["quality_flag"] == "unknown_dimensions"
    assert content["rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert content["aic_image_id"] == "12345678-aaaa-bbbb-cccc-123456789abc"
    assert content["aic_manifest_url"] == (
        "https://api.artic.edu/api/v1/artworks/27992/manifest.json"
    )
    assert content["aic_is_public_domain"] is True
    assert content["place_of_origin"] == "France"
    assert content["department"] == "Painting and Sculpture of Europe"
    assert content["accession_number"] == "1926.224"
    assert len(content["content_hash"]) == 64
    assert validation_status(content) == "valid"

