# Asset Intelligence Optimization Runtime v1

## Mission

Design an additive Asset Intelligence runtime for improving asset-class,
creator, and place signal quality without redesigning Commerce Intelligence or
Product Routing.

This design uses Asset Coverage Audit v1 as its boundary: BHL illustrations are
the only asset class with implemented ingestion-to-publication traversal today;
LOC maps and historical photography need future bridge work before they can
traverse the same runtime from ingestion.

## Runtime Boundary

Asset Intelligence is a signal authority layer upstream of Commerce
Intelligence scoring and downstream of ingestion/discovery.

```text
ingestion / discovery
  -> asset intelligence registries
  -> commerce_opportunity_worker
  -> commerce_opportunities.score_inputs
  -> product_routing_worker
  -> catalog_intelligence_worker
  -> publication_worker
```

Allowed:

- Normalize `anchor_type`.
- Resolve creator identity and creator authority.
- Resolve creator prestige.
- Resolve place-iconic taxa.
- Write replayable registry resolution snapshots.
- Mark dependent commerce/catalog/publication records stale when registry
  versions change.

Not allowed:

- No change to Commerce Intelligence formulas.
- No change to Product Routing policy or route thresholds.
- No external provider routing.
- No catalog publication or execution.
- No worker-local hardcoded authority lists once registry data is available.

PostgreSQL remains authoritative for all registry records, resolved signals, and
replay snapshots.

## Design Principles

1. Registries are versioned and independently governed.
2. Active registry rows require second-human approval.
3. Workers may read only active registry versions for new computation.
4. Replay uses the registry rows pinned in the original input snapshot, not the
   current active rows.
5. Registry changes do not rewrite historical scores; they mark downstream
   records stale or require recompute.
6. Product Routing consumes the existing `commerce_opportunities` fields only.
7. Catalog and Publication consume registry-derived signals through upstream
   snapshots, not by re-scoring assets.

## Registries

### anchor_type support

`anchor_type` is already represented as `commerce_anchor_type_vocabulary`
(`biological`, `geographic`, `cultural`) but is not yet attached to the runtime
commerce input record. Additive support should introduce a governed
`anchor_type` field on the commerce input surface.

Recommended migration shape:

```sql
ALTER TABLE illustration_opportunities
  ADD COLUMN anchor_type TEXT
  REFERENCES commerce_anchor_type_vocabulary(value);
```

Recommended defaulting:

- `bhl` taxon-driven illustration opportunities default to `biological`.
- LOC maps default to `geographic` when bridged into the commerce pathway.
- Historical photographs default only when a source adapter can justify
  `geographic` or `cultural` from metadata.
- Unknown anchor type must not be guessed for non-BHL sources; it should block
  scoring or remain `not_evaluated` until reviewed.

Replay contract:

```json
{
  "anchor_type": "biological",
  "anchor_type_source": "illustration_opportunities.anchor_type",
  "anchor_type_registry_version": "commerce_anchor_type_vocabulary:v1"
}
```

### creator_authority_registry

`creator_authority_registry` resolves creator names to a stable governed creator
identity. It is not a prestige table. It answers: who is this creator, how was
the identity resolved, and how trustworthy is the attribution?

Recommended table:

```sql
CREATE TABLE creator_authority_registry (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    registry_version      TEXT NOT NULL,
    canonical_creator_key TEXT NOT NULL,
    display_name          TEXT NOT NULL,
    normalized_names      TEXT[] NOT NULL DEFAULT '{}',
    external_authorities  JSONB NOT NULL DEFAULT '{}',
    creator_roles         TEXT[] NOT NULL DEFAULT '{}',
    authority_confidence  NUMERIC(4,3) NOT NULL CHECK (authority_confidence BETWEEN 0 AND 1),
    attribution_risk      TEXT NOT NULL CHECK (attribution_risk IN ('low','medium','high','unknown')),
    status                TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by           TEXT NOT NULL,
    approved_by           TEXT,
    approved_at           TIMESTAMPTZ,
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (registry_version, canonical_creator_key),
    CONSTRAINT chk_creator_authority_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    )
);
```

Recommended supporting table for name matching:

```sql
CREATE TABLE creator_authority_aliases (
    id                   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    creator_authority_id UUID NOT NULL REFERENCES creator_authority_registry(id),
    alias                TEXT NOT NULL,
    normalized_alias     TEXT NOT NULL,
    alias_source         TEXT NOT NULL,
    confidence_score     NUMERIC(4,3) NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    provenance           JSONB NOT NULL DEFAULT '{}',
    UNIQUE (creator_authority_id, normalized_alias)
);
```

Replay contract:

```json
{
  "creator_authority": {
    "registry_id": "uuid",
    "registry_version": "2026.06.0",
    "canonical_creator_key": "john-james-audubon",
    "display_name": "John James Audubon",
    "authority_confidence": 0.98,
    "attribution_risk": "medium",
    "matched_alias": "Audubon"
  }
}
```

### creator_prestige_registry

`creator_prestige_registry` replaces worker-local prestige lists as the
PostgreSQL authority for `illustrator_prestige`. It can be seeded from the
existing `priority_illustrators_vocabulary`, but the runtime should treat it as
creator-scoped, versioned intelligence rather than a substring list.

Recommended table:

```sql
CREATE TABLE creator_prestige_registry (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    registry_version      TEXT NOT NULL,
    creator_authority_id  UUID NOT NULL REFERENCES creator_authority_registry(id),
    prestige_score        NUMERIC(4,3) NOT NULL CHECK (prestige_score BETWEEN 0 AND 1),
    prestige_tier         TEXT NOT NULL CHECK (prestige_tier IN ('master','major','notable','standard','none')),
    prestige_rationale    TEXT NOT NULL,
    applies_to_anchor_types TEXT[] NOT NULL DEFAULT ARRAY['biological','geographic','cultural'],
    status                TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by           TEXT NOT NULL,
    approved_by           TEXT,
    approved_at           TIMESTAMPTZ,
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (registry_version, creator_authority_id),
    CONSTRAINT chk_creator_prestige_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    )
);
```

Replay contract:

```json
{
  "creator_prestige": {
    "registry_id": "uuid",
    "registry_version": "2026.06.0",
    "prestige_score": 1.0,
    "prestige_tier": "master",
    "prestige_rationale_hash": "sha256"
  }
}
```

### place_iconic_taxa_registry

`place_iconic_taxa_vocabulary` already exists. This design formalizes it as the
place-iconic taxa registry consumed by Asset Intelligence. A future migration
may rename it or create a compatibility view named
`place_iconic_taxa_registry`; the authoritative behavior should remain row-level
governance with active/retired lifecycle and second-human approval.

Recommended additive columns if the current table is extended:

```sql
ALTER TABLE place_iconic_taxa_vocabulary
  ADD COLUMN IF NOT EXISTS registry_version TEXT NOT NULL DEFAULT '1.0.0',
  ADD COLUMN IF NOT EXISTS taxon_key TEXT,
  ADD COLUMN IF NOT EXISTS iconic_rationale TEXT,
  ADD COLUMN IF NOT EXISTS authority_confidence NUMERIC(4,3)
      CHECK (authority_confidence IS NULL OR authority_confidence BETWEEN 0 AND 1);
```

Replay contract:

```json
{
  "place_iconic_taxa": {
    "registry_id": "uuid",
    "registry_version": "2026.06.0",
    "place_id": "uuid",
    "scientific_name": "Acanthaster planci",
    "iconic_score": 0.91
  }
}
```

## Resolved Signal Snapshot

Introduce an append-only or immutable-after-write resolution table so registry
inputs can be replayed independently of current active registry state.

Recommended table:

```sql
CREATE TABLE asset_intelligence_signal_snapshots (
    id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id             UUID NOT NULL REFERENCES illustration_opportunities(id),
    resolved_at                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_by                TEXT NOT NULL,
    registry_version_set       JSONB NOT NULL,
    anchor_type                TEXT REFERENCES commerce_anchor_type_vocabulary(value),
    creator_authority_id       UUID REFERENCES creator_authority_registry(id),
    creator_prestige_id        UUID REFERENCES creator_prestige_registry(id),
    place_iconic_taxa_id       UUID REFERENCES place_iconic_taxa_vocabulary(id),
    resolved_signals           JSONB NOT NULL,
    input_snapshot             JSONB NOT NULL,
    input_hash_sha256          TEXT NOT NULL,
    provenance                 JSONB NOT NULL DEFAULT '{}',
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (opportunity_id, input_hash_sha256)
);
```

