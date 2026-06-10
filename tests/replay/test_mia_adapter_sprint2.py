import json
from pathlib import Path

from workers.mia_adapter.normalize import build_rights_evidence, normalize_record, normalize_records
from workers.mia_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "mia"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_mia_sprint2_replay_rights_matrix_is_deterministic() -> None:
    public_domain = fixture_json("object_public_domain_valid_image.json")
    educational = fixture_json("object_restricted_zero_inc_edu.json")

    assert classify_rights(public_domain) == classify_rights(public_domain)
    assert classify_rights(educational) == classify_rights(educational)
    assert classify_rights(public_domain)["decision"] == "ALLOWED"
    assert classify_rights(educational)["decision"] == "BLOCKED"


def test_mia_sprint2_replay_mixed_search_candidate_counts_are_stable() -> None:
    candidates = normalize_records(fixture_json("search_mixed_rights_page.json"))

    assert len(candidates) == 1
    assert candidates[0]["mia_object_id"] == "278"
    assert candidates[0]["mia_rights_type"] == "Public Domain"


def test_mia_sprint2_replay_blocked_records_produce_zero_writes() -> None:
    writes: list[dict] = []
    for candidate in normalize_record(fixture_json("object_restricted_zero_inc_edu.json")):
        writes.append(candidate)

    assert writes == []


def test_mia_sprint2_replay_required_evidence_fields_are_stable_for_blocked_record() -> None:
    evidence = build_rights_evidence(fixture_json("object_restricted_zero_inc_edu.json"))

    assert evidence == {
        "mia_object_id": "1003",
        "mia_rights_type": "In Copyright–Educational Use",
        "mia_rights_uri": None,
        "mia_rights_image_display": "Full",
        "mia_image": "valid",
        "mia_public_access": 1,
        "mia_restricted": 0,
        "mia_primary_rendition_number": "mia_1003.jpg",
        "mia_cache_location": "001003\\000\\00\\1003",
        "mia_image_width": 1200,
        "mia_image_height": 900,
        "mia_accession_number": "1003.1",
        "mia_source_record_uri": "https://collections.artsmia.org/art/1003",
        "mia_image_url": "https://2.api.artsmia.org/800/1003.jpg",
        "mia_iiif_manifest_url": None,
    }
