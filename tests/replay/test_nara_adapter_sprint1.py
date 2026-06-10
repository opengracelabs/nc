import json
from pathlib import Path

import httpx

from workers.nara_adapter.client import (
    build_public_domain_candidates,
    extract_digital_objects,
    extract_hits,
    extract_next_search_after,
    extract_record,
    extract_restriction_evidence,
    extract_total,
    fetch_record,
    search_records,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nara"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_nara_sprint1_replay_search_envelope_is_deterministic() -> None:
    left = fixture_json("search_page_images.json")
    right = fixture_json("search_page_images.json")

    assert extract_total(left) == extract_total(right) == 2
    assert [hit["_id"] for hit in extract_hits(left)] == ["1667751", "999"]
    assert extract_next_search_after(left) == "1,999"


def test_nara_sprint1_replay_record_and_object_extraction_is_stable() -> None:
    response = fixture_json("search_page_images.json")
    record = extract_record(response)
    objects = extract_digital_objects(record)

    assert record["naId"] == 1667751
    assert [item.object_id for item in objects] == ["14721029"]
    assert objects[0].object_url.endswith("00303_2003_001_AC.jpg")


def test_nara_sprint1_replay_rights_evidence_is_stable() -> None:
    unrestricted = fixture_json("record_unrestricted.json")
    restricted = fixture_json("record_restricted.json")

    assert extract_restriction_evidence(unrestricted).rights_basis == "nara_unrestricted"
    assert extract_restriction_evidence(restricted).rights_basis == "restricted_use"
    assert len(build_public_domain_candidates(unrestricted)) == 2
    assert build_public_domain_candidates(restricted) == []


async def test_nara_sprint1_no_store_writes_fetches_records_only_with_mock_client(
    monkeypatch,
) -> None:
    monkeypatch.setenv("NARA_API_KEY", "mock-key")
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("search_page_images.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await search_records(query="constitution", limit=1, http_client=client)
        await fetch_record(1667751, http_client=client)

    assert [request.method for request in seen] == ["GET", "GET"]
    assert [request.url.path for request in seen] == [
        "/api/v2/records/search",
        "/api/v2/records/search",
    ]
    assert seen[0].headers["x-api-key"] == "mock-key"

