# Universal Media Substrate Constitution v1.2

| Field | Value |
|---|---|
| Version | 1.2.0 |
| Status | Ratified — constitutional changes only; implementation authorized per Migration 36 |
| Supersedes | `media_substrate_constitution_v1.1.md` (v1.1.0) |
| Repository | opengracelabs/nc |
| Branch | v0.4.0-collection-000001 |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |

---

## Amendment Log — v1.1.0 → v1.2.0

Three constitutional additions. No entity changes. No migration required.
All articles not listed are unchanged from v1.1.0.

| Amendment | Description | Articles Affected |
|---|---|---|
| A-1 | Phase boundary criteria: constitutional definition of what conditions assign a media type to each phase. Prevents arbitrary reclassification. | Article 5 — new 5.7 |
| A-2 | Constitutional activation sequence: total ordering of all eleven media types, with concurrent activation rules and prerequisite chain. | Article 5 — new 5.8; Article 23 — new 23.3, 23.4 |
| A-3 | Constitutional Reference Institution Framework: six institutions evaluated, tiered, and governed. Per-institution adopted and rejected governance rules recorded. | New Part IX: Articles 28, 29, 30 |

Housekeeping: Article 3 authority chain updated to reference v1.2 (not listed separately).

---

## Amendments to Existing Articles

### Article 5 — `media_type_registry` (Amended v1.2 — A-1, A-2)

Articles 5.1 through 5.6 are unchanged from v1.1.0. The following sub-articles are added.

---

**5.7** `[New v1.2 — A-1]` Phase boundary criteria. A media type's phase assignment is
determined by the following criteria. Phase assignments may not be changed without a
constitutional amendment. A media type that comes to satisfy the criteria of an earlier phase
may be reclassified by amendment.

**Phase 1** — immediate activation authorized by this Constitution:

(a) Single-file asset: one master `media_file` per `source_item`.
(b) Delivery governed by IIIF Presentation API 3.0 and IIIF Image API — infrastructure
    present in NC's stack at Phase 1 activation.
(c) Archival format: TIFF or JPEG2000 — supported by NC workers at Phase 1.
(d) Rights model: fully determinable by standard PD rules — US publication before 1928
    or life+70 (international); no ancillary rights complexity (no performance rights,
    no sound recording rights, no unsettled 3D scan disputes).

**Phase 2** — requires constitutional amendment before activation:

(a) Multi-file asset (`requires_file_manifest = true`), OR single-file asset delivered
    by a protocol not present in NC's Phase 1 stack.
(b) Requires at least one new `delivery_protocol` value in the Article 23.2 vocabulary.
(c) Introduces new `content_spec_schema` field categories not present in Phase 1:
    text layers, chapter structure, track sequencing, or reading-order metadata.
(d) Extends the Phase 1 IIIF delivery pipeline (multi-Canvas manifest) or introduces
    a new delivery protocol alongside it. Does not replace Phase 1 infrastructure.

**Phase 3** — requires Phase 2 infrastructure proven in production + constitutional amendment:

(a) Time-based media: streaming delivery required; download or IIIF is not sufficient.
(b) New archival format standard requiring dedicated format validation tooling
    (FFV1/MKV, BWF at scale).
(c) Infrastructure dependency on a Phase 2 type: the Phase 3 type reuses Phase 2
    archival format workers (audio reuses audiobook's BWF pipeline; film requires
    HTML5 streaming proven by audio).
(d) Rights model may involve ancillary complexity: performance rights or sound
    recording copyright requiring additional human verification steps.

**Phase 4** — requires Phase 3 infrastructure proven in production + constitutional amendment:

(a) Non-linear, volumetric, or aggregated structure: not reducible to a sequential
    ordered file list.
(b) New delivery protocol not present in Phases 1–3.
(c) Rights model involves unsettled or contested law: 3D scan copyright status,
    dataset compilation rights, or equivalent.
