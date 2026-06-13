# NC-ICH-001: Intangible Heritage Architecture Blueprint

| Field | Value |
|---|---|
| Document | NC-ICH-001 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | NC-GRAPH-002 · NC-AI-001 · Strategic Direction v1 · Illustration Opportunity Doctrine |
| Stack | PostgreSQL · PostGIS · Neo4j · Grounded AI |
| Designation systems | UNESCO ICH · UNESCO WH · Biosphere Reserve · UNESCO Geopark · Ramsar · Dark Sky |

---

## Governing Doctrine

**The commercial object is an Illustration Opportunity, not the heritage practice.**

Intangible Cultural Heritage (ICH) is a living system. The ICH practice itself — a weaving
tradition, a ceremony, throat singing, traditional navigation — is not for sale and is never
the product. What NC commerce serves is the **public-domain documentary record**: the
18th–19th century illustration, the expedition watercolour, the botanical plate, the manuscript
illumination that was created when the practice was first documented.

ICH is therefore a **first-class editorial layer** that:
- grounds illustration opportunities in cultural meaning
- connects natural heritage (places, taxa) to human knowledge and practice
- creates discovery paths that neither natural history nor art history can open alone
- answers the question: "who were the people of this place, and what did they know?"

A `HeritagePractice` node explains *why* an illustration matters. The `Illustration` node
remains the commercial object. This boundary is unconditional.

---

## I. ICH Taxonomy and Domain Mapping

### I.1 UNESCO ICH Five Domains

The 2003 UNESCO Convention for the Safeguarding of ICH defines five domains. NC maps each to
its primary illustration opportunity type.

| Domain | Code | Description | NC Illustration Opportunity |
|---|---|---|---|
| Oral traditions and expressions | OTE | Storytelling, language, proverbs | Manuscript illumination, calligraphic pages |
| Performing arts | PA | Music, dance, theatre, puppetry | Costume plates, instrument drawings, performance illustration |
| Social practices, rituals and festive events | SP | Ceremonies, festivals, rites of passage | Ethnographic expedition illustration |
| Knowledge and practices concerning nature | NK | Traditional ecological knowledge, astronomy, cosmology | Ethnobotanical plates, traditional calendar illustration, navigational charts |
| Traditional craftsmanship | TC | Weaving, pottery, lacquer, metalwork, shipbuilding | Craft process illustration, tool drawings, textile pattern plates |

**NC Priority Domains:** NK (Nature Knowledge) and TC (Traditional Craftsmanship) have the
highest intersection with the existing illustration collection and with the natural heritage layer.
Domain NK is the direct bridge between ICH and the natural history illustration canon.

### I.2 Designation Systems

| System | Governing body | ID format | NC slug pattern |
|---|---|---|---|
| UNESCO Intangible Cultural Heritage | UNESCO (2003 Convention) | Five-digit element ID (e.g. `00008`) | `ich:RL:00008` |
| UNESCO World Heritage | UNESCO WHC | Four-digit site number | `wh:001234` |
| UNESCO Biosphere Reserve | UNESCO MAB Programme | Site name / national code | `br:{country}:{name}` |
| UNESCO Global Geopark | UNESCO | Running number | `gp:001` |
| Ramsar Wetland | Ramsar Secretariat | Running site number | `rs:001` |
| Dark Sky Place | IDA or national equivalent | Designation type + site name | `ds:ida:{name}` |
| IUCN Protected Area | IUCN | Category I–VI | `iucn:{cat}:{wdpa_id}` |

---

## II. The Designation Stack Architecture

The most strategically significant architectural concept in NC-ICH-001 is the **Designation
Stack**: a single place can carry multiple independent heritage designations from different
governing bodies, each confirming its significance through a different lens.

### II.1 Designation Stack Model

```
Place
  │
  ├──[HAS_DESIGNATION]──► HeritageDesignation(type=UNESCO_WH, criteria=[ix,x])
  ├──[HAS_DESIGNATION]──► HeritageDesignation(type=Ramsar, site_no=631)
  ├──[HAS_DESIGNATION]──► HeritageDesignation(type=UNESCO_Biosphere, name="Danube Delta")
  └──[HAS_DESIGNATION]──► HeritageDesignation(type=DarkSky_IDA, name="Westhavelland")
```

### II.2 Stack Height

A place's **stack height** is the count of its active designations. Stack height governs
editorial priority — places with stack ≥3 are NC's highest-significance candidates.

| Stack height | Category | Editorial weight |
|---|---|---|
| 5+ | Exceptional | Highest editorial priority. Feature story mandatory. |
| 4 | Outstanding | Premium collection anchor. |
| 3 | Significant | Standard Tier 1 treatment. |
| 2 | Notable | Tier 2 priority. |
| 1 | Designated | Standard place page. |

### II.3 Known High-Stack Places (examples)

| Place | WH | ICH | Biosphere | Geopark | Ramsar | Dark Sky | Stack |
|---|---|---|---|---|---|---|---|
| Tongariro NP (NZ) | ✓ natural + ✓ cultural | Māori practice (associated) | — | ✓ | — | — | **4** |
| Svalbard (Norway) | — | Arctic practice (assoc.) | ✓ | — | ✓ multiple | ✓ | **4** |
| Wadden Sea | ✓ | — | ✓ | ✓ components | ✓ multiple | — | **4** |
| Shiretoko (Japan) | ✓ | Ainu practice (assoc.) | — | — | ✓ | — | **3** |
| Socotra (Yemen) | ✓ | Practice assoc. | ✓ | — | — | — | **3** |
| Great Barrier Reef | ✓ | Indigenous practice | ✓ | — | ✓ | — | **3** |
| Galápagos | ✓ | — | ✓ | — | ✓ | — | **3** |

### II.4 Dual Cultural + Natural WH (Rare Sites)

UNESCO World Heritage designations may be natural (IUCN criteria vii–x), cultural (ICOMOS
criteria i–vi), or both. Dual WH sites are among the rarest and most significant places on Earth.

| Dual WH site | Natural criteria | Cultural criteria |
|---|---|---|
| Tongariro NP (NZ) | vii, viii | vi |
| Mount Olympus (Greece) | vii | associated |
| Machu Picchu (Peru) | vii | i, iii |
| Tikal (Guatemala) | ix, x | i, iii |
| Kilimanjaro (Tanzania) | vii | associated |

Dual WH sites receive `wh_type: 'mixed'` on their HeritageDesignation nodes and are surfaced
in the "World Heritage: Mixed Sites" discovery collection.

---

## Part I: Node Model

### 1.1 New Constraints and Indexes

