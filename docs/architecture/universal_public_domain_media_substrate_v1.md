# Universal Public Domain Media Substrate v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Date | 2026-06-07 |
| Role | Lead Platform Engineer |
| Status | Architecture design |
| Scope | No implementation |

## Mission

Design the Universal Public Domain Media Substrate so Nature & Culture can support:

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

The substrate must avoid future platform redesign by keeping media and source complexity upstream
of the existing Commerce, Product Routing, Catalog, Publication, and Asset Intelligence spine.

## Design Thesis

Nature & Culture should not become one table per media type and one worker per institution. That
would force redesign every time a new source or format appears.

The stable architecture is:

```text
Institution / Aggregator / Repository
  -> source_item
  -> source_record
  -> media_file
  -> media_derivative
  -> media_rights
  -> preservation_event
  -> media_profile
  -> activation_target
  -> existing Commerce / Routing / Catalog / Publication spine
```

The core substrate stores what is universal:

- Where did this come from?
- What source record was observed?
- What files exist?
- What derivatives exist?
- What rights apply?
- What technical metadata is known?
- What preservation events occurred?
- What media-specific profile qualifies it for downstream use?

Commerce should never need to know whether an asset came from LOC IIIF, Smithsonian 3D, Internet
Archive files, NASA media, NIST datasets, or BHL pages. Commerce receives a governed,
rights-cleared activation target with stable inputs.

## Non-Negotiable Invariants

1. PostgreSQL remains authoritative for state, governance, rights, provenance, replay inputs, and
   activation decisions.
2. Object storage remains authoritative for preserved files and derivatives.
3. Public Domain or CC0 remains the commercial activation floor.
4. Rights are stored at multiple levels: source item, source record, file, derivative, edition,
   clip, model, and dataset package.
5. Source records are snapshots, not live assumptions.
6. Aggregators are not rights authorities unless they are also the source institution.
7. Every downstream activation must be traceable to a source record, file checksum, rights record,
   media profile, policy version, and human decision when required.
8. New media families extend the substrate through profiles, not by redesigning core tables.
9. Time-based media, 3D, and datasets remain non-commerce-capable until their profiles and QA gates
   are ratified.
10. Existing Commerce, Routing, Catalog, Publication, and Asset Intelligence models are consumers,
    not the place to solve source/media complexity.

## Core Entity Model

### 1. `source_institution`

Represents the institution, repository, archive, aggregator, or platform from which records are
observed.

Examples:

- `bhl`
- `loc`
- `smithsonian`
- `nara`
- `nasa`
- `internet_archive`
- `europeana`
- `nist_pdr`
- `cern_open_data`
- `mit_dspace`

Required concepts:

- institution key
- display name
- institution type: `source`, `aggregator`, `repository`, `standards_authority`
- source-of-record eligibility
- default rights reliability
- API/access profile
- standards supported: IIIF, JSON-LD, MARC, DCAT, PROV, OAI-PMH, file manifest, custom API

### 2. `source_item`

Stable representation of a source-side object, work, record, item, dataset, book, map, media item,
or 3D object.

Examples:

- BHL item
- LOC object/resource
- Smithsonian object
- Internet Archive item
- NASA media asset
- NIST dataset landing page
- CERN dataset record

Key fields:

- source institution
- source item identifier
- canonical source URL
- item family: `visual`, `book`, `av`, `3d`, `dataset`, `mixed`
- source-of-record flag
- title
- creators/contributors
- dates
- collection/context
- source item metadata hash
- current source state: `observed`, `active`, `withdrawn`, `unavailable`, `superseded`

Design rule:

`source_item` is not a commercial asset. It is the source-side thing from which media and metadata
are derived.

### 3. `source_record`

Versioned snapshot of metadata observed from a source API, page, manifest, catalog record, or
aggregator record.

Key fields:

- source item
- retrieval method
- retrieval URL
- retrieved at
- raw metadata JSON/XML/text
- normalized metadata JSON
- metadata hash
- source API version
- source rights statement observed
- source license URL observed
- source record status

Design rule:

If a source changes metadata tomorrow, historical scoring and publication are still replayable
against the pinned `source_record`.

### 4. `source_relationship`

