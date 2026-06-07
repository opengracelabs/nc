# Universal Media Substrate Runtime v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Status | Runtime design |
| Migration | UMS M36 |
| Basis | Universal Media Substrate Constitution v1.0 |
| Scope | Design only — no implementation |

## Mission

Design the Migration 36 runtime for the Universal Public Domain Media Substrate so Nature &
Culture can support these media types without future platform redesign:

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

The runtime must keep these downstream layers frozen:

- Commerce Intelligence
- Product Routing
- Catalog
- Publication
- Asset Intelligence

## Runtime Conclusion

M36 should introduce a substrate layer upstream of the existing commercial spine. It should not
rename `illustration_opportunities`, should not change Commerce scoring formulas, and should not
make Phase 2–4 media types commercially active.

The runtime boundary is:

```text
source institution / aggregator
  -> source_item
  -> source_record
  -> media_file
  -> media_derivative
  -> media_rights
  -> media_technical_metadata
  -> preservation_event
  -> activation_target
  -> illustration_opportunities compatibility bridge
  -> existing Commerce / Product Routing / Catalog / Publication / Asset Intelligence
```

The design principle is simple:

> Normalize source, file, rights, and technical complexity before Commerce sees anything.

## Migration Numbering Note

`docs/governance/commerce_execution_constitution_v1.0.md` previously reserved an M-36 for Commerce
Execution, but that section states implementation of M-35 through M-37 is not authorized until
ratification. `docs/governance/media_substrate_constitution_v1.0.md` is ratified and explicitly
authorizes Migration 36.

Runtime naming should therefore use `UMS M36` in documentation and implementation comments. If
Commerce Execution is later ratified, its migration sequence should be renumbered or namespaced to
avoid collision.

## Open Question Resolutions

The Constitution defers four implementation choices to M36. Runtime v1 resolves them as follows:

| Open question | Runtime decision | Reason |
|---|---|---|
| OQ-1: `source_record` physical realization | Use a separate immutable `source_record` table. | Required for replay, versioning, source refetch history, and aggregator/source-of-record separation. |
| OQ-2: `media_rights` physical realization | Use a separate versioned `media_rights` table. | Rights history must survive re-investigation and must be pinned by activation and replay. |
| OQ-3: `content_spec_schema` validation | Prefer PostgreSQL validation through `pg_jsonschema` or equivalent. If unavailable, enforce worker validation and store validation result/hash in PostgreSQL. | Strongest model is database enforcement; fallback preserves deployability without weakening replay because validated schema version is still pinned. |
| OQ-4: rename `illustration_opportunities` | Do not rename in M36. | Rename would require coordinated amendments across five downstream constitutions. M36 uses a compatibility bridge instead. |

## Reference Model Alignment

| Reference | Runtime role |
|---|---|
| Library of Congress | Source authority model for MARC/MODS records, maps, photography, posters, image service, linked data, and rights evidence. |
| Europeana | Aggregator/source-of-record separation model: provider object, aggregation, web resource, rights/provider normalization. |
| Internet Archive | Item/file manifest model for broad media packages, books, eBooks, audio, film, and arbitrary derivatives. |
| Smithsonian | CC0 open access and 3D object/media package model. |
| IIIF Presentation API 3.0 | Manifest/canvas model for images, maps, posters, books, page sequences, and AV canvases. |
| IIIF Image API | Tile/image delivery model for Phase 1 visual media and page images. |
| JSON-LD | Public semantic output, Schema.org alignment, linked data graph projection, and source payload validation where applicable. |

## M36 Runtime Objects

### `media_type_registry`

Governs supported media types, activation phase, archival format, delivery protocol, delivery
format, manifest requirement, and content schema.

M36 seed posture:

| media type | Phase | M36 status | Runtime authorization |
|---|---:|---|---|
| `image` | 1 | `active` | Ingest and activate after rights/technical gates. |
| `map` | 1 | `active` | Ingest and activate after rights/technical gates. |
| `photography` | 1 | `active` | Ingest and activate after rights/technical gates. |
| `poster` | 1 | `active` | Ingest and activate after rights/technical gates. |
| `book` | 2 | `pending` | Register only. No ingestion/activation until amendment. |
| `ebook` | 2 | `pending` | Register only. No ingestion/activation until amendment. |
| `audiobook` | 2 | `pending` | Register only. No ingestion/activation until amendment. |
| `audio` | 3 | `pending` | Register only. No ingestion/activation until amendment. |
| `film` | 3 | `pending` | Register only. No ingestion/activation until amendment. |
| `3d` | 4 | `pending` | Register only. No ingestion/activation until amendment. |
| `dataset` | 4 | `pending` | Register only. No ingestion/activation until amendment. |

This is how M36 supports every future type without activating every type.

### `source_item`

The acquisition-side atomic work. It is the source-side intellectual object, not a file and not a
commerce record.

Runtime rules:

- One `source_item` per institution-native item/object/work.
- Current source, rights, and technical metadata are pinned through FKs.
- `source_item.status` enforces the substrate lifecycle.
- A `source_item` may have at most one active or nominated `activation_target`.
- Phase 1 compatibility may create a `source_item` linked to an existing
  `illustration_opportunities` row, but the legacy row remains the downstream commerce anchor.

### `source_record`

Immutable metadata snapshot.

Runtime rules:

- Store raw source payload verbatim.
- Store schema standard: `marc`, `edm`, `lido`, `dc`, `mods`, `oai_pmh`, `schema_org`, `bhl_api`.
- Store normalized payload separately.
- New source fetch means new `source_record`; never mutate old payloads.
- `source_item.current_source_record_id` points at the current version.

Reference model mapping:

- LOC: MARC/MODS/linked data payloads.
- Europeana: EDM provider/aggregation payloads.
- Internet Archive: Dublin Core-ish item metadata plus file manifest.
- Smithsonian: object metadata and open access media payload.

### `media_file`

WORM or governed physical file in MinIO.

Runtime rules:

- Every file has SHA-256.
- Every file has one constitutional role: `master`, `page`, `track`, `segment`, `model`, `data`.
- Every WORM file must have an ingestion `preservation_event`.
- Multi-file media packages use `sequence_position`.
- The file graph supports Internet Archive-style items and IIIF page sequences without changing
  the core model.

### `media_derivative`

Delivery or preview file derived from a master file.

Runtime rules:

- Derivatives reference a source `media_file`.
- Derivatives are regenerable and versioned by preservation events.
- IIIF delivery derivatives are generated only for active Phase 1 visual types in M36.
- Phase 2–4 derivative types are registered as future policy concepts, not runtime activation.

### `media_rights`

Versioned rights determination for `source_item`.

Runtime rules:

- Only `verified_pd` and `verified_cc0` permit pipeline entry.
- `verified_pd`, `verified_cc0`, and `blocked` records are immutable.
- Re-investigation creates a new rights record.
- `activation_target` pins the exact `media_rights.id` used at approval time.
- Automated verification is permitted only for explicitly authorized rights strategies.

### `media_technical_metadata`

Validated technical description of the source item under the active `media_type_registry`
`content_spec_schema`.

Runtime rules:

- One current record per `source_item`.
- Each record stores schema version.
- Each record is immutable once superseded.
- Commerce replay must pin the technical metadata ID when scoring uses its fields.

### `preservation_event`

Append-only PREMIS/PROV-aligned file lifecycle log.

Runtime rules:

- No UPDATE.
- No DELETE.
- Every file ingestion, validation, normalization, fixity check, rights verification, migration,
  replication, or deletion is recorded.
- Deletion events require Director Decision and human agent.

### `activation_target`

The bridge between substrate and commercial pipeline.

Runtime rules:

- Created only for `source_item.status = 'activation_eligible'`.
- Approved only by second human.
- Approved target authorizes exactly one downstream pipeline record.
- Phase 1 downstream physical target remains `illustration_opportunities`.
- `activation_target.id` must be stored on the downstream opportunity record or in a compatibility
  link table.

### `asset_delivery_manifests`

Runtime support table required by Article 18.

Purpose:

- Stores IIIF Presentation API 3.0 manifests and JSON-LD public delivery payloads.
- Keeps delivery documents versioned and replayable.
- Separates manifest generation from source acquisition.

Runtime rules:

- One current manifest per `source_item` and delivery profile.
- Manifests are regenerated when derivatives or public metadata change.
- Prior manifest payloads remain available for replay/audit.
- Manifest generation never changes source records, rights records, or activation decisions.

## IIIF Runtime Strategy

M36 should treat IIIF as the canonical delivery model for active Phase 1 media types.

### Single-Canvas IIIF

Applies to:

- `image`
- `map`
- `photography`
- `poster`

Runtime output:

- One IIIF Presentation API 3.0 Manifest.
- One Canvas.
- One painting Annotation.
- Annotation body references a IIIF Image API service when a tiled derivative exists.
- Rights URI comes from the pinned active `media_rights`.
- JSON-LD context is valid and stable.

### Multi-Canvas IIIF

Registered in M36 but not activated for commerce.

Applies later to:

- `book`
- page-image eBook forms
- manuscript-like sequences

Runtime output:

- One Manifest.
- One Canvas per `media_file` with role `page`.
- Canvas order from `sequence_position`.
- OCR/text annotations from page-level derivatives.

### AV Canvas

Registered in M36 but pending activation.

Applies later to:

- `audiobook`
- `audio`
- `film`

Runtime output:

- Canvas with duration.
- Audio or video body.
- Optional transcript/caption annotations.
- Clip ranges represented as annotations.

### 3D and Dataset JSON-LD

M36 registers these types but does not require active delivery runtime.

Future posture:

- 3D uses JSON-LD + delivery protocol `model-viewer`.
- Dataset uses JSON-LD + Schema.org `Dataset` and direct download profile.
- Both may be linked from IIIF manifests through `seeAlso`, `rendering`, or annotation patterns
  only after media type activation.

## JSON-LD Runtime Strategy

Every public manifest or delivery document should be JSON-LD compatible.

Schema.org mapping:

| media type | Schema.org type |
|---|---|
| `image` | `schema:ImageObject` or `schema:VisualArtwork` |
| `map` | `schema:Map` |
| `photography` | `schema:ImageObject` or `schema:Photograph` when supported by vocabulary/profile |
| `poster` | `schema:VisualArtwork` or `schema:ImageObject` |
| `book` | `schema:Book` |
| `ebook` | `schema:Book` |
| `audiobook` | `schema:Audiobook` |
| `audio` | `schema:AudioObject` |
| `film` | `schema:Movie` or `schema:VideoObject` |
| `3d` | `schema:3DModel` |
| `dataset` | `schema:Dataset` |

JSON-LD output must reference:

- canonical NC URL
- source institution
- source item identifier
- rights statement URI
- creator/contributor when known
- source record provenance
- delivery manifest or file URL
- derivative checksum where public export requires it

## Source Adapter Runtime

Adapters are source-specific at the edge and generic at the substrate boundary.

Adapter responsibilities:

1. Fetch source payload.
2. Create or locate `source_item`.
3. Insert immutable `source_record`.
4. Discover media files and file manifests.
5. Store master files in MinIO.
6. Insert `media_file`.
7. Insert ingestion and validation `preservation_event` records.
8. Propose or attach `media_rights`.
9. Extract `media_technical_metadata`.
10. Propose `activation_target` if gates pass.

Adapters are forbidden to:

- create Commerce scores
- create Product Routing recommendations
- approve activation targets
- bypass rights verification
- rewrite source records
- treat aggregator payloads as source-of-record evidence when a provider record is available

### LOC Adapter Shape

Primary M36 source for active Phase 1.

Supports:

- image
- map
- photography
- poster

Source record standards:

- MARC/MODS/LOC JSON payloads.
- Linked data authority references when available.

Delivery:

- IIIF Image API where available.
- NC-generated delivery derivative otherwise.

### Europeana Adapter Shape

M36 role: aggregator and reconciliation reference, not commercial source-of-record by default.

Supports:

- discovery
- EDM normalization
- provider/source linking
- rights anomaly detection

Activation rule:

- Do not approve an activation target solely on Europeana aggregation unless direct source
  confirmation is unavailable and Director Decision authorizes the specific strategy.

### Internet Archive Adapter Shape

M36 role: future package/file-manifest model. Phase 2–4 media types remain pending.

