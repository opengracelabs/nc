# Capability: Discovery

## Mission

Systematically locate, identify, and register cultural and ecological records from authoritative external sources. Discovery produces candidate records in PostgreSQL for human review before any downstream processing begins.

---

## Strategy

- **Phase 1 — UNESCO World Heritage Sites:** Harvest all ~1,200 inscribed sites via the UNESCO API and Wikidata SPARQL. Establish the canonical site registry.
- **Phase 2 — UNESCO Intangible Cultural Heritage:** Extend to ICH elements across all Convention categories.
- **Phase 3 — Biodiversity overlay:** Cross-reference sites with GBIF, IUCN Red List, and Darwin Core occurrence sources.
- **Ongoing:** Scheduled re-discovery runs detect new inscriptions, boundary revisions, and status changes.

Discovery never writes final records. It writes candidates. Humans approve.

---

## Standards

| Standard | Application |
|---|---|
| Wikidata | Entity reconciliation and QID assignment |
| GeoNames | Place name normalization and geographic hierarchy |
| OpenStreetMap | Boundary geometry source |
| SKOS | Category and heritage type vocabulary |
| CIDOC CRM | Event modeling (inscription, nomination, revision) |
| PROV-O | Lineage from source URL to candidate record |
| ISO 8601 | All date fields |
| ISO 3166 | Country codes on site records |
| UNESCO WHC | Outstanding Universal Value criteria (i–x) |

---

## Workflow

```
1. Trigger         — scheduled cron or manual API call
2. Fetch           — pull source index (UNESCO API / Wikidata SPARQL)
3. Normalize       — map source fields to canonical schema
4. Deduplicate     — match against existing records by QID / site ID
5. Enrich          — resolve GeoNames, OSM geometry, Wikidata labels
6. Score           — completeness and confidence scoring
7. Stage           — write candidate to discovery_candidates table (status: pending)
8. Notify          — emit DiscoveryCandidateCreated event
9. Review          — human approves, rejects, or flags in Mission Control
10. Promote        — approved candidates written to canonical sites table
```

---

## Data

### Source

- UNESCO World Heritage API: `https://whc.unesco.org/en/list/`
- Wikidata SPARQL endpoint for `Q9259` (World Heritage Site) subclasses

### Canonical Fields (discovery_candidates)

| Field | Type | Source |
|---|---|---|
| `id` | UUID | generated |
| `source` | text | `unesco_whc`, `wikidata`, etc. |
| `source_id` | text | site ID or QID at source |
| `wikidata_qid` | text | Wikidata reconciliation |
| `name` | jsonb | `{lang: label}` multilingual |
| `country_codes` | text[] | ISO 3166-1 alpha-2 |
| `inscription_year` | int | WHC record |
| `ouv_criteria` | text[] | `["i","ii","vii"]` |
| `geometry` | geometry | OSM / WHC boundary |
| `confidence_score` | float | 0.0–1.0 |
| `status` | text | `pending`, `approved`, `rejected`, `flagged` |
| `provenance` | jsonb | PROV-O lineage |
| `discovered_at` | timestamptz | pipeline run timestamp |
| `reviewed_by` | text | human reviewer |
| `reviewed_at` | timestamptz | approval timestamp |

### Storage

- Candidates: PostgreSQL `discovery_candidates`
- Raw source responses: MinIO `raw/discovery/{source}/{run_id}/`
- Normalized payloads: MinIO `normalized/discovery/{source}/{run_id}/`

---

## Governance

- No candidate is promoted to canonical without human approval.
- Bulk approval is permitted only for high-confidence batches (score ≥ 0.95) with supervisor sign-off.
- Rejections require a reason code (duplicate, out-of-scope, data-quality, policy).
- All approval actions are logged with reviewer identity and timestamp.
- Re-discovery runs on existing approved sites produce a revision candidate, not an overwrite.

---

## API

All endpoints require authentication. Discovery is triggered and reviewed through the FastAPI governance gateway.

```
POST   /discovery/runs                  Trigger a discovery run
GET    /discovery/runs/{run_id}         Run status and summary
GET    /discovery/candidates            List candidates (filterable by status, source, country)
GET    /discovery/candidates/{id}       Candidate detail
PATCH  /discovery/candidates/{id}       Approve / reject / flag
POST   /discovery/candidates/{id}/promote  Promote approved candidate to canonical
```

---

## Worker

**Name:** `discovery_worker`
**Location:** `workers/discovery_worker/`

Responsibilities:
- Poll the `discovery_runs` queue (PostgreSQL-backed via pgqueue or Redis).
- Execute fetch → normalize → deduplicate → enrich → score pipeline.
- Write candidates and provenance to PostgreSQL.
- Store raw and normalized artifacts to MinIO.
- Emit events on completion or failure.
- Idempotent: re-running the same source + run_id produces no duplicate candidates.

Configuration (via environment):
```
DISCOVERY_SOURCES=unesco_whc,wikidata
DISCOVERY_SCHEDULE=0 2 * * 0        # weekly, Sunday 02:00 UTC
UNESCO_API_KEY=...
WIKIDATA_SPARQL_ENDPOINT=https://query.wikidata.org/sparql
MINIO_BUCKET_RAW=nc-raw
POSTGRES_DSN=...
```

---

## Agent

The AI advisory layer assists discovery but never writes directly to PostgreSQL.

**Roles:**
- **Reconciliation assistance:** Suggest Wikidata QID matches when automated reconciliation is ambiguous.
- **Name normalization:** Propose canonical names for multilingual records.
- **Completeness scoring:** Flag fields likely to be missing or incorrect based on source patterns.
- **Anomaly flagging:** Surface candidates that appear to be duplicates or out-of-scope for human review.

