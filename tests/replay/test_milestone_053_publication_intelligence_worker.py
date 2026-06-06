"""v0.5.3 Publication Intelligence replay tests."""
from __future__ import annotations

import importlib.util
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

from workers.commerce_opportunity_worker.score import compute_scores
from workers.publication_replay_worker.replay import verify_publication_replay
from workers.publication_worker import WORKER_VERSION
from workers.publication_worker.publication import build_publication_candidate, is_publication_stale
from workers.publication_worker.store import claim_publication_inputs, write_publication_candidate

_PHASE3_SPEC = importlib.util.spec_from_file_location(
    "phase3_commerce_worker_fixtures",
    Path(__file__).with_name("test_milestone_050_commerce_opportunity_worker.py"),
)
assert _PHASE3_SPEC and _PHASE3_SPEC.loader
_PHASE3 = importlib.util.module_from_spec(_PHASE3_SPEC)
_PHASE3_SPEC.loader.exec_module(_PHASE3)
_benchmark_inputs = _PHASE3._benchmark_inputs
_policy = _PHASE3._policy

_PUBLICATION_POLICY_ID = UUID("60000000-0000-0000-0000-000000000001")
_CHANNEL_ID = UUID("60000000-0000-0000-0000-000000000002")


def _publication_policy() -> dict:
    return {
        "id": _PUBLICATION_POLICY_ID,
        "version": "1.0.0",
        "eligibility_gates": {"requires_catalog_status": ["draft", "approved"]},
        "channel_fit_rules": {"weights": {"family_allowed": 0.45, "quality_fit": 0.25, "commerce_fit": 0.20, "variant_fit": 0.10}},
        "publication_readiness_rules": {"weights": {"metadata_complete": 0.25, "rights_confidence": 0.30, "media_ready": 0.20, "price_ready": 0.15, "variant_complete": 0.10}},
        "risk_rules": {"weights": {"rights_uncertainty": 0.50, "missing_media": 0.25, "missing_metadata": 0.25}, "block_if_risk_above": 0.700},
        "ranking_rules": {"weights": {"readiness_score": 0.45, "channel_fit_score": 0.40, "inverse_risk_score": 0.15}, "recommend_threshold": 0.750, "hold_threshold": 0.500, "risk_recommend_max": 0.250, "priority_thresholds": {"high": 0.850, "medium": 0.650, "low": 0.000}},
        "staleness_rules": {"stale_parent_catalog_statuses": ["needs_revision", "blocked", "retired", "superseded"], "stale_variant_statuses": ["needs_revision", "blocked", "retired", "superseded"]},
    }


def _channel_profile() -> dict:
    return {
        "id": _CHANNEL_ID,
        "profile_key": "editorial_catalog",
        "allowed_product_families": ["wall_art", "calendar", "museum_print"],
        "minimum_rights_confidence": 0.70,
        "risk_tolerance": 0.25,
    }


def _commerce_record(name: str) -> dict:
    result = compute_scores(_policy(), _benchmark_inputs(name), opportunity_id=str(uuid4()), event_at=datetime(2026, 6, 6, tzinfo=UTC))
    record = dict(result.commerce_record)
    record.update({"id": uuid4(), "opportunity_id": uuid4(), "policy_version_id": _policy()["id"], "curator_decision": "approved", "policy_stale": False})
    return record


def _catalog_candidate(name: str, family: str = "wall_art") -> dict:
    return {
        "id": uuid4(),
        "product_recommendation_id": uuid4(),
        "commerce_opportunity_id": uuid4(),
        "opportunity_id": uuid4(),
        "product_family": family,
        "catalog_title": f"{name.title()} Catalog Candidate",
        "catalog_description": f"Internal candidate for {name}",
        "catalog_status": "draft",
        "rights_snapshot": {"rights_confidence": 1.0, "hard_gate_status": "passed"},
        "media_requirements": {"required_assets": ["source_image"], "min_width_px": 2000},
    }


def _catalog_variant(candidate: dict, family: str = "wall_art") -> dict:
    return {
        "id": uuid4(),
        "catalog_candidate_id": candidate["id"],
        "product_family": family,
        "product_type": "standard_print" if family == "wall_art" else "calendar",
        "variant_key": "standard_print_12x16" if family == "wall_art" else "wall_calendar_annual",
        "variant_title": "Variant",
        "variant_status": "draft",
        "asset_requirements": {"required_assets": ["source_image"]},
        "price_snapshot": {"currency": "USD", "final_price_cents": 3699},
    }


