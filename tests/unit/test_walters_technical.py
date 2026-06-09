from pathlib import Path

from workers.walters_adapter.client import load_dataset
from workers.walters_adapter.normalize import normalize_dataset_record
from workers.walters_adapter.technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path("tests/fixtures/walters")


def test_build_technical_metadata_includes_walters_evidence_fields() -> None:
    normalized = normalize_dataset_record(load_dataset(FIXTURES), "1001")

    content = build_technical_metadata(normalized, media_type_id="image")

    assert content["source"] == "walters"
    assert content["schema_standard"] == SCHEMA_STANDARD
    assert content["record_id"] == "1001"
    assert content["media_type_id"] == "image"
    assert content["quality_flag"] == "unknown_dimensions"
    assert validation_status(content) == "valid"
    assert content["walters_object_id"] == "1001"
    assert content["walters_object_number"] == "W.174"
    assert content["walters_image_url"] == "https://art.thewalters.org/images/raw/W174_fnt.jpg"
    assert content["walters_media_xref_id"] == "2001"
    assert content["walters_is_primary"] == "1"
    assert content["walters_collection_ids"] == ["MAN", "MED"]
    assert content["walters_collection_names"] == ["Manuscripts", "Medieval"]
    assert content["content_hash"]


def test_walters_technical_constants_are_stable() -> None:
    assert TECHNICAL_SCHEMA_VERSION == "walters-technical-v1"
    assert VALIDATOR_NAME == "walters_adapter.technical"
    assert VALIDATOR_VERSION == "v1"
    assert SCHEMA_STANDARD == "walters_opendata_v1"
