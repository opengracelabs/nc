# NC-GRAPH-002: Neo4j Implementation Blueprint

| Field | Value |
|---|---|
| Document | NC-GRAPH-002 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-13 |
| Authority | NC-GRAPH-IMPLEMENTATION-001 · neo4j_pgvector_runtime_architecture_v1 · NC-AI-001 · Strategic Direction v1 |
| Stack | PostgreSQL · PostGIS · Neo4j · Grounded AI |
| Scale targets | 100 places (immediate) · 1,000 places (next) |
| **Decision** | **APPROVED** |

---

## Decision Record

Neo4j is approved as the discovery graph layer for Nature & Culture. This document is the
implementation blueprint. It does not re-evaluate the decision.

PostgreSQL and PostGIS remain the canonical authority for all entity state, rights, spatial geometry,
and commerce. Neo4j is a projection layer: read-only, derived from PostgreSQL, full-rebuild capable.

**Governing invariants (unconditional):**

| Code | Invariant |
|---|---|
| G-1 | No application writes directly to Neo4j. All writes flow through the PostgreSQL → Neo4j projection pipeline. |
| G-2 | Every Neo4j node carries `pg_id`, `pg_table`, `schema_version`, `projection_run_id`, `projected_at`. |
| G-3 | Every Neo4j relationship carries `derivation` (direct/derived), `pg_source`, `pg_source_id`, `schema_version`, `projection_run_id`. |
| G-4 | Rights retraction in PostgreSQL propagates to Neo4j node removal within 15 minutes (priority queue). |
| G-5 | Commerce scoring does not consume Neo4j signals. FM-4 is unconditionally permanent. |
| G-6 | Grounded AI reads from the graph. It does not write to the graph or to PostgreSQL canonical tables. |
| G-7 | Full rebuild from PostgreSQL is always the recovery path. No graph state is irreplaceable. |
| G-8 | New node labels and relationship types require a new `projection_schema_registry` entry before activation. |

---

## Part I: Reference Model Synthesis

Each reference model contributes a specific architectural pattern. The synthesis defines what NC builds.

### 1.1 Google Arts & Culture → Object-to-Object Traversal

**Contribution:** Any object opens a network of connected objects. The central discovery gesture is
traversal, not search. Color, period, movement, subject, and institution are all graph dimensions.

**NC adoption:**
- Every `Illustration` node is a traversal hub, not a leaf record
- `DEPICTS`, `CREATED_BY`, `PART_OF_MOVEMENT`, `CREATED_IN` make every illustration reachable from
  multiple entry dimensions
- The "stories" pattern: `Story` nodes thread multiple objects into editorial paths

**What NC does not adopt:** Color palette similarity (visual feature vectors, not graph structure).
That belongs to pgvector when activated.

---

### 1.2 Google Knowledge Graph → Entity Identity and Confidence

**Contribution:** Every entity has stable IDs, typed relationships, and fact provenance. The knowledge
panel (entity summary + relationships) is the canonical display format. Confidence scores on facts.
Entity disambiguation — the same name resolves to the correct entity.

**NC adoption:**
- Stable `place_id`, `illustration_id`, `artist_id` UUIDs as Neo4j unique constraints
- `SAME_AS` relationships to Wikidata QIDs and GeoNames IDs — the disambiguation layer
- Fact provenance on every relationship: `pg_source`, `pg_source_id`
- The "knowledge panel" pattern: single Cypher query returns entity + immediate relationships for
  display, grounded AI assembly, and attribution rendering
- `confidence: FLOAT` property on derived relationships (CONTEMPORARY_WITH, PROXIMATE_TO)

**What NC does not adopt:** Open-edit authority. Google KG allows web crawl to modify entity facts.
NC graph is read-only; PostgreSQL is the sole write path.

---

### 1.3 Airbnb → Spatial Graph Edges

**Contribution:** Geographic proximity is a first-class relationship in the graph, not a query-time
calculation. Neighborhood containment, distance ranking, and "experiences near here" are all
graph-traversable. The map is the primary discovery interface.

**NC adoption:**
- `PROXIMATE_TO` relationships between places (PostGIS-derived, ≤600km, stored as graph edges)
- `WITHIN_BIOREGION` containment edges (PostGIS polygon containment, stored)
- `distance_km: FLOAT` on PROXIMATE_TO allows ordering without PostGIS round-trip in graph queries
- `Bioregion` nodes enable "all places in the Indo-Pacific" as a graph traversal

**What NC does not adopt:** User listing behavior (Airbnb's core graph is host-guest-listing
behavioral data). NC has no equivalent until session behavior is captured.

---

### 1.4 Spotify → Taste Graph and Explainable Recommendation

**Contribution:** Recommendations are explainable paths through the graph, not opaque scores.
"Artist radio" is graph traversal through influence and co-listen edges. "Fans also like" is a
second-degree traversal (user → tracks → other users → other tracks). Playlist is the collection
analog.

**NC adoption:**
- `INFLUENCED_BY` between artists (editorial, explicit source)
- `CONTEMPORARY_WITH` as derived influence proxy before explicit influence data exists
- Recommendation reasons are graph paths, not scores: "Both created by Audubon" = shared
  CREATED_BY edge
- Collection as playlist: `IN_COLLECTION` ordering + `ANCHORED_AT` place create a traversable
  collection graph

**What NC does not adopt:** Collaborative filtering until session behavior graph exists. The
behavior graph (User → Viewed/Saved/Purchased → Illustration) is a Phase 3 graph extension, not
part of this blueprint.

---

### 1.5 National Geographic → Place as Story Hub

**Contribution:** Every place is a story with a cast (species, explorers, events), a setting
(geography, climate, ecosystem), and a present-day stakes (conservation status). The expedition is
a narrative structure that connects people, places, and time. NatGeo's "grid" = editorial paths
that are pre-curated traversals of the knowledge graph.

**NC adoption:**
- `Expedition` as a first-class node connecting `Artist` → `Place` → `Taxon` → `Illustration`
- `Story` nodes as pre-curated traversal paths through the graph
- `Topic` nodes as thematic bridges (Wildlife, Exploration, Marine, Botanical, Conservation)
- `PASSED_THROUGH` on expeditions models the narrative journey through places

**What NC does not adopt:** Real-time news or event data. NC's temporal scope is primarily 1750–1900
golden age content.

---

### 1.6 Smithsonian → Cross-Discipline Bridges

**Contribution:** 19 museums connected by shared topics, themes, and historical figures. An object
in American History connects to a specimen in Natural History connects to a painting in American Art.
The bridge is a topic or person node, not a direct relationship between objects.

**NC adoption:**
- `Topic` as the cross-discipline bridge: Yellowstone → Topic:Geothermal → Illustration:Haeckel
- `Taxon` as the natural history bridge: Illustration:Audubon → Taxon:GBH → Place:Everglades
- Multi-hop Cypher patterns that traverse these bridges to generate discovery panels

