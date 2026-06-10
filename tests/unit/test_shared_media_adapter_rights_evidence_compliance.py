from workers.nara_adapter.store import _build_evidence_extension as nara_evidence_extension
from workers.shared_media_adapter.replay import assert_rights_evidence_contract
from workers.shared_media_adapter.store import StoreRuntime, build_rights_evidence


def _build_technical_metadata(normalized: dict, media_type_id: str) -> dict:
    return {"record_id": normalized.get("record_id"), "media_type_id": media_type_id}


def _validation_status(content: dict) -> str:
    return "valid"


def _runtime(source_slug: str, *, build_evidence_extension=None) -> StoreRuntime:
    kwargs = {}
    if build_evidence_extension is not None:
        kwargs["build_evidence_extension"] = build_evidence_extension
    return StoreRuntime(
        worker_id=f"{source_slug}:test",
        source_slug=source_slug,
        technical_schema_version="shared-technical-v1",
        validator_name="shared.validator",
        validator_version="v1",
        build_technical_metadata=_build_technical_metadata,
        validation_status=_validation_status,
        **kwargs,
    )


def _rights() -> dict:
    return {
        "decision": "ALLOWED",
        "allowed": True,
        "rights_statement_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "rights_status": "verified_cc0",
        "rights_basis": "cc0_statement",
    }


def test_common_evidence_fields_are_unchanged_for_default_extension() -> None:
    normalized = {"record_id": "record-1", "raw_payload_hash": "1" * 64}

    evidence = build_rights_evidence(
        runtime=_runtime("shared_source"),
        source_record_id="source-record-1",
        normalized=normalized,
        rights=_rights(),
    )

    assert_rights_evidence_contract(evidence, source="shared_source")
    assert set(evidence) == {
        "source",
        "schema_standard",
        "source_record_id",
        "edm_rights_uri",
        "rights_matrix_classification",
        "applying_policy",
        "oai_pmh_identifier",
        "rights_basis",
        "rights_statement_uri",
        "raw_payload_hash",
        "worker_classified_status",
        "evidence_status",
    }


def test_nara_extension_keys_are_present_even_when_normalized_values_are_missing() -> None:
    normalized = {"record_id": "record-1", "raw_payload_hash": "1" * 64}

    evidence = build_rights_evidence(
        runtime=_runtime("nara", build_evidence_extension=nara_evidence_extension),
        source_record_id="source-record-1",
        normalized=normalized,
        rights=_rights(),
    )

    assert_rights_evidence_contract(evidence, source="nara")
    for key in (
        "nara_naid",
        "nara_use_restriction",
        "nara_object_url",
        "nara_catalog_url",
        "nara_local_identifier",
    ):
        assert key in evidence
        assert evidence[key] is None
