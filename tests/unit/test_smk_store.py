import json
from pathlib import Path

from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)
from workers.smk_adapter.normalize import normalize_record
from workers.smk_adapter.store import derive_anchor_type, write_record

FIXTURES = Path("tests/fixtures/smk")


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_derive_anchor_type_marks_asset_zero_as_geographic() -> None:
    normalized = normalize_record(load_json("object_kms3696_public_domain.json"))

    assert derive_anchor_type(normalized, "image") == "geographic"


def test_derive_anchor_type_marks_biological_subjects_as_biological() -> None:
    normalized = {"subject_terms": ["Birds", "Flowers"], "title": "Study"}

    assert derive_anchor_type(normalized, "image") == "biological"


async def test_write_record_uses_shared_m36_write_path_for_asset_zero() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("object_kms3696_public_domain.json"),
        source_id="source-smk",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "KMS3696"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "smk_openaccess_v1"
    assert conn.args_by_table["media_file"][3].startswith("https://api.smk.dk/api/v1/download/")

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["smk_public_domain"] is True
    assert normalized_payload["smk_manifest_url"] == (
        "https://api.smk.dk/api/v1/iiif/manifest?id=KMS3696"
    )
    assert normalized_payload["smk_image_rights"] == (
        "https://creativecommons.org/publicdomain/mark/1.0/"
    )


async def test_write_record_rejects_not_public_domain_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("object_not_public_domain.json"),
        source_id="source-smk",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "not_public_domain",
        "record_id": "KMS1",
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_write_record_rejects_missing_image_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("object_public_domain_no_image.json"),
        source_id="source-smk",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "no_image_url",
        "record_id": "KMS1",
        "writes": 0,
    }
    assert_no_writes(conn)
