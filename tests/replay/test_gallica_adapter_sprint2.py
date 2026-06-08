from pathlib import Path

from workers.gallica_adapter.edm import normalize_edm_record
from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

FIXTURES = Path("tests/fixtures/gallica")


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_gallica_sprint2_replay_is_deterministic_for_same_oairecord_and_iiif() -> None:
    payload = {
        "oai_record_xml": fixture("oairecord_french_public_domain.xml"),
        "iiif_manifest": {"rights": CC0_URI},
        "iiif_info": {"width": 1400, "height": 900},
    }

    left = normalize_edm_record(payload)
    right = normalize_edm_record(dict(reversed(list(payload.items()))))

    assert left["raw_payload_hash"] == right["raw_payload_hash"]
    assert left["record_id"] == right["record_id"] == "ark:/12148/bpt6k5619759j"
    assert left["rights_uri"] == right["rights_uri"] == CC0_URI
    assert left["rights_decision"] == right["rights_decision"] == RightsDecision.ALLOWED


def test_gallica_sprint2_replay_blocks_restricted_rights_without_store_write_path() -> None:
    normalized = normalize_edm_record(
        {"oai_record_xml": fixture("oairecord_restricted_rights.xml")}
    )

    assert normalized["record_id"] == "ark:/12148/bpt6k9999999"
    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["gallica_rights_basis"] == "reserved_rights_text"
