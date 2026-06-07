# Neo4j + pgvector Runtime Architecture v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Status | Architecture design only |
| Scope | Relationship Intelligence Runtime + Semantic Intelligence Runtime |
| Current stack | PostgreSQL, PostGIS, MinIO, Universal Media Substrate |
| Proposed derived layers | Neo4j, pgvector |
| Governing doctrine | `relationship_semantic_constitution_v1.0.md` |

## Executive Position

Neo4j and pgvector should be added only as projection runtimes.

They must not become authorities, write paths, scoring engines, or activation gates. The existing
stack remains authoritative:

```text
PostgreSQL  -> canonical state, replay state, IDs, governance, rights, catalog, commerce
PostGIS     -> canonical spatial geometry and spatial predicates
MinIO       -> canonical file evidence and media bytes
UMS M36     -> canonical source_item/media_file/media_rights/activation_target substrate
Neo4j       -> derived relationship traversal projection
pgvector    -> derived semantic similarity projection inside PostgreSQL
FastAPI     -> gateway that joins derived discovery signals back to PostgreSQL authority
```

Implementation is not authorized until the Strategic Direction amendment required by
`relationship_semantic_constitution_v1.0.md` is recorded. This document defines the runtime that
should be implemented after that gate, not an implementation approval.

## Runtime Goals

The runtime must support these discovery and enrichment behaviors without changing Commerce
Intelligence, Product Routing, Catalog, Publication, Asset Intelligence, or UMS M36:

- Multi-hop relationship discovery across places, media, creators, institutions, collections,
  subject terms, standards classifications, and activation targets.
- Semantic search and "similar to this" discovery across text-bearing source items, places,
  stories, collections, and future media transcripts or dataset metadata.
- Hybrid discovery that combines PostgreSQL filters, PostGIS geography, Neo4j traversal, and
  pgvector similarity while returning PostgreSQL IDs as the canonical result identity.
- Full rebuild of both derived layers from PostgreSQL and MinIO.
- Replayable advisory signals with projection schema, model, input hash, and run provenance.

The runtime must not:

- Accept writes from users, API endpoints, or downstream workers into Neo4j.
- Treat vector similarity as canonical classification.
- Feed graph or vector signals into commerce scoring without a Commerce Intelligence amendment.
- Store rights decisions, activation approvals, or product eligibility in Neo4j or pgvector as
  authorities.

## Reference Model Adoption

| Reference model | Adopt | Reject |
|---|---|---|
| Google Knowledge Graph | Entity-centered graph; stable IDs; typed relationships; fact traversal. | Autonomous fact extraction from the open web; opaque relationship authority. |
| Wikidata | Stable external IDs, aliases, `same_as` links, statement provenance, external federation posture. | Open-edit authority model; external edits changing NC truth. |
| Palantir Foundry | Versioned ontology, lineage on transforms, derived graph as operational ontology. | All-in-one platform authority; graph-based canonical writes. |
| Neo4j best practices | Explicit labels and relationship types, constraints, indexed stable keys, bulk rebuilds, directed edges, narrow relationship vocabulary. | Over-generic `RELATED_TO` edges; user-authored graph mutations; graph as source of truth. |
| PostgreSQL + pgvector | Vectors stored beside authoritative IDs, named vector spaces, model/version metadata, HNSW indexes, hybrid SQL filtering. | One global embedding table without space/model boundaries; unversioned embeddings. |

## Runtime Boundary

```text
Authoritative write path
------------------------
source institution / aggregator
  -> UMS M36 ingestion
  -> PostgreSQL canonical records
  -> MinIO canonical files
  -> Commerce / Catalog / Publication / Asset Intelligence

Derived discovery path
----------------------
PostgreSQL + PostGIS + MinIO
  -> projection queue
  -> relationship projection worker
  -> Neo4j graph
  -> relationship discovery API

PostgreSQL + MinIO
  -> embedding input worker
  -> embedding generation worker
  -> pgvector vector spaces
  -> semantic discovery API

Hybrid API
----------
FastAPI receives graph/vector candidates
  -> rehydrates every candidate from PostgreSQL
  -> filters by rights, activation, publication, visibility, and media type
  -> returns canonical PostgreSQL IDs with derived signal metadata
```