Supports:

- item/file manifest normalization design
- books/eBooks/audio/film registration only
- no broad commercial activation in M36

Activation rule:

- Only Phase 1 image-like records can activate in M36, and only if source-of-record and rights
  evidence satisfy the Constitution.

### Smithsonian Adapter Shape

M36 role: CC0 still-image candidate source and future 3D model guide.

Supports:

- image
- photography
- poster-like cultural objects where metadata supports it
- 3D registration as pending profile

Activation rule:

- 2D CC0 records may activate after rights and technical gates.
- 3D records remain discovery/pending until Phase 4 amendment.

## Media Type Runtime Matrix

| media type | M36 registry | M36 ingest | M36 activation | Delivery runtime | Future redesign needed? |
|---|---|---|---|---|---|
| `image` | active | yes | yes | IIIF Presentation + IIIF Image | No |
| `map` | active | yes | yes | IIIF Presentation + IIIF Image | No |
| `photography` | active | yes | yes | IIIF Presentation + IIIF Image | No |
| `poster` | active | yes | yes | IIIF Presentation + IIIF Image | No |
| `book` | pending | no, except legacy provenance references | no | Registered multi-canvas IIIF | No |
| `ebook` | pending | no | no | Registered EPUB/JSON-LD profile | No |
| `audiobook` | pending | no | no | Registered AV canvas/profile | No |
| `audio` | pending | no | no | Registered AV canvas/profile | No |
| `film` | pending | no | no | Registered AV canvas/profile | No |
| `3d` | pending | no | no | Registered model-viewer/JSON-LD profile | No |
| `dataset` | pending | no | no | Registered Schema.org Dataset/download profile | No |

The answer to "without future redesign" is: register every type and its validation/delivery
contract now, but activate only Phase 1. Future phases activate existing registry rows and profiles
by amendment rather than redesigning tables.

## Migration Strategy

### M36-A: Registry and Vocabulary Foundation

Create and seed:

- `media_type_registry`
- media type lifecycle vocabulary
- media file role vocabulary
- derivative role vocabulary
- rights status vocabulary
- preservation event type vocabulary
- delivery protocol vocabulary
- source record schema standard vocabulary
- activation target status vocabulary

Seed all eleven media types. Only Phase 1 types are `active`.

### M36-B: Source Identity and Source Records

Create:

- `source_item`
- `source_record`
- optional `source_relationship`

Runtime decision:

- Use `source_record` as a separate immutable table.
- Store `source_item.current_source_record_id`.
- Support source refetch by appending new source records.

### M36-C: File and Preservation Runtime

Create:

- `media_file`
- `media_derivative`
- `preservation_event`

Runtime decision:

- Enforce WORM behavior on master/page/track/segment/model/data roles.
- Enforce append-only preservation events.
- Enforce MinIO key convention by database validation and worker tests.

### M36-D: Rights Runtime

Create:

- `media_rights`

Runtime decision:

- Separate versioned table.
- `source_item.current_media_rights_id`.
- Immutable verified/blocked rights records.
- Activation impossible without `verified_pd` or `verified_cc0`.

### M36-E: Technical Metadata Runtime

Create:

- `media_technical_metadata`

Runtime decision:

- `source_item.current_technical_metadata_id`.
- Store schema version.
- Prefer PostgreSQL JSON Schema validation.
- If database extension is unavailable, worker validation must write validation hash, schema
  version, validator name, and validator version to the record.

### M36-F: Activation Runtime

Create:

- `activation_target`
- downstream compatibility reference, either:
  - nullable `activation_target_id` on `illustration_opportunities`, or
  - `activation_target_downstream_link` table if altering the downstream table is too invasive

Runtime decision:

- Prefer a link table for M36 to avoid downstream table mutation.
- Later migration may add direct FK if downstream constitutions are amended.

### M36-G: Delivery Manifest Runtime

Create:

- `asset_delivery_manifests`

Runtime decision:

- Store IIIF Presentation API 3.0 manifests.
- Store JSON-LD output payloads.
- Version manifests.
- Pin manifest generation to derivative IDs and rights IDs.

### M36-H: Compatibility Backfill

