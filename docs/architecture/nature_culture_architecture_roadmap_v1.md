# Nature & Culture Architecture Roadmap v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Horizon | 10-year architecture |
| Status | Architecture review |

## Mission

Review the current Nature & Culture architecture across Commerce, Routing, Catalog, Publication,
and Asset Intelligence, then determine what is still missing to support:

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

Evaluated institutions and standards anchors:

- MIT
- CERN
- NASA
- NIST
- W3C
- Internet Archive
- Library of Congress
- Smithsonian

No implementation is authorized by this document.

## Executive Finding

Nature & Culture has a strong governed commerce spine, but it is still a visual-asset platform, not
a general media repository.

The complete layers are the decision and governance layers:

- Commerce Intelligence
- Product Routing
- Catalog planning
- Publication planning
- Asset Intelligence registries
- Rights-first commercial gates
- Replayable scoring and audit doctrine

The missing layers are the durable media and source layers:

- General source item model
- General media file model
- Derivative and preservation model
- Time-based media model
- 3D model
- Dataset model
- Aggregator/source-of-record reconciliation
- Long-term repository and citation model

The next major architecture frontier is not another scoring layer. It is the **Universal Public
Domain Media Substrate**: a governed source-record, media-file, derivative, rights, preservation,
and citation architecture capable of feeding the existing commerce spine without weakening it.

## Institutional Architecture Lessons

| Institution | 10-year architecture lesson | Applies most to | Use in roadmap |
|---|---|---|---|
| MIT | Institutional repository discipline: durable collections, DSpace lineage, scholarly object deposits, preservation-oriented access. | Books, eBooks, datasets, repository governance. | Guide repository object lifecycle and deposit/citation models. |
| CERN | Open science at scale: large datasets, file indexes, software/data documentation, reproducibility, persistent research access. | Datasets, scientific media, high-volume files. | Guide dataset packages, file manifests, reproducibility metadata, and long-lived data access. |
| NASA | Public multimedia plus scientific data: image/video/audio/3D resources, open APIs, mission metadata, public-domain federal media with caveats. | Images, film, audio, 3D, datasets. | Guide multi-format media discovery and mission/source metadata, but keep rights validation explicit. |
| NIST | Standards, FAIR data, trusted repository posture, public data repository metadata, measurement-quality governance. | Datasets, validation, security, provenance, quality. | Guide dataset metadata, repository trust, versioning, validation, and audit requirements. |
| W3C | Web interoperability: HTML, CSS, SVG, accessibility, RDF/JSON-LD, PROV, DCAT, web media, linked data. | All public APIs and web-native metadata. | Freeze as the default external standards authority for web, provenance, dataset, and accessibility layers. |
| Internet Archive | Broad item/file repository: flexible item metadata, file manifests, derivatives, books/audio/video/web captures. | eBooks, audiobooks, audio, film, arbitrary files. | Use as a future generalized media-file pattern after stronger rights and file governance exists. |
| Library of Congress | Cultural source authority: bibliographic records, linked data, image services, maps, photos, posters, books. | Images, maps, photography, posters, books. | Use as first non-BHL source bridge and authority metadata model. |
| Smithsonian | CC0 open access and 3D leadership: object metadata, images, datasets, 3D Voyager/Open Access assets. | Images, photography, 3D, datasets. | Use as first 3D pilot anchor and high-confidence CC0 2D source. |

## Current Layer Assessment

| Layer | Current state | Complete for current scope? | Complete for 10-year media scope? | Decision |
|---|---|---:|---:|---|
| Rights gate | Public Domain/CC0 floor is constitutional and non-overridable. | Yes | Partially | Freeze the floor; extend rights granularity to files, derivatives, datasets, and time-based media. |
| Commerce Intelligence | Scoring, replay, audit, stale handling, policy versioning, and approval doctrine are defined. | Yes | Partially | Freeze formulas and governance spine; add media-neutral input adapter layer later. |
| Product Routing | Governed product recommendation layer exists for visual products. | Yes | Partially | Freeze visual product routing; defer audio/film/3D/dataset products. |
| Catalog | Internal catalog candidate/variant planning is defined. | Yes | Partially | Freeze internal catalog planning; extend later for digital downloads and media packages. |
| Publication | Internal publication candidates and channel profiles are defined. | Yes | Partially | Freeze current publication planning; defer execution and non-visual publication surfaces. |
| Asset Intelligence | Anchor types, creator authority/prestige, place signals, and registry governance are defined. | Yes | Partially | Freeze registry governance; extend asset classes and media-specific signal registries. |
| Source ingestion | BHL works; LOC is partial proof/candidate support. | No | No | Missing frontier layer. |
| Source-of-record model | Source semantics are still tied to BHL/LOC paths and `illustration_opportunities`. | No | No | Build after current architecture is frozen. |
| Media file model | MinIO preserves evidence, but there is no generic file/derivative graph. | No | No | Missing. Required before Internet Archive, audio, film, 3D, and datasets. |
| Preservation model | Checksums exist in narrow paths; long-term preservation policy is not generalized. | Partial | No | Missing. Use MIT/CERN/NIST guidance. |
| Dataset model | Dataset support is evidence/enrichment only, not first-class. | No | No | Missing. Use NIST/CERN/W3C DCAT-style architecture. |
| Time-based media model | No first-class duration, clip, transcript, caption, audio/video derivative, or stream policy layer. | No | No | Defer. |
| 3D model | No first-class geometry/material/texture/file validation or 3D viewer/export governance. | No | No | Defer except Smithsonian pilot architecture. |
| Aggregator model | No Europeana/Internet Archive-style aggregator/source reconciliation model. | No | No | Missing. |

