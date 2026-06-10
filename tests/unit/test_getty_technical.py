import json
from pathlib import Path

from workers.getty_adapter.normalize import normalize_record
from workers.getty_adapter.technical import (
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "getty"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_build_technical_metadata_includes_getty_evidence_fields() -> None:
    normalized = normalize_record(
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
    )

    content = build_technical_metadata(normalized, media_type_id="image")

    assert content["source"] == "getty"
    assert content["schema_standard"] == "getty_linked_art_v1"
    assert content["record_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert content["media_type_id"] == "image"
    assert content["quality_flag"] == "unknown_dimensions"
    assert validation_status(content) == "valid"
    assert content["getty_object_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert content["getty_rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert content["getty_manifest_uri"] == (
        "https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
    )
    assert content["getty_image_service"] == (
        "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
    )
    assert content["getty_accession_number"] == "90.PA.20"
    assert content["content_hash"]


def test_getty_technical_constants_are_stable() -> None:
    assert TECHNICAL_SCHEMA_VERSION == "getty-linked-art-technical-v1"
    assert VALIDATOR_NAME == "getty_adapter.technical"
    assert VALIDATOR_VERSION == "v1"

