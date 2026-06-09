from pathlib import Path

from workers.walters_adapter.client import (
    get_creators_for_object,
    get_images_for_object,
    get_object,
    get_primary_image,
    load_dataset,
    search_objects,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "walters"


def test_walters_sprint1_csv_fixtures_load_required_tables() -> None:
    dataset = load_dataset(FIXTURES)

    assert {row["ObjectID"] for row in dataset.art} == {"1001", "1002", "1003"}
    assert {row["ObjectID"] for row in dataset.media} == {"1001", "1002", "1003"}
    assert get_object(dataset, "1001")["ObjectNumber"] == "W.174"


def test_walters_sprint1_replay_primary_image_selection_is_stable() -> None:
    left = load_dataset(FIXTURES)
    right = load_dataset(FIXTURES)

    assert get_images_for_object(left, "1001") == get_images_for_object(right, "1001")
    assert get_primary_image(left, "1001") == get_primary_image(right, "1001")
    assert get_primary_image(left, "1001")["Filename"] == "W174_fnt.jpg"
    assert get_primary_image(left, "1002")["Filename"] == "zeus_front.jpg"
    assert get_primary_image(left, "1003") is None


def test_walters_sprint1_replay_creator_join_and_search_are_stable() -> None:
    dataset = load_dataset(FIXTURES)

    assert [row["id"] for row in get_creators_for_object(dataset, "1001")] == ["501", "502"]
    assert [row["ObjectID"] for row in search_objects(dataset, has_image=True)] == [
        "1001",
        "1002",
    ]
    assert [row["ObjectID"] for row in search_objects(dataset, query="zeus")] == ["1002"]
