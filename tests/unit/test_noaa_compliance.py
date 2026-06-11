from pathlib import Path

from workers.noaa_adapter import store as noaa_store
from workers.noaa_adapter.rights import classify_rights

NOAA_ADAPTER = Path(__file__).resolve().parents[2] / "workers" / "noaa_adapter"
SHARED_STORE = Path(__file__).resolve().parents[2] / "workers" / "shared_media_adapter" / "store.py"


def test_noaa_sprint3_review_required_final_decision_is_pilot_exclusion() -> None:
    assert noaa_store.REVIEW_REQUIRED_PILOT_EXCLUSION == "review_required_pilot_exclusion"


def test_noaa_sprint3_has_store_but_no_workflow_specific_adapter_path() -> None:
    source = (NOAA_ADAPTER / "store.py").read_text(encoding="utf-8")

    assert "write_normalized_record" in source
    assert "insert_workflow_item" not in source
    assert "workflow_items" not in source


def test_noaa_sprint3_does_not_edit_or_depend_on_shared_store_noaa_logic() -> None:
    source = SHARED_STORE.read_text(encoding="utf-8")

    assert "noaa" not in source.lower()


def test_noaa_sprint3_rights_gate_compliance_order_examples() -> None:
    assert classify_rights({"credit": "Jane Smith/NOAA"})["decision"] == "BLOCKED"
    assert classify_rights({"credit": "NASA/ESA"})["decision"] == "REVIEW_REQUIRED"
    assert classify_rights({"credit": "NOAA/NOS"})["decision"] == "ALLOWED"
    assert classify_rights({"license_id": "0", "credit": "NOAA"})["decision"] == "BLOCKED"

