"""Migration 26 catalog policy replay tests."""
from pathlib import Path


MIGRATION_26 = Path("infrastructure/postgres/init/26_catalog_policy.sql")


def test_migration_26_exists() -> None:
    assert MIGRATION_26.exists()


def test_migration_26_creates_catalog_policy() -> None:
    sql = MIGRATION_26.read_text()

    assert "CREATE TABLE IF NOT EXISTS catalog_policy" in sql
    for field in (
        "version              TEXT NOT NULL UNIQUE",
        "status               TEXT NOT NULL REFERENCES commerce_policy_status_vocabulary(value)",
        "catalog_rules        JSONB NOT NULL",
        "variant_rules        JSONB NOT NULL",
        "pricing_rules        JSONB NOT NULL",
        "eligibility_gates    JSONB NOT NULL",
    ):
        assert field in sql


def test_migration_26_has_policy_governance() -> None:
    sql = MIGRATION_26.read_text()

    assert "uniq_catalog_policy_one_active" in sql
    assert "active catalog_policy requires second-human approval" in sql
    assert "only one catalog_policy may be active" in sql
    assert "enforce_catalog_policy_immutability" in sql


def test_migration_26_prohibits_channels_providers_and_publication() -> None:
    sql = MIGRATION_26.read_text()

    for phrase in (
        "No Shopify",
        "No Etsy",
        "No Gelato",
        "No Printful",
        "No Lulu",
        "No provider identifiers",
        "No catalog publication",
    ):
        assert phrase in sql
    assert "chk_catalog_policy_no_channels_providers" in sql