```cypher
// ── NEW CONSTRAINTS ───────────────────────────────────────────────────────

CREATE CONSTRAINT practice_id   FOR (n:HeritagePractice) REQUIRE n.practice_id IS UNIQUE;
CREATE CONSTRAINT practice_slug FOR (n:HeritagePractice) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT desig_id      FOR (n:HeritageDesignation) REQUIRE n.designation_id IS UNIQUE;
CREATE CONSTRAINT desig_slug    FOR (n:HeritageDesignation) REQUIRE n.slug IS UNIQUE;

// ── NEW INDEXES ───────────────────────────────────────────────────────────

CREATE INDEX practice_domain    FOR (n:HeritagePractice) ON (n.unesco_domain);
CREATE INDEX practice_list      FOR (n:HeritagePractice) ON (n.ich_list);
CREATE INDEX practice_country   FOR (n:HeritagePractice) ON (n.countries);
CREATE INDEX practice_sensitive FOR (n:HeritagePractice) ON (n.cultural_sensitivity);
CREATE INDEX desig_type         FOR (n:HeritageDesignation) ON (n.designation_type);
CREATE INDEX desig_body         FOR (n:HeritageDesignation) ON (n.inscribing_body);
CREATE INDEX desig_year         FOR (n:HeritageDesignation) ON (n.inscription_year);
CREATE INDEX desig_status       FOR (n:HeritageDesignation) ON (n.status);
```

---

### 1.2 Node: HeritagePractice

A single ICH element registered with UNESCO or an equivalent national/regional body. The node
represents the living practice. It is not a product. It is the cultural frame around which
illustration opportunities are organized.

```cypher
(hp:HeritagePractice {
  // Identity
  practice_id:          STRING,   // PostgreSQL UUID PK
  slug:                 STRING,   // kebab-case (e.g. 'tuvan-throat-singing')
  display_name:         STRING,   // English display name
  local_name:           STRING,   // Name in original language/script
  local_language_code:  STRING,   // ISO 639-1 (e.g. 'ja', 'ar', 'qu')

  // UNESCO Registration
  ich_element_id:       STRING,   // UNESCO element ID (e.g. '00008'); null if non-UNESCO
  ich_list:             STRING,   // 'Representative' | 'Urgent_Safeguarding' | 'Good_Practices' | 'National'
  inscription_year:     INTEGER,  // Year of inscription on the list
  is_multinational:     BOOLEAN,  // true if shared across multiple countries
  countries:            STRING[], // ISO 3166-1 alpha-2 country codes

  // Domain
  unesco_domain:        STRING,   // 'OralTraditions' | 'PerformingArts' | 'SocialPractices'
                                  // | 'NatureKnowledge' | 'Craftsmanship'
  nc_domain_priority:   INTEGER,  // 1 = highest NC relevance (NK and TC = 1)

  // Community
  community_name:       STRING,   // The practicing community name
  community_wikidata:   STRING,   // Wikidata QID for the community entity

  // Cultural governance
  cultural_sensitivity: STRING,   // 'none' | 'consult' | 'restricted'
  // 'restricted' = sacred/ceremonial; blocks ALL product activation paths
  // 'consult' = community review required before product activation
  // 'none' = standard PD documentary product path available

  community_review_status: STRING, // 'approved' | 'pending' | 'declined' | 'not_required'
  // Only 'approved' or 'not_required' permit product activation for 'consult' practices

  // Illustration connection
  has_pd_documentation: BOOLEAN,  // true if confirmed PD documentary illustration exists
  earliest_documentation_year: INTEGER, // year of earliest known PD illustration

  // Identity links
  wikidata_qid:         STRING,   // Required before production activation (ICH-4)
  ich_url:              STRING,   // UNESCO ICH element page URL

  // Editorial
  summary:              STRING,   // One-sentence NC editorial summary
  status:               STRING,   // 'active' | 'endangered' | 'extinct' | 'revitalized'

  // Provenance (G-2)
  pg_id:                STRING,
  pg_table:             STRING,   // 'nc_heritage_practices'
  schema_version:       STRING,
  projection_run_id:    STRING,
  projected_at:         DATETIME
})
```

---

### 1.3 Node: HeritageDesignation

A formal inscription on a heritage list by a recognized governing body. One place may carry
many designations. The designation is metadata about the place's significance — it governs
editorial weight and discovery ranking, but never directly governs commerce or rights.

```cypher
(hd:HeritageDesignation {
  // Identity
  designation_id:       STRING,   // PostgreSQL UUID PK
  slug:                 STRING,   // e.g. 'wh-1234' | 'ramsar-631' | 'ich-rl-00008'
  official_name:        STRING,   // Official name as inscribed

  // Classification
  designation_type:     STRING,
  // 'UNESCO_WH_Natural'     — IUCN natural criteria (vii, viii, ix, x)
  // 'UNESCO_WH_Cultural'    — ICOMOS cultural criteria (i, ii, iii, iv, v, vi)
  // 'UNESCO_WH_Mixed'       — both natural AND cultural criteria
  // 'UNESCO_ICH_Representative' — 2003 Convention Representative List
  // 'UNESCO_ICH_Urgent'     — Urgent Safeguarding List
  // 'UNESCO_ICH_GoodPractice' — Register of Good Safeguarding Practices
  // 'UNESCO_Biosphere'      — UNESCO MAB Biosphere Reserve
  // 'UNESCO_Geopark'        — UNESCO Global Geopark
  // 'Ramsar'                — Ramsar Convention wetland
  // 'DarkSky_IDA'           — IDA International Dark Sky Place
  // 'DarkSky_NPS'           — NPS Night Sky Programme
  // 'IUCN_Ia'–'IUCN_VI'     — IUCN protected area categories

  inscribing_body:      STRING,   // 'UNESCO' | 'Ramsar_Secretariat' | 'IDA' | 'IUCN'
  official_id:          STRING,   // Governing body's list number/code

  // For UNESCO World Heritage
  wh_site_number:       INTEGER,  // WHC site number (4 digits)
  wh_criteria:          STRING[], // criteria applied: ['vii','ix'] or ['i','vi']
  wh_type:              STRING,   // 'natural' | 'cultural' | 'mixed'

  // Inscription
  inscription_year:     INTEGER,
  extension_years:      INTEGER[], // years of boundary extensions
  status:               STRING,   // 'Active' | 'In_Danger' | 'Delisted'
  in_danger_since:      INTEGER,  // year placed on In Danger list (if applicable)

  // Scope
  area_ha:              FLOAT,    // designated area in hectares
  is_serial:            BOOLEAN,  // true if nomination covers multiple components
  component_count:      INTEGER,  // number of components (serial sites)
  is_transboundary:     BOOLEAN,  // true if crosses national borders
  country_codes:        STRING[], // countries participating in transboundary designation

  // Editorial
  nc_editorial_weight:  INTEGER,  // 1–5; contributes to place stack height calculation

  // Provenance (G-2)
  pg_id:                STRING,
  pg_table:             STRING,   // 'nc_heritage_designations'
  schema_version:       STRING,
  projection_run_id:    STRING,
  projected_at:         DATETIME
})
```

