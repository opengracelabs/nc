# M36 Engineering Specification v2

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Status | Engineering specification |
| Scope | No implementation |
| Governing constitution | `docs/governance/media_substrate_constitution_v1.2.md` |
| Runtime design | `docs/architecture/universal_media_substrate_runtime_v1.md` |
| Supersedes | `docs/implementation/m36_universal_media_substrate_implementation_specification.md` |
| Decision | GO for Phase 1 M36; NO-GO for Phase 2–4 activation |

## Mission

Produce the exact implementation roadmap for M36 Universal Media Substrate under
`media_substrate_constitution_v1.2`.

M36 supports all eleven media types by registering their constitutional contracts:

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

M36 activates only Phase 1:

- `image`
- `map`
- `photography`
- `poster`

M36 must keep frozen:

- Commerce Intelligence
- Product Routing
- Catalog
- Publication
- Asset Intelligence

## v2 Delta From v1 Specification

`media_substrate_constitution_v1.2` adds no new entities and requires no new migration tables
beyond v1.1. It does change engineering execution by adding:

1. Constitutional phase boundary criteria.
2. A total activation order for all eleven media types.
3. Minimum future amendment requirements for P2-1, P3-1, and P4-1.
4. Tier 1 reference institution rules for LOC, Europeana, Smithsonian, Internet Archive, and
   British Library.
5. Rejected governance patterns that workers must not accidentally import.

Engineering effect:

- M36 remains additive.
- M36 must enforce Phase 1 activation only.
- M36 test coverage must include v1.2 reference-institution rules for Phase 1.
- M36 must explicitly block Phase 2–4 ingestion and activation.

## GO / NO-GO

### GO

M36 is GO for Phase 1 implementation planning because:

- v1.2 confirms no additional entities are required.
- v1.1 resolved all physical table decisions.
- v1.2 authorizes immediate concurrent activation of `image`, `map`, `photography`, and `poster`.
- The downstream commerce spine remains frozen by using `activation_target_downstream_link`.

### NO-GO

M36 is NO-GO for any production activation of:

- `book`
- `ebook`
- `audiobook`
- `audio`
- `film`
- `dataset`
- `3d`

These types may be seeded in `media_type_registry` as `pending` only.

## SQL DDL Sequence

M36 should be implemented as deterministic sub-migrations. The sequence below is the recommended
execution order.

| Step | Sub-migration | DDL action | Critical constraints |
|---:|---|---|---|
| 1 | M36-001 | Create substrate vocabulary tables. | No DELETE on vocabulary rows; values seeded exactly from constitution. |
| 2 | M36-002 | Create `media_type_registry`. | Immutable registry fields; Phase 2–4 activation requires amendment; active requires second-human approval. |
| 3 | M36-003 | Seed all eleven `media_type_registry` rows. | Phase 1 active; Phase 2–4 pending. |
| 4 | M36-004 | Create `source_item` shell with nullable current FKs. | Unique source identity; no DELETE; pending types cannot ingest. |
| 5 | M36-005 | Create standalone immutable `source_record`. | Raw payload immutability; schema vocabulary; source refetch creates new row. |
| 6 | M36-006 | Create standalone versioned `media_rights`. | Verified/blocked immutability; governed rights URI vocabulary. |
| 7 | M36-007 | Create `media_technical_metadata`. | Worker-level JSON Schema validation evidence fields; schema version pinned. |
| 8 | M36-008 | Add current FK constraints to `source_item`. | Current source record, rights, technical metadata FKs. |
| 9 | M36-009 | Create `media_file`. | WORM roles; MinIO key pattern; SHA-256 required. |
| 10 | M36-010 | Create `media_derivative`. | Complete derivative-to-master chain; versionable derivatives. |
| 11 | M36-011 | Create `preservation_event`. | Append-only; PREMIS/PROV event vocabulary; deletion requires Director Decision. |
| 12 | M36-012 | Add file-event integrity references. | Ingestion event required before WORM finalization. |
| 13 | M36-013 | Create `asset_delivery_manifest`. | One active manifest per source item; endpoint immutable after publication. |
| 14 | M36-014 | Create `activation_target`. | Approval atomically pins rights and technical metadata IDs. |
| 15 | M36-015 | Create `activation_target_downstream_link`. | One approved target maps to exactly one downstream pipeline record. |
| 16 | M36-016 | Install trigger suite. | Immutability, status transitions, second-human rule, pending-type ingestion block. |
| 17 | M36-017 | Install index suite. | Current FK indexes, source lookup, replay anchors, manifest active partial index. |
| 18 | M36-018 | Install compatibility views if useful. | Read-only views only; no downstream behavior change. |

