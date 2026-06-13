import json

from services.data.place_source_connectors import (
    BIOSPHERE_SPARQL,
    GEOPARK_SPARQL,
    RAMSAR_SPARQL,
    UNESCO_ICH_SPARQL,
    WORLD_HERITAGE_SPARQL,
    export_priority_place_candidates,
    ingest_priority_place_sources,
    priority_place_source_connectors,
)


def _payload_for_url(url: str):
    if "Q9259" in url:
        return _sparql_payload("Test World Heritage Site", "Testland", "45.1", "7.2")
    if "Q158454" in url:
        return _sparql_payload("Test Biosphere Reserve", "Testland", "46.1", "8.2")
    if "Q53444003" in url:
        return _sparql_payload("Test Global Geopark", "Testland", "47.1", "9.2")
    if "Q59544" in url:
        return _sparql_payload("Test Oral Tradition", "Testland", None, None)
    if "Q19683138" in url:
        return _sparql_payload("Test Ramsar Wetland", "Testland", "-1.5", "35.2")
    raise AssertionError(f"unexpected url: {url}")


def _sparql_payload(name: str, country: str, lat: str | None, lon: str | None):
    binding = {
        "name": {"value": name},
        "countryLabel": {"value": country},
    }
    if lat is not None:
        binding["lat"] = {"value": lat}
    if lon is not None:
        binding["lon"] = {"value": lon}
    return {"results": {"bindings": [binding]}}


def test_priority_place_source_connectors_cover_required_sources():
    connectors = priority_place_source_connectors()

    assert [connector.source_list for connector in connectors] == [
        "unesco_world_heritage",
        "biosphere_reserves",
        "global_geoparks",
        "ramsar",
        "unesco_ich",
    ]
    assert {connector.designation_type for connector in connectors} == {
        "UNESCO",
        "Biosphere",
        "Geopark",
        "Ramsar",
        "ICH",
    }


def test_sparql_queries_use_expected_wikidata_classes_and_designations():
    assert "Q9259" in WORLD_HERITAGE_SPARQL
    assert "Q158454" in BIOSPHERE_SPARQL
    assert "Q53444003" in GEOPARK_SPARQL
    assert "Q19683138" in RAMSAR_SPARQL
    assert "Q59544" in UNESCO_ICH_SPARQL


def test_ingest_priority_place_sources_maps_real_source_payloads():
    candidates = ingest_priority_place_sources(_payload_for_url)

    assert len(candidates) == 5
    assert {candidate["designation_family"] for candidate in candidates} == {
        "UNESCO",
        "Biosphere",
        "Geopark",
        "Ramsar",
        "ICH",
    }
    assert all(candidate["authority_status"] == "source_observed" for candidate in candidates)
    assert all("canonical_place_id" not in candidate for candidate in candidates)
    assert {candidate["source_list"] for candidate in candidates} == {
        "unesco_world_heritage",
        "biosphere_reserves",
        "global_geoparks",
        "ramsar",
        "unesco_ich",
    }


def test_export_priority_place_candidates_writes_batch(tmp_path):
    output = export_priority_place_candidates(_payload_for_url, output_dir=tmp_path)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert output.name == "nc-places-2000-priority-sources.json"
    assert len(payload) == 5
    assert all(candidate["authority_status"] == "source_observed" for candidate in payload)
    assert all("canonical_identity" not in candidate for candidate in payload)
