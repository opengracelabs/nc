import json
from pathlib import Path

from workers.geonames_adapter.normalize import EVIDENCE_FIELDS, normalize_place_payload

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "geonames"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_geonames_normalizes_place_identity_evidence() -> None:
    evidence = normalize_place_payload(
        fixture_json("place_yellowstone.json"),
        hierarchy_payload=fixture_json("hierarchy_yellowstone.json"),
    )

    assert tuple(evidence) == EVIDENCE_FIELDS
    assert evidence["source"] == "geonames"
    assert evidence["source_role"] == "place_identity"
    assert evidence["geonames_id"] == "5843591"
    assert evidence["name"] == "Yellowstone National Park"
    assert evidence["coordinates"] == {"latitude": 44.42796, "longitude": -110.58846}
    assert evidence["feature_class"] == "L"
    assert evidence["feature_code"] == "PRKA"
    assert evidence["country_code"] == "US"
    assert evidence["admin1_code"] == "WY"
    assert evidence["admin2_code"] == "029"
    assert evidence["timezone"] == "America/Denver"
    assert evidence["source_url"] == "https://www.geonames.org/5843591"
    assert len(evidence["raw_payload_hash"]) == 64


def test_geonames_normalizes_alternate_names_and_hierarchy() -> None:
    evidence = normalize_place_payload(
        fixture_json("place_yellowstone.json"),
        hierarchy_payload=fixture_json("hierarchy_yellowstone.json"),
    )

    assert evidence["alternate_names"] == [
        {
            "name": "Yellowstone",
            "language": "en",
            "preferred": True,
            "short": False,
        },
        {
            "name": "Parque Nacional Yellowstone",
            "language": "es",
            "preferred": False,
            "short": False,
        },
    ]
    assert [item["geonames_id"] for item in evidence["hierarchy"]] == [
        "6295630",
        "6252001",
        "5843591",
    ]


def test_geonames_payload_hash_is_stable() -> None:
    place = fixture_json("place_yellowstone.json")
    hierarchy = fixture_json("hierarchy_yellowstone.json")

    left = normalize_place_payload(place, hierarchy_payload=hierarchy)
    right = normalize_place_payload(json.loads(json.dumps(place)), hierarchy_payload=hierarchy)

    assert left["raw_payload_hash"] == right["raw_payload_hash"]

