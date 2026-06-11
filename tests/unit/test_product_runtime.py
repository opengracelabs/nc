from services.api.main import app
from services.product.export import build_product_snapshot_export, build_publication_snapshot
from services.product.provider.manual import (
    build_manual_export_manifest,
    build_manual_export_package,
)
from services.product.rights_gate import verify_candidate_gates
from services.product.state_machine import activation_actions, transition_activation_state
from services.product.template import verify_template_dimensions


def test_product_router_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/products/lines" in paths
    assert "/products/lines/{line_slug}" in paths
    assert "/products/candidates" in paths
    assert "/products/candidates/{candidate_id}" in paths
    assert "/products/candidates/{candidate_id}/verify" in paths
    assert "/products/publications" in paths
    assert "/products/publications/{publication_id}" in paths
    assert "/products/publications/{publication_id}/manual-export" in paths
    assert "/products/publications/{publication_id}/snapshot-export" in paths
    assert "/products/publications/{publication_id}/packages" in paths
    assert "/products/publications/{publication_id}/audit-events" in paths
    assert "/products/publications/{publication_id}/workflow" in paths
    assert "/products/first-sale-activations" in paths
    assert "/products/production-packages" in paths
    assert "/products/health" in paths


def test_template_dimension_gate_passes_for_large_asset() -> None:
    result = verify_template_dimensions(
        {"width_px": 6000, "height_px": 6000},
        {"min_width_px": 3600, "min_height_px": 4800},
    )

    assert result["passed"] is True
    assert result["missing"] == []


def test_template_dimension_gate_fails_for_small_asset() -> None:
    result = verify_template_dimensions(
        {"width_px": 1200, "height_px": 1200},
        {"min_width_px": 3600, "min_height_px": 4800},
    )

    assert result["passed"] is False
    assert result["missing"] == ["minimum_image_dimensions"]


def test_candidate_gate_verification_passes_manual_export_candidate() -> None:
    candidate = {
        "asset_snapshot": {"width_px": 6000, "height_px": 6000},
        "gate_result": {
            "checks": {
                "asset_allowed": True,
                "open_content_proof": True,
                "attribution_assembled": True,
                "minimum_dimensions": True,
                "no_review_or_blocked_assets": True,
                "no_osm_derived_stored_data": True,
                "no_gbif_media": True,
                "no_wikidata_commons_media": True,
                "manual_export_idempotent": True,
                "provider_http_outside_transaction": True,
            }
        },
    }

    result = verify_candidate_gates(candidate, {"min_width_px": 3600, "min_height_px": 4800})

    assert result["passed"] is True
    assert result["missing"] == []


def test_candidate_gate_verification_rejects_missing_gate() -> None:
    result = verify_candidate_gates(
        {"asset_snapshot": {"width_px": 6000, "height_px": 6000}, "gate_result": {"checks": {}}},
        {"min_width_px": 3600, "min_height_px": 4800},
    )

    assert result["passed"] is False
    assert "asset_allowed" in result["missing"]
    assert "provider_http_outside_transaction" in result["missing"]


def test_publication_snapshot_is_deterministic() -> None:
    candidate = {
        "candidate_key": "earthrise-as08-14-2383-archival-print",
        "title": "Earthrise AS08-14-2383 Archival Print",
        "asset_snapshot": {"width_px": 6000, "height_px": 6000},
        "assembled_attribution": [{"source": "nasa", "statement": "Image credit: NASA."}],
        "gate_result": {
            "checks": {
                "asset_allowed": True,
                "open_content_proof": True,
                "attribution_assembled": True,
                "minimum_dimensions": True,
                "no_review_or_blocked_assets": True,
                "no_osm_derived_stored_data": True,
                "no_gbif_media": True,
                "no_wikidata_commons_media": True,
                "manual_export_idempotent": True,
                "provider_http_outside_transaction": True,
            }
        },
    }
    template = {"slug": "earthrise-18x24-manual", "min_width_px": 3600, "min_height_px": 4800}

    first = build_publication_snapshot(candidate, template)
    second = build_publication_snapshot(candidate, template)

    assert first == second
    assert len(first["snapshot_sha256"]) == 64


def test_manual_export_manifest_is_deterministic() -> None:
    publication = {
        "id": "00000000-0000-0000-0000-000000000001",
        "publication_version": "sprint1-v1",
        "snapshot_sha256": "a" * 64,
        "snapshot": {
            "candidate_key": "earthrise-as08-14-2383-archival-print",
            "title": "Earthrise AS08-14-2383 Archival Print",
            "assembled_attribution": [{"source": "nasa", "statement": "Image credit: NASA."}],
        },
    }

    first = build_manual_export_manifest(publication)
    second = build_manual_export_manifest(publication)

    assert first == second
    assert first["provider"] == "manual"
    assert first["candidate_key"] == "earthrise-as08-14-2383-archival-print"
    assert len(first["manifest_sha256"]) == 64


def test_activation_state_machine_allows_expected_path() -> None:
    assert transition_activation_state("ready", "package") == "packaged"
    assert transition_activation_state("packaged", "activate") == "activated"
    assert transition_activation_state("activated", "pause") == "paused"
    assert transition_activation_state("paused", "resume") == "activated"
    assert transition_activation_state("activated", "retract") == "retracted"
    assert activation_actions("ready") == ["package", "retract"]


def test_activation_state_machine_rejects_invalid_transition() -> None:
    try:
        transition_activation_state("ready", "activate")
    except ValueError as exc:
        assert "Cannot apply action" in str(exc)
    else:
        raise AssertionError("invalid transition should fail")


def test_manual_export_package_contains_snapshot_and_attribution_files() -> None:
    publication = {
        "id": "00000000-0000-0000-0000-000000000002",
        "publication_version": "sprint1-v1",
        "snapshot_sha256": "b" * 64,
        "snapshot": {
            "candidate_key": "yellowstone-hayden-map-print",
            "title": "Yellowstone Hayden Survey Map Print",
            "assembled_attribution": [
                {"source": "nara", "statement": "Source: U.S. National Archives."}
            ],
        },
    }

    package = build_manual_export_package(publication)

    assert package["provider"] == "manual"
    assert package["candidate_key"] == "yellowstone-hayden-map-print"
    assert {item["path"] for item in package["files"]} == {
        "snapshot.json",
        "attribution.json",
        "README.txt",
    }
    assert len(package["package_sha256"]) == 64


def test_product_snapshot_export_is_deterministic() -> None:
    publication = {
        "snapshot": {
            "candidate_key": "grand-canyon-dutton-atlas-print",
            "title": "Grand Canyon Dutton Atlas Print",
        }
    }

    first = build_product_snapshot_export(publication)
    second = build_product_snapshot_export(publication)

    assert first == second
    assert first["filename"] == "grand-canyon-dutton-atlas-print-snapshot.json"
    assert len(first["snapshot_sha256"]) == 64
