# Universal Media Substrate Constitution v1.0

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified — implementation authorized for Migration 36 |
| Supersedes | None — inaugural substrate constitution |
| Repository | opengracelabs/nc |
| Branch | v0.4.0-collection-000001 |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |

---

## Preamble

This Constitution establishes the governance model for the Universal Public Domain Media Substrate
of Nature & Culture. It answers twelve questions:

1. What is the `media_type_registry` and how are media types governed?
2. What is a `source_item`?
3. What is a `source_record`?
4. What is a `media_file`?
5. What is a `media_derivative`?
6. What is `media_rights`?
7. What is `media_technical_metadata`?
8. What is a `preservation_event`?
9. What is an `activation_target`?
10. Where are the human approval boundaries?
11. What is the replayability invariant for the substrate layer?
12. How are new media types added without platform redesign?

This Constitution is subordinate to the Strategic Directive and the Illustration Opportunity
Doctrine. It is senior to the Commerce Intelligence Constitution, the Asset Intelligence
Constitution, the Product Routing Constitution, the Catalog Constitution, and the Publication
Constitution. Any provision in those constitutions that conflicts with this document is void unless
this Constitution explicitly defers to them.

This Constitution governs the acquisition, storage, rights verification, and activation layers of
Nature & Culture. It does not govern scoring, routing, catalog, or publication. Those layers are
governed by their own constitutions, which depend on this substrate as their upstream source. A
downstream constitution that requires the substrate to behave differently from what is defined here
must be amended — the substrate does not yield to downstream requirements.

---

## Part I — Foundations

### Article 1 — Identity and Doctrine

**1.1** Nature & Culture is a place-centered public-domain heritage commerce platform. It acquires
public-domain assets, verifies their rights, scores them for commercial potential, and routes them
to products.

**1.2** The substrate governed by this Constitution is the acquisition and storage layer. Its
responsibility begins when NC discovers an asset at a source institution and ends when the asset
becomes an `activation_target` approved for commercial pipeline entry.

**1.3** The commercial pipeline boundary is the `activation_target`. Before it: substrate
governance. After it: Commerce Intelligence governance. These two layers are strictly separated.
Nothing in this Constitution governs scoring, routing, or catalog decisions. Nothing in downstream
constitutions governs acquisition, storage, or rights decisions.

**1.4** Every entity in this Constitution exists in PostgreSQL. No entity is authoritative unless
recorded in PostgreSQL. MinIO holds file evidence. Workers execute processes. FastAPI provides the
governance gateway. Humans hold the approval authority. AI provides advisory input only. Workers
do not govern. Workers do not approve.

**1.5** The hard gate is unconditional: no `source_item` crosses the substrate boundary into the
commercial pipeline without a verified Public Domain or CC0 rights determination. This rule admits
no exceptions, overrides, or temporary relaxations. It cannot be weakened by Director decision,
constitutional amendment, or worker configuration.

### Article 2 — Scope

This Constitution governs exactly nine entities:

| Entity | Role |
|---|---|
| `media_type_registry` | Governing authority for media type definitions, formats, delivery protocols, and activation status |
| `source_item` | The atomic unit of acquisition — one identifiable intellectual work at one source institution |
| `source_record` | The raw metadata from the source institution, preserved verbatim and immutably |
| `media_file` | A physical file stored in MinIO, with a governed role classification and canonical key |
| `media_derivative` | A file produced from a master `media_file` by a governed normalization worker |
| `media_rights` | The rights determination for a `source_item`, including structured evidence chain and rights statement URI |
| `media_technical_metadata` | Type-specific technical properties of a `source_item`, validated against the registered content schema |
| `preservation_event` | An append-only, PREMIS-aligned event in the lifecycle of a `media_file` or `media_derivative` |
| `activation_target` | The governed approval record that bridges substrate and commercial pipeline |

This Constitution does not govern: `places`, `concepts`, `sources`, `workflow_items`,
`illustration_opportunities` downstream of activation, `commerce_opportunities`, or any commerce,
routing, catalog, or publication entity.

### Article 3 — Constitutional Authority Order

```
Strategic Directive
  └─ Illustration Opportunity Doctrine
       └─ Universal Media Substrate Constitution v1.0  ← this document
            └─ Commerce Intelligence Constitution v1.2
                 └─ Asset Intelligence Constitution v1.1
                      └─ Product Routing Constitution v1.1
                           └─ Catalog Constitution v1.1
                                └─ Publication Constitution v1.1
```

No lower authority may override a higher authority. A downstream constitutional provision that
requires a substrate entity to behave differently from how this Constitution defines it is void.
The downstream constitution must be amended to comply.

### Article 4 — PostgreSQL Authority Doctrine

**4.1** PostgreSQL is the sole authority for all substrate state. An acquisition event, a rights
determination, a file registration, or an activation decision does not exist unless recorded in
PostgreSQL.

**4.2** MinIO is evidence storage, not authority. The presence or absence of a file in MinIO does
not change the authoritative state in PostgreSQL. When PostgreSQL and MinIO conflict, PostgreSQL
governs. MinIO confirms.

