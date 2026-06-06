"""Migration 24 product routing policy replay tests."""
from pathlib import Path


MIGRATION_24 = Path("infrastructure/postgres/init/24_product_routing_policy.sql")


def test_migration_24_exists() -> None:
    assert MIGRATION_24.exists()


def test_migration_24_creates_product_routing_policy() -> None:
    sql = MIGRATION_24.read_text()

    assert "CREATE TABLE IF NOT EXISTS product_routing_policy" in sql
    for field in (
        "version                      TEXT NOT NULL UNIQUE",
        "status                       TEXT NOT NULL REFERENCES commerce_policy_status_vocabulary(value)",
        "max_route_age_days           INT NOT NULL DEFAULT 90 CHECK (max_route_age_days > 0)",
        "product_surface_requirements JSONB NOT NULL",
        "routing_formula_spec         JSONB NOT NULL",
        "family_caps                  JSONB NOT NULL DEFAULT '{}'",
        "curator_gate_spec            JSONB NOT NULL DEFAULT '{}'",
    ):
        assert field in sql


def test_migration_24_enforces_governed_policy_lifecycle() -> None:
    sql = MIGRATION_24.read_text()

    assert "uniq_product_routing_policy_one_active" in sql
    assert "approved_by IS DISTINCT FROM authored_by" in sql
    assert "active product_routing_policy requires second-human approval" in sql
    assert "active product_routing_policy requires effective_from" in sql
    assert "only one product_routing_policy may be active" in sql
    assert "enforce_product_routing_policy_immutability" in sql


def test_migration_24_seed_contains_expected_product_families() -> None:
    sql = MIGRATION_24.read_text()

    for family in (
        "wall_art",
        "calendar",
        "book",
        "puzzle",
        "card",
        "museum_print",
        "educational",
        "institutional_license",
    ):
        assert f'"{family}"' in sql
    assert '"routing_scorer_version": "product_routing_weighted_threshold_v1"' in sql
    assert '"max_recommendations_per_opportunity": 8' in sql


def test_migration_24_is_explicitly_not_catalog_or_provider_integration() -> None:
    sql = MIGRATION_24.read_text()

    assert "No catalog generation" in sql
    assert "No provider integration" in sql
    normalized = sql.lower().replace("no catalog generation", "").replace("no provider integration", "")
    assert "shopify" not in normalized
    assert "etsy" not in normalized
