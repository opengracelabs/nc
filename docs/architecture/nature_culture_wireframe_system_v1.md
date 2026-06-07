# Nature & Culture Wireframe System v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Status | Wireframe specification |
| Scope | Desktop, tablet, mobile |

## Mission

Define a world-class wireframe system for Nature & Culture across editorial, media, learning,
tourism, institution, and commerce surfaces.

Pages:

- Homepage
- Place Page
- Story Page
- Media Viewer
- Collection Page
- Tourism Page
- Education Page
- Commerce Page
- Institution Page
- Universal Media Viewer

The system must support:

- Maps
- Photography
- Botanical Art
- Fine Art
- Posters
- Books
- eBooks
- Audiobooks
- Audio
- Film
- 3D
- Datasets

Architecture dependencies:

- PostGIS for place geometry, spatial filters, bounding boxes, map overlays, tourism routes.
- Neo4j for related-content graph traversal.
- pgvector for semantic and visual similarity search.
- Universal Media Substrate for source items, delivery manifests, media files, rights, technical
  metadata, derivatives, and activation targets.

## Reference Model Lessons

| Reference | Adopted design lesson | Rejected pattern |
|---|---|---|
| Apple TV+ | Cinematic browsing, media-first rails, strong episode/media viewer affordances. | Do not hide provenance, rights, or source metadata behind entertainment-only chrome. |
| Google Arts & Culture | Immersive stories, deep zoom, collection browsing, artwork-first discovery. | Do not use platform-mediated source authority; always point back to NC source records. |
| National Geographic | Place-led stories, maps, photography, tourism/education framing. | Do not become a magazine landing page where commerce and provenance disappear. |
| Rijksmuseum | Open collection search, high-resolution image inspection, download/reuse clarity. | Do not assume every object is fine art; NC must support maps, books, AV, 3D, datasets. |
| Smithsonian | Cross-institution search, Open Access reuse, 2D/3D breadth. | Do not collapse all units/media into a flat search result without media-specific states. |
| Amazon | Product detail structure, buy box clarity, variants, reviews/Q&A-like confidence signals. | Do not let commerce override rights/provenance or editorial context. |

## System Principles

1. The first viewport should always reveal the actual subject: place, media, story, collection, or
   product.
2. Provenance and rights are first-class, visible, and never optional.
3. Media browsing is not one viewer. It is one universal shell with media-specific controls.
4. Place is the default organizing concept; institutions, media, and products remain connected to
   place context.
5. PostGIS owns spatial truth, Neo4j owns relationship exploration, pgvector owns similarity, and
   PostgreSQL/Universal Media Substrate own authority.
6. Commerce appears only where rights and activation permit it.
7. Desktop supports simultaneous context panels. Tablet uses stacked panels. Mobile uses progressive
   disclosure and bottom sheets.

