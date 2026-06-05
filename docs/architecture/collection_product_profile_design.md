# Collection Product Profile Design

Mission:

- Design `collection_product_profiles`.
- Define how collections activate product families.
- Define how product families activate product types.
- Keep product generation manageable at 70, 700, and 7000 collections.
- Avoid unnecessary product generation.

Context:

- Commerce Runtime
- Shopify
- Gelato
- Printful
- Lulu Direct
- Etsy

Boundaries:

- No implementation.
- No migrations.
- No schema redesign.
- PostgreSQL remains the Nature & Culture authority.
- Shopify remains the commerce catalog/cart/checkout authority.
- Gelato, Printful, and Lulu Direct are fulfillment providers.
- Etsy is a marketplace syndication channel.

Provider assumptions from current public docs:

- Shopify supports product, variant, metafield, collection, publication, cart, checkout, and webhook workflows through Admin and Storefront APIs.
- Gelato supports catalog/product UID driven order automation and webhooks.
- Printful supports API product templates, mockups, and orders, but should be treated as a controlled route rather than the default bulk generation provider.
- Lulu Print API supports book-focused print jobs, product/package IDs, cost calculation, and webhooks.
- Etsy Open API v3 supports listings and inventory, but Etsy should not be the canonical catalog.

## Product Profile Model

`collection_product_profiles` should be the curation and automation control plane between a governed collection and generated commerce products.

It answers:

- Which product families are allowed for this collection?
- Which product types inside each family are active?
- Which provider route is approved?
- How many assets can generate products?
- Which channels can publish?
- What is manual, semi-automatic, or automatic?

Recommended design-level shape:

```sql
CREATE TABLE collection_product_profiles (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    collection_id       UUID NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    profile_name        TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'draft',
    automation_mode     TEXT NOT NULL DEFAULT 'manual',
    product_families    JSONB NOT NULL DEFAULT '{}',
    channel_policy      JSONB NOT NULL DEFAULT '{}',
    generation_limits   JSONB NOT NULL DEFAULT '{}',
    quality_gates       JSONB NOT NULL DEFAULT '{}',
    pricing_policy      JSONB NOT NULL DEFAULT '{}',
    provenance          JSONB NOT NULL DEFAULT '{}',
    agent_notes         JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (collection_id, profile_name)
);
```

Design-only status values:

- `draft`
- `approved`
- `active`
- `paused`
- `retired`

Design-only automation modes:

- `manual`: no product generation without curator action.
- `assisted`: generate product plans, not Shopify products.
- `draft_products`: generate Shopify draft products only.
- `publish_shopify`: publish to Shopify after QA gates.
- `syndicate_etsy`: publish selected approved Shopify products to Etsy.

Recommended profile granularity:

- One default profile per collection.
- Optional seasonal or campaign profiles for special drops.
- Do not create one profile per product unless the product is a special edition.

## Activation Model

### 1. Collection Activates Product Families

A collection should activate a product family only when its assets and editorial context fit that family.

Family activation record inside `product_families`:

```json
{
  "wall_art": {
    "status": "active",
    "provider_priority": ["gelato", "printful"],
    "max_assets": 6,
    "max_product_types": 3,
    "channels": ["shopify", "etsy"],
    "automation_mode": "draft_products"
  }
}
```

Family activation rules:

- A family starts as `inactive`.
- A family can move to `candidate` when the collection has eligible assets.
- A family can move to `active` only after provider mapping, print-file validation, pricing, and QA policy exist.
- A family can be `paused` without pausing the whole collection.

Family statuses:

- `inactive`
- `candidate`
- `active`
- `paused`
- `retired`

### 2. Product Families Activate Product Types

Product types are the concrete sellable product templates within a family.

Example:

```json
{
  "wall_art": {
    "types": {
      "fine_art_print": {
        "status": "active",
        "provider": "gelato",
        "max_variants": 6,
        "etsy_enabled": true
      },
      "framed_print": {
        "status": "candidate",
        "provider": "printful",
        "max_variants": 4,
        "etsy_enabled": false
      }
    }
  }
}
```

