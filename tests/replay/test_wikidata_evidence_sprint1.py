import json
from pathlib import Path

from workers.wikidata_adapter.normalize import normalize_entity_payload
from workers.wikidata_adapter.rights import evidence_rights

WIKIDATA_ADAPTER = Path(__file__).resolve().parents[2] / "workers" / "wikidata_adapter"
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "wikidata"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_wikidata_sprint1_file_boundary_is_identity_evidence_only() -> None:
    assert (WIKIDATA_ADAPTER / "__init__.py").exists()
    assert (WIKIDATA_ADAPTER / "config.py").exists()
    assert (WIKIDATA_ADAPTER / "client.py").exists()
    assert (WIKIDATA_ADAPTER / "entity.py").exists()
    assert (WIKIDATA_ADAPTER / "normalize.py").exists()
    assert (WIKIDATA_ADAPTER / "rights.py").exists()
    assert not (WIKIDATA_ADAPTER / "store.py").exists()
    assert not (WIKIDATA_ADAPTER / "media.py").exists()


def test_wikidata_sprint1_no_content_pipeline_terms() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in WIKIDATA_ADAPTER.glob("*.py"))

    assert "write_normalized_record" not in combined
    assert "source_item" not in combined
    assert "workflow_item" not in combined
    assert "M36" not in combined
    assert "media_file" not in combined


def test_wikidata_sprint1_identity_replay_is_stable() -> None:
    evidence = normalize_entity_payload(fixture_json("entity_yellowstone.json"), qid="Q351")

    assert evidence["wikidata_qid"] == "Q351"
    assert evidence["geonames_id"] == "5844046"
    assert evidence["source_url"] == "https://www.wikidata.org/wiki/Q351"
    assert evidence["raw_payload_hash"] == normalize_entity_payload(
        fixture_json("entity_yellowstone.json"),
        qid="Q351",
    )["raw_payload_hash"]


def test_wikidata_sprint1_rights_are_cc0_evidence_only() -> None:
    rights = evidence_rights()

    assert rights["decision"] == "ALLOWED"
    assert rights["rights_status"] == "evidence_allowed"
    assert rights["rights_basis"] == "cc0_structured_data"
    assert rights["commercial_media_allowed"] is False

