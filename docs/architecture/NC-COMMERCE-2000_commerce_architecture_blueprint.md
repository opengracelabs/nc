# NC-COMMERCE-2000: Commerce Architecture Blueprint

| Field | Value |
|---|---|
| Document | NC-COMMERCE-2000 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | NC-PRODUCT-001 · NC-PLACES-1000 · NC-PLACES-2000 · NC-ICH-001 · NC-TRUST-003 · Illustration Opportunity Doctrine |
| Scope | Commerce architecture for Nature & Culture at 2,000 places. Extends NC-PRODUCT-001 (product lines) and NC-PLACES-2000 (place expansion roadmap) into a unified commerce system. |
| Reference Models | Rijksmuseum Shop · Smithsonian Store · British Museum Shop · National Geographic Store · Getty Store · Gelato · Printful |
| Standards Applied | CIDOC CRM · Darwin Core · IIIF Presentation 3.0 + Image 3.0 · Schema.org · RightsStatements.org |

---

## Governing Doctrine

Before any architecture, the doctrine. These constraints govern everything else in this document.

**1. The commercial object is an Illustration Opportunity, not a place.**
At 2,000 places, the temptation is to treat the place as the commercial anchor. The doctrine says otherwise: the place is the discovery architecture; the Illustration Opportunity is the commercial object. Earthrise is sold because William Anders made a photograph on December 24, 1968 — not because Apollo 8 orbited the Moon.

**2. Golden age priority: 1750–1900.**
The core illustration pool is the Golden Age of natural history and architectural illustration. Audubon, Haeckel, Redouté, Gould, Jones, Roberts, Merian, Nodder, Lear, Wolf. Later material is eligible where it meets PD/CC0 criteria, but product curation defaults to the Golden Age.

**3. PD/CC0 hard gate is unconditional.**
IFC-1 is a constitutional invariant. InC, CC BY-NC, and all non-commercial restriction classes are permanently blocked regardless of the quality or commercial potential of the work. No exception path exists.

**4. Designation stack drives commerce priority, not taxonomy.**
A place with WH + Biosphere + ICH + Ramsar (designation stack ≥ 4) is commercially prioritised over a more famous place with no designations. Designations anchor illustration relevance and educational value.

**5. NC is the activated commercial layer.**
Rijksmuseum, Smithsonian, NatGeo, Getty each decline to be NC. Rijksmuseum makes the collection; NC sells it. NatGeo makes the story; NC sells the illustration behind it. Getty runs the provenance research; NC sells the print. NC is not a museum. It is the layer of commerce those museums explicitly chose not to build.

---

## Part I — Collection Architecture at 2,000 Places

### 1.1 Scale Parameters

| Metric | Pilot (now) | Target |
|---|---|---|
| Active places | 7 | 2,000 |
| Commerce-tier places | 5 | ~700 (35%) |
| Illustration Opportunities in database | ~20 | ~15,000 |
| Active product SKUs | 2 | ~40,000 |
| Signed Collector Editions | 2 | ~2,100 |
| Digital editions | 2 | ~15,000 |
| Estimated active collections | 6 | ~1,400 |

At 2,000 places, not all reach commerce tier. The publishing tier hierarchy governs:
- **SEED:** Place exists in graph. No editorial content. Not visible.
- **STUB:** Place page live. Minimal content. No illustrations. Discovery only.
- **ILLUSTRATED:** Illustrations loaded. Editorial copy active. No products yet.
- **COMMERCE:** Products live. Minimum 3 Illustration Opportunities confirmed.
- **PREMIUM:** Full collection. Signature product. CE available. IIIF manifest published.

### 1.2 Collection Taxonomy

Ten collection families, mapped to designation drivers and illustration pools.

| # | Collection Family | Primary Designations | Golden Age Source | Illustration Type | Commerce Priority |
|---|---|---|---|---|---|
| 1 | Wilderness | Biosphere + MPA + Ramsar | Gould, Audubon, Haeckel, Hooker | Natural history plate | Tier 1 |
| 2 | Sacred Geography | WH + ICH | Roberts, Prout, Lear, Müller | Topographical engraving | Tier 1 |
| 3 | Lost Civilisations | WH + Geopark | Catherwood, Prisse d'Avennes, Lane | Archaeological drawing | Tier 1 |
| 4 | Imperial Gardens | WH + ICH | Redouté, Basilius Besler, Ehret | Botanical illustration | Tier 1 |
| 5 | Expedition Frontiers | Biosphere + Geopark | Wilson, Hooker, Parkinson, Nodder | Field watercolour | Tier 1 |
| 6 | Urban Heritage | WH + ICH | Jones, Prout, Girault de Prangey | Architectural drawing | Tier 1 |
| 7 | Seascape | MPA + Biosphere | Haeckel, Müller, Gray | Marine plate | Tier 2 |
| 8 | Mountain | WH + Biosphere + Geopark | Hooker, Marianne North | Botanical / geological | Tier 2 |
| 9 | River | Ramsar + Biosphere | Catlin, Bodmer, Church | Expedition landscape | Tier 2 |
| 10 | ICH | ICH (element type TC only) | Documentary illustration | Cultural documentary | Tier 2 |

**ICH commerce rule (from NC-ICH-001):** ICH element type TC (Traditional Craftsmanship) is the only ICH domain with a direct documentary illustration commerce path. Performing Arts and Oral Traditions generate editorial context but not primary commercial products. Practice is never the product; only the PD documentary illustration is.

### 1.3 Designation-Commerce Activation Matrix

Designations are the discovery and editorial layer; illustrations are the commercial layer. The matrix defines which designation combination unlocks which product families.

