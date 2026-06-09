import inspect
import json
from pathlib import Path

from workers.shared_media_adapter.replay import ReplayConn
from workers.walters_adapter import store
from workers.walters_adapter.client import load_dataset
from workers.walters_adapter.store import write_record

FIXTURES = Path("tests/fixtures/walters")


def test_walters_store_reuses_shared_media_adapter_write_path() -> None:
    source = inspect.getsource(store)

    assert "write_normalized_record" in source
    assert "INSERT INTO" not in source
    assert "UPDATE source_item" not in source


async def test_walters_media_rights_evidence_uses_policy_and_pending_review() -> None:
    conn = ReplayConn()

    await write_record(
        conn,
        load_dataset(FIXTURES),
        "1001",
        source_id="source-walters",
        media_type_id="image",
    )

    media_rights_args = conn.args_by_table["media_rights"]
    evidence = json.loads(media_rights_args[2])
    assert media_rights_args[1] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert evidence["source"] == "walters"
    assert evidence["applying_policy"] == "walters_rights_matrix_v1"
    assert evidence["evidence_status"] == "pending_human_review"
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["walters_object_id"] == "1001"
    assert evidence["walters_object_number"] == "W.174"
    assert evidence["walters_image_url"] == "https://art.thewalters.org/images/raw/W174_fnt.jpg"
    assert evidence["walters_media_xref_id"] == "2001"
    assert evidence["walters_is_primary"] == "1"
    assert evidence["walters_collection_ids"] == ["MAN", "MED"]
    assert evidence["walters_collection_names"] == ["Manuscripts", "Medieval"]
    assert evidence["rights_matrix_classification"] == "allowed"
