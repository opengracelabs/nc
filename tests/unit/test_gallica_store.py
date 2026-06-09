from pathlib import Path

from workers.gallica_adapter.store import (
    GALLICA_DEACTIVATION_REASON,
    derive_anchor_type,
    write_record,
)
from workers.shared_media_adapter.replay import ReplayConn, assert_no_writes

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "gallica"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def catalan_payload() -> dict:
    return {
        "oai_record_xml": fixture("catalan_atlas_oairecord.xml"),
        "iiif_manifest_url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b55002481n/manifest.json",
        "iiif_info": {"width": 6200, "height": 4300},
        "pagination_pages": 6,
        "selected_page": 1,
    }


def test_derive_anchor_type_marks_maps_as_geographic() -> None:
    normalized = {
        "subject_terms": ["Portolan Atlas", "Map"],
        "edm_type": "map",
    }

    assert derive_anchor_type(normalized, "map") == "geographic"


async def test_write_record_rejects_gallica_ingestion_under_dd_gallica_003() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        catalan_payload(),
        source_id="source-gallica",
        media_type_id="map",
    )

    assert result == {
        "status": "rejected",
        "reason": GALLICA_DEACTIVATION_REASON,
        "record_id": None,
        "writes": 0,
    }
    assert_no_writes(conn)


async def test_write_record_rejects_restricted_gallica_rights_without_writes() -> None:
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
