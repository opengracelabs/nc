# Capability: Ingestion

## Mission

Fetch, validate, store, and register all source materials for approved discovery candidates. Ingestion transforms an approved candidate into a durable evidence record: artifacts in MinIO, metadata in PostgreSQL, provenance intact.

---

## Strategy

- **Trigger-driven:** Ingestion runs in response to `DiscoveryCandidateApproved` events — never speculatively.
- **Artifact-first:** Raw source materials are written to MinIO before any parsing or normalization begins. Evidence is never lost to a processing failure.
- **Incremental:** Re-ingestion of an existing record fetches only changed or missing artifacts, verified by checksum.
- **Source hierarchy:** For each site, ingest in priority order — UNESCO WHC official record → Wikidata → supplementary sources (OSM, GeoNames, GBIF).

---

## Standards

| Standard | Application |
|---|---|
| PREMIS | Preservation metadata for every artifact stored in MinIO |
| PROV-O | Lineage from source URL to ingested record |
| Wikidata | Entity linking on all ingested records |
| Darwin Core | Mandatory for biodiversity and occurrence artifacts |
| CIDOC CRM | Object and event modeling for cultural heritage materials |
| SKOS | Controlled vocabulary for artifact type classification |
| ISO 8601 | All date fields |
| ISO 3166 | Country codes |

---

## Workflow

```
1. Trigger         — DiscoveryCandidateApproved event received
2. Resolve         — load approved candidate from PostgreSQL
3. Plan            — determine artifact set to fetch (URLs, formats, expected types)
4. Fetch           — download all artifacts (HTML, JSON, PDF, images, GeoJSON)
5. Store raw       — write to MinIO raw/ingestion/{site_id}/{ingest_id}/
6. Validate        — checksum, MIME type, size, schema conformance
7. Normalize       — parse and map to canonical schemas
8. Store normalized — write to MinIO normalized/ingestion/{site_id}/{ingest_id}/
9. Preserve        — create PREMIS Object record in PostgreSQL for each artifact
10. Register       — write ingested_record to PostgreSQL (status: staged)
11. Emit           — IngestionCompleted event
12. Review         — human confirms or flags in Mission Control (for flagged artifact types)
13. Activate       — status set to active; downstream workers notified
```

---

## Data

### Source Artifacts

| Artifact | Source | Format |
|---|---|---|
| Site description | UNESCO WHC | HTML / JSON |
| Outstanding Universal Value statement | UNESCO WHC | HTML / PDF |
| Boundary geometry | OSM / WHC | GeoJSON |
| Images | Wikimedia Commons | JPEG / PNG |
| Bibliographic references | Wikidata | JSON-LD |
| Species occurrence records | GBIF | Darwin Core / CSV |
| Nomination dossier | UNESCO WHC | PDF |

### Canonical Fields (ingested_records)

| Field | Type | Description |
|---|---|---|
| `id` | UUID | generated |
| `candidate_id` | UUID | FK → discovery_candidates |
| `site_id` | UUID | FK → sites (canonical) |
| `ingest_id` | text | unique run identifier |
| `source` | text | `unesco_whc`, `wikidata`, `osm`, etc. |
| `status` | text | `staged`, `active`, `failed`, `superseded` |
| `artifact_count` | int | total artifacts fetched |
| `checksum_manifest` | jsonb | `{path: sha256}` |
| `provenance` | jsonb | PROV-O lineage |
| `ingested_at` | timestamptz | |
| `activated_at` | timestamptz | |
| `schema_version` | text | version of canonical schema applied |

### Storage Layout

```
MinIO
├── raw/ingestion/{site_id}/{ingest_id}/
│   ├── unesco_whc_record.json
│   ├── ouv_statement.html
│   ├── boundary.geojson
│   └── images/
└── normalized/ingestion/{site_id}/{ingest_id}/
    ├── record.json          ← canonical schema
    ├── geometry.geojson
    └── occurrences.jsonl    ← Darwin Core, one record per line
```

---

## Institutional Sources

Sources are registered in the source registry with a priority rank, fetch strategy, and rate limit profile. The ingestion worker selects sources per candidate based on the approved candidate's `source` field and the site type.

