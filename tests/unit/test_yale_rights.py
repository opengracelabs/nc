import json
from pathlib import Path

from workers.yale_adapter.client import CC0_URI, NOC_US_URI
from workers.yale_adapter.rights import YALE_RIGHTS_POLICY_ID, classify_rights, is_allowed_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "yale"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_missing_object_is_blocked() -> None:
    rights = classify_rights(None)

    assert rights == {
        "decision": "BLOCKED",
        "allowed": False,
        "rights_statement_uri": None,
        "rights_status": "blocked",
        "rights_basis": "missing_object",
        "rights_policy_id": YALE_RIGHTS_POLICY_ID,
        "source_slug": None,
    }
    assert is_allowed_rights(None) is False


def test_missing_subject_to_is_blocked() -> None:
    record = {"id": "https://lux.collections.yale.edu/data/object/ycba-obj-1"}

    rights = classify_rights(record)

    assert rights["decision"] == "BLOCKED"
    assert rights["allowed"] is False
    assert rights["rights_statement_uri"] is None
    assert rights["rights_basis"] == "missing_subject_to"
    assert rights["source_slug"] == "ycba"


def test_ycba_cc0_uri_is_allowed() -> None:
    rights = classify_rights(fixture_json("ycba_object_cc0.json"))

    assert rights["decision"] == "ALLOWED"
    assert rights["allowed"] is True
    assert rights["rights_statement_uri"] == CC0_URI
    assert rights["rights_status"] == "pending_verification"
    assert rights["rights_basis"] == "ycba_cc0"
    assert rights["source_slug"] == "ycba"


def test_yuag_noc_us_uri_is_allowed() -> None:
    rights = classify_rights(fixture_json("yuag_object_noc_us.json"))

    assert rights["decision"] == "ALLOWED"
    assert rights["allowed"] is True
    assert rights["rights_statement_uri"] == NOC_US_URI
    assert rights["rights_status"] == "pending_verification"
    assert rights["rights_basis"] == "yuag_noc_us"
    assert rights["source_slug"] == "yuag"


def test_unknown_rights_uri_is_blocked() -> None:
    rights = classify_rights(fixture_json("ycba_object_restricted.json"))

    assert rights["decision"] == "BLOCKED"
    assert rights["allowed"] is False
    assert rights["rights_statement_uri"] == "https://rightsstatements.org/vocab/UND/1.0/"
    assert rights["rights_basis"] == "unknown_rights_uri"
    assert rights["source_slug"] == "ycba"

