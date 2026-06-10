import json
from pathlib import Path

from workers.nara_adapter.rights import (
    NARA_RIGHTS_POLICY_ID,
    PUBLIC_DOMAIN_MARK_URI,
    classify_rights,
    is_allowed_rights,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nara"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_nara_rights_matrix_allows_unrestricted_use_restriction() -> None:
    rights = classify_rights(fixture_json("record_unrestricted.json"))

    assert rights == {
        "decision": "ALLOWED",
        "allowed": True,
        "rights_statement_uri": PUBLIC_DOMAIN_MARK_URI,
        "rights_status": "pending_verification",
        "rights_basis": "nara_unrestricted",
        "rights_policy_id": NARA_RIGHTS_POLICY_ID,
    }
    assert is_allowed_rights(fixture_json("record_unrestricted.json")) is True


def test_nara_rights_matrix_blocks_everything_else() -> None:
    restricted = classify_rights(fixture_json("record_restricted.json"))
    missing = classify_rights(fixture_json("record_missing_use_restriction.json"))
    empty = classify_rights({})

    assert restricted["decision"] == "BLOCKED"
    assert restricted["allowed"] is False
    assert restricted["rights_statement_uri"] is None
    assert restricted["rights_basis"] == "restricted_use"
    assert restricted["rights_policy_id"] == NARA_RIGHTS_POLICY_ID
    assert missing["rights_basis"] == "missing_use_restriction"
    assert empty["rights_basis"] == "missing_object"
    assert is_allowed_rights(fixture_json("record_restricted.json")) is False
