from pathlib import Path

from workers.nga_adapter.client import load_dataset
from workers.nga_adapter.normalize import normalize_dataset_record
from workers.nga_adapter.technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path("tests/fixtures/nga")


def test_build_technical_metadata_includes_nga_evidence_fields() -> None:
    normalized = normalize_dataset_record(load_dataset(FIXTURES), "2001")

    content = build_technical_metadata(normalized, media_type_id="image")

    assert content["source"] == "nga"
    assert content["schema_standard"] == SCHEMA_STANDARD
    assert content["record_id"] == "2001"
    assert content["media_type_id"] == "image"
    assert content["quality_flag"] == "meets_minimum"
    assert validation_status(content) == "valid"
    assert content["nga_openaccess"] == "1"
    assert content["nga_image_uuid"] == "img-primary-2001"
    assert content["nga_iiifurl"] == "https://api.nga.gov/iiif/img-primary-2001"
    assert content["nga_iiif_thumb_url"].endswith("/full/200,200/0/default.jpg")
    assert content["nga_viewtype"] == "primary"
    assert content["nga_objectid"] == "2001"
    assert content["nga_accessionnum"] == "1942.9.97"
    assert content["school"] == "French"
    assert content["place_executed"] == "France"
    assert content["creator_nationality"] == "French"
    assert content["content_hash"]


def test_nga_technical_constants_are_stable() -> None:
    assert TECHNICAL_SCHEMA_VERSION == "nga-technical-v1"
    assert VALIDATOR_NAME == "nga_adapter.technical"
    assert VALIDATOR_VERSION == "v1"
    assert SCHEMA_STANDARD == "nga_openaccess_v1"
