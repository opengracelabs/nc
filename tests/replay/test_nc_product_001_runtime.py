"""NC-PRODUCT-001 Sprint 1 runtime replay tests."""
from pathlib import Path

MIGRATION_39 = Path("infrastructure/postgres/init/39_product_001_runtime.sql")


def test_product_runtime_migration_exists() -> None:
    assert MIGRATION_39.exists()


def test_product_runtime_creates_sprint1_tables_only() -> None:
    sql = MIGRATION_39.read_text(encoding="utf-8")

    for table in (
        "product_line",
        "product_template",
        "product_candidate",
        "product_publication",
    ):
        assert f"CREATE TABLE IF NOT EXISTS {table}" in sql

    assert "CREATE TABLE IF NOT EXISTS product_provider_export" not in sql
    assert "CREATE TABLE IF NOT EXISTS product_variant" not in sql
    assert "CREATE TABLE IF NOT EXISTS product_asset_link" not in sql


def test_product_runtime_is_manual_provider_only() -> None:
    sql = MIGRATION_39.read_text(encoding="utf-8")

    assert "Manual provider only" in sql
    assert "provider              TEXT NOT NULL DEFAULT 'manual' CHECK (provider = 'manual')" in sql
    assert "manual_provider_only BOOLEAN NOT NULL DEFAULT TRUE" in sql
    for forbidden in ("printful", "printify", "gelato"):
        assert forbidden in sql.lower()
        assert f'"provider":"{forbidden}"' not in sql.lower()


def test_product_runtime_seeds_requested_product_lines() -> None:
    sql = MIGRATION_39.read_text(encoding="utf-8")

    for slug in (
        "earthrise-archival-print",
        "yellowstone-map-print",
        "grand-canyon-dutton-atlas-print",
    ):
        assert f"'{slug}'" in sql


def test_product_runtime_generates_requested_candidates() -> None:
    sql = MIGRATION_39.read_text(encoding="utf-8")

    for candidate in (
        "earthrise-as08-14-2383-archival-print",
        "yellowstone-hayden-map-print",
        "grand-canyon-dutton-atlas-print",
    ):
        assert candidate in sql
    assert "source_anchor_slug" in sql
    assert "'approved'" in sql


def test_product_runtime_enforces_rights_and_source_gates() -> None:
    sql = MIGRATION_39.read_text(encoding="utf-8")

    for gate in (
        "asset_allowed",
        "open_content_proof",
        "attribution_assembled",
        "minimum_dimensions",
        "no_review_or_blocked_assets",
        "no_osm_derived_stored_data",
        "no_gbif_media",
        "no_wikidata_commons_media",
        "manual_export_idempotent",
        "provider_http_outside_transaction",
    ):
        assert gate in sql
    assert "rights_snapshot->>'rights_decision' = 'ALLOWED'" in sql
    assert "source <> 'gbif'" in sql
    assert "wikidata_commons" in sql
    assert "osm_geometry" in sql


def test_product_runtime_uses_on_conflict_for_idempotency() -> None:
    sql = MIGRATION_39.read_text(encoding="utf-8")

    assert "ON CONFLICT (slug) DO UPDATE" in sql
    assert "ON CONFLICT (product_line_id, slug) DO UPDATE" in sql
    assert "ON CONFLICT (product_line_id, candidate_key) DO UPDATE" in sql
    assert "ON CONFLICT (product_candidate_id, publication_version) DO UPDATE" in sql
    assert "UNIQUE (product_candidate_id, publication_version)" in sql


def test_product_runtime_publications_are_seeded_from_candidate_upsert() -> None:
    sql = MIGRATION_39.read_text(encoding="utf-8")

    assert "RETURNING id, candidate_key, title, assembled_attribution, gate_result" in sql
    assert "FROM seeded_candidates c" in sql
    assert "manual_export_manifest" in sql
    assert "NC-PRODUCT-001-sprint1" in sql
