import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "smk"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_smk_sprint1_search_fixture_is_public_domain_with_images() -> None:
    response = load("search_public_domain_has_image.json")

    assert response["found"] >= 1
    assert response["offset"] == 0
    assert response["rows"] == 2
    assert len(response["items"]) == 2
    for item in response["items"]:
        assert item["public_domain"] is True
        assert item["has_image"] is True
        assert item["object_number"]
        assert item["image_native"].startswith("https://api.smk.dk/api/v1/download/")
        assert item["iiif_manifest"].startswith("https://api.smk.dk/api/v1/iiif/manifest")


def test_smk_sprint1_single_object_fixture_contains_required_fields() -> None:
    response = load("object_kms1_public_domain.json")
    record = response["items"][0]

    assert record["object_number"] == "KMS1"
    assert record["public_domain"] is True
    assert record["has_image"] is True
    assert record["rights"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert record["image_native"].startswith("https://api.smk.dk/api/v1/download/")
    assert record["image_iiif_id"].startswith("https://iip.smk.dk/iiif/")
    assert record["iiif_manifest"] == "https://api.smk.dk/api/v1/iiif/manifest?id=KMS1"


def test_smk_sprint1_manifest_fixture_is_iiif_presentation_3() -> None:
    manifest = load("manifest_kms1.json")

    assert manifest["@context"] == "http://iiif.io/api/presentation/3/context.json"
    assert manifest["type"] == "Manifest"
    assert manifest["id"] == "https://api.smk.dk/api/v1/iiif/manifest?id=KMS1"
    assert manifest["rights"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert manifest["items"][0]["type"] == "Canvas"

