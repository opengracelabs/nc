from workers.shared_media_adapter.contracts import mandatory_field_warnings
from workers.shared_media_adapter.rights import (
    RIGHTS_POLICY_ID,
    RightsDecision,
    classify_rights,
    normalize_rights_uri,
)
from workers.shared_media_adapter.technical import (
    build_technical_metadata,
    content_hash,
    quality_flag,
    validation_status,
)


def _normalized() -> dict:
    return {
        "record_id": "source/1",
        "title": "Shared Asset",
        "description": "A normalized media record.",
        "date": "1890",
        "creator": "Creator",
        "subject_terms": ["Maps", "Yellowstone"],
        "rights_uri": "https://creativecommons.org/publicdomain/mark/1.0/",
        "provider": "Provider",
        "dataProvider": "Data Provider",
        "edm_type": "IMAGE",
        "source_url": "https://example.test/source/1",
        "representative_media_url": "https://example.test/source/1.jpg",
        "preview_urls": ["https://example.test/source/1-preview.jpg"],
        "width_px": "1200",
        "height_px": "900",
        "raw_payload_hash": "0" * 64,
        "rights_decision": "ALLOWED",
        "rights_allowed": True,
    }


def test_shared_rights_classification_matches_governed_matrix() -> None:
    assert RIGHTS_POLICY_ID == "europeana_rights_matrix_v1.0"
    assert normalize_rights_uri("http://creativecommons.org/publicdomain/mark/1.0") == (
        "https://creativecommons.org/publicdomain/mark/1.0/"
    )
    assert classify_rights("http://creativecommons.org/publicdomain/mark/1.0/")["decision"] == (
        RightsDecision.ALLOWED
    )
    assert classify_rights("https://creativecommons.org/licenses/by/4.0/")["decision"] == (
        RightsDecision.BLOCKED
    )


def test_shared_mandatory_field_warnings_contract() -> None:
    assert mandatory_field_warnings(_normalized()) == []
    assert mandatory_field_warnings({}) == [
        "missing_record_id",
        "missing_title",
        "missing_rights_uri",
        "missing_description",
        "missing_date",
        "missing_provider",
        "missing_data_provider",
    ]


def test_shared_technical_metadata_is_source_parameterized_and_stable() -> None:
    content = build_technical_metadata(
        _normalized(),
        media_type_id="image",
        source_slug="test_source",
    )
    reordered = dict(reversed(list(content.items())))

    assert content["source"] == "test_source"
    assert content["schema_standard"] == "edm"
    assert content["width_px"] == 1200
    assert content["height_px"] == 900
    assert content["quality_flag"] == "meets_minimum"
    assert content["subject_terms"] == [
        {"term": "Maps", "controlled_vocabulary": False},
        {"term": "Yellowstone", "controlled_vocabulary": False},
    ]
    assert content_hash(content) == content_hash(reordered)
    assert validation_status(content) == "valid"


def test_shared_quality_and_validation_guards() -> None:
    assert quality_flag(399, 200) == "below_minimum"
    assert quality_flag(None, None) == "unknown_dimensions"

    content = build_technical_metadata(
        {**_normalized(), "representative_media_url": None, "source_url": None},
        media_type_id="image",
        source_slug="test_source",
    )
    assert validation_status(content) == "invalid"
