import json
from pathlib import Path

from workers.smk_adapter.normalize import normalize_record
from workers.smk_adapter.technical import (
    SCHEMA_STANDARD,
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path("tests/fixtures/smk")


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_build_technical_metadata_includes_smk_fields_for_asset_zero() -> None:
    normalized = normalize_record(load_json("object_kms3696_public_domain.json"))

    content = build_technical_metadata(normalized, media_type_id="image")

    assert content["source"] == "smk"
    assert content["schema_standard"] == SCHEMA_STANDARD
    assert content["record_id"] == "KMS3696"
    assert content["smk_public_domain"] is True
    assert content["smk_manifest_url"] == "https://api.smk.dk/api/v1/iiif/manifest?id=KMS3696"
    assert content["smk_image_rights"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert content["smk_object_number"] == "KMS3696"
    assert content["width_px"] == 23311
    assert content["height_px"] == 20467
    assert content["quality_flag"] == "meets_minimum"
    assert content["content_hash"]
    assert validation_status(content) == "valid"
    assert TECHNICAL_SCHEMA_VERSION == "smk-technical-v1"
    assert VALIDATOR_NAME == "smk_adapter.technical"
