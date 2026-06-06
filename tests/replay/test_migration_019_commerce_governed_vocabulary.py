"""Migration 19 Commerce Intelligence governed vocabulary replay tests."""
from pathlib import Path


MIGRATION_19 = Path("infrastructure/postgres/init/19_commerce_governed_vocabulary.sql")


def test_migration_19_exists() -> None:
    assert MIGRATION_19.exists()


def test_migration_19_allows_bhl_and_loc_sources_only() -> None:
    sql = MIGRATION_19.read_text()

    assert "DROP CONSTRAINT IF EXISTS chk_illustration_opportunity_source" in sql
    assert "ADD CONSTRAINT chk_illustration_opportunity_source" in sql
    assert "source IN ('bhl','loc')" in sql
    assert "source = 'bhl'" not in sql


def test_migration_19_seeds_six_state_policy_status_vocabulary() -> None:
    sql = MIGRATION_19.read_text()

    assert "CREATE TABLE IF NOT EXISTS commerce_policy_status_vocabulary" in sql
    for status in (
        "draft",
        "pending_approval",
        "active",
        "paused",
        "superseded",
        "retired",
    ):
        assert f"('{status}'" in sql


def test_migration_19_seeds_commerce_scoring_vocabularies() -> None:
    sql = MIGRATION_19.read_text()

    for table in (
        "commerce_tier_vocabulary",
        "commerce_csm_tier_vocabulary",
        "commerce_hard_gate_status_vocabulary",
        "commerce_computation_trigger_vocabulary",
        "commerce_curator_decision_vocabulary",
        "commerce_curator_review_reason_vocabulary",
        "commerce_audit_event_type_vocabulary",
        "commerce_actor_type_vocabulary",
        "commerce_color_profile_vocabulary",
        "commerce_resolution_tier_vocabulary",
        "commerce_anchor_type_vocabulary",
    ):
        assert f"CREATE TABLE IF NOT EXISTS {table}" in sql

    for value in (
        "tier_1",
        "blocked_rights",
        "policy_version_change",
        "score_computed",
        "system_worker",
        "chromolithograph",
        "premium",
        "biological",
        "MASTERWORK",
        "FLAGSHIP",
        "STANDARD",
        "REFERENCE",
        "BLOCKED",
    ):
        assert f"('{value}'" in sql

    csm_block = sql.split("CREATE TABLE IF NOT EXISTS commerce_csm_tier_vocabulary", 1)[1]
    csm_block = csm_block.split("CREATE TABLE IF NOT EXISTS commerce_hard_gate_status_vocabulary", 1)[0]
    for rejected_csm_tier in ("strong", "moderate", "weak"):
        assert f"('{rejected_csm_tier}'" not in csm_block


def test_migration_19_governs_independent_signal_tables() -> None:
    sql = MIGRATION_19.read_text()

    for table in (
        "taxon_commercial_tier_vocabulary",
        "priority_illustrators_vocabulary",
        "place_iconic_taxa_vocabulary",
    ):
        assert f"CREATE TABLE IF NOT EXISTS {table}" in sql
        assert "authored_by" in sql
        assert "approved_by" in sql
        assert "approved_at" in sql
        assert "approved_by IS DISTINCT FROM authored_by" in sql

    assert "UNIQUE (place_id, scientific_name)" in sql
    assert "status IN ('proposed','active','retired')" in sql


def test_migration_19_seeds_benchmark_vocabulary_rows_as_proposed() -> None:
    sql = MIGRATION_19.read_text()

    for value in ("high", "moderate", "low", "none"):
        assert f"('{value}'" in sql

    for illustrator in (
        "Audubon",
        "Gould",
        "Merian",
        "Redoute",
        "Lear",
        "Nodder",
        "Haeckel",
        "Wolf",
    ):
        assert illustrator in sql

    assert "commerce_migration_19" in sql
    assert "ON CONFLICT" in sql
