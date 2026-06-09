import json
from pathlib import Path

from workers.aic_adapter.normalize import normalize_record
from workers.aic_adapter.store import derive_anchor_type, write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

FIXTURES = Path("tests/fixtures/aic")


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_derive_anchor_type_marks_la_grande_jatte_as_geographic() -> None:
    normalized = normalize_record(load_json("artwork_seurat_public_domain.json"))

    assert derive_anchor_type(normalized, "image") == "geographic"


def test_derive_anchor_type_marks_biological_subjects_as_biological() -> None:
    normalized = {"subject_terms": ["Birds", "Flowers"], "place_of_origin": "France"}

    assert derive_anchor_type(normalized, "image") == "biological"


async def test_write_record_uses_shared_m36_write_path_for_la_grande_jatte() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("artwork_seurat_public_domain.json"),
        source_id="source-aic",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "27992"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "aic_openaccess_v1"
    assert conn.args_by_table["media_file"][3] == (
        "https://www.artic.edu/iiif/2/"
        "12345678-aaaa-bbbb-cccc-123456789abc/full/843,/0/default.jpg"
    )

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["aic_is_public_domain"] is True
    assert normalized_payload["aic_manifest_url"] == (
        "https://api.artic.edu/api/v1/artworks/27992/manifest.json"
    )


async def test_write_record_rejects_not_public_domain_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("artwork_not_public_domain.json"),
        source_id="source-aic",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "not_public_domain",
        "record_id": "90001",
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_write_record_rejects_missing_image_id_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("artwork_public_domain_no_image_id.json"),
        source_id="source-aic",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "no_image_id",
        "record_id": "90003",
        "writes": 0,
    }
    assert_no_writes(conn)

