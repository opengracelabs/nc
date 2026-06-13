# NC-GRAPH-003: NC-GRAPH-002 Implementation Review

| Field | Value |
|---|---|
| Document | NC-GRAPH-003 |
| Version | 1.0 |
| Status | **DRAFT** |
| Date | 2026-06-13 |
| Reviews | NC-GRAPH-002 v1.0 |
| Focus | Explainable recommendations · Governance isolation · Rights isolation · PostgreSQL authority |

---

## Review Summary

NC-GRAPH-002 is architecturally sound. The node model, relationship vocabulary, sync pipeline,
and invariant framework are correct in their design intent.

**17 findings identified.** 3 are critical and block ratification. 7 are high-severity and should
be corrected before implementation begins. 5 are medium. 2 are minor.

| Severity | Count | Ratification gate |
|---|---|---|
| Critical | 3 | Yes — must resolve before ratification |
| High | 7 | Yes — must resolve before implementation |
| Medium | 5 | No — document before Sprint 1 |
| Minor | 2 | No — note for Sprint 2 |

---

## Area 1: Explainable Recommendations

### REC-1 · HIGH · Deduplication query picks wrong reason code

**Location:** Part V, Section 5.2, "Merge and deduplicate" block.

**Problem:** The current deduplication logic:

```cypher
WITH artist_recs + subject_recs + place_recs AS all_candidates
UNWIND all_candidates AS candidate
WITH candidate.id AS rec_id,
     max(candidate.score) AS best_score,
     collect(candidate)[0].reason_code AS reason_code,
     collect(candidate)[0].reason_text AS reason_text
```

`collect(candidate)[0]` returns the first candidate in collection order, which is
non-deterministic. When an illustration is a match for both `same_artist` (score 100) and
`same_place_other_artist` (score 60), the displayed reason may be the weaker one. The user sees
"Also from Yellowstone" when the correct reason is "By Thomas Moran."

**Correction:**

```cypher
WITH artist_recs + subject_recs + place_recs AS all_candidates
UNWIND all_candidates AS candidate
WITH candidate
ORDER BY candidate.score DESC
WITH candidate.id AS rec_id,
     collect(candidate)[0] AS best_candidate
RETURN rec_id,
       best_candidate.score    AS best_score,
       best_candidate.reason_code AS reason_code,
       best_candidate.reason_text AS reason_text
ORDER BY best_score DESC
LIMIT 8
```

---

### REC-2 · HIGH · Signals 2 and 3 use MATCH instead of OPTIONAL MATCH

**Location:** Part V, Section 5.2, Signal 2 and Signal 3.

**Problem:** After Signal 1 outputs `WITH i, ... AS artist_recs`, Signals 2 and 3 use plain
`MATCH`. If an illustration has no `DEPICTS` relationships (Signal 2 finds zero rows), the entire
query returns nothing — even when Signal 1 found valid artist recommendations. Signals 2 and 3
are additive, not required.

**Correction:** Replace `MATCH` with `OPTIONAL MATCH` for Signals 2 and 3:

```cypher
// Signal 2: same subject, other place (strong)
OPTIONAL MATCH (i)-[:DEPICTS]->(t:Taxon)<-[:DEPICTS]-(rec2:Illustration)
              -[:ASSOCIATED_WITH]->(p2:Place)
WHERE rec2.illustration_id <> $illus_id AND rec2.product_safe = true
WITH i, artist_recs, collect(DISTINCT {
  id: rec2.illustration_id,
  score: 80,
  reason_code: 'same_subject_other_place',
  reason_text: coalesce(t.common_name, 'same subject') + ' at ' + coalesce(p2.name, 'another place')
}) AS subject_recs

// Signal 3: same place, other artist (medium)
OPTIONAL MATCH (i)-[:ASSOCIATED_WITH]->(p:Place)<-[:ASSOCIATED_WITH]-(rec3:Illustration)
WHERE rec3.illustration_id <> $illus_id AND rec3.product_safe = true
  AND NOT EXISTS { MATCH (i)-[:CREATED_BY]->(ax:Artist)<-[:CREATED_BY]-(rec3) }
WITH i, artist_recs, subject_recs, collect(DISTINCT {
  id: rec3.illustration_id,
  score: 60,
  reason_code: 'same_place_other_artist',
  reason_text: 'Also from ' + coalesce(p.name, 'the same place')
}) AS place_recs
```

