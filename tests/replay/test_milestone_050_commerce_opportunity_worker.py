"""v0.5.0 Commerce Opportunity Worker replay tests."""
from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from workers.commerce_opportunity_worker import WORKER_VERSION
from workers.commerce_opportunity_worker.score import compute_scores, replay_score
from workers.commerce_opportunity_worker.store import build_input_snapshot, claim_approved_opportunities, write_score_and_opportunity
from workers.commerce_replay_worker.replay import verify_audit_entry

_POLICY_ID = UUID("30000000-0000-0000-0000-000000000001")
_OPPORTUNITY_ID = UUID("30000000-0000-0000-0000-000000000002")


def _policy() -> dict:
    formula_spec = {
        "version": "1.0.0",
        "scorer_version": "weighted_sum_v1",
        "subscores": {
            "museum_score": {"inputs": [
                {"signal": "illustrator_prestige", "weight": 0.35},
                {"signal": "rights_confidence", "weight": 0.25},
                {"signal": "golden_age_factor", "weight": 0.20},
                {"signal": "institutional_credit", "weight": 0.10},
                {"signal": "provenance_completeness", "weight": 0.10},
            ]},
            "retail_score": {"inputs": [
                {"signal": "image_quality_score", "weight": 0.30},
                {"signal": "taxon_commercial_tier_score", "weight": 0.25},
                {"signal": "resolution_tier_score", "weight": 0.20},
                {"signal": "composition_fit", "weight": 0.15},
                {"signal": "color_score", "weight": 0.10},
            ]},
            "publishing_score": {"inputs": [
                {"signal": "identification_confidence", "weight": 0.30},
                {"signal": "image_quality_score", "weight": 0.25},
                {"signal": "golden_age_factor", "weight": 0.20},
                {"signal": "taxon_commercial_tier_score", "weight": 0.15},
                {"signal": "rights_confidence", "weight": 0.10},
            ]},
            "tourism_score": {"inputs": [
                {"signal": "place_relevance_score", "weight": 0.35},
                {"signal": "taxon_place_iconic", "weight": 0.25},
                {"signal": "place_tier_score", "weight": 0.20},
                {"signal": "image_quality_score", "weight": 0.20},
            ]},
            "reference_score": {"inputs": [
                {"signal": "identification_confidence", "weight": 0.35},
                {"signal": "taxon_commercial_tier_score", "weight": 0.20},
                {"signal": "golden_age_factor", "weight": 0.20},
                {"signal": "image_quality_score", "weight": 0.15},
                {"signal": "provenance_completeness", "weight": 0.10},
            ]},
        },
        "composite": {"inputs": [
            {"signal": "retail_score", "weight": 0.30},
            {"signal": "tourism_score", "weight": 0.25},
            {"signal": "museum_score", "weight": 0.20},
            {"signal": "publishing_score", "weight": 0.15},
            {"signal": "reference_score", "weight": 0.10},
        ]},
        "signal_defaults": {
            "image_quality_score": None,
            "composition_fit": None,
            "identification_confidence": 0.0,
            "taxon_place_iconic": 0.0,
            "color_profile": "unknown",
            "color_score": 0.3,
        },
        "resolution_tier_map": {
            "premium": {"min_width_px": 4000, "score": 1.0},
            "standard": {"min_width_px": 2000, "score": 0.75},
            "marginal": {"min_width_px": 1200, "score": 0.4},
            "blocked": {"min_width_px": 0, "score": 0.0},
        },
        "csm_dimension_map": {
            "scorer_version": "csm_pass2_v1",
            "dimensions": {
                "VAS": {"inputs": [
                    {"signal": "image_quality_score", "weight": 0.50},
                    {"signal": "composition_fit", "weight": 0.30},
                    {"signal": "color_score", "weight": 0.20},
                ]},
                "PIS": {"inputs": [
                    {"signal": "place_relevance_score", "weight": 0.60},
                    {"signal": "taxon_place_iconic", "weight": 0.40},
                ]},
                "SSS": {"inputs": [
                    {"signal": "provenance_completeness", "weight": 0.40},
                    {"signal": "golden_age_factor", "weight": 0.35},
                    {"signal": "illustrator_prestige", "weight": 0.25},
                ]},
                "TAS": {"inputs": [
                    {"signal": "taxon_place_iconic", "weight": 0.40},
                    {"signal": "place_tier_score", "weight": 0.35},
                    {"signal": "place_relevance_score", "weight": 0.25},
                ]},
                "IPS": {"inputs": [
                    {"signal": "institutional_credit", "weight": 0.70},
                    {"signal": "provenance_completeness", "weight": 0.30},
                ]},
                "PVS": {"inputs": [
                    {"signal": "resolution_tier_score", "weight": 0.70},
                    {"signal": "identification_confidence", "weight": 0.30},
                ]},
            },
            "composite": {"inputs": [
                {"signal": "VAS", "weight": 0.30},
                {"signal": "PIS", "weight": 0.20},
                {"signal": "SSS", "weight": 0.15},
                {"signal": "TAS", "weight": 0.15},
                {"signal": "IPS", "weight": 0.10},
                {"signal": "PVS", "weight": 0.10},
            ]},
            "tier_thresholds": {
                "MASTERWORK": 0.90,
                "FLAGSHIP": 0.75,
                "STANDARD": 0.60,
                "REFERENCE": 0.40,
                "BLOCKED": 0.0,
            },
            "rcs_gate": {
                "signal": "rights_confidence",
                "min_value": 0.70,
                "blocked_tier": "BLOCKED",
            },
        },
    }
    return {
        "id": _POLICY_ID,
        "version": "1.0.0",
        "formula_spec": formula_spec,
        "tier_thresholds": {"tier_1": 0.80, "tier_2": 0.65, "tier_3": 0.50, "blocked": 0.0},
        "hard_gate_values": {
            "gate_0_rights_record_exists": {"required": True, "blocked_status": "blocked_rights"},
            "gate_1_min_rights_confidence": {"min_rights_confidence": 0.70, "blocked_status": "blocked_rights"},
            "gate_2_min_image_width_px": {"min_image_width_px": 2000, "blocked_status": "blocked_resolution"},
            "gate_3_legal_hold": {"rights_confidence_equals": 0.0, "blocked_status": "blocked_legal"},
            "gate_4_min_quality_score": {"min_quality_score": 0.40, "null_blocks": True, "blocked_status": "blocked_quality"},
        },
        "product_surface_requirements": {
            "wall_art_premium": {"min_cos": 0.80, "min_image_width_px": 4000, "min_quality_score": 0.75},
            "wall_art_standard": {"min_cos": 0.65, "min_image_width_px": 2000, "min_quality_score": 0.55},
            "calendar": {"min_cos": 0.65, "min_composition_fit": 0.60},
            "puzzle": {"min_cos": 0.60, "min_composition_fit": 0.65},
            "card": {"min_cos": 0.55, "min_image_width_px": 1200, "min_quality_score": 0.50},
            "book_illustration": {"min_publishing_score": 0.70, "min_identification_confidence": 0.85},
            "educational": {"min_reference_score": 0.65},
            "museum_print": {"min_museum_score": 0.80, "illustrator_prestige": 1.0, "min_rights_confidence": 1.0},
            "institutional_license": {"min_museum_score": 0.80, "min_rights_confidence": 1.0},
        },
    }


