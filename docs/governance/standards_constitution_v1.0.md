# Standards Constitution v1.0

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified — effective immediately |
| Repository | opengracelabs/nc |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |

---

## Preamble

This Constitution maps every NC subsystem to 13 external standards and issues a governance
ruling for each pairing: Adopt, Map, Extend, or Invent Last. It defines where NC is a
compliant participant in the heritage data ecosystem, where NC builds bridges to peer
systems, where NC adds commercial intelligence on top of existing standards, and where
NC's commercial mission requires invention with no prior art.

The purpose is not interoperability for its own sake. NC is not a library catalog, a
biodiversity database, a GIS platform, or a digital archive. NC is the world's
place-centered public domain heritage commerce platform. Standards governance serves two
commercial ends: (1) keeping NC's source ingestion pathways open to peer institutions;
and (2) ensuring NC's commercial intelligence — the scores, the tiers, the anchor
classifications, the commerce routing — is unmistakably NC's own.

**The governing axiom of this Constitution: adopt the data layer, own the intelligence
layer.** Standards govern what NC receives, stores, preserves, and delivers. Inventions
govern what NC creates: the commercial scoring, the anchor classification, the activation
lifecycle, and the place-asset routing that make NC's catalog competitively defensible.

---

## Part I — Doctrine

### Article 1 — Scope

**1.1 — Covered subsystems:**

| ID | Subsystem | Primary tables / entities |
|---|---|---|
| SS-01 | Source Record | `source_record` |
| SS-02 | Source Item | `source_item` |
| SS-03 | Media File | `media_file`, `media_derivative` |
| SS-04 | Media Rights | `media_rights` |
| SS-05 | Media Technical Metadata | `media_technical_metadata` |
| SS-06 | Preservation Event | `preservation_event` |
| SS-07 | Asset Delivery Manifest | `asset_delivery_manifest` |
| SS-08 | Asset Opportunity | `illustration_opportunities` |
| SS-09 | Activation Target | `activation_target` |
| SS-10 | Place | `places`, PostGIS geometry |
| SS-11 | Subject Terms | TGM vocabulary, `media_technical_metadata.content.subject_terms` |
| SS-12 | Creator Authority | `creator_authority_registry` |
| SS-13 | Collection | `collections` |
| SS-14 | Commerce Opportunity | `commerce_opportunities` |
| SS-15 | Workflow / Pipeline | `workflow_items`, `discovery_candidates` |
| SS-16 | Provenance (cross-cutting) | `provenance` JSONB columns, `projection_event` |
| SS-17 | Relationship Intelligence | Neo4j graph (pending SD-AMEND-1) |
| SS-18 | FM Advisory | `fm_inference_record`, `fm_candidate_record` |

**1.2 — Covered standards:** CIDOC CRM, SKOS, Dublin Core (DCTERMS), PROV-O, PREMIS,
IIIF, Darwin Core, GeoJSON, JSON-LD, Schema.org, Europeana EDM, Wikidata, GeoNames.

**1.3 — Not covered by this Constitution:** application code, internal API logic, UI
markup (except JSON-LD structured data output), worker implementation details. Those are
governed by implementation constitutions (Media Substrate, Wireframe, Foundation Model).

### Article 2 — The Four Postures

**Adopt** — NC uses the standard's vocabulary, data model, or protocol directly within
the governed scope. The subsystem produces and consumes compliant output without
translation. Implementation must conform to the standard's normative requirements. Where
the standard offers optionality (SHOULD vs. MUST), NC's choice is governed by the
relevant article per standard.

**Map** — NC maintains a governed, versioned mapping between its internal model and the
standard's terms. NC does not adopt the standard's model internally, but produces
compliant output for federation and interoperability. The mapping is a governed artifact:
it must be updated when either the NC schema or the external standard evolves. A mapping
that falls out of date is a governance violation.

**Extend** — NC adopts the standard as a base and adds NC-specific classes, properties,
or event types absent from the standard. Extensions must be backwards-compatible: a
standard-compliant consumer processes the base content without error, ignoring NC
extensions. Extensions are declared in Part IV and versioned independently.

**Invent Last** — No existing standard adequately governs the domain. This designation
signals that NC has verified no existing standard covers the need before inventing its
own model. Inventions are declared in Part V. Every Invent Last item is reviewed annually
for standard emergence. If a relevant standard emerges, a constitutional amendment governs
the transition.

**Hierarchy:** When postures conflict for the same subsystem, Adopt supersedes Map
supersedes Extend. Invent Last applies only to the gap the other three cannot cover.

### Article 3 — Authority Precedence

**Standards govern the data layer:**

- What a source record contains (Dublin Core, EDM, CIDOC CRM mapping)
- How files are preserved (PREMIS)
- How images are delivered (IIIF)
- How places are identified (GeoNames, GeoJSON)
- How provenance is expressed (PROV-O)
- How subjects are organized (SKOS, TGM)
- How structured data is published to the web (Schema.org, JSON-LD)

**NC inventions govern the intelligence layer:**

- How assets are scored for commercial opportunity (COS)
- How assets are classified for scoring (anchor_type)
- How assets are tiered for routing (CSM tier)
- How places connect to asset relevance (place relevance score)
- How FM advisory outputs are governed (candidate boundary)

Adopting a standard for the data layer does not constrain NC's commercial intelligence
layer. NC may produce a Schema.org/Product with standard structured data while scoring
that product with a fully invented COS formula. These layers do not conflict.

**S-1 — Standards Authority Invariant:** No external standard overrides PostgreSQL
canonical records for internal state. Standards govern the shape and vocabulary of
NC's outputs and mappings, not its internal authority chain.

### Article 4 — Mapping Governance Rules

**4.1** Every mapping declared in Part II must be implemented as a governed artifact:
a documented field crosswalk in `docs/standards/`, a validated transform layer in the
API, or a test that produces compliant output. "We intend to map" is not a mapping.

**4.2** Mappings are versioned. When an external standard publishes a new major version,
the Director assesses whether the mapping is affected within 60 days. If affected, a
constitutional amendment governs the update.

**4.3** Extensions declared in Part IV are versioned independently of their base
standard. A breaking change to an extension requires a constitutional amendment.

**4.4** Invent Last items in Part V are reviewed at each new major NC version. The review
determines: (a) whether a relevant standard has emerged; (b) whether the invention should
remain, be replaced by a standard, or be mapped to an emerging standard.

---

## Part II — Standard Rulings

### Article 5 — CIDOC CRM

**Ruling: Map**

CIDOC CRM (ISO 21127:2023) is the ICOM/ICOMOS formal ontology for cultural heritage
documentation. It governs the semantic interoperability layer between museums, libraries,
archives, and research institutions globally.

**Why Map, not Adopt:** CIDOC CRM is an OWL ontology. NC's authority layer is relational
PostgreSQL. Adopting CRM internally would require RDF as the canonical model —
incompatible with NC's frozen stack. The mapping is sufficient for institutional
federation.

