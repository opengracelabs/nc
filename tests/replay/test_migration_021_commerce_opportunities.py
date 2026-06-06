"""Migration 21 Commerce Intelligence opportunity replay tests."""
from pathlib import Path


MIGRATION_21 = Path("infrastructure/postgres/init/21_commerce_opportunities.sql")


def test_migration_21_exists() -> None:
    assert MIGRATION_21.exists()


def test_migration_21_creates_commerce_opportunities_table() -> None:
    sql = MIGRATION_21.read_text()

    assert "CREATE TABLE IF NOT EXISTS commerce_opportunities" in sql
    assert "opportunity_id                      UUID NOT NULL UNIQUE" in sql
    assert "REFERENCES illustration_opportunities(id)" in sql
    assert "policy_version_id                   UUID NOT NULL REFERENCES commerce_policy(id)" in sql


def test_migration_21_uses_director_approved_scoring_columns() -> None:
    sql = MIGRATION_21.read_text()

    for field in (
        "museum_score",
        "retail_score",
        "publishing_score",
        "tourism_score",
        "reference_score",
        "commerce_opportunity_score",
        "commerce_tier",
        "csm_score",
        "csm_tier",
    ):
        assert field in sql

    assert "collection_fit_score" not in sql
    assert "commercial_value_score" not in sql


def test_migration_21_has_staleness_and_input_hash_fields() -> None:
    sql = MIGRATION_21.read_text()

    assert "policy_stale                        BOOLEAN NOT NULL DEFAULT FALSE" in sql
    assert "last_scored_at                      TIMESTAMPTZ" in sql
    assert "input_hash_sha256                   TEXT NOT NULL" in sql
    assert "input_hash_sha256 ~ '^[0-9a-f]{64}$'" in sql
    assert "idx_commerce_opportunities_last_scored" in sql


def test_migration_21_references_governed_vocabularies() -> None:
    sql = MIGRATION_21.read_text()

    for reference in (
        "commerce_computation_trigger_vocabulary(value)",
        "commerce_hard_gate_status_vocabulary(value)",
        "commerce_color_profile_vocabulary(value)",
        "commerce_resolution_tier_vocabulary(value)",
        "commerce_tier_vocabulary(value)",
        "commerce_csm_tier_vocabulary(value)",
        "commerce_curator_review_reason_vocabulary(value)",
        "commerce_curator_decision_vocabulary(value)",
    ):
        assert f"REFERENCES {reference}" in sql


def test_migration_21_enforces_active_taxon_tier_with_trigger_not_check() -> None:
    sql = MIGRATION_21.read_text()

    assert "CREATE OR REPLACE FUNCTION enforce_active_taxon_commercial_tier" in sql
    assert "FROM taxon_commercial_tier_vocabulary" in sql
    assert "status = 'active'" in sql
    assert "CREATE TRIGGER trg_commerce_opportunities_active_taxon_tier" in sql
    assert "EXISTS (SELECT" not in sql


def test_migration_21_enforces_failed_gate_blocks_product_eligibility() -> None:
    sql = MIGRATION_21.read_text()

    assert "CREATE OR REPLACE FUNCTION enforce_commerce_opportunity_gate_eligibility" in sql
    assert "NEW.hard_gate_status <> 'passed'" in sql
    for field in (
        "eligible_wall_art_premium",
        "eligible_wall_art_standard",
        "eligible_calendar",
        "eligible_puzzle",
        "eligible_card",
        "eligible_book_illustration",
        "eligible_educational",
        "eligible_museum_print",
        "eligible_institutional_license",
    ):
        assert field in sql


def test_migration_21_does_not_create_later_phase_tables() -> None:
    sql = MIGRATION_21.read_text()

    assert "CREATE TABLE IF NOT EXISTS score_audit_log" not in sql
    assert "CREATE TABLE IF NOT EXISTS product_recommendations" not in sql
    assert "CREATE TABLE IF NOT EXISTS collection_recommendations" not in sql
    assert "Migration 22" in sql


def test_migration_21_contains_benchmark_fixture_insert_contract() -> None:
    sql = MIGRATION_21.read_text()

    assert "commerce_benchmark_fixture_v1" in sql
    assert "INSERT INTO commerce_opportunities" in sql
    assert "benchmark fixture" in sql
    assert "ON CONFLICT (opportunity_id) DO UPDATE" in sql
    assert "'MASTERWORK'" in sql
    assert "'moderate'" not in sql
