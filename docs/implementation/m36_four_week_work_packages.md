# M36 Four-Week Implementation Plan

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Basis | `m36_engineering_specification_v2.md` |
| Scope | Executable work packages |
| Activation | Phase 1 only: `image`, `map`, `photography`, `poster` |

## Mission

Convert the M36 Engineering Specification v2 into four weeks of ordered executable work packages.

The plan assumes M36 remains additive and keeps Commerce Intelligence, Product Routing, Catalog,
Publication, and Asset Intelligence frozen.

## Week 1 — Database Contract

Goal: land the M36 substrate schema, seed contracts, and prove hard database invariants before any
worker code is trusted.

### Exact Order

1. Create M36 migration branch and freeze scope.
   - Confirm M36 is Phase 1 only.
   - Confirm Phase 2–4 media types are registry-only.
   - Confirm no rename of `illustration_opportunities`.

2. Implement `M36-001` vocabulary tables.
   - Media type status.
   - Source item status.
   - Source record schema standards.
   - Media file roles.
   - Media derivative roles.
   - Media rights status.
   - Preservation event types/outcomes/agents.
   - Activation target status.
   - Delivery protocols.

3. Implement `M36-002` `media_type_registry`.
   - Add immutability triggers.
   - Add no-DELETE rule.
   - Add active-row second-human constraints.

4. Implement `M36-003` registry seeds.
   - Active: `image`, `map`, `photography`, `poster`.
   - Pending: `book`, `ebook`, `audiobook`, `audio`, `film`, `dataset`, `3d`.
   - Add tests blocking pending media ingestion.

5. Implement `M36-004` `source_item` shell.
   - Current FKs nullable for now.
   - Add source identity uniqueness.
   - Add no-DELETE rule.

6. Implement `M36-005` `source_record`.
   - Standalone table.
   - Raw payload immutability.
   - Schema standard FK/check.
   - Duplicate hash protection.

7. Implement `M36-006` `media_rights`.
   - Standalone versioned table.
   - Verified/blocked immutability.
   - Rights URI constraints.

8. Implement `M36-007` `media_technical_metadata`.
   - Worker validation evidence fields.
   - Schema version pin.
   - Content hash.

9. Implement `M36-008` current FK wiring on `source_item`.
   - `current_source_record_id`.
   - `current_media_rights_id`.
   - `current_technical_metadata_id`.

10. Implement first SQL test suite.
    - Registry seed posture.
    - Active field immutability.
    - Pending type ingestion block.
    - Source record immutability.
    - Verified rights immutability.
    - Current FK integrity.

### Week 1 Exit Criteria

- All registry and core acquisition tables exist.
- Phase 1 active / Phase 2–4 pending is enforced.
- Immutable source records and verified rights cannot be altered.
- No worker implementation is required to pass Week 1.

## Week 2 — Files, Preservation, Rights, Metadata

Goal: prove that a Phase 1 source item can be acquired, file-backed, rights-reviewed, and made
technically eligible without touching downstream Commerce.

### Exact Order

1. Implement `M36-009` `media_file`.
   - SHA-256 required.
   - WORM file roles.
   - MinIO key pattern checks.
   - Pending ingestion state.

2. Implement `M36-010` `media_derivative`.
   - Delivery and thumbnail roles.
   - Derivative-to-master chain.
   - Regeneration support through `superseded_by`.

3. Implement `M36-011` `preservation_event`.
   - Append-only rule.
   - No UPDATE.
   - No DELETE.
   - Deletion requires Director Decision.

4. Implement `M36-012` file-event integrity.
   - Ingestion event must exist before WORM finalization.
   - Controlled update allowed only to attach `ingestion_event_id`.

5. Build `source_acquisition_worker` skeleton.
   - Create `source_item`.
   - Insert immutable `source_record`.
   - Update current source record FK.
   - Reject pending media types.