## Architecture Layers

| Layer | Runtime | Authority posture | Purpose |
|---|---|---|---|
| Canonical entity layer | PostgreSQL | Sole authority | Places, source items, media, rights, technical metadata, creators, collections, commerce, publication. |
| Spatial layer | PostGIS | Sole spatial authority | Geometry, containment, proximity, bounding boxes, map search. |
| Evidence layer | MinIO | File evidence authority | Master files, derivatives, manifests, transcripts, dataset packages. |
| Relationship projection layer | Neo4j | Derived | Multi-hop traversal and explainable relationship paths. |
| Semantic projection layer | pgvector | Derived | Similarity search over governed vector spaces. |
| Query gateway | FastAPI | Read orchestration only | Joins derived candidates to PostgreSQL canonical state. |
| Replay/audit layer | PostgreSQL | Sole audit authority | Projection runs, embedding runs, input hashes, model versions, query metadata. |

## 1. Projection Pipeline

### Relationship Projection

Neo4j is populated only from PostgreSQL rows and governed derivation rules.

```text
PostgreSQL authority tables
  -> projection_source_snapshot
  -> projection_run
  -> node upserts
  -> relationship upserts
  -> derived relationship computation
  -> projection_event
  -> validation counts/checksums
```

Projection stages:

1. Select eligible source rows from PostgreSQL.
2. Build a canonical projection snapshot with PostgreSQL table, row ID, status, visibility,
   rights posture, source hash, and schema version.
3. Validate every row against the active `projection_schema_registry`.
4. Upsert Neo4j nodes by immutable PostgreSQL identity key.
5. Upsert Neo4j relationships from direct PostgreSQL relationships.
6. Compute governed derived relationships from PostgreSQL and PostGIS, not from Neo4j alone.
7. Write a PostgreSQL `projection_event` row with counts, run ID, schema version, outcome,
   and worker identity.
8. Validate that every Neo4j node and edge has a PostgreSQL source or derivation rule.

Neo4j never creates novel relationships. Relationship inference is limited to rules registered in
PostgreSQL and ratified by governance.

### Semantic Projection

pgvector is populated from governed embedding inputs.

```text
PostgreSQL + MinIO source content
  -> embedding input materialization
  -> source_hash
  -> model registry validation
  -> embedding generation
  -> vector space write
  -> HNSW index refresh
  -> projection_event
```

Embedding stages:

1. Select eligible entities for each active vector space.
2. Materialize the governed input text or feature payload.
3. Compute SHA-256 `source_hash` for the input payload.
4. Confirm the active embedding model is registered and active.
5. Generate the embedding.
6. Store the vector with entity ID, table, space, model ID, model version, dimension,
   source hash, content language, rights visibility, and projected timestamp.
7. Refresh pgvector indexes for the active space.
8. Write `projection_event` and embedding run metadata.

No vector record is valid without a PostgreSQL entity ID and input hash.

## 2. Refresh Strategy

Refresh is incremental by default and full rebuild only by explicit trigger.