(d) Infrastructure dependency on Phase 3 completion.

---

**5.8** `[New v1.2 — A-2]` Constitutional activation sequence. The following table governs
the order in which media types may reach `status = 'active'` in `media_type_registry`.
This is a governance constraint on human approval decisions, not a database constraint.
Approval of a type that violates its prerequisite is a constitutional violation.

| Priority | media_type_id | Phase | Concurrent | Prerequisite |
|---|---|---|---|---|
| 1 | `image` | 1 | With `map`, `photography`, `poster` | None |
| 1 | `map` | 1 | With `image`, `photography`, `poster` | None |
| 1 | `photography` | 1 | With `image`, `map`, `poster` | None |
| 1 | `poster` | 1 | With `image`, `map`, `photography` | None |
| 2 | `book` | 2 | With `ebook` | Phase 1 complete; Amendment P2-1 ratified |
| 2 | `ebook` | 2 | With `book` | Phase 1 complete; Amendment P2-1 ratified |
| 3 | `audiobook` | 2 | No | `book` active AND one book `source_item` activated in production |
| 4 | `audio` | 3 | No | `audiobook` active AND one audiobook `source_item` activated; Amendment P3-1 ratified |
| 5 | `film` | 3 | No | `audio` active AND one audio `source_item` activated; Amendment P3-1 ratified |
| 6 | `dataset` | 4 | No | Phase 3 complete; Amendment P4-1 ratified |
| 7 | `3d` | 4 | No | `dataset` active AND one dataset `source_item` activated; Amendment P4-1 ratified |

Definitions:

- **Phase N complete**: all media types in Phase N have `status = 'active'` in
  `media_type_registry` AND at least one `source_item` per type has reached `activated`
  status in production.
- **"One source_item activated"** prerequisites (audiobook, audio, film, 3d): confirm the
  predecessor type's infrastructure pipeline is production-proven before extending it.
  Proving the pipeline with one record is the constitutional minimum; the Director may
  require more before approving an amendment.

---

### Article 23 — Activation Protocol (Amended v1.2 — A-2)

Articles 23.1 and 23.2 are unchanged from v1.1.0. The following sub-articles are added.

---

**23.3** `[New v1.2 — A-2]` The constitutional activation order for all eleven governed
media types, expressed as a total sequence:

```
Step 1 — Phase 1 (this Constitution, no additional amendment):
  image + map + photography + poster (concurrent)

Step 2 — Phase 2 (Amendment P2-1 required):
  book + ebook (concurrent)
    ↓ book file manifest proven in production
  audiobook

Step 3 — Phase 3 (Amendment P3-1 required):
  audio
    ↓ BWF streaming proven in production
  film

Step 4 — Phase 4 (Amendment P4-1 required):
  dataset
    ↓ dataset pipeline proven in production
  3d
```

Each step requires the completion of the preceding step. Steps within a step that show
concurrent activation may proceed simultaneously under a single amendment. Steps separated
by a "proven in production" line require an intervening operational gate — at least one
production-activated `source_item` of the preceding type — before the next type may proceed.

**23.4** `[New v1.2 — A-2]` Future amendment authorization framework. Amendments P2-1,
P3-1, and P4-1 are constitutional amendments to this Constitution. They do not exist yet.
This article records what each must address at minimum before ratification.

**Amendment P2-1 must address:**
1. File manifest governance: rules for multi-file `source_item` assembly, `sequence_position`
   ordering, and manifest integrity verification.
2. Multi-Canvas IIIF manifest generation rules for `book` type.
3. EPUB3 delivery protocol governance for `ebook` type.
4. `audiobook` sequencing prerequisite: confirmation that the `book` pipeline is
   production-proven before `audiobook` may activate.
5. DD-4 mandatory precondition: the `illustration_opportunities → asset_opportunities` table
   rename must be complete before P2-1 may be ratified (per DD-4 of v1.1.0).

