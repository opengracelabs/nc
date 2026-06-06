"""Migration 28 catalog policy seed replay tests."""
from pathlib import Path


MIGRATION_28 = Path("infrastructure/postgres/init/28_catalog_policy_seed.sql")


def test_migration_28_exists() -> None:
    assert MIGRATION_28.exists()


def test_migration_28_seeds_draft_policy_v1() -> None:
    sql = MIGRATION_28.read_text()

    assert "INSERT INTO catalog_policy" in sql
    assert "'1.0.0'" in sql
    assert "'draft'" in sql
    assert "Initial Catalog Intelligence policy." in sql
    assert '"requires_product_recommendation_status": "curator_approved"' in sql


def test_migration_28_seed_has_variant_and_pricing_rules() -> None:
    sql = MIGRATION_28.read_text()

    for value in (
        "wall_art",
        "museum_print",
        "calendar",
        "book",
        "puzzle",
        "card",
        "educational",
        "institutional_license",
        "standard_print_12x16",
        "archival_print_24x36",
        "base_price_cents",
    ):
        assert value in sql


def test_migration_28_seed_has_no_channel_provider_terms_in_json() -> None:
    sql = MIGRATION_28.read_text()

    normalized = sql.lower()
    for allowed in (
        "no shopify",
        "no etsy",
        "no gelato",
        "no printful",
        "no lulu",
        "no provider identifiers",
        "no catalog publication",
    ):
        normalized = normalized.replace(allowed, "")
    for blocked in ("shopify", "etsy", "gelato", "printful", "lulu", "provider"):
        assert blocked not in normalized
