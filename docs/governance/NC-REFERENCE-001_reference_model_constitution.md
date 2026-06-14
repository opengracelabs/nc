# NC-REFERENCE-001: Reference Model Constitution

| Field | Value |
|---|---|
| Document | NC-REFERENCE-001 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-14 |
| Authority | Strategic Direction v1 · Standards Constitution v1.0 · Wireframe Constitution v1 · Institution Factory v1 · NC-AI-001 · NC-CANON-001 |
| Governing Doctrine | "Adopt the data layer, own the intelligence layer." (Standards Constitution v1.0 axiom) |
| Scope | Prevention of platform drift while scaling to 2,000 places, 10,000 collections, and 1,000,000 assets. Defines what NC learns, adopts, rejects, and improves from 9 reference institutions and 8 reference standards. Codifies five sets of canonical principles and 20 constitutional invariants. |

---

## Preamble

Platform drift is the slow erosion of founding principles under operational pressure. It happens when an institution includes a work that is "almost PD," adds a place page without a GeoNames ID, launches a collection without a place anchor, uses a new technology because it solves an immediate problem, or writes product copy that implies endorsement by a government institution. Each individual decision seems reasonable. The accumulated pattern destroys the moat.

NC-REFERENCE-001 exists to prevent this. It does not describe what NC should aspire to become. It describes what NC must not become, and what specific practices from 9 reference institutions and 8 reference standards NC has examined, tested, and made decisions about. Every principle in this document is grounded in a specific example of a specific institution doing something right, doing something wrong, or doing something that NC must do differently at NC's scale and commercial model.

This constitution governs at scale. The invariants in Part V apply at 7 places and at 2,000 places equally. An invariant that only works at small scale is not a constitutional invariant.

---

## Part I: Reference Institution Analysis

### I.1 — Smithsonian Institution

*The world's largest museum complex. 19 museums, 21 libraries, 9 research centres. 155M+ objects. CC0 commitment (2017–present, ongoing). Primary NC content institution: pending DD-SMITHSONIAN-001.*

| Dimension | Assessment |
|---|---|
| **Best at** | Heritage depth. The Smithsonian holds Audubon's original elephant folios, Moran's Yellowstone paintings, and the largest American natural history collection in existence. No institution combines American expedition legacy and institutional authority at this scale. Their CC0 commitment (2017) was a sector-defining move. |
| **NC adopts** | Expedition provenance narrative. Collection depth standard. CC0 as the institutional default, not an opt-in. The Smithsonian proves that CC0 and institutional trust are compatible — NC does not need to choose between openness and authority. |
| **NC rejects** | Discovery architecture. Smithsonian's digital collections are siloed by museum; there is no cross-collection discovery layer. Collections.si.edu does not connect the Natural History Museum to the American Art Museum. NC's place-centric graph connects what the Smithsonian leaves disconnected. Also: their digitization pace. Masterpieces remain unavailable digitally. |
| **NC improves** | Commerce activation. The Smithsonian holds NC-CANON-001 works #2 and #3 (Carolina Parakeet + Passenger Pigeon) and the Wild Turkey (Pl. I). None are commercially deployed at the quality their significance demands. NC's product pipeline — once DD-SMITHSONIAN-001 is ratified — is the commerce layer the Smithsonian has never built. |

**Constitutional note:** DD-SMITHSONIAN-001 is the highest-priority unblocking action in NC's institution pipeline. Until it is ratified, 14 NC Masterpieces are activation-blocked.

---

### I.2 — Rijksmuseum

*Netherlands national museum. 1M+ objects. Rijksstudio (2013) enabled user download and remixing of all CC0 works. API-first institution since 2013. Gold standard for cultural heritage API design.*

| Dimension | Assessment |
|---|---|
| **Best at** | Open infrastructure. The Rijksmuseum API is the best-designed cultural heritage API in existence: REST, paginated, JSON, image delivery integrated. Rijksstudio proved that enabling commercial use of PD collections increases institutional prestige rather than diminishing it. High-resolution image delivery at ≥6000px confirmed standard. |
| **NC adopts** | API design philosophy. CC0 as prestige-builder, not risk. High-resolution delivery standard (≥6000px for all MASTERWORK-tier products). Collection depth over breadth: the Rijksmuseum would rather have 100 exceptional Dutch masterworks fully documented than 10,000 mediocre works poorly described. |
| **NC rejects** | Geographic and taxonomic scope. The Rijksmuseum is a Dutch national museum. NC is a global platform. The Rijksmuseum is also art-only; NC integrates natural history, scientific illustration, and documentary photography as equal categories. Dutch Golden Age ≠ NC's Canon priority era (1750–1900). |
| **NC improves** | Place-centric discovery. The Rijksmuseum organizes by artist and period. NC organizes by place. Every Rijksmuseum work in NC's collection (Van Huysum from Getty, Rembrandt from Yale/YUAG) connects to its place of origin as the primary discovery axis. Also: commerce. Rijksstudio enables download; NC enables purchase. |

---

### I.3 — Getty

*J. Paul Getty Trust. Open Content Program (2013, ~88,000 CC0 images). Linked Art standard (co-developed). Getty Research Institute holds Vocabulary Project: Art & Architecture Thesaurus (AAT), Thesaurus of Geographic Names (TGN), Union List of Artist Names (ULAN).*

| Dimension | Assessment |
|---|---|
| **Best at** | Linked Art + vocabulary infrastructure. The Getty co-developed Linked Art (JSON-LD subset of CIDOC CRM) as the practical interchange format for museum data. The TGN, AAT, and ULAN are the most complete vocabularies in cultural heritage. The Open Content Program (CC0, explicit commercial permission, no fees, no ToS restriction) is the cleanest rights model in NC's institution pipeline. |
| **NC adopts** | Linked Art (JSON-LD) for API responses where applicable (Yale LUX uses Linked Art; Getty Open Content uses it). Open Content CC0 model as the institutional gold standard: no ToS restriction, commercial use explicitly permitted, no fee. Getty vocabulary references (AAT for subject terms, ULAN for creator identity) as supplementary authority. |
| **NC rejects** | Art history as primary axis. The Getty is organized around art history periods, movements, and media. NC is organized around places and natural history. The Getty's provenance depth (every change of ownership, every auction record) exceeds what NC needs. NC's provenance requirement is 7 links, not 70. |
| **NC improves** | Natural history integration. Getty has zero natural history content. NC connects Getty's Dutch Golden Age botanical works (Van Huysum "Vase of Flowers," Getty Asset Zero 82.PB.70) to the botanical illustration tradition and to Netherlands/Amsterdam place pages. Also: NC deploys Getty CC0 works commercially, which Getty itself does not do. |

