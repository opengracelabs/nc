from workers.europeana_adapter.rights import classify_rights as europeana_classify_rights
from workers.rijksmuseum_adapter.rights import RightsDecision, classify_rights, normalize_rights_uri


def test_rijksmuseum_reuses_europeana_rights_classification() -> None:
    uri = "http://creativecommons.org/publicdomain/mark/1.0/"

    assert classify_rights(uri) == europeana_classify_rights(uri)
    assert classify_rights(uri)["decision"] == RightsDecision.ALLOWED
    assert normalize_rights_uri(uri) == "https://creativecommons.org/publicdomain/mark/1.0/"


def test_rijksmuseum_blocks_creative_commons_restricted_licenses() -> None:
    result = classify_rights("https://creativecommons.org/licenses/by-nc-sa/4.0/")

    assert result["decision"] == RightsDecision.BLOCKED
    assert result["rights_basis"] == "blocked_rights_statement"