6. Build LOC Phase 1 adapter first.
   - Support `image`, `map`, `photography`, `poster`.
   - Store raw payload.
   - Record schema standard.
   - Do not score or route.

7. Build `reference_rule_evaluation_worker`.
   - LOC TGM subject-term handling.
   - LOC BagIt/API transfer event detail handling.
   - Europeana EDM minimum-field warning behavior.
   - Smithsonian CC0 evidence requirement.
   - IA rights self-assertion prohibition.

8. Build `media_file_ingestion_worker`.
   - Store/fetch file evidence.
   - Compute checksum.
   - Write ingestion, format identification, validation events.
   - Advance `proposed → acquired`.

9. Build `media_rights_worker`.
   - Create `pending`.
   - Create `verified_pd` / `verified_cc0` only under authorized strategy or human workflow.
   - Create `under_review` on Article 7.7 inconsistency.
   - Write rights verification preservation events.

10. Build `media_technical_metadata_worker`.
    - Extract Phase 1 image/map/photo/poster technical fields.
    - Validate against registry schema in worker.
    - Persist validator name/version/schema version/content hash.
    - Add TGM and Europeana quality flags.
    - Advance `rights_verified → activation_eligible`.

11. Implement Week 2 replay/constraint tests.
    - WORM file cannot change after ingestion.
    - Preservation event append-only.
    - Article 7.7 rights inconsistency creates `under_review`.
    - IA rights-only evidence cannot verify.
    - Smithsonian CC0 missing `cc0_declaration_url` cannot verify.
    - Invalid technical metadata cannot become current.

### Week 2 Exit Criteria

- A LOC Phase 1 item can reach `activation_eligible`.
- Rights and technical metadata are replay-pinned.
- File evidence is checksum-backed.
- Article 7.7 and v1.2 reference-institution rules are enforced.

## Week 3 — Delivery, Activation, Compatibility

Goal: generate governed delivery manifests, approve activation targets, and link to the existing
downstream pipeline without changing downstream schemas.

### Exact Order

1. Implement `M36-013` `asset_delivery_manifest`.
   - One active manifest per source item.
   - No manifest before `activation_eligible`.
   - Published endpoint immutability.
   - Manifest versioning through `invalidated_at`.

2. Implement `M36-014` `activation_target`.
   - Nomination only for `activation_eligible`.
   - Second-human rule.
   - One nominated/approved target per source item.
   - Atomic approval pins `media_rights_id_at_approval` and
     `technical_metadata_id_at_approval`.
   - Retraction requires Director Decision.

3. Implement `M36-015` `activation_target_downstream_link`.
   - Link approved target to exactly one downstream record.
   - `downstream_type = 'illustration_opportunity'`.
   - Immutable after insert.

4. Implement `M36-016` final trigger suite.
   - Status transitions.
   - Pending media type block.
   - Second-human approvals.
   - Activation approval transaction constraints.
   - Manifest endpoint immutability.
   - Retraction Director Decision check.

5. Implement `M36-017` index suite.
   - Source lookup indexes.
   - Current FK indexes.
   - Replay anchor indexes.
   - Active manifest partial index.
   - Active/nominated activation target partial index.

6. Implement `M36-018` read-only compatibility views.
   - Substrate-to-opportunity view.
   - Activation replay view.
   - Manifest delivery inspection view.
   - No writable compatibility views.

7. Build `media_derivative_worker`.
   - Generate Phase 1 delivery derivatives.
   - Generate thumbnails.
   - Write normalization and fixity events.

8. Build `asset_delivery_manifest_worker`.
   - Generate IIIF Presentation API 3.0 manifest.
   - Include IIIF Image API service when derivative exists.
   - Generate JSON-LD-compatible payload.
   - Store manifest hash.

9. Build `activation_target_worker`.
   - Nominate eligible item.
   - Expose human approval transaction.
   - Approve with row lock on `source_item`.
   - Create downstream link after downstream record exists.

