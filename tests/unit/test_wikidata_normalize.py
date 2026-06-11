import json
from pathlib import Path

from workers.wikidata_adapter.normalize import (
    EVIDENCE_FIELDS,
    normalize_entity_payload,
    summarize_context,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "wikidata"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_wikidata_normalizes_required_evidence_fields() -> None:
    evidence = normalize_entity_payload(fixture_json("entity_yellowstone.json"), qid="Q351")

    assert tuple(evidence) == EVIDENCE_FIELDS
    assert evidence["wikidata_qid"] == "Q351"
    assert evidence["label"] == "Yellowstone National Park"
    assert evidence["description"] == "national park in the United States"
    assert evidence["aliases"] == ["Yellowstone", "Yellowstone Park"]
    assert evidence["instance_of"] == ["Q46169"]
    assert evidence["country"] == ["Q30"]
    assert evidence["coordinates"] == {"latitude": 44.6, "longitude": -110.5}
    assert evidence["geonames_id"] == "5844046"
    assert evidence["osm_relation"] == "1453307"
    assert evidence["wikipedia_links"] == {
        "en": "https://en.wikipedia.org/wiki/Yellowstone_National_Park",
        "fr": "https://fr.wikipedia.org/wiki/Parc_national_de_Yellowstone",
    }
    assert evidence["commons_category"] == "Yellowstone National Park"
    assert evidence["source_url"] == "https://www.wikidata.org/wiki/Q351"
    assert len(evidence["raw_payload_hash"]) == 64


def test_wikidata_payload_hash_is_stable() -> None:
    payload = fixture_json("entity_yellowstone.json")
    left = normalize_entity_payload(payload, qid="Q351")
    right = normalize_entity_payload(json.loads(json.dumps(payload)), qid="Q351")

    assert left["raw_payload_hash"] == right["raw_payload_hash"]


def test_wikidata_context_summary_is_context_only() -> None:
    evidence = normalize_entity_payload(fixture_json("entity_yellowstone.json"), qid="Q351")

    assert summarize_context(evidence) == {
        "source": "wikidata",
        "source_role": "context_only",
        "wikidata_qid": "Q351",
        "source_url": "https://www.wikidata.org/wiki/Q351",
    }

