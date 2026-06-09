from pathlib import Path

import httpx

from workers.walters_adapter.client import (
    ART_CSV,
    CREATORS_CSV,
    MEDIA_CSV,
    REQUIRED_CSV_FILES,
    csv_url,
    fetch_csv,
    get_creators_for_object,
    get_images_for_object,
    get_object,
    get_primary_image,
    is_image_media,
    is_primary_image,
    load_csv_text,
    load_dataset,
    search_objects,
    select_primary_image,
    split_pipe_values,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "walters"


def test_csv_url_uses_official_walters_opendata_raw_files() -> None:
    assert REQUIRED_CSV_FILES == (ART_CSV, MEDIA_CSV, CREATORS_CSV)
    assert csv_url("art.csv") == (
        "https://raw.githubusercontent.com/WaltersArtMuseum/api-thewalters-org/main/art.csv"
    )

    try:
        csv_url("relationships.csv")
    except ValueError as exc:
        assert str(exc) == "unsupported_walters_csv"
    else:
        raise AssertionError("unsupported CSV was accepted")


def test_load_csv_text_parses_camel_case_rows_deterministically() -> None:
    rows = load_csv_text("ObjectID,Title\n1,Alpha\n2,Beta\n")

    assert rows == [{"ObjectID": "1", "Title": "Alpha"}, {"ObjectID": "2", "Title": "Beta"}]


async def test_fetch_csv_requests_official_raw_url() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, text="ObjectID,Title\n1,Alpha\n")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        rows = await fetch_csv("art.csv", http_client=client)

    assert seen[0].url.host == "raw.githubusercontent.com"
    assert seen[0].url.path == "/WaltersArtMuseum/api-thewalters-org/main/art.csv"
    assert seen[0].headers["user-agent"].startswith("NC-OpenGrace-Pipeline/1.0")
    assert rows == [{"ObjectID": "1", "Title": "Alpha"}]


def test_load_dataset_indexes_required_walters_csv_fixtures() -> None:
    dataset = load_dataset(FIXTURES)

    assert len(dataset.art) == 3
    assert len(dataset.media) == 6
    assert len(dataset.creators) == 3
    assert get_object(dataset, "1001")["Title"] == "Leaf from a Book of Hours"
    assert get_object(dataset, 1002)["ObjectNumber"] == "54.975"
    assert get_object(dataset, "9999") is None


def test_image_lookup_and_primary_selection_prefer_is_primary() -> None:
    dataset = load_dataset(FIXTURES)
    images = get_images_for_object(dataset, "1001")

    assert [row["Filename"] for row in images] == ["W174_fnt.jpg", "W174_det.jpg"]
    assert all(is_image_media(row) for row in images)
    assert is_primary_image(images[0]) is True
    assert get_primary_image(dataset, "1001")["MediaXrefID"] == "2001"


def test_primary_selection_falls_back_to_lowest_rank_image() -> None:
    dataset = load_dataset(FIXTURES)

    assert get_primary_image(dataset, "1002")["Filename"] == "zeus_front.jpg"
    assert get_primary_image(dataset, "1003") is None
    assert select_primary_image([{"MediaType": "Image", "ImageURL": "", "IsPrimary": "1"}]) is None


def test_creator_lookup_pipe_splitting_and_search_are_deterministic() -> None:
    dataset = load_dataset(FIXTURES)

    assert split_pipe_values("MAN|MED|| ") == ["MAN", "MED"]
    creators = get_creators_for_object(dataset, "1001")
    assert [row["name"] for row in creators] == ["Master of Walters W.174", "Unknown scribe"]
    assert [row["nationality"] for row in creators] == ["French", "French"]

    results = search_objects(dataset, query="hours", has_image=True)
    assert [row["ObjectID"] for row in results] == ["1001"]
    assert [row["ObjectID"] for row in search_objects(dataset, classification="Metal")] == [
        "1002"
    ]
    assert [row["ObjectID"] for row in search_objects(dataset, limit=1)] == ["1001"]

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
        get_creators_for_object,
    )
    for call in calls:
        try:
            call(dataset, " ")
        except ValueError as exc:
            assert str(exc) == "missing_object_id"
        else:
            raise AssertionError(f"{call.__name__} accepted a blank object id")
