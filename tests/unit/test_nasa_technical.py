import json
from pathlib import Path

from workers.nasa_adapter.normalize import normalize_record
from workers.nasa_adapter.technical import (
    NASA_EVIDENCE_FIELDS,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nasa"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_nasa_technical_metadata_carries_sprint2_evidence() -> None:
    normalized = normalize_record(
        fixture_json("record_nasa_federal_image.json"),
        asset_manifest=fixture_json("asset_gsfc_20171208_archive_manifest.json"),
    )[0]

    content = build_technical_metadata(normalized, media_type_id="image")

    assert validation_status(content) == "valid"
    assert content["source"] == "nasa_images"
    assert content["schema_standard"] == "nasa_images_collection_json_v1"
    assert content["nasa_id"] == "GSFC_20171208_ARCHIVE"
    assert content["nasa_rights_basis"] == "federal_center_clean_rights"
    assert content["nasa_publicity_risk_detected"] is False
    assert all(field in content for field in NASA_EVIDENCE_FIELDS)
