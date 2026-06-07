from workers.europeana_adapter.edm import (
    canonical_json_hash,
    extract_record_id,
    mandatory_field_warnings,
    normalize_edm_record,
)
from workers.europeana_adapter.rights import RightsDecision


def test_extract_record_id_prefers_object_id() -> None:
    raw = {"id": "/fallback/id", "object": {"id": "/123/abc"}}

    assert extract_record_id(raw) == "/123/abc"


def test_normalize_edm_record_extracts_sprint_2_fields() -> None:
    raw = {
        "object": {
            "id": "/123/abc",
            "title": ["Yellowstone map"],
            "rights": ["http://creativecommons.org/publicdomain/mark/1.0/"],
            "provider": ["Europeana"],
            "dataProvider": ["Example Museum"],
        }
    }

    normalized = normalize_edm_record(raw)

    assert normalized["record_id"] == "/123/abc"
    assert normalized["title"] == "Yellowstone map"
    assert normalized["rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert normalized["provider"] == "Europeana"
    assert normalized["dataProvider"] == "Example Museum"
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["rights_allowed"] is True


def test_normalize_edm_record_accepts_top_level_payload_shape() -> None:
    raw = {
        "id": "/123/top",
        "dcTitle": ["Top level title"],
        "edmRights": ["https://rightsstatements.org/vocab/NoC-US/1.0/"],
        "provider": ["Europeana"],
        "dataProvider": ["Example Archive"],
    }

    normalized = normalize_edm_record(raw)

    assert normalized["record_id"] == "/123/top"
    assert normalized["title"] == "Top level title"
    assert normalized["rights_uri"] == "https://rightsstatements.org/vocab/NoC-US/1.0/"
    assert normalized["dataProvider"] == "Example Archive"


def test_normalize_edm_record_blocks_in_copyright_rights() -> None:
    raw = {
        "object": {
            "id": "/123/inc",
            "title": ["Restricted item"],
            "rights": ["https://rightsstatements.org/vocab/InC/1.0/"],
            "provider": ["Europeana"],
            "dataProvider": ["Example Museum"],
        }
    }

    normalized = normalize_edm_record(raw)

    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False


def test_mandatory_field_warnings_report_missing_fields() -> None:
    normalized = normalize_edm_record({"object": {"id": "/123/missing"}})

    assert mandatory_field_warnings(normalized) == [
        "missing_title",
        "missing_rights_uri",
        "missing_provider",
        "missing_data_provider",
    ]


def test_raw_payload_hash_is_stable() -> None:
    left = {"object": {"id": "/123/abc", "title": ["Yellowstone map"]}}
    right = {"object": {"title": ["Yellowstone map"], "id": "/123/abc"}}

    assert canonical_json_hash(left) == canonical_json_hash(right)
    assert normalize_edm_record(left)["raw_payload_hash"] == normalize_edm_record(right)["raw_payload_hash"]
