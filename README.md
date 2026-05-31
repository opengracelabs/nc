# Nature & Culture

> Preserve, model, discover, publish and activate humanity's cultural and ecological knowledge.

## Core Doctrine

| Layer | Role |
|---|---|
| PostgreSQL | Authority — source of truth for all state |
| MinIO | Evidence — raw and normalized artifacts |
| Workers | Execution — all async processing |
| FastAPI | Governance Gateway — the only API surface |
| Mission Control | Visibility — observability and queue dashboards |
| Humans | Approval — required for consequential actions |
| AI | Advisory — inference and enrichment, never authority |

## Initial Goal

**UNESCO Discovery → Search Pipeline**

Discover UNESCO World Heritage Sites and associated cultural/ecological records, ingest and preserve source materials, model knowledge relationships, and surface them through a governed search interface.

## Repository Structure

```
docs/           System documentation (capabilities, standards, architecture, decisions, runbooks)
schemas/        Canonical data schemas (core, governance, reality, semantic, knowledge, ...)
infrastructure/ Deployment configuration (Docker, Postgres, MinIO, Neo4j, monitoring, Tailscale)
services/       FastAPI service modules
workers/        Async background workers
data/           Raw → normalized → curated data pipeline
tests/          Unit, integration, workflow, and replay tests
observability/  Dashboards, alerts, and reports
mission_control/ Queue and operational dashboards
scripts/        Operational scripts
```

## Principles

- No worker writes to the API — all state flows through PostgreSQL.
- Every artifact stored in MinIO carries a provenance record in PostgreSQL.
- No AI output is persisted without a human approval step.
- All pipeline decisions are observable and replayable.