---

### REC-3 · MEDIUM · Journey 4 ORDER BY fails when Collection is NULL

**Location:** Part IV, Section 4.4, Journey 4 Tier 1 query.

**Problem:**

```cypher
ORDER BY
  CASE WHEN c.status = 'live' THEN 0 ELSE 1 END,
  dist
```

`c` comes from `OPTIONAL MATCH`. When a nearby place has no collection, `c` is NULL. The
`CASE` expression evaluates `NULL.status`, producing NULL — which sorts below 1, not above it.
Places with a live collection will sort identically with places with no collection.

**Correction:**

```cypher
ORDER BY
  CASE WHEN c IS NOT NULL AND c.status = 'live' THEN 0
       WHEN c IS NOT NULL THEN 1
       ELSE 2 END,
  dist
```

---

### REC-4 · MEDIUM · `a2.priority_rank` filter excludes non-priority artists from Artist Radio

**Location:** Part IV, Section 4.3, Journey 3 Step 1.

**Problem:**

```cypher
WHERE a2.artist_id <> $artist_id
  AND a2.nc_priority = true    // prioritize golden age illustrators
```

The `AND a2.nc_priority = true` filter completely excludes non-priority artists from the
shared-territory result. At small graph scale (few priority artists), the result set may be
empty or too small. The intent was to rank priority artists first, not exclude all others.

**Correction:** Remove the WHERE filter; add to ORDER BY:

```cypher
WHERE a2.artist_id <> $artist_id
WITH a2, collect(DISTINCT p.name) AS shared_places, count(DISTINCT p) AS place_overlap
RETURN a2.artist_id, a2.name, shared_places, place_overlap,
       'shared_expedition_territory' AS reason_code
ORDER BY a2.nc_priority DESC, place_overlap DESC, coalesce(a2.priority_rank, 99) ASC
LIMIT 6
```

---

### REC-5 · MINOR · No `reason_version` on recommendation output

**Location:** Part V, Section 5.1 (Reason Code Registry) and Section 5.2.

**Problem:** Reason text templates ("By {artist.name}", "Also from {place.name}") will change
as copy is refined. Stored recommendation results or cached panels will show stale reason text
without any version signal. No mechanism exists to detect or invalidate outdated reason copy.

**Recommendation:** Add `reason_version: STRING` to the recommendation output schema (e.g., `v1`).
When reason templates change, increment the version. API responses carrying `reason_version`
can be invalidated by the frontend on version mismatch.

---

### REC-6 · MINOR · `product_safe` staleness not handled at API layer

**Location:** Part IV, Section 4 header and all discovery journey queries.

**Problem:** The document states "Rights authority is PostgreSQL — graph visibility flags are
advisory." Discovery queries use `WHERE i.product_safe = true` as the primary filter. If the
graph is stale (sync lag, failed batch), product-unsafe illustrations pass through to the
frontend. There is no API-layer recheck specified.

**Recommendation:** Define an explicit API contract: graph queries return `pg_id` values only
for rights-sensitive entities; the API layer does a batch PostgreSQL lookup of `product_safe`,
`rights`, and activation status before returning results to the frontend. This contract should
appear in NC-GRAPH-002 as a named section.

---

## Area 2: Governance Isolation

### GV-1 · HIGH · Trigger function uses hardcoded `place_id` column

**Location:** Part VIII, Section 8.2, trigger function definition.

**Problem:**

```sql
COALESCE(NEW.place_id, OLD.place_id),  -- adjust per table
```

