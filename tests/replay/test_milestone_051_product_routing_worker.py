"""v0.5.1 Product Routing Worker replay tests."""
from __future__ import annotations

import importlib.util
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

from workers.commerce_opportunity_worker.score import compute_scores
from workers.product_routing_worker import WORKER_VERSION
from workers.product_routing_worker.route import route_product_families
from workers.product_routing_worker.store import claim_routable_commerce_opportunities, write_product_routes

_PHASE3_SPEC = importlib.util.spec_from_file_location(
    "phase3_commerce_worker_fixtures",
    Path(__file__).with_name("test_milestone_050_commerce_opportunity_worker.py"),
)
assert _PHASE3_SPEC and _PHASE3_SPEC.loader
_PHASE3 = importlib.util.module_from_spec(_PHASE3_SPEC)
_PHASE3_SPEC.loader.exec_module(_PHASE3)
_benchmark_inputs = _PHASE3._benchmark_inputs
_policy = _PHASE3._policy

_ROUTING_POLICY_ID = UUID("40000000-0000-0000-0000-000000000001")


def _routing_policy() -> dict:
    return {
        "id": _ROUTING_POLICY_ID,
        "version": "1.0.0",
        "product_surface_requirements": {
            "wall_art": {
                "required_flags": ["eligible_wall_art_standard"],
                "min_cos": 0.65,
                "min_image_width_px": 2000,
                "min_quality_score": 0.55,
                "basis_model": "retail_score",
                "recommended_product_types": ["standard_print"],
            },
            "calendar": {
                "required_flags": ["eligible_calendar"],
                "min_cos": 0.65,
                "min_composition_fit": 0.60,
                "basis_model": "tourism_score",
                "recommended_product_types": ["calendar"],
            },
            "book": {
                "required_flags": ["eligible_book_illustration"],
                "min_publishing_score": 0.70,
                "min_identification_confidence": 0.85,
                "basis_model": "publishing_score",
                "recommended_product_types": ["book_illustration"],
            },
            "puzzle": {
                "required_flags": ["eligible_puzzle"],
                "min_cos": 0.60,
                "min_composition_fit": 0.65,
                "basis_model": "retail_score",
                "recommended_product_types": ["puzzle"],
            },
            "card": {
                "required_flags": ["eligible_card"],
                "min_cos": 0.55,
                "min_image_width_px": 1200,
                "min_quality_score": 0.50,
                "basis_model": "retail_score",
                "recommended_product_types": ["card"],
            },
            "museum_print": {
                "required_flags": ["eligible_museum_print"],
                "min_museum_score": 0.80,
                "basis_model": "museum_score",
                "recommended_product_types": ["archival_print"],
            },
            "educational": {
                "required_flags": ["eligible_educational"],
                "min_reference_score": 0.65,
                "basis_model": "reference_score",
                "recommended_product_types": ["education_license"],
            },
            "institutional_license": {
                "required_flags": ["eligible_institutional_license"],
                "min_museum_score": 0.80,
                "basis_model": "museum_score",
                "recommended_product_types": ["institutional_license"],
            },
        },
        "routing_formula_spec": {
            "routing_scorer_version": "product_routing_weighted_threshold_v1",
            "status_on_create": "pending_curator_review",
            "confidence_weights": {
                "commerce_opportunity_score": 0.45,
                "basis_model_score": 0.35,
                "csm_score": 0.20,
            },
        },
        "family_caps": {"max_recommendations_per_opportunity": 8},
        "curator_gate_spec": {},
    }


def _commerce_record(name: str) -> dict:
    result = compute_scores(
        _policy(),
        _benchmark_inputs(name),
        opportunity_id=str(uuid4()),
        event_at=datetime(2026, 6, 6, tzinfo=UTC),
    )
    record = dict(result.commerce_record)
    record.update(
        {
            "id": uuid4(),
            "opportunity_id": uuid4(),
            "policy_version_id": _policy()["id"],
            "curator_decision": "approved",
            "policy_stale": False,
        }
    )
    return record


def _families(routes) -> set[str]:
    return {route.recommended_product_family for route in routes}


def test_moran_routes_to_premium_nature_and_culture_products() -> None:
    routes = route_product_families(_routing_policy(), _commerce_record("moran"))

    families = _families(routes)
    assert {"wall_art", "museum_print", "book", "educational", "institutional_license"}.issubset(families)
    assert all(route.recommended_providers == {} for route in routes)


