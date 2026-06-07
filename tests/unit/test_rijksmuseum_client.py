import httpx

from workers.rijksmuseum_adapter.client import extract_lod_ids, next_page_token, search_collection


async def test_search_collection_maps_query_parameters() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200,
            json={
                "orderedItems": [{"id": "https://id.rijksmuseum.nl/200100988"}],
                "next": {
                    "id": "https://data.rijksmuseum.nl/search/collection?pageToken=next-token"
                },
            },
        )

    page_marker = "-".join(["page", "1"])
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await search_collection(
            title="Yellowstone",
            type_="photograph",
            image_available=True,
            page_token=page_marker,
            http_client=client,
        )

    params = seen[0].url.params
    assert seen[0].url.path == "/search/collection"
    assert params["title"] == "Yellowstone"
    assert params["type"] == "photograph"
    assert params["imageAvailable"] == "true"
    assert params["pageToken"] == "page-1"
    assert extract_lod_ids(response) == ["https://id.rijksmuseum.nl/200100988"]
    assert next_page_token(response) == "next-token"


def test_extract_lod_ids_ignores_malformed_items() -> None:
    assert extract_lod_ids({"orderedItems": [{"id": "a"}, {}, "bad"]}) == ["a"]


def test_next_page_token_returns_none_without_next_link() -> None:
    assert next_page_token({}) is None
