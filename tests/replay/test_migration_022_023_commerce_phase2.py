"""Migration 22-23 Commerce Intelligence Phase 2 replay tests."""
from pathlib import Path


MIGRATION_22 = Path("infrastructure/postgres/init/22_score_audit_log.sql")
MIGRATION_23 = Path("infrastructure/postgres/init/23_commerce_recommendations.sql")


def test_phase2_migrations_exist_in_expected_order() -> None:
    assert MIGRATION_22.exists()
    assert MIGRATION_23.exists()
    assert MIGRATION_22.name < MIGRATION_23.name


def test_phase2_keeps_postgresql_authoritative() -> None:
    m22 = MIGRATION_22.read_text()
    m23 = MIGRATION_23.read_text()

    assert "PostgreSQL is authoritative" in m22
    assert "PostgreSQL is authoritative" in m23
    assert "CREATE TABLE IF NOT EXISTS score_audit_log" in m22
    assert "CREATE TABLE IF NOT EXISTS product_recommendations" in m23
    assert "CREATE TABLE IF NOT EXISTS collection_recommendations" in m23


def test_phase2_audit_before_recommendations_contract() -> None:
    m22 = MIGRATION_22.read_text()
    m23 = MIGRATION_23.read_text()

    assert "score_audit_log" in m22
    assert "enforce_commerce_opportunity_audit_exists" in m22
    assert "commerce_opportunities" in m23
    assert "curator_decision = 'approved'" in m23


def test_phase2_is_append_only_for_score_audit() -> None:
    sql = MIGRATION_22.read_text()

    assert "CREATE OR REPLACE RULE score_audit_log_no_update" in sql
    assert "CREATE OR REPLACE RULE score_audit_log_no_delete" in sql
    assert "enforce_score_audit_hash_chain" in sql


def test_phase2_has_no_worker_or_marketplace_activation() -> None:
    combined = f"{MIGRATION_22.read_text()}\n{MIGRATION_23.read_text()}"

    assert "CREATE TABLE IF NOT EXISTS scoring_worker" not in combined
    assert "CREATE ROLE" not in combined
    assert "CREATE TABLE IF NOT EXISTS products" not in combined
    assert "product_generation" not in combined
    assert "shopify" not in combined.lower().replace("no shopify integration", "")
    assert "etsy" not in combined.lower().replace("no etsy integration", "")