---

### I.4 — National Geographic

*Media company. 135-year photographic archive. National Geographic 100 Photographs editorial standard. Conservation narrative authority. Place-first editorial identity.*

| Dimension | Assessment |
|---|---|
| **Best at** | Place narrative. NatGeo proves that place-first editorial identity creates unrivalled brand loyalty. Their photographs are not organized by photographer — they are organized by the places they depict. Their editorial standard for the 100 Photographs benchmark is NC's editorial standard for Canon anchor annotations: every image must be able to answer "what does this image tell you that you cannot learn any other way?" |
| **NC adopts** | Place-first editorial identity. Conservation narrative as commerce driver (not as guilt mechanism). The single-image editorial statement (NC's Canon anchor annotations follow this structure directly). "Stories" as the named editorial mode — NatGeo calls them Stories; NC's L1 navigation includes Stories. |
| **NC rejects** | Photographic archive as core asset. NatGeo's photographs are copyright-restricted and cannot be commercially deployed by NC. NatGeo's commercial identity is subscriber-supported magazine/streaming media. NC's commercial identity is product-based, PD-first, illustration-primary. |
| **NC improves** | 1750–1900 illustration depth. NatGeo was founded in 1888 — it barely covers the golden age of natural history illustration. NC's core commercial assets predate NatGeo by 50–150 years. NC gives those assets NatGeo-quality editorial framing. Also: commerce activation beyond subscriptions. NatGeo sells magazine subscriptions; NC sells physical and digital products from the illustrations that inspired NatGeo's founders. |

---

### I.5 — Google Arts & Culture

*Cultural aggregation platform. 2,000+ partner institutions. High-resolution zoom (Gigapixel). 7M+ artworks. No commerce. Educational focus.*

| Dimension | Assessment |
|---|---|
| **Best at** | Aggregation at scale. No institution has indexed more cultural heritage content or made it more accessible. Cross-institutional discovery (all Haeckel plates, everywhere, at once) is Google A&C's strongest feature. High-resolution delivery proved that institutions would consent to it when the platform is trusted. Educational content at global scale. |
| **NC adopts** | Cross-institutional discovery model. Resolution delivery as an accessibility argument (not a cost). Educational layer as a distinct content mode. The principle that the aggregator can improve discoverability more than individual institutions can. |
| **NC rejects** | No curation. Google A&C aggregates without a quality gate. NC requires a Rights Confidence score ≥8 for any asset to enter the pipeline. Google A&C has no PD-first policy — it aggregates in-copyright works with the same interface as PD works. NC's PD hard gate is the opposite of Google A&C's neutral aggregation stance. Also: no commerce, no editorial voice. |
| **NC improves** | Commerce activation. Google A&C proves the demand exists: people engage with cultural heritage content at scale. NC converts that engagement into commerce. Also: curation. 7M artworks without a quality layer is noise. NC's 1,000 Elite IOs and 100 Canon works are signal. |

---

### I.6 — Europeana

*Pan-European cultural heritage aggregator. 60M+ objects. Developed RightsStatements.org vocabulary (with DPLA). IIIF adoption across European institutions. EDM (Europeana Data Model) as interchange standard.*

| Dimension | Assessment |
|---|---|
| **Best at** | Rights vocabulary. Europeana co-developed RightsStatements.org — the 12 standardized rights statements that NC uses as its primary rights expression vocabulary. The Europeana Data Model (EDM) is the most complete metadata model for aggregated cultural heritage in existence. IIIF adoption across European institutions. |
| **NC adopts** | RightsStatements.org vocabulary (all 12 statements, with NC's Europeana Rights Matrix v1 as the allowed/blocked classification). Europeana as a content source via the Europeana API (Europeana Activation Checklist v1, 8-gate path). EDM minimum field requirements as a metadata baseline. |
| **NC rejects** | Aggregator quality floor. Europeana's 60M objects include scans of marginal quality from institutions with unverified rights claims. NC requires Rights Class assignment and DD ratification before any asset enters production. Also: no place-centric organization. Europeana does not connect objects to places via discovery graph — it uses subject tags. |
| **NC improves** | Curation layer. NC takes Europeana-sourced content and runs it through the Institution Factory pipeline, the rights gate, the IO scoring model, and the place-centric discovery graph. The same Owen Jones Alhambra plate that exists as a raw Europeana record becomes a Canon work connected to 5 Islamic sphere places via NC's discovery graph. |

**Constitutional note:** Europeana Rights Matrix v1 invariants RM-I-1 through RM-I-5 govern all Europeana-sourced content. These are separate from but consistent with NC-REFERENCE-001 invariants.

---

### I.7 — GBIF

*Global Biodiversity Information Facility. Occurrence database. Darwin Core authority. 2.6B+ occurrence records. Taxon backbone.*

| Dimension | Assessment |
|---|---|
| **Best at** | Biological identity infrastructure. GBIF's taxon backbone (derived from multiple authoritative checklists) is the most complete biological name authority in existence. The gbif_taxon_key is the permanent stable identifier for any species encountered in NC's content pipeline. Occurrence data validates that a species occurs at a given place. |
| **NC adopts** | Darwin Core as the biological metadata standard (per Standards Constitution v1.0). gbif_taxon_key as NC's biological anchor — the permanent key linking any NC Taxon node to the global biological identity system. Occurrence counts (capped at 100 per CI Constitution) as place-relevance validation signals. GBIF source role: "validation_only," immutable. |
| **NC rejects** | Occurrence database as NC's content model. GBIF indexes where species have been observed — NC curates where species have been illustrated. These are different questions with different answers. A species may have 50,000 GBIF occurrence records and zero NC Illustration Opportunities; a species may have zero GBIF records and a Haeckel masterplate. Also: GBIF media ingestion is permanently prohibited (SA-GBIF-001). |
| **NC improves** | Illustration-place linkage. GBIF shows that a species occurs at a place. NC shows how that species was illustrated at that place, by whom, in what publication, with what provenance. NC's commercial proposition is that illustration is more valuable than occurrence record — it is the difference between a data point and an art object. |

---

### I.8 — BHL (Biodiversity Heritage Library)

*Pre-1928 natural history digitization consortium. 60M+ pages. 560+ institutional members. Open access. Primary NC content discovery source.*

| Dimension | Assessment |
|---|---|
| **Best at** | Scale of pre-1928 PD natural history content. BHL has digitized more natural history illustration than any other institution. The BHL rights classification (Tier 1 = CC0 member institution, confirmed pre-1928 PD) is NC's Wave 1 activation standard. BHL is where NC's content pipeline begins for all non-institutional-CC0 works. |
| **NC adopts** | BHL as primary content discovery source (per Illustration Opportunity Doctrine: "BHL is where the commercial pipeline begins"). BHL Tier 1 classification = RC 9 (PD confirmed) in NC's rights scoring system. BHL API for bibliographic metadata and page image access. Pre-1928 PD standard as NC's rights safe harbor for text-based content. |
| **NC rejects** | Raw digitization as NC's content delivery method. BHL provides page scans; NC requires curated plate extraction, quality scoring, and illustration-level metadata. A BHL scan of a 300-page Audubon folio is raw material; NC's NC-BHL-NH-00001 (Carolina Parakeet, Pl. XXVI) is a precisely identified, scored, placed, and commercially activated Illustration Opportunity. |
| **NC improves** | Plate-level curation and commerce. BHL makes the entire Kunstformen der Natur available as a set of scanned pages. NC extracts the 100 plates, scores each one on the 6-criterion framework, places each one geographically, assigns each one to a Canon series, and deploys the highest-scoring plates as commercial products. BHL produces access; NC produces commerce. |

---

### I.9 — UNESCO

*United Nations cultural and scientific agency. World Heritage List (1,199 sites). Intangible Cultural Heritage (ICH) list. Convention Concerning the Protection of World Cultural and Natural Heritage (1972).*

| Dimension | Assessment |
|---|---|
| **Best at** | Designation authority. UNESCO's Outstanding Universal Value (OUV) determination is the highest international designation for both natural and cultural heritage. The World Heritage List is the most authoritative place significance signal in existence. The ICH Convention (2003) created the first international framework for intangible heritage — the practices, expressions, and knowledge that define cultures. |
| **NC adopts** | WH site list as NC's primary place significance signal (per NC-PLACES-1000 and Place Factory Blueprint). ICH framework as NC's intangible heritage layer (per NC-ICH-001, invariants ICH-1 through ICH-6). Designation taxonomy: WH + Ramsar + Geopark + UNESCO Biosphere Reserve as NC's top-tier place selection drivers. |
| **NC rejects** | UNESCO's pace and documentation model. UNESCO sites take decades to designate and are documented in text-heavy nomination dossiers. NC moves at a different pace: a place enters NC's Tier 1 pipeline within a sprint once the NC-DATA-* authority resolution is complete. Also: UNESCO does not curate illustrations or activate commerce. |
| **NC improves** | Visual discovery layer for heritage sites. UNESCO designates Angkor; NC connects Mouhot's 1864 lithograph to Angkor's place page, the Khmer discovery chain, and an archival print product. UNESCO designates Galápagos; NC has Darwin's Finches (NC-PROD-005) active on the Galápagos place page. NC is the commerce layer UNESCO has never built. |

---

## Part II: Reference Standard Analysis

### II.1 — CIDOC CRM (ISO 21127)

*Conceptual Reference Model for cultural heritage documentation. 86 entity classes, 137 properties. Event-centric provenance model.*

| Dimension | Assessment |
|---|---|
| **Ruling** | MAP — Standards Constitution v1.0, Article 12. NC maps to CRM concepts without implementing the full ontology. |
| **NC adopts** | Event-centric provenance model: every NC asset has a production event (E12 Production), a publication event (E87 Curation Activity), and a rights event. The CRM's E5 Event chain maps to NC's 7-link provenance chain (publication → plate → scan → rights → institution → NC → product). |
| **NC rejects** | Full CRM implementation. 86 classes and 137 properties are unworkable for NC's operational database. The CRM is a documentation ontology, not a commerce database schema. NC uses the CRM as a conceptual reference, not as a schema. |
| **NC improves** | Commerce event types. The CRM has no commerce events. NC extends the provenance chain with NC-PRODUCT event types: the moment an IO becomes a product, the rights clearance that authorizes it, and the CE registration that limits its edition size. |

---

### II.2 — Darwin Core (TDWG)

*Biodiversity data standard. Taxon, Occurrence, Event, Location terms. Basis for GBIF, iNaturalist, all major occurrence databases.*

| Dimension | Assessment |
|---|---|
| **Ruling** | MAP — Standards Constitution v1.0, Article 13. Darwin Core fields map to NC's taxon and occurrence data model. Darwin Core is not NC's primary data model. |
| **NC adopts** | scientificName, taxonKey (as gbif_taxon_key), decimalLatitude/Longitude, eventDate, institutionCode, license, rightsHolder — all mapped to NC fields. Darwin Core as the biological interoperability layer enabling GBIF cross-reference. |
| **NC rejects** | Occurrence-record primacy. Darwin Core was designed for occurrence data ("species X was observed at location Y on date Z"). NC's primary entity is the Illustration Opportunity, not the occurrence. An NC IO does not require an occurrence record; it requires a place connection, a publication source, and a rights clearance. |
| **NC improves** | Illustration-primary extension. NC adds plate_number, publication_title, illustrator, golden_age_flag, and illustration_opportunity_id to the Darwin Core-inspired metadata model. These fields do not exist in Darwin Core — they are NC's intelligence layer over the Darwin Core data layer. |

---

### II.3 — IIIF (International Image Interoperability Framework)

*Image API + Presentation API v3 + Search API + Authentication API. Standard for delivery of digital images at any resolution, with structured manifests.*

| Dimension | Assessment |
|---|---|
| **Ruling** | EXTEND — Standards Constitution v1.0, Article 14. NC implements IIIF Image API Level 2 minimum, with NC Commerce Context extension. |
| **NC adopts** | Image API Level 2: image requests with region, size, rotation, quality, format parameters. Presentation API v3 manifests for structured work description. Deep zoom via IIIF-compatible viewers. IIIF as the interoperability layer enabling content from NHM, Met, Yale, Getty, Walters to be served through a single delivery interface. |
| **NC rejects** | IIIF as canonical metadata store. The IIIF manifest describes an image; NC's PostgreSQL graph describes an Illustration Opportunity. These are different entities. The manifest is a delivery artefact, not a provenance record. NC's 7-link provenance chain cannot be derived from a IIIF manifest; it must be authored in the NC database and published to the manifest. |
| **NC improves** | NC Commerce Context extension: adds `nc:rights_clearance_level`, `nc:product_eligible`, `nc:ce_allocation_remaining`, and `nc:canonical_place_id` to IIIF manifests served by NC. This extension allows downstream consumers to know not just what the image is, but whether it can be commercially deployed. |

**Scale note:** At 1,000,000 assets, IIIF tile generation and manifest caching become infrastructure requirements. NC's image delivery stack must plan for IIIF at scale before the 50,000-asset threshold.

---

### II.4 — Schema.org

*Structured data vocabulary for web content. Supported by Google, Microsoft, Yandex. Governs rich results in search engines.*

| Dimension | Assessment |
|---|---|
| **Ruling** | EXTEND — Standards Constitution v1.0, Article 15. NC implements Schema.org with NC Heritage Properties extension (5 custom properties). |
| **NC adopts** | VisualArtwork for illustration pages. Place for place pages. ImageObject for asset metadata. Product + Offer for commerce. BreadcrumbList for navigation. FAQPage for educational content. Event for expedition provenance. Person for illustrators. Organization for institutions. |
| **NC rejects** | Schema.org as canonical internal data model. Schema.org is an SEO and interoperability vocabulary, not a database schema. NC uses Schema.org exclusively for structured markup on public web pages; all canonical data lives in the NC PostgreSQL schema. |
| **NC improves** | NC Heritage Properties: `nc:IllustrationOpportunity`, `nc:ExtinctionStatus`, `nc:GoldenAgeIndicator`, `nc:RightsConfidenceLevel`, `nc:ExpeditionProvenance`. These properties do not exist in Schema.org. They are NC's intelligence layer — the signals that distinguish an NC product description from a generic VisualArtwork record. |

---

### II.5 — RightsStatements.org

*12 standardized rights statements for cultural heritage. Developed by Europeana + DPLA. Includes PDM (Public Domain Mark), NoC-US, InC (In Copyright) variants, and ambiguous statements (UND, CNE).*

| Dimension | Assessment |
|---|---|
| **Ruling** | ADOPT — the primary NC rights expression vocabulary. Europeana Rights Matrix v1 (invariants RM-I-1 through RM-I-5) governs the allowed/blocked classification for Europeana-sourced content. |
| **NC adopts** | All 12 RightsStatements.org URIs as the canonical vocabulary for rights expression in NC asset records. The PDM and NoC-US statements as the highest-confidence PD signals. NC rights scoring (RC 1–10) maps to RightsStatements.org categories: PDM + NoC-US = RC 9–10; InC variants = RC 0 (hard blocked). |
| **NC rejects** | All InC (In Copyright) variants — permanently and unconditionally. All NoC-NC (No Copyright – Non-Commercial Use Only) variants. All CC BY-NC variants. CNE (Copyright Not Evaluated) and UND (Undetermined) without DD resolution. The NC PD hard gate is more restrictive than RightsStatements.org allows — NC treats UND as blocked pending resolution, not as a permissive ambiguity. |
| **NC improves** | Activation State layer. RightsStatements.org tells NC whether a work is in the public domain. It does not tell NC whether a work is commercially activatable by NC — that requires a ratified DD, a confirmed image resolution, and a Gate E record. NC's Activation State (Wave 1 / Wave 2 / Wave 3 / ACTIVE) is a layer above RightsStatements.org that RightsStatements.org cannot provide. |

---

### II.6 — GeoNames

*Geographical database. 11M+ features. Canonical place IDs, coordinates, feature codes, alternate names. CC BY 4.0.*

| Dimension | Assessment |
|---|---|
| **Ruling** | ADOPT — place identity lock. Standards Constitution v1.0, Invariant S-3: GeoNames ID is the canonical place key. Governing standard DD-GEONAMES-001. |
| **NC adopts** | GeoNames ID as NC's primary place key (invariant, non-negotiable). Feature codes (PRKA, PRK, RF, etc.) as NC place type classification. Coordinates as authoritative lat/lon for place bounding boxes. Alternate names for multilingual place page titles. CC BY 4.0 attribution as required by DD-GEONAMES-001. |
| **NC rejects** | GeoNames as the only place authority. Wikidata provides QIDs that cross-reference GeoNames IDs (property P1566) and is used as secondary identity confirmation in NC-DATA-* documents. OSM provides polygon geometry for visual display but is permanently banned from canonical tables (ODbL share-alike incompatibility). |
| **NC improves** | NC-DATA-* authority resolution layer. When GeoNames has conflicting records for the same place (Yellowstone: 5843591 vs. 5843642 vs. 5844046), NC issues an NC-DATA-* authority resolution document with evidence package, canonical ID ruling, and retired ID register. GeoNames does not resolve these conflicts; NC does. |

---

### II.7 — Wikidata

*Free collaborative knowledge base. CC0. Q-numbers (entities), P-numbers (properties), structured statements with references.*

| Dimension | Assessment |
|---|---|
| **Ruling** | MAP — Standards Constitution v1.0, Article 17. Read-only identity confirmation. DD-WIKIDATA-001 (8 invariants W-1 through W-8). |
| **NC adopts** | Wikidata QID as secondary place identifier. P1566 (GeoNames ID property) for cross-reference validation in NC-DATA-* authority resolution. Creator QIDs for 8 Priority Illustrators and all registered NC illustrators. Institution QIDs for all content institutions. Taxon QIDs as cross-reference to GBIF backbone. |
| **NC rejects** | Wikidata as place identity authority (GeoNames is primary; Wikidata confirmed as secondary per DD-WIKIDATA-001). Wikidata Commons content pipeline (permanently prohibited, invariant W-6: Commons Boundary Doctrine). Wikidata coordinates as NC canonical coordinates (GeoNames is primary). |
| **NC improves** | Identity verification layer. NC uses Wikidata's P1566 property to confirm that a GeoNames ID matches the expected entity before writing it to the canonical place table. A Wikidata QID without a matching P1566 = GeoNames ID is a flag for NC-DATA-* authority resolution. Wikidata makes NC's identity resolution auditable. |

---

### II.8 — OpenStreetMap / Overture Maps

*OSM: Collaborative geographic database. ODbL share-alike licence. Polygon geometry, routing, place boundaries. Overture Maps: Linux Foundation. CC BY 4.0. Building/place/road data derived from OSM + proprietary sources.*

| Dimension | Assessment |
|---|---|
| **Ruling** | OSM: INFRASTRUCTURE REFERENCE ONLY (produced-works tile path authorized). Raw OSM data permanently banned from canonical tables. DD-OSM-001 invariants OS-1 through OS-5. Overture Maps: OQ-3 highest-priority geographic data follow-on. |
| **NC adopts** | OSM produced-works tiles for visual display on place pages (tile endpoint, not raw data). Overture Maps CC BY 4.0 polygon geometry when available — does not trigger ODbL share-alike. |
| **NC rejects** | OSM raw data (nodes, ways, relations) in any NC canonical table. ODbL is a share-alike licence incompatible with NC's commercial doctrine. Any import of OSM raw data into NC's PostgreSQL database violates OS-1. Parcel boundaries, road data, and administrative boundaries from OSM are permanently banned as canonical NC data sources. |
| **NC improves** | Overture Maps as the geographic data path that resolves NC's polygon geometry gap without ODbL exposure. Overture Maps is OQ-3: the highest-priority open action for NC's geographic infrastructure after GeoNames and Wikidata are fully implemented. |

---

## Part III: Five Canonical Principle Sets

### III.1 — Architecture Principles (ARCH)

**ARCH-1 — Place primacy.** Every entity in NC's data model connects to a named place via a verifiable path. A place connection is not optional metadata — it is a constitutional requirement. An Illustration Opportunity without a place connection is not an NC IO; it is an unclassified image object.

**ARCH-2 — PostgreSQL canonical.** The NC data store is PostgreSQL. All canonical data — place identity, asset rights, IO scores, product records, edition limits, provenance chains — lives in PostgreSQL. Alternative data stores (Neo4j, pgvector, Elasticsearch, Redis, proprietary vector stores) may serve as projection layers but may not hold canonical state. The projection layer is dispensable; the canonical layer is not. *(Basis: Strategic Direction v1 frozen stack; Wireframe Constitution v1 stack ruling.)*

**ARCH-3 — IIIF delivery.** Image delivery uses IIIF Image API Level 2 as the minimum standard. Family A products (Museum Giclée) require source images ≥6,000 pixels on the longest side. No product is activated without confirmation of source image resolution. *(Basis: Standards Constitution v1.0, IIIF extension.)*

**ARCH-4 — Linked Art for interchange.** Where NC exposes structured data about collection objects to external consumers, the response format is JSON-LD following the Linked Art profile. Internal APIs may use application-specific formats; external-facing APIs representing collection objects use Linked Art. *(Basis: Standards Constitution v1.0, Getty Linked Art alignment.)*

**ARCH-5 — GeoNames identity lock.** The primary place key in NC's database is the GeoNames ID. No place page goes live without a confirmed GeoNames ID documented in an NC-DATA-* authority resolution record. Wikidata QID is the secondary identifier. OSM data is visual-display only. *(Basis: Standards Constitution v1.0 Invariant S-3; DD-GEONAMES-001.)*

**ARCH-6 — pg_trgm for search.** Text search uses PostgreSQL pg_trgm trigram indexing with weighted ranking. Semantic/vector search using pgvector or external embedding APIs is not implemented in the canonical database. If semantic similarity is required, it is computed as score-vector proximity in JSONB, within PostgreSQL, without an external vector store. *(Basis: Wireframe Constitution v1 stack ruling; NC-AI-001 stack conflict resolution.)*

**ARCH-7 — Rights gate at ingestion.** Every asset is rights-cleared before it enters the NC asset table. The rights gate is not applied at display time — it is enforced at the pipeline ingestion boundary. An asset with RC < 8 does not enter the assets table; it enters the candidate table with a blocked_reason field. This is the mechanism that prevents PD gate erosion at scale.

**ARCH-8 — Five-stage pipeline immutable.** NC's content pipeline is: Place → Discovery → Asset → Collection → Product. No asset bypasses any stage. No product is created from an asset that has not passed through all prior stages with documented records. *(Basis: Strategic Direction v1 frozen elements.)*

---

### III.2 — Collection Principles (COL)

**COL-1 — The Illustration Opportunity is NC's primary commercial entity.** Taxon is metadata on the IO. Place is the discovery axis. The illustrator is the provenance axis. The IO is the commercial object. An IO is not a species — it is a specific illustration of a specific subject in a specific publication at a specific date. *(Basis: Illustration Opportunity Doctrine.)*

**COL-2 — Golden age 1750–1900 priority.** Publications from this period receive a prestige bonus in IO scoring. Pre-1750 works require a documented exception (filed in the IO record's `exception_reason` field). Post-1900 works require a higher rights confidence score to compensate for reduced age-based PD certainty. *(Basis: Illustration Opportunity Doctrine.)*

**COL-3 — Eight Priority Illustrators.** Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel, Wolf receive a permanent prestige bonus in NC's IO scoring model. This list is permanent; names may be added by constitutional amendment but may not be removed. The prestige bonus is documented in the NC-IO-001 scoring formula. *(Basis: Illustration Opportunity Doctrine, NC-IO-001.)*

**COL-4 — PD/CC0 hard gate.** No In Copyright work, No Copyright — Non-Commercial Use Only work, and no Undetermined rights work without DD resolution enters the NC assets table. The gate has no exceptions, no staged rollbacks, and no conditional periods. A work is either PD/CC0-confirmed or it is blocked. *(Basis: Strategic Direction v1 frozen elements; Europeana Rights Matrix v1 Invariant RM-I-1.)*

**COL-5 — Complete IO record requirement.** Every IO entering the NC assets table must have: (a) a GeoNames-confirmed place connection; (b) a BHL, NHM, NARA, or equivalent confirmed source with rights class assignment; (c) an IO score ≥45/60 for the Top 1,000 portfolio; (d) a series classification (NHM / EXP / BOT / EX / CUL / SCI / GEO); (e) a wave assignment. Incomplete IO records do not advance to the Collection stage.

**COL-6 — Depth over breadth.** Ten exceptional IOs per place at full documentation depth beats 100 mediocre IOs with shallow records. NC's place pages are editorial statements, not catalogs. The place page for Galápagos with Darwin's Finches, the 1835 Haeckel radiolaria analogue, and a Cook voyage botanical is more commercially powerful than 100 species occurrence records. Quality is the NC moat; quantity is available everywhere else.

**COL-7 — Canon and Masterpiece designations are permanent.** A Canon designation (NC-CANON-001) cannot be removed. A Masterpiece designation (NC-MASTERPIECES-001) cannot be removed. Rights defects do not remove the designation — they block commercial activation while preserving the editorial standing. Designations may be added annually; they may never be removed.

**COL-8 — Extinction Archive priority.** Works documenting species now confirmed or presumed extinct receive top editorial and commercial priority within their category. The Extinction Archive is NC's most important editorial series. Every Extinction Archive product carries a conservation narrative. The archive is maintained in NC-MASTERPIECES-001 and NC-CANON-001; it is reviewed annually.

---

### III.3 — Discovery Principles (DISC)

**DISC-1 — Seven discovery journeys, permanent.** NC's canonical discovery journeys are: Expedition Trail, Illustrator's World, Cultural Sphere, ICH Thread, Designation Network, Taxon Trail, Ecological Corridor. These seven are permanent. No new journey type may be declared without a constitutional amendment to this document and to the NC-GRAPH-002 discovery architecture blueprint.

**DISC-2 — No orphan entities.** Every IO has ≥1 place connection. Every place has ≥1 IO. Every collection has a place anchor. Every discovery journey contains ≥3 connected nodes before launch. Orphan pages — pages with no discovery graph edges — are constitutionally prohibited. This rule applies at 7 places and at 2,000 places equally.

**DISC-3 — Taxon is a discovery handle, not a subject.** The Taxon Trail discovery journey uses taxa to connect IOs across places. Taxa are not displayed as primary subjects on IO pages — places and illustrators are. A search for "Quetzal" returns IOs organized by place of illustration, not by taxonomic classification. Taxon drives discovery; place drives commerce.

**DISC-4 — Discovery graph in PostgreSQL CTE.** NC's discovery graph — 13 node types, 32 relationship types — is implemented as PostgreSQL recursive Common Table Expressions. It does not require Neo4j. Neo4j may serve as a projection layer (per Relationship & Semantic Intelligence Constitution v1.0) but is permanently prohibited from holding canonical discovery state. *(Basis: Wireframe Constitution v1 stack ruling; NC-AI-001 stack resolution.)*

**DISC-5 — Place network connectivity.** Every place must maintain ≥2 discovery graph edges to adjacent places before launch. This prevents isolated place pages. The Yellowstone → Grand Canyon → Olympic → Great Smoky chain is an example of the minimum connectivity standard. At 2,000 places, this standard generates ≥4,000 discovery edges — the density that makes the discovery graph a genuine navigation tool rather than a link list.

**DISC-6 — Designation drives priority.** Among places in NC's pipeline, the designation stack determines editorial priority. Designation score = count of active designations (WH + Ramsar + Geopark + Biosphere Reserve + Dark Sky + ICH). A place with designation score ≥3 receives editorial priority over an equally-scored place with designation score 0. *(Basis: NC-PLACES-1000 GPN-8; NC-ICH-001 ICH Stack Rule.)*

**DISC-7 — ICH as first-class discovery layer.** Intangible Cultural Heritage practices are full discovery nodes in the NC graph, connected to places, illustrators, taxon collections, and product lines. The ICH Thread discovery journey (Kyoto → Samarkand → Isfahan → Fez) is a permanently supported journey type. ICH product lines (Traditional Craft products) require SA-ICH-PLACE-001 ratification before activation. *(Basis: NC-ICH-001 invariants ICH-1 through ICH-6.)*

**DISC-8 — Creator Page is a canonical entity.** The illustrator/creator page (`/discover/creator/{slug}`) is a first-class NC page, designated as a 6th canonical page in Wireframe Constitution v1.1 (OQ-1). Every Priority Illustrator has a Creator Page before the corresponding Canon series is commercially deployed. A Canon series without a Creator Page is editorially incomplete.

---

### III.4 — Trust Principles (TRUST)

**TRUST-1 — Institution Factory mandatory.** Every content institution follows the 9-stage Institution Factory path (Discovery → Governance → Connectivity → Rights → Adapter → M36 → Asset Zero → Pilot → Operational). No institution enters production via a shortcut. IFC v1 invariants IFC-1 through IFC-12 apply unconditionally. IFC-3 (FM-4: rights analysis never automated) and IFC-1 (PD hard gate) are permanently non-waivable. *(Basis: Institution Factory Constitution v1.)*

**TRUST-2 — DD ratification before production.** No asset from a content institution enters the NC production database until that institution's Decision Document is ratified. DD drafting is not sufficient — ratification is required. This rule has no exceptions for "obviously safe" institutions. The institution that seems most obviously safe is the institution most likely to have an unexamined ToS restriction. *(See: Gallica DD-GALLICA-003 disqualification.)*

**TRUST-3 — Seven-link provenance chain for Masterpieces.** Every MASTERWORK-tier product eventually has a published 7-link NC-PDPS provenance chain: publication → plate → scan → rights → institution → NC → product. The chain is published on the product page before CE activation. Products without a complete provenance chain may not be offered at MASTERWORK tier price points.

**TRUST-4 — NC-DATA-* for every disputed identity.** When two or more identifiers claim to represent the same place (as occurred with Yellowstone GeoNames IDs 5843591, 5843642, and 5844046), NC issues an NC-DATA-* authority resolution document with an evidence package, a canonical ruling, and a retired ID register. No disputed place identity is resolved by convention or assumption — it is resolved by documented evidence.

**TRUST-5 — Graph = truth, models = advisory.** AI models may generate, summarize, interpret, and personalize. They may not determine rights, establish provenance, or write canonical place IDs into NC's database. FM-4 (Foundation Model Constitution v1.0) is permanent and non-waivable: no model output constitutes a rights determination. Attribution strings are retrieved from verified sources, never generated. *(Basis: NC-AI-001; Foundation Model Constitution v1.0 Invariant FM-4.)*

**TRUST-6 — Federal nonendorsement zero-tolerance.** No NC product, page, or marketing copy may imply endorsement by any US federal agency (NASA, NARA, NOAA, USGS, NPS, US Fish & Wildlife Service, or any agency whose works are used under 17 U.S.C. § 105). The FS-001 correction (Earthrise page, 2026-06-11) established the precedent: attribution identifies the source; it does not claim endorsement. This rule applies permanently to all US Government works in NC's commercial pipeline.

**TRUST-7 — Human gate for MASTERWORK tier.** Every MASTERWORK-tier product requires Curator review before Gate E authorization. No MASTERWORK product is automated from asset to product without human sign-off on the provenance chain, the product copy, and the attribution record. This gate does not scale away at 1,000,000 assets — MASTERWORK is a small, permanent, human-reviewed category.

**TRUST-8 — Rights display mandatory.** Rights status (PD/CC0 badge) is displayed on every asset appearance throughout the NC platform — collection pages, place pages, product pages, editorial stories — without exception. The rights badge is never hidden for aesthetic reasons. *(Basis: Wireframe Constitution v1, Article 16.)*

---

### III.5 — Commerce Principles (COM)

**COM-1 — Gate E required for all activations.** No product may be publicly listed or sold without a completed Gate E record: rights confirmed, attribution verified, federal nonendorsement checked, curator sign-off (for MASTERWORK tier), and activation logged with timestamp and approver identity. Gate E has no expedited path. *(Basis: NC-COMMERCE-002; NC-FIRST-SALE authorization.)*

**COM-2 — Product family classification governs rights floor.** Family A (Museum Giclée) requires institution-wide CC0 with DD ratified and image ≥6,000px confirmed. Family B (Art Print) requires PD/CC0 with RC ≥9. Family C through E have graduated requirements per NC-PRODUCT-001. Family classification is not negotiable: an asset below the Family A rights floor cannot be listed as a Museum Giclée under any commercial argument.

**COM-3 — Masterpiece tier = CE eligible.** Every work registered in NC-MASTERPIECES-001 is eligible for Collector Edition (CE) allocation, subject to CE Allocation Register limits (3 per MASTERWORK / 5 per FLAGSHIP / 3 per STANDARD / 20 per REFERENCE per place per year). CE eligibility is earned by Masterpiece registration; it is not granted by commercial demand.

**COM-4 — Place commerce chain.** Every NC product is deployed via a place page. A product without a place page connection is not a valid NC product deployment. The product page is not the commerce endpoint — the place page, through contextual commerce integration, is where products are discovered and purchased. *(Basis: Wireframe Constitution v1, Commerce hierarchy.)*

**COM-5 — NC is not a subscription platform.** NC's commerce model is product-based: physical and digital products sold individually, in portfolios, and via institutional licensing. Advertising, subscription, and page-view-monetization models are permanently excluded. *(Basis: Strategic Direction v1: "What must NOT be built.")*

**COM-6 — Price integrity for MASTERWORK tier.** MASTERWORK products are not discounted except within CE bundle pricing. Price integrity is a trust signal: a MASTERWORK product that appears at 20% off signals that it was overpriced, not that it is a good deal. NC's MASTERWORK tier derives its value from scarcity and provenance depth, both of which require price integrity.

**COM-7 — B2B licensing is Era 2.** NC's commercial programme is: Era 1 (B2C product sales) → Era 2 (B2B licensed catalog API) → Era 3 (collection-level commerce, private-label brand). B2B institutional licensing does not begin until NC has demonstrated product market fit in Era 1. No B2B infrastructure is built before Era 1 revenue authorization is confirmed. *(Basis: Strategic Direction v1, Commerce Intelligence domain.)*

**COM-8 — Educational tier is a licensing category.** Educational products (Family E, REFERENCE tier CSP 40–59) are sold via B2B educational licence, not as retail products. Educational licensing does not begin until Era 2. Until then, educational value is realized through place page editorial content, not through separate educational product lines.

---

## Part IV: Constitutional Invariants

The following invariants are permanent. They may be amended only by the full constitutional amendment procedure (Part V). No Director Decision, sprint decision, or operational convenience may override them.

| # | Invariant | One-line statement | Governing document |
|---|---|---|---|
| **RM-1** | Place primacy | Every NC commercial asset connects to a named place with a confirmed GeoNames ID | ARCH-1; S-3 |
| **RM-2** | IO primacy | The Illustration Opportunity is NC's primary commercial entity; taxon is metadata | COL-1; IO Doctrine |
| **RM-3** | PD hard gate | No InC, NoC-NC, or UND-unresolved asset enters the NC assets table — ever | COL-4; RM-I-1 |
| **RM-4** | DD before production | No institution asset reaches production without a ratified Decision Document | TRUST-2; IFC v1 |
| **RM-5** | Golden age priority | 1750–1900 receives prestige bonus; pre-1750 requires documented exception | COL-2; IO Doctrine |
| **RM-6** | GeoNames identity lock | GeoNames ID is the canonical place key; disputed IDs require NC-DATA-* resolution | ARCH-5; S-3 |
| **RM-7** | PostgreSQL canonical | All canonical NC data lives in PostgreSQL; projection layers do not hold canonical state | ARCH-2; SD-v1 |
| **RM-8** | IIIF minimum | IIIF Image API Level 2 minimum for all institutional images; ≥6,000px for Family A | ARCH-3; Standards v1.0 |
| **RM-9** | RightsStatements.org | RightsStatements.org vocabulary governs all NC rights expression; NC extends but does not replace | II.5; Europeana Matrix |
| **RM-10** | Seven discovery journeys | The 7 NC discovery journeys are permanent; no new journey without constitutional amendment | DISC-1; NC-GRAPH-002 |
| **RM-11** | No orphan entities | Every IO has ≥1 place connection; every place has ≥1 IO; no orphan pages | DISC-2 |
| **RM-12** | Canon permanent | Canon designation (NC-CANON-001) cannot be removed; Masterpiece designation cannot be removed | COL-7; NC-CANON-001 |
| **RM-13** | Gate E required | No product goes live without a completed Gate E record | COM-1; NC-COMMERCE-002 |
| **RM-14** | Federal nonendorsement | Zero tolerance for implied government endorsement in any NC product or marketing copy | TRUST-6; FS-001 |
| **RM-15** | Eight Priority Illustrators | Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel, Wolf have permanent prestige bonus; list may be extended but not reduced | COL-3; IO Doctrine |
| **RM-16** | FM-4 permanent | No model output constitutes a rights determination; this invariant cannot be lifted by any means | TRUST-5; FMC FM-4 |
| **RM-17** | OSM raw data banned | OSM raw data is permanently banned from all NC canonical tables; ODbL incompatibility | II.8; DD-OSM-001 |
| **RM-18** | Graph = truth | AI models are advisory; canonical data is authored by humans in the NC database | TRUST-5; NC-AI-001 |
| **RM-19** | Institution Factory mandatory | All content institutions follow the 9-stage Institution Factory path with 12 IFC invariants | TRUST-1; IFC v1 |
| **RM-20** | Rights display mandatory | Rights badge (PD/CC0) is displayed on every asset appearance without exception | TRUST-8; Wireframe v1 Art. 16 |

---

## Part V: Platform Drift Prevention Protocol

Platform drift is detected by monitoring the following indicators. Each indicator has a constitutional firebreak.

| Drift Type | Early Warning Signal | Firebreak |
|---|---|---|
| **PD gate erosion** | An asset with RC < 8 appears in the assets table | ARCH-7 (rights gate at ingestion); RM-3 |
| **Quality gate erosion** | IO scores below 45/60 appear in active collections | COL-5 (complete IO record requirement); COL-6 (depth over breadth) |
| **Place-first drift** | A collection is organized by taxon or illustrator without a place anchor | COL-1 (IO primacy); DISC-2 (no orphan entities) |
| **Commerce model drift** | Subscription, advertising, or page-view revenue models are proposed | COM-5 (product-based model permanent) |
| **Institution shortcut** | An institution is activated without a ratified DD | TRUST-2; RM-4; RM-19 |
| **Stack drift** | Neo4j, pgvector, or a proprietary vector store is added to the canonical stack | RM-7; ARCH-2; SD-v1 frozen stack |
| **Breadth over depth** | Place pages launch with <5 IOs or without a GeoNames-confirmed ID | ARCH-5; RM-1; COL-6 |
| **AI rights contamination** | A model output determines a rights classification | RM-16; FM-4 (permanent) |
| **Endorsement language** | Federal agency name appears in product copy as endorser | RM-14; TRUST-6; FS-001 |
| **Orphan entity creation** | Place page launches with 0 discovery graph edges | RM-11; DISC-5 |

**Annual drift audit:** NC conducts an annual review of all 10 drift indicators against the production database and the active product catalogue. Audit results are filed as NC-DRIFT-[YEAR]-001. Any detected drift triggers a constitutional correction record and a sprint-priority remediation.

---

## Part VI: Scale Governance

The following rulings apply as NC crosses specific scale thresholds. They are governed by this constitution from the moment of adoption, not from the moment the threshold is crossed.

### At 100 places
- Place Factory automation (NC-PLACES-FACTORY-001) must be live before the 100th place is activated
- GeoNames authority resolution backlog must be ≤5 unresolved disputes
- Discovery graph must have ≥200 edges with average node degree ≥4

### At 500 places
- All 7 canonical discovery journeys must be traversable with ≥10 nodes per journey
- Overture Maps CC BY 4.0 polygon geometry must be implemented for all active places
- Institution count must be ≥10 ratified DDs covering ≥3 geographic regions

### At 2,000 places
- Place Factory must run automated Stage 1–5 with human gates at Stages 4, 6, 8, and 9 only
- GeoNames authority resolution must be automated for unambiguous records (single canonical match)
- Rights clearance pipeline must process ≥1,000 candidates per sprint without manual review per candidate

### At 10,000 collections
- Every collection must have a canonical place anchor before it is published
- Discovery graph density must maintain average node degree ≥6 across all place types
- Collection assembly automation may generate drafts; human editorial review is required before activation

### At 1,000,000 assets
- IIIF tile generation and manifest caching must be infrastructure-level (not per-request)
- Rights gate automation must achieve ≥98% precision on PD/CC0 classification before any human review backlog exceeds 5,000 candidates
- IO scoring automation must be calibrated against NC-MASTERPIECES-001 top 100 as the ground truth set

---

## Part VII: Amendment Procedure

This constitution may be amended by the following procedure only:

1. **Proposal:** A constitutional amendment is proposed in writing, referencing the specific invariant(s) or principle(s) affected and the specific rationale.
2. **Impact assessment:** Every proposed amendment must include an impact assessment across all 5 canonical principle sets.
3. **Second-human approval:** Amendments to RM-1 through RM-10 require two-human approval. Amendments to RM-11 through RM-20 require one-human approval.
4. **Cross-document consistency check:** The proposing party must verify that the amendment does not conflict with Strategic Direction v1, Standards Constitution v1.0, Foundation Model Constitution v1.0, Wireframe Constitution v1, or Institution Factory Constitution v1.
5. **Version increment:** This document increments to the next minor version (1.1, 1.2, etc.) for principle amendments and to the next major version (2.0) for invariant amendments.
6. **Exceptions not permitted:** No amendment may remove a work from the Canon (RM-12), lift the PD hard gate (RM-3), authorize OSM raw data in canonical tables (RM-17), or lift FM-4 rights hardening (RM-16). These four invariants are unconditionally permanent.

---

*Document: NC-REFERENCE-001 · Version 1.0 · 2026-06-14 · DRAFT pending ratification*
