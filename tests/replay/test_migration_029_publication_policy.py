"""Migration 29 publication policy replay tests."""
from pathlib import Path

MIGRATION_29 = Path("infrastructure/postgres/init/29_publication_policy.sql")


def test_migration_29_exists() -> None:
    assert MIGRATION_29.exists()


def test_migration_29_creates_publication_policy() -> None:
    sql = MIGRATION_29.read_text()
    assert "CREATE TABLE IF NOT EXISTS publication_policy" in sql
    for field in ("eligibility_gates", "channel_fit_rules", "publication_readiness_rules", "risk_rules", "ranking_rules", "staleness_rules"):
        assert field in sql


def test_migration_29_has_governance() -> None:
    sql = MIGRATION_29.read_text()
    assert "uniq_publication_policy_one_active" in sql
    assert "active publication_policy requires second-human approval" in sql
    assert "only one publication_policy may be active" in sql
    assert "enforce_publication_policy_immutability" in sql


def test_migration_29_blocks_external_execution_terms() -> None:
    sql = MIGRATION_29.read_text()
    for phrase in ("No Shopify", "No Etsy", "No Gelato", "No Printful", "No Lulu", "No external IDs", "No publication execution"):
        assert phrase in sql
    assert "chk_publication_policy_no_external_execution" in sql