This function is registered as `nc_queue_graph_change()` and applied to all entity tables via
`CREATE TRIGGER`. A single function referencing `NEW.place_id` will fail when applied to the
artists table (PK column is `artist_id`) or the illustrations table (PK is `illustration_id`).
The comment "adjust per table" acknowledges the problem but leaves it unresolved.

**Correction:** One trigger function per entity type, each referencing the correct PK column:

```sql
-- For places
CREATE OR REPLACE FUNCTION nc_queue_place_change() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO nc_graph_change_queue
    (entity_type, entity_id, pg_table, operation, priority)
  VALUES (
    'place', COALESCE(NEW.place_id, OLD.place_id), 'nc_places', TG_OP,
    CASE WHEN TG_OP = 'DELETE' THEN 1 ELSE 5 END
  );
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- For illustrations — rights field change gets priority 1
CREATE OR REPLACE FUNCTION nc_queue_illustration_change() RETURNS TRIGGER AS $$
DECLARE
  v_priority INTEGER := 5;
BEGIN
  IF TG_OP = 'DELETE'
     OR (TG_OP = 'UPDATE' AND OLD.rights IS DISTINCT FROM NEW.rights)
     OR (TG_OP = 'UPDATE' AND OLD.product_safe IS DISTINCT FROM NEW.product_safe) THEN
    v_priority := 1;
  END IF;
  INSERT INTO nc_graph_change_queue
    (entity_type, entity_id, pg_table, operation, priority, changed_fields)
  VALUES (
    'illustration', COALESCE(NEW.illustration_id, OLD.illustration_id),
    'source_item', TG_OP, v_priority, NULL
  );
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

Each entity table requires its own function referencing the correct PK column.

---

### GV-2 · HIGH · Projection worker does not verify schema_registry before writing derived edges

**Location:** Part VIII, Section 8.3 (Projection Worker Logic); Part IX, Section 9.1 (Schema Registry).

**Problem:** Section 8.3 says the derived_relationship_worker computes PROXIMATE_TO,
CONTEMPORARY_WITH, and CO_OCCURS_WITH automatically when "any place or artist changed."
Section 9.1 says new relationship types require `projection_schema_registry` registration with
`is_active = true`. But the worker pseudocode does not check the registry before writing derived
edges. G-8 is stated as a constraint but has no enforcement in the worker.

**Correction:** Worker logic must add a registry check step before any derived relationship write:

```
BEFORE computing derived relationships:
  SELECT is_active FROM nc_projection_schema_registry
  WHERE label = $relationship_type
    AND entity_type = 'relationship'
    AND schema_version = $active_version;
  IF NOT FOUND OR NOT is_active:
    SKIP and log skipped_relationship_type
```

---

### GV-3 · MEDIUM · G-5 audit is a data check, not a behavioral check

**Location:** Part IX, Section 9.5, G-5 audit query.

**Problem:**

```cypher
MATCH (prod:Product)
WHERE prod.rights IS NOT NULL
RETURN count(prod) AS violation_count
```

G-5 states "Commerce scoring does not consume Neo4j signals." This audit query checks only
that Product nodes don't carry a `rights` property. It cannot detect if a commerce worker
imports the Neo4j driver and reads Product or Illustration nodes for scoring decisions.

The audit verifies a property constraint, not the behavioral invariant.

**Correction:** The behavioral invariant must be enforced in code, not in graph queries:

1. The commerce scoring worker must have a test assertion that it does not import the Neo4j
   driver or any Neo4j client library.
2. The projection_schema_registry should have an `allowed_readers` column listing which
   worker categories may query each node/relationship type — commerce workers not listed.
3. The Cypher audit query is useful as a data sanity check but must be supplemented with the
   behavioral test.

---

### GV-4 · MEDIUM · `director_decision_id` is unvalidated TEXT

**Location:** Part IX, Section 9.1, `nc_projection_schema_registry` table definition.

**Problem:**

```sql
director_decision_id TEXT  -- governance gate
```

This is a free text field. Any string satisfies the column constraint. There is no referential
integrity check that the director decision actually exists in a decisions registry. The governance
gate is bypassed by inserting any non-NULL string.

**Correction:** Create an `nc_director_decisions` table as the governance anchor:

```sql
CREATE TABLE nc_director_decisions (
  decision_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  decision_code  TEXT UNIQUE NOT NULL,  -- e.g. 'SD-AMEND-1', 'NC-GRAPH-003-GV4'
  description    TEXT NOT NULL,
  decided_at     TIMESTAMPTZ NOT NULL,
  decided_by     TEXT NOT NULL,
  document_ref   TEXT NOT NULL          -- e.g. 'NC-GRAPH-002 v1.0'
);

