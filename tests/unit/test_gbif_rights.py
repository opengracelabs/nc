from workers.gbif_adapter.rights import CC_BY_NC_URI, CC_BY_URI, classify_license
from workers.shared_media_adapter.rights import CC0_URI


def test_gbif_rights_allows_cc0_evidence() -> None:
    rights = classify_license("http://creativecommons.org/publicdomain/zero/1.0/legalcode")

    assert rights["decision"] == "ALLOWED"
    assert rights["allowed"] is True
    assert rights["license_uri"] == CC0_URI
    assert rights["rights_basis"] == "cc0_evidence"
    assert rights["attribution_required"] is False
    assert rights["commercial_media_allowed"] is False


def test_gbif_rights_allows_cc_by_evidence_with_attribution() -> None:
    rights = classify_license("https://creativecommons.org/licenses/by/4.0/")

    assert rights["decision"] == "ALLOWED"
    assert rights["allowed"] is True
    assert rights["license_uri"] == CC_BY_URI
    assert rights["rights_basis"] == "cc_by_evidence_attribution_required"
    assert rights["attribution_required"] is True
    assert rights["commercial_media_allowed"] is False


def test_gbif_rights_marks_cc_by_nc_non_commercial_evidence_only() -> None:
    rights = classify_license("https://creativecommons.org/licenses/by-nc/4.0/")

    assert rights["decision"] == "REVIEW_REQUIRED"
    assert rights["allowed"] is False
    assert rights["license_uri"] == CC_BY_NC_URI
    assert rights["rights_status"] == "non_commercial_evidence_only"
    assert rights["rights_basis"] == "cc_by_nc_non_commercial"
    assert rights["commercial_media_allowed"] is False


def test_gbif_rights_blocks_missing_license() -> None:
    rights = classify_license(None)

    assert rights["decision"] == "BLOCKED"
    assert rights["allowed"] is False
    assert rights["license_uri"] is None
    assert rights["rights_basis"] == "missing_license"