| Change source | Relationship refresh | Semantic refresh |
|---|---|---|
| `source_item.status -> activated` | Add `SourceItem`, media type, institution, place, creator, subject relationships. | Add eligible vector rows for active spaces. |
| `source_item.status -> retracted` | Remove node and dependent relationships. | Delete or deactivate vectors immediately. |
| `media_rights` change | Update visibility metadata and remove ineligible relationships if activation is retracted. | Deactivate vectors if public visibility or rights eligibility is lost. |
| `media_technical_metadata` subject change | Refresh subject term nodes and `TAGGED` relationships. | Rebuild source-item embedding when input hash changes. |
| `source_record` metadata change | Refresh source item and institution relationships if projected fields changed. | Rebuild embedding when normalized metadata input changes. |
| `places` geometry or status change | Refresh place node, `LOCATED_IN`, `PROXIMATE_TO`, and map discovery relationships. | Rebuild place embedding only if text input changes; spatial filters remain PostGIS. |
| `collection.status -> published` | Add collection node and membership relationships. | Add collection vector space row if active. |
| `collection.status -> retracted` | Remove collection projection. | Deactivate collection embeddings. |
| Embedding model activation | No graph impact. | Full rebuild of affected vector spaces. |
| Projection schema activation | Full Neo4j rebuild. | Rebuild only if vector input schema or schema version changes. |

Operational rules:

- Incremental refresh target: within 15 minutes of PostgreSQL change.
- Rights and visibility retractions are priority refreshes and should bypass ordinary queue order.
- Refresh workers record stale counts and oldest stale age in PostgreSQL.
- API responses must treat stale derived layers as advisory and recheck canonical PostgreSQL state
  before returning public results.

## 3. Rebuild Strategy

### Neo4j Full Rebuild

Neo4j rebuild is routine recovery and schema migration tooling.

```text
1. Record Director Decision authorizing rebuild.
2. Freeze graph projection writes except the rebuild worker.
3. Create rebuild run in PostgreSQL.
4. Clear or replace the active Neo4j graph namespace.
5. Bulk project nodes from PostgreSQL.
6. Bulk project direct relationships from PostgreSQL.
7. Compute governed derived relationships from PostgreSQL/PostGIS.
8. Validate counts, labels, relationship types, orphan checks, and source hashes.
9. Mark projection_event = full_rebuild/success.
10. Release graph discovery from degraded mode.
```

Preferred production pattern: build into a replacement graph database or schema namespace, verify,
then switch the active alias. If Community Edition deployment limits alias switching, use a
maintenance rebuild window with discovery degraded but canonical platform operations online.

### pgvector Full Rebuild

pgvector rebuild is per vector space and model version.

```text
1. Record Director Decision naming spaces, model, and reason.
2. Create new inactive vector space version.
3. Materialize all eligible embedding inputs.
4. Generate embeddings under the active model.
5. Build HNSW indexes.
6. Validate counts, dimensions, source hashes, and sample retrieval.
7. Switch active vector space version.
8. Retire old vector space version after replay retention expires.
```

The old vector space should remain queryable for audit until retention policy allows retirement,
but public discovery uses only the active vector space.

## 4. Replay Implications

Neo4j and pgvector outputs are replayable only as derived advisory signals.

Relationship replay:

- Every graph result used by a workflow must record query type, schema version, traversal depth,
  result count, projection run ID, and timestamp.
- Consequential decisions must be reproducible from PostgreSQL using equivalent SQL or recursive
  CTEs, because Neo4j is not the authority.
- Graph traversal may assist discovery but cannot be the sole replay source.

Semantic replay:

- Every semantic result must record vector space, model ID, model version, dimension, input hash,
  query entity or query text hash, similarity score, rank, and embedding run ID.
- Exact nearest-neighbor ordering may change after model or index changes. Replay must flag this
  caveat instead of pretending old similarity ranking is perfectly reproducible.
- Any stored decision that consumes semantic similarity must pin the original signal metadata.
- Commerce scoring cannot consume semantic similarity unless Invariant P-4 is lifted by amendment.

Discovery replay:

- Public UI discovery does not require exact replay of every result ordering.
- Editorial recommendations, curated collection decisions, and any stored publication decision
  should store top-N candidate snapshots if graph/vector signals materially influenced selection.

## 5. Relationship Ontology

The v1 ontology should stay small, explicit, and source-backed.

### Node Labels

