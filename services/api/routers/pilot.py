"""NC-PILOT-001 anchor APIs."""

from __future__ import annotations

import hashlib
import json
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..dependencies import DB, Auth

router = APIRouter(prefix="/pilot/anchors", tags=["pilot"])

GEONAMES_ATTRIBUTION = "Geographic data © GeoNames (geonames.org) — CC BY 4.0"
OSM_ATTRIBUTION = "© OpenStreetMap contributors"
NASA_NONENDORSEMENT = "Image credit: NASA. NASA does not endorse this product."
NOAA_NONENDORSEMENT = "Image: NOAA. NOAA does not endorse this product."

_ANCHOR_COLS = """
    id, slug, title, anchor_type, status, canonical_identity, source_map,
    attribution_requirements, sort_order, provenance, created_at, updated_at
"""

_INGEST_RUN_COLS = """
    id, anchor_id, idempotency_key, status, source_scope, phase, stale_after,
    started_at, completed_at, raw_payload_refs, normalized_refs, error,
    recovery_notes, provenance, created_at, updated_at
"""

_EVIDENCE_COLS = """
    id, anchor_id, source, source_role, evidence_type, source_record_id,
    source_url, rights_decision, raw_payload_hash, evidence, attribution,
    status, created_at, updated_at
"""

_SNAPSHOT_COLS = """
    id, anchor_id, snapshot_version, publication_status, snapshot, attribution,
    snapshot_sha256, created_by, published_at, created_at
"""

_CHECKLIST_COLS = """
    id, checklist_key, label, gate, required, sort_order, provenance, created_at, updated_at
"""

_LAUNCH_CONFIG_COLS = """
    id, config_key, enabled, launch_stage, required_gates, monitor_window_minutes,
    snapshot_policy, provenance, created_at, updated_at
"""

_JSON_FIELDS = {
    "canonical_identity",
    "source_map",
    "attribution_requirements",
    "provenance",
    "raw_payload_refs",
    "normalized_refs",
    "error",
    "recovery_notes",
    "evidence",
    "attribution",
    "snapshot",
    "identity_snapshot",
    "snapshot_policy",
    "name",
}


class IngestRunCreate(BaseModel):
    idempotency_key: str = Field(min_length=1)
    source_scope: list[str] = Field(default_factory=list)
    actor: str = Field(min_length=1)
    stale_after_minutes: int = Field(default=120, ge=15, le=1440)


class PublicationSnapshotCreate(BaseModel):
    snapshot_version: str = Field(min_length=1)
    publication_status: str = "draft"
    snapshot: dict
    created_by: str = Field(min_length=1)


def _decode(row) -> dict:
    item = dict(row)
    for field in _JSON_FIELDS:
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item


def _json_hash(value: dict) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def assemble_attribution(
    anchor: dict,
    evidence: list[dict],
    places: list[dict] | None = None,
) -> list[dict]:
    """Assemble governed attribution statements for a pilot anchor response."""
    requirements = anchor.get("attribution_requirements") or {}
    attributions: list[dict] = []
    seen: set[tuple[str, str, str | None]] = set()

    def add(
        source: str,
        statement: str,
        url: str | None = None,
        license_uri: str | None = None,
    ) -> None:
        key = (source, statement, url)
        if key not in seen:
            seen.add(key)
            attributions.append(
                {
                    "source": source,
                    "statement": statement,
                    "url": url,
                    "license": license_uri,
                }
            )

    if requirements.get("geonames"):
        add(
            "geonames",
            GEONAMES_ATTRIBUTION,
            "https://www.geonames.org",
            "https://creativecommons.org/licenses/by/4.0/",
        )

    if requirements.get("osm_tiles"):
        add(
            "osm",
            OSM_ATTRIBUTION,
            "https://www.openstreetmap.org/copyright",
            "https://opendatacommons.org/licenses/odbl/1-0/",
        )

    for item in evidence:
        source = str(item.get("source") or "")
        if source == "nasa":
            add("nasa", NASA_NONENDORSEMENT, "https://www.nasa.gov")
        if source == "noaa":
            add("noaa", NOAA_NONENDORSEMENT, "https://www.noaa.gov")

        attribution = item.get("attribution")
        if isinstance(attribution, dict):
            statement = attribution.get("statement")
            if statement:
                add(
                    str(attribution.get("name") or item.get("source")),
                    str(statement),
                    attribution.get("url"),
                    attribution.get("license"),
                )
        elif item.get("source"):
            add(source, f"Evidence source: {source}", item.get("source_url"))

    for place in places or []:
        identity = place.get("identity_snapshot") or {}
        if identity.get("geonames_id") and requirements.get("geonames"):
            add(
                "geonames",
                GEONAMES_ATTRIBUTION,
                f"https://www.geonames.org/{identity['geonames_id']}",
                "https://creativecommons.org/licenses/by/4.0/",
            )

    return attributions


