# NC-ICH-001 Technical Plan

| Field | Value |
|---|---|
| Document | NC-ICH-001 |
| Version | 1.0 |
| Status | DRAFT - technical plan |
| Date | 2026-06-13 |
| Scope | ICH authority and discovery architecture extension |
| Systems | PostgreSQL, PostGIS, Neo4j |

---

## 1. Purpose

NC-ICH-001 extends the place, authority, and discovery architecture to support Intangible
Cultural Heritage (ICH) as a first-class candidate discovery layer.

The ICH layer represents living cultural practices and documented traditions. It does not create
canonical place identity, product eligibility, or commerce authority. It enriches discovery by
connecting places, communities, public-domain documentation, themes, festivals, craft knowledge,
food traditions, performances, and related journeys.

Primary user jobs:

| User job | ICH contribution | Required system behavior |
|---|---|---|
| Discover a place through living heritage | Show practices linked to a place or region | PostgreSQL stores candidates; PostGIS scopes location; Neo4j projects relationships |
| Continue from a collection into a tradition | Traverse collection -> ICH -> place -> asset -> person | Neo4j traversal with PostgreSQL authority recheck |
| Understand cultural context before product or editorial work | Surface sensitivity, authority status, and evidence | PostgreSQL owns status and governance |
| Find nearby or regional heritage practices | Query practices by place anchors and cultural regions | PostGIS owns containment/proximity |
| Build recommendation panels | Explain why a practice relates to a journey | Neo4j computes related paths; API returns reason metadata |

---

## 2. ICH Node Types

NC-ICH-001 introduces an `ICH` concept family. In PostgreSQL, the type is a controlled value in
candidate tables. In Neo4j, it projects as `(:ICH)` plus one subtype label.

Required types:

| ICH type | Neo4j labels | Description | Example discovery use |
|---|---|---|---|
| Craft | `:ICH:Craft` | Material practice, tools, making processes, textiles, ceramics, carving | Connect Kyoto to ceramics, dyeing, lacquer, tools, makers |
| Festival | `:ICH:Festival` | Recurring ritual or public cultural event | Link place pages to seasonal journeys |
| Oral Tradition | `:ICH:OralTradition` | Storytelling, language, epics, memory, narrative transmission | Connect place and collection pages to origin stories |
| Knowledge System | `:ICH:KnowledgeSystem` | Nature knowledge, navigation, astronomy, agriculture, medicine | Bridge taxa, places, expeditions, and documentary assets |
| Food Tradition | `:ICH:FoodTradition` | Cuisine, preparation, agricultural foodways, ceremonial food | Regional discovery and cultural context |
| Performance | `:ICH:Performance` | Music, dance, theatre, instruments, costume, procession | Connect public-domain costume, instrument, and event records |

Canonical rule: these are not products and not canonical place identities. They remain authority
candidates until evidence and review promote them.

---

## 3. PostgreSQL Responsibilities

PostgreSQL is the authority system for ICH records, review state, source evidence, sensitivity,
and API eligibility. It owns every status field that can affect publication, sensitivity handling,
or downstream product decisions.

### 3.1 Proposed Tables

