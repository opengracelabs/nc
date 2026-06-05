# Standards-Based Commerce Classification Design

Mission:

- Design a standards-first classification model.
- Stop using "Archetype" as a primary classification.
- Allow archetypes only as a derived commerce layer, if used at all.

Boundaries:

- No implementation.
- No migrations.
- No schema redesign in this document.
- PostgreSQL remains authority.
- Neo4j remains a projection.

Design path:

```text
Place
↓
Designation
↓
Standards Classifications
↓
Derived Commerce Profile
↓
Product Families
```

## Standards Reviewed

### UNESCO World Heritage

Authoritative role:

- Designation program and criteria for World Heritage properties.
- Criteria `i` through `x` remain source-backed classification values.
- Outstanding Universal Value, inscription data, and designation status remain designation metadata, not commerce categories.

Use in Nature & Culture:

- `Place` can have one or more UNESCO designations.
- UNESCO criteria classify why the place is designated.
- UNESCO criteria can influence commerce derivation, but do not directly activate products.

### Ramsar

Authoritative role:

- Wetlands of International Importance and nine Ramsar criteria.
- Ramsar criteria classify wetland importance, waterbird/species support, ecological representativeness, and related wetland significance.

Use in Nature & Culture:

- Ramsar designation and criteria classify wetland context.
- Ramsar data can support commerce profiles for wetland ecology, waterbirds, aquatic plants, migratory species, and education products.

### IUCN

Authoritative role:

- Protected Area Management Categories classify protected areas by management objective.
- Categories include Ia, Ib, II, III, IV, V, and VI.

Use in Nature & Culture:

- IUCN category is authoritative when source-backed for a place/protected area.
- IUCN category influences visitor-facing themes, conservation framing, and product suitability.
- It should not be converted into a commerce category directly.

### Darwin Core

Authoritative role:

- Biodiversity data exchange terms for taxa, occurrences, events, locations, identifications, and related biodiversity records.

Use in Nature & Culture:

- Taxon and occurrence context should use Darwin Core-aligned terms.
- Darwin Core classifications support concept and opportunity context.
- Darwin Core does not classify commerce products.

### CIDOC CRM

Authoritative role:

- Cultural heritage ontology and semantic model.
- Useful classes include `E53 Place`, `E55 Type`, `E36 Visual Item`, `E39 Actor`, `E22 Human-Made Object`, and rights/provenance related entities.

Use in Nature & Culture:

- CIDOC CRM provides semantic alignment for places, visual items, objects, creators, source records, and depicted concepts.
- CIDOC CRM supports graph projection and provenance semantics.
- CIDOC CRM classes should not be product-family labels.

## Classification Design

### Principle 1: Standards Classifications Are Authoritative

Authoritative classifications must come from:

- Source designation records.
- Recognized standards.
- Governed facts and relationships.
- Human-reviewed source mappings.

Examples:

- UNESCO criterion `vii`.
- Ramsar criterion `6`.
- IUCN category `II`.
- Darwin Core `dwc:Taxon` or `dwc:Occurrence` context.
- CIDOC CRM `E36 Visual Item` or `E53 Place` mapping.

### Principle 2: Commerce Profiles Are Derived

Commerce profiles are generated from standards classifications plus asset/product readiness signals.

Derived commerce profiles can say:

- This collection is suitable for wall art.
- This collection may support education products.
- This collection is not suitable for fashion.
- This collection requires manual review before books.

Derived commerce profiles must not say:

- This is a UNESCO wall-art archetype.
- This place is commercially valuable because of a standard alone.
- This source classification equals a product category.

### Principle 3: Product Families Are Runtime Activation Targets

Product families are activation targets, not authoritative classifications.

Product families:

- Wall Art
- Books
- Calendars
- Cards
- Puzzles
- Fashion
- Home Decor
- Education

Product families inherit from derived commerce profiles, not directly from standards.

## What Remains Authoritative

PostgreSQL authoritative entities:

- `places`
- `place_designations`
- `concepts`
- `facts`
- `relationships`
- `illustration_opportunities`
- `assets`
- `asset_rights`
- `collections`
- `collection_assets`
- `collection_places`

Authoritative classification records:

- Designation program.
- Source record ID.
- Source URL.
- Criteria.
- Standards vocabulary URI or key.
- Source-backed concept.
- Reviewed source mapping.
- Rights and provenance.