### Required DDL Details

#### `media_type_registry`

Must include:

- `media_type_id`
- `display_name`
- `expansion_phase`
- `anchor_types_allowed`
- `delivery_protocol`
- `archival_format`
- `delivery_format`
- `requires_file_manifest`
- `content_spec_schema`
- `content_spec_schema_version`
- `status`
- `constitutional_ref`
- `authored_by`
- `approved_by`
- `approved_at`
- `provenance`

Required v1.2 rules:

- Phase assignment cannot change without amendment.
- Phase 2–4 rows seeded as `pending`.
- Activation order is governance-enforced by migration seed posture and tests.
- Phase 1 rows active concurrently.

#### `source_item`

Must include:

- `source_id`
- `source_identifier`
- `media_type_id`
- `canonical_source_url`
- `title`
- `status`
- `anchor_type`
- `current_source_record_id`
- `current_media_rights_id`
- `current_technical_metadata_id`
- `provenance`

Required v1.2 rules:

- `image`, `map`, `photography`, `poster` may progress.
- Phase 2–4 types may not progress past registry pending state.
- DD-4 remains: `illustration_opportunities → asset_opportunities` rename is mandatory before
  any Phase 2 source item reaches `activation_eligible`.

#### `source_record`

Must include:

- `source_item_id`
- `institution_id`
- `source_identifier`
- `schema_standard`
- `raw_payload`
- `raw_payload_hash`
- `normalized_payload`
- `fetched_at`
- `fetched_by`
- `superseded_by`

Required v1.2 rules:

- LOC schema records may use `marc` and `mods`.
- Europeana records may use `edm` and must be checked for required fields.
- Internet Archive records may use `dc` or `oai_pmh`.
- Raw payload is immutable.
- New source records must trigger rights inconsistency evaluation when current rights are verified.

#### `media_file`

Must include:

- `source_item_id`
- `source_record_id`
- `media_type_id`
- `file_role`
- `sequence_position`
- `source_url`
- `original_filename`
- `minio_bucket`
- `minio_key`
- `mime_type`
- `byte_size`
- `checksum_sha256`
- `preservation_status`
- `ingestion_event_id`
- `provenance`

Required v1.2 rules:

- WORM roles remain WORM.
- LOC bulk transfers must record BagIt verification in ingestion event detail.
- IA WORM philosophy adopted; IA rights self-assertion rejected.

#### `media_derivative`

Must include:

- `source_item_id`
- `media_file_id`
- `media_type_id`
- `file_role`
- `derivative_policy_version`
- `minio_bucket`
- `minio_key`
- `mime_type`
- `byte_size`
- `checksum_sha256`
- dimensions/duration where applicable
- `generated_by`
- `generated_at`
- `superseded_by`
- `provenance`

M36 derivative scope:

- Phase 1 visual delivery and thumbnails only.
- No active EPUB, audio, film, dataset, or 3D derivatives in M36.

#### `media_rights`

Must include:

- `source_item_id`
- `rights_status`
- `rights_statement_uri`
- `rights_evidence`
- `commercial_reuse_permitted`
- `modification_permitted`
- `verified_by`
- `verified_at`
- `authored_by`
- `superseded_by`
- `provenance`

Required v1.2 rules:

- Smithsonian CC0 institutional strategy requires `cc0_declaration_url`.
- IA-sourced content cannot use automated rights verification and cannot rely solely on IA
  `dc:rights`.
- Rights statement URI limited to governed vocabulary.

#### `media_technical_metadata`

Must include:

- `source_item_id`
- `media_type_id`
- `schema_version`
- `content`
- `validation_status`
- `validated_by`
- `validated_at`
- `validator_name`
- `validator_version`
- `content_hash`
- `superseded_by`
- `provenance`

Required v1.2 rules:

- Worker-level validation only; no `pg_jsonschema` dependency.
- Phase 1 content must support TGM subject terms.
- Non-TGM terms must be tagged `controlled_vocabulary: false`.
- Europeana image baseline must be evaluated: longest edge under 400px gets
  `quality_flag: 'below_minimum'`.

#### `preservation_event`

Must include:

- `subject_type`
- `subject_id`
- `media_file_id`
- `media_derivative_id`
- `event_type`
- `event_datetime`
- `event_outcome`
- `event_detail`
- `agent_type`
- `agent_id`

Required v1.2 rules:

- Append-only.
- LOC bulk BagIt verification represented in `event_detail`.
- Europeana missing minimum fields represented as `rights_verification` warning.
- Audio/BWF sequence is registered for future Phase 2/3, not enforced for active M36 media.

#### `asset_delivery_manifest`

Must include:

- `source_item_id`
- `media_type_id`
- `delivery_protocol`
- `primary_endpoint`
- `manifest_payload`
- `manifest_payload_hash`
- `generated_at`
- `generated_by`
- `published_at`
- `invalidated_at`
- `triggering_derivative_id`
- `media_rights_id`
- `technical_metadata_id`
- `superseded_by`
- `provenance`

Required v1.2 rules:

- IIIF manifest for Phase 1 active media.
- One active manifest per source item.
- No manifest before `activation_eligible`.
- Primary endpoint immutable after publication.

#### `activation_target`

Must include:

- `source_item_id`
- `status`
- `nominated_by`
- `nominated_at`
- `approved_by`
- `approved_at`
- `media_rights_id_at_approval`
- `technical_metadata_id_at_approval`
- `rejection_reason`
- `escalation_reason`
- `provenance`

Required v1.2 rules:

- Approval atomically pins current rights and technical metadata.
- Second-human rule.
- One nominated/approved activation target per source item.
- Retraction requires Director Decision in provenance.

#### `activation_target_downstream_link`

Must include:

- `activation_target_id`
- `downstream_type`
- `downstream_id`
- `created_at`
- `created_by`
- `provenance`

M36 value:

- `downstream_type = 'illustration_opportunity'`

This avoids mutating the frozen downstream tables.

## Data Migration Sequence

| Step | Data action | Notes |
|---:|---|---|
| 1 | Seed all vocabulary rows. | Values exactly match constitution. |
| 2 | Seed Phase 1 `media_type_registry` rows as active. | Use governance/system author identity; approval metadata must satisfy second-human rule. |
| 3 | Seed Phase 2–4 `media_type_registry` rows as pending. | Include future content schemas but block ingestion. |
| 4 | Backfill source institution references only where `sources.governance_state = 'active'`. | No new source activation in M36 backfill. |
| 5 | Backfill `source_item` rows for existing BHL/LOC Phase 1 records with source evidence. | Do not infer missing source identifiers. |
| 6 | Backfill `source_record` snapshots from existing provenance/source metadata. | Store as normalized historical payload if raw unavailable; mark provenance clearly. |
| 7 | Backfill `media_rights` only for explicit Public Domain/CC0 records. | Do not backfill ambiguous rights. |
| 8 | Backfill `media_technical_metadata` from existing image dimensions/quality where present. | Worker validation evidence required. |
| 9 | Backfill `media_file` only where MinIO object/checksum evidence exists. | No checksum, no media_file. |
| 10 | Backfill `activation_target` as `nominated` only if a governed backfill policy exists. | Do not auto-approve historical records. |
| 11 | Create downstream links only for approved activation targets. | Likely none in first backfill unless human workflow runs. |
| 12 | Generate Phase 1 IIIF manifests only for `activation_eligible` or `activated` source items. | Respect manifest gate. |

