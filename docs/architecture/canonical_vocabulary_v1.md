# Canonical Vocabulary v1

This document defines the Version 1.0 release of the Nature & Culture Canonical Vocabulary. It provides the authoritative controlled vocabularies, SKOS hierarchies, CIDOC CRM alignments, and Wikidata mappings for all entities within the platform's knowledge graph.

---

## 1. CONTROLLED VOCABULARIES

### 1.1 Countries (`concept_type: country`)
- **Authority:** ISO 3166-1 alpha-2.
- **Key Pattern:** `country:{ISO_CODE}`.

| Key | Label (en) | Label (fr) | Wikidata QID |
|---|---|---|---|
| `country:AU` | Australia | Australie | Q408 |
| `country:FR` | France | France | Q142 |
| `country:EC` | Ecuador | Équateur | Q736 |
| `country:TZ` | Tanzania | Tanzanie | Q924 |

### 1.2 UNESCO Criteria (`concept_type: ouv_criterion`)
- **Authority:** World Heritage Convention Operational Guidelines.
- **Key Pattern:** `ouv_criterion:{roman_numeral}`.

| Key | Label (en) | Label (fr) | Domain |
|---|---|---|---|
| `ouv_criterion:i` | Criterion (i) | Critère (i) | Cultural |
| `ouv_criterion:ii` | Criterion (ii) | Critère (ii) | Cultural |
| `ouv_criterion:vii` | Criterion (vii) | Critère (vii) | Natural |
| `ouv_criterion:x` | Criterion (x) | Critère (x) | Natural |

### 1.3 Heritage Types (`concept_type: heritage_type`)
- **Authority:** UNESCO.
- **Key Pattern:** `heritage_type:{slug}`.

| Key | Label (en) | Label (fr) |
|---|---|---|
| `heritage_type:cultural` | Cultural Heritage | Patrimoine culturel |
| `heritage_type:natural` | Natural Heritage | Patrimoine naturel |
| `heritage_type:mixed` | Mixed Heritage | Patrimoine mixte |

### 1.4 Designations (`concept_type: designation`)
- **Authority:** Institutional framework.
- **Key Pattern:** `designation:{slug}`.

| Key | Label (en) | Label (fr) | Wikidata QID |
|---|---|---|---|
| `designation:world_heritage_site` | UNESCO World Heritage Site | Patrimoine mondial de l'UNESCO | Q9259 |
| `designation:biosphere_reserve` | UNESCO Biosphere Reserve | Réserve de biosphère de l'UNESCO | Q158454 |
| `designation:ramsar_site` | Ramsar Site | Site Ramsar | Q170145 |

### 1.5 Institutional Actors (`concept_type: institution`)
- **Authority:** International organizational registry.
- **Key Pattern:** `institution:{slug}`.

| Key | Label (en) | Wikidata QID | Role |
|---|---|---|---|
| `institution:unesco` | UNESCO | Q7809 | Primary Authority (WHC, MAB) |
| `institution:iucn` | IUCN | Q180587 | Advisory Body (Natural) |
| `institution:icomos` | ICOMOS | Q273160 | Advisory Body (Cultural) |
| `institution:iccrom` | ICCROM | Q667793 | Advisory Body (Preservation) |

---

## 2. SKOS MAPPINGS (Simple Knowledge Organization System)

The following mappings enable semantic hierarchy and interoperability.

| NC Concept Type | SKOS Property | Target / URI |
|---|---|---|
| `designation` | `skos:broader` | `http://vocabularies.unesco.org/thesaurus/concept547` (Protected Area) |
| `ouv_criterion` | `skos:related` | `http://vocabularies.unesco.org/thesaurus/concept456` (Cultural Property) |
| `country` | `skos:exactMatch` | `https://www.wikidata.org/wiki/Entity/{QID}` |
| `institution` | `skos:exactMatch` | `https://www.wikidata.org/wiki/Entity/{QID}` |

---

## 3. CIDOC CRM MAPPINGS (ISO 21127)

Aligning the model with the Conceptual Reference Model for Cultural Heritage.

| NC Entity / Relationship | CIDOC CRM Class / Property | Semantic Role |
|---|---|---|
| `Place` (Record) | `E53 Place` | Geographic location and extent. |
| `Place` (Record) | `E27 Site` | The heritage entity with value. |
| `institution` | `E39 Actor` | An organization capable of agency. |
| `inscription_year` | `E65 Creation` -> `P4 has time-span` | The event of designation. |
| `LOCATED_IN_COUNTRY` | `P53 has former or current location` | Geographic containment. |
| `MEETS_CRITERION` | `P2 has type` | Typological classification. |

---

## 4. WIKIDATA LINKS

Wikidata serves as the primary external reconciliation target. Every `Concept` in v1 SHOULD carry a Wikidata QID in its `external_ids` or `concept_key`.

- **Site Reconciliation:** `nc:place_id` -> `wd:P1435` (Heritage designation).
- **Institutional Links:** `nc:institution:unesco` -> `wd:Q7809`.
- **Administrative Links:** `nc:country:AU` -> `wd:Q408`.

---

## 5. MIGRATION RECOMMENDATIONS

1. **Seed Completion:** Execute a one-time migration to seed the `concepts` table with the Institutional Actors defined in 1.5.
2. **Concept Redirection:** For existing concepts that use non-slugified keys, implement a `skos:exactMatch` link in the `concept_aliases` table to point to the v1 canonical keys.
3. **Multilingual Backfill:** Use the `translation_worker` to ensure every v1 concept has a valid `fr` (French) label in the `concepts.label` JSONB field.
4. **Wikidata Sync:** Run a batch reconciliation job to ensure all v1 `country` and `designation` concepts have their Wikidata QID stored in the `provenance` or a new `external_ids` field.
