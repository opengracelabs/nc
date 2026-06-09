from tests.unit.test_gallica_store import catalan_payload, fixture
from workers.gallica_adapter.store import GALLICA_DEACTIVATION_REASON, write_record
from workers.shared_media_adapter.replay import ReplayConn, assert_no_writes


async def test_gallica_sprint3_replay_rejects_catalan_atlas_after_deactivation() -> None:
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

    assert left == right == {
        "status": "rejected",
        "reason": GALLICA_DEACTIVATION_REASON,
        "record_id": None,
        "writes": 0,
    }
    assert_no_writes(left_conn)
    assert_no_writes(right_conn)


async def test_gallica_sprint3_replay_rejects_restricted_rights_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        {"oai_record_xml": fixture("oairecord_restricted_rights.xml")},
        source_id="source-gallica",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == GALLICA_DEACTIVATION_REASON
    assert result["writes"] == 0
    assert_no_writes(conn)
