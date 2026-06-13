# NC-PLACES-FACTORY-001: Global Place Strategy

**Subject:** Editorial & Commercial Scaling for Thousands of Places
**Strategy:** Standards-First Architecture & Automated Commerce Derivation
**Status:** Approved for Implementation
**Date:** June 13, 2026

---

## 1. Place Category System (Standards-First)

Nature & Culture does not invent categories. We utilize authoritative international standards to classify every location. This ensures global interoperability and museum-grade intelligence.

| Standard | Category Labels | Usage |
| :--- | :--- | :--- |
| **UNESCO World Heritage** | Natural (i-x), Cultural (i-vi), Mixed | Defines "Outstanding Universal Value." |
| **UNESCO Biosphere** | Core Area, Buffer Zone, Transition Area | Defines human-nature integration. |
| **UNESCO Geopark** | Geological Heritage of International Significance | Defines "Deep Time" and Earth history. |
| **Ramsar** | Wetlands of International Importance (1-9) | Defines aquatic and bird migration hubs. |
| **IUCN** | Category Ia (Strict Nature) to VI (Sustainable Use) | Defines management and accessibility. |
| **IDA (Dark Sky)** | Sanctuary, Reserve, Park, Community | Defines celestial purity and night visibility. |
| **MPA (Marine)** | No-Take, Multiple Use, Seasonal | Defines ocean health and species factories. |
| **UNESCO ICH** | Oral, Performing, Social, Nature, Craft | Links living culture to physical geography. |

---

## 2. Collection Families

Collections are grouped into "Families" to allow for cross-place discovery and thematic consistency.

*   **Family: The Primeval Forge (Geology & Deep Time)**
    *   *Inputs:* UNESCO Geoparks, UNESCO Natural (viii).
    *   *Examples:* Grand Canyon, Vatnajökull, Zhangjiajie.
*   **Family: The Species Factory (Biodiversity & Life)**
    *   *Inputs:* Ramsar, Biosphere Reserves, UNESCO Natural (ix, x), IUCN II-IV.
    *   *Examples:* Galápagos, Serengeti, Pantanal.
*   **Family: The Blue Jewel (Marine & Aquatic)**
    *   *Inputs:* MPAs, Ramsar, UNESCO Natural (vii, x).
    *   *Examples:* Great Barrier Reef, Raja Ampat, Ross Sea.
*   **Family: The Human Signature (Culture & Heritage)**
    *   *Inputs:* UNESCO Cultural (i-vi), UNESCO ICH.
    *   *Examples:* Kyoto, Venice, Machu Picchu, Lalibela.
*   **Family: The Celestial Veil (Dark Sky & Astronomy)**
    *   *Inputs:* IDA Reserves/Sanctuaries.
    *   *Examples:* Namibrand, Aoraki Mackenzie, Central Idaho.

---

## 3. Product Families (Commerce Derivation)

Products are activated based on a **Commerce Profile** derived from standard classifications and asset readiness.

| Product Family | Derived From (Inputs) | Activation Trigger |
| :--- | :--- | :--- |
| **Masterpiece Prints** | CIDOC E36 (Visual Item) + High-Res Scan | Single "Iconic" asset found. |
| **Thematic Books** | Narrative Depth + Multiple Related Assets | >20 related assets + editorial plan. |
| **Ecological Calendars** | Ramsar (Migration) + Seasonal Assets | 12 monthly-distinct visual assets. |
| **Botanical Cards** | Darwin Core (Taxa) + Illustration Opportunity | Rights-cleared scientific plates. |
| **Cartographic Puzzles** | PostGIS (Geometry) + High-Detail Map | 19th C Topographic or Nautical chart. |
| **Heritage Textiles** | UNESCO ICH (Craft) + Pattern/Motif | Verified decorative motif in collection. |

---

## 4. Tourism Journeys (PostGIS Led)

Tourism journeys use spatial proximity and designation clusters to group places into logical visitor paths.

*   **The Tectonic Trail:** Linking Geoparks along the Mid-Atlantic Ridge or Ring of Fire.
*   **The Flyway Path:** Linking Ramsar sites along major bird migration routes (e.g., East Asian-Australasian Flyway).
*   **The Heritage Loop:** Linking UNESCO Cultural sites within a 500km radius using PostGIS proximity.

---

## 5. Education Journeys (Taxon/Concept Led)

Education journeys are built around scientific concepts and taxonomic groups, cutting across geography.

*   **The Darwinian Lab:** Linking Galápagos, Komodo, and the Great Barrier Reef via `dwc:Taxon` and `Concept:Evolution`.
*   **The Carbon Lungs:** Linking the Amazon, Congo Basin, and Borneo via `UNESCO Biosphere` and `Concept:Climate`.
*   **The Water Temple:** Linking Bali's Subak, Omani Aflaj, and Andean Andenes via `UNESCO ICH` and `Concept:Irrigation`.

---

## 6. Conservation Journeys (IUCN/Ramsar Led)

These journeys highlight the *protection* of nature, using management categories to show the intensity of conservation.

*   **The Wildest Earth:** A tour of Category Ia (Strict Nature) sites where human presence is minimal.
*   **The Living Buffer:** Exploring UNESCO Biosphere "Buffer Zones" where traditional culture protects the core.
*   **The Wetland Pulse:** A deep dive into Ramsar "Criteria 6" sites (supporting 1% of a species population).

---

## 7. ICH-Linked Discovery (Neo4j/Topic Led)

This is the "Deep Intelligence" layer, where physical places are linked to the *intangible knowledge* of those who live there.

*   **The Star Navigators:** Linking `Place:Papahānaumokuākea` to `ICH:Polynesian Wayfinding` via `Neo4j:Concept`.
*   **The Color of the Earth:** Linking `Place:Pisac (Peru)` to `ICH:Quechua Textile Dyeing` via `Neo4j:Material`.
*   **The Song of the Forest:** Linking `Place:Arnhem Land` to `ICH:Songlines` via `Neo4j:Oral_Tradition`.

---

## 8. Summary: The Factory Workflow

1.  **Ingest:** Designation records from UNESCO, Ramsar, IUCN, etc.
2.  **Classify:** Map to standard criteria and CIDOC/Darwin Core concepts.
3.  **Traverse:** Use Neo4j to find related ICH, creators, and stories.
4.  **Activate:** Derive commerce profiles based on asset quality and rights.
5.  **Publish:** Generate place pages, collection rails, and product listings automatically.

---
*NC-PLACES-FACTORY-001 Global Place Strategy produced by Gemini CLI for Nature & Culture*