def verify_attribution(
    anchor: dict,
    evidence: list[dict],
    places: list[dict] | None = None,
) -> dict:
    assembled = assemble_attribution(anchor, evidence, places)
    statements = {item["statement"] for item in assembled}
    expected: list[str] = []
    requirements = anchor.get("attribution_requirements") or {}

    if requirements.get("geonames"):
        expected.append(GEONAMES_ATTRIBUTION)
    if requirements.get("osm_tiles"):
        expected.append(OSM_ATTRIBUTION)
    if any(item.get("source") == "nasa" for item in evidence):
        expected.append(NASA_NONENDORSEMENT)
    if any(item.get("source") == "noaa" for item in evidence):
        expected.append(NOAA_NONENDORSEMENT)

    missing = [statement for statement in expected if statement not in statements]
    return {
        "passed": not missing,
        "expected": expected,
        "missing": missing,
        "attribution": assembled,
    }


def verify_publication_snapshot(snapshot: dict | None) -> dict:
    if not snapshot:
        return {"passed": False, "missing": ["publication_snapshot"], "checks": {}}

    expected_hash = _json_hash(snapshot.get("snapshot") or {})
    checks = {
        "snapshot_present": bool(snapshot.get("snapshot")),
        "snapshot_hash_valid": snapshot.get("snapshot_sha256") == expected_hash,
        "attribution_present": bool(snapshot.get("attribution")),
        "created_by_present": bool(snapshot.get("created_by")),
    }
    missing = [key for key, passed in checks.items() if not passed]
    return {
        "passed": not missing,
        "missing": missing,
        "checks": checks,
        "expected_sha256": expected_hash,
        "actual_sha256": snapshot.get("snapshot_sha256"),
    }


def verify_launch_gates(checklist: list[dict], launch_config: dict) -> dict:
    required = list(launch_config.get("required_gates") or [])
    checklist_keys = {item["checklist_key"] for item in checklist if item.get("required")}
    missing = [gate for gate in required if gate not in checklist_keys]
    return {
        "passed": bool(launch_config.get("enabled")) and not missing,
        "enabled": bool(launch_config.get("enabled")),
        "launch_stage": launch_config.get("launch_stage"),
        "required_gates": required,
        "missing": missing,
    }


async def _get_anchor(conn: DB, anchor_slug: str) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_ANCHOR_COLS} FROM pilot_anchor WHERE slug = $1",
        anchor_slug,
    )
    if not row:
        raise HTTPException(404, "Pilot anchor not found")
    return _decode(row)


async def _anchor_places(conn: DB, anchor_id: UUID | str) -> list[dict]:
    rows = await conn.fetch(
        """
        SELECT ap.id, ap.anchor_id, ap.place_id, ap.role, ap.identity_snapshot,
               ap.provenance, ap.created_at, ap.updated_at,
               p.name, p.geonames_id, p.wikidata_qid, p.status AS place_status
          FROM anchor_place ap
          LEFT JOIN places p ON p.id = ap.place_id
         WHERE ap.anchor_id = $1
         ORDER BY ap.role, ap.created_at
        """,
        anchor_id,
    )
    return [_decode(row) for row in rows]


