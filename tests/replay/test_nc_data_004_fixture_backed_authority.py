"""NC-DATA-004 fixture-backed authority replay tests."""

from pathlib import Path

from services.data.fixture_acquisition import (
    has_fixture_backed_evidence,
    load_place_fixture_inventories,
)

FIXTURES = Path("tests/fixtures")
MIGRATION_48 = Path("infrastructure/postgres/init/48_nc_data_004_fixture_backed_authority.sql")


def test_nc_data_004_migration_exists() -> None:
    assert MIGRATION_48.exists()


def test_great_barrier_reef_has_fixture_backed_evidence() -> None:
    geonames, wikidata = load_place_fixture_inventories("great-barrier-reef", FIXTURES)

    assert has_fixture_backed_evidence("great-barrier-reef", FIXTURES)
    assert set(geonames.capture_kinds) == {"direct", "search", "hierarchy"}
    assert set(wikidata.capture_kinds) == {"search", "entity"}
    assert geonames.canonical_assignment is False
    assert wikidata.canonical_assignment is False


def test_missing_fixture_bundles_block_ratification() -> None:
    for anchor_slug in ("galapagos", "venice", "papahanaumokuakea"):
        assert not has_fixture_backed_evidence(anchor_slug, FIXTURES)


def test_nc_data_004_demotes_unfixture_backed_places() -> None:
    sql = MIGRATION_48.read_text(encoding="utf-8")

    assert "WHERE anchor_slug IN ('galapagos','venice')" in sql
    assert "DELETE FROM canonical_identity" in sql
    assert "blocked_missing_fixture" in sql
    assert "demoted until fixture-backed" in sql


def test_nc_data_004_blocks_papahanaumokuakea_provisional_promotion() -> None:
    sql = MIGRATION_48.read_text(encoding="utf-8")

    assert "WHERE anchor_slug = 'papahanaumokuakea'" in sql
    assert "no provisional promotion" in sql
    assert "geonames_status" in sql
    assert "unconfirmed" in sql
    assert "DELETE FROM canonical_identity" in sql
    assert "WHERE anchor_slug = 'papahanaumokuakea'" in sql


def test_nc_data_004_great_barrier_reef_ratification_references_fixtures() -> None:
    sql = MIGRATION_48.read_text(encoding="utf-8")

    assert "great-barrier-reef" in sql
    assert "ratified_fixture_backed" in sql
    assert "tests/fixtures/geonames/great_barrier_reef/manifest.json" in sql
    assert "tests/fixtures/wikidata/great_barrier_reef/manifest.json" in sql
