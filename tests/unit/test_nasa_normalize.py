import json
from pathlib import Path

from workers.nasa_adapter.normalize import (
    build_rights_evidence,
    enrich_search_data_with_dimensions,
    normalize_record,
    normalize_search_payload,
)
from workers.nasa_adapter.rights import NO_COPYRIGHT_US_URI

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nasa"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_nasa_normalize_allowed_record_with_manifest_url_resolution() -> None:
    normalized = normalize_record(
        fixture_json("record_allowed_jsc_image.json"),
        asset_manifest=fixture_json("asset_jsc2007e034221_manifest.json"),
        metadata_location=fixture_json("metadata_jsc2007e034221_location.json"),
    )

    assert len(normalized) == 1
    item = normalized[0]
    assert item["record_id"] == "jsc2007e034221"
    assert item["rights_uri"] == NO_COPYRIGHT_US_URI
    assert item["rights_decision"] == "ALLOWED"
    assert item["representative_media_url"].endswith("jsc2007e034221~orig.jpg")
    assert item["nasa_asset_manifest_url"] == (
        "https://images-api.nasa.gov/asset/jsc2007e034221"
    )
    assert item["nasa_metadata_url"] == (
        "https://images-assets.nasa.gov/image/jsc2007e034221/metadata.json"
    )


def test_nasa_normalize_review_or_blocked_records_emit_no_candidates() -> None:
    assert normalize_record(
        fixture_json("record_jpl_review_image.json"),
        asset_manifest=fixture_json("asset_pia00001_manifest.json"),
    ) == []
    assert normalize_record(
        fixture_json("record_getty_blocked_image.json"),
        asset_manifest=fixture_json("asset_jsc2007e034221_manifest.json"),
    ) == []


def test_nasa_normalize_requires_manifest_delivery_url() -> None:
    assert normalize_record(
        fixture_json("record_allowed_jsc_image.json"),
        asset_manifest=fixture_json("asset_empty_manifest.json"),
    ) == []


def test_nasa_rights_evidence_preserves_partner_markers() -> None:
    evidence = build_rights_evidence(fixture_json("record_esa_review_image.json"))

    assert evidence["nasa_id"] == "GSFC_ESA_001"
    assert evidence["nasa_rights_uri"] == NO_COPYRIGHT_US_URI
    assert evidence["nasa_rights_basis"] == "review_partner_marker"
    assert evidence["nasa_partner_markers"] == ["ESA"]
    assert evidence["nasa_source_api"] == "images-api.nasa.gov"


def test_nasa_search_payload_normalizes_only_allowed_manifest_backed_images() -> None:
    payload = fixture_json("search_mixed_images_page.json")
    first = fixture_json("search_mixed_images_page.json")["collection"]["items"][0]
    enriched = enrich_search_data_with_dimensions(first)

    assert enriched["width"] == 1920
    assert enriched["height"] == 1280
    candidates = normalize_search_payload(
        payload,
        manifests_by_nasa_id={
            "jsc2007e034221": fixture_json("asset_jsc2007e034221_manifest.json"),
            "PIA00001": fixture_json("asset_pia00001_manifest.json"),
        },
    )
    assert [candidate["record_id"] for candidate in candidates] == ["jsc2007e034221"]


def test_nasa_rights_evidence_detects_publicity_risk() -> None:
    evidence = build_rights_evidence(fixture_json("record_publicity_risk_review_image.json"))

    assert evidence["nasa_rights_basis"] == "publicity_risk_detected"
    assert evidence["nasa_publicity_risk_detected"] is True
    assert evidence["nasa_copyright_detected"] is False