Data migration policy:

- Evidence-only backfill is safe.
- Approval backfill is unsafe without human review.
- Historical commerce replay must not be rewritten.

## Replay Test Matrix

| Area | Test | Expected result |
|---|---|---|
| Registry | Phase 1 rows active, Phase 2–4 pending. | Only Phase 1 can ingest. |
| Registry | Attempt Phase 2 activation without amendment. | Blocked. |
| Registry | Attempt to change active archival format/protocol. | Blocked. |
| Source record | Update raw payload after insert. | Blocked. |
| Source record | Re-fetch changed payload. | New source_record; current FK updated. |
| Source record | Europeana EDM missing required fields. | `rights_verification` warning before rights review. |
| Source record | Rights contradiction on re-fetch. | New `under_review` rights record; warning event; advancement halted. |
| Rights | Mutate verified rights evidence. | Blocked. |
| Rights | Smithsonian CC0 without `cc0_declaration_url`. | Verification blocked. |
| Rights | IA rights from `dc:rights` only. | Verification blocked. |
| Technical metadata | Invalid worker validation status linked as current. | Blocked. |
| Technical metadata | Phase 1 non-TGM subject term. | Allowed only with `controlled_vocabulary: false`. |
| Technical metadata | Visual longest edge under 400px. | `quality_flag: 'below_minimum'`. |
| Preservation | Update preservation event. | Blocked. |
| Preservation | Delete preservation event. | Blocked. |
| Preservation | WORM file overwritten after ingestion event. | Blocked. |
| Preservation | LOC bulk transfer without BagIt verification. | Integrity violation. |
| Derivatives | Regenerate derivative. | New derivative + normalization/fixity events. |
| Manifest | Generate manifest before `activation_eligible`. | Blocked. |
| Manifest | Publish then change primary endpoint. | Blocked unless redirect policy exists. |
| Manifest | Phase 1 IIIF manifest payload invalid. | Manifest generation fails. |
| Activation | Nominate before `activation_eligible`. | Blocked. |
| Activation | Approver equals nominator. | Blocked. |
| Activation | Approval pins wrong/current-stale rights ID. | Blocked by transactional row lock test. |
| Activation | Duplicate approved downstream link. | Blocked. |
| Retraction | `activated → retracted` without Director Decision. | Blocked. |
| Legacy replay | Pre-M36 commerce record lacks substrate anchors. | Replay still valid. |
| Post-M36 replay | New score uses substrate activation target. | Score inputs include source, rights, technical metadata anchors. |
| Pending media | Ingest `book`, `audio`, `dataset`, or `3d`. | Blocked in M36. |

## Worker Sequence

Workers should be introduced in this order.

| Order | Worker | Purpose | M36 phase |
|---:|---|---|---|
| 1 | `media_type_registry_seed_worker` | Seed and verify registry/vocabularies. | Foundation |
| 2 | `source_acquisition_worker` | Create source items and source records. | Phase 1 |
| 3 | `reference_rule_evaluation_worker` | Apply v1.2 LOC/Europeana/Smithsonian/IA rules. | Phase 1 |
| 4 | `media_file_ingestion_worker` | Store files, compute SHA-256, write ingestion events. | Phase 1 |
| 5 | `media_rights_worker` | Create pending/verified/under-review rights records under governance. | Phase 1 |
| 6 | `media_technical_metadata_worker` | Extract and validate technical metadata. | Phase 1 |
| 7 | `media_derivative_worker` | Generate Phase 1 delivery and thumbnail derivatives. | Phase 1 |
| 8 | `asset_delivery_manifest_worker` | Generate IIIF/JSON-LD manifests. | Phase 1 |
| 9 | `activation_target_worker` | Nominate activation targets; execute human-approved transition. | Phase 1 |
| 10 | `substrate_replay_worker` | Verify replay anchors and historical reconstruction. | Phase 1 |
| 11 | `fixity_check_worker` | Scheduled WORM fixity verification. | Operations |

