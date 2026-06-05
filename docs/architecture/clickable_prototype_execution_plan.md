# Clickable Prototype Execution Plan

Mission:

- Define how to move from wireframes to a clickable prototype.

Scope:

- Planning only.
- No implementation.
- No code generation.
- No schema redesign.

Prototype scope:

- Yellowstone-only content path.
- Six-page prototype path:
  - Home
  - Place
  - Collection
  - Asset
  - Shop Collection
  - Product

Target outcome:

- A reviewer can click through the core Nature & Culture experience from editorial discovery to commerce product detail without needing live full production data.

Flow:

```text
Wireframes
↓
Prototype content fixture
↓
Route map
↓
Static clickable screens
↓
Light data wiring
↓
Review build
↓
Prototype acceptance
```

## Phase 1: Freeze Prototype Scope

Inputs:

- `wireframe_specifications.md`
- `yellowstone_prototype_build_plan.md`
- `collection_model.md`
- `commerce_runtime_design.md`

Decisions:

- Locale: `en`.
- Place: Yellowstone.
- Collection: Yellowstone Natural History.
- Asset: one rights-cleared BHL or Smithsonian asset.
- Product: one Shopify-style product.

Acceptance:

- The prototype contains only the six agreed pages.
- All routes are clickable.
- No additional architecture redesign is introduced.

## Phase 2: Build Prototype Content Fixture

Create a single fixture document for the prototype.

Required fixture sections:

- Place.
- Collection.
- Asset.
- Opportunity/context.
- Shopify collection.
- Shopify product.
- Rights/provenance.
- Navigation labels.

Fixture rules:

- Use multilingual dictionary shape even if only `en` exists.
- Every page must have title, summary, and description values.
- Every asset must have rights status and source attribution.
- Every shop product must map back to Nature & Culture IDs.

Acceptance:

- All copy and labels needed by the six pages are available in one fixture.
- No page depends on missing production data.

## Phase 3: Route Map

Prototype routes:

- `/en`
- `/en/places/yellowstone`
- `/en/collections/yellowstone-natural-history`
- `/en/assets/yellowstone-asset`
- `/en/shop/collections/yellowstone-natural-history`
- `/en/shop/products/yellowstone-product`

Navigation paths:

1. Home -> Place.
2. Home -> Collection.
3. Home -> Shop Collection.
4. Place -> Collection.
5. Place -> Asset.
6. Collection -> Asset.
7. Collection -> Shop Collection.
8. Asset -> Product.
9. Shop Collection -> Product.
10. Product -> Asset story.

Acceptance:

- A reviewer can complete the full path:

```text
Home -> Place -> Collection -> Asset -> Product
```

and:

```text
Home -> Shop Collection -> Product -> Asset
```

## Phase 4: Component Inventory

Use the smallest component set needed for clickable review.

Core components:

- Header.
- Shop header.
- Footer.
- Breadcrumbs.
- Hero.
- Card.
- Rail.
- Gallery.
- Rights panel.
- Source/provenance panel.
- Product purchase panel.
- CTA link/button.

Do not build:

- Full search.
- Full cart.
- Live checkout.
- Live graph exploration.
- Admin controls.
- Localization management UI.

Acceptance:

- Components are enough to evaluate layout, navigation, story, and commerce handoff.
- Components do not imply production completeness.

## Phase 5: Visual Fidelity Target

Prototype fidelity:

- Medium-high.
- Real layout, spacing, typography, and imagery.
- Static or fixture-driven content.
- Clickable navigation.
- Minimal dynamic behavior.

Required states:

- Desktop.
- Mobile.
- Image loading fallback.
- Missing translation fallback.
- Product unavailable placeholder.

Not required:

- Full responsive QA matrix.
- Checkout completion.
- API loading skeletons beyond basic placeholders.
- Account/auth states.

Acceptance:

- Prototype feels realistic enough to judge product direction.
- Prototype is not mistaken for production launch readiness.

## Phase 6: Data Wiring Strategy

Preferred sequence:

1. Static fixture JSON.
2. Local mock API wrapper.
3. FastAPI integration after prototype review.
4. Shopify Storefront integration after product direction is approved.

Reason:

- Static fixture keeps prototype fast and stable.
- API wiring should not block visual/navigation validation.
- Production integration belongs after the clickable prototype is accepted.

Acceptance:

- Clickable prototype can run without FastAPI, Shopify, or Neo4j.
- Data shape mirrors expected API contracts closely enough to reduce rework.

## Phase 7: Review Script

Reviewer tasks:

1. Start on Home.
2. Open Yellowstone Place.
3. Open Yellowstone Collection.
4. Open the featured Asset.
5. Open the Product.
6. Return to Collection.
7. Open Shop Collection.
8. Open Product again.
9. Check rights and source attribution on Asset and Product.
10. Check multilingual fallback behavior.

Review questions:

- Does the place-centered story make sense?
- Is the collection page the right bridge between editorial and commerce?
- Does the asset page build trust?
- Does the product page preserve source/provenance without hurting conversion?
- Are CTAs clear?
- Is anything important missing before real data integration?

Acceptance:

- Reviewers can complete the script without verbal guidance.
- Feedback can be categorized into content, layout, navigation, commerce, or data issues.

## Phase 8: Acceptance Criteria

Clickable prototype is accepted when:

- All six routes exist.
- All primary CTAs work.
- Home, Place, Collection, Asset, Shop Collection, and Product pages are reachable.
- Yellowstone-only data appears consistently.
- Rights/provenance is visible where expected.
- Product page links back to source asset/story.
- Shop Collection links back to editorial collection.
- Mobile layout is usable.
- No live production integration is required to review.

## Phase 9: Post-Prototype Next Steps

After acceptance:

1. Convert fixture fields to FastAPI response contracts.
2. Implement public collection and asset endpoints.
3. Map Shopify product metafields.
4. Replace static product fixture with Shopify Storefront product data.
5. Replace graph placeholders with Neo4j projection snippets.
6. Add multilingual routing beyond `en`.
7. Run visual QA on mobile and desktop.

## Prototype Risk Controls

Risks:

- Prototype expands into architecture redesign.
- Prototype blocks on live APIs.
- Commerce pages become too generic.
- Editorial pages hide rights/provenance.
- Product page becomes too provenance-heavy.

Controls:

- Yellowstone only.
- Six routes only.
- Static fixture first.
- No schema work.
- No ingestion work.
- No checkout work.
- Review against the scripted path.