-- Then in schema_registry:
director_decision_id UUID REFERENCES nc_director_decisions (decision_id) NOT NULL
```

---

### GV-5 · MEDIUM · Full rebuild deletes graph before shadow namespace is built

**Location:** Part VIII, Section 8.5, step 3.

**Problem:**

```
3. Clear all non-constraint nodes from Neo4j (MATCH (n) DETACH DELETE n).
```

This step runs before the rebuild is complete. If the rebuild fails at step 4j
(Illustrations — the largest batch), the graph is empty and the incremental worker is frozen.
The platform has no graph discovery for the duration of the rebuild. The prior architecture
document (`neo4j_pgvector_runtime_architecture_v1.md`) noted: "Preferred production pattern:
build into a replacement graph database or schema namespace, verify, then switch the active
alias."

NC-GRAPH-002 dropped this caution without explanation.

**Correction:** Restore the shadow namespace pattern for full rebuilds:

```
3.  [Neo4j Enterprise] Create a new database 'nc_graph_rebuild'. Build into it.
    OR
3.  [Neo4j Community] Set a maintenance flag in PostgreSQL. Serve cached/degraded results
    from the API layer during rebuild. Do not delete the active graph until step 6 passes.
    On validation success, drop old graph and promote rebuilt graph.
```

Document the maintenance window requirement for Community Edition deployments.

---

## Area 3: Rights Isolation

### RI-1 · CRITICAL · Dual rights fields create inconsistency between node and relationship

**Location:** Part II, Section 2.2 (Illustration node); Part III, Section 3.1 (SOURCED_FROM
relationship).

**Problem:** Rights information appears in two places in the graph:

1. `Illustration.rights: STRING` — on the node
2. `Illustration-[:SOURCED_FROM {rights: STRING}]->Institution` — on the relationship

These are populated by different workers at different times. A rights retraction in PostgreSQL
triggers a priority-1 queue entry that updates the Illustration node. But the SOURCED_FROM
relationship is updated by the relationship_upsert_worker, which may run at lower priority.

During the sync window, `Illustration.rights = 'InC'` (retracted) but
`Illustration-[:SOURCED_FROM].rights = 'CC0'` (stale). A query reading the relationship's
rights field will incorrectly show the illustration as available.

There is no audit query in Section 9.5 that checks for this divergence.

**Correction:**

1. Remove `rights` and `rights_matrix_version` from the SOURCED_FROM relationship. Rights
   belong on the Illustration node only (where they are the advisory display field).
2. Add to the Section 9.5 audit:

```cypher
// RI-1 check: SOURCED_FROM relationship must not carry rights fields
MATCH ()-[r:SOURCED_FROM]->()
WHERE r.rights IS NOT NULL
RETURN count(r) AS stale_rights_on_relationship
// Expected: 0 rows after schema correction
```

---

### RI-2 · CRITICAL · `shopify_variant_id` on Product node creates G-5 violation pathway

**Location:** Part II, Section 2.2, Product node definition.

**Problem:**

```cypher
(:Product {
  ...
  shopify_variant_id: STRING,
  ...
})
```

Shopify variant IDs are direct commerce transaction identifiers. If a downstream system reads
`shopify_variant_id` from a Neo4j Product node and passes it to the Shopify cart API, it has
executed a commerce transaction using a graph-sourced value, bypassing the PostgreSQL authority
check. G-1 states no application writes directly to Neo4j, but the deeper concern is G-5:
commerce decisions must not flow through graph data.

A stale `shopify_variant_id` (Shopify variant was deleted and recreated in PostgreSQL but the
graph hasn't synced) would cause a cart addition to fail or add the wrong product.

**Correction:** Remove `shopify_variant_id` from the Product node. Commerce transactions must
read the Shopify variant ID from PostgreSQL at transaction time. The graph Product node exists
for discovery traversal only; it should not carry any identifier that can trigger a commerce
action.

Revised Product node:

```cypher
(:Product {
  product_id:       STRING,
  nc_product_id:    STRING,   // 'NC-PROD-001' — display identifier only
  name:             STRING,
  product_line:     INTEGER,
  status:           STRING,   // advisory display signal
  // price_usd: REMOVED — see RI-3
  // shopify_variant_id: REMOVED — commerce transaction identifier
  ...provenance
})
```

---

### RI-3 · HIGH · `price_usd` in graph creates stale pricing risk

**Location:** Part II, Section 2.2, Product node (`price_usd`) and Collection node
(`price_from_usd`).

**Problem:** Prices in the graph become stale whenever Shopify prices are updated.
The sync pipeline updates the Product node on PostgreSQL change, but there is a window
during which the graph shows an old price. If the discovery API returns prices from the
graph directly to the frontend, the user sees incorrect pricing. Depending on jurisdiction,
displaying a different price than the actual charged price is a consumer protection issue.

Additionally, having `price_from_usd` on the Collection node creates a second stale pricing
point for collection pages.

**Correction:** Remove `price_usd` from the Product node. Remove `price_from_usd` from the
Collection node. Pricing must be fetched from PostgreSQL (or Shopify directly) at display time.
The graph is for discovery traversal; it is not a product catalog or price display system.

---

### RI-4 · HIGH · Denormalized counters not decremented on Illustration DELETE

**Location:** Part VIII, Section 8.3 (worker step f); Part II, node definitions with
`illustration_count` fields.

**Problem:** When an Illustration node is DETACH DELETEd from Neo4j (rights retraction, G-4),
the following denormalized counters become stale:

- `Place.illustration_count` (for each associated place)
- `Artist.illustration_count` (for the creating artist)
- `Taxon.illustration_count` (for each depicted taxon)
- `Collection.illustration_count` (for each collection it was in)
- `Expedition.illustration_count` (for any associated expedition)

These counters are used in discovery ordering (`ORDER BY illustration_count DESC`). An artist
or place showing `illustration_count = 5` when 2 illustrations have been retracted will rank
incorrectly in discovery.

The worker pseudocode handles the DELETE case (step f: "DETACH DELETE node from Neo4j") but
does not update related node counters.

**Correction:** Add a counter update step after Illustration DELETE:

```
f. If operation = 'DELETE':
   1. Before DETACH DELETE, fetch all related entity IDs from the node:
      - associated place_ids via ASSOCIATED_WITH
      - artist_ids via CREATED_BY
      - taxon_ids via DEPICTS
      - collection_ids via IN_COLLECTION
   2. DETACH DELETE the illustration node
   3. For each related entity: decrement illustration_count by 1 in Neo4j
      (MATCH (n {entity_id: $id}) SET n.illustration_count = n.illustration_count - 1)
   4. Enqueue PostgreSQL counter refresh for the same entities
