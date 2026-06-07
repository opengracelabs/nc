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
        "missing_description",
        "missing_date",
        "missing_provider",
        "missing_data_provider",
    ]


def test_raw_payload_hash_is_stable() -> None:
    left = {"object": {"id": "/123/abc", "title": ["Yellowstone map"]}}
    right = {"object": {"title": ["Yellowstone map"], "id": "/123/abc"}}

    assert canonical_json_hash(left) == canonical_json_hash(right)
    assert (
        normalize_edm_record(left)["raw_payload_hash"]
        == normalize_edm_record(right)["raw_payload_hash"]
    )


def test_normalize_edm_record_accepts_nested_live_record_shape() -> None:
    raw = {
        "object": {
            "about": "/90402/RP_F_2001_7_1062",
            "type": "IMAGE",
            "organizations": [
                {
                    "about": "http://data.europeana.eu/organization/4579",
                    "prefLabel": {"en": ["Rijksmuseum"]},
                }
            ],
            "europeanaAggregation": {
                "edmRights": {"def": ["http://creativecommons.org/publicdomain/mark/1.0/"]},
                "edmPreview": "https://api.europeana.eu/thumbnail/v2/url.json?uri=example",
                "edmLandingPage": "https://www.europeana.eu/item/90402/RP_F_2001_7_1062",
            },
            "aggregations": [
                {
                    "edmDataProvider": {"def": ["http://data.europeana.eu/organization/4579"]},
                    "edmProvider": {"def": ["http://data.europeana.eu/organization/4579"]},
                    "edmIsShownAt": "http://hdl.handle.net/10934/RM0001.COLLECT.676394",
                    "edmIsShownBy": "https://lh3.googleusercontent.com/example=s0",
                    "webResources": [
                        {
                            "about": "https://lh3.googleusercontent.com/example=s0",
                            "ebucoreHasMimeType": "image/jpeg",
                            "ebucoreWidth": 2500,
                            "ebucoreHeight": 2002,
                            "textAttributionSnippet": "Yellowstone National Park attribution",
                        }
                    ],
                }
            ],
            "proxies": [
                {
                    "europeanaProxy": False,
                    "dcTitle": {"en": ["Yellowstone National Park"]},
                    "dctermsCreated": {"def": ["1891"]},
                    "edmType": "IMAGE",
                }
            ],
        }
    }

    normalized = normalize_edm_record(raw)

    assert normalized["record_id"] == "/90402/RP_F_2001_7_1062"
    assert normalized["title"] == "Yellowstone National Park"
    assert normalized["date"] == "1891"
    assert normalized["rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert normalized["provider"] == "Rijksmuseum"
    assert normalized["dataProvider"] == "Rijksmuseum"
    assert normalized["source_url"] == "http://hdl.handle.net/10934/RM0001.COLLECT.676394"
    assert normalized["representative_media_url"] == "https://lh3.googleusercontent.com/example=s0"
    assert normalized["width_px"] == 2500
    assert normalized["height_px"] == 2002
    assert normalized["rights_allowed"] is True
