# Standards Constitution v1.0

**Role:** Chief Curator / Architect  
**Objective:** Define the formal mapping of Nature & Culture subsystems to global standards to ensure interoperability, trust, and long-term preservation.

---

## 1. The Standards Hierarchy: "Adopt, Map, Extend, Invent Last"

Nature & Culture prioritizes the use of established global standards to ensure that our "Place-Centered" data can be understood by search engines, museums, and scientific repositories.

1.  **Adopt:** Use the standard as the native schema for the subsystem.
2.  **Map:** Maintain a 1:1 crosswalk between internal data and the standard.
3.  **Extend:** Add custom properties to a standard only when no alternative exists.
4.  **Invent Last:** Create a new schema only if the requirement is unique to Nature & Culture (e.g., Atmospheric Runtime).

---

## 2. Subsystem Mapping Matrix

| Subsystem | Primary Standard | Role | strategy |
| :--- | :--- | :--- | :--- |
| **Knowledge Graph** | **CIDOC CRM** | Conceptual backbone (Events, People, Things). | **Adopt** |
| **Taxonomy / Bio** | **Darwin Core** | Biological occurrence and species data. | **Adopt** |
| **Presentation** | **IIIF (v3.0)** | High-fidelity media delivery (Images, A/V, 3D). | **Adopt** |
| **Web Discovery** | **Schema.org** | SEO and AI-agent readability (JSON-LD). | **Map** |
| **Spatial / Geography** | **GeoJSON / PostGIS** | Coordinate and boundary data. | **Adopt** |
| **Authority Files** | **Wikidata / GeoNames** | Global IDs for places and entities. | **Map** |
| **Curation Control** | **SKOS / Dublin Core** | Controlled vocabularies and basic discovery. | **Adopt** |
| **Provenance** | **PROV-O** | Chain of custody and data lineage. | **Adopt** |
| **Preservation** | **PREMIS** | Technical metadata for long-term digital health. | **Adopt** |
| **Cultural Portal** | **Europeana EDM** | Mapping for global cultural aggregation. | **Map** |
| **Data Exchange** | **JSON-LD** | The universal language for all metadata. | **Adopt** |

---

## 3. Structural Crosswalks (The "Bridge" Rules)

### 3.1 The Event-Centric Bridge
Nature & Culture is an "Event-First" platform. All standards must converge on the **Event** (E5 Event in CIDOC CRM).

*   **CIDOC CRM:** `E5 Event` (e.g., The Hayden Survey).
*   **Darwin Core:** `dwc:Event` (The collection event for a specimen).
*   **PROV-O:** `prov:Activity` (The creation or modification of a digital asset).
*   **Schema.org:** `schema:Event` (The historical or discovery event).

### 3.2 The Place-Centered Bridge
*   **GeoNames:** Every Place in NC must map to a `gn:Feature`.
*   **CIDOC CRM:** Every Place is an `E53 Place`.
*   **GeoJSON:** Geometry is stored as `Point`, `Polygon`, or `MultiPolygon`.
*   **Wikidata:** Every Place must have a `wd:Q-Number` for global linkage.

### 3.3 The Media Bridge
*   **IIIF Canvas:** The universal container for all media.
*   **CIDOC CRM:** The IIIF resource is an `E31 Document` depicting an `E22 Human-Made Object`.
*   **Darwin Core:** Linked via `dwc:associatedMedia`.

---

## 4. Subsystem Implementation Guidance

*   **Knowledge Worker:** Must emit **CIDOC CRM** compatible RDF/JSON-LD.
*   **Discovery Worker:** Must generate **Schema.org** rich snippets for all public pages.
*   **Ingestion Worker:** Must normalize incoming institutional data to **Darwin Core** (Nature) or **EDM** (Culture).
*   **Preservation Worker:** Must audit assets against **PREMIS** health markers.

---

## 5. "Invent Last" Exceptions (The NC Namespace)

The following properties are unique to Nature & Culture and exist in the `nc:` namespace:
*   `nc:atmosphere`: Vibe, Lighting, and Soundscape parameters.
*   `nc:opportunity`: The link between a Place, a Collection, and a Commercial Product.
*   `nc:curatorNote`: Internal expert guidance that doesn't map to standard provenance.

---

**Next Steps:**
*   Implement the **JSON-LD context** for all public API responses.
*   Establish the **Wikidata Reconciliation** worker for automatic entity linking.
*   Audit the **Smithsonian Ingestion** against the Europeana EDM crosswalk.
