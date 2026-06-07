# Future Media Architecture Audit v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Status | Architecture audit |

## Mission

Determine which public-domain and open cultural institutions should guide future support for:

- Images
- Maps
- Photography
- Posters
- Books
- eBooks
- Audiobooks
- Audio
- Film
- 3D
- Datasets

This audit evaluates:

- Library of Congress
- Internet Archive
- Europeana
- Smithsonian
- NARA
- BBC Archives
- Biodiversity Heritage Library
- British Library
- Google Arts & Culture

## Existing Architecture Baseline

The current implemented runtime is narrow by design:

- BHL illustrations are the only asset class with implemented ingestion-to-publication traversal.
- LOC map support exists as proof/candidate data, but does not yet bridge into the commerce runtime.
- Commerce currently hangs off `illustration_opportunities`.
- PostgreSQL is authoritative for rights, provenance, scores, governance events, and replay inputs.
- MinIO preserves evidence files and checksums.
- Product, catalog, and publication workers are internal planning and governance systems, not external provider execution.
- The ratified Asset Intelligence and Commerce Intelligence governance now support biological, geographic, and cultural anchors, including maps and photography once source bridges exist.

Implication: institutions align best when they provide stable object metadata, explicit rights, source URLs, high-quality visual media or IIIF-like delivery, and reusable authority/provenance structures. They force redesign when they require generalized time-based media, lending states, opaque partner rights, proprietary access, or broad arbitrary file manifests.

## Institution Architecture Matrix

Legend:

- Aligns: can enter the current or near-term architecture with source adapters and bridge migrations.
- Redesign pressure: requires new first-class media/object models beyond the current visual opportunity path.
- Metadata model: reusable descriptive, authority, provenance, or aggregation structure.
- Media model: reusable delivery, file, page, image, IIIF, AV, 3D, or dataset structure.

