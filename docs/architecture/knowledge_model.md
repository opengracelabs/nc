# UNESCO Knowledge Model (Phase 2)

This document defines the canonical knowledge representation for UNESCO World Heritage data within the Nature & Culture platform. It aligns with CIDOC CRM and SKOS standards to ensure interoperability with global heritage and biodiversity networks.

---

## 1. Fact Types (Attributes)

Facts are discrete properties of a Place that do not necessarily link to another primary entity but provide essential descriptive metadata.

| Predicate | Value Type | Description |
|---|---|---|
| `has_inscription_year` | Number | The year the property was added to the World Heritage List. |
| `has_unesco_ref` | Text | The official alphanumeric reference ID (e.g., `123bis`). |
| `is_transboundary` | Boolean | True if the site spans multiple sovereign states. |
| `has_core_area` | Number | Area of the core zone in hectares. |
| `has_buffer_area` | Number | Area of the buffer zone in hectares. |
| `has_ouv_statement` | JSONB | Multilingual dictionary of the Statement of Outstanding Universal Value. |
| `has_justification` | JSONB | Multilingual dictionary of the justification for criteria. |

---

## 2. Relationship Types

Relationships link a `Place` to a `Concept` or another `Place`.

| Subject | Predicate | Object | Description |
|---|---|---|---|
| Place | `LOCATED_IN_COUNTRY` | Concept (Country) | Links a site to its host state(s). |
| Place | `MEETS_CRITERION` | Concept (Criterion) | Links a site to the UNESCO criteria (i-x). |
| Place | `HAS_HERITAGE_TYPE` | Concept (HeritageType) | Links to Cultural, Natural, or Mixed. |
| Place | `HAS_DESIGNATION` | Concept (Designation) | Canonical link to "UNESCO World Heritage Site". |

---

## 3. Controlled Vocabularies

### `designation`
- `world_heritage_site` (UNESCO World Heritage Site)

### `heritage_type`
- `cultural`
- `natural`
- `mixed`

### `ouv_criterion`
- `i`, `ii`, `iii`, `iv`, `v`, `vi` (Cultural criteria)
- `vii`, `viii`, `ix`, `x` (Natural criteria)

### `country`
- ISO 3166-1 alpha-2 codes (e.g., `AU`, `FR`, `EC`).

---

## 4. SKOS Mappings

| Internal Term | SKOS Mapping | URI (Target) |
|---|---|---|
| `Place` | `skos:Concept` | `http://www.w3.org/2004/02/skos/core#Concept` |
| `ouv_criterion` | `skos:Concept` | `http://vocabularies.unesco.org/thesaurus/concept456...` |
| `heritage_type` | `skos:narrower` | Maps under a broader "Heritage" concept. |

---

## 5. CIDOC CRM Mappings (ISO 21127)

| Internal Type | CRM Class | Description |
|---|---|---|
| `Place` | `E53 Place` | The geographic extent of the heritage site. |
| `Site` | `E27 Site` | The physical entity and its cultural/natural value. |
| `Inscription` | `E65 Creation` | The event of designation (inscription). |
| `Country` | `E53 Place` | The administrative geographic entity. |

---

## 6. Concept Normalization Rules

1. **Multilingual Labels:** All `Concept` labels and `ConceptAlias` entries must support at least English (`en`) and French (`fr`).
2. **Keying:** `concept_key` must be lowercase and use underscores (e.g., `heritage_type:cultural`).
3. **Reconciliation:** Where possible, `concept_key` should match the Wikidata QID (e.g., `country:Q408` for Australia) to facilitate graph linking.
4. **Provenance:** Every triple (Fact or Relationship) must carry a `provenance` record linking it to the specific `knowledge_worker` run and the source `Asset`.
