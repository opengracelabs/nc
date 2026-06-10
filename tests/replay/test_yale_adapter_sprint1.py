import json
from pathlib import Path

from workers.yale_adapter.client import (
    CC0_URI,
    derive_manifest_candidate,
    extract_iiif_image_services,
    extract_manifest_rights,
    extract_object_uris_from_search,
    extract_rights,
    fetch_env,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "yale"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_yale_sprint1_replay_fixtures_cover_ycba_yuag_and_blocked_rights() -> None:
    ycba = fixture_json("ycba_object_cc0.json")
    yuag = fixture_json("yuag_object_noc_us.json")
    restricted = fixture_json("ycba_object_restricted.json")

    assert extract_rights(ycba).rights_basis == "ycba_cc0"
    assert extract_rights(yuag).rights_basis == "yuag_noc_us"
    assert extract_rights(restricted).rights_basis == "rights_not_allowed"


def test_yale_sprint1_replay_manifest_resolution_is_stable() -> None:
    left = fixture_json("ycba_object_cc0.json")
    right = fixture_json("ycba_object_cc0.json")

    left_candidate = derive_manifest_candidate(left)
    right_candidate = derive_manifest_candidate(right)

    assert left_candidate == right_candidate
    assert left_candidate is not None
    assert left_candidate.url == "https://manifests.collections.yale.edu/ycba/obj/12345"
    assert left_candidate.source == "record"


def test_yale_sprint1_replay_iiif_v3_service_extraction_is_stable() -> None:
    manifest = fixture_json("manifest_ycba_12345_v3.json")

    assert extract_manifest_rights(manifest) == CC0_URI
    assert extract_iiif_image_services(manifest) == [
        "https://media.collections.yale.edu/iiif/2/ycba-12345"
    ]


def test_yale_sprint1_replay_search_results_are_deterministic() -> None:
    response = fixture_json("ycba_search_page.json")

    assert extract_object_uris_from_search(response) == [
        "https://lux.collections.yale.edu/data/object/ycba-obj-12345",
        "https://lux.collections.yale.edu/data/object/ycba-obj-55555",
    ]


async def test_yale_sprint1_no_store_writes_fetches_env_only_with_mock_client() -> None:
    import httpx

    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("env.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        env = await fetch_env(http_client=client)

    assert env["luxEnv"] == "production"
    assert [request.url.path for request in seen] == ["/env"]