| Institution | Source ID | Coverage | Fetch Strategy | Auth |
|---|---|---|---|---|
| UNESCO World Heritage Centre | `unesco_whc` | ~1,200 inscribed sites | REST API + HTML scrape | API key |
| UNESCO Intangible Cultural Heritage | `unesco_ich` | ~700 ICH elements | REST API | API key |
| Wikidata | `wikidata` | All WHC/ICH entities | SPARQL + Entity API | None (User-Agent) |
| Wikimedia Commons | `wikimedia_commons` | Images for all sites | MediaWiki API | None (User-Agent) |
| OpenStreetMap | `osm` | Boundary geometry | Overpass API | None |
| GeoNames | `geonames` | Place hierarchy | REST API | API key |
| GBIF | `gbif` | Species occurrences at sites | REST API | None (registered) |
| IUCN Red List | `iucn` | Threatened species per site | REST API | API key |
| Europeana | `europeana` | Cultural heritage objects | REST API | API key |

**Source priority per site record:**
```
1. UNESCO WHC / ICH    ← authoritative institution
2. Wikidata            ← linked data reconciliation
3. OSM                 ← geometry
4. GeoNames            ← place hierarchy
5. GBIF / IUCN         ← biodiversity overlay
6. Wikimedia Commons   ← media
7. Europeana           ← supplementary objects
```

---

## API Retrieval

API retrieval covers all sources that expose a structured REST or SPARQL endpoint.

### Protocol

```python
class APISource:
    base_url: str
    auth: AuthConfig          # api_key | oauth | none
    rate_limit: RateLimit     # requests/second, burst
    timeout_seconds: int
    retry_max: int
    retry_backoff: str        # exponential | fixed
    pagination: PaginationConfig | None
```

### Fetch rules

- All requests include a `User-Agent: NatureAndCulture/1.0 (opengracelabs@protonmail.com)` header.
- Responses are written to MinIO raw path immediately upon receipt — before any parsing.
- HTTP 429 or 503 triggers exponential backoff starting at 5s, max 5 retries.
- HTTP 404 is recorded as `artifact_status: missing` on the PREMIS record — not a worker failure.
- Paginated responses are concatenated into a single raw artifact per source per run.
- All API responses include the response headers in a sidecar `{artifact}.headers.json` file.

### Per-source notes

| Source | Endpoint pattern | Pagination | Notes |
|---|---|---|---|
| UNESCO WHC | `/api/v2/sites/{id}` | None per site | Bulk list at `/api/v2/sites/` |
| Wikidata SPARQL | `query.wikidata.org/sparql` | `LIMIT/OFFSET` | 60s timeout; chunk by 500 |
| Wikidata Entity | `www.wikidata.org/wiki/Special:EntityData/{QID}.json` | None | Prefer JSON-LD |
| OSM Overpass | `overpass-api.de/api/interpreter` | None | Relation query by OSM ID |
| GBIF | `api.gbif.org/v1/occurrence/search` | `offset/limit` | Max 300 per page |
| GeoNames | `api.geonames.org/getJSON` | None | |

---

## File Retrieval

File retrieval covers artifacts delivered as binary files — PDFs, images, bulk data exports — that cannot be accessed through a structured API call.

### Protocol

```python
class FileSource:
    url: str
    expected_mime: str
    expected_size_max_bytes: int
    stream: bool              # True for large files (PDF, zip)
    checksum_expected: str | None
```

### Fetch rules

- Files are streamed directly to MinIO; never fully buffered in worker memory for artifacts > 10 MB.
- MIME type is validated against `Content-Type` header before storage begins.
- File size is checked against `Content-Length` header; abort if `expected_size_max_bytes` exceeded.
- SHA-256 checksum computed during streaming; mismatch triggers quarantine.
- On re-ingestion, existing checksum is compared before re-downloading — skip if identical.

### Artifact size limits

| Artifact type | Max size | On exceed |
|---|---|---|
| JSON / JSON-LD | 50 MB | Quarantine + alert |
| GeoJSON geometry | 200 MB | Quarantine + alert |
| HTML page | 5 MB | Truncate + flag |
| PDF (nomination dossier) | 500 MB | Stream; flag for sensitivity review |
| Image (JPEG / PNG) | 50 MB | Quarantine + alert |
| CSV / JSONL (occurrences) | 1 GB | Stream in chunks |

### Known file sources

| Source | Artifact | URL pattern |
|---|---|---|
| UNESCO WHC | Nomination dossier PDF | `whc.unesco.org/document/{doc_id}` |
| UNESCO WHC | OUV statement PDF | `whc.unesco.org/document/{doc_id}` |
| Wikimedia Commons | Site image | `upload.wikimedia.org/...` |
| GBIF | Occurrence export | DwC-A zip via occurrence download API |

