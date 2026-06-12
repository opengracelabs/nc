"""NC-AI-001 schema replay tests."""

from pathlib import Path

MIGRATION_43 = Path("infrastructure/postgres/init/43_nc_ai_001_runtime.sql")


def test_ai_runtime_migration_exists() -> None:
    assert MIGRATION_43.exists()


def test_ai_runtime_creates_required_tables() -> None:
    sql = MIGRATION_43.read_text(encoding="utf-8")

    for table in (
        "ai_model_registry",
        "ai_task_policy",
        "ai_prompt_template",
        "ai_generation_request",
        "ai_generation_result",
        "ai_grounding_source",
        "ai_model_route_decision",
        "ai_human_review",
        "ai_audit_event",
    ):
        assert f"CREATE TABLE IF NOT EXISTS {table}" in sql


def test_ai_runtime_blocks_autopublish_and_external_calls() -> None:
    sql = MIGRATION_43.read_text(encoding="utf-8")

    assert "external_calls_allowed BOOLEAN NOT NULL DEFAULT FALSE" in sql
    assert "publication_allowed = FALSE" in sql
    assert "human_review_required = TRUE" in sql
    assert "CONSTRAINT chk_ai_model_no_paid_calls" in sql
    assert "CONSTRAINT chk_ai_result_no_autopublish" in sql


def test_ai_runtime_enforces_banned_media_policies() -> None:
    sql = MIGRATION_43.read_text(encoding="utf-8")

    assert "chk_ai_grounding_no_gbif_media" in sql
    assert "chk_ai_grounding_no_wikidata_commons_product_safe" in sql
    assert "chk_ai_grounding_osm_display_only" in sql


def test_ai_runtime_seeds_required_task_policies() -> None:
    sql = MIGRATION_43.read_text(encoding="utf-8")

    assert "'rights_governance', 'claude_policy', 'claude'" in sql
    assert "'product_copy', 'narrative_policy', 'openai'" in sql
    assert "'code_generation', 'codex_policy', 'codex'" in sql
    assert "'public_website_copy', 'narrative_policy', 'openai'" in sql
    assert "'user_assistant', 'assistant_policy', 'openai'" in sql
