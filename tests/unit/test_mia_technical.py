import json
from pathlib import Path

from workers.mia_adapter.normalize import normalize_record
from workers.mia_adapter.technical import (
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "mia"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_build_technical_metadata_includes_mia_evidence_fields() -> None:
    normalized = normalize_record(fixture_json("object_public_domain_valid_image.json"))[0]

    content = build_technical_metadata(normalized, media_type_id="image")

    assert content["source"] == "mia"
    assert content["schema_standard"] == "mia_collection_json_v1"
    assert content["record_id"] == "278"
    assert content["media_type_id"] == "image"
    assert content["quality_flag"] == "meets_minimum"
    assert validation_status(content) == "valid"
    assert content["mia_object_id"] == "278"
    assert content["mia_rights_type"] == "Public Domain"
    assert content["mia_rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert content["mia_rights_image_display"] == "Full"
    assert content["mia_image"] == "valid"
    assert content["mia_public_access"] == 1
    assert content["mia_restricted"] == 0
    assert content["mia_primary_rendition_number"] == "mia_278.jpg"
    assert content["mia_cache_location"] == "000278\\000\\00\\278"
    assert content["mia_image_width"] == 1200
    assert content["mia_image_height"] == 900
    assert content["mia_accession_number"] == "278.1"
    assert content["mia_source_record_uri"] == "https://collections.artsmia.org/art/278"
    assert content["mia_image_url"] == "https://5.api.artsmia.org/800/278.jpg"
    assert content["mia_iiif_manifest_url"] is None
    assert content["content_hash"]


def test_mia_technical_constants_are_stable() -> None:
    assert TECHNICAL_SCHEMA_VERSION == "mia-collection-technical-v1"
    assert VALIDATOR_NAME == "mia_adapter.technical"
    assert VALIDATOR_VERSION == "v1"