10. Implement Week 3 tests.
    - Manifest cannot generate before `activation_eligible`.
    - One active manifest per source item.
    - Published endpoint cannot change.
    - Activation before eligibility blocked.
    - Approver equals nominator blocked.
    - Approval pins current rights and technical metadata IDs.
    - Duplicate downstream link blocked.
    - Existing Commerce replay does not require substrate IDs.

### Week 3 Exit Criteria

- A Phase 1 item can move from `activation_eligible` to approved `activation_target`.
- IIIF/JSON-LD delivery manifest exists.
- Downstream compatibility link exists.
- No frozen downstream table has been redesigned.

## Week 4 — Replay, Backfill, Reference Fixtures, Release Gate

Goal: prove replay, run safe compatibility backfill, exercise reference-institution fixtures, and
prepare the release gate.

### Exact Order

1. Build `substrate_replay_worker`.
   - Reconstruct activation state from source record, rights, technical metadata, file,
     derivative, manifest, preservation events, and approval pins.
   - Verify no external refetch is needed.

2. Build `fixity_check_worker`.
   - Verify WORM SHA-256.
   - Write `fixity_check` preservation events.
   - Escalate failures.

3. Build compatibility backfill tooling.
   - Backfill evidence only.
   - No auto-approved activation targets.
   - No rewrite of historical `commerce_opportunities.score_inputs`.
   - No inference of missing source identifiers.

4. Run LOC end-to-end fixtures.
   - Image.
   - Map.
   - Photography.
   - Poster.
   - API transfer event detail.
   - BagIt bulk-transfer warning/verification path if fixture exists.

5. Run Smithsonian fixture.
   - CC0 evidence includes `cc0_declaration_url`.
   - Missing declaration blocks `verified_cc0`.

6. Run Europeana fixture.
   - EDM source record.
   - Missing `dc:title`, `dc:description`, `dc:date`, or `edm:rights` creates warning.
   - Under-400px visual gets `quality_flag: 'below_minimum'`.

7. Run Internet Archive fixture.
   - `dc:rights` alone cannot verify rights.
   - Human verification required.
   - WORM philosophy still applies to master file.

8. Run full replay matrix.
   - Source record replay.
   - Rights replay.
   - Technical metadata replay.
   - Preservation replay.
   - Manifest replay.
   - Activation replay.
   - Legacy replay.
   - Pending media block.

9. Run backfill dry run.
   - Report eligible evidence rows.
   - Report skipped rows and reasons.
   - Confirm no approval records created.

10. Run release gate.
    - SQL constraints green.
    - Worker unit tests green.
    - Replay tests green.
    - Reference fixtures green.
    - Compatibility backfill dry run green.
    - No downstream schema redesign detected.

11. Prepare operator runbook.
    - Phase 1 activation flow.
    - Rights review flow.
    - Manifest regeneration flow.
    - Fixity failure response.
    - Article 7.7 rights inconsistency response.

12. Prepare GO / NO-GO release memo.
    - GO only if all Week 4 release gates pass.
    - NO-GO if any Phase 2–4 ingestion path exists.
    - NO-GO if activation approval pins are not atomic.
    - NO-GO if legacy replay is broken.

### Week 4 Exit Criteria

- Substrate replay is proven.
- Reference-institution rules are tested.
- Backfill is evidence-only and safe.
- Phase 1 M36 is ready for production release decision.

## Final Four-Week Order

1. Week 1: SQL foundation and immutable core.
2. Week 2: acquisition, file evidence, rights, technical metadata.
3. Week 3: derivatives, manifests, activation, compatibility link.
4. Week 4: replay, backfill, reference fixtures, release gate.

Do not start Week 2 worker work until Week 1 database invariants pass. Do not start Week 3
activation work until Week 2 proves `activation_eligible`. Do not release until Week 4 proves
replay and legacy compatibility.
