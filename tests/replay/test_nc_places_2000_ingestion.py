import json
from pathlib import Path

from services.data.place_factory import summarize_place_factory
from services.data.place_source_connectors import export_priority_place_candidates

STORED_BATCH = Path(
    "data/curated/place_candidates/nc-places-2000-priority-sources.json"
)


def _sparql_payload(name: str, country: str, lat: str | None = None, lon: str | None = None):
    binding = {
        "name": {"value": name},
        "countryLabel": {"value": country},
    }
    if lat is not None:
        binding["lat"] = {"value": lat}
    if lon is not None:
        binding["lon"] = {"value": lon}
    return {"results": {"bindings": [binding]}}


def _replay_payload(url: str):
    if "Q9259" in url:
        return _sparql_payload("Yellowstone", "United States", "44.6", "-110.5")
    if "Q158454" in url:
        return _sparql_payload("Sian Ka'an Biosphere Reserve", "Mexico", "19.5", "-87.7")
    if "Q53444003" in url:
        return _sparql_payload("Arouca Geopark", "Portugal", "40.9", "-8.2")
    if "Q19683138" in url:
        return _sparql_payload("Okavango Delta", "Botswana", "-19.3", "22.9")
    if "Q59544" in url:
        return _sparql_payload("Pacific Wayfinding", "Multiple")
    raise AssertionError(url)


def test_nc_places_2000_exports_priority_source_candidate_batch(tmp_path):
    output = export_priority_place_candidates(_replay_payload, output_dir=tmp_path)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert Path(output).name == "nc-places-2000-priority-sources.json"
    assert len(payload) == 5
    assert {candidate["designation_family"] for candidate in payload} == {
        "UNESCO",
        "Biosphere",
        "Geopark",
        "Ramsar",
        "ICH",
    }
    assert all(candidate["authority_status"] == "source_observed" for candidate in payload)
    assert all("canonical_place_id" not in candidate for candidate in payload)


def test_nc_places_2000_stores_candidate_batch():
    payload = json.loads(STORED_BATCH.read_text(encoding="utf-8"))

    assert len(payload) == 5
    assert {candidate["source_list"] for candidate in payload} == {
        "unesco_world_heritage",
        "biosphere_reserves",
        "global_geoparks",
        "ramsar",
        "unesco_ich",
    }
    assert all(candidate["authority_status"] == "source_observed" for candidate in payload)
    assert all("canonical_place_id" not in candidate for candidate in payload)


def test_nc_places_2000_summary_is_dashboard_ready(tmp_path):
    output = export_priority_place_candidates(_replay_payload, output_dir=tmp_path)
    payload = json.loads(output.read_text(encoding="utf-8"))
    summary = summarize_place_factory(payload)

    assert summary["total_candidates"] == 5
    assert summary["authority_status_counts"] == {"source_observed": 5}
    assert summary["scale_target"] == 10000
    assert summary["canonical_identity_written"] is False
    assert set(summary["collection_readiness_counts"])
    assert set(summary["graph_readiness_counts"])
    assert set(summary["product_readiness_counts"])