def _base_inputs() -> dict:
    return {
        "rights_record_exists": True,
        "rights_confidence": 1.0,
        "golden_age_factor": 1.0,
        "institutional_credit": 1.0,
        "provenance_completeness": 1.0,
        "place_relevance_score": 1.0,
        "place_tier_score": 1.0,
        "illustrator_prestige": 1.0,
        "taxon_commercial_tier": None,
        "taxon_commercial_tier_score": 1.0,
        "taxon_place_iconic": 1.0,
        "image_quality_score": 1.0,
        "composition_fit": 1.0,
        "identification_confidence": 1.0,
        "color_profile": "chromolithograph",
        "color_score": 1.0,
        "image_width_px": 5200,
    }


def _benchmark_inputs(name: str) -> dict:
    data = _base_inputs()
    if name == "moran":
        data.update({"image_quality_score": 1.0, "composition_fit": 1.0, "color_score": 1.0, "provenance_completeness": 0.95, "image_width_px": 5000})
    elif name == "hayden":
        data.update({"image_quality_score": 0.95, "composition_fit": 0.95, "color_score": 0.95, "place_tier_score": 0.57, "image_width_px": 5000})
    elif name == "jackson":
        data.update({"image_quality_score": 0.80, "composition_fit": 0.80, "color_score": 0.80, "place_relevance_score": 0.95, "taxon_place_iconic": 0.95, "place_tier_score": 0.95, "provenance_completeness": 0.90, "illustrator_prestige": 0.90, "taxon_commercial_tier_score": 0.85, "image_width_px": 2400})
    elif name == "audubon":
        data.update({"image_quality_score": 0.98, "composition_fit": 0.98, "color_score": 0.98, "place_relevance_score": 0.85, "taxon_place_iconic": 0.85, "place_tier_score": 1.0, "image_width_px": 5000})
    else:
        raise AssertionError(name)
    return data


