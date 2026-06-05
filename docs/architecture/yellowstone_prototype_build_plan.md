# Yellowstone Prototype Build Plan

Scope:

- Planning only.
- No implementation.
- No code generation.
- No schema redesign.
- Prototype data fixture: Yellowstone only.

Pages:

- Home
- Place
- Collection
- Asset
- Shop Collection
- Product

Foundation:

- Next.js Commerce frontend.
- Shopify for product, cart, checkout, price, inventory, and variants.
- FastAPI for Nature & Culture public data.
- PostgreSQL as Nature & Culture authority.
- Neo4j projection for related-content exploration only.

## Prototype Content Anchor

Canonical place:

- Place: Yellowstone
- Working slug: `yellowstone`
- Primary page route: `/en/places/yellowstone`

Prototype collection:

- Collection: Yellowstone Natural History
- Working slug: `yellowstone-natural-history`
- Editorial route: `/en/collections/yellowstone-natural-history`
- Shop route: `/en/collections/yellowstone-natural-history`

Prototype asset:

- Asset: one rights-cleared BHL or Smithsonian visual asset connected to Yellowstone.
- Working route: `/en/assets/{asset_id_or_slug}`

Prototype product:

- Product: one Shopify product derived from the prototype asset.
- Working route: `/en/products/{product_handle}`

## Page Map

### 1. Home

Domain:

- `natureandculture.net`

Route:

- `/en`

Purpose:

- Introduce the prototype using Yellowstone as the sole featured place and route users into the place, collection, asset, and shop paths.

Sections:

1. Header.
2. Yellowstone hero.
3. Featured Yellowstone collection.
4. Featured Yellowstone asset.
5. Prototype pipeline: Place -> Collection -> Asset -> Product.
6. Shop callout.
7. Footer.

Primary CTAs:

- Explore Yellowstone.
- View Collection.
- Shop Yellowstone.

Data source:

- FastAPI for place, collection, asset context.
- Shopify only for shop/product preview.

### 2. Place

Domain:

- `natureandculture.net`

Route:

- `/en/places/yellowstone`

Purpose:

- Present Yellowstone as the geographic anchor for the prototype.

Sections:

1. Header.
2. Breadcrumbs.
3. Place hero.
4. Place facts.
5. Featured collection.
6. Connected asset.
7. Related concepts.
8. Graph preview.
9. Shop callout.
10. Footer.

Primary CTAs:

- View Yellowstone Collection.
- Shop Products.

Data source:

- FastAPI for Yellowstone place, collection, asset, opportunity, and concepts.
- Neo4j projection for related concepts and graph preview.

### 3. Collection

Domain:

- `natureandculture.net`

Route:

- `/en/collections/yellowstone-natural-history`

Purpose:

- Present the governed editorial collection for Yellowstone.

Sections:

1. Header.
2. Breadcrumbs.
3. Collection hero.
4. Collection stats.
5. Asset gallery.
6. Place context.
7. Source and rights panel.
8. Product preview.
9. Related graph preview.
10. Footer.

Primary CTAs:

- View Asset.
- Shop Collection.

Data source:

- FastAPI for collection, collection assets, places, rights, export metadata.
- Shopify for products linked by collection metafield.

### 4. Asset

Domain:

- `natureandculture.net`

Route:

- `/en/assets/{asset_id_or_slug}`

Purpose:

- Present one Yellowstone-connected rights-cleared visual asset with provenance and commerce links.

Sections:

1. Header.
2. Breadcrumbs.
3. Asset viewer.
4. Asset metadata.
5. Rights verification.
6. Source record.
7. Connected Yellowstone place.
8. Containing collection.
9. Product preview.
10. Footer.

Primary CTAs:

- View Collection.
- Buy Product.

Data source:

- FastAPI for asset, rights, provenance, place, collection.
- Shopify for product linked by asset metafield.

### 5. Shop Collection

Domain:

- `natureandculture.shop`

Route:

- `/en/collections/yellowstone-natural-history`

Purpose:

- Sell products grouped under the Yellowstone Natural History collection.

Sections:

1. Commerce header.
2. Shop collection hero.
3. Product grid.
4. Collection story panel.
5. Rights assurance band.
6. Link to editorial collection page.
7. Footer.

Primary CTAs:

- View Product.
- Explore Story.

Data source:

- Shopify for collection and products.
- FastAPI for Nature & Culture collection context.

### 6. Product

Domain:

- `natureandculture.shop`

Route:

- `/en/products/{product_handle}`

Purpose:

- Sell one product derived from the Yellowstone prototype asset.

Sections:

1. Commerce header.
2. Product media gallery.
3. Purchase panel.
4. Product details.
5. Source asset story.
6. Yellowstone place context.
7. Rights assurance.
8. Related products.
9. Footer.

Primary CTAs:

- Add to Cart.
- Checkout.
- View Source Asset.

Data source:

- Shopify for product, variants, price, availability, cart, checkout.
- FastAPI for asset, collection, place, and rights context.

## Component Map

### Shared Components

| Component | Used On | Responsibility |
| --- | --- | --- |
| `LocalizedText` | All | Render JSONB language dictionaries with fallback |
| `SiteHeader` | Home, Place, Collection, Asset | Editorial navigation |
| `ShopHeader` | Shop Collection, Product | Commerce navigation and cart |
| `Breadcrumbs` | Place, Collection, Asset, Product | Route context |
| `Footer` | All | Global links, rights, source policy |
| `RightsAssuranceBand` | Collection, Asset, Shop Collection, Product | Public-domain/CC0 confidence |
| `GraphPreview` | Place, Collection | Small Neo4j projection preview |
| `ShopCallout` | Home, Place, Asset | Bridge to Shopify route |

### Home Components

| Component | Data |
| --- | --- |
| `YellowstoneHero` | Place title, summary, hero asset |
| `FeaturedCollectionCard` | Collection title, summary, cover asset |
| `FeaturedAssetCard` | Asset image, title, rights |
| `PrototypePipeline` | Static labels and linked route targets |
| `ShopCollectionCallout` | Shopify collection handle and cover image |

### Place Components

| Component | Data |
| --- | --- |
| `PlaceHero` | Yellowstone title, summary, description, hero image |
| `PlaceFactPanel` | Country, designation, source IDs, area if present |
| `PlaceCollectionRail` | Collections linked to Yellowstone |
| `PlaceAssetRail` | Assets linked to Yellowstone |
| `ConceptPillList` | Related concepts from PostgreSQL/Neo4j |

### Collection Components

| Component | Data |
| --- | --- |
| `CollectionHero` | Collection title, summary, cover asset |
| `CollectionStats` | Asset count, place count, rights summary |
| `AssetGallery` | Ordered collection assets |
| `PlaceContextPanel` | Yellowstone context |
| `SourceRightsPanel` | Rights and provenance |
| `ProductPreviewRail` | Shopify products linked to collection |

### Asset Components

| Component | Data |
| --- | --- |
| `AssetViewer` | Image URL, alt text, zoom availability |
| `AssetMetadataPanel` | Title, summary, source metadata |
| `RightsPanel` | Rights status, verified by/at, source URL |
| `SourceRecordPanel` | BHL/Smithsonian source record |
| `RelatedCollectionCard` | Yellowstone collection |
| `RelatedProductCard` | Shopify product linked by asset |

### Shop Collection Components

| Component | Data |
| --- | --- |
| `ShopCollectionHero` | Shopify collection plus NC collection context |
| `ProductGrid` | Shopify products |
| `ProductFilterBar` | Product type, availability, price |
| `CollectionStoryPanel` | NC collection summary and editorial link |
| `EditorialLinkCard` | Link to `.net` collection page |

### Product Components