**4.3** Workers write substrate records. Workers do not govern. Workers do not approve. Workers do
not override humans. A worker that writes a record it is not authorized to write has violated this
Constitution regardless of whether the record is technically valid.

**4.4** The second-human rule applies at every human-approval gate in this Constitution. A person
may not approve a record they authored or nominated. This rule is enforced at the database level
by `CHECK (approved_by IS DISTINCT FROM authored_by)` or equivalent on all governed entities.

---

## Part II — Entity Definitions

### Article 5 — `media_type_registry`

**5.1** The `media_type_registry` is the governing authority for what media types NC supports, in
what phase, under what delivery protocol, in what archival and delivery format, and under what
constitutional authorization. An entry in this registry is a constitutional assertion.

**5.2** Each entry must declare:

| Field | Governance requirement |
|---|---|
| `media_type_id` | Canonical immutable identifier. Lowercase, no spaces. Set at INSERT. Never modified. |
| `display_name` | Human-readable label. |
| `expansion_phase` | Integer 1–4. Governs when activation is authorized. Phase 1 = immediate; Phase 2–4 = requires amendment. |
| `anchor_types_allowed` | The anchor types this media type may carry: `biological`, `geographic`, `cultural`, `mixed`. At least one required. |
| `delivery_protocol` | One governed value from the Article 22 delivery protocol vocabulary. |
| `archival_format` | The WORM master file format for this type. Immutable after `status = 'active'`. |
| `delivery_format` | The normalized delivery file format for this type. |
| `requires_file_manifest` | Boolean. `TRUE` for multi-file types (book, audiobook, audio, film, 3d). |
| `content_spec_schema` | A JSON Schema fragment governing valid `media_technical_metadata` for this type. |
| `status` | Governed lifecycle: `pending` → `active` → `retired`. |
| `constitutional_ref` | The amendment ID authorizing activation. Required for Phase 2+ types before `status = 'active'`. |

**5.3** The `media_type_registry` is immutable on the following fields once `status = 'active'`:
`media_type_id`, `expansion_phase`, `archival_format`, `delivery_protocol`. Changes to
`content_spec_schema` or `delivery_format` after activation require a new constitutional amendment
and are implemented as a new versioned entry, not an update to the existing one.

**5.4** Phase 1 types (`image`, `map`, `photography`, `poster`) are governed by the existing
constitutions and may be activated without a new amendment to this Constitution. Phase 2–4 types
require a ratified amendment before `status` may be set to `active`. Registering Phase 2–4 types
in advance with `status = 'pending'` is explicitly authorized. Registration is not activation. A
`pending` entry does not authorize ingestion.

**5.5** The `media_type_registry` is governed by a no-DELETE rule. Retirement sets
`status = 'retired'`. The row is never removed. Retired types remain registered and their
`media_type_id` is reserved permanently.

**5.6** The governing initial registry, with Phase 1 types `active` and Phase 2–4 types `pending`:

| media_type_id | phase | delivery_protocol | archival_format | delivery_format | requires_manifest | status |
|---|---|---|---|---|---|---|
| `image` | 1 | `iiif` | `tiff` | `jpeg2000` | false | active |
| `map` | 1 | `iiif` | `tiff` | `jpeg2000` | false | active |
| `photography` | 1 | `iiif` | `tiff` | `jpeg2000` | false | active |
| `poster` | 1 | `iiif` | `tiff` | `jpeg2000` | false | active |
| `book` | 2 | `iiif` | `pdf` | `epub3` | true | pending |
| `ebook` | 2 | `epub-js` | `epub3` | `epub3` | false | pending |
| `audiobook` | 2 | `html5-audio` | `wav-bwf` | `mp3` | true | pending |
| `audio` | 3 | `html5-audio` | `wav-bwf` | `flac` | true | pending |
| `film` | 3 | `hls` | `ffv1-mkv` | `h264` | true | pending |
| `3d` | 4 | `model-viewer` | `gltf` | `glb` | true | pending |
| `dataset` | 4 | `download` | `csv` | `json-ld` | true | pending |

---

### Article 6 — `source_item`

**6.1** A `source_item` is a single identifiable intellectual work at a single governed source
institution, as identified by NC's acquisition workers using the institution's native identifier.
It is the atomic unit of the acquisition layer.

**6.2** A `source_item` is not a file. It is not metadata. It is not a rights determination. It is
the intellectual work itself — the thing that files represent, that metadata describes, that rights
apply to. These are governed by separate entities.

**6.3** The relationship between a `source_item` and its supporting entities:

| Relationship | Cardinality | Notes |
|---|---|---|
| `source_item` → `source_record` | 1:many | One active (current) record; prior versions retained |
| `source_item` → `media_rights` | 1:many | One active determination; prior versions retained |
| `source_item` → `media_technical_metadata` | 1:many | One active version; prior versions retained |
| `source_item` → `media_file` | 1:many | One per file role × sequence position |
| `source_item` → `media_derivative` | 1:many | Zero or many |
| `source_item` → `activation_target` | 1:0..1 | At most one active nomination at any time |