```sql
CREATE TABLE ich_candidate (
    ich_candidate_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ich_slug               TEXT NOT NULL UNIQUE,
    display_name           TEXT NOT NULL,
    ich_type               TEXT NOT NULL CHECK (ich_type IN (
        'Craft',
        'Festival',
        'Oral Tradition',
        'Knowledge System',
        'Food Tradition',
        'Performance'
    )),
    alternate_names        TEXT[] NOT NULL DEFAULT '{}',
    description            TEXT NOT NULL DEFAULT '',
    candidate_status       TEXT NOT NULL DEFAULT 'candidate' CHECK (
        candidate_status IN ('candidate','needs_review','rejected','ratified')
    ),
    authority_status       TEXT NOT NULL DEFAULT 'unverified' CHECK (
        authority_status IN ('unverified','source_backed','community_review','ratified')
    ),
    sensitivity_level      TEXT NOT NULL DEFAULT 'unknown' CHECK (
        sensitivity_level IN ('unknown','low','consult','restricted')
    ),
    public_domain_potential TEXT NOT NULL DEFAULT 'unknown' CHECK (
        public_domain_potential IN ('unknown','low','medium','high')
    ),
    source_hints           JSONB NOT NULL DEFAULT '[]',
    evidence_summary       JSONB NOT NULL DEFAULT '{}',
    created_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ich_place_anchor (
    ich_place_anchor_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ich_candidate_id       UUID NOT NULL REFERENCES ich_candidate(ich_candidate_id),
    place_slug             TEXT NOT NULL,
    anchor_role            TEXT NOT NULL CHECK (
        anchor_role IN ('origin','primary','associated','diaspora','documentation_site')
    ),
    confidence             NUMERIC(4,3) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    evidence               JSONB NOT NULL DEFAULT '{}',
    candidate_status       TEXT NOT NULL DEFAULT 'candidate',
    UNIQUE (ich_candidate_id, place_slug, anchor_role)
);

CREATE TABLE ich_source_evidence (
    ich_source_evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ich_candidate_id       UUID NOT NULL REFERENCES ich_candidate(ich_candidate_id),
    source_system          TEXT NOT NULL,
    source_url             TEXT,
    source_identifier      TEXT,
    evidence_type          TEXT NOT NULL CHECK (
        evidence_type IN ('designation','catalog_record','scholarly_reference','community_source','editorial_note')
    ),
    evidence_payload       JSONB NOT NULL DEFAULT '{}',
    reviewed_status        TEXT NOT NULL DEFAULT 'unreviewed' CHECK (
        reviewed_status IN ('unreviewed','accepted','rejected')
    ),
    captured_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ich_asset_link (
    ich_asset_link_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ich_candidate_id       UUID NOT NULL REFERENCES ich_candidate(ich_candidate_id),
    asset_slug             TEXT NOT NULL,
    relationship_role      TEXT NOT NULL CHECK (
        relationship_role IN ('documents','depicts_context','instrument','costume','tool','ingredient','place_record')
    ),
    product_path_allowed   BOOLEAN NOT NULL DEFAULT false,
    evidence               JSONB NOT NULL DEFAULT '{}',
    UNIQUE (ich_candidate_id, asset_slug, relationship_role)
);

CREATE TABLE ich_collection_link (
    ich_collection_link_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ich_candidate_id       UUID NOT NULL REFERENCES ich_candidate(ich_candidate_id),
    collection_slug        TEXT NOT NULL,
    feature_role           TEXT NOT NULL CHECK (feature_role IN ('anchor','context','related')),
    reason                 TEXT NOT NULL DEFAULT '',
    UNIQUE (ich_candidate_id, collection_slug, feature_role)
);
```

### 3.2 PostgreSQL Invariants

| Invariant | Rule |
|---|---|
| PG-ICH-1 | No ICH row is canonical by default. `authority_status='ratified'` requires accepted evidence. |
| PG-ICH-2 | `sensitivity_level='restricted'` blocks product-path flags regardless of asset rights. |
| PG-ICH-3 | `ich_asset_link.product_path_allowed` is advisory only; commerce still rechecks asset/product gates. |
| PG-ICH-4 | Source evidence is stored in PostgreSQL, not Neo4j relationship-only properties. |
| PG-ICH-5 | No GeoNames, Wikidata, or UNESCO ID is treated as canonical until the authority pipeline ratifies it. |

---

## 4. PostGIS Responsibilities

PostGIS remains the spatial authority. ICH records are usually not points or polygons themselves;
they are anchored to places, regions, routes, and cultural landscapes.

### 4.1 Proposed Spatial Tables

```sql
CREATE TABLE ich_region_geometry (
    ich_region_geometry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_slug            TEXT NOT NULL UNIQUE,
    display_name           TEXT NOT NULL,
    region_type            TEXT NOT NULL CHECK (
        region_type IN ('cultural_region','language_region','practice_region','festival_route')
    ),
    authority_status       TEXT NOT NULL DEFAULT 'unverified',
    geometry               GEOMETRY(Geometry, 4326) NOT NULL,
    evidence               JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX idx_ich_region_geometry_geom
    ON ich_region_geometry USING GIST (geometry);

CREATE TABLE ich_place_region_candidate (
    ich_place_region_candidate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ich_candidate_id              UUID NOT NULL REFERENCES ich_candidate(ich_candidate_id),
    region_slug                   TEXT NOT NULL REFERENCES ich_region_geometry(region_slug),
    relationship_role             TEXT NOT NULL CHECK (
        relationship_role IN ('within','overlaps','route','seasonal_route')
    ),
    evidence                      JSONB NOT NULL DEFAULT '{}',
    UNIQUE (ich_candidate_id, region_slug, relationship_role)
);
```

### 4.2 Spatial Query Responsibilities

| Query | PostGIS owner | Example |
|---|---|---|
| Practices near a place | `ST_DWithin` through place geometry anchors | festivals near Kyoto |
| Practices within region | `ST_Within` / `ST_Intersects` | crafts within Kansai |
| Festival route intersects place | `ST_Intersects` | procession route crossing city district |
| Cultural region overlay | polygon intersection | food tradition region overlapping a protected landscape |
| Map browse | tile/viewport filtering | ICH candidates visible in a map viewport |