---

### 1.4 Extended Node Properties

The following existing node types receive new properties to participate in the ICH layer.

**Place** — add:
```
  designation_stack_height: INTEGER,  // count of active HAS_DESIGNATION edges; updated by projection
  wh_type:                  STRING,   // 'natural' | 'cultural' | 'mixed' | null
  has_ich_element:          BOOLEAN,  // true if any PRACTICES_HERE edge exists
  has_dark_sky:             BOOLEAN,  // true if DarkSky_IDA or DarkSky_NPS designation active
```

**Illustration** — add:
```
  documents_practice:       BOOLEAN,  // true if DOCUMENTS_PRACTICE edge exists
  ich_domain:               STRING,   // ICH domain of the documented practice (denormalized)
```

**Collection** — add:
```
  collection_type:          STRING,   // existing + new types (see Part III)
  heritage_designation_types: STRING[], // designation types this collection represents
  ich_domain_focus:         STRING,   // primary ICH domain (null for non-ICH collections)
```

---

## Part II: Relationship Model

### 2.1 New Relationships

```cypher
// ── DESIGNATION RELATIONSHIPS ─────────────────────────────────────────────

(p:Place)-[:HAS_DESIGNATION {
  primary_feature: BOOLEAN,       // true if this designation names the place directly
  buffer_zone:     BOOLEAN,       // true if place is in buffer zone only
  component_id:    STRING,        // for serial sites: which component this place represents
  confirmed_year:  INTEGER,
  derivation:      'direct',
  pg_source:       'nc_place_designations',
  pg_source_id:    STRING,
  ...relationship_provenance
}]->(hd:HeritageDesignation)


// ── ICH PRACTICE RELATIONSHIPS ────────────────────────────────────────────

(hp:HeritagePractice)-[:PRACTICED_AT {
  // The place where this ICH practice originates or is predominantly practiced
  role:            STRING,        // 'origin' | 'primary' | 'secondary' | 'diaspora'
  active_since:    INTEGER,       // earliest confirmed year of practice at this place
  still_active:    BOOLEAN,
  derivation:      'direct',
  pg_source:       'nc_practice_place_anchors',
  pg_source_id:    STRING,
  ...relationship_provenance
}]->(p:Place)


(hp:HeritagePractice)-[:DOCUMENTED_BY {
  // Connects a living practice to its PD documentary illustration record
  // THIS is the bridge between living ICH and the illustration opportunity
  documentation_year: INTEGER,    // year the illustration was created
  documenter_role: STRING,        // 'expedition_artist' | 'naturalist' | 'court_artist' | 'traveller'
  documentation_context: STRING,  // brief note: e.g. 'Cook First Voyage, Tahiti, 1769'
  product_path_clear: BOOLEAN,    // true only if cultural_sensitivity != 'restricted' AND
                                  // community_review_status IN ('approved', 'not_required')
  derivation:      'direct',
  pg_source:       'nc_practice_illustrations',
  pg_source_id:    STRING,
  ...relationship_provenance
}]->(i:Illustration)


(i:Illustration)-[:DOCUMENTS_PRACTICE {
  // Inverse of DOCUMENTED_BY; required for bidirectional traversal
  documentation_year: INTEGER,
  derivation:      'direct',
  pg_source:       'nc_practice_illustrations',
  pg_source_id:    STRING,
  ...relationship_provenance
}]->(hp:HeritagePractice)


(a:Artist)-[:DOCUMENTED_CULTURE {
  // Artist who created PD illustrations documenting ICH practices
  context:         STRING,        // expedition, commission, self-directed observation
  period:          STRING,        // approximate period: '1750-1800' etc.
  derivation:      'direct',
  pg_source:       'nc_practice_illustrations',
  pg_source_id:    STRING,
  ...relationship_provenance
}]->(hp:HeritagePractice)


(e:Expedition)-[:DOCUMENTED_CULTURE {
  // Expedition that produced documentary illustrations of ICH
  stop_name:       STRING,        // place name at time of expedition
  year:            INTEGER,
  derivation:      'direct',
  pg_source:       'nc_expedition_culture_records',
  pg_source_id:    STRING,
  ...relationship_provenance
}]->(hp:HeritagePractice)


(hp:HeritagePractice)-[:EVOLVED_INTO {
  // Explicit editorial relationship: practice A evolved into or gave rise to practice B
  estimated_period: STRING,
  evidence_source:  STRING,
  derivation:      'direct',
  pg_source:       'nc_practice_lineage',
  pg_source_id:    STRING,
  ...relationship_provenance
}]->(hp2:HeritagePractice)


// ── DERIVED ICH RELATIONSHIPS ──────────────────────────────────────────────

(hp:HeritagePractice)-[:CO_PRACTICED_WITH {
  // Derived: two practices share at least one common PRACTICED_AT place
  shared_place_count: INTEGER,    // number of shared places
  confidence:         FLOAT,      // 1.0 if both have 'origin' role at same place
  derivation:         'derived',
  pg_source:          'nc_practice_place_anchors JOIN',
  ...relationship_provenance
}]->(hp2:HeritagePractice)


(hd:HeritageDesignation)-[:OVERLAPS_WITH {
  // Derived: two designations share at least one place
  shared_place_count: INTEGER,
  overlap_type:       STRING,     // 'same_place' | 'nested' | 'adjacent'
  derivation:         'derived',
  pg_source:          'nc_place_designations JOIN',
  ...relationship_provenance
}]->(hd2:HeritageDesignation)


// ── COLLECTION RELATIONSHIPS (extensions) ─────────────────────────────────

(c:Collection)-[:FEATURES_PRACTICE {
  feature_role:    STRING,        // 'anchor' | 'context' | 'supporting'
  ich_domain:      STRING,
  derivation:      'direct',
  pg_source:       'nc_collection_practices',
  pg_source_id:    STRING,
  ...relationship_provenance
}]->(hp:HeritagePractice)


// ── CROSS-DOMAIN BRIDGE ────────────────────────────────────────────────────

(hp:HeritagePractice)-[:USES_TAXON {
  // Connects Nature Knowledge practices (Domain NK) to biological taxa
  // e.g. traditional plant medicine → the plant; traditional fishing → the fish species
  use_type:        STRING,        // 'medicinal' | 'food' | 'ceremonial' | 'material' | 'spiritual'
  derivation:      'direct',
  pg_source:       'nc_practice_taxa',
  pg_source_id:    STRING,
  ...relationship_provenance
}]->(t:Taxon)
```

