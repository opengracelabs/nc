from pathlib import Path

import httpx

from workers.smk_adapter.client import (
    DEFAULT_FIELDS,
    build_manifest_url,
    build_object_url,
    canonical_request_params,
    extract_object_numbers,
    fetch_manifest,
    fetch_object,
    next_offset,
    search_artworks,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "smk"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_canonical_request_params_drops_empty_values_and_sorts() -> None:
    assert canonical_request_params(
        {
            "keys": "*",
            "filters": "[has_image:true],[public_domain:true]",
            "empty": "",
            "none": None,
            "offset": 0,
        }
    ) == {
        "filters": "[has_image:true],[public_domain:true]",
        "keys": "*",
        "offset": "0",
    }


def test_build_urls_are_deterministic() -> None:
    assert build_object_url(" KMS1 ") == "https://api.smk.dk/api/v1/art/?object_number=KMS1"
    assert build_manifest_url("KMS1") == "https://api.smk.dk/api/v1/iiif/manifest?object_number=KMS1"


async def test_search_artworks_requests_public_domain_image_page() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("search_public_domain_has_image.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await search_artworks(
            offset=20,
            rows=2,
            fields=("object_number", "public_domain", "image_native"),
            sort="object_number",
            http_client=client,
        )

    params = seen[0].url.params
    assert seen[0].url.path == "/api/v1/art/search/"
    assert params["keys"] == "*"
    assert params["filters"] == "[has_image:true],[public_domain:true]"
    assert params["offset"] == "20"
    assert params["rows"] == "2"
    assert params["fields"] == "object_number,public_domain,image_native"
    assert params["lang"] == "en"
    assert params["sort"] == "object_number"
    assert seen[0].headers["user-agent"].startswith("NC-OpenGrace-Pipeline/1.0")
    assert extract_object_numbers(response) == ["KKS5261", "KKSgb22423"]


async def test_search_artworks_defaults_to_id_sort_for_replay_determinism() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("search_public_domain_has_image.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await search_artworks(rows=2, http_client=client)

    assert seen[0].url.params["sort"] == "id"


async def test_fetch_object_requests_object_number_endpoint() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("object_kms1_public_domain.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        response = await fetch_object(" KMS1 ", http_client=client)

    assert seen[0].url.path == "/api/v1/art/"
    assert seen[0].url.params["object_number"] == "KMS1"
    assert seen[0].url.params["lang"] == "en"
    assert extract_object_numbers(response) == ["KMS1"]
    assert response["items"][0]["public_domain"] is True
    assert response["items"][0]["image_native"].startswith("https://api.smk.dk/api/v1/download/")


async def test_fetch_manifest_requests_iiif_manifest_endpoint() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, content=fixture("manifest_kms1.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        manifest = await fetch_manifest("KMS1", http_client=client)

    assert seen[0].url.path == "/api/v1/iiif/manifest"
    assert seen[0].url.params["object_number"] == "KMS1"
    assert manifest["type"] == "Manifest"
    assert manifest["rights"] == "https://creativecommons.org/publicdomain/mark/1.0/"


async def test_missing_inputs_are_rejected_before_request() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(500))
    async with httpx.AsyncClient(transport=transport) as client:
        for call in (fetch_object, fetch_manifest):
            try:
                await call(" ", http_client=client)
            except ValueError as exc:
                assert str(exc) == "missing_object_number"
            else:
                raise AssertionError(f"{call.__name__} accepted a blank object number")

        try:
            await search_artworks(keys=" ", http_client=client)
        except ValueError as exc:
            assert str(exc) == "missing_keys"
        else:
            raise AssertionError("search_artworks accepted blank keys")

        for kwargs, reason in (
            ({"offset": -1}, "invalid_offset"),
            ({"rows": 0}, "invalid_rows"),
            ({"rows": 2001}, "rows_exceeds_smk_max"),
        ):
            try:
                await search_artworks(http_client=client, **kwargs)
            except ValueError as exc:
                assert str(exc) == reason
            else:
                raise AssertionError(f"search_artworks accepted {kwargs}")


def test_pagination_and_extract_helpers_handle_terminal_pages() -> None:
    assert next_offset({"offset": 0, "rows": 2, "found": 5, "items": [{}, {}]}) == 2
    assert next_offset({"offset": 4, "rows": 2, "found": 5, "items": [{}]}) is None
    assert next_offset({"items": None}) is None
    assert extract_object_numbers({"items": [{"object_number": " KMS1 "}, {}, "bad"]}) == [
        "KMS1"
    ]
    assert "public_domain" in DEFAULT_FIELDS