**Entity-level CRM mapping:**

| NC entity | CRM class | Rule |
|---|---|---|
| `source_item` | `E22_Human-Made_Object` | One-to-one. The physical or digital object NC commercializes. |
| `source_item.title` | `E35_Title` | `P102_has_title`. |
| `creator_authority_registry` entry | `E21_Person` / `E74_Group` | `P14i_performed` (creation activity). |
| `places` | `E53_Place` | `P55_has_current_location` for place-anchored items. |
| `preservation_event` | `E7_Activity` | `P14_carried_out_by` (ingestion worker as `E39_Actor`). |
| `media_rights` record | `E30_Right` | `P75i_is_possessed_by` (NC as `E40_Legal_Body`). |
| `source_record` raw fetch | `E13_Attribute_Assignment` | `P140_assigned_attribute_to source_item`. |
| Era (1750–1900) | `E52_Time-Span` | `P4_has_time-span` for `source_item.publication_year`. |
| Ingestion event | `E65_Creation` | `P94_was_created` (source_item as output). |
| `illustration_opportunity_places` link | `E13_Attribute_Assignment` | Attribute assignment of place relevance to source_item. |

**Scope of the map:** SS-01, SS-02, SS-04, SS-06, SS-08, SS-10, SS-12, SS-13, SS-16, SS-17.

**Explicitly outside CRM scope:** SS-14 (Commerce Opportunity), commercial scoring
signals (COS, CSM tier, anchor_type weights). No CRM class governs commercial scoring.
This is by design — NC's intelligence layer has no CRM analogue.

**Activation trigger:** CRM mapping must be implemented (as a documented crosswalk and
API output) before NC offers institutional data exchange with Europeana, Smithsonian, or
peer museum APIs.

### Article 6 — SKOS

**Ruling: Adopt**

SKOS (W3C 2009) governs controlled vocabularies, thesauri, and concept schemes. NC uses
TGM (LOC Thesaurus of Graphic Materials) as the primary subject term authority. TGM is
published as a SKOS concept scheme. NC inherits SKOS by adopting TGM.

**6.1 — TGM as Primary Subject Term Authority.** All entries in
`media_technical_metadata.content.subject_terms` must be resolvable to TGM concept URIs
(`http://id.loc.gov/vocabulary/graphicMaterials/{term}`). TGM is a `skos:ConceptScheme`.
NC does not maintain a competing thesaurus for graphical subject terms.

**6.2 — Anchor Type Vocabulary.** NC's `anchor_type` vocabulary
(biological / geographic / cultural / mixed) must be expressed as a SKOS
`ConceptScheme` with NC as issuing authority (`nc:AnchorTypeScheme`). Each value is a
`skos:Concept` with `skos:prefLabel` (English), `skos:definition`, `skos:topConceptOf`,
and `skos:closeMatch` to its nearest peer standard (see Part IV, Article 21).

**6.3 — Media Type Registry.** `media_type_registry` values must be expressible as a
SKOS `ConceptScheme` (`nc:MediaTypeScheme`). Each `media_type_id` is a `skos:Concept`.
Where an equivalent term exists in the LOC format vocabulary
(`http://id.loc.gov/vocabulary/formatTypes/`), `skos:exactMatch` must be declared.

**6.4 — Priority Illustrator Collection.** The priority illustrator list (Audubon,
Gould, Merian, Redouté, Lear, Nodder, Haeckel, Wolf) is expressible as a
`skos:Collection` annotating the relevant `creator_authority_registry` entries. This is
a `skos:Collection` (unordered, no hierarchy), not a `ConceptScheme` — illustrators
are an authority registry, not a knowledge organization system.

**6.5 — Rights Statement Vocabulary.** `media_rights.rights_statement_uri` values must
be from `rightsstatements.org` or `creativecommons.org`. These vocabularies are
SKOS-compatible. NC does not invent rights statement URIs.

**Scope:** SS-02, SS-04, SS-05, SS-08, SS-10, SS-11, SS-12, SS-13. Extension in SS-14
(anchor_type scoring annotation, Part IV Article 21).

### Article 7 — Dublin Core (DCTERMS)

**Ruling: Adopt**

Dublin Core (ISO 15836:2019) and its terms extension (DCTERMS) provide the baseline
metadata vocabulary for resource description. Dublin Core is the floor for all NC
descriptive metadata. Every NC `source_item` can be expressed in DCTERMS without loss of
core descriptive content.

**DCTERMS to NC field mapping:**

| DCTERMS term | NC field | Rule |
|---|---|---|
| `dcterms:title` | `source_item.title` | Direct. |
| `dcterms:creator` | `source_item.illustrator` (authority form) | Maps to `creator_authority_registry`. |
| `dcterms:subject` | TGM terms + anchor_type | SKOS concepts per Article 6. |
| `dcterms:description` | `source_record.raw_payload.description` | From institution. NC does not author descriptions in DC. |
| `dcterms:publisher` | `sources.name` | The source institution, not NC. |
| `dcterms:created` | `source_item.publication_year` | Year of original publication, not NC ingestion. |
| `dcterms:type` | `media_type_registry.media_type_id` | Mapped to DCMI type vocabulary: `dctype:StillImage`, `dctype:Text`, `dctype:Sound`, `dctype:MovingImage`, `dctype:Dataset`. |
| `dcterms:format` | `media_technical_metadata.content.format` | MIME type. |
| `dcterms:identifier` | `source_item.{institution}_item_id` | Institution-assigned identifier. NC UUID uses `dcterms:identifier` with NC namespace. |
| `dcterms:source` | `source_record.source_url` | The institutional record URL. |
| `dcterms:rights` | `media_rights.rights_statement_uri` | Rights statement URI (rightsstatements.org). |
| `dcterms:coverage` | Linked `places.name` | Geographic coverage as place name. |
| `dcterms:isPartOf` | `collections.title` (if activated) | Collection membership. |

**Adoption rule:** DCTERMS is preferred over DC15 elements. `dcterms:created` not
`dc:date`. `dcterms:rights` not `dc:rights`. NC does not use bare DC elements where a
DCTERMS refinement is available.

**What DC does not cover:** NC commercial intelligence fields (COS, CSM tier, anchor
type, place relevance score, illustrator prestige) have no DC equivalents. These are NC
inventions (Part V).

**Scope:** SS-01, SS-02, SS-03, SS-04, SS-07, SS-08, SS-10, SS-11, SS-12, SS-13.

### Article 8 — PROV-O

**Ruling: Map** (with extension for FM advisory provenance — see Part IV Article 23)

PROV-O (W3C 2013) governs provenance representation. NC's Strategic Directive mandates
provenance on every row. NC's internal provenance model (JSONB `provenance` columns,
`preservation_event`, `fm_inference_record`) is not RDF-native, but every key provenance
claim maps to PROV-O.