### 2.2 New Relationship Summary

| Relationship | Direction | Derivation | Cardinality | Key use |
|---|---|---|---|---|
| HAS_DESIGNATION | Place → HeritageDesignation | direct | many:many | Designation Stack |
| PRACTICED_AT | HeritagePractice → Place | direct | many:many | ICH geographic anchor |
| DOCUMENTED_BY | HeritagePractice → Illustration | direct | many:many | Commerce bridge |
| DOCUMENTS_PRACTICE | Illustration → HeritagePractice | direct | many:many | Reverse traversal |
| DOCUMENTED_CULTURE | Artist → HeritagePractice | direct | many:many | Maker identity |
| DOCUMENTED_CULTURE | Expedition → HeritagePractice | direct | many:many | Expedition thread |
| EVOLVED_INTO | HeritagePractice → HeritagePractice | direct | many:many | Lineage navigation |
| FEATURES_PRACTICE | Collection → HeritagePractice | direct | many:many | Collection model |
| USES_TAXON | HeritagePractice → Taxon | direct | many:many | NK domain bridge |
| CO_PRACTICED_WITH | HeritagePractice ↔ HeritagePractice | **derived** | many:many | Discovery |
| OVERLAPS_WITH | HeritageDesignation ↔ HeritageDesignation | **derived** | many:many | Stack discovery |

---

## Part III: Collection Model

### 3.1 New Collection Types

Six ICH-specific collection types extend the existing `Collection` node vocabulary.

```
Existing collection_type values:
  PLACE_ANCHOR, ARTIST_SURVEY, TAXON_SURVEY, PERIOD_SURVEY,
  EDITORIAL_STORY, PRODUCT_CAPSULE

New ICH collection_type values:
  PLACE_HERITAGE_PACK
  PRACTICE_PORTFOLIO
  TRADITION_SURVEY
  DOMAIN_COLLECTION
  DESIGNATION_BUNDLE
  HERITAGE_EXPEDITION
```

---

### 3.2 Collection Type Definitions

**PLACE_HERITAGE_PACK**
All illustration opportunities associated with a single place's full heritage stack — natural
history, ICH documentation, landscape painting, and expedition records unified. The editorial
question: "What is the complete visual record of this place and its people?"

```cypher
// Heritage Pack for Tongariro National Park
MATCH (p:Place {slug: 'tongariro-national-park'})
MATCH (p)-[:HAS_DESIGNATION]->(hd:HeritageDesignation)
MATCH (p)<-[:PRACTICED_AT]-(hp:HeritagePractice)
MATCH (hp)-[:DOCUMENTED_BY]->(i:Illustration)
  WHERE i.product_safe = true
MATCH (p)<-[:ASSOCIATED_WITH]-(i2:Illustration)
  WHERE i2.product_safe = true
RETURN p, hd, hp, collect(DISTINCT i) + collect(DISTINCT i2) AS pack_illustrations
```

---

**PRACTICE_PORTFOLIO**
All confirmed PD illustrations that document a single ICH practice, organized by documentation
period and expedition context.

```cypher
// Portfolio for Japanese Traditional Tea Ceremony (example slug)
MATCH (hp:HeritagePractice {slug: 'traditional-tea-ceremony-chanoyu'})
  WHERE hp.cultural_sensitivity IN ['none', 'consult']
  AND hp.community_review_status IN ['approved', 'not_required']
MATCH (hp)-[:DOCUMENTED_BY]->(i:Illustration)
  WHERE i.product_safe = true AND i.year < 1928
OPTIONAL MATCH (i)-[:CREATED_BY]->(a:Artist)
RETURN hp, collect({illustration: i, artist: a}) AS portfolio
  ORDER BY i.year
```

---

**TRADITION_SURVEY**
PD illustrations spanning a **cultural tradition** — a cluster of related practices from a
shared cultural lineage. The editorial question: "What is the visual legacy of this civilization
as documented by its contemporaries?"

Examples:
- "Japanese Court Arts" — Noh, Tea, Ikebana, Calligraphy documentation
- "Pacific Navigation Tradition" — wayfinding, star charts, canoe illustration
- "West African Court Tradition" — royal court art documentation

Anchor: multiple `HeritagePractice` nodes connected by `CO_PRACTICED_WITH` or explicit
`EVOLVED_INTO` edges, all sharing a common `community_wikidata` entity or geographic cluster.

---

**DOMAIN_COLLECTION**
All illustration opportunities organized by a single UNESCO ICH domain, filtered by region.
The editorial question: "What is the visual record of traditional craftsmanship in East Asia?"

```cypher
// Traditional Craftsmanship in East Asia
MATCH (hp:HeritagePractice {unesco_domain: 'Craftsmanship'})
  WHERE 'JP' IN hp.countries OR 'CN' IN hp.countries
    OR 'KR' IN hp.countries
MATCH (hp)-[:DOCUMENTED_BY]->(i:Illustration)
  WHERE i.product_safe = true
RETURN hp.display_name, collect(DISTINCT i) AS illustrations
```

---

**DESIGNATION_BUNDLE**
The full heritage designation profile of a place — all UNESCO WH, ICH, Biosphere, Geopark,
Ramsar, and Dark Sky designations overlaid. The editorial question: "What makes this place one
of the most recognized heritage sites on Earth?"

Purpose: flagship editorial collection for high-stack-height places. Unlocked only when
`Place.designation_stack_height >= 3`.

---

**HERITAGE_EXPEDITION**
All ICH documentation produced by a single historic expedition. The editorial question:
"What did the Forster/Cook Second Voyage reveal about Pacific traditional culture?"

```cypher
// Cook Second Voyage (1772–75) heritage documentation
MATCH (e:Expedition {slug: 'cook-second-voyage'})
MATCH (e)-[:DOCUMENTED_CULTURE]->(hp:HeritagePractice)
MATCH (hp)-[:DOCUMENTED_BY]->(i:Illustration)
  WHERE i.product_safe = true
MATCH (e)-[:PASSED_THROUGH]->(p:Place)
RETURN e, p, hp, collect(i) AS illustrations
```

---

## Part IV: Product Model

### 4.1 ICH Product Types

ICH documentation enables five product types beyond the existing natural history and landscape
illustration lines. All five types are governed by the Illustration Opportunity Doctrine and the
ICH-1/ICH-2/ICH-3 commerce invariants.

