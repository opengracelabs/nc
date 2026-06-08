from tests.unit.test_gallica_store import catalan_payload, fixture
from workers.gallica_adapter.store import write_record
from workers.shared_media_adapter.replay import M36_WRITE_ORDER, ReplayConn


async def test_gallica_sprint3_replay_is_deterministic_for_catalan_atlas() -> None:
    left_conn = ReplayConn()
    right_conn = ReplayConn()

    left = await write_record(
        left_conn,
        catalan_payload(),
        source_id="source-gallica",
        media_type_id="map",
    )
    right = await write_record(
        right_conn,
        catalan_payload(),
        source_id="source-gallica",
        media_type_id="map",
    )

    assert left["raw_payload_hash"] == right["raw_payload_hash"]
    assert left["technical_content_hash"] == right["technical_content_hash"]
    assert left_conn.sql_order == right_conn.sql_order == M36_WRITE_ORDER


async def test_gallica_sprint3_replay_rejects_restricted_rights_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        {"oai_record_xml": fixture("oairecord_restricted_rights.xml")},
        source_id="source-gallica",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["writes"] == 0
    assert conn.sql_order == []
