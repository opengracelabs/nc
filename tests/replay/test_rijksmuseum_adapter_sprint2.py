from pathlib import Path

from workers.rijksmuseum_adapter.edm import canonical_xml_hash, normalize_search_getrecord

_FIXTURE = Path("tests/fixtures/rijksmuseum/yellowstone_getrecord_edm.xml")


def _search_response() -> dict:
    return {
        "orderedItems": [
            {"id": "https://id.rijksmuseum.nl/200343467", "title": "Yellowstone National Park"}
        ]
    }


def test_rijksmuseum_search_getrecord_normalization_replays_stably() -> None:
    xml = _FIXTURE.read_text()

    first = normalize_search_getrecord(_search_response(), xml)
    second = normalize_search_getrecord(_search_response(), xml)

    assert first == second
    assert first["raw_payload_hash"] == canonical_xml_hash(xml)
    assert first["record_id"] == "https://id.rijksmuseum.nl/200343467"
    assert first["rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert first["representative_media_url"] == "https://iiif.micr.io/example/full/max/0/default.jpg"