## Media Class Roadmap

| Media class | Current support | Missing architecture | 10-year target | Primary guides |
|---|---|---|---|---|
| Images | Strong for BHL illustrations; partial for LOC. | General source item, asset class vocabulary, image derivative registry, IIIF-aware source bridge. | First-class governed still-image assets across BHL, LOC, Smithsonian, NASA, NARA. | LOC, Smithsonian, NASA, W3C, IIIF. |
| Maps | Architecturally supported by geographic anchor; runtime bridge missing. | LOC map bridge, cartography authority, map-specific dimensions/projection/scale fields. | First-class map assets with place, historical, creator, and product readiness signals. | LOC, NIST geospatial practice, W3C linked data. |
| Photography | Governance support exists; ingestion missing. | Photography candidate table, EXIF/technical metadata, creator authority, monochrome/color calibration. | First-class historical and scientific photography assets. | LOC, Smithsonian, NASA, NARA. |
| Posters | Governance support exists; ingestion missing. | Cultural-anchor poster source bridge, typography/layout quality signals, edition/series metadata. | First-class cultural poster assets for wall art and educational products. | LOC, Smithsonian, Internet Archive selectively. |
| Books | Books are provenance containers today. | Work/edition/item/page model, table of contents, OCR, rights by edition/file. | Books as both provenance and governed product packages. | BHL, LOC, MIT, Internet Archive. |
| eBooks | Not first-class. | Digital publication package model, EPUB/PDF policy, download rights, accessibility metadata. | Governed digital downloads and educational eBook products. | W3C, MIT, Internet Archive, LOC. |
| Audiobooks | Not supported. | Time-based audio model, narrator/edition rights, chapters, transcripts, delivery policy. | Deferred until media-file and time-based layers are mature. | Internet Archive, W3C media, NIST metadata discipline. |
| Audio | Not supported. | Audio file derivatives, duration, waveform, transcript, rights window, stream/download policy. | Research and heritage audio support after still-image/media-file substrate. | NASA, Internet Archive, W3C. |
| Film | Not supported. | Video derivatives, scenes/clips, captions, poster frames, rights windows, playback policy. | Select public-domain film support after audio architecture. | NASA, Internet Archive, LOC. |
| 3D | Not supported. | 3D file graph, geometry/material/texture model, unit/scale, viewer, derivative validation. | Smithsonian-led governed 3D pilot, then reusable 3D asset class. | Smithsonian, NASA, W3C/WebXR. |
| Datasets | Evidence/enrichment only. | Dataset package, schema, DOI/citation, version, license, checksum, reproducibility metadata. | First-class evidence datasets and later public dataset products. | NIST, CERN, NASA, MIT, W3C DCAT/PROV. |

## Complete Layers

These are complete enough for the current public-domain visual commerce scope and should not be
redesigned casually:

1. Commerce policy lifecycle, scoring, replay, and audit.
2. Product recommendation governance.
3. Internal catalog candidate and variant planning.
4. Internal publication candidate planning.
5. Public Domain/CC0 commercial rights floor.
6. Human approval boundaries for consequential actions.
7. Asset Intelligence registry governance for creators, prestige, anchors, and place signals.
8. PostgreSQL authority plus MinIO evidence split.
9. BHL illustration-as-provenance model.

These layers are not complete for broad media, but the core governance decisions are sound.

## Missing Layers

The missing architecture is concentrated upstream and around files:

1. `source_item`
   - Stable representation of an institution item, work, record, dataset, object, or package.

2. `source_record`
   - Versioned source metadata snapshots with source API, retrieval time, source hash, and source-of-record semantics.

3. `media_file`
   - File-level object for every original or fetched file, including MIME type, byte size, checksum, storage location, source URL, and rights assertion.

4. `media_derivative`
   - Derived images, thumbnails, crops, IIIF tiles, PDFs, EPUBs, audio encodes, video transcodes, 3D derivatives, and dataset extracts.

