import inspect
import json
from pathlib import Path

from workers.nga_adapter import store
from workers.nga_adapter.client import load_dataset
from workers.nga_adapter.store import write_record
from workers.shared_media_adapter.replay import ReplayConn

FIXTURES = Path("tests/fixtures/nga")


def test_nga_store_reuses_shared_media_adapter_write_path() -> None:
    source = inspect.getsource(store)

    assert "write_normalized_record" in source
    assert "INSERT INTO" not in source
    assert "UPDATE source_item" not in source


async def test_nga_media_rights_evidence_includes_required_nga_fields() -> None:
    conn = ReplayConn()

    await write_record(
        conn,
        load_dataset(FIXTURES),
        "2001",
        source_id="source-nga",
        media_type_id="image",
    )

    media_rights_args = conn.args_by_table["media_rights"]
    evidence = json.loads(media_rights_args[2])
    assert media_rights_args[1] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert evidence["source"] == "nga"
    assert evidence["applying_policy"] == "nga_rights_matrix_v1"
    assert evidence["evidence_status"] == "pending_human_review"
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["nga_openaccess"] == "1"
    assert evidence["nga_image_uuid"] == "img-primary-2001"
    assert evidence["nga_iiifurl"] == "https://api.nga.gov/iiif/img-primary-2001"
    assert evidence["nga_iiif_thumb_url"].endswith("/full/200,200/0/default.jpg")
    assert evidence["nga_viewtype"] == "primary"
    assert evidence["nga_objectid"] == "2001"
    assert evidence["nga_accessionnum"] == "1942.9.97"
    assert evidence["rights_matrix_classification"] == "allowed"