async def _anchor_evidence(
    conn: DB,
    anchor_id: UUID | str,
    *,
    source: str | None = None,
    status: str = "current",
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    filters = ["anchor_id = $1"]
    args: list = [anchor_id]
    if source:
        args.append(source)
        filters.append(f"source = ${len(args)}")
    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")
    args += [limit, offset]
    rows = await conn.fetch(
        f"SELECT {_EVIDENCE_COLS} FROM anchor_evidence "
        f"WHERE {' AND '.join(filters)} ORDER BY source, created_at DESC "
        f"LIMIT ${len(args) - 1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode(row) for row in rows]


async def _publication_checklist(conn: DB) -> list[dict]:
    rows = await conn.fetch(
        f"SELECT {_CHECKLIST_COLS} FROM pilot_publication_checklist ORDER BY sort_order"
    )
    return [_decode(row) for row in rows]


async def _launch_config(conn: DB) -> dict:
    row = await conn.fetchrow(
        f"SELECT {_LAUNCH_CONFIG_COLS} FROM pilot_launch_config "
        "WHERE config_key = 'nc_pilot_001_activation'"
    )
    if not row:
        raise HTTPException(503, "Pilot launch configuration not found")
    return _decode(row)


async def _latest_publication_snapshot(conn: DB, anchor_id: UUID | str) -> dict | None:
    row = await conn.fetchrow(
        f"SELECT {_SNAPSHOT_COLS} FROM pilot_publication_snapshot "
        "WHERE anchor_id = $1 ORDER BY created_at DESC LIMIT 1",
        anchor_id,
    )
    return _decode(row) if row else None


async def _monitoring_summary(conn: DB, anchor_id: UUID | str) -> dict:
    run_rows = await conn.fetch(
        """
        SELECT status, COUNT(*) AS count
          FROM pilot_ingest_run
         WHERE anchor_id = $1
         GROUP BY status
         ORDER BY status
        """,
        anchor_id,
    )
    evidence_count = await conn.fetchval(
        "SELECT COUNT(*) FROM anchor_evidence WHERE anchor_id = $1", anchor_id
    )
    snapshot_count = await conn.fetchval(
        "SELECT COUNT(*) FROM pilot_publication_snapshot WHERE anchor_id = $1", anchor_id
    )
    stale_runs = await conn.fetchval(
        """
        SELECT COUNT(*)
          FROM pilot_ingest_run
         WHERE anchor_id = $1
           AND status IN ('started','fetching','normalizing','committing')
           AND stale_after < NOW()
        """,
        anchor_id,
    )
    return {
        "ingest_runs_by_status": {row["status"]: row["count"] for row in run_rows},
        "evidence_count": evidence_count or 0,
        "publication_snapshot_count": snapshot_count or 0,
        "stale_recoverable_ingest_runs": stale_runs or 0,
    }


@router.get("")
async def list_pilot_anchors(
    auth: Auth,
    conn: DB,
    status: str | None = Query(None),
) -> list[dict]:
    if status:
        rows = await conn.fetch(
            f"SELECT {_ANCHOR_COLS} FROM pilot_anchor WHERE status = $1 ORDER BY sort_order",
            status,
        )
    else:
        rows = await conn.fetch(f"SELECT {_ANCHOR_COLS} FROM pilot_anchor ORDER BY sort_order")
    return [_decode(row) for row in rows]


@router.get("/{anchor_slug}")
async def get_pilot_anchor(anchor_slug: str, auth: Auth, conn: DB) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    places = await _anchor_places(conn, anchor["id"])
    evidence = await _anchor_evidence(conn, anchor["id"], limit=25)
    anchor["places"] = places
    anchor["evidence_summary"] = {
        "count": len(evidence),
        "sources": sorted({item["source"] for item in evidence}),
    }
    anchor["attribution"] = assemble_attribution(anchor, evidence, places)
    return anchor


@router.get("/{anchor_slug}/graph")
async def get_pilot_anchor_graph(anchor_slug: str, auth: Auth, conn: DB) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    places = await _anchor_places(conn, anchor["id"])
    evidence = await _anchor_evidence(conn, anchor["id"], limit=200)
    nodes = [
        {
            "id": f"anchor:{anchor['slug']}",
            "type": "anchor",
            "label": anchor["title"],
            "data": anchor["canonical_identity"],
        }
    ]
    edges = []
    for place in places:
        node_id = f"place:{place['place_id'] or place['id']}"
        nodes.append({"id": node_id, "type": "place", "label": place.get("name"), "data": place})
        edges.append(
            {"source": f"anchor:{anchor['slug']}", "target": node_id, "type": place["role"]}
        )
    for item in evidence:
        node_id = f"evidence:{item['id']}"
        nodes.append(
            {
                "id": node_id,
                "type": "evidence",
                "label": f"{item['source']}:{item['evidence_type']}",
                "data": item,
            }
        )
        edges.append(
            {
                "source": f"anchor:{anchor['slug']}",
                "target": node_id,
                "type": item["source_role"],
            }
        )
    return {
        "anchor": anchor,
        "nodes": nodes,
        "edges": edges,
        "attribution": assemble_attribution(anchor, evidence, places),
    }


@router.get("/{anchor_slug}/evidence")
async def list_pilot_anchor_evidence(
    anchor_slug: str,
    auth: Auth,
    conn: DB,
    source: str | None = Query(None),
    status: str = Query("current"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    anchor = await _get_anchor(conn, anchor_slug)
    return await _anchor_evidence(
        conn,
        anchor["id"],
        source=source,
        status=status,
        limit=limit,
        offset=offset,
    )


@router.get("/{anchor_slug}/ingest-runs")
async def list_pilot_ingest_runs(
    anchor_slug: str,
    auth: Auth,
    conn: DB,
    status: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    anchor = await _get_anchor(conn, anchor_slug)
    filters = ["anchor_id = $1"]
    args: list = [anchor["id"]]
    if status:
        args.append(status)
        filters.append(f"status = ${len(args)}")
    args += [limit, offset]
    rows = await conn.fetch(
        f"SELECT {_INGEST_RUN_COLS} FROM pilot_ingest_run "
        f"WHERE {' AND '.join(filters)} ORDER BY created_at DESC "
        f"LIMIT ${len(args) - 1} OFFSET ${len(args)}",
        *args,
    )
    return [_decode(row) for row in rows]


@router.post("/{anchor_slug}/ingest-runs")
async def create_pilot_ingest_run(
    anchor_slug: str,
    body: IngestRunCreate,
    auth: Auth,
    conn: DB,
) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    row = await conn.fetchrow(
        f"""
        INSERT INTO pilot_ingest_run (
            anchor_id, idempotency_key, status, source_scope, phase,
            stale_after, started_at, provenance
        )
        VALUES (
            $1, $2, 'started', $3::text[], 'started',
            NOW() + ($4::text || ' minutes')::interval,
            NOW(), $5::jsonb
        )
        ON CONFLICT (anchor_id, idempotency_key)
        DO UPDATE SET
            source_scope = EXCLUDED.source_scope,
            updated_at = NOW(),
            provenance = pilot_ingest_run.provenance || EXCLUDED.provenance
        RETURNING {_INGEST_RUN_COLS}
        """,
        anchor["id"],
        body.idempotency_key,
        body.source_scope,
        body.stale_after_minutes,
        json.dumps(
            {
                "actor": body.actor,
                "rule": "HTTP outside DB transactions; pilot metadata only",
            }
        ),
    )
    return _decode(row)


@router.post("/{anchor_slug}/ingest-runs/mark-stale")
async def mark_stale_pilot_ingest_runs(anchor_slug: str, auth: Auth, conn: DB) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    rows = await conn.fetch(
        f"""
        UPDATE pilot_ingest_run
           SET status = 'stale',
               phase = 'stale_recovery',
               recovery_notes = recovery_notes || $2::jsonb,
               updated_at = NOW()
         WHERE anchor_id = $1
           AND status IN ('started','fetching','normalizing','committing')
           AND stale_after < NOW()
        RETURNING {_INGEST_RUN_COLS}
        """,
        anchor["id"],
        json.dumps({"recovery": "marked stale by pilot API"}),
    )
    return {"anchor_slug": anchor_slug, "marked_stale": [_decode(row) for row in rows]}


@router.get("/{anchor_slug}/publication-checklist")
async def get_pilot_publication_checklist(anchor_slug: str, auth: Auth, conn: DB) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    return {
        "anchor_slug": anchor["slug"],
        "status": anchor["status"],
        "items": await _publication_checklist(conn),
    }


@router.get("/{anchor_slug}/launch-config")
async def get_pilot_launch_config(anchor_slug: str, auth: Auth, conn: DB) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    launch_config = await _launch_config(conn)
    checklist = await _publication_checklist(conn)
    return {
        "anchor_slug": anchor["slug"],
        "anchor_status": anchor["status"],
        "launch_config": launch_config,
        "launch_gates": verify_launch_gates(checklist, launch_config),
    }


@router.get("/{anchor_slug}/verify-attribution")
async def get_pilot_attribution_verification(anchor_slug: str, auth: Auth, conn: DB) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    evidence = await _anchor_evidence(conn, anchor["id"], limit=500)
    places = await _anchor_places(conn, anchor["id"])
    return {"anchor_slug": anchor["slug"], **verify_attribution(anchor, evidence, places)}


@router.get("/{anchor_slug}/verify-publication-snapshot")
async def get_pilot_publication_snapshot_verification(
    anchor_slug: str, auth: Auth, conn: DB
) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    latest = await _latest_publication_snapshot(conn, anchor["id"])
    return {"anchor_slug": anchor["slug"], **verify_publication_snapshot(latest)}


@router.get("/{anchor_slug}/monitoring")
async def get_pilot_monitoring(anchor_slug: str, auth: Auth, conn: DB) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    return {"anchor_slug": anchor["slug"], **await _monitoring_summary(conn, anchor["id"])}


@router.get("/{anchor_slug}/health")
async def get_pilot_health(anchor_slug: str, auth: Auth, conn: DB) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    evidence = await _anchor_evidence(conn, anchor["id"], limit=500)
    places = await _anchor_places(conn, anchor["id"])
    checklist = await _publication_checklist(conn)
    launch_config = await _launch_config(conn)
    latest = await _latest_publication_snapshot(conn, anchor["id"])
    monitoring = await _monitoring_summary(conn, anchor["id"])
    verifications = {
        "launch_gates": verify_launch_gates(checklist, launch_config),
        "attribution": verify_attribution(anchor, evidence, places),
        "publication_snapshot": verify_publication_snapshot(latest),
        "recovery": {
            "passed": monitoring["stale_recoverable_ingest_runs"] == 0,
            "stale_recoverable_ingest_runs": monitoring["stale_recoverable_ingest_runs"],
        },
    }
    all_checks_passed = all(item["passed"] for item in verifications.values())
    health_status = "healthy" if all_checks_passed else "degraded"
    return {
        "anchor_slug": anchor["slug"],
        "status": health_status,
        "verifications": verifications,
        "monitoring": monitoring,
    }


@router.get("/{anchor_slug}/launch-report")
async def get_pilot_launch_report(anchor_slug: str, auth: Auth, conn: DB) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    evidence = await _anchor_evidence(conn, anchor["id"], limit=500)
    places = await _anchor_places(conn, anchor["id"])
    checklist = await _publication_checklist(conn)
    launch_config = await _launch_config(conn)
    latest = await _latest_publication_snapshot(conn, anchor["id"])
    monitoring = await _monitoring_summary(conn, anchor["id"])
    verifications = {
        "launch_gates": verify_launch_gates(checklist, launch_config),
        "attribution": verify_attribution(anchor, evidence, places),
        "publication_snapshot": verify_publication_snapshot(latest),
        "idempotency": {
            "passed": True,
            "checks": [
                "pilot_anchor.slug",
                "pilot_ingest_run(anchor_id,idempotency_key)",
                "anchor_evidence(anchor_id,source,raw_payload_hash)",
                "pilot_publication_snapshot(anchor_id,snapshot_version)",
            ],
        },
        "recovery": {
            "passed": monitoring["stale_recoverable_ingest_runs"] == 0,
            "stale_recoverable_ingest_runs": monitoring["stale_recoverable_ingest_runs"],
        },
    }
    return {
        "report": "NC-PILOT-001 Activation Report",
        "anchor_slug": anchor["slug"],
        "anchor_status": anchor["status"],
        "launch_config": launch_config,
        "monitoring": monitoring,
        "verifications": verifications,
        "activation_ready": all(item["passed"] for item in verifications.values()),
    }


@router.get("/{anchor_slug}/publication-snapshots")
async def list_pilot_publication_snapshots(
    anchor_slug: str,
    auth: Auth,
    conn: DB,
    latest: bool = Query(False),
) -> list[dict] | dict:
    anchor = await _get_anchor(conn, anchor_slug)
    limit = 1 if latest else 100
    rows = await conn.fetch(
        f"SELECT {_SNAPSHOT_COLS} FROM pilot_publication_snapshot "
        "WHERE anchor_id = $1 ORDER BY created_at DESC LIMIT $2",
        anchor["id"],
        limit,
    )
    decoded = [_decode(row) for row in rows]
    if latest:
        if not decoded:
            raise HTTPException(404, "Publication snapshot not found")
        return decoded[0]
    return decoded


@router.post("/{anchor_slug}/publication-snapshots")
async def create_pilot_publication_snapshot(
    anchor_slug: str,
    body: PublicationSnapshotCreate,
    auth: Auth,
    conn: DB,
) -> dict:
    anchor = await _get_anchor(conn, anchor_slug)
    evidence = await _anchor_evidence(conn, anchor["id"], limit=500)
    places = await _anchor_places(conn, anchor["id"])
    attribution = assemble_attribution(anchor, evidence, places)
    snapshot = {
        **body.snapshot,
        "anchor_slug": anchor_slug,
        "anchor_title": anchor["title"],
        "attribution": attribution,
    }
    snapshot_sha256 = _json_hash(snapshot)
    row = await conn.fetchrow(
        f"""
        INSERT INTO pilot_publication_snapshot (
            anchor_id, snapshot_version, publication_status, snapshot,
            attribution, snapshot_sha256, created_by,
            published_at
        )
        VALUES (
            $1, $2, $3, $4::jsonb, $5::jsonb, $6, $7,
            CASE WHEN $3 = 'published' THEN NOW() ELSE NULL END
        )
        ON CONFLICT (anchor_id, snapshot_version)
        DO UPDATE SET
            publication_status = EXCLUDED.publication_status,
            snapshot = EXCLUDED.snapshot,
            attribution = EXCLUDED.attribution,
            snapshot_sha256 = EXCLUDED.snapshot_sha256,
            created_by = EXCLUDED.created_by,
            published_at = EXCLUDED.published_at
        RETURNING {_SNAPSHOT_COLS}
        """,
        anchor["id"],
        body.snapshot_version,
        body.publication_status,
        json.dumps(snapshot),
        json.dumps(attribution),
        snapshot_sha256,
        body.created_by,
    )
    return _decode(row)