Authoritative standards examples:

| Standard | Authoritative Values |
| --- | --- |
| UNESCO | designation program, criteria `i-x`, inscription/designation fields |
| Ramsar | Ramsar designation and criteria `1-9` |
| IUCN | protected area management category `Ia-VI` |
| Darwin Core | taxon, occurrence, event, location, identification terms |
| CIDOC CRM | place, type, actor, visual item, object, provenance mappings |

## What Is Derived

Derived entities:

- Commerce profile.
- Product family suitability.
- Product type suitability.
- Channel suitability.
- Provider suitability.
- Automation mode.
- Variant limits.
- Product generation priority.
- Etsy eligibility.
- Sample-required flag.

Derived values must carry:

- Input standards classifications.
- Input asset signals.
- Rule version.
- Score components.
- Explanation.
- Timestamp.

Derived values should be reproducible from authoritative data.

## Commerce Profile Design

### Derived Commerce Profile Shape

Design-level shape:

```json
{
  "collection_id": "uuid",
  "profile_version": "standards-commerce:v1",
  "status": "candidate",
  "inputs": {
    "designations": [],
    "standards_classifications": [],
    "concepts": [],
    "assets": []
  },
  "scores": {
    "visual_product_fit": 0.0,
    "educational_fit": 0.0,
    "decorative_fit": 0.0,
    "narrative_depth": 0.0,
    "rights_readiness": 0.0,
    "provider_readiness": 0.0
  },
  "product_families": {
    "wall_art": {
      "status": "candidate",
      "confidence": 0.0,
      "reason": ""
    }
  }
}
```

### Commerce Profile Generation

Profile generation should evaluate four input layers:

1. Designation and standards classifications.
2. Collection content and asset characteristics.
3. Rights/provenance readiness.
4. Provider/channel readiness.

Standards do not activate products alone. They contribute evidence.

Example:

```text
UNESCO criterion vii
+ CIDOC E36 Visual Item
+ rights-cleared high-resolution asset
+ collection has approved asset sequence
= wall_art candidate
```

Example:

```text
Ramsar criterion 6
+ Darwin Core waterbird taxon concepts
+ 12 rights-cleared seasonal assets
+ editorial month sequence
= calendar candidate and education candidate
```

Example:

```text
IUCN category II
+ place designation
+ weak visual assets
= no product family activation
```

## Product Family Derivation Rules

### Wall Art

Strong inputs:

- CIDOC CRM `E36 Visual Item`.
- High-resolution rights-cleared asset.
- Visual quality score.
- UNESCO natural criteria `vii`, `viii`, `ix`, `x` can support context.
- Strong place or concept story.

Do not activate when:

- Asset resolution is insufficient.
- Rights are unclear.
- Visual composition is weak.

### Books

Strong inputs:

- Strong narrative depth.
- Multiple related assets.
- Source-backed place/concept structure.
- UNESCO, Ramsar, IUCN, Darwin Core, and CIDOC classifications with explainable connections.

Do not activate automatically:

- Books require editorial plan and manual review.

### Calendars

Strong inputs:

- 12 or more suitable assets.
- Seasonal or monthly narrative.
- Place/concept diversity.
- Ramsar/Darwin Core seasonal migration or ecological context can contribute evidence.

Do not activate when:

- Fewer than 12 assets.
- Assets are visually repetitive.

### Cards

Strong inputs:

- Clear single-image appeal.
- Rights-cleared assets.
- Short caption potential.
- CIDOC visual item or object classification.

Do not activate when:

- Asset requires long explanation to make sense.

### Puzzles

Strong inputs:

- High-detail image.
- Strong color/shape variation.
- Large print derivative.

Do not activate from standards alone.

### Fashion

Strong inputs:

- Decorative motif or repeatable pattern.
- Strong crop compatibility.
- Human mockup review.

Do not activate from UNESCO/Ramsar/IUCN status alone.

### Home Decor

Strong inputs:

- Decorative motif.
- Pattern or crop works at product scale.
- Asset supports repeated use.

Do not activate when:

- Source image is too documentary or text-heavy.

### Education

Strong inputs:

- Darwin Core taxon/occurrence context.
- Ramsar ecological criteria.
- IUCN management category.
- UNESCO OUV narrative.
- CIDOC provenance/creator/source context.

