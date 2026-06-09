import json
from pathlib import Path

from workers.shared_media_adapter.rights import CC0_URI, RightsDecision
from workers.smk_adapter.rights import SMK_RIGHTS_POLICY_ID, classify_rights, is_allowed_rights

FIXTURES = Path("tests/fixtures/smk")


def load_record(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))["items"][0]


def test_smk_rights_matrix_allows_public_domain_object_with_image() -> None:
    result = classify_rights(load_record("object_kms1_public_domain.json"))

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_statement_uri"] == CC0_URI
    assert result["rights_status"] == "pending_verification"
    assert result["rights_basis"] == "smk_public_domain"
    assert result["rights_policy_id"] == SMK_RIGHTS_POLICY_ID


def test_smk_rights_matrix_allows_first_image_url_when_native_image_missing() -> None:
    record = load_record("object_kms1_public_domain.json")
    record["image_native"] = ""

    result = classify_rights(record)

    assert result["decision"] == RightsDecision.ALLOWED
    assert is_allowed_rights(record)


def test_smk_rights_matrix_does_not_use_image_iiif_id_as_image_fallback() -> None:
    record = load_record("object_kms1_public_domain.json")
    record["image_native"] = ""
    record["images"] = []

    result = classify_rights(record)

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "no_image_url"


def test_smk_rights_matrix_blocks_not_public_domain() -> None:
    result = classify_rights(load_record("object_not_public_domain.json"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "not_public_domain"
    assert not is_allowed_rights(load_record("object_not_public_domain.json"))


def test_smk_rights_matrix_blocks_missing_public_domain() -> None:
    result = classify_rights(load_record("object_missing_public_domain.json"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "missing_rights_field"


def test_smk_rights_matrix_blocks_public_domain_without_image() -> None:
    result = classify_rights(load_record("object_public_domain_no_image.json"))

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "no_image_url"


def test_smk_rights_matrix_blocks_none_payload() -> None:
    result = classify_rights(None)

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "missing_rights_field"