Links source records to each other without merging their authority.

Examples:

- Europeana record points to provider record.
- Internet Archive item mirrors a BHL book.
- LOC linked data authority identifies a creator.
- NASA image belongs to a mission/dataset.

Relationship types:

- `aggregates`
- `mirrors`
- `same_as`
- `derived_from`
- `authority_match`
- `collection_member`
- `manifest_member`
- `page_member`
- `file_member`

Design rule:

Do not collapse aggregator and source authority into one record. Preserve the relationship.

### 5. `media_file`

A preserved original or source-retrieved file.

Examples:

- TIFF
- JPEG
- JP2
- PDF
- EPUB
- MP3
- WAV
- MP4
- WebM
- GLB
- OBJ
- CSV
- Parquet
- ZIP

Key fields:

- source item
- source record
- source URL
- storage URI
- filename
- MIME type
- media family
- byte size
- checksum algorithm
- checksum
- file role: `original`, `source_derivative`, `access_file`, `metadata_file`, `ocr_file`,
  `caption_file`, `texture_file`, `dataset_file`, `archive_file`
- retrieval status
- preservation status

Design rule:

Every durable file has a checksum. No checksum, no downstream activation.

### 6. `media_derivative`

A file generated by Nature & Culture or accepted as a source derivative for a defined purpose.

Examples:

- display image
- print image
- thumbnail
- IIIF tile set
- cropped map detail
- OCR text
- EPUB package
- audio transcode
- video transcode
- poster frame
- caption file
- 3D preview model
- dataset extract

Key fields:

- parent media file
- derivative type
- derivative policy version
- storage URI
- checksum
- dimensions/duration/size
- generation worker version
- generated at
- quality status
- rights inherited flag
- derivative rights record

Design rule:

Derivatives are not informal helper files. They are governed media records.

### 7. `media_rights`

Rights evidence and activation gate at any relevant granularity.

Applies to:

- source item
- source record
- media file
- media derivative
- book edition
- clip
- 3D package
- dataset package

Key fields:

- subject type
- subject ID
- rights status: `Public Domain`, `CC0`, `Open Licensed`, `Restricted`, `Unknown`,
  `Mixed`, `Blocked`
- commercial reuse permitted
- modification permitted
- attribution required
- source rights statement
- source rights URL
- jurisdiction note
- evidence URL
- reviewed by
- reviewed at
- status: `proposed`, `active`, `superseded`, `blocked`

Design rule:

Only `Public Domain` and `CC0` can activate commerce. Other statuses may support research,
discovery, or internal evidence only.

### 8. `media_technical_metadata`

Normalized technical facts extracted from files and source records.

Common fields:

- file format
- MIME type
- byte size
- checksum
- dimensions
- color profile
- creation/capture date if present
- software/tool metadata if present
- extraction worker version

Family-specific fields are stored through profile records, not by expanding this table forever.

### 9. `preservation_event`

Append-only event log for the lifecycle of files, derivatives, fixity, and source observations.

Event types:

- `source_record_observed`
- `file_retrieved`
- `checksum_computed`
- `fixity_verified`
- `fixity_failed`
- `derivative_generated`
- `rights_reviewed`
- `technical_metadata_extracted`
- `source_unavailable`
- `source_changed`
- `file_quarantined`
- `media_activated`
- `media_deactivated`

Design rule:

Preservation is not background plumbing. It is part of the trust contract.

### 10. `activation_target`

The media-neutral bridge into the existing platform.

An activation target says: this source/media object is now eligible to behave as a downstream
platform object.

Activation target types:

- `illustration_opportunity`
- `commerce_asset`
- `collection_asset`
- `book_package`
- `digital_download`
- `dataset_evidence`
- `media_exhibit`
- `research_only`

Key fields:

- source item
- source record
- primary media file
- primary derivative
- rights record
- media profile
- activation policy
- activation status
- approved by
- approved at
- downstream object references

Design rule:

This is how the substrate avoids redesigning Commerce. Commerce consumes activation targets, not
raw source records.

## Extension Profiles

The core substrate stays stable. Media families add profile tables or profile JSON schemas.

### Still Visual Profile

Applies to:

- Images
- Photography
- Posters
- Most map renderings