**6.4** The `source_item` lifecycle:

| Status | Meaning | Pipeline access |
|---|---|---|
| `proposed` | Discovered by a worker; not yet acquired | None |
| `acquired` | Files and source_record received; rights not yet verified | None |
| `rights_verified` | Active `media_rights` status is `verified_pd` or `verified_cc0` | Eligible for technical validation |
| `activation_eligible` | Valid `media_technical_metadata` confirmed against type schema | Eligible for `activation_target` creation |
| `activated` | `activation_target` approved; commercial pipeline entry created | In commercial pipeline |
| `rejected` | Rejected at activation review or rights verification | Barred from pipeline |
| `retracted` | Previously activated; subsequently withdrawn by Director decision | Removed from pipeline |

**6.5** No `source_item` may advance to `activation_eligible` without a `media_technical_metadata`
record that validates against the `content_spec_schema` for its registered `media_type`.

**6.6** The existing `illustration_opportunities` table is the physical realization of `source_item`
during Phase 1. The `anchor_type`, `media_type`, `content_spec`, and rights fields on that table
implement this Constitution's requirements. The table rename (`illustration_opportunities` →
`asset_opportunities`) is authorized by this Constitution but is deferred to a future constitutional
amendment addressing all five downstream constitutions simultaneously. Until that amendment is
ratified, `illustration_opportunities` is treated as semantically equivalent to `source_item` for
all purposes of this Constitution.

---

### Article 7 — `source_record`

**7.1** A `source_record` is the raw metadata returned by a source institution's API or catalog,
preserved verbatim at the moment of acquisition. It is NC's record of what the source institution
said about the `source_item`.

**7.2** The `source_record` is the metadata replay anchor. Any downstream process that must
reconstruct what NC knew about an asset at acquisition time reads the `source_record`.

**7.3** A `source_record` is immutable once written. Workers may not modify a `source_record` after
its initial write. An immutability trigger must prevent mutation of: `institution_id`,
`source_identifier`, `raw_payload`, `schema_standard`, and `fetched_at`.

**7.4** If a re-fetch of the source returns different metadata, a new `source_record` is created.
The `source_item` is updated to reference the new record as current. The prior `source_record` is
not deleted; it is retained as versioned history. The `source_item` holds a `current_source_record_id`
FK that always points to the active version.

**7.5** The `source_record.raw_payload` is stored verbatim as received from the institution.
NC does not modify, normalize, or translate the raw payload. Normalization is the responsibility
of `media_technical_metadata`. The `schema_standard` field identifies the metadata schema in use:

| Value | Standard | Reference institution |
|---|---|---|
| `marc` | MARC 21 | Library of Congress |
| `edm` | Europeana Data Model | Europeana |
| `lido` | LIDO (Lightweight Information Describing Objects) | Rijksmuseum |
| `dc` | Dublin Core | Internet Archive |
| `mods` | Metadata Object Description Schema | Library of Congress |
| `oai_pmh` | OAI-PMH envelope | Multiple |
| `schema_org` | Schema.org JSON-LD | Multiple |
| `bhl_api` | BHL API response format | BHL |

Values outside this vocabulary require a constitutional amendment.

**7.6** EDM alignment: the `source_record` corresponds to `edm:ProvidedCHO` in the Europeana Data
Model — the cultural heritage object as described by the providing institution. The `source_item`
corresponds to `ore:Aggregation`. NC's stored file corresponds to `edm:WebResource`.

---

### Article 8 — `media_file`

**8.1** A `media_file` is a physical binary file stored in MinIO, associated with a `source_item`.
Every `media_file` has a governed role, a canonical MinIO key, and a SHA-256 checksum.

**8.2** `media_file.file_role` governs the nature of the file:

| Role | WORM | Description |
|---|---|---|
| `master` | Yes | Archival-quality original. The primary preservation copy. |
| `page` | Yes | A single page of a multi-page asset (book, manuscript). Ordered by `sequence_position`. |
| `track` | Yes | A single audio track. Ordered by `sequence_position`. |
| `segment` | Yes | A single film segment. Ordered by `sequence_position`. |
| `model` | Yes | The primary 3D mesh file. |
| `data` | Yes | A dataset file (CSV, Parquet, JSON-LD). |

All WORM roles share one invariant: once the associated `preservation_event` of type `ingestion`
is written, the file at the governed MinIO key may not be overwritten. A new master requires a
new `source_item`, a new MinIO key, and a new ingestion event.

**8.3** The MinIO key convention is constitutional. Workers must use this convention exactly.
Deviation is a constraint violation:

```
Masters and WORM ordered files:
  masters/{source_id}/{media_type_id}/{source_item_id}/{seq:05d}/{original_filename}

Examples:
  masters/loc/map/a1b2c3d4/00001/hayden_survey_1871.tif
  masters/ia/book/e5f6g7h8/00001/origin_of_species_page_001.tif
  masters/ia/book/e5f6g7h8/00002/origin_of_species_page_002.tif
  masters/bl/audio/i9j0k1l2/00001/nightingale_1889.wav
  masters/smithsonian/3d/m3n4o5p6/00001/triceratops_skull.gltf
```