Product type statuses:

- `inactive`
- `candidate`
- `active`
- `sample_required`
- `paused`
- `retired`

Activation rules:

- Product type cannot be `active` unless parent family is `active`.
- Product type must declare a provider route.
- Product type must declare variant limits.
- Product type must pass QA gates before publishing.
- Product type can be `sample_required` when provider/product quality has not been approved.

## Product Family Evaluation

### Wall Art

Default posture:

- Primary launch family.

Providers:

- Gelato primary.
- Printful fallback for quality-sensitive framed/canvas routes.
- Etsy eligible after Shopify product QA.

Activation requirements:

- Asset has high-resolution print derivative.
- Rights are Public Domain or CC0.
- Crop/safe-area preview exists.
- At least one provider product UID/template is approved.

Recommended product types:

- Fine art print.
- Framed print.
- Canvas print.
- Poster.

Generation guidance:

- Start with 1 to 3 hero assets per collection.
- Avoid generating every size/material combination initially.
- Use variants for size/material rather than separate products where Shopify UX supports it.

### Books

Default posture:

- Selective specialist family.

Providers:

- Lulu Direct primary.
- Shopify catalog surface.
- Etsy disabled for v1 unless manual.

Activation requirements:

- Collection has enough assets and editorial text for a coherent book.
- Interior PDF and cover PDF can be generated and validated.
- Lulu POD package ID is approved.
- Human review approves content, sequence, title, and cover.

Recommended product types:

- Collection catalog.
- Field guide.
- Educational workbook.
- Art book.

Generation guidance:

- Do not auto-generate books for every collection.
- Books should be campaign-level products, not default products.

### Calendars

Default posture:

- Seasonal/campaign family.

Providers:

- Gelato primary for standard calendars.
- Lulu optional for book-like or premium calendar formats.

Activation requirements:

- Collection has at least 12 strong assets or a curated 12-month concept.
- Month/page layout passes editorial review.
- Seasonal launch window exists.

Recommended product types:

- Wall calendar.
- Desk calendar.
- Educational calendar.

Generation guidance:

- Generate calendars only for curated seasonal collections.
- Retire or pause calendar products after season window.

### Cards

Default posture:

- Good automation family after wall art.

Providers:

- Gelato primary.
- Etsy eligible.

Activation requirements:

- Asset crop works at card scale.
- Localized caption/inside message exists or card is blank.
- Pack strategy is selected.

Recommended product types:

- Single greeting card.
- Note card pack.
- Educational card set.

Generation guidance:

- Use bundles/packs to reduce catalog sprawl.
- Avoid one listing per asset unless asset is proven high demand.

### Puzzles

Default posture:

- Selective family.

Providers:

- Gelato if product quality and format are approved.
- Printful fallback only after sample approval.

Activation requirements:

- Image has enough detail and visual variety.
- No important detail is lost at puzzle crop.
- Provider sample approved.

Recommended product types:

- Jigsaw puzzle.
- Educational puzzle.

Generation guidance:

- Generate only from top visual assets.
- Avoid low-detail botanical plates or text-heavy source images.

### Fashion

Default posture:

- Very selective.

Providers:

- Gelato primary.
- Printful fallback for apparel quality routes.
- Etsy optional after manual review.

Activation requirements:

- Artwork adapts to garment print area.
- Design feels intentional, not pasted.
- Product mockup reviewed.

Recommended product types:

- T-shirt.
- Sweatshirt.
- Tote.

Generation guidance:

- Do not activate automatically for scholarly or delicate archival images.
- Use limited drops rather than broad automatic catalog generation.

### Home Decor

Default posture:

- Selective, asset-dependent.

Providers:

- Gelato primary.
- Printful fallback for specific home items after sample review.

Activation requirements:

- Pattern or visual crop works at product scale.
- Product type matches collection theme.
- Mockup reviewed.