PostGIS does not ratify cultural authority. It only answers spatial questions once candidate or
ratified geometry exists.

---

## 5. Neo4j Responsibilities

Neo4j is a projection and traversal layer. It serves discovery experiences where relationship
paths matter. It must not become the authority store for sensitivity, rights, publication, or
commerce decisions.

### 5.1 Node Projection

```cypher
(:ICH {
  id: STRING,                    // pg UUID as string
  slug: STRING,
  display_name: STRING,
  ich_type: STRING,              // one of the six required types
  candidate_status: STRING,
  authority_status: STRING,
  sensitivity_level: STRING,     // display/filter hint only; PostgreSQL rechecked
  public_domain_potential: STRING,
  summary: STRING,
  pg_table: 'ich_candidate',
  pg_id: STRING,
  schema_version: STRING,
  projection_run_id: STRING,
  projected_at: DATETIME
})
```

Subtype labels are added from `ich_type`:

```cypher
(:ICH:Craft)
(:ICH:Festival)
(:ICH:OralTradition)
(:ICH:KnowledgeSystem)
(:ICH:FoodTradition)
(:ICH:Performance)
```

### 5.2 Constraints and Indexes

```cypher
CREATE CONSTRAINT ich_id IF NOT EXISTS FOR (n:ICH) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT ich_slug IF NOT EXISTS FOR (n:ICH) REQUIRE n.slug IS UNIQUE;
CREATE INDEX ich_type IF NOT EXISTS FOR (n:ICH) ON (n.ich_type);
CREATE INDEX ich_authority_status IF NOT EXISTS FOR (n:ICH) ON (n.authority_status);
CREATE INDEX ich_candidate_status IF NOT EXISTS FOR (n:ICH) ON (n.candidate_status);
```

### 5.3 Relationships

```cypher
(:ICH)-[:PRACTICED_AT {
  anchor_role: STRING,
  confidence: FLOAT,
  derivation: 'direct',
  pg_source: 'ich_place_anchor',
  pg_source_id: STRING
}]->(:Place)

(:ICH)-[:DOCUMENTED_BY {
  relationship_role: STRING,
  product_path_allowed: BOOLEAN,
  derivation: 'direct',
  pg_source: 'ich_asset_link',
  pg_source_id: STRING
}]->(:Asset)

(:Collection)-[:FEATURES_ICH {
  feature_role: STRING,
  reason: STRING,
  derivation: 'direct',
  pg_source: 'ich_collection_link',
  pg_source_id: STRING
}]->(:ICH)

(:ICH)-[:RELATED_TO {
  reason: STRING,
  weight: FLOAT,
  derivation: 'editorial|derived',
  pg_source: STRING,
  pg_source_id: STRING
}]->(:ICH)

(:ICH)-[:USES_TAXON {
  use_type: STRING,
  derivation: 'direct',
  pg_source: 'ich_taxon_link',
  pg_source_id: STRING
}]->(:Species)

(:Event)-[:CELEBRATES_ICH {
  season: STRING,
  derivation: 'direct',
  pg_source: 'ich_event_link',
  pg_source_id: STRING
}]->(:ICH)

(:Person)-[:CUSTODIAN_OF {
  role: STRING,
  derivation: 'direct',
  pg_source: 'ich_person_link',
  pg_source_id: STRING
}]->(:ICH)

(:Institution)-[:DOCUMENTS_ICH {
  collection_ref: STRING,
  derivation: 'direct',
  pg_source: 'ich_source_evidence',
  pg_source_id: STRING
}]->(:ICH)
```

### 5.4 Traversal Use Cases

| Experience | Neo4j traversal | PostgreSQL recheck |
|---|---|---|
| Related journeys | Collection -> ICH -> Place/Asset/Species | candidate status, sensitivity, publication |
| Recommendation panel | ICH -> RELATED_TO -> ICH/Collection | authority and display eligibility |
| Place page context | Place <- PRACTICED_AT - ICH -> Asset | source evidence, restricted sensitivity |
| Knowledge journey | ICH:KnowledgeSystem -> Species -> Place | taxon authority, asset rights |
| Festival journey | Event -> CELEBRATES_ICH -> Place/Collection | event publication and cultural review |

---

## 6. System Integration

### 6.1 Data Flow

```
Source hints / editorial candidates
  -> PostgreSQL ich_candidate + evidence tables
  -> authority review and sensitivity review
  -> optional PostGIS region/place geometry links
  -> Neo4j projection for discovery traversal
  -> API returns graph paths with PostgreSQL rechecks
  -> frontend renders ICH context, not product authority
```