**Amendment P3-1 must address:**
1. BWF-at-scale format validation rules: fixity requirements, sample rate and bit depth
   verification, broadcast chunk validation.
2. HTML5 audio streaming governance for the `audio` type.
3. HLS delivery infrastructure governance for the `film` type.
4. Film segment handling: `file_role = 'segment'` multi-file assembly and HLS playlist
   generation rules.
5. Performance rights and sound recording rights verification protocol for time-based media
   (supplemental to the existing rights model).

**Amendment P4-1 must address:**
1. 3D scan copyright determination rules: the constitutional position NC takes on the
   copyright status of 3D scans of PD physical objects.
2. DCAT and Schema.org `Dataset` type governance for the `dataset` type.
3. Direct download delivery rules: canonical download URL structure, versioning, and
   `asset_delivery_manifest` requirements for `delivery_protocol = 'download'`.
4. model-viewer delivery governance: glTF 2.0 conformance requirements, texture and
   material derivative handling.

---

## Part IX — Constitutional Reference Institution Framework

### Article 28 — Reference Institution Registry `[New v1.2 — A-3]`

**28.1** A constitutional reference institution is an external institution whose governance
framework, metadata standards, preservation practices, or vocabulary are formally adopted
as NC constitutional doctrine. A reference institution's rules appear in one or more NC
constitutional articles. A reference institution is not a data source relationship. It is
a governance relationship. The distinction: NC may acquire assets from any governed source
institution; NC adopts governance patterns only from constitutional reference institutions.

**28.2** Tier classification:

| Tier | Definition |
|---|---|
| **Tier 1 — Constitutional Governance** | The institution's standards, vocabularies, or frameworks are directly cited in NC constitutional articles. Adoption of the institution's governance rules is mandatory for the governed domain. |
| **Tier 2 — Operational Reference** | The institution's quality standards or delivery patterns are NC operational reference. No institution-level governance rule is constitutionally mandated. The institution's policies do not bind NC's implementation. |

**28.3** The six evaluated institutions and their constitutional classifications:

| Institution | Tier | Governance domains |
|---|---|---|
| Library of Congress | Tier 1 | Metadata standards (MARC 21, MODS), preservation events (PREMIS), rights vocabulary (NoC-US/1.0/), image subject terms (TGM), transfer packaging (BagIt) |
| Europeana | Tier 1 | Metadata aggregation model (EDM), rights statement vocabulary (Rights Statements Working Group) |
| Smithsonian Institution | Tier 1 | 3D digitization output standard (Smithsonian X 3D), CC0 institutional source verification protocol |
| Internet Archive | Tier 1 | Metadata schema standards (OAI-PMH, Dublin Core), WORM file philosophy |
| British Library | Tier 1 | Audio archival format (BWF), sound archive preservation event sequence |
| UNESCO | Tier 2 | Cultural heritage policy reference; Memory of the World provenance signal |

**28.4** The constitutional reference institution registry is a governance document, not a
database table. Institutions may be added, elevated between tiers, or reclassified only by
constitutional amendment.

**28.5** Tier 1 designation does not mean NC endorses the institution's full governance model.
Article 30 records the explicit rejections. Tier 1 means: NC formally adopts the named
rules from this institution and recognizes the institution as the authority for those rules.
If the institution publishes a breaking revision to a governed standard, NC must evaluate
the impact within one calendar quarter of the revision's effective date.

---

### Article 29 — Adopted Governance Rules `[New v1.2 — A-3]`

This article enumerates the governance rules formally adopted from each Tier 1 reference
institution. Rules listed here that correspond to pre-existing constitutional articles are
now attributed to the named institution; the institution is the governing authority for
that rule. Rules listed here that are new to v1.2 are additive to — and do not supersede —
the entity governance in Articles 5–14.

---

**29.1 — Library of Congress**