| Designation Present | Unlocks |
|---|---|
| UNESCO World Heritage | Core product lines 1–16, 19–20; Place Portfolio (line 7); Map Print (line 5) |
| UNESCO Biosphere Reserve | Natural history product families; Botanical print line; Educational ecology packs |
| UNESCO Geopark | Geological illustration line; Expedition print sets; Geo-tourism educational packs |
| Ramsar Wetland | Ornithological illustration line; Wetland ecology educational packs |
| ICH (element type TC) | Cultural documentary print line; Textile pattern-inspired products |
| Dark Sky | Astronomical illustration line; Celestial map prints; Night ecology educational packs |
| Marine Protected Area | Marine illustration line; Haeckel/Müller plate sets |
| Designation stack ≥ 3 | Priority for CE allocation; PREMIUM tier publishing |
| Designation stack ≥ 4 | Eligible for Signature Collection status; Institutional licensing priority |

### 1.4 Machine-Readable Collection Schema

Each collection has two schema layers:

**Heritage layer (CIDOC CRM):**

```json
{
  "@context": "http://www.cidoc-crm.org/cidoc-crm/",
  "@type": "crm:E78_Curated_Holding",
  "crm:P1_is_identified_by": {
    "@type": "crm:E42_Identifier",
    "crm:P190_has_symbolic_content": "NC-COL-001"
  },
  "crm:P46_is_composed_of": [
    {
      "@type": "crm:E22_Human-Made_Object",
      "crm:P102_has_title": "Court of the Lions",
      "crm:P108i_was_produced_by": {
        "@type": "crm:E12_Production",
        "crm:P14_carried_out_by": {
          "@type": "crm:E21_Person",
          "crm:P1_is_identified_by": {"ulan": "500010851"},
          "rdfs:label": "Owen Jones"
        },
        "crm:P4_has_time-span": {
          "crm:P82a_begin_of_the_begin": "1834",
          "crm:P82b_end_of_the_end": "1845"
        }
      },
      "crm:P50_has_current_keeper": {
        "@type": "crm:E74_Group",
        "crm:P1_is_identified_by": {"ror": "https://ror.org/051z9gg54"},
        "rdfs:label": "Walters Art Museum"
      },
      "crm:P104_is_subject_to": {
        "@type": "crm:E30_Right",
        "schema:license": "http://creativecommons.org/publicdomain/mark/1.0/"
      }
    }
  ]
}
```

**Commerce layer (Schema.org):**

```json
{
  "@context": "https://schema.org",
  "@type": "Collection",
  "name": "Alhambra: The Geometry Collection",
  "url": "https://nc.art/collections/alhambra",
  "description": "...",
  "provider": {
    "@type": "Organization",
    "name": "Nature & Culture",
    "url": "https://nc.art"
  },
  "about": {
    "@type": "Place",
    "name": "Alhambra",
    "identifier": "https://sws.geonames.org/2521674/",
    "geo": {"@type": "GeoCoordinates", "latitude": 37.176, "longitude": -3.588}
  },
  "license": "http://creativecommons.org/publicdomain/mark/1.0/",
  "creditText": "Owen Jones / Walters Art Museum (CC0)",
  "hasPart": [{"@type": "Product", "url": "https://nc.art/products/alhambra-court-of-lions-print"}]
}
```

**Natural history layer (Darwin Core):** Applied where the Illustration Opportunity depicts a taxon.

```json
{
  "dcterms:type": "StillImage",
  "dwc:basisOfRecord": "HumanObservation",
  "dwc:institutionCode": "NHM",
  "dwc:collectionCode": "Endeavour-Botanical",
  "dwc:recordedBy": "Sydney Parkinson",
  "dwc:scientificName": "Strelitzia reginae",
  "dwc:vernacularName": "Bird-of-paradise flower",
  "dwc:locality": "South Africa",
  "gbif:taxonKey": "3189866",
  "dwc:year": "1769",
  "dcterms:rights": "http://creativecommons.org/publicdomain/zero/1.0/",
  "dcterms:rightsHolder": "Natural History Museum London"
}
```

---

## Part II — Product Architecture

### 2.1 Product Taxonomy Extension

NC-PRODUCT-001 defines 18 approved product lines (20 total, 2 reserved). NC-COMMERCE-2000 adds structure: the product taxonomy is organised into eight product families that map to fulfillment method, governance tier, and target customer.

| Family | Lines from NC-PRODUCT-001 | New at 2,000 places | Fulfillment |
|---|---|---|---|
| **A: Museum Print** | 1, 6, 20 | Signature prints (Tier 3) | Specialist studio (Loxley, Bay Photo) |
| **B: Wall Art** | 2, 3, 4, 5 | Map prints (expanded) | Gelato primary |
| **C: Educational** | 9, 10, 12 | Curriculum packs; Place trail cards | Digital + Gelato |
| **D: Books & Guides** | 11, 13 | Field guide series | Print-on-demand book specialist |
| **E: Paper Goods** | 14, 15, 16, 19 | Designation series postcards | Gelato |
| **F: Digital** | 8 | IIIF download tier; Research license | Digital delivery |
| **G: Collector** | 1 (CE variants), 20 | CE print + COA bundle | Specialist studio + NC direct |
| **H: Subscription** | *(new — see Part VIII)* | Explorer / Collector / Institutional | Mixed |

### 2.2 Illustration Opportunity–Product Compatibility Matrix

Not every IO generates every product type. Compatibility is governed by three factors:
- **Resolution class** (R1/R2/R3): see NC-PRODUCT-001 Article 13
- **Subject class** (natural history / architectural / cartographic / documentary)
- **Designation class** (which designation stack anchors the place)