**Why Map, not Adopt:** PROV-O is an OWL ontology. NC stores provenance as structured
JSONB in PostgreSQL. The mapping enables external audit and compliance without forcing
NC off its frozen stack.

**PROV-O mapping:**

| NC construct | PROV-O class / property | Rule |
|---|---|---|
| Source record (fetched from institution) | `prov:Entity` | The fetched document is a PROV-O entity. |
| Ingestion worker run | `prov:Activity` | The ingestion activity. |
| Ingestion worker | `prov:Agent` (`prov:SoftwareAgent`) | Worker identity. |
| `source_item` (derived from source_record) | `prov:Entity` `prov:wasDerivedFrom source_record` | Derivation provenance. |
| Human approval action | `prov:Activity` `prov:wasAssociatedWith prov:Person` | The human approver. |
| Rights verification | `prov:Activity` `prov:used media_rights_evidence` → `prov:generated media_rights` | Two-entity provenance chain. |
| FM inference | `nc:StochasticActivity` (subclass of `prov:Activity`) | See Part IV Article 23. |
| FM candidate | `prov:Entity` `prov:wasGeneratedBy fm_inference` | Candidate entity. |
| Canonical promotion | `prov:Entity` `prov:wasDerivedFrom fm_candidate` `prov:wasAttributedTo human_approver` | Human makes the attribution. |
| `preservation_event` | `prov:Activity` | Maps to both PROV-O Activity and PREMIS Event. |
| Director Decision | `prov:Activity` `prov:wasAssociatedWith prov:Person` | Governance activity. |

**Scope:** SS-01, SS-02, SS-06, SS-08, SS-09, SS-15, SS-16, SS-17. Extension in SS-18.

### Article 9 — PREMIS

**Ruling: Extend**

PREMIS (Library of Congress v3.0) is the standard for digital preservation metadata.
NC's Media Substrate Constitution mandates PREMIS alignment for `preservation_event` and
`media_file`. This article formalizes the adoption scope and the NC extension layer.

**Base PREMIS adoption (no NC modifications):**

| PREMIS entity | NC equivalent | Rule |
|---|---|---|
| Object (intellectual) | `source_item` | The intellectual entity NC commercializes. |
| Object (file) | `media_file` | File-level PREMIS object with format, fixity, size, storage location. |
| Object (bitstream) | `media_derivative` | Derivative representations. |
| Event | `preservation_event` | Full PREMIS event: event type from LOC vocabulary, event identifier, datetime, detail, linking objects/agents. |
| Agent | Workers (`worker_id`) + Human (`reviewed_by`) | One PREMIS agent per event. |
| Rights | `media_rights` | PREMIS rights basis (copyright / license / other) maps to `media_rights.rights_basis`. |

**Required PREMIS event types from the LOC controlled vocabulary** (use standard LOC
event type URIs — not NC-invented strings):

| Event | LOC URI | NC trigger |
|---|---|---|
| ingestion | `http://id.loc.gov/vocabulary/preservation/eventType/ing` | `source_record` first fetch |
| fixity check | `http://id.loc.gov/vocabulary/preservation/eventType/fix` | `media_file` checksums |
| format identification | `http://id.loc.gov/vocabulary/preservation/eventType/for` | `media_file` format normalization |
| normalization | `http://id.loc.gov/vocabulary/preservation/eventType/nor` | JPEG2000 / archival format conversion |
| validation | `http://id.loc.gov/vocabulary/preservation/eventType/val` | Schema + rights validation |
| deletion | `http://id.loc.gov/vocabulary/preservation/eventType/del` | Retraction of `media_file` |

**NC PREMIS event extensions** (see Part IV Article 23 for URIs and full declarations):

| NC event | NC trigger |
|---|---|
| `nc:activation` | `activation_target` → `activated` |
| `nc:retraction` | `activation_target` → `retracted` (Director Decision required) |
| `nc:rights_commercial_clearance` | `media_rights.rights_status` set to `verified_pd` by human verifier |
| `nc:commerce_scoring` | `commerce_opportunities` score computed or recalculated |

**Extension invariant:** NC extension event types must never shadow LOC event type URIs.
LOC events are adopted without modification. NC events cover the activation lifecycle and
commercial layer that PREMIS does not address.

**Scope:** SS-03, SS-04, SS-06, SS-09. Extension in SS-18 (FM candidate events).

### Article 10 — IIIF

**Ruling: Extend**

IIIF Presentation API 3.0 and Image API 3.0 are the delivery standards for all Phase 1
visual media types (image, map, photography, poster). Ruled in Media Substrate
Constitution v1.2. This article formalizes the adoption and extension scope.

**Base IIIF adoption (no NC modifications):**

| IIIF element | NC use | Rule |
|---|---|---|
| Manifest | `asset_delivery_manifest.manifest_payload` | One manifest per `activation_target`. Top-level type: `Manifest`. |
| Canvas | Per `media_file` for visual assets | One canvas per primary image. |
| Annotation Page | Per canvas | IIIF painting annotations. |
| Annotation body | IIIF Image API URL to MinIO | Standard IIIF image body. |
| `label` | `source_item.title` | Multilingual label. |
| `metadata` | DCTERMS fields (Article 7) | Standard IIIF metadata array. |
| `rights` | `media_rights.rights_statement_uri` | Required. Never empty. |
| `requiredStatement` | Institution attribution | Standard attribution. |
| `provider` | Source institution + NC | Standard provider array. |
| `thumbnail` | IIIF Image API thumbnail URL | Standard thumbnail annotation. |
| `homepage` | NC media page URL | Standard IIIF `homepage`. |
| `seeAlso` | Dublin Core metadata endpoint | Standard `seeAlso`. |

**NC IIIF commerce extension** (`nc:commerce_context` — see Part IV Article 22):

```jsonc
{
  "@context": [
    "http://iiif.io/api/presentation/3/context.json",
    "https://opengracelabs.com/ns/nc/iiif/commerce/1.0/context.json"
  ],
  "nc:activation_target_id": "uuid",
  "nc:csm_tier": "MASTERWORK",
  "nc:quality_tier_label": "Masterwork",
  "nc:shop_url": "https://nc.example/shop/...",
  "nc:product_count": 12
}
```

**IIIF invariants:**
- No manifest may be generated without `media_rights.rights_status = 'verified_pd'`
  and `activation_target.status = 'activated'`.
- The `rights` field must always be a valid `rightsstatements.org` URI.
- Phase 2–4 media types must not generate IIIF manifests until their Phase gate is
  satisfied (Media Substrate Constitution v1.2, Article 5.8).

**Scope:** SS-07, SS-03, SS-09. Extension in SS-13 (collection manifests).

### Article 11 — Darwin Core

**Ruling: Map**

