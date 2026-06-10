import json
from pathlib import Path

from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)
from workers.yale_adapter.store import derive_anchor_type, write_record

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "yale"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_write_record_uses_shared_m36_write_path_for_ycba_allowed_object() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("ycba_object_cc0.json"),
        manifest=fixture_json("manifest_ycba_12345_v3.json"),
        source_id="source-ycba",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "12345"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "yale_lux_linked_art_v1"
    assert conn.args_by_table["media_file"][3] == (
        "https://media.collections.yale.edu/iiif/2/ycba-12345/full/!1024,1024/0/default.jpg"
    )

    raw_payload = json.loads(conn.args_by_table["source_record"][4])
    assert raw_payload["object"]["object_id"] == "12345"
    assert raw_payload["iiif_manifest"]["type"] == "Manifest"

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["yale_object_id"] == "12345"
    assert normalized_payload["ycba_rights_uri"] == (
        "https://creativecommons.org/publicdomain/zero/1.0/"
    )
    assert normalized_payload["ycba_attribution"] == "Yale Center for British Art"
    assert normalized_payload["yale_iiif_manifest"] == (
        "https://manifests.collections.yale.edu/ycba/obj/12345"
    )
    assert normalized_payload["yale_image_service"] == (
        "https://media.collections.yale.edu/iiif/2/ycba-12345"
    )

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["source"] == "ycba"
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["ycba_rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert evidence["ycba_attribution"] == "Yale Center for British Art"
    assert evidence["yale_object_id"] == "12345"
    assert evidence["yale_iiif_manifest"] == "https://manifests.collections.yale.edu/ycba/obj/12345"
    assert evidence["yale_image_service"] == "https://media.collections.yale.edu/iiif/2/ycba-12345"

    technical_content = json.loads(conn.args_by_table["media_technical_metadata"][3])
    assert technical_content["schema_standard"] == "yale_lux_linked_art_v1"
    assert technical_content["yale_object_id"] == "12345"
    assert technical_content["ycba_attribution"] == "Yale Center for British Art"


async def test_write_record_uses_yuag_evidence_for_allowed_yuag_object() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("yuag_object_noc_us.json"),
        manifest=fixture_json("manifest_yuag_98765_v3.json"),
        source_id="source-yuag",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "98765"
    assert result["writes"] == 7
    assert_m36_write_order(conn)

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["source"] == "yuag"
    assert evidence["worker_classified_status"] == "classified_pd"
    assert evidence["yuag_rights_uri"] == "http://rightsstatements.org/vocab/NoC-US/1.0/"
    assert evidence["yale_object_id"] == "98765"
    assert evidence["yale_iiif_manifest"] == "https://manifests.collections.yale.edu/yuag/obj/98765"
    assert evidence["yale_image_service"] == "https://media.collections.yale.edu/iiif/2/yuag-98765"
    assert "ycba_attribution" not in evidence


async def test_write_record_rejects_blocked_record_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("ycba_object_restricted.json"),
        source_id="source-ycba",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "unknown_rights_uri",
        "record_id": "55555",
        "writes": 0,
    }
    assert_no_writes(conn)


def test_derive_anchor_type_marks_ycba_views_as_geographic() -> None:
    assert derive_anchor_type({"title": "A View of Snowdon"}, "image") == "geographic"
    assert derive_anchor_type({"title": "The Windmill"}, "image") == "cultural"
    assert derive_anchor_type({"title": "The Windmill"}, "map") == "geographic"
