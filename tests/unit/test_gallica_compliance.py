import json

from tests.unit.test_gallica_store import catalan_payload, fixture
from workers.gallica_adapter.store import write_record
from workers.shared_media_adapter.replay import ReplayConn, assert_no_writes


async def test_gallica_compliance_catalan_atlas_writes_required_m36_tables() -> None:
    conn = ReplayConn()

    await write_record(
        conn,
        catalan_payload(),
        source_id="source-gallica",
        media_type_id="map",
    )

    assert {
        "source_item",
        "source_record",
        "media_file",
        "media_rights",
        "media_technical_metadata",
        "preservation_event",
    }.issubset(set(conn.sql_order))

    technical = json.loads(conn.args_by_table["media_technical_metadata"][3])
    assert technical["record_id"] == "ark:/12148/btv1b55002481n"
    assert technical["quality_flag"] == "meets_minimum"


async def test_gallica_compliance_missing_rights_does_not_enter_m36_write_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        {"oai_record_xml": "<results><title>No rights</title></results>"},
        source_id="source-gallica",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["writes"] == 0
    assert_no_writes(conn)


async def test_gallica_compliance_blocked_uri_does_not_enter_m36_write_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        {
            "oai_record_xml": fixture("oairecord_dc_rights_uri.xml"),
            "iiif_manifest": {"license": "https://creativecommons.org/licenses/by/4.0/"},
        },
        source_id="source-gallica",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == "blocked_rights_statement"
    assert result["writes"] == 0
    assert_no_writes(conn)

