import json

from workers.getty_adapter.store import _build_evidence_extension as getty_evidence_extension
from workers.shared_media_adapter.replay import ReplayConn, assert_m36_write_order
from workers.shared_media_adapter.store import StoreRuntime, write_normalized_record


def _build_technical_metadata(normalized: dict, media_type_id: str) -> dict:
    return {
        "record_id": normalized.get("record_id"),
        "representative_media_url": normalized.get("representative_media_url"),
        "content_hash": "2" * 64,
        "media_type_id": media_type_id,
    }


def _validation_status(content: dict) -> str:
    return "valid"


def _runtime(source_slug: str) -> StoreRuntime:
    return StoreRuntime(
        worker_id=f"{source_slug}:test",
        source_slug=source_slug,
        technical_schema_version="shared-technical-v1",
        validator_name="shared.validator",
        validator_version="v1",
        build_technical_metadata=_build_technical_metadata,
        validation_status=_validation_status,
        build_evidence_extension=getty_evidence_extension,
        rights_policy_id=f"{source_slug}_rights_matrix_v1",
        generated_at_time="2026-06-10T00:00:00+00:00",
    )


def _normalized() -> dict:
    return {
        "record_id": "getty-1",
        "title": "Getty Record",
        "source_url": "https://example.test/getty-1",
        "representative_media_url": "https://example.test/getty-1.jpg",
        "raw_payload_hash": "1" * 64,
        "rights_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "getty_object_id": "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb",
        "getty_rights_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "getty_manifest_uri": "https://media.getty.edu/iiif/manifest/1",
        "getty_image_service": "https://media.getty.edu/iiif/image/1",
        "getty_accession_number": "90.PA.20",
    }


async def test_extension_driven_rights_evidence_replay_through_m36_write_path() -> None:
    conn = ReplayConn()

    result = await write_normalized_record(
        conn,
        runtime=_runtime("getty"),
        raw_payload={"raw": "payload"},
        normalized=_normalized(),
        source_id="source-getty",
        media_type_id="image",
    )

    assert result["status"] == "written"
    assert result["writes"] == 7
    assert_m36_write_order(conn)

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["source"] == "getty"
    assert evidence["worker_classified_status"] == "classified_cc0"
    assert evidence["getty_object_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert evidence["getty_rights_uri"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert evidence["getty_manifest_uri"] == "https://media.getty.edu/iiif/manifest/1"
    assert evidence["getty_image_service"] == "https://media.getty.edu/iiif/image/1"
    assert evidence["getty_accession_number"] == "90.PA.20"
