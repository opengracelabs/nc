import json
from pathlib import Path

from workers.mia_adapter.rights import (
    MIA_RIGHTS_POLICY_ID,
    NO_COPYRIGHT_US_URI,
    OBSERVED_RIGHTS_TYPES,
    PUBLIC_DOMAIN_MARK_URI,
    classify_rights,
    is_allowed_rights,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "mia"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def assert_blocked(name: str, basis: str = "blocked_observed_rights_type") -> None:
    rights = classify_rights(fixture_json(name))

    assert rights["decision"] == "BLOCKED"
    assert rights["allowed"] is False
    assert rights["rights_statement_uri"] is None
    assert rights["rights_status"] == "blocked"
    assert rights["rights_basis"] == basis
    assert rights["rights_policy_id"] == MIA_RIGHTS_POLICY_ID
    assert is_allowed_rights(fixture_json(name)) is False


def test_mia_rights_matrix_v2_allows_public_domain_only() -> None:
    rights = classify_rights(fixture_json("object_public_domain_valid_image.json"))

    assert rights == {
        "decision": "ALLOWED",
        "allowed": True,
        "rights_statement_uri": PUBLIC_DOMAIN_MARK_URI,
        "rights_status": "pending_verification",
        "rights_basis": "mia_public_domain",
        "rights_policy_id": MIA_RIGHTS_POLICY_ID,
    }
    assert is_allowed_rights(fixture_json("object_public_domain_valid_image.json")) is True


def test_mia_rights_allows_noc_us() -> None:
    rights = classify_rights(fixture_json("object_noc_us_valid_image.json"))

    assert rights == {
        "decision": "ALLOWED",
        "allowed": True,
        "rights_statement_uri": NO_COPYRIGHT_US_URI,
        "rights_status": "pending_verification",
        "rights_basis": "mia_no_copyright_us",
        "rights_policy_id": MIA_RIGHTS_POLICY_ID,
    }
    assert is_allowed_rights(fixture_json("object_noc_us_valid_image.json")) is True


def test_mia_rights_matrix_v2_blocks_missing_object() -> None:
    rights = classify_rights(None)

    assert rights["decision"] == "BLOCKED"
    assert rights["allowed"] is False
    assert rights["rights_statement_uri"] is None
    assert rights["rights_basis"] == "missing_object"
    assert rights["rights_policy_id"] == MIA_RIGHTS_POLICY_ID


def test_mia_rights_matrix_v2_blocks_missing_rights_type() -> None:
    assert_blocked("object_missing_rights_type.json", "missing_rights_type")


def test_mia_rights_matrix_v2_blocks_in_copyright() -> None:
    assert_blocked("object_in_copyright.json")


def test_mia_rights_matrix_v2_blocks_in_copyright_educational_use() -> None:
    assert_blocked("object_in_copyright_educational_use.json")


def test_restricted_zero_inc_edu_is_blocked() -> None:
    record = fixture_json("object_restricted_zero_inc_edu.json")

    assert record["restricted"] == 0
    assert record["rights_type"] == "In Copyright–Educational Use"
    assert_blocked("object_restricted_zero_inc_edu.json")


def test_mia_rights_matrix_v2_blocks_in_copyright_non_commercial_use() -> None:
    assert_blocked("object_in_copyright_non_commercial_use.json")


def test_mia_rights_matrix_v2_blocks_unknown() -> None:
    assert_blocked("object_unknown_rights.json")


def test_mia_rights_matrix_v2_blocks_not_evaluated() -> None:
    assert_blocked("object_not_evaluated.json")


def test_mia_rights_matrix_v2_blocks_copyright_not_evaluated() -> None:
    assert_blocked("object_copyright_not_evaluated.json")


def test_mia_rights_matrix_v2_blocks_no_known_copyright() -> None:
    assert_blocked("object_no_known_copyright.json")


def test_mia_rights_matrix_v2_blocks_unrecognized_future_rights_type() -> None:
    assert_blocked("object_future_rights_type.json", "blocked_unrecognized_rights_type")


def test_mia_rights_matrix_v2_does_not_allow_unobserved_cc0_or_unrestricted() -> None:
    assert "CC0" not in OBSERVED_RIGHTS_TYPES
    assert "Unrestricted" not in OBSERVED_RIGHTS_TYPES
    assert_blocked("object_cc0_unobserved.json", "blocked_unrecognized_rights_type")
    assert_blocked("object_unrestricted_unobserved.json", "blocked_unrecognized_rights_type")