**Before activating any ICH illustration product:**
1. `HeritagePractice.cultural_sensitivity` must be `'none'` OR `'consult'` with `community_review_status = 'approved'`
2. `HeritagePractice.cultural_sensitivity` must **not** be `'restricted'`
3. `Illustration.product_safe = true` AND `Illustration.year < 1928`
4. The illustration must be a **documentary record**, not an appropriation of sacred material

| Product type | Code | Description | Primary illustration source |
|---|---|---|---|
| Craft Documentation Giclée | ICH-PROD-01 | Museum-quality print of PD craft process illustration | Met, CMA, Walters |
| Ceremonial Object Study | ICH-PROD-02 | PD illustration of traditional objects (non-sacred only) | Walters, NHM, Europeana |
| Ethnobotanical Plate | ICH-PROD-03 | Traditional plant knowledge documented by naturalists (NK domain) | NHM, Europeana |
| Maritime Heritage Chart | ICH-PROD-04 | Traditional navigation knowledge (Pacific wayfinding, Norse charts) | NHM, NARA |
| Performance Costume Plate | ICH-PROD-05 | Costume and instrument illustration from PD documentation | Met, CMA, NHM |

### 4.2 Commerce Path Governance

The commerce path for an ICH product requires **four gates** in addition to the standard NC
product activation sequence:

```
Gate ICH-A: cultural_sensitivity check
  PASS: cultural_sensitivity = 'none' → proceed
  HOLD: cultural_sensitivity = 'consult' → require community_review_status = 'approved'
  BLOCK: cultural_sensitivity = 'restricted' → permanent block, no override

Gate ICH-B: PD documentation verification
  PASS: illustration.year < 1928 AND product_safe = true
  BLOCK: any image where documentation predates the practice being claimed (anachronism)

Gate ICH-C: appropriation review
  PASS: illustration depicts craft process, material objects, or landscape context
  BLOCK: illustration depicts active ceremony, sacred ritual, or restricted knowledge
  (Editorial judgment required — flag for Principal Architect review)

Gate ICH-D: attribution completeness
  PASS: both institution attribution AND heritage_practice attribution are resolvable
  HOLD: if ICH attribution path is unclear
```

### 4.3 Highest-Value ICH Product Opportunities

| ICH Practice | Primary illustration anchor | Institution | NC product type | Est. demand |
|---|---|---|---|---|
| Japanese Noh Theatre | Noh mask and costume woodblocks | Met, CMA | ICH-PROD-05 | High |
| Traditional Silk Weaving (China/Japan) | Sericulture process illustration | Met, CMA | ICH-PROD-01 | High |
| Falconry (multinational) | Medieval falconry manuscript illuminations | Walters | ICH-PROD-02 | High |
| Pacific Traditional Navigation | Cook voyage star chart and canoe illustration | NHM | ICH-PROD-04 | High |
| Andean Textile Weaving | Humboldt/Tschudi expedition textile illustration | NHM, Europeana | ICH-PROD-01 | High |
| Arabic Calligraphy | Walters Islamic manuscript pages | Walters | ICH-PROD-02 | High |
| Traditional Japanese Tea | Utensil and teahouse illustration | Met, CMA | ICH-PROD-02 | High |
| Mediterranean Viticulture | Botanical grape plate (Redouté-era) | Europeana | ICH-PROD-03 | High |
| Ethnobotanical Plant Knowledge | NHM ethnobotanical plates | NHM | ICH-PROD-03 | High |
| Traditional Beekeeping (Mediterranean) | Hive illustration, natural history period | NHM, Europeana | ICH-PROD-01 | Medium |

---

## Part V: Discovery Model

### 5.1 New Discovery Journeys

Six discovery journeys open when the ICH layer is active. All six require both ICH nodes
(`HeritagePractice`, `HeritageDesignation`) to be populated in the graph.

---

#### Journey ICH-1: Designation Stack Discovery

**Entry point:** Any place page  
**Question:** "What makes this place globally significant — and how many ways?"  
**Output:** The full designation stack with editorial narrative per designation type

```cypher
MATCH (p:Place {slug: $slug})
MATCH (p)-[:HAS_DESIGNATION]->(hd:HeritageDesignation)
OPTIONAL MATCH (p)<-[:PRACTICED_AT]-(hp:HeritagePractice)
RETURN p.name AS place,
       p.designation_stack_height AS stack_height,
       collect(DISTINCT {
         type:         hd.designation_type,
         official_id:  hd.official_id,
         year:         hd.inscription_year,
         status:       hd.status,
         criteria:     hd.wh_criteria,
         body:         hd.inscribing_body
       }) AS designations,
       collect(DISTINCT {
         practice:  hp.display_name,
         domain:    hp.unesco_domain,
         status:    hp.status
       }) AS ich_elements
ORDER BY hd.inscription_year
```

---

#### Journey ICH-2: Living Practice → Illustration Archaeology

**Entry point:** Any `HeritagePractice` node  
**Question:** "Who first documented this practice? What illustration did they leave?"  
**Output:** Illustration opportunities with expedition/artist context, ordered by year

```cypher
MATCH (hp:HeritagePractice {slug: $practice_slug})
  WHERE hp.cultural_sensitivity <> 'restricted'
MATCH (hp)-[db:DOCUMENTED_BY]->(i:Illustration)
  WHERE i.product_safe = true
OPTIONAL MATCH (i)-[:CREATED_BY]->(a:Artist)
OPTIONAL MATCH (i)-[:PART_OF_EXPEDITION]->(e:Expedition)
OPTIONAL MATCH (i)-[:SOURCED_FROM]->(inst:Institution)
RETURN hp.display_name                          AS practice,
       hp.unesco_domain                         AS domain,
       collect({
         illustration:  i.display_title,
         year:          i.year,
         artist:        a.name,
         expedition:    e.name,
         institution:   inst.display_name,
         rights:        i.rights,
         product_safe:  i.product_safe,
         context:       db.documentation_context
       }) AS documentary_record
ORDER BY i.year ASC
```

---

#### Journey ICH-3: Cross-Domain Heritage Bridge (Nature + Culture)

**Entry point:** Any `Place` node  
**Question:** "Where does the natural history and the cultural history of this place intersect?"  
**Output:** Parallel illustration opportunities — the naturalist and the ethnographer at the same place

