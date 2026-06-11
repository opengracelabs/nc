"""NC-COMMERCE-002 activation migration replay tests."""
from pathlib import Path

MIGRATION_40 = Path("infrastructure/postgres/init/40_nc_commerce_002_activation.sql")


def test_commerce_activation_migration_exists() -> None:
    assert MIGRATION_40.exists()


def test_commerce_activation_adds_state_package_and_audit() -> None:
    sql = MIGRATION_40.read_text(encoding="utf-8")

    assert "ADD COLUMN IF NOT EXISTS activation_state" in sql
    assert "CREATE TABLE IF NOT EXISTS product_activation_state_vocabulary" in sql
    assert "CREATE TABLE IF NOT EXISTS product_manual_export_package" in sql
    assert "CREATE TABLE IF NOT EXISTS product_audit_event" in sql


def test_commerce_activation_is_manual_only() -> None:
    sql = MIGRATION_40.read_text(encoding="utf-8")

    assert "Manual provider only" in sql
    assert "provider              TEXT NOT NULL DEFAULT 'manual' CHECK (provider = 'manual')" in sql
    for forbidden in ("Printful", "Printify", "Gelato"):
        assert f"No {forbidden}" in sql
    for forbidden in ("printful", "printify", "gelato"):
        assert f"provider', '{forbidden}'" not in sql.lower()


def test_commerce_activation_state_machine_is_enforced() -> None:
    sql = MIGRATION_40.read_text(encoding="utf-8")

    assert "enforce_product_publication_activation_transition" in sql
    assert "invalid product activation transition from ready" in sql
    assert "invalid product activation transition from packaged" in sql
    assert "invalid product activation transition from activated" in sql
    assert "invalid product activation transition from retracted" in sql


def test_commerce_activation_generates_manual_packages_for_three_products() -> None:
    sql = MIGRATION_40.read_text(encoding="utf-8")

    for candidate in (
        "earthrise-as08-14-2383-archival-print",
        "yellowstone-hayden-map-print",
        "grand-canyon-dutton-atlas-print",
    ):
        assert candidate in sql
    assert "nc-commerce-002-v1" in sql
    assert "snapshot_export" in sql
    assert "snapshot.json" in sql
    assert "attribution.json" in sql
    assert "README.txt" in sql


def test_commerce_activation_seeds_audit_events() -> None:
    sql = MIGRATION_40.read_text(encoding="utf-8")

    assert "manual_package_generated" in sql
    assert "snapshot_export_generated" in sql
    assert "ON CONFLICT (event_sha256) DO NOTHING" in sql
    assert "UNIQUE (event_sha256)" in sql


def test_commerce_activation_uses_idempotent_package_upsert() -> None:
    sql = MIGRATION_40.read_text(encoding="utf-8")

    assert "UNIQUE (product_publication_id, package_version)" in sql
    assert "ON CONFLICT (product_publication_id, package_version) DO UPDATE" in sql
    assert "UNIQUE (package_sha256)" in sql