@pytest.mark.parametrize(
    ("fixture", "expected_csm_tier", "min_csm", "expected_commerce_tier"),
    [
        ("hayden", "MASTERWORK", 0.90, "tier_1"),
        ("moran", "MASTERWORK", 0.90, "tier_1"),
        ("jackson", "FLAGSHIP", 0.75, "tier_1"),
        ("audubon", "MASTERWORK", 0.90, "tier_1"),
    ],
)
def test_benchmark_fixture_scores_expected_tiers(fixture: str, expected_csm_tier: str, min_csm: float, expected_commerce_tier: str) -> None:
    result = compute_scores(_policy(), _benchmark_inputs(fixture), opportunity_id=str(uuid4()))

    assert result.score_outputs["csm_tier"] == expected_csm_tier
    assert result.score_outputs["csm_score"] >= min_csm
    assert result.score_outputs["commerce_tier"] == expected_commerce_tier
    for subscore in ("museum_score", "retail_score", "publishing_score", "tourism_score", "reference_score"):
        assert 0.0 <= result.score_outputs[subscore] <= 1.0


def test_replay_recomputes_identical_outputs_from_audit_snapshot() -> None:
    result = compute_scores(_policy(), _benchmark_inputs("hayden"), opportunity_id=str(uuid4()))

    assert replay_score(_policy(), result.score_inputs, result.score_outputs)


def test_hard_gate_failure_blocks_scores_and_tier() -> None:
    inputs = _benchmark_inputs("moran")
    inputs["image_width_px"] = 800

    result = compute_scores(_policy(), inputs, opportunity_id=str(uuid4()))

    assert result.hard_gate_failure == "blocked_resolution"
    assert result.score_outputs["commerce_opportunity_score"] == 0.0
    assert result.score_outputs["commerce_tier"] == "blocked"
    assert result.score_outputs["csm_tier"] == "BLOCKED"
    assert result.commerce_record["eligible_wall_art_standard"] is False


class FakeTx:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeCommerceConn:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.fetchrow_queries: list[tuple[str, tuple]] = []
        self.execute_queries: list[tuple[str, tuple]] = []

    def transaction(self):
        self.calls.append("transaction")
        return FakeTx()

    async def fetchrow(self, query: str, *args):
        self.fetchrow_queries.append((query, args))
        if "FROM commerce_opportunities" in query and "RETURNING" not in query:
            return None
        if "FROM score_audit_log" in query:
            return None
        if "INSERT INTO commerce_opportunities" in query:
            self.calls.append("commerce")
            return {"id": UUID("30000000-0000-0000-0000-000000000099")}
        return None

    async def execute(self, query: str, *args):
        self.execute_queries.append((query, args))
        if "INSERT INTO score_audit_log" in query:
            self.calls.append("audit")
        return "OK"