**8.4** Every `media_file` must have a `preservation_event` of type `ingestion` written before it
is linked to a `source_item`. Linking a file without a prior ingestion event is a constraint
violation enforced at the database level.

**8.5** The SHA-256 checksum of every master `media_file` must be verified by a `preservation_event`
of type `fixity_check` at minimum once per calendar year. A fixity failure produces an event with
`event_outcome = 'failure'` and triggers a human notification. Fixity failures must not be silently
logged and ignored.

---

### Article 9 — `media_derivative`

**9.1** A `media_derivative` is a file produced from a WORM `media_file` by a governed normalization
worker. It is the delivery-ready or preview form of the master.

**9.2** `media_derivative.file_role` vocabulary:

| Role | Description |
|---|---|
| `delivery` | Format-normalized file served to consumers (JPEG2000, MP3, H.264, GLB, EPUB3, HLS playlist) |
| `thumbnail` | Generated preview image at governed dimensions |
| `texture` | Derived texture map for a 3D model delivery asset |
| `material` | Derived material definition for a 3D model delivery asset |

**9.3** `media_derivative` records are not WORM. They may be regenerated when delivery format
standards change, quality requirements improve, or a technical defect is identified. Each
regeneration creates a new `preservation_event` of type `normalization`. The prior delivery file
may be deleted from MinIO after the new delivery file is confirmed by a `fixity_check` event.
Deletion requires a `preservation_event` of type `deletion`.

**9.4** The MinIO key convention for derivatives:

```
Delivery:
  delivery/{media_type_id}/{source_item_id}/{role}/{filename}

Thumbnails:
  thumbnails/{source_item_id}/{width}x{height}.jpg

Examples:
  delivery/map/a1b2c3d4/delivery/hayden_survey_1871.jp2
  delivery/book/e5f6g7h8/delivery/page_001.jpg
  delivery/audio/i9j0k1l2/delivery/nightingale_1889.mp3
  thumbnails/a1b2c3d4/400x300.jpg
```

**9.5** Every `media_derivative` must reference its source `media_file`. The chain
`media_derivative → media_file → source_item` must be complete and traversable. A derivative
without a traceable master is an integrity violation. W3C PROV alignment: this chain is
`prov:wasDerivedFrom`.

---

### Article 10 — `media_rights`

**10.1** `media_rights` is the rights determination for a `source_item`. It records the determined
rights status, the structured evidence chain that supports that status, and the identity and
timestamp of the verifying party.

**10.2** The commercial pipeline hard gate: only two rights status values permit a `source_item`
to cross the substrate boundary. All other values bar pipeline entry unconditionally.

**10.3** The `media_rights.rights_status` vocabulary:

| Status | Pipeline access | Meaning |
|---|---|---|
| `pending` | Barred | Rights investigation not yet complete |
| `verified_pd` | Permitted | Public Domain confirmed with evidence chain |
| `verified_cc0` | Permitted | CC0 dedication confirmed with evidence chain |
| `blocked` | Barred permanently | Rights investigation concluded: pipeline entry is not possible |
| `under_review` | Suspended | Previously verified; re-investigation in progress |

**10.4** A `media_rights` record with status `verified_pd`, `verified_cc0`, or `blocked` is
immutable. An immutability trigger must prevent mutation of `rights_status`, `rights_evidence`,
`rights_statement_uri`, `verified_by`, and `verified_at` after these statuses are set.

**10.5** Rights re-evaluation creates a new `media_rights` record. The `source_item` is updated
to reference the new record as current. Prior records are not deleted. No prior record's status
may be modified.

**10.6** Every `media_rights` record with status `verified_pd` or `verified_cc0` must contain:

- `rights_statement_uri` — A URI from the governed Rights Statement vocabulary (Article 18.4).
- `rights_evidence` — A structured JSONB document recording the reasoning chain: publication date,
  creator death date (if applicable), country of first publication, and any institutional rights
  assertion consulted.
- `verified_by` — The identity of the human, or the authorized automated rights worker, that made
  the determination.
- `verified_at` — The timestamp of verification.

**10.7** Automated rights verification is permitted only when:
- The source has `governance_state = 'active'`
- The source's `config` specifies an explicit and governed `rights_strategy`
- The Director has authorized the strategy by Director Decision and the decision is recorded

Outside these conditions, rights verification requires a human verifier. `verified_by` must
identify a human, not a worker.

---

### Article 11 — `media_technical_metadata`

**11.1** `media_technical_metadata` is NC's normalized technical description of a `source_item`.
It is what NC knows about the asset's technical properties — distinct from what the source
institution said (`source_record`) and distinct from how NC scores the asset
(`commerce_opportunities`).

