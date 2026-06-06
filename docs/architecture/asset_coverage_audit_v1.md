# Asset Coverage Audit v1

## Scope

This audit reviews implemented migrations 19 through 31 and these workers:

- `commerce_opportunity_worker`
- `commerce_replay_worker`
- `product_routing_worker`
- `catalog_intelligence_worker`
- `publication_worker`
- `publication_replay_worker`

It answers which asset classes can traverse the implemented runtime today. It
does not redesign the runtime.

## Runtime Boundary Observed

The implemented commerce runtime is anchored on `illustration_opportunities`.
Migration 19 expands `illustration_opportunities.source` to allow `bhl` and
`loc`, but migrations 21, 23, 27, and 30 keep downstream foreign keys pointed at
`illustration_opportunities.id`.

The worker chain is:

```text
illustration_opportunities
  -> commerce_opportunities
  -> score_audit_log
  -> product_recommendations
  -> catalog_candidates
  -> catalog_variants
  -> publication_candidates
```

Provider routing is not implemented in migrations 19 through 31. The existing
provider routing document is architecture only, and there are no implemented
provider routing migrations, runtime tables, workers, or replay workers.

Fresh migration state is also not self-running. Migrations 20, 24, 28, and 31
seed policies as `draft`; the workers require `active` policies. Successful
runtime traversal therefore requires governance activation of the relevant
policy plus the existing curator approval gates.

## Supported Asset Matrix

Legend:

- Yes: implemented runtime path exists.
- Conditional: implemented path exists only after required policy or human
  approval gates are satisfied.
- Partial: implemented support exists for an earlier or narrower stage, but not
  for full runtime traversal.
- No: no implemented runtime support in migrations 19 through 31 and reviewed
  workers.

| Asset class | Ingestion support | Scoring support | Routing support | Catalog support | Publication support | Provider-routing support |
| --- | --- | --- | --- | --- | --- | --- |
| BHL illustration (`assets.asset_type = 'bhl_illustration'`, `illustration_opportunities.source = 'bhl'`) | Yes. BHL illustration discovery creates `illustration_opportunities`; BHL asset ingestion creates linked source assets after Public Domain or CC0 rights verification. | Conditional. `commerce_opportunity_worker` claims approved illustration opportunities and computes scores when an active `commerce_policy` exists. | Conditional. `product_routing_worker` routes approved, passed, non-stale, non-blocked commerce opportunities when an active `product_routing_policy` exists. | Conditional. `catalog_intelligence_worker` creates internal catalog candidates and variants from curator-approved product recommendations when an active `catalog_policy` exists. | Conditional. `publication_worker` creates internal publication candidates from draft or approved catalog candidates and variants when an active `publication_policy` and channel profiles exist. | No. Provider routing is architecture-only and has no implemented migration or worker. |
| LOC historic map (`asset_class = 'map'`, `asset_subclass = 'historic_map'`) | Partial. Migration 18 and `loc_maps_asset_worker` create LOC map candidate and rights-evidence proof data for the Hayden map. They do not create a linked `illustration_opportunities` row or a normalized asset-to-commerce bridge. | No for ingested map records. The commerce worker only claims `illustration_opportunities`. LOC fixture/manual rows can be scored if inserted as approved illustration opportunities, but LOC map candidate rows cannot traverse scoring directly. | No for ingested map records. Product routing requires `commerce_opportunities`, which require upstream scoring from an illustration opportunity. | No for ingested map records. Catalog requires curator-approved `product_recommendations`. | No for ingested map records. Publication requires catalog candidates and variants. | No. Provider routing is not implemented. |
| Historical photography | No. There is benchmark and validation-dataset coverage, but no implemented photography ingestion worker or migration-backed runtime table feeding commerce. | No for runtime ingestion. Scoring logic can evaluate manually constructed approved `illustration_opportunities`, but there is no photography ingestion path into that table. | No for runtime ingestion. Routing depends on scored commerce opportunities. | No for runtime ingestion. Catalog depends on routed product recommendations. | No for runtime ingestion. Publication depends on catalog variants. | No. Provider routing is not implemented. |
| Generic LOC illustration opportunity (`illustration_opportunities.source = 'loc'`) | Partial. Migration 19 permits `source = 'loc'`, and the commerce input builder has LOC scoring defaults. No reviewed worker creates LOC illustration opportunities. | Conditional only for manually inserted and approved LOC illustration opportunities. | Conditional only after manual LOC opportunity scoring plus curator approval. | Conditional only after product recommendation curator approval. | Conditional only after catalog generation. | No. Provider routing is not implemented. |
| Non-BHL, non-LOC visual assets | No. Migration 19 constrains `illustration_opportunities.source` to `bhl` or `loc`. | No. The commerce worker claims only approved `illustration_opportunities`, and the source constraint excludes other sources. | No. | No. | No. | No. |
| Non-visual/document assets | No. The reviewed runtime is commerce intelligence for visual illustration opportunities. Documents are registered as possible LOC source entity types in migration 18, but no document ingestion-to-commerce path exists. | No. | No. | No. | No. | No. |

