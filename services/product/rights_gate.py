"""NC-PRODUCT-001 candidate gate verification."""

from .template import verify_template_dimensions

REQUIRED_GATE_KEYS = (
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
)


def verify_candidate_gates(candidate: dict, template: dict | None = None) -> dict:
    gate_result = candidate.get("gate_result") or {}
    checks = dict(gate_result.get("checks") or {})

    if template:
        dimension_result = verify_template_dimensions(
            candidate.get("asset_snapshot") or {}, template
        )
        checks["minimum_dimensions"] = dimension_result["passed"]

    missing = [key for key in REQUIRED_GATE_KEYS if not checks.get(key)]
    return {
        "passed": not missing,
        "checks": checks,
        "missing": missing,
    }
