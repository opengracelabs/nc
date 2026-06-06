"""Migration 23 commerce recommendation replay tests."""
from pathlib import Path


MIGRATION_23 = Path("infrastructure/postgres/init/23_commerce_recommendations.sql")


def test_migration_23_exists() -> None:
    assert MIGRATION_23.exists()


def test_migration_23_creates_product_recommendations() -> None:
    sql = MIGRATION_23.read_text()

    assert "CREATE TABLE IF NOT EXISTS product_recommendations" in sql
    for field in (
        "opportunity_id              UUID NOT NULL REFERENCES illustration_opportunities(id)",
        "commerce_opportunity_id     UUID NOT NULL REFERENCES commerce_opportunities(id)",
        "policy_version_id           UUID NOT NULL REFERENCES commerce_policy(id)",
        "recommended_product_family  TEXT NOT NULL",
        "recommended_product_types   JSONB NOT NULL DEFAULT '{}'",
        "recommended_providers       JSONB NOT NULL DEFAULT '{}'",
        "recommendation_confidence   NUMERIC(4,3)",
        "recommendation_basis        JSONB NOT NULL DEFAULT '{}'",
        "status                      TEXT NOT NULL DEFAULT 'pending_curator_review'",
    ):
        assert field in sql

    assert "UNIQUE (opportunity_id, recommended_product_family)" in sql
    assert "product_family_vocabulary(value)" in sql
    assert "commerce_recommendation_status_vocabulary(value)" in sql
    assert "recommendation_confidence BETWEEN 0 AND 1" in sql


def test_migration_23_creates_governed_product_family_vocabulary() -> None:
    sql = MIGRATION_23.read_text()

    assert "CREATE TABLE IF NOT EXISTS product_family_vocabulary" in sql
    assert "INSERT INTO product_family_vocabulary" in sql
    for value in (
        "wall_art",
        "calendar",
        "book",
        "puzzle",
        "card",
        "museum_print",
        "educational",
        "home_decor",
        "fashion",
        "institutional_license",
    ):
        assert f"'{value}'" in sql


def test_migration_23_creates_collection_recommendations() -> None:
    sql = MIGRATION_23.read_text()

    assert "CREATE TABLE IF NOT EXISTS collection_recommendations" in sql
    for field in (
        "opportunity_id              UUID NOT NULL REFERENCES illustration_opportunities(id)",
        "commerce_opportunity_id     UUID NOT NULL REFERENCES commerce_opportunities(id)",
        "policy_version_id           UUID NOT NULL REFERENCES commerce_policy(id)",
        "recommended_collection_id   UUID REFERENCES collections(id)",
        "new_collection_proposal     JSONB NOT NULL DEFAULT '{}'",
        "fit_score                   NUMERIC(4,3) NOT NULL",
        "fit_basis                   JSONB NOT NULL DEFAULT '{}'",
        "collection_gap_type         TEXT NOT NULL DEFAULT 'none'",
        "status                      TEXT NOT NULL DEFAULT 'pending_curator_review'",
    ):
        assert field in sql

    assert "commerce_collection_gap_type_vocabulary(value)" in sql
    assert "fit_score BETWEEN 0 AND 1" in sql
    assert "recommended_collection_id IS NOT NULL OR new_collection_proposal <> '{}'::jsonb" in sql


def test_migration_23_enforces_approved_parent_opportunity() -> None:
    sql = MIGRATION_23.read_text()

    assert "CREATE OR REPLACE FUNCTION enforce_product_recommendation_parent_approved" in sql
    assert "CREATE CONSTRAINT TRIGGER trg_product_recommendations_parent_approved" in sql
    assert "CREATE OR REPLACE FUNCTION enforce_collection_recommendation_parent_approved" in sql
    assert "CREATE CONSTRAINT TRIGGER trg_collection_recommendations_parent_approved" in sql
    assert "co.curator_decision = 'approved'" in sql
    assert "co.hard_gate_status = 'passed'" in sql
    assert "co.policy_stale = FALSE" in sql
    assert "co.commerce_tier <> 'blocked'" in sql
    assert "DEFERRABLE INITIALLY DEFERRED" in sql


def test_migration_23_has_explainability_and_review_guards() -> None:
    sql = MIGRATION_23.read_text()

    assert "recommendation_basis <> '{}'::jsonb" in sql
    assert "fit_basis <> '{}'::jsonb" in sql
    assert "status = 'pending_curator_review'" in sql
    assert "curator_reviewed_by IS NOT NULL" in sql
    assert "trg_product_recommendations_updated_at" in sql
    assert "trg_collection_recommendations_updated_at" in sql


def test_migration_23_enforces_gate_5_before_downstream_statuses() -> None:
    sql = MIGRATION_23.read_text()

    assert "INSERT INTO commerce_recommendation_status_vocabulary" in sql
    assert "'generated'" in sql
    assert "'converted_to_collection'" in sql
    assert "CREATE OR REPLACE FUNCTION enforce_product_recommendation_gate_5" in sql
    assert "CREATE TRIGGER trg_product_recommendations_gate_5" in sql
    assert "CREATE OR REPLACE FUNCTION enforce_collection_recommendation_gate_5" in sql
    assert "CREATE TRIGGER trg_collection_recommendations_gate_5" in sql
    assert "NEW.status IN ('assigned','generated','converted_to_collection')" in sql
    assert "OLD.status IS DISTINCT FROM NEW.status" in sql
    assert "curator_decision = approved before recommendation status transition" in sql


def test_migration_23_has_replay_safe_indexes() -> None:
    sql = MIGRATION_23.read_text()

    for index_name in (
        "idx_product_recommendations_opportunity",
        "idx_product_recommendations_commerce_opportunity",
        "idx_product_recommendations_policy",
        "idx_product_recommendations_status",
        "idx_product_recommendations_family_confidence",
        "idx_collection_recommendations_opportunity",
        "idx_collection_recommendations_commerce_opportunity",
        "idx_collection_recommendations_policy",
        "idx_collection_recommendations_status",
        "idx_collection_recommendations_gap_fit",
        "uniq_collection_recommendations_existing_target",
    ):
        assert index_name in sql


def test_migration_23_excludes_downstream_generation_and_channels() -> None:
    sql = MIGRATION_23.read_text()

    assert "No scoring worker activation" in sql
    assert "No product generation" in sql
    assert "No Shopify integration" in sql
    assert "No Etsy integration" in sql
    assert "shopify" not in sql.lower().replace("no shopify integration", "")
    assert "etsy" not in sql.lower().replace("no etsy integration", "")
