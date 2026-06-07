from pathlib import Path

from workers.rijksmuseum_adapter.edm import normalize_search_getrecord
from workers.rijksmuseum_adapter.technical import (
    TECHNICAL_SCHEMA_VERSION,
    build_technical_metadata,
    content_hash,
    quality_flag,
    validation_status,
)

_FIXTURE = Path("tests/fixtures/rijksmuseum/yellowstone_getrecord_edm.xml")


def _search_response() -> dict:
    return {
        "orderedItems": [
            {"id": "https://id.rijksmuseum.nl/200343467", "title": "Yellowstone National Park"}
        ]
    }


def _yellowstone_normalized() -> dict:
    return normalize_search_getrecord(_search_response(), _FIXTURE.read_text())


def test_build_technical_metadata_from_yellowstone_getrecord_fixture() -> None:
    content = build_technical_metadata(_yellowstone_normalized(), media_type_id="image")

    assert TECHNICAL_SCHEMA_VERSION == "rijksmuseum-edm-technical-v1"
    assert content["source"] == "rijksmuseum"
    assert content["schema_standard"] == "edm"
    assert content["record_id"] == "https://id.rijksmuseum.nl/200343467"
    assert content["title"] == "Yellowstone National Park"
    assert content["source_url"] == "https://www.rijksmuseum.nl/en/collection/RP-F-2001-7-1062"
    assert content["representative_media_url"] == "https://iiif.micr.io/example/full/max/0/default.jpg"
    assert content["rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert content["width_px"] == 2500
    assert content["height_px"] == 2002
    assert content["quality_flag"] == "meets_minimum"
    assert content["subject_terms"] == [
        {"term": "Yellowstone", "controlled_vocabulary": False},
        {"term": "National parks", "controlled_vocabulary": False},
    ]
    assert content["mandatory_field_warnings"] == []
    assert validation_status(content) == "valid"


def test_quality_flag_tracks_visual_baseline() -> None:
    assert quality_flag(2500, 2002) == "meets_minimum"
    assert quality_flag(399, 200) == "below_minimum"
    assert quality_flag(None, None) == "unknown_dimensions"


def test_content_hash_is_replay_stable() -> None:
    content = build_technical_metadata(_yellowstone_normalized(), media_type_id="image")
    reordered = dict(reversed(list(content.items())))

    assert content_hash(content) == content_hash(reordered)


def test_validation_status_rejects_missing_identity_or_urls() -> None:
    valid = build_technical_metadata(_yellowstone_normalized(), media_type_id="image")

    missing_identity = {**valid, "record_id": None}
    missing_urls = {**valid, "representative_media_url": None, "source_url": None}

    assert validation_status(missing_identity) == "invalid"
    assert validation_status(missing_urls) == "invalid"