### Adapter Priority

| Priority | Adapter | Reason |
|---:|---|---|
| 1 | LOC | Primary Phase 1 source for image, map, photography, poster and Tier 1 rules. |
| 2 | Smithsonian | CC0 verification and future 3D reference; Phase 1 still images. |
| 3 | Europeana | Aggregator/source-record warning and EDM rule coverage. |
| 4 | Internet Archive | File-manifest and WORM model; rights automation prohibited. |

## Activation Sequence

### M36 Active Sequence

Only Step 1 of the v1.2 constitutional sequence is active in M36:

```text
image + map + photography + poster
```

These may activate concurrently.

Runtime path for each Phase 1 media type:

```text
source_item proposed
  -> source_record inserted
  -> media_file ingested
  -> preservation_event ingestion/validation written
  -> source_item acquired
  -> media_rights verified_pd or verified_cc0
  -> source_item rights_verified
  -> media_technical_metadata valid
  -> source_item activation_eligible
  -> media_derivative delivery generated
  -> asset_delivery_manifest generated
  -> activation_target nominated
  -> activation_target approved
  -> source_item activated
  -> activation_target_downstream_link created
  -> existing commerce pipeline can consume downstream opportunity
```

### Future Activation Sequence

M36 must seed but not activate future rows in this total order:

| Future order | Type(s) | Activation precondition |
|---:|---|---|
| 2 | `book` + `ebook` | Phase 1 complete; P2-1 ratified; table rename completed. |
| 3 | `audiobook` | `book` active and one book source item activated. |
| 4 | `audio` | `audiobook` active and one audiobook source item activated; P3-1 ratified. |
| 5 | `film` | `audio` active and one audio source item activated. |
| 6 | `dataset` | Phase 3 complete; P4-1 ratified. |
| 7 | `3d` | `dataset` active and one dataset source item activated. |

## Media Type Engineering Matrix

| Media type | M36 registry | M36 ingestion | M36 activation | Runtime profile | Future work |
|---|---|---|---|---|---|
| `image` | Active | Yes | Yes | Single-canvas IIIF + Image API | None for substrate. |
| `map` | Active | Yes | Yes | Single-canvas IIIF + Image API + geographic metadata | Map-specific scoring remains downstream. |
| `photography` | Active | Yes | Yes | Single-canvas IIIF + Image API | Photography authority seeding downstream. |
| `poster` | Active | Yes | Yes | Single-canvas IIIF + Image API + TGM terms | Cultural anchor review downstream. |
| `book` | Pending | No | No | Multi-canvas IIIF registered | P2-1 + rename. |
| `ebook` | Pending | No | No | EPUB3 profile registered | P2-1 + download/publication governance. |
| `audiobook` | Pending | No | No | Track sequence profile registered | Book pipeline proven first. |
| `audio` | Pending | No | No | BWF/HTML5 audio registered | P3-1. |
| `film` | Pending | No | No | FFV1/HLS registered | P3-1. |
| `dataset` | Pending | No | No | DCAT/Schema.org Dataset registered | P4-1. |
| `3d` | Pending | No | No | Smithsonian X 3D/glTF registered | Dataset pipeline proven first. |

## Estimated Implementation Effort

Assumes one senior engineer, one backend engineer, one QA/data engineer, and part-time curator
availability for rights workflow review.