Darwin Core (TDWG 2021) governs biological specimen and occurrence data. NC's
biological-anchored illustration opportunities (`anchor_type = 'biological'`) connect
to DwC taxa via GBIF. NC is not a biodiversity system. NC does not publish occurrence
records. NC maps to DwC for the biological intelligence layer only.

**DwC field mapping (biological anchor only):**

| NC field | DwC term | Rule |
|---|---|---|
| `illustration_opportunities.concept_id` (biological) | `dwc:taxonID` | Maps to GBIF taxon key. GBIF is DwC-compliant. |
| Taxon name string (from source_record) | `dwc:scientificName` | As found in source metadata. |
| Taxon rank (from GBIF) | `dwc:taxonRank` | kingdom / phylum / class / order / family / genus / species |
| Kingdom (from GBIF) | `dwc:kingdom` | Animalia / Plantae / Fungi / etc. |
| GBIF occurrence ID (evidence source) | `dwc:occurrenceID` | FK reference to GBIF occurrence evidence. |
| BHL publication (biological anchor) | `dwc:bibliographicCitation` | BHL item metadata as DwC citation string. |

**What NC does not adopt from DwC:**
- Occurrence records (NC does not publish sighting data)
- Observation events (no field observations in NC pipeline)
- Sampling framework (not applicable)
- MeasurementOrFact (NC quality scores are commercial, not scientific)

**Consumption rule:** NC reads DwC-compliant records from GBIF as evidence for
biological-anchored opportunities. DwC terms are consumed, not stored natively — they
inform `concept_id` resolution and are preserved in `source_record.raw_payload`.

**Scope:** SS-02 (biological anchor only), SS-08 (biological anchor only), SS-11
(biological subject terms only).

### Article 12 — GeoJSON

**Ruling: Adopt**

GeoJSON (IETF RFC 7946) is the wire format for all NC place geometry in API responses.
PostGIS natively exports GeoJSON. All API responses delivering place geometry must use
GeoJSON.

**Adoption scope:**

| NC entity | GeoJSON type | Rule |
|---|---|---|
| `places.geom` (point) | `Feature` + `geometry.type: "Point"` | `ST_AsGeoJSON()`. |
| `places.boundary` (polygon/multipolygon) | `Feature` + `"Polygon"` / `"MultiPolygon"` | `ST_AsGeoJSON()`. |
| Place collection response | `FeatureCollection` | All places in a region or search result set. |
| Asset-place link (API) | `Feature` with commerce properties in `properties` | See Article 12 `properties` convention below. |

**GeoJSON `properties` convention for NC place features:**

```jsonc
{
  "type": "Feature",
  "geometry": { "type": "Point", "coordinates": [lon, lat] },
  "properties": {
    "nc:place_id": "uuid",
    "nc:geonames_id": 12345,
    "nc:place_name": "Great Barrier Reef",
    "nc:feature_code": "RFU",
    "nc:activated_asset_count": 248,
    "nc:masterwork_count": 12
  }
}
```

**Coordinate system:** WGS 84 (EPSG:4326), required by RFC 7946. PostGIS geometry stored
in SRID 4326. No other coordinate system in GeoJSON output.

**GeoJSON does not govern:** place relevance scoring (Invent Last, Article 27), tourism
attraction scoring (Article 28), or the place-asset connection model. GeoJSON provides
the geometry; NC provides the commercial intelligence.

**Scope:** SS-10.

### Article 13 — JSON-LD

**Ruling: Adopt**

JSON-LD (W3C 2020) is the serialization format for all NC entity API responses intended
for external consumption, structured data markup, and linked data federation. JSON-LD is
not NC's internal storage format. PostgreSQL is the internal authority. JSON-LD is the
external expression layer.

**Adoption scope:**

**13.1 — Entity API responses.** All entity endpoints (`GET /api/v1/places/{id}`,
`/media/{id}`, `/collections/{slug}`, `/creators/{slug}`) must return JSON-LD with an
appropriate `@context`. The NC context document is versioned:
`https://opengracelabs.com/ns/nc/v1/context.json`.

**13.2 — Page structured data markup.** Embedded `<script type="application/ld+json">`
on all canonical public pages must be valid JSON-LD conforming to the Schema.org context
(Article 14).

**13.3 — IIIF manifests.** IIIF manifests are JSON-LD (`@context` from IIIF namespace).
The IIIF commerce extension (Article 10) adds a second context entry.

**13.4 — NC context declaration.** NC's JSON-LD `@context` must declare prefix bindings
for all standards used in NC API responses:

```jsonc
{
  "@context": {
    "nc":       "https://opengracelabs.com/ns/nc/v1/",
    "dc":       "http://purl.org/dc/elements/1.1/",
    "dcterms":  "http://purl.org/dc/terms/",
    "schema":   "https://schema.org/",
    "skos":     "http://www.w3.org/2004/02/skos/core#",
    "prov":     "http://www.w3.org/ns/prov#",
    "premis":   "http://www.loc.gov/premis/rdf/v3/",
    "edm":      "http://www.europeana.eu/schemas/edm/",
    "geonames": "http://www.geonames.org/ontology#",
    "wikidata": "http://www.wikidata.org/entity/",
    "dwc":      "http://rs.tdwg.org/dwc/terms/",
    "iiif_p3":  "http://iiif.io/api/presentation/3#"
  }
}
```

**JSON-LD invariant:** JSON-LD output must be valid per the JSON-LD 1.1 specification.
The NC namespace document at the `nc:` prefix URI must be resolvable. API responses that
fail JSON-LD validation are a governance violation.

**Scope:** SS-01 through SS-18 (all subsystems — JSON-LD is the universal output
serialization layer).

### Article 14 — Schema.org

**Ruling: Extend**

Schema.org is the shared vocabulary for web-based structured data. NC adopts Schema.org
as the SEO and rich results layer on all public-facing pages. NC extends it with heritage
commerce properties that have no Schema.org equivalent.

**Schema.org type assignments per NC entity:**

| NC entity | Schema.org type | Governed fields |
|---|---|---|
| Visual asset (image / photo / poster) | `schema:ImageObject` + `schema:VisualArtwork` | name, description, creator, dateCreated, encodingFormat, contentUrl, thumbnailUrl, license, creditText |
| Map asset | `schema:Map` | name, description, creator, dateCreated, mapType, contentUrl |
| Book / eBook asset | `schema:Book` | name, author, datePublished, publisher, inLanguage |
| Audio asset (Phase 2–3) | `schema:AudioObject` | name, duration, encodingFormat |
| Place | `schema:Place` | name, description, geo, containedInPlace, sameAs (GeoNames URI) |
| Place with tourism signal (TAS > 0.5) | `schema:TouristAttraction` | subtype of Place |
| Creator / Illustrator | `schema:Person` | name, birthDate, deathDate, nationality, sameAs (Wikidata URI) |
| Institution | `schema:Organization` | name, url, description, sameAs (Wikidata URI) |
| Collection | `schema:Collection` | name, description, keywords |
| Product listing | `schema:Product` + `schema:Offer` | name, image, offers (price, priceCurrency, availability) |

