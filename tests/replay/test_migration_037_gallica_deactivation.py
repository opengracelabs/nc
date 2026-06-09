"""Migration 37 Gallica deactivation replay tests."""
from pathlib import Path

MIGRATION_37 = Path("infrastructure/postgres/init/37_gallica_deactivation.sql")


def test_migration_37_deprecates_gallica_source_registry() -> None:
    sql = MIGRATION_37.read_text()

    assert "DD-GALLICA-003" in sql
    assert "ADD COLUMN IF NOT EXISTS commercial_status" in sql
    assert "'bnf_gallica'" in sql
    assert "governance_state = 'deprecated'" in sql
    assert "status = 'deprecated'" in sql
    assert "commercial_status = 'restricted'" in sql
    assert "ingestion_enabled" in sql
    assert "false" in sql


def test_migration_37_contains_retirement_note_and_keeps_research_assets() -> None:
    sql = MIGRATION_37.read_text()

    assert "Gallica retired from production source list." in sql
    assert '"code_retained": true' in sql
    assert '"tests_retained": true' in sql
    assert '"fixtures_retained": true' in sql
    assert "DELETE FROM" not in sql
    assert "DROP TABLE" not in sql
