import inspect
import json
from pathlib import Path

from workers.nasa_adapter import store as nasa_store
from workers.nasa_adapter.store import write_record
from workers.shared_media_adapter import store as shared_store
from workers.shared_media_adapter.replay import ReplayConn

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nasa"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def _write_earthrise() -> ReplayConn:
    conn = ReplayConn()
    result = await write_record(
        conn,
        fixture_json("record_earthrise.json"),
        source_id="source-nasa",
        media_type_id="image",
        asset_manifest=fixture_json("asset_as08_14_2383_manifest.json"),
    )
    assert result["status"] == "written"
    return conn


def test_nasa_store_reuses_shared_media_adapter_write_path() -> None:
    source = inspect.getsource(nasa_store.write_record)

    assert "write_normalized_record" in source
    assert "insert into" not in source.lower()


def test_shared_store_remains_sa9r_clean_for_nasa() -> None:
    source = inspect.getsource(shared_store)

    assert "source_slug == \"nasa_images\"" not in source
    assert "source_slug == 'nasa_images'" not in source
    assert "nasa_" not in source
    assert "RIGHTS_EVIDENCE_REGISTRY" not in source
    assert "RightsEvidenceMapping" not in source


def test_store_runtime_receives_callable_evidence_extension() -> None:
    runtime = nasa_store._runtime()

    assert callable(runtime.build_evidence_extension)
    assert runtime.build_evidence_extension({"nasa_id": "x", "other": "y"}) == {"nasa_id": "x"}


def test_media_rights_status_column_is_pending_verification() -> None:
    source = inspect.getsource(shared_store.insert_media_rights)

    assert "source_item_id, rights_status, rights_statement_uri" in source
    assert "'pending_verification'" in source


async def test_evidence_worker_classified_status_is_classified_pd() -> None:
    conn = await _write_earthrise()

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["worker_classified_status"] == "classified_pd"


async def test_media_file_url_comes_from_manifest_orig_asset() -> None:
    conn = await _write_earthrise()

    media_file_url = conn.args_by_table["media_file"][3]
    manifest = fixture_json("asset_as08_14_2383_manifest.json")
    manifest_urls = [item["href"] for item in manifest["collection"]["items"]]
    assert media_file_url in manifest_urls
    assert media_file_url.endswith("~orig.jpg")
