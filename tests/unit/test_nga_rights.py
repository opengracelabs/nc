from pathlib import Path

from workers.nga_adapter.client import load_csv_file, load_dataset
from workers.nga_adapter.rights import NGA_RIGHTS_POLICY_ID, classify_rights, is_allowed_rights
from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

FIXTURES = Path("tests/fixtures/nga")


def image_row(name: str) -> dict | None:
    rows = load_csv_file(FIXTURES / name)
    return rows[0] if rows else None


def test_nga_rights_matrix_allows_openaccess_image_with_iiifurl() -> None:
    dataset = load_dataset(FIXTURES)
    row = dataset.images_by_object_id["2001"][0]

    result = classify_rights(row)

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_statement_uri"] == CC0_URI
    assert result["rights_status"] == "pending_verification"
    assert result["rights_basis"] == "nga_open_access_cc0"
    assert result["rights_policy_id"] == NGA_RIGHTS_POLICY_ID
    assert is_allowed_rights(row)


def test_nga_rights_matrix_blocks_no_published_image() -> None:
    result = classify_rights(None)

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "no_published_image"


def test_nga_rights_matrix_blocks_not_open_access() -> None:
    result = classify_rights(image_row("published_images_not_open_access.csv"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "not_open_access"


def test_nga_rights_matrix_blocks_no_iiif_url() -> None:
    result = classify_rights(image_row("published_images_no_iiif_url.csv"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "no_iiif_url"
