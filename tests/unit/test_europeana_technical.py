import json
from pathlib import Path

from workers.europeana_adapter.edm import normalize_edm_record
from workers.europeana_adapter.technical import (
    TECHNICAL_SCHEMA_VERSION,
    build_technical_metadata,
    content_hash,
    quality_flag,
    validation_status,
)

_FIXTURE = Path("tests/fixtures/europeana/yellowstone_launch_metadata_v1_record.json")


def _yellowstone_normalized() -> dict:
    return normalize_edm_record(json.loads(_FIXTURE.read_text()))


def test_build_technical_metadata_from_yellowstone_launch_fixture() -> None:
    content = build_technical_metadata(_yellowstone_normalized(), media_type_id="map")

    assert TECHNICAL_SCHEMA_VERSION == "europeana-edm-technical-v1"
    assert content["record_id"] == "/9200518/ark__12148_btv1b530248434"
    assert content["title"] == "Map of Yellowstone Lake"
    assert content["source_url"] == "https://www.europeana.eu/en/item/9200518/ark__12148_btv1b530248434"
    assert content["rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert content["width_px"] == 4500
    assert content["height_px"] == 3200
    assert content["quality_flag"] == "meets_minimum"
    assert content["subject_terms"] == [
        {"term": "Yellowstone Lake", "controlled_vocabulary": False},
        {"term": "Maps", "controlled_vocabulary": False},
        {"term": "National parks", "controlled_vocabulary": False},
    ]
    assert content["mandatory_field_warnings"] == []
    assert validation_status(content) == "valid"


def test_quality_flag_tracks_europeana_minimum_visual_baseline() -> None:
    assert quality_flag(4500, 3200) == "meets_minimum"
    assert quality_flag(399, 200) == "below_minimum"
    assert quality_flag(None, None) == "unknown_dimensions"


def test_content_hash_is_replay_stable() -> None:
    content = build_technical_metadata(_yellowstone_normalized(), media_type_id="map")
    reordered = dict(reversed(list(content.items())))

    assert content_hash(content) == content_hash(reordered)


def test_validation_status_rejects_missing_identity_or_urls() -> None:
    valid = build_technical_metadata(_yellowstone_normalized(), media_type_id="map")

    missing_identity = {**valid, "record_id": None}
    missing_urls = {**valid, "representative_media_url": None, "source_url": None}

    assert validation_status(missing_identity) == "invalid"
    assert validation_status(missing_urls) == "invalid"