**What NC does not adopt:** Archive/document relationships (Smithsonian's archives layer). NC's
scope is illustration commerce, not general archive discovery.

---

### 1.7 Rijksmuseum → Maker and Provenance Depth

**Contribution:** Every object's full provenance chain is traversable: maker → workshop → movement →
period → patron → current institution. Iconclass subject taxonomy (14 levels deep) enables subject
traversal at depth. Material and technique as graph dimensions.

**NC adoption:**
- `Movement` nodes (Hudson River School, Golden Age Natural History, Romantic Naturalism)
- `PART_OF_MOVEMENT` connects artists and illustrations to movements
- Artist contemporaries as a graph query (`CONTEMPORARY_WITH`)
- Provenance: `SOURCED_FROM` connects illustration to institution with rights metadata

**What NC does not adopt:** 14-level iconographic taxonomy. NC uses a flat-to-3-level subject tag
vocabulary. Rijksmuseum iconographic depth is appropriate for a research institution; NC's scope is
discovery commerce.

---

### 1.8 Synthesis: Seven Design Principles

| Principle | Source | Graph expression |
|---|---|---|
| Every entity is a traversal hub | GAC | Minimum 3 relationship types per node |
| Stable identity with external anchors | Google KG | SAME_AS edges to Wikidata/GeoNames |
| Proximity is a relationship, not a query | Airbnb | PROXIMATE_TO stored edges |
| Recommendations are explainable paths | Spotify | Reason codes = shared graph paths |
| Place is a story hub | NatGeo | Place connects Expedition + Artist + Taxon + Story |
| Topics bridge disciplines | Smithsonian | Topic as a cross-entity connector node |
| Provenance depth is commerce-relevant | Rijksmuseum | Full CREATED_BY + SOURCED_FROM chain |

---

## Part II: Node Model

### 2.1 Schema Constraints and Indexes

```cypher
// ── CONSTRAINTS ───────────────────────────────────────────────────────────

CREATE CONSTRAINT place_id      FOR (n:Place)      REQUIRE n.place_id IS UNIQUE;
CREATE CONSTRAINT place_geo     FOR (n:Place)      REQUIRE n.geonames_id IS UNIQUE;
CREATE CONSTRAINT illus_id      FOR (n:Illustration) REQUIRE n.illustration_id IS UNIQUE;
CREATE CONSTRAINT illus_asset   FOR (n:Illustration) REQUIRE n.nc_asset_id IS UNIQUE;
CREATE CONSTRAINT artist_id     FOR (n:Artist)     REQUIRE n.artist_id IS UNIQUE;
CREATE CONSTRAINT taxon_id      FOR (n:Taxon)      REQUIRE n.taxon_id IS UNIQUE;
CREATE CONSTRAINT taxon_gbif    FOR (n:Taxon)      REQUIRE n.gbif_taxon_key IS UNIQUE;
CREATE CONSTRAINT inst_id       FOR (n:Institution) REQUIRE n.institution_id IS UNIQUE;
CREATE CONSTRAINT inst_slug     FOR (n:Institution) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT coll_id       FOR (n:Collection) REQUIRE n.collection_id IS UNIQUE;
CREATE CONSTRAINT coll_slug     FOR (n:Collection) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT story_id      FOR (n:Story)      REQUIRE n.story_id IS UNIQUE;
CREATE CONSTRAINT expd_id       FOR (n:Expedition) REQUIRE n.expedition_id IS UNIQUE;
CREATE CONSTRAINT expd_slug     FOR (n:Expedition) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT mvmt_id       FOR (n:Movement)   REQUIRE n.movement_id IS UNIQUE;
CREATE CONSTRAINT topic_id      FOR (n:Topic)      REQUIRE n.topic_id IS UNIQUE;
CREATE CONSTRAINT topic_slug    FOR (n:Topic)      REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT period_id     FOR (n:Period)     REQUIRE n.period_id IS UNIQUE;
CREATE CONSTRAINT bio_id        FOR (n:Bioregion)  REQUIRE n.bioregion_id IS UNIQUE;
CREATE CONSTRAINT prod_id       FOR (n:Product)    REQUIRE n.product_id IS UNIQUE;
CREATE CONSTRAINT prod_nc_id    FOR (n:Product)    REQUIRE n.nc_product_id IS UNIQUE;

// ── INDEXES ───────────────────────────────────────────────────────────────

CREATE INDEX place_name         FOR (n:Place)        ON (n.name);
CREATE INDEX place_fcode        FOR (n:Place)        ON (n.fcode);
CREATE INDEX place_country      FOR (n:Place)        ON (n.country_code);
CREATE INDEX illus_year         FOR (n:Illustration) ON (n.year);
CREATE INDEX illus_rights       FOR (n:Illustration) ON (n.rights);
CREATE INDEX illus_safe         FOR (n:Illustration) ON (n.product_safe);
CREATE INDEX illus_inst         FOR (n:Illustration) ON (n.institution_slug);
CREATE INDEX artist_name        FOR (n:Artist)       ON (n.name);
CREATE INDEX artist_priority    FOR (n:Artist)       ON (n.nc_priority);
CREATE INDEX artist_active      FOR (n:Artist)       ON (n.active_start, n.active_end);
CREATE INDEX taxon_sci          FOR (n:Taxon)        ON (n.scientific_name);
CREATE INDEX taxon_common       FOR (n:Taxon)        ON (n.common_name);
CREATE INDEX taxon_kingdom      FOR (n:Taxon)        ON (n.kingdom);
CREATE INDEX coll_status        FOR (n:Collection)   ON (n.status);
CREATE INDEX prod_line          FOR (n:Product)      ON (n.product_line);
CREATE INDEX prod_status        FOR (n:Product)      ON (n.status);
CREATE INDEX topic_domain       FOR (n:Topic)        ON (n.domain);
```

---

### 2.2 Node Definitions

All nodes carry the projection provenance block. Abbreviated here as `...provenance`:

```
pg_id: STRING           // PostgreSQL primary key UUID
pg_table: STRING        // PostgreSQL source table
schema_version: STRING  // Projection schema version
projection_run_id: STRING
projected_at: DATETIME
```

---

#### Place

```cypher
(:Place {
  // Identity
  place_id:         STRING,   // UUID, PostgreSQL pk
  geonames_id:      INTEGER,  // canonical spatial authority (NC-DATA-001/002/004)
  wikidata_qid:     STRING,   // identity authority (DD-WIKIDATA-001)
  name:             STRING,
  canonical_name:   STRING,

  // Geography
  fcode:            STRING,   // GeoNames feature code: PRKA, RF, MT, ISL, LK, OCN
  country_code:     STRING,
  admin1_code:      STRING,
  centroid_lat:     FLOAT,    // derived from PostGIS — display only, not authority
  centroid_lng:     FLOAT,
  area_km2:         FLOAT,

  // Classification
  place_type:       STRING,   // 'national_park' | 'reef' | 'mountain' | 'island' | 'river'
  established_year: INTEGER,
  heritage_type:    STRING,   // 'natural' | 'cultural' | 'mixed' | null

  // Discovery signals
  illustration_count: INTEGER, // denormalized from projection for fast card rendering
  collection_count:   INTEGER,
  artist_count:       INTEGER,
  is_pilot:         BOOLEAN,

  ...provenance
})
```

---

#### Illustration

```cypher
(:Illustration {
  // Identity
  illustration_id:  STRING,   // UUID
  nc_asset_id:      STRING,   // NC-ASSET-001 etc.
  title:            STRING,

  // Temporal
  year:             INTEGER,
  year_circa:       BOOLEAN,
  period_label:     STRING,   // denormalized: 'Golden Age Natural History 1750-1900'

  // Rights — display only; PostgreSQL is authoritative gate
  rights:           STRING,   // CC0 | PDM | NoC-US
  institution_slug: STRING,

  // Commerce signals — advisory; product activation gate is PostgreSQL
  product_safe:     BOOLEAN,
  resolution_mp:    FLOAT,
  has_active_product: BOOLEAN,

  // Visual
  color_primary:    STRING,   // dominant hex
  color_palette:    LIST,     // top 5 hex colors

  // AI assembly hints
  ai_description:   STRING,   // grounded AI generated, approved
  ai_description_run_id: STRING,  // generation run for audit

  ...provenance
})
```

---

#### Artist

```cypher
(:Artist {
  // Identity
  artist_id:        STRING,
  wikidata_qid:     STRING,
  name:             STRING,
  name_variants:    LIST,     // aliases, married names, transliterations

  // Temporal
  birth_year:       INTEGER,
  death_year:       INTEGER,
  active_start:     INTEGER,
  active_end:       INTEGER,
  nationality:      STRING,
  birth_country:    STRING,

  // NC priority classification (Illustration Opportunity Doctrine)
  nc_priority:      BOOLEAN,  // Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel, Wolf
  priority_rank:    INTEGER,  // 1–8 for priority illustrators

  // Discovery signals
  illustration_count: INTEGER,
  place_count:        INTEGER,

  ...provenance
})
```

---

#### Taxon

```cypher
(:Taxon {
  // Identity
  taxon_id:         STRING,
  gbif_taxon_key:   INTEGER,  // GBIF biological anchor — evidence layer
  wikidata_qid:     STRING,
  scientific_name:  STRING,
  common_name:      STRING,

  // Taxonomy
  rank:             STRING,   // species | genus | family | order | class | phylum
  kingdom:          STRING,
  phylum:           STRING,
  class:            STRING,
  order:            STRING,
  family:           STRING,
  genus:            STRING,

  // Conservation — editorial signal, never a commerce gate (FM-4)
  iucn_status:      STRING,   // LC | NT | VU | EN | CR | EW | EX | null
  iucn_year:        INTEGER,

  // Discovery signals
  illustration_count: INTEGER,
  place_count:        INTEGER,

  ...provenance
})
```

---

#### Institution

```cypher
(:Institution {
  institution_id:   STRING,
  slug:             STRING,   // 'nasa' | 'smithsonian' | 'met' | 'nhm' | 'mia' etc.
  name:             STRING,
  wikidata_qid:     STRING,
  country_code:     STRING,

  // Adapter characteristics (from institution factory)
  adapter_class:    STRING,   // 'boolean' | 'csv' | 'linked_art' | 'ckan' | 'activity_streams'
  rights_matrix:    STRING,   // rights matrix version slug
  source_role:      STRING,   // 'content' | 'identity' | 'evidence' | 'validation_only'
  iiif_version:     STRING,   // '2' | '3' | null

  // Discovery signals
  illustration_count: INTEGER,

  ...provenance
})
```

---

#### Collection

```cypher
(:Collection {
  collection_id:    STRING,
  slug:             STRING,   // 'earthrise' | 'darwin-finches'
  name:             STRING,
  subtitle:         STRING,

  // Anchor
  anchor_place_id:  STRING,   // FK to Place.place_id

  // Status
  status:           STRING,   // 'live' | 'coming_soon' | 'reserved' | 'deferred'
  launch_phase:     INTEGER,

  // Commerce
  illustration_count: INTEGER,
  product_count:    INTEGER,
  price_from_usd:   FLOAT,

  // AI assembly
  ai_synopsis:      STRING,   // grounded AI generated, approved
  ai_synopsis_run_id: STRING,

  ...provenance
})
```

---

#### Story

```cypher
(:Story {
  story_id:         STRING,
  slug:             STRING,
  title:            STRING,
  dek:              STRING,   // editorial subtitle

  // Publication
  status:           STRING,   // 'published' | 'draft' | 'archived'
  published_at:     DATETIME,

  // Discovery signals
  anchor_place_id:  STRING,
  anchor_collection_id: STRING,
  word_count:       INTEGER,

  ...provenance
})
```

---

#### Expedition

```cypher
(:Expedition {
  expedition_id:    STRING,
  slug:             STRING,   // 'hayden-survey-1871' | 'hms-beagle' | 'cook-voyage-1'
  name:             STRING,

  // Temporal
  start_year:       INTEGER,
  end_year:         INTEGER,

  // Personnel
  lead_naturalist:  STRING,
  vessel_name:      STRING,
  sponsor:          STRING,   // 'USGS' | 'Royal Navy' | 'Linnean Society'

  // Derived geometry hint (authority is PostGIS)
  route_summary:    STRING,   // 'Pacific → New Zealand → Australia → Indonesia'

  // Discovery signals
  place_count:      INTEGER,
  artist_count:     INTEGER,
  illustration_count: INTEGER,

  ...provenance
})
```

---

#### Movement

```cypher
(:Movement {
  movement_id:      STRING,
  slug:             STRING,
  name:             STRING,

  // Temporal
  start_year:       INTEGER,
  end_year:         INTEGER,
  origin_country:   STRING,

  // Classification
  discipline:       STRING,   // 'painting' | 'natural_history' | 'photography'
  description:      STRING,

  ...provenance
})
```

---

#### Topic

```cypher
(:Topic {
  topic_id:         STRING,
  slug:             STRING,   // 'geothermal' | 'coral-reef' | 'bird-migration'
  name:             STRING,
  domain:           STRING,   // 'wildlife' | 'exploration' | 'marine' | 'botanical' | 'conservation' | 'geology'
  description:      STRING,

  ...provenance
})
```

---

#### Period

```cypher
(:Period {
  period_id:        STRING,
  name:             STRING,   // 'Golden Age Natural History' | 'Victorian Era'
  start_year:       INTEGER,
  end_year:         INTEGER,
  description:      STRING,

  ...provenance
})
```

---

#### Bioregion

```cypher
(:Bioregion {
  bioregion_id:     STRING,
  name:             STRING,   // 'Indo-Pacific' | 'Rocky Mountain West'
  region_type:      STRING,   // 'marine' | 'terrestrial' | 'freshwater'
  description:      STRING,
  place_count:      INTEGER,

  ...provenance
})
```

---

#### Product

```cypher
(:Product {
  product_id:       STRING,
  nc_product_id:    STRING,   // 'NC-PROD-001'
  name:             STRING,
  product_line:     INTEGER,  // 1–20 per NC-PRODUCT-001
  status:           STRING,   // 'active' | 'deferred' | 'reserved'
  price_usd:        FLOAT,
  shopify_variant_id: STRING,

  ...provenance
})
```

---

## Part III: Relationship Model

### 3.1 Direct Relationships (derived from PostgreSQL FK)

```cypher
// ── ILLUSTRATION RELATIONSHIPS ────────────────────────────────────────────

(i:Illustration)-[:CREATED_BY {
  year: INTEGER,                  // creation year (may differ from illustration.year)
  confirmed: BOOLEAN,             // false if attributed/workshop
  attribution_note: STRING,       // 'workshop of' | 'after' | 'attributed to'
  derivation: 'direct',
  pg_source: 'illustration_artist',
  ...relationship_provenance
}]->(a:Artist)

(i:Illustration)-[:DEPICTS {
  primary: BOOLEAN,               // true if the main depicted subject
  confidence: FLOAT,              // 0.0–1.0; 1.0 = explicit metadata
  derivation: 'direct',
  pg_source: 'illustration_taxon',
  ...relationship_provenance
}]->(t:Taxon)

(i:Illustration)-[:ASSOCIATED_WITH {
  evidence_type: STRING,          // 'created_at' | 'depicts_place' | 'expedition_stop'
  year: INTEGER,
  derivation: 'direct',
  pg_source: 'illustration_place',
  ...relationship_provenance
}]->(p:Place)

(i:Illustration)-[:SOURCED_FROM {
  asset_id: STRING,               // institution-side asset identifier
  rights: STRING,                 // CC0 | PDM | NoC-US
  rights_matrix_version: STRING,
  derivation: 'direct',
  pg_source: 'source_item',
  ...relationship_provenance
}]->(inst:Institution)

(i:Illustration)-[:IN_COLLECTION {
  display_order: INTEGER,
  added_at: DATETIME,
  derivation: 'direct',
  pg_source: 'collection_item',
  ...relationship_provenance
}]->(c:Collection)

(i:Illustration)-[:CREATED_IN {
  derivation: 'direct',
  pg_source: 'illustration_period',
  ...relationship_provenance
}]->(per:Period)

(i:Illustration)-[:PART_OF_EXPEDITION {
  year: INTEGER,
  stop_sequence: INTEGER,         // order within expedition
  derivation: 'direct',
  pg_source: 'illustration_expedition',
  ...relationship_provenance
}]->(e:Expedition)

(i:Illustration)-[:HAS_TOPIC {
  relevance: FLOAT,               // 0.0–1.0
  derivation: 'direct',
  pg_source: 'illustration_topic',
  ...relationship_provenance
}]->(top:Topic)

(prod:Product)-[:DERIVED_FROM {
  derivation: 'direct',
  pg_source: 'product_illustration',
  ...relationship_provenance
}]->(i:Illustration)

// ── ARTIST RELATIONSHIPS ──────────────────────────────────────────────────

(a:Artist)-[:VISITED {
  year: INTEGER,
  expedition_id: STRING,          // null if independent visit
  derivation: 'direct',
  pg_source: 'artist_place',
  ...relationship_provenance
}]->(p:Place)

(a:Artist)-[:PART_OF_EXPEDITION {
  role: STRING,                   // 'lead_artist' | 'staff_artist' | 'naturalist'
  derivation: 'direct',
  pg_source: 'artist_expedition',
  ...relationship_provenance
}]->(e:Expedition)

(a:Artist)-[:ACTIVE_IN {
  derivation: 'direct',
  pg_source: 'artist_period',
  ...relationship_provenance
}]->(per:Period)

(a:Artist)-[:PART_OF_MOVEMENT {
  year_joined: INTEGER,
  derivation: 'direct',
  pg_source: 'artist_movement',
  ...relationship_provenance
}]->(m:Movement)

(a:Artist)-[:INFLUENCED_BY {
  influence_type: STRING,         // 'mentor' | 'contemporary' | 'predecessor'
  source: STRING,                 // citation for the influence claim
  derivation: 'direct',
  pg_source: 'artist_influence',
  ...relationship_provenance
}]->(a2:Artist)

// ── TAXON RELATIONSHIPS ───────────────────────────────────────────────────

(t:Taxon)-[:OCCURS_AT {
  occurrence_count: INTEGER,
  gbif_confirmed: BOOLEAN,
  last_synced_at: DATETIME,
  derivation: 'direct',
  pg_source: 'taxon_place',
  ...relationship_provenance
}]->(p:Place)

(t:Taxon)-[:CHILD_OF {
  rank_step: STRING,              // 'species_to_genus' | 'genus_to_family'
  derivation: 'direct',
  pg_source: 'taxon_hierarchy',
  ...relationship_provenance
}]->(t2:Taxon)

(t:Taxon)-[:HAS_TOPIC {
  derivation: 'direct',
  pg_source: 'taxon_topic',
  ...relationship_provenance
}]->(top:Topic)

// ── PLACE RELATIONSHIPS ───────────────────────────────────────────────────

(p:Place)-[:LOCATED_IN {
  hierarchy_type: STRING,         // 'country' | 'region' | 'continent'
  derivation: 'direct',
  pg_source: 'place_hierarchy',
  ...relationship_provenance
}]->(p2:Place)

(p:Place)-[:HAS_TOPIC {
  derivation: 'direct',
  pg_source: 'place_topic',
  ...relationship_provenance
}]->(top:Topic)

// ── COLLECTION AND STORY RELATIONSHIPS ───────────────────────────────────

(c:Collection)-[:ANCHORED_AT {
  derivation: 'direct',
  pg_source: 'collection',
  ...relationship_provenance
}]->(p:Place)

(c:Collection)-[:FEATURES_ARTIST {
  derivation: 'direct',
  pg_source: 'collection_artist',
  ...relationship_provenance
}]->(a:Artist)

(s:Story)-[:FEATURES_PLACE {
  section: STRING,
  derivation: 'direct',
  pg_source: 'story_place',
  ...relationship_provenance
}]->(p:Place)

(s:Story)-[:FEATURES_ILLUSTRATION {
  display_order: INTEGER,
  derivation: 'direct',
  pg_source: 'story_illustration',
  ...relationship_provenance
}]->(i:Illustration)

(s:Story)-[:PART_OF_COLLECTION {
  derivation: 'direct',
  pg_source: 'story_collection',
  ...relationship_provenance
}]->(c:Collection)

// ── EXPEDITION RELATIONSHIPS ──────────────────────────────────────────────

(e:Expedition)-[:PASSED_THROUGH {
  year: INTEGER,
  stop_sequence: INTEGER,
  days_at_location: INTEGER,
  derivation: 'direct',
  pg_source: 'expedition_place',
  ...relationship_provenance
}]->(p:Place)

// ── EXTERNAL IDENTITY (Google KG pattern) ─────────────────────────────────

(p:Place)-[:SAME_AS {
  authority: STRING,              // 'wikidata' | 'geonames'
  external_id: STRING,
  derivation: 'direct',
  pg_source: 'place',
  ...relationship_provenance
}]->(external_entity)

(a:Artist)-[:SAME_AS {
  authority: STRING,              // 'wikidata' | 'loc' | 'viaf'
  external_id: STRING,
  derivation: 'direct',
  pg_source: 'artist',
  ...relationship_provenance
}]->(external_entity)
```

---

### 3.2 Derived Relationships (computed from PostgreSQL + PostGIS rules)

```cypher
// ── PLACE PROXIMITY (PostGIS-derived, stored for graph traversal) ──────────

(p1:Place)-[:PROXIMATE_TO {
  distance_km: FLOAT,
  spatial_relationship: STRING,  // 'adjacent' | 'same_bioregion' | 'same_country'
  derivation: 'derived',
  derivation_rule: 'postgis_st_dwithin_600km',
  confidence: FLOAT,             // 1.0 for all stored (threshold-filtered)
  pg_source: 'nc_places',
  ...relationship_provenance
}]->(p2:Place)

// ── BIOREGION CONTAINMENT (PostGIS ST_Within) ─────────────────────────────

(p:Place)-[:WITHIN_BIOREGION {
  derivation: 'derived',
  derivation_rule: 'postgis_st_within',
  pg_source: 'nc_bioregions',
  ...relationship_provenance
}]->(b:Bioregion)

// ── ARTIST CONTEMPORARIES (active year overlap) ───────────────────────────

(a1:Artist)-[:CONTEMPORARY_WITH {
  overlap_years: INTEGER,        // years of overlapping active periods
  overlap_start: INTEGER,
  overlap_end: INTEGER,
  derivation: 'derived',
  derivation_rule: 'active_year_overlap_lte_30',
  confidence: FLOAT,             // 1.0 if overlap ≥ 10 yr; 0.7 if 1–9 yr
  pg_source: 'nc_artists',
  ...relationship_provenance
}]->(a2:Artist)

// ── TAXON CO-OCCURRENCE (same place occurrence) ───────────────────────────

(t1:Taxon)-[:CO_OCCURS_WITH {
  shared_place_count: INTEGER,   // number of shared places
  representative_place_id: STRING,
  derivation: 'derived',
  derivation_rule: 'shared_taxon_place_occurrence',
  pg_source: 'nc_taxon_place',
  ...relationship_provenance
}]->(t2:Taxon)

// ── EXPEDITION ROUTE INTERSECTION (PostGIS ST_Intersects) ─────────────────

(e:Expedition)-[:ROUTE_PASSES_NEAR {
  closest_point_km: FLOAT,
  derivation: 'derived',
  derivation_rule: 'postgis_st_dwithin_route_100km',
  pg_source: 'nc_expeditions',
  ...relationship_provenance
}]->(p:Place)
```

---

## Part IV: Discovery Journeys

All queries return canonical `pg_id` values for API rehydration from PostgreSQL.
The `WHERE n.product_safe = true AND n.rights IN ['CC0','PDM','NoC-US']` guard must be on every
illustration result. Rights authority is PostgreSQL — graph visibility flags are advisory.

---

### 4.1 Journey 1: Place → Discovery Grid

*Entry point: place detail page. Returns illustration grid.*

```cypher
// Primary: Place → Taxa → Illustrations
MATCH (p:Place {place_id: $place_id})
      <-[:OCCURS_AT]-(t:Taxon)
      <-[:DEPICTS]-(i:Illustration)
WHERE i.product_safe = true
  AND i.rights IN ['CC0', 'PDM', 'NoC-US']
WITH i, t, count(t) AS subject_count
RETURN i.illustration_id,
       i.nc_asset_id,
       i.title,
       i.year,
       i.rights,
       i.color_primary,
       i.has_active_product,
       collect(DISTINCT t.common_name)[0..3] AS subjects,
       subject_count
ORDER BY i.has_active_product DESC, i.year DESC
LIMIT 12

// Secondary: Place → Direct association (expedition illustrations, landmark views)
MATCH (p:Place {place_id: $place_id})<-[:ASSOCIATED_WITH]-(i:Illustration)
WHERE i.product_safe = true
  AND i.rights IN ['CC0', 'PDM', 'NoC-US']
  AND NOT EXISTS {
    MATCH (p)<-[:OCCURS_AT]-(t:Taxon)<-[:DEPICTS]-(i)  // exclude already shown
  }
RETURN i.illustration_id, i.title, i.year, 'direct_association' AS source
LIMIT 6
```

---

### 4.2 Journey 2: Illustration → Connected Illustrations

*Entry point: illustration detail page. Returns the "explore more" panels.*

```cypher
// Panel A: By the same artist
MATCH (i:Illustration {illustration_id: $illus_id})-[:CREATED_BY]->(a:Artist)
      <-[:CREATED_BY]-(i2:Illustration)
WHERE i2.illustration_id <> $illus_id
  AND i2.product_safe = true
RETURN i2.illustration_id, i2.title, i2.year,
       a.name AS artist_name,
       'same_artist' AS reason_code,
       'By ' + a.name AS reason_text
ORDER BY i2.has_active_product DESC, i2.year DESC
LIMIT 4

// Panel B: Same subjects at different places
MATCH (i:Illustration {illustration_id: $illus_id})-[:DEPICTS]->(t:Taxon)
      <-[:DEPICTS]-(i2:Illustration)-[:ASSOCIATED_WITH]->(p2:Place)
WHERE i2.illustration_id <> $illus_id
  AND i2.product_safe = true
WITH i2, t, p2
RETURN i2.illustration_id, i2.title, i2.year,
       t.common_name AS shared_subject,
       p2.name AS other_place,
       'same_subject_other_place' AS reason_code,
       t.common_name + ' also depicted at ' + p2.name AS reason_text
LIMIT 4

// Panel C: Same place, other artists
MATCH (i:Illustration {illustration_id: $illus_id})-[:ASSOCIATED_WITH]->(p:Place)
      <-[:ASSOCIATED_WITH]-(i2:Illustration)
WHERE i2.illustration_id <> $illus_id
  AND i2.product_safe = true
MATCH (i2)-[:CREATED_BY]->(a2:Artist)
WHERE NOT EXISTS {
  MATCH (i)-[:CREATED_BY]->(a2)  // different artist
}
RETURN i2.illustration_id, i2.title, i2.year,
       a2.name AS other_artist,
       p.name AS shared_place,
       'same_place_other_artist' AS reason_code,
       'Also from ' + p.name AS reason_text
LIMIT 4
```

---

### 4.3 Journey 3: Artist Radio (Spotify model)

*Entry point: artist profile or "explore this artist's world".*

```cypher
// Step 1: Artist's places → other artists who visited those places
MATCH (a:Artist {artist_id: $artist_id})-[:VISITED]->(p:Place)<-[:VISITED]-(a2:Artist)
WHERE a2.artist_id <> $artist_id
  AND a2.nc_priority = true    // prioritize golden age illustrators
WITH a2, collect(DISTINCT p.name) AS shared_places, count(DISTINCT p) AS place_overlap
RETURN a2.artist_id, a2.name, shared_places, place_overlap,
       'shared_expedition_territory' AS reason_code
ORDER BY place_overlap DESC, a2.priority_rank ASC
LIMIT 6

// Step 2: Artist's movement → other artists in same movement
MATCH (a:Artist {artist_id: $artist_id})-[:PART_OF_MOVEMENT]->(m:Movement)
      <-[:PART_OF_MOVEMENT]-(a2:Artist)
WHERE a2.artist_id <> $artist_id
RETURN a2.artist_id, a2.name, m.name AS shared_movement,
       'same_movement' AS reason_code
LIMIT 4

// Step 3: Contemporary artists with illustration overlap
MATCH (a:Artist {artist_id: $artist_id})-[:CONTEMPORARY_WITH]-(a2:Artist)
WHERE a2.illustration_count > 0
RETURN a2.artist_id, a2.name,
       a2.nc_priority AS is_priority,
       'contemporary_artist' AS reason_code
ORDER BY a2.nc_priority DESC, a2.illustration_count DESC
LIMIT 6
```

---

### 4.4 Journey 4: Nearby Places (Airbnb model)

*Entry point: place detail page "related places" panel.*

```cypher
// Tier 1: Stored PROXIMATE_TO edges (fast, no PostGIS round-trip)
MATCH (p:Place {place_id: $place_id})-[r:PROXIMATE_TO]->(p2:Place)
WHERE p2.illustration_count > 0
WITH p2, r.distance_km AS dist, r.spatial_relationship AS rel_type
OPTIONAL MATCH (p2)<-[:ANCHORED_AT]-(c:Collection)
WHERE c.status IN ['live', 'coming_soon']
RETURN p2.place_id, p2.name, p2.fcode, p2.country_code,
       dist, rel_type,
       collect(DISTINCT c.slug) AS collections,
       p2.illustration_count
ORDER BY
  CASE WHEN c.status = 'live' THEN 0 ELSE 1 END,
  dist
LIMIT 5

// Tier 2: Same bioregion (for places outside 600km proximity window)
MATCH (p:Place {place_id: $place_id})-[:WITHIN_BIOREGION]->(b:Bioregion)
      <-[:WITHIN_BIOREGION]-(p2:Place)
WHERE p2.place_id <> $place_id
  AND p2.illustration_count > 0
  AND NOT EXISTS {
    MATCH (p)-[:PROXIMATE_TO]->(p2)  // exclude already shown
  }
RETURN p2.place_id, p2.name, b.name AS shared_bioregion,
       'same_bioregion' AS relation_type
LIMIT 3

// Tier 3: Same expedition thread
MATCH (p:Place {place_id: $place_id})<-[:PASSED_THROUGH]-(e:Expedition)
      -[:PASSED_THROUGH]->(p2:Place)
WHERE p2.place_id <> $place_id
RETURN p2.place_id, p2.name, e.name AS expedition_name,
       'expedition_route' AS relation_type
ORDER BY e.start_year
LIMIT 3
```

---

### 4.5 Journey 5: Expedition Thread (NatGeo model)

*Entry point: expedition node — the journey narrative.*

```cypher
// Full expedition thread: stops in order, artists, illustrations from each stop
MATCH (e:Expedition {expedition_id: $expedition_id})
MATCH (e)-[r:PASSED_THROUGH]->(p:Place)
OPTIONAL MATCH (a:Artist)-[:PART_OF_EXPEDITION]->(e)
OPTIONAL MATCH (i:Illustration)-[:PART_OF_EXPEDITION]->(e)
OPTIONAL MATCH (i)-[:ASSOCIATED_WITH]->(p)
WHERE i.product_safe = true
RETURN e.name, e.start_year, e.end_year, e.lead_naturalist,
       p.place_id, p.name, r.stop_sequence, r.year AS stop_year,
       collect(DISTINCT a.name) AS artists,
       collect(DISTINCT i.illustration_id) AS illustrations_at_stop
ORDER BY r.stop_sequence
```

---

### 4.6 Journey 6: Topic Bridge (Smithsonian model)

*Cross-entity discovery via shared topic — the NatGeo "grid" equivalent.*

```cypher
// All entities connected to a topic
MATCH (top:Topic {slug: $topic_slug})
OPTIONAL MATCH (top)<-[:HAS_TOPIC]-(p:Place)
OPTIONAL MATCH (top)<-[:HAS_TOPIC]-(t:Taxon)
OPTIONAL MATCH (top)<-[:HAS_TOPIC]-(i:Illustration)
WHERE i.product_safe = true
OPTIONAL MATCH (top)<-[:HAS_TOPIC]-(c:Collection)
WHERE c.status IN ['live', 'coming_soon']
RETURN top.name, top.domain,
       collect(DISTINCT {id: p.place_id, name: p.name, type: 'place'})[0..6] AS places,
       collect(DISTINCT {id: t.taxon_id, name: t.common_name, type: 'taxon'})[0..6] AS taxa,
       collect(DISTINCT {id: i.illustration_id, title: i.title, type: 'illustration'})[0..8] AS illustrations,
       collect(DISTINCT {id: c.collection_id, name: c.name, type: 'collection'})[0..4] AS collections
```

---

### 4.7 Journey 7: Knowledge Panel (Google KG model)

*Entity summary for any node — used for display cards, AI context assembly, and hover panels.*

```cypher
// Place knowledge panel
MATCH (p:Place {place_id: $place_id})
OPTIONAL MATCH (p)-[:WITHIN_BIOREGION]->(b:Bioregion)
OPTIONAL MATCH (p)-[:LOCATED_IN {hierarchy_type: 'country'}]->(country:Place)
OPTIONAL MATCH (p)<-[:ANCHORED_AT]-(c:Collection)
OPTIONAL MATCH (p)<-[:OCCURS_AT]-(t:Taxon) WITH p, b, country, c, t ORDER BY t.illustration_count DESC LIMIT 5
OPTIONAL MATCH (p)<-[:VISITED]-(a:Artist) WITH p, b, country, c, t, a ORDER BY a.nc_priority DESC, a.priority_rank ASC LIMIT 3
RETURN p,
       b.name AS bioregion,
       country.name AS country_name,
       collect(DISTINCT c)[0..2] AS collections,
       collect(DISTINCT t) AS top_taxa,
       collect(DISTINCT a) AS top_artists
```

---

## Part V: Recommendation Journeys

All recommendations return a `reason_code` and `reason_text` for display. The reason is the
graph path — no opaque scores.

### 5.1 Reason Code Registry

| reason_code | Display text template | Graph source |
|---|---|---|
| `same_artist` | By {artist.name} | Shared CREATED_BY edge |
| `same_subject_other_place` | {taxon.common_name} also depicted at {place.name} | Shared DEPICTS → OCCURS_AT chain |
| `same_place_other_artist` | Also from {place.name} | Shared ASSOCIATED_WITH edge |
| `same_expedition` | From the same {expedition.name} | Shared PART_OF_EXPEDITION edge |
| `same_movement` | Both {movement.name} artists | Shared PART_OF_MOVEMENT path |
| `same_period` | Both from {period.name} | Shared CREATED_IN edge |
| `contemporary_artist` | {artist.name} was a contemporary | CONTEMPORARY_WITH derived edge |
| `shared_expedition_territory` | Both explored {place.name} | Shared VISITED → Place path |
| `same_bioregion` | Both in the {bioregion.name} | Shared WITHIN_BIOREGION path |
| `expedition_route` | Connected by {expedition.name} route | PASSED_THROUGH chain |
| `shared_topic` | Both tagged {topic.name} | Shared HAS_TOPIC path |
| `institutional_sibling` | Both from {institution.name} | Shared SOURCED_FROM edge |

---

### 5.2 Multi-Signal Recommendation Query

*Returns candidates with best reason for each, ranked by signal strength.*

```cypher
MATCH (i:Illustration {illustration_id: $illus_id})

// Signal 1: same artist (strongest)
OPTIONAL MATCH (i)-[:CREATED_BY]->(a:Artist)<-[:CREATED_BY]-(rec:Illustration)
WHERE rec.illustration_id <> $illus_id AND rec.product_safe = true
WITH i, collect(DISTINCT {
  id: rec.illustration_id,
  score: 100,
  reason_code: 'same_artist',
  reason_text: 'By ' + a.name
}) AS artist_recs

// Signal 2: same subject, other place (strong)
MATCH (i)-[:DEPICTS]->(t:Taxon)<-[:DEPICTS]-(rec2:Illustration)-[:ASSOCIATED_WITH]->(p2:Place)
WHERE rec2.illustration_id <> $illus_id AND rec2.product_safe = true
WITH i, artist_recs, collect(DISTINCT {
  id: rec2.illustration_id,
  score: 80,
  reason_code: 'same_subject_other_place',
  reason_text: t.common_name + ' at ' + p2.name
}) AS subject_recs

// Signal 3: same place, other artist (medium)
MATCH (i)-[:ASSOCIATED_WITH]->(p:Place)<-[:ASSOCIATED_WITH]-(rec3:Illustration)
WHERE rec3.illustration_id <> $illus_id AND rec3.product_safe = true
  AND NOT EXISTS { MATCH (i)-[:CREATED_BY]->(a:Artist)<-[:CREATED_BY]-(rec3) }
WITH i, artist_recs, subject_recs, collect(DISTINCT {
  id: rec3.illustration_id,
  score: 60,
  reason_code: 'same_place_other_artist',
  reason_text: 'Also from ' + p.name
}) AS place_recs

// Merge and deduplicate, keep highest score per illustration
WITH artist_recs + subject_recs + place_recs AS all_candidates
UNWIND all_candidates AS candidate
WITH candidate.id AS rec_id,
     max(candidate.score) AS best_score,
     collect(candidate)[0].reason_code AS reason_code,
     collect(candidate)[0].reason_text AS reason_text
RETURN rec_id, best_score, reason_code, reason_text
ORDER BY best_score DESC
LIMIT 8
```

---

## Part VI: Collection Graph

The collection is the commercial and editorial hub. Every collection connects upward to a place and
downward to illustrations, products, and stories. It is also the Spotify playlist analog: an
ordered set with a curatorial intent.

### 6.1 Collection Hub Query

```cypher
// Full collection graph: everything connected to a collection
MATCH (c:Collection {slug: $slug})

// Place anchor
MATCH (c)-[:ANCHORED_AT]->(p:Place)
OPTIONAL MATCH (p)-[:WITHIN_BIOREGION]->(b:Bioregion)

// Members
OPTIONAL MATCH (c)<-[:IN_COLLECTION]-(i:Illustration)
OPTIONAL MATCH (i)-[:CREATED_BY]->(a:Artist)
OPTIONAL MATCH (i)-[:DEPICTS]->(t:Taxon)
OPTIONAL MATCH (prod:Product)-[:DERIVED_FROM]->(i)

// Stories
OPTIONAL MATCH (s:Story)-[:PART_OF_COLLECTION]->(c)

// Related collections (same bioregion or same expedition)
OPTIONAL MATCH (c)-[:ANCHORED_AT]->(p)-[:PROXIMATE_TO]->(p2:Place)
              <-[:ANCHORED_AT]-(c2:Collection)
WHERE c2.collection_id <> c.collection_id
  AND c2.status IN ['live', 'coming_soon']

RETURN c,
       p, b,
       collect(DISTINCT {
         illustration: i,
         artist: a,
         subjects: collect(DISTINCT t.common_name),
         products: collect(DISTINCT prod)
       }) AS members,
       collect(DISTINCT s) AS stories,
       collect(DISTINCT {collection: c2, place: p2})[0..3] AS related_collections
```

---

### 6.2 Collection Completeness Graph

*For editorial planning: what would complete this collection?*

```cypher
// What taxa occur at the anchor place but are NOT yet depicted in this collection?
MATCH (c:Collection {collection_id: $coll_id})-[:ANCHORED_AT]->(p:Place)
MATCH (p)<-[:OCCURS_AT]-(t:Taxon)
WHERE NOT EXISTS {
  MATCH (c)<-[:IN_COLLECTION]-(i:Illustration)-[:DEPICTS]->(t)
}
// And check if any illustration exists for this taxon elsewhere
OPTIONAL MATCH (i2:Illustration)-[:DEPICTS]->(t)
WHERE i2.product_safe = true
RETURN t.scientific_name, t.common_name, t.iucn_status,
       count(DISTINCT i2) AS available_illustrations,
       'gap' AS type
ORDER BY available_illustrations DESC
LIMIT 20
```

---

### 6.3 Collection Commerce Path

```cypher
// What products are available from this collection?
MATCH (c:Collection {slug: $slug})<-[:IN_COLLECTION]-(i:Illustration)
      <-[:DERIVED_FROM]-(prod:Product)
WHERE prod.status = 'active'
RETURN c.name, c.slug,
       collect(DISTINCT {
         product_id: prod.product_id,
         nc_product_id: prod.nc_product_id,
         name: prod.name,
         product_line: prod.product_line,
         price_usd: prod.price_usd,
         illustration_id: i.illustration_id,
         illustration_title: i.title
       }) AS products
ORDER BY prod.price_usd ASC
```

---

## Part VII: AI Retrieval Graph

Grounded AI reads from the graph. It does not write to the graph.

The pattern: every FM task that requires factual claims about NC entities must first receive a
structured subgraph as context. The FM generates from the graph context. It cannot assert facts
about entities not present in the graph.

### 7.1 Context Assembly Patterns

#### Pattern A: Place Context (for editorial generation)

```cypher
// Assemble grounded context for FM before generating place copy
MATCH (p:Place {place_id: $place_id})

// Immediate relationships
OPTIONAL MATCH (p)-[:WITHIN_BIOREGION]->(b:Bioregion)
OPTIONAL MATCH (p)-[:LOCATED_IN {hierarchy_type:'country'}]->(country:Place)

// Content relationships
OPTIONAL MATCH (p)<-[:OCCURS_AT]-(t:Taxon)
  WITH p, b, country, t ORDER BY t.illustration_count DESC LIMIT 8
OPTIONAL MATCH (p)<-[:ASSOCIATED_WITH]-(i:Illustration)-[:CREATED_BY]->(a:Artist)
  WITH p, b, country, t, i, a ORDER BY a.nc_priority DESC
OPTIONAL MATCH (p)<-[:PASSED_THROUGH]-(e:Expedition)

// External identity
OPTIONAL MATCH (p)-[:SAME_AS {authority:'wikidata'}]->(wikidata_id)
OPTIONAL MATCH (p)-[:SAME_AS {authority:'geonames'}]->(geonames_id)

RETURN {
  place: p {.*},
  bioregion: b.name,
  country: country.name,
  geonames_id: p.geonames_id,
  wikidata_qid: p.wikidata_qid,
  top_taxa: collect(DISTINCT t {scientific_name, common_name, iucn_status})[0..8],
  artists_who_visited: collect(DISTINCT a {name, birth_year, death_year, nc_priority})[0..5],
  expeditions: collect(DISTINCT e {name, start_year, end_year, lead_naturalist}),
  illustration_count: p.illustration_count
} AS ground_context
```

This structured payload is the sole factual input for the FM generating place editorial copy.
The FM must not introduce entities, relationships, or facts not present in `ground_context`.

---

#### Pattern B: Illustration Context (for description generation)

```cypher
MATCH (i:Illustration {illustration_id: $illus_id})
OPTIONAL MATCH (i)-[:CREATED_BY]->(a:Artist)
OPTIONAL MATCH (i)-[:DEPICTS]->(t:Taxon)
OPTIONAL MATCH (i)-[:ASSOCIATED_WITH]->(p:Place)
OPTIONAL MATCH (i)-[:SOURCED_FROM]->(inst:Institution)
OPTIONAL MATCH (i)-[:IN_COLLECTION]->(c:Collection)
OPTIONAL MATCH (i)-[:PART_OF_EXPEDITION]->(e:Expedition)
OPTIONAL MATCH (i)-[:CREATED_IN]->(per:Period)

RETURN {
  illustration: i {illustration_id, nc_asset_id, title, year, year_circa, rights},
  artist: a {name, birth_year, death_year, nationality, nc_priority},
  depicted_subjects: collect(DISTINCT t {scientific_name, common_name, rank, iucn_status}),
  associated_place: p {name, geonames_id, country_code},
  institution: inst {name, slug, country_code},
  collections: collect(DISTINCT c {name, slug}),
  expedition: e {name, start_year, lead_naturalist},
  period: per {name, start_year, end_year}
} AS ground_context
```

---

#### Pattern C: Recommendation Reason Generation

```cypher
// Why is illustration B recommended from illustration A?
MATCH (i1:Illustration {illustration_id: $from_id})
MATCH (i2:Illustration {illustration_id: $to_id})

// Find all shared graph paths
OPTIONAL MATCH (i1)-[:CREATED_BY]->(a:Artist)<-[:CREATED_BY]-(i2)
OPTIONAL MATCH (i1)-[:DEPICTS]->(t:Taxon)<-[:DEPICTS]-(i2)
OPTIONAL MATCH (i1)-[:ASSOCIATED_WITH]->(p:Place)<-[:ASSOCIATED_WITH]-(i2)
OPTIONAL MATCH (i1)-[:CREATED_IN]->(per:Period)<-[:CREATED_IN]-(i2)
OPTIONAL MATCH (i1)-[:PART_OF_EXPEDITION]->(e:Expedition)<-[:PART_OF_EXPEDITION]-(i2)
OPTIONAL MATCH (i1)-[:PART_OF_EXPEDITION]->(e2:Expedition)
              -[:PASSED_THROUGH]->(p2:Place)<-[:ASSOCIATED_WITH]-(i2)

RETURN {
  shared_artist: a.name,
  shared_subjects: collect(DISTINCT t.common_name),
  shared_place: p.name,
  shared_period: per.name,
  shared_expedition: e.name,
  expedition_route_connection: {expedition: e2.name, via_place: p2.name}
} AS shared_paths
```

The FM generates a single human-readable recommendation sentence from `shared_paths`. It may not
invent connections not present in this result.

---

#### Pattern D: Search Query Expansion

```cypher
// Expand a user query to canonical graph entities before search
// Input: free text query "Yellowstone bears"
// Step 1: Identify entity candidates
MATCH (n)
WHERE (n:Place OR n:Taxon OR n:Artist OR n:Collection OR n:Topic)
  AND (toLower(n.name) CONTAINS toLower($query_term)
    OR toLower(coalesce(n.common_name, '')) CONTAINS toLower($query_term)
    OR toLower(coalesce(n.canonical_name, '')) CONTAINS toLower($query_term))
RETURN labels(n)[0] AS entity_type,
       coalesce(n.place_id, n.taxon_id, n.artist_id, n.collection_id, n.topic_id) AS entity_id,
       coalesce(n.name, n.common_name) AS entity_name
LIMIT 10
```

This canonical entity set is passed to the FM for query intent classification before the
discovery query is executed. The FM classifies, not retrieves.

---

### 7.2 AI Retrieval Invariants

| Code | Invariant |
|---|---|
| AI-G1 | FM receives a structured `ground_context` payload before generating editorial claims. |
| AI-G2 | FM may not assert facts about entities absent from `ground_context`. |
| AI-G3 | Every FM generation run records: entity_id, entity_type, context_query_hash, model_id, model_version, run_id, generated_at. |
| AI-G4 | Generated text stored in Neo4j (`ai_description`, `ai_synopsis`) carries the `ai_description_run_id` for traceability. |
| AI-G5 | AI-generated text displayed to users must carry attribution to the source graph entities, not to the FM. |
| AI-G6 | Rights claims are never generated by FM. Rights are read from the canonical PostgreSQL record. |

---

## Part VIII: Sync Architecture

### 8.1 Architecture Overview

```
PostgreSQL (canonical)
  │
  ├─ triggers → nc_graph_change_queue (append-only change log)
  │
  └─ projection_worker (polls change_queue)
       │
       ├─ node_upsert_worker → Neo4j nodes
       ├─ relationship_upsert_worker → Neo4j direct relationships
       ├─ derived_relationship_worker → Neo4j derived edges
       │    ├─ PostGIS (ST_DWithin for PROXIMATE_TO)
       │    ├─ PostgreSQL (year overlap for CONTEMPORARY_WITH)
       │    └─ PostgreSQL (occurrence join for CO_OCCURS_WITH)
       │
       └─ validation_worker → PostgreSQL projection_event log

PostGIS (spatial authority)
  → provides derived relationship inputs only
  → PostGIS is never written to from graph layer
```

---

### 8.2 Change Queue Schema (PostgreSQL)

```sql
CREATE TABLE nc_graph_change_queue (
  change_id       BIGSERIAL PRIMARY KEY,
  entity_type     TEXT NOT NULL,       -- 'place' | 'illustration' | 'artist' | 'taxon' | ...
  entity_id       UUID NOT NULL,
  pg_table        TEXT NOT NULL,       -- source table name
  operation       TEXT NOT NULL,       -- 'INSERT' | 'UPDATE' | 'DELETE'
  changed_fields  TEXT[],              -- NULL = all fields (for INSERT/DELETE)
  changed_at      TIMESTAMPTZ DEFAULT now(),
  priority        INTEGER DEFAULT 5,   -- 1 = rights retraction (highest), 5 = normal
  processed_at    TIMESTAMPTZ,
  projection_run_id UUID,
  status          TEXT DEFAULT 'pending',  -- 'pending' | 'processing' | 'done' | 'failed'
  error_message   TEXT,
  retry_count     INTEGER DEFAULT 0
);

CREATE INDEX idx_change_queue_pending  ON nc_graph_change_queue (status, priority, changed_at)
  WHERE status = 'pending';
CREATE INDEX idx_change_queue_entity   ON nc_graph_change_queue (entity_type, entity_id);

-- Trigger function (example: places table)
CREATE OR REPLACE FUNCTION nc_queue_graph_change()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO nc_graph_change_queue (entity_type, entity_id, pg_table, operation, priority)
  VALUES (
    TG_TABLE_NAME,
    COALESCE(NEW.place_id, OLD.place_id),  -- adjust per table
    TG_TABLE_NAME,
    TG_OP,
    CASE WHEN TG_OP = 'DELETE' THEN 1    -- immediate removal
         ELSE 5 END
  );
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Apply to each entity table
CREATE TRIGGER nc_places_graph_sync
AFTER INSERT OR UPDATE OR DELETE ON nc_places
FOR EACH ROW EXECUTE FUNCTION nc_queue_graph_change();
```

---

### 8.3 Projection Worker Logic

```
LOOP every 15 seconds:
  1. SELECT TOP 100 FROM nc_graph_change_queue
     WHERE status = 'pending'
     ORDER BY priority ASC, changed_at ASC
     FOR UPDATE SKIP LOCKED

  2. FOR EACH change:
     a. Mark status = 'processing'
     b. Fetch canonical entity from PostgreSQL
     c. MERGE node in Neo4j by pg_id (MERGE on unique constraint key)
     d. SET all properties from PostgreSQL record
     e. For direct relationships: upsert from FK tables
     f. If operation = 'DELETE': DETACH DELETE node from Neo4j
     g. Mark status = 'done', set processed_at

  3. AFTER batch:
     IF any place or artist changed:
       → Run derived relationship recomputation for affected entities
         - PROXIMATE_TO: PostGIS ST_DWithin(centroid::geography, 600000)
         - CONTEMPORARY_WITH: year overlap query across artist pairs
         - CO_OCCURS_WITH: shared taxon_place occurrence pairs

  4. Write projection_event record to PostgreSQL:
     {run_id, batch_size, success_count, fail_count, duration_ms, worker_id}
```

---

### 8.4 Derived Relationship Recomputation (SQL → Neo4j)

```sql
-- PROXIMATE_TO: places within 600km
SELECT p1.place_id AS from_id, p2.place_id AS to_id,
       ST_Distance(p1.centroid::geography, p2.centroid::geography) / 1000 AS distance_km,
       CASE
         WHEN ST_DWithin(p1.centroid::geography, p2.centroid::geography, 100000)
           THEN 'adjacent'
         WHEN p1.country_code = p2.country_code
           THEN 'same_country'
         ELSE 'same_bioregion'
       END AS spatial_relationship
FROM nc_places p1, nc_places p2
WHERE p1.place_id = $changed_place_id
  AND p2.place_id <> p1.place_id
  AND ST_DWithin(p1.centroid::geography, p2.centroid::geography, 600000);
```

```sql
-- CONTEMPORARY_WITH: active year overlap
SELECT a1.artist_id AS from_id, a2.artist_id AS to_id,
       GREATEST(a1.active_start, a2.active_start) AS overlap_start,
       LEAST(a1.active_end, a2.active_end) AS overlap_end,
       LEAST(a1.active_end, a2.active_end)
         - GREATEST(a1.active_start, a2.active_start) AS overlap_years,
       CASE WHEN (LEAST(a1.active_end, a2.active_end)
              - GREATEST(a1.active_start, a2.active_start)) >= 10
         THEN 1.0 ELSE 0.7
       END AS confidence
FROM nc_artists a1, nc_artists a2
WHERE a1.artist_id = $changed_artist_id
  AND a2.artist_id <> a1.artist_id
  AND a1.active_start <= a2.active_end
  AND a1.active_end >= a2.active_start
  AND ABS(a1.active_start - a2.active_start) <= 30;
```

---

### 8.5 Full Rebuild Protocol

Full rebuild is triggered by: schema version change, governance amendment, recovery from
data corruption, or on-demand Director Decision.

```
1.  Record Director Decision authorizing full rebuild in PostgreSQL.
2.  Set projection_run status = 'rebuilding'. Freeze incremental workers.
3.  Clear all non-constraint nodes from Neo4j (MATCH (n) DETACH DELETE n).
4.  Load in dependency order (no cross-references break):
    a. Bioregions
    b. Institutions
    c. Periods
    d. Movements
    e. Topics
    f. Places (no FK dependencies)
    g. Artists
    h. Taxa
    i. Expeditions (depends on places + artists)
    j. Illustrations (depends on artists + taxa + places + institutions)
    k. Collections (depends on illustrations + places)
    l. Stories (depends on collections + illustrations + places)
    m. Products (depends on illustrations)
5.  Compute derived relationships:
    a. PROXIMATE_TO (PostGIS batch)
    b. WITHIN_BIOREGION (PostGIS batch)
    c. CONTEMPORARY_WITH (SQL batch across all artist pairs)
    d. CO_OCCURS_WITH (SQL batch across taxon_place pairs)
    e. INFLUENCED_BY (where explicit source data exists)
6.  Validate:
    a. Node count matches PostgreSQL entity counts
    b. No orphan nodes (every node has ≥1 relationship except leaf nodes)
    c. Every node has pg_id, pg_table, projection_run_id
    d. Constraint violations = 0
    e. Sample 10 entities: verify relationships match PostgreSQL FK data
7.  Set projection_run status = 'active'. Release incremental workers.
8.  Record projection_event: full_rebuild/success with counts and checksums.
```

---

## Part IX: Governance Controls

### 9.1 Projection Schema Registry

Every node label and relationship type must be registered before use.

```sql
CREATE TABLE nc_projection_schema_registry (
  schema_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  schema_version  TEXT NOT NULL,           -- 'v1.0', 'v1.1'
  entity_type     TEXT NOT NULL,           -- 'node' | 'relationship'
  label           TEXT NOT NULL,           -- 'Place', 'CREATED_BY', etc.
  pg_source_table TEXT NOT NULL,
  pg_source_id_field TEXT NOT NULL,
  derivation_type TEXT NOT NULL,           -- 'direct' | 'derived'
  derivation_rule TEXT,                    -- null for direct; SQL/PostGIS rule for derived
  is_active       BOOLEAN DEFAULT true,
  activated_at    TIMESTAMPTZ,
  deactivated_at  TIMESTAMPTZ,
  director_decision_id TEXT                -- governance gate
);
```

New labels/types require a row in this table + `director_decision_id` before the projection
worker will write them to Neo4j.

---

### 9.2 Projection Event Log

```sql
CREATE TABLE nc_projection_events (
  event_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  projection_run_id UUID NOT NULL,
  event_type      TEXT NOT NULL,    -- 'incremental_batch' | 'full_rebuild' | 'schema_update'
  schema_version  TEXT NOT NULL,
  entity_type     TEXT,
  operation       TEXT,             -- 'upsert' | 'delete' | 'derive'
  success_count   INTEGER,
  fail_count      INTEGER,
  orphan_count    INTEGER,
  duration_ms     INTEGER,
  worker_id       TEXT,
  recorded_at     TIMESTAMPTZ DEFAULT now(),
  notes           TEXT
);
```

---

### 9.3 Staleness Monitor

```sql
CREATE TABLE nc_projection_staleness (
  entity_type     TEXT PRIMARY KEY,
  oldest_pending_age_minutes INTEGER,
  pending_count   INTEGER,
  last_measured_at TIMESTAMPTZ DEFAULT now()
);
```

Alert conditions:
- Rights retraction (priority=1) pending > 5 minutes → PagerDuty
- Any entity pending > 30 minutes → Warning
- Full rebuild not completed within 2 hours → Alert

---

### 9.4 Scale Parameters

| Parameter | 100 places | 1,000 places |
|---|---|---|
| Estimated nodes | ~15,000 | ~150,000 |
| Estimated relationships | ~80,000 | ~800,000 |
| Recommended deployment | Neo4j AuraDB Free/Professional or self-hosted Community | Neo4j AuraDB Professional or Enterprise |
| Full rebuild time (target) | < 10 minutes | < 60 minutes |
| Incremental sync lag (target) | < 15 minutes | < 15 minutes |
| Rights retraction lag (target) | < 5 minutes | < 5 minutes |
| Read replicas needed | No | Consider 1 for high-traffic discovery API |

---

### 9.5 Governance Invariant Audit Checklist

Run weekly (or after every full rebuild):

```cypher
// G-2: Every node has required provenance fields
MATCH (n)
WHERE n.pg_id IS NULL OR n.pg_table IS NULL OR n.projection_run_id IS NULL
RETURN labels(n) AS label, count(n) AS orphan_count
// Expected: 0 rows

// G-3: Every relationship has derivation
MATCH ()-[r]->()
WHERE r.derivation IS NULL
RETURN type(r) AS rel_type, count(r) AS missing_derivation
// Expected: 0 rows

// G-5: No Product has a rights-derived property
// (Commerce scoring must be PostgreSQL only)
MATCH (prod:Product)
WHERE prod.rights IS NOT NULL  // Products must not carry rights fields
RETURN count(prod) AS violation_count
// Expected: 0 rows

// G-7: Full rebuild inputs are current
MATCH (n)
WHERE n.projected_at < datetime() - duration('P7D')  // older than 7 days
RETURN labels(n)[0] AS label, count(n) AS stale_count
// Expected: 0 rows (or alert if any)
```

---

## Appendix A: Node Summary Table (Scale Reference)

| Node label | PostgreSQL source | 100 places (est.) | 1,000 places (est.) |
|---|---|---|---|
| Place | nc_places | 100 | 1,000 |
| Illustration | source_item / illustration_opportunities | 5,000–10,000 | 50,000–100,000 |
| Artist | creator_authority_registry | 200–500 | 2,000–5,000 |
| Taxon | nc_taxa | 1,000–2,000 | 10,000–20,000 |
| Institution | sources | 20–25 | 25–30 |
| Collection | nc_collections | 20–50 | 200–500 |
| Story | story / publication tables | 5–20 | 50–200 |
| Expedition | nc_expeditions | 20–50 | 100–200 |
| Movement | nc_movements | 10–20 | 15–25 |
| Topic | nc_topics | 20–30 | 30–50 |
| Period | nc_periods | 5–10 | 5–10 |
| Bioregion | nc_bioregions | 8–12 | 15–25 |
| Product | nc_products | 10–20 | 100–500 |
| **Total (est.)** | | **~16,000** | **~160,000** |

---

## Appendix B: Relationship Summary Table

| Relationship | Direction | Derivation | Cardinality |
|---|---|---|---|
| CREATED_BY | Illustration → Artist | direct | many:1 |
| DEPICTS | Illustration → Taxon | direct | many:many |
| ASSOCIATED_WITH | Illustration → Place | direct | many:many |
| SOURCED_FROM | Illustration → Institution | direct | many:1 |
| IN_COLLECTION | Illustration → Collection | direct | many:many |
| CREATED_IN | Illustration → Period | direct | many:1 |
| PART_OF_EXPEDITION | Illustration → Expedition | direct | many:many |
| HAS_TOPIC | Illustration/Place/Taxon → Topic | direct | many:many |
| VISITED | Artist → Place | direct | many:many |
| PART_OF_EXPEDITION | Artist → Expedition | direct | many:many |
| ACTIVE_IN | Artist → Period | direct | many:1 |
| PART_OF_MOVEMENT | Artist → Movement | direct | many:many |
| INFLUENCED_BY | Artist → Artist | direct | many:many |
| CONTEMPORARY_WITH | Artist ↔ Artist | **derived** | many:many |
| OCCURS_AT | Taxon → Place | direct | many:many |
| CHILD_OF | Taxon → Taxon | direct | many:1 |
| CO_OCCURS_WITH | Taxon ↔ Taxon | **derived** | many:many |
| LOCATED_IN | Place → Place | direct | many:1 |
| PROXIMATE_TO | Place → Place | **derived** (PostGIS) | many:many |
| WITHIN_BIOREGION | Place → Bioregion | **derived** (PostGIS) | many:1 |
| PASSED_THROUGH | Expedition → Place | direct | many:many |
| ROUTE_PASSES_NEAR | Expedition → Place | **derived** (PostGIS) | many:many |
| ANCHORED_AT | Collection → Place | direct | many:1 |
| FEATURES_ARTIST | Collection → Artist | direct | many:many |
| PART_OF_COLLECTION | Story → Collection | direct | many:1 |
| FEATURES_PLACE | Story → Place | direct | many:many |
| FEATURES_ILLUSTRATION | Story → Illustration | direct | many:many |
| DERIVED_FROM | Product → Illustration | direct | many:1 |
| SAME_AS | Any → External | direct | many:many |

---

*NC-GRAPH-002 · v1.0 · 2026-06-13 · DRAFT*
