import json
from pathlib import Path

from workers.gallica_adapter.store import derive_anchor_type, write_record
from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_no_writes,
)

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


async def test_write_record_uses_shared_m36_write_path_for_catalan_atlas() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        catalan_payload(),
        source_id="source-gallica",
        media_type_id="map",
    )

    assert result["status"] == "written"
    assert result["record_id"] == "ark:/12148/btv1b55002481n"
    assert result["writes"] == 7
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    assert conn.args_by_table["source_item"][5] == "geographic"
    assert conn.args_by_table["source_record"][3] == "gallica_api_profile_v1"
    assert conn.args_by_table["media_file"][3] == (
        "https://gallica.bnf.fr/iiif/ark:/12148/btv1b55002481n/f1/full/full/0/native.jpg"
    )

    normalized_payload = json.loads(conn.args_by_table["source_record"][6])
    assert normalized_payload["pagination_pages"] == 6
    assert normalized_payload["iiif_image_service_url"] == (
        "https://gallica.bnf.fr/iiif/ark:/12148/btv1b55002481n/f1"
    )


async def test_write_record_rejects_restricted_gallica_rights_without_writes() -> None:
    conn = ReplayConn()

    result = await write_record(
        conn,
        {"oai_record_xml": fixture("oairecord_restricted_rights.xml")},
        source_id="source-gallica",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == "missing_rights_uri"
    assert result["writes"] == 0
    assert_no_writes(conn)