(a) **MARC 21 and MODS metadata standards.** MARC 21 and MODS are governed `schema_standard`
values in the Article 7.5 vocabulary. LOC is the authority for these standards. Any breaking
revision by LOC triggers a mandatory NC evaluation within one calendar quarter. (Existing
rule — attributed to LOC in v1.2.)

(b) **NoC-US/1.0/ rights statement.** `http://rightsstatements.org/vocab/NoC-US/1.0/` is
a governed `media_rights.rights_statement_uri` value under Article 24.1. LOC co-authored
this statement through the Rights Statements Working Group. It is the governing rights
statement for US-published works in the public domain under US copyright law. (Existing
rule — attributed to LOC/Rights Statements WG in v1.2.)

(c) **PREMIS preservation event framework.** PREMIS (Preservation Metadata: Implementation
Strategies) is the governing framework for `preservation_event` under Article 13. LOC
co-maintains PREMIS. Any new `preservation_event.event_type` value must be evaluated for
PREMIS compatibility before constitutional adoption. (Existing rule — attributed to LOC
in v1.2.)

(d) **LOC Thesaurus of Graphic Materials (TGM) as subject term authority.** For
`media_type_id IN ('image', 'map', 'photography', 'poster')`, TGM is the governing
subject term authority for the `subject_terms` field within `media_technical_metadata.content`.
TGM terms are the canonical values. Non-TGM terms must be tagged `controlled_vocabulary: false`
in the `content` JSONB. This rule applies from Phase 1 activation.
(New rule added in v1.2.)

(e) **BagIt transfer packaging for LOC bulk delivery.** Files delivered to NC from LOC
in bulk transfers must be received as BagIt packages (RFC 8493). The ingestion
`preservation_event.event_detail` for LOC-sourced bulk file deliveries must include
`bagit_checksum_verified: true`. Files acquired via direct API calls (where BagIt is
inapplicable) must note `transfer_method: 'api'` in `event_detail`. A bulk LOC-sourced
file received outside a BagIt package whose `event_detail` does not record
`bagit_checksum_verified: true` is a preservation integrity violation.
(New rule added in v1.2.)

---

**29.2 — Europeana**

(a) **EDM tripartite aggregation model.** The Europeana Data Model (EDM) tripartite
structure governs the NC substrate mapping: `edm:ProvidedCHO` = `source_item`;
`ore:Aggregation` = `source_record`; `edm:WebResource` = `media_file`. This mapping
is maintained in Article 7.6 and governs interpretation of all EDM-schema `source_record`
entries. Europeana is the authority for the EDM. (Existing rule — attributed to Europeana
in v1.2.)

(b) **Rights Statements Working Group vocabulary.** The Rights Statements Working Group
vocabulary (rightsstatements.org), co-authored by Europeana, governs `media_rights.rights_statement_uri`
under Article 24.1. Europeana is a co-authority for this vocabulary alongside LOC.
(Existing rule — attributed to Europeana/Rights Statements WG in v1.2.)

(c) **Minimum required metadata fields for EDM-schema source records.** A `source_record`
with `schema_standard = 'edm'` that lacks any of the following fields in `raw_payload`
must receive a `preservation_event` of `event_type = 'rights_verification'` with
`event_outcome = 'warning'`: `dc:title`, `dc:description`, `dc:date`, `edm:rights`.
These are the Europeana minimum mandatory metadata fields. A missing field does not block
ingestion. The warning must be written before rights verification begins and must be visible
to the human rights verifier. A rights verification approved without this evaluation for
a deficient EDM record is a constitutional violation.
(New rule added in v1.2.)

(d) **Image quality baseline.** Visual assets (`media_type_id IN ('image', 'map', 'photography',
'poster')`) must be evaluated against the Europeana minimum image resolution baseline —
400px minimum on the longest edge — during `media_technical_metadata` creation. Assets
below this threshold must have `quality_flag: 'below_minimum'` in `media_technical_metadata.content`.
This flag is a commerce scoring signal; it does not block activation. The quality gate
for commerce is in the downstream scoring layer (CSM), not the substrate. The substrate
records the finding; the scoring layer acts on it.
(New rule added in v1.2.)