| Product Line | R1 (4K+) | R2 (2K+) | R3 (1K+) | Natural History | Architectural | Cartographic | Documentary |
|---|---|---|---|---|---|---|---|
| 1 Museum giclee | ✓ | — | — | ✓ | ✓ | — | — |
| 2 Framed print | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| 3 Poster | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 4 Canvas | ✓ | ✓ | — | ✓ | ✓ | — | ✓ |
| 5 Map print | ✓ | ✓ | ✓ | — | — | ✓ | — |
| 6 Archival plate set | ✓ | — | — | ✓ | ✓ | — | — |
| 7 Place portfolio | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| 8 Digital download | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 9 PDF guide | — | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| 10 Education pack | — | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| 11 Tourism guide | — | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| 13 Coffee-table book | ✓ | — | — | ✓ | ✓ | — | — |
| 14 Calendar | ✓ | ✓ | — | ✓ | ✓ | — | — |
| 15 Postcard/card | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 16 Sticker | — | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| 19 Notebook | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 20 Collector bundle | ✓ | — | — | ✓ | ✓ | — | — |

### 2.3 Designation-Specific Product Series

Each designation family has a named product series. These are marketing families, not separate product lines; they use the existing 18 approved lines with designation-specific curation and naming.

| Series Name | Designation Driver | Signature SKU | Educational Anchor |
|---|---|---|---|
| **World Heritage Series** | UNESCO WH | Archival plate set from primary illustrator | WH Discovery Pack |
| **Living Biosphere Series** | UNESCO Biosphere | Natural history giclee (Audubon / Gould) | Field Ecology Pack |
| **Geopark Expedition Series** | UNESCO Geopark | Expedition field watercolour | Geological Survey Educational Pack |
| **Wetland & Bird Series** | Ramsar | Ornithological plate (Audubon / Gould / Lear) | Wetland Ecology Classroom Pack |
| **Craft Heritage Series** | ICH (TC element) | Documentary print + textile pattern card | ICH Context Guide |
| **Dark Sky Series** | Dark Sky | Celestial map / astronomical illustration | Star Chart Educational Pack |
| **Ocean Atlas Series** | MPA | Marine plate (Haeckel / Hooker) | Marine Biodiversity Educational Pack |

---

## Part III — POD Architecture

### 3.1 Vendor Role Assignment

At 2,000 places, production localization is the primary efficiency lever. Carbon cost and delivery time both depend on producing near the customer.

| Vendor | Role | Product Families | Production Regions |
|---|---|---|---|
| **Gelato** | Primary POD | B (Wall Art), C (Educational print), E (Paper Goods) | Global (32+ countries) — route to nearest facility |
| **Printful** | Secondary POD + apparel reserve | B (overflow), Apparel (when line 17/18 activate) | Americas, EU, APAC |
| **Specialist studio** (Loxley / Bay Photo / Whitewall) | Museum-quality print | A (Museum Print) — lines 1, 6, 20 | Per-region designated studio |
| **POD book specialist** (Mixam / Blurb) | Books | D (Books & Guides) — lines 11, 13 | Per-region routing |
| **NC direct** (in-house) | CE fulfillment | G (Collector) — CE bundle with COA | NC ships direct from designated inventory |

### 3.2 Production Routing Logic

```
ORDER RECEIVED
    ↓
product_family = ?
    ├── Family A (Museum Print / CE)
    │       → specialist_studio_routing(customer_region)
    │       → NC sends COA separately (tracked)
    │
    ├── Family B/C/E (Wall Art / Educational / Paper)
    │       → gelato_api.create_order(sku, ship_to)
    │       → gelato routes to nearest production facility
    │       → fallback to printful if gelato SKU unavailable
    │
    ├── Family D (Books)
    │       → book_pod_routing(customer_region)
    │
    ├── Family F (Digital)
    │       → digital_delivery.issue_download_token(nc_ers_edition_id)
    │
    └── Family G (Collector CE)
            → nc_inventory_check(edition_id)
            → if in_stock: nc_direct_fulfillment
            → else: waitlist + curator_notification
```

### 3.3 Quality Tiers

| Tier | Applies to | Specification | Governed by |
|---|---|---|---|
| **Q1 Museum** | Line 1, 6, 20 | 300 DPI minimum at final size; archival ink set (pigment-based, ISO 11798); acid-free cotton rag substrate | NC-PRODUCT-001 Art. 13; NC-COAS §ISO |
| **Q2 Premium** | Line 2, 4, 7 | 300 DPI at final size; archival ink; acid-free substrate preferred | NC-PRODUCT-001 Art. 13 |
| **Q3 Standard** | Lines 3, 5, 14–16, 19 | 150 DPI minimum at final size; standard POD ink and substrate | Gelato/Printful default spec |
| **Q4 Digital** | Line 8; DD products | IIIF Image API Level 2 compliance; sRGB; max 6000px long edge for standard; original IIIF for research tier | NC-EDRS; NC-ERS |

### 3.4 Image Delivery Pipeline

```
Source IIIF endpoint (NHM / NGA / Walters / CMA / Met / etc.)
    ↓
NC image processor (validate rights + resolution)
    ↓
NC asset store (canonical master file)
    ├── Product file prep (crop, profile, color-correct for product spec)
    │       → POD upload (Gelato Product Hub / Printful API)
    │
    ├── IIIF manifest generation (NC-hosted)
    │       → Public manifest at nc.art/iiif/[collection]/manifest.json
    │
    └── Digital download package (NC-ERS edition ID + metadata + XMP)
            → Watermarked preview
            → Full-resolution on purchase
```

