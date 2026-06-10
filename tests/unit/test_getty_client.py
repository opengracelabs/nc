import json
from pathlib import Path

import httpx

from workers.getty_adapter.client import (
    CC0_URI,
    build_activity_stream_page_url,
    build_object_url,
    build_open_content_candidate,
    canonical_request_params,
    extract_activity_record_uris,
    extract_iiif_image_service,
    extract_iiif_image_services,
    extract_manifest_url,
    extract_rights,
    extract_rights_uris,
    fetch_activity_stream_page,
    fetch_iiif_manifest,
    fetch_linked_art_record,
    is_open_content_candidate,
    next_activity_stream_page,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "getty"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_url_builders_are_deterministic() -> None:
    assert build_activity_stream_page_url(1) == (
        "https://data.getty.edu/museum/collection/activity-stream/page/1"
    )
    assert build_activity_stream_page_url(
        "https://data.getty.edu/museum/collection/activity-stream/page/2"
    ) == "https://data.getty.edu/museum/collection/activity-stream/page/2"
    assert build_object_url("c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb") == (
        "https://data.getty.edu/museum/collection/object/"
        "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    )


def test_url_builders_reject_blank_and_non_object_inputs() -> None:
    for call, expected in (
        (lambda: build_activity_stream_page_url(""), "missing_activity_stream_page"),
        (lambda: build_activity_stream_page_url("abc"), "invalid_activity_stream_page"),
        (lambda: build_object_url(""), "missing_object_id"),
        (
            lambda: build_object_url("https://data.getty.edu/museum/collection/person/1"),
            "not_getty_object_uri",
        ),
    ):
        try:
            call()
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError(f"{expected} was not raised")


def test_canonical_request_params_drops_empty_values_and_sorts() -> None:
    assert canonical_request_params({"page": 2, "empty": "", "q": "abc", "none": None}) == {
        "page": "2",
        "q": "abc",
    }


def test_activity_stream_page_parsing_filters_create_and_update_objects() -> None:
    page = fixture_json("activity_stream_page_1.json")

    assert next_activity_stream_page(page) == (
        "https://data.getty.edu/museum/collection/activity-stream/page/2"
    )
    assert extract_activity_record_uris(page) == [
        "https://data.getty.edu/museum/collection/object/"
        "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb",
        "https://data.getty.edu/museum/collection/object/"
        "00000000-0000-4000-8000-000000000002",
    ]
    assert extract_activity_record_uris(page, include_types=("Create",)) == [
        "https://data.getty.edu/museum/collection/object/"
        "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    ]


async def test_fetch_activity_stream_and_object_use_public_getty_endpoints() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path == "/museum/collection/activity-stream/page/1":
            return httpx.Response(200, json=fixture_json("activity_stream_page_1.json"))
        if request.url.path.endswith("/c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"):
            return httpx.Response(200, json=fixture_json("object_cc0.json"))
        return httpx.Response(404)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        page = await fetch_activity_stream_page(1, http_client=client)
        record = await fetch_linked_art_record(
            "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb",
            http_client=client,
        )

    assert page["type"] == "OrderedCollectionPage"
    assert record["_label"] == "Irises"
    assert [request.url.path for request in seen] == [
        "/museum/collection/activity-stream/page/1",
        "/museum/collection/object/c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb",
    ]
    assert seen[0].headers["user-agent"].startswith("NC-OpenGrace-Pipeline/1.0")


def test_rights_extraction_reads_referred_to_by_subject_to_classification() -> None:
    record = fixture_json("object_cc0.json")
    evidence = extract_rights(record)

    assert extract_rights_uris(record) == [CC0_URI]
    assert evidence.allowed is True
    assert evidence.decision == "ALLOWED"
    assert evidence.rights_statement_uri == CC0_URI
    assert evidence.rights_basis == "getty_cc0"
    assert is_open_content_candidate(record) is True


def test_rights_extraction_blocks_missing_object_missing_subject_to_and_unknown() -> None:
    missing = fixture_json("object_missing_subject_to.json")
    unknown = fixture_json("object_unknown_rights.json")

    assert extract_rights({}).rights_basis == "missing_object"
    assert extract_rights(missing).rights_basis == "missing_subject_to"
    unknown_rights = extract_rights(unknown)
    assert unknown_rights.allowed is False
    assert unknown_rights.rights_basis == "rights_not_allowed"
    assert unknown_rights.rights_statement_uri == "https://rightsstatements.org/vocab/InC/1.0/"
    assert is_open_content_candidate(unknown) is False


def test_manifest_discovery_and_iiif_v2_image_service_extraction() -> None:
    record = fixture_json("object_cc0.json")
    manifest = fixture_json("manifest_irises_v2.json")

    assert extract_manifest_url(record) == (
        "https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
    )
    assert extract_iiif_image_services(manifest) == [
        "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
    ]
    assert extract_iiif_image_service(manifest) == (
        "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
    )


def test_iiif_v3_service_extraction_is_supported_for_forward_compatibility() -> None:
    manifest = fixture_json("manifest_irises_v3.json")

    assert extract_iiif_image_services(manifest) == ["https://media.getty.edu/iiif/image/v3-image"]


async def test_fetch_iiif_manifest_accepts_linked_art_record() -> None:
    seen = []
    record = fixture_json("object_cc0.json")

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("manifest_irises_v2.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        manifest = await fetch_iiif_manifest(record, http_client=client)

    assert seen[0].url.path == "/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
    assert manifest["@type"] == "sc:Manifest"


def test_build_open_content_candidate_requires_rights_manifest_and_service() -> None:
    record = fixture_json("object_cc0.json")
    manifest = fixture_json("manifest_irises_v2.json")
    blocked = fixture_json("object_unknown_rights.json")

    candidate = build_open_content_candidate(record, manifest)

    assert candidate is not None
    assert candidate.source_slug == "getty"
    assert candidate.rights_uri == CC0_URI
    assert candidate.iiif_manifest == (
        "https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
    )
    assert candidate.iiif_image_service == (
        "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
    )
    assert build_open_content_candidate(blocked, manifest) is None

