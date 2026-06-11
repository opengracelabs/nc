import json
from pathlib import Path

import httpx

from workers.geonames_adapter.client import build_lookup_params, build_search_params
from workers.geonames_adapter.place import resolve_geonames_id, resolve_place

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "geonames"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_geonames_lookup_params_are_stable() -> None:
    params = build_lookup_params("5843591", username="nc-test")

    assert params == {"geonameId": "5843591", "username": "nc-test"}


def test_geonames_search_params_are_stable() -> None:
    params = build_search_params(
        "Yellowstone National Park",
        country="US",
        feature_code="PRKA",
        max_rows=1,
        username="nc-test",
    )

    assert params == {
        "country": "US",
        "fcode": "PRKA",
        "maxRows": "1",
        "q": "Yellowstone National Park",
        "username": "nc-test",
    }


async def test_geonames_resolve_id_returns_existing_id_without_http() -> None:
    assert await resolve_geonames_id("5843591") == "5843591"
    assert await resolve_geonames_id(5843591) == "5843591"


async def test_geonames_resolve_place_with_mock_client() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path.endswith("/searchJSON"):
            return httpx.Response(200, json=fixture_json("search_yellowstone.json"))
        if request.url.path.endswith("/hierarchyJSON"):
            return httpx.Response(200, json=fixture_json("hierarchy_yellowstone.json"))
        return httpx.Response(200, json=fixture_json("place_yellowstone.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        evidence = await resolve_place(
            "Yellowstone National Park",
            country="US",
            feature_code="PRKA",
            username="nc-test",
            http_client=client,
        )

    assert evidence["geonames_id"] == "5843591"
    assert evidence["feature_code"] == "PRKA"
    assert evidence["coordinates"] == {"latitude": 44.42796, "longitude": -110.58846}
    assert [request.url.path for request in seen] == [
        "/searchJSON",
        "/getJSON",
        "/hierarchyJSON",
    ]