**Schema.org `nc:` extension properties** (see Part IV Article 25):

| Property | Type | Attached to |
|---|---|---|
| `nc:qualityTier` | `schema:Text` | `schema:CreativeWork` |
| `nc:rightsStatus` | `schema:Text` | `schema:CreativeWork` |
| `nc:sourceInstitution` | `schema:Organization` | `schema:CreativeWork` |
| `nc:anchorType` | `schema:Text` | `schema:CreativeWork` |
| `nc:goldenAge` | `schema:Boolean` | `schema:CreativeWork` |
| `nc:placeRelevanceScore` | `schema:Number` | `schema:CreativeWork` |
| `nc:priorityIllustrator` | `schema:Boolean` | `schema:Person` |

**Schema.org invariant:** NC must not publish `schema:Product` markup for assets without
`activation_target.status = 'activated'` and `media_rights.rights_status = 'verified_pd'`.
Unpublished assets have no Schema.org Product markup.

**Scope:** SS-02, SS-07, SS-10, SS-12, SS-13. Extension in SS-14 (product/offer layer).

### Article 15 — Europeana EDM

**Ruling: Map**

Europeana EDM governs aggregation of cultural heritage records. EDM's tripartite model
(ProvidedCHO, Aggregation, WebResource) is the closest peer-institution mapping for NC's
core entities. The entity alignment was first documented in Media Substrate Constitution
v1.2. This article makes it constitutional.

**EDM entity mapping:**

| EDM class / property | NC equivalent | Rule |
|---|---|---|
| `edm:ProvidedCHO` | `source_item` | The cultural heritage object. One source_item = one ProvidedCHO. |
| `ore:Aggregation` | `source_record` | The aggregation record. NC is the aggregating provider. |
| `edm:WebResource` | `media_file` | The digital file. One WebResource per media_file. |
| `edm:aggregatedCHO` | `source_record.source_item_id` | FK from Aggregation to ProvidedCHO. |
| `edm:isShownAt` | `source_record.source_url` | The institutional page URL. |
| `edm:isShownBy` | `asset_delivery_manifest.manifest_url` | The IIIF manifest URL. |
| `edm:object` | Primary `media_file` IIIF image URL | The representative image. |
| `edm:rights` | `media_rights.rights_statement_uri` | The rights statement URI. |
| `edm:provider` | `sources.name` | The providing institution. |
| `edm:dataProvider` | "Nature & Culture" | NC as data aggregator. |
| `dc:title` | `source_item.title` | Standard DC field. |
| `dc:creator` | `source_item.illustrator` (authority form) | Normalized creator. |
| `dcterms:created` | `source_item.publication_year` | Publication year as `xsd:gYear`. |

**EDM quality threshold:** Records contributing to Europeana must meet EDM Tier 2 at
minimum — mandatory `edm:isShownAt`, `edm:rights`, `dc:title`, `dc:type`. Records below
Tier 2 must be flagged with `quality_flag: edm_tier_1_only` in `media_technical_metadata`
(Media Substrate Constitution v1.2, Article 29.2).

**What NC does not map to EDM:** NC commercial intelligence fields (COS, CSM tier, anchor
type, place relevance) have no EDM equivalents. The EDM output is the institution-facing
discovery layer; the commerce layer is NC-exclusive.

**Scope:** SS-01, SS-02, SS-03, SS-04, SS-07.

### Article 16 — Wikidata

**Ruling: Map**

Wikidata is the Wikimedia Foundation's linked entity database. NC uses Wikidata Q-items
as identity anchors for creators, places, taxa, and institutions.

**Wikidata mapping scope:**

| NC entity | Wikidata use | Rule |
|---|---|---|
| `creator_authority_registry` entry | `wikidata_qid` column | Every authority record carries a Wikidata Q-item where one exists. Resolution via FM `creator_identity_resolution` use case. |
| `places` | `wikidata_qid` column | Every place carries a Wikidata Q-item where one exists. |
| Biological taxa (`anchor_type = 'biological'`) | Taxon Q-item via GBIF | GBIF maps taxa to Wikidata Q-items. Inherited. |
| `sources` (institutions) | Institution Q-item | Every governed institution has a Wikidata Q-item. |
| `media_rights` | Wikidata P6216 (copyright status) | Advisory cross-check only. Never canonical. Rights are NC-governed. |

**16.1 — Read-only rule.** NC reads from Wikidata; NC does not write to Wikidata.
Wikidata's open-edit model is incompatible with NC's provenance doctrine.

**16.2 — QID versioning.** Wikidata QIDs are stored with a resolution date. NC's local
record of the QID at resolution time is the canonical mapping. NC does not continuously
sync against Wikidata. Wikidata entities can be merged, deleted, or altered; NC's
mapping record is the stable reference.

**16.3 — Rights exclusion.** Wikidata is not a rights evidence source. Wikidata copyright
properties (P6216, P275) may be advisory FM context only; they may never set
`media_rights.rights_status` (Invariant FM-4 of Foundation Model Constitution).

**Scope:** SS-02, SS-10, SS-11, SS-12, SS-17.

### Article 17 — GeoNames

**Ruling: Adopt**

GeoNames is the authoritative geographic names database. NC adopts GeoNames as the place
identity authority. Every NC place maps to a GeoNames ID. GeoNames provides: feature
code, feature class, country code, administrative hierarchy, alternate names, and
authoritative lat/lon.

**Adoption scope — GeoNames field mappings:**

| NC place field | GeoNames equivalent | Rule |
|---|---|---|
| `places.geonames_id` | `geonameId` | Required. Every NC place has a GeoNames ID. |
| `places.feature_code` | `fcode` | NC place type follows GeoNames feature codes. |
| `places.feature_class` | `fclass` (A/H/L/P/R/S/T/U/V) | NC place hierarchy uses GeoNames feature classes. |
| `places.country_code` | `countryCode` (ISO 3166-1 alpha-2) | Two-letter country code. |
| `places.admin1_code` | `adminCode1` | Province / state. |
| `places.admin2_code` | `adminCode2` | County / district. |
| `places.alternate_names` | `alternateNames` | Multilingual place names. |
| `places.population` | `population` | Population figure (populated places). |

**Key GeoNames feature codes for NC place types:**

| fcode | Place type | NC use |
|---|---|---|
| `PPLC` | Capital of political entity | Country capital pages |
| `PPL` | Populated place | City / town pages |
| `PRKA` / `PRK` | Park / reserve | National park pages |
| `RFU` | Reef | Marine heritage pages |
| `MT` / `MTS` | Mountain / mountain range | Mountain heritage pages |
| `ISL` / `ISLX` | Island / island group | Island heritage pages |
| `PCLI` | Independent political entity | Country pages |
| `ADM1` | First-order administrative division | State / province pages |
| `RGN` | Region | Regional pages |
| `CONT` | Continent | Continent rollup pages |

