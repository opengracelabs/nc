import json
from pathlib import Path

from workers.yale_adapter.normalize import build_rights_evidence, normalize_record
from workers.yale_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "yale"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_yale_sprint2_replay_rights_matrix_is_stable() -> None:
    ycba = fixture_json("ycba_object_cc0.json")
    yuag = fixture_json("yuag_object_noc_us.json")
    restricted = fixture_json("ycba_object_restricted.json")

    assert classify_rights(None)["rights_basis"] == "missing_object"
    assert classify_rights({"id": ycba["id"]})["rights_basis"] == "missing_subject_to"
    assert classify_rights(ycba)["rights_basis"] == "ycba_cc0"
    assert classify_rights(yuag)["rights_basis"] == "yuag_noc_us"
    assert classify_rights(restricted)["rights_basis"] == "unknown_rights_uri"


def test_yale_sprint2_replay_required_evidence_is_stable() -> None:
    record = fixture_json("ycba_object_cc0.json")
    manifest = fixture_json("manifest_ycba_12345_v3.json")

    left = build_rights_evidence(record, manifest=manifest)
    right = build_rights_evidence(record, manifest=manifest)

    assert left == right
    assert set(left) == {
        "ycba_subject_to_uri",
        "ycba_record_id",
        "ycba_object_id",
        "ycba_iiif_manifest",
        "ycba_attribution",
        "yale_object_id",
        "yale_rights_uri",
        "yale_collection",
        "yale_iiif_manifest",
        "yale_image_service",
    }


def test_yale_sprint2_replay_normalized_payload_is_stable_and_read_only() -> None:
    record = fixture_json("ycba_object_cc0.json")
    manifest = fixture_json("manifest_ycba_12345_v3.json")

    left = normalize_record(record, manifest=manifest)
    right = normalize_record(record, manifest=manifest)

    assert left == right
    assert left["rights_decision"] == "ALLOWED"
    assert left["representative_media_url"].endswith("/full/!1024,1024/0/default.jpg")
    assert "store" not in left