## Global Shell

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Logo  Places  Stories  Collections  Media  Learn  Travel  Shop   Search  │
├────────────────────────────────────────────────────────────────────────────┤
│ Page content                                                               │
└────────────────────────────────────────────────────────────────────────────┘
```

Tablet:

```text
┌──────────────────────────────────────────────┐
│ Logo    Search                         Menu │
├──────────────────────────────────────────────┤
│ Page content                                 │
└──────────────────────────────────────────────┘
```

Mobile:

```text
┌──────────────────────────────┐
│ Logo        Search     Menu │
├──────────────────────────────┤
│ Page content                 │
├──────────────────────────────┤
│ Places Stories Media Shop    │
└──────────────────────────────┘
```

Global controls:

- Search button opens command palette.
- Media-type filters are icon-led: image, map, photo, art, poster, book, audio, film, 3D, data.
- Rights badge always appears on media/product-adjacent cards.
- Source badge links to institution/source item.
- Language selector preserves route.

## Shared Data Modules

### PostGIS Modules

- Place boundary map.
- Nearby protected/cultural/natural places.
- Tourism route geometry.
- Map overlay bounding boxes.
- Asset geocoverage and place relevance.

### Neo4j Modules

- Related places.
- Related media.
- Related creators.
- Related taxa/concepts.
- Related institutions.
- Story graph.

### pgvector Modules

- Similar images.
- Similar maps/posters by visual embedding.
- Similar stories by text embedding.
- Similar products by asset/product profile.
- Search ranking blend with keyword and locale.

### Universal Media Substrate Modules

- `source_item` identity.
- `asset_delivery_manifest`.
- `media_type_registry`.
- `media_rights`.
- `media_technical_metadata`.
- `media_derivative`.
- `activation_target`.

## 1. Homepage

Purpose:

- Establish Nature & Culture as a place-centered public-domain media and commerce platform.
- Route users into places, stories, media, learning, travel, and shop without a marketing-only page.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Global nav                                                                 │
├────────────────────────────────────────────────────────────────────────────┤
│ FULL-BLEED PLACE + MEDIA HERO                                              │
│ Yellowstone / Kyoto / Great Barrier Reef                                   │
│ [Explore Places] [Browse Media] [Shop Public-Domain Collections]           │
│                                                          media rights chip │
├──────────────────────────────┬─────────────────────────────────────────────┤
│ Featured Places              │ Live Media Rail                             │
│ [map tile] [place] [place]   │ image map photo poster book audio 3D data   │
├──────────────────────────────┴─────────────────────────────────────────────┤
│ Story band: map -> source -> media -> story -> product                     │
├────────────────────────────────────────────────────────────────────────────┤
│ Collections: Botanical Art | Historic Maps | Posters | Field Guides        │
├────────────────────────────────────────────────────────────────────────────┤
│ Trust band: PD/CC0 | IIIF | Source records | Preservation | Activation    │
└────────────────────────────────────────────────────────────────────────────┘
```

Tablet:

```text
┌──────────────────────────────────────────────┐
│ Nav                                          │
├──────────────────────────────────────────────┤
│ Hero media                                   │
│ Title + CTAs                                 │
├──────────────────────────────────────────────┤
│ Featured places carousel                     │
├──────────────────────────────────────────────┤
│ Media type rail                              │
├──────────────────────────────────────────────┤
│ Collections                                  │
└──────────────────────────────────────────────┘
```

Mobile:

```text
┌──────────────────────────────┐
│ Hero media                   │
│ Title                        │
│ [Places] [Media]             │
├──────────────────────────────┤
│ Swipe: Places                │
├──────────────────────────────┤
│ Swipe: Media types           │
├──────────────────────────────┤
│ Swipe: Collections           │
└──────────────────────────────┘
```

Primary components:

- `HomeHero`
- `MediaTypeRail`
- `FeaturedPlaceGrid`
- `StoryPreviewBand`
- `CollectionRail`
- `RightsTrustBand`

Data:

- PostgreSQL: featured places, collections, rights, source records.
- PostGIS: featured place geometry thumbnails.
- Neo4j: featured graph path.
- pgvector: recommended media.
- Universal Media Substrate: delivery manifest thumbnails.

## 2. Place Page

Purpose:

- Present one place as the anchor connecting geography, media, stories, tourism, education, and
  commerce.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Breadcrumbs                                                                │