```

---

### RI-5 · HIGH · `has_active_product` as ORDER BY signal needs explicit governance ruling

**Location:** Part II, Section 2.2, Illustration node; Part IV, Section 4.1, Journey 1.

**Problem:** Discovery queries rank illustrations by product availability:

```cypher
ORDER BY i.has_active_product DESC, i.year DESC
```

G-5 states "Commerce scoring does not consume Neo4j signals." The intent was: Neo4j signals
must not flow into commerce scoring. The concern in RI-5 is the reverse direction: a commerce
signal (`has_active_product`) flows into graph-based discovery ranking.

This is arguably permitted under G-5 as written (G-5 prohibits Neo4j→Commerce, not
Commerce→Neo4j). But it creates a coupling between the commerce layer and the discovery layer
that should be explicitly governed.

**Correction:** One of two approaches, both acceptable:

Option A (explicit permission): Add a note to G-5 in NC-GRAPH-002:
> "G-5 permits commerce state (has_active_product, product status) to appear as advisory
> display signals in the graph. It prohibits graph signals from feeding into commerce scoring.
> Direction is: PostgreSQL commerce state → graph display advisory; graph → commerce: BLOCKED."

Option B (remove from graph): Remove `has_active_product` from the Illustration node and
handle the ranking in the API rehydration layer, where it can read live product status from
PostgreSQL without graph involvement.

---

## Area 4: PostgreSQL Authority Preservation

### PA-1 · HIGH · No API rehydration layer specification

**Location:** Part IV, Section 4 header: "All queries return canonical `pg_id` values for API
rehydration from PostgreSQL."

**Problem:** The stated contract is "all queries return `pg_id` for rehydration." But the
Cypher queries in Sections 4–7 return full node objects, not just IDs. For example,
Journey 7 (Knowledge Panel):

```cypher
RETURN p,                           // full Place node with all properties
       collect(DISTINCT t) AS top_taxa,    // full Taxon nodes
       collect(DISTINCT a) AS top_artists  // full Artist nodes
