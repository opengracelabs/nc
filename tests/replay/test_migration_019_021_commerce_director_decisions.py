"""Cross-migration replay tests for Commerce Intelligence Director Decisions."""
from pathlib import Path


MIGRATION_19 = Path("infrastructure/postgres/init/19_commerce_governed_vocabulary.sql")
MIGRATION_20 = Path("infrastructure/postgres/init/20_commerce_policy.sql")
MIGRATION_21 = Path("infrastructure/postgres/init/21_commerce_opportunities.sql")


def _combined_sql() -> str:
    return "\n".join(path.read_text() for path in (MIGRATION_19, MIGRATION_20, MIGRATION_21))


def test_phase_1_migrations_exist_in_expected_order() -> None:
    for path in (MIGRATION_19, MIGRATION_20, MIGRATION_21):
        assert path.exists()


def test_director_decision_b3_loc_source_expansion_precedes_scoring() -> None:
    migration_19 = MIGRATION_19.read_text()
    migration_21 = MIGRATION_21.read_text()

    assert "source IN ('bhl','loc')" in migration_19
    assert "CREATE TABLE IF NOT EXISTS commerce_opportunities" in migration_21


def test_director_decision_b2_policy_uses_six_states() -> None:
    sql = _combined_sql()

    for status in (
        "draft",
        "pending_approval",
        "active",
        "paused",
        "superseded",
        "retired",
    ):
        assert f"('{status}'" in sql


def test_director_decision_h1_h2_use_cos_and_csm_without_legacy_scores() -> None:
    sql = _combined_sql()

    for field in (
        "museum_score",
        "retail_score",
        "publishing_score",
        "tourism_score",
        "reference_score",
        "csm_score",
        "csm_tier",
    ):
        assert field in sql

    assert "collection_fit_score" not in sql
    assert "commercial_value_score" not in sql


def test_director_decision_d2_adds_polling_staleness_fields() -> None:
    sql = _combined_sql()

    assert "max_score_age_days" in sql
    assert "last_scored_at" in sql
    assert "policy_stale" in sql
    assert "poll_interval_hours" in sql


def test_phase_1_excludes_migration_22_and_23_tables() -> None:
    sql = _combined_sql()

    assert "CREATE TABLE IF NOT EXISTS score_audit_log" not in sql
    assert "CREATE TABLE IF NOT EXISTS product_recommendations" not in sql
    assert "CREATE TABLE IF NOT EXISTS collection_recommendations" not in sql


def test_phase_1_declares_workers_and_product_generation_out_of_scope() -> None:
    sql = _combined_sql()

    assert "No scoring worker activation" in sql
    assert "No product generation" in sql
    assert "No Shopify integration" in sql
