# Universal Public Domain Media Substrate v1

**Role:** Chief Curator / Architect  
**Objective:** Design a future-proof foundation for all cultural and natural media types, ensuring interoperability, discovery, and atmospheric fidelity.

---

## 1. Architectural Philosophy: The "Canvas-First" Model

To avoid redesigning for every new media type, Nature & Culture adopts the **IIIF Presentation API 3.0** as its core substrate. We move away from "File-Based" thinking to "Canvas-Based" thinking.

### The Universal Canvas
A **Canvas** is a virtual container with a coordinate system (X, Y, Z) and a temporal dimension (Duration). Every piece of media—regardless of its format—is "painted" onto a Canvas.

| Media Type | Substrate Implementation |
| :--- | :--- |
| **Images / Photos / Posters** | Painted as `Image` annotations on a 2D Canvas. Supports Deep Zoom. |
| **Maps** | Geo-referenced `Image` annotations with tiling (XYZ/WMTS) overlays. |
| **Books / eBooks** | A `Manifest` containing a sequence of Canvases (pages) with OCR text annotations. |
| **Audio / Audiobooks** | A Canvas with `Duration` but no dimensions, with an `Audio` body. |
| **Film / Video** | A Canvas with both `Dimensions` and `Duration`, with a `Video` body. |
| **3D Models** | A `Scene` (3D Canvas) containing `3DModel` bodies (glTF/USDZ). |
| **Datasets** | Linked as a `seeAlso` resource or a `Dataset` annotation for raw analysis. |

---

## 2. Core Metadata Substrate: Schema.org + Linked Data

Every asset in the substrate is represented as a **JSON-LD** object, ensuring search engines and AI agents can "understand" the content without proprietary parsing.

### The "Core" Object
```json
{
  "@context": [
    "http://iiif.io/api/presentation/3/context.json",
    { "schema": "http://schema.org/", "nc": "https://natureandculture.org/ns#" }
  ],
  "id": "https://nc.org/assets/000001",
  "type": "Manifest",
  "schema:type": "schema:CreativeWork",
  "label": { "en": [ "Yellowstone Map 1872" ] },
  "nc:atmosphere": {
    "vibe": "Ethereal",
    "lighting": "Golden Hour",
    "soundscape": "Boreal Forest Wind"
  }
}
```

---

## 3. Supporting Diverse Media (The "Substrate Matrix")

| Media Category | Primary Format | Interoperability Standard | Key Strategy |
| :--- | :--- | :--- | :--- |
| **Visual** | JPEG2000 / WebP | IIIF Image API | Use tiled pyramid files for "Infinite Zoom." |
| **Cartographic** | GeoTIFF / MBTiles | OGC / IIIF Maps | Layer historical maps over modern satellite data. |
| **Textual** | ALTO / HOCR / EPUB | IIIF Presentation | Treat pages as individual Canvases for deep search. |
| **Auditory** | FLAC / AAC | IIIF A/V API | Support spatial audio (Binaural) as a primary layer. |
| **Cinematic** | H.265 / AV1 | IIIF A/V API | Stream via HLS/DASH with synchronized captions. |
| **Spatial** | glTF 2.0 / USDZ | IIIF 3D (Experimental) | Use Draco compression for web-ready 3D performance. |
| **Informational** | JSON / CSV / Parquet | W3C Data Cube | Provide raw downloads + interactive visualizers. |

---

## 4. Design & Experience Extensions

To fulfill the **Experience Strategy**, the substrate includes a "Curation Layer" that persists with the media.

1.  **Atmospheric Anchors:** Every asset can have a "Soundscape" or "Lighting Profile" attached as a IIIF Annotation. When the asset is loaded, the environment (the "Atmospheric Runtime") adapts automatically.
2.  **Contextual Bridges:** AI-generated links (`nc:relatedBy`) that connect a 3D scan of a fossil to a 19th-century illustration of the same species and the dataset of its current habitat.
3.  **The "Close Look" Anchor:** A specialized annotation type that marks "Points of Interest" on any media, allowing for guided tours within a single asset.

---

## 5. Universal Principles for the Substrate

1.  **Format Agnostic:** The UI doesn't care if it's a PNG or a GLB; it only cares about the **Canvas** it's rendering.
2.  **Stateless Fidelity:** The substrate holds the metadata for *how* an object should feel (Lighting, Sound), while the UI/App decides *how* to render it.
3.  **Recursive Discovery:** Collections can contain Manifests, and Manifests can contain other Manifests (e.g., a "Box" containing a "Book" and a "Map").
4.  **Open by Default:** All media URI's are stable, permanent, and interoperable, allowing other institutions to "mount" NC assets into their own viewers.

---

**Next Steps:**
*   Implement the `BaseAsset` schema in the `schemas/core/` directory.
*   Convert the *Smithsonian Top 100* JSON data to this IIIF-compatible substrate.
*   Build the "Media Gateway" worker to handle multi-format ingestion.