Recommended product types:

- Cushion.
- Throw.
- Mug.
- Tea towel.

Generation guidance:

- Prefer product bundles and curated sets.
- Avoid applying every asset to every home item.

### Education

Default posture:

- High editorial value, lower automation.

Providers:

- Lulu Direct for workbooks/books.
- Gelato for posters/cards.
- Shopify as catalog.
- Etsy optional for selected downloadable/physical learning sets if policy permits.

Activation requirements:

- Educational objective exists.
- Age/level/use-case is defined.
- Text is reviewed.
- Rights and source context are clear.

Recommended product types:

- Field guide.
- Classroom poster.
- Learning card set.
- Workbook.

Generation guidance:

- Treat education as curriculum/editorial product generation, not asset merchandising.

## Scaling Rules

### 70 Collections

Goal:

- Manual and assisted workflow.

Recommended limits:

- 1 active profile per collection.
- 1 to 2 active product families per collection.
- 1 to 3 product types per active family.
- 1 to 6 assets productized per collection.
- Shopify drafts generated; publication requires human QA.
- Etsy only for selected wall art/cards.

Expected catalog shape:

- 70 collections.
- 100 to 300 Shopify products.
- Etsy subset under 50 listings.

### 700 Collections

Goal:

- Rules-driven generation with human exception review.

Recommended limits:

- Product families activate from scoring thresholds.
- Only top assets are productized.
- Wall art/cards become semi-automated.
- Books, education, fashion, home decor, calendars, and puzzles remain curated.
- Shopify draft generation can be automated for approved profiles.
- Publication still requires batch QA or trusted-family approval.

Expected catalog shape:

- 700 collections.
- 1,000 to 3,000 Shopify products.
- Etsy subset limited to proven sellers and seasonal campaigns.

### 7000 Collections

Goal:

- Catalog control and demand-driven generation.

Recommended limits:

- Do not generate products for every collection.
- Generate product plans for many collections, products for few.
- Use lazy generation:
  - On curator approval.
  - On campaign inclusion.
  - On search/traffic signal.
  - On preorder/waitlist threshold.
- Use strict caps by family and channel.
- Archive inactive products automatically by season/performance.

Expected catalog shape:

- 7000 collections.
- Active Shopify products should remain intentionally capped.
- Most collections should have no products or only collection-level product plans.

## Avoiding Unnecessary Products

Rules:

- Never productize every asset by default.
- Never activate every product family by default.
- Never syndicate every Shopify product to Etsy.
- Never create separate Shopify products when variants are sufficient.
- Do not generate products from assets missing rights, provenance, print derivatives, or visual QA.
- Do not generate products for collections without demand, campaign, editorial priority, or curator approval.

Recommended gating scores:

- `collection_commerce_readiness_score`
- `asset_product_fit_score`
- `product_family_fit_score`
- `provider_quality_score`
- `channel_fit_score`
- `expected_margin_score`

Minimum gates:

- Collection approved/published.
- Product profile approved/active.
- Asset rights are Public Domain or CC0.
- Asset has approved print derivative.
- Product type provider route exists.
- Variant count under configured cap.
- QA policy satisfied.

## Commerce Runtime Design

Runtime path:

```text
Collection
↓
collection_product_profile
↓
active product family
↓
active product type
↓
product generation plan
↓
Shopify draft product
↓
QA approval
↓
Shopify publication
↓
Gelato / Printful / Lulu fulfillment
↓
Optional Etsy syndication
```

Authority boundaries:

- PostgreSQL: profile, governance, asset rights, product generation intent.
- Shopify: product catalog, variants, price, cart, checkout.
- Gelato: primary fulfillment for wall art, cards, selected calendars, fashion, home decor, gifts.
- Printful: fallback fulfillment for sample-approved apparel, wall art, and home decor.
- Lulu Direct: books, education workbooks, premium catalogs.
- Etsy: curated marketplace listings only.

