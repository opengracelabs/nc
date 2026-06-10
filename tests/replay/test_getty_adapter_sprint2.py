import json
from pathlib import Path

from workers.getty_adapter.client import CC0_URI
from workers.getty_adapter.normalize import build_rights_evidence, normalize_record
from workers.getty_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "getty"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_getty_sprint2_replay_rights_matrix_is_deterministic() -> None:
    cc0 = fixture_json("object_cc0.json")
    unknown = fixture_json("object_unknown_rights.json")
    missing_referred = fixture_json("object_missing_subject_to.json")
    missing_subject = fixture_json("object_missing_subject_to_in_referred_to_by.json")

    assert classify_rights(cc0)["rights_basis"] == "getty_cc0"
    assert classify_rights(cc0)["rights_statement_uri"] == CC0_URI
    assert classify_rights(unknown)["rights_basis"] == "unknown_rights_uri"
    assert classify_rights(missing_referred)["rights_basis"] == "missing_referred_to_by"
    assert classify_rights(missing_subject)["rights_basis"] == "missing_subject_to"


def test_getty_sprint2_replay_required_evidence_is_stable() -> None:
    evidence = build_rights_evidence(
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
    )

    assert evidence["getty_object_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert evidence["getty_rights_uri"] == CC0_URI
    assert evidence["getty_image_service"] == (
        "https://media.getty.edu/iiif/image/7ff0a543-569a-4cb0-b92b-cd78877d4141"
    )
    assert evidence["getty_manifest_uri"] == (
        "https://media.getty.edu/iiif/manifest/53be857e-41e8-4198-b45d-2e0f52d3051b"
    )
    assert evidence["getty_accession_number"] == "90.PA.20"


def test_getty_sprint2_replay_normalization_is_stable() -> None:
    left = normalize_record(
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
    )
    right = normalize_record(
        fixture_json("object_cc0.json"),
        manifest=fixture_json("manifest_irises_v2.json"),
    )

    assert left == right
    assert left["record_id"] == "c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb"
    assert left["rights_decision"] == "ALLOWED"
    assert left["getty_rights_policy_id"] == "getty_rights_matrix_v1"

