from pathlib import Path

from workers.met_adapter.normalize import normalize_record
from workers.shared_media_adapter.rights import CC0_URI, RightsDecision

FIXTURES = Path("tests/fixtures/met")


def load_json(name: str) -> dict:
    import json

    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_met_sprint2_replay_is_deterministic_for_same_object_payload() -> None:
    payload = load_json("object_hokusai_public_domain.json")

    left = normalize_record(payload)
    right = normalize_record(dict(reversed(list(payload.items()))))

    assert left["raw_payload_hash"] == right["raw_payload_hash"]
    assert left["record_id"] == right["record_id"] == "45434"
    assert left["rights_uri"] == right["rights_uri"] == CC0_URI
    assert left["rights_decision"] == right["rights_decision"] == RightsDecision.ALLOWED
    assert left["primary_image"] == right["primary_image"]
    assert left["additional_images"] == right["additional_images"]


def test_met_sprint2_replay_blocks_non_public_domain_without_store_write_path() -> None:
    normalized = normalize_record(load_json("object_not_public_domain.json"))

    assert normalized["record_id"] == "90001"
    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["met_rights_basis"] == "not_public_domain"


def test_met_sprint2_replay_blocks_missing_rights_without_store_write_path() -> None:
    normalized = normalize_record(load_json("object_missing_rights_field.json"))

    assert normalized["record_id"] == "90002"
    assert normalized["rights_decision"] == RightsDecision.BLOCKED
    assert normalized["rights_allowed"] is False
    assert normalized["met_rights_basis"] == "missing_rights_field"