```cypher
MATCH (p:Place {slug: $slug})

// Natural history strand
OPTIONAL MATCH (p)<-[:ASSOCIATED_WITH]-(nat:Illustration)
  WHERE nat.product_safe = true
OPTIONAL MATCH (nat)-[:DEPICTS]->(t:Taxon)

// Cultural heritage strand
OPTIONAL MATCH (p)<-[:PRACTICED_AT]-(hp:HeritagePractice)
  WHERE hp.cultural_sensitivity <> 'restricted'
OPTIONAL MATCH (hp)-[:DOCUMENTED_BY]->(cul:Illustration)
  WHERE cul.product_safe = true

// Shared expeditions: naturalists who also documented culture
OPTIONAL MATCH (nat)-[:PART_OF_EXPEDITION]->(e:Expedition)
OPTIONAL MATCH (cul)-[:PART_OF_EXPEDITION]->(e)

RETURN p.name AS place,
       collect(DISTINCT {strand: 'nature', illustration: nat.display_title, taxon: t.common_name}) AS natural_record,
       collect(DISTINCT {strand: 'culture', illustration: cul.display_title, practice: hp.display_name}) AS cultural_record,
       collect(DISTINCT e.name) AS shared_expeditions
```

---

#### Journey ICH-4: Domain Immersion (ICH Domain Browse)

**Entry point:** ICH domain selection (e.g. "Traditional Craftsmanship")  
**Question:** "Show me all illustration opportunities for traditional craftsmanship in Asia"  
**Output:** Practice → illustration grid filtered by domain and region

```cypher
MATCH (hp:HeritagePractice {unesco_domain: $domain})
  WHERE hp.cultural_sensitivity <> 'restricted'
  AND any(c IN hp.countries WHERE c IN $country_codes)
MATCH (hp)-[:DOCUMENTED_BY]->(i:Illustration)
  WHERE i.product_safe = true
OPTIONAL MATCH (hp)-[:PRACTICED_AT]->(p:Place)
OPTIONAL MATCH (i)-[:SOURCED_FROM]->(inst:Institution)
RETURN hp.display_name    AS practice,
       hp.community_name  AS community,
       p.name             AS primary_place,
       collect({
         title:       i.display_title,
         year:        i.year,
         institution: inst.display_name,
         rights:      i.rights
       }) AS illustrations
ORDER BY size(illustrations) DESC
```

---

#### Journey ICH-5: World Heritage Depth (Mixed Sites)

**Entry point:** UNESCO WH designation  
**Question:** "Show me the world's places that hold both natural and cultural World Heritage status"  
**Output:** Mixed WH sites with their combined illustration record

```cypher
MATCH (hd:HeritageDesignation {wh_type: 'mixed'})
MATCH (p:Place)-[:HAS_DESIGNATION]->(hd)

// Natural record
OPTIONAL MATCH (p)<-[:ASSOCIATED_WITH]-(nat_i:Illustration)
  WHERE nat_i.product_safe = true

// Cultural record
OPTIONAL MATCH (p)<-[:PRACTICED_AT]-(hp:HeritagePractice)
  WHERE hp.cultural_sensitivity <> 'restricted'

RETURN p.name                  AS place,
       hd.wh_criteria          AS criteria,
       hd.inscription_year     AS inscribed,
       count(DISTINCT nat_i)   AS natural_illustrations,
       count(DISTINCT hp)      AS ich_elements,
       p.designation_stack_height AS stack_height
ORDER BY p.designation_stack_height DESC, natural_illustrations DESC
```

---

#### Journey ICH-6: Heritage Density Discovery (Highest-Stack Places)

**Entry point:** Discovery homepage or collection browse  
**Question:** "Show me the places on Earth recognized by the most heritage bodies"  
**Output:** Top places by designation stack height, with full designation profile

```cypher
MATCH (p:Place)
  WHERE p.designation_stack_height >= 3
MATCH (p)-[:HAS_DESIGNATION]->(hd:HeritageDesignation)
OPTIONAL MATCH (p)<-[:PRACTICED_AT]-(hp:HeritagePractice)
  WHERE hp.cultural_sensitivity <> 'restricted'
OPTIONAL MATCH (p)<-[:ASSOCIATED_WITH]-(i:Illustration)
  WHERE i.product_safe = true
RETURN p.name                         AS place,
       p.designation_stack_height      AS stack_height,
       collect(DISTINCT hd.designation_type) AS designation_types,
       count(DISTINCT hp)              AS ich_elements,
       count(DISTINCT i)               AS product_safe_illustrations,
       p.geonames_id                   AS geonames_id
ORDER BY stack_height DESC, product_safe_illustrations DESC
LIMIT 25
```

---

### 5.2 Discovery Routing by Entry Point

| Entry point | Journey | Primary node | Output shape |
|---|---|---|---|
| Place page (any) | ICH-1 Designation Stack | Place | Designation cards + ICH element list |
| ICH practice page | ICH-2 Practice Archaeology | HeritagePractice | Timeline of documentary illustration |
| Place page (any) | ICH-3 Cross-Domain Bridge | Place | Parallel nature/culture illustration grid |
| Domain browse | ICH-4 Domain Immersion | HeritagePractice | Practice → illustration grid |
| UNESCO WH browse | ICH-5 Mixed Sites | HeritageDesignation | Criteria + combined record |
| Discovery homepage | ICH-6 Heritage Density | Place (sorted by stack) | Top 25 places by recognition |

---

## Part VI: PostgreSQL Schema Integration

### 6.1 New Tables

