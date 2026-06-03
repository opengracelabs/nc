# Nature & Culture

> A place-centered public-domain illustration discovery and commerce platform.

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

## Current Direction

Nature & Culture is not a biodiversity inventory system. It is a place-centered public-domain illustration discovery and commerce platform.

Nature & Culture is no longer building infrastructure. The platform foundation is in place; current work is Milestone 3 public-domain illustration opportunity discovery.

| Milestone | Focus | Status |
|---|---|---|
| 1 | UNESCO Pipeline | Complete |
| 2 | Knowledge Modeling | Complete |
| 2.1 | Knowledge Hardening | Complete |
| 3 | Taxon Discovery | Active |

Milestone 3 produces ranked public-domain illustration opportunities for a place. Taxa from GBIF and Wikidata are search handles for BHL targets, not the optimization goal. Commercial assets attach to concepts; places connect to concepts. The output is Illustration Opportunity, not Species.

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
