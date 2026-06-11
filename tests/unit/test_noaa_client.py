import json
from pathlib import Path

import httpx

from workers.noaa_adapter.client import (
    build_people_get_public_photos_params,
    build_public_photo_page_url,
    extract_credit,
    extract_flickr_photos,
    extract_total,
    fetch_public_photos,
    flickr_record_to_discovery_payload,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_noaa_client_builds_stable_flickr_params() -> None:
    params = build_people_get_public_photos_params(
        api_key="key",
        user_id="usoceangov",
        page=2,
        per_page=50,
        tags="coral",
    )

    assert params["method"] == "flickr.people.getPublicPhotos"
    assert params["format"] == "json"
    assert params["nojsoncallback"] == "1"
    assert params["page"] == "2"
    assert params["per_page"] == "50"
    assert "license" in params["extras"]
    assert "url_o" in params["extras"]


def test_noaa_client_extracts_flickr_records_and_credit() -> None:
    payload = fixture_json("flickr_search_page_mixed.json")
    records = extract_flickr_photos(payload)
    source_record = flickr_record_to_discovery_payload(records[0])

    assert extract_total(payload) == 3
    assert [record["id"] for record in records] == ["1001", "1003", "1008"]
    assert source_record["source_system"] == "flickr"
    assert source_record["source_url"] == "https://www.flickr.com/photos/usoceangov/1001"
    assert source_record["image_url"].endswith("1001_clean_o.jpg")
    assert source_record["credit"] == "NOAA/NOS"
    assert extract_credit(records[1]) == "Jane Smith/NOAA"


async def test_noaa_client_fetches_public_photos_with_mock_transport() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("flickr_search_page_mixed.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await fetch_public_photos(
            api_key="mock-key",
            user_id="usoceangov",
            page=1,
            per_page=3,
            http_client=client,
        )

    assert len(extract_flickr_photos(payload)) == 3
    assert seen[0].method == "GET"
    assert seen[0].url.host == "api.flickr.com"
    assert seen[0].url.params["api_key"] == "mock-key"
    assert seen[0].headers["user-agent"] == "opengrace-nc-noaa-discovery/1.0"


def test_noaa_client_public_photo_page_requires_ids() -> None:
    assert build_public_photo_page_url("usoceangov", "1001").endswith("/usoceangov/1001")
    try:
        build_public_photo_page_url("", "1001")
    except ValueError as exc:
        assert str(exc) == "missing_owner"
    else:
        raise AssertionError("missing owner accepted")