```sql
-- Heritage practices (ICH elements and analogs)
CREATE TABLE nc_heritage_practices (
  practice_id           UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  slug                  TEXT         NOT NULL UNIQUE,
  display_name          TEXT         NOT NULL,
  local_name            TEXT,
  local_language_code   CHAR(2),
  ich_element_id        TEXT,                     -- UNESCO element ID; null if non-UNESCO
  ich_list              TEXT         NOT NULL,    -- Representative|Urgent_Safeguarding|Good_Practices|National
  inscription_year      INTEGER,
  is_multinational      BOOLEAN      NOT NULL DEFAULT false,
  countries             TEXT[]       NOT NULL,    -- ISO 3166-1 alpha-2 codes
  unesco_domain         TEXT         NOT NULL,    -- OralTraditions|PerformingArts|SocialPractices|NatureKnowledge|Craftsmanship
  nc_domain_priority    SMALLINT     NOT NULL DEFAULT 2,
  community_name        TEXT,
  community_wikidata    TEXT,
  cultural_sensitivity  TEXT         NOT NULL DEFAULT 'none'
    CHECK (cultural_sensitivity IN ('none', 'consult', 'restricted')),
  community_review_status TEXT       NOT NULL DEFAULT 'not_required'
    CHECK (community_review_status IN ('approved', 'pending', 'declined', 'not_required')),
  has_pd_documentation  BOOLEAN      NOT NULL DEFAULT false,
  earliest_documentation_year INTEGER,
  wikidata_qid          TEXT,
  ich_url               TEXT,
  summary               TEXT,
  status                TEXT         NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'endangered', 'extinct', 'revitalized')),
  created_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),
  updated_at            TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Heritage designations (formal inscriptions by recognized bodies)
CREATE TABLE nc_heritage_designations (
  designation_id        UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  slug                  TEXT         NOT NULL UNIQUE,
  official_name         TEXT         NOT NULL,
  designation_type      TEXT         NOT NULL,
  inscribing_body       TEXT         NOT NULL,
  official_id           TEXT,
  wh_site_number        INTEGER,
  wh_criteria           TEXT[],
  wh_type               TEXT         CHECK (wh_type IN ('natural', 'cultural', 'mixed')),
  inscription_year      INTEGER      NOT NULL,
  extension_years       INTEGER[],
  status                TEXT         NOT NULL DEFAULT 'Active'
    CHECK (status IN ('Active', 'In_Danger', 'Delisted')),
  in_danger_since       INTEGER,
  area_ha               NUMERIC(14,2),
  is_serial             BOOLEAN      NOT NULL DEFAULT false,
  component_count       INTEGER,
  is_transboundary      BOOLEAN      NOT NULL DEFAULT false,
  country_codes         TEXT[],
  nc_editorial_weight   SMALLINT     NOT NULL DEFAULT 1
    CHECK (nc_editorial_weight BETWEEN 1 AND 5),
  wikidata_qid          TEXT,
  created_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),
  updated_at            TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Place ↔ Designation (many-to-many)
CREATE TABLE nc_place_designations (
  place_id              UUID         NOT NULL REFERENCES nc_places(place_id),
  designation_id        UUID         NOT NULL REFERENCES nc_heritage_designations(designation_id),
  primary_feature       BOOLEAN      NOT NULL DEFAULT true,
  buffer_zone           BOOLEAN      NOT NULL DEFAULT false,
  component_id          TEXT,
  confirmed_year        INTEGER,
  PRIMARY KEY (place_id, designation_id)
);

-- Practice ↔ Place (many-to-many)
CREATE TABLE nc_practice_place_anchors (
  practice_id           UUID         NOT NULL REFERENCES nc_heritage_practices(practice_id),
  place_id              UUID         NOT NULL REFERENCES nc_places(place_id),
  role                  TEXT         NOT NULL DEFAULT 'primary'
    CHECK (role IN ('origin', 'primary', 'secondary', 'diaspora')),
  active_since          INTEGER,
  still_active          BOOLEAN      NOT NULL DEFAULT true,
  PRIMARY KEY (practice_id, place_id)
);

-- Practice ↔ Illustration (the documentary record bridge)
CREATE TABLE nc_practice_illustrations (
  practice_id           UUID         NOT NULL REFERENCES nc_heritage_practices(practice_id),
  illustration_id       UUID         NOT NULL REFERENCES nc_illustration_opportunities(illustration_id),
  documentation_year    INTEGER,
  documenter_role       TEXT,
  documentation_context TEXT,
  PRIMARY KEY (practice_id, illustration_id),
  -- ICH-2 enforcement: products blocked for restricted practices
  CONSTRAINT practice_not_restricted CHECK (
    (SELECT cultural_sensitivity FROM nc_heritage_practices p WHERE p.practice_id = nc_practice_illustrations.practice_id) <> 'restricted'
  )
);

-- Practice ↔ Taxon (NK domain cross-domain bridge)
CREATE TABLE nc_practice_taxa (
  practice_id           UUID         NOT NULL REFERENCES nc_heritage_practices(practice_id),
  taxon_id              UUID         NOT NULL REFERENCES nc_taxa(taxon_id),
  use_type              TEXT         NOT NULL
    CHECK (use_type IN ('medicinal', 'food', 'ceremonial', 'material', 'spiritual')),
  PRIMARY KEY (practice_id, taxon_id)
);
```

### 6.2 Computed Column: designation_stack_height

```sql
-- Maintained by trigger; also queryable directly
CREATE OR REPLACE FUNCTION nc_update_designation_stack_height()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE nc_places
  SET designation_stack_height = (
    SELECT COUNT(*)
    FROM nc_place_designations pd
    JOIN nc_heritage_designations hd ON pd.designation_id = hd.designation_id
    WHERE pd.place_id = COALESCE(NEW.place_id, OLD.place_id)
      AND hd.status = 'Active'
  )
  WHERE place_id = COALESCE(NEW.place_id, OLD.place_id);
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_stack_height
AFTER INSERT OR UPDATE OR DELETE ON nc_place_designations
FOR EACH ROW EXECUTE FUNCTION nc_update_designation_stack_height();
```

---

## Part VII: Governance Invariants

Six unconditional ICH governance invariants, appended to the G-1–G-8 set from NC-GRAPH-002.

| Code | Invariant |
|---|---|
| ICH-1 | A `HeritagePractice` node is never the commercial object. Only `Illustration` nodes with `product_safe = true`, reachable via the `DOCUMENTED_BY` edge and governed by G-5/FM-4, are commercial objects. |
| ICH-2 | `HeritagePractice` nodes with `cultural_sensitivity = 'restricted'` block all `DOCUMENTED_BY → DERIVED_FROM` commerce paths. No product activation is permitted for restricted practices. No override exists. |
| ICH-3 | `HeritagePractice` nodes with `cultural_sensitivity = 'consult'` require `community_review_status = 'approved'` before any product line activation. Approval must come from an identified community representative and must be documented in `nc_heritage_practices.community_review_notes`. |
| ICH-4 | `ich_element_id` from the UNESCO ICH Register is the identity authority for UNESCO-listed `HeritagePractice` nodes. Wikidata QID cross-link via `SAME_AS` is required before any `HeritagePractice` enters production. National-only practices must document the national register source. |
| ICH-5 | `HeritageDesignation` nodes are evidence-layer metadata. No rights determination, no commerce gate, and no product pricing decision derives from designation status alone. Designations govern editorial weight and discovery ranking only. |
| ICH-6 | `CO_PRACTICED_WITH` relationships are derived exclusively from shared `PRACTICED_AT` place edges in the graph. No editorial assertion of co-practice may be made without at least one shared `PRACTICED_AT` place evidence. |

---

## Part VIII: Content Institution Mapping

### 8.1 ICH Domain × Institution Matrix

| ICH Domain | Best institutions (current) | Content type | Coverage |
|---|---|---|---|
| Traditional Craftsmanship (TC) | Met (Japan, China), CMA (East Asia), Walters (Islamic crafts), Europeana | Process illustration, tool drawings, textile plates | **High** — extensive PD material confirmed |
| Nature & Universe Knowledge (NK) | NHM (ethnobotany, Cook voyage), Europeana, DPLA | Ethnobotanical plates, traditional calendars, star maps | **High** — NHM core strength |
| Performing Arts (PA) | Met (East Asian performance), CMA, NHM (expedition costume records) | Costume plates, instrument drawings | **Medium** — scattered across institutions |
| Social Practices (SP) | Walters (illuminated manuscript rituals), Europeana, DPLA (Native American) | Ethnographic illustration | **Medium** — requires per-item rights check |
| Oral Traditions (OTE) | Walters (manuscript traditions), CMA (calligraphy), NHM | Calligraphy pages, manuscript illumination | **Medium** — limited direct illustration |

