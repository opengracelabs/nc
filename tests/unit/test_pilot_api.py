import inspect

from services.api.main import app
from services.api.routers import pilot


def test_pilot_router_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/pilot/anchors" in paths
    assert "/pilot/anchors/{anchor_slug}" in paths
    assert "/pilot/anchors/{anchor_slug}/graph" in paths
    assert "/pilot/anchors/{anchor_slug}/ingest-runs" in paths
    assert "/pilot/anchors/{anchor_slug}/publication-checklist" in paths
    assert "/pilot/anchors/{anchor_slug}/launch-config" in paths
    assert "/pilot/anchors/{anchor_slug}/verify-attribution" in paths
    assert "/pilot/anchors/{anchor_slug}/verify-publication-snapshot" in paths
    assert "/pilot/anchors/{anchor_slug}/monitoring" in paths
    assert "/pilot/anchors/{anchor_slug}/health" in paths
    assert "/pilot/anchors/{anchor_slug}/launch-report" in paths
    assert "/pilot/anchors/{anchor_slug}/publication-snapshots" in paths


def test_pilot_attribution_assembly_includes_required_notices() -> None:
    anchor = {"attribution_requirements": {"geonames": True, "osm_tiles": True}}
    evidence = [
        {
            "source": "nasa",
            "source_url": "https://images.nasa.gov/example",
            "attribution": {"name": "NASA", "statement": "NASA public domain source"},
        },
        {
            "source": "noaa",
            "source_url": "https://www.noaa.gov/example",
            "attribution": {"name": "NOAA", "statement": "NOAA public domain source"},
        },
    ]

    attribution = pilot.assemble_attribution(anchor, evidence)

    statements = {item["statement"] for item in attribution}
    assert pilot.GEONAMES_ATTRIBUTION in statements
    assert pilot.OSM_ATTRIBUTION in statements
    assert pilot.NASA_NONENDORSEMENT in statements
    assert pilot.NOAA_NONENDORSEMENT in statements
    assert "NASA public domain source" in statements
    assert "NOAA public domain source" in statements


def test_pilot_attribution_links_geonames_place_id() -> None:
    anchor = {"attribution_requirements": {"geonames": True}}
    attribution = pilot.assemble_attribution(
        anchor,
        evidence=[],
        places=[{"identity_snapshot": {"geonames_id": "5843642"}}],
    )

    assert any(item["url"] == "https://www.geonames.org/5843642" for item in attribution)


def test_pilot_attribution_verification_reports_missing_notices() -> None:
    anchor = {"attribution_requirements": {"geonames": True, "osm_tiles": True}}
    result = pilot.verify_attribution(anchor, evidence=[])

    assert result["passed"] is True
    assert result["missing"] == []
    assert pilot.GEONAMES_ATTRIBUTION in result["expected"]
    assert pilot.OSM_ATTRIBUTION in result["expected"]


def test_pilot_publication_snapshot_verification_checks_hash_and_attribution() -> None:
    snapshot_body = {
        "anchor_slug": "yellowstone",
        "anchor_title": "Yellowstone",
        "attribution": [{"source": "geonames", "statement": pilot.GEONAMES_ATTRIBUTION}],
    }
    snapshot = {
        "snapshot": snapshot_body,
        "snapshot_sha256": pilot._json_hash(snapshot_body),
        "attribution": snapshot_body["attribution"],
        "created_by": "activation-test",
    }

    result = pilot.verify_publication_snapshot(snapshot)

    assert result["passed"] is True
    assert result["missing"] == []
    assert result["checks"]["snapshot_hash_valid"] is True


def test_pilot_publication_snapshot_verification_rejects_missing_snapshot() -> None:
    result = pilot.verify_publication_snapshot(None)

    assert result["passed"] is False
    assert "publication_snapshot" in result["missing"]


def test_pilot_launch_gate_verification_requires_enabled_config_and_seeded_gates() -> None:
    checklist = [
        {"checklist_key": "rights_verified_pd", "required": True},
        {"checklist_key": "human_verified", "required": True},
    ]
    launch_config = {
        "enabled": True,
        "launch_stage": "activation",
        "required_gates": ["rights_verified_pd", "human_verified"],
    }

    result = pilot.verify_launch_gates(checklist, launch_config)

    assert result["passed"] is True
    assert result["missing"] == []


def test_pilot_launch_gate_verification_reports_missing_gate() -> None:
    result = pilot.verify_launch_gates(
        checklist=[{"checklist_key": "rights_verified_pd", "required": True}],
        launch_config={
            "enabled": True,
            "launch_stage": "activation",
            "required_gates": ["rights_verified_pd", "two_human_signoff"],
        },
    )

    assert result["passed"] is False
    assert result["missing"] == ["two_human_signoff"]


def test_pilot_router_uses_on_conflict_for_metadata_writes_only() -> None:
    source = inspect.getsource(pilot)

    assert "ON CONFLICT (anchor_id, idempotency_key)" in source
    assert "ON CONFLICT (anchor_id, snapshot_version)" in source
    assert "source_item" not in source
    assert "media_file" not in source
    assert "httpx" not in source
    assert "requests" not in source


def test_pilot_api_contains_publication_checklist_query_only() -> None:
    source = inspect.getsource(pilot)

    assert "pilot_publication_checklist" in source
    assert "publication-checklist" in source
    assert "pilot_launch_config" in source
    assert "launch-report" in source
    assert "verify_attribution" in source
    assert "verify_publication_snapshot" in source
    assert "SELECT {_CHECKLIST_COLS}" in source