| Component | Data |
| --- | --- |
| `ProductMediaGallery` | Shopify product media |
| `ProductPurchasePanel` | Price, variants, availability, add to cart |
| `VariantSelector` | Shopify variants |
| `ProductStoryPanel` | NC asset, place, collection context |
| `SourceAssetCard` | Linked asset from FastAPI |
| `ShippingReturnsPanel` | Shopify/static commerce policy |

## API Map

### Home

FastAPI:

- `GET /public/places/yellowstone?locale=en`
- `GET /public/collections/yellowstone-natural-history?locale=en`
- `GET /public/collections/yellowstone-natural-history/assets?locale=en`

Shopify:

- Collection by handle: `yellowstone-natural-history`
- Products by collection handle: `yellowstone-natural-history`

Neo4j:

- Not required for first prototype render.

### Place

FastAPI:

- `GET /public/places/yellowstone?locale=en`
- `GET /public/places/{place_id}/collections?locale=en`
- `GET /public/places/{place_id}/assets?locale=en`
- `GET /public/places/{place_id}/opportunities?locale=en`

Neo4j projection:

- `GET /public/graph/place/{place_id}?depth=1&locale=en`

Shopify:

- Optional product previews by place metafield: `nc.place_id`.

### Collection

FastAPI:

- `GET /public/collections/yellowstone-natural-history?locale=en`
- `GET /public/collections/{collection_id}/assets?locale=en`
- `GET /public/collections/{collection_id}/places?locale=en`
- `GET /public/collections/{collection_id}/products?locale=en`

Shopify:

- Products by collection metafield or handle.

Neo4j projection:

- `GET /public/graph/collection/{collection_id}?depth=1&locale=en`

### Asset

FastAPI:

- `GET /public/assets/{asset_id_or_slug}?locale=en`
- `GET /public/assets/{asset_id}/places?locale=en`
- `GET /public/assets/{asset_id}/collections?locale=en`
- `GET /public/assets/{asset_id}/products?locale=en`

Shopify:

- Product lookup by metafield: `nc.asset_id`.

Neo4j projection:

- Optional related concepts by asset ID.

### Shop Collection

Shopify:

- Collection by handle: `yellowstone-natural-history`
- Products by collection handle.

FastAPI:

- `GET /public/collections/by-shopify-handle/yellowstone-natural-history?locale=en`
- `GET /public/collections/{collection_id}/assets?locale=en`
- `GET /public/collections/{collection_id}/places?locale=en`

Neo4j:

- Not required for v1 prototype.

### Product

Shopify:

- Product by handle.
- Product variants.
- Cart create/update.
- Checkout handoff.

FastAPI:

- `GET /public/products/by-shopify-handle/{product_handle}/context?locale=en`
- `GET /public/assets/{asset_id}?locale=en`
- `GET /public/collections/{collection_id}?locale=en`
- `GET /public/places/{place_id}?locale=en`

Neo4j:

- Not required for v1 prototype.

## Prototype Data Checklist

Required Yellowstone records:

- One active/published Yellowstone place.
- One approved/published Yellowstone collection.
- One rights-cleared asset connected to Yellowstone.
- One opportunity connecting the asset to place/concept context.
- One Shopify collection linked to `nc.collection_id`.
- One Shopify product linked to:
  - `nc.asset_id`
  - `nc.collection_id`
  - `nc.place_id`
  - `nc.opportunity_id`

Required multilingual fields:

- Place `title`, `summary`, `description`.
- Collection `title`, `summary`, `description`.
- Asset `title`, `summary`, `description` where available.
- Product editorial context from FastAPI.

Minimum locale:

- `en`

Additional locales can use fallback behavior until translations are available.

## Prototype Build Order

1. Product.
2. Shop Collection.
3. Collection.
4. Asset.
5. Place.
6. Home.

Reason:

- Product and shop collection validate Shopify plus NC context mapping first.
- Collection and asset validate the PostgreSQL/FastAPI public data path.
- Place and home can then compose the verified pieces.
