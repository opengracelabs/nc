---
name: project-nc-commerce-2000
description: "NC-COMMERCE-2000 Commerce Architecture Blueprint. Commerce design at 2,000 places. 8 product families, 8 subscription tiers, POD routing (Gelato primary/Printful secondary/specialist studio), standards integration (CIDOC CRM/Darwin Core/IIIF/Schema.org/RightsStatements.org), 10 designation-series product lines, 12 commerce invariants, 4-phase activation roadmap."
metadata:
  type: project
---

NC-COMMERCE-2000 Commerce Architecture Blueprint — DRAFT 2026-06-13, pending ratification.
File: `docs/architecture/NC-COMMERCE-2000_commerce_architecture_blueprint.md`

**Scale parameters:** 2,000 places → ~15,000 IOs → ~40,000 SKUs → ~2,100 CE editions → 3-tier subscriptions.

**8 Product families (extending NC-PRODUCT-001's 18 approved lines):**
- A: Museum Print (lines 1, 6, 20) — specialist studio
- B: Wall Art (2, 3, 4, 5) — Gelato primary
- C: Educational (9, 10, 12) — digital + Gelato
- D: Books & Guides (11, 13) — POD book specialist
- E: Paper Goods (14, 15, 16, 19) — Gelato
- F: Digital (8) — digital delivery; IIIF tiers
- G: Collector (CE variants + 20) — specialist studio + NC direct
- H: Subscription (new)

**7 Designation-specific product series:** World Heritage · Living Biosphere · Geopark Expedition · Wetland & Bird · Craft Heritage · Dark Sky · Ocean Atlas.

**POD routing:** Gelato = primary (global 32+ countries). Printful = secondary + apparel reserve. Specialist studio = Museum Print tier. POD book specialist = books.

**4 Educational tiers:** EDU-0 (free, 1920px + context card) · EDU-1 (Classroom £12–18) · EDU-2 (Curriculum £45–65) · EDU-3 (Institutional £150/yr) · EDU-4 (Research £350/yr).

**3 Subscription tiers:** S1 Explorer (£75/yr: monthly DDS + 10% discount) · S2 Collector (£195/yr: CE pre-registration priority, 30-day window) · S3 Institutional (£495/yr: EDU-3 + IIIF + Darwin Core export).

**5 Digital product types:** DDS (Digital Study Edition, OE, £15–25) · DDR (Digital Research Edition, OE, £45–95) · DDC (Digital Collector Edition, CE 100, £95–195) · IIIF Access License (per-manifest, £45/collection/yr).

**5 Institutional product tiers:** CC0 Partner (reciprocal/attribution) · Place Collection License (£2,500/yr) · Domain License (£5,000/yr) · Full Catalog (£15,000/yr) · Educator Annual (£150/yr).

**Standards integration:**
- CIDOC CRM: E22/E12/E21/E78/E74/E30/E53/E36 entity types for heritage layer
- Darwin Core: scientificName + gbif:taxonKey + recordedBy + basisOfRecord for natural history IOs
- IIIF Presentation 3.0 + Image 3.0: manifests at nc.art/iiif/collections/{slug}/manifest.json
- Schema.org Product + CreativeWork + Place on all product and collection pages
- RightsStatements.org URIs: 4 surfaces (IIIF manifest, Schema.org, XMP metadata, CIDOC CRM E30)

**12 Commerce invariants CI-1–CI-12:** PD hard gate · IO doctrine · edition lock · no invented rights language · ULAN anchor · GeoNames anchor · no real-person endorsement · federal nonendorsement · OSM permanent exclusion · CE permanence (Internet Archive) · ICH practice ≠ product · no Darwin Core media from GBIF.

**4-phase activation:** Phase 0 (now: Earthrise only) → Phase 1 (Sprint 1: Wall Art + Paper Goods; SA-GEOPARK-001 + SA-ICH-PLACE-001 required) → Phase 2 (Sprint 2: Educational + Books + Collector expanded; IIIF manifests) → Phase 3 (Sprint 3: Subscriptions + Institutional licensing) → Phase 4 (Sprint 4: White-label + Apparel when Routing Policy v2.0 activates).

**Reference model doctrine:**
- Rijksmuseum: IO as commercial anchor (not generic category)
- Smithsonian: Educational products are revenue, not giveback
- BM: Geographic/designation organisation as primary discovery
- NatGeo: Subscription as the anchor relationship
- Getty: Provenance chain is the value proposition, not the disclaimer
- Gelato: Production locality is a design constraint
- Printful: Reserve for specialised expansion (apparel)

See also: [[project-nc-product-001]] [[project-nc-places-1000]] [[project-nc-places-2000]] [[project-nc-ich-001]] [[project-nc-trust-003]]
