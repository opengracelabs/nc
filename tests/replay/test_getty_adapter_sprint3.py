import json
from pathlib import Path

from workers.getty_adapter.store import write_record
from workers.shared_media_adapter.replay import ReplayConn, assert_m36_write_order, assert_no_writes

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "getty"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_getty_sprint3_replay_writes_allowed_object_full_m36_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
        source_id="source-getty",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["writes"] == 7
    assert_m36_write_order(conn)

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["getty_object_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert evidence["getty_rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert evidence["getty_manifest_uri"] == (
        "https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
    )
    assert evidence["getty_image_service"] == (
        "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
    )
    assert evidence["getty_accession_number"] == "90.PA.20"


async def test_getty_sprint3_replay_blocks_unknown_rights_without_store_write_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_unknown_rights.json"),
        source_id="source-getty",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == "unknown_rights_uri"
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_getty_sprint3_replay_blocks_missing_iiif_without_store_write_path() -> None:
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

