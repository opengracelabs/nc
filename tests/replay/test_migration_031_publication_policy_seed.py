"""Migration 31 publication policy seed replay tests."""
from pathlib import Path

MIGRATION_31 = Path("infrastructure/postgres/init/31_publication_policy_seed.sql")


def test_migration_31_exists() -> None:
    assert MIGRATION_31.exists()


def test_migration_31_seeds_draft_policy() -> None:
    sql = MIGRATION_31.read_text()
    assert "INSERT INTO publication_policy" in sql
    assert "'1.0.0'" in sql
    assert "'draft'" in sql
    assert "Initial Publication Intelligence policy." in sql


def test_migration_31_seeds_channel_profiles() -> None:
    sql = MIGRATION_31.read_text()
    assert "INSERT INTO publication_channel_profiles" in sql
    for profile in ("editorial_catalog", "collection_feature", "educational_release"):
        assert profile in sql


def test_migration_31_seed_has_no_external_provider_terms_in_json() -> None:
    sql = MIGRATION_31.read_text().lower()
    for allowed in ("no shopify", "no etsy", "no gelato", "no printful", "no lulu", "no external ids", "no publication execution"):
        sql = sql.replace(allowed, "")
    for blocked in ("shopify", "etsy", "gelato", "printful", "lulu", "provider", "api"):
        assert blocked not in sql