---

**29.3 — Smithsonian Institution**

(a) **Smithsonian X 3D content specification.** For `media_type_id = '3d'`, the
`content_spec_schema` registered in `media_type_registry` must require the following
fields in `media_technical_metadata.content`, derived from the Smithsonian X 3D standard:
`capture_method`, `polygon_count`, `texture_resolution`, `coordinate_system`, `units`.
A 3D `source_item` lacking any of these fields in its active `media_technical_metadata`
may not advance to `activation_eligible`. This rule applies from the moment
`media_type_id = '3d'` reaches `status = 'active'` (Amendment P4-1).
(Formalizes existing reference in Article 12.6 — elevated to constitutional requirement
in v1.2.)

(b) **CC0 institutional source verification protocol.** For source institutions with
`rights_strategy = 'cc0_institutional'` in `sources.config`, the CC0 verification
protocol must confirm all three of the following before a `media_rights` record may be
set to `verified_cc0`: (i) the source institution has issued a blanket CC0 dedication
for the relevant collection; (ii) the specific asset is within the declared CC0 scope
per the institution's published documentation; (iii) the institutional CC0 statement URL
is recorded in `media_rights.rights_evidence` as `cc0_declaration_url`. The Smithsonian
Open Access policy (si.edu/openaccess) is the governing reference for this protocol.
A `verified_cc0` determination that lacks a `cc0_declaration_url` in `rights_evidence`
is a constitutional violation.
(New rule added in v1.2.)

---

**29.4 — Internet Archive**

(a) **OAI-PMH and Dublin Core metadata standards.** `oai_pmh` and `dc` are governed
`schema_standard` values in the Article 7.5 vocabulary. Internet Archive is the primary
reference institution for these standards in the NC context. (Existing rule — attributed
to Internet Archive in v1.2.)

(b) **WORM file philosophy.** The WORM (Write Once Read Many) principle for master
`media_file` records is constitutionalized in Articles 8.2 and 16.1. Internet Archive's
preservation doctrine is the reference for this principle. The invariant: once an
ingestion `preservation_event` is written for a master file, the file at its governed
MinIO key may not be overwritten. (Existing rule — attributed to Internet Archive in v1.2.)

(c) **IA rights self-assertion exclusion.** This rule is simultaneously an adoption and
an exclusion — NC adopts IA's WORM doctrine but explicitly rejects IA's rights
self-assertion model. IA-sourced content with `schema_standard = 'dc'` may not use
automated rights verification under Article 11.7. All IA-sourced content requires human
rights verification under Article 15.4, regardless of what the `dc:rights` field in the
`raw_payload` states. A `media_rights` record for an IA-sourced `source_item` whose
sole rights evidence is the IA `dc:rights` assertion is a constitutional violation of
Article 1.5. This rule may not be relaxed by Director Decision.
(New rule added in v1.2.)

---

**29.5 — British Library**

(a) **BWF as audio archival format.** BWF (Broadcast Wave Format, ITU-R BS.2088-1) is
the governing archival format for `media_type_id IN ('audio', 'audiobook')` under Article
12.6. British Library Sound Archive is the reference institution for this standard.
(Existing rule — attributed to British Library in v1.2.)

(b) **Minimum audio master quality standard.** Audio and audiobook master files
(`media_file.file_role IN ('master', 'track')`) sourced from British Library must achieve
a minimum of 24-bit word length / 96 kHz sample rate. Files that do not meet this standard
must receive a `preservation_event` with `event_type = 'validation'` and
`event_outcome = 'warning'`, with `event_detail` recording the measured word length and
sample rate. The warning must be recorded as `quality_flag: 'below_bl_standard'` in
`media_technical_metadata.content`. This flag is a commerce scoring signal and does not
block activation. This rule applies from Phase 2 activation (Amendment P2-1).
(New rule added in v1.2.)

