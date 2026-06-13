# NC-PLATFORM-001: Implementation Roadmap

| Field | Value |
|---|---|
| Program | NC-PLATFORM-001 |
| Title | World-Class Nature & Culture Platform |
| Date | 2026-06-12 |
| Status | Draft implementation roadmap |
| Scope | Website, Commerce Runtime, AI Runtime, Authority Registry, Product Runtime |
| Reference models | Apple.com, Airbnb, National Geographic, Google Arts & Culture, Stripe |

## 1. Platform Thesis

Nature & Culture should become a governed discovery, storytelling, and commerce platform for public-domain nature and culture assets. The production system must feel editorially refined like Apple and National Geographic, searchable and place-native like Airbnb and Google Arts & Culture, and operationally trustworthy like Stripe.

The platform should not be built as a set of static landing pages. It should be built as a set of reusable governed primitives:

- Places with identity, authority, geography, evidence, stories, collections, and products.
- Collections with curated assets, provenance, publication status, and product eligibility.
- Products with source lineage, rights state, provider routing, fulfillment state, and channel publication state.
- AI outputs that are grounded, cited, reviewed, and unable to mutate canonical authority directly.
- Search and recommendations that retrieve approved entities from PostgreSQL, then enrich with derived spatial, graph, semantic, and editorial signals.

The core invariant remains:

> PostgreSQL records canonical authority. AI, search, graph, vector, and commerce providers produce derived signals, drafts, proposals, or execution state.

## 2. Production Platform Architecture

```text
Website
  -> Public pages, editorial journeys, search, product discovery, account/order surfaces

API Gateway
  -> Governed read APIs, activation gates, public serialization, preview endpoints

Authority Registry
  -> PostgreSQL canonical identities, rights, provenance, places, assets, reviews, publication

Collection Runtime
  -> Curated asset groupings, place links, manifests, lifecycle, export state

Product Runtime
  -> Product profiles, product families, variants, pricing, QA, provider routes

Commerce Runtime
  -> Shopify catalog/cart/checkout, Gelato/Lulu fulfillment, Etsy syndication

AI Runtime
  -> Retrieval contracts, context packs, model invocation, output validation, review queue

Search + Recommendation Runtime
  -> Postgres filters, PostGIS, pgvector, Neo4j projections, ranking, audit

Observability + Replay
  -> policy versions, source hashes, worker versions, invocation records, web vitals, commerce events
```

## 3. Information Architecture

The public website should be organized around user intent, not internal data models.

Primary navigation:

| Surface | Purpose | First production routes |
|---|---|---|
| Home | Editorial platform entry and current flagship | `/` |
| Places | Browse place-led journeys | `/places`, `/places/[slug]` |
| Collections | Curated asset/product groupings | `/collections`, `/collections/[slug]` |
| Products | Shop governed product families | `/products`, `/products/[slug]` |
| Stories | Long-form editorial experiences | `/stories/[slug]` |
| Search | Cross-platform discovery | `/search` |
| About | Trust, sourcing, governance, attribution | `/about` |

Page types:

- Home: flagship editorial entry, active phase modules, product and place teasers.
- Place page: hero, identity panel, authority/provenance strip, editorial journey, map, collection modules, product modules, related places.
- Collection page: curator framing, asset grid, source/provenance panel, product family modules, download/export status where allowed.
- Product page: product media, variants, source lineage, rights and attribution, fulfillment profile, related story/place/collection.
- Story page: magazine-quality narrative, cited media, source references, product or collection callouts.
- Search results: places, collections, products, stories, and assets with governed filters.

## 4. Collection Architecture

Collections are the bridge between authority and experience. A collection should be publication-ready before it becomes a public page or product source.

Required collection primitives:

- Stable `collection_id`, slug, title, type, lifecycle status.
- One or more place connections, including cosmic anchors such as Earthrise where governed.
- Ordered collection assets with rights status, source lineage, and display eligibility.
- Manifest export with checksum, byte size, creator, format, and provenance.
- Product profile linking the collection to allowed product families.
- Editorial modules for story, education, product, and search surfaces.

Collection lifecycle:

```text
draft -> approved -> published
draft -> rejected
approved/published -> disputed -> retracted
```

Collection page sections:

1. Collection hero.
2. Curator statement.
3. Key assets.
4. Place and theme context.
5. Product families.
6. Provenance and attribution.
7. Related collections.

## 5. Place Architecture

Places are the primary discovery unit for the production platform.

Required place primitives:

- Canonical place identity from the Authority Registry.
- GeoNames ID where applicable.
- Wikidata QID where applicable.
- OSM relation only for display/map context, never as the canonical authority.
- Place status: `draft`, `coming_soon`, `preview`, `live`, `paused`, `retracted`.
- Authority package: identifiers, coordinates, feature code, source evidence, attribution rules.
- Content package: hero asset, story modules, education modules, tourism modules, product modules.
- Commerce package: eligible products and product families.
- Search package: synonyms, themes, related entities, editorial tags.

Place page sections:

1. Full-bleed visual hero with place name and concise editorial line.
2. Authority strip: identifiers, rights posture, source/attribution access.
3. Editorial journey: National Geographic quality story modules.
4. Map and spatial context where OSM attribution gates are satisfied.
5. Collections connected to the place.
6. Product modules tied to governed assets.
7. Related places and stories.

Phase place order:

| Phase | Places | Activation posture |
|---|---|---|
| Phase 1 | Earthrise | Cosmic anchor, NASA-only attribution, no GeoNames/OSM dependency |
| Phase 2 | Yellowstone, Grand Canyon | GeoNames + OSM gates, NASA/BHL/NARA asset gates |
| Phase 3 | Great Barrier Reef, Galápagos | GeoNames + OSM gates, NOAA/GBIF/ALA/authority gates |
| Phase 4 | Venice, Papahānaumokuākea | Venice cultural-waterfront authority model; Papahānaumokuākea GeoNames confirmation required |

## 6. Product Architecture

Products are not standalone merch. Every product must be traceable to a governed asset, place, collection, and rights decision.

Product hierarchy:

```text
Collection
  -> Product Profile
    -> Product Family
      -> Product Type
        -> Shopify Product
          -> Variant
            -> Fulfillment Route
```

Initial product families:

| Family | Provider posture | Launch use |
|---|---|---|
| Wall art | Gelato primary, Printful fallback if adopted | Earthrise, Yellowstone, Grand Canyon, GBR |
| Posters | Gelato primary | Education and maps |
| Digital downloads | Shopify digital/manual v1 | Earthrise and selected education assets |
| Books/field guides | Lulu Direct later | Phase 3+ |
| Calendars/cards | Gelato after sample approval | Yellowstone and broader place collections |

Product activation rules:

- Rights status must be `verified_pd` or equivalent governed public-domain/CC0 state.
- Human verification must be true for displayed and sold assets.
- Product copy cannot imply institutional endorsement unless explicitly authorized.
- Provider route must be declared before publication.
- Shopify metafields must preserve NC IDs: collection, asset, place, opportunity, rights, source record, fulfillment profile.
- Marketplace syndication must not precede Shopify canonical product creation.

## 7. AI Content Architecture

AI should make the platform more scalable without weakening authority.

AI runtime responsibilities:

- Draft story modules, education copy, product copy, captions, search summaries, and recommendation explanations.
- Extract or normalize candidate metadata for human review.
- Generate retrieval plans from natural language search intent.
- Produce cited context packs and structured outputs.

AI runtime prohibitions:

- No rights approval.
- No activation approval.
- No canonical place, source, asset, collection, or product mutation.
- No publication without validation and review policy satisfaction.
- No uncited factual claims in public content.

Required AI production tables or equivalents:

- `foundation_model_registry`
- `prompt_registry`
- `retrieval_contract`
- `agent_invocation`
- `context_pack`
- `model_output_proposal`
- `page_generation_review`

Public content flow:

```text
page intent
  -> retrieval contract
  -> eligible source/context pack
  -> model invocation
  -> output validation
  -> review
  -> approved public serialization
```

## 8. Search Architecture

Search must work like a cultural and natural knowledge system, not a keyword-only store search.

Search modes:

- Keyword: exact names, product names, place names, identifiers.
- Faceted: place, collection, product family, rights, source institution, media type, phase.
- Spatial: near a place, inside a region, along a route, map viewport.
- Semantic: "volcanoes and conservation", "reef biodiversity", "space photographs that changed culture".
- Editorial: curated journeys, featured themes, campaign modules.

Runtime:

```text
query
  -> intent parser
  -> PostgreSQL identity and eligibility filters
  -> optional PostGIS spatial filter
  -> optional pgvector semantic retrieval
  -> optional Neo4j relationship traversal
  -> PostgreSQL rehydration
  -> ranking
  -> public result serialization
```

Search result types:

- Place
- Collection
- Product
- Story
- Asset
- Source/institution reference where public-safe

Production invariant:

> Every search result must rehydrate from PostgreSQL and pass rights, publication, visibility, and retraction checks before rendering.

## 9. Recommendation Architecture

Recommendations should feel editorial, explainable, and commercially useful.

Recommendation surfaces:

- Home: current flagship, next places, seasonal collections.
- Place page: related collections, products, stories, nearby/similar places.
- Product page: matching collection, related products, story context.
- Collection page: related places, products, and stories.
- Cart/post-purchase later: complementary products and education modules.

Signal classes:

| Signal | Source | Authority posture |
|---|---|---|
| Same place | PostgreSQL | Canonical |
| Same collection | PostgreSQL | Canonical |
| Same asset theme | Governed taxonomy | Canonical or reviewed |
| Spatial proximity | PostGIS | Authoritative spatial predicate |
| Relationship path | Neo4j projection | Derived |
| Semantic similarity | pgvector | Derived |
| Commerce performance | Shopify/internal event store | Derived operational signal |
| Editorial priority | Human curation | Canonical campaign policy |

Recommendation records should store explanation data:

- Why this was recommended.
- Which signals were used.
- Which policy version ranked it.
- Which entities were filtered out by rights/publication gates.

## 10. Commerce Architecture

Commerce should use Shopify as the customer-facing catalog, cart, checkout, and order authority while retaining NC as the rights and provenance authority.

Authority boundaries:

| System | Owns |
|---|---|
| PostgreSQL | Rights, provenance, product intent, source lineage, activation, audit |
| Shopify | Public sellable catalog, variants, carts, checkout, orders |
| Gelato | Non-book fulfillment execution |
| Lulu Direct | Book and workbook print jobs |
| Etsy | Curated marketplace syndication |

Commerce flow:

```text
approved collection/product profile
  -> product plan
  -> QA and provider route
  -> Shopify draft product
  -> human product review
  -> publish Shopify
  -> optional Etsy syndication
  -> order webhooks
  -> fulfillment provider
  -> status sync and audit
```

First production commerce target:

- Keep Earthrise manual purchase stable until product pages and product data are API-backed.
- Add Shopify only after NC IDs, attribution, rights state, and product variants are serialized cleanly from the API.
- Do not start Etsy before Shopify product authority and fulfillment status sync exist.

## 11. Performance Architecture

Performance is part of the product. The site should feel as immediate and polished as the reference models.

Website targets:

- Static or ISR rendering for public place, story, collection, and product pages where possible.
- API revalidation windows by content type.
- Responsive images with explicit dimensions and modern formats.
- Minimal client JavaScript for editorial pages.
- Search uses server-backed APIs with cached facets and paginated results.
- Attribution and rights blocks render from the same serialized source data as the visible asset.

