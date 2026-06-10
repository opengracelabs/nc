import inspect
import json
from pathlib import Path

from workers.mia_adapter import store as mia_store
from workers.mia_adapter.store import write_record
from workers.shared_media_adapter import store as shared_store
from workers.shared_media_adapter.replay import ReplayConn, assert_m36_write_order, assert_no_writes

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "mia"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


async def test_mia_sprint3_compliance_allowed_record_writes_all_m36_tables_and_pins() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_public_domain_valid_image.json"),
        source_id="source-mia",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["writes"] == 7
    assert_m36_write_order(conn)
    assert set(conn.args_by_table) >= {
        "source_item",
        "source_record",
        "media_file",
        "media_rights",
        "preservation_event",
        "media_technical_metadata",
        "execute:source_item",
    }
    assert conn.args_by_table["execute:source_item"] == (
        "source_item-1",
        "source_record-2",
        "media_rights-4",
        "media_technical_metadata-6",
    )


async def test_mia_sprint3_compliance_blocked_record_has_zero_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        fixture_json("object_restricted_zero_inc_edu.json"),
        source_id="source-mia",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["writes"] == 0
    assert_no_writes(conn)


def test_mia_store_reuses_shared_media_adapter_write_path() -> None:
    source = inspect.getsource(mia_store.write_record)

    assert "write_normalized_record" in source
    assert "insert into" not in source.lower()


def test_mia_evidence_extension_is_adapter_owned() -> None:
    extension = mia_store._build_evidence_extension(
        {
            "mia_object_id": "278",
            "mia_rights_type": "Public Domain",
            "mia_rights_uri": "https://creativecommons.org/publicdomain/mark/1.0/",
        }
    )

    assert extension["mia_object_id"] == "278"
    assert extension["mia_rights_type"] == "Public Domain"
    assert extension["mia_rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"


def test_shared_store_remains_sa9_clean_for_mia() -> None:
    source = inspect.getsource(shared_store)

    assert "RIGHTS_EVIDENCE_REGISTRY" not in source
    assert "RightsEvidenceMapping" not in source
    assert "source_slug == \"mia\"" not in source
    assert "source_slug == 'mia'" not in source
    assert "mia_" not in source