Fields:

- width
- height
- aspect ratio
- color profile
- resolution tier
- source image service
- IIIF info URL if available
- print eligibility
- crop safety
- visual quality score
- OCR/caption availability if present

Feeds:

- Asset Intelligence
- Commerce Intelligence
- Product Routing
- Catalog
- Publication

### Map Profile

Applies to:

- Historic maps
- Scientific maps
- Atlas plates
- Cartographic images

Additional fields:

- map type
- geographic coverage
- scale
- projection
- coordinate reference if known
- bounding box if known
- cartographer/survey authority
- place anchors
- inset/detail regions
- georeference status

Feeds:

- Asset Intelligence geographic anchor
- Commerce score substitutions for geographic assets
- Map-specific product surfaces

### Book Profile

Applies to:

- Books
- Volumes
- Monographs
- Field guides
- Source books used as provenance

Fields:

- work identifier
- edition identifier
- volume
- publication date
- publisher
- authors/contributors
- page count
- table of contents
- OCR availability
- page image coverage
- illustration page links
- rights by edition

Feeds:

- Source provenance
- Illustration discovery
- Future book packages

### eBook Profile

Applies to:

- EPUB
- PDF digital editions
- accessible digital downloads

Fields:

- package format
- reading order
- accessibility metadata
- embedded media inventory
- text/OCR confidence
- downloadable file rights
- digital publication channel eligibility

Feeds:

- Future digital download profiles
- Publication layer extension

### Time-Based Media Profile

Applies to:

- Audiobooks
- Audio
- Film
- Video clips

Fields:

- duration
- media type
- codec
- bitrate
- frame rate for video
- channels/sample rate for audio
- chapters
- transcript
- captions/subtitles
- language
- clip ranges
- poster frame
- stream/download rights
- takedown sensitivity

Feeds:

- Research/discovery first
- Future publication profiles after governance ratification

### 3D Profile

Applies to:

- GLB
- glTF
- OBJ
- STL
- USD/USDZ
- Source 3D packages

Fields:

- primary model file
- geometry files
- material files
- texture files
- units
- scale
- polygon/vertex counts
- bounding dimensions
- viewer compatibility
- printable/exportable flag
- derivative model versions
- inspection status

Feeds:

- 3D viewer surfaces
- Future 3D product eligibility only after policy ratification

### Dataset Profile

Applies to:

- CSV
- JSON
- Parquet
- ZIP dataset packages
- Scientific data packages
- Repository datasets

Fields:

- dataset identifier
- DOI or persistent identifier
- schema
- data files
- metadata files
- license
- version
- release date
- citation
- validation profile
- reproducibility notes
- related publication
- related code/software
- refresh policy

Feeds:

- Evidence/enrichment first
- Public dataset products only after governance ratification

## Media Family Support Matrix

| Media family | Core substrate support | Required profile | Downstream status |
|---|---|---|---|
| Images | `source_item`, `source_record`, `media_file`, `media_derivative`, `media_rights` | Still Visual Profile | Commerce-capable after rights and quality gates. |
| Maps | Core substrate plus source relationships and place anchors | Map Profile plus Still Visual Profile | Commerce-capable after geographic anchor validation. |
| Photography | Core substrate plus creator authority | Still Visual Profile | Commerce-capable after photography governance seeding. |
| Posters | Core substrate plus cultural anchor | Still Visual Profile | Commerce-capable after cultural anchor validation. |
| Books | Core substrate plus page/file relationships | Book Profile | Provenance-capable first; product-capable after book policy. |
| eBooks | Core substrate plus package derivatives | eBook Profile | Deferred until digital publication governance. |
| Audiobooks | Core substrate plus duration/chapter/transcript metadata | Time-Based Media Profile | Deferred. |
| Audio | Core substrate plus audio derivatives | Time-Based Media Profile | Deferred. |
| Film | Core substrate plus video derivatives, captions, clips | Time-Based Media Profile | Deferred. |
| 3D | Core substrate plus model package graph | 3D Profile | Deferred except governed Smithsonian/NASA pilot. |
| Datasets | Core substrate plus package/schema/citation | Dataset Profile | Evidence-capable first; product-capable later. |

