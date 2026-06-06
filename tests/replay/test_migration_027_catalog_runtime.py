"""Migration 27 catalog runtime replay tests."""
from pathlib import Path


MIGRATION_27 = Path("infrastructure/postgres/init/27_catalog_runtime.sql")


def test_migration_27_exists() -> None:
    assert MIGRATION_27.exists()


def test_migration_27_creates_catalog_runtime_tables() -> None:
    sql = MIGRATION_27.read_text()

    for table in (
        "catalog_candidates",
        "catalog_variants",
        "catalog_pricing_profiles",
        "catalog_audit_log",
    ):
        assert f"CREATE TABLE IF NOT EXISTS {table}" in sql


def test_migration_27_enforces_approved_recommendation_parent() -> None:
    sql = MIGRATION_27.read_text()

    assert "enforce_catalog_candidate_parent_approved" in sql
    assert "pr.status = 'curator_approved'" in sql
    assert "co.curator_decision = 'approved'" in sql
    assert "co.hard_gate_status = 'passed'" in sql
    assert "co.policy_stale = FALSE" in sql
    assert "co.commerce_tier <> 'blocked'" in sql


def test_migration_27_has_append_only_catalog_audit() -> None:
    sql = MIGRATION_27.read_text()

    assert "CREATE OR REPLACE RULE catalog_audit_log_no_update" in sql
    assert "CREATE OR REPLACE RULE catalog_audit_log_no_delete" in sql
    assert "enforce_catalog_audit_hash_chain" in sql
    assert "previous_entry_checksum must match latest catalog_audit_log entry" in sql


def test_migration_27_prohibits_channels_providers_and_publication() -> None:
    sql = MIGRATION_27.read_text()

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
    assert "chk_catalog_candidates_no_provider_publication" in sql
    assert "chk_catalog_variants_no_provider_identifiers" in sql


def test_migration_27_chains_catalog_audit_by_product_recommendation_first() -> None:
    sql = MIGRATION_27.read_text()

    assert "COALESCE(cal.product_recommendation_id, cal.catalog_candidate_id, cal.catalog_variant_id)" in sql
    assert "COALESCE(NEW.product_recommendation_id, NEW.catalog_candidate_id, NEW.catalog_variant_id)" in sql