| Institution | Best-fit media classes | Architecture alignment | Redesign pressure | Reusable metadata model | Reusable media model | Recommendation |
|---|---|---|---|---|---|---|
| Biodiversity Heritage Library | Images, books, eBooks, datasets, OCR, page images | Very high. Already the implemented platform precedent for public-domain illustration discovery, page/image provenance, OCR, and taxon-linked source context. | Low for illustrations and page images. Medium if treating complete books as first-class products instead of provenance containers. | Strong. BHL API exposes title, item, page, part, OCR, name, and bibliographic metadata. BHL metadata is made available under CC0. | Strong for page images, thumbnails, OCR text, item/page structure. | Keep as the canonical model for source evidence, book/page provenance, OCR, and natural-history illustration ingestion. |
| Library of Congress | Images, maps, photography, posters, books, film/audio selectively, authority data | Very high for maps, photography, posters, and still images. Current architecture already recognizes `loc` as a source and has LOC map proof work. | Low to medium for still visual assets. High for audio, film, and generalized books unless first-class non-visual asset classes are added. | Very strong. LOC JSON/YAML API, MARC-derived records, linked data service, authorities, bibliographic metadata. | Strong for images where LOC image services/IIIF are available. Medium for AV and documents because media formats vary by collection. | First priority for non-BHL expansion: maps, historical photography, posters, and creator/place authority seeding. |
| Smithsonian | Images, photography, 3D, datasets, object records, some posters/artifacts | High for 2D open-access images and object metadata. Strong strategic fit for CC0 visual collections. | Medium. 3D requires new media derivatives, file-type validation, viewer/export policy, and product surfaces. | Strong. Smithsonian Open Access/API provides cross-museum object metadata and CC0 open access records. | Strong for 2D and uniquely strong for 3D because Smithsonian exposes open 3D content via 3D Voyager/Open Access. | Onboard after LOC still-image bridge. Treat 2D as current visual assets; treat 3D as a governed pilot, not a side effect of image ingestion. |
| NARA | Photography, images, posters, maps, film, audio, datasets, OCR, authority records | High for US federal public-domain archival records and still visual media. Good fit with rights-first governance. | Medium for archival hierarchy and extracted text. High for film/audio because duration, captions, derivatives, and preservation metadata need new runtime support. | Strong. Catalog API exposes archival descriptions, authority records, digital object metadata, OCR/extracted text, and public contributions. Metadata is generally public domain as US government work, with rare exceptions. | Medium to strong. Digital objects include images/videos and technical metadata, but media delivery is less reusable as a universal product model than IIIF. | Onboard after LOC/Smithsonian for public-domain photography, federal posters, maps, and later film/audio. Split still-image support from time-based media support. |
| Europeana | Images, maps, photography, posters, books, audio/video selectively, 3D selectively | Medium to high as a metadata aggregation and discovery layer. Lower as a canonical media source because rights and media authority remain provider-specific. | Medium. Requires multi-provider provenance, source-of-record resolution, rights normalization by provider, and dedupe across aggregators. | Very strong. Europeana Data Model is a mature reusable aggregation model; Record/Search APIs expose EDM records. | Strong for IIIF-enabled 2D records. Medium for audio/video/3D because coverage and provider implementations vary. | Use as a standards and aggregation guide. Onboard after direct-source adapters so Europeana records can point to source institutions rather than become the source of truth. |
| Internet Archive | Books, eBooks, audiobooks, audio, film, images, datasets, software/web captures | Medium as a broad public file repository and book/audio/video source. Weak as a rights-authoritative cultural institution because items vary by uploader, collection, and rights quality. | High. Requires arbitrary file manifests, lending/access states, multiple derivatives per item, stricter rights validation, and media-family-specific QA. | Medium. Item metadata API is useful but flexible and inconsistent; good for file manifests and collection discovery, not a disciplined heritage model. | Strong for file lists, derivatives, downloads, thumbnails, and broad media. Weak as a semantic media model. | Defer until a generalized `source_item` and `media_file` model exists. Use selectively for clearly public-domain books, public-domain film/audio, and preserved derivative access. |
| British Library | Books, maps, manuscripts, images, sound recordings, newspapers | Medium. Excellent institutional fit for books/maps/manuscripts, but rights and machine access are not as clean as BHL/LOC/Smithsonian. Recent service disruption also makes production dependency risk higher. | Medium to high. Complete books, legal deposit, sound, manuscripts, and access restrictions require richer rights/access modeling. | Strong. MARC/Z39.50 and collection metadata services are useful for bibliographic modeling. | Medium. IIIF guidance exists for British Library collections, but media availability varies and is not a uniform open media pipeline. | Use as a reference model for book/map metadata and IIIF practice. Defer production ingestion until source access and rights paths are explicit per collection. |
| BBC Archives | Audio, film, video, broadcast metadata | Low for public-domain commerce architecture. BBC archive content is not a public-domain corpus, public access is restricted, and APIs are not broadly open for this use case. | Very high. Broadcast archive support requires rights windows, territorial licensing, clip policy, time-based metadata, transcripts, captions, and non-commercial restrictions. | Medium as a conceptual broadcast metadata reference only; not as an ingestible public model. | Medium for internal broadcast/archive systems, low for open reusable media. | Do not onboard as a public-domain source. Treat as a future broadcast-archive reference only if the platform later supports licensed non-public-domain media. |
| Google Arts & Culture | Images, virtual exhibits, museum objects, some video/3D-like experiences | Low as a source institution. It is a platform/aggregator, not the rights authority, and does not provide a stable public ingestion API suitable for governed source-of-record use. | Very high if treated as source. Would require scraping/proprietary platform dependency, partner rights resolution, and source institution reconciliation. | Low for platform ingestion. Partner museum metadata may be useful only when traced back to the museum source. | Low for reusable media architecture because delivery is platform-mediated. | Do not onboard. Use only as a manual discovery surface that points curators back to source institutions with open APIs/rights. |

## Media Class Guidance

