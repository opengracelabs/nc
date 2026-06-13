# NC-TAXON-001: Taxon Factory Blueprint

| Field | Value |
|---|---|
| Document | NC-TAXON-001 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | DD-GBIF-001 · DD-BHL-001 · NC-GRAPH-002 · NC-ASSETS-1000000 · NC-COMMERCE-2000 · Illustration Opportunity Doctrine |
| Reference Models | GBIF Backbone Taxonomy · BHL Name Usage Service · NHM Data Portal · Smithsonian Open Access NMNH |
| Scope | Taxonomic authority architecture for Nature & Culture from hundreds to one million assets. Defines the Taxon node schema, factory pipeline, Species→Place model, Species→Collection model, Species→Product model, BHL→GBIF integration, Darwin Core integration, Neo4j graph schema, and educational pathway architecture. |

---

## Governing Doctrine

**A taxon is not a product. An Illustration Opportunity is a product.**

The Taxon Factory does not sell species. It resolves the biological identity of a named illustrator's documented observation, anchors that observation to a place, and routes the result into NC's collection and product pipeline.

The commercial object is always: an illustration by a named person, depicting a specific organism, at or associated with a specific place, verified PD, published under NC's editorial authority.

The taxon provides three things: identity (what is this organism?), geography (where does it live?), and narrative (why does it matter?). It is the scientific substrate of the Illustration Opportunity — not the thing sold.

---

## 1. Taxonomic Authority Architecture

### GBIF as the Canonical Biological Anchor

Every taxon in Nature & Culture traces to a single identifier: a GBIF Backbone Taxonomy taxon key. No taxon enters the NC graph without one.

**Why GBIF, not alternatives:**

| Alternative | Reason not used |
|---|---|
| Catalogue of Life (CoL) | GBIF backbone derives from CoL; GBIF provides direct API + taxon keys + occurrence records in one system |
| iNaturalist taxon IDs | iNaturalist is GBIF-indexed; iNaturalist observation media is CC BY-NC — permanently prohibited (DD-GBIF-001, DD-ALA-001) |
| EOL (Encyclopedia of Life) | Inconsistent PD coverage; media pipeline risks |
| ITIS | US-centric; superseded by GBIF for global coverage |
| WoRMS (marine) | Use as supplementary authority for marine taxa; cross-reference to GBIF key |

**GBIF Backbone resolution contract:**

```
Input:  scientific_name (string) OR bhl_gbif_usage_key (integer)
Output: {
  gbif_taxon_key:      integer (canonical anchor, immutable)
  gbif_canonical_name: string  (accepted scientific name)
  gbif_synonym_of:     integer (if taxonomic status = SYNONYM → points to accepted key)
  gbif_kingdom:        string
  gbif_phylum:         string
  gbif_class:          string
  gbif_order:          string
  gbif_family:         string
  gbif_genus:          string
  gbif_species:        string  (null for genus-rank or above)
  gbif_taxon_rank:     enum    (SPECIES | GENUS | FAMILY | ORDER | CLASS | PHYLUM | KINGDOM)
  gbif_taxonomic_status: enum  (ACCEPTED | SYNONYM | DOUBTFUL | HETEROTYPIC_SYNONYM)
  gbif_vernacular_name: string (English common name, if available)
  gbif_backbone_version: string (GBIF backbone release date, e.g., "2024-09-01")
  gbif_resolution_date: ISO date
  gbif_confidence:      float  (0.0 – 1.0)
  resolution_method:   enum    (BHL_NAMES | OCR_NER | MANUAL | FUZZY_MATCH)
}
```

**Synonym handling:**
If GBIF returns `taxonomic_status = SYNONYM`, NC follows the pointer to the accepted name and records both:
- `gbif_taxon_key` = accepted species key
- `gbif_synonym_key` = original name key (for provenance; BHL may use the old name)
- `gbif_canonical_name` = accepted name in product copy

**Backbone version pinning:**
GBIF releases backbone updates approximately twice yearly. NC records `gbif_backbone_version` with every resolution. Annual review confirms whether updated backbone changes any existing IO's taxon key. If a key is retired or merged, the affected IOs require a human review gate before any product copy changes.

### Taxonomic Hierarchy in NC

NC does not store the full eight-rank Linnaean hierarchy for every asset. The working hierarchy is:

```
Kingdom → Class → Order → Family → Genus → Species
```

Phylum is stored for completeness but not used in collection generation or product routing. Subspecies is stored when the original illustration explicitly depicts a named subspecies.

**Hierarchy roles in NC:**

| Rank | NC Role |
|---|---|
| Kingdom | Broad category navigation (Plantae / Animalia / Fungi / Chromista / Protozoa) |
| Class | Editorial category (Aves, Mammalia, Insecta, Liliopsida, Magnoliopsida…) |
| Order | Collection grouping boundary (Passeriformes, Lepidoptera, Rosales…) |
| Family | Primary collection-generation unit (Trochilidae, Orchidaceae, Rosaceae…) |
| Genus | Attribution unit (used when species is uncertain in historical illustrations) |
| Species | Canonical IO biological anchor |

---

## 2. Species → Place Model

### The Place Association Problem