```

If the API layer returns these graph-sourced node properties directly to the frontend, it has
bypassed the PostgreSQL authority recheck. This is tolerable for display-only fields (name,
year, color) but is incorrect for rights, commerce status, and activation state.

The document states the principle but does not define the boundary: which properties may be
served directly from graph nodes, and which must be rehydrated from PostgreSQL?

**Correction:** Define an explicit API data contract:

```
From Neo4j (may serve directly — display metadata only):
  - name, canonical_name, title, year, year_circa
  - color_primary, color_palette
  - fcode, country_code, centroid_lat, centroid_lng
  - nc_priority, priority_rank, domain
  - reason_code, reason_text
  - All provenance fields (pg_id, pg_table, projected_at)

Must rehydrate from PostgreSQL before serving to frontend:
  - rights (all forms)
  - product_safe, has_active_product
  - status (Collection, Product, Story)
  - price_usd (all forms — remove from graph per RI-3)
  - shopify_variant_id (remove from graph per RI-2)
  - Any field ending in _count that gates display decisions
```

Add this contract as Section 10 (API Rehydration Contract) in NC-GRAPH-002.

---

### PA-2 · HIGH · PostGIS geometry change does not trigger PROXIMATE_TO recomputation

**Location:** Part VIII, Section 8.3 (worker step 3); Part III, Section 3.2 (PROXIMATE_TO).

**Problem:** The worker recomputes derived relationships "IF any place or artist changed."
But PROXIMATE_TO edges are computed from PostGIS centroids (`ST_DWithin(centroid::geography, ...)`).
The centroid is stored as `centroid_lat / centroid_lng` in the Place node — derived from the
PostGIS `centroid GENERATED ALWAYS AS (ST_Centroid(geom)) STORED` column.

If the PostGIS `geom` column for a place is corrected (e.g., NC-DATA-001 corrected Yellowstone's
GeoNames ID, which would update its canonical geometry), the trigger must fire on the
`nc_places.geom` column change, not just on metadata changes.

The current trigger:
```sql
CREATE TRIGGER nc_places_graph_sync
AFTER INSERT OR UPDATE OR DELETE ON nc_places
FOR EACH ROW EXECUTE FUNCTION nc_queue_place_change();
```

This fires on any `UPDATE`. Good. But the trigger function must mark geometry changes as
requiring PROXIMATE_TO recomputation specifically. The current worker logic only checks
"any place changed" — it doesn't distinguish between a name change (no recomputation needed)
and a geometry change (full PROXIMATE_TO recomputation needed for that place).

**Correction:** Add a `requires_spatial_recompute: BOOLEAN` flag to the change queue:

```sql
-- In trigger function
IF TG_OP = 'UPDATE' AND (
  OLD.geom IS DISTINCT FROM NEW.geom OR
  OLD.geonames_id IS DISTINCT FROM NEW.geonames_id
) THEN
  v_requires_spatial_recompute := true;
