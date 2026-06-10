import json
from pathlib import Path

from workers.nara_adapter.normalize import build_rights_evidence, normalize_record
from workers.nara_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "nara"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_nara_sprint2_replay_rights_matrix_is_deterministic() -> None:
    unrestricted = fixture_json("record_unrestricted.json")
    restricted = fixture_json("record_restricted.json")
    missing = fixture_json("record_missing_use_restriction.json")

    assert classify_rights(unrestricted)["decision"] == "ALLOWED"
    assert classify_rights(restricted)["decision"] == "BLOCKED"
    assert classify_rights(missing)["decision"] == "BLOCKED"
    assert classify_rights(restricted) == classify_rights(restricted)


def test_nara_sprint2_replay_normalization_is_deterministic() -> None:
    record = fixture_json("record_unrestricted.json")

    left = normalize_record(record)
    right = normalize_record(record)

    assert left == right
    assert [item["record_id"] for item in left] == [
        "1667751:14721029",
        "1667751:14721030",
    ]
    assert left[0]["nara_naid"] == "1667751"
    assert left[0]["nara_use_restriction"] == "Unrestricted"
    assert left[0]["nara_catalog_url"] == "https://catalog.archives.gov/id/1667751"
    assert left[0]["nara_local_identifier"] == "00303"


def test_nara_sprint2_replay_required_evidence_fields_are_stable() -> None:
    record = fixture_json("record_unrestricted.json")
    normalized = normalize_record(record)

    evidence = build_rights_evidence(record, digital_object=None)

    assert set(evidence) == {
        "nara_naid",
        "nara_use_restriction",
        "nara_object_url",
        "nara_catalog_url",
        "nara_local_identifier",
    }
    assert normalized[0]["nara_object_url"].endswith("00303_2003_001_AC.jpg")
