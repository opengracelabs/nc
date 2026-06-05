# Prototype Data Dependency Plan

Mission:

- Begin prototype implementation planning.
- Define what can be mocked.
- Define what requires real Nature & Culture data.
- Define what requires Shopify.

Boundaries:

- Planning only.
- No implementation.
- No code generation.
- No schema redesign.

Prototype target:

- Yellowstone-only clickable prototype.
- Routes:
  - Home
  - Place
  - Collection
  - Asset
  - Shop Collection
  - Product

## Summary

Use three dependency levels:

1. Mocked: safe to fake for layout, navigation, and review.
2. Real Nature & Culture data: required where trust, provenance, or canonical IDs matter.
3. Shopify: required only where commerce behavior, products, variants, price, cart, or checkout matter.

Recommended prototype sequence:

```text
Static mocked fixture
↓
Real NC place/collection/asset fixture
↓
Shopify product fixture
↓
Live Shopify Storefront read
↓
Cart/checkout later
```

## What Can Be Mocked

Mock these in the first clickable prototype:

### Page Layout

- Hero layout.
- Card grids.
- Rails.
- Breadcrumbs.
- Footer.
- Section ordering.
- CTA placement.
- Mobile stacking.

Reason:

- These validate experience and navigation, not data correctness.

### Copy

- Homepage headline.
- Shop homepage headline.
- CTA labels.
- Short editorial captions.
- Empty states.
- Introductory explanatory text.

Rule:

- Mock copy must be clearly traceable to prototype fixture files so it can later be replaced by PostgreSQL/FastAPI fields.

### Images

- Hero image.
- Collection cover.
- Product mockup image.
- Placeholder map image.
- Placeholder graph preview image.

Rule:

- Asset detail page should move to real rights-cleared image data as soon as possible.

### Neo4j Graph Preview

- Related concept pills.
- Small graph preview.
- Related content rail.

Reason:

- Neo4j is not required to validate the first clickable flow.
- Graph data is enhancement, not page authority.

### Shopify Product-Like Cards

- Product preview cards on Home, Collection, Asset, and Shop Collection.
- Product category tiles.
- Product recommendation rails.

Rule:

- Product Detail page needs Shopify earlier than preview cards do.

## What Requires Real Nature & Culture Data

Use real or fixture-faithful Nature & Culture data for these areas:

### Canonical IDs

Required:

- `place_id`
- `collection_id`
- `asset_id`
- `opportunity_id`

Reason:

- These IDs become the bridge to FastAPI, Shopify metafields, Neo4j projection, and commerce runtime.

### Multilingual Field Shape

Required:

- `title = {"en": "..."}`
- `summary = {"en": "..."}`
- `description = {"en": "..."}`

Reason:

- The prototype must prove multilingual rendering from day one.

### Place Page

Real data required:

- Yellowstone place title.
- Yellowstone summary.
- Yellowstone description or safe placeholder derived from authoritative copy.
- Country/region.
- Source/provenance references.

Mockable:

- Decorative map image.
- Related content counts.
- Graph preview.

### Collection Page

Real data required:

- Collection ID.
- Collection title/summary/description.
- Collection status.
- Ordered asset membership.
- Place membership.
- Rights summary.

Mockable:

- Product preview count.
- Related collection rail.

### Asset Page

Real data required:

- Asset ID.
- Image or source-linked placeholder.
- Rights status.
- Rights source URL.
- Source record URL.
- Source institution.
- Connected collection.
- Connected place.

Reason:

- Asset trust is central to Nature & Culture.
- Rights/provenance cannot be hand-waved in the prototype.

### Product Context

Real Nature & Culture data required:

- Product-to-asset mapping.
- Product-to-collection mapping.
- Product-to-place mapping.
- Product-to-opportunity mapping if available.

Reason:

- Shopify product metafields must map back to Nature & Culture authority.

## What Requires Shopify

Shopify is required only for commerce-specific behavior.

### Product Page

Requires Shopify for:

- Product handle.
- Product title as sold.
- Product images/mockups.
- Variant options.
- Price.
- Availability.
- Product description.
- Add-to-cart behavior.

Can be mocked initially:

- Shipping estimate.
- Related products.
- Reviews.
- Discounts.
- Checkout completion.

### Shop Collection Page

Requires Shopify for:

- Shopify collection handle.
- Products in collection.
- Product prices.
- Product availability.
- Product images.

Can be mocked initially:

- Filter behavior.
- Sort behavior.
- Related collections.

### Cart And Checkout

Requires Shopify for:

- Cart create.
- Cart lines.
- Quantity updates.
- Checkout handoff.

Prototype recommendation:

- Do not require live cart/checkout for first clickable prototype.
- Use disabled or stubbed Add to Cart in the first visual prototype.
- Enable Storefront cart only after Product Page layout is approved.

### Shopify Metafields

Required before real integration:

- `nc.asset_id`
- `nc.collection_id`
- `nc.place_id`
- `nc.opportunity_id`

Reason:

- Without these, Shopify cannot reliably bridge back to Nature & Culture pages.

## Page-by-Page Dependency Matrix

| Page | Mock OK | Real NC Data Required | Shopify Required |
| --- | --- | --- | --- |
| Home | Layout, hero image, product previews, graph hints | Yellowstone IDs, localized labels, featured collection/asset references | No |
| Place | Map image, graph preview, related counts | Place ID, title, summary, description, source/provenance | No |
| Collection | Product preview cards, related rails | Collection ID, localized fields, asset membership, place membership, rights summary | No |
| Asset | Viewer layout, product preview card | Asset ID, image/source placeholder, rights, source URL, collection/place links | No for editorial page |
| Shop Collection | Filters, sort, related rails | NC collection context via metafield mapping | Yes for product grid/prices |
| Product | Related products, shipping copy, reviews | NC asset/collection/place context | Yes for product, variants, price, availability |

## Recommended Prototype Fixtures

### `yellowstone.nc.fixture.json`

Should contain:

- Place.
- Collection.
- Asset.
- Opportunity.
- Rights.
- Provenance.
- Related concepts.

### `yellowstone.shopify.fixture.json`

Should contain:

- Shopify collection handle.
- Product handle.
- Product title.
- Images/mockups.
- Variants.
- Price.
- Availability.
- Metafields mapping to Nature & Culture IDs.

### `yellowstone.graph.fixture.json`

Should contain:

- Nodes:
  - Place
  - Concept
  - Opportunity
  - Asset
  - Collection
- Edges:
  - Collection -> Asset
  - Asset -> Opportunity
  - Opportunity -> Place
  - Opportunity -> Concept

Graph fixture is optional for first prototype.

## Implementation Planning Sequence

### Step 1: Static Clickable Prototype

Use:

- Mock page layout.
- Realistic Yellowstone fixture.
- Mock Shopify product card.

Do not use:

- Live FastAPI.
- Live Shopify.
- Live Neo4j.

Goal:

- Validate navigation and content hierarchy.

### Step 2: Real Nature & Culture Fixture

Use fixture shaped exactly like expected FastAPI responses.

Goal:

- Validate multilingual rendering, canonical IDs, rights, provenance, and collection membership.

### Step 3: Shopify Read Integration

Use Shopify Storefront API for:

- Shop Collection.
- Product Page.

Goal:

- Validate product handles, images, variants, price, and availability.

### Step 4: Shopify Cart Integration

Use Shopify Storefront cart only after product page approval.

Goal:

- Validate add-to-cart and checkout handoff.

### Step 5: FastAPI Integration

Replace NC fixtures with public FastAPI endpoints.

Goal:

- Validate production data path after prototype UX is accepted.

### Step 6: Neo4j Projection Integration

Replace graph fixtures with projection API.

Goal:

- Validate related-content modules.

## Decision Rules

Mock if:

- It only affects layout.
- It only affects navigation.
- It is not authoritative.
- It does not affect price, availability, rights, or provenance.

Use real Nature & Culture data if:

- It identifies a place, collection, asset, opportunity, or source.
- It affects rights or provenance.
- It controls product eligibility.
- It maps Shopify back to PostgreSQL.

Use Shopify if:

- It affects product price.
- It affects variant selection.
- It affects availability.
- It affects cart.
- It affects checkout.

Use Neo4j only when:

- The feature is related-content exploration.
- The page can still render without graph data.

## Prototype Acceptance For Data Dependencies

Accepted when:

- Six pages render from fixtures.
- IDs are stable across pages.
- Multilingual dictionaries render through the same component path.
- Rights and source panels use real or fixture-faithful fields.
- Shop Collection and Product can be switched from fixture to Shopify without changing page layout.
- FastAPI can replace NC fixtures without redesigning components.
- Neo4j can be added later without blocking the prototype.
