import json
from pathlib import Path

import httpx

from workers.wikidata_adapter.client import build_entity_params, build_search_params
from workers.wikidata_adapter.entity import resolve_entity, resolve_place, resolve_qid

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "wikidata"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_wikidata_entity_params_are_stable() -> None:
    params = build_entity_params("351")

    assert params == {
        "action": "wbgetentities",
        "format": "json",
        "ids": "Q351",
        "languages": "en",
        "props": "labels|descriptions|aliases|claims|sitelinks",
    }


def test_wikidata_search_params_are_stable() -> None:
    params = build_search_params("Yellowstone National Park", limit=1)

    assert params == {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "limit": "1",
        "search": "Yellowstone National Park",
    }


async def test_wikidata_resolve_qid_returns_existing_qid_without_http() -> None:
    assert await resolve_qid("q351") == "Q351"
    assert await resolve_qid(351) == "Q351"


async def test_wikidata_resolve_entity_with_mock_client() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        action = request.url.params["action"]
        if action == "wbsearchentities":
            return httpx.Response(200, json=fixture_json("search_yellowstone.json"))
        return httpx.Response(200, json=fixture_json("entity_yellowstone.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        evidence = await resolve_entity("Yellowstone National Park", http_client=client)

    assert evidence["wikidata_qid"] == "Q351"
    assert evidence["label"] == "Yellowstone National Park"
    assert [request.url.params["action"] for request in seen] == [
        "wbsearchentities",
        "wbgetentities",
    ]


async def test_wikidata_resolve_place_uses_entity_evidence_shape() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=fixture_json("entity_yellowstone.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        evidence = await resolve_place("Q351", http_client=client)

    assert evidence["wikidata_qid"] == "Q351"
    assert evidence["source_url"] == "https://www.wikidata.org/wiki/Q351"

