import json
from pathlib import Path

from workers.nasa_adapter.client import choose_asset_url, extract_asset_urls
from workers.nasa_adapter.normalize import enrich_search_data_with_dimensions, normalize_record
from workers.nasa_adapter.rights import CENTER_ALLOWLIST, classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nasa"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def _assert_g6_live_sample(snapshot: dict, *, expected_nasa_id: str) -> dict:
    record = enrich_search_data_with_dimensions(snapshot["item"])
    manifest = snapshot["asset_manifest"]
    verification = snapshot["verification"]
    rights = classify_rights(record)
    selected_asset_url = choose_asset_url(extract_asset_urls(manifest))
    candidates = normalize_record(record, asset_manifest=manifest)

    assert snapshot["source_api"] == "images-api.nasa.gov"
    assert record["nasa_id"] == expected_nasa_id
    assert record["media_type"] == "image"
    assert record["center"] in CENTER_ALLOWLIST
    assert rights["decision"] == "ALLOWED"
    assert rights["rights_basis"] == verification["expected_rights_basis"]
    assert selected_asset_url is not None
    assert selected_asset_url.startswith("https://")
    assert selected_asset_url.endswith("~orig.jpg")
    assert len(candidates) == 1
    assert candidates[0]["record_id"] == expected_nasa_id
    assert candidates[0]["representative_media_url"] == selected_asset_url
    assert candidates[0]["nasa_rights_basis"] == "federal_center_clean_rights"
    assert verification["expected_pilot_eligible"] is True
    return candidates[0]


def test_nasa_g6_yellowstone_live_sample_fixture() -> None:
    candidate = _assert_g6_live_sample(
        fixture_json("live_g6_yellowstone_sample_fixture.json"),
        expected_nasa_id="sts068-247-061",
    )

    assert candidate["title"] == "Yellowstone Lake/National Park"
    assert candidate["nasa_center"] == "JSC"


def test_nasa_g6_grand_canyon_live_sample_fixture() -> None:
    candidate = _assert_g6_live_sample(
        fixture_json("live_g6_grand_canyon_sample_fixture.json"),
        expected_nasa_id="SL2-04-018",
    )

    assert candidate["title"] == "Lake Powell, Colorado River, Utah and Grand Canyon, Arizona"
    assert candidate["nasa_center"] == "JSC"
