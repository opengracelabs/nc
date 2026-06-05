# Wireframe Specifications

Scope:

- `natureandculture.net`
- `natureandculture.shop`

Foundation:

- Next.js Commerce
- Shopify
- FastAPI
- PostgreSQL
- Neo4j projection

Boundaries:

- No implementation yet.
- No code generation yet.
- No schema redesign.
- PostgreSQL remains the authority for Nature & Culture data.
- Shopify remains the authority for commerce product, variant, cart, checkout, inventory, and payment data.
- Neo4j is a projection used for related-content exploration, not a write authority.

## Multilingual Rules

Multilingual support is required from day one.

Assumed data shape:

- `title = JSONB language dictionary`
- `summary = JSONB language dictionary`
- `description = JSONB language dictionary`

Frontend language behavior:

- Every page receives a locale from route, cookie, or browser preference.
- Preferred route shape: `/{locale}/...`, for example `/en/places/great-barrier-reef`.
- Language fallback order: requested locale -> `en` -> first available language value -> empty state.
- The UI must never expose raw JSON.
- Search should query all available languages but rank exact-locale matches higher.
- URLs should remain stable across locales; slugs may be locale-specific later, but v1 can use canonical English slugs.

Required shared multilingual component behavior:

- `LocalizedText`: renders language dictionaries with fallback.
- `LanguageSwitcher`: preserves current entity and route when switching locale.
- `MissingTranslationBadge`: editorial-only indicator; not visible on public pages.
- Metadata tags: localized page title, description, Open Graph title, and Open Graph description.

## Shared Page Shell

### `natureandculture.net`

Primary purpose: editorial discovery, place context, collections, assets, provenance, and knowledge graph navigation.

Global components:

- Header with logo, primary nav, search, language selector, and shop link.
- Primary nav: Places, Collections, Assets, Illustrators, Search.
- Footer with source attribution, rights policy, about, contact, and shop link.
- Breadcrumbs on detail pages.
- Related-content rail on detail pages.
- Newsletter or launch notification module optional for v1.

### `natureandculture.shop`

Primary purpose: commerce conversion for rights-cleared products and collections.

Global components:

- Commerce header with logo, product search, cart, language selector, and `.net` link.
- Primary nav: Collections, Wall Art, Calendars, Cards, Puzzles, Books.
- Shopify cart drawer.
- Product recommendation rail.
- Footer with shipping, returns, rights, contact, and editorial link.

## Shared Data Contracts

### Nature & Culture API

Base role: FastAPI reads PostgreSQL authority data and returns public-ready records.

Public API response rules:

- All public records must include `id`, localized dictionaries, `status`, `provenance`, and timestamps when relevant.
- Public endpoints should return only approved, published, or active records.
- Rights fields must be explicit on asset and product-adjacent responses.
- Place, collection, asset, opportunity, illustrator, and graph relationships should be retrievable independently.

### Shopify API

Base role: Shopify owns commerce products.

Required integration data:

- Product handle.
- Product title and description.
- Product images.
- Variants.
- Price.
- Availability.
- Cart and checkout URLs.
- Product metafields linking back to Nature & Culture IDs:
  - `nc.collection_id`
  - `nc.asset_id`
  - `nc.place_id`
  - `nc.opportunity_id`

### Neo4j Projection API

Base role: related-content graph traversal.

Required projected node types:

- Designation
- Place
- Concept
- Opportunity
- Asset
- Collection

Frontend usage:

- Do not query Neo4j for primary page authority.
- Use Neo4j for related entities, graph previews, and "explore connections" modules.
- Every graph result must include PostgreSQL IDs so the UI links back to canonical detail pages.

## 1. Homepage

Domain: `natureandculture.net`

Route:

- `/{locale}`

Purpose:

- Introduce Nature & Culture as a place-centered public-domain illustration and commerce platform.
- Move users quickly into flagship places, collections, and search.

Wireframe:

1. Header.
2. Full-bleed hero with flagship collection image.
3. Hero text:
   - localized `title`
   - localized `summary`
   - primary CTA: Explore Places
   - secondary CTA: Shop Collections
4. Featured designation/family strip.
5. Featured places grid.
6. Featured collections band.
7. Featured assets carousel.
8. "How it connects" section: Place -> Opportunity -> Asset -> Collection -> Product.
9. Source/rights trust band.
10. Footer.

Page components:

- `HeroFeature`
- `DesignationStrip`
- `PlaceCardGrid`
- `CollectionRail`
- `AssetCarousel`
- `PipelineExplainer`
- `RightsTrustBand`
- `LocalizedSEO`

Required APIs:

- `GET /public/home?locale={locale}`
- `GET /public/places?featured=true&limit=6&locale={locale}`
- `GET /public/collections?featured=true&limit=6&locale={locale}`
- `GET /public/assets?featured=true&limit=12&locale={locale}`
- `GET /public/graph/featured?locale={locale}`

Data requirements:

- Featured collection image.
- Featured places with `title`, `summary`, country codes, designation labels, hero asset.
- Featured collections with title, summary, asset count, place count.
- Featured assets with image URL, title, rights, source, creator/illustrator.
- Localized metadata.

## 2. Place Page

Domain: `natureandculture.net`

Route:

- `/{locale}/places/{place_slug}`

Purpose:

- Present one place as the geographic anchor for opportunities, assets, and collections.

Wireframe:

1. Header.
2. Breadcrumbs.
3. Place hero:
   - localized place title
   - localized summary
   - country/region
   - designation badges
   - hero asset or map image
4. Place facts panel:
   - designation family
   - source IDs
   - inscription/designation dates where available
   - area/core/buffer where available
5. Map/context panel.
6. Collections featuring this place.
7. Assets connected to this place.
8. Opportunities connected to this place.
9. Related concepts.
10. Graph preview.
11. Footer.

Page components:

- `PlaceHero`
- `DesignationBadgeList`
- `PlaceFactPanel`
- `MapContextPanel`
- `CollectionRail`
- `AssetGrid`
- `OpportunityList`
- `ConceptPillList`
- `GraphPreview`
- `SourceProvenancePanel`

Required APIs:

- `GET /public/places/{place_id_or_slug}?locale={locale}`
- `GET /public/places/{place_id}/collections?locale={locale}`
- `GET /public/places/{place_id}/assets?locale={locale}`
- `GET /public/places/{place_id}/opportunities?locale={locale}`
- `GET /public/places/{place_id}/graph?depth=1&locale={locale}`

Data requirements:

- Place `title`, `summary`, `description`.
- Geometry or map-safe derived context.
- Designation records.
- Related collections.
- Related assets.
- Related opportunities.
- Related concepts from PostgreSQL/Neo4j projection.
- Provenance and source attribution.

## 3. Collection Page

Domain: `natureandculture.net`

Route:

- `/{locale}/collections/{collection_slug}`

Purpose:

- Present a governed collection as the main editorial unit linking places, assets, and products.

Wireframe:

1. Header.
2. Breadcrumbs.
3. Collection hero:
   - localized title
   - localized summary
   - cover asset
   - collection status/rights indicator
   - shop CTA
4. Collection metadata:
   - places represented
   - asset count
   - rights summary
   - source mix
5. Asset gallery.
6. Place context rail.
7. Illustrator/creator rail.
8. Product previews from Shopify.
9. Provenance and rights section.
10. Related collections.
11. Footer.

Page components:

- `CollectionHero`
- `CollectionStats`
- `AssetGallery`
- `PlaceContextRail`
- `IllustratorRail`
- `ShopProductRail`
- `RightsProvenancePanel`
- `RelatedCollectionRail`

Required APIs:

- `GET /public/collections/{collection_id_or_slug}?locale={locale}`
- `GET /public/collections/{collection_id}/assets?locale={locale}`
- `GET /public/collections/{collection_id}/places?locale={locale}`
- `GET /public/collections/{collection_id}/illustrators?locale={locale}`
- `GET /public/collections/{collection_id}/products?locale={locale}`
- Shopify Storefront API product lookup by `nc.collection_id`.

Data requirements:

- Collection `title`, `summary`, `description`.
- Cover asset.
- Asset list ordered by collection sequence.
- Place list.
- Illustrator/creator list.
- Product handles and variant availability.
- Rights and export metadata.

## 4. Asset Page

Domain: `natureandculture.net`

Route:

- `/{locale}/assets/{asset_id_or_slug}`

Purpose:

- Present one rights-cleared visual asset with provenance, source, concept, place, and shop links.

Wireframe:

1. Header.
2. Breadcrumbs.
3. Asset viewer:
   - large image
   - zoom control where available
   - alt text
4. Asset title and summary.
5. Rights panel:
   - rights status
   - rights source URL
   - verified by/at
6. Source/provenance panel:
   - BHL or Smithsonian source
   - source record ID
   - publication/object metadata
7. Related places.
8. Related concepts/taxa.
9. Collections using this asset.
10. Product previews.
11. Footer.

Page components:

- `AssetViewer`
- `AssetMetadataHeader`
- `RightsPanel`
- `SourceRecordPanel`
- `RelatedPlaceRail`
- `ConceptPillList`
- `CollectionRail`
- `ShopProductRail`

Required APIs:

- `GET /public/assets/{asset_id}?locale={locale}`
- `GET /public/assets/{asset_id}/places?locale={locale}`
- `GET /public/assets/{asset_id}/collections?locale={locale}`
- `GET /public/assets/{asset_id}/products?locale={locale}`
- Shopify Storefront API product lookup by `nc.asset_id`.

Data requirements:

- Asset image URLs or signed public derivative URLs.
- `title`, `summary`, `description` where available.
- Rights verification fields.
- Source URL and source metadata.
- Related opportunity.
- Related concept.
- Related collection/product links.

## 5. Illustrator Page

Domain: `natureandculture.net`

Route:

- `/{locale}/illustrators/{illustrator_slug}`

Purpose:

- Present an illustrator/creator as an editorial route into assets and collections.

Wireframe:

1. Header.
2. Breadcrumbs.
3. Illustrator hero:
   - name
   - localized summary/biography if available
   - date range
   - primary image if available
4. Featured works grid.
5. Collections featuring this illustrator.
6. Places connected through depicted concepts/assets.
7. Source/provenance notes.
8. Related illustrators/creators.
9. Footer.

Page components:

- `IllustratorHero`
- `CreatorFactPanel`
- `AssetGrid`
- `CollectionRail`
- `PlaceContextRail`
- `GraphPreview`
- `SourceProvenancePanel`

Required APIs:

- `GET /public/illustrators/{illustrator_id_or_slug}?locale={locale}`
- `GET /public/illustrators/{illustrator_id}/assets?locale={locale}`
- `GET /public/illustrators/{illustrator_id}/collections?locale={locale}`
- `GET /public/illustrators/{illustrator_id}/places?locale={locale}`
- `GET /public/illustrators/{illustrator_id}/graph?depth=1&locale={locale}`

Data requirements:

- Creator/illustrator name.
- Localized biography fields where available.
- Asset list.
- Collection list.
- Related places and concepts.
- Source attribution.

## 6. Search Page

Domain: `natureandculture.net`

Route:

- `/{locale}/search`

Purpose:

- Unified discovery across places, collections, assets, illustrators, concepts, and opportunities.

Wireframe:

1. Header.
2. Search input with locale-aware placeholder.
3. Filter row:
   - content type
   - designation/source
   - rights
   - country/region
   - collection/product availability
4. Result tabs:
   - All
   - Places
   - Collections
   - Assets
   - Illustrators
   - Concepts
5. Results grid/list.
6. Related graph suggestions.
7. Empty state with suggested searches.
8. Footer.

Page components:

- `SearchInput`
- `SearchFilterBar`
- `SearchTabs`
- `SearchResultList`
- `AssetResultCard`
- `PlaceResultCard`
- `CollectionResultCard`
- `GraphSuggestionRail`
- `SearchEmptyState`

Required APIs:

- `GET /public/search?q={query}&locale={locale}&type={type}&limit={limit}&offset={offset}`
- `GET /public/search/suggest?q={query}&locale={locale}`
- `GET /public/graph/suggest?q={query}&locale={locale}`

Data requirements:

- Locale-weighted search index over title, summary, description, source IDs, illustrator names, place names, concept labels.
- Type-specific result cards.
- Rights and availability filters.
- Graph suggestions linked to canonical pages.

## 7. Shop Homepage

Domain: `natureandculture.shop`

Route:

- `/{locale}`

Purpose:

- Convert editorial interest into commerce browsing and purchase paths.

Wireframe:

1. Commerce header.
2. Shop hero:
   - featured collection image
   - localized shop headline
   - primary CTA: Shop Collections
   - secondary CTA: Explore the Story
3. Product category tiles:
   - Wall Art
   - Calendars
   - Cards
   - Puzzles
   - Books
4. Featured shop collections.
5. Bestselling/new products.
6. Rights-cleared assurance band.
7. Editorial bridge to `.net`.
8. Footer.

Page components:

- `ShopHero`
- `ProductCategoryTiles`
- `ShopCollectionGrid`
- `ProductGrid`
- `CartDrawer`
- `RightsAssuranceBand`
- `EditorialBridge`

Required APIs:

- Shopify Storefront API collections.
- Shopify Storefront API products.
- `GET /public/shop/home?locale={locale}`
- `GET /public/collections?shop_featured=true&locale={locale}`

Data requirements:

- Shopify collections/products.
- NC collection IDs linked through Shopify metafields.
- Product imagery.
- Price and availability.
- Localized editorial copy.

## 8. Shop Collection Page

Domain: `natureandculture.shop`

Route:

- `/{locale}/collections/{shopify_collection_handle}`

Purpose:

- Sell products grouped by a Nature & Culture governed collection.

Wireframe:

1. Commerce header.
2. Collection commerce hero:
   - product collection title
   - localized editorial summary from NC
   - cover image
   - link to full story on `.net`
3. Product grid with filters:
   - product type
   - price
   - size
   - availability
