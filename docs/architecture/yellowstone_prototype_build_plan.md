# Yellowstone Prototype Build Plan

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Role | Lead Platform Engineer |
| Status | Build plan only |
| Scope | First working Yellowstone prototype |
| Inputs | Wireframe Constitution, Media Substrate, M36, PostGIS |
| Constraint | No architecture redesign |

## Mission

Build the first working Nature & Culture prototype around Yellowstone.

The prototype must prove the existing architecture can render a place-centered public-domain experience using:

- Homepage
- Yellowstone Place Page
- Map Viewer
- Media Viewer
- Collection Page
- Commerce Rail

This is a build plan, not a redesign. It uses the existing authority model:

```text
PostgreSQL + PostGIS  -> canonical place, spatial, collection, media, commerce context
MinIO                 -> media/file evidence and derivatives
UMS M36               -> source_item, source_record, media_file, media_rights,
                         media_technical_metadata, asset_delivery_manifest,
                         activation_target
FastAPI               -> public read APIs
Frontend              -> place-centered prototype surfaces
```

Neo4j, pgvector, foundation models, checkout, and Shopify sync are not required for this first working build.

## Prototype Success Path

A reviewer must be able to:

1. Open the Homepage.
2. Enter Yellowstone.
3. View Yellowstone as a place with facts, map, media, collection, and commerce rail.
4. Open an interactive Map Viewer focused on Yellowstone.
5. Open a Media Viewer for a rights-cleared Yellowstone asset.
6. Open the Yellowstone collection.
7. See commerce-ready product cards derived from activated assets.

## Prototype Content Anchor

Primary place:

- Name: Yellowstone National Park
- Slug: `yellowstone`
- Route: `/places/americas/yellowstone`
- Type: natural heritage / national park / UNESCO-aligned place

Prototype collection:

- Title: Icons of the American West: The Audubon Folio
- Slug: `yellowstone-icons-american-west`
- Route: `/collections/yellowstone-icons-american-west`
- Anchor: Yellowstone place + BHL natural history illustrations

Minimum media set:

| Role | Media type | Candidate source | Runtime use |
|---|---|---|---|
| Hero | image / photography | Smithsonian or public-domain Yellowstone landscape | Homepage + Place hero |
| Map | map | LOC/Hayden/Yellowstone historic map where rights allow | Map Viewer |
| Primary asset | image | BHL Audubon bison or Yellowstone iconic taxon plate | Media Viewer + Collection + Commerce Rail |
| Supporting assets | image / photography / poster | BHL, Smithsonian, LOC | Collection grid |

Commerce rail:

- At least 3 product cards.
- Product cards are prototype records derived from activated assets.
- No live checkout required.
- Product cards must show rights/provenance confidence and product family.

## Exact Implementation Order

Build from data authority outward.

1. Confirm M36 schema readiness and current table names.
2. Define Yellowstone seed fixture IDs and slugs.
3. Seed or verify `places` record with PostGIS geometry.
4. Seed M36 Phase 1 `media_type_registry` rows if missing.
5. Seed source institutions: BHL, Smithsonian, LOC as needed.
6. Seed `source_item` records for Yellowstone hero, map, primary asset, and supporting assets.
7. Seed immutable `source_record` snapshots.
8. Seed `media_rights` with `verified_pd` or `verified_cc0`.
9. Seed `media_technical_metadata` for media type, dimensions, subjects, and source fields.
10. Seed `media_file` and `media_derivative` references to MinIO or stable fixture URLs.
11. Seed `preservation_event` records for fixture file evidence.
12. Seed `asset_delivery_manifest` records, including IIIF-compatible manifests where available.
13. Seed `activation_target` records for Phase 1 activated assets.
14. Seed collection and collection membership records.
15. Seed commerce rail records linked to activation targets.
16. Implement FastAPI read endpoints.
17. Implement frontend data clients.
18. Build Homepage shell.
19. Build Yellowstone Place Page.
20. Build Map Viewer.
21. Build Media Viewer.
22. Build Collection Page.
23. Build Commerce Rail and wire it into Home, Place, Media, and Collection pages.
24. Run smoke tests and reviewer path.

## Database Requirements

