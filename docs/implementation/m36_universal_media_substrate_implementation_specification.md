# M36 Universal Media Substrate Implementation Specification

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Status | Implementation specification |
| Scope | No implementation |
| Governing constitution | `docs/governance/media_substrate_constitution_v1.1.md` |
| Runtime design | `docs/architecture/universal_media_substrate_runtime_v1.md` |
| Decision | GO, with constraints |

## Mission

Specify Migration 36 for the Universal Media Substrate.

M36 introduces the substrate entities required to support:

- `image`
- `map`
- `photography`
- `poster`
- `book`
- `ebook`
- `audiobook`
- `audio`
- `film`
- `3d`
- `dataset`

M36 must keep these layers frozen:

- Commerce Intelligence
- Product Routing
- Catalog
- Publication
- Asset Intelligence

No implementation is authorized by this specification. This document defines SQL scope, workers,
replay tests, migration ordering, compatibility risks, and GO / NO-GO conditions.

## Executive Decision

M36 is a **GO** as an additive substrate migration.

GO is conditional on these constraints:

1. Do not rename `illustration_opportunities` in M36.
2. Do not change Commerce scoring formulas.
3. Do not change Product Routing, Catalog, Publication, or Asset Intelligence schemas except where
   future constitution amendments explicitly authorize them.
4. Register all eleven media types, but activate only Phase 1 types: `image`, `map`,
   `photography`, `poster`.
5. Include `asset_delivery_manifest` even though it was not listed in the prompt; v1.1 makes it
   a governed entity.
6. Use standalone `source_record` and standalone `media_rights` tables per DD-1 and DD-2.
7. Use worker-level JSON Schema validation for `media_technical_metadata` per DD-3.
8. Treat Phase 2–4 rows as registry-only until constitutional amendments activate them.

## M36 Entity Scope

M36 creates or amends runtime support for ten governed entities:

| Entity | Required in M36 | Notes |
|---|---:|---|
| `media_type_registry` | Yes | Seed all 11 media types; Phase 1 active, Phase 2–4 pending. |
| `source_item` | Yes | Acquisition atomic work. Current source, rights, technical metadata FKs. |
| `source_record` | Yes | Standalone immutable metadata snapshot table. |
| `media_file` | Yes | WORM/source file records stored in MinIO. |
| `media_derivative` | Yes | Delivery and thumbnail derivatives. |
| `asset_delivery_manifest` | Yes | Required by v1.1 Article 10. |
| `media_rights` | Yes | Standalone versioned rights table. |
| `media_technical_metadata` | Yes | Worker-validated technical metadata with schema version pinning. |
| `preservation_event` | Yes | Append-only PREMIS/PROV event log. |
| `activation_target` | Yes | Final substrate-to-commerce approval boundary. |

M36 also creates compatibility glue:

- `activation_target_downstream_link`

This avoids mutating downstream commerce tables while still satisfying the constitutional
requirement that the pipeline record reference the authorizing `activation_target`.

## SQL Changes Required

### 1. Extensions and common assumptions

Required existing assumptions:

- UUID generation is available.
- `sources` exists from earlier migrations.
- `illustration_opportunities` exists and remains the Phase 1 downstream physical realization.
- PostgreSQL is the authority.
- MinIO keys are evidence references, not state authority.

M36 should not require `pg_jsonschema`. v1.1 DD-3 explicitly chooses worker-level validation.

### 2. Vocabulary tables

Create small governed vocabulary tables or equivalent checked seed tables for:

- `media_type_status_vocabulary`: `pending`, `active`, `retired`
- `source_item_status_vocabulary`: `proposed`, `acquired`, `rights_verified`,
  `activation_eligible`, `activated`, `rejected`, `retracted`
- `source_record_schema_standard_vocabulary`: `marc`, `edm`, `lido`, `dc`, `mods`, `oai_pmh`,
  `schema_org`, `bhl_api`
