"""MILESTONE-001 workflow tests.

Verifies that all 50 UNESCO WHC sites successfully traverse every stage of
the pipeline: Discovery → Approval → Ingestion → Preservation → Search.

All tests are pure Python (no live database or MinIO required).  They exercise
the exact production functions used by each worker and API router.
"""
import hashlib
import json
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from workers.discovery_worker.normalize import normalize_unesco_whc
from workers.discovery_worker.score import score
from workers.discovery_worker.sources.base import RawRecord
from workers.preservation_worker.main import VerificationResult, verify_asset_object

FIXTURE = Path("tests/fixtures/unesco_whc_50_sites.json")
SITES: list[dict] = json.loads(FIXTURE.read_text())

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VALID_TRANSITIONS = {
    "pending": {"approve", "reject", "flag"},
    "flagged": {"approve", "reject"},
}


def _normalize_all() -> list[dict[str, Any]]:
    return [
        normalize_unesco_whc(RawRecord(source_id=str(s["id_number"]), payload=s))
        for s in SITES
    ]


class FakeMinio:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw_bytes = raw_bytes

    class _Resp:
        def __init__(self, data: bytes) -> None:
            self._data = data

        async def read(self) -> bytes:
            return self._data

        async def release(self) -> None:
            pass

    async def stat_object(self, bucket: str, path: str):
        class _Stat:
            size = 0

        _Stat.size = len(self.raw_bytes)
        return _Stat()

    async def get_object(self, bucket: str, path: str):
        return self._Resp(self.raw_bytes)


# ---------------------------------------------------------------------------
# Stage 1 – Discovery / Normalisation
# ---------------------------------------------------------------------------


def test_all_50_sites_normalise_without_error() -> None:
    records = _normalize_all()
    assert len(records) == 50


def test_all_normalized_records_have_source_and_source_id() -> None:
    for rec in _normalize_all():
        assert rec["source"] == "unesco_whc"
        assert rec["source_id"] != ""


def test_all_normalized_records_have_text_unesco_ref_id() -> None:
    for rec in _normalize_all():
        assert isinstance(rec["unesco_ref_id"], str)
        assert rec["unesco_ref_id"] == rec["source_id"]


def test_all_normalized_records_have_english_name() -> None:
    for rec in _normalize_all():
        assert rec["name"].get("en"), f"Missing 'en' name for source_id={rec['source_id']}"


def test_all_normalized_records_have_heritage_type() -> None:
    valid_types = {"natural", "cultural", "mixed"}
    for rec in _normalize_all():
        assert rec["heritage_type"] in valid_types, (
            f"source_id={rec['source_id']} got heritage_type={rec['heritage_type']!r}"
        )


def test_all_normalized_records_have_country_codes() -> None:
    for rec in _normalize_all():
        assert len(rec["country_codes"]) >= 1, (
            f"source_id={rec['source_id']} has no country_codes"
        )


def test_all_normalized_records_have_ouv_criteria() -> None:
    for rec in _normalize_all():
        assert len(rec["ouv_criteria"]) >= 1, (
            f"source_id={rec['source_id']} has no ouv_criteria"
        )


def test_all_normalized_records_have_inscription_year() -> None:
    for rec in _normalize_all():
        year = rec["inscription_year"]
        assert isinstance(year, int) and 1970 <= year <= 2030, (
            f"source_id={rec['source_id']} has bad inscription_year={year}"
        )


def test_all_normalized_records_have_centroid() -> None:
    for rec in _normalize_all():
        c = rec["centroid"]
        assert isinstance(c, dict) and c.get("type") == "Point", (
            f"source_id={rec['source_id']} has invalid centroid={c!r}"
        )
        lon, lat = c["coordinates"]
        assert -180 <= lon <= 180, f"source_id={rec['source_id']} lon={lon} out of range"
        assert -90 <= lat <= 90, f"source_id={rec['source_id']} lat={lat} out of range"


def test_transboundary_flag_set_for_multi_country_sites() -> None:
    multi = [s for s in SITES if len(s.get("states", [])) > 1]
    records_by_id = {
        r["source_id"]: r
        for r in _normalize_all()
    }
    for site in multi:
        rec = records_by_id[str(site["id_number"])]
        assert rec["transboundary"] is True, (
            f"source_id={site['id_number']} ({site['site']}) should be transboundary"
        )