def _aligned_inputs(name: str, family: str = "wall_art"):
    commerce = _commerce_record(name)
    candidate = _catalog_candidate(name, family)
    candidate["commerce_opportunity_id"] = commerce["id"]
    candidate["opportunity_id"] = commerce["opportunity_id"]
    variant = _catalog_variant(candidate, family)
    return commerce, candidate, variant


def test_moran_creates_publication_candidate() -> None:
    commerce, candidate, variant = _aligned_inputs("moran")
    result = build_publication_candidate(_publication_policy(), _channel_profile(), candidate, variant, commerce)

    assert result.decision == "recommend"
    assert result.publication_status == "draft"
    assert result.publication_score >= 0.75


def test_hayden_creates_publication_candidate() -> None:
    commerce, candidate, variant = _aligned_inputs("hayden")
    result = build_publication_candidate(_publication_policy(), _channel_profile(), candidate, variant, commerce)

    assert result.decision in {"recommend", "hold"}
    assert result.readiness_score >= 0.90


def test_jackson_creates_publication_candidate() -> None:
    commerce, candidate, variant = _aligned_inputs("jackson", "calendar")
    result = build_publication_candidate(_publication_policy(), _channel_profile(), candidate, variant, commerce)

    assert result.publication_channel_profile_id == str(_CHANNEL_ID)
    assert result.channel_fit_score >= 0.70


def test_publication_replay_reproduces_scores() -> None:
    commerce, candidate, variant = _aligned_inputs("moran")
    expected = build_publication_candidate(_publication_policy(), _channel_profile(), candidate, variant, commerce).__dict__

    replay = verify_publication_replay(_publication_policy(), _channel_profile(), candidate, variant, commerce, expected)

    assert replay.verified is True
    assert replay.expected_event_type == "publication_replay_verified"


def test_staleness_handling_works() -> None:
    commerce, candidate, variant = _aligned_inputs("moran")
    stale_candidate = dict(candidate)
    stale_candidate["catalog_status"] = "retired"

    assert is_publication_stale(_publication_policy(), stale_candidate, variant, commerce)
    result = build_publication_candidate(_publication_policy(), _channel_profile(), stale_candidate, variant, commerce)
    assert result.staleness_status == "stale"
    assert result.publication_status == "stale"
    assert result.decision == "block"


class FakeTx:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakePublicationConn:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.fetchrow_queries: list[tuple[str, tuple]] = []
        self.execute_queries: list[tuple[str, tuple]] = []

    def transaction(self):
        self.calls.append("transaction")
        return FakeTx()

    async def fetchrow(self, query: str, *args):
        self.fetchrow_queries.append((query, args))
        if "FROM publication_audit_log" in query:
            return None
        if "INSERT INTO publication_candidates" in query:
            self.calls.append("candidate")
            return {"id": UUID("60000000-0000-0000-0000-000000000099")}
        return None

    async def execute(self, query: str, *args):
        self.execute_queries.append((query, args))
        if "INSERT INTO publication_audit_log" in query:
            self.calls.append("audit")
        return "OK"


async def test_audit_chain_works() -> None:
    conn = FakePublicationConn()
    commerce, candidate, variant = _aligned_inputs("moran")

    publication_id = await write_publication_candidate(conn, _publication_policy(), _channel_profile(), candidate, variant, commerce, event_at=datetime(2026, 6, 6, tzinfo=UTC))

    assert publication_id == UUID("60000000-0000-0000-0000-000000000099")
    assert conn.calls.index("audit") < conn.calls.index("candidate")
    audit_query, audit_args = next((q, a) for q, a in conn.execute_queries if "INSERT INTO publication_audit_log" in q)
    assert "publication_candidate_created" in audit_args
    assert WORKER_VERSION in audit_args
    assert "external" not in audit_query.lower()


def test_no_external_publication_state_exists() -> None:
    commerce, candidate, variant = _aligned_inputs("moran")
    result = build_publication_candidate(_publication_policy(), _channel_profile(), candidate, variant, commerce)
    text = str(result.__dict__).lower()

    for blocked in ("shopify", "etsy", "gelato", "printful", "lulu", "external_id", "api", "provider"):
        assert blocked not in text


class FakeClaimConn:
    def __init__(self) -> None:
        self.query = ""

    async def fetch(self, query: str, *args):
        self.query = query
        return []


async def test_claim_query_uses_publication_gates() -> None:
    conn = FakeClaimConn()

    await claim_publication_inputs(conn, 10)

    assert "cc.catalog_status IN ('draft','approved')" in conn.query
    assert "cv.variant_status IN ('draft','approved')" in conn.query
    assert "pr.status = 'curator_approved'" in conn.query
    assert "co.curator_decision = 'approved'" in conn.query
    assert "co.hard_gate_status = 'passed'" in conn.query
    assert "co.policy_stale = FALSE" in conn.query
