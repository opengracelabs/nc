from workers.gallica_adapter.rights import (
    GALLICA_RIGHTS_ADDENDUM_ID,
    classify_rights,
    extract_rights_uri,
    is_allowed_rights,
)
from workers.shared_media_adapter.rights import NKC_URI, PDM_URI, RightsDecision


def test_dc_rights_uri_reuses_shared_classifier() -> None:
    result = classify_rights("http://creativecommons.org/publicdomain/mark/1.0")

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_statement_uri"] == PDM_URI
    assert result["rights_basis"] == "public_domain_mark"
    assert result["rights_policy_id"] == GALLICA_RIGHTS_ADDENDUM_ID
    assert result["rights_source"] == "uri"


def test_extract_rights_uri_from_iiif_style_value() -> None:
    assert (
        extract_rights_uri({"rights": "https://creativecommons.org/publicdomain/zero/1.0/"})
        == "https://creativecommons.org/publicdomain/zero/1.0/"
    )


def test_domaine_public_is_allowed() -> None:
    result = classify_rights("domaine public")

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_statement_uri"] == PDM_URI
    assert result["rights_status"] == "verified_pd"
    assert result["rights_basis"] == "gallica_domaine_public_text"
    assert is_allowed_rights("Domaine Public")


def test_addendum_allowed_patterns_are_allowed() -> None:
    expected = {
        "public domain": "gallica_public_domain_text",
        "libre de reutilisation": "gallica_free_reuse_text",
        "usage commercial autorise": "gallica_commercial_use_authorized_text",
    }

    for text, basis in expected.items():
        result = classify_rights(text)

        assert result["decision"] == RightsDecision.ALLOWED
        assert result["allowed"] is True
        assert result["rights_statement_uri"] == PDM_URI
        assert result["rights_basis"] == basis


def test_domaine_public_revisite_requires_review() -> None:
    result = classify_rights("domaine public revisite")

    assert result["decision"] == RightsDecision.REVIEW_REQUIRED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] == NKC_URI
    assert result["rights_basis"] == "gallica_public_domain_revisited"


def test_droits_reserves_are_blocked() -> None:
    result = classify_rights("droits reserves")

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "reserved_rights_text"


def test_usage_non_commercial_is_blocked() -> None:
    result = classify_rights("usage non-commercial")

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_basis"] == "noncommercial_use_text"


def test_unknown_french_text_requires_review() -> None:
    result = classify_rights("conditions de reutilisation a verifier")

    assert result["decision"] == RightsDecision.REVIEW_REQUIRED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_basis"] == "unknown_gallica_rights_text"


def test_missing_rights_are_blocked() -> None:
    result = classify_rights(None)

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_statement_uri"] is None
    assert result["rights_status"] == "blocked"
    assert result["rights_basis"] == "missing_gallica_rights"
