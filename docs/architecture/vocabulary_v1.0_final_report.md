# Canonical Vocabulary v1.0 Final Report

## VOCABULARY REPORT
The Version 1.0 vocabulary is now complete and seeded in the database.

### 1. Institutional Actors
Canonical keys established for:
- `institution:unesco` (UNESCO)
- `institution:iucn` (IUCN/UICN)
- `institution:icomos` (ICOMOS)
- `institution:iccrom` (ICCROM)

### 2. Heritage Types
Standardized keys:
- `heritage_type:cultural`
- `heritage_type:natural`
- `heritage_type:mixed`

### 3. Designations
Primary institutional frameworks:
- `designation:world_heritage_site`
- `designation:biosphere_reserve`
- `designation:ramsar_site`

### 4. UNESCO Criteria
Full roman numeral set (i–x) with Cultural/Natural domain metadata.

### 5. Multilingual Support
All v1.0 concepts carry authoritative labels in **English (en)** and **French (fr)**.

---

## SKOS REPORT
Semantic hierarchy is defined via SKOS properties in the platform documentation.

- **`skos:Concept`**: Base class for all vocabulary entries.
- **`skos:broader`**: Used to link specific designations to the global "Protected Area" concept.
- **`skos:exactMatch`**: Maps internal concepts to Wikidata and the UNESCO Thesaurus.
- **`skos:prefLabel`**: Implemented via the `label` JSONB field (EN/FR).

---

## CIDOC CRM REPORT
Knowledge graph alignment with ISO 21127.

- **`E39 Actor`**: Mapped to the `institution` concept type.
- **`E27 Site`**: Mapped to the `Place` record (as a heritage entity).
- **`E53 Place`**: Mapped to both `Place` records (geographic) and `country` concepts (administrative).
- **`P2 has type`**: Used for criteria and heritage type relationships.

---

## WIKIDATA REPORT
Standardized reconciliation targets.

- **Countries**: Mapped via ISO codes to Wikidata QIDs (e.g., `AU` -> `Q408`).
- **Designations**: Mapped to authoritative entities (e.g., World Heritage Site -> `Q9259`).
- **Institutions**: Mapped to global organization IDs (e.g., UNESCO -> `Q7809`).

---

## SEED MIGRATIONS
The following migration file has been created to finalize the v1.0 deployment:
- `infrastructure/postgres/init/09_vocabulary_v1_seed.sql`
