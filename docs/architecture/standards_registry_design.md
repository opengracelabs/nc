# Standards Registry Design

Mission:

- Design `standards_registry`.
- Provide a standards registry architecture for Nature & Culture.

Boundaries:

- No implementation.
- No migrations.
- No schema redesign.

## Purpose

`standards_registry` is the authoritative internal index of standards used by Nature & Culture.

It should answer:

- Which standards does the platform recognize?
- Which authority maintains each standard?
- Which standards family does each belong to?
- Which version or profile is currently used?
- Is the standard active, candidate, deprecated, or reference-only?

The registry does not replace the standards. It records how Nature & Culture references and applies them.

## Standards Registry Architecture

Design-level table shape:

```sql
CREATE TABLE standards_registry (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    standard_name       TEXT NOT NULL,
    standard_family     TEXT NOT NULL,
    authority           TEXT NOT NULL,
    version             TEXT,
    status              TEXT NOT NULL DEFAULT 'active',
    canonical_url       TEXT,
    description         TEXT,
    applies_to          TEXT[] NOT NULL DEFAULT '{}',
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (standard_name, authority, COALESCE(version, ''))
);
```

Required fields from this mission:

- `standard_name`
- `standard_family`
- `authority`
- `version`
- `status`

Recommended status values:

- `active`
- `candidate`
- `reference_only`
- `deprecated`

Recommended standard families:

- `security`
- `identity`
- `web`
- `geospatial`
- `heritage`
- `biodiversity`
- `vocabulary`
- `preservation`
- `provenance`
- `metadata`
- `image_interoperability`
- `accessibility`
- `application_security`
- `supply_chain_security`
- `zero_trust`
- `secure_software_development`

## Standards Map

| Standard | standard_name | standard_family | authority | version | status |
| --- | --- | --- | --- | --- | --- |
| NIST | NIST Cybersecurity Framework | security | National Institute of Standards and Technology | CSF 2.0 | candidate |
| ISO | ISO 19115 Geographic Metadata | geospatial | International Organization for Standardization | ISO 19115 series | reference_only |
| W3C | W3C Web Standards | web | World Wide Web Consortium | living/current | active |
| OGC | OGC GeoJSON / Simple Features / API Features | geospatial | Open Geospatial Consortium | current profiles | active |
| UNESCO | UNESCO World Heritage Criteria | heritage | UNESCO World Heritage Centre | current Operational Guidelines | active |
| CIDOC CRM | CIDOC Conceptual Reference Model | heritage | ICOM CIDOC CRM SIG / ISO | ISO 21127:2023 / CRM 7.1.3 | active |
| Darwin Core | Darwin Core | biodiversity | Biodiversity Information Standards TDWG | current term list | active |
| SKOS | Simple Knowledge Organization System | vocabulary | W3C | W3C Recommendation | active |
| PREMIS | PREMIS Data Dictionary | preservation | Library of Congress / PREMIS Editorial Committee | current | active |
| PROV-O | PROV-O Provenance Ontology | provenance | W3C | W3C Recommendation | active |
| Schema.org | Schema.org Vocabulary | metadata | Schema.org Community Group | current | active |
| IIIF | International Image Interoperability Framework | image_interoperability | IIIF Consortium | Image/API Presentation current profiles | candidate |
| WCAG | Web Content Accessibility Guidelines | accessibility | World Wide Web Consortium | WCAG 2.2 | active |
| WAI-ARIA | Accessible Rich Internet Applications | accessibility | World Wide Web Consortium | WAI-ARIA 1.2 | active |
| NIST Zero Trust | NIST Zero Trust Architecture | zero_trust | National Institute of Standards and Technology | SP 800-207 | candidate |
| OWASP | OWASP Application Security Verification Standard | application_security | Open Worldwide Application Security Project | ASVS 5.0 | candidate |
| SLSA | Supply-chain Levels for Software Artifacts | supply_chain_security | OpenSSF | SLSA 1.1 | candidate |
| SSDF | Secure Software Development Framework | secure_software_development | National Institute of Standards and Technology | SP 800-218 | candidate |

## Usage Rules

### Authoritative Use

Use standards registry records when:

- Mapping database fields to external standards.
- Producing provenance or metadata exports.
- Building Neo4j projection labels and relationships.
- Explaining classification decisions.
- Validating product/public data contracts.

### Non-Authoritative Use

Do not use `standards_registry` to:

- Store individual classifications.
- Store place designations.
- Store product family decisions.
- Replace source-specific tables.
- Replace controlled vocabulary concepts.

The registry says which standard is recognized. It does not store every term from that standard.

## Relationship To Other Models

### Standards Classifications

Standards classifications should reference the registry conceptually:

```text
standards_registry
↓
standard_classification
↓
place_designation / concept / opportunity / asset
```

Example:

```text
CIDOC CRM
↓
cidoc:E36_Visual_Item
↓
Asset / Opportunity
```

### Concepts

`concepts` can use standards registry entries for provenance and alignment:

- SKOS concept scheme.
- Darwin Core taxon concept.
- CIDOC CRM type.
- Schema.org public metadata type.

### Commerce Profiles

Commerce profiles may derive from standards classifications, but they must not become standards registry records.

Example:

```text
UNESCO criterion vii + CIDOC E36 Visual Item + Public Domain asset
↓
derived wall_art candidate
```

`wall_art` is not a standard.

## Neo4j Projection

Neo4j should project registry records separately from derived commerce records.

Projected labels:

- `Standard`
- `StandardFamily`
- `Authority`

Projected relationships:

```text
(Standard)-[:IN_FAMILY]->(StandardFamily)
(Standard)-[:MAINTAINED_BY]->(Authority)
(StandardClassification)-[:USES_STANDARD]->(Standard)
(CommerceProfile)-[:DERIVED_FROM]->(StandardClassification)
```

Rules:

- `Standard` nodes come from `standards_registry`.
- Standards nodes are authoritative references.
- Commerce profile nodes are derived.
- Product family nodes are not standards.

## Recommended Initial Records

```json
[
  {
    "standard_name": "NIST Cybersecurity Framework",
    "standard_family": "security",
    "authority": "National Institute of Standards and Technology",
    "version": "CSF 2.0",
    "status": "candidate"
  },
  {
    "standard_name": "ISO 19115 Geographic Metadata",
    "standard_family": "geospatial",
    "authority": "International Organization for Standardization",
    "version": "ISO 19115 series",
    "status": "reference_only"
  },
  {
    "standard_name": "W3C Web Standards",
    "standard_family": "web",
    "authority": "World Wide Web Consortium",
    "version": "living/current",
    "status": "active"
  },
  {
    "standard_name": "OGC GeoJSON / Simple Features / API Features",
    "standard_family": "geospatial",
    "authority": "Open Geospatial Consortium",
    "version": "current profiles",
    "status": "active"
  },
  {
    "standard_name": "UNESCO World Heritage Criteria",
    "standard_family": "heritage",
    "authority": "UNESCO World Heritage Centre",
    "version": "current Operational Guidelines",
    "status": "active"
  },
  {
    "standard_name": "CIDOC Conceptual Reference Model",
    "standard_family": "heritage",
    "authority": "ICOM CIDOC CRM SIG / ISO",
    "version": "ISO 21127:2023 / CRM 7.1.3",
    "status": "active"
  },
  {
    "standard_name": "Darwin Core",
    "standard_family": "biodiversity",
    "authority": "Biodiversity Information Standards TDWG",
    "version": "current term list",
    "status": "active"
  },
  {
    "standard_name": "Simple Knowledge Organization System",
    "standard_family": "vocabulary",
    "authority": "World Wide Web Consortium",
    "version": "W3C Recommendation",
    "status": "active"
  },
  {
    "standard_name": "PREMIS Data Dictionary",
    "standard_family": "preservation",
    "authority": "Library of Congress / PREMIS Editorial Committee",
    "version": "current",
    "status": "active"
  },
  {
    "standard_name": "PROV-O Provenance Ontology",
    "standard_family": "provenance",
    "authority": "World Wide Web Consortium",
    "version": "W3C Recommendation",
    "status": "active"
  },
  {
    "standard_name": "Schema.org Vocabulary",
    "standard_family": "metadata",
    "authority": "Schema.org Community Group",
    "version": "current",
    "status": "active"
  },
  {
    "standard_name": "International Image Interoperability Framework",
    "standard_family": "image_interoperability",
    "authority": "IIIF Consortium",
    "version": "current Image/API Presentation profiles",
    "status": "candidate"
  },
  {
    "standard_name": "Web Content Accessibility Guidelines",
    "standard_family": "accessibility",
    "authority": "World Wide Web Consortium",
    "version": "WCAG 2.2",
    "status": "active"
  },
  {
    "standard_name": "Accessible Rich Internet Applications",
    "standard_family": "accessibility",
    "authority": "World Wide Web Consortium",
    "version": "WAI-ARIA 1.2",
    "status": "active"
  },
  {
    "standard_name": "NIST Zero Trust Architecture",
    "standard_family": "zero_trust",
    "authority": "National Institute of Standards and Technology",
    "version": "SP 800-207",
    "status": "candidate"
  },
  {
    "standard_name": "OWASP Application Security Verification Standard",
    "standard_family": "application_security",
    "authority": "Open Worldwide Application Security Project",
    "version": "ASVS 5.0",
    "status": "candidate"
  },
  {
    "standard_name": "Supply-chain Levels for Software Artifacts",
    "standard_family": "supply_chain_security",
    "authority": "OpenSSF",
    "version": "SLSA 1.1",
    "status": "candidate"
  },
  {
    "standard_name": "Secure Software Development Framework",
    "standard_family": "secure_software_development",
    "authority": "National Institute of Standards and Technology",
    "version": "SP 800-218",
    "status": "candidate"
  }
]
```

## Governance

Registry changes should require review when:

- A standard moves from `candidate` to `active`.
- A standard version changes.
- A standard is deprecated.
- A new authority is introduced.

Each registry record should preserve:

- Source URL.
- Version note.
- Reviewer.
- Review date.
- Reason for activation or deprecation.

## Design Recommendation

Create `standards_registry` as a compact authority index, not a full standards term warehouse.

Keep term-level mappings in standards classification records or controlled vocabulary tables.

Use the registry to make standards use explicit, reviewable, and projectable into Neo4j.