├───────────────────────────────┬────────────────────────────────────────────┤
│ PLACE HERO                    │ PostGIS Map                                │
│ Title, designation, summary   │ boundary, routes, related media bounds     │
│ [View media] [Plan visit]     │                                            │
├───────────────────────────────┴────────────────────────────────────────────┤
│ Tabs: Overview | Media | Stories | Travel | Learn | Shop | Sources         │
├───────────────────────────────┬────────────────────────────────────────────┤
│ Featured media grid           │ Place facts / source / rights              │
│ map photo botanical poster    │ designation, coordinates, institutions     │
├───────────────────────────────┴────────────────────────────────────────────┤
│ Neo4j connections: creators, concepts, taxa, institutions, collections     │
└────────────────────────────────────────────────────────────────────────────┘
```

Tablet:

```text
┌──────────────────────────────────────────────┐
│ Place hero                                   │
├──────────────────────────────────────────────┤
│ Map panel                                    │
├──────────────────────────────────────────────┤
│ Sticky tabs                                  │
├──────────────────────────────────────────────┤
│ Media grid                                   │
├──────────────────────────────────────────────┤
│ Facts + graph                                │
└──────────────────────────────────────────────┘
```

Mobile:

```text
┌──────────────────────────────┐
│ Place title                  │
│ designation chips            │
├──────────────────────────────┤
│ Map preview                  │
├──────────────────────────────┤
│ Horizontal tabs              │
├──────────────────────────────┤
│ Media cards                  │
├──────────────────────────────┤
│ Facts bottom sheet           │
└──────────────────────────────┘
```

Must support:

- Maps as primary context and media.
- Photography and story galleries.
- Tourism route panels.
- Education activities by grade/subject.
- Commerce products only from approved activation targets.

## 3. Story Page

Purpose:

- National Geographic / Google Arts & Culture style narrative, grounded in source records and
  place graph.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Story masthead: title, dek, place, media type, reading/listening time      │
├────────────────────────────────────────────────────────────────────────────┤
│ Immersive lead media: photo/map/film/audio/3D                              │
├───────────────────────────────┬────────────────────────────────────────────┤
│ Article body                  │ Sticky context rail                        │
│ pull quotes, images, maps     │ source items, rights, graph, products      │
│ embedded viewer modules       │                                            │
├───────────────────────────────┴────────────────────────────────────────────┤
│ Related stories and collections                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

Tablet:

```text
┌──────────────────────────────────────────────┐
│ Masthead                                     │
│ Lead media                                   │
├──────────────────────────────────────────────┤
│ Story body                                   │
├──────────────────────────────────────────────┤
│ Context accordion                            │
└──────────────────────────────────────────────┘
```

Mobile:

```text
┌──────────────────────────────┐
│ Lead media                   │
│ Title                        │
├──────────────────────────────┤
│ Body                         │
├──────────────────────────────┤
│ Sources / related / shop     │
└──────────────────────────────┘
```

Story blocks:

- `TextBlock`
- `MapBlock`
- `MediaViewerBlock`
- `AudioBlock`
- `FilmBlock`
- `3DBlock`
- `DatasetBlock`
- `SourceCitationBlock`
- `ProductInlineBlock`

## 4. Media Viewer

Purpose:

- Detail page for a single activated media object, using the Universal Media Substrate as source.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Viewer toolbar: media type | zoom | compare | download | cite | share     │
├─────────────────────────────────────────────┬──────────────────────────────┤
│ Media stage                                 │ Metadata panel               │
│ IIIF image/map, audio, film, 3D, dataset    │ title, source, rights, tech   │
│                                             │ place, creator, graph, shop   │
├─────────────────────────────────────────────┴──────────────────────────────┤
│ Similar media via pgvector | Related graph via Neo4j                       │
└────────────────────────────────────────────────────────────────────────────┘
```

Tablet:

```text
┌──────────────────────────────────────────────┐
│ Toolbar                                      │
│ Media stage                                  │
├──────────────────────────────────────────────┤
│ Metadata tabs: About Source Rights Related   │
└──────────────────────────────────────────────┘
```

Mobile:

```text
┌──────────────────────────────┐
│ Toolbar icons                │
├──────────────────────────────┤
│ Media stage                  │
├──────────────────────────────┤
│ Bottom sheet: About/Rights   │
└──────────────────────────────┘
```

Media-specific controls:

- Image/photo/poster/botanical/fine art: zoom, pan, rotate, compare, download, details.
- Map: zoom, pan, opacity, georeference toggle, modern map overlay, measure, place pins.
- Book/eBook: page thumbnails, page turn, search text, TOC, download where permitted.
- Audiobook/audio: play, chapter/track list, transcript, waveform, speed.
- Film: play, captions, chapters, poster frame, transcript, scene clips.
- 3D: orbit, pan, zoom, lighting, material toggle, measurement, reset view.
- Dataset: schema, preview table, download, provenance, related media.

## 5. Collection Page

Purpose:

- Curated set of media, stories, places, and commerce products.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Collection hero: title, summary, cover media, rights scope                 │
├────────────────────────────────────────────────────────────────────────────┤
│ Tabs: Media | Map | Stories | Products | Sources                           │
├───────────────────────────────┬────────────────────────────────────────────┤
│ Filterable media grid         │ Collection map / graph summary             │
│ type, source, place, rights   │ PostGIS + Neo4j                            │
├───────────────────────────────┴────────────────────────────────────────────┤
│ Product rail if commerce-approved                                          │
└────────────────────────────────────────────────────────────────────────────┘
```

Tablet/mobile:

- Hero.
- Sticky type filters.
- Media grid.
- Map accordion.
- Products rail.
- Sources accordion.

Collection types:

- Place collection.
- Institution collection.
- Media-type collection.
- Story collection.
- Commerce collection.
- Education collection.

## 6. Tourism Page

Purpose:

- Place-first travel planning with public-domain context, not a booking funnel.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Destination hero: place photo/map, season, region                          │
├──────────────────────────────┬─────────────────────────────────────────────┤
│ PostGIS route map            │ Itinerary panel                             │
│ points, trails, overlays     │ day plan, media stops, field notes          │
├──────────────────────────────┴─────────────────────────────────────────────┤
│ Historic context: maps, photos, books, audio stories                       │
├────────────────────────────────────────────────────────────────────────────┤
│ Shop travel collection: maps, guides, posters                              │
└────────────────────────────────────────────────────────────────────────────┘
```

Mobile:

- Hero.
- Map.
- Itinerary cards.
- Media stops.
- Shop rail.

Data:

- PostGIS routes, points, boundaries.
- Neo4j related stories/media.
- pgvector similar places/itineraries.
- Universal Media Substrate for historic media.

## 7. Education Page

Purpose:

- Classroom-ready learning surfaces from public-domain media.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Learn hero: topic, grade, media type                                       │
├────────────────────────────────────────────────────────────────────────────┤
│ Filters: grade | subject | place | media type | duration                   │
├───────────────────────────────┬────────────────────────────────────────────┤
│ Lesson/activity cards         │ Featured media viewer                      │
├───────────────────────────────┴────────────────────────────────────────────┤
│ Teacher resources: datasets, maps, books, citations                        │
└────────────────────────────────────────────────────────────────────────────┘
```

Mobile:

- Topic hero.
- Filter chips.
- Activity cards.
- Media preview.
- Download/cite panel.

Education supports:

- Map literacy.
- Botanical illustration.
- Fine art analysis.
- Poster/media literacy.
- Public-domain books/eBooks.
- Audio/film analysis when phases activate.
- Dataset activities.

## 8. Commerce Page

Purpose:

- Amazon-like clarity with museum-grade provenance.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Product media gallery        │ Buy panel                                   │
│ image zoom / variants        │ title, price, variant, quantity, cart       │
├──────────────────────────────┴─────────────────────────────────────────────┤
│ Product tabs: Story | Source | Rights | Materials | Shipping               │
├──────────────────────────────┬─────────────────────────────────────────────┤
│ Related products             │ Source media / collection context           │
└──────────────────────────────┴─────────────────────────────────────────────┘
```

Tablet/mobile:

- Product gallery.
- Sticky buy bar.
- Variant selector.
- Source/rights accordion.
- Related products.

Commerce rules:

- Only approved activation targets.
- Rights visible near buy action.
- Shopify owns cart/checkout.
- NC owns source/provenance/rights context.
- Reviews may be replaced by "confidence signals": source authority, rights verified, print
  quality, collection fit.

## 9. Institution Page

Purpose:

- Present source institutions as trusted provenance partners and browsing anchors.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Institution hero: name, role, open access/rules, logo/image                │
├────────────────────────────────────────────────────────────────────────────┤
│ Stats: source items, media types, rights verified, collections             │
├───────────────────────────────┬────────────────────────────────────────────┤
│ Institution media grid        │ Source rules / standards / rights          │
├───────────────────────────────┴────────────────────────────────────────────┤
│ Related places, stories, collections, products                             │
└────────────────────────────────────────────────────────────────────────────┘
```

Mobile:

- Institution title.
- Trust/rules cards.
- Media-type filters.
- Media list.
- Source standards accordion.

Institution types:

- Source institution.
- Reference institution.
- Aggregator.
- Standards authority.

## 10. Universal Media Viewer

Purpose:

- One viewer shell that supports all media types through Universal Media Substrate manifests and
  media profiles.

Desktop:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Top toolbar: back | title | media type | rights | source | actions         │
├──────────────┬──────────────────────────────────────────────┬──────────────┤
│ Filmstrip    │ Universal stage                              │ Inspector    │
│ pages/tracks │ IIIF / map / book / audio / film / 3D / data │ About        │
│ variants     │                                              │ Source       │
│ related      │                                              │ Rights       │
│              │                                              │ Graph        │
├──────────────┴──────────────────────────────────────────────┴──────────────┤
│ Similar via pgvector | Related via Neo4j | Products if activated           │
└────────────────────────────────────────────────────────────────────────────┘
```

