from pathlib import Path

import httpx

from workers.nga_adapter.client import (
    CONSTITUENTS_CSV,
    OBJECTS_CONSTITUENTS_CSV,
    OBJECTS_CSV,
    OBJECTS_TERMS_CSV,
    PUBLISHED_IMAGES_CSV,
    REQUIRED_CSV_FILES,
    csv_url,
    fetch_csv,
    get_constituents_for_object,
    get_images_for_object,
    get_object,
    get_primary_image,
    get_terms_for_object,
    is_openaccess_image,
    load_csv_text,
    load_dataset,
    search_objects,
    select_primary_image,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nga"


def test_csv_url_uses_official_nga_opendata_raw_files() -> None:
    assert REQUIRED_CSV_FILES == (
        OBJECTS_CSV,
        PUBLISHED_IMAGES_CSV,
        OBJECTS_CONSTITUENTS_CSV,
        CONSTITUENTS_CSV,
        OBJECTS_TERMS_CSV,
    )
    assert csv_url("objects.csv") == (
        "https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/objects.csv"
    )

    try:
        csv_url("unsupported.csv")
    except ValueError as exc:
        assert str(exc) == "unsupported_nga_csv"
    else:
        raise AssertionError("unsupported CSV was accepted")


def test_load_csv_text_parses_rows_deterministically() -> None:
    rows = load_csv_text("objectid,title\n1,Alpha\n2,Beta\n")

    assert rows == [{"objectid": "1", "title": "Alpha"}, {"objectid": "2", "title": "Beta"}]


async def test_fetch_csv_requests_official_raw_url() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, text="objectid,title\n1,Alpha\n")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        rows = await fetch_csv("objects.csv", http_client=client)

    assert seen[0].url.host == "raw.githubusercontent.com"
    assert seen[0].url.path == "/NationalGalleryOfArt/opendata/main/data/objects.csv"
    assert seen[0].headers["user-agent"].startswith("NC-OpenGrace-Pipeline/1.0")
    assert rows == [{"objectid": "1", "title": "Alpha"}]


def test_load_dataset_indexes_required_nga_csv_fixtures() -> None:
    dataset = load_dataset(FIXTURES)

    assert len(dataset.objects) == 2
    assert len(dataset.published_images) == 3
    assert get_object(dataset, "2001")["title"] == "The Japanese Footbridge"
    assert get_object(dataset, 2002)["classification"] == "Photograph"
    assert get_object(dataset, "9999") is None


def test_image_lookup_and_primary_selection_require_openaccess_iiif() -> None:
    dataset = load_dataset(FIXTURES)
    images = get_images_for_object(dataset, "2001")

    assert [row["uuid"] for row in images] == ["img-primary-2001", "img-alt-2001"]
    assert all(is_openaccess_image(row) for row in images)
    assert get_primary_image(dataset, "2001")["uuid"] == "img-primary-2001"
    assert get_primary_image(dataset, "2002") is None
    assert select_primary_image([{"openaccess": "1", "iiifurl": "", "uuid": "bad"}]) is None


def test_terms_constituents_and_search_are_deterministic() -> None:
    dataset = load_dataset(FIXTURES)

    assert [row["term"] for row in get_terms_for_object(dataset, "2001")] == [
        "Bridge",
        "France",
        "French",
    ]
    constituents = get_constituents_for_object(dataset, "2001")
    assert constituents[0]["forwarddisplayname"] == "Claude Monet"
    assert constituents[0]["object_role"] == "painter"

    results = search_objects(dataset, query="monet", openaccess=True)
    assert [row["objectid"] for row in results] == ["2001"]
    assert search_objects(dataset, classification="Photograph", openaccess=True) == []
    assert [row["objectid"] for row in search_objects(dataset, limit=1)] == ["2001"]

    try:
        search_objects(dataset, limit=0)
    except ValueError as exc:
        assert str(exc) == "invalid_limit"
    else:
        raise AssertionError("limit=0 was accepted")


def test_missing_object_inputs_are_rejected() -> None:
    dataset = load_dataset(FIXTURES)

    calls = (
        get_object,
        get_images_for_object,
        get_terms_for_object,
        get_constituents_for_object,
    )
    for call in calls:
        try:
            call(dataset, " ")
        except ValueError as exc:
            assert str(exc) == "missing_object_id"
        else:
            raise AssertionError(f"{call.__name__} accepted a blank object id")
