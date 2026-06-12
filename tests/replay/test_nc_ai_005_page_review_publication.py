"""NC-AI-005 review queue and publication schema replay tests."""

from pathlib import Path

MIGRATION_45 = Path("infrastructure/postgres/init/45_nc_ai_005_page_review_publication.sql")


def test_ai_page_review_publication_migration_exists() -> None:
    assert MIGRATION_45.exists()


def test_ai_page_review_publication_creates_required_tables() -> None:
    sql = MIGRATION_45.read_text(encoding="utf-8")

    assert "CREATE TABLE IF NOT EXISTS ai_page_review_queue" in sql
    assert "CREATE TABLE IF NOT EXISTS ai_page_publication_snapshot" in sql
    assert "CREATE TABLE IF NOT EXISTS ai_page_version_history" in sql


def test_ai_page_review_publication_tracks_approval_and_rollback_events() -> None:
    sql = MIGRATION_45.read_text(encoding="utf-8")

    assert "approved_generation" in sql
    assert "rollback_generation" in sql
    assert "queued_generation" in sql


def test_ai_page_review_publication_requires_human_review() -> None:
    sql = MIGRATION_45.read_text(encoding="utf-8")

    assert "human_review_required BOOLEAN NOT NULL DEFAULT TRUE" in sql
    assert "chk_ai_page_review_queue_human" in sql


def test_ai_page_publication_snapshot_preserves_attribution_and_blocks_prohibited_terms() -> None:
    sql = MIGRATION_45.read_text(encoding="utf-8")

    assert "Image credit: NASA. NASA does not endorse this product." in sql
    assert "NARA" in sql
    assert "Verified by NASA" in sql
    assert "Moran" in sql
    assert "Smithsonian" in sql