**11.2** Every `source_item` must have a valid `media_technical_metadata` record before it may
advance to `activation_eligible` status. "Valid" means the record's `content` JSONB conforms to
the `content_spec_schema` registered for the `source_item`'s `media_type` in `media_type_registry`.

**11.3** `media_technical_metadata` is versioned. Updates produce new records. The `source_item`
holds a `current_technical_metadata_id` FK pointing to the active record. Prior records are
retained. The `content` field of any record that has been linked as current by a `source_item`
may not be modified after it is superseded — it is the historical technical state at that time.

**11.4** The `content_spec_schema` in `media_type_registry` is the sole validation authority.
Workers must not validate against any other schema. If the schema changes, the new schema applies
only to new records; existing records retain validity under the schema version current when they
were written. Every `media_technical_metadata` record must record `schema_version` — the
`media_type_registry` entry version against which it was validated.

**11.5** Scoring workers that use `media_technical_metadata` fields as scoring signals must record
the `media_technical_metadata.id` that was active at the time of scoring in
`commerce_opportunities.score_inputs`. This is the technical metadata replay anchor: replay
reconstructs signal values from the pinned record, not from the current record.

**11.6** Reference standard alignment for `content_spec_schema` governance:

| Media type | Technical metadata authority |
|---|---|
| image, photography, poster, map | EXIF/TIFF field set; LOC Thesaurus of Graphic Materials for subject terms |
| book, ebook | MARC 21 bibliographic fields (LOC); Dublin Core for aggregation layer |
| audiobook, audio | BWF (Broadcast Wave Format) technical fields; British Library Sound Archive standards |
| film | SMPTE technical fields; LOC Motion Picture and Television Reading Room standards |
| 3d | Smithsonian X 3D field set; glTF 2.0 asset properties |
| dataset | DCAT (Data Catalog Vocabulary); Schema.org `Dataset` type |

---

### Article 12 — `preservation_event`

**12.1** A `preservation_event` is an append-only, PREMIS-aligned record of a single event in
the lifecycle of a `media_file` or `media_derivative`. It is the authoritative audit trail for
every file NC holds.

**12.2** The `preservation_event.event_type` vocabulary is constitutional. Only the following
values are permitted:

| Event type | Required trigger |
|---|---|
| `ingestion` | File received and written to MinIO. Required before the file is linked to a `source_item`. |
| `format_identification` | MIME type and format confirmed by an identification tool. |
| `validation` | File integrity and format-compliance verified against the registered `archival_format`. |
| `fixity_check` | SHA-256 checksum verified against the stored value. |
| `normalization` | File converted to a delivery or derivative format. |
| `rights_verification` | Rights status confirmed for the file's associated `source_item`. |
| `replication` | File copied to secondary or geographically redundant storage. |
| `migration` | File migrated to a new archival format standard. |
| `deletion` | File removed from MinIO. Requires Director approval (Article 24.2). |

Values outside this vocabulary require a constitutional amendment.

**12.3** The `preservation_event` is governed by two no-modify rules enforced at the database level:
no UPDATE and no DELETE. Append-only is absolute and unconditional.

**12.4** Every `preservation_event` must record:

- `event_type` — from the governed vocabulary above
- `event_datetime` — timestamp of the event
- `event_outcome` — `success` | `failure` | `warning`
- `event_detail` — structured JSONB: tool name, tool version, outcome detail
- `agent_type` — `worker` | `human` | `institution`
- `agent_id` — the specific worker name, username, or institution `source_id`

**12.5** PREMIS alignment: `media_file` and `media_derivative` map to PREMIS `Object`.
`preservation_event` maps to PREMIS `Event`. `agent_type` + `agent_id` map to PREMIS `Agent`.

**12.6** W3C PROV alignment: `preservation_event` maps to PROV `Activity`. The file it describes
maps to PROV `Entity`. The agent maps to PROV `Agent`.

**12.7** A `preservation_event` of type `deletion` requires: `event_outcome = 'success'`,
`event_detail` containing a Director Decision reference, and `agent_type = 'human'`. Workers may
not write `deletion` events. A deletion event written without a valid Director Decision reference
in `event_detail` is an integrity violation.

---

### Article 13 — `activation_target`

**13.1** An `activation_target` is the governed decision record that bridges the substrate layer
and the commercial pipeline. Its creation nominates a `source_item` for pipeline entry. Its
approval authorizes that entry.

**13.2** An `activation_target` may only be created for a `source_item` with status
`activation_eligible`. A `source_item` that is not `activation_eligible` cannot be nominated.
This constraint must be enforced at the database level.

**13.3** The `activation_target.status` lifecycle:

| Status | Meaning | Who may act |
|---|---|---|
| `nominated` | Nominated for pipeline entry; awaiting human approval | Curator (second-human rule) |
| `approved` | Human approval received; pipeline entry authorized | Creates a downstream opportunity record |
| `rejected` | Human review concluded: item must not enter the pipeline | Source_item status → `rejected` |
| `escalated` | Referred to Director; curator-level approval or rejection blocked | Director decision required |

**13.4** The second-human rule applies: the person who nominates an `activation_target` may not
approve it. This is enforced at the database level.