**GeoNames identity invariant:** No NC place may exist without a GeoNames ID. A place
without a GeoNames ID is a candidate requiring resolution before it enters the canonical
`places` table. NC does not invent place identifiers.

**GeoNames does not govern:** place relevance score (Article 27, Invent Last), tourism
attraction score (Article 28), or the place-asset connection model. GeoNames provides
identity; NC provides commercial intelligence.

**Scope:** SS-10.

---

## Part III — Subsystem Matrix

### Article 18 — Cross-Reference Matrix

**Posture legend:** A = Adopt | M = Map | E = Extend | — = not applicable to this pairing

| Subsystem | CIDOC CRM | SKOS | DC | PROV-O | PREMIS | IIIF | DwC | GeoJSON | JSON-LD | Schema.org | EDM | Wikidata | GeoNames |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SS-01 Source Record** | M | — | A | M | — | — | — | — | A | — | M | M | — |
| **SS-02 Source Item** | M | M | A | M | — | — | M† | — | A | A | M | M | — |
| **SS-03 Media File** | — | — | A | M | E | E | — | — | A | A | M | — | — |
| **SS-04 Media Rights** | M | A | A | M | E | — | — | — | A | — | — | — | — |
| **SS-05 Media Tech Meta** | — | A | — | — | A | — | — | — | A | — | — | — | — |
| **SS-06 Preservation Event** | M | — | — | M | A | — | — | — | A | — | — | — | — |
| **SS-07 Delivery Manifest** | — | — | A | — | — | E | — | — | A | A | M | — | — |
| **SS-08 Asset Opportunity** | M | M | A | — | — | — | M† | — | A | A | — | M | — |
| **SS-09 Activation Target** | — | — | — | M | E | — | — | — | A | — | — | — | — |
| **SS-10 Place** | M | A | A | — | — | — | — | A | A | E | — | M | A |
| **SS-11 Subject Terms** | — | A | — | — | — | — | M† | — | A | — | M | M | — |
| **SS-12 Creator Authority** | M | A | A | — | — | — | — | — | A | A | — | A | — |
| **SS-13 Collection** | M | A | A | M | — | E | — | — | A | A | — | — | — |
| **SS-14 Commerce Opportunity** | — | E‡ | — | — | — | E | — | — | A | E | — | — | — |
| **SS-15 Workflow / Pipeline** | — | — | — | M | — | — | — | — | A | — | — | — | — |
| **SS-16 Provenance** | M | — | — | A | A | — | — | — | A | — | — | — | — |
| **SS-17 Relationship Intelligence** | M | M | — | M | — | — | — | — | A | — | — | M | — |
| **SS-18 FM Advisory** | — | — | — | E | E | — | — | — | A | — | — | — | — |

†DwC applies only to `anchor_type = 'biological'` records.
‡SKOS Extend in SS-14 = anchor_type scoring annotation extension (Part IV Article 21).

**Summary by posture:**

