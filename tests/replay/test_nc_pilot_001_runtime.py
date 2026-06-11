"""NC-PILOT-001 runtime replay tests."""
from pathlib import Path

MIGRATION_38 = Path("infrastructure/postgres/init/38_pilot_001_runtime.sql")
BLUEPRINT = Path("docs/implementation/nc_pilot_001_experience_blueprint.md")


def test_pilot_runtime_migration_exists() -> None:
    assert MIGRATION_38.exists()


def test_pilot_runtime_creates_required_tables() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")
    for table in (
        "pilot_anchor",
        "pilot_ingest_run",
        "anchor_place",
        "anchor_evidence",
        "pilot_publication_snapshot",
        "pilot_launch_config",
        "pilot_publication_checklist",
    ):
        assert f"CREATE TABLE IF NOT EXISTS {table}" in sql


def test_pilot_runtime_seeds_activation_launch_config() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")

    assert "CREATE TABLE IF NOT EXISTS pilot_launch_config" in sql
    assert "'nc_pilot_001_activation'" in sql
    assert "TRUE, 'activation'" in sql
    assert "monitor_window_minutes" in sql
    assert "require_snapshot_hash" in sql
    assert "require_attribution" in sql
    assert "ON CONFLICT (config_key) DO UPDATE" in sql


def test_pilot_runtime_activation_config_contains_all_launch_gates() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")

    for gate in (
        "rights_verified_pd",
        "human_verified",
        "source_authority_active",
        "nasa_noaa_nonendorsement",
        "geonames_attribution",
        "osm_attribution",
        "geonames_id_written",
        "two_human_signoff",
    ):
        assert f"'{gate}'" in sql


def test_pilot_runtime_seeds_all_target_anchors() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")
    for slug in (
        "yellowstone",
        "grand-canyon",
        "great-barrier-reef",
        "papahanaumokuakea",
        "venice",
        "galapagos",
        "earthrise",
    ):
        assert f"'{slug}'" in sql


def test_pilot_runtime_resolves_geonames_identity_conflicts() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")

    assert '"preferred_geonames_id":"5843642"' in sql
    assert '"preferred_geonames_id":"5296401"' in sql
    assert '"preferred_wikidata_qid":"Q220289"' in sql
    assert '"preferred_geonames_id":"2164628"' in sql
    assert '"preferred_geonames_id":"3164603"' in sql
    assert '"preferred_geonames_id":"3658931"' in sql
    assert '"preferred_wikidata_qid":"Q787425"' in sql
    assert '"geonames_status":"unconfirmed"' in sql
    assert '"preferred_geonames_id":"5843591"' not in sql
    assert '"preferred_wikidata_qid":"Q118841"' not in sql


def test_pilot_runtime_marks_venice_partial_launch() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")

    assert "('partial_launch'," in sql
    assert "('venice', 'Venice', 'place', 'partial_launch'" in sql
    assert "editorial-only until rights and source authority gates pass" in sql


def test_pilot_runtime_builds_publication_checklist() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")

    for key in (
        "rights_verified_pd",
        "human_verified",
        "source_authority_active",
        "nasa_noaa_nonendorsement",
        "geonames_attribution",
        "osm_attribution",
        "geonames_id_written",
        "two_human_signoff",
    ):
        assert f"'{key}'" in sql
    assert "ON CONFLICT (checklist_key) DO UPDATE" in sql


def test_pilot_runtime_has_governed_attribution_assertions() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")

    assert "Geographic data © GeoNames (geonames.org) — CC BY 4.0" in sql
    assert "© OpenStreetMap contributors" in sql
    assert "Image credit: NASA. NASA does not endorse this product." in sql
    assert "Image: NOAA. NOAA does not endorse this product." in sql


def test_pilot_runtime_removes_esa_only_launch_asset() -> None:
    blueprint = BLUEPRINT.read_text(encoding="utf-8")
    sql = MIGRATION_38.read_text(encoding="utf-8")

    assert "NASA/ESA" not in blueprint
    assert "Copernicus Sentinel-2" not in blueprint
    assert "ESA-only" not in blueprint
    assert "excluded pending ESA source authority" in blueprint
    assert "copernicus_sentinel_2_lagoon_esa_only" in sql


def test_pilot_runtime_uses_on_conflict_for_idempotency() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")
    assert "ON CONFLICT (slug) DO UPDATE" in sql
    assert "UNIQUE (anchor_id, idempotency_key)" in sql
    assert "UNIQUE (anchor_id, source, raw_payload_hash)" in sql
    assert "UNIQUE (anchor_id, snapshot_version)" in sql
    assert "UNIQUE" in sql and "config_key" in sql


def test_pilot_runtime_has_recovery_and_no_osm_storage_guards() -> None:
    sql = MIGRATION_38.read_text(encoding="utf-8")
    assert "stale_after" in sql
    assert "recovery_notes" in sql
    assert "chk_anchor_place_no_osm_storage" in sql
    assert "chk_anchor_evidence_no_osm_vectors" in sql
    assert "No external HTTP" in sql
    assert "No source onboarding" in sql
    assert "metadata-only launch configuration; no source onboarding" in sql
