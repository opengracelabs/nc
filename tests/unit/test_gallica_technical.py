from pathlib import Path

from workers.gallica_adapter.edm import normalize_edm_record
from workers.gallica_adapter.technical import (
    TECHNICAL_SCHEMA_VERSION,
    VALIDATOR_NAME,
    VALIDATOR_VERSION,
    build_technical_metadata,
    validation_status,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "gallica"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def _catalan_payload() -> dict:
    return {
        "oai_record_xml": fixture("catalan_atlas_oairecord.xml"),
        "iiif_manifest_url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b55002481n/manifest.json",
        "iiif_info": {"width": 6200, "height": 4300},
        "pagination_pages": 6,
        "selected_page": 1,
    }


def test_gallica_technical_constants_are_sprint3_values() -> None:
    assert TECHNICAL_SCHEMA_VERSION == "gallica-technical-v1"
    assert VALIDATOR_NAME == "gallica_adapter.technical"
    assert VALIDATOR_VERSION == "v1"


def test_build_technical_metadata_reuses_shared_visual_contract_with_gallica_fields() -> None:
    normalized = normalize_edm_record(_catalan_payload())

    content = build_technical_metadata(normalized, media_type_id="map")

    assert content["source"] == "gallica"
    assert content["schema_standard"] == "gallica_api_profile_v1"
    assert content["record_id"] == "ark:/12148/btv1b55002481n"
    assert content["media_type_id"] == "map"
    assert content["quality_flag"] == "meets_minimum"
    assert content["gallica_ark"] == "ark:/12148/btv1b55002481n"
    assert content["iiif_manifest_url"].endswith("/manifest.json")
    assert content["iiif_image_service_url"] == (
        "https://gallica.bnf.fr/iiif/ark:/12148/btv1b55002481n/f1"
    )
    assert content["pagination_pages"] == 6
    assert content["selected_page"] == 1
    assert len(content["content_hash"]) == 64
    assert validation_status(content) == "valid"

