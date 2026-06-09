from pathlib import Path

from workers.nga_adapter.client import load_csv_file, load_dataset
from workers.nga_adapter.normalize import (
    build_collection_url,
    canonical_json_hash,
    mandatory_field_warnings,
    normalize_dataset_record,
    normalize_record,
    representative_media_url,
)
from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

FIXTURES = Path("tests/fixtures/nga")


def test_normalize_dataset_record_maps_openaccess_object_and_evidence() -> None:
    dataset = load_dataset(FIXTURES)
    normalized = normalize_dataset_record(dataset, "2001")

    assert normalized["record_id"] == "2001"
    assert normalized["title"] == "The Japanese Footbridge"
    assert normalized["rights_uri"] == CC0_URI
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True
    assert normalized["source_url"] == "https://www.nga.gov/collection/art-object-page.2001.html"
    assert normalized["representative_media_url"] == (
        "https://api.nga.gov/iiif/img-primary-2001/full/!1024,1024/0/default.jpg"
    )
    assert normalized["preview_urls"][1].endswith("/full/200,200/0/default.jpg")
    assert normalized["width_px"] == 3200
    assert normalized["height_px"] == 2400
    assert normalized["creator"] == "Claude Monet"
    assert normalized["creator_nationality"] == "French"
    assert normalized["school"] == "French"
    assert normalized["place_executed"] == "France"
    assert normalized["subject_terms"] == ["Bridge", "France", "French"]
    assert normalized["source_object"]["objectid"] == "2001"
    assert normalized["nga_openaccess"] == "1"
    assert normalized["nga_image_uuid"] == "img-primary-2001"
    assert normalized["nga_iiifurl"] == "https://api.nga.gov/iiif/img-primary-2001"
    assert normalized["nga_iiif_thumb_url"].endswith("/full/200,200/0/default.jpg")
    assert normalized["nga_viewtype"] == "primary"
    assert normalized["nga_objectid"] == "2001"
    assert normalized["nga_accessionnum"] == "1942.9.97"
    assert mandatory_field_warnings(normalized) == []


def test_normalize_record_reports_no_published_image_as_blocked() -> None:
    dataset = load_dataset(FIXTURES)
    object_row = dataset.objects_by_id["2001"]

    normalized = normalize_record(object_row, None)

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["rights_uri"] is None
    assert normalized["nga_rights_basis"] == "no_published_image"
    assert normalized["representative_media_url"] is None
    assert "missing_rights_uri" in mandatory_field_warnings(normalized)
    assert "missing_representative_media_url" in mandatory_field_warnings(normalized)


def test_normalize_record_reports_no_iiif_url_as_blocked() -> None:
    dataset = load_dataset(FIXTURES)
    object_row = dataset.objects_by_id["2001"]
    image_row = load_csv_file(FIXTURES / "published_images_no_iiif_url.csv")[0]

    normalized = normalize_record(object_row, image_row)

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["nga_rights_basis"] == "no_iiif_url"
    assert normalized["nga_iiifurl"] is None
    assert normalized["representative_media_url"] is None


def test_helpers_are_replay_stable() -> None:
    dataset = load_dataset(FIXTURES)
    normalized = normalize_dataset_record(dataset, "2001")
    payload = {"normalized": normalized}

    assert canonical_json_hash(payload) == canonical_json_hash(payload)
    assert build_collection_url("2001") == "https://www.nga.gov/collection/art-object-page.2001.html"
    assert representative_media_url({"iiifurl": "https://example.test/iiif/abc/"}) == (
        "https://example.test/iiif/abc/full/!1024,1024/0/default.jpg"
    )


def test_normalize_dataset_record_rejects_missing_inputs() -> None:
    dataset = load_dataset(FIXTURES)

    try:
        normalize_dataset_record(dataset, " ")
    except ValueError as exc:
        assert str(exc) == "missing_object_id"
    else:
        raise AssertionError("blank object id was accepted")

    try:
        normalize_dataset_record(dataset, "9999")
    except KeyError as exc:
        assert str(exc) == "'missing_nga_object:9999'"
    else:
        raise AssertionError("missing object id was accepted")