**13.5** An `activation_target` with status `approved` authorizes exactly one commercial pipeline
entry record (an `illustration_opportunity` record or its named successor). The pipeline record
must reference `activation_target.id` as its authorization source. This reference is immutable.

**13.6** A `rejected` `activation_target` may not be re-nominated without a Director Decision.
A Director Decision that reopens a rejected nomination must be recorded in the `activation_target`
record's `provenance` JSONB before a new nomination is created.

**13.7** At most one `activation_target` per `source_item` may be in `nominated` or `approved`
status at any time. This constraint must be enforced at the database level.

**13.8** `activation_target` immutability: `source_item_id`, `nominated_by`, and `nominated_at`
are immutable on INSERT. `approved_by`, `approved_at`, and final `status` are immutable once
`status = 'approved'`.

---

## Part III — Approval Boundaries

### Article 14 — The Four Substrate Approval Gates

**14.1** The substrate has exactly four human approval gates. No gate may be automated without an
explicit Director Decision recorded in the relevant source or rights configuration. No gate may
be bypassed. Each gate produces an immutable record of the approval decision.

**Gate 1 — Source Institution Activation**

**14.2** Before any source institution may supply `source_item` records to the substrate, its
`sources.governance_state` must be `active`. Transition from `proposed` to `active` requires
human approval by the Director. The second-human rule applies. This gate is established by
Migration 17 and is not superseded by this Constitution.

**Gate 2 — Media Type Activation**

**14.3** Before a `media_type_registry` entry may have `status = 'active'`, it must have
`approved_by IS DISTINCT FROM authored_by`. Phase 2–4 entries additionally require a ratified
constitutional amendment to this Constitution, and `constitutional_ref` must reference it before
activation is permitted. Both the amendment and the approval are required; neither alone is
sufficient.

**Gate 3 — Rights Verification**

**14.4** Before any `source_item` may advance to `rights_verified` or `activation_eligible` status,
it must have an active `media_rights` record with `status = 'verified_pd'` or `'verified_cc0'`.
Rights verification requires a human verifier, or an automated rights worker authorized by a
Director Decision that specifies the governed rights strategy in `sources.config`. Automated
verification is permitted only for date-based strategies on US-published works before 1928.
All other rights determinations require human verification without exception.

**Gate 4 — Activation Target Approval**

**14.5** Before any `source_item` may enter the commercial pipeline, a human must approve its
`activation_target`. The second-human rule applies. The approval is the final substrate gate.
Downstream commerce governance begins at this boundary and has no authority over the substrate
decisions that led to it.

---

## Part IV — Immutability and Versioning

### Article 15 — Immutability Rules

**15.1** The following fields and records are immutable once their governing condition is met.
Immutability is enforced by BEFORE UPDATE triggers. No worker, administrator, or API endpoint
may override them.

| Entity | Immutable fields | Condition |
|---|---|---|
| `media_type_registry` | `media_type_id`, `expansion_phase`, `archival_format`, `delivery_protocol` | On INSERT — always immutable |
| `media_type_registry` | `content_spec_schema`, `delivery_format` | When `status = 'active'` |
| `source_record` | `institution_id`, `source_identifier`, `raw_payload`, `schema_standard`, `fetched_at` | On INSERT — always immutable |
| `media_rights` | `rights_status`, `rights_evidence`, `rights_statement_uri`, `verified_by`, `verified_at` | When `rights_status IN ('verified_pd', 'verified_cc0', 'blocked')` |
| `media_file` (WORM roles) | `minio_bucket`, `minio_key`, `checksum_sha256`, `file_role`, `source_item_id` | After linked `ingestion` preservation_event is written |
| `activation_target` | `source_item_id`, `nominated_by`, `nominated_at` | On INSERT — always immutable |
| `activation_target` | `approved_by`, `approved_at`, `status` | When `status = 'approved'` |
| `preservation_event` | All fields | On INSERT — append-only, no UPDATE permitted |

### Article 16 — Versioning Rules

**16.1** Entities that legitimately change over time use versioning: new records are created, prior
records are retained, and the parent entity holds a FK to the current version.

| Entity | Versioning pattern |
|---|---|
| `source_record` | New record on re-fetch. `source_item.current_source_record_id` updated to new record. |
| `media_rights` | New record on re-investigation. `source_item.current_media_rights_id` updated. Prior record retained with its original status intact. |
| `media_technical_metadata` | New record on re-analysis or schema revision. `source_item.current_technical_metadata_id` updated. |
| `media_derivative` | New record on regeneration. Prior delivery file may be deleted after regeneration is confirmed by a `fixity_check` event. |

**16.2** Versioned entity records must include a `superseded_by` field (UUID, nullable) referencing
the record that replaced them. This enables forward-traversal of version history for audit
purposes.

---

## Part V — Replayability

### Article 17 — Replayability Invariants

**17.1** Replayability means: given the same substrate state at any past moment, any downstream
scoring or routing decision made at that time can be reproduced from stored records alone, without
re-fetching from external sources.