Minimum `resolved_signals`:

```json
{
  "anchor_type": "biological",
  "creator_authority_confidence": 0.98,
  "creator_attribution_risk": "medium",
  "illustrator_prestige": 1.0,
  "taxon_place_iconic": 0.91,
  "requires_curator_review": true,
  "curator_review_reason": "priority_illustrator"
}
```

`commerce_opportunities.score_inputs` must embed the registry snapshot IDs and
resolved signal values used for scoring. This is the replay boundary.

## Worker Integration

### commerce_opportunity_worker

The commerce worker is the primary integration point. It should enrich
`build_input_snapshot` with registry-derived values before calling
`compute_scores`.

Current behavior:

- `illustrator_prestige` is derived from score components and a hardcoded
  priority-name tuple.
- `taxon_place_iconic` falls back to place relevance.
- LOC sources require curator review by default.
- `anchor_type` is not present on the opportunity input surface.

Designed behavior:

1. Claim approved `illustration_opportunities` as today.
2. Load active registry rows matching the opportunity:
   creator aliases, creator authority, creator prestige, anchor type, and
   place-iconic taxa.
3. Write or reuse an `asset_intelligence_signal_snapshots` row.
4. Build `score_inputs` from the resolved snapshot.
5. Continue using the existing `compute_scores` function and existing
   `commerce_policy` formula.
6. Write `commerce_opportunities` and `score_audit_log` as today, with registry
   snapshot IDs included inside `score_inputs`.

No Product Routing field changes are required. Existing fields remain:

- `illustrator_prestige`
- `taxon_place_iconic`
- `requires_curator_review`
- `curator_review_reason`
- `score_inputs`
- `input_hash_sha256`

Replay behavior:

- `commerce_replay_worker` must replay against the `score_inputs` stored in
  `score_audit_log`.
- It must not resolve current registry rows during replay.
- If the same `score_inputs` reproduce the same `score_outputs`, replay passes
  even if registry rows have since changed.

Staleness behavior:

- Retiring or superseding a creator authority, creator prestige, or iconic-taxa
  row should not mutate existing commerce rows.
- A registry-change job should mark affected `commerce_opportunities.policy_stale
  = TRUE` or create a `signal_updated` / `policy_version_change` audit event,
  depending on governance choice.
- Recompute uses the then-active registry rows and writes a new audit entry.

### catalog_intelligence_worker

Catalog Intelligence should not independently resolve creator prestige or
place-iconic taxa. It should consume the registry-derived values already pinned
on `commerce_opportunities` and expose them in internal catalog metadata.

Designed behavior:

1. Claim curator-approved product recommendations as today.
2. Read parent `commerce_opportunities` fields and `score_inputs`.
3. Copy registry summary into `catalog_candidates.source_snapshot` or
   `catalog_basis`.
4. Use existing catalog policy and variant rules unchanged.
5. Preserve internal-only constraints: no providers, no external IDs, no catalog
   publication.

Recommended catalog snapshot fields:

```json
{
  "asset_intelligence": {
    "anchor_type": "biological",
    "creator_authority_key": "john-james-audubon",
    "creator_authority_confidence": 0.98,
    "creator_prestige_score": 1.0,
    "creator_prestige_tier": "master",
    "place_iconic_taxa_score": 0.91,
    "registry_snapshot_id": "uuid"
  }
}
```

Catalog pricing may continue using the existing `csm_score`-based prestige
multiplier. This design does not require catalog pricing formulas to change.
If a future catalog policy wants creator-aware pricing, it should do so through
catalog policy versioning, not through hidden worker logic.

Replay behavior:

- `catalog_replay` must compare generated candidate and variant output against
  the stored catalog input snapshot.
- It must not re-resolve current creator or place registries.

Staleness behavior:

- If a parent commerce opportunity is marked stale due to registry change,
  catalog candidates derived from it should be marked stale/superseded by a
  downstream governance job or excluded from new publication claims.

### publication_worker

Publication Intelligence should treat Asset Intelligence as contextual planning
metadata, not a new scoring authority. It should not recalculate Commerce
Intelligence or Catalog Intelligence values.

Designed behavior:

1. Claim draft or approved catalog candidates and variants as today.
2. Read registry summaries from the catalog candidate snapshot and parent
   commerce score inputs.
3. Include registry summary in `publication_candidates.input_snapshot` and
   `decision_basis`.
4. Use existing publication readiness, channel fit, risk, and ranking rules
   unchanged.
5. Continue producing internal publication candidates only.

Recommended publication snapshot fields:

```json
{
  "asset_intelligence": {
    "anchor_type": "geographic",
    "creator_attribution_risk": "low",
    "creator_authority_confidence": 0.94,
    "creator_prestige_tier": "major",
    "place_iconic_taxa_score": null,
    "registry_snapshot_id": "uuid"
  }
}
```

Publication policy can later choose to treat attribution risk as a risk signal,
but that requires a publication policy version change. The worker must not add
unversioned risk logic.

Replay behavior:

- `publication_replay_worker` must replay from stored publication inputs.
- It must not re-query active registry rows.

Staleness behavior:

- If catalog or commerce parents become stale from registry change,
  `publication_worker.is_publication_stale` should treat the upstream stale flag
  as authoritative.
- Registry changes should cascade by staleness marking, not by mutating existing
  publication candidate decisions.

## Integration Summary

| Registry | Commerce worker | Catalog worker | Publication worker |
| --- | --- | --- | --- |
| `anchor_type` | Reads active value and embeds it in `score_inputs`; required for LOC and non-biological future assets. | Copies value from commerce snapshot for catalog context. | Copies value from catalog or commerce snapshot for publication context. |
| `creator_authority_registry` | Resolves creator identity and attribution confidence before scoring. | Carries authority key/confidence into `source_snapshot` or `catalog_basis`. | Carries authority key/confidence into `input_snapshot` and `decision_basis`. |
| `creator_prestige_registry` | Produces `illustrator_prestige` without hardcoded lists. | May expose prestige tier for catalog metadata; no hidden pricing change. | May expose prestige tier for planning metadata; no hidden risk/ranking change. |
| `place_iconic_taxa_registry` | Produces `taxon_place_iconic` for Tourism scoring. | Carries iconic score into catalog context. | Carries iconic score into planning context. |

## Required Future Migrations

- Add `illustration_opportunities.anchor_type` with a foreign key to
  `commerce_anchor_type_vocabulary`.
- Create `creator_authority_registry`.
- Create `creator_authority_aliases`.
- Create `creator_prestige_registry`.
- Extend or alias `place_iconic_taxa_vocabulary` as
  `place_iconic_taxa_registry` with registry version, rationale, and confidence
  fields.
- Create `asset_intelligence_signal_snapshots`.
- Add stale-marking/audit support for registry changes affecting scored
  commerce opportunities.
- Seed and activate initial BHL creator authority/prestige rows through
  second-human approval.
- Seed and activate place-iconic taxa rows for the first supported places.

## Non-Goals

- No changes to Product Routing policy.
- No changes to Product Routing worker input requirements.
- No replacement of `commerce_policy` formulas.
- No external provider routing.
- No catalog execution.
- No publication execution.
- No attempt to make LOC maps or historical photography traverse runtime without
  the bridge migrations identified in Asset Coverage Audit v1.

## Conclusion

Asset Intelligence should be implemented as a PostgreSQL-authoritative,
versioned signal-resolution layer. The only scoring worker integration that
changes behavior is `commerce_opportunity_worker`, which should resolve and pin
registry-derived signals before invoking existing Commerce Intelligence scoring.

`catalog_intelligence_worker` and `publication_worker` should consume those
signals as immutable upstream context. They should not re-resolve registries, and
they should not introduce hidden scoring, pricing, routing, or publication
logic. This preserves replay safety while improving asset intelligence quality
for the currently supported BHL illustration path and for future LOC/map/photo
bridges.
