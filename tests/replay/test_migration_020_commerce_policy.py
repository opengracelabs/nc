"""Migration 20 Commerce Intelligence policy replay tests."""
from pathlib import Path


MIGRATION_20 = Path("infrastructure/postgres/init/20_commerce_policy.sql")


def test_migration_20_exists() -> None:
    assert MIGRATION_20.exists()


def test_migration_20_creates_postgresql_authoritative_policy_table() -> None:
    sql = MIGRATION_20.read_text()

    assert "CREATE TABLE IF NOT EXISTS commerce_policy" in sql
    for field in (
        "version",
        "status",
        "effective_from",
        "effective_until",
        "authored_by",
        "approved_by",
        "approved_at",
        "previous_version_id",
        "max_score_age_days",
        "formula_spec",
        "composite_weights",
        "tier_thresholds",
        "hard_gate_values",
        "model_activation_thresholds",
        "product_surface_requirements",
    ):
        assert field in sql


def test_migration_20_uses_six_state_policy_vocabulary_and_staleness_default() -> None:
    sql = MIGRATION_20.read_text()

    assert "REFERENCES commerce_policy_status_vocabulary(value)" in sql
    assert "max_score_age_days           INT NOT NULL DEFAULT 90" in sql
    assert "CHECK (max_score_age_days > 0)" in sql


def test_migration_20_enforces_single_active_policy_and_second_human_approval() -> None:
    sql = MIGRATION_20.read_text()

    assert "uniq_commerce_policy_one_active" in sql
    assert "WHERE status = 'active'" in sql
    assert "approved_by IS DISTINCT FROM authored_by" in sql
    assert "status NOT IN ('active','paused','superseded')" in sql
    assert "approved_by IS NOT NULL AND approved_at IS NOT NULL" in sql


def test_migration_20_locks_policy_scoring_fields_after_activation() -> None:
    sql = MIGRATION_20.read_text()

    assert "CREATE OR REPLACE FUNCTION enforce_commerce_policy_immutability" in sql
    assert "OLD.status IN ('active','paused','superseded')" in sql
    for field in (
        "formula_spec",
        "composite_weights",
        "tier_thresholds",
        "hard_gate_values",
        "model_activation_thresholds",
        "product_surface_requirements",
        "max_score_age_days",
    ):
        assert field in sql
    assert "RAISE EXCEPTION" in sql


def test_migration_20_seeds_draft_policy_with_article_13_formula_spec() -> None:
    sql = MIGRATION_20.read_text()

    assert "'1.0.0'" in sql
    assert "'draft'" in sql
    assert "Initial Commerce Intelligence policy" in sql
    assert "weighted_sum_v1" in sql
    assert "csm_pass2_v1" in sql
    for signal in (
        "illustrator_prestige",
        "rights_confidence",
        "golden_age_factor",
        "institutional_credit",
        "provenance_completeness",
        "image_quality_score",
        "taxon_commercial_tier_score",
        "resolution_tier_score",
        "composition_fit",
        "color_score",
        "place_relevance_score",
        "taxon_place_iconic",
        "place_tier_score",
        "identification_confidence",
    ):
        assert signal in sql
    for subscore in ("museum_score", "retail_score", "publishing_score", "tourism_score", "reference_score"):
        assert subscore in sql
    for csm_dimension in ("VAS", "PIS", "SSS", "TAS", "IPS", "PVS"):
        assert csm_dimension in sql
    assert "sha256" in sql
    assert "lowercase_hex" in sql
    assert "alpha_sorted_keys" in sql
    assert "retain_json_nulls" in sql
    assert "poll_interval_hours" in sql


def test_migration_20_uses_constitution_composite_weights_and_gate_values() -> None:
    sql = MIGRATION_20.read_text()

    for expected in (
        '"retail_score": 0.3',
        '"tourism_score": 0.25',
        '"museum_score": 0.2',
        '"publishing_score": 0.15',
        '"reference_score": 0.1',
        '"min_rights_confidence": 0.7',
        '"min_image_width_px": 2000',
        '"min_quality_score": 0.4',
        '"rights_confidence_equals": 0.0',
        '"null_blocks": true',
        '"publication_stage_only": true',
    ):
        assert expected in sql

    assert "null_blocks_MASTERWORK_FLAGSHIP" in sql
    for tier in ("MASTERWORK", "FLAGSHIP", "STANDARD", "REFERENCE", "BLOCKED"):
        assert tier in sql