### 3.5 IIIF Manifest Standard

Every PREMIUM-tier collection publishes a IIIF Presentation 3.0 manifest. Required fields per item:

```json
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
  "id": "https://nc.art/iiif/collections/{slug}/manifest.json",
  "type": "Manifest",
  "label": {"en": ["{Collection title}"]},
  "metadata": [
    {"label": {"en": ["Curator"]}, "value": {"en": ["Nathan Holderhead, Founding Curator"]}},
    {"label": {"en": ["Rights"]}, "value": {"en": ["{RightsStatements.org URI}"]}},
    {"label": {"en": ["Source Institution"]}, "value": {"en": ["{institution name}"]}},
    {"label": {"en": ["Source Identifier"]}, "value": {"en": ["{source_id}"]}},
    {"label": {"en": ["Illustrator"]}, "value": {"en": ["{illustrator name} (ULAN {id})"]}},
    {"label": {"en": ["Date"]}, "value": {"en": ["{year or range}"]}}
  ],
  "rights": "{RightsStatements.org URI}",
  "requiredStatement": {
    "label": {"en": ["Attribution"]},
    "value": {"en": ["{full attribution string}"]}
  },
  "items": [...]
}
```

---

## Part IV — Educational Products

### 4.1 Governing Principle

Educational products at NC operate on the NC-EDRS (Educational Reuse Standard) no-friction principle: the baseline educational product is always free. Paid educational products add curriculum depth, not access.

| Tier | Product | Price | Governed by |
|---|---|---|---|
| **EDU-0 Free** | Single illustration download (1920px, 150dpi) + one-page context card | Free | NC-EDRS §2 |
| **EDU-1 Classroom** | Six-illustration place pack + teacher guide + 10 source-literacy activities | £12–£18 | NC-EDRS §4 |
| **EDU-2 Curriculum** | Full collection + curriculum alignment (KS2–KS5 or grade equivalents) + assessment guides | £45–£65 | NC-EDRS §5 |
| **EDU-3 Institutional** | Annual educator licence: all collections, all free tiers, curriculum packs, IIIF classroom viewer | £150/year per institution | NC-ITS |
| **EDU-4 Research** | IIIF manifest access + Darwin Core metadata export + full-resolution originals | £350/year | NC-ITS research tier |

### 4.2 Context Guide Format (per NC-EDRS §6)

Every educational product includes a six-section context guide:

1. **The Illustration** — what is depicted, by whom, when
2. **The Illustrator** — biography (100 words), context, significance
3. **The Place** — GeoNames anchor, designation stack, current conservation status
4. **The Science / Craft** — what the work documents scientifically or culturally
5. **Source and Rights** — full NC-PDPS provenance chain, RightsStatements.org URI
6. **Teaching Activities** — 3–5 classroom activities with age range

### 4.3 Designation-Specific Educational Product Lines

| Educational Series | Designation Driver | Core Content | Target Audience |
|---|---|---|---|
| **WH Explorer Packs** | UNESCO WH | Architecture + archaeology + cultural landscape | Secondary (age 12–18) |
| **Living World Packs** | Biosphere + Ramsar | Natural history illustration + ecology | Primary + Secondary |
| **Earth History Packs** | Geopark | Geological illustration + expedition history | Secondary + tertiary |
| **Night Sky Packs** | Dark Sky | Astronomical illustration + celestial mechanics | Secondary |
| **Cultural Heritage Packs** | ICH (TC) | Documentary illustration of traditional craftsmanship | Secondary + tertiary |
| **Ocean Packs** | MPA | Marine illustration + biodiversity | Primary + Secondary |

### 4.4 Curriculum Alignment Standards

Educational products are aligned to:
- UK National Curriculum (KS2, KS3, KS4)
- US Common Core / Next Generation Science Standards (NGSS)
- IB Curriculum Programme (Primary Years, Middle Years, Diploma)
- UNESCO ESD (Education for Sustainable Development) framework

Alignment metadata is embedded in product descriptions and available as structured JSON at `/api/products/[sku]/curriculum`.

---

## Part V — Collector Products

### 5.1 Architecture

The Collector product family is NC's highest-trust, highest-value tier. Every collector product is governed by NC-COAS (Certificate of Authenticity Standard) and NC-ERS (Edition Registry Standard).

**Product types:**

| Product | Abbreviation | Edition type | Max run | Numbering | COA |
|---|---|---|---|---|---|
| **Collector's Edition Print** | CE | Fixed count | 100 | Pencil, lower margin | Yes, physical |
| **Signature Collection Set** | SCS | Fixed count | 25 | Pencil + curator initial | Yes, physical + digital |
| **Founding Edition Print** | FE | Fixed count, one per collection | 50 | Pencil, lower margin | Yes, physical |
| **Open Edition Archival Print** | OE | Unlimited | — | — | Digital only |
| **Premium Collector Bundle** | PCB | Fixed count (bundle) | 10 | Full suite | Yes, physical |

**Edition governance:** All CE, SCS, FE, and PCB editions require two-person ratification at Gate E before the first print is made. Edition size is locked at ratification and cannot change. NC-ERS closure procedure applies upon sell-out.

### 5.2 Physical Mark Specification

Per NC-TRUST-003 (NC-ERS §V): pencil edition number in lower margin, format `[n]/[total]`, curator initials adjacent. Medium: acid-free graphite HB or 2H (Senefelder convention). Physical mark does not appear on digital or open editions.

### 5.3 Certificate of Authenticity (NC-COAS compliant)

