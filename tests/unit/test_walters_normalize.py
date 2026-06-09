from pathlib import Path

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision
from workers.walters_adapter.client import load_dataset
from workers.walters_adapter.normalize import (
    canonical_json_hash,
    mandatory_field_warnings,
    normalize_dataset_record,
    normalize_record,
    representative_media_url,
)

FIXTURES = Path("tests/fixtures/walters")


def test_normalize_dataset_record_maps_walters_object_and_evidence() -> None:
    dataset = load_dataset(FIXTURES)
    normalized = normalize_dataset_record(dataset, "1001")

    assert normalized["record_id"] == "1001"
    assert normalized["title"] == "Leaf from a Book of Hours"
    assert normalized["rights_uri"] == CC0_URI
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True
    assert normalized["source_url"] == "https://purl.thewalters.org/art/W.174"
    assert normalized["representative_media_url"] == (
        "https://art.thewalters.org/images/raw/W174_fnt.jpg"
    )
    assert normalized["preview_urls"] == [
        "https://art.thewalters.org/images/raw/W174_fnt.jpg",
        "https://art.thewalters.org/images/raw/W174_det.jpg",
    ]
    assert normalized["creator"] == "Master of Walters W.174; Unknown scribe"
    assert normalized["creator_nationality"] == "French; French"
    assert normalized["description"] == "Illuminated manuscript leaf."
    assert normalized["date_start"] == 1450
    assert normalized["date_end"] == 1475
    assert normalized["walters_object_id"] == "1001"
    assert normalized["walters_object_number"] == "W.174"
    assert normalized["walters_image_url"] == (
        "https://art.thewalters.org/images/raw/W174_fnt.jpg"
    )
    assert normalized["walters_media_xref_id"] == "2001"
    assert normalized["walters_collection_ids"] == ["MAN", "MED"]
    assert normalized["walters_collection_names"] == ["Manuscripts", "Medieval"]
    assert mandatory_field_warnings(normalized) == []


def test_normalize_record_reports_no_primary_image_as_blocked() -> None:
    dataset = load_dataset(FIXTURES)
    object_row = dataset.objects_by_id["1001"]

    normalized = normalize_record(object_row, None)

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["rights_uri"] is None
    assert normalized["walters_rights_basis"] == "no_primary_image"
    assert normalized["representative_media_url"] is None
    assert "missing_rights_uri" in mandatory_field_warnings(normalized)
    assert "missing_representative_media_url" in mandatory_field_warnings(normalized)


def test_normalize_record_reports_missing_image_url_as_blocked() -> None:
    dataset = load_dataset(FIXTURES)
    object_row = dataset.objects_by_id["1003"]
    image_row = dataset.media_by_object_id["1003"][0]

    normalized = normalize_record(object_row, image_row, all_images=[image_row])

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["walters_rights_basis"] == "missing_image_url"
    assert normalized["walters_image_url"] is None
    assert normalized["representative_media_url"] is None


def test_helpers_are_replay_stable() -> None:
    dataset = load_dataset(FIXTURES)
    normalized = normalize_dataset_record(dataset, "1001")
    payload = {"normalized": normalized}

    assert canonical_json_hash(payload) == canonical_json_hash(payload)
    assert representative_media_url({"ImageURL": "https://example.test/image.jpg"}) == (
        "https://example.test/image.jpg"
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
        assert str(exc) == "'missing_walters_object:9999'"
    else:
        raise AssertionError("missing object id was accepted")
