import json
from pathlib import Path

from workers.yale_adapter.normalize import normalize_record
from workers.yale_adapter.technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "yale"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_build_technical_metadata_includes_yale_evidence_fields() -> None:
    normalized = normalize_record(
        fixture_json("ycba_object_cc0.json"),
        manifest=fixture_json("manifest_ycba_12345_v3.json"),
    )

    content = build_technical_metadata(normalized, media_type_id="image")

    assert content["source"] == "ycba"
    assert content["schema_standard"] == SCHEMA_STANDARD
    assert content["record_id"] == "12345"
    assert content["media_type_id"] == "image"
    assert content["quality_flag"] == "unknown_dimensions"
    assert validation_status(content) == "valid"
    assert content["yale_object_id"] == "12345"
    assert content["yale_rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert content["yale_collection"] == "Yale Center for British Art"
    assert content["yale_iiif_manifest"] == "https://manifests.collections.yale.edu/ycba/obj/12345"
    assert content["yale_image_service"] == "https://media.collections.yale.edu/iiif/2/ycba-12345"
    assert content["ycba_rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert content["ycba_attribution"] == "Yale Center for British Art"
    assert content["yuag_rights_uri"] is None
    assert content["content_hash"]


def test_yale_technical_constants_are_stable() -> None:
    assert TECHNICAL_SCHEMA_VERSION == "yale-lux-technical-v1"
    assert VALIDATOR_NAME == "yale_adapter.technical"
    assert VALIDATOR_VERSION == "v1"
    assert SCHEMA_STANDARD == "yale_lux_linked_art_v1"
