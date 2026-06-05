# Ingestion Specification: 1871 Hayden Survey Map
# Target: Yellowstone Place Knowledge Profile
# Status: Ready for Ingestion (Post-Migration 18)

## 1. Metadata Package (Asset Schema)

```json
{
  "asset_metadata": {
    "source_id": "LOC_GMD",
    "source_url": "https://www.loc.gov/item/74692510/",
    "asset_type": "image",
    "mime_type": "image/tiff",
    "language": "en",
    "place_id": "{{ YELLOWSTONE_UUID }}",
    "ingest_id": "ingest_2026_06_05_loc_yellowstone_maps",
    "premis_original_name": "g4262y4_1871_h4.tif",
    "premis_creating_application": "U.S. Geological Survey of the Territories",
    "agent_notes": {
      "curator_note": "Primary foundational map for the Yellowstone collection. High resolution TIF required for wall art production.",
      "standards_alignment": {
        "cidoc_crm": "E36 Visual Item",
        "schema_org": "http://schema.org/Map"
      }
    }
  },
  "knowledge_profile_update": {
    "place_asset_profile": {
      "asset_class": "HM",
      "status": "covered",
      "provenance": "Library of Congress Geography and Map Division"
    }
  }
}
```

## 2. Collection Relationships

*   **Parent Collection:** Yellowstone Heritage Collection
*   **Sibling Assets (1871 Expedition):**
    *   **Fine Art:** Thomas Moran, *The Grand Canyon of the Yellowstone* (1872)
    *   **Photography:** William Henry Jackson, *Old Faithful Geyser* (1872)
*   **Thematic Cluster:** "The Blueprint of Wilderness"
*   **Archetype:** Geological Power / Scientific Frontier

## 3. Educational Narrative: "The Blueprint of Wilderness"

The 1871 Hayden Survey Map is the foundational document of the National Park movement. Before its publication, the wonders of Yellowstone were dismissed as frontiersman's "tall tales." By providing precise topographic coordinates for Old Faithful, Yellowstone Lake, and the Grand Canyon of the Yellowstone, Ferdinand V. Hayden’s team moved the region from the realm of myth into the realm of scientific fact. 

This map serves as a "Deep Time" baseline, allowing students to compare 19th-century geyser locations with modern seismic and geothermal data. It is the primary tool for teaching how boundaries and scientific evidence can influence political action and environmental preservation.

## 4. Commerce Narrative: "The Aesthetic of Discovery"

As a commercial asset, the Hayden Survey Map is the "Masterwork" anchor for the Yellowstone product line. Its clean, technical lines and historic patina appeal to collectors of cartography and American history. 

**Target Products:**
*   **Wall Art:** Premium archival linen prints (Full Scale).
*   **Portfolio Books:** The centerpiece of the "Expedition 1871" commemorative folio.
*   **Stationery:** Minimalist "Surveyor" series postcards and journals.
*   **Educational Puzzles:** A 1,000-piece "Trace the Expedition" puzzle.

The high-resolution TIF from the Library of Congress ensures that every fine-line survey mark is preserved, maintaining the "Museum Quality" promise of the Nature & Culture brand.
