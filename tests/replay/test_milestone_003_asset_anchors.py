"""MILESTONE-003 asset anchor migration tests."""
from pathlib import Path

from schemas.core.asset import Asset

MIGRATION_16 = Path("infrastructure/postgres/init/16_taxon_discovery.sql")
TABLES_01 = Path("infrastructure/postgres/init/01_tables.sql")
INGESTION_STORE = Path("workers/ingestion_worker/store.py")


def test_migration_16_adds_concept_anchor_to_assets() -> None:
    sql = MIGRATION_16.read_text()
    assert "ADD COLUMN IF NOT EXISTS concept_id UUID REFERENCES concepts(id)" in sql
    assert "ALTER COLUMN place_id DROP NOT NULL" in sql
    assert "CONSTRAINT chk_assets_anchor CHECK" in sql
    assert "concept_id IS NOT NULL OR place_id IS NOT NULL" in sql
    assert "idx_assets_concept" in sql


def test_migration_16_keeps_legacy_unesco_place_assets_valid() -> None:
    sql = MIGRATION_16.read_text()
    assert "place_id DROP NOT NULL" in sql
    assert "concept_id IS NOT NULL OR place_id IS NOT NULL" in sql
    original = TABLES_01.read_text()
    assert "place_id                UUID NOT NULL REFERENCES places(id)" in original


def test_migration_16_adds_asset_rights_schema() -> None:
    sql = MIGRATION_16.read_text()
    assert "CREATE TABLE asset_rights" in sql
    assert "asset_id            UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE" in sql
    assert "rights_status IN" in sql
    assert "'Public Domain','CC0'" in sql
    asset_rights_table = sql.split("CREATE TABLE asset_rights", 1)[1]
    asset_rights_table = asset_rights_table.split("CREATE INDEX idx_asset_rights_status", 1)[0]
    assert "rights_source_url   TEXT," in asset_rights_table
    assert "UNIQUE (asset_id)" in sql


def test_migration_16_blocks_active_commercial_assets_without_verified_rights() -> None:
    sql = MIGRATION_16.read_text()
    assert "check_commercial_asset_rights_verified" in sql
    assert "NEW.asset_type = 'bhl_illustration'" in sql
    assert "NEW.status = 'active'" in sql
    assert "has no explicit Public Domain or CC0 rights verification" in sql


def test_asset_schema_accepts_concept_or_legacy_place_anchor() -> None:
    legacy = Asset(
        place_id="00000000-0000-0000-0000-000000000001",
        source_id="unesco_whc",
        ingest_id="i",
    )
    concept = Asset(
        concept_id="00000000-0000-0000-0000-000000000002",
        source_id="bhl",
        ingest_id="i",
    )

    assert legacy.place_id is not None
    assert legacy.concept_id is None
    assert concept.place_id is None
    assert concept.concept_id is not None


def test_unesco_ingestion_still_writes_place_anchored_assets() -> None:
    source = INGESTION_STORE.read_text()
    assert "INSERT INTO assets" in source
    assert "place_id, source_id, ingest_id" in source
    assert "'site_record', 'application/json'" in source
    asset_insert_block = source[
        source.index("INSERT INTO assets"):source.index("INSERT INTO ingested_records")
    ]
    assert "concept_id" not in asset_insert_block
