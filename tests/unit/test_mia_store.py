import json
from pathlib import Path

from workers.mia_adapter.store import derive_anchor_type, write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "mia"
REQUIRED_MIA_EVIDENCE_FIELDS = {
    "mia_object_id",
    "mia_rights_type",
    "mia_rights_uri",
    "mia_rights_image_display",
    "mia_image",
    "mia_public_access",
    "mia_restricted",
    "mia_primary_rendition_number",
    "mia_cache_location",
    "mia_image_width",
    "mia_image_height",
    "mia_accession_number",
    "mia_source_record_uri",
    "mia_image_url",
    "mia_iiif_manifest_url",
}


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_write_record_uses_shared_m36_write_path_for_public_domain_valid_image() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_public_domain_valid_image.json"),
        source_id="source-mia",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "278"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "cultural"
    assert conn.args_by_table["source_record"][3] == "mia_collection_json_v1"
    assert conn.args_by_table["media_file"][3] == "https://5.api.artsmia.org/800/278.jpg"

    raw_payload = json.loads(conn.args_by_table["source_record"][4])
    assert raw_payload["object"]["title"] == "Mia Fixture 278"

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["mia_object_id"] == "278"
    assert normalized_payload["mia_rights_type"] == "Public Domain"
    assert normalized_payload["mia_restricted"] == 0
    assert normalized_payload["mia_public_access"] == 1

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert REQUIRED_MIA_EVIDENCE_FIELDS.issubset(evidence)
    assert evidence["source"] == "mia"
    assert evidence["worker_classified_status"] == "classified_pd"
    assert evidence["rights_matrix_classification"] == "allowed"
    assert evidence["mia_object_id"] == "278"
    assert evidence["mia_rights_type"] == "Public Domain"
    assert evidence["mia_rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert evidence["mia_restricted"] == 0
    assert evidence["mia_public_access"] == 1

    technical_content = json.loads(conn.args_by_table["media_technical_metadata"][3])
    assert technical_content["schema_standard"] == "mia_collection_json_v1"
    assert technical_content["mia_accession_number"] == "278.1"


async def test_write_record_rejects_restricted_zero_inc_edu_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_restricted_zero_inc_edu.json"),
        source_id="source-mia",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "blocked_observed_rights_type",
        "record_id": "1003",
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_write_record_rejects_public_domain_missing_image_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_public_domain_missing_image.json"),
        source_id="source-mia",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "missing_media_candidate",
        "record_id": "279",
        "writes": 0,
    }
    assert_no_writes(conn)


def test_derive_anchor_type_marks_mia_views_as_geographic() -> None:
    assert derive_anchor_type({"title": "View of Minneapolis"}, "image") == "geographic"
    assert derive_anchor_type({"title": "Mia Fixture 278"}, "image") == "cultural"
    assert derive_anchor_type({"title": "Mia Fixture 278"}, "map") == "geographic"