(c) **Required preservation event sequence for audio and audiobook masters.** For
`media_type_id IN ('audio', 'audiobook')`, the minimum required preservation event sequence
for any `media_file.file_role IN ('master', 'track')` is: `ingestion` → `format_identification`
→ `validation` (BWF conformance check) → `fixity_check`. A master audio file that does not
have all four of these events in sequence may not advance past `acquired` status. This
sequence must be enforced by the acquisition worker before linking the file to its
`source_item`. This rule applies from Phase 2 activation (Amendment P2-1).
(New rule added in v1.2.)

---

**29.6 — UNESCO**

No governance rules are adopted from UNESCO as constitutional doctrine. UNESCO is a Tier 2
operational reference institution.

UNESCO relevance to NC operations:

(a) **Memory of the World provenance signal.** UNESCO's Memory of the World programme
designation for a source institution or collection is a recognized positive provenance
signal in the Asset Intelligence layer (institutional authority scoring). This is an
operational signal, not a constitutional substrate rule. No constitutional article governs it.

(b) **World Heritage Site geographic authority.** UNESCO World Heritage Site designations
are a recognized geographic authority signal for the Place Intelligence layer (TAS score).
This is likewise an operational signal, not a constitutional substrate rule.

No constitutional amendment is required to use these signals. They are operational inputs
to the downstream scoring layer.

---

### Article 30 — Rejected Governance Patterns `[New v1.2 — A-3]`

**30.1 — Purpose**

This article records the governance patterns from each reference institution that NC
explicitly does not adopt. Explicit rejection prevents scope creep: a future implementer
or amendment author cannot claim that NC's Tier 1 relationship with an institution implies
adoption of all that institution's practices. These exclusions are permanent unless
reversed by constitutional amendment.

---

**30.2 — Library of Congress**

(a) **Full MARC 21 bibliographic validation.** NC does not implement full MARC 21 field
validation. `source_record.raw_payload` is stored verbatim. NC does not parse, validate,
or reject records based on individual MARC field codes. Complete MARC validation is the
source institution's responsibility. NC's obligation is verbatim storage.

(b) **Patron and researcher service model.** LOC's model of reading room access, duplication
orders, and reference services for scholars and researchers is not adopted. NC is a
commerce platform. Researcher service is a library function outside NC's mission.

(c) **In-copyright holdings.** LOC holds both PD and in-copyright materials. NC's PD hard
gate (Article 1.5) means LOC's in-copyright collection model does not apply. NC never
holds, acquires, or commercializes in-copyright works.

---

**30.3 — Europeana**

(a) **Full EDM entity model.** EDM defines `edm:Agent`, `edm:Event`, `edm:PhysicalThing`,
and `edm:Place` as entities beyond the adopted tripartite model. NC does not implement
the full EDM entity model. NC maps provenance to W3C PROV (Article 22) and uses the
`places` table for geographic entities. Full EDM entity implementation is explicitly out
of scope.

(b) **Multilingual metadata mandate.** Europeana requires multilingual metadata for all
aggregated collections. NC's current scope is English-language commerce. Multilingual
metadata is a future extension — it is not a constitutional requirement and Europeana's
multilingual mandate does not bind NC.

(c) **Pan-European geographic scope.** Europeana's collection policy prioritizes European
cultural heritage. NC is globally scoped and not regionally bounded. Europeana's geographic
scope limits do not constrain NC's acquisition or activation decisions.

(d) **Metadata re-aggregation rights.** Europeana's framework includes institutional
provisions about rights over aggregated metadata. NC's constitutional position: metadata
derived from PD sources is PD. NC asserts no proprietary rights over aggregated PD
metadata and does not adopt Europeana's aggregation rights posture.

---

**30.4 — Smithsonian Institution**

(a) **Digitization mandate.** The Smithsonian has an active digitization mission. NC does
not digitize physical objects. NC aggregates from already-digitized sources. Smithsonian's
digitization protocols, capture specifications, and object handling standards are not adopted.

