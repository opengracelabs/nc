"""NC-DATA-003 fixture acquisition replay tests."""

from pathlib import Path

from services.data.fixture_acquisition import load_grand_canyon_fixture_inventory

FIXTURES = Path("tests/fixtures")
GEONAMES_GRAND_CANYON = FIXTURES / "geonames" / "grand_canyon"
WIKIDATA_GRAND_CANYON = FIXTURES / "wikidata" / "grand_canyon"


def test_nc_data_003_fixture_directories_exist() -> None:
    assert GEONAMES_GRAND_CANYON.is_dir()
    assert WIKIDATA_GRAND_CANYON.is_dir()


def test_nc_data_003_fixture_inventory_has_required_captures() -> None:
    geonames, wikidata = load_grand_canyon_fixture_inventory(FIXTURES)

    assert geonames.anchor_slug == "grand-canyon"
    assert geonames.provider == "geonames"
    assert set(geonames.capture_kinds) == {"direct", "search", "hierarchy"}
    assert wikidata.anchor_slug == "grand-canyon"
    assert wikidata.provider == "wikidata"
    assert set(wikidata.capture_kinds) == {"search", "entity"}


def test_nc_data_003_does_not_assign_canonical_id() -> None:
    inventories = load_grand_canyon_fixture_inventory(FIXTURES)

    for inventory in inventories:
        assert inventory.canonical_assignment is False
        manifest = (inventory.fixture_dir / "manifest.json").read_text(encoding="utf-8")
        assert "canonical_place_id" not in manifest
        assert "canonical_authority" not in manifest


def test_nc_data_003_geonames_payloads_are_evidence_only() -> None:
    geonames, _ = load_grand_canyon_fixture_inventory(FIXTURES)
    payloads = {capture.kind: capture.payload for capture in geonames.captures}

    assert payloads["direct"]["geonameId"] == 5296401
    assert payloads["direct"]["name"] == "Grand Canyon National Park"
    assert payloads["search"]["geonames"][0]["geonameId"] == 5296401
    assert payloads["hierarchy"]["geonames"][-1]["geonameId"] == 5296401
    for payload in payloads.values():
        assert "canonical_place_id" not in payload
        assert "canonical_authority" not in payload


def test_nc_data_003_wikidata_payloads_are_evidence_only() -> None:
    _, wikidata = load_grand_canyon_fixture_inventory(FIXTURES)
    payloads = {capture.kind: capture.payload for capture in wikidata.captures}

    assert payloads["search"]["search"][0]["id"] == "Q220289"
    assert payloads["entity"]["entities"]["Q220289"]["id"] == "Q220289"
    for payload in payloads.values():
        assert "canonical_place_id" not in payload
        assert "canonical_authority" not in payload
