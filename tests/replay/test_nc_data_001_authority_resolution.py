"""NC-DATA-001 authority resolution schema replay tests."""

from pathlib import Path

MIGRATION_46 = Path("infrastructure/postgres/init/46_nc_data_001_authority_resolution.sql")


def test_authority_resolution_migration_exists() -> None:
    assert MIGRATION_46.exists()


def test_authority_resolution_creates_required_tables() -> None:
    sql = MIGRATION_46.read_text(encoding="utf-8")

    assert "CREATE TABLE IF NOT EXISTS authority_resolution_registry" in sql
    assert "CREATE TABLE IF NOT EXISTS canonical_identity" in sql


def test_authority_resolution_supports_required_authorities() -> None:
    sql = MIGRATION_46.read_text(encoding="utf-8")

    assert "authority IN ('geonames','wikidata','gbif')" in sql
    assert "'geonames', '5843591', 'canonical_place_id'" in sql
    assert "'wikidata', 'Q351', 'cross_reference'" in sql
    assert "'gbif', 'yellowstone-place-validation', 'validation_only'" in sql


def test_authority_resolution_enforces_one_canonical_place_id() -> None:
    sql = MIGRATION_46.read_text(encoding="utf-8")

    assert "uq_authority_resolution_one_canonical_place" in sql
    assert "WHERE authority_role = 'canonical_place_id' AND status = 'active'" in sql
    assert "anchor_slug           TEXT NOT NULL UNIQUE" in sql
    assert "canonical_place_id    TEXT NOT NULL UNIQUE" in sql


def test_yellowstone_canonical_identity_is_geonames_only() -> None:
    sql = MIGRATION_46.read_text(encoding="utf-8")

    assert "'yellowstone'" in sql
    assert "'geonames:5843591'" in sql
    assert "'5843591'" in sql
    assert "'Q351'" in sql
    assert "geonames_id_claim" in sql
    assert "5844046" in sql
    assert "canonical_place_id = 'geonames:' || geonames_id" in sql