Recommended services:

- `profile_evaluator`
- `product_plan_generator`
- `print_file_validator`
- `shopify_draft_sync`
- `product_qa_queue`
- `channel_publisher`
- `provider_router`
- `etsy_syndicator`

## Product Generation Rules

### Product Plan Before Product Creation

Every generation run should create a plan first.

Plan should include:

- Collection ID.
- Profile ID.
- Asset IDs.
- Product family.
- Product type.
- Provider route.
- Variant plan.
- Channel plan.
- Required print files.
- Estimated cost.
- Expected margin.
- QA gates.

No Shopify product should be created until the plan is valid.

### Variant Caps

Recommended v1 caps:

- Wall art: 6 variants per product.
- Cards: 3 variants per product.
- Calendars: 2 variants per product.
- Books: 3 variants per product.
- Fashion: 6 variants per product.
- Home decor: 4 variants per product.
- Puzzles: 2 variants per product.
- Education: 4 variants per product.

### Channel Caps

Shopify:

- Primary channel.
- Can receive draft products for all approved plans.

Etsy:

- Only products with `etsy_enabled = true`.
- Start with wall art and cards.
- No books in v1 Etsy automation.
- No automatic Etsy publish without marketplace QA.

### Provider Selection

Provider priority:

| Product Family | Primary | Secondary | Notes |
| --- | --- | --- | --- |
| Wall Art | Gelato | Printful | Printful only after sample approval |
| Books | Lulu Direct | None | Specialist route |
| Calendars | Gelato | Lulu Direct | Lulu for premium/book-like calendars |
| Cards | Gelato | Printful | Printful optional after samples |
| Puzzles | Gelato | Printful | Selective only |
| Fashion | Gelato | Printful | Limited drops |
| Home Decor | Gelato | Printful | Product-specific approval |
| Education | Lulu Direct | Gelato | Lulu for books/workbooks; Gelato for posters/cards |

## Automation Recommendations

### V1

- Use `manual` or `assisted` profiles by default.
- Allow `draft_products` for wall art only after QA gates are reliable.
- Publish to Shopify manually.
- Syndicate to Etsy manually or semi-manually.
- Use Lulu only for one book/workbook pilot.
- Use Printful only as a sample-approved fallback, not a default bulk route.

### V2

- Enable `draft_products` for wall art and cards.
- Add batch QA for Shopify publication.
- Add Etsy listing sync for selected wall art/cards.
- Add calendar campaign workflow.
- Keep books, education, fashion, home decor, and puzzles curated.

### V3

- Add demand-driven generation at scale.
- Add product plan scoring.
- Add auto-retirement rules for inactive products.
- Add channel-specific product copy and pricing policies.
- Add provider performance scoring.

## Recommended Default Profile

For Collection #000001:

```json
{
  "profile_name": "default",
  "status": "draft",
  "automation_mode": "assisted",
  "product_families": {
    "wall_art": {
      "status": "candidate",
      "provider_priority": ["gelato", "printful"],
      "max_assets": 3,
      "max_product_types": 2,
      "types": {
        "fine_art_print": {
          "status": "candidate",
          "provider": "gelato",
          "max_variants": 6,
          "etsy_enabled": true
        },
        "framed_print": {
          "status": "sample_required",
          "provider": "printful",
          "max_variants": 4,
          "etsy_enabled": false
        }
      }
    },
    "books": {
      "status": "inactive",
      "provider_priority": ["lulu_direct"],
      "reason": "requires editorial book plan"
    },
    "cards": {
      "status": "candidate",
      "provider_priority": ["gelato"],
      "max_assets": 6,
      "max_product_types": 1
    }
  },
  "channel_policy": {
    "shopify": "draft_only",
    "etsy": "manual_review"
  },
  "generation_limits": {
    "max_products_per_collection": 12,
    "max_active_product_families": 2
  }
}
```

This keeps the first collection commercially useful without turning the catalog into uncontrolled product sprawl.
