from pathlib import Path

import pytest

from workers.rijksmuseum_adapter.edm import (
    canonical_xml_hash,
    extract_oai_identifier,
    first_search_identifier,
    mandatory_field_warnings,
    normalize_oai_edm_record,
    normalize_search_getrecord,
)
from workers.rijksmuseum_adapter.rights import RightsDecision

_FIXTURE = Path("tests/fixtures/rijksmuseum/yellowstone_getrecord_edm.xml")
_ERROR_FIXTURE = Path("tests/fixtures/rijksmuseum/oai_error.xml")


def _xml() -> str:
    return _FIXTURE.read_text()


def _search_response() -> dict:
    return {
        "orderedItems": [
            {
                "id": "https://id.rijksmuseum.nl/200343467",
                "title": "Yellowstone National Park",
                "type": "IMAGE",
            }
        ]
    }


def test_extract_oai_identifier() -> None:
    assert extract_oai_identifier(_xml()) == "https://id.rijksmuseum.nl/200343467"


def test_first_search_identifier() -> None:
    assert first_search_identifier(_search_response()) == "https://id.rijksmuseum.nl/200343467"
    assert first_search_identifier({"orderedItems": [{}, "bad"]}) is None


def test_normalize_oai_edm_record_maps_m36_fields() -> None:
    normalized = normalize_oai_edm_record(_xml())

    assert normalized["record_id"] == "https://id.rijksmuseum.nl/200343467"
    assert normalized["title"] == "Yellowstone National Park"
    assert normalized["description"] == "Photographic view of Yellowstone National Park."
    assert normalized["date"] == "1891"
    assert normalized["creator"] == "Rijksmuseum"
    assert normalized["subject_terms"] == ["Yellowstone", "National parks"]
    assert normalized["rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert normalized["provider"] == "Rijksmuseum"
    assert normalized["dataProvider"] == "Rijksmuseum"
    assert normalized["edm_type"] == "IMAGE"
    assert normalized["source_url"] == "https://www.rijksmuseum.nl/en/collection/RP-F-2001-7-1062"
    assert normalized["representative_media_url"] == "https://iiif.micr.io/example/full/max/0/default.jpg"
    assert normalized["preview_urls"] == ["https://iiif.micr.io/example/full/200,/0/default.jpg"]
    assert normalized["width_px"] == 2500
    assert normalized["height_px"] == 2002
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True
    assert normalized["raw_payload_hash"] == canonical_xml_hash(_xml())
    assert mandatory_field_warnings(normalized) == []


def test_normalize_search_getrecord_preserves_oai_authority() -> None:
    normalized = normalize_search_getrecord(_search_response(), _xml())

    assert normalized["record_id"] == "https://id.rijksmuseum.nl/200343467"
    assert normalized["title"] == "Yellowstone National Park"


def test_mandatory_field_warnings_reports_missing_values() -> None:
    assert mandatory_field_warnings({}) == [
        "missing_record_id",
        "missing_title",
        "missing_rights_uri",
        "missing_description",
        "missing_date",
        "missing_provider",
        "missing_data_provider",
    ]


def test_oai_error_raises_value_error() -> None:
    with pytest.raises(ValueError, match="oai_error:idDoesNotExist"):
        normalize_oai_edm_record(_ERROR_FIXTURE.read_text())