| Standard | Adopt (SS-#) | Map (SS-#) | Extend (SS-#) | Invent Last |
|---|---|---|---|---|
| CIDOC CRM | — | 01, 02, 04, 06, 08, 10, 12, 13, 16, 17 | — | commerce/scoring layer |
| SKOS | 04, 05, 10, 11, 12, 13 | 02, 08, 11, 17 | 14 | anchor_type scoring annotation |
| Dublin Core | 01, 02, 03, 04, 07, 08, 10, 12, 13 | — | — | commerce layer |
| PROV-O | 16 | 01, 02, 04, 06, 08, 09, 15, 17 | 18 | stochastic activity class |
| PREMIS | 05, 06, 16 | — | 03, 04, 09, 18 | activation lifecycle events |
| IIIF | — | — | 03, 07, 13, 14 | commerce manifest extension |
| Darwin Core | — | 02, 08, 11 | — | NC not a biodiversity system |
| GeoJSON | 10 | — | — | place-commerce `properties` |
| JSON-LD | 01–18 (all) | — | — | NC namespace |
| Schema.org | 02, 07, 10, 12, 13 | — | 03, 14 | heritage commerce properties |
| Europeana EDM | — | 01, 02, 03, 04, 07 | — | NC commercial layer |
| Wikidata | 12 | 01, 02, 08, 10, 11, 17 | — | — |
| GeoNames | 10 | — | — | place relevance / TAS scoring |

---

## Part IV — Extension Registry

NC extensions are versioned governed artifacts. Each has a canonical namespace URI, a
stability guarantee, a backwards-compatibility rule, and a Director Decision that
authorizes its first deployment.

### Article 19 — IIIF Commerce Context Extension v1.0

**Namespace:** `https://opengracelabs.com/ns/nc/iiif/commerce/1.0/context.json`
**Base standard:** IIIF Presentation API 3.0

**Extended properties:**

| Property | JSON-LD key | Type | Rule |
|---|---|---|---|
| Activation target ID | `nc:activation_target_id` | UUID string | Present on all NC-generated manifests. |
| CSM tier | `nc:csm_tier` | string | MASTERWORK / FLAGSHIP / STANDARD / REFERENCE |
| Quality tier label | `nc:quality_tier_label` | string | Human-readable label. |
| Shop URL | `nc:shop_url` | URI | Canonical NC shop page URL for this asset. |
| Product count | `nc:product_count` | integer | Number of active products. |

**Backwards-compatibility rule:** IIIF-compliant consumers must ignore all `nc:` prefixed
properties without error. The base IIIF manifest without NC extensions is a valid IIIF
manifest.

**Amendment trigger:** Any new commerce property added to NC manifests requires a version
bump to this extension and a Director Decision.

### Article 20 — PREMIS Lifecycle Extension v1.0

**Namespace:** `https://opengracelabs.com/ns/nc/premis/lifecycle/1.0/`
**Base standard:** PREMIS 3.0 / LOC Event Type Vocabulary

**NC-specific PREMIS event types:**

| NC event URI | Label | Semantic | PREMIS agents |
|---|---|---|---|
| `nc:pev/activation` | Activation | `activation_target` → `activated` | Human approver |
| `nc:pev/retraction` | Retraction | `activation_target` → `retracted` (Director Decision required) | Director |
| `nc:pev/rights_commercial_clearance` | Rights Commercial Clearance | `media_rights.rights_status` set to `verified_pd` | Human rights verifier |
| `nc:pev/commerce_scoring` | Commerce Scoring | `commerce_opportunities` score computed / recalculated | Scoring worker (SoftwareAgent) |
| `nc:pev/fm_candidate_generated` | FM Candidate Generated | `fm_candidate_record` created from FM inference | FM worker (SoftwareAgent) |
| `nc:pev/fm_candidate_approved` | FM Candidate Approved | FM candidate promoted to canonical record | Human reviewer |

**Extension invariant:** NC extension event type URIs must never shadow or replace LOC
event type URIs. LOC events are adopted without modification.

### Article 21 — SKOS Anchor Type Scheme v1.0

**Namespace:** `https://opengracelabs.com/ns/nc/skos/anchortype/1.0/`
**Base standard:** SKOS W3C 2009

**Concept declarations:**

```turtle
nc:AnchorTypeScheme a skos:ConceptScheme ;
  skos:prefLabel "NC Anchor Type Classification"@en ;
  skos:definition "Classifies illustration opportunities by the real-world entity type 
                   they anchor to for commercial place-routing and scoring purposes."@en .

nc:biological a skos:Concept ;
  skos:inScheme nc:AnchorTypeScheme ;
  skos:prefLabel "Biological"@en ;
  skos:definition "Asset anchors to a biological taxon."@en ;
  skos:closeMatch dwc:Taxon ;
  nc:scoringFormula "composite_biological_v1.2"^^xsd:string .

nc:geographic a skos:Concept ;
  skos:inScheme nc:AnchorTypeScheme ;
  skos:prefLabel "Geographic"@en ;
  skos:definition "Asset anchors to a geographic feature (map, landscape, survey, region)."@en ;
  skos:closeMatch geonames:Feature ;
  nc:scoringFormula "composite_geographic_v1.2"^^xsd:string .

nc:cultural a skos:Concept ;
  skos:inScheme nc:AnchorTypeScheme ;
  skos:prefLabel "Cultural"@en ;
  skos:definition "Asset anchors to a cultural site, monument, or built environment."@en ;
  skos:closeMatch crm:E22_Human-Made_Object ;
  nc:scoringFormula "composite_cultural_v1.2"^^xsd:string .

nc:mixed a skos:Concept ;
  skos:inScheme nc:AnchorTypeScheme ;
  skos:prefLabel "Mixed"@en ;
  skos:definition "Asset anchors to more than one anchor type."@en .
```

**NC scoring annotation** (`nc:scoringFormula`) is NC-specific. SKOS-compliant consumers
ignore it. It links each anchor type concept to its governing CI Constitution formula.

### Article 22 — IIIF Commerce Context Extension (see Article 19)

### Article 23 — PROV-O Stochastic Activity Extension v1.0

**Namespace:** `https://opengracelabs.com/ns/nc/prov/stochastic/1.0/`
**Base standard:** PROV-O W3C 2013

**New class and properties governing FM inference provenance:**

```turtle
nc:StochasticActivity a owl:Class ;
  rdfs:subClassOf prov:Activity ;
  skos:definition "An activity performed by a stochastic agent (Foundation Model).
    Replay covers input reconstruction and decision traceability.
    Exact output reproduction is not guaranteed (FM-3 Weaker Guarantee Doctrine)."@en .

nc:weakerReplayGuarantee a owl:DatatypeProperty ;
  rdfs:domain nc:StochasticActivity ;
  rdfs:range xsd:string ;
  skos:definition "Records the specific nature of the replay limitation for this 
                   FM inference activity."@en .

nc:modelVersion a owl:DatatypeProperty ;
  rdfs:domain nc:StochasticActivity ;
  rdfs:range xsd:string ;
  skos:definition "The exact pinned version of the Foundation Model."@en .
```

### Article 24 — Schema.org Heritage Commerce Extension v1.0

**Namespace:** `https://opengracelabs.com/ns/nc/schema/heritage/1.0/`
**Base standard:** Schema.org

**New properties extending Schema.org types:**

| NC property | Domain | Range | Description |
|---|---|---|---|
| `nc:qualityTier` | `schema:CreativeWork` | `schema:Text` | MASTERWORK / FLAGSHIP / STANDARD / REFERENCE |
| `nc:rightsStatus` | `schema:CreativeWork` | `schema:Text` | `verified_pd` / `cc0` |
| `nc:sourceInstitution` | `schema:CreativeWork` | `schema:Organization` | The source institution |
| `nc:anchorType` | `schema:CreativeWork` | `schema:Text` | biological / geographic / cultural / mixed |
| `nc:goldenAge` | `schema:CreativeWork` | `schema:Boolean` | TRUE if publication year 1750–1900 |
| `nc:placeRelevanceScore` | `schema:CreativeWork` | `schema:Number` | Advisory place relevance 0.0–1.0 |
| `nc:priorityIllustrator` | `schema:Person` | `schema:Boolean` | TRUE if in Priority Illustrator Registry |

**Backwards-compatibility:** Standard Schema.org consumers ignore `nc:` prefixed
properties without error.

---

## Part V — Invention Registry

Inventions are NC-designed models with no adequate precedent in the 13 governed
standards. Each is documented with commercial justification and review schedule.

### Article 25 — Asset Opportunity Object

**NC construct:** `illustration_opportunities` table and its governance model.

**Standards evaluated and rejected:** CIDOC CRM E22 Human-Made Object (governs
description, not commercial opportunity); PREMIS Object (governs preservation, not
scoring); EDM ProvidedCHO (governs aggregation, not commercial routing); Schema.org
CreativeWork (governs discovery metadata, not commercial eligibility).

**Gap:** No external standard defines a commercially scored, place-anchored,
public-domain-verified heritage asset opportunity. The Asset Opportunity is not a
specimen record, not a preservation object, not an aggregation record, and not an OWL
individual. It is a structured commercial opportunity that links a heritage object to
place relevance, carries PD certainty as a gate, carries commercial quality scores, and
routes to products via the CI Constitution.

**Commercial justification:** NC's competitive moat is the Asset Opportunity model —
the ability to score and route PD heritage assets for commercial production. No peer
institution or standard defines this. This is NC's core IP.

**Review schedule:** Annual. Watch for: Schema.org commercial creative work property
extensions, emerging GLAM commercial asset exchange standards.

### Article 26 — Commerce Opportunity Score and CSM Tier

**NC construct:** `commerce_opportunities` scoring model, `csm_score`, `csm_tier`
(MASTERWORK / FLAGSHIP / STANDARD / REFERENCE).

**Standards evaluated and rejected:** Schema.org `schema:offers` (governs price and
availability, not quality/eligibility scoring); CIDOC CRM (no commercial scoring class);
PREMIS (preservation only); Dublin Core (descriptive only).

**Gap:** No heritage or commerce standard defines a multi-axis commercial scoring formula
for print-on-demand product eligibility or a four-tier commercial classification for
heritage assets.

**Review schedule:** Annual. Watch for: Schema.org Product quality rating extensions,
emerging commercial heritage licensing standards.

### Article 27 — Anchor Type Classification

**NC construct:** `illustration_opportunities.anchor_type`
(biological / geographic / cultural / mixed).

**Standards evaluated:** DwC governs biological specimens. GeoNames governs geographic
features. CIDOC CRM governs cultural objects. The SKOS close-match declarations in
Article 21 acknowledge partial alignment; they do not claim equivalence. No standard
provides a unified classification axis across all three in a single commercial platform.

**Gap:** NC needs a single classification axis to select which scoring formula applies
in the CI Constitution. The three peer standards each own one third of the space;
none owns the unified selection mechanism.

**Review schedule:** At every CI Constitution major amendment. New anchor types (e.g.,
`astronomical`) require a constitutional amendment before entering the scoring formula.

### Article 28 — Place-Asset Relevance Score

**NC construct:** `illustration_opportunity_places.relevance_score`.

**Standards evaluated:** GeoNames governs place identity. PostGIS governs spatial
proximity. CIDOC CRM P55 governs place-object association. None governs scored
commercial relevance between a heritage asset and a place for product routing.

**Gap:** The place-asset relevance score is a commerce routing signal, not a geographic
or bibliographic signal. "This asset is commercially relevant to this place at this
confidence level" has no standard expression.

**Review schedule:** Annual.

### Article 29 — Tourism Attraction Score

**NC construct:** `commerce_opportunities.tourism_attraction_score`.

**Standards evaluated:** GeoNames feature codes (provide type, not commercial
attractiveness); Schema.org TouristAttraction (provides type, not scored attractiveness);
UNWTO tourism statistics vocabulary (governs aggregate statistics, not per-place
commercial scores).

**Gap:** No standard defines commercial tourism attractiveness as a scored signal for
heritage asset routing and B2B licensing.

**Review schedule:** Annual. Watch for: UNWTO linked data standards, OpenStreetMap
tourism tagging convergence.

### Article 30 — Creator Prestige Score and Priority Illustrator Registry

**NC construct:** `creator_authority_registry.prestige_tier`, the Priority Illustrator
List (Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel, Wolf).

**Standards evaluated:** ULAN (Getty Union List of Artist Names) — governs authority
records but not commercial prestige scoring. Wikidata — governs entity identity but not
scored commercial prestige.

**Gap:** No standard defines a commercial prestige scoring model for Golden Age
(1750–1900) natural history illustrators. The priority illustrator list is a governed
constitutional fixture; it changes only by constitutional amendment.

**Future mapping:** Getty ULAN adoption as the creator authority base is recommended
in OQ-1. Prestige scoring remains NC invention on top of a ULAN base.

**Review schedule:** Annual. Watch for: new priority illustrator candidates (requires
constitutional amendment), ULAN adoption readiness (OQ-1).

### Article 31 — FM Candidate / Canonical Boundary and Governance Protocol

**NC construct:** `fm_candidate_record`, `fm_inference_record`, five FM Constitutional
Invariants (FM-1 through FM-5), Weaker Guarantee Doctrine (FM-3), Rights Hardening
(FM-4).

**Standards evaluated:** PROV-O — partially governs AI provenance (prov:Activity,
prov:Agent) but does not define a governance model for AI advisory vs. canonical
authority, a candidate-to-canonical promotion protocol, or the Rights Hardening invariant.
The PROV-O stochastic activity extension (Part IV Article 23) maps what PROV-O covers;
the governance boundary itself is NC invention. W3C PROV has no "this output may never
become canonical" class.

**Gap:** The five FM Constitutional Invariants and their operational implementation have
no standard precedent.

**Review schedule:** Annual. Watch for: W3C AI transparency standards, EU AI Act
governance vocabulary, ISO/IEC AI governance standards.

---

## Part VI — Invariants

**S-1 — Standards Authority Invariant.** No external standard overrides PostgreSQL
canonical records for internal NC state. Standards govern the shape and vocabulary of
NC's outputs and mappings, not its internal authority chain.

**S-2 — Lossless Adoption Not Required.** NC mappings (CRM, PROV-O, EDM, Wikidata, DwC)
are not required to be lossless in the direction NC → standard. NC's schema is richer
than any of these standards. The mapping is the intersection. NC-specific information
not in the standard is expressed in the NC namespace; it is not suppressed.

**S-3 — GeoNames Place Identity Lock.** No NC place entity exists without a GeoNames ID.
A place without a GeoNames ID is a candidate, not a canonical place record. NC does not
invent geographic identifiers.

**S-4 — Rights Statement URI Vocabulary Lock.** Rights statement URIs in
`media_rights.rights_statement_uri` must come from `rightsstatements.org` or
`creativecommons.org`. NC does not invent rights statement URIs.

**S-5 — Extension Backwards-Compatibility.** Every NC extension (IIIF commerce, PREMIS
lifecycle, SKOS anchor type, Schema.org heritage, PROV-O stochastic activity) must be
backwards-compatible with its base standard. A consumer implementing only the base
standard processes NC output without error by ignoring `nc:` prefixed properties. A
breaking change to an extension requires a version bump and a constitutional amendment.

**S-6 — JSON-LD as the Exclusive External Serialization.** All NC entity API responses
and all structured data markup on public pages use JSON-LD. XML, Turtle, N-Triples, or
other RDF serializations are not governed by this Constitution and may not be implemented
without a constitutional amendment.

**S-7 — Invent Last Documentation Requirement.** Any NC-invented term, table concept,
relationship type, media profile, or API field must be documented in Part V with:
(a) standards evaluated and rejected; (b) the specific gap; (c) commercial justification;
(d) annual review schedule. Invention without documentation is a governance violation.

---

## Open Questions

| OQ | Question | Recommended resolution |
|---|---|---|
| OQ-1 | Should NC adopt Getty ULAN as the creator authority base? | Yes — recommended for v1.1. ULAN has URIs for all 8 priority illustrators. NC adds `ulan_id` alongside `wikidata_qid` in `creator_authority_registry`. ULAN becomes the authority URI for JSON-LD `schema:Person` output; NC prestige scoring remains an invention on top. Requires Article 30 amendment. |
| OQ-2 | Should NC adopt RDA (Resource Description and Access) for book / serial assets? | Deferred to Phase 2 activation (P2-1 amendment). RDA governs book/serial cataloging. Add to P2-1 constitutional amendment scope. |
| OQ-3 | Should NC map to Schema.org `MusicRecording` / `Audiobook` for Phase 2–3 audio types? | Deferred to Phase 2/3 activation. Add to P2-1 / P3-1 amendment scope. |
| OQ-4 | Should NC adopt the Linked Art profile of CIDOC CRM rather than full CRM? | Recommended: Yes, for institutional API phase. Linked Art is a JSON-LD profile of CRM used by MET, Getty, and Rijksmuseum. It is more practical than full CRM and produces directly useful JSON-LD. Amend this Constitution when institutional API exchange is activated. |
| OQ-5 | Should NC publish a Wikidata reconciliation service? | Not now. When the activated catalog exceeds 10,000 assets, publishing a Wikidata reconciliation endpoint for creator QID resolution would strengthen the ecosystem position. Requires security and data governance review. |