- `media_file_role_vocabulary`: `master`, `page`, `track`, `segment`, `model`, `data`
- `media_derivative_role_vocabulary`: `delivery`, `thumbnail`, `texture`, `material`
- `media_rights_status_vocabulary`: `pending`, `verified_pd`, `verified_cc0`, `blocked`,
  `under_review`
- `preservation_event_type_vocabulary`: `ingestion`, `format_identification`, `validation`,
  `fixity_check`, `normalization`, `rights_verification`, `replication`, `migration`, `deletion`
- `preservation_event_outcome_vocabulary`: `success`, `failure`, `warning`
- `preservation_agent_type_vocabulary`: `worker`, `human`, `institution`
- `activation_target_status_vocabulary`: `nominated`, `approved`, `rejected`, `escalated`
- `delivery_protocol_vocabulary`: `iiif`, `hls`, `model-viewer`, `epub-js`, `html5-audio`,
  `pdf-js`, `download`

### 3. `media_type_registry`

Required fields:

- `id UUID PRIMARY KEY`
- `media_type_id TEXT UNIQUE NOT NULL`
- `display_name TEXT NOT NULL`
- `expansion_phase INT NOT NULL CHECK (expansion_phase BETWEEN 1 AND 4)`
- `anchor_types_allowed TEXT[] NOT NULL`
- `delivery_protocol TEXT NOT NULL`
- `archival_format TEXT NOT NULL`
- `delivery_format TEXT NOT NULL`
- `requires_file_manifest BOOLEAN NOT NULL`
- `content_spec_schema JSONB NOT NULL`
- `content_spec_schema_version TEXT NOT NULL`
- `status TEXT NOT NULL`
- `constitutional_ref TEXT`
- `authored_by TEXT NOT NULL`
- `approved_by TEXT`
- `approved_at TIMESTAMPTZ`
- `provenance JSONB NOT NULL DEFAULT '{}'`
- timestamps

Constraints:

- `media_type_id` lowercase/no spaces.
- `anchor_types_allowed` non-empty and limited to `biological`, `geographic`, `cultural`,
  `mixed`.
- Phase 2–4 cannot become `active` without `constitutional_ref`.
- Active rows require `approved_by`, `approved_at`, and second-human rule.
- No DELETE.
- Immutable on insert: `media_type_id`, `expansion_phase`, `archival_format`,
  `delivery_protocol`.
- Immutable once active: `content_spec_schema`, `delivery_format`.

Seed posture:

| media_type_id | phase | protocol | archival | delivery | manifest | status |
|---|---:|---|---|---|---:|---|
| `image` | 1 | `iiif` | `tiff` | `jpeg2000` | false | `active` |
| `map` | 1 | `iiif` | `tiff` | `jpeg2000` | false | `active` |
| `photography` | 1 | `iiif` | `tiff` | `jpeg2000` | false | `active` |
| `poster` | 1 | `iiif` | `tiff` | `jpeg2000` | false | `active` |
| `book` | 2 | `iiif` | `pdf` | `epub3` | true | `pending` |
| `ebook` | 2 | `epub-js` | `epub3` | `epub3` | false | `pending` |
| `audiobook` | 2 | `html5-audio` | `wav-bwf` | `mp3` | true | `pending` |
| `audio` | 3 | `html5-audio` | `wav-bwf` | `flac` | true | `pending` |
| `film` | 3 | `hls` | `ffv1-mkv` | `h264` | true | `pending` |
| `3d` | 4 | `model-viewer` | `gltf` | `glb` | true | `pending` |
| `dataset` | 4 | `download` | `csv` | `json-ld` | true | `pending` |

### 4. `source_item`

Required fields:

- `id UUID PRIMARY KEY`
- `source_id UUID NOT NULL REFERENCES sources(id)`
- `source_identifier TEXT NOT NULL`
- `media_type_id TEXT NOT NULL REFERENCES media_type_registry(media_type_id)`
- `canonical_source_url TEXT`
- `title TEXT`
- `status TEXT NOT NULL DEFAULT 'proposed'`
- `anchor_type TEXT`
- `current_source_record_id UUID`
- `current_media_rights_id UUID`
- `current_technical_metadata_id UUID`
- `provenance JSONB NOT NULL DEFAULT '{}'`
- timestamps

Constraints:

- Unique `(source_id, source_identifier)`.
- `media_type_id` must reference an `active` type before ingestion. Pending types may be registered
  but not ingested.
- Workers may perform only constitutional automatic transitions.
- `activated → retracted` requires Director Decision in authorizing `activation_target.provenance`.
- Cannot be `activation_eligible` without current verified rights and valid technical metadata.
- No DELETE.

FK cycle handling:

- Create `source_item` first with nullable current FKs.
- Create versioned child tables.
- Add FKs from `source_item.current_*_id` after child tables exist.

### 5. `source_record`

Required fields:

- `id UUID PRIMARY KEY`
- `source_item_id UUID NOT NULL REFERENCES source_item(id)`
- `institution_id UUID NOT NULL REFERENCES sources(id)`
- `source_identifier TEXT NOT NULL`
- `schema_standard TEXT NOT NULL`
- `raw_payload JSONB NOT NULL`
- `raw_payload_hash TEXT NOT NULL`
- `normalized_payload JSONB NOT NULL DEFAULT '{}'`
- `fetched_at TIMESTAMPTZ NOT NULL`
- `fetched_by TEXT NOT NULL`
- `superseded_by UUID REFERENCES source_record(id)`
- timestamps

Constraints:

- Immutable on insert: `institution_id`, `source_identifier`, `raw_payload`, `schema_standard`,
  `fetched_at`.
- `schema_standard` limited to governed vocabulary.
- No DELETE.
- Optional uniqueness on `(source_item_id, raw_payload_hash)` to avoid duplicate snapshots.

Required trigger behavior:

- On insert of new source record for an item with current rights `verified_pd` or `verified_cc0`,
  acquisition worker must evaluate rights inconsistency. Database cannot fully detect semantic
  inconsistency; tests must prove the worker performs Article 7.7.

### 6. `media_file`

Required fields:

- `id UUID PRIMARY KEY`
- `source_item_id UUID NOT NULL REFERENCES source_item(id)`
- `source_record_id UUID REFERENCES source_record(id)`
- `media_type_id TEXT NOT NULL REFERENCES media_type_registry(media_type_id)`
- `file_role TEXT NOT NULL`
- `sequence_position INT NOT NULL DEFAULT 1`
- `source_url TEXT`
- `original_filename TEXT NOT NULL`
- `minio_bucket TEXT NOT NULL`
- `minio_key TEXT NOT NULL`
- `mime_type TEXT NOT NULL`
- `byte_size BIGINT NOT NULL CHECK (byte_size > 0)`
- `checksum_sha256 TEXT NOT NULL`
- `preservation_status TEXT NOT NULL DEFAULT 'pending_ingestion'`
- `ingestion_event_id UUID`
- `provenance JSONB NOT NULL DEFAULT '{}'`
- timestamps

Constraints:

- Unique `(minio_bucket, minio_key)`.
- Unique `(source_item_id, file_role, sequence_position)` for WORM roles.
- Check MinIO key convention:
  `masters/{source_id}/{media_type_id}/{source_item_id}/{seq}/{filename}` for WORM roles.
- WORM immutability after ingestion event.
- Link to ingestion preservation event after `preservation_event` exists.
- No downstream activation when source item lacks at least one master/page/track/segment/model/data
  file with successful ingestion.

### 7. `media_derivative`

Required fields:

- `id UUID PRIMARY KEY`
- `source_item_id UUID NOT NULL REFERENCES source_item(id)`
- `media_file_id UUID NOT NULL REFERENCES media_file(id)`
- `media_type_id TEXT NOT NULL REFERENCES media_type_registry(media_type_id)`
- `file_role TEXT NOT NULL`
- `derivative_policy_version TEXT NOT NULL`
- `minio_bucket TEXT NOT NULL`
- `minio_key TEXT NOT NULL`
- `mime_type TEXT NOT NULL`
- `byte_size BIGINT NOT NULL CHECK (byte_size > 0)`
- `checksum_sha256 TEXT NOT NULL`
- `width_px INT`
- `height_px INT`
- `duration_seconds NUMERIC`
- `generated_by TEXT NOT NULL`
- `generated_at TIMESTAMPTZ NOT NULL`
- `superseded_by UUID REFERENCES media_derivative(id)`
- `provenance JSONB NOT NULL DEFAULT '{}'`
- timestamps

Constraints:

- `file_role` limited to `delivery`, `thumbnail`, `texture`, `material`.
- Complete chain `media_derivative → media_file → source_item`.
- Delivery derivative protocol must match media type delivery protocol.
- No DELETE unless paired with valid preservation deletion event for non-WORM derivative policy.

### 8. `asset_delivery_manifest`

Required by v1.1.

Required fields:

- `id UUID PRIMARY KEY`
- `source_item_id UUID NOT NULL REFERENCES source_item(id)`
- `media_type_id TEXT NOT NULL REFERENCES media_type_registry(media_type_id)`
- `delivery_protocol TEXT NOT NULL`
- `primary_endpoint TEXT NOT NULL`
- `manifest_payload JSONB`
- `manifest_payload_hash TEXT`
- `generated_at TIMESTAMPTZ`
- `generated_by TEXT`
- `published_at TIMESTAMPTZ`
- `invalidated_at TIMESTAMPTZ`
- `triggering_derivative_id UUID REFERENCES media_derivative(id)`
- `media_rights_id UUID REFERENCES media_rights(id)`
- `technical_metadata_id UUID REFERENCES media_technical_metadata(id)`
- `superseded_by UUID REFERENCES asset_delivery_manifest(id)`
- `provenance JSONB NOT NULL DEFAULT '{}'`
- timestamps

Constraints:

- At most one active manifest per `source_item`: unique partial index where `invalidated_at IS NULL`.
- Manifest can be generated only when `source_item.status IN ('activation_eligible','activated')`.
- `delivery_protocol` must match `media_type_registry.delivery_protocol`.
- Immutable on insert: `source_item_id`, `media_type_id`, `delivery_protocol`.
- `primary_endpoint` immutable after `published_at IS NOT NULL`.
- Regeneration sets `invalidated_at` and inserts a new row; never DELETE.
- IIIF manifests for `delivery_protocol = 'iiif'` must be worker-validated as IIIF Presentation
  API 3.0 payloads.

### 9. `media_rights`

Required fields:

- `id UUID PRIMARY KEY`
- `source_item_id UUID NOT NULL REFERENCES source_item(id)`
- `rights_status TEXT NOT NULL DEFAULT 'pending'`
- `rights_statement_uri TEXT`
- `rights_evidence JSONB NOT NULL DEFAULT '{}'`
- `commercial_reuse_permitted BOOLEAN NOT NULL DEFAULT FALSE`
- `modification_permitted BOOLEAN NOT NULL DEFAULT FALSE`
- `verified_by TEXT`
- `verified_at TIMESTAMPTZ`
- `authored_by TEXT NOT NULL`
- `superseded_by UUID REFERENCES media_rights(id)`
- `provenance JSONB NOT NULL DEFAULT '{}'`
- timestamps

Constraints:

- `verified_pd` and `verified_cc0` require governed `rights_statement_uri`, evidence,
  `verified_by`, and `verified_at`.