A historical illustration of *Nymphaea caerulea* (Blue Lotus) may have been painted by Pierre-Joseph Redouté in Paris from a specimen sent from Egypt. The correct place anchor is Egypt — not France, despite the illustration's physical production location.

NC's place association model resolves this by classifying every species-place link by its confidence class:

### Five Place Association Classes

| Class | Name | Basis | Confidence Range | Automation |
|---|---|---|---|---|
| **PAC-1** | Explicit | Place named in caption, plate title, or expedition record | 0.90 – 0.99 | Yes |
| **PAC-2** | Biographical | Illustrator documented at place during the period of the illustration | 0.75 – 0.90 | Yes, with ULAN date validation |
| **PAC-3** | Ecological | GBIF occurrence records confirm species present at place (≥3 occurrences within place bounding box) | 0.65 – 0.80 | Yes, with GBIF validation |
| **PAC-4** | Range | Species native range (GBIF expert range polygon) intersects place boundary | 0.45 – 0.65 | Yes, but requires human gate to accept |
| **PAC-5** | Editorial | Species is ecologically representative of the place (editorial decision) | 0.30 – 0.50 | Human only |

**Commercial pipeline requirements:**
- Tier 1 IO (Commerce): PAC-1 or PAC-2 required. PAC-3 accepted only if ≥3 GBIF occurrences confirmed within the NC place boundary and illustrator's known working region overlaps.
- Tier 2 IO (Editorial): PAC-1 through PAC-3 accepted.
- Tier 3 IO (Discovery): PAC-1 through PAC-4 accepted.

**PAC-4 and PAC-5 cannot generate CE products without human gate review.**

### Place Relevance Score

Each Taxon-Place edge in the graph carries a `place_relevance_score` (0.0 – 1.0):

```
place_relevance_score = 
  (pac_class_confidence)                        * 0.40 +
  (endemism_score)                              * 0.30 +
  (illustrator_documented_at_place ? 1.0 : 0.3) * 0.20 +
  (designation_endemic ? 1.0 : 0.0)             * 0.10
```

Where:

```
endemism_score = gbif_occurrence_at_place_capped / max(gbif_occurrence_total_capped, 1)
  — uses gbif_occurrence_count_capped (≤100) per CI Constitution / DD-GBIF-001 Article 3
  — never uses raw occurrence count in any scoring formula
```

**Default when GBIF validation absent:**
`place_relevance_score = 0.72` (SA-GBIF-001 default; see DD-GBIF-001)

### Multi-Place Association

A single species may be associated with multiple NC places. This is expected and correct. *Haematopus ostralegus* (Oystercatcher) occurs at South Georgia, Great Barrier Reef, and the Netherlands simultaneously.

Multi-place associations generate:
- Multiple Taxon-Place graph edges (each with its own `place_relevance_score`)
- The IO is anchored to the place where the illustration was most likely created (PAC-1/2 hierarchy)
- Discovery journeys surface the IO across all associated places

---

## 3. Species → Collection Model

### Collection Generation Triggers

A collection is generated when a set of IOs crosses a defined threshold. Four triggers exist:

**T1 — Illustrator Collection (Family/Order anchor):**
```
Trigger: Count(IO) WHERE illustrator = X AND taxon.family = F ≥ 3
         OR Count(IO) WHERE illustrator = X AND taxon.order = O ≥ 5
Result:  Collection candidate: "{Illustrator}'s {Common Name of Family/Order}"
Example: Gould's Trochilidae → "Gould: A Monograph of the Hummingbirds"
```

**T2 — Place Collection (Ecological anchor):**
```
Trigger: Count(IO) WHERE place = P AND pac_class ≤ PAC-3 ≥ 5
Result:  Collection candidate: "{Place} Natural History Series"
Example: 5+ IOs of species confirmed at Great Barrier Reef → "Reef Natural History"
```

**T3 — Designation Collection (Endemic anchor):**
```
Trigger: Count(IO) WHERE taxon.endemism_at_designation ≥ 0.80 AND designation = D ≥ 3
Result:  Collection candidate: "{Designation Name} Endemic Species"
Example: 3+ IOs of species endemic to Galápagos Marine Reserve → "Galápagos Endemic Series"
```

**T4 — Family Atlas:**
```
Trigger: Count(IO) WHERE taxon.family = F ≥ 10 AND distinct_illustrators ≥ 2
Result:  Collection candidate: "{Family Common Name} Atlas"
Example: 10+ IOs of Orchidaceae from multiple illustrators → "Orchid Atlas"
```

### Collection Priority Scoring

When multiple triggers fire simultaneously, collections are ranked by:

```
collection_priority_score =
  (illustrator_priority_score)   * 0.35  -- priority illustrators score higher
  (io_count / threshold_count)   * 0.25  -- more IOs = more complete collection
  (place_designation_depth)      * 0.20  -- WH > Biosphere > Geopark > undesignated
  (commercial_readiness)         * 0.20  -- all IOs Tier 1 = higher priority
```

**Priority illustrators (doctrine-defined) always score 1.0 for `illustrator_priority_score`.**

A collection candidate at threshold becomes visible to the curator queue. No collection is published without the curator review gate (one of the four mandatory human gates in the Place Factory model).

### Expedition Collections (Special Case)

Expeditions generate collections that cut across families and places:

```
Trigger: Count(IO) WHERE expedition = E ≥ 5 AND distinct_places ≥ 2
Result:  Collection: "{Expedition Name}: Natural History Plates"
```

Key expedition collections enabled by BHL + Taxon Factory:

| Expedition | Illustrators | Places | Key Taxa |
|---|---|---|---|
| Cook's First Voyage (Endeavour) | Parkinson · Nodder | Pacific / NZ / Australia | Pacific flora + fauna |
| Cook's Second Voyage | Forster (G+R) | South Georgia · Tahiti | Sub-Antarctic species |
| Humboldt/Bonpland | Various | Andes · Amazon | Neotropical flora |
| Audubon's Mississippi Journey | Audubon | SE USA / Mississippi River | American birds |
| Darwin's Beagle | Various (FitzRoy voyage) | Galápagos · Patagonia | Finches + tortoises |
| Haeckel's Adriatic Surveys | Haeckel | Mediterranean · Atlantic | Radiolarians + medusae |

---

## 4. Species → Product Model

### The IO Completeness Test

A taxon enables a product only when attached to a complete Illustration Opportunity. The IO Completeness Test requires all five fields:

```
IO_COMPLETE = (
  ulan_id IS NOT NULL          AND  -- named illustrator (ULAN-anchored)
  gbif_taxon_key IS NOT NULL   AND  -- biological identity confirmed
  geonames_id IS NOT NULL      AND  -- place anchor confirmed
  rights_status = "ALLOWED"   AND  -- PD rights cleared
  asset_tier IN ("Tier 1", "Tier 2")  -- quality threshold met
)
```

If any field is null or fails: the asset is not commerce-ready. It routes to Editorial (Tier 2) or Discovery (Tier 3) only.

### Product Routing by IO Tier

| Tier | Condition | Products Enabled |
|---|---|---|
| **Tier 1** | All five IO fields complete + confidence ≥ 0.85 | All product families: A (Museum Print), B (Wall Art), C (Educational), D (Books), E (Paper Goods), F (Digital), G (Collector CE) |
| **Tier 2** | Rights + one anchor (illustrator OR place, not both) | B (Wall Art), C (Educational), F (Digital Study) — no CE |
| **Tier 3** | Rights confirmed, no anchors | Discovery display only — no products |
| **Tier 4** | Below quality threshold | Reference only — never public |

### Taxon-Specific Product Requirements

All natural history products (any product derived from an IO with a confirmed taxon) require Darwin Core metadata at the product record level. This is non-negotiable for institutional credibility.

**Minimum Darwin Core for any product:**

```
dwc:scientificName      -- from GBIF canonical name
gbif:taxonKey           -- GBIF Backbone key (integer)
dwc:vernacularName      -- English common name from GBIF (used in product title)
dwc:basisOfRecord       -- "HumanObservation" (all illustrated records)
dwc:recordedBy          -- illustrator name + ULAN ID
dwc:eventDate           -- illustration date (year or year range)
dwc:locality            -- place name + GeoNames ID
dwc:family              -- taxonomic family
dwc:kingdom             -- taxonomic kingdom
```

### Product Copy Rules for Taxon Content

From NC-COMMERCE-2000 invariant CI-11 (no invented rights language) extended to taxonomy:

**PERMITTED in product copy:**
- Vernacular name (from GBIF name usage): "Wild Turkey", "Blue Lotus", "Giant Radiolarian"
- Illustrator attribution: "John James Audubon (1785–1851)"
- Place name: "Observed at the Florida Everglades"
- Family name: "Family Phasianidae"
- Date of illustration: "Birds of America, 1827"

**PROHIBITED in product copy:**
- Scientific name as headline (permitted in body text; not for marketing lead)
- Conservation status language ("endangered", "vulnerable") — NC does not sell species; conservation status is not product copy
- "Discovered by" language for any living taxonomists or scientists without explicit permission
- Any claim about the species' current distribution (NC content is historical; present distribution is editorial matter)
- IUCN Red List status as a product selling point (introduces animal welfare framing inconsistent with PD cultural commerce doctrine)

---

## 5. BHL → GBIF Integration

### The Bridge Architecture

BHL's Name Usage service performs taxon name recognition (TNR) against the GBIF backbone for every OCR-processed page. The output is a `GBIFUsageKey` attached to each identified name. This is NC's primary automated resolution path.

**Bridge pipeline:**

```
Stage 1: BHL Page API
  GET /api3?op=GetPageNames&pageid={id}&format=json
  Response: Names[]{
    NameFound:            string  (raw OCR name)
    NameConfidenceRating: integer (0–100)
    GBIFUsageKey:         integer (nullable)
  }

Stage 2: GBIF Usage Key Validation
  For each GBIFUsageKey != null:
    GET https://api.gbif.org/v1/species/{key}
    Confirm: acceptedKey, canonicalName, kingdom, taxonomicStatus
    If taxonomicStatus = SYNONYM → follow acceptedKey

Stage 3: NC Taxon Record Write
  INSERT taxon {
    gbif_taxon_key      = acceptedKey,
    gbif_canonical_name = canonicalName,
    bhl_usage_key       = GBIFUsageKey (may differ if synonym was resolved),
    bhl_name_found      = NameFound,
    gbif_confidence     = NameConfidenceRating / 100.0,
    resolution_method   = "BHL_NAMES"
  }

Stage 4: Cross-validation
  — Confirm kingdom consistency with illustration context
    (an illustration in a botanical monograph should not resolve to Animalia)
  — If kingdom mismatch: downgrade confidence by 0.30, flag REVIEW_REQUIRED

Stage 5: Confidence Threshold Routing
  gbif_confidence ≥ 0.85: automated acceptance → Taxon node created
  gbif_confidence 0.70–0.84: REVIEW_REQUIRED workflow item opened
  gbif_confidence < 0.70: human gate required
  GBIFUsageKey = null: fallback to OCR-NER pipeline (Stage 6)
```

