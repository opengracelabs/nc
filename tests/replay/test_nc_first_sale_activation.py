"""NC-FIRST-SALE activation replay tests."""
from pathlib import Path

MIGRATION_41 = Path("infrastructure/postgres/init/41_nc_first_sale_activation.sql")


def test_first_sale_migration_exists() -> None:
    assert MIGRATION_41.exists()


def test_first_sale_uses_existing_product_runtime() -> None:
    sql = MIGRATION_41.read_text(encoding="utf-8")

    assert "ALTER TABLE product_candidate" in sql
    assert "ALTER TABLE product_publication" not in sql
    assert "CREATE TABLE IF NOT EXISTS product_first_sale_activation" in sql
    assert "product_manual_export_package" in sql
    assert "product_audit_event" in sql


def test_first_sale_activates_requested_products() -> None:
    sql = MIGRATION_41.read_text(encoding="utf-8")

    assert "NC-PROD-001" in sql
    assert "NC-PROD-008" in sql
    assert "Earthrise Museum Giclée Print" in sql
    assert "Earthrise High-Resolution Digital Download" in sql
    assert "earthrise-as08-14-2383-archival-print" in sql
    assert "earthrise-as08-14-2383-digital-download" in sql


def test_first_sale_generates_snapshots_packages_and_activation_records() -> None:
    sql = MIGRATION_41.read_text(encoding="utf-8")

    assert "first-sale-v1" in sql
    assert "nc-first-sale-v1" in sql
    assert "snapshot_export" in sql
    assert "package_manifest" in sql
    assert "product_first_sale_activation" in sql
    assert "activation_status" in sql
    assert "'activated'" in sql


def test_first_sale_includes_gate_e_and_metadata_requirements() -> None:
    sql = MIGRATION_41.read_text(encoding="utf-8")

    assert "Gate E" in sql
    assert "curator_review" in sql
    assert "principal_architect_signoff" in sql
    assert "two_human_activation" in sql
    assert "nc:nasa_attribution" in sql
    assert "nc:rights_basis" in sql
    assert "nc:rights_statement_uri" in sql
    assert "Image credit: NASA. NASA does not endorse this product." in sql


def test_first_sale_has_audit_trail() -> None:
    sql = MIGRATION_41.read_text(encoding="utf-8")

    assert "manual_package_generated" in sql
    assert "snapshot_export_generated" in sql
    assert "manual_package_activated" in sql
    assert "ON CONFLICT (event_sha256) DO NOTHING" in sql


def test_first_sale_has_no_provider_integration() -> None:
    sql = MIGRATION_41.read_text(encoding="utf-8")

    for forbidden in ("No Printful", "No Printify", "No Gelato"):
        assert forbidden in sql
    assert "provider_integration', false" in sql
    for forbidden in ('"provider":"printful"', '"provider":"printify"', '"provider":"gelato"'):
        assert forbidden not in sql.lower()