| Label | PostgreSQL authority | Purpose |
|---|---|---|
| `Place` | `places` | Geographic and cultural anchor. |
| `SourceItem` | `source_item` / compatibility bridge to `illustration_opportunities` | Public media/intellectual object after activation. |
| `MediaFile` | `media_file` | Optional projection for package/file exploration, not rights authority. |
| `MediaType` | `media_type_registry` | Image, map, photography, poster, book, ebook, audiobook, audio, film, 3d, dataset. |
| `Creator` | `creator_authority_registry` | Resolved creator identity. |
| `Institution` | `sources` / source institution registry | Holding or providing institution. |
| `SubjectTerm` | governed vocabulary or technical metadata subject terms | Controlled subject traversal. |
| `Concept` | `concepts` | Taxon, standard concept, or knowledge concept. |
| `Designation` | standards/designation tables | UNESCO/Ramsar/IUCN-style designation. |
| `StandardClassification` | standards classification tables | Explainable standards alignment. |
| `Collection` | `collections` | Published collection. |
| `Story` | story/publication tables | Published editorial story when available. |
| `ActivationTarget` | `activation_target` | Bridge from substrate to existing platform spine. |
| `ProductFamily` | product routing tables | Derived commerce navigation, not scoring authority. |

Every node must carry:

```json
{
  "pg_id": "...",
  "pg_table": "...",
  "schema_version": "...",
  "projection_run_id": "...",
  "projected_at": "..."
}
```

### Relationship Types

| Relationship | Direction | Derivation |
|---|---|---|
| `LOCATED_IN` | `Place -> Place` | PostgreSQL place hierarchy. |
| `PROXIMATE_TO` | `Place -> Place` | PostGIS distance rule, stored as derived traversal aid. |
| `HAS_DESIGNATION` | `Place -> Designation` | Standards/designation source rows. |
| `HAS_CLASSIFICATION` | `Designation -> StandardClassification` | Standards classification source rows. |
| `DEPICTS` | `SourceItem -> Place/Concept/SubjectTerm` | Source item metadata and link tables. |
| `CREATED_BY` | `SourceItem -> Creator` | Resolved creator authority. |
| `HELD_BY` | `SourceItem -> Institution` | Source institution authority. |
| `OF_TYPE` | `SourceItem -> MediaType` | `media_type_registry` FK. |
| `HAS_FILE` | `SourceItem -> MediaFile` | UMS `media_file` package membership. |
| `HAS_ACTIVATION_TARGET` | `SourceItem -> ActivationTarget` | UMS activation bridge. |
| `IN_COLLECTION` | `SourceItem -> Collection` | Collection membership authority. |
| `FEATURES_PLACE` | `Collection/Story -> Place` | Published content metadata. |
| `FEATURES_ITEM` | `Collection/Story -> SourceItem` | Published content metadata. |
| `USES_STANDARD` | `Designation/Classification -> Concept` | Standards alignment. |
| `SAME_AS` | `Place/Concept/Creator -> external ID` | Wikidata/LOC/source external ID fields. |
| `ROUTES_TO_PRODUCT_FAMILY` | `ActivationTarget -> ProductFamily` | Product routing projection, explainability only. |

Every relationship must carry:

```json
{
  "derivation": "direct|derived",
  "pg_source": "...",
  "pg_source_id": "...",
  "schema_version": "...",
  "projection_run_id": "...",
  "projected_at": "..."
}
```

`SIMILAR_TO` should not be a v1 Neo4j relationship. Similarity belongs in pgvector unless a
future constitutional amendment defines a structural similarity rule.

## 6. Vector Embedding Architecture

pgvector should use named vector spaces, not one universal embedding table.