**17.2** The following five invariants are constitutional requirements. Any implementation that
violates them produces a non-replayable pipeline. Replayability invariants may not be weakened
by Director Decision.

**Invariant R-1: Source Record Immutability.**
The `source_record.raw_payload` that was current at the time of any downstream decision is always
recoverable. A scoring replay must record the `source_record.id` that was active at scoring time
in `commerce_opportunities.score_inputs`.

**Invariant R-2: Rights Chain Immutability.**
The rights determination that authorized any commercial pipeline entry is always recoverable. The
`activation_target` must record the `media_rights.id` that was active at approval time. The
authorizing rights record may never be modified after approval.

**Invariant R-3: Technical Metadata Version Pinning.**
`commerce_opportunities.score_inputs` must record the `media_technical_metadata.id` that was
active at scoring time. Replay reconstructs technical signal values from the pinned record, not
from the current record.

**Invariant R-4: Preservation Event Completeness.**
Every state transition in a `media_file` or `media_derivative` lifecycle must produce a
`preservation_event`. The event log must allow complete reconstruction of the file state at any
past moment.

**Invariant R-5: Schema Version Pinning.**
Every `media_technical_metadata` record must store the `content_spec_schema_version` under which
it was validated. Replay can determine whether the record was valid under the governing schema at
the time of scoring.

---

## Part VI — Reference Standard Alignment

### Article 18 — IIIF

**18.1** For all `media_type_registry` entries with `delivery_protocol = 'iiif'`, the delivery
layer must generate a IIIF Presentation API 3.0 manifest for each `source_item`. The manifest is
stored as the `manifest_payload` in the `asset_delivery_manifests` record.

**18.2** IIIF Manifest structure for NC media types:

- A single-file source_item (image, map, photography, poster) produces a Manifest with one Canvas.
- A multi-file source_item (book) produces a Manifest with one Canvas per page, ordered by
  `media_file.sequence_position`.
- A Collection of related source_items produces a IIIF 3.0 Collection.

**18.3** IIIF Image API governs tile serving for all `media_derivative` files with
`file_role = 'delivery'` on visual media types.

**18.4** The governed Rights Statement vocabulary for `media_rights.rights_statement_uri`:

| URI fragment | Meaning |
|---|---|
| `http://rightsstatements.org/vocab/NoC-US/1.0/` | No Copyright — United States |
| `http://rightsstatements.org/vocab/NoC-CR/1.0/` | No Copyright — Contractual Restrictions |
| `http://creativecommons.org/publicdomain/mark/1.0/` | Public Domain Mark |
| `http://creativecommons.org/publicdomain/zero/1.0/` | CC0 1.0 Universal |

Values outside this vocabulary require a constitutional amendment before use in a `media_rights`
record.

### Article 19 — JSON-LD and Schema.org

**19.1** `source_record.raw_payload` with `schema_standard = 'schema_org'` or `'edm'` must be a
valid JSON-LD document.

**19.2** Schema.org type alignment governs how NC's media types are represented in JSON-LD output:

| media_type_id | Schema.org type |
|---|---|
| `image`, `photography`, `poster` | `schema:VisualArtwork` or `schema:ImageObject` |
| `map` | `schema:Map` |
| `book`, `ebook` | `schema:Book` |
| `audiobook` | `schema:Audiobook` |
| `audio` | `schema:AudioObject` |
| `film` | `schema:Movie` |
| `3d` | `schema:3DModel` |
| `dataset` | `schema:Dataset` |

**19.3** Where the `source_record.raw_payload` contains a `schema:license` or equivalent rights
property, its value must be reconcilable with `media_rights.rights_statement_uri`. Irreconcilable
inconsistency must be flagged as a `rights_evidence` anomaly and must block automatic rights
verification.

### Article 20 — PREMIS

**20.1** The `preservation_event` entity is governed by PREMIS (Preservation Metadata:
Implementation Strategies), a LOC/OCLC co-standard. PREMIS mapping:

| PREMIS concept | NC entity |
|---|---|
| Object | `media_file` or `media_derivative` |
| Event | `preservation_event` |
| Agent | `preservation_event.agent_type` + `agent_id` |
| Rights | `media_rights` |

**20.2** Any new `preservation_event.event_type` value not in the governed vocabulary of Article
12.2 requires a constitutional amendment. Workers may not introduce undeclared event types.

### Article 21 — W3C PROV

**21.1** Provenance chain requirements (W3C PROV alignment):

| PROV concept | NC realization |
|---|---|
| `prov:Entity` | `source_item` (the intellectual work); `media_file`; `media_derivative` |
| `prov:Activity` | Acquisition; ingestion; normalization; rights verification; activation |
| `prov:Agent` | Source institution (`sources`); acquisition worker; human curator |
| `prov:wasGeneratedBy` | `source_item` was generated by the acquisition activity |
| `prov:wasDerivedFrom` | `media_derivative` was derived from `media_file` |
| `prov:wasAttributedTo` | `source_item` attributed to the source institution |
| `prov:wasAssociatedWith` | `activation_target` approval associated with the approving curator |

