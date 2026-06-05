"""Migration 18 LOC maps proof-of-concept replay tests."""
from pathlib import Path

from workers.loc_maps_asset_worker.adapter import (
    HAYDEN_IIIF_SERVICE,
    adapter_inputs,
    build_canonical_asset_record,
    extract_loc_map_rights,
    loc_maps_raw_paths,
)

MIGRATION_18 = Path("infrastructure/postgres/init/18_loc_maps_activation.sql")


def _loc_item_json() -> dict:
    return {
        "item": {
            "date": "1871",
            "title": "Yellowstone National Park : 1871",
            "created_published": ["[S.l.], 1871."],
            "contributor_names": [
                "United States. Department of the Interior",
                "Hayden, F.V. (Ferdinand Vandeveer), 1829-1887",
                "Hergesheimer, E. (Edwin)",
                "Bien, Julius, 1826-1909",
                "Geological Survey of the Territories (U.S.)",
            ],
            "subject_headings": [
                "Parks",
                "United States--Wyoming--Yellowstone National Park",
            ],
            "language": ["english"],
            "description": [
                "Available also through the Library of Congress Web site as a raster image. "
                "3 copies; 1 accompanied by Act establishing Park."
            ],
            "digital_id": ["http://hdl.loc.gov/loc.gmd/g4262y.ye000023"],
            "library_of_congress_control_number": "97683567",
            "call_number": ["G4262.Y4 1871 .U5 TIL"],
            "rights": [
                "The content of the Library of Congress Geography and Map Division "
                "digitized collections is free to use and reuse unless a Rights "
                "Advisory statement is present that indicates otherwise."
            ],
        }
    }


def test_migration_18_registers_loc_and_seeds_yellowstone() -> None:
    sql = MIGRATION_18.read_text()

    assert "INSERT INTO sources" in sql
    assert "'loc'" in sql
    assert "'Library of Congress'" in sql
    assert "'loc_maps'" in sql
    assert "'nc:geo/yellowstone-national-park'" in sql
    assert "United States--Wyoming--Yellowstone National Park" in sql


def test_migration_18_adds_only_loc_map_poc_tables() -> None:
    sql = MIGRATION_18.read_text()

    assert "CREATE TABLE IF NOT EXISTS loc_map_asset_candidates" in sql
    assert "CREATE TABLE IF NOT EXISTS loc_map_rights_evidence" in sql
    assert "asset_class = 'map' AND asset_subclass = 'historic_map'" in sql
    assert "source_record_id = 'loc:97683567'" in sql
    assert "INSERT INTO collection_assets" not in sql
    assert "a.asset_type = 'bhl_illustration'" not in sql


def test_migration_18_activates_loc_asset_as_unknown_legacy_type() -> None:
    sql = MIGRATION_18.read_text()

    assert "INSERT INTO assets" in sql
    assert "'loc_maps:97683567'" in sql
    assert "'unknown'" in sql
    assert "'asset_class', 'map'" in sql
    assert "'asset_subclass', 'historic_map'" in sql
    assert "Deliberately no insert into collection_assets" in sql


def test_loc_maps_adapter_inputs_are_exact_for_hayden_map() -> None:
    inputs = adapter_inputs(place_id="yellowstone-place-id", fetched_at="2026-06-05T00:00:00Z")

    assert inputs["adapter_id"] == "loc_maps_asset_adapter_v1"
    assert inputs["source_profile_id"] == "loc_maps"
    assert inputs["target"]["loc_item_id"] == "97683567"
    assert inputs["target"]["loc_resource_id"] == "g4262y.ye000023"
    assert inputs["policy"]["allowed_asset_classes"] == ["map"]


def test_loc_maps_rights_extractor_maps_1871_item_to_public_domain_reviewed_gate() -> None:
    rights = extract_loc_map_rights(_loc_item_json())

    assert rights["rights_extractor_id"] == "loc_maps_rights_extractor_v1"
    assert rights["source_record_id"] == "loc:97683567"
    assert rights["normalized_rights_status"] == "Public Domain"
    assert rights["commercial_reuse"] == "allowed"
    assert rights["requires_human_review"] is True


def test_loc_maps_adapter_builds_canonical_map_record() -> None:
    record = build_canonical_asset_record(
        item_json=_loc_item_json(),
        place_id="yellowstone-place-id",
        fetched_at="2026-06-05T00:00:00Z",
    )

    assert record["asset_class"] == "map"
    assert record["asset_subclass"] == "historic_map"
    assert record["legacy_asset_type"] == "unknown"
    assert record["source_id"] == "loc"
    assert record["source_record_id"] == "loc:97683567"
    assert record["source_native_ids"]["loc_resource_id"] == "g4262y.ye000023"
    assert record["title"]["en"] == "Yellowstone National Park : 1871"
    assert record["places"][0]["place_id"] == "yellowstone-place-id"
    assert record["media"]["iiif_image_service"] == HAYDEN_IIIF_SERVICE
    assert record["media"]["files"][0]["role"] == "preservation_master"
    assert record["rights"]["normalized_rights_status"] == "Public Domain"
    assert record["preservation"]["media_raw_path"].endswith("/ye000023.tif")


def test_loc_maps_storage_paths_are_deterministic() -> None:
    paths = loc_maps_raw_paths("loc_maps:97683567")

    assert paths["raw_payload_path"] == (
        "raw/loc/maps/loc_maps:97683567/97683567/item.json"
    )
    assert paths["iiif_info_path"].endswith("/iiif-info.json")
    assert paths["media_raw_path"].endswith("/ye000023.tif")
    assert paths["normalized_path"].endswith("/canonical_asset_record.json")
