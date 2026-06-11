import json
from pathlib import Path

from workers.noaa_adapter.client import (
    build_people_get_public_photos_params,
    extract_flickr_photos,
    extract_total,
    flickr_record_to_discovery_payload,
)
from workers.noaa_adapter.normalize import build_rights_evidence, normalize_flickr_search_payload
from workers.noaa_adapter.rights import classify_rights

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "noaa"
NOAA_ADAPTER = Path(__file__).resolve().parents[2] / "workers" / "noaa_adapter"
RETRIEVED_AT = "2026-06-11T00:00:00Z"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_noaa_sprint1_read_only_module_boundary() -> None:
    assert (NOAA_ADAPTER / "client.py").exists()
    assert (NOAA_ADAPTER / "rights.py").exists()
    assert (NOAA_ADAPTER / "normalize.py").exists()
    assert (NOAA_ADAPTER / "store.py").exists()


def test_noaa_sprint1_flickr_request_surface_is_deterministic() -> None:
    params = build_people_get_public_photos_params(
        api_key="fixture-key",
        user_id="usoceangov",
        page=1,
        per_page=3,
        tags="coral",
    )

    assert params["method"] == "flickr.people.getPublicPhotos"
    assert params["api_key"] == "fixture-key"
    assert params["tags"] == "coral"


def test_noaa_sprint1_mixed_fixture_replay_candidate_count_is_stable() -> None:
    payload = fixture_json("flickr_search_page_mixed.json")
    candidates = normalize_flickr_search_payload(payload, retrieved_at=RETRIEVED_AT)

    assert extract_total(payload) == 3
    assert [record["id"] for record in extract_flickr_photos(payload)] == ["1001", "1003", "1008"]
    assert len(candidates) == 1
    assert candidates[0]["record_id"] == "1001"
    assert candidates[0]["rights_decision"] == "ALLOWED"


def test_noaa_sprint1_required_evidence_is_stable() -> None:
    record = flickr_record_to_discovery_payload(fixture_json("flickr_photo_usgov_clean_noaa.json"))
    evidence = build_rights_evidence(record, retrieved_at=RETRIEVED_AT)

    assert evidence == {
        "source_system": "flickr",
        "source_record_id": "1001",
        "source_url": "https://www.flickr.com/photos/usoceangov/1001",
        "image_url": "https://live.staticflickr.com/1/1001_clean_o.jpg",
        "title": "Florida Keys coral reef",
        "description": (
            "Coral reef habitat in Florida Keys National Marine Sanctuary.\nCredit: NOAA/NOS"
        ),
        "creator": "NOAA/NOS",
        "credit": "NOAA/NOS",
        "owner_name": "NOAA's National Ocean Service",
        "license_id": "8",
        "license_label": "United States Government Work",
        "rights_statement_uri": "https://rightsstatements.org/vocab/NoC-US/1.0/",
        "rights_decision": "ALLOWED",
        "rights_basis": "flickr_us_government_work",
        "rights_policy_id": "noaa_rights_matrix_v1",
        "partner_markers": [],
        "contributor_markers": [],
        "blocked_markers": [],
        "raw_payload_hash": evidence["raw_payload_hash"],
        "retrieved_at": RETRIEVED_AT,
    }
    assert len(evidence["raw_payload_hash"]) == 64


def test_noaa_sprint1_no_store_writes_are_modeled() -> None:
    writes: list[dict] = []
    for source_record in extract_flickr_photos(fixture_json("flickr_search_page_mixed.json")):
        discovery_record = flickr_record_to_discovery_payload(source_record)
        rights = classify_rights(discovery_record)
        if rights["decision"] == "ALLOWED":
            writes.append(
                {
                    "would_write": False,
                    "source_record_id": discovery_record["source_record_id"],
                }
            )

    assert writes == [{"would_write": False, "source_record_id": "1001"}]