Backfill existing Phase 1 BHL and LOC-like rows without changing downstream semantics:

- Create compatibility `source_item` rows for existing `illustration_opportunities` where source
  evidence exists.
- Create source records from existing provenance/source metadata where available.
- Create rights records from existing `asset_rights` only when the existing rights record is
  explicit Public Domain or CC0.
- Create technical metadata from existing image width/quality fields where available.
- Do not auto-create approved activation targets for historical rows unless a governed backfill
  policy and human review path exists.

## Backward Compatibility

### Existing Commerce Runtime

Frozen:

- `commerce_opportunities`
- `score_audit_log`
- Commerce formulas
- Commerce policy lifecycle
- Commerce replay worker semantics

M36 compatibility:

- Existing commerce workers continue to read `illustration_opportunities`.
- New activation targets create or link to `illustration_opportunities`.
- Commerce may optionally read substrate IDs from a compatibility link, but must not require them
  for legacy replay.

### Existing Product Routing

Frozen:

- Product recommendation inputs.
- Routing thresholds.
- Product family policy.

M36 compatibility:

- Phase 1 activated media flows into the same recommendation path.
- Phase 2–4 media types cannot produce product recommendations because they cannot activate.

### Existing Catalog

Frozen:

- Catalog candidate and variant planning.
- No provider identifiers.
- Internal-only publication planning posture.

M36 compatibility:

- Catalog sees the same downstream product recommendations.
- IIIF/JSON-LD manifests are delivery evidence, not catalog authority.

### Existing Publication

Frozen:

- Publication candidate model.
- Channel profile governance.
- No external execution semantics.

M36 compatibility:

- Publication consumes Phase 1 image/map/photo/poster outputs through existing image fields and
  can reference `asset_delivery_manifests` for public display.
- eBook/audio/film/3D/dataset publication surfaces remain blocked until their media type phases
  are activated.

### Existing Asset Intelligence

Frozen:

- Anchor type governance.
- Creator authority/prestige registries.
- Place signal registries.

M36 compatibility:

- Asset Intelligence consumes `activation_target`-derived normalized signals.
- It does not parse source payloads or files directly.
- Phase 1 media uses existing biological/geographic/cultural/mixed anchor semantics.

### Existing BHL Runtime

Compatibility strategy:

- Do not replace BHL illustration flow in M36.
- Create substrate records in parallel for replay and future source unification.
- Keep BHL books as provenance containers unless Phase 2 book activation is ratified.

### Existing LOC Map Proof Runtime

Compatibility strategy:

- Promote LOC map proof candidates through substrate records rather than direct insertion into
  Commerce.
- Approved LOC map activation target creates or links to the legacy downstream opportunity path.
- This closes the existing bridge gap without redesigning Commerce.

## Replay Implications

M36 adds a substrate replay layer but does not break legacy replay.

### New Substrate Replay Anchors

Every new Commerce score generated from an M36 activation target should pin:

- `activation_target.id`
- `source_item.id`
- `source_record.id`
- `source_record.raw_payload_hash`
- `media_rights.id`
- `media_technical_metadata.id`
- primary `media_file.id`
- primary `media_file.checksum_sha256`
- primary `media_derivative.id` if used
- manifest ID if delivery payload informed scoring or publication

### Legacy Replay

Existing scores without substrate anchors remain valid under their previous replay contract.

Rules:

- Do not require substrate IDs for pre-M36 records.
- Do not rewrite historical score inputs.
- Optional backfill records must not alter historical `score_inputs`.
- If a legacy record is recomputed after M36, the recomputation should use substrate anchors when
  an activation target exists.

### Source Refetch Replay

If a source changes metadata:

- Insert a new `source_record`.
- Update `source_item.current_source_record_id`.
- Mark dependent activation targets or downstream records stale only if governed policy declares
  the changed fields material.
- Replay old scores from pinned old `source_record`, not the current record.

### Rights Reinvestigation Replay

If rights are re-investigated:

- Insert a new `media_rights` record.
- Update `source_item.current_media_rights_id`.
- If new status is not `verified_pd` or `verified_cc0`, deactivate future activation and mark
  dependent downstream records stale/blocked.
