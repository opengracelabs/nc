import inspect
import json
from pathlib import Path

from workers.met_adapter import store
from workers.met_adapter.store import write_record
from workers.shared_media_adapter.replay import ReplayConn

FIXTURES = Path("tests/fixtures/met")


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_met_store_reuses_shared_media_adapter_write_path() -> None:
    source = inspect.getsource(store)

    assert "write_normalized_record" in source
    assert "INSERT INTO" not in source
    assert "UPDATE source_item" not in source


async def test_met_media_rights_evidence_uses_met_policy_and_pending_human_review() -> None:
    conn = ReplayConn()

    await write_record(
        conn,
        load_json("object_hokusai_public_domain.json"),
        source_id="source-met",
        media_type_id="image",
    )

    media_rights_args = conn.args_by_table["media_rights"]
    evidence = json.loads(media_rights_args[2])
    assert media_rights_args[1] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert evidence["source"] == "met"
    assert evidence["applying_policy"] == "met_rights_matrix_v1"
    assert evidence["evidence_status"] == "pending_human_review"
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["met_is_public_domain"] is True
    assert evidence["rights_matrix_classification"] == "allowed"

