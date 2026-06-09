from pathlib import Path

import httpx

from workers.met_adapter.client import (
    build_object_url,
    canonical_request_params,
    extract_object_ids,
    fetch_object,
    fetch_objects,
    search_objects,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "met"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_canonical_request_params_drops_empty_values_and_sorts() -> None:
    assert canonical_request_params(
        {
            "departmentId": 6,
            "medium": "",
            "q": "Japan",
            "isPublicDomain": "true",
            "none": None,
        }
    ) == {
        "departmentId": "6",
        "isPublicDomain": "true",
        "q": "Japan",
    }


def test_build_object_url_is_deterministic() -> None:
    assert build_object_url(" 45434 ") == (
        "https://collectionapi.metmuseum.org/public/collection/v1/objects/45434"
    )


async def test_fetch_objects_requests_department_scoped_objects_endpoint() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("objects_asian_art.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await fetch_objects(department_ids=6, http_client=client)

    assert seen[0].url.path == "/public/collection/v1/objects"
    assert seen[0].url.params["departmentIds"] == "6"
    assert seen[0].headers["user-agent"].startswith("NC-OpenGrace-Pipeline/1.0")
    assert extract_object_ids(response) == [45434, 45435, 45436]


async def test_fetch_object_requests_object_endpoint() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("object_hokusai_public_domain.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await fetch_object("45434", http_client=client)

    assert seen[0].url.path == "/public/collection/v1/objects/45434"
    assert response["objectID"] == 45434
    assert response["isPublicDomain"] is True
    assert response["primaryImage"].startswith("https://images.metmuseum.org/")


async def test_search_objects_maps_supported_search_parameters() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("search_japan_public_domain.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await search_objects(
            " Japan ",
            is_public_domain=True,
            department_id=6,
            title=True,
            tags=True,
            medium="Prints",
            has_images=True,
            geo_location="Japan",
            date_begin=1800,
            date_end=1900,
            http_client=client,
        )

    params = seen[0].url.params
    assert seen[0].url.path == "/public/collection/v1/search"
    assert params["q"] == "Japan"
    assert params["isPublicDomain"] == "true"
    assert params["departmentId"] == "6"
    assert params["title"] == "true"
    assert params["tags"] == "true"
    assert params["medium"] == "Prints"
    assert params["hasImages"] == "true"
    assert params["geoLocation"] == "Japan"
    assert params["dateBegin"] == "1800"
    assert params["dateEnd"] == "1900"
    assert extract_object_ids(response) == [45434, 45435]


async def test_missing_object_id_and_query_are_rejected_before_request() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(500))
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            await fetch_object(" ", http_client=client)
        except ValueError as exc:
            assert str(exc) == "missing_object_id"
        else:
            raise AssertionError("fetch_object accepted a blank object ID")

        try:
            await search_objects(" ", http_client=client)
        except ValueError as exc:
            assert str(exc) == "missing_query"
        else:
            raise AssertionError("search_objects accepted a blank query")


def test_extract_object_ids_ignores_malformed_values() -> None:
    assert extract_object_ids({"objectIDs": [1, "2", None, "bad", True, 3.0]}) == [1, 2, 3]
    assert extract_object_ids({"objectIDs": None}) == []