---

## Validation

Validation runs after raw storage and before normalization. A failed validation sets `artifact_status: invalid` on the PREMIS record and halts normalization for that artifact without failing the entire ingestion run.

### Checks

| Check | Applies To | Failure Action |
|---|---|---|
| MIME type match | All | Quarantine artifact |
| SHA-256 integrity | All | Quarantine artifact |
| Size within limit | All | Quarantine artifact |
| JSON parseable | JSON / JSON-LD | Quarantine artifact |
| Required fields present | JSON / JSON-LD | Flag for review |
| GeoJSON valid geometry | GeoJSON | Flag for review |
| Darwin Core required terms | CSV / JSONL | Flag for review |
| PDF not password-protected | PDF | Flag for review |
| Image not corrupt | JPEG / PNG | Quarantine artifact |
| Encoding is UTF-8 | HTML / JSON / CSV | Attempt re-encoding; flag on failure |

### Schema validation

Each source has a pinned JSON Schema or Pydantic model at `schemas/core/sources/{source_id}_v{n}.json`. Validation runs the raw artifact against the pinned schema. Unknown fields are logged but do not fail validation. Missing required fields produce a `validation_warning` on the PREMIS record.

### Quarantine

Quarantined artifacts are written to MinIO at `raw/quarantine/{site_id}/{ingest_id}/` and surfaced in Mission Control. The ingestion run continues for remaining artifacts.

---

## Normalization

Normalization maps validated raw artifacts to the canonical schemas defined in `schemas/`. Normalization is source-specific and schema-version-pinned.

### Principles

- Normalization is a pure transformation: same input always produces same output.
- All field mappings are explicit — no implicit inference or AI inference at this stage.
- Missing optional fields are omitted; missing required fields produce a `normalization_warning`.
- Multilingual fields are stored as `{lang_code: value}` objects (ISO 639-1).
- All identifiers are normalized to their canonical form (QID stripped of prefix, OSM ID as integer).

### Per-source mapping summary

**UNESCO WHC JSON → `schemas/core/site.py`**
| Source field | Canonical field | Transform |
|---|---|---|
| `id_number` | `source_id` | string |
| `site` | `name.en` | strip whitespace |
| `short_description` | `description.en` | strip HTML tags |
| `date_inscribed` | `inscription_year` | extract year (ISO 8601) |
| `criteria_txt` | `ouv_criteria` | parse `(i)(ii)` → `["i","ii"]` |
| `longitude` / `latitude` | `centroid` | WGS84 Point GeoJSON |
| `states_parties` | `country_codes` | map name → ISO 3166-1 |
| `category` | `heritage_type` | `Cultural` / `Natural` / `Mixed` |

**Wikidata Entity JSON → `schemas/core/entity_links.py`**
| Source field | Canonical field | Transform |
|---|---|---|
| `id` | `wikidata_qid` | `Q12345` |
| `labels` | `name` | `{lang: value}` |
| `descriptions` | `description` | `{lang: value}` |
| `claims.P625` | `centroid` | coordinate → GeoJSON Point |
| `claims.P17` | `country_codes` | QID → ISO 3166-1 via lookup |

**OSM Overpass → `schemas/core/geometry.py`**
| Source field | Canonical field | Transform |
|---|---|---|
| `elements[0].geometry` | `boundary` | relation → GeoJSON Polygon/MultiPolygon |
| `elements[0].tags.name` | `osm_name` | string |
| `elements[0].id` | `osm_relation_id` | integer |

**GBIF Occurrence → `schemas/core/occurrence.py`** (Darwin Core pass-through)
| DwC term | Canonical field | Transform |
|---|---|---|
| `scientificName` | `scientific_name` | string |
| `taxonRank` | `taxon_rank` | lowercase |
| `decimalLatitude/Longitude` | `location` | GeoJSON Point |
| `eventDate` | `observed_at` | ISO 8601 |
| `occurrenceStatus` | `occurrence_status` | `present` / `absent` |

### Output

Normalized artifacts are written to MinIO `normalized/ingestion/{site_id}/{ingest_id}/` as:
- `record.json` — canonical site record (JSON)
- `geometry.geojson` — boundary geometry
- `entity_links.json` — Wikidata / GeoNames / OSM identifiers
- `occurrences.jsonl` — one Darwin Core occurrence per line

---

## Governance