Operational targets:

- Public API responses include cache headers where safe.
- Expensive AI, graph, vector, and provider calls never run in public page render paths.
- Derived search/recommendation indexes are rebuilt asynchronously from PostgreSQL.
- Web vitals, API latency, provider webhook failures, and product publication failures are observable.
- Every activation has a rollback path: pause place, pause collection, unpublish product, retract asset.

## 12. Phase Roadmap

### Phase 1: Earthrise

Goal:

- Turn the current Earthrise website into the first production-grade platform slice.

Build outcomes:

- API-backed home, Earthrise story, Earthrise product, about, and products pages.
- Earthrise authority package with NASA-only attribution and explicit nonendorsement.
- Earthrise product package for NC-PROD-001 and NC-PROD-008.
- Reviewed AI page generation available only where `review_status = approved` and `publication_allowed = true`.
- Product data model prepared for Shopify metafields, even if checkout remains manual.
- Search stub that can index and return Earthrise, its story, and products.

Exit criteria:

- No hardcoded product authority remains outside governed content/API serialization.
- Earthrise product page displays the same rights, attribution, source, and product state used by the API.
- Public tests verify NASA attribution, NASA nonendorsement, no NARA attribution, and no unapproved collector-edition language.

### Phase 2: Yellowstone and Grand Canyon

Goal:

- Prove terrestrial place architecture with GeoNames, OSM, mixed asset sources, and contextual commerce.

Build outcomes:

- `/places/yellowstone` and `/places/grand-canyon`.
- Place API serialization for canonical IDs, source references, content status, map attribution, and eligible assets.
- Place index driven by API data.
- First place collections and product profile records.
- Search filters for place, product, story, and collection.
- Recommendation modules: related products, related stories, related places.

Exit criteria:

- Yellowstone uses GeoNames ID `5843591`.
- Grand Canyon uses GeoNames ID `5296401`.
- OSM attribution renders only when map tiles render.
- Pending NARA assets display as unavailable or coming soon, not as sellable products.
- Place pages can be paused or hidden from API status without code deletion.

### Phase 3: Great Barrier Reef and Galápagos

Goal:

- Extend the platform to marine/ecological authority models and biodiversity-driven content.

Build outcomes:

- GBR and Galápagos place pages.
- NOAA/GBIF/ALA authority packages.
- Biodiversity and conservation story modules.
- Product profiles for reef and island products.
- Search facets for ecosystem, species/taxon, source institution, and product family.
- AI-generated education modules with strict citation and review.

Exit criteria:

- NOAA nonendorsement/credit rules are enforced for NOAA assets.
- Biodiversity evidence resolves through governed authority records.
- No ecological or conservation factual claim renders without citation/source evidence.

### Phase 4: Venice and Papahānaumokuākea

Goal:

- Validate cultural-waterfront and protected marine monument patterns.

Build outcomes:

- Venice place architecture with cultural heritage, maps, images, and future climate/conservation themes.
- Papahānaumokuākea place architecture after GeoNames identity confirmation.
- Advanced related-place recommendations across cultural, ecological, and spatial signals.
- Expanded collections and product families.
- Shopify product publication path if Phase 1-3 product serialization is stable.

Exit criteria:

- Venice does not enter production with generic travel copy; it must have source-backed cultural and environmental content.
- Papahānaumokuākea does not activate until the GeoNames identity gate is resolved.
- Recommendation explanations are visible or inspectable for internal QA.

## 13. What Should Be Built Next In Code

The next code work should be a platformization pass, not another static page pass.

### Build Next: Platform Content API Contract

Implement a governed public content contract that can power Earthrise now and every later place/collection/product page.

Recommended first code package:

1. Add typed API response models for:
   - `PublicPlace`
   - `PublicCollection`
   - `PublicProduct`
   - `PublicStory`
   - `AttributionBlock`
   - `AuthorityReference`
   - `PublicationStatus`