| Media class | Primary guiding institutions | Secondary/reference institutions | Architecture note |
|---|---|---|---|
| Images | BHL, LOC, Smithsonian, NARA | Europeana, British Library | Current architecture can support still images after source bridges and asset-type vocabulary expansion. |
| Maps | LOC | British Library, NARA, Europeana, Internet Archive | LOC should define the first map bridge because it already appears in the repo and has strong image/metadata support. |
| Photography | LOC, NARA, Smithsonian | Europeana, British Library | Requires photography ingestion worker, creator prestige seeding, and `anchor_type` confirmation. |
| Posters | LOC, NARA, Smithsonian | Europeana, Internet Archive | Fits cultural anchor support. Rights and creator attribution quality determine scoreability. |
| Books | BHL, LOC, British Library | Internet Archive, Europeana | Current doctrine treats books as provenance containers. First-class book products require governance and runtime extension. |
| eBooks | BHL, Internet Archive, LOC | British Library, Europeana | Needs a digital publication/download model distinct from visual print products. |
| Audiobooks | Internet Archive | BBC as reference only | Not supported by current runtime. Requires time-based media, rights, transcript, and distribution policy. |
| Audio | Internet Archive, NARA | British Library, BBC as reference only | Not supported by current runtime. Start only after media-file and rights-window models exist. |
| Film | NARA, Internet Archive, LOC | BBC as reference only | Not supported by current runtime. Needs duration, derivatives, captions, scenes/clips, and streaming/download policy. |
| 3D | Smithsonian | Europeana | Requires a new governed 3D media model, derivative policy, file validation, viewer, and product surface rules. |
| Datasets | Smithsonian, NARA, BHL, LOC | Europeana, Internet Archive | Should enter as source evidence and enrichment data before becoming public dataset products. |

## Answers To Audit Questions

### 1. Institutions that align with the existing architecture

Primary alignment:

- BHL: strongest existing fit and implemented precedent.
- LOC: strongest next fit for maps, photography, posters, still images, and authority metadata.
- Smithsonian: strong fit for CC0 2D images and metadata; strategic 3D pilot.
- NARA: strong fit for public-domain US archival still images, metadata, OCR, and authority records.

Conditional alignment:

- Europeana: aligns as aggregation metadata and standards guidance, but not as the canonical source of media truth.
- British Library: aligns as metadata/IIIF reference and selective source once collection-specific rights/access are proven.

### 2. Institutions that would force redesign

Highest redesign pressure:

- BBC Archives: licensed/restricted broadcast archive, not public-domain source.
- Google Arts & Culture: platform-mediated aggregator without stable open source-of-record API for governed ingestion.
- Internet Archive: broad file repository with inconsistent metadata and rights, useful only after generalized media file modeling.

Targeted redesign pressure:

- Smithsonian 3D: requires first-class 3D support.
- NARA film/audio: requires time-based media support.
- British Library books/sound/legal-deposit material: requires richer access and rights modeling.
- Europeana as source-of-record: requires aggregator provenance and provider reconciliation.

### 3. Institutions with reusable metadata models

Strong reusable metadata models:

- Europeana: EDM for aggregation, provider/resource separation, rights/provider context.
- LOC: MARC-derived JSON/YAML, linked data, authority and bibliographic metadata.
- BHL: item/page/title/name/OCR bibliographic model for natural-history literature.
- NARA: archival description, authority records, digital object metadata, extracted text.
- British Library: MARC/Z39.50 and bibliographic metadata services.
- Smithsonian: object metadata across museum/research collections and open access records.

Medium reusable metadata models:

- Internet Archive: useful item metadata and file manifest, but flexible and inconsistent.
- BBC Archives: useful conceptual broadcast metadata reference, not a public-domain ingestion model.

Weak reusable metadata model for this architecture:

- Google Arts & Culture: partner/platform presentation metadata should not become source-of-record.

### 4. Institutions with reusable media models

Strong reusable media models:

- BHL: page image, thumbnail, OCR, item/page structure.
- LOC: image services and IIIF-compatible image delivery where available.
- Smithsonian: 2D open access media plus 3D model access.
- Internet Archive: item file manifests and derivatives, useful after generalized media modeling.

Medium reusable media models:

- Europeana: IIIF where provider records support it; media varies by contributing institution.
- NARA: digital object media and technical metadata, strong for archival files but not a universal product model.
- British Library: IIIF practice and collection media where available, but uneven access/rights for ingestion.

Low reusable media models for current architecture:

- BBC Archives: restricted broadcast media access.
- Google Arts & Culture: platform-mediated media access.

## Priority Onboarding Order