def test_hayden_routes_to_map_print_and_reference_products() -> None:
    routes = route_product_families(_routing_policy(), _commerce_record("hayden"))

    families = _families(routes)
    assert {"wall_art", "museum_print", "book", "educational", "institutional_license"}.issubset(families)
    assert all(route.recommendation_basis["routing_policy_version"] == "1.0.0" for route in routes)


def test_jackson_routes_correctly_without_museum_print() -> None:
    routes = route_product_families(_routing_policy(), _commerce_record("jackson"))

    families = _families(routes)
    assert {"wall_art", "calendar"}.issubset(families)
    assert "museum_print" not in families


def test_routes_are_replay_deterministic_for_same_policy_and_record() -> None:
    record = _commerce_record("moran")

    first = route_product_families(_routing_policy(), record)
    second = route_product_families(deepcopy(_routing_policy()), deepcopy(record))

    assert first == second


def test_routing_requires_approved_current_unblocked_commerce_opportunity() -> None:
    record = _commerce_record("moran")

    for key, value in (
        ("curator_decision", "pending"),
        ("policy_stale", True),
        ("commerce_tier", "blocked"),
        ("hard_gate_status", "blocked_rights"),
    ):
        blocked = dict(record)
        blocked[key] = value
        assert route_product_families(_routing_policy(), blocked) == []


class FakeTx:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeRoutingConn:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.fetchrow_queries: list[tuple[str, tuple]] = []
        self.execute_queries: list[tuple[str, tuple]] = []

    def transaction(self):
        self.calls.append("transaction")
        return FakeTx()

    async def fetchrow(self, query: str, *args):
        self.fetchrow_queries.append((query, args))
        if "FROM score_audit_log" in query:
            return None
        if "INSERT INTO product_recommendations" in query:
            self.calls.append("recommendation")
            return {"id": UUID("40000000-0000-0000-0000-000000000099")}
        return None

    async def execute(self, query: str, *args):
        self.execute_queries.append((query, args))
        if "INSERT INTO score_audit_log" in query:
            self.calls.append("audit")
        return "OK"


async def test_store_writes_score_audit_log_before_product_recommendation() -> None:
    conn = FakeRoutingConn()
    commerce_record = _commerce_record("jackson")
    routes = route_product_families(_routing_policy(), commerce_record)[:1]

    ids = await write_product_routes(
        conn,
        _routing_policy(),
        commerce_record,
        routes,
        event_at=datetime(2026, 6, 6, tzinfo=UTC),
    )

    assert ids == [UUID("40000000-0000-0000-0000-000000000099")]
    assert conn.calls.index("audit") < conn.calls.index("recommendation")
    audit_query, audit_args = next((q, a) for q, a in conn.execute_queries if "INSERT INTO score_audit_log" in q)
    rec_query, rec_args = next((q, a) for q, a in conn.fetchrow_queries if "INSERT INTO product_recommendations" in q)
    assert "product_route_recommended" in audit_query
    assert WORKER_VERSION in audit_args
    assert rec_args[5] == "{}"
    assert "collection_recommendations" not in rec_query


async def test_store_uses_monotonic_event_times_for_audit_chain() -> None:
    conn = FakeRoutingConn()
    commerce_record = _commerce_record("moran")
    routes = route_product_families(_routing_policy(), commerce_record)[:3]

    await write_product_routes(
        conn,
        _routing_policy(),
        commerce_record,
        routes,
        event_at=datetime(2026, 6, 6, tzinfo=UTC),
    )

    audit_event_times = [args[2] for query, args in conn.execute_queries if "INSERT INTO score_audit_log" in query]
    assert audit_event_times == sorted(audit_event_times)
    assert len(set(audit_event_times)) == len(audit_event_times)


class FakeClaimConn:
    def __init__(self) -> None:
        self.query = ""

    async def fetch(self, query: str, *args):
        self.query = query
        return []


async def test_claim_query_uses_postgresql_governance_gates() -> None:
    conn = FakeClaimConn()

    await claim_routable_commerce_opportunities(conn, 10)

    assert "co.curator_decision = 'approved'" in conn.query
    assert "co.hard_gate_status = 'passed'" in conn.query
    assert "co.policy_stale = FALSE" in conn.query
    assert "co.commerce_tier <> 'blocked'" in conn.query
    assert "product_recommendations" in conn.query
    assert "collection_recommendations" not in conn.query
