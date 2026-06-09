from pathlib import Path

from workers.met_adapter.normalize import normalize_record
from workers.met_adapter.technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path("tests/fixtures/met")


def load_json(name: str) -> dict:
    import json

    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_met_technical_constants_are_sprint3_values() -> None:
    assert TECHNICAL_SCHEMA_VERSION == "met-technical-v1"
    assert VALIDATOR_NAME == "met_adapter.technical"
    assert VALIDATOR_VERSION == "v1"
    assert SCHEMA_STANDARD == "met_openaccess_v1"


def test_build_technical_metadata_reuses_shared_visual_contract_with_met_fields() -> None:
    normalized = normalize_record(load_json("object_hokusai_public_domain.json"))

    content = build_technical_metadata(normalized, media_type_id="image")

    assert content["source"] == "met"
    assert content["schema_standard"] == "met_openaccess_v1"
    assert content["record_id"] == "45434"
    assert content["media_type_id"] == "image"
    assert content["quality_flag"] == "unknown_dimensions"
    assert content["rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert content["met_object_id"] == "45434"
    assert content["met_is_public_domain"] is True
    assert content["primary_image"].startswith("https://images.metmuseum.org/")
    assert content["additional_images"] == [
        "https://images.metmuseum.org/CRDImages/as/original/DP130156.jpg"
    ]
    assert content["department"] == "Asian Art"
    assert content["country"] == "Japan"
    assert len(content["content_hash"]) == 64
    assert validation_status(content) == "valid"

