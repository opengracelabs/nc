"""Migration 22 score audit log replay tests."""
from pathlib import Path


MIGRATION_22 = Path("infrastructure/postgres/init/22_score_audit_log.sql")


def test_migration_22_exists() -> None:
    assert MIGRATION_22.exists()


def test_migration_22_creates_hybrid_score_audit_log() -> None:
    sql = MIGRATION_22.read_text()

    assert "CREATE TABLE IF NOT EXISTS score_audit_log" in sql
    for field in (
        "opportunity_id              UUID NOT NULL REFERENCES illustration_opportunities(id)",
        "policy_version_id           UUID NOT NULL REFERENCES commerce_policy(id)",
        "event_type                  TEXT NOT NULL REFERENCES commerce_audit_event_type_vocabulary(value)",
        "actor_type                  TEXT NOT NULL REFERENCES commerce_actor_type_vocabulary(value)",
        "actor_id                    TEXT NOT NULL",
        "trigger                     TEXT NOT NULL REFERENCES commerce_computation_trigger_vocabulary(value)",
        "score_inputs                JSONB NOT NULL DEFAULT '{}'",
        "score_outputs               JSONB NOT NULL DEFAULT '{}'",
        "previous_state              JSONB NOT NULL DEFAULT '{}'",
        "new_state                   JSONB NOT NULL DEFAULT '{}'",
        "entry_checksum_sha256       TEXT NOT NULL",
        "previous_entry_checksum     TEXT",
        "reason                      TEXT NOT NULL",
        "generated_by                TEXT NOT NULL",
    ):
        assert field in sql


def test_migration_22_enforces_append_only_rules() -> None:
    sql = MIGRATION_22.read_text()

    assert "CREATE OR REPLACE RULE score_audit_log_no_update" in sql
    assert "ON UPDATE TO score_audit_log" in sql
    assert "CREATE OR REPLACE RULE score_audit_log_no_delete" in sql
    assert "ON DELETE TO score_audit_log" in sql
    assert "commerce_raise_exception" in sql
    assert "no UPDATE permitted on score_audit_log" in sql
    assert "no DELETE permitted on score_audit_log" in sql
    assert "CREATE ROLE" not in sql
    assert "REVOKE" not in sql


def test_migration_22_enforces_audit_hash_chain() -> None:
    sql = MIGRATION_22.read_text()

    assert "entry_checksum_sha256 ~ '^[0-9a-f]{64}$'" in sql
    assert "previous_entry_checksum IS NULL OR previous_entry_checksum ~ '^[0-9a-f]{64}$'" in sql
    assert "CREATE OR REPLACE FUNCTION enforce_score_audit_hash_chain" in sql
    assert "ORDER BY event_at DESC, created_at DESC, id DESC" in sql
    assert "previous_entry_checksum must match latest score_audit_log entry" in sql
    assert "CREATE TRIGGER trg_score_audit_hash_chain" in sql


def test_migration_22_enforces_required_audit_context() -> None:
    sql = MIGRATION_22.read_text()

    assert "length(actor_id) > 0" in sql
    assert "length(reason) > 0" in sql
    assert "length(generated_by) > 0" in sql
    assert "actor_type <> 'curator'" in sql
    assert "actor_notes IS NOT NULL" in sql


def test_migration_22_adds_deferred_commerce_score_audit_gate() -> None:
    sql = MIGRATION_22.read_text()

    assert "CREATE OR REPLACE FUNCTION enforce_commerce_opportunity_audit_exists" in sql
    assert "commerce_opportunity_score IS NOT NULL" in sql
    assert "FROM score_audit_log sal" in sql
    assert "sal.opportunity_id = NEW.opportunity_id" in sql
    assert "sal.policy_version_id = NEW.policy_version_id" in sql
    assert "CREATE CONSTRAINT TRIGGER trg_commerce_opportunities_audit_exists" in sql
    assert "DEFERRABLE INITIALLY DEFERRED" in sql


def test_migration_22_remains_runtime_only() -> None:
    sql = MIGRATION_22.read_text()

    assert "No scoring worker activation" in sql
    assert "No product generation" in sql
    assert "No Shopify integration" in sql
    assert "No Etsy integration" in sql
    assert "CREATE TABLE IF NOT EXISTS product_recommendations" not in sql
    assert "CREATE TABLE IF NOT EXISTS collection_recommendations" not in sql
