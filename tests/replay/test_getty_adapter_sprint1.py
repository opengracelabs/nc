import json
from pathlib import Path

import httpx

from workers.getty_adapter.client import (
    CC0_URI,
    build_open_content_candidate,
    extract_activity_record_uris,
    extract_iiif_image_services,
    extract_manifest_url,
    extract_rights,
    fetch_activity_stream_page,
    is_open_content_candidate,
    next_activity_stream_page,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "getty"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_getty_sprint1_replay_activity_stream_harvest_is_deterministic() -> None:
    left = fixture_json("activity_stream_page_1.json")
    right = fixture_json("activity_stream_page_1.json")

    assert extract_activity_record_uris(left) == extract_activity_record_uris(right)
    assert next_activity_stream_page(left) == (
        "https://data.getty.edu/museum/collection/activity-stream/page/2"
    )
    assert extract_activity_record_uris(left) == [
        "https://data.getty.edu/museum/collection/object/"
        "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb",
        "https://data.getty.edu/museum/collection/object/"
        "00000000-0000-4000-8000-000000000002",
    ]


def test_getty_sprint1_replay_open_content_filtering_is_stable() -> None:
    cc0 = fixture_json("object_cc0.json")
    unknown = fixture_json("object_unknown_rights.json")
    missing = fixture_json("object_missing_subject_to.json")

    assert extract_rights(cc0).rights_basis == "getty_cc0"
    assert extract_rights(cc0).rights_statement_uri == CC0_URI
    assert extract_rights(unknown).rights_basis == "rights_not_allowed"
    assert extract_rights(missing).rights_basis == "missing_subject_to"
    assert is_open_content_candidate(cc0) is True
    assert is_open_content_candidate(unknown) is False
    assert is_open_content_candidate(missing) is False


def test_getty_sprint1_replay_iiif_discovery_is_stable() -> None:
    record = fixture_json("object_cc0.json")
    manifest = fixture_json("manifest_irises_v2.json")

    assert extract_manifest_url(record) == (
        "https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
    )
    assert extract_iiif_image_services(manifest) == [
        "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
    ]


def test_getty_sprint1_replay_candidate_requires_open_content_and_iiif() -> None:
    record = fixture_json("object_cc0.json")
    manifest = fixture_json("manifest_irises_v2.json")
    blocked = fixture_json("object_unknown_rights.json")

    candidate = build_open_content_candidate(record, manifest)

    assert candidate is not None
    assert candidate.object_uri.endswith("c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb")
    assert candidate.rights_uri == CC0_URI
    assert candidate.iiif_image_service.endswith("7ff0a543-569a-4cb0-b92b-cd78877d4141")
    assert build_open_content_candidate(blocked, manifest) is None


async def test_getty_sprint1_no_store_writes_fetches_activity_page_only_with_mock_client() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("activity_stream_page_1.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        page = await fetch_activity_stream_page(1, http_client=client)

    assert page["type"] == "OrderedCollectionPage"
    assert [request.url.path for request in seen] == [
        "/museum/collection/activity-stream/page/1"
    ]

