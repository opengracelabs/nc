# Canonical Concept Vocabulary

This document defines the controlled vocabularies, SKOS mappings, and CIDOC CRM alignments for the Nature & Culture platform. It ensures semantic consistency across all heritage and ecological data processed by the system.

---

## 1. Controlled Vocabularies

### 1.1 Countries (`concept_type: country`)
- **Authority:** ISO 3166-1 alpha-2.
- **Key Pattern:** `country:{ISO_CODE}` (e.g., `country:AU`, `country:FR`).
- **Mapping:** Every country concept maps to a specific **Wikidata QID** for global reconciliation.

| Key | Label (en) | Label (fr) | Wikidata QID |
|---|---|---|---|
| `country:AU` | Australia | Australie | Q408 |
| `country:FR` | France | France | Q142 |
| `country:EC` | Ecuador | Équateur | Q736 |
| `country:TZ` | Tanzania | Tanzanie | Q924 |

### 1.2 Heritage Types (`concept_type: heritage_type`)
- **Authority:** UNESCO World Heritage Convention.
- **Key Pattern:** `heritage_type:{slug}`.

| Key | Label (en) | Label (fr) | SKOS Alignment |
|---|---|---|---|
| `heritage_type:cultural` | Cultural Heritage | Patrimoine culturel | `skos:Concept` |
| `heritage_type:natural` | Natural Heritage | Patrimoine naturel | `skos:Concept` |
| `heritage_type:mixed` | Mixed Heritage | Patrimoine mixte | `skos:Concept` |

### 1.3 UNESCO Criteria (`concept_type: ouv_criterion`)
- **Authority:** Operational Guidelines for the Implementation of the World Heritage Convention.
- **Key Pattern:** `ouv_criterion:{roman_numeral}`.

| Key | Label (en) | Label (fr) | Description |
|---|---|---|---|
| `ouv_criterion:i` | Criterion (i) | Critère (i) | Human creative genius |
| `ouv_criterion:vii` | Criterion (vii) | Critère (vii) | Natural beauty/aesthetic |
| `ouv_criterion:x` | Criterion (x) | Critère (x) | Biological diversity |

### 1.4 Designations (`concept_type: designation`)
- **Authority:** Institutional frameworks.
- **Key Pattern:** `designation:{slug}`.

| Key | Label (en) | Label (fr) | Wikidata QID |
|---|---|---|---|
| `designation:world_heritage_site` | UNESCO World Heritage Site | Patrimoine mondial de l'UNESCO | Q9259 |
| `designation:biosphere_reserve` | UNESCO Biosphere Reserve | Réserve de biosphère de l'UNESCO | Q158454 |
| `designation:ramsar_site` | Ramsar Site | Site Ramsar | Q170145 |

---

## 2. SKOS Mappings (Simple Knowledge Organization System)

The platform uses SKOS for concept hierarchy and cross-vocabulary linking.

| NC Concept Type | SKOS Property | Target / URI |
|---|---|---|
| `designation` | `skos:broader` | `http://vocabularies.unesco.org/thesaurus/concept547` (Protected Area) |
| `ouv_criterion` | `skos:related` | `http://vocabularies.unesco.org/thesaurus/concept456` (Cultural Property) |
| `country` | `skos:exactMatch` | `https://www.wikidata.org/wiki/Entity/{QID}` |
| Any Alias | `skos:altLabel` | Alternative names in multiple languages. |

---

## 3. CIDOC CRM Mappings (ISO 21127)

Aligning the knowledge model with the Conceptual Reference Model for cultural heritage.

| NC Entity / Fact | CIDOC CRM Class / Property | Semantic Role |
|---|---|---|
| `Place` record | `E53 Place` | The geographic location and extent. |
| `Place` record | `E27 Site` | The heritage entity with value. |
| `country` Concept | `E53 Place` | The administrative territorial entity. |
| `inscription_year` | `E65 Creation` -> `P4 has time-span` | The event of formal designation. |
| `LOCATED_IN_COUNTRY` | `P53 has former or current location` | Geographic containment. |
| `MEETS_CRITERION` | `P2 has type` | Typological classification. |

---

## 4. Normalization Rules

1. **Case Sensitivity:** All `concept_key` values are stored in **lowercase**, except for ISO country codes which use **uppercase** for visual consistency.
2. **Slugification:** Keys use underscores (`_`) instead of spaces.
3. **Multilingualism:** Every concept MUST have a label in English (`en`). Labels in French (`fr`) are highly recommended for UNESCO compliance.
4. **Identifier Persistence:** Once a `concept_key` is established, it should never change. Merges should use a redirection or `skos:exactMatch` link.
5. **Traceability:** Every concept creation or update is logged in the `provenance` field of the `concepts` table, linking back to the `knowledge_worker` run.
