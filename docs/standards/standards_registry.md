# Standards Registry

Canonical external standards adopted by Nature & Culture. All schemas, ingestion pipelines, and knowledge models must align to the entries below.

---

## Identity & Linked Data

### Wikidata
- **URI:** `https://www.wikidata.org/entity/`
- **Use:** Authoritative entity identifiers (sites, people, organizations, taxa). Primary reconciliation target.
- **Key property:** `wikidata_qid` on any entity record.

### Schema.org
- **URI:** `https://schema.org/`
- **Use:** Structured data markup for publication and search indexing. Maps to JSON-LD output layer.

---

## Geography

### GeoNames
- **URI:** `https://www.geonames.org/`
- **Use:** Place name authority and geographic hierarchy. Fallback when Wikidata coverage is thin.
- **Key property:** `geonames_id`.

### OpenStreetMap
- **URI:** `https://www.openstreetmap.org/`
- **Use:** Geometry source for site boundaries and spatial queries. OSM relation IDs stored alongside Wikidata QIDs.
- **Key property:** `osm_relation_id`.

---

## Knowledge Organization

### SKOS (Simple Knowledge Organization System)
- **URI:** `https://www.w3.org/2004/02/skos/core#`
- **Use:** Concept schemes, thesauri, and controlled vocabularies. All taxonomy nodes carry SKOS mappings (`skos:Concept`, `skos:broader`, `skos:narrower`, `skos:exactMatch`).

### CIDOC CRM
- **URI:** `http://www.cidoc-crm.org/cidoc-crm/`
- **Use:** Cultural heritage event and object modeling. Governs how acquisition, creation, modification, and destruction events are represented.

### Darwin Core
- **URI:** `https://dwc.tdwg.org/terms/`
- **Use:** Biodiversity and ecological occurrence records. Mandatory for species, specimen, and observation data.

---

## Provenance & Preservation

### PREMIS
- **URI:** `http://www.loc.gov/premis/`
- **Use:** Digital preservation metadata for all objects stored in MinIO. Every artifact carries a PREMIS `Object` record.

### PROV-O (W3C Provenance Ontology)
- **URI:** `https://www.w3.org/TR/prov-o/`
- **Use:** Pipeline lineage. Every derived record links `prov:wasDerivedFrom` its source and `prov:wasGeneratedBy` the worker activity that produced it.

---

## Institutional Standards

### ISO Standards
| Standard | Domain |
|---|---|
| ISO 639 | Language codes |
| ISO 3166 | Country and subdivision codes |
| ISO 8601 | Date and time representation |
| ISO 19115 | Geographic metadata |
| ISO 21127 | CIDOC CRM reference model |

### UNESCO Standards
| Standard | Domain |
|---|---|
| UNESCO World Heritage Convention (1972) | Site classification and Outstanding Universal Value criteria |
| UNESCO Intangible Cultural Heritage Convention (2003) | ICH element categories |
| UNESCO Recommendation on the HUL (2011) | Historic Urban Landscape methodology |

---

## Conformance Rules

1. Every entity record must carry at least one external identifier (`wikidata_qid`, `geonames_id`, or `osm_relation_id`).
2. All dates stored in ISO 8601 format. All language tags in ISO 639-1/3.
3. Provenance chains (PROV-O) are mandatory for any AI-derived or worker-derived field.
4. Biodiversity records must be Darwin Core compliant before leaving the ingestion worker.
5. Cultural heritage objects must map to at least one CIDOC CRM class.
6. Preservation records in MinIO require a PREMIS Object entry in PostgreSQL.
