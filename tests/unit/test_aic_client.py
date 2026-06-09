from pathlib import Path

import httpx

from workers.aic_adapter.client import (
    DEFAULT_FIELDS,
    build_artwork_url,
    build_manifest_url,
    canonical_request_params,
    extract_artwork_ids,
    fetch_artwork,
    fetch_artworks,
    fetch_manifest,
    fetch_next_page,
    next_page_url,
    search_artworks,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "aic"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_canonical_request_params_drops_empty_values_and_sorts() -> None:
    assert canonical_request_params(
        {
            "fields": "id,title",
            "empty": "",
            "page": 1,
            "none": None,
            "query[term][is_public_domain]": "true",
        }
    ) == {
        "fields": "id,title",
        "page": "1",
        "query[term][is_public_domain]": "true",
    }


def test_build_urls_are_deterministic() -> None:
    assert build_artwork_url(" 27992 ") == "https://api.artic.edu/api/v1/artworks/27992"
    assert build_manifest_url(27992) == (
        "https://api.artic.edu/api/v1/artworks/27992/manifest.json"
    )


async def test_fetch_artworks_requests_paginated_artworks_endpoint_with_fields() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("artworks_public_domain_page_1.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await fetch_artworks(page=1, limit=2, fields=("id", "title"), http_client=client)

    assert seen[0].url.path == "/api/v1/artworks"
    assert seen[0].url.params["page"] == "1"
    assert seen[0].url.params["limit"] == "2"
    assert seen[0].url.params["fields"] == "id,title"
    assert seen[0].headers["user-agent"].startswith("NC-OpenGrace-Pipeline/1.0")
    assert extract_artwork_ids(response) == [27992, 14620]
    assert next_page_url(response) == "https://api.artic.edu/api/v1/artworks?page=2&limit=2"


async def test_fetch_artwork_requests_single_artwork_endpoint() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("artwork_seurat_public_domain.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await fetch_artwork("27992", fields=("id", "title"), http_client=client)

    assert seen[0].url.path == "/api/v1/artworks/27992"
    assert seen[0].url.params["fields"] == "id,title"
    assert response["data"]["id"] == 27992
    assert response["data"]["is_public_domain"] is True


async def test_search_artworks_maps_public_domain_filter_query_and_fields() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("search_public_domain_france.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await search_artworks(
            query=" France ",
            public_domain=True,
            page=3,
            limit=25,
            fields=("id", "title", "is_public_domain", "image_id"),
            http_client=client,
        )

    params = seen[0].url.params
    assert seen[0].url.path == "/api/v1/artworks/search"
    assert params["q"] == "France"
    assert params["query[term][is_public_domain]"] == "true"
    assert params["page"] == "3"
    assert params["limit"] == "25"
    assert params["fields"] == "id,title,is_public_domain,image_id"
    assert extract_artwork_ids(response) == [27992]


async def test_fetch_manifest_requests_manifest_endpoint() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("manifest_seurat.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        manifest = await fetch_manifest(27992, http_client=client)

    assert seen[0].url.path == "/api/v1/artworks/27992/manifest.json"
    assert manifest["@type"] == "sc:Manifest"


async def test_fetch_next_page_follows_pagination_next_url() -> None:
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, content=fixture("artworks_public_domain_page_2.json"))

    first_page = {
        "pagination": {
            "next_url": "https://api.artic.edu/api/v1/artworks?page=2&limit=2"
        }
    }
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await fetch_next_page(first_page, http_client=client)

    assert requests[0].url.path == "/api/v1/artworks"
    assert requests[0].url.params["page"] == "2"
    assert response is not None
    assert next_page_url(response) is None


async def test_missing_ids_are_rejected_before_request() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(500))
    async with httpx.AsyncClient(transport=transport) as client:
        for call in (fetch_artwork, fetch_manifest):
            try:
                await call(" ", http_client=client)
            except ValueError as exc:
                assert str(exc) == "missing_artwork_id"
            else:
                raise AssertionError(f"{call.__name__} accepted a blank artwork ID")


def test_helpers_handle_missing_or_malformed_pagination_and_ids() -> None:
    assert next_page_url({}) is None
    assert next_page_url({"pagination": {"next_url": ""}}) is None
    assert extract_artwork_ids({"data": [{"id": 1}, {"id": "2"}, {"id": True}, {}, "bad"]}) == [
        1,
        2,
    ]
    assert extract_artwork_ids({"data": None}) == []
    assert "is_public_domain" in DEFAULT_FIELDS