### 8.2 Highest-Value ICH × Institution Pairs

| Practice | Institution | PD illustration | Product type |
|---|---|---|---|
| Noh Theatre (Japan) | Met, CMA | Woodblock costume and mask plates | ICH-PROD-05 |
| Silk Weaving (China/Japan) | Met, CMA | Sericulture process illustration | ICH-PROD-01 |
| Falconry (multinational) | Walters | *De Arte Venandi cum Avibus* illuminations | ICH-PROD-02 |
| Pacific Navigation | NHM | Cook voyage star and canoe illustration | ICH-PROD-04 |
| Andean Textile | NHM | Humboldt/Tschudi textile plates | ICH-PROD-01 |
| Arabic Calligraphy | Walters | Islamic manuscript pages (CC0, pre-1928) | ICH-PROD-02 |
| Chanoyu / Tea Ceremony | Met, CMA | Utensil and teahouse illustration | ICH-PROD-02 |
| Mediterranean Viticulture | Europeana | Ampelography botanical plates | ICH-PROD-03 |
| Traditional Lacquerwork | CMA, Met | Lacquer object and process illustration | ICH-PROD-01 |
| Shipbuilding (Nordic/Pacific) | NHM, SMK | Maritime craft illustration | ICH-PROD-04 |

### 8.3 Institution Gaps for ICH (Not Yet Onboarded)

| Gap | Content needed | Target institution |
|---|---|---|
| African ICH (West/Central Africa) | Griots, court music, royal regalia illustration | Smithsonian NMAFA; British Museum (rights complex) |
| South Asian performing arts | Indian classical dance, shadow puppetry | Wellcome Collection (Must Add); V&A (Should Add) |
| Latin American indigenous ICH | Andean ceremony, Amazonian traditional knowledge | MNHN Paris (Should Add) |
| Indigenous Australian ICH | Songlines, traditional land management | Trove / NLA (Must Add) |

---

## Part IX: Node Scale Addendum (extends NC-GRAPH-002 Appendix A)

| Node label | PostgreSQL source | 100 places (est.) | 1,000 places (est.) |
|---|---|---|---|
| HeritagePractice | nc_heritage_practices | 200–500 | 1,500–3,000 |
| HeritageDesignation | nc_heritage_designations | 150–300 | 400–800 |
| (existing nodes unchanged) | | | |
| **ICH layer additions** | | **+350–800** | **+1,900–3,800** |

New relationships added per 100 places (estimates):
- HAS_DESIGNATION: 200–400 (avg 2–4 designations per place)
- PRACTICED_AT: 300–600 (avg 3–6 practices per active place)
- DOCUMENTED_BY: 600–1,500 (avg 3–4 illustrations per practice)
- CO_PRACTICED_WITH (derived): 100–300
- USES_TAXON: 200–500 (NK domain practices)

---

## Part X: Implementation Sequence

### Sprint ICH-1: Schema and authority (prerequisite: NC-GRAPH-002 Sprint 2)
1. Ratify this document
2. Run PostgreSQL migrations: 5 new tables + trigger
3. Add `designation_stack_height` computed column to `nc_places`
4. Register `HeritagePractice` and `HeritageDesignation` in `nc_projection_schema_registry`
5. Seed Tier 0 pilot place designations (Yellowstone UNESCO WH, Grand Canyon UNESCO WH,
   Great Barrier Reef UNESCO WH + Ramsar, Papahānaumokuākea, Venice UNESCO WH)
6. Seed 10 high-priority ICH practices with confirmed PD documentation

### Sprint ICH-2: Graph projection
1. Build projection worker for `nc_heritage_practices` → `HeritagePractice` nodes
2. Build projection worker for `nc_heritage_designations` → `HeritageDesignation` nodes
3. Build `nc_place_designations` → `HAS_DESIGNATION` edge projection
4. Build `nc_practice_place_anchors` → `PRACTICED_AT` edge projection
5. Build `nc_practice_illustrations` → `DOCUMENTED_BY` + `DOCUMENTS_PRACTICE` edge projection
6. Implement `CO_PRACTICED_WITH` derived relationship computation

### Sprint ICH-3: Discovery and commerce
1. Implement Journeys ICH-1 through ICH-3 in graph API
2. Apply ICH-2 gate to product activation pipeline
3. Activate first 5 ICH illustration products (falconry, silk weaving, Pacific navigation,
   Walters calligraphy, NHM ethnobotanical)
4. Build DESIGNATION_BUNDLE and PLACE_HERITAGE_PACK collection types
5. Implement designation stack display on Place page

### Sprint ICH-4: Full domain coverage
1. Implement Journeys ICH-4 through ICH-6
2. Build DOMAIN_COLLECTION and HERITAGE_EXPEDITION collection types
3. Onboard Trove (NLA) → unlocks Australian ICH documentation
4. Mixed WH site discovery collection (Journey ICH-5)
5. Heritage Density leaderboard (Journey ICH-6)

---

## Appendix: Designation Type Reference

| Code | Full name | Governing body | Count (approx) | Notes |
|---|---|---|---|---|
| UNESCO_WH_Natural | World Heritage — Natural | UNESCO WHC | ~220 sites | IUCN criteria vii–x |
| UNESCO_WH_Cultural | World Heritage — Cultural | UNESCO WHC | ~900 sites | ICOMOS criteria i–vi |
| UNESCO_WH_Mixed | World Heritage — Mixed | UNESCO WHC | ~40 sites | Both criteria sets |
| UNESCO_ICH_Representative | ICH Representative List | UNESCO | ~600 elements | 2003 Convention |
| UNESCO_ICH_Urgent | ICH Urgent Safeguarding | UNESCO | ~70 elements | At-risk practices |
| UNESCO_Biosphere | Biosphere Reserve | UNESCO MAB | ~730 reserves | Conservation-development |
| UNESCO_Geopark | Global Geopark | UNESCO | ~200 parks | Geological heritage |
| Ramsar | Wetland of International Importance | Ramsar Secretariat | ~2,400 sites | 1971 Convention |
| DarkSky_IDA | International Dark Sky Place | IDA | ~200 designations | Light pollution |
| IUCN_II | National Park | IUCN | ~6,500 areas | Protected landscape |

---

*NC-ICH-001 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
