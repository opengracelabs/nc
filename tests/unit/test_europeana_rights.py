from workers.europeana_adapter.rights import (
    RightsDecision,
    classify_rights,
    is_allowed_rights,
    normalize_rights_uri,
)


def test_cc0_is_allowed() -> None:
    result = classify_rights("http://creativecommons.org/publicdomain/zero/1.0/")

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_status"] == "verified_cc0"
    assert result["rights_basis"] == "cc0_statement"
    assert result["rights_statement_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"


def test_public_domain_mark_is_allowed() -> None:
    result = classify_rights("https://creativecommons.org/publicdomain/mark/1.0")

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_status"] == "verified_pd"
    assert result["rights_basis"] == "public_domain_mark"
    assert result["rights_statement_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"


def test_noc_us_is_allowed() -> None:
    result = classify_rights("http://rightsstatements.org/vocab/NoC-US/1.0/")

    assert result["decision"] == RightsDecision.ALLOWED
    assert result["allowed"] is True
    assert result["rights_status"] == "verified_pd"
    assert result["rights_basis"] == "noc_us_statement"
    assert result["rights_statement_uri"] == "https://rightsstatements.org/vocab/NoC-US/1.0/"


def test_in_copyright_is_blocked() -> None:
    result = classify_rights("https://rightsstatements.org/vocab/InC/1.0/")

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False
    assert result["rights_basis"] == "blocked_rights_statement"


def test_creative_commons_license_is_blocked_unless_cc0() -> None:
    result = classify_rights("https://creativecommons.org/licenses/by/4.0/")

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["allowed"] is False


def test_missing_rights_requires_review_but_is_not_allowed() -> None:
    result = classify_rights(None)

    assert result["decision"] == RightsDecision.REVIEW_REQUIRED
    assert result["allowed"] is False
    assert result["rights_status"] == "pending_verification"
    assert result["rights_basis"] == "missing_rights"


def test_unknown_rights_requires_review_but_is_not_allowed() -> None:
    result = classify_rights("https://example.org/rights/unknown")

    assert result["decision"] == RightsDecision.REVIEW_REQUIRED
    assert result["allowed"] is False
    assert result["rights_status"] == "pending_verification"
    assert result["rights_basis"] == "unknown_rights_statement"


def test_review_required_statements_are_not_blocked() -> None:
    for uri in (
        "https://rightsstatements.org/vocab/NoC-CR/1.0/",
        "https://rightsstatements.org/vocab/NoC-OKLR/1.0/",
        "https://rightsstatements.org/vocab/NKC/1.0/",
    ):
        result = classify_rights(uri)

        assert result["decision"] == RightsDecision.REVIEW_REQUIRED
        assert result["allowed"] is False
        assert result["rights_status"] == "pending_verification"
        assert result["rights_basis"] == "review_required_statement"


def test_is_allowed_rights_matches_allowlist() -> None:
    assert is_allowed_rights("https://creativecommons.org/publicdomain/zero/1.0/")
    assert not is_allowed_rights("https://rightsstatements.org/vocab/InC/1.0/")


def test_normalize_rights_uri_canonicalizes_http_and_trailing_slash() -> None:
    assert (
        normalize_rights_uri("http://rightsstatements.org/vocab/NoC-US/1.0")
        == "https://rightsstatements.org/vocab/NoC-US/1.0/"
    )
