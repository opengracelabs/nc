import json
from pathlib import Path

from workers.nasa_adapter.client import (
    build_asset_url,
    build_search_url,
    choose_asset_url,
    extract_asset_urls,
    reject_api_nasa_url,
)
from workers.nasa_adapter.normalize import (
    build_rights_evidence,
    normalize_record,
    normalize_search_payload,
)
from workers.nasa_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nasa"
NASA_ADAPTER = Path(__file__).resolve().parents[2] / "workers" / "nasa_adapter"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_nasa_g1_images_api_only_and_api_nasa_family_excluded() -> None:
    assert build_search_url() == "https://images-api.nasa.gov/search"
    assert build_asset_url("jsc2007e034221") == (
        "https://images-api.nasa.gov/asset/jsc2007e034221"
    )
    try:
        reject_api_nasa_url("https://api.nasa.gov/planetary/apod")
    except ValueError as exc:
        assert str(exc) == "api_nasa_gov_excluded"
    else:
        raise AssertionError("api.nasa.gov was accepted")


def test_nasa_g2_center_allowlist_allows_nasa_origin_image() -> None:
    rights = classify_rights(fixture_json("record_allowed_jsc_image.json"))

    assert rights["decision"] == "ALLOWED"
    assert rights["rights_basis"] == "federal_center_clean_rights"


def test_nasa_g3_jpl_is_review_required() -> None:
    rights = classify_rights(fixture_json("record_jpl_review_image.json"))

    assert rights["decision"] == "REVIEW_REQUIRED"
    assert rights["allowed"] is False
    assert rights["rights_basis"] == "review_center_jpl"


def test_nasa_g4_esa_csa_jaxa_partner_markers_are_review_required() -> None:
    for fixture in (
        "record_esa_review_image.json",
        "record_csa_review_image.json",
        "record_jaxa_review_image.json",
    ):
        rights = classify_rights(fixture_json(fixture))
        assert rights["decision"] == "REVIEW_REQUIRED"
        assert rights["rights_basis"] == "review_partner_marker"


def test_nasa_g5_getty_ap_reuters_are_blocked() -> None:
    for fixture in (
        "record_getty_blocked_image.json",
        "record_ap_blocked_image.json",
        "record_reuters_blocked_image.json",
    ):
        rights = classify_rights(fixture_json(fixture))
        assert rights["decision"] == "BLOCKED"
        assert rights["rights_basis"] == "blocked_partner_marker"


def test_nasa_g6_asset_url_resolution_uses_asset_manifest() -> None:
    urls = extract_asset_urls(fixture_json("asset_jsc2007e034221_manifest.json"))

    assert choose_asset_url(urls) == (
        "https://images-assets.nasa.gov/image/jsc2007e034221/jsc2007e034221~orig.jpg"
    )


def test_nasa_g7_mixed_replay_candidate_count_is_stable() -> None:
    candidates = normalize_search_payload(
        fixture_json("search_mixed_images_page.json"),
        manifests_by_nasa_id={
            "jsc2007e034221": fixture_json("asset_jsc2007e034221_manifest.json"),
            "PIA00001": fixture_json("asset_pia00001_manifest.json"),
        },
    )

    assert len(candidates) == 1
    assert candidates[0]["record_id"] == "jsc2007e034221"
    assert candidates[0]["representative_media_url"].endswith("~orig.jpg")


def test_nasa_g8_discovery_blocked_record_produces_no_candidates() -> None:
    writes: list[dict] = []
    for candidate in normalize_record(
        fixture_json("record_getty_blocked_image.json"),
        asset_manifest=fixture_json("asset_jsc2007e034221_manifest.json"),
    ):
        writes.append(candidate)

    assert writes == []


def test_nasa_sprint1_required_evidence_is_stable() -> None:
    evidence = build_rights_evidence(
        fixture_json("record_allowed_jsc_image.json"),
        asset_manifest=fixture_json("asset_jsc2007e034221_manifest.json"),
        metadata_location=fixture_json("metadata_jsc2007e034221_location.json"),
    )

    assert evidence == {
        "nasa_id": "jsc2007e034221",
        "nasa_center": "JSC",
        "nasa_media_type": "image",
        "nasa_rights_uri": "https://rightsstatements.org/vocab/NoC-US/1.0/",
        "nasa_rights_basis": "federal_center_clean_rights",
        "nasa_asset_manifest_url": "https://images-api.nasa.gov/asset/jsc2007e034221",
        "nasa_metadata_url": "https://images-assets.nasa.gov/image/jsc2007e034221/metadata.json",
        "nasa_original_url": "https://images-assets.nasa.gov/image/jsc2007e034221/jsc2007e034221~orig.jpg",
        "nasa_large_url": "https://images-assets.nasa.gov/image/jsc2007e034221/jsc2007e034221~large.jpg",
        "nasa_preview_url": None,
        "nasa_selected_asset_url": "https://images-assets.nasa.gov/image/jsc2007e034221/jsc2007e034221~orig.jpg",
        "nasa_photographer": None,
        "nasa_secondary_creator": None,
        "nasa_keywords": ["Apollo", "NASA"],
        "nasa_album": [],
        "nasa_partner_markers": [],
        "nasa_copyright_detected": False,
        "nasa_publicity_risk_detected": False,
        "nasa_source_api": "images-api.nasa.gov",
    }
