# Institution Coverage Matrix v1

| Field | Value |
|---|---|
| Repository | opengracelabs/nc |
| Role | Lead Platform Engineer |
| Status | Planning matrix |
| Scope | Institution coverage against the Universal Media Substrate |
| Substrate basis | UMS M36 media types and activation phases |
| Constraint | No architecture redesign |

## Mission

Evaluate the current institution set against the Universal Media Substrate and determine which
media types are covered, weak, redundant, or missing.

Media types evaluated:

- Images
- Maps
- Photography
- Posters
- Fine Art
- Botanical Art
- Books
- eBooks
- Audiobooks
- Audio
- Film
- 3D
- Datasets

Institutions evaluated:

- BHL
- LOC
- Smithsonian
- NARA
- Europeana
- Rijksmuseum
- British Library
- NYPL
- DPLA
- Getty
- Met
- Kew
- Internet Archive
- Wikidata

## Coverage Legend

| Mark | Meaning |
|---|---|
| Strong | High-value source for this media type with useful metadata and plausible rights path. |
| Medium | Useful source, but coverage, rights, delivery, or metadata are uneven. |
| Weak | Discovery/reference value only, or media type exists but is not a reliable ingestion source. |
| None | Not a meaningful source for this media type. |
| Ref | Reference/authority/metadata role rather than media source. |

## Substrate Phase Context

| Media type | M36 substrate status | Prototype/activation posture |
|---|---|---|
| Images | Active | Supported now. |
| Maps | Active | Supported now. |
| Photography | Active | Supported now. |
| Posters | Active | Supported now. |
| Fine Art | Active as `image` + cultural classification | Supported now when rights/source quality pass. |
| Botanical Art | Active as `image` + biological classification | Supported now when rights/source quality pass. |
| Books | Pending Phase 2 | Registered, not broadly activated. |
| eBooks | Pending Phase 2 | Registered, not broadly activated. |
| Audiobooks | Pending Phase 2 | Registered, not activated. |
| Audio | Pending Phase 3 | Registered, not activated. |
| Film | Pending Phase 3 | Registered, not activated. |
| 3D | Pending Phase 4 | Registered, not activated. |
| Datasets | Pending Phase 4 | Registered, not activated. |

## Institution Coverage Matrix

| Institution | Images | Maps | Photography | Posters | Fine Art | Botanical Art | Books | eBooks | Audiobooks | Audio | Film | 3D | Datasets |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BHL | Strong | Weak | Weak | Weak | Weak | Strong | Strong | Medium | None | Weak | None | None | Medium |
| LOC | Strong | Strong | Strong | Strong | Medium | Medium | Strong | Medium | Weak | Medium | Medium | None | Medium |
| Smithsonian | Strong | Medium | Strong | Medium | Strong | Medium | Medium | Weak | Weak | Medium | Medium | Strong | Strong |
| NARA | Strong | Medium | Strong | Strong | Weak | None | Medium | Weak | Weak | Strong | Strong | None | Strong |
| Europeana | Medium | Medium | Medium | Medium | Medium | Medium | Medium | Medium | Weak | Medium | Medium | Weak | Medium |
| Rijksmuseum | Strong | Weak | Medium | Medium | Strong | Medium | Weak | Weak | None | None | None | Weak | Weak |
| British Library | Strong | Strong | Medium | Medium | Medium | Strong | Strong | Medium | Weak | Medium | Weak | None | Medium |
| NYPL | Strong | Strong | Strong | Strong | Medium | Medium | Strong | Medium | None | Weak | Weak | None | Medium |
| DPLA | Medium | Medium | Medium | Medium | Medium | Medium | Medium | Medium | Weak | Medium | Medium | Weak | Medium |
| Getty | Strong | Weak | Medium | Medium | Strong | Weak | Medium | Weak | None | Weak | Weak | Weak | Strong |
| Met | Strong | Weak | Medium | Medium | Strong | Medium | Medium | Weak | None | Weak | Weak | Medium | Medium |
| Kew | Strong | Weak | Medium | Weak | Medium | Strong | Strong | Medium | None | Weak | None | Medium | Strong |
| Internet Archive | Medium | Medium | Medium | Medium | Weak | Weak | Strong | Strong | Strong | Strong | Strong | Weak | Strong |
| Wikidata | Ref | Ref | Ref | Ref | Ref | Ref | Ref | Ref | Ref | Ref | Ref | Ref | Ref |

