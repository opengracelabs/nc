from workers.shared_media_adapter.rights import CC0_URI
from workers.wikidata_adapter.rights import classify_license, evidence_rights, is_allowed_evidence


def test_wikidata_rights_allows_cc0_evidence() -> None:
    rights = classify_license("http://creativecommons.org/publicdomain/zero/1.0/legalcode")

    assert rights["decision"] == "ALLOWED"
    assert rights["allowed"] is True
    assert rights["license_uri"] == CC0_URI
    assert rights["rights_basis"] == "cc0_structured_data"
    assert rights["commercial_media_allowed"] is False
    assert is_allowed_evidence("CC0") is True


def test_wikidata_rights_blocks_non_cc0_evidence() -> None:
    rights = classify_license("https://creativecommons.org/licenses/by/4.0/")

    assert rights["decision"] == "BLOCKED"
    assert rights["allowed"] is False
    assert rights["rights_basis"] == "non_cc0_wikidata_evidence"
    assert is_allowed_evidence("https://creativecommons.org/licenses/by/4.0/") is False


def test_wikidata_evidence_rights_defaults_to_cc0() -> None:
    rights = evidence_rights()

    assert rights["decision"] == "ALLOWED"
    assert rights["license_uri"] == CC0_URI

