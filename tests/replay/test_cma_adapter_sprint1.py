import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "cma"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_cma_sprint1_search_fixture_is_cc0_with_images() -> None:
    response = load("search_china_cc0_has_image.json")

    assert response["info"]["parameters"]["skip"] == 0
    assert response["info"]["parameters"]["limit"] == 2
    assert len(response["data"]) == 2
    for item in response["data"]:
        assert item["share_license_status"] == "CC0"
        assert isinstance(item["images"], dict)
        assert item["images"]["print"]["url"].startswith(
            "https://openaccess-cdn.clevelandart.org/"
        )


def test_cma_sprint1_single_artwork_fixture_contains_required_fields() -> None:
    response = load("artwork_94979_cc0.json")
    record = response["data"]

    assert record["id"] == 94979
    assert record["accession_number"] == "1915.534"
    assert record["title"] == "Nathaniel Hurd"
    assert record["share_license_status"] == "CC0"
    assert record["images"]["print"]["url"].startswith(
        "https://openaccess-cdn.clevelandart.org/1915.534/"
    )