## Institution Roles

### BHL

Best role:

- Natural history illustration.
- Botanical art.
- Book/page provenance.
- OCR/name/taxon evidence.

Substrate fit:

- Strong current fit for Phase 1 still images extracted from books.
- Strong reference model for source evidence and page-level provenance.

Weakness:

- Not a broad map, poster, photography, audio, film, or 3D source.
- Complete books/eBooks remain Phase 2.

### LOC

Best role:

- Maps.
- Photography.
- Posters.
- Still images.
- Books/bibliographic metadata.
- Authority and linked data.

Substrate fit:

- Best immediate expansion source after BHL.
- Strongest single institution for Phase 1 media breadth.

Weakness:

- Audio/film/books need media-family-specific runtime beyond Phase 1.
- 3D is not a meaningful LOC coverage target.

### Smithsonian

Best role:

- CC0 images.
- Photography.
- Fine art and cultural objects.
- Open 3D.
- Scientific/cultural datasets.

Substrate fit:

- Strong 2D Phase 1 source.
- Strategic future 3D pilot.

Weakness:

- 3D remains Phase 4 despite strong source availability.
- Books/eBooks are not the first Smithsonian value path.

### NARA

Best role:

- US federal archival photography.
- Posters.
- Maps.
- Film.
- Audio.
- Datasets and archival records.

Substrate fit:

- Strong still-image and archival record source.
- Best government source for future film/audio.

Weakness:

- Time-based media must wait for Phase 3.
- Archival hierarchy and rights review need careful source-record modeling.

### Europeana

Best role:

- Aggregation.
- EDM normalization.
- Provider/source linking.
- Rights anomaly detection.
- Cross-institution discovery.

Substrate fit:

- Strong metadata and aggregation model.
- Useful for discovery and dedupe.

Weakness:

- Redundant as media source when direct source institution records exist.
- Should not become source-of-record by default.

### Rijksmuseum

Best role:

- Fine art.
- Public collection UX benchmark.
- High-quality images and object metadata.

Substrate fit:

- Strong selective fine-art source.

Weakness:

- Narrow compared with LOC/Smithsonian/Met/Getty.
- Not a broad substrate coverage institution.

### British Library

Best role:

- Books.
- Maps.
- Manuscripts.
- Botanical and historical illustration.
- Bibliographic metadata and IIIF reference.

Substrate fit:

- Strong future book/map source.
- Useful institutional reference for IIIF and bibliographic workflows.

Weakness:

- Rights/access paths vary by collection.
- Production dependency should be selective until source-specific access is proven.

### NYPL

Best role:

- Public-domain digital images.
- Maps.
- Photography.
- Posters.
- Books and cultural collections.

Substrate fit:

- Strong Phase 1 supplement, especially maps/posters/photography.

Weakness:

- Overlaps heavily with LOC and DPLA.
- Less important than LOC for national-scale authority metadata.

### DPLA

Best role:

- Aggregation across US institutions.
- Metadata discovery.
- Partner/source routing.

Substrate fit:

- Useful US analogue to Europeana for discovery and provider linking.

Weakness:

- Redundant as source-of-record.
- Should point to provider institutions rather than drive activation directly.

### Getty

Best role:

- Fine art metadata.
- Art objects.
- Vocabulary and research datasets.
- Images where open access permits.

Substrate fit:

- Strong for art authority/reference and datasets.

Weakness:

- Overlaps with Met/Rijksmuseum for fine art source role.
- Less useful for maps, posters, broad photography, and books.

### Met

Best role:

- Fine art.
- Object images.
- Open access cultural collections.
- Some 3D/object experimentation.

Substrate fit:

- Strong direct fine-art source.

Weakness:

- Narrower media coverage than Smithsonian/LOC/NARA/Internet Archive.
- Botanical art and books are secondary.

### Kew

Best role:

- Botanical art.
- Botanical collections.
- Plant science references.
- Herbarium/scientific datasets.

Substrate fit:

- Best specialist gap-filler for botanical art and plant datasets.

Weakness:

- Narrow domain.
- Not a general substrate coverage source.

### Internet Archive

Best role:

- Books.
- eBooks.
- Audiobooks.
- Audio.
- Film.
- Broad file manifests.
- Datasets and preserved derivatives.

Substrate fit:

- Best stress test for Phase 2/3/4 file-manifest generality.

Weakness:

- Rights and metadata quality are inconsistent by uploader/collection.
- Should be deferred until M36 source_item/media_file/rights gates are mature.

### Wikidata

Best role:

- Entity reconciliation.
- QIDs.
- Cross-institution links.
- Place, creator, concept, taxon, and institution identity hints.

Substrate fit:

- Essential authority-reference layer.

Weakness:

- Not a media source.
- Open-edit model cannot override NC PostgreSQL authority.

## Already Covered Media Types

Covered strongly enough for Phase 1 activation:

| Media type | Primary institutions | Notes |
|---|---|---|
| Images | BHL, LOC, Smithsonian, Met, Rijksmuseum, NYPL | M36 active; rights/source quality are the main gates. |
| Maps | LOC, British Library, NYPL, NARA | M36 active; LOC should be first production bridge. |
| Photography | LOC, Smithsonian, NARA, NYPL | M36 active; strong public-domain source pool. |
| Posters | LOC, NARA, NYPL, Smithsonian | M36 active; WPA/National Park/poster collections are strong candidates. |
| Fine Art | Smithsonian, Met, Rijksmuseum, Getty | M36 active as `image` + cultural classification. |
| Botanical Art | BHL, Kew, British Library | M36 active as `image` + biological/botanical classification. |

Covered structurally but not activation-ready:

| Media type | Primary institutions | Reason |
|---|---|---|
| Books | BHL, LOC, British Library, Internet Archive, NYPL | M36 registers but Phase 2 activation required. |
| eBooks | Internet Archive, BHL, LOC, British Library | Requires Phase 2 delivery/access profile. |
| Datasets | Smithsonian, NARA, Kew, Internet Archive, LOC | M36 registers but Phase 4 activation required. |

## Weak Media Types

| Media type | Weakness | Best institution to close gap |
|---|---|---|
| Audiobooks | Almost entirely dependent on Internet Archive-like file manifests and rights. | Internet Archive |
| Audio | Requires time-based media, transcripts, rights, derivatives, streaming/download policy. | NARA, Internet Archive, British Library |
| Film | Requires time-based media, captions, segment/derivative policy, streaming/download policy. | NARA, Internet Archive, LOC |
| 3D | Strong source exists, but runtime is Phase 4 and needs model validation/viewer policy. | Smithsonian |
| Datasets | Source coverage exists, but product/public dataset governance is deferred. | Smithsonian, NARA, Kew, Internet Archive |

## Redundant Institutions

Redundancy is not bad; it becomes a problem only when multiple aggregators or museums add the same
media type without adding a new authority, rights, or metadata advantage.

| Redundancy cluster | Institutions | Recommendation |
|---|---|---|
| Aggregators | Europeana, DPLA | Keep both as discovery/metadata routes; do not make either canonical media source by default. |
| Fine art museums | Rijksmuseum, Getty, Met, Smithsonian | Keep Smithsonian + Met as broad open-access anchors; add Rijksmuseum/Getty selectively for quality/reference depth. |
| Broad books/files | Internet Archive, LOC, British Library, NYPL, BHL | Use BHL for natural history, LOC for authority/maps, Internet Archive for file manifests, British Library/NYPL selectively. |
| Maps/photography/posters | LOC, NARA, NYPL, British Library | LOC first; NARA for federal archival depth; NYPL/BL for collection-specific enrichment. |

## Missing Institutions

The current list is strong, but these institutions would close strategic gaps.