- `verified_pd` and `verified_cc0` require `commercial_reuse_permitted = TRUE`.
- `blocked` requires evidence and verifier.
- `verified_pd`, `verified_cc0`, and `blocked` immutable.
- No DELETE.
- Rights statement URI limited to v1.1 Article 24 vocabulary.

### 10. `media_technical_metadata`

Required fields:

- `id UUID PRIMARY KEY`
- `source_item_id UUID NOT NULL REFERENCES source_item(id)`
- `media_type_id TEXT NOT NULL REFERENCES media_type_registry(media_type_id)`
- `schema_version TEXT NOT NULL`
- `content JSONB NOT NULL`
- `validation_status TEXT NOT NULL`
- `validated_by TEXT NOT NULL`
- `validated_at TIMESTAMPTZ NOT NULL`
- `validator_name TEXT NOT NULL`
- `validator_version TEXT NOT NULL`
- `content_hash TEXT NOT NULL`
- `superseded_by UUID REFERENCES media_technical_metadata(id)`
- `provenance JSONB NOT NULL DEFAULT '{}'`
- timestamps

Constraints:

- Database enforces non-null content, schema version, valid media type FK.
- Worker validates JSON Schema conformance and writes validation evidence.
- Only `validation_status = 'valid'` can be linked as `source_item.current_technical_metadata_id`.
- Content immutable once the record has served as current.

### 11. `preservation_event`

Required fields:

- `id UUID PRIMARY KEY`
- `subject_type TEXT NOT NULL`
- `subject_id UUID NOT NULL`
- `media_file_id UUID REFERENCES media_file(id)`
- `media_derivative_id UUID REFERENCES media_derivative(id)`
- `event_type TEXT NOT NULL`
- `event_datetime TIMESTAMPTZ NOT NULL`
- `event_outcome TEXT NOT NULL`
- `event_detail JSONB NOT NULL DEFAULT '{}'`
- `agent_type TEXT NOT NULL`
- `agent_id TEXT NOT NULL`
- timestamps

Constraints:

- Append-only: no UPDATE, no DELETE.
- `event_type` and `event_outcome` limited to vocabulary.
- `deletion` requires `event_outcome = 'success'`, `agent_type = 'human'`, and Director Decision
  reference in `event_detail`.
- `ingestion` event required before WORM `media_file` is considered acquired.
- `rights_verification` warning event required for Article 7.7 inconsistency.

### 12. `activation_target`

Required fields:

- `id UUID PRIMARY KEY`
- `source_item_id UUID NOT NULL REFERENCES source_item(id)`
- `status TEXT NOT NULL DEFAULT 'nominated'`
- `nominated_by TEXT NOT NULL`
- `nominated_at TIMESTAMPTZ NOT NULL`
- `approved_by TEXT`
- `approved_at TIMESTAMPTZ`
- `media_rights_id_at_approval UUID REFERENCES media_rights(id)`
- `technical_metadata_id_at_approval UUID REFERENCES media_technical_metadata(id)`
- `rejection_reason TEXT`
- `escalation_reason TEXT`
- `provenance JSONB NOT NULL DEFAULT '{}'`
- timestamps

Constraints:

- Can be created only for `source_item.status = 'activation_eligible'`.
- Unique partial index: one `nominated` or `approved` target per `source_item`.
- Second-human rule: `approved_by IS DISTINCT FROM nominated_by`.
- On transition to `approved`, atomically set approval timestamp, rights ID, and technical
  metadata ID from source item current FKs.
- Approved fields immutable.
- Rejected target cannot be re-nominated without Director Decision.
- Source item retraction requires Director Decision in authorizing activation target provenance.

### 13. `activation_target_downstream_link`

Required for M36 backward compatibility.

Required fields:

- `id UUID PRIMARY KEY`
- `activation_target_id UUID NOT NULL REFERENCES activation_target(id)`
- `downstream_type TEXT NOT NULL`
- `downstream_id UUID NOT NULL`
- `created_at TIMESTAMPTZ NOT NULL`
- `created_by TEXT NOT NULL`
- `provenance JSONB NOT NULL DEFAULT '{}'`

