# Yellowstone Prototype Build Sequence

Mission:

- Define the day-by-day build sequence until the Yellowstone clickable prototype exists.

Boundaries:

- Planning document only.
- No implementation in this step.
- No schema redesign.
- No ingestion changes.

Prototype target:

- Yellowstone-only clickable prototype.
- Six routes:
  - Home
  - Place
  - Collection
  - Asset
  - Shop Collection
  - Product

## Day 1: Prototype Fixture And Route Contract

Goal:

- Freeze the prototype content and route map.

Tasks:

- Create Yellowstone fixture plan:
  - place
  - collection
  - asset
  - opportunity/context
  - Shopify collection stub
  - Shopify product stub
- Confirm IDs and slugs:
  - `yellowstone`
  - `yellowstone-natural-history`
  - `yellowstone-asset`
  - `yellowstone-product`
- Confirm multilingual fixture shape:
  - `title: {"en": "..."}`
  - `summary: {"en": "..."}`
  - `description: {"en": "..."}`
- Confirm six routes:
  - `/en`
  - `/en/places/yellowstone`
  - `/en/collections/yellowstone-natural-history`
  - `/en/assets/yellowstone-asset`
  - `/en/shop/collections/yellowstone-natural-history`
  - `/en/shop/products/yellowstone-product`

Exit criteria:

- Prototype has one fixture contract.
- No page has unknown required data.
- Route names are final for prototype.

## Day 2: App Shell And Navigation

Goal:

- Create the clickable skeleton.

Tasks:

- Build editorial shell:
  - header
  - nav
  - language selector placeholder
  - footer
- Build shop shell:
  - shop header
  - cart icon placeholder
  - footer
- Add route-level pages with placeholder content.
- Wire navigation between all six routes.
- Add breadcrumbs to detail pages.

Exit criteria:

- Every route loads.
- Every route links to at least one next route.
- Reviewer can click Home -> Place -> Collection -> Asset -> Product.

## Day 3: Shared Components

Goal:

- Build reusable components before page-specific polish.

Tasks:

- `LocalizedText`
- `Hero`
- `Card`
- `Rail`
- `Gallery`
- `Breadcrumbs`
- `RightsPanel`
- `SourceProvenancePanel`
- `ShopCallout`
- `ProductCard`
- `CTAButton`

Exit criteria:

- Components can render fixture-backed content.
- Multilingual fallback works for `en`.
- Rights/provenance components have real fields in the fixture.

## Day 4: Editorial Pages

Goal:

- Build Home, Place, Collection, and Asset pages with fixture data.

Tasks:

- Home:
  - Yellowstone hero
  - featured collection
  - featured asset
  - shop callout
- Place:
  - place hero
  - facts panel
  - collection rail
  - asset rail
- Collection:
  - collection hero
  - collection stats
  - asset gallery
  - rights/source panel
  - product preview
- Asset:
  - asset viewer
  - asset metadata
  - rights panel
  - source panel
  - collection/product links

Exit criteria:

- Editorial pages feel coherent as one Yellowstone story.
- Asset page clearly shows rights and source.
- Collection page bridges editorial and commerce.

## Day 5: Shop Pages

Goal:

- Build Shop Collection and Product pages using Shopify-shaped fixture data.

Tasks:

- Shop Collection:
  - collection commerce hero
  - product grid
  - collection story panel
  - rights assurance
  - editorial link
- Product:
  - product media gallery
  - product purchase panel
  - variant selector placeholder
  - add-to-cart disabled or stubbed
  - source asset story
  - rights assurance

Exit criteria:

- Shop Collection page routes to Product.
- Product page routes back to Asset and Collection.
- Product page communicates item, price, variants, provenance, and rights.

## Day 6: Responsive Pass

Goal:

- Make the prototype usable on mobile and desktop.

Tasks:

- Check mobile:
  - nav
  - hero
  - galleries
  - product purchase panel
  - rights/source panels
- Check desktop:
  - page width
  - rails
  - galleries
  - product layout
- Fix text overflow.
- Fix image aspect ratios.
- Ensure CTAs remain visible.

Exit criteria:

- Prototype is usable on mobile and desktop.
- No major overlapping text or layout breakage.
- Product page purchase panel is legible on mobile.

## Day 7: Review Build

Goal:

- Prepare the clickable prototype for stakeholder review.

Tasks:

- Add review script to README or prototype notes.
- Add "prototype only" marker if needed.
- Remove dead links.
- Confirm fixture data is consistent.
- Confirm rights/source fields appear on Asset and Product.
- Confirm shop/editorial cross-links.

Review script:

1. Open Home.
2. Click Yellowstone Place.
3. Click Yellowstone Collection.
4. Click featured Asset.
5. Click Product.
6. Return to Asset.
7. Open Shop Collection.
8. Open Product.
9. Check rights/source attribution.
10. Check mobile layout.

Exit criteria:

- Reviewer can complete script without guidance.
- All six routes are reachable.
- Prototype is ready for feedback.

## Day 8: Feedback Triage

Goal:

- Convert review feedback into actionable changes.

Tasks:

- Categorize feedback:
  - content
  - layout
  - navigation
  - commerce
  - data
  - accessibility
- Fix critical click-path issues.
- Fix confusing labels or CTAs.
- Defer production-only issues.

Exit criteria:

- Critical feedback is resolved or logged.
- Prototype remains Yellowstone-only.
- No scope expansion.

## Day 9: Data Integration Readiness

Goal:

- Prepare to replace fixtures with real APIs later.

Tasks:

- Compare fixture shape to expected FastAPI response shape.
- Compare Shopify fixture shape to Storefront API product/collection shape.
- List missing fields.
- Identify adapter functions needed.
- Confirm Shopify metafield mapping:
  - `nc.asset_id`
  - `nc.collection_id`
  - `nc.place_id`
  - `nc.opportunity_id`

Exit criteria:

- Clear adapter plan exists.
- No component redesign needed for API integration.

## Day 10: Prototype Acceptance

Goal:

- Freeze the clickable prototype as accepted baseline.

Tasks:

- Final desktop/mobile smoke review.
- Confirm six-route click path.
- Confirm rights/source visibility.
- Confirm commerce/editorial bridge.
- Document known limitations.
- Mark prototype accepted or list blockers.

Exit criteria:

- Yellowstone clickable prototype exists.
- Prototype is accepted as the v1 UX baseline.
- Next step can be FastAPI/Shopify integration planning.

## Required Non-Goals During Build

- Do not add new pages.
- Do not add live checkout before prototype acceptance.
- Do not add live Neo4j.
- Do not redesign schema.
- Do not change ingestion.
- Do not expand beyond Yellowstone.
- Do not generate full product catalog.