5. `media_rights`
   - Rights at source item, file, derivative, edition, clip, and dataset level.

6. `media_technical_metadata`
   - Image dimensions, EXIF, color profile, duration, codec, bitrate, transcript state, 3D geometry metadata, dataset schema.

7. `preservation_event`
   - Fixity checks, source retrieval, derivative generation, checksum changes, revalidation, tombstones.

8. `dataset_package`
   - Schema, version, DOI/citation, license, files, checksum, validation profile, reproducibility notes.

9. `aggregation_link`
   - Links Europeana/Internet Archive-style aggregator records to direct source records without treating aggregators as final authority.

10. `media_publication_profile`
   - Non-visual publication profiles for downloads, streams, datasets, 3D viewers, and educational packages.

## Layers To Freeze

Freeze means preserve the decision model and avoid redesign unless a contradiction appears in
production evidence.

| Layer | Freeze decision | Reason |
|---|---|---|
| Rights floor | Freeze. | Public Domain/CC0 is the correct commercial invariant. |
| PostgreSQL authority | Freeze. | Replay, audit, and governance require one state authority. |
| MinIO evidence store | Freeze. | Source files and derivatives need object storage separate from relational governance. |
| Commerce scoring governance | Freeze. | The policy/replay/audit model is media-neutral enough once adapters provide inputs. |
| Product routing governance | Freeze. | Recommendation governance should remain separate from product execution. |
| Catalog/publication internal planning | Freeze. | Internal planning avoids premature provider lock-in. |
| Human approval boundaries | Freeze. | Necessary for rights, product, and source uncertainty. |
| Asset Intelligence registry lifecycle | Freeze. | Versioned registries with second-human approval are the right model for 10-year trust. |
| Standards registry concept | Freeze. | W3C, NIST, IIIF, CIDOC, SKOS, PROV, DCAT-style references need an internal registry. |

## Layers To Defer

Defer means do not build until the Universal Public Domain Media Substrate exists.

| Layer | Defer decision | Reason |
|---|---|---|
| Audiobook products | Defer. | Requires time-based media, narrator/edition rights, chapters, and digital delivery policy. |
| Audio products | Defer. | Requires audio derivatives, transcripts, streaming/download rights, and QA. |
| Film products | Defer. | Requires video derivatives, captions, clip policy, rights windows, and playback surfaces. |
| 3D commerce | Defer except Smithsonian pilot architecture. | Requires new file graph, viewer, derivative validation, and product rules. |
| Dataset commerce | Defer. | Datasets should first be evidence/enrichment, not products. |
| Internet Archive broad ingestion | Defer. | Rights and metadata vary too much without file-level governance. |
| NASA broad multimedia ingestion | Defer. | Use selectively after media-file and rights granularity exist. |
| Provider execution for non-visual media | Defer. | Execution is downstream of stable catalog/publication profiles. |
| Licensed/non-public-domain media | Defer indefinitely. | It would change the platform doctrine. |

## 10-Year Architecture Frontier

The next major frontier is:

```text
Universal Public Domain Media Substrate
  -> source_item
  -> source_record
  -> media_file
  -> media_derivative
  -> media_rights
  -> preservation_event
  -> dataset_package
  -> media_publication_profile
  -> existing Commerce / Routing / Catalog / Publication spine
```

This frontier lets the platform expand without rewriting the commerce spine. The principle is:

> Source and media complexity is normalized upstream; commerce consumes stable, governed,
> rights-cleared inputs.

## Roadmap

### Phase 1: Freeze The Visual Commerce Spine

Horizon: now to 12 months.

Architecture outcomes:

- Freeze Commerce, Product Routing, Catalog, Publication, and Asset Intelligence governance.
- Freeze BHL as the canonical source-evidence precedent.
- Freeze Public Domain/CC0 as the commercial activation floor.
- Add only bridge architecture for LOC maps, photography, and posters.
- Do not add arbitrary media support.

Primary guides:

- LOC for source metadata and still visual source patterns.
- Smithsonian for CC0 object/image metadata.
- W3C for web metadata and provenance export.

### Phase 2: Build The Source And Media Substrate

Horizon: 12 to 30 months.

Architecture outcomes:

- Design `source_item`, `source_record`, `media_file`, `media_derivative`, and `media_rights`.
- Add preservation and fixity events.
- Add file-level rights and derivative-level rights.
- Add aggregator/source-of-record reconciliation.
- Define IIIF-compatible still-image and page-image profiles.

Primary guides:

- MIT for repository lifecycle.
- CERN for file manifests and reproducible data access.
- NIST for trusted data repository and FAIR metadata posture.
- W3C for PROV, JSON-LD, DCAT, accessibility, and web-native exchange.

### Phase 3: Expand Still Visual Sources

Horizon: 24 to 48 months.

Architecture outcomes:

- Onboard LOC, Smithsonian, NARA, NASA still images selectively.
- Support maps, photography, posters, scientific imagery, and cultural objects.
- Keep time-based and 3D media as non-scoreable discovery records unless pilot-approved.

Primary guides:

- LOC for maps/photos/posters.
- Smithsonian for CC0 museum objects.
- NASA for public federal scientific imagery.
- NARA for archival federal images and OCR.

### Phase 4: Add Book And Digital Publication Architecture

Horizon: 36 to 60 months.

Architecture outcomes:

- Add work/edition/item/page package architecture.
- Add OCR and accessibility metadata.
- Add PDF/EPUB/eBook publication profiles.
- Keep book products governed separately from image-derived products.

Primary guides:

- MIT and LOC for repository and bibliographic architecture.
- BHL for page/image/OCR provenance.
- Internet Archive for broad item/file patterns, with strict rights validation.
- W3C for accessibility and digital publishing standards.

### Phase 5: Add Dataset Architecture

Horizon: 48 to 72 months.

Architecture outcomes:

- Add dataset packages, schemas, versions, citations, checksums, licenses, and validation profiles.
- Treat datasets first as evidence and enrichment.
- Later allow public dataset products only after governance review.

Primary guides:

- NIST for public data repository and metadata rigor.
- CERN for large open-data file indexes and reproducibility.
- NASA for scientific data APIs.
- W3C for DCAT and PROV.

### Phase 6: Pilot 3D

Horizon: 60 to 84 months.

Architecture outcomes:

- Add 3D asset type, file graph, allowed formats, geometry/material/texture metadata, derivative policy, and viewer/export governance.
- Pilot only with Smithsonian or NASA-style high-authority public/open assets.
- Keep 3D commerce blocked until product and QA policies exist.

Primary guides:

- Smithsonian for open 3D.
- NASA for 3D/VR public media patterns.
- W3C/WebXR for web presentation.

### Phase 7: Add Time-Based Media

Horizon: 84 to 120 months.

Architecture outcomes:

- Add audio/film file derivatives, duration, codec, transcript, caption, clip, poster-frame, stream/download policy, and rights windows.
- Start with clearly public-domain, downloadable media.
- Do not support licensed broadcast archives without a separate constitutional amendment.

Primary guides:

- Internet Archive for broad public audio/video file patterns.
- NASA for public-domain multimedia.
- LOC and NARA for archival AV.
- W3C for media, captions, accessibility, and web playback.

## Strategic Non-Goals

- Do not turn Nature & Culture into a general archive mirror.
- Do not make Internet Archive or any aggregator the rights authority when a direct source exists.
- Do not weaken Public Domain/CC0 commercial gates for growth.
- Do not add licensed media architecture inside the public-domain platform doctrine.
- Do not create audio, film, 3D, or dataset products before file-level rights and derivative governance exist.
- Do not redesign Commerce Intelligence to solve upstream source complexity.

## Final Recommendation

Freeze the current commerce spine. It is the durable part of the platform.

Invest the next architecture cycle in the Universal Public Domain Media Substrate. This is the
missing 10-year foundation that lets Nature & Culture support images, maps, photography, posters,
books, eBooks, audiobooks, audio, film, 3D, and datasets without corrupting the existing governance
model.

Institutional priority for architecture guidance:

1. W3C: web, provenance, linked data, accessibility, dataset exchange.
2. NIST: trusted public data, validation, repository discipline.
3. LOC: cultural metadata, maps, photography, posters, authority data.
4. Smithsonian: CC0 open access and 3D.
5. MIT: repository lifecycle and institutional preservation.
6. CERN: large dataset packages and reproducibility.
7. NASA: public scientific multimedia and datasets.
8. Internet Archive: generalized file/item pattern after stronger internal governance exists.

## Source Notes

- W3C Web Standards: https://www.w3.org/standards/
- W3C Standards and Drafts: https://www.w3.org/TR/
- NIST Data: https://www.nist.gov/data
- NIST Public Data Repository: https://data.nist.gov/pdr/
- NIST OAR metadata model: https://data.nist.gov/od/dm/
- CERN Open Data Portal: https://openscience.web.cern.ch/open-data-portal
- ATLAS guide to CERN Open Data Portal: https://opendata.atlas.cern/docs/data/cern_opendata_portal
- NASA Open APIs: https://api.nasa.gov/
- NASA Image and Media Resources: https://www.nasa.gov/nasa-brand-center/images-and-media
- Library of Congress JSON/YAML APIs: https://www.loc.gov/apis/json-and-yaml/
- Smithsonian Open Access: https://www.si.edu/OpenAccess
- Internet Archive developer portal: https://archive.org/developers/
- Internet Archive Item Metadata API: https://doc-tools.readthedocs.io/en/ia-test-gsod/metadata.html
