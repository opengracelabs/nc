import json
from pathlib import Path

from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)
from workers.smk_adapter.store import write_record

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "smk"


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_smk_sprint3_replay_writes_asset_zero_full_m36_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        load_json("object_kms3696_public_domain.json"),
        source_id="source-smk",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "KMS3696"
    assert result["source_item_id"] == "source_item-1"
    assert result["source_record_id"] == "source_record-2"
    assert result["media_file_id"] == "media_file-3"
    assert result["media_rights_id"] == "media_rights-4"
    assert result["technical_metadata_id"] == "media_technical_metadata-6"
    assert result["workflow_item_id"] is None
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)

    preservation_args = conn.args_by_table["preservation_event"]
    assert preservation_args[4] == "rights_verification"
    assert preservation_args[5] == "pending_human_review"

    media_rights_args = conn.args_by_table["media_rights"]
    evidence = json.loads(media_rights_args[2])
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["smk_public_domain"] is True
    assert evidence["smk_object_number"] == "KMS3696"
    assert evidence["smk_manifest_url"] == "https://api.smk.dk/api/v1/iiif/manifest?id=KMS3696"
    assert evidence["smk_image_rights"] == "https://creativecommons.org/publicdomain/mark/1.0/"


async def test_smk_sprint3_replay_blocks_no_image_without_store_write_path() -> None:
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
