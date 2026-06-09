from pathlib import Path

import httpx

from workers.cma_adapter.client import (
    DEFAULT_FIELDS,
    build_artwork_url,
    canonical_request_params,
    extract_artwork_ids,
    fetch_artwork,
    fetch_artworks,
    next_skip,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "cma"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_canonical_request_params_drops_empty_values_and_sorts() -> None:
    assert canonical_request_params(
        {
            "q": "China",
            "skip": 0,
            "limit": 2,
            "cc0": "1",
            "empty": "",
            "none": None,
        }
    ) == {
        "cc0": "1",
        "limit": "2",
        "q": "China",
        "skip": "0",
    }


def test_build_artwork_url_is_deterministic() -> None:
    assert build_artwork_url(" 94979 ") == (
        "https://openaccess-api.clevelandart.org/api/artworks/94979"
    )


async def test_fetch_artworks_requests_filtered_artworks_page() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("search_china_cc0_has_image.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await fetch_artworks(
            q=" China ",
            skip=10,
            limit=2,
            cc0=True,
            has_image=True,
            fields=("id", "title", "share_license_status", "images"),
            http_client=client,
        )

    params = seen[0].url.params
    assert seen[0].url.path == "/api/artworks"
    assert params["q"] == "China"
    assert params["skip"] == "10"
    assert params["limit"] == "2"
    assert params["cc0"] == "1"
    assert params["has_image"] == "1"
    assert params["select"] == "id,title,share_license_status,images"
    assert params["orderby"] == "id"
    assert seen[0].headers["user-agent"].startswith("NC-OpenGrace-Pipeline/1.0")
    assert extract_artwork_ids(response) == [130939, 117940]


async def test_fetch_artwork_requests_single_artwork_endpoint() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("artwork_94979_cc0.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await fetch_artwork("94979", fields=("id", "title"), http_client=client)

    assert seen[0].url.path == "/api/artworks/94979"
    assert seen[0].url.params["select"] == "id,title"
    assert extract_artwork_ids(response) == [94979]
    assert response["data"]["share_license_status"] == "CC0"


async def test_missing_inputs_are_rejected_before_request() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(500))
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            await fetch_artwork(" ", http_client=client)
        except ValueError as exc:
            assert str(exc) == "missing_artwork_id"
        else:
            raise AssertionError("fetch_artwork accepted a blank artwork ID")

        for kwargs, reason in (
            ({"skip": -1}, "invalid_skip"),
            ({"limit": 0}, "invalid_limit"),
            ({"limit": 1001}, "limit_exceeds_cma_max"),
        ):
            try:
                await fetch_artworks(http_client=client, **kwargs)
            except ValueError as exc:
                assert str(exc) == reason
            else:
                raise AssertionError(f"fetch_artworks accepted {kwargs}")


def test_pagination_and_extract_helpers_handle_terminal_pages() -> None:
    assert next_skip(
        {"info": {"total": 5, "parameters": {"skip": 0, "limit": 2}}, "data": [{}, {}]}
    ) == 2
    assert next_skip(
        {"info": {"total": 5, "parameters": {"skip": 4, "limit": 2}}, "data": [{}]}
    ) is None
    assert next_skip({"data": None}) is None
    assert extract_artwork_ids({"data": [{"id": 1}, {"id": "2"}, {"id": True}, {}, "bad"]}) == [
        1,
        2,
    ]
    assert "share_license_status" in DEFAULT_FIELDS
    assert "is_highlight" in DEFAULT_FIELDS