END IF;
```

Worker checks this flag before running PostGIS queries, skipping the expensive ST_DWithin
computation for non-geometry changes.

---

### PA-3 · MEDIUM · Denormalized counters have no specified update trigger

**Location:** Part II, all node definitions carrying `*_count` fields (13 denormalized counters
across 7 node types).

**Problem:** The projection worker upserts node properties from PostgreSQL. But
`Place.illustration_count`, `Artist.illustration_count`, `Collection.illustration_count`, and
similar fields must be kept current as entities are added, retracted, or removed. The blueprint
does not specify when and how these counters are recalculated.

Discovery ordering (`ORDER BY illustration_count DESC`, `ORDER BY place_overlap DESC`) is
incorrect if counters are stale. A place showing 0 illustrations because the counter was never
initialized will never surface in discovery.

**Correction:** Define the counter update strategy explicitly:

```
Option A — Recompute on projection (recommended for small scale):
  After upserting any node, run a counter refresh query:
  MATCH (p:Place {place_id: $id})
  SET p.illustration_count = COUNT { (:Illustration)-[:ASSOCIATED_WITH|DEPICTS*1..2]->(p) }
  
  Run this after every Illustration upsert/delete for all connected places.

Option B — Batch refresh (acceptable for < 1,000 places):
  After every full batch completion, run counter refresh for all affected nodes.
  Accept stale counts within a single batch window (~15 min).
