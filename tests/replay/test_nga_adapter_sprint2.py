from pathlib import Path

from workers.nga_adapter.client import load_csv_file, load_dataset
from workers.nga_adapter.normalize import normalize_dataset_record, normalize_record
from workers.nga_adapter.rights import classify_rights
from workers.shared_media_adapter.rights import RightsDecision

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nga"


def image_row(name: str) -> dict | None:
    rows = load_csv_file(FIXTURES / name)
    return rows[0] if rows else None


def test_nga_sprint2_rights_replay_matrix() -> None:
    dataset = load_dataset(FIXTURES)
    cases = [
        (dataset.images_by_object_id["2001"][0], RightsDecision.ALLOWED, "nga_open_access_cc0"),
        (None, RightsDecision.BLOCKED, "no_published_image"),
        (
            image_row("published_images_not_open_access.csv"),
            RightsDecision.BLOCKED,
            "not_open_access",
        ),
        (
            image_row("published_images_no_iiif_url.csv"),
            RightsDecision.BLOCKED,
            "no_iiif_url",
        ),
    ]

    for row, decision, basis in cases:
        result = classify_rights(row)
        assert result["decision"] == decision
        assert result["rights_basis"] == basis


def test_nga_sprint2_normalization_replay_keeps_nga_evidence() -> None:
    normalized = normalize_dataset_record(load_dataset(FIXTURES), "2001")

    assert normalized["record_id"] == "2001"
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["nga_openaccess"] == "1"
    assert normalized["nga_image_uuid"] == "img-primary-2001"
    assert normalized["nga_iiifurl"] == "https://api.nga.gov/iiif/img-primary-2001"
    assert normalized["nga_iiif_thumb_url"]
    assert normalized["nga_viewtype"] == "primary"
    assert normalized["nga_objectid"] == "2001"
    assert normalized["nga_accessionnum"] == "1942.9.97"
    assert normalized["school"] == "French"
    assert normalized["place_executed"] == "France"
    assert normalized["creator_nationality"] == "French"


def test_nga_sprint2_normalization_replay_blocks_missing_image_without_media_url() -> None:
    dataset = load_dataset(FIXTURES)
    normalized = normalize_record(dataset.objects_by_id["2001"], None)

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["nga_rights_basis"] == "no_published_image"
    assert normalized["representative_media_url"] is None


def test_nga_sprint2_normalization_replay_blocks_missing_object_record() -> None:
    normalized = normalize_record(None, {"openaccess": "1", "iiifurl": "https://example.test/iiif"})

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["nga_rights_basis"] == "missing_object_record"
    assert normalized["record_id"] is None