| Missing institution/source | Gap closed | Why it matters |
|---|---|---|
| GBIF | Biodiversity occurrences/datasets | Complements BHL and Darwin Core evidence for place/species relevance. |
| USGS | Maps, geology, datasets, photography | Strong Yellowstone/geospatial/scientific source; supports PostGIS and datasets. |
| National Park Service | Place authority, maps, photography, interpretive datasets | Direct park context for Yellowstone and US place pages. |
| OpenStreetMap | Geometry/boundaries | Practical spatial geometry source when official boundaries are incomplete. |
| Natural History Museum London | Botanical/zoological collections and datasets | Fills natural-history object gap beyond BHL/Kew. |
| British Museum | Cultural objects, fine art, archaeology | Broader cultural heritage source beyond art museums. |
| Art Institute of Chicago / Cleveland Museum of Art | Open-access fine art | Adds high-quality public-domain fine-art breadth if Met/Getty/Rijksmuseum are insufficient. |
| Europe PMC / HathiTrust | Books and scholarly text | Future book/text layer, not Phase 1. |

## Minimum Institutional Set

Purpose: launch Phase 1 visual/place-commerce prototype and early production without excess adapters.

| Institution | Why included |
|---|---|
| BHL | Botanical art, natural history illustrations, book/page provenance, existing precedent. |
| LOC | Maps, photography, posters, still images, books, authority metadata. |
| Smithsonian | CC0 images, photography, fine art/cultural objects, future 3D. |
| Wikidata | Entity reconciliation for places, concepts, institutions, creators, taxa. |

Minimum set coverage:

- Strong: images, maps, photography, posters, fine art, botanical art.
- Medium: books, datasets.
- Weak/deferred: eBooks, audiobooks, audio, film, 3D.

## Optimal Institutional Set

Purpose: broad, balanced coverage without overloading the platform with redundant sources.

| Institution | Why included |
|---|---|
| BHL | Natural history and botanical core. |
| LOC | Phase 1 breadth and authority metadata. |
| Smithsonian | CC0 2D and strategic 3D. |
| NARA | Federal photography, posters, maps, datasets, film/audio future. |
| Internet Archive | Books/eBooks/audio/film/file manifests after future phases. |
| British Library | Books, maps, manuscripts, IIIF/bibliographic reference. |
| Kew | Botanical specialization and plant datasets. |
| Wikidata | Entity reconciliation. |
| Europeana | International aggregation/reference, EDM. |

Optimal set coverage:

- Strong: all Phase 1 media.
- Medium to strong: books, eBooks, datasets.
- Medium future coverage: audio, film, 3D.
- Redundancy controlled: Europeana is aggregator/reference, not source-of-record.

## Maximum Institutional Set

Purpose: full institutional breadth once adapter governance and dedupe are mature.

Include all current institutions:

- BHL
- LOC
- Smithsonian
- NARA
- Europeana
- Rijksmuseum
- British Library
- NYPL
- DPLA
- Getty
- Met
- Kew
- Internet Archive
- Wikidata

Add missing strategic institutions:

- GBIF
- USGS
- National Park Service
- OpenStreetMap
- Natural History Museum London
- British Museum
- selected open-access art museums

Maximum set warning:

- Do not implement maximum set early.
- It requires aggregator dedupe, provider/source-of-record resolution, rights normalization,
  institution-specific adapter contracts, and source priority rules.
- Without those, the maximum set will create duplicate records, ambiguous rights, and inconsistent
  media quality.

## Recommended Onboarding Order

1. BHL reinforcement.
2. LOC Phase 1 bridge: maps, photography, posters, images.
3. Smithsonian 2D Open Access.
4. Wikidata reconciliation hardening.
5. NARA still-image/poster/map pilot.
6. Kew botanical art/dataset pilot.
7. British Library selective maps/books pilot.
8. Internet Archive book/eBook/file-manifest pilot.
9. Europeana and DPLA aggregation/dedupe pilots.
10. Met/Rijksmuseum/Getty fine-art selective pilots.
11. Smithsonian 3D pilot after Phase 4 amendment.
12. NARA/Internet Archive audio/film pilots after Phase 3 amendment.

## Final Recommendation

Use the minimum set for the first working prototype and early Phase 1 production:

```text
BHL + LOC + Smithsonian + Wikidata
```

Adopt the optimal set as the 10-year institutional architecture:

```text
BHL + LOC + Smithsonian + NARA + Internet Archive + British Library + Kew + Wikidata + Europeana
```

Treat the maximum set as a mature network target, not an implementation starting point.
