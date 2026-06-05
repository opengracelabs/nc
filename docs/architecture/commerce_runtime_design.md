# Commerce Runtime Design

Mission:

- Design the runtime path from Nature & Culture Collection to generated products, Shopify storefront, Gelato/Lulu fulfillment, and Etsy marketplace listings.

Boundaries:

- No implementation.
- No code generation.
- No schema redesign.
- PostgreSQL remains the Nature & Culture authority.
- Shopify remains the commerce catalog, cart, checkout, and primary order authority.
- Gelato and Lulu are fulfillment providers.
- Etsy is a marketplace syndication channel, not the canonical catalog.

Runtime model:

```text
Collection
↓
Product Generation
↓
Shopify
↓
Gelato / Lulu
↓
Etsy
```

## API Evaluation

### Shopify API

Role:

- Primary commerce catalog.
- Primary storefront.
- Cart and checkout.
- Product/variant/media/metafield authority for sellable products.

Relevant API surfaces:

- Admin GraphQL API for product creation, variant creation, media, metafields, publications, and bulk operations.
- Storefront API for public product, collection, cart, and checkout flows.
- Webhooks for order creation, payment, fulfillment, and product lifecycle events.

Strengths:

- Strongest fit as the commerce hub.
- Product and variant model supports wall art size/material variants.
- Metafields can preserve Nature & Culture IDs.
- GraphQL Admin supports bulk variant operations.
- Storefront API fits Next.js Commerce.
- Mature webhook ecosystem.

Constraints:

- Product generation must respect Shopify product/variant limits and media workflow.
- Shopify should not become the source of truth for rights, provenance, asset lineage, or collection governance.
- Marketplace syndication needs explicit mapping; Etsy should not be treated as automatic Shopify parity.

Recommended use:

- Generate Shopify products from approved Nature & Culture collection assets.
- Attach canonical IDs using metafields:
  - `nc.collection_id`
  - `nc.asset_id`
  - `nc.opportunity_id`
  - `nc.place_id`
  - `nc.provider`
  - `nc.fulfillment_profile`
  - `nc.rights_status`
  - `nc.source_record_id`

### Gelato API

Role:

- Primary automated fulfillment provider for wall art, fashion, home, gifts, cards, calendars, and some education products.

Relevant API surfaces:

- Product catalog API for catalogs and product UIDs.
- Order create API with `orderReferenceId`, `customerReferenceId`, and `itemReferenceId`.
- Webhooks for order status, item status, tracking, delivery estimate, and store product events.

Strengths:

- Strong automation model.
- Simple one-request order creation for many product types.
- Explicit internal reference IDs map cleanly to Shopify order and line item IDs.
- Product UID model is suitable for deterministic product generation.
- Webhook lifecycle is suitable for fulfillment status sync.

Constraints:

- Print quality and production routing must be sample-validated by product family.
- Provider-specific product UID catalog must be cached and versioned internally.
- Multi-provider order splitting can happen; runtime must tolerate connected orders and item-level status.

Recommended use:

- Fulfill non-book products by default:
  - Wall art
  - Fashion
  - Home
  - Gifts
  - Cards
  - Calendars where Gelato quality is accepted

### Lulu Direct API

Role:

- Specialist fulfillment provider for books, education products, workbooks, art books, and some calendars.

Relevant API surfaces:

- Print Job API.
- Product/package model using POD package IDs.
- Cost calculation.
- Print-job status checks.
- `PRINT_JOB_STATUS_CHANGED` webhook.

Strengths:

- Strongest book automation fit.
- Explicit print-job lifecycle.
- Sandbox support.
- Webhook signatures via HMAC.
- Reusable printable file IDs can reduce repeat file transfer.

Constraints:

- Book files must be print-ready and hosted at accessible URLs.
- Lulu API is separate from Lulu account projects; files from Lulu projects cannot be pulled directly by API.
- Product construction is more technical than Gelato because trim, binding, paper, quality, and cover options must be encoded correctly.
- Poor fit for fashion/home/gift runtime.

Recommended use:

- Fulfill:
  - Books
  - Field guides
  - Educational workbooks
  - Premium collection catalogs
  - Book-like calendars if selected after samples

### Etsy API

Role:

- Marketplace syndication channel.
- Secondary sales channel for selected products.

Relevant API surfaces:

- Open API v3 for listings.
- Inventory/listing management.
- Shop management.
- Receipts/order retrieval.
- Shipment tracking submission.

Strengths:

- Good marketplace reach for gifts, wall art, and home products.
- Listings can be automated enough for selected catalog syndication.
- Receipt and tracking APIs support order visibility.

Constraints:

- Etsy should not be a fulfillment coordinator.
- Listing taxonomy, attributes, personalization, production partner policy, and marketplace compliance require careful manual rules.
- Marketplace listing copy may need separate SEO treatment.
- Etsy order handling should either route back to the same fulfillment adapter or remain limited until operationally proven.

Recommended use:

- Publish a curated subset from Shopify/Nature & Culture to Etsy.
- Start with wall art and gifts.
- Do not launch Etsy with books first.
- Keep Etsy listing IDs mapped back to Shopify product IDs and Nature & Culture IDs.

## API Architecture

### Authority Boundaries

PostgreSQL:

- Collection governance.
- Asset rights and provenance.
- Asset-to-opportunity-to-place relationships.
- Product generation intent and audit trail, if implemented later.

Shopify:

- Sellable product catalog.
- Product handles.
- Product media visible to customers.
- Variants, prices, availability.
- Cart and checkout.
- Shopify order IDs.

Gelato:

- Non-book fulfillment execution.
- Provider order ID.
- Item-level fulfillment status.
- Tracking details.

Lulu:

- Book fulfillment execution.
- Print-job ID.
- Print-job status.
- Tracking details.

Etsy:

- Marketplace listing.
- Marketplace receipt/order ID.
- Marketplace shipment tracking submission.

### Runtime Services

Recommended service boundaries:

- `product_generation_service`
  - Inputs: approved Collection, assets, product templates, provider catalog mappings.
  - Outputs: product generation plan and Shopify product payloads.

- `shopify_catalog_sync`
  - Creates/updates Shopify products, variants, media, collections, metafields.
  - Publishes products to configured channels.

- `fulfillment_router`
  - Maps Shopify order line items to Gelato or Lulu.
  - Splits orders by provider.
  - Sends fulfillment orders to provider APIs.

- `provider_status_sync`
  - Consumes Gelato and Lulu webhooks.
  - Updates fulfillment state in PostgreSQL and Shopify.

- `etsy_listing_sync`
  - Creates/updates Etsy listings from approved Shopify/Nature & Culture products.
  - Maintains listing ID mappings.

- `etsy_order_bridge`
  - Optional later service.
  - Pulls Etsy receipts and routes them into the same provider fulfillment flow.

### Identifier Map

Every runtime event needs stable IDs:

| Domain | Required IDs |
| --- | --- |
| PostgreSQL | `collection_id`, `asset_id`, `opportunity_id`, `place_id` |
| Shopify | `product_id`, `variant_id`, `collection_id`, `order_id`, `line_item_id` |
| Gelato | `orderReferenceId`, `itemReferenceId`, `orderId`, `productUid` |
| Lulu | `external_id`, `print_job_id`, `pod_package_id`, `printable_id` |
| Etsy | `listing_id`, `receipt_id`, `transaction_id`, `shop_id` |

Canonical internal reference format:

```text
nc:{collection_id}:{asset_id}:{product_type}:{variant_key}
```

Provider order reference format:

```text
shopify:{shopify_order_id}
shopify-line:{shopify_line_item_id}
etsy:{etsy_receipt_id}
etsy-line:{etsy_transaction_id}
```

## Automation Architecture

### Product Lifecycle

```text
approved_collection
  -> generate_product_plan
  -> create_shopify_products
  -> QA_review
  -> publish_shopify
  -> optionally_publish_etsy
  -> receive_order
  -> route_fulfillment
  -> provider_order
  -> provider_webhook
  -> sync_tracking
  -> complete_order
```

### Shopify Order Flow

1. Customer orders on `natureandculture.shop`.
2. Shopify creates order.
3. Shopify order webhook triggers runtime.
4. Runtime reads line item metafields.
5. Fulfillment router selects provider:
   - Gelato for wall art, fashion, home, gifts.
   - Lulu for books and education products.
6. Runtime creates provider order/print job.
7. Provider webhook updates status.
8. Runtime posts tracking/fulfillment back to Shopify.

### Etsy Order Flow

Initial recommended mode:

1. Etsy listing exists as a curated mirror of a Shopify product.
2. Etsy order is received.
3. Etsy receipt polling or webhook-equivalent scheduled sync imports order.
4. Runtime maps Etsy transaction to Nature & Culture product mapping.
5. Fulfillment router sends order to Gelato or Lulu.
6. Provider tracking is submitted back to Etsy.

Launch recommendation:

- Do Etsy listing sync before Etsy order automation.
- Keep Etsy fulfillment semi-manual until Gelato/Lulu routing is proven through Shopify orders.

### Provider Routing Rules

Gelato:

- `wall_art`
- `fashion`
- `home`
- `gifts`
- `cards`
- `poster`
- `calendar` unless Lulu selected for a book-like calendar