Required fields on every CE, SCS, FE, and PCB certificate:

| Field | Content |
|---|---|
| Certificate ID | `NC-[COL]-[PROD]-[NNN]-[YYYY]` |
| Work title | Illustration title |
| Illustrator | Full name, ULAN ID |
| Date of original | Year or range |
| Source institution | Name, ROR ID |
| Source identifier | Institution's object/image ID |
| Rights statement | RightsStatements.org URI + full statutory language |
| Rights statutory basis | Full legal text (e.g., "17 U.S.C. § 105: a work of the US Government is not subject to copyright protection") |
| Edition size | Locked number |
| Edition number | This copy's number |
| Print specification | Substrate, ink, dimensions, DPI |
| ISO conservation | ISO 11798 (ink permanence) + ISO 9706 (paper permanence) |
| Curator signatory | Name, title, date, signature line |
| Permanence commitment | Internet Archive transfer within 90 days of cessation |
| Verification URL | `https://nc.art/verify/[certificate_id]` |

### 5.4 Collector Edition Allocation at Scale

At 2,000 places, CE allocation is constrained by curator capacity. Governance rule:

- Maximum 3 active CE editions open simultaneously per curator
- New CE requires Gate E ratification before announcement
- Waitlist accepted before Gate E; no payment taken until Gate E confirmed
- CE editions for Signature Collections (NC-SIGNATURE-001 tier) have priority

---

## Part VI — Institutional Products

### 6.1 Institutional Tier Architecture

NC-ITS (Institutional Transparency Standard) defines three institutional tiers. Commerce products map to each tier differently.

| Tier | Who | NC product access | License type | Price model |
|---|---|---|---|---|
| **CC0 Partner** | Source institution that provided the work as CC0 | Attribution + co-presentation | Attribution agreement, no fee | Reciprocal |
| **PD Source** | Institutional client licensing NC's editorial + commerce layer | Product white-label; NC product catalog under client brand | Annual institutional license | £2,500–£15,000/year depending on product lines |
| **Aggregator / Edu** | Schools, universities, libraries, heritage bodies | Educational product catalog; IIIF viewer; curriculum packs | Annual institutional license | £150–£500/year |

### 6.2 Institutional License Products

| Product | Target | Content | Price |
|---|---|---|---|
| **Place Collection License** | Museum / heritage body | Full IIIF manifest access + Darwin Core export + commerce use permissions for one collection | £2,500/year |
| **Domain License** | University / research | IIIF access across one collection family (e.g., all natural history collections) | £5,000/year |
| **Full Catalog License** | Major institutional partner | All published collections, all formats, full IIIF + Darwin Core | £15,000/year |
| **Educator Annual License** | School / university department | All EDU-0/EDU-1/EDU-2 products; IIIF classroom viewer | £150/year |
| **Research Annual License** | Academic researcher | IIIF manifest + full-resolution originals + Darwin Core exports | £350/year |

### 6.3 White-Label Institutional Products

At PREMIUM tier, NC can offer white-label collection products to partner institutions:

- Institution-branded art prints from NC collections (source institution receives attribution; NC handles fulfillment)
- Co-branded educational packs (institution's name on NC's curriculum pack)
- IIIF viewer embed (institution embeds NC's IIIF viewer in their own web presence)

Governance rule: white-label requires PD Source agreement (Tier 2), naming of the curator of record, and NC attribution on all products.

---

## Part VII — Digital Products

### 7.1 Digital Product Tiers

| Product | Edition type | Format | Resolution | Price range | NC-ERS registration |
|---|---|---|---|---|---|
| **Digital Study Edition** (DDS) | Open Edition | TIFF/JPEG + XMP metadata | 3000px long edge | £15–£25 | Yes, `editionType: "digital_open"` |
| **Digital Research Edition** (DDR) | Open Edition | Full-resolution master + Darwin Core export | Source resolution | £45–£95 | Yes, `editionType: "digital_research"` |
| **Digital Collector Edition** (DDC) | Fixed count (100) | Full-resolution + certificate + provenance JSON | Source resolution | £95–£195 | Yes, `editionType: "digital_collector"` |
| **IIIF Access License** | Per-manifest | IIIF Presentation 3.0 manifest + Image API access | Level 2 | £45/collection/year | No — licensed access |

### 7.2 Digital Delivery Specification

Per NC-EDRS and NC-ERS:

**Download package contents (all digital editions):**
- Master image file (TIFF preferred; JPEG fallback)
- XMP sidecar file with full provenance metadata
- NC provenance JSON (NC-PDPS compliant 6-link chain)
- Attribution text file (plain text, markdown, HTML variants)
- Rights statement file referencing RightsStatements.org URI
- Context card PDF (1 page, educational summary)

**XMP metadata template:**
```xml
<rdf:RDF>
  <rdf:Description rdf:about="">
    <dc:title>Court of the Lions, Alhambra</dc:title>
    <dc:creator>Owen Jones (ULAN 500010851)</dc:creator>
    <dc:date>1842</dc:date>
    <dc:rights>Public Domain Mark 1.0</dc:rights>
    <xmpRights:UsageTerms>No rights reserved — public domain</xmpRights:UsageTerms>
    <xmpRights:WebStatement>http://creativecommons.org/publicdomain/mark/1.0/</xmpRights:WebStatement>
    <nc:sourceInstitution>Walters Art Museum</nc:sourceInstitution>
    <nc:sourceIdentifier>W.650</nc:sourceIdentifier>
    <nc:curator>Nathan Holderhead, Founding Curator</nc:curator>
    <nc:certificateId>NC-COL001-PROD006-001-2026</nc:certificateId>
    <nc:verifyUrl>https://nc.art/verify/NC-COL001-PROD006-001-2026</nc:verifyUrl>
  </rdf:Description>
</rdf:RDF>
```

### 7.3 RightsStatements.org URI Mapping

All digital products display a RightsStatements.org URI. Mapping by rights class:

| Rights Class | Statute / Grant | RightsStatements.org URI |
|---|---|---|
| Class 1: § 105 (NASA/NOAA/NARA) | 17 U.S.C. § 105 | `http://rightsstatements.org/vocab/NoC-US/1.0/` |
| Class 2: CC0 | CC0 1.0 grant | `http://creativecommons.org/publicdomain/zero/1.0/` |
| Class 3: PDM | Public Domain Mark | `http://creativecommons.org/publicdomain/mark/1.0/` |
| Class 3B: NoC-US | Life + 100+ years, US-published | `http://rightsstatements.org/vocab/NoC-US/1.0/` |
| Class 8: Dataset-level CC | CC BY (data layer only, no image) | Not applicable to product (rights class inherited from underlying PD image) |

---

## Part VIII — Subscription Products

### 8.1 Rationale

Subscriptions are new at NC. Reference models:
- **NatGeo:** Subscription as the flagship product — the magazine anchors everything
- **Rijks Studio:** Annual access to high-resolution downloads — recurring revenue from the collection
- **Getty Images:** Research licensing as a subscription tier
- **Patagonia:** Mission-aligned subscriber identity (customers subscribe to the values, not just the product)

NC's subscription is anchored in the collection, not in content delivery. The subscriber gets privileged access to the edition system — early CE pre-registration, exclusive digital editions, educational priority — not a generic content feed.

### 8.2 Subscription Tier Design

| Tier | Name | Price | Core benefits |
|---|---|---|---|
| **S1** | Explorer | £75/year | Monthly digital download (DDS tier); early access to new collections; 10% discount on all products; access to /educators free tier for personal use |
| **S2** | Collector | £195/year | All S1 benefits; CE pre-registration priority (30-day window before public); one DDS download per new collection at launch; 15% discount on all products; annual printed provenance card for CE holdings |
| **S3** | Institutional | £495/year | All S2 benefits; full EDU-3 educator licence; IIIF access to all published collections; Darwin Core metadata export; white-label classroom viewer; named on annual disclosure report as institutional subscriber |

### 8.3 Subscription Fulfillment Model

| Component | Delivery | Frequency |
|---|---|---|
| Monthly digital download (S1+) | Automated: NC-ERS digital edition token | Monthly on billing date |
| CE pre-registration window (S2+) | Email + account notification 30 days before public CE launch | Per-CE |
| Educator licence activation (S3) | Account feature flag; access to `/educators` premium tier | Annual |
| IIIF manifest access (S3) | API key; access to `nc.art/iiif/` manifest endpoints | Annual |
| Annual provenance card (S2+) | Physical card, posted, for each CE held by subscriber | Annual |
| Annual disclosure report (S3) | Named in report (if consented); PDF emailed | Annual |

### 8.4 CE Pre-Registration Model

S2/S3 subscribers receive a 30-day exclusive window to register for upcoming CE editions before the public launch. Pre-registration is non-binding; payment is taken only after Gate E confirms the edition.

Pre-registration governance:
- Maximum 3 active CE pre-registrations per subscriber at any time
- Subscriber list is not published; collector privacy is maintained
- If a CE edition is cancelled before Gate E, pre-registrations are voided with notification

### 8.5 Subscription and the Edition Registry

Subscriber-held editions are listed in the NC-ERS registry under the subscriber's edition number. The public registry record shows the edition number but not the subscriber's identity.

---

## Part IX — Standards Integration

### 9.1 CIDOC CRM Application

CIDOC CRM (the ICOM standard for cultural heritage information) governs NC's heritage data model. It applies at the Illustration Opportunity layer, not the product layer.

**Primary entity types used:**

| CRM Entity | NC Use |
|---|---|
| E22 Human-Made Object | The original illustration (physical artefact in source institution) |
| E12 Production | The production event (illustrator + date) |
| E21 Person | The illustrator (ULAN identifier as P1_is_identified_by) |
| E78 Curated Holding | The NC collection |
| E74 Group | The source institution (ROR ID) |
| E30 Right | The rights status (RightsStatements.org URI) |
| E52 Time-Span | Date of creation (golden age precision: year or range) |
| E53 Place | The place depicted (GeoNames ID as canonical identifier) |
| E36 Visual Item | The digital image (IIIF endpoint) |

**What CIDOC CRM unlocks for NC:** Structural interoperability with any institution that uses CRM (Europeana, NHM, Smithsonian, British Museum, NGA). A CRM-conformant NC record can be ingested by these institutions' discovery systems without transformation.

### 9.2 Darwin Core Application

Darwin Core governs the natural history layer — where the Illustration Opportunity depicts a taxon.

**Mandatory Darwin Core terms for natural history IOs:**

| Term | Source | Example |
|---|---|---|
| `dwc:scientificName` | GBIF taxonomy | `Strelitzia reginae` |
| `gbif:taxonKey` | GBIF authority (DD-GBIF-001) | `3189866` |
| `dwc:vernacularName` | GBIF / Wikidata | `Bird-of-paradise flower` |
| `dwc:recordedBy` | ULAN → illustrator name | `Sydney Parkinson` |
| `dwc:institutionCode` | Source institution | `NHM` |
| `dwc:collectionCode` | Source collection | `Endeavour-Botanical` |
| `dwc:basisOfRecord` | Always `HumanObservation` for illustrations | `HumanObservation` |
| `dwc:locality` | GeoNames place name | `Cape of Good Hope, South Africa` |
| `dwc:year` | Year illustrated | `1769` |
| `dcterms:rights` | RightsStatements.org URI | `http://creativecommons.org/publicdomain/zero/1.0/` |

**What Darwin Core unlocks:** Discoverability in GBIF, iNaturalist, and any GBIF-federated system. A Haeckel medusa plate in NC's database becomes findable by anyone searching for illustrations of _Chrysaora melanaster_ in GBIF's literature + media layer.

### 9.3 IIIF Integration

IIIF (International Image Interoperability Framework) is the image delivery and manifest standard for PREMIUM-tier collections.

**Two APIs in use:**

| API | Version | NC Use |
|---|---|---|
| IIIF Image API | 3.0 | Image tile delivery; product image requests; digital download endpoint |
| IIIF Presentation API | 3.0 | Collection manifests; multi-canvas sequences; metadata delivery |

**Per-collection IIIF artifact:**

Every PREMIUM collection generates:
1. A Manifest at `https://nc.art/iiif/collections/{slug}/manifest.json`
2. One Canvas per Illustration Opportunity
3. One Annotation with `motivation: "painting"` per image
4. Required metadata per canvas: illustrator, date, source identifier, rights URI
5. A `thumbnail` annotation pointing to the NC-hosted IIIF Image API endpoint

**What IIIF unlocks:** Any IIIF-compatible viewer (Universal Viewer, Mirador, Clover) can load NC collections. Institutional partners can embed NC collections in their own environments without any NC-specific integration.

### 9.4 Schema.org Application

Schema.org structured data is applied to every product page and collection page for SEO and structured discovery.

**Product page schema (product pages):**

```json
{
  "@type": ["Product", "CreativeWork"],
  "name": "{product name}",
  "image": "{product image URL}",
  "description": "{product description}",
  "brand": {"@type": "Organization", "name": "Nature & Culture"},
  "offers": {
    "@type": "Offer",
    "price": "{price}",
    "priceCurrency": "GBP",
    "availability": "https://schema.org/InStock",
    "seller": {"@type": "Organization", "name": "Nature & Culture"}
  },
  "isRelatedTo": {
    "@type": "CreativeWork",
    "name": "{illustration title}",
    "creator": {
      "@type": "Person",
      "name": "{illustrator name}",
      "sameAs": "http://vocab.getty.edu/ulan/{ulan_id}"
    },
    "dateCreated": "{year}",
    "license": "{RightsStatements.org URI}",
    "creditText": "{full attribution string}"
  },
  "about": {
    "@type": "Place",
    "name": "{place name}",
    "identifier": "https://sws.geonames.org/{geonames_id}/"
  },
  "contentLocation": {
    "@type": "Place",
    "name": "{place name}"
  }
}
```

**Collection page schema:**

```json
{
  "@type": ["Collection", "CreativeWork"],
  "name": "{collection name}",
  "curator": {
    "@type": "Person",
    "name": "Nathan Holderhead",
    "jobTitle": "Founding Curator",
    "affiliation": {"@type": "Organization", "name": "Nature & Culture"}
  },
  "about": {"@type": "Place", "identifier": "https://sws.geonames.org/{geonames_id}/"},
  "license": "{RightsStatements.org URI}"
}
```

### 9.5 RightsStatements.org Application Summary

RightsStatements.org URIs appear in four surfaces:
1. IIIF manifest `rights` field
2. Schema.org `license` field on product and collection pages
3. XMP metadata in digital download packages
4. CIDOC CRM `E30 Right` entity

NC never invents rights language. The URI is authoritative; the human-readable display text is derived from the URI's published description. The statutory text on the certificate (`17 U.S.C. § 105`) is the underlying legal basis; the URI is the machine-readable signal.

---

## Part X — Commerce Invariants

These rules cannot be changed without Principal Architect review and a new governance document.

| # | Invariant | Rule |
|---|---|---|
| CI-1 | **PD hard gate** | IFC-1 is unconditional. No commercial product from a non-PD/CC0 source. |
| CI-2 | **Illustration Opportunity doctrine** | The commercial object is an IO, not a place, not a taxon. |
| CI-3 | **Edition lock** | Once a CE edition size is ratified at Gate E, it cannot be changed. |
| CI-4 | **No invented rights language** | Rights text cites a statute or links to a RightsStatements.org URI. NC does not invent rights language. |
| CI-5 | **ULAN anchor for named illustrators** | Every named illustrator in a product record must have a ULAN ID or a documented research record explaining its absence. |
| CI-6 | **GeoNames anchor for place products** | Every place-anchored product must have a confirmed GeoNames canonical ID. |
| CI-7 | **No real-person endorsement** | No product implies endorsement by a living person or active institution without explicit written agreement. |
| CI-8 | **Federal nonendorsement** | NASA, NOAA, NARA do not endorse NC products. This language is required on every product page using those sources. |
| CI-9 | **OSM data permanent exclusion** | ODbL-derived OSM data may not be stored in any NC canonical table. Produced-works tiles are permitted for display only. |
| CI-10 | **CE permanence** | NC-ERS requires edition records to be transferred to Internet Archive within 90 days if NC ceases operations. |
| CI-11 | **ICH practice ≠ product** | ICH living practice is context and editorial. Only PD documentary illustration of that practice is the commercial object. |
| CI-12 | **No Darwin Core media from GBIF** | GBIF occurrence media is permanently prohibited from the product pipeline (DD-GBIF-001). |

---

## Part XI — Scale Roadmap

### 11.1 Commerce Milestones

| Milestone | Places | IOs | Active SKUs | CE Editions | Subscriptions live |
|---|---|---|---|---|---|
| **Now** (Pilot) | 7 | ~20 | 2 | 2 | No |
| **Sprint 1** (6 months) | 25 | ~120 | 80 | 15 | No |
| **Sprint 2** (12 months) | 100 | ~500 | 400 | 50 | S1 only |
| **Sprint 3** (24 months) | 500 | ~2,500 | 2,000 | 200 | S1, S2, S3 |
| **Target** (36–48 months) | 2,000 | ~15,000 | ~40,000 | ~2,100 | Full |

### 11.2 Product Family Activation Sequence

| Phase | Families activated | Gate |
|---|---|---|
| Phase 0 (now) | A (Museum Print, Earthrise only), F (Digital, Earthrise only) | Gate E confirmed |
| Phase 1 (Sprint 1) | B (Wall Art), E (Paper Goods), F expanded | SA-GEOPARK-001 + SA-ICH-PLACE-001 ratified |
| Phase 2 (Sprint 2) | C (Educational), D (Books), G (Collector — expanded) | NC-EDRS /educators page live |
| Phase 3 (Sprint 3) | H (Subscription), Institutional licensing | Subscription infrastructure built |
| Phase 4 (Sprint 4) | White-label institutional; Apparel (when Routing Policy v2.0 activates) | DD-fashion-001 ratified |

### 11.3 Standards Activation Dependencies

| Standard | Activation requirement | Blocking |
|---|---|---|
| CIDOC CRM records | Database schema migration for CRM entity types | Phase 2 |
| Darwin Core export | NHM / Walters / NGA IOs in database | Phase 1 |
| IIIF manifests | PREMIUM collections (Sprint 2 target: Alhambra, South Georgia) | Phase 2 |
| Schema.org structured data | Product pages live | Phase 1 |
| RightsStatements.org URIs | Present from Phase 0 on all existing pages | Now |
| NC-PDPS 6-link chain (full) | Named curator + trust.ts restructure | Now (see NC-INSTITUTION-002A) |

---

## Part XII — Reference Model Doctrine

What each reference model contributes to the NC-COMMERCE-2000 architecture — and where NC must not follow.

**Rijksmuseum Shop → Collection object as the commercial anchor.**
The Rijksmuseum's product page is a product page for the work of art, not for "a print of a Dutch painting." NC follows this: every product page is anchored to the Illustration Opportunity, not to a generic category. The IO's metadata — illustrator, date, source, rights — is primary. The product type is secondary.

**Smithsonian Store → Educational products are a revenue tier, not a giveback.**
The Smithsonian treats educational products as first-class commerce, not subsidised charity. NC does likewise: EDU-1/EDU-2 curriculum packs are paid products with genuine educational value. The free tier (EDU-0) is the floor, not the ceiling.

**British Museum Shop → Geographic organisation as a discovery axis.**
The BM organises by culture and geography. NC's designation-series organisation (World Heritage Series, Living Biosphere Series, etc.) applies this principle: the place is the primary discovery node, and the product is the souvenir of the place's intellectual heritage.

**National Geographic Store → Subscription as the anchor relationship.**
NatGeo's magazine is not a revenue line; it is the relationship that makes all other commerce possible. NC's S2 Collector subscription follows this model: the subscription is the mechanism by which the most engaged customers become long-term stakeholders in the edition system.

**Getty Store → Provenance chain on the product page is trust, not compliance.**
Getty does not show provenance because it is required to; it shows provenance because provenance is the value proposition. NC follows this unconditionally: the NC-PDPS 6-link chain is the product's selling point, not its disclaimer.

**Gelato → Production locality is a design constraint, not an afterthought.**
Gelato's global production network is NC's logistics architecture at scale. Every product decision must be evaluated against whether Gelato can produce it near the customer. Products that only viable in one geography are Tier 3 products at best.

**Printful → Reserve for specialised product expansion, not parallel production.**
Printful is the apparel reserve when fashion family products activate. It is not a parallel fulfillment system. Running parallel fulfillment systems adds integration complexity without commercial gain until the product catalog justifies it.

---

## Open Actions

| # | Action | Priority | Blocking |
|---|---|---|---|
| OA-1 | Ratify NC-COMMERCE-2000 | Critical | All Phase 1 products |
| OA-2 | SA-GEOPARK-001: Geopark standards amendment | High | Geopark Expedition Series |
| OA-3 | SA-ICH-PLACE-001: ICH place standards amendment | High | Craft Heritage Series |
| OA-4 | SA-DARK-SKY-001: Dark Sky standards amendment | Medium | Dark Sky Series |
| OA-5 | Activate Gelato integration (API key + POD catalog setup) | High | Phase 1 product activation |
| OA-6 | Implement IIIF manifest generation for Alhambra (first PREMIUM collection) | Medium | Phase 2 IIIF standard |
| OA-7 | Add RightsStatements.org URI field to product schema | High | NC-PDPS conformance |
| OA-8 | Darwin Core field schema in illustration_opportunity table | Medium | Phase 1 natural history products |
| OA-9 | CIDOC CRM entity model in database | Low | Phase 2 standards integration |
| OA-10 | Design subscription fulfillment infrastructure (account system, CE pre-registration) | Medium | Phase 3 |
| OA-11 | Routing Policy v2.0 (activate fashion/apparel lines 17, 18) | Low | Phase 4 |
| OA-12 | DD-FASHION-001: Apparel governance document | Low | Phase 4 |

---

*NC-COMMERCE-2000 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