4. Source collection context:
   - places
   - assets
   - rights status
5. Related shop collections.
6. Footer.

Page components:

- `ShopCollectionHero`
- `ProductFilterBar`
- `ProductGrid`
- `CollectionStoryPanel`
- `RightsAssuranceBand`
- `RelatedShopCollectionRail`

Required APIs:

- Shopify Storefront API collection by handle.
- Shopify Storefront API products by collection.
- `GET /public/collections/by-shopify-handle/{handle}?locale={locale}`
- `GET /public/collections/{collection_id}/assets?locale={locale}`
- `GET /public/collections/{collection_id}/places?locale={locale}`

Data requirements:

- Shopify collection handle.
- NC collection ID metafield.
- Product list.
- NC collection title/summary/description.
- Rights summary.
- Place and asset context.

## 9. Product Page

Domain: `natureandculture.shop`

Route:

- `/{locale}/products/{product_handle}`

Purpose:

- Sell one Shopify product while preserving Nature & Culture source, rights, and story context.

Wireframe:

1. Commerce header.
2. Product media gallery.
3. Product purchase panel:
   - title
   - price
   - variant selectors
   - quantity
   - add to cart
   - checkout affordance
4. Story context:
   - source asset
   - collection
   - place
   - illustrator/creator
5. Rights assurance panel.
6. Product details and shipping.
7. Related products.
8. Related editorial links.
9. Footer.

Page components:

- `ProductMediaGallery`
- `ProductPurchasePanel`
- `VariantSelector`
- `AddToCartButton`
- `ProductStoryPanel`
- `RightsAssuranceBand`
- `ShippingReturnsPanel`
- `RelatedProductRail`
- `EditorialLinkRail`

Required APIs:

- Shopify Storefront API product by handle.
- Shopify Storefront API cart mutation.
- `GET /public/products/by-shopify-handle/{handle}/context?locale={locale}`
- `GET /public/assets/{asset_id}?locale={locale}`
- `GET /public/collections/{collection_id}?locale={locale}`

Data requirements:

- Shopify product title, description, images, variants, price, availability.
- Shopify metafields:
  - `nc.asset_id`
  - `nc.collection_id`
  - `nc.place_id`
  - `nc.opportunity_id`
- NC asset rights.
- NC source attribution.
- NC collection/place context.

## API Summary

Nature & Culture public FastAPI endpoints needed for v1:

- `GET /public/home`
- `GET /public/places`
- `GET /public/places/{id_or_slug}`
- `GET /public/places/{id}/collections`
- `GET /public/places/{id}/assets`
- `GET /public/places/{id}/opportunities`
- `GET /public/collections`
- `GET /public/collections/{id_or_slug}`
- `GET /public/collections/{id}/assets`
- `GET /public/collections/{id}/places`
- `GET /public/collections/{id}/illustrators`
- `GET /public/assets/{id_or_slug}`
- `GET /public/assets/{id}/places`
- `GET /public/assets/{id}/collections`
- `GET /public/illustrators/{id_or_slug}`
- `GET /public/illustrators/{id}/assets`
- `GET /public/search`
- `GET /public/search/suggest`
- `GET /public/graph/featured`
- `GET /public/graph/suggest`
- `GET /public/products/by-shopify-handle/{handle}/context`

Shopify Storefront API requirements:

- Product by handle.
- Collection by handle.
- Products by collection.
- Cart create/update.
- Checkout handoff.

Neo4j projection API requirements:

- Related entities by PostgreSQL ID.
- Search suggestions by graph neighborhood.
- Detail-page graph preview by node ID and depth.

## Data Requirements Summary

PostgreSQL authority data:

- Places with localized title/summary/description.
- Collections with localized title/summary/description.
- Assets with rights, provenance, image paths, and source metadata.
- Opportunities linking places, concepts, assets, and sources.
- Illustrators/creators as concepts or actor records.
- Collection membership and ordering.
- Product context mappings through Shopify metafields.

Shopify authority data:

- Products.
- Variants.
- Prices.
- Availability.
- Cart.
- Checkout.
- Product media.
- Product collections.

Neo4j projection data:

- Place, concept, opportunity, asset, collection relationships.
- Related-content traversal.
- Graph preview payloads.

## V1 Page Priority

Build order:

1. Shop Product Page.
2. Shop Collection Page.
3. Collection Page.
4. Asset Page.
5. Place Page.
6. Homepage.
7. Shop Homepage.
8. Search Page.
9. Illustrator Page.

Reasoning:

- Commerce pages validate the Shopify integration first.
- Collection and asset pages validate the Nature & Culture public API.
- Search and illustrator pages depend on richer indexes and relationship coverage, so they can follow after core detail pages.