1. BHL reinforcement.
   - Keep BHL as the canonical model for evidence, page images, OCR, public-domain/CC0 rights verification, and book-as-provenance design.

2. LOC still visual bridge.
   - Implement LOC map, photography, and poster bridge into `illustration_opportunities` or a generalized commerce input table.
   - Seed cartography and photography creator authority/prestige registries.
   - Make LOC the first guide for maps and historical photography.

3. Smithsonian Open Access 2D.
   - Add Smithsonian as a CC0 object/image source after LOC bridge patterns are stable.
   - Treat 3D records as discoverable but not scoreable until 3D governance exists.

4. NARA still visual and OCR.
   - Onboard federal public-domain photographs, posters, maps, OCR, and archival metadata.
   - Keep film/audio out of the first NARA phase.

5. Europeana metadata aggregation.
   - Use EDM to guide aggregator modeling, rights/provider separation, dedupe, and source reconciliation.
   - Do not make Europeana the canonical media source when direct source institution records exist.

6. British Library selective metadata/IIIF pilots.
   - Use as book/map/manuscript metadata reference.
   - Pilot only collection-specific open media with explicit rights and stable access.

7. Internet Archive generalized media pilot.
   - Add only after a `source_item` plus `media_file`/`media_derivative` model exists.
   - Start with clearly public-domain books, public-domain film, or audio collections with explicit rights.

8. Smithsonian 3D governed pilot.
   - Run separately from 2D ingestion.
   - Requires 3D asset type, allowed file formats, checksum policy, derivative policy, viewer/export policy, and product eligibility rules.

9. BBC Archives and Google Arts & Culture excluded from source onboarding.
   - BBC is a broadcast-rights reference, not a public-domain source.
   - Google Arts & Culture is a discovery surface, not a governed source institution.

## Required Architecture Work Before Broad Future Media

Minimum migrations/design changes:

- Generalize upstream commerce input beyond `illustration_opportunities` or formally bridge every future source into that table with clear semantics.
- Add first-class asset class vocabulary for `illustration`, `map`, `photograph`, `poster`, `book`, `ebook`, `audio`, `audiobook`, `film`, `3d`, and `dataset`.
- Add `source_item`, `source_record`, `media_file`, and `media_derivative` concepts if Internet Archive, audio, film, 3D, or datasets become first-class.
- Preserve rights at both source-record and file/derivative level.
- Add time-based media metadata: duration, transcript, caption, clip range, derivative format, streaming/download permission.
- Add 3D metadata: file format, geometry/material/texture files, units/scale, viewer compatibility, derivative set, inspection status.
- Add dataset metadata: schema, license, version, checksum, provenance, refresh policy, and whether the dataset is evidence, enrichment, or product.
- Add aggregator provenance for Europeana-style records: aggregator record ID, provider record ID, source institution, rights source, media source, and dedupe key.

## Source Notes

- Library of Congress API documentation: https://www.loc.gov/apis/json-and-yaml/
- Library of Congress image services: https://www.loc.gov/apis/micro-services/image-services/
- Library of Congress linked data service: https://www.loc.gov/apis/additional-apis/linked-data-service/
- BHL API documentation: https://www.biodiversitylibrary.org/docs/api3.html
- BHL developer/data tools and CC0 metadata note: https://about.biodiversitylibrary.org/tools-and-services/developer-and-data-tools/
- Smithsonian Open Access: https://www.si.edu/OpenAccess
- NARA Catalog API: https://www.archives.gov/research/catalog/help/api
- NARA Catalog API documentation: https://usnationalarchives.github.io/Catalog-API/
- Europeana APIs: https://www.europeana.eu/en/apis
- Europeana Data Model documentation: https://pro.europeana.eu/page/edm-documentation
- British Library collection metadata services: https://www.bl.uk/services/collection-metadata-services
- British Library collections overview: https://www.bl.uk/collection
- British Library IIIF guide by the IIIF Consortium: https://iiif.io/guides/guides/bl.uk/
- Internet Archive developer portal: https://archive.org/developers/
- Google Arts & Culture overview: https://about.artsandculture.google.com/
- BBC Information Syndication API overview: https://information-syndication.api.bbc.com/
