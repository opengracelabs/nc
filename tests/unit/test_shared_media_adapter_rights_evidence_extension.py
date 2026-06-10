import inspect

from workers.aic_adapter.store import _build_evidence_extension as aic_evidence_extension
from workers.getty_adapter.store import _build_evidence_extension as getty_evidence_extension
from workers.nara_adapter.store import _build_evidence_extension as nara_evidence_extension
from workers.shared_media_adapter.store import StoreRuntime, build_rights_evidence


def _build_technical_metadata(normalized: dict, media_type_id: str) -> dict:
    return {"record_id": normalized.get("record_id"), "media_type_id": media_type_id}


def _validation_status(content: dict) -> str:
    return "valid" if content.get("record_id") else "invalid"


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


def _rights(status: str = "verified_cc0") -> dict:
    return {
        "decision": "ALLOWED",
        "allowed": True,
        "rights_statement_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "rights_status": status,
        "rights_basis": "cc0_statement",
    }


def _normalized() -> dict:
    return {
        "record_id": "record-1",
        "raw_payload_hash": "1" * 64,
        "aic_is_public_domain": True,
        "aic_copyright_notice": None,
        "aic_manifest_url": "https://example.test/aic/manifest",
        "getty_object_id": "getty-1",
        "getty_rights_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "getty_manifest_uri": "https://example.test/getty/manifest",
        "getty_image_service": "https://example.test/getty/service",
        "getty_accession_number": "90.PA.20",
        "nara_naid": "1667751",
        "nara_use_restriction": "Unrestricted",
        "nara_object_url": "https://catalog.archives.gov/object.jpg",
        "nara_catalog_url": "https://catalog.archives.gov/id/1667751",
        "nara_local_identifier": "00303",
    }


def test_build_rights_evidence_uses_runtime_extension_not_registry_or_branching() -> None:
    source = inspect.getsource(build_rights_evidence)

    assert "build_evidence_extension" in source
    assert "RIGHTS_EVIDENCE_REGISTRY" not in source
    assert "RightsEvidenceMapping" not in source
    assert "if runtime.source_slug ==" not in source
    assert "elif runtime.source_slug" not in source


def test_store_runtime_rejects_non_callable_evidence_extension() -> None:
    try:
        _runtime("bad_source", build_evidence_extension={})
    except ValueError as exc:
        assert str(exc) == "build_evidence_extension_not_callable"
    else:
        raise AssertionError("non-callable evidence extension was accepted")


def test_status_remap_is_unconditional_for_all_sources() -> None:
    evidence = build_rights_evidence(
        runtime=_runtime("new_future_source"),
        source_record_id="source-record-1",
        normalized=_normalized(),
        rights=_rights("verified_pd"),
    )

    assert evidence["worker_classified_status"] == "classified_pd"


def test_default_evidence_extension_returns_no_source_specific_fields() -> None:
    evidence = build_rights_evidence(
        runtime=_runtime("shared_source"),
        source_record_id="source-record-1",
        normalized=_normalized(),
        rights=_rights(),
    )

    assert evidence["worker_classified_status"] == "classified_cc0"
    assert "aic_is_public_domain" not in evidence
    assert "getty_object_id" not in evidence


def test_adapter_owned_extensions_supply_source_specific_evidence() -> None:
    normalized = _normalized()

    aic = build_rights_evidence(
        runtime=_runtime("aic", build_evidence_extension=aic_evidence_extension),
        source_record_id="source-record-1",
        normalized=normalized,
        rights=_rights(),
    )
    getty = build_rights_evidence(
        runtime=_runtime("getty", build_evidence_extension=getty_evidence_extension),
        source_record_id="source-record-1",
        normalized=normalized,
        rights=_rights(),
    )
    nara = build_rights_evidence(
        runtime=_runtime("nara", build_evidence_extension=nara_evidence_extension),
        source_record_id="source-record-1",
        normalized=normalized,
        rights=_rights(),
    )

    assert aic["aic_is_public_domain"] is True
    assert aic["aic_manifest_url"] == "https://example.test/aic/manifest"
    assert getty["getty_object_id"] == "getty-1"
    assert getty["getty_accession_number"] == "90.PA.20"
    assert nara["nara_naid"] == "1667751"
    assert nara["nara_use_restriction"] == "Unrestricted"
    assert nara["nara_object_url"] == "https://catalog.archives.gov/object.jpg"
    assert nara["nara_catalog_url"] == "https://catalog.archives.gov/id/1667751"
    assert nara["nara_local_identifier"] == "00303"
