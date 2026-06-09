from pathlib import Path

from workers.shared_media_adapter.rights import RightsDecision
from workers.walters_adapter.client import load_dataset
from workers.walters_adapter.normalize import normalize_dataset_record, normalize_record
from workers.walters_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "walters"


def test_walters_sprint2_rights_replay_matrix() -> None:
    dataset = load_dataset(FIXTURES)
    cases = [
        (
            dataset.objects_by_id["1001"],
            dataset.media_by_object_id["1001"][1],
            RightsDecision.ALLOWED,
            "walters_institution_cc0",
        ),
        (
            None,
            dataset.media_by_object_id["1001"][1],
            RightsDecision.BLOCKED,
            "missing_object_record",
        ),
        (dataset.objects_by_id["1001"], None, RightsDecision.BLOCKED, "no_primary_image"),
        (
            dataset.objects_by_id["1003"],
            dataset.media_by_object_id["1003"][0],
            RightsDecision.BLOCKED,
            "missing_image_url",
        ),
    ]

    for object_row, image_row, decision, basis in cases:
        result = classify_rights(object_row, image_row)
        assert result["decision"] == decision
        assert result["rights_basis"] == basis


def test_walters_sprint2_normalization_replay_keeps_walters_evidence() -> None:
    normalized = normalize_dataset_record(load_dataset(FIXTURES), "1001")

    assert normalized["record_id"] == "1001"
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["walters_object_id"] == "1001"
    assert normalized["walters_object_number"] == "W.174"
    assert normalized["walters_image_url"] == (
        "https://art.thewalters.org/images/raw/W174_fnt.jpg"
    )
    assert normalized["walters_media_xref_id"] == "2001"
    assert normalized["walters_collection_ids"] == ["MAN", "MED"]
    assert normalized["walters_collection_names"] == ["Manuscripts", "Medieval"]


def test_walters_sprint2_normalization_replay_blocks_missing_primary_image() -> None:
    dataset = load_dataset(FIXTURES)
    normalized = normalize_record(dataset.objects_by_id["1001"], None)

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["walters_rights_basis"] == "no_primary_image"
    assert normalized["representative_media_url"] is None


def test_walters_sprint2_normalization_replay_blocks_missing_object_record() -> None:
    normalized = normalize_record(None, {"ImageURL": "https://example.test/image.jpg"})

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["walters_rights_basis"] == "missing_object_record"
    assert normalized["record_id"] is None
