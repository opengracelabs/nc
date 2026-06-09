from pathlib import Path

from workers.met_adapter.rights import MET_RIGHTS_POLICY_ID, classify_rights, is_allowed_rights
from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

FIXTURES = Path("tests/fixtures/met")


def load_json(name: str) -> dict:
    import json

    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_met_rights_matrix_allows_public_domain_object_with_primary_image() -> None:
    result = classify_rights(load_json("object_hokusai_public_domain.json"))

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_statement_uri"] == CC0_URI
    assert result["rights_status"] == "pending_verification"
    assert result["rights_basis"] == "met_is_public_domain"
    assert result["rights_policy_id"] == MET_RIGHTS_POLICY_ID


def test_met_rights_matrix_blocks_not_public_domain() -> None:
    result = classify_rights(load_json("object_not_public_domain.json"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "not_public_domain"
    assert not is_allowed_rights(load_json("object_not_public_domain.json"))


def test_met_rights_matrix_blocks_missing_rights_field() -> None:
    result = classify_rights(load_json("object_missing_rights_field.json"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "missing_rights_field"


def test_met_rights_matrix_blocks_public_domain_without_primary_image() -> None:
    result = classify_rights(load_json("object_public_domain_no_image.json"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "no_image_url"


def test_met_rights_matrix_blocks_none_payload() -> None:
    result = classify_rights(None)

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "missing_rights_field"

