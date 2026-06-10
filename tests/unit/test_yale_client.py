import json
from pathlib import Path

import httpx

from workers.yale_adapter.client import (
    CC0_URI,
    NOC_US_URI,
    YCBA_LABEL,
    YUAG_LABEL,
    build_data_url,
    build_iiif_image_url,
    build_manifest_url,
    build_search_url,
    canonical_request_params,
    derive_manifest_candidate,
    detect_source_slug,
    extract_iiif_image_services,
    extract_manifest_rights,
    extract_manifest_url,
    extract_object_id,
    extract_object_uris_from_search,
    extract_rights,
    extract_subject_to_uris,
    fetch_advanced_search_config,
    fetch_env,
    fetch_manifest,
    fetch_object,
    has_representation,
    search_ycba_items,
    search_yuag_items,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "yale"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_url_builders_are_deterministic() -> None:
    assert build_data_url("object", " abc ") == (
        "https://lux.collections.yale.edu/data/object/abc"
    )
    assert build_data_url("object", "https://lux.collections.yale.edu/data/object/abc") == (
        "https://lux.collections.yale.edu/data/object/abc"
    )
    assert build_search_url("item") == "https://lux.collections.yale.edu/api/search/item"
    assert build_manifest_url("ycba", "12345") == (
        "https://manifests.collections.yale.edu/ycba/obj/12345"
    )
    assert build_manifest_url("yuag", 98765, version=2) == (
        "https://manifests.collections.yale.edu/v2/yuag/obj/98765"
    )


def test_url_builders_reject_blank_and_unsupported_inputs() -> None:
    for call, expected in (
        (lambda: build_data_url("", "abc"), "missing_entity_type"),
        (lambda: build_data_url("object", ""), "missing_identifier"),
        (lambda: build_search_url(""), "missing_entity_type"),
        (lambda: build_manifest_url("peabody", "1"), "unsupported_yale_source"),
        (lambda: build_manifest_url("ycba", ""), "missing_object_id"),
        (lambda: build_manifest_url("ycba", "1", version=4), "unsupported_iiif_version"),
    ):
        try:
            call()
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError(f"{expected} was not raised")


def test_canonical_request_params_drops_empty_values_and_sorts() -> None:
    assert canonical_request_params({"pageLength": 20, "empty": "", "q": "abc", "none": None}) == {
        "pageLength": "20",
        "q": "abc",
    }


async def test_fetch_env_and_advanced_search_config_request_public_lux_endpoints() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path == "/env":
            return httpx.Response(200, json=fixture_json("env.json"))
        if request.url.path == "/api/advanced-search-config":
            return httpx.Response(200, json=fixture_json("advanced_search_config.json"))
        return httpx.Response(404)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        env = await fetch_env(http_client=client)
        config = await fetch_advanced_search_config(http_client=client)

    assert env["dataApiBaseUrl"] == "https://lux.collections.yale.edu/"
    assert "hasDigitalImage" in config["terms"]["item"]
    assert "isPublicDomain" in config["terms"]["work"]
    assert [request.url.path for request in seen] == ["/env", "/api/advanced-search-config"]
    assert seen[0].headers["user-agent"].startswith("NC-OpenGrace-Pipeline/1.0")


async def test_fetch_object_requests_concrete_data_uri_and_rejects_view_routes() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("ycba_object_cc0.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        record = await fetch_object("ycba-obj-12345", http_client=client)

        try:
            await fetch_object(
                "https://lux.collections.yale.edu/view/object/abc",
                http_client=client,
            )
        except ValueError as exc:
            assert str(exc) == "view_routes_are_not_data_uris"
        else:
            raise AssertionError("view route accepted")

    assert seen[0].url.path == "/data/object/ycba-obj-12345"
    assert record["id"].endswith("ycba-obj-12345")


async def test_search_ycba_and_yuag_items_use_responsible_unit_query() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("ycba_search_page.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await search_ycba_items(page=2, page_length=10, http_client=client)
        await search_yuag_items(page=1, page_length=20, http_client=client)

    assert seen[0].url.path == "/api/search/item"
    assert seen[0].url.params["page"] == "2"
    assert seen[0].url.params["pageLength"] == "10"
    assert YCBA_LABEL in seen[0].url.params["q"]
    assert YUAG_LABEL in seen[1].url.params["q"]


def test_rights_extraction_supports_ycba_cc0_and_yuag_noc_us() -> None:
    ycba = fixture_json("ycba_object_cc0.json")
    yuag = fixture_json("yuag_object_noc_us.json")

    ycba_rights = extract_rights(ycba)
    yuag_rights = extract_rights(yuag)

    assert detect_source_slug(ycba) == "ycba"
    assert detect_source_slug(yuag) == "yuag"
    assert extract_subject_to_uris(ycba) == [CC0_URI]
    assert ycba_rights.allowed is True
    assert ycba_rights.rights_basis == "ycba_cc0"
    assert ycba_rights.rights_statement_uri == CC0_URI
    assert yuag_rights.allowed is True
    assert yuag_rights.rights_basis == "yuag_noc_us"
    assert yuag_rights.rights_statement_uri == NOC_US_URI


def test_rights_extraction_blocks_missing_empty_and_unallowed_subject_to() -> None:
    restricted = fixture_json("ycba_object_restricted.json")

    assert extract_rights({}).rights_basis == "missing_subject_to"
    assert extract_rights({"subject_to": []}).rights_basis == "no_rights_statement"
    restricted_rights = extract_rights(restricted)
    assert restricted_rights.allowed is False
    assert restricted_rights.rights_basis == "rights_not_allowed"
    assert restricted_rights.rights_statement_uri == "https://rightsstatements.org/vocab/UND/1.0/"


def test_object_and_manifest_extraction_prefers_record_manifest_then_derivation() -> None:
    ycba = fixture_json("ycba_object_cc0.json")
    yuag = fixture_json("yuag_object_noc_us.json")

    assert has_representation(ycba) is True
    assert extract_object_id(ycba) == "12345"
    assert extract_manifest_url(ycba) == "https://manifests.collections.yale.edu/ycba/obj/12345"

    ycba_candidate = derive_manifest_candidate(ycba)
    yuag_candidate = derive_manifest_candidate(yuag)

    assert ycba_candidate is not None
    assert ycba_candidate.url == "https://manifests.collections.yale.edu/ycba/obj/12345"
    assert ycba_candidate.source == "record"
    assert yuag_candidate is not None
    assert yuag_candidate.url == "https://manifests.collections.yale.edu/yuag/obj/98765"
    assert yuag_candidate.source == "derived"


async def test_fetch_manifest_accepts_lux_record_and_fetches_v3_manifest() -> None:
    seen = []
    record = fixture_json("yuag_object_noc_us.json")

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("manifest_ycba_12345_v3.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        manifest = await fetch_manifest(record, http_client=client)

    assert seen[0].url.path == "/yuag/obj/98765"
    assert manifest["type"] == "Manifest"


def test_iiif_v3_manifest_rights_and_image_service_extraction() -> None:
    manifest = fixture_json("manifest_ycba_12345_v3.json")

    services = extract_iiif_image_services(manifest)

    assert extract_manifest_rights(manifest) == CC0_URI
    assert services == ["https://media.collections.yale.edu/iiif/2/ycba-12345"]
    assert build_iiif_image_url(services[0]) == (
        "https://media.collections.yale.edu/iiif/2/ycba-12345/full/!1024,1024/0/default.jpg"
    )
    assert build_iiif_image_url(services[0], size="max") == (
        "https://media.collections.yale.edu/iiif/2/ycba-12345/full/max/0/default.jpg"
    )


def test_search_result_uri_extraction_handles_ordered_items() -> None:
    response = fixture_json("ycba_search_page.json")

    assert extract_object_uris_from_search(response) == [
        "https://lux.collections.yale.edu/data/object/ycba-obj-12345",
        "https://lux.collections.yale.edu/data/object/ycba-obj-55555",
    ]