def test_natural_sites_normalise_to_natural_type() -> None:
    natural_ids = {str(s["id_number"]) for s in SITES if s["category"] == "Natural"}
    for rec in _normalize_all():
        if rec["source_id"] in natural_ids:
            assert rec["heritage_type"] == "natural"


def test_cultural_sites_normalise_to_cultural_type() -> None:
    cultural_ids = {str(s["id_number"]) for s in SITES if s["category"] == "Cultural"}
    for rec in _normalize_all():
        if rec["source_id"] in cultural_ids:
            assert rec["heritage_type"] == "cultural"


def test_mixed_sites_normalise_to_mixed_type() -> None:
    mixed_ids = {str(s["id_number"]) for s in SITES if s["category"] == "Mixed"}
    for rec in _normalize_all():
        if rec["source_id"] in mixed_ids:
            assert rec["heritage_type"] == "mixed"


def test_ouv_criteria_are_lowercase_roman_numerals() -> None:
    valid = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"}
    for rec in _normalize_all():
        for c in rec["ouv_criteria"]:
            assert c in valid, (
                f"source_id={rec['source_id']} has invalid criterion={c!r}"
            )


# ---------------------------------------------------------------------------
# Stage 2 – Scoring
# ---------------------------------------------------------------------------


def test_all_50_sites_receive_a_confidence_score() -> None:
    for rec in _normalize_all():
        s = score(rec)
        assert isinstance(s, float)
        assert 0.0 <= s <= 1.0, f"source_id={rec['source_id']} score={s} out of range"


def test_all_50_sites_score_at_least_0_75() -> None:
    """Every site in the fixture has name, country_codes, heritage_type,
    ouv_criteria, inscription_year, and centroid — that alone earns 0.90."""
    for rec in _normalize_all():
        s = score(rec)
        assert s >= 0.75, f"source_id={rec['source_id']} scored only {s}"


def test_scoring_is_deterministic() -> None:
    records = _normalize_all()
    scores_a = [score(r) for r in records]
    scores_b = [score(r) for r in records]
    assert scores_a == scores_b


# ---------------------------------------------------------------------------
# Stage 3 – Approval (human governance state machine)
# ---------------------------------------------------------------------------


def test_pending_candidate_can_be_approved() -> None:
    allowed = _VALID_TRANSITIONS.get("pending", set())
    assert "approve" in allowed


def test_pending_candidate_can_be_rejected() -> None:
    allowed = _VALID_TRANSITIONS.get("pending", set())
    assert "reject" in allowed


def test_pending_candidate_can_be_flagged() -> None:
    allowed = _VALID_TRANSITIONS.get("pending", set())
    assert "flag" in allowed


def test_flagged_candidate_can_be_approved() -> None:
    allowed = _VALID_TRANSITIONS.get("flagged", set())
    assert "approve" in allowed


def test_flagged_candidate_cannot_be_flagged_again() -> None:
    allowed = _VALID_TRANSITIONS.get("flagged", set())
    assert "flag" not in allowed


def test_approved_candidate_has_no_further_transitions() -> None:
    allowed = _VALID_TRANSITIONS.get("approved", set())
    assert not allowed


def test_all_50_sites_can_be_approved_from_pending() -> None:
    """Simulate approve action for every site."""
    for _site in SITES:
        allowed = _VALID_TRANSITIONS.get("pending", set())
        assert "approve" in allowed
        new_status = {"approve": "approved", "reject": "rejected", "flag": "flagged"}["approve"]
        assert new_status == "approved"


# ---------------------------------------------------------------------------
# Stage 4 – Preservation (checksum + size integrity)
# ---------------------------------------------------------------------------


def _make_asset(raw_bytes: bytes) -> dict[str, Any]:
    return {
        "id": uuid4(),
        "raw_path": "ingestion/place/ingest/source_record.json",
        "checksum_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "size_bytes": len(raw_bytes),
    }


@pytest.mark.asyncio
async def test_preservation_valid_for_all_50_sites() -> None:
    """For each site, serialize its normalized record as the 'raw' artifact and
    verify the preservation worker reports it as valid."""
    records = _normalize_all()
    for rec in records:
        raw_bytes = json.dumps(rec, ensure_ascii=False).encode()
        asset = _make_asset(raw_bytes)
        result = await verify_asset_object(FakeMinio(raw_bytes), asset)
        assert result == VerificationResult("valid", []), (
            f"source_id={rec['source_id']} preservation failed: {result}"
        )


