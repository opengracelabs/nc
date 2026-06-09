import json
from pathlib import Path

from workers.shared_media_adapter.rights import RightsDecision
from workers.smk_adapter.normalize import normalize_record
from workers.smk_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "smk"


def load_record(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))["items"][0]


def load_payload(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_smk_sprint2_rights_replay_matrix() -> None:
    cases = {
        "object_kms1_public_domain.json": (RightsDecision.ALLOWED, "smk_public_domain"),
        "object_not_public_domain.json": (RightsDecision.BLOCKED, "not_public_domain"),
        "object_missing_public_domain.json": (
            RightsDecision.BLOCKED,
            "missing_rights_field",
        ),
        "object_public_domain_no_image.json": (RightsDecision.BLOCKED, "no_image_url"),
    }

    for fixture_name, (decision, basis) in cases.items():
        result = classify_rights(load_record(fixture_name))
        assert result["decision"] == decision
        assert result["rights_basis"] == basis


def test_smk_sprint2_normalization_replay_keeps_smk_fields() -> None:
    normalized = normalize_record(load_payload("object_kms1_public_domain.json"))

    assert normalized["record_id"] == "KMS1"
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["smk_public_domain"] is True
    assert normalized["smk_image_rights"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert normalized["smk_image_native"]
    assert normalized["smk_image_iiif_id"]
    assert normalized["smk_manifest_url"]