async def test_store_writes_score_audit_log_before_commerce_opportunity() -> None:
    conn = FakeCommerceConn()
    computation = compute_scores(
        _policy(),
        _benchmark_inputs("audubon"),
        opportunity_id=str(_OPPORTUNITY_ID),
        event_at=datetime(2026, 6, 6, tzinfo=UTC),
    )

    commerce_id = await write_score_and_opportunity(conn, _policy(), _OPPORTUNITY_ID, computation)

    assert commerce_id == UUID("30000000-0000-0000-0000-000000000099")
    assert conn.calls.index("audit") < conn.calls.index("commerce")
    audit_query, audit_args = next((q, a) for q, a in conn.execute_queries if "INSERT INTO score_audit_log" in q)
    commerce_query, _ = next((q, a) for q, a in conn.fetchrow_queries if "INSERT INTO commerce_opportunities" in q)
    assert WORKER_VERSION in audit_args
    assert "product_recommendations" not in audit_query
    assert "collection_recommendations" not in commerce_query


def test_score_hash_is_replay_safe_for_same_inputs() -> None:
    first = compute_scores(_policy(), _benchmark_inputs("jackson"), opportunity_id=str(_OPPORTUNITY_ID), event_at=datetime(2026, 6, 6, tzinfo=UTC))
    second = compute_scores(_policy(), deepcopy(_benchmark_inputs("jackson")), opportunity_id=str(_OPPORTUNITY_ID), event_at=datetime(2026, 6, 6, tzinfo=UTC))

    assert first.input_hash_sha256 == second.input_hash_sha256
    assert first.audit_checksum_sha256 == second.audit_checksum_sha256



def test_build_input_snapshot_uses_explicit_rights_evidence_for_gate_0() -> None:
    opportunity = {
        "source": "bhl",
        "rights_status": "Public Domain",
        "rights_verified_by": "metadata-only",
        "rights_evidence_exists": 0,
        "asset_rights_record_exists": 0,
        "illustration_quality_score": 0.95,
        "score_components": {"image_width_px": 2600},
    }

    inputs = build_input_snapshot(opportunity)
    result = compute_scores(_policy(), inputs, opportunity_id=str(uuid4()))

    assert inputs["rights_record_exists"] is False
    assert result.hard_gate_failure == "blocked_rights"
    assert result.score_outputs["hard_gate_status"] == "blocked_rights"


def test_build_input_snapshot_missing_width_fails_resolution_gate() -> None:
    opportunity = {
        "source": "bhl",
        "rights_status": "Public Domain",
        "rights_verified_by": "phase3",
        "rights_evidence_exists": 1,
        "asset_rights_record_exists": 0,
        "illustration_quality_score": 0.95,
        "score_components": {},
    }

    inputs = build_input_snapshot(opportunity)
    result = compute_scores(_policy(), inputs, opportunity_id=str(uuid4()))

    assert inputs["image_width_px"] == 0
    assert result.hard_gate_failure == "blocked_resolution"


class FakeClaimConn:
    def __init__(self) -> None:
        self.query = ""

    async def fetch(self, query: str, *args):
        self.query = query
        return []


async def test_claim_query_does_not_bypass_hard_gate_inputs() -> None:
    conn = FakeClaimConn()

    await claim_approved_opportunities(conn, 10)

    assert "io.status = 'approved'" in conn.query
    assert "io.rights_status IN ('Public Domain','CC0')" not in conn.query
    assert "io.rights_verified_by IS NOT NULL" not in conn.query
    assert "illustration_opportunity_evidence" in conn.query
    assert "taxon_commercial_tier_vocabulary" in conn.query
    assert "tctv.status = 'active'" in conn.query
    assert "tctv.approved_by IS NOT NULL" in conn.query