- Ingestion is only triggered by an approved candidate — no ingestion without human discovery approval.
- Artifacts containing personal data (nomination dossiers with author names) require a data-sensitivity review before activation.
- Re-ingestion of an active record creates a new `ingest_id` and sets the previous record to `superseded` — no destructive overwrite.
- Failed ingestions are quarantined in `status: failed` and surfaced in Mission Control for triage.
- Bulk activation is permitted for low-risk artifact types (structured JSON, GeoJSON) when checksums pass.

---

## API

```
POST   /ingestion/runs                      Manually trigger ingestion for a candidate
GET    /ingestion/runs/{ingest_id}          Run status and artifact manifest
GET    /ingestion/records                   List ingested records (filterable by status, site, source)
GET    /ingestion/records/{id}              Record detail with artifact manifest
PATCH  /ingestion/records/{id}             Activate / flag / quarantine
GET    /ingestion/records/{id}/artifacts    List artifacts with MinIO paths and checksums
GET    /ingestion/records/{id}/provenance   PROV-O provenance chain
```

---

## Worker

**Name:** `ingestion_worker`
**Location:** `workers/ingestion_worker/`

Responsibilities:
- Subscribe to `DiscoveryCandidateApproved` events.
- Execute fetch → validate → normalize → preserve pipeline.
- Write all artifacts to MinIO before touching PostgreSQL.
- Create PREMIS Object records for every artifact.
- Emit `IngestionCompleted` or `IngestionFailed` on conclusion.
- Idempotent: re-running with the same `ingest_id` skips already-fetched artifacts (checksum match).

Configuration:
```
INGESTION_CONCURRENCY=4
FETCH_TIMEOUT_SECONDS=30
FETCH_RETRY_MAX=3
MINIO_BUCKET_RAW=nc-raw
MINIO_BUCKET_NORMALIZED=nc-normalized
POSTGRES_DSN=...
UNESCO_API_KEY=...
WIKIMEDIA_USER_AGENT=NatureAndCulture/1.0
```

---

## Agent

**Roles:**
- **Schema mapping assistance:** Suggest field mappings when source structure deviates from canonical schema.
- **Artifact classification:** Identify artifact type (OUV statement, nomination dossier, occurrence record) when MIME type or filename is ambiguous.
- **Quality flagging:** Surface artifacts with low information density, broken encoding, or apparent truncation.
- **Translation advisory:** Flag non-English artifacts for the translation capability; suggest primary language.

**Constraints:**
- Agent outputs stored as `agent_notes` on the artifact PREMIS record.
- No agent suggestion modifies stored artifact content.
- All agent calls logged with model version and response hash.

---

## Events

| Event | Emitted By | Consumed By |
|---|---|---|
| `IngestionRunStarted` | ingestion_worker | mission_control |
| `IngestionArtifactFetched` | ingestion_worker | mission_control |
| `IngestionArtifactFailed` | ingestion_worker | mission_control, alerting |
| `IngestionCompleted` | ingestion_worker | mission_control |
| `IngestionFailed` | ingestion_worker | mission_control, alerting |
| `IngestionRecordActivated` | api | preservation_worker, knowledge_worker, search_worker |
| `IngestionRecordSuperseded` | api | knowledge_worker, search_worker |

---

## Metrics

| Metric | Description |
|---|---|
| `ingestion.run.duration_seconds` | Time per full ingestion run |
| `ingestion.artifacts.fetched` | Artifacts fetched per run |
| `ingestion.artifacts.failed` | Fetch failures per run |
| `ingestion.artifacts.size_bytes_p50/p95` | Artifact size distribution |
| `ingestion.checksum.mismatch_rate` | Re-ingestion checksum failures |
| `ingestion.records.activation_lag_hours` | Time from completion to human activation |
| `ingestion.source.fetch_error_rate` | Failures by source |
| `ingestion.normalization.schema_error_rate` | Records failing canonical schema validation |

---

## Risk

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Source URL changed or removed | Medium | Medium | Store raw immediately; flag dead URLs in Mission Control |
| Artifact too large (PDF dossiers) | Medium | Low | Size cap per artifact; stream to MinIO without full buffering |
| Source rate limiting | High | Low | Per-source rate limiter with exponential backoff |
| Normalization schema drift | Low | High | Schema versioning; validation against pinned schema version |
| Duplicate artifact storage | Medium | Low | Checksum deduplication; hard-link in MinIO manifest |
| Personal data in dossiers | Medium | High | Sensitivity review gate before activation |
| Corrupt or truncated artifact | Low | Medium | Checksum + size validation; quarantine on failure |