Lulu:

- `book`
- `field_guide`
- `education_workbook`
- `collection_catalog`
- `premium_calendar` if using Lulu Wire-O/calendar product specs

Reject or manual review:

- Missing provider product UID/package ID.
- Missing print file.
- Missing rights-cleared asset.
- Missing shipping address or phone when required.
- Unsupported destination.
- Product template version mismatch.

## Product Generation Architecture

### Inputs

Required Nature & Culture inputs:

- Approved collection.
- Ordered collection assets.
- Rights-cleared assets only.
- Asset image or print-ready derivative.
- Place and concept context.
- Localized title, summary, and description.
- Product template definitions.

Required provider inputs:

- Gelato product UID for non-book items.
- Lulu POD package ID for book items.
- Print area dimensions.
- Safe area and bleed rules.
- File format requirements.
- Destination availability.

Required Shopify inputs:

- Product title.
- Product handle.
- Product description.
- Media.
- Variants.
- Price.
- Product type.
- Vendor.
- Tags.
- Collections.
- Metafields.

### Product Template Families

Wall Art:

- Provider: Gelato primary, Printful fallback if added later.
- Variants: size, frame, material.
- Source asset requirement: high-resolution image.
- Shopify product type: `Wall Art`.

Books:

- Provider: Lulu.
- Variants: paperback, hardcover, premium color where applicable.
- Source requirement: print-ready interior PDF and cover PDF.
- Shopify product type: `Book`.

Fashion:

- Provider: Gelato.
- Variants: size, color, garment type.
- Source requirement: artwork adapted to print area.
- Shopify product type: `Apparel`.

Home:

- Provider: Gelato.
- Variants: product type, size, color where applicable.
- Shopify product type: `Home`.

Gifts:

- Provider: Gelato.
- Variants: product type, pack size, finish.
- Shopify product type: `Gift`.

Education:

- Provider: Lulu for workbooks/books; Gelato for cards/posters.
- Variants: format and binding.
- Shopify product type: `Education`.

### Product Generation Steps

1. Select collection asset.
2. Validate rights and provenance.
3. Select product template family.
4. Select provider route.
5. Generate print file derivative.
6. Validate print file dimensions and format.
7. Generate Shopify product copy from collection/place/asset context.
8. Generate Shopify variants from provider product mapping.
9. Attach canonical IDs as Shopify metafields.
10. Create Shopify draft product.
11. Run QA review.
12. Publish to Shopify.
13. Optionally syndicate to Etsy.

### Product Copy Rules

Product title pattern:

```text
{Asset or Collection Title} - {Product Type}
```

Subtitle/description should include:

- Place context.
- Collection context.
- Source institution.
- Rights status.
- Material/format details.

Do not include unsupported claims:

- No invented species/place relationships.
- No rights language beyond verified rights.
- No source attribution not present in PostgreSQL.

### Product Metafields

Required namespace: `nc`

Required product metafields:

- `nc.collection_id`
- `nc.asset_id`
- `nc.opportunity_id`
- `nc.place_id`
- `nc.source`
- `nc.rights_status`
- `nc.provider`
- `nc.provider_product_key`
- `nc.product_template_version`

Required variant metafields:

- `nc.provider_variant_key`
- `nc.print_file_id`
- `nc.print_file_checksum`
- `nc.fulfillment_route`

### QA Gates

A product cannot publish until:

- Collection is approved or published.
- Asset has explicit Public Domain or CC0 rights.
- Print file exists and passes dimensions/format checks.
- Provider product mapping exists.
- Shopify draft product exists.
- Product preview/mockup exists.
- Price and margin are set.
- Shipping destination policy is known.
- Human review approves title, image crop, and attribution.

## Recommended V1 Runtime

V1 should launch in this order:

1. Shopify catalog generation from one approved collection.
2. Gelato fulfillment for one wall art product.
3. Lulu fulfillment for one book or workbook product.
4. Shopify order-to-provider fulfillment automation.
5. Provider webhook-to-Shopify tracking sync.
6. Etsy listing sync for selected wall art.
7. Etsy order bridge only after Shopify fulfillment proves stable.

Do not make Etsy part of the critical checkout path for v1.

Do not use Lulu for general gifts/home/fashion.

Do not use Gelato for flagship books until samples prove quality.

## Open Questions

- Which Gelato product UIDs are approved for the first wall art formats?
- Which Lulu POD package IDs are approved for first books/workbooks?
- Will Etsy orders be fulfilled automatically in v1 or listed only?
- What is the minimum print derivative pipeline before product generation can be automated?
- Which Shopify markets and languages are required at first launch?