### 6.2 Responsibility Split

| Concern | PostgreSQL | PostGIS | Neo4j |
|---|---|---|---|
| ICH candidate identity | Owner | None | Projection only |
| Authority status | Owner | None | Display/filter copy only |
| Cultural sensitivity | Owner | None | Display/filter copy only |
| Source evidence | Owner | None | Relationship provenance summary only |
| Place anchoring | Stores anchor rows | Validates spatial relation | Traversal edge |
| Cultural region geometry | Metadata owner | Geometry owner | Optional projected region node later |
| Nearby/within/intersects | Query source | Owner | Not authoritative |
| Related journey paths | Eligibility recheck | Spatial enrichment | Traversal owner |
| Product eligibility | Owner through commerce gates | None | Must not decide |

### 6.3 API Surfaces

Initial read-only API candidates:

| Endpoint | Purpose | Backing systems |
|---|---|---|
| `GET /ich/candidates` | list candidate ICH records | PostgreSQL |
| `GET /ich/{slug}` | detail with evidence summary | PostgreSQL |
| `GET /ich/{slug}/places` | place anchors and spatial context | PostgreSQL + PostGIS |
| `GET /ich/{slug}/related` | related ICH and collections | Neo4j + PostgreSQL recheck |
| `GET /discover/ich/within-region` | region-bounded ICH discovery | PostGIS + PostgreSQL |
| `GET /graph/ich/{slug}` | graph journey projection | Neo4j + PostgreSQL recheck |

No write API is proposed in NC-ICH-001.

---

## 7. Example Journey

Example: Kyoto craft discovery.

1. PostgreSQL stores `ich_candidate` row:
   - `ich_slug='kyoto-lacquerware'`
   - `ich_type='Craft'`
   - `candidate_status='candidate'`
   - `authority_status='unverified'`
   - `sensitivity_level='consult'`

2. PostgreSQL stores `ich_place_anchor`:
   - `place_slug='kyoto'`
   - `anchor_role='primary'`

3. PostGIS associates Kyoto and Kansai geometries for map/region filtering.

4. Neo4j projects:

```cypher
(:ICH:Craft {slug: 'kyoto-lacquerware'})-[:PRACTICED_AT]->(:Place {slug: 'kyoto'})
(:Collection {slug: 'kyoto-collection'})-[:FEATURES_ICH]->(:ICH:Craft {slug: 'kyoto-lacquerware'})
```

5. API response may show Kyoto lacquerware as cultural context, but product or asset activation
   requires PostgreSQL evidence, rights, and sensitivity gates.

---

## 8. Implementation Phases

### Phase 0 - Candidate schema only

- Create PostgreSQL candidate/evidence/link tables.
- Seed a small candidate set with all six ICH types.
- No canonical IDs.
- No product pages.
- No graph write requirement.

### Phase 1 - Spatial anchoring

- Add `ich_region_geometry` and `ich_place_region_candidate`.
- Expose within-region and nearby candidate discovery.
- Keep authority unratified unless evidence review is complete.

### Phase 2 - Neo4j discovery projection

- Project `(:ICH)` nodes and subtype labels.
- Project `PRACTICED_AT`, `FEATURES_ICH`, `DOCUMENTED_BY`, `RELATED_TO`.
- API always rechecks PostgreSQL before returning public journey panels.

### Phase 3 - Authority ratification workflow

- Add review states, reviewer notes, evidence acceptance, and sensitivity gates.
- Promote only source-backed rows.
- Still do not allow Neo4j to make product decisions.

---

## 9. Acceptance Criteria

| ID | Criterion |
|---|---|
| ICH-AC-1 | Schema supports all six requested ICH types. |
| ICH-AC-2 | PostgreSQL remains authority for candidate status, authority status, sensitivity, and evidence. |
| ICH-AC-3 | PostGIS owns spatial queries for nearby, within-region, intersects, and route overlap. |
| ICH-AC-4 | Neo4j stores only projection nodes/relationships for discovery traversal. |
| ICH-AC-5 | No product activation can be derived from ICH graph data alone. |
| ICH-AC-6 | Restricted or consult-sensitive ICH records are blocked or held by PostgreSQL gates. |
| ICH-AC-7 | Graph responses include PostgreSQL provenance IDs so authority can be rechecked. |

---

## 10. Decision

NC-ICH-001 should proceed as a candidate-first architecture extension.

The first implementation should create PostgreSQL candidate/evidence tables and optional PostGIS
region anchors. Neo4j projection should wait until there are enough reviewed candidate links to
power meaningful related journeys. If Neo4j projection is added early, nodes must be clearly
marked as candidate/unverified and must not be used as canonical authority or product eligibility.