Constraints:

- Unique `(activation_target_id)`.
- Unique `(downstream_type, downstream_id)`.
- `downstream_type = 'illustration_opportunity'` in M36.
- Link records immutable after insert.

This satisfies Article 14.5 without mutating downstream tables in M36.

## Workers Required

### 1. `media_type_registry_seed_worker`

Purpose:

- Seed M36 registry rows and vocabularies.
- Verify Phase 1 active / Phase 2–4 pending posture.

Must not:

- Activate Phase 2–4.
- Modify active immutable registry fields.

### 2. `source_acquisition_worker`

Purpose:

- Create `source_item`.
- Fetch source payload.
- Insert immutable `source_record`.
- Update `source_item.current_source_record_id`.
- Detect rights inconsistency on source refetch per Article 7.7.

Required source adapters:

- LOC Phase 1 adapter.
- Smithsonian Phase 1 adapter.
- Europeana aggregator/reconciliation adapter.
- Internet Archive manifest-normalization adapter, registry-only unless Phase 1 rights-safe item.

### 3. `media_file_ingestion_worker`

Purpose:

- Fetch/store master files in MinIO.
- Compute SHA-256.
- Insert `media_file`.
- Write ingestion, format identification, validation preservation events.
- Advance `source_item proposed → acquired` when gates pass.

### 4. `media_derivative_worker`

Purpose:

- Generate Phase 1 delivery derivatives and thumbnails.
- Write `media_derivative`.
- Write normalization and fixity events.

M36 scope:

- IIIF/Image API suitable derivatives for `image`, `map`, `photography`, `poster`.
- Do not generate active delivery derivatives for Phase 2–4 media.

### 5. `media_rights_worker`

Purpose:

- Create pending or under-review rights records.
- Assist rights evidence extraction.
- Perform automated verification only if source strategy has Director authorization.
- Write rights verification preservation events.

Must not:

- Verify rights outside authorized strategy.
- Override Public Domain/CC0 hard gate.

### 6. `media_technical_metadata_worker`

Purpose:

- Extract EXIF/TIFF/image metadata for Phase 1 media.
- Validate `content` against `media_type_registry.content_spec_schema`.
- Write schema version, validator name/version, content hash, and validation status.
- Link valid metadata as current.
- Advance `rights_verified → activation_eligible` when valid.

### 7. `asset_delivery_manifest_worker`

Purpose:

- Generate IIIF Presentation API 3.0 manifests for eligible Phase 1 source items.
- Generate JSON-LD/Schema.org delivery payloads.
- Store `asset_delivery_manifest`.
- Regenerate manifests after derivative changes by invalidating old row and inserting new row.

Must not:

- Generate manifests for `proposed`, `acquired`, or only `rights_verified` source items.
- Change published primary endpoint without redirect/provenance policy.

### 8. `activation_target_worker`

Purpose:

- Nominate eligible source items for activation.
- Create `activation_target` in `nominated`.
- On human approval through API/governance workflow, atomically capture current rights and
  technical metadata IDs.
- Create `activation_target_downstream_link` after downstream opportunity creation.

Must not:

- Approve its own nomination.
- Create commerce scores directly.

### 9. `substrate_replay_worker`

Purpose:

- Reconstruct substrate state at activation time.
- Verify source record, rights, technical metadata, files, derivatives, manifest, and preservation
  events.
- Feed replay assertions to Commerce replay without changing Commerce formulas.

### 10. `fixity_check_worker`

Purpose:

- Annual SHA-256 verification for WORM files.
- Write `fixity_check` preservation events.
- Escalate failures.

## Replay Tests Required

### Source record replay

