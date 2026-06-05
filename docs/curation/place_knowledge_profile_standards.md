# Place Knowledge Profile: Standards Alignment

The **Place Knowledge Profile** (formerly shorthand "Place Genome") is the canonical multi-dimensional record of a flagship location. It bridges the gap between biological data (Natural History) and cultural narratives (Fine Art/History).

## 1. Core Taxonomy
A complete **Place Knowledge Profile** requires the integration of the following asset classes:

| Shorthand | Asset Class | Standard Alignment |
| :--- | :--- | :--- |
| **NH** | Natural History Illustration | Darwin Core (DwC), Dublin Core |
| **FA** | Fine Art | CIDOC CRM (E22 Man-Made Object), IIIF |
| **HM** | Historic Maps | CIDOC CRM (E36 Visual Item), Schema.org/Map |
| **PH** | Photography | CIDOC CRM (E38 Image), IIIF |
| **FJ** | Field Journals | CIDOC CRM (E31 Document), TEI |
| **SS** | Scientific Surveys | ISO 19115 (Metadata for Geographic Information) |
| **ER** | Ethnographic Records | CIDOC CRM (E7 Activity), SKOS |
| **AU** | Audio | CIDOC CRM (E73 Information Object), Schema.org/AudioObject |

## 2. Standards Mapping

### Cultural Heritage (CIDOC CRM / ISO 21127)
*   **Place Identification:** `E53 Place`
*   **Asset Linkage:** `P138 represents` (e.g., A Moran painting *represents* Yellowstone)
*   **Event Attribution:** `E7 Activity` (e.g., The 1871 Hayden Expedition)

### Natural History (Darwin Core)
*   **Taxonomic Identity:** `dwc:Taxon` (e.g., *Bison bison*)
*   **Spatiotemporal Evidence:** `dwc:Occurrence` (Linked to `dwc:Event`)

### Web Discovery (Schema.org)
*   **Place:** `schema:Place`
*   **Collection:** `schema:Collection`
*   **CreativeWork:** `schema:CreativeWork` (for specific assets)

## 3. Coherence Mechanism
Coherence is maintained by anchoring all disparate assets to a single **Place Knowledge Profile** URI. This ensures that a scientific specimen (DwC) and a landscape painting (CIDOC CRM) are semantically unified under the same geographic and narrative entity.
