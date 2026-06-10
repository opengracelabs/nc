import json
from pathlib import Path

from workers.nasa_adapter.rights import NO_COPYRIGHT_US_URI, classify_rights, is_allowed_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nasa"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_nasa_rights_allows_center_allowlist() -> None:
    rights = classify_rights(fixture_json("record_allowed_jsc_image.json"))

    assert rights["decision"] == "ALLOWED"
    assert rights["allowed"] is True
    assert rights["rights_statement_uri"] == NO_COPYRIGHT_US_URI
    assert rights["rights_basis"] == "federal_center_clean_rights"
    assert is_allowed_rights(fixture_json("record_allowed_jsc_image.json")) is True


def test_nasa_rights_jpl_is_review_required() -> None:
    rights = classify_rights(fixture_json("record_jpl_review_image.json"))

    assert rights["decision"] == "REVIEW_REQUIRED"
    assert rights["allowed"] is False
    assert rights["rights_statement_uri"] == NO_COPYRIGHT_US_URI
    assert rights["rights_basis"] == "review_center_jpl"


def test_nasa_rights_esa_csa_jaxa_are_review_required() -> None:
    for name, marker in (
        ("record_esa_review_image.json", "ESA"),
        ("record_csa_review_image.json", "CSA"),
        ("record_jaxa_review_image.json", "JAXA"),
    ):
        rights = classify_rights(fixture_json(name))
        assert rights["decision"] == "REVIEW_REQUIRED"
        assert rights["allowed"] is False
        assert marker in rights["partner_markers"]
        assert rights["rights_basis"] == "review_partner_marker"


def test_nasa_rights_getty_ap_reuters_are_blocked() -> None:
    for name, marker in (
        ("record_getty_blocked_image.json", "Getty"),
        ("record_ap_blocked_image.json", "AP"),
        ("record_reuters_blocked_image.json", "Reuters"),
    ):
        rights = classify_rights(fixture_json(name))
        assert rights["decision"] == "BLOCKED"
        assert rights["allowed"] is False
        assert rights["rights_statement_uri"] is None
        assert marker in rights["partner_markers"]
        assert rights["rights_basis"] == "blocked_partner_marker"


def test_nasa_rights_blocks_non_image_and_missing_object() -> None:
    assert classify_rights(fixture_json("record_video_blocked.json"))["rights_basis"] == (
        "unsupported_media_type"
    )
    assert classify_rights(None)["rights_basis"] == "missing_object"


def test_nasa_rights_stsci_aura_are_review_required() -> None:
    for name, marker in (
        ("record_stsci_review_image.json", "STScI"),
        ("record_aura_review_image.json", "AURA"),
    ):
        rights = classify_rights(fixture_json(name))
        assert rights["decision"] == "REVIEW_REQUIRED"
        assert rights["allowed"] is False
        assert marker in rights["partner_markers"]
        assert rights["rights_basis"] == "review_partner_marker"


def test_nasa_rights_publicity_risk_requires_review() -> None:
    rights = classify_rights(fixture_json("record_publicity_risk_review_image.json"))

    assert rights["decision"] == "REVIEW_REQUIRED"
    assert rights["allowed"] is False
    assert rights["rights_basis"] == "publicity_risk_detected"
    assert rights["publicity_risk_markers"] == ["commercial use", "endorsement", "publicity"]
