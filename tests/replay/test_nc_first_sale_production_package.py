"""NC-FIRST-SALE production package replay tests."""
from pathlib import Path

MIGRATION_42 = Path("infrastructure/postgres/init/42_nc_first_sale_production_package.sql")


def test_production_package_migration_exists() -> None:
    assert MIGRATION_42.exists()


def test_production_package_creates_runtime_table() -> None:
    sql = MIGRATION_42.read_text(encoding="utf-8")

    assert "CREATE TABLE IF NOT EXISTS product_production_package" in sql
    assert "final_publication_snapshot" in sql
    assert "final_manual_export_package" in sql
    assert "attribution_manifest" in sql
    assert "disclaimer_manifest" in sql
    assert "rights_evidence_manifest" in sql


def test_production_package_targets_first_sale_products() -> None:
    sql = MIGRATION_42.read_text(encoding="utf-8")

    assert "NC-PROD-001" in sql
    assert "NC-PROD-008" in sql
    assert "WHERE fsa.product_code IN ('NC-PROD-001', 'NC-PROD-008')" in sql


def test_production_package_generates_required_manifests() -> None:
    sql = MIGRATION_42.read_text(encoding="utf-8")

    assert "attribution-manifest.json" in sql
    assert "disclaimer-manifest.json" in sql
    assert "rights-evidence-manifest.json" in sql
    assert "Image credit: NASA. NASA does not endorse this product." in sql
    assert "17 U.S.C. § 105" in sql
    assert "proof_url" in sql


def test_production_package_verifies_hashes_and_activation_state() -> None:
    sql = MIGRATION_42.read_text(encoding="utf-8")

    assert "publication_snapshot_hash_verified" in sql
    assert "export_package_hash_verified" in sql
    assert "activation_state_verified" in sql
    assert "activation_state = 'activated'" in sql
    assert "final_snapshot_sha256 ~ '^[0-9a-f]{64}$'" in sql
    assert "final_package_sha256 ~ '^[0-9a-f]{64}$'" in sql


def test_production_package_has_no_provider_integration() -> None:
    sql = MIGRATION_42.read_text(encoding="utf-8")

    for forbidden in ("No Printful", "No Printify", "No Gelato"):
        assert forbidden in sql
    assert "provider_integration', false" in sql
    for forbidden in ('"provider":"printful"', '"provider":"printify"', '"provider":"gelato"'):
        assert forbidden not in sql.lower()


def test_production_package_is_idempotent_and_audited() -> None:
    sql = MIGRATION_42.read_text(encoding="utf-8")

    assert "ON CONFLICT (product_code) DO UPDATE" in sql
    assert "UNIQUE (product_publication_id, package_version)" in sql
    assert "product_audit_event" in sql
    assert "ON CONFLICT (event_sha256) DO NOTHING" in sql
