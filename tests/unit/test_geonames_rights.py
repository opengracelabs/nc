from workers.geonames_adapter.config import CC_BY_4_URI
from workers.geonames_adapter.rights import build_attribution, classify_license, is_allowed_evidence


def test_geonames_rights_allows_cc_by_4_with_attribution() -> None:
    rights = classify_license("http://creativecommons.org/licenses/by/4.0")

    assert rights["decision"] == "ALLOWED"
    assert rights["allowed"] is True
    assert rights["license_uri"] == CC_BY_4_URI
    assert rights["rights_basis"] == "cc_by_4_attribution_required"
    assert rights["attribution_required"] is True
    assert rights["commercial_media_allowed"] is False
    assert is_allowed_evidence("CC BY 4.0") is True


def test_geonames_rights_blocks_non_cc_by_4() -> None:
    rights = classify_license("CC0")

    assert rights["decision"] == "BLOCKED"
    assert rights["allowed"] is False
    assert rights["rights_basis"] == "non_cc_by_4_geonames_evidence"


def test_geonames_attribution_metadata_includes_identifier() -> None:
    attribution = build_attribution("5843591")

    assert attribution["name"] == "GeoNames"
    assert attribution["license"] == CC_BY_4_URI
    assert attribution["geonames_id"] == "5843591"
    assert "GeoNames" in attribution["statement"]