---

## Part VII — Media Type Lifecycle

### Article 22 — Activation Protocol

**22.1** The governed sequence for activating a new media type is:

```
1. INSERT INTO media_type_registry (status = 'pending')
        ↓ governance action
2. For Phase 2–4: draft and ratify a constitutional amendment to this Constitution
        ↓ human approval (second-human rule)
3. approved_by signs off on the media_type_registry entry
        ↓
4. UPDATE media_type_registry SET status = 'active', constitutional_ref = '[amendment_id]'
        ↓ first authorized worker action
5. Source institutions with governance_state = 'active' may begin ingesting this type
```

Steps 1–4 are governance. Step 5 is the first worker action. No worker may ingest a media type
before step 4 is complete.

**22.2** The `delivery_protocol` vocabulary is constitutional. New values require a constitutional
amendment before use:

| Value | Governing standard |
|---|---|
| `iiif` | IIIF Presentation API 3.0 + IIIF Image API |
| `hls` | HTTP Live Streaming (HLS); adaptive bitrate |
| `model-viewer` | Google model-viewer Web Component; glTF 2.0 |
| `epub-js` | epub.js; EPUB 3.0 |
| `html5-audio` | HTML5 Audio element; MP3 or FLAC delivery |
| `pdf-js` | pdf.js; PDF delivery |
| `download` | Direct file download; CSV, JSON-LD, Parquet |

---

## Part VIII — Human Governance

### Article 23 — Second-Human Rule

**23.1** The second-human rule applies at every approval gate. A human may not approve a record
they authored, nominated, or created. This rule is enforced at the database level.

**23.2** The gates subject to this rule:

1. Source institution activation (Gate 1)
2. Media type activation (Gate 2)
3. Rights verification where a single human both requests and verifies the determination (Gate 3)
4. Activation target approval (Gate 4)

### Article 24 — Director Authority

**24.1** A Director Decision (DD-X) is a governed override of a constitutional constraint or the
authorization of an action not permitted without explicit approval. Director decisions require the
Director's documented authorization and are recorded in the relevant entity's `provenance` JSONB:

```json
{
  "director_decision": "DD-X",
  "authorized_by": "...",
  "authorized_at": "...",
  "rationale": "..."
}
```

**24.2** The following actions require Director Decisions and may not be performed by workers or
curators acting alone:

- Deletion of any WORM `media_file` (`preservation_event.event_type = 'deletion'`)
- Re-nomination of a `rejected` `activation_target`
- Authorization of automated rights verification for any new source or rights strategy
- Activation of a Phase 2–4 media type (jointly requires a constitutional amendment)
- Retirement of a `media_type_registry` entry (`status` → `'retired'`)
- Status reset of a `source_item` from `rejected` or `retracted` to any prior status

**24.3** No Director Decision may lower the hard gate of Article 1.5. The requirement for
`verified_pd` or `verified_cc0` before commercial pipeline entry is not subject to Director
override.

### Article 25 — Worker Authority Boundaries

**25.1** Workers are authorized to:

- Create `source_item` records in `proposed` status
- Write `source_record` records (INSERT only)
- Write `media_file` records and their associated ingestion `preservation_event`
- Write `media_derivative` records and their normalization `preservation_event`
- Write `media_technical_metadata` records
- Write non-deletion `preservation_event` records
- Advance `source_item` status automatically as governed transitions are satisfied: `proposed` →
  `acquired`, `acquired` → `rights_verified` (after a human verifies rights or an authorized
  automated strategy confirms PD), `rights_verified` → `activation_eligible` (after technical
  metadata validates)

**25.2** Workers are not authorized to:

- Write `activation_target` approval decisions
- Write `media_rights` records with `verified_pd`, `verified_cc0`, or `blocked` status without
  explicit human or Director authorization
- Modify any immutable field on any entity
- Write `preservation_event` records of type `deletion`
- Change `media_type_registry.status` to `active`
- Change `sources.governance_state` to `active`

---

## Open Questions

| OQ | Question | Deferred to |
|---|---|---|
| OQ-1 | Physical realization of `source_record`: separate table (cleaner versioning, indexable) or immutable JSONB column on `source_item` with trigger enforcement (lower migration scope)? Both satisfy Article 7. | Implementation Migration 36 |
| OQ-2 | Physical realization of `media_rights`: separate versioned table (full history) or immutable fields on `source_item` with version linked by FK? Separate table is the stronger governance model. | Implementation Migration 36 |
| OQ-3 | `content_spec_schema` validation: PostgreSQL-level trigger using `pg_jsonschema` extension (stronger enforcement, requires extension), or worker-level validation only (no extension required, weaker enforcement)? | Implementation Migration 36 |
| OQ-4 | When should `illustration_opportunities` be renamed to `asset_opportunities`? This Constitution authorizes the rename (Article 6.6) but defers it. The rename requires coordinated amendment of all five downstream constitutions. | Dedicated constitutional amendment — future session requiring Director decision |