| Vector space | Entity | Input | Initial status |
|---|---|---|---|
| `source_item_semantic` | `SourceItem` | Title, description, subject terms, source institution, creator, date, place names, media type. | Active after SD-AMEND-1 and model approval. |
| `place_semantic` | `Place` | Name, description, OUV statement, heritage type, country, continent, subject summaries. | Active after SD-AMEND-1 and model approval. |
| `collection_semantic` | `Collection` | Title, description, featured places, subjects, item summaries. | Pending until collection publication is stable. |
| `story_semantic` | `Story` | Title, dek, body summary, places, subjects, linked media. | Pending until NC-authored stories exist. |
| `media_transcript_semantic` | Audio/Film/Audiobook | Transcript or caption text plus source metadata. | Deferred until Phase 2/3 media activation. |
| `dataset_metadata_semantic` | Dataset | Dataset title, description, variables, temporal/spatial coverage, license. | Deferred until Phase 4. |
| `visual_caption_semantic` | Image/Map/Photo/Poster/3D | Human or governed machine caption plus metadata. | Deferred unless caption governance is ratified. |

Required embedding record fields:

| Field | Purpose |
|---|---|
| `embedding_id` | Stable row identity. |
| `space_name` | Vector space boundary. |
| `space_version` | Allows parallel rebuild and active-space switch. |
| `entity_table` | PostgreSQL source table. |
| `entity_id` | PostgreSQL source ID. |
| `model_id` | Governed embedding model. |
| `model_version` | Provider/model version. |
| `dimension` | Vector dimension; immutable per model. |
| `embedding` | pgvector value. |
| `input_hash` | SHA-256 of governed input. |
| `input_schema_version` | Version of input materialization logic. |
| `rights_visibility` | Public/private/retracted visibility copied from authority for filtering. |
| `status` | active/stale/retracted/retired. |
| `embedded_at` | Timestamp. |

Query pattern:

```text
1. PostgreSQL filters canonical eligibility: media type, rights, publication, place, collection.
2. pgvector returns candidate entity IDs and similarity scores.
3. Neo4j optionally expands candidates by governed relationships.
4. FastAPI rehydrates candidates from PostgreSQL.
5. PostGIS applies authoritative spatial filters when geography matters.
6. Response includes canonical fields plus derived signal metadata.
```

## Migration Sequence

Use a separate relationship/semantic migration sequence after UMS M36. The sequence below is
ordered for execution after the required Strategic Direction amendment.

| Order | Package | Purpose |
|---:|---|---|
| 1 | Governance gate | Record SD-AMEND-1 permitting Neo4j and pgvector as projection-only layers. |
| 2 | `projection_schema_registry` | Register active graph node/relationship vocabulary and derivation rules. |
| 3 | `projection_event` | Append-only provenance for graph/vector projection cycles. |
| 4 | `projection_run` | Run-level state, counts, watermarks, checksums, degraded-mode reason. |
| 5 | `projection_cursor` | Incremental refresh cursor per source table and projection layer. |
| 6 | `projection_staleness_queue` | Prioritized queue for changed entity IDs; rights retractions highest priority. |
| 7 | `pgvector` extension | Enable vector type in PostgreSQL. |
| 8 | `pgvector_model_registry` | Govern embedding providers, dimensions, statuses, and model-change rebuild rules. |
| 9 | `semantic_vector_space_registry` | Govern vector spaces, entity sources, input schema, active space version. |
| 10 | Vector tables/indexes | Create per-space or partitioned embedding storage with HNSW indexes. |
| 11 | Neo4j constraints/indexes | Apply stable key constraints and label/relationship indexes. |
| 12 | API provenance contract | Require graph/vector signal metadata in discovery responses. |
| 13 | Replay fixtures | Add projection replay fixtures before production activation. |
| 14 | Staging full rebuild | Build graph and active vector spaces from PostgreSQL/MinIO. |
| 15 | Production activation | Enable derived discovery endpoints in degraded-safe mode. |

## Worker Sequence

