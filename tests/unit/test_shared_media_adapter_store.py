import json

from workers.shared_media_adapter.replay import (
    M36_WRITE_ORDER,
    ReplayConn,
    assert_m36_write_order,
    assert_rights_evidence_contract,
)
from workers.shared_media_adapter.store import (
    StoreRuntime,
    build_rights_evidence,
    write_normalized_record,
)


def _normalized() -> dict:
    return {
        "record_id": "shared/1",
        "title": "Shared Asset",
        "description": "A normalized media record.",
        "date": "1890",
        "creator": "Creator",
        "subject_terms": ["Maps"],
        "rights_uri": "https://creativecommons.org/publicdomain/mark/1.0/",
        "provider": "Provider",
        "dataProvider": "Data Provider",
        "edm_type": "IMAGE",
        "source_url": "https://example.test/shared/1",
        "representative_media_url": "https://example.test/shared/1.jpg",
        "preview_urls": [],
        "width_px": 1200,
        "height_px": 900,
        "raw_payload_hash": "1" * 64,
        "rights_decision": "ALLOWED",
        "rights_allowed": True,
    }


def _build_technical_metadata(normalized: dict, media_type_id: str) -> dict:
    content = {
        "record_id": normalized.get("record_id"),
        "title": normalized.get("title"),
        "source_url": normalized.get("source_url"),
        "representative_media_url": normalized.get("representative_media_url"),
        "content_hash": "2" * 64,
        "media_type_id": media_type_id,
    }
    return content


def _validation_status(content: dict) -> str:
    if not content.get("record_id"):
        return "invalid"
    if not content.get("representative_media_url") and not content.get("source_url"):
        return "invalid"
    return "valid"


def _runtime(*, anchor_type: str = "cultural") -> StoreRuntime:
    return StoreRuntime(
        worker_id="shared_adapter:test",
        source_slug="shared_source",
        technical_schema_version="shared-technical-v1",
        validator_name="shared.validator",
        validator_version="v1",
        build_technical_metadata=_build_technical_metadata,
        validation_status=_validation_status,
        workflow_record_id_key="shared_record_id",
        anchor_type=anchor_type,
        generated_at_time="2026-06-07T00:00:00+00:00",
    )


async def test_write_normalized_record_preserves_m36_write_order_and_statuses() -> None:
    conn = ReplayConn()

    result = await write_normalized_record(
        conn,
        runtime=_runtime(),
        raw_payload={"raw": "payload"},
        normalized=_normalized(),
        source_id="shared-source",
        media_type_id="image",
    )

    assert result == {
        "status": "written",
        "record_id": "shared/1",
        "source_item_id": "source_item-1",
        "source_record_id": "source_record-2",
        "media_file_id": "media_file-3",
        "media_rights_id": "media_rights-4",
        "technical_metadata_id": "media_technical_metadata-6",
        "workflow_item_id": None,
        "raw_payload_hash": "1" * 64,
        "technical_content_hash": "2" * 64,
        "writes": 7,
    }
    assert conn.sql_order == M36_WRITE_ORDER
    assert_m36_write_order(conn)
    media_rights_args = conn.args_by_table["media_rights"]
    evidence = json.loads(media_rights_args[2])
    assert media_rights_args[1] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert evidence["evidence_status"] == "pending_human_review"
    assert evidence["worker_classified_status"] == "verified_pd"
    assert evidence["rights_matrix_classification"] == "allowed"


async def test_write_normalized_record_routes_missing_rights_to_review_workflow() -> None:
    conn = ReplayConn()
    normalized = {**_normalized(), "rights_uri": None}

    result = await write_normalized_record(
        conn,
        runtime=_runtime(),
        raw_payload={"raw": "payload"},
        normalized=normalized,
        source_id="shared-source",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "missing_rights_uri",
        "record_id": "shared/1",
        "writes": 0,
    }
    assert conn.sql_order == []


def test_build_rights_evidence_contains_shared_contract_fields() -> None:
    rights = {
        "decision": "ALLOWED",
        "allowed": True,
        "rights_statement_uri": "https://creativecommons.org/publicdomain/mark/1.0/",
        "rights_status": "verified_pd",
        "rights_basis": "public_domain_mark",
    }

    evidence = build_rights_evidence(
        runtime=_runtime(),
        source_record_id="source-record-1",
        normalized=_normalized(),
        rights=rights,
    )

    assert evidence["source"] == "shared_source"
    assert evidence["source_record_id"] == "source-record-1"
    assert evidence["edm_rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert evidence["rights_matrix_classification"] == "allowed"
    assert evidence["applying_policy"] == "europeana_rights_matrix_v1.0"
    assert evidence["oai_pmh_identifier"] == "shared/1"
    assert evidence["evidence_status"] == "pending_human_review"


def test_store_runtime_defaults_anchor_type_to_cultural() -> None:
    assert _runtime().anchor_type == "cultural"


def test_store_runtime_rejects_invalid_freeze_configuration() -> None:
    try:
        StoreRuntime(
            worker_id="shared_adapter:test",
            source_slug="shared_source",
            technical_schema_version="shared-technical-v1",
            validator_name="shared.validator",
            validator_version="v1",
            build_technical_metadata=_build_technical_metadata,
            validation_status=_validation_status,
            anchor_type="invalid",
        )
    except ValueError as exc:
        assert str(exc) == "invalid_anchor_type:invalid"
    else:
        raise AssertionError("invalid anchor type was accepted")


async def test_write_normalized_record_uses_runtime_schema_standard_and_replay_time() -> None:
    conn = ReplayConn()
    runtime = StoreRuntime(
        worker_id="shared_adapter:test",
        source_slug="shared_source",
        technical_schema_version="shared-technical-v1",
        validator_name="shared.validator",
        validator_version="v1",
        build_technical_metadata=_build_technical_metadata,
        validation_status=_validation_status,
        schema_standard="custom_edm",
        anchor_type="cultural",
        generated_at_time="2026-06-07T00:00:00+00:00",
    )

    await write_normalized_record(
        conn,
        runtime=runtime,
        raw_payload={"raw": "payload"},
        normalized=_normalized(),
        source_id="shared-source",
        media_type_id="image",
    )

    source_record_args = conn.args_by_table["source_record"]
    source_item_args = conn.args_by_table["source_item"]
    assert source_record_args[3] == "custom_edm"
    assert source_item_args[5] == "cultural"
    provenance = json.loads(source_item_args[6])
    assert provenance["prov:generatedAtTime"] == "2026-06-07T00:00:00+00:00"


def test_replay_rights_evidence_contract_assertion() -> None:
    rights = {
        "decision": "ALLOWED",
        "allowed": True,
        "rights_statement_uri": "https://creativecommons.org/publicdomain/mark/1.0/",
        "rights_status": "verified_pd",
        "rights_basis": "public_domain_mark",
    }
    evidence = build_rights_evidence(
        runtime=_runtime(),
        source_record_id="source-record-1",
        normalized=_normalized(),
        rights=rights,
    )

    assert_rights_evidence_contract(evidence, source="shared_source")