Tablet:

```text
┌──────────────────────────────────────────────┐
│ Toolbar                                      │
├──────────────────────────────────────────────┤
│ Universal stage                              │
├──────────────────────────────────────────────┤
│ Tabs: Filmstrip About Source Rights Related  │
└──────────────────────────────────────────────┘
```

Mobile:

```text
┌──────────────────────────────┐
│ Back Title Actions           │
├──────────────────────────────┤
│ Universal stage              │
├──────────────────────────────┤
│ Control strip                │
├──────────────────────────────┤
│ Bottom sheet inspector       │
└──────────────────────────────┘
```

Viewer engines:

| Media | Engine |
|---|---|
| Image, photography, poster, botanical art, fine art | IIIF Image viewer |
| Map | IIIF image + PostGIS overlay/map renderer |
| Book/eBook | IIIF multi-canvas/page reader or EPUB reader |
| Audiobook/audio | HTML audio player + transcript/waveform |
| Film | HTML video/HLS player + captions |
| 3D | model-viewer/WebGL shell |
| Dataset | Table/schema/download/visualization panel |

Required states:

- Loading.
- Rights blocked.
- Derivative unavailable.
- Manifest invalid.
- Source withdrawn.
- Media pending activation.
- Mobile low-bandwidth.
- Offline/cached citation.

## Search And Discovery

Desktop search:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Search input                                                               │
├──────────────┬──────────────────────────────────────────────┬──────────────┤
│ Filters      │ Results                                      │ Preview      │
│ media type   │ cards ranked by keyword + pgvector           │ selected     │
│ place map    │                                              │ media/source │
│ rights       │                                              │ graph        │
└──────────────┴──────────────────────────────────────────────┴──────────────┘
```

Search blend:

- PostgreSQL keyword and filters.
- PostGIS spatial constraints.
- Neo4j graph expansion.
- pgvector semantic/visual similarity.
- Universal Media Substrate rights/delivery readiness.

## Responsive Rules

Desktop:

- Three-panel layouts allowed: navigation/context, media/story, inspector.
- Use full-width bands for page sections.
- Keep commerce buy panel sticky but not intrusive.

Tablet:

- Two-column layouts collapse to stacked modules.
- Inspector becomes tabs/accordion.
- Map and media viewers keep stable aspect ratios.

Mobile:

- One primary task per viewport.
- Viewer controls become bottom strip.
- Metadata/provenance becomes bottom sheet.
- Filters become horizontal chips or modal drawers.
- Buy action becomes sticky bottom bar.

## API Surface

Representative endpoints:

- `GET /public/home`
- `GET /public/places/{id_or_slug}`
- `GET /public/places/{id}/media`
- `GET /public/stories/{id_or_slug}`
- `GET /public/collections/{id_or_slug}`
- `GET /public/institutions/{id_or_slug}`
- `GET /public/media/{source_item_id}`
- `GET /public/media/{source_item_id}/manifest`
- `GET /public/media/{source_item_id}/related`
- `GET /public/search`
- `GET /public/tourism/{place_id_or_slug}`
- `GET /public/education`
- `GET /commerce/products/{handle}`

Public responses must include:

- localized title/summary.
- rights status.
- source institution.
- delivery manifest status.
- media type.
- activation status.
- provenance.

## Source Notes

- Smithsonian Collections and Open Access support broad 2D/3D public media search and reuse.
- Google Arts & Culture demonstrates immersive stories, zoomable images, virtual collections, and
  partner-published cultural content.
- Rijksmuseum Collection Online demonstrates open high-resolution collection access, linked open
  data, and reuse-first collection browsing.
- National Geographic provides the model for place-led photography, maps, travel, and educational
  storytelling.
- Amazon provides the model for commerce clarity: image gallery, variant selection, buy action,
  reviews/confidence signals, and product Q&A-like information retrieval.
- Apple TV+ provides the model for cinematic media browsing and playback rails.