## Integration With Existing Platform

### Asset Intelligence

Asset Intelligence consumes profile outputs:

- anchor type
- creator authority
- creator prestige
- place relevance
- media quality
- source trust
- rights certainty

It does not fetch source files or parse arbitrary media.

### Commerce Intelligence

Commerce consumes only activation targets that have:

- active Public Domain or CC0 rights
- required media profile
- primary derivative suitable for the product family
- replayable source record
- checksum-backed file evidence
- policy version

Commerce formulas do not change for each source. If a media family needs special scoring, the
scoring policy receives normalized input signals from the media profile.

### Product Routing

Product Routing consumes product-eligible activation targets. It does not inspect raw files except
through normalized fields:

- image width
- print eligibility
- format eligibility
- digital download eligibility
- 3D export eligibility
- dataset package eligibility

### Catalog

Catalog produces internal candidates from activation targets and publication profiles. It should
not contain source-specific logic.

### Publication

Publication uses media publication profiles:

- wall art/profile image
- poster/card/calendar image
- book package
- eBook download
- audio stream/download
- film stream/download
- 3D viewer/download
- dataset landing page/download

Publication remains internal planning until provider/execution governance exists.

## Source Adapter Pattern

Each institution gets an adapter, but adapters do not create downstream commerce records directly.

Adapter responsibilities:

1. Fetch source metadata.
2. Create or update `source_item`.
3. Write immutable `source_record` snapshots.
4. Discover media file candidates.
5. Retrieve or register files.
6. Compute checksums.
7. Extract technical metadata.
8. Propose rights records.
9. Attach profile records.
10. Propose activation targets.

Adapters are forbidden to:

- bypass rights review
- write commerce scores
- create product recommendations
- publish catalog records
- infer commercial eligibility from source popularity
- treat aggregator rights as direct-source rights without evidence

## How This Avoids Redesign

The platform avoids redesign because future media change only three things:

1. Add source adapter.
2. Add or extend media profile.
3. Add activation policy.

The core remains stable:

- `source_item`
- `source_record`
- `media_file`
- `media_derivative`
- `media_rights`
- `preservation_event`
- `activation_target`

The downstream spine remains stable:

- Asset Intelligence
- Commerce Intelligence
- Product Routing
- Catalog
- Publication

## Governance Model

### Required Policies

- source adapter policy
- media retrieval policy
- rights evidence policy
- derivative generation policy
- profile validation policy
- activation policy
- preservation/fixity policy
- deactivation/takedown policy

### Required Human Gates

Human approval is required for:

- first activation of a new source institution
- first activation of a new media family
- any rights record used for commerce
- any file with mixed or ambiguous rights
- any 3D, audio, film, audiobook, eBook, or dataset product eligibility
- any aggregator record used without direct-source confirmation

### Replay Contract

Every activation target must be replayable from:

- source record ID
- source record hash
- media file checksum
- derivative checksum
- rights record ID
- media profile ID
- activation policy version
- worker version
- approval event

## Recommended Build Order

1. Core substrate vocabulary.
   - `source_institution`, media family, file role, derivative type, rights status, activation target type.

2. Source identity and snapshots.
   - `source_item`, `source_record`, `source_relationship`.

3. File and derivative graph.
   - `media_file`, `media_derivative`, checksum and storage conventions.

4. Rights and preservation.
   - `media_rights`, `preservation_event`, fixity policy.

5. Still visual and map profiles.
   - Images, maps, photography, posters.

6. Activation target bridge.
   - Bridge still visual assets into existing `illustration_opportunities` or a media-neutral commerce input.

7. Book/eBook profiles.
   - Books as provenance first, eBooks as deferred digital publication.

8. Dataset profile.
   - Evidence/enrichment first.

9. 3D pilot profile.
   - Smithsonian/NASA only.

10. Time-based media profile.
   - Audiobook/audio/film only after the file and rights model has production evidence.

## Final Architecture Position

Support every future media family by separating **source truth**, **file truth**, **rights truth**,
**profile truth**, and **commerce truth**.

The substrate owns source/media complexity. The existing platform owns scoring, routing, catalog,
publication, and governance decisions.

That is the line that prevents redesign.
