import json
from pathlib import Path

from workers.geonames_adapter.normalize import normalize_place_payload
from workers.geonames_adapter.rights import evidence_rights

GEONAMES_ADAPTER = Path(__file__).resolve().parents[2] / "workers" / "geonames_adapter"
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "geonames"


def fixture_json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_geonames_sprint1_file_boundary_is_place_identity_only() -> None:
    assert (GEONAMES_ADAPTER / "__init__.py").exists()
    assert (GEONAMES_ADAPTER / "config.py").exists()
    assert (GEONAMES_ADAPTER / "client.py").exists()
    assert (GEONAMES_ADAPTER / "place.py").exists()
    assert (GEONAMES_ADAPTER / "normalize.py").exists()
    assert (GEONAMES_ADAPTER / "rights.py").exists()
    assert not (GEONAMES_ADAPTER / "store.py").exists()
    assert not (GEONAMES_ADAPTER / "media.py").exists()


def test_geonames_sprint1_no_content_pipeline_terms() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in GEONAMES_ADAPTER.glob("*.py"))

    assert "write_normalized_record" not in combined
    assert "source_item" not in combined
    assert "workflow_item" not in combined
    assert "M36" not in combined
    assert "media_file" not in combined


def test_geonames_sprint1_identity_replay_is_stable() -> None:
    evidence = normalize_place_payload(
        fixture_json("place_yellowstone.json"),
        hierarchy_payload=fixture_json("hierarchy_yellowstone.json"),
    )

    assert evidence["geonames_id"] == "5843591"
    assert evidence["feature_code"] == "PRKA"
    assert evidence["country_code"] == "US"
    assert evidence["admin1_code"] == "WY"
    assert evidence["source_url"] == "https://www.geonames.org/5843591"
    assert evidence["raw_payload_hash"] == normalize_place_payload(
        fixture_json("place_yellowstone.json"),
        hierarchy_payload=fixture_json("hierarchy_yellowstone.json"),
    )["raw_payload_hash"]


def test_geonames_sprint1_rights_are_attribution_required_evidence() -> None:
    rights = evidence_rights()

    assert rights["decision"] == "ALLOWED"
    assert rights["rights_status"] == "evidence_allowed"
    assert rights["rights_basis"] == "cc_by_4_attribution_required"
    assert rights["attribution_required"] is True
    assert rights["commercial_media_allowed"] is False

