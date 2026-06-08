from pathlib import Path

from workers.gallica_adapter.edm import (
    canonical_json_hash,
    extract_record_id,
    mandatory_field_warnings,
    normalize_edm_record,
)
from workers.shared_media_adapter.rights import CC0_URI, PDM_URI, RightsDecision

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "gallica"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_extract_record_id_from_gallica_oairecord() -> None:
    raw = {"oai_record_xml": fixture("oairecord_dc_rights_uri.xml")}

    assert extract_record_id(raw) == "ark:/12148/btv1b53066668g"


def test_normalize_prefers_iiif_rights_uri_over_dc_rights() -> None:
    raw = {
        "oai_record_xml": fixture("oairecord_french_public_domain.xml"),
        "iiif_manifest": {"rights": CC0_URI},
        "iiif_info": {"width": 1400, "height": 900},
    }

    normalized = normalize_edm_record(raw)

    assert normalized["record_id"] == "ark:/12148/bpt6k5619759j"
    assert normalized["title"] == "Page illustree de test"
    assert normalized["rights_uri"] == CC0_URI
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True
    assert normalized["representative_media_url"] == (
        "https://gallica.bnf.fr/iiif/ark:/12148/bpt6k5619759j/f1/full/full/0/native.jpg"
    )
    assert normalized["width_px"] == 1400
    assert normalized["height_px"] == 900


def test_normalize_uses_iiif_manifest_license_fallback() -> None:
    raw = {
        "oai_record_xml": fixture("oairecord_restricted_rights.xml"),
        "iiif_manifest": {"license": PDM_URI},
    }

    normalized = normalize_edm_record(raw)

    assert normalized["rights_uri"] == PDM_URI
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True


def test_normalize_uses_dc_rights_uri_when_iiif_rights_absent() -> None:
    normalized = normalize_edm_record({"oai_record_xml": fixture("oairecord_dc_rights_uri.xml")})

    assert normalized["rights_uri"] == PDM_URI
    assert normalized["rights_allowed"] is True
    assert normalized["provider"] == "Bibliotheque nationale de France"
    assert normalized["dataProvider"] == "Gallica"


def test_normalize_supports_french_domaine_public_text() -> None:
    normalized = normalize_edm_record(
        {"oai_record_xml": fixture("oairecord_french_public_domain.xml")}
    )

    assert normalized["rights_uri"] == PDM_URI
    assert normalized["gallica_rights_basis"] == "gallica_domaine_public_text"
    assert normalized["rights_decision"] == RightsDecision.ALLOWED


def test_normalize_blocks_restricted_french_rights_text() -> None:
    normalized = normalize_edm_record(
        {"oai_record_xml": fixture("oairecord_restricted_rights.xml")}
    )

    assert normalized["rights_uri"] is None
    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["gallica_rights_basis"] == "reserved_rights_text"


def test_mandatory_field_warnings_report_missing_fields() -> None:
    normalized = normalize_edm_record({"oai_record_xml": "<results />"})

    assert mandatory_field_warnings(normalized) == [
        "missing_record_id",
        "missing_title",
        "missing_rights_uri",
        "missing_description",
        "missing_date",
    ]


def test_raw_payload_hash_is_stable() -> None:
    left = {"oai_record_xml": fixture("oairecord_dc_rights_uri.xml"), "iiif_info": {"width": 1}}
    right = {"iiif_info": {"width": 1}, "oai_record_xml": fixture("oairecord_dc_rights_uri.xml")}

    assert canonical_json_hash(left) == canonical_json_hash(right)
    assert normalize_edm_record(left)["raw_payload_hash"] == normalize_edm_record(right)[
        "raw_payload_hash"
    ]