### Fallback: OCR-NER Pipeline

When BHL Names service returns no key (older volumes with poor OCR, non-Latin script captions):

```
Stage 6: OCR Caption Extraction
  — Extract full page OCR text from BHL pageimage
  — Apply spaCy NER with biological entity model (en_core_sci_md or equivalent)
  — Identify candidate scientific names (Genus species pattern)

Stage 7: GBIF Fuzzy Species Search
  GET https://api.gbif.org/v1/species/suggest?q={candidate_name}
  → Return top 3 candidates, each with confidence score

Stage 8: Context Disambiguation
  — If illustrator = Audubon AND kingdom = Animalia AND class = Aves:
    bias toward North American bird species (known Audubon range)
  — If title contains geographic indicator ("Flora of Ceylon", "Birds of Australia"):
    filter GBIF candidates by occurrence region

Stage 9: Manual queue
  — If best confidence < 0.70 after disambiguation: add to curator review queue
  — resolution_method = "OCR_NER" (lower confidence than BHL_NAMES)
```

### Handling Multi-Species Illustrations

Some illustrations depict multiple species (e.g., Haeckel's radiolarian plates show 8–20 distinct organisms). NC's handling:

- **Primary taxon**: The dominant organism in the composition (largest, most centered, or most identified by the original plate title)
- **Secondary taxa**: Stored as `taxon_associations[]` with `association_type = "co-depicted"`
- **Product copy**: Uses primary taxon's vernacular name
- **Graph edges**: All depicted taxa receive `DEPICTED_IN` edges to the IO, with `is_primary: true/false`
- **Darwin Core**: Primary taxon in `dwc:scientificName`; secondary taxa in `dwc:associatedTaxa` (comma-separated)

---

## 6. Darwin Core Integration

### Full Darwin Core Field Mapping

NC implements Darwin Core as the canonical natural history metadata standard. Every IO with a confirmed taxon generates a Darwin Core record. This record is:

1. Stored in `illustration_opportunities.darwin_core_json` (JSONB column)
2. Exposed in the IIIF manifest `metadata[]` array for each IO
3. Available as Darwin Core XML export via the S3 Institutional subscription tier
4. Used to populate `Schema.org/CreativeWork` structured data on product pages

**Complete NC Darwin Core mapping:**

```json
{
  "dcterms:type":             "StillImage",
  "basisOfRecord":            "HumanObservation",

  "occurrenceID":             "nc-io-{uuid}",
  "catalogNumber":            "NC-{COLLECTION_SLUG}-{IO_NUMBER}",

  "scientificName":           "{gbif_canonical_name}",
  "taxonID":                  "gbif:{gbif_taxon_key}",
  "taxonRank":                "{gbif_taxon_rank}",
  "taxonomicStatus":          "accepted",
  "nameAccordingTo":          "GBIF Backbone Taxonomy v{gbif_backbone_version}",

  "kingdom":                  "{gbif_kingdom}",
  "phylum":                   "{gbif_phylum}",
  "class":                    "{gbif_class}",
  "order":                    "{gbif_order}",
  "family":                   "{gbif_family}",
  "genus":                    "{gbif_genus}",
  "vernacularName":           "{gbif_vernacular_name}",

  "recordedBy":               "{illustrator_name} [ULAN:{ulan_id}]",
  "eventDate":                "{illustration_date_year}",

  "locality":                 "{place_name}",
  "locationID":               "geonames:{geonames_id}",
  "countryCode":              "{iso_country_2}",
  "decimalLatitude":          "{geonames_latitude}",
  "decimalLongitude":         "{geonames_longitude}",
  "coordinateUncertaintyInMeters": 50000,

  "associatedMedia":          "nc.art/collections/{collection_slug}/io/{uuid}",
  "associatedReferences":     "{bhl_title_citation}",
  "bibliographicCitation":    "{illustrator_surname}, {initials}. ({year}). {title}, {plate}. {source_institution}. {bhl_url}",

  "dcterms:license":          "{rights_uri}",
  "dcterms:rightsHolder":     "{source_institution_name}",
  "dcterms:accessRights":     "CC0 1.0 Universal / Public Domain Mark 1.0",

  "institutionCode":          "NC",
  "collectionCode":           "{collection_slug}",
  "datasetName":              "Nature & Culture Illustration Opportunities",
  "datasetID":                "nc.art/data/ios/{collection_slug}",

  "nc:illustrationOpportunityID": "{uuid}",
  "nc:assetTier":             "Tier 1",
  "nc:rightsConfidence":      "{confidence_score}",
  "nc:ulanID":                "{ulan_id}",
  "nc:gbifTaxonKey":          "{gbif_taxon_key}",
  "nc:bhlPageID":             "{bhl_page_id}",
  "nc:placeRelevanceScore":   "{place_relevance_score}"
}
```

**`nc:` extension namespace:** NC registers a Darwin Core extension namespace at `nc.art/data/terms/` to accommodate institution-specific fields (ulan_id, gbif taxon key, bhl page id, place relevance score). This is standard Darwin Core practice for domain-specific extensions.

### Darwin Core Validity Rules

```
VALID if:
  basisOfRecord = "HumanObservation"
  scientificName = GBIF accepted name (not synonym)
  taxonID format = "gbif:{integer}"
  eventDate = ISO 8601 year (YYYY) or year range (YYYY/YYYY)
  recordedBy includes ULAN ID in brackets
  locationID format = "geonames:{integer}"
  coordinateUncertaintyInMeters ≥ 1000 (historical illustrations have geographic uncertainty)

INVALID if:
  scientificName is a common name
  taxonID is missing or null
  recordedBy is "Unknown" or anonymous
  eventDate is absent
```

Invalid Darwin Core records do not block Editorial (Tier 2) display but do block:
- S3 Institutional subscription Darwin Core export
- IIIF manifest `metadata[]` taxon fields
- Any CE product where the taxon is the primary marketing claim

---

## 7. Neo4j Taxonomic Graph

### Taxon Node Schema

Extending NC-GRAPH-002's existing Taxon node type with full schema:

```cypher
(:Taxon {
  id:                     string   // UUID, NC-internal
  gbif_taxon_key:         integer  // GBIF Backbone canonical key — immutable anchor
  gbif_canonical_name:    string   // Accepted scientific name (binomial or uninomial)
  gbif_synonym_key:       integer? // If resolved from synonym; null if originally accepted
  gbif_vernacular_name:   string?  // English common name
  kingdom:                string   // Animalia | Plantae | Fungi | Chromista | Protozoa
  phylum:                 string?
  class:                  string?
  order:                  string?
  family:                 string   // Required for collection generation
  genus:                  string?
  species:                string?  // null if rank = GENUS or above
  taxon_rank:             string   // SPECIES | GENUS | FAMILY | ORDER
  gbif_backbone_version:  string   // "2024-09-01"
  gbif_resolution_date:   date
  gbif_confidence:        float    // 0.0 – 1.0
  resolution_method:      string   // BHL_NAMES | OCR_NER | MANUAL | FUZZY_MATCH
  endemism_score:         float?   // 0.0 – 1.0, calculated from GBIF occurrences
  nc_io_count:            integer  // Derived: count of DEPICTED_IN edges (Tier 1)
  nc_collection_count:    integer  // Derived: count of collections this taxon appears in
  is_priority_taxon:      boolean  // True if taxon illustrated by a priority illustrator
  created_at:             datetime
  updated_at:             datetime
})
```

**Index requirements:**
```cypher
CREATE INDEX taxon_gbif_key FOR (t:Taxon) ON (t.gbif_taxon_key)
CREATE INDEX taxon_family   FOR (t:Taxon) ON (t.family)
CREATE INDEX taxon_kingdom  FOR (t:Taxon) ON (t.kingdom)
CREATE INDEX taxon_class    FOR (t:Taxon) ON (t.class)
```

### New Relationship Types (Taxon-specific additions to NC-GRAPH-002's 32)

| Relationship | From → To | Properties | Notes |
|---|---|---|---|
| `DEPICTED_IN` | Taxon → IllustrationOpportunity | `is_primary: bool` | Primary or co-depicted |
| `OCCURS_AT` | Taxon → Place | `pac_class: int`, `place_relevance_score: float`, `occurrence_count_capped: int`, `validated_by_gbif: bool` | Central place-species edge |
| `BELONGS_TO_FAMILY` | Taxon → TaxonFamily | — | Graph hierarchy |
| `CO_OCCURS_WITH` | Taxon → Taxon | `place_slug: string`, `co_io_count: int` | Derived: same illustration |
| `NAMED_AFTER_PLACE` | Taxon → Place | `naming_authority: string` | e.g., Epidendrum yosemitense |
| `FIRST_DESCRIBED_BY` | Taxon → Person | `year: int`, `publication: string` | Taxonomic authority |
| `ENDEMIC_TO` | Taxon → Place | `endemism_score: float`, `designation: string?` | Strict endemism (score > 0.90) |

### New Node Type: TaxonFamily

Intermediate graph node enabling family-level collection navigation:

```cypher
(:TaxonFamily {
  id:           string   // UUID
  family_name:  string   // e.g., "Trochilidae"
  order_name:   string   // e.g., "Apodiformes"
  kingdom:      string
  common_name:  string?  // e.g., "Hummingbirds"
  nc_io_count:  integer  // Derived
})
```

### Graph Build Order

Taxon nodes are built after Artist (Person) and before Expedition in the sync dependency order:

```
Bioregion → Institution → Period → Movement → Topic
→ Place → Artist → TaxonFamily → Taxon
→ Expedition → Illustration (IO) → Collection → Story → Product
```

**Taxon before IO** because IOs have DEPICTED_IN edges to Taxon, and the Taxon node must exist before the IO edge is written.

### Canonical Cypher Queries

**Q1: All IOs for a specific place (natural history)**
```cypher
MATCH (io:IllustrationOpportunity)-[:DEPICTED_IN]->(t:Taxon)
      -[:OCCURS_AT]->(p:Place {slug: $place_slug})
WHERE io.asset_tier = "Tier 1"
  AND io.rights_status = "ALLOWED"
RETURN io, t
ORDER BY io.quality_score DESC
LIMIT 50
```

**Q2: All places where this species has been illustrated**
```cypher
MATCH (io:IllustrationOpportunity)-[:DEPICTED_IN]->(t:Taxon {gbif_taxon_key: $key})
      (io)-[:ANCHORED_TO]->(p:Place)
RETURN io.title, p.name, p.slug, io.asset_tier
ORDER BY io.asset_tier, io.quality_score DESC
```

**Q3: Priority illustrator collection candidate (Trigger T1)**
```cypher
MATCH (artist:Person {ulan_id: $ulan_id})
      -[:CREATED]->(io:IllustrationOpportunity)
      -[:DEPICTED_IN]->(t:Taxon)
WHERE t.family = $family
  AND io.asset_tier = "Tier 1"
WITH artist, t.family AS family, count(io) AS io_count, collect(io) AS ios
WHERE io_count >= 3
RETURN artist.name, family, io_count
ORDER BY io_count DESC
```

**Q4: Designation endemic collection candidate (Trigger T3)**
```cypher
MATCH (t:Taxon)-[:ENDEMIC_TO]->(p:Place)
      -[:DESIGNATED_AS]->(d:Designation {type: "UNESCO_BIOSPHERE"})
      (io:IllustrationOpportunity)-[:DEPICTED_IN]->(t)
WHERE io.asset_tier IN ["Tier 1", "Tier 2"]
  AND t.endemism_score >= 0.80
WITH d.name AS designation, count(DISTINCT t) AS taxon_count, collect(DISTINCT io) AS ios
WHERE taxon_count >= 3
RETURN designation, taxon_count, size(ios) AS io_count
ORDER BY taxon_count DESC
```

**Q5: Co-occurrence discovery (related species at same place)**
```cypher
MATCH (t1:Taxon {gbif_taxon_key: $key})-[:OCCURS_AT]->(p:Place)
      <-[:OCCURS_AT]-(t2:Taxon)
WHERE t1 <> t2
  AND t1.kingdom = t2.kingdom
WITH t2, count(DISTINCT p) AS shared_places
ORDER BY shared_places DESC
LIMIT 10
RETURN t2.gbif_canonical_name, t2.gbif_vernacular_name, shared_places
```

**Q6: Family atlas candidate (Trigger T4)**
```cypher
MATCH (io:IllustrationOpportunity)-[:DEPICTED_IN]->(t:Taxon {family: $family})
      (io)-[:CREATED_BY]->(artist:Person)
WHERE io.asset_tier = "Tier 1"
WITH t.family, count(DISTINCT io) AS io_count, count(DISTINCT artist) AS artist_count
WHERE io_count >= 10 AND artist_count >= 2
RETURN t.family, io_count, artist_count
```

**Q7: Expedition natural history thread**
```cypher
MATCH (exp:Expedition {slug: $expedition_slug})
      -[:INCLUDED]->(io:IllustrationOpportunity)
      -[:DEPICTED_IN]->(t:Taxon)
      (io)-[:ANCHORED_TO]->(p:Place)
RETURN exp.name, io.title, t.gbif_canonical_name, t.gbif_vernacular_name,
       p.name, t.family
ORDER BY p.name, t.family
```

### Sync Architecture for Taxon Nodes

Following NC-GRAPH-002's trigger → queue → worker pattern:

```
PostgreSQL event:
  INSERT/UPDATE illustration_opportunities WHERE gbif_taxon_key IS NOT NULL
  → nc_graph_change_queue: {entity_type: "taxon", action: "upsert", gbif_taxon_key: X}

projection_worker:
  1. MERGE (:Taxon {gbif_taxon_key: X}) SET all properties
  2. MERGE (:TaxonFamily {family_name: T.family}) if not exists
  3. MERGE (t)-[:BELONGS_TO_FAMILY]->(f)
  4. For each place in gbif_occurrence_cache WHERE place_relevance_score > 0.50:
     MERGE (t)-[:OCCURS_AT {pac_class, score, occurrence_count_capped}]->(p)
  5. For each IO with DEPICTED_IN: MERGE (io)-[:DEPICTED_IN {is_primary}]->(t)
  6. Recalculate nc_io_count, nc_collection_count on affected nodes

Rights retraction (priority 1, <5 min SLA):
  If IO rights_status changes to BLOCKED:
    Remove DEPICTED_IN edges → taxon's nc_io_count decrements
    If taxon.nc_io_count = 0: mark taxon inactive in graph (do not delete)
```

---

## 8. Educational Pathways

### Four Educational Narratives

Every taxon in NC's graph can be contextualized through four parallel narratives, each mapped to an NC educational product tier:

**Narrative 1 — The Biological Story** (Who is this organism?)
```
Content: Scientific name + classification + ecological role + typical habitat
Format:  Species Context Card (EDU-0, free)
Source:  GBIF vernacular name + Wikipedia summary (AI-drafted, human-reviewed) + place context
Example: "Wild Turkey — Family Phasianidae. North America's largest game bird,
          observed from Florida to Maine. John James Audubon painted this plate
          from a live specimen he encountered in Louisiana in 1821."
```

**Narrative 2 — The Illustrator Story** (Who drew it and why?)
```
Content: Illustrator biography + how this species fit their larger project + place of observation
Format:  Illustrator Context Module (EDU-1, £12-18)
Source:  NC curator-authored text + ULAN authority record + BHL volume metadata
Example: "Audubon spent fifteen years documenting all known North American birds.
          The Wild Turkey was his Plate I — he chose it deliberately, as the turkey
          was the symbol of the new republic, and this was his opening statement."
```

**Narrative 3 — The Expedition Story** (How was it discovered?)
```
Content: Expedition timeline + places visited + scientific context of the discovery period
Format:  Expedition Module (EDU-2, £45-65)
Source:  BHL volume metadata + NC-GRAPH-002 Expedition nodes + curator text
Example: "Birds of America was the largest natural history publication ever attempted
          at the time of publication. Audubon's Mississippi River journey of 1820–21
          forms the foundation of Plates I through LVII..."
```

**Narrative 4 — The Taxonomy Story** (How was it classified?)
```
Content: Linnaean nomenclature history + original description + subsequent reclassifications
Format:  Research Edition (EDU-4, £350/yr or S3 Institutional subscription)
Source:  BHL-GBIF bridge + GBIF backbone history + Darwin Core export
Example: Full Darwin Core record + GBIF synonym history + BHL original description page.
         Suitable for university teaching and museum education programs.
```

### Educational Product Activation by Tier

| EDU Tier | Price | Taxon Requirement | Contents |
|---|---|---|---|
| EDU-0 | Free | gbif_vernacular_name + species context card copy | 1920px image + 3-sentence species context + illustrator attribution |
| EDU-1 | £12–18 per module | Complete IO (Tier 1 or 2) | Illustrator story + species card + place map + 3-question discussion prompt |
| EDU-2 | £45–65 per pack | 5+ IOs from same expedition or place | Expedition timeline + 5 species modules + teaching guide PDF |
| EDU-3 | £150/yr institutional | Institutional license | EDU-1 + EDU-2 + IIIF collection manifests + classroom toolkit |
| EDU-4 | £350/yr research | Darwin Core export | Full Darwin Core XML/JSON + IIIF + API access to NC taxonomic data |

### Curriculum Alignment

NC's educational taxonomy products align to:
- **UK National Curriculum**: KS3/KS4 Biology (classification + evolution + ecology)
- **IB Diploma Biology**: Topic 5 (Evolution and Biodiversity) — GBIF data + historical illustration
- **US NGSS**: LS4 (Biological Evolution) — paleontological + historical observation records
- **UNESCO ESD**: Education for Sustainable Development — biosphere + geopark place connections

The GBIF taxon key enables NC to link to external biodiversity databases, giving educators access to current occurrence data alongside historical illustrations. The combination is unique: GBIF provides the present; BHL provides the historical record; NC provides the bridge.

### AI-Assisted Educational Content Generation

Educational content is generated under NC-AI-001 governance:

```
PERMITTED (AI-drafted, human-reviewed):
  - Species context card body text (Narrative 1)
  - Discussion prompts for EDU-1 modules
  - Expedition summary text (Narrative 3)
  - Translation of educational copy (S3 multilingual)

PROHIBITED (human only, AI never writes):
  - Attribution strings (AI-ATT-1 permanent invariant)
  - Rights statements
  - Darwin Core field values
  - Scientific name determination
  - Illustrator identity claims
  - Any text implying NC endorsement by GBIF, BHL, NHM, or Smithsonian
```

---

## 9. Taxon Factory Pipeline

**Eight automated stages, two human gates:**

```
Stage 1: Name Extraction
  Input:  BHL page ID (or raw image + caption text)
  Method: BHL Names API (primary) → OCR-NER fallback
  Output: candidate_name, gbif_usage_key, bhl_name_confidence
  Gate:   Confidence < 0.70 → human review queue (Gate TF-A)

Stage 2: GBIF Backbone Resolution
  Input:  gbif_usage_key OR candidate_name
  Method: GBIF Species API → synonym resolution → accepted key
  Output: Full taxonomy record (kingdom through species)
  Gate:   taxonomicStatus = DOUBTFUL → human review queue

Stage 3: Taxon Node Upsert
  Input:  Resolved GBIF record
  Method: PostgreSQL INSERT OR UPDATE illustration_opportunities.gbif_taxon_key
          + graph MERGE (:Taxon)
  Output: Taxon node in Neo4j, Darwin Core JSON in PostgreSQL

Stage 4: GBIF Occurrence Validation
  Input:  gbif_taxon_key + NC place GeoNames IDs
  Method: GBIF Occurrence API (occurrence_count per place bounding box)
          → gbif_occurrence_count_capped = min(count, 100)
  Output: Candidate place-taxon edges with occurrence counts
  Constraint: Raw occurrence count NEVER used in any scoring (CI Constitution)

Stage 5: Place Relevance Scoring
  Input:  PAC class + endemism + illustrator location + occurrence count capped
  Method: place_relevance_score formula (§2)
  Output: Ranked candidate place associations
  Gate:   PAC-4 or PAC-5 association → human gate required (Gate TF-B)

Stage 6: Graph Edge Write
  Input:  Confirmed place-taxon associations (PAC-1 through PAC-3)
  Method: Neo4j MERGE (t)-[:OCCURS_AT]->(p) with score properties
          MERGE (io)-[:DEPICTED_IN]->(t)
  Output: Graph edges committed; nc_io_count incremented

Stage 7: Collection Routing
  Input:  Updated taxon counts per illustrator/place/family/designation
  Method: Evaluate T1–T4 triggers (§3)
  Output: Collection candidates → curator queue (if threshold crossed)

Stage 8: Product Routing
  Input:  IO Completeness Test (§4)
  Method: Check all five IO fields; assign asset_tier
  Output: If Tier 1: product record created → curator review queue
          If Tier 2: editorial record; no product until human upgrades
          If Tier 3/4: discovery record only
```

**Gate TF-A** (Name confidence < 0.70): Curator confirms species identity from illustration context. Opens REVIEW workflow item. 30-day resolution SLA.

**Gate TF-B** (PAC-4/5 place association): Curator confirms place anchor from editorial knowledge. Opens REVIEW workflow item. Required before any product routing from that IO.

---

## 10. Governance Invariants

| # | Invariant |
|---|---|
| TF-1 | Every taxon in NC has a GBIF taxon key. No taxon node may exist in the graph without `gbif_taxon_key`. |
| TF-2 | GBIF occurrence count is capped at 100 in all scoring formulas. The raw occurrence count may never be used in any scoring formula, ranking, or display. (CI Constitution · DD-GBIF-001 I-3) |
| TF-3 | GBIF media is permanently prohibited. The BHL-GBIF bridge provides taxon keys, not images. (DD-GBIF-001 I-5) |
| TF-4 | A Taxon node does not authorize product creation. Only a complete IO (all five fields confirmed) routes to product. |
| TF-5 | Synonyms are always resolved to the accepted GBIF name before any product copy is written. The synonym key is stored for provenance only. |
| TF-6 | GBIF backbone version is recorded with every resolution. Annual backbone review is required. Backbone updates that change existing IO taxon keys require human gate review before product copy updates. |
| TF-7 | PAC-4 (range intersection) and PAC-5 (editorial) place associations require a human gate before any product is created from that IO. These classes alone are never sufficient for CE products. |
| TF-8 | Darwin Core fields are retrieved from the authoritative source (GBIF, BHL, ULAN, GeoNames). AI may draft surrounding educational copy; AI may never write Darwin Core field values. (AI-ATT-1) |
| TF-9 | Conservation status (IUCN Red List) is not a product selling point. It is not surfaced in product copy, titles, or marketing materials. |
| TF-10 | The REVIEW_REQUIRED queue for taxon resolution has a 30-day maximum age. Unresolved items after 30 days are escalated to curator review or downgraded to Tier 3. |
| TF-11 | Taxon nodes with `nc_io_count = 0` are retained in the graph (not deleted) but marked inactive. Rights retraction that reduces nc_io_count to 0 does not delete the node. (CI-9 deduplication protocol) |
| TF-12 | Darwin Core XML/JSON export is an institutional product (EDU-4/S3). It is not a free public endpoint. Export is gated behind the S3 Institutional subscription or EDU-4 license. |

---

## 11. Open Actions

| # | Action | Priority | Depends On |
|---|---|---|---|
| OA-1 | Extend M36 schema: add `darwin_core_json` JSONB column to `illustration_opportunities` | HIGH | NC-ASSETS-1000000 M36 migration |
| OA-2 | Implement BHL Names API → GBIF resolution module (Stage 1–2 pipeline) | HIGH | SA-BHL-001 + DD-BHL-001 ratified |
| OA-3 | Add TaxonFamily node type to Neo4j schema (NC-GRAPH-002 Amendment) | HIGH | NC-GRAPH-002 ratification |
| OA-4 | Implement OCCURS_AT edge writer (Stage 6) with PAC class scoring | HIGH | OA-2 + OA-3 |
| OA-5 | Implement collection generation trigger checks (T1–T4) as cron job | MEDIUM | OA-4 + NC-GRAPH-002 live |
| OA-6 | Build Darwin Core XML/JSON serializer | MEDIUM | OA-1 |
| OA-7 | Darwin Core `nc:` extension namespace registration at `nc.art/data/terms/` | MEDIUM | — |
| OA-8 | Curator review queue UI for Gate TF-A and TF-B items | MEDIUM | — |
| OA-9 | Educational copy generation pipeline (AI-drafted, human-reviewed per NC-AI-001) | MEDIUM | NC-AI-001 ratified |
| OA-10 | GBIF backbone version sync and annual review procedure | LOW | OA-2 |
| OA-11 | IUCN Red List cross-reference (supplementary educational context only; never product copy) | LOW | — |
| OA-12 | Darwin Core export API for S3 Institutional subscription | LOW | OA-6 + NC-COMMERCE-2000 S3 tier |

---

*NC-TAXON-001 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
*Priority ratification dependencies: NC-GRAPH-002 · DD-BHL-001 · SA-BHL-001 · SA-BHL-002 · DD-GBIF-001 · SA-GBIF-001*