(b) **Specimen-centric labeling.** Smithsonian's natural history collection labeling
standards (catalog numbers, collection codes, preparation types, taxonomic identifiers
as primary keys) are not adopted as NC metadata standards. NC's primary anchor is
place + asset opportunity. Specimen identity is a secondary signal, not a governing key.

(c) **Internal 3D capture workflow.** Smithsonian X 3D is adopted as an output specification —
what a valid 3D model record must contain (Article 29.3(a)). Smithsonian's internal
capture workflows, photogrammetry protocols, equipment standards, and processing pipelines
are not adopted. NC governs what it receives, not how it was produced.

---

**30.5 — Internet Archive**

(a) **Rights self-assertion model.** IA accepts user-uploaded content with self-asserted
rights statements. NC does not. This rejection is constitutionalized in Article 29.4(c)
and may not be relaxed by Director Decision.

(b) **"Anything goes" ingestion philosophy.** IA's broad ingestion policy accepts content
with low quality thresholds and minimal curation. NC's quality gate (CSM scoring) and
constitutional governance produce a curated, scored, commercially viable inventory. IA's
ingestion philosophy is incompatible with NC's commerce mission.

(c) **Controlled Digital Lending (CDL).** IA's CDL model lends in-copyright books under
a DRM system on a "one copy, one user" basis. NC does not hold, acquire, or lend
in-copyright works. CDL is entirely inapplicable.

---

**30.6 — British Library**

(a) **Legal deposit function.** BL has legal deposit authority under UK law, requiring
UK publishers to deposit copies of new publications. NC has no legal deposit relationship
with any institution and no legal deposit obligations. BL's legal deposit framework
does not apply.

(b) **In-copyright access programs.** BL operates licensed access programs (ETAS and
equivalents) for in-copyright digital content. NC is PD-only. These programs are
inapplicable.

(c) **Manuscript and visual digitization workflows.** BL has proprietary internal workflows
for manuscript digitization (multispectral imaging, conservation-grade scanning). NC adopts
BL's audio preservation standards (Article 29.5). BL's visual and manuscript digitization
workflows are not adopted; they govern how BL produces its digitized assets, which is
outside NC's scope.

---

**30.7 — UNESCO**

(a) **Intangible cultural heritage (ICH) framework.** UNESCO's ICH Convention governs
living traditions, oral heritage, performing arts, and social practices. These categories
are not PD-eligible by definition: they are living, actively practiced, and often
community-owned. NC governs only fixed, PD-eligible recorded works. UNESCO's ICH
framework is entirely out of scope and is not adopted in any form.

(b) **State-actor governance model.** UNESCO operates as an intergovernmental body with
member state obligations and voting structures. NC is a constitutional commercial platform
governed by its own doctrine. UNESCO's intergovernmental governance structures do not apply.

(c) **Multilingual content rights framework.** UNESCO promotes protection of linguistic
diversity and has frameworks for multilingual cultural content rights. NC's current
commercial scope is English-language. This framework is not adopted.

(d) **"Right to culture" free access mandate.** UNESCO promotes universal free access to
cultural heritage as a human right. NC is a commerce platform; access to NC's products
is commercial. UNESCO's free-access mandate does not apply to NC's product layer. This
rejection does not contradict NC's PD mission: the underlying PD assets are public by
definition. NC's products, scores, collections, and derived commercial outputs are NC
intellectual property and are priced accordingly.

---

## Articles Not Listed

All articles not appearing in this amendment document are unchanged from
`media_substrate_constitution_v1.1.md` (v1.1.0) and carry full force in v1.2.0.

---

## Open Questions

None. All open questions from v1.1 remain resolved. Amendments P2-1, P3-1, and P4-1
are future documents, not open questions — their content requirements are defined in
Article 23.4 and are not ambiguous at this time.
