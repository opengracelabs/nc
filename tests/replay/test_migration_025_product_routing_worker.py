"""Migration 25 product routing worker replay tests."""
from pathlib import Path


MIGRATION_25 = Path("infrastructure/postgres/init/25_product_routing_worker.sql")


def test_migration_25_exists() -> None:
    assert MIGRATION_25.exists()


def test_migration_25_registers_routing_audit_event() -> None:
    sql = MIGRATION_25.read_text()

    assert "INSERT INTO commerce_audit_event_type_vocabulary" in sql
    assert "'product_route_recommended'" in sql
    assert "Product routing worker recommended one product family." in sql


def test_migration_25_does_not_create_catalog_or_provider_tables() -> None:
    sql = MIGRATION_25.read_text()

    assert "No catalog generation" in sql
    assert "No provider integration" in sql
    normalized = sql.lower().replace("no catalog generation", "").replace("no provider integration", "")
    assert "create table" not in normalized
    assert "shopify" not in normalized
    assert "etsy" not in normalized