1. Immutable source payload cannot be changed.
2. Re-fetch creates a new source record and updates current FK.
3. Historical activation still points to old source record.
4. Rights inconsistency in new source payload creates `under_review` rights record and warning
   preservation event.

### Rights replay

1. Verified rights record cannot be mutated.
2. Rights re-evaluation creates new record.
3. Activation approval pins `media_rights_id_at_approval`.
4. Current rights can become `under_review` without altering historical activation replay.
5. No activation when current rights are `pending`, `blocked`, or `under_review`.

### Technical metadata replay

1. Worker-valid metadata can be linked as current.
2. Invalid metadata cannot be linked as current.
3. Schema version is pinned.
4. Technical metadata used at approval is captured on activation target.
5. Commerce score inputs for post-M36 records include technical metadata ID when technical signals
   are used.

### Preservation replay

1. `preservation_event` is append-only.
2. WORM media file cannot change after ingestion event.
3. Derivative regeneration writes normalization/fixity events.
4. Deletion event requires human Director Decision.
5. File state can be reconstructed from event history.

### Activation replay

1. Activation target cannot be nominated before `activation_eligible`.
2. Approval enforces second-human rule.
3. Approval atomically captures rights and technical metadata IDs.
4. One active/nominated activation target per source item.
5. Approved activation authorizes exactly one downstream link.
6. Rejected activation cannot be re-nominated without Director Decision.
7. Retraction requires Director Decision in activation target provenance.

### Manifest replay

1. No manifest for `proposed`, `acquired`, or `rights_verified`.
2. IIIF manifest generated for Phase 1 `activation_eligible` item.
3. One active manifest per source item.
4. Manifest regeneration invalidates prior record and inserts new record.
5. Published endpoint is immutable unless redirect policy/provenance is present.
6. Manifest payload references pinned derivative and rights record.

### Backward compatibility replay

1. Pre-M36 commerce replay does not require substrate IDs.
2. Optional backfill does not alter historical `commerce_opportunities.score_inputs`.
3. Post-M36 recompute uses substrate anchors when available.
4. Legacy BHL flow remains operational.
5. LOC map proof candidates can promote through substrate without direct Commerce mutation.

## Migration Ordering Required

M36 should be split into deterministic sub-migrations:

| Order | Step | Purpose | Depends on |
|---:|---|---|---|
| 1 | M36-A vocabularies | Seed lifecycle/status/protocol vocabularies. | Existing DB |
| 2 | M36-B media type registry | Create registry, triggers, seed 11 types. | M36-A |
| 3 | M36-C source item shell | Create `source_item` without current FKs. | M36-B, `sources` |
| 4 | M36-D source record | Create immutable standalone `source_record`. | M36-C |
| 5 | M36-E media rights | Create standalone versioned `media_rights`. | M36-C |
| 6 | M36-F technical metadata | Create `media_technical_metadata`. | M36-B, M36-C |
| 7 | M36-G current FK wiring | Add current FKs on `source_item`. | M36-D/E/F |
| 8 | M36-H media files | Create `media_file`. | M36-C/D |
| 9 | M36-I derivatives | Create `media_derivative`. | M36-H |
| 10 | M36-J preservation events | Create append-only `preservation_event`, then add file event references. | M36-H/I |
| 11 | M36-K delivery manifests | Create `asset_delivery_manifest`. | M36-B/C/E/F/I |
| 12 | M36-L activation targets | Create `activation_target` with approval pins. | M36-C/E/F |
| 13 | M36-M downstream link | Create `activation_target_downstream_link`. | M36-L |
| 14 | M36-N triggers and policies | Install all immutability/status/second-human/append-only triggers. | All tables |
| 15 | M36-O compatibility backfill | Create non-invasive compatibility rows where evidence is sufficient. | M36-N |
| 16 | M36-P verification suite | Run replay, immutability, and compatibility tests. | M36-O |

Important ordering note:

- `preservation_event` references `media_file` and `media_derivative`, while `media_file` needs an
  ingestion event for WORM finalization. Implement by creating `media_file` first in pending state,
  writing `preservation_event`, then updating `media_file.ingestion_event_id` under controlled
  trigger rules.

## Backward Compatibility Strategy

### No downstream schema mutation in M36

M36 should prefer `activation_target_downstream_link` over adding `activation_target_id` to
`illustration_opportunities`.

Reason:

- Keeps Commerce, Routing, Catalog, Publication, and Asset Intelligence frozen.
- Avoids coordinated amendment burden.
- Allows future successor table after the mandatory Phase 2 rename amendment.

### Legacy BHL compatibility

Rules:

- Existing BHL illustration flow remains valid.
- Backfill substrate records only where source/right/file evidence exists.
- Do not create approved activation targets for historical records without a governed backfill
  review workflow.

### LOC proof compatibility

Rules:

- LOC proof candidates should promote into substrate first.
- Activation creates or links to downstream opportunity only after rights, technical metadata, and
  approval gates pass.

### Phase 2–4 compatibility

Rules:

- Phase 2–4 registry rows exist as pending.
- Workers must reject ingestion for pending media types.
- Mandatory rename of `illustration_opportunities` to successor table is deferred, but must occur
  before any Phase 2 `source_item` reaches `activation_eligible` in production.

## Compatibility Risks

| Risk | Severity | Mitigation |
|---|---|---|
| M36 numbering collision with older Commerce Execution docs | Medium | Use `UMS M36`; renumber execution migrations if later ratified. |
| Downstream systems expect `illustration_opportunities` only | High | Use compatibility link; do not rename in M36. |
| Constitution v1.1 makes `asset_delivery_manifest` mandatory but runtime v1 was based on v1.0 wording | Medium | Include manifest table and manifest replay tests in M36. |
| Worker-level schema validation is weaker than database validation | Medium | Store validator name/version/schema version/content hash and test invalid metadata rejection. |
| Rights inconsistency on source refetch is semantic, not fully DB-enforceable | High | Mandatory worker tests for Article 7.7; alert and preservation event requirements. |
| Historical backfill may imply approval that never happened | High | Backfill evidence only; do not auto-approve activation targets. |
| MinIO key convention cannot be fully validated semantically in SQL | Medium | SQL pattern checks plus worker tests. |
| Phase 2–4 pending types accidentally ingested | High | Database trigger blocks ingestion unless `media_type_registry.status = 'active'`. |
| Published manifest endpoint changes break consumers | Medium | Track `published_at`; immutable endpoint after publication. |
| Activation approval pins wrong rights/technical metadata under race | High | Approval transition must be one database transaction with row locks on source item/current FKs. |

## GO / NO-GO

### GO

M36 is GO for implementation planning because:

- v1.1 resolves all constitutional open questions.
- Standalone `source_record` and `media_rights` tables are now mandated.
- Worker-level schema validation is explicitly authorized.
- The existing downstream architecture can remain frozen through a compatibility link table.
- Phase 2–4 media can be safely registered without activation.

### NO-GO conditions

Do not implement M36 if any of the following cannot be satisfied:

1. Database triggers cannot enforce append-only `preservation_event`.
2. Verified/blocked `media_rights` records cannot be made immutable.
3. `activation_target` approval cannot atomically pin rights and technical metadata IDs.
4. Pending media types cannot be blocked from ingestion.
5. Existing Commerce replay would be forced to require substrate IDs for pre-M36 records.
6. `asset_delivery_manifest` cannot be included.
7. Backfill would auto-approve historical assets without human/governed review.

## Final Specification Position

M36 should proceed as an additive, upstream substrate migration.

It should implement the ten governed substrate entities from
`media_substrate_constitution_v1.1`, seed all media types, activate only Phase 1, preserve legacy
Commerce behavior, and establish replay anchors that future media phases can reuse without
redesigning the platform.
