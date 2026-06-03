# BHL Illustration Asset Model

## Platform Identity

Nature & Culture is not a biodiversity inventory system. Nature & Culture is a place-centered public-domain illustration discovery and commerce platform. Biodiversity data is used only when it helps discover, verify, rank, or explain illustration opportunities connected to places.

Milestone 3 research is narrowed to commercially reusable public-domain illustration assets from the Biodiversity Heritage Library (BHL). The product path is asset-first:

```
Illustration Asset
        ↓
Species
        ↓
Place
```

This is not a book ingestion program and not a full literature graph. Books, pages, authors, publishers, citations, and bibliographic relationships are source context only when needed to prove image provenance, rights, taxon identity, or commercial reuse eligibility.

## Commercial Reuse Contract

An illustration asset is eligible only when all of the following are traceable:

- The original BHL item/page/image source URL.
- The preserved MinIO object and checksum.
- Public-domain or equivalent commercial reuse rights.
- The depicted species or taxon candidate.
- The place association derived from species range, occurrence, habitat, or governed place knowledge.

Outputs must support these product surfaces:

- Collections
- Wall Art
- Calendars
- Cards
- Puzzles
- Books

## Scope Rules

- Prefer high-quality illustration assets over complete books.
- Do not build full literature graphs.
- Do not persist unsupported species or place claims.
- Use books and pages only as provenance containers for the illustration asset.
- Optimize for asset reuse, rights clarity, visual quality, and product fit.

## Data Shape

The frozen architecture remains unchanged: PostgreSQL is authority, MinIO is evidence, workers execute, and FastAPI governs. Commercial assets are concept-centered: BHL illustration assets belong to taxon/concept context, and places connect to those concepts through governed evidence. The BHL path should add records that connect:

- Ranked taxon candidates for a place from GBIF and Wikidata evidence.
- BHL search targets generated from scientific names, canonical names, historic synonyms, common names, and genus fallback.
- `assets.asset_type = 'bhl_illustration'` only after BHL rights are explicitly verified as Public Domain or CC0.
- A species/taxon concept or fact with Darwin Core-aligned provenance.
- A governed relationship from the species/taxon context to place context.
- Product suitability metadata in derived research or product records, never as unsupported free text.

## Product Ranking Signals

Commercial reuse ranking should favor:

- Confirmed public-domain rights.
- Strong image integrity and preserved checksum.
- Clear species identification.
- Clear place association.
- Large usable image dimensions.
- Clean visual composition suitable for print products.
- Low ambiguity in source provenance.

## Taxon Discovery Stage

Input: one governed place. Output: prioritized public-domain illustration opportunities expressed as taxa-backed BHL search targets.

Nature & Culture does not optimize for species. Taxa are intermediate search handles for discovering high-value public-domain illustration opportunities. GBIF occurrence counts are evidence for place relevance only; they are capped and cannot dominate the ranking. Wikidata supplies taxon identity, GBIF taxon ID links, names, and place/range corroboration where available.

No BHL asset rights are inferred at this stage. Public-domain certainty is verified only after candidate BHL item/page/image metadata is retrieved.


## Illustration Opportunity Doctrine

Nature & Culture is place-centered, not species-centered and not art-centered. The commercial object is `Illustration Opportunity`, not `Species`, `Occurrence Record`, or `Taxon`.

Taxa are metadata, semantic anchors, and search handles. They are never the optimization target.

The output path is:

```
Place
↓
Illustration Opportunity
↓
Public-Domain Asset
↓
Collection
↓
Product
```

Source roles:

- BHL: Primary Discovery Source
- GBIF: Validation Source
- Wikidata: Context Source

Every Illustration Opportunity must satisfy place relevance, public-domain certainty, illustration quality, commercial value, provenance, and replayability.

Golden Age priority: publications from 1750 through 1900 receive the highest historical priority. Priority illustrators are Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel, and Wolf.

Roadmap order: Migration 16 → Illustration Opportunity Discovery → Human Approval → BHL Asset Ingestion → Collections → Products.

## Illustration Opportunity Output

The success metric is not `Species`; it is `Illustration Opportunity`. A taxon is context for search and provenance. The durable commercial object is a verified public-domain or CC0 illustration opportunity connected to one or more places through concepts.

Example shape:

```
Place: Great Barrier Reef
Taxon: Acanthaster planci
Publication: Naturalist's Miscellany
Illustrator: Nodder
Year: 1789
Public Domain: True
Opportunity Score: 0.91
```

One illustration can support many places. It must not be duplicated per place.

Commercial opportunity scoring maximizes:

- Public-domain certainty
- Illustration quality
- Place relevance
- Historical significance
- Commercial value
- Provenance
- Replayability

It must not maximize species frequency, popularity, raw occurrence counts, or biodiversity inventory completeness.
