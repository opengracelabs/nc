from tests.unit.test_gallica_store import catalan_payload, fixture
from workers.gallica_adapter.config import settings
from workers.gallica_adapter.store import GALLICA_DEACTIVATION_REASON, write_record
from workers.shared_media_adapter.replay import ReplayConn, assert_no_writes


async def test_gallica_compliance_catalan_atlas_is_deactivated_before_m36_write_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        catalan_payload(),
        source_id="source-gallica",
        media_type_id="map",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == GALLICA_DEACTIVATION_REASON
    assert result["writes"] == 0
    assert_no_writes(conn)


def test_gallica_dry_run_remains_default_enabled() -> None:
    assert settings.gallica_dry_run is True


async def test_gallica_compliance_missing_rights_does_not_enter_m36_write_path() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        {"oai_record_xml": "<results><title>No rights</title></results>"},
        source_id="source-gallica",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == GALLICA_DEACTIVATION_REASON
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
    assert result["reason"] == GALLICA_DEACTIVATION_REASON
    assert result["writes"] == 0
    assert_no_writes(conn)
