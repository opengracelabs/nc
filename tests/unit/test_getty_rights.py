import json
from pathlib import Path

from workers.getty_adapter.client import CC0_URI
from workers.getty_adapter.rights import GETTY_RIGHTS_POLICY_ID, classify_rights, is_allowed_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "getty"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_getty_rights_matrix_allows_open_content_cc0() -> None:
    result = classify_rights(fixture_json("object_cc0.json"))

    assert result == {
        "decision": "ALLOWED",
        "allowed": True,
        "rights_statement_uri": CC0_URI,
        "rights_status": "pending_verification",
        "rights_basis": "getty_cc0",
        "rights_policy_id": GETTY_RIGHTS_POLICY_ID,
    }
    assert is_allowed_rights(fixture_json("object_cc0.json")) is True


def test_getty_rights_matrix_blocks_missing_object() -> None:
    result = classify_rights(None)

    assert result["decision"] == "BLOCKED"
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_status"] == "blocked"
    assert result["rights_basis"] == "missing_object"
    assert result["rights_policy_id"] == GETTY_RIGHTS_POLICY_ID


def test_getty_rights_matrix_blocks_missing_referred_to_by() -> None:
    result = classify_rights(fixture_json("object_missing_subject_to.json"))

    assert result["decision"] == "BLOCKED"
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "missing_referred_to_by"


def test_getty_rights_matrix_blocks_missing_subject_to() -> None:
    result = classify_rights(fixture_json("object_missing_subject_to_in_referred_to_by.json"))

    assert result["decision"] == "BLOCKED"
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "missing_subject_to"


def test_getty_rights_matrix_blocks_empty_subject_to() -> None:
    result = classify_rights({"id": "x", "referred_to_by": [{"subject_to": []}]})

    assert result["decision"] == "BLOCKED"
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "no_rights_statement"


def test_getty_rights_matrix_blocks_unknown_rights_uri() -> None:
    result = classify_rights(fixture_json("object_unknown_rights.json"))

    assert result["decision"] == "BLOCKED"
    assert result["allowed"] is False
    assert result["rights_statement_uri"] == "https://rightsstatements.org/vocab/InC/1.0/"
    assert result["rights_status"] == "blocked"
    assert result["rights_basis"] == "unknown_rights_uri"
    assert is_allowed_rights(fixture_json("object_unknown_rights.json")) is False