Education is standards-rich but still requires editorial review.

## Neo4j Graph Projection Design

Neo4j must project standards and commerce profiles separately.

### Standards Projection

Projected nodes:

- `Place`
- `Designation`
- `Standard`
- `StandardClassification`
- `Concept`
- `Opportunity`
- `Asset`
- `Collection`

Projected relationships:

```text
(Designation)-[:DESIGNATES]->(Place)
(Designation)-[:USES_STANDARD]->(Standard)
(Designation)-[:HAS_CLASSIFICATION]->(StandardClassification)
(Place)-[:HAS_CONCEPT]->(Concept)
(Opportunity)-[:DEPICTS]->(Concept)
(Asset)-[:REALIZES]->(Opportunity)
(Collection)-[:FEATURES]->(Asset)
(Collection)-[:ABOUT_PLACE]->(Place)
```

Standards node examples:

- `UNESCO World Heritage`
- `Ramsar`
- `IUCN Protected Area Categories`
- `Darwin Core`
- `CIDOC CRM`

Standard classification node examples:

- `unesco:criterion:vii`
- `ramsar:criterion:6`
- `iucn:category:II`
- `dwc:Taxon`
- `cidoc:E36_Visual_Item`

### Commerce Projection

Projected nodes:

- `CommerceProfile`
- `ProductFamily`
- `ProductType`
- `CommerceChannel`
- `Provider`

Projected relationships:

```text
(Collection)-[:HAS_DERIVED_PROFILE]->(CommerceProfile)
(CommerceProfile)-[:DERIVED_FROM]->(StandardClassification)
(CommerceProfile)-[:ACTIVATES]->(ProductFamily)
(ProductFamily)-[:ENABLES]->(ProductType)
(ProductType)-[:ROUTES_TO]->(Provider)
(ProductType)-[:PUBLISHES_TO]->(CommerceChannel)
```

Rules:

- `StandardClassification` nodes are source-backed.
- `CommerceProfile` nodes are derived.
- Neo4j must not collapse standards and commerce into the same label.
- Graph queries should be able to explain why a product family was activated.

Example query path:

```text
Collection
-> HAS_DERIVED_PROFILE
-> CommerceProfile
-> DERIVED_FROM
-> unesco:criterion:vii
```

This separation keeps commerce explainable without corrupting standards semantics.

## Replacement For Archetypes

Do not use archetypes as primary classification.

Allowed use:

- A derived commerce convenience label generated after standards classification.
- A UI/internal shorthand only.
- Never authoritative.
- Never a source field.
- Never the first classification layer.

Preferred replacement terms:

- `standards_classification`
- `commerce_profile`
- `product_family_fit`
- `product_generation_policy`

If an archetype-like label is retained, it must be stored as derived profile metadata:

```json
{
  "derived_label": "natural_history_plate_like",
  "derived_from": [
    "cidoc:E36_Visual_Item",
    "dwc:Taxon",
    "rights:Public_Domain"
  ],
  "authoritative": false
}
```

## Classification Governance

Required governance rules:

- Standards mappings require source or reviewer provenance.
- Derived commerce profiles can be regenerated.
- Manual overrides must record reviewer, reason, and date.
- Product family activation must show input classifications and asset readiness.
- Commerce profile changes must not alter source designation records.

## Design Recommendation

Use this hierarchy:

```text
Authoritative:
Place
Designation
Standard
StandardClassification
Concept
Opportunity
Asset
Collection

Derived:
CommerceProfile
ProductFamilyFit
ProductTypeFit
ProviderRoute
ChannelPolicy
DerivedArchetypeLabel (optional)
```

This preserves standards integrity while still allowing automated commerce decisions.

## References

- UNESCO World Heritage criteria: https://whc.unesco.org/en/criteria
- Ramsar Sites Criteria: https://www.ramsar.org/document/ramsar-sites-criteria
- IUCN protected area categories: https://iucn.org/content/protected-area-categories
- Darwin Core / TDWG standards: https://www.tdwg.org/standards/
- Darwin Core terms: https://dwc.tdwg.org/terms/
- CIDOC CRM: https://cidoc-crm.org/
- CIDOC CRM version 7.1.3 / ISO 21127:2023 alignment: https://cidoc-crm.org/sites/default/files/Documents/cidoc_crm_version_7.1.3.html
