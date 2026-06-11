import json
from pathlib import Path

import httpx

from workers.gbif_adapter.client import build_species_match_params, species_match
from workers.gbif_adapter.identity import normalize_taxon_identity, resolve_taxon_name

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "gbif"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_gbif_species_match_params_are_stable() -> None:
    params = build_species_match_params(
        scientific_name="Panthera leo",
        rank="SPECIES",
        kingdom="Animalia",
    )

    assert params == {
        "kingdom": "Animalia",
        "name": "Panthera leo",
        "rank": "SPECIES",
    }


def test_gbif_identity_normalizes_accepted_species_match() -> None:
    evidence = normalize_taxon_identity(fixture_json("species_match_panthera_leo.json"))

    assert evidence["record_id"] == "5219404"
    assert evidence["gbif_taxon_key"] == "5219404"
    assert evidence["accepted_taxon_key"] == "5219404"
    assert evidence["scientific_name"] == "Panthera leo (Linnaeus, 1758)"
    assert evidence["taxon_rank"] == "SPECIES"
    assert evidence["synonym"] is False
    assert evidence["source_url"] == "https://www.gbif.org/species/5219404"
    assert evidence["darwin_core_mapping"]["scientific_name"] == "dwc:scientificName"
    assert len(evidence["raw_payload_hash"]) == 64


def test_gbif_identity_normalizes_synonym_to_accepted_taxon() -> None:
    evidence = normalize_taxon_identity(fixture_json("species_synonym_felis_leo.json"))

    assert evidence["synonym"] is True
    assert evidence["scientific_name"] == "Felis leo Linnaeus, 1758"
    assert evidence["accepted_scientific_name"] == "Panthera leo (Linnaeus, 1758)"
    assert evidence["accepted_taxon_key"] == "5219404"


async def test_gbif_identity_species_match_integration_with_mock_client() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("species_match_panthera_leo.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await species_match("Panthera leo", http_client=client)
        evidence = await resolve_taxon_name("Panthera leo", http_client=client)

    assert payload["usageKey"] == 5219404
    assert evidence["gbif_taxon_key"] == "5219404"
    assert [request.url.path for request in seen] == ["/v1/species/match", "/v1/species/match"]
    assert seen[0].url.params["name"] == "Panthera leo"