| Order | Worker | Responsibility |
|---:|---|---|
| 1 | `projection_schema_seed_worker` | Loads the initial graph schema and vector-space registries after governance approval. |
| 2 | `projection_staleness_worker` | Watches PostgreSQL changes and queues stale entity IDs. |
| 3 | `relationship_snapshot_worker` | Materializes graph projection snapshots from PostgreSQL. |
| 4 | `neo4j_projection_worker` | Upserts nodes and direct relationships into Neo4j. |
| 5 | `neo4j_derived_relationship_worker` | Computes governed derived edges from PostgreSQL/PostGIS. |
| 6 | `neo4j_validation_worker` | Checks orphan nodes, missing source IDs, counts, relationship vocabulary, and checksums. |
| 7 | `embedding_input_worker` | Builds governed input payloads and input hashes. |
| 8 | `embedding_generation_worker` | Generates embeddings with the active registered model. |
| 9 | `pgvector_index_worker` | Builds and refreshes vector indexes per active space. |
| 10 | `semantic_validation_worker` | Checks dimensions, model IDs, stale hashes, visibility filters, and counts. |
| 11 | `hybrid_discovery_worker` | Optional async candidate enrichment for precomputed discovery surfaces. |
| 12 | `projection_replay_worker` | Recomputes graph/vector advisory metadata for replay tests. |
| 13 | `projection_drift_audit_worker` | Periodically compares derived layers against PostgreSQL authority. |

## Activation Sequence

1. Activate governance amendment.
2. Deploy PostgreSQL projection registries and audit tables.
3. Enable pgvector extension and model registry.
4. Deploy Neo4j service with no public query path.
5. Seed projection schema v1.
6. Seed vector spaces as pending.
7. Approve initial embedding model.
8. Run staging Neo4j full rebuild.
9. Run staging pgvector full rebuild for `source_item_semantic` and `place_semantic`.
10. Run replay and drift validation.
11. Enable internal discovery API in degraded-safe mode.
12. Enable public discovery enrichment behind feature flag.
13. Record production projection events.
14. Monitor staleness and drift before enabling broader semantic surfaces.

## Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Derived layer becomes accidental authority | Critical | API must rehydrate from PostgreSQL; graph/vector responses carry provenance; no downstream writes. |
| Rights or visibility retraction remains visible in discovery | Critical | Priority staleness queue; PostgreSQL recheck before response; deactivate vectors on rights changes. |
| Commerce scoring consumes graph/vector signals without amendment | Critical | Enforce Score Gate Invariant; tests assert commerce workers do not read Neo4j/pgvector. |
| Embedding model change breaks replay comparability | High | Model registry, vector-space versioning, input hashes, replay caveat reporting. |
| Graph relationship vocabulary grows into ungoverned ontology | High | `projection_schema_registry`; constitutional amendments for new labels/types/rules. |
| Neo4j/pgvector diverge from PostgreSQL | High | Drift audit worker; rebuild from PostgreSQL as recovery path. |
| Approximate nearest-neighbor ranking is nondeterministic | Medium | Store top-N snapshots for consequential decisions; label semantic replay caveats. |
| Graph explosion from proximity or subject edges | Medium | Govern thresholds; cap derived relationships; validate edge counts by type. |
| Vector cost and latency | Medium | Batch embeddings; per-space rebuilds; self-hosted model option; cache only advisory results. |
| PostGIS and Neo4j spatial views disagree | Medium | PostGIS remains authority; Neo4j proximity edges are derived and rebuildable. |
| Multi-media embedding inputs become inconsistent | Medium | Separate vector spaces by media/input class; defer transcript/caption spaces until governance exists. |

## GO / NO-GO

NO-GO for implementation today.

Reason: the governing constitution states Neo4j and pgvector implementation is blocked until
Director Decision SD-AMEND-1 amends the frozen stack clause.

GO for architecture only:

- Keep PostgreSQL/PostGIS/MinIO/UMS authoritative.
- Treat Neo4j and pgvector as derived, rebuildable, degraded-safe discovery layers.
- Implement only after the governance amendment, projection registries, replay fixtures, and
  rebuild protocols are in place.
