import json
from pathlib import Path

from workers.cma_adapter.rights import CMA_RIGHTS_POLICY_ID, classify_rights, is_allowed_rights
from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

FIXTURES = Path("tests/fixtures/cma")


def load_record(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))["data"]


def test_cma_rights_matrix_allows_cc0_object_with_print_or_web_image() -> None:
    result = classify_rights(load_record("artwork_94979_cc0.json"))

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_statement_uri"] == CC0_URI
    assert result["rights_status"] == "pending_verification"
    assert result["rights_basis"] == "cma_share_license_status_cc0"
    assert result["rights_policy_id"] == CMA_RIGHTS_POLICY_ID


def test_cma_rights_matrix_allows_cc0_when_full_tiff_missing_but_print_exists() -> None:
    record = load_record("artwork_94979_cc0.json")
    record["images"]["full"]["url"] = ""

    result = classify_rights(record)

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["rights_basis"] == "cma_share_license_status_cc0"


def test_cma_rights_matrix_blocks_not_cc0() -> None:
    result = classify_rights(load_record("artwork_not_cc0.json"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "not_cc0"
    assert not is_allowed_rights(load_record("artwork_not_cc0.json"))


def test_cma_rights_matrix_blocks_missing_share_license_status() -> None:
    result = classify_rights(load_record("artwork_missing_share_license_status.json"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "missing_rights_field"


def test_cma_rights_matrix_blocks_cc0_without_print_or_web_image() -> None:
    result = classify_rights(load_record("artwork_cc0_no_web_image.json"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "no_image_url"


def test_cma_rights_matrix_blocks_none_payload() -> None:
    result = classify_rights(None)

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "missing_rights_field"

