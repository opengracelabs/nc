import json
from pathlib import Path

from workers.cma_adapter.normalize import normalize_record
from workers.cma_adapter.rights import classify_rights
from workers.shared_media_adapter.rights import RightsDecision

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "cma"


def load_record(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))["data"]


def load_payload(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_cma_sprint2_rights_replay_matrix() -> None:
    cases = {
        "artwork_94979_cc0.json": (
            RightsDecision.ALLOWED,
            "cma_share_license_status_cc0",
        ),
        "artwork_not_cc0.json": (RightsDecision.BLOCKED, "not_cc0"),
        "artwork_missing_share_license_status.json": (
            RightsDecision.BLOCKED,
            "missing_rights_field",
        ),
        "artwork_cc0_no_web_image.json": (RightsDecision.BLOCKED, "no_image_url"),
    }

    for fixture_name, (decision, basis) in cases.items():
        result = classify_rights(load_record(fixture_name))
        assert result["decision"] == decision
        assert result["rights_basis"] == basis


def test_cma_sprint2_normalization_replay_keeps_cma_fields() -> None:
    normalized = normalize_record(load_payload("artwork_94979_cc0.json"))

    assert normalized["record_id"] == "94979"
    assert normalized["rights_decision"] == RightsDecision.ALLOWED
    assert normalized["cma_share_license_status"] == "CC0"
    assert normalized["cma_image_print_url"]
    assert normalized["cma_image_web_url"]
    assert normalized["cma_image_full_url"]