- Replay historical scores from the pinned rights record, but current publication/product action
  must respect the current rights state.

### Derivative Regeneration Replay

If a delivery derivative is regenerated:

- Insert new `media_derivative`.
- Write `normalization` and `fixity_check` events.
- Regenerate manifests.
- Do not rewrite old manifest payloads.
- Existing publication candidates can be marked stale if the derivative was part of their
  publication input snapshot.

## Runtime State Machine

`source_item` lifecycle:

```text
proposed
  -> acquired
  -> rights_verified
  -> activation_eligible
  -> activated
```

Blocking states:

```text
rejected
retracted
```

Transition requirements:

| Transition | Required records |
|---|---|
| `proposed` → `acquired` | current `source_record`, at least one valid `media_file`, ingestion event |
| `acquired` → `rights_verified` | active `media_rights` with `verified_pd` or `verified_cc0` |
| `rights_verified` → `activation_eligible` | active valid `media_technical_metadata` |
| `activation_eligible` → `activated` | approved `activation_target` |

## Compatibility Bridge Options

### Option A: Link Table

Create `activation_target_downstream_link`:

- `activation_target_id`
- `downstream_type`
- `downstream_id`
- `created_at`
- immutable provenance

Pros:

- No mutation of downstream tables.
- Works for future successor tables.
- Keeps downstream constitutions frozen.

Cons:

- Requires join for traceability.

Recommended for M36.

### Option B: Direct FK

Add `activation_target_id` to `illustration_opportunities`.

Pros:

- Simpler local joins.
- Clear authorization source.

Cons:

- Mutates a downstream/upstream table already referenced by five runtime layers.
- Higher constitutional coordination burden.

Deferred.

## Constraints And Triggers

M36 should include these enforcement classes:

- no DELETE on governed registry and append-only entities
- immutability triggers on active registry fields
- immutability triggers on `source_record.raw_payload`
- WORM immutability on master/page/track/segment/model/data files after ingestion event
- immutable verified/blocked rights records
- activation target second-human rule
- activation target approval gate requiring verified rights and valid technical metadata
- one active/nominated activation target per source item
- delivery protocol and media type FK checks
- preservation event append-only rule
- schema version pinning on technical metadata

## Worker Runtime Boundaries

M36 workers may:

- fetch source metadata
- insert source records
- retrieve files
- write media file records
- compute checksums
- generate derivatives
- extract technical metadata
- write preservation events except deletion
- propose rights records
- propose activation targets
- generate IIIF/JSON-LD manifests

M36 workers may not:

- approve rights unless an authorized automated strategy exists
- approve activation targets
- alter immutable source records
- alter verified rights records
- create Commerce scores directly
- create Product Routing recommendations directly
- publish catalog records
- write deletion preservation events

## API Runtime Boundaries

FastAPI should expose governance and inspection endpoints, not direct mutation shortcuts.

Runtime endpoint groups:

- source item inspection
- source record inspection
- media file and derivative inspection
- preservation event inspection
- rights review workflow
- technical metadata validation result
- activation nomination and approval workflow
- IIIF manifest retrieval
- JSON-LD delivery retrieval

No API endpoint may bypass the second-human rule, rights gate, or activation target approval.

## M36 Success Criteria

M36 is successful when:

1. All eleven media types are registered.
2. Phase 1 media types are active.
3. Phase 2–4 media types are pending and blocked from ingestion/activation.
4. Source records are immutable and versioned.
5. Rights records are separate, immutable when final, and versioned.
6. Media files have checksums and preservation events.
7. Technical metadata validates against pinned schema versions.
8. Activation targets bridge to downstream commerce without changing Commerce formulas.
9. Existing BHL and LOC proof flows remain compatible.
10. Legacy replay remains valid.
11. New replay pins substrate anchors.
12. IIIF manifests and JSON-LD payloads are generated for Phase 1 delivery.

## Final Runtime Position

M36 should be an additive substrate migration, not a platform rewrite.

It supports future media by registering their constitutional contracts now, while activating only
the media types that the existing platform can safely consume. New media later become operational
through amendment, adapter, profile, and activation policy — not by redesigning Commerce, Product
Routing, Catalog, Publication, or Asset Intelligence.