def test_build_input_snapshot_uses_governed_taxon_tier_values_only() -> None:
    governed = build_input_snapshot({
        "source": "bhl",
        "rights_status": "Public Domain",
        "rights_evidence_exists": 1,
        "illustrator": "John James Audubon",
        "taxon_commercial_tier": "high",
        "taxon_commercial_tier_score": 0.65,
        "illustration_quality_score": 0.9,
        "score_components": {"image_width_px": 2600},
    })
    missing_governed = build_input_snapshot({
        "source": "bhl",
        "rights_status": "Public Domain",
        "rights_evidence_exists": 1,
        "illustrator": "John James Audubon",
        "illustration_quality_score": 0.9,
        "score_components": {"image_width_px": 2600},
    })

    assert governed["taxon_commercial_tier"] == "high"
    assert governed["taxon_commercial_tier_score"] == 0.65
    assert governed["illustrator_prestige"] == 1.0
    assert missing_governed["taxon_commercial_tier"] is None
    assert missing_governed["taxon_commercial_tier_score"] == 0.0


def test_csm_rights_gate_uses_policy_threshold() -> None:
    policy = _policy()
    policy["formula_spec"]["csm_dimension_map"]["rcs_gate"]["min_value"] = 0.95
    inputs = _benchmark_inputs("audubon")
    inputs["rights_confidence"] = 0.90

    result = compute_scores(policy, inputs, opportunity_id=str(uuid4()))

    assert result.score_outputs["commerce_tier"] != "blocked"
    assert result.score_outputs["csm_tier"] == "BLOCKED"


def test_policy_seed_contains_runtime_schema_expected_by_worker() -> None:
    sql = Path("infrastructure/postgres/init/20_commerce_policy.sql").read_text()

    assert '"scorer_version": "weighted_sum_v1"' in sql
    assert '"csm_dimension_map"' in sql
    assert '"tier_thresholds"' in sql
    assert '"rcs_gate": {' in sql
    assert '"signal": "rights_confidence"' in sql
    assert '"min_value": 0.70' in sql
    assert '"blocked_tier": "BLOCKED"' in sql
    assert "tier_thresholds" in sql and "JSONB NOT NULL" in sql
    assert "hard_gate_values" in sql and "JSONB NOT NULL" in sql
    assert "product_surface_requirements" in sql and "JSONB NOT NULL" in sql


def test_replay_worker_verifies_audit_entry_against_pinned_policy() -> None:
    computation = compute_scores(
        _policy(),
        _benchmark_inputs("hayden"),
        opportunity_id=str(_OPPORTUNITY_ID),
        event_at=datetime(2026, 6, 6, tzinfo=UTC),
    )
    audit_entry = {
        "id": UUID("30000000-0000-0000-0000-000000000088"),
        "opportunity_id": _OPPORTUNITY_ID,
        "score_inputs": computation.score_inputs,
        "score_outputs": computation.score_outputs,
    }

    result = verify_audit_entry(_policy(), audit_entry)

    assert result.verified is True
    assert result.expected_event_type == "replay_verified"


def test_replay_worker_detects_score_mismatch() -> None:
    computation = compute_scores(
        _policy(),
        _benchmark_inputs("hayden"),
        opportunity_id=str(_OPPORTUNITY_ID),
        event_at=datetime(2026, 6, 6, tzinfo=UTC),
    )
    tampered_outputs = deepcopy(computation.score_outputs)
    tampered_outputs["commerce_opportunity_score"] = 0.001
    audit_entry = {
        "id": UUID("30000000-0000-0000-0000-000000000089"),
        "opportunity_id": _OPPORTUNITY_ID,
        "score_inputs": computation.score_inputs,
        "score_outputs": tampered_outputs,
    }

    result = verify_audit_entry(_policy(), audit_entry)

    assert result.verified is False
    assert result.expected_event_type == "replay_failure"
