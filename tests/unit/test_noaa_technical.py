import json
from pathlib import Path

from workers.noaa_adapter.client import flickr_record_to_discovery_payload
from workers.noaa_adapter.normalize import normalize_record
from workers.noaa_adapter.technical import (
    NOAA_TECHNICAL_EVIDENCE_FIELDS,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"
RETRIEVED_AT = "2026-06-11T00:00:00Z"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_noaa_technical_metadata_carries_sprint2_evidence() -> None:
    source = flickr_record_to_discovery_payload(fixture_json("flickr_photo_usgov_clean_noaa.json"))
    source["o_width"] = "1600"
    source["o_height"] = "1000"
    normalized = normalize_record(source, retrieved_at=RETRIEVED_AT)[0]

    content = build_technical_metadata(normalized)

    assert validation_status(content) == "valid"
    assert content["source"] == "noaa"
    assert content["schema_standard"] == "noaa_discovery_v1"
    assert content["technical_schema_version"] == "noaa-discovery-technical-v1"
    assert content["source_record_id"] == "1001"
    assert content["rights_decision"] == "ALLOWED"
    assert content["noaa_rights_class"] == "rights_class_9"
    assert content["quality_flag"] == "meets_minimum"
    assert len(content["content_hash"]) == 64
    assert all(field in content for field in NOAA_TECHNICAL_EVIDENCE_FIELDS)

