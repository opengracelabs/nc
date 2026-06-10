import json
from pathlib import Path

from workers.getty_adapter.store import derive_anchor_type, write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "getty"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_write_record_uses_shared_m36_write_path_for_allowed_getty_object() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
        source_id="source-getty",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "cultural"
    assert conn.args_by_table["source_record"][3] == "getty_linked_art_v1"
    assert conn.args_by_table["media_file"][3] == (
        "https://media.getty.edu/iiif/image/"
        "7ff0a543-569a-4cb0-b92b-cd78877d4141/full/!1024,1024/0/default.jpg"
    )

    raw_payload = json.loads(conn.args_by_table["source_record"][4])
    assert raw_payload["object"]["_label"] == "Irises"
    assert raw_payload["iiif_manifest"]["@type"] == "sc:Manifest"

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["getty_object_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert normalized_payload["getty_rights_uri"] == (
        "https://creativecommons.org/publicdomain/zero/1.0/"
    )
    assert normalized_payload["getty_manifest_uri"] == (
        "https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
    )
    assert normalized_payload["getty_image_service"] == (
        "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
    )
    assert normalized_payload["getty_accession_number"] == "90.PA.20"

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["source"] == "getty"
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["getty_object_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert evidence["getty_rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert evidence["getty_manifest_uri"] == (
        "https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
    )
    assert evidence["getty_image_service"] == (
        "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
    )
    assert evidence["getty_accession_number"] == "90.PA.20"

    technical_content = json.loads(conn.args_by_table["media_technical_metadata"][3])
    assert technical_content["schema_standard"] == "getty_linked_art_v1"
    assert technical_content["getty_accession_number"] == "90.PA.20"


async def test_write_record_rejects_blocked_record_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_unknown_rights.json"),
        source_id="source-getty",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "unknown_rights_uri",
        "record_id": "00000000-0000-4000-8000-000000000002",
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_write_record_rejects_missing_iiif_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_cc0.json"),
        source_id="source-getty",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == "missing_iiif_evidence"
    assert result["writes"] == 0
    assert_no_writes(conn)


def test_derive_anchor_type_marks_getty_views_as_geographic() -> None:
    assert derive_anchor_type({"title": "View of Rome"}, "image") == "geographic"
    assert derive_anchor_type({"title": "Irises"}, "image") == "cultural"
    assert derive_anchor_type({"title": "Irises"}, "map") == "geographic"

