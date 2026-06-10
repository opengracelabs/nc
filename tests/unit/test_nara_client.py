import json
from pathlib import Path

import httpx

from workers.nara_adapter.client import (
    PUBLIC_DOMAIN_MARK_URI,
    build_catalog_record_url,
    build_headers,
    build_public_domain_candidates,
    build_record_lookup_params,
    build_search_params,
    build_search_url,
    canonical_request_params,
    extract_access_restriction,
    extract_digital_objects,
    extract_hits,
    extract_next_search_after,
    extract_record,
    extract_restriction_evidence,
    extract_total,
    extract_use_restriction,
    fetch_record,
    is_still_image_object,
    search_records,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nara"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_url_and_param_builders_are_deterministic() -> None:
    assert build_search_url() == "https://catalog.archives.gov/api/v2/records/search"
    assert build_catalog_record_url(" 1667751 ") == "https://catalog.archives.gov/id/1667751"
    assert build_search_params(
        query="constitution",
        page=2,
        limit=10,
        available_online=True,
        object_type="Image (JPG)",
        source_includes="naId,title",
    ) == {
        "availableOnline": "true",
        "limit": "10",
        "objectType": "Image (JPG)",
        "page": "2",
        "q": "constitution",
        "sourceIncludes": "naId,title",
    }
    assert build_record_lookup_params(1667751) == {
        "limit": "1",
        "naId_is": "1667751",
        "page": "1",
        "sourceIncludes": (
            "naId,title,useRestriction,accessRestriction,digitalObjects,"
            "generalRecordsTypes,levelOfDescription"
        ),
    }


def test_builders_reject_invalid_inputs() -> None:
    for call, expected in (
        (lambda: build_catalog_record_url(""), "missing_na_id"),
        (lambda: build_search_params(page=0), "invalid_page"),
        (lambda: build_search_params(limit=0), "invalid_limit"),
        (lambda: build_record_lookup_params(""), "missing_na_id"),
    ):
        try:
            call()
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError(f"{expected} was not raised")


def test_canonical_request_params_drops_empty_values_and_sorts() -> None:
    assert canonical_request_params({"q": "abc", "empty": "", "none": None, "limit": 1}) == {
        "limit": "1",
        "q": "abc",
    }


def test_headers_use_environment_variable_only(monkeypatch) -> None:
    monkeypatch.delenv("NARA_API_KEY", raising=False)
    try:
        build_headers()
    except RuntimeError as exc:
        assert str(exc) == "missing_nara_api_key"
    else:
        raise AssertionError("missing key accepted")

    monkeypatch.setenv("NARA_API_KEY", "unit-test-key")
    headers = build_headers()

    assert headers["x-api-key"] == "unit-test-key"
    assert headers["user-agent".title()].startswith("NC-OpenGrace-Pipeline/1.0")


async def test_search_and_fetch_record_send_api_key_header(monkeypatch) -> None:
    monkeypatch.setenv("NARA_API_KEY", "mock-key")
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=fixture_json("search_page_images.json"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await search_records(query="constitution", limit=1, http_client=client)
        await fetch_record(1667751, http_client=client)

    assert [request.url.path for request in seen] == [
        "/api/v2/records/search",
        "/api/v2/records/search",
    ]
    assert seen[0].headers["x-api-key"] == "mock-key"
    assert seen[0].url.params["q"] == "constitution"
    assert seen[1].url.params["naId_is"] == "1667751"


def test_response_envelope_and_deep_pagination_are_extracted() -> None:
    response = fixture_json("search_page_images.json")

    assert extract_total(response) == 2
    assert len(extract_hits(response)) == 2
    assert extract_record(response)["title"] == "Constitution of the United States"
    assert extract_next_search_after(response) == "1,999"


def test_restriction_evidence_classifies_unrestricted_and_restricted_records() -> None:
    unrestricted = fixture_json("record_unrestricted.json")
    restricted = fixture_json("record_restricted.json")

    unrestricted_rights = extract_restriction_evidence(unrestricted)
    restricted_rights = extract_restriction_evidence(restricted)

    assert extract_use_restriction(unrestricted) == "Unrestricted"
    assert extract_access_restriction(unrestricted) == "Unrestricted"
    assert unrestricted_rights.allowed is True
    assert unrestricted_rights.rights_basis == "nara_unrestricted"
    assert unrestricted_rights.rights_statement_uri == PUBLIC_DOMAIN_MARK_URI
    assert restricted_rights.allowed is False
    assert restricted_rights.rights_basis == "restricted_use"
    assert extract_restriction_evidence({}).rights_basis == "missing_record"


def test_digital_object_extraction_keeps_still_images_only() -> None:
    record = fixture_json("record_unrestricted.json")
    digital_objects = extract_digital_objects(record)

    assert len(digital_objects) == 2
    assert digital_objects[0].na_id == "1667751"
    assert digital_objects[0].object_id == "14721029"
    assert digital_objects[0].object_type == "Image (JPG)"
    assert digital_objects[0].object_file_size == 62296840
    assert is_still_image_object(record["digitalObjects"][0]) is True
    assert is_still_image_object(record["digitalObjects"][2]) is False


def test_public_domain_candidates_are_evidence_only() -> None:
    unrestricted = fixture_json("record_unrestricted.json")
    restricted = fixture_json("record_restricted.json")

    candidates = build_public_domain_candidates(unrestricted)

    assert len(candidates) == 2
    assert candidates[0].source_slug == "nara"
    assert candidates[0].na_id == "1667751"
    assert candidates[0].title == "Constitution of the United States"
    assert candidates[0].rights.rights_basis == "nara_unrestricted"
    assert build_public_domain_candidates(restricted) == []