| Workstream | Effort |
|---|---:|
| SQL DDL and trigger suite | 8-12 engineering days |
| Registry seeding and vocabulary fixtures | 2-3 engineering days |
| LOC Phase 1 adapter | 6-10 engineering days |
| Smithsonian Phase 1 adapter | 5-8 engineering days |
| Europeana reference-rule adapter | 4-6 engineering days |
| Internet Archive manifest/reference adapter | 4-6 engineering days |
| Media file ingestion + MinIO/fixity integration | 7-10 engineering days |
| Rights workflow and Article 7.7 inconsistency checks | 6-9 engineering days |
| Technical metadata worker + validation evidence | 5-8 engineering days |
| Derivative and IIIF manifest generation | 7-12 engineering days |
| Activation workflow and downstream link | 5-8 engineering days |
| Replay worker/tests | 7-10 engineering days |
| Compatibility backfill tooling | 4-8 engineering days |
| Documentation and operator runbooks | 2-4 engineering days |

Estimated total:

- Minimal Phase 1 M36: 8-10 calendar weeks.
- Full Phase 1 with all four reference adapters and replay coverage: 12-16 calendar weeks.

## Highest-Risk Areas

| Risk | Severity | Why it matters | Mitigation |
|---|---|---|---|
| Activation approval race condition | Critical | Wrong rights/technical metadata pins break replay. | Single transaction; row locks on `source_item`; approval trigger sets pins. |
| Rights inconsistency detection | Critical | New source metadata can invalidate verified rights. | Dedicated Article 7.7 worker tests and warnings. |
| IA rights self-assertion | High | IA metadata is not rights authority under v1.2. | Hard-code prohibition in rights worker and tests. |
| Smithsonian CC0 evidence completeness | High | CC0 verification requires `cc0_declaration_url`. | Rights schema validation and tests. |
| Phase 2–4 accidental ingestion | High | Violates activation sequence and rename deadline. | DB trigger blocks pending media type ingestion. |
| `asset_delivery_manifest` endpoint immutability | High | Broken public endpoints damage public delivery. | Published endpoint immutability trigger. |
| WORM file immutability | High | Preservation trust depends on it. | MinIO key uniqueness + DB WORM trigger + fixity tests. |
| Backfill overreach | High | Historical rows could appear newly approved. | Evidence-only backfill; no auto-approved activation. |
| Europeana aggregator authority confusion | Medium | Aggregator records are not direct source authority. | Source relationship modeling and warning tests. |
| LOC BagIt handling | Medium | Bulk transfers require checksum verification. | Event detail enforcement for transfer method. |
| Worker-level schema validation | Medium | DB does not prove JSON Schema conformance. | Persist validator metadata; negative tests; CI fixtures. |

## Recommended Execution Order

1. Ratify implementation branch decision: M36 is Phase 1 only.
2. Implement DDL through M36-018 with no workers.
3. Run SQL constraint and trigger tests.
4. Seed registry and assert activation sequence.
5. Build source acquisition and reference-rule worker for LOC first.
6. Build media file ingestion and preservation events.
7. Build rights worker and human review workflow.
8. Build technical metadata worker for Phase 1 visuals.
9. Build derivative and IIIF manifest workers.
10. Build activation target workflow and downstream link.
11. Add Smithsonian adapter.
12. Add Europeana rule adapter.
13. Add Internet Archive reference adapter.
14. Add replay worker and replay tests.
15. Add compatibility backfill tooling.
16. Run end-to-end LOC map/photo/poster/image fixtures.
17. Run Smithsonian CC0 fixture.
18. Run Europeana EDM warning fixture.
19. Run IA rights-block fixture.
20. Only after all replay tests pass, allow Phase 1 activation in production.

## Final Engineering Position

M36 v2 should implement the full substrate table set, seed all media contracts, and activate only
Phase 1 visual media. It should not attempt Phase 2 books/eBooks, audio, film, datasets, or 3D.

The engineering priority is replayable trust:

- immutable source records
- immutable/versioned rights
- WORM file evidence
- worker-validated technical metadata
- governed delivery manifests
- activation approval pins
- compatibility links that leave the downstream platform frozen

That delivers a future-proof substrate without redesigning Commerce, Routing, Catalog,
Publication, or Asset Intelligence.