**Constraints:**
- Agent outputs are stored as `agent_suggestions` (jsonb) on the candidate record.
- No agent suggestion is applied without human confirmation.
- All agent calls logged with model version, prompt hash, and response.

---

## Events

| Event | Emitted By | Consumed By |
|---|---|---|
| `DiscoveryRunStarted` | discovery_worker | mission_control |
| `DiscoveryRunCompleted` | discovery_worker | mission_control, ingestion_worker |
| `DiscoveryRunFailed` | discovery_worker | mission_control, alerting |
| `DiscoveryCandidateCreated` | discovery_worker | mission_control |
| `DiscoveryCandidateApproved` | api | ingestion_worker |
| `DiscoveryCandidateRejected` | api | mission_control |
| `DiscoveryCandidatePromoted` | api | search_worker, knowledge_worker |

---

## Metrics

| Metric | Description |
|---|---|
| `discovery.run.duration_seconds` | Time per full discovery run |
| `discovery.candidates.created` | New candidates per run |
| `discovery.candidates.duplicate_rate` | Fraction matched to existing records |
| `discovery.candidates.approval_rate` | Fraction approved by humans |
| `discovery.candidates.confidence_score_p50/p95` | Score distribution |
| `discovery.candidates.pending_age_hours` | How long candidates wait for review |
| `discovery.source.fetch_errors` | Fetch failures by source |
| `discovery.enrichment.wikidata_hit_rate` | Successful QID resolution rate |

---

## Risk

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| UNESCO API unavailable | Medium | Low | Retry with backoff; fallback to Wikidata SPARQL |
| Wikidata SPARQL timeout | High | Low | Paginate queries; cache results in MinIO |
| Duplicate candidate explosion | Medium | Medium | Deduplication by QID + source_id before insert |
| Human review bottleneck | Medium | High | Bulk approval workflow for high-confidence batches |
| Schema drift at source | Low | High | Schema validation at fetch; alert on unknown fields |
| AI reconciliation hallucination | Medium | Medium | Agent suggestions require human confirmation |

---

## Pseudocode

```python
def run_discovery(source: str, run_id: str):
    raw = fetch_source(source)                        # HTTP GET, store to MinIO raw/
    store_raw(run_id, source, raw)

    records = normalize(source, raw)                  # map to canonical fields
    store_normalized(run_id, source, records)

    for record in records:
        existing = lookup_by_qid_or_source_id(record)
        if existing and not changed(existing, record):
            continue                                  # no-op, already known

        record.confidence_score = score(record)
        record.provenance = build_provenance(source, run_id, record)
        record.agent_suggestions = agent_advisory(record)

        upsert_candidate(record, status="pending")
        emit(DiscoveryCandidateCreated, record.id)

    emit(DiscoveryRunCompleted, run_id, summary=stats())
```

---

## Tests

### Unit
- `normalize()` correctly maps all known UNESCO API fields
- `score()` returns expected confidence for complete vs. sparse records
- `deduplicate()` correctly matches on QID and source_id
- `build_provenance()` produces valid PROV-O structure

### Integration
- Full run against a fixture of 10 UNESCO records produces expected candidates in PostgreSQL
- MinIO artifacts written to correct bucket paths
- Duplicate run produces no new candidates (idempotency)

### Workflow
- Approve → promote flow writes to canonical sites table and emits `DiscoveryCandidatePromoted`
- Reject flow sets status, records reason, emits no downstream events

### Replay
- Stored raw MinIO fixture can be replayed through normalize → score without network calls
- Replayed run produces identical candidates (determinism)

---

## Implementation

### Phase 1 (UNESCO WHC)
1. `workers/discovery_worker/sources/unesco_whc.py` — fetch and parse WHC list
2. `workers/discovery_worker/sources/wikidata.py` — SPARQL reconciliation
3. `workers/discovery_worker/normalize.py` — canonical field mapping
4. `workers/discovery_worker/score.py` — completeness scoring
5. `workers/discovery_worker/main.py` — orchestration loop
6. `services/discovery/` — FastAPI routes for run management and candidate review
7. `schemas/core/discovery_candidate.py` — Pydantic schema

### Phase 2
- Add `sources/gbif.py`, `sources/iucn.py` following the same source interface.

---

## Operations

**Trigger a manual run:**
```bash
curl -X POST https://api.nc.internal/discovery/runs \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"source": "unesco_whc"}'
```

**Check pending candidates:**
```bash
psql $POSTGRES_DSN -c "SELECT count(*) FROM discovery_candidates WHERE status = 'pending';"
```

**Re-run failed run:**
```bash
curl -X POST https://api.nc.internal/discovery/runs \
  -d '{"source": "unesco_whc", "run_id": "<failed_run_id>", "force": true}'
```

---

## Improvement

- Add source connectors for IUCN Red List, GBIF, and Europeana.
- Confidence scoring model trained on historical approval/rejection decisions.
- Automated bulk approval pipeline for high-confidence, low-risk candidate batches.
- Webhook support: notify reviewers via email or Slack when pending candidates exceed threshold.
- Spatial deduplication: flag candidates whose geometry overlaps an existing approved site.

---

## Continuity

- Discovery worker is stateless; any failure can be retried without data loss.
- Raw artifacts in MinIO are the authoritative replay source — no re-fetching needed for re-processing.
- PostgreSQL `discovery_candidates` is the sole state store; no in-memory queues hold critical state.
- If the UNESCO API is deprecated, the Wikidata SPARQL source covers the same entity set.
- Weekly scheduled runs ensure the candidate pool stays current without manual intervention.
- All run history retained indefinitely in PostgreSQL for audit and replay.