---

## Pseudocode

```python
def run_ingestion(candidate_id: str, ingest_id: str):
    candidate = load_candidate(candidate_id)
    plan = build_artifact_plan(candidate)               # determine URLs and expected types

    artifacts = []
    for item in plan:
        raw = fetch_with_retry(item.url)
        path = store_raw(ingest_id, candidate.site_id, item.name, raw)
        checksum = sha256(raw)

        validate(raw, item.expected_mime, item.expected_schema)

        normalized = normalize(item.type, raw)
        norm_path = store_normalized(ingest_id, candidate.site_id, item.name, normalized)

        premis = create_premis_object(
            path=path, checksum=checksum, mime=item.mime,
            agent_notes=agent_classify(item, raw)
        )
        artifacts.append(premis)

    record = register_ingested_record(candidate_id, ingest_id, artifacts)
    emit(IngestionCompleted, ingest_id, record.id)
```

---

## Tests

### Unit
- `build_artifact_plan()` produces correct URL set for each source type
- `normalize()` maps UNESCO JSON fields to canonical schema without data loss
- `validate()` rejects mismatched MIME types and oversized artifacts
- `create_premis_object()` produces valid PREMIS structure

### Integration
- Full ingestion of a fixture candidate writes expected artifacts to MinIO and records to PostgreSQL
- Re-ingestion with same `ingest_id` skips artifacts whose checksums match (idempotency)
- Re-ingestion with new `ingest_id` creates new record, sets previous to `superseded`

### Workflow
- `IngestionCompleted` → human activation → `IngestionRecordActivated` emitted to downstream workers
- Failed artifact quarantine surfaces correctly in Mission Control

### Replay
- Stored raw MinIO fixtures can be re-normalized without network calls
- Replay produces byte-identical normalized artifacts (determinism)

---

## Implementation

### Phase 1 (UNESCO WHC)
1. `workers/ingestion_worker/sources/unesco_whc.py` — fetch and artifact plan for WHC records
2. `workers/ingestion_worker/sources/wikimedia.py` — image fetch from Commons
3. `workers/ingestion_worker/fetch.py` — rate-limited HTTP client with retry
4. `workers/ingestion_worker/validate.py` — MIME, size, schema validation
5. `workers/ingestion_worker/normalize.py` — canonical field mapping per source
6. `workers/ingestion_worker/preserve.py` — PREMIS Object creation
7. `workers/ingestion_worker/main.py` — event-driven orchestration loop
8. `services/ingestion/` — FastAPI routes
9. `schemas/core/ingested_record.py` — Pydantic schema

### Phase 2
- Darwin Core normalization for GBIF occurrence records.
- PDF text extraction pipeline for nomination dossiers.

---

## Operations

**Manually trigger ingestion:**
```bash
curl -X POST https://api.nc.internal/ingestion/runs \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"candidate_id": "<uuid>"}'
```

**Check staged records awaiting activation:**
```bash
psql $POSTGRES_DSN -c \
  "SELECT count(*) FROM ingested_records WHERE status = 'staged';"
```

**Inspect artifact manifest for a record:**
```bash
curl https://api.nc.internal/ingestion/records/{id}/artifacts \
  -H "Authorization: Bearer $TOKEN"
```

**Re-ingest a failed record:**
```bash
curl -X POST https://api.nc.internal/ingestion/runs \
  -d '{"candidate_id": "<uuid>", "force": true}'
```

---

## Improvement

- Streaming ingestion for large PDFs to avoid memory pressure.
- Per-source schema version tracking so normalization logic can be pinned and upgraded independently.
- Automated sensitivity classifier for personal data detection in dossier artifacts.
- Artifact deduplication across sites (shared images, common reference documents).
- Delta ingestion: detect and fetch only changed fields on re-discovery without full re-fetch.

---

## Continuity

- Ingestion worker is stateless; any crash can be retried without data loss — raw artifacts in MinIO are written before PostgreSQL records.
- MinIO raw artifacts are the authoritative replay source; normalization can be re-run without re-fetching.
- PREMIS records ensure every artifact's provenance and integrity is permanently documented.
- Failed ingestions do not block the queue; each candidate is processed independently.
- If a source changes its schema, pinned schema versions allow historical records to remain valid while new records adopt the updated mapping.
- All ingestion history retained in PostgreSQL for audit, replay, and lineage queries.
