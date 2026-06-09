from pathlib import Path

from workers.nga_adapter.client import (
    get_images_for_object,
    get_object,
    get_primary_image,
    load_dataset,
    search_objects,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nga"


def test_nga_sprint1_csv_fixtures_load_required_tables() -> None:
    dataset = load_dataset(FIXTURES)

    assert {row["objectid"] for row in dataset.objects} == {"2001", "2002"}
    assert {row["depictstmsobjectid"] for row in dataset.published_images} == {"2001", "2002"}
    assert get_object(dataset, "2001")["accessionnum"] == "1942.9.97"


def test_nga_sprint1_replay_primary_image_selection_is_stable() -> None:
    left = load_dataset(FIXTURES)
    right = load_dataset(FIXTURES)

    assert get_images_for_object(left, "2001") == get_images_for_object(right, "2001")
    assert get_primary_image(left, "2001") == get_primary_image(right, "2001")
    assert get_primary_image(left, "2001")["uuid"] == "img-primary-2001"
    assert get_primary_image(left, "2002") is None


def test_nga_sprint1_replay_search_filters_to_openaccess_objects() -> None:
    dataset = load_dataset(FIXTURES)

    assert [row["objectid"] for row in search_objects(dataset, openaccess=True)] == ["2001"]
    assert [row["objectid"] for row in search_objects(dataset, query="study")] == ["2002"]