```

Select one option and document it in Section 8.3.

---

### PA-4 · MEDIUM · AI-generated text in graph has no defined regeneration trigger or approval gate

**Location:** Part II, Section 2.2, Illustration node (`ai_description`, `ai_description_run_id`);
Collection node (`ai_synopsis`, `ai_synopsis_run_id`); Part VII, Section 7.2, AI-G3/AI-G4.

**Problem:** `ai_description` and `ai_synopsis` are stored in Neo4j nodes. AI-G4 says these
must carry `_run_id` for traceability. But:

1. Where is the authoritative copy? If it's PostgreSQL (as G-1 requires), the graph carries
   a derived copy — but there's no PostgreSQL table defined for AI-generated text.
2. When is `ai_description` regenerated? If the associated Artist, Taxon, or Place changes
   (e.g., a new illustration is added to a place), the editorial context changes but
   `ai_description` on existing illustrations would not be regenerated.
3. Who approves AI-generated text before it appears in `ai_description`? NC-AI-001 requires
   AI-generated editorial content to be human-approved. There is no approval workflow here.

**Correction:** Before storing AI-generated text in the graph:

1. Define the authoritative PostgreSQL table: `nc_ai_generated_content` with columns
   `entity_id`, `entity_type`, `field_name`, `content`, `run_id`, `approved_by`, `approved_at`.
2. Define the regeneration trigger: AI description is regenerated when the `ground_context`
   query for that entity would return different data than when the existing description was
   generated (detectable via context query hash change — per AI-G3).
3. Define the approval gate: AI-generated text is written to the graph only after
   `approved_at IS NOT NULL` in the PostgreSQL record. The projection worker copies approved
   text to the graph node; unapproved text stays in PostgreSQL only.

---

### PA-5 · MINOR · PART_OF_EXPEDITION ambiguity should be documented

**Location:** Part III, Appendix B (Relationship Summary Table); Part VIII, Section 8.5.

**Problem:** `PART_OF_EXPEDITION` is used for both `Illustration → Expedition` and
`Artist → Expedition`. Cypher queries that match `(n)-[:PART_OF_EXPEDITION]->(e)` without
a label on `n` will match both types. Journey 5 handles this correctly with separate MATCH
clauses, but any developer writing a new query against the graph could inadvertently match
both directions.

Additionally, the Full Rebuild sequence step 4e states:
> "Expeditions (depends on places + artists)"

Expedition nodes do not depend on artists — they have no required fields from Artist. It is the
`PART_OF_EXPEDITION` relationships that create the dependency, not the Expedition node itself.

**Correction:**

1. Add a note to the relationship model: "PART_OF_EXPEDITION is shared across Illustration and
   Artist source nodes. All queries traversing this relationship must specify the source label:
   `(i:Illustration)-[:PART_OF_EXPEDITION]->` or `(a:Artist)-[:PART_OF_EXPEDITION]->`."

2. Correct the Full Rebuild sequence:
   ```
   4e. Expeditions (no FK dependencies — Expedition nodes only)
       [After all Illustrations and Artists are loaded:]
   4f. PART_OF_EXPEDITION relationships from Illustrations → Expeditions
   4g. PART_OF_EXPEDITION relationships from Artists → Expeditions
   ```

---

## Resolution Matrix

| ID | Area | Severity | Location | Status |
|---|---|---|---|---|
| RI-1 | Rights | **CRITICAL** | Part III §3.1 SOURCED_FROM | Open |
| RI-2 | Rights | **CRITICAL** | Part II §2.2 Product node | Open |
| GV-1 | Governance | **HIGH** | Part VIII §8.2 trigger function | Open |
| REC-1 | Recommendations | **HIGH** | Part V §5.2 deduplication | Open |
| REC-2 | Recommendations | **HIGH** | Part V §5.2 Signal 2 & 3 | Open |
| RI-3 | Rights | **HIGH** | Part II §2.2 price fields | Open |
| RI-4 | Rights | **HIGH** | Part VIII §8.3 step f | Open |
| RI-5 | Rights | **HIGH** | Part II §2.2 / Part IV §4.1 | Open |
| PA-1 | PG Authority | **HIGH** | Part IV header / §4.7 | Open |
| PA-2 | PG Authority | **HIGH** | Part VIII §8.3 | Open |
| GV-2 | Governance | **HIGH** | Part VIII §8.3 / Part IX §9.1 | Open |
| REC-3 | Recommendations | **MEDIUM** | Part IV §4.4 | Open |
| REC-4 | Recommendations | **MEDIUM** | Part IV §4.3 | Open |
| GV-3 | Governance | **MEDIUM** | Part IX §9.5 | Open |
| GV-4 | Governance | **MEDIUM** | Part IX §9.1 | Open |
| GV-5 | Governance | **MEDIUM** | Part VIII §8.5 | Open |
| PA-3 | PG Authority | **MEDIUM** | Part II node definitions | Open |
| PA-4 | PG Authority | **MEDIUM** | Part II §2.2 / Part VII §7.2 | Open |
| PA-5 | PG Authority | **MINOR** | Part III Appendix B / Part VIII §8.5 | Open |
| REC-5 | Recommendations | **MINOR** | Part V §5.1 | Open |

---

## Ratification Gate

NC-GRAPH-002 may not be ratified until the following are resolved:

**Critical (3):**
- RI-1: Remove `rights` from SOURCED_FROM relationship
- RI-2: Remove `shopify_variant_id` from Product node
- GV-1: Separate trigger functions per entity type with correct PK column

**Required before implementation (7):**
- REC-1: Fix deduplication query
- REC-2: Signal 2 and 3 → OPTIONAL MATCH
- RI-3: Remove `price_usd` from Product and `price_from_usd` from Collection
- RI-4: Specify counter decrement on Illustration DELETE
- RI-5: Explicit G-5 directional ruling on `has_active_product`
- PA-1: Define API rehydration contract (which fields may be served from graph)
- PA-2: PostGIS geometry change → PROXIMATE_TO recomputation trigger
- GV-2: Schema registry check in projection worker before derived edge writes

Recommend: incorporate all critical and high findings into NC-GRAPH-002 v1.1 before
ratification vote. Medium findings can be addressed in Sprint 1 implementation PRs.

---

*NC-GRAPH-003 · v1.0 · 2026-06-13 · DRAFT*
