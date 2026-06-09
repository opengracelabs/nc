from pathlib import Path

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision
from workers.walters_adapter.client import load_dataset
from workers.walters_adapter.rights import (
    WALTERS_RIGHTS_POLICY_ID,
    classify_rights,
    is_allowed_rights,
)

FIXTURES = Path("tests/fixtures/walters")


def test_walters_rights_matrix_allows_institution_cc0_with_valid_image() -> None:
    dataset = load_dataset(FIXTURES)
    object_row = dataset.objects_by_id["1001"]
    image_row = dataset.media_by_object_id["1001"][1]

    result = classify_rights(object_row, image_row)

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_statement_uri"] == CC0_URI
    assert result["rights_status"] == "pending_verification"
    assert result["rights_basis"] == "walters_institution_cc0"
    assert result["rights_policy_id"] == WALTERS_RIGHTS_POLICY_ID
    assert is_allowed_rights(object_row, image_row)


def test_walters_rights_matrix_blocks_missing_object_row() -> None:
    result = classify_rights(None, {"ImageURL": "https://example.test/image.jpg"})

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "missing_object_record"


def test_walters_rights_matrix_blocks_missing_primary_image() -> None:
    result = classify_rights({"ObjectID": "1001"}, None)

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "no_primary_image"


def test_walters_rights_matrix_blocks_missing_image_url() -> None:
    result = classify_rights({"ObjectID": "1003"}, {"ImageURL": " "})

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "missing_image_url"
