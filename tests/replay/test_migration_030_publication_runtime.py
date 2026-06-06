"""Migration 30 publication runtime replay tests."""
from pathlib import Path

MIGRATION_30 = Path("infrastructure/postgres/init/30_publication_runtime.sql")


def test_migration_30_exists() -> None:
    assert MIGRATION_30.exists()


def test_migration_30_creates_runtime_tables() -> None:
    sql = MIGRATION_30.read_text()
    for table in ("publication_channel_profiles", "publication_candidates", "publication_audit_log"):
        assert f"CREATE TABLE IF NOT EXISTS {table}" in sql


def test_migration_30_enforces_parent_gates() -> None:
    sql = MIGRATION_30.read_text()
    assert "enforce_publication_candidate_parent_approved" in sql
    assert "pr.status = 'curator_approved'" in sql
    assert "co.curator_decision = 'approved'" in sql
    assert "co.hard_gate_status = 'passed'" in sql
    assert "co.policy_stale = FALSE" in sql
    assert "co.commerce_tier <> 'blocked'" in sql


def test_migration_30_has_append_only_audit() -> None:
    sql = MIGRATION_30.read_text()
    assert "CREATE OR REPLACE RULE publication_audit_log_no_update" in sql
    assert "CREATE OR REPLACE RULE publication_audit_log_no_delete" in sql
    assert "enforce_publication_audit_hash_chain" in sql


def test_migration_30_has_no_external_publication_state() -> None:
    sql = MIGRATION_30.read_text()
    assert "chk_publication_candidates_no_external_state" in sql
    for phrase in ("No Shopify", "No Etsy", "No Gelato", "No Printful", "No Lulu", "No external IDs", "No publication execution"):
        assert phrase in sql