2. Add API endpoints:
   - `GET /public/home`
   - `GET /public/places`
   - `GET /public/places/{slug}`
   - `GET /public/products`
   - `GET /public/products/{slug}`
   - `GET /public/stories/{slug}`

3. Move Earthrise public page data behind those endpoints:
   - NASA attribution.
   - NASA nonendorsement.
   - Product codes `NC-PROD-001` and `NC-PROD-008`.
   - Story copy fallback and reviewed AI copy override.
   - Publication status and manual purchase state.

4. Update the Next.js app to consume the public content contract:
   - Home uses `GET /public/home`.
   - Products index uses `GET /public/products`.
   - Earthrise product uses `GET /public/products/earthrise`.
   - Earthrise story uses `GET /public/stories/earthrise`.
   - Places index uses `GET /public/places`.

5. Add tests:
   - API contract tests for Earthrise public serialization.
   - Web rendering tests for attribution and prohibited-copy rules.
   - Fallback tests when API is unavailable.

Why this is first:

- It converts the current Earthrise pilot into the reusable production platform.
- It creates the same contract Yellowstone, Grand Canyon, GBR, Galápagos, Venice, and Papahānaumokuākea will use.
- It reduces hardcoded governance risk in the frontend.
- It prepares Shopify/search/recommendation work without prematurely integrating external commerce.

### Build Second: Place Runtime v1

After the public content contract exists, add live place runtime support:

- Authority-backed `PublicPlace` serializer.
- Place status gating.
- Attribution matrix per place.
- Eligible asset summary.
- Product module summary.
- Related story and collection summary.

First targets:

- Yellowstone.
- Grand Canyon.

### Build Third: Search v1

Build search only after public serialization exists:

- Index public-safe places, products, stories, and collections.
- Start with PostgreSQL keyword/facet search.
- Add pgvector semantic search later under a governed vector-space registry.
- Do not call foundation models in the public request path.

### Build Fourth: Product Runtime v1

Build product runtime after Earthrise and two terrestrial places can render from API contracts:

- Product profile records.
- Product family/type status.
- Provider route placeholders.
- Shopify metafield mapping.
- Draft product generation command.
- Manual QA before publish.

### Build Fifth: Recommendation v1

Start with deterministic editorial recommendations:

- Same place.
- Same collection.
- Same product family.
- Human campaign priority.

Add semantic/graph recommendations only after deterministic recommendations are observable and testable.

## 14. Engineering Acceptance Criteria

NC-PLATFORM-001 is ready for implementation when:

- The public content contract is accepted as the common interface between API and website.
- Earthrise can be rendered entirely from governed public serialization plus local fallback.
- Place pages can be activated, paused, or hidden through data state.
- Attribution is data-driven and tested.
- AI content cannot publish unless reviewed and explicitly allowed.
- Product pages carry NC IDs and rights state through the API.
- Search and recommendation work is downstream of public eligibility gates.

## 15. Non-Goals For The Next Build

- Do not integrate Etsy yet.
- Do not launch broad AI generation for unreviewed public pages.
- Do not build generic media support for audio, film, 3D, or datasets yet.
- Do not make Shopify the authority for rights, provenance, or product eligibility.
- Do not create static one-off place pages that bypass the public content contract.
- Do not activate Papahānaumokuākea before the GeoNames identity gate is resolved.

## 16. Final Build Order

1. Public content API contract.
2. Earthrise API-backed frontend.
3. Place Runtime v1 for Yellowstone and Grand Canyon.
4. Search v1 over public-safe entities.
5. Product Runtime v1 with Shopify-ready mapping.
6. Recommendation v1 deterministic modules.
7. GBR and Galápagos authority/content expansion.
8. Commerce execution: Shopify draft product generation, then publish workflow.
9. Venice and Papahānaumokuākea expansion after authority gates.

