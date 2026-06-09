import inspect
import json
from pathlib import Path

from workers.cma_adapter import store
from workers.cma_adapter.store import write_record
from workers.shared_media_adapter.replay import ReplayConn

FIXTURES = Path("tests/fixtures/cma")


def load_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_cma_store_reuses_shared_media_adapter_write_path() -> None:
    source = inspect.getsource(store)

    assert "write_normalized_record" in source
    assert "INSERT INTO" not in source
    assert "UPDATE source_item" not in source


async def test_cma_media_rights_evidence_includes_required_cma_fields() -> None:
    conn = ReplayConn()

    await write_record(
        conn,
        load_json("artwork_cloudy_mountains_cc0.json"),
        source_id="source-cma",
        media_type_id="image",
    )

    media_rights_args = conn.args_by_table["media_rights"]
    evidence = json.loads(media_rights_args[2])
    assert media_rights_args[1] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert evidence["source"] == "cma"
    assert evidence["applying_policy"] == "cma_rights_matrix_v1"
    assert evidence["evidence_status"] == "pending_human_review"
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["cma_share_license_status"] == "CC0"
    assert evidence["cma_copyright"] is None
    assert evidence["cma_accession_number"] == "1933.220"
    assert evidence["cma_image_web_url"].endswith("1933.220_web.jpg")
    assert evidence["cma_image_print_url"].endswith("1933.220_print.jpg")
    assert evidence["cma_image_full_url"].endswith("1933.220_full.tif")
    assert evidence["rights_matrix_classification"] == "allowed"
