"""NC-AI-004 page generation schema replay tests."""

from pathlib import Path

MIGRATION_44 = Path("infrastructure/postgres/init/44_nc_ai_004_page_generation.sql")


def test_ai_page_generation_migration_exists() -> None:
    assert MIGRATION_44.exists()


def test_ai_page_generation_creates_required_tables() -> None:
    sql = MIGRATION_44.read_text(encoding="utf-8")

    assert "CREATE TABLE IF NOT EXISTS ai_page_generation" in sql
    assert "CREATE TABLE IF NOT EXISTS ai_page_generation_snapshot" in sql


def test_ai_page_generation_schema_requires_review_and_blocks_autopublish() -> None:
    sql = MIGRATION_44.read_text(encoding="utf-8")

    assert "publication_allowed   BOOLEAN NOT NULL DEFAULT FALSE" in sql
    assert "human_review_required BOOLEAN NOT NULL DEFAULT TRUE" in sql
    assert "chk_ai_page_generation_human_review" in sql
    assert "chk_ai_page_snapshot_human_review" in sql


def test_ai_page_generation_schema_preserves_sources_and_attribution() -> None:
    sql = MIGRATION_44.read_text(encoding="utf-8")

    assert "jsonb_array_length(source_references) > 0" in sql
    assert "Image credit: NASA. NASA does not endorse this product." in sql
    assert "chk_ai_page_snapshot_attribution" in sql


def test_ai_page_generation_schema_blocks_prohibited_earthrise_phrases() -> None:
    sql = MIGRATION_44.read_text(encoding="utf-8")

    assert "NARA" in sql
    assert "National Archives" in sql
    assert "Verified by NASA" in sql
    assert "Moran" in sql
    assert "Smithsonian" in sql