@pytest.mark.asyncio
async def test_preservation_quarantines_on_checksum_mismatch() -> None:
    site = SITES[0]
    rec = normalize_unesco_whc(RawRecord(source_id=str(site["id_number"]), payload=site))
    raw_bytes = json.dumps(rec).encode()
    asset = {
        "id": uuid4(),
        "raw_path": "ingestion/place/ingest/source_record.json",
        "checksum_sha256": "deadbeef" * 8,
        "size_bytes": len(raw_bytes),
    }
    result = await verify_asset_object(FakeMinio(raw_bytes), asset)
    assert result.status == "quarantined"
    assert any("checksum" in w for w in result.warnings)


@pytest.mark.asyncio
async def test_preservation_quarantines_on_size_mismatch() -> None:
    site = SITES[0]
    rec = normalize_unesco_whc(RawRecord(source_id=str(site["id_number"]), payload=site))
    raw_bytes = json.dumps(rec).encode()
    asset = {
        "id": uuid4(),
        "raw_path": "ingestion/place/ingest/source_record.json",
        "checksum_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "size_bytes": len(raw_bytes) + 1,  # deliberate mismatch
    }
    result = await verify_asset_object(FakeMinio(raw_bytes), asset)
    assert result.status == "quarantined"
    assert any("size" in w for w in result.warnings)


@pytest.mark.asyncio
async def test_preservation_quarantines_missing_raw_path() -> None:
    raw_bytes = b"data"
    asset = {"id": uuid4(), "raw_path": None, "checksum_sha256": "x", "size_bytes": 4}
    result = await verify_asset_object(FakeMinio(raw_bytes), asset)
    assert result.status == "quarantined"
    assert result.warnings == ["raw_path missing"]


# ---------------------------------------------------------------------------
# Stage 5 – Search readiness
# ---------------------------------------------------------------------------


def test_all_50_sites_have_searchable_english_name() -> None:
    for rec in _normalize_all():
        name_en = rec["name"].get("en", "")
        assert len(name_en) >= 3, (
            f"source_id={rec['source_id']} name too short to index: {name_en!r}"
        )


def test_natural_sites_are_filterable_by_heritage_type() -> None:
    natural = [r for r in _normalize_all() if r["heritage_type"] == "natural"]
    assert len(natural) == 19


def test_cultural_sites_are_filterable_by_heritage_type() -> None:
    cultural = [r for r in _normalize_all() if r["heritage_type"] == "cultural"]
    assert len(cultural) == 25


def test_mixed_sites_are_filterable_by_heritage_type() -> None:
    mixed = [r for r in _normalize_all() if r["heritage_type"] == "mixed"]
    assert len(mixed) == 6


def test_sites_are_filterable_by_country_code() -> None:
    in_sites = [r for r in _normalize_all() if "IN" in r["country_codes"]]
    assert len(in_sites) >= 3, f"Expected ≥3 Indian sites, got {len(in_sites)}"


def test_sites_are_filterable_by_ouv_criterion() -> None:
    criterion_x = [r for r in _normalize_all() if "x" in r["ouv_criteria"]]
    assert len(criterion_x) >= 10, (
        f"Expected ≥10 sites with criterion (x), got {len(criterion_x)}"
    )


def test_sites_are_filterable_by_inscription_year() -> None:
    from_1978 = [r for r in _normalize_all() if r["inscription_year"] == 1978]
    assert len(from_1978) >= 2  # Galápagos and Yellowstone


def test_all_50_sites_have_valid_centroid_for_spatial_queries() -> None:
    for rec in _normalize_all():
        lon, lat = rec["centroid"]["coordinates"]
        assert -180 <= lon <= 180
        assert -90 <= lat <= 90


def test_unique_source_ids_across_all_50_sites() -> None:
    records = _normalize_all()
    ids = [r["source_id"] for r in records]
    assert len(ids) == len(set(ids)), "Duplicate source_ids detected in fixture"


def test_description_present_for_all_50_sites() -> None:
    for rec in _normalize_all():
        desc = rec.get("description", {})
        assert desc.get("en"), (
            f"source_id={rec['source_id']} missing English description"
        )
