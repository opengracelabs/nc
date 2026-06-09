import json
from pathlib import Path

from workers.cma_adapter.normalize import normalize_record
from workers.cma_adapter.technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path("tests/fixtures/cma")


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_build_technical_metadata_includes_cma_evidence_fields() -> None:
    normalized = normalize_record(load_json("artwork_cloudy_mountains_cc0.json"))

    content = build_technical_metadata(normalized, media_type_id="image")

    assert content["source"] == "cma"
    assert content["schema_standard"] == SCHEMA_STANDARD
    assert content["record_id"] == "113945"
    assert content["media_type_id"] == "image"
    assert content["quality_flag"] == "meets_minimum"
    assert validation_status(content) == "valid"
    assert content["cma_share_license_status"] == "CC0"
    assert content["cma_copyright"] is None
    assert content["cma_image_web_url"].endswith("1933.220_web.jpg")
    assert content["cma_image_print_url"].endswith("1933.220_print.jpg")
    assert content["cma_image_full_url"].endswith("1933.220_full.tif")
    assert content["accession_number"] == "1933.220"
    assert content["content_hash"]


def test_cma_technical_constants_are_stable() -> None:
    assert TECHNICAL_SCHEMA_VERSION == "cma-technical-v1"
    assert VALIDATOR_NAME == "cma_adapter.technical"
    assert VALIDATOR_VERSION == "v1"
    assert SCHEMA_STANDARD == "cma_openaccess_v1"