## What Can Traverse Today

The only asset class with a complete implemented path from ingestion into the
reviewed runtime is BHL illustration, subject to these gates:

1. BHL discovery must create an `illustration_opportunities` row.
2. The opportunity must be human-approved.
3. BHL asset ingestion must link a source asset and rights record for Public
   Domain or CC0 material.
4. `commerce_policy` must be activated.
5. `commerce_opportunity_worker` must compute a passed, non-blocked commerce
   opportunity.
6. A human curator must approve the commerce opportunity.
7. `product_routing_policy` must be activated.
8. `product_routing_worker` must create product recommendations.
9. A human curator must approve the product recommendation.
10. `catalog_policy` must be activated.
11. `catalog_intelligence_worker` must create internal catalog candidates and
    variants.
12. `publication_policy` must be activated and channel profiles must be usable.
13. `publication_worker` must create internal publication candidates.

The terminal implemented output is internal `publication_candidates`. There is
no implemented provider routing or external publication/execution in the
reviewed migrations and workers.

## Missing Runtime Capabilities

- Active policy bootstrap is absent. Migrations seed commerce, routing, catalog,
  and publication policies as `draft`, while workers require `active` policies.
- LOC map candidates do not bridge into `illustration_opportunities`,
  `commerce_opportunities`, or the downstream product/catalog/publication chain.
- LOC map proof data is candidate/evidence-level only; it does not create a
  normalized commerce-ready asset linked to the reviewed runtime.
- Historical photography has benchmark coverage but no ingestion worker,
  migration-backed candidate table, rights evidence table, or opportunity bridge.
- Product routing writes empty `recommended_providers`; provider selection is
  explicitly not implemented.
- Catalog runtime is internal-only. Migration 26 and 27 constraints prohibit
  provider identifiers, external product IDs, and publication/provider terms.
- Publication runtime is internal planning only. Migration 29 and 30 constraints
  prohibit external IDs, API/provider/execution state, and publication execution.
- Provider routing has architecture documentation only. No implemented
  `provider_routing_policy`, `provider_capability_profiles`,
  `provider_route_candidates`, audit log, worker, or replay worker exists.
- Commerce scoring is generic enough to score manually inserted LOC rows, but
  source-specific ingestion support is only implemented for BHL illustrations
  and LOC map proof candidates.

## Future Migrations Required

These are required to expand runtime coverage beyond BHL illustrations:

- Policy activation or governance migration for active `commerce_policy`,
  `product_routing_policy`, `catalog_policy`, and `publication_policy`, if the
  platform should run from migration state without manual policy promotion.
- LOC map commerce bridge migration to promote approved `loc_map_asset_candidates`
  into the commerce input model, either by creating governed
  `illustration_opportunities` rows or by generalizing commerce inputs beyond
  illustration opportunities.
- LOC map asset activation migration to link approved LOC map candidates to
  `assets`, `asset_rights`, and downstream commerce provenance.
- Historical photography ingestion migration and worker runtime, including
  candidate table, rights evidence, media metadata, asset activation, and
  commerce opportunity bridge.
- General asset-class vocabulary migration if commerce should support first-class
  `map`, `photograph`, `illustration`, and `document` asset classes instead of
  routing everything through illustration opportunity semantics.
- Provider routing migrations for `provider_routing_policy`,
  `provider_capability_profiles`, `provider_route_candidates`, and append-only
  provider routing audit logs.
- Provider routing worker and replay worker implementation.
- Optional commerce execution migrations only after provider routing exists;
  execution is outside migrations 19 through 31 and is not required for the
  current internal publication-candidate boundary.

## Audit Conclusion

Runtime coverage is currently narrow and internally bounded. BHL illustrations
are the only asset class with implemented ingestion support and a conditional
end-to-end path through scoring, product routing, internal catalog generation,
and internal publication planning.

LOC historic maps are partially ingested as proof candidates but do not
successfully traverse the reviewed runtime without manual fixture-style insertion
into `illustration_opportunities`. Historical photography and other asset
classes are benchmarked or documented only; they do not have implemented runtime
ingestion-to-publication traversal.
