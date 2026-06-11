import json
from pathlib import Path

import httpx

from workers.gbif_adapter.client import build_occurrence_search_params, search_occurrences
from workers.gbif_adapter.occurrence import (
    cap_occurrence_count,
    normalize_occurrence,
    normalize_occurrence_search_payload,
    search_occurrence_evidence,
    summarize_place_relevance,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "gbif"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_gbif_occurrence_search_params_are_stable() -> None:
    params = build_occurrence_search_params(taxon_key=5219404, country="KE", limit=50)

    assert params == {
        "country": "KE",
        "hasCoordinate": "true",
        "limit": "50",
        "offset": "0",
        "taxonKey": "5219404",
    }


def test_gbif_occurrence_normalizes_darwin_core_and_citation_fields() -> None:
    evidence = normalize_occurrence(fixture_json("occurrence_cc0.json"))

    assert evidence["record_id"] == "3001"
    assert evidence["gbif_occurrence_key"] == "3001"
    assert evidence["gbif_taxon_key"] == "5219404"
    assert evidence["basis_of_record"] == "HUMAN_OBSERVATION"
    assert evidence["dataset_doi"] == "10.15468/example.cc0"
    assert evidence["download_doi"] == "10.15468/example.cc0"
    assert evidence["citation"] == "Example Museum (2026). Open savanna observations. GBIF."
    assert evidence["rights_decision"] == "ALLOWED"
    assert evidence["darwin_core_mapping"]["event_date"] == "dwc:eventDate"
    assert evidence["source_url"] == "https://www.gbif.org/occurrence/3001"
    assert evidence["dataset_url"] == "https://www.gbif.org/dataset/dataset-cc0"
    assert len(evidence["raw_payload_hash"]) == 64


def test_gbif_occurrence_normalizes_license_variants() -> None:
    cc_by = normalize_occurrence(fixture_json("occurrence_cc_by.json"))
    cc_by_nc = normalize_occurrence(fixture_json("occurrence_cc_by_nc.json"))
    missing = normalize_occurrence(fixture_json("occurrence_missing_license.json"))

    assert cc_by["rights_decision"] == "ALLOWED"
    assert cc_by["attribution_required"] is True
    assert cc_by_nc["rights_decision"] == "REVIEW_REQUIRED"
    assert cc_by_nc["rights_basis"] == "cc_by_nc_non_commercial"
    assert missing["rights_decision"] == "BLOCKED"
    assert missing["rights_basis"] == "missing_license"


def test_gbif_occurrence_count_cap_logic() -> None:
    assert cap_occurrence_count(4) == 4
    assert cap_occurrence_count(10000) == 100
    assert cap_occurrence_count(-5) == 0

    summary = summarize_place_relevance(fixture_json("occurrence_search_page.json"))
    assert summary["source_role"] == "validation_only"
    assert summary["occurrence_count"] == 10000
    assert summary["occurrence_count_capped"] == 100
    assert summary["evidence_count"] == 2
    assert summary["taxon_keys"] == ["5219404"]


async def test_gbif_occurrence_search_integration_with_mock_client() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("occurrence_search_page.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await search_occurrences(taxon_key=5219404, limit=2, http_client=client)
        evidence = await search_occurrence_evidence(
            taxon_key=5219404,
            limit=2,
            http_client=client,
        )

    assert len(normalize_occurrence_search_payload(payload)) == 2
    assert [item["gbif_occurrence_key"] for item in evidence] == ["3001", "3002"]
    assert [request.url.path for request in seen] == [
        "/v1/occurrence/search",
        "/v1/occurrence/search",
    ]
    assert seen[0].url.params["taxonKey"] == "5219404"