Required existing authority tables:

- `places`
- collection tables: `collections`, `collection_assets`, `collection_places` or current equivalents
- commerce/product recommendation tables if already present
- public API compatible legacy opportunity tables where required

Required M36 objects:

- `media_type_registry`
- `source_item`
- `source_record`
- `media_file`
- `media_derivative`
- `media_rights`
- `media_technical_metadata`
- `preservation_event`
- `asset_delivery_manifest`
- `activation_target`
- `activation_target_downstream_link`

Required Yellowstone rows:

| Record class | Minimum |
|---|---:|
| Place | 1 Yellowstone record |
| PostGIS geometry | 1 centroid and preferably 1 boundary |
| Source institution | 3: BHL, Smithsonian, LOC |
| Source items | 6 minimum: hero, map, primary asset, 3 supporting assets |
| Source records | 1 per source item |
| Media rights | 1 current verified rights record per source item |
| Media technical metadata | 1 current record per source item |
| Media files | 1 master or fixture file per source item |
| Media derivatives | thumbnail + display derivative per source item |
| Delivery manifests | 1 IIIF/JSON-LD payload per source item where relevant |
| Activation targets | 1 per display/commerce eligible source item |
| Collection | 1 Yellowstone collection |
| Collection membership | 4 to 6 items |
| Commerce rail items | 3 product-card fixtures |

PostGIS requirements:

- Yellowstone centroid in WGS84.
- Yellowstone boundary polygon or simplified bounding polygon.
- Place envelope/bounds for map fit.
- Spatial query for media within or linked to the Yellowstone viewport.

Prototype PostGIS queries:

- Fetch place centroid and bounds by slug.
- Fetch media items linked to Yellowstone.
- Fetch media with geometry/bounds intersecting the map viewport.
- Fetch nearby places only if seeded; otherwise omit nearby rail.

## API Requirements

All endpoints are read-only for the prototype.

Homepage:

```text
GET /public/home?prototype=yellowstone
```

Yellowstone Place Page:

```text
GET /public/places/yellowstone
GET /public/places/yellowstone/media
GET /public/places/yellowstone/collections
GET /public/places/yellowstone/commerce-rail
```

Map Viewer:

```text
GET /public/map/places/yellowstone
GET /public/map/places/yellowstone/media?bbox={bbox}
GET /public/media/{source_item_id}/manifest
```

Media Viewer:

```text
GET /public/media/{source_item_id}
GET /public/media/{source_item_id}/manifest
GET /public/media/{source_item_id}/related
GET /public/media/{source_item_id}/commerce-rail
```

Collection Page:

```text
GET /public/collections/yellowstone-icons-american-west
GET /public/collections/yellowstone-icons-american-west/media
GET /public/collections/yellowstone-icons-american-west/commerce-rail
```

Commerce Rail:

```text
GET /public/commerce/rails/yellowstone
GET /public/commerce/rails/by-place/yellowstone
GET /public/commerce/rails/by-media/{source_item_id}
GET /public/commerce/rails/by-collection/yellowstone-icons-american-west
```

API response rules:

- Every media response includes rights, source, technical metadata, derivatives, manifest, and activation state.
- Every commerce card includes source item ID or collection ID, activation target ID, product family, rights badge, image derivative, CTA label, and prototype status.
- API must not return commerce cards for records without valid activation targets.
- Map endpoints return GeoJSON for place geometry and map/media markers.

## Frontend Requirements

Required routes:

```text
/
/places/americas/yellowstone
/map/yellowstone
/media/{source_item_slug_or_id}
/collections/yellowstone-icons-american-west
```

Commerce rail is a component, not a separate page.

Shared components:

- `GlobalHeader`
- `PageShell`
- `RightsBadge`
- `SourceBadge`
- `MediaCard`
- `CommerceRail`
- `CommerceCard`
- `PostGISMap`
- `IIIFViewer`
- `Breadcrumbs`

Homepage components:

- `HomeHero`
- `FeaturedPlacePanel`
- `FeaturedMediaRail`
- `FeaturedCollectionPanel`
- `HomeCommerceRail`

Yellowstone Place components:

- `PlaceHero`
- `PlaceFacts`
- `PlaceMapPreview`
- `PlaceMediaRails`
- `PlaceCollectionFeature`
- `PlaceCommerceRail`

Map Viewer components:

- `MapViewerShell`
- `MapLayerControls`
- `HistoricMapOverlay`
- `MediaMarkerLayer`
- `MapContextPanel`

Media Viewer components:

- `MediaViewerShell`
- `MediaMetadataPanel`
- `RightsProvenancePanel`
- `LinkedPlacePanel`
- `LinkedCollectionPanel`
- `MediaCommerceRail`

Collection components:

- `CollectionHero`
- `CollectionNarrative`
- `CollectionMediaGrid`
- `CollectionSourceSummary`
- `CollectionCommerceRail`

Frontend rules:

- Render seeded API data only; no hardcoded media or commerce cards after API fixtures exist.
- Show rights/provenance on every media and commerce card.
- Do not show commerce cards for assets without `activation_target`.
- Map Viewer uses PostGIS GeoJSON and viewport queries.
- Media Viewer uses `asset_delivery_manifest` first; derivative URL is fallback.
- Mobile supports Place, Map, Media, and Collection routes without hiding critical metadata.

## Seed Data Requirements

Place seed:

- `slug = 'yellowstone'`
- canonical name, summary, description
- country/region and designation tags
- centroid and boundary or bounding box
- source IDs: Wikidata/GeoNames if available, otherwise pending references

Minimum six media items:

1. Thomas Moran / Yellowstone landscape hero candidate.
2. Hayden or LOC historic Yellowstone map.
3. Audubon American Bison plate.
4. Grizzly bear plate or Yellowstone iconic fauna candidate.
5. Gray wolf plate or Yellowstone iconic fauna candidate.
6. Supporting Yellowstone photograph/poster/map.

Each media item needs:

- `source_item`
- `source_record`
- `media_rights`
- `media_technical_metadata`
- `media_file`
- `media_derivative`
- `preservation_event`
- `asset_delivery_manifest`
- `activation_target` when display/commerce eligible

Collection seed:

- title: `Icons of the American West: The Audubon Folio`
- slug: `yellowstone-icons-american-west`
- narrative
- cover source item
- ordered media membership
- linked Yellowstone place
- source summary
- rights summary

Commerce rail seed:

| Product | Source item | Product family |
|---|---|---|
| Yellowstone Bison Heritage Print | Audubon bison plate | wall_art |
| Yellowstone Expedition Map Print | historic map | wall_art |
| Icons of the American West Set | collection bundle | print_set |

Required commerce card fields:

- product title
- product family
- source item or collection ID
- activation target ID
- image derivative
- rights badge
- CTA label
- price placeholder
- product status: `prototype`

## Week 1

Goal: authoritative Yellowstone fixture and API spine.

Exact order:

1. Confirm current database schema and M36 readiness.
2. Create Yellowstone seed manifest listing all fixture IDs, slugs, and source URLs.
3. Seed or verify Yellowstone `places` row.
4. Add centroid and boundary/bounds in PostGIS.
5. Seed source institutions for BHL, Smithsonian, and LOC where missing.
6. Seed M36 Phase 1 media type registry rows for `image`, `map`, `photography`, `poster`.
7. Seed six `source_item` rows.
8. Seed `source_record`, `media_rights`, and `media_technical_metadata` for each item.
9. Seed `media_file`, `media_derivative`, and `preservation_event` fixture records.
10. Seed `asset_delivery_manifest` records.
11. Seed `activation_target` records for display/commerce-eligible items.
12. Implement read endpoints for place, place media, collection shell, media detail, and commerce rail.
13. Add API smoke tests for seeded IDs and rights/activation gates.

Exit criteria:

- `/public/places/yellowstone` returns canonical place plus GeoJSON.
- `/public/places/yellowstone/media` returns seeded media only.
- `/public/media/{id}` returns rights, source, technical metadata, manifest, and derivatives.
- Commerce rail excludes non-activated items.

## Week 2

Goal: Homepage and Yellowstone Place Page working against APIs.

Exact order:

1. Build frontend API client and typed response shapes.
2. Build shared shell: header, breadcrumbs, rights badge, source badge, media card.
3. Build `CommerceRail` and `CommerceCard` as reusable components.
4. Build Homepage with Yellowstone hero, featured media, collection feature, and commerce rail.
5. Build Yellowstone Place Page hero and facts.
6. Build Place map preview from PostGIS GeoJSON.
7. Build Place media rails grouped by media type.
8. Build Place collection feature.
9. Wire Place commerce rail.
10. Add responsive tablet/mobile states for Homepage and Place Page.
11. Run frontend smoke path from Homepage to Place Page.

Exit criteria:

- Homepage renders with API-backed Yellowstone data.
- Place Page displays PostGIS map preview, media rails, collection, and commerce rail.
- Rights/source badges are visible on every media and commerce card.

## Week 3

Goal: Map Viewer and Media Viewer.

Exact order:

1. Select map rendering library already compatible with the frontend stack.
2. Build `PostGISMap` component using GeoJSON from API.
3. Build `/map/yellowstone` viewer shell.
4. Add Yellowstone boundary/bounds fit behavior.
5. Add media marker layer from `/public/map/places/yellowstone/media`.
6. Add historic map overlay using delivery manifest or derivative fallback.
7. Build `MapContextPanel` with selected media/source/rights metadata.
8. Build `IIIFViewer` or image deep-zoom fallback for active manifests.
9. Build `/media/{id}` Media Viewer route.
10. Add metadata, rights, source record, linked place, linked collection, and commerce rail panels.
11. Link Place Page media cards into Media Viewer.
12. Link Map Viewer markers into Media Viewer.

Exit criteria:

- Map Viewer opens Yellowstone, fits to boundary/bounds, and shows seeded media.
- Historic map asset can be inspected.
- Media Viewer renders at least one manifest-backed item and one derivative fallback item.
- Media Viewer commerce rail appears only for activated items.

## Week 4

Goal: Collection Page, polish, and reviewer-ready prototype.

Exact order:

1. Complete collection seed membership ordering and cover asset.
2. Implement collection detail API and ordered media API.
3. Build `/collections/yellowstone-icons-american-west` route.
4. Build collection hero, narrative, ordered media grid, source summary, rights summary.
5. Wire Collection commerce rail.
6. Add links: Homepage -> Collection, Place -> Collection, Media -> Collection.
7. Add links: Collection media grid -> Media Viewer.
8. Add loading/error/empty states for all prototype routes.
9. Run responsive pass for desktop, tablet, mobile.
10. Run accessibility pass for keyboard navigation, alt text, map fallback, viewer controls.
11. Run API smoke tests and frontend route smoke tests.
12. Execute reviewer script: Homepage, Yellowstone Place, Map Viewer, Media Viewer, Collection, Commerce Rail.
13. Freeze prototype fixture IDs and document known limitations.

Exit criteria:

- Reviewer can complete the full Yellowstone path without dead links.
- All visible media and commerce cards show rights/provenance.
- Map and Media Viewer work on desktop and mobile.
- No page depends on Neo4j, pgvector, foundation models, checkout, or architecture redesign.

## Risks

| Risk | Severity | Mitigation |
|---|---|---|
| M36 schema not implemented when prototype starts | High | Use fixture-compatible views or run M36 first; do not redesign downstream pages. |
| Rights-cleared media source URLs are unstable | High | Store source records and fixture derivatives; preserve source URL in provenance. |
| IIIF manifest unavailable for a candidate asset | Medium | Use `asset_delivery_manifest` fallback with derivative display URL. |
| PostGIS boundary too complex for prototype map | Medium | Seed simplified boundary plus canonical centroid. |
| Commerce rail drifts into checkout scope | Medium | Keep product cards prototype-only; no cart/checkout in v1. |
| UI hardcodes content and bypasses API | High | Week 2 exit criteria require API-backed cards. |
| Collection narrative outruns seeded evidence | Medium | Keep narrative constrained to BHL/Smithsonian/LOC seeded records. |

## Final Build Rule

The prototype proves the existing architecture by making Yellowstone real:

- one canonical place
- one PostGIS map context
- one M36-backed media set
- one governed collection
- one reusable media viewer
- one commerce rail

Anything outside that path is deferred.
