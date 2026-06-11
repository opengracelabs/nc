# SA-OSM-001: OSM Tile Service Selection and Attribution Standard

| Field | Value |
|---|---|
| Amendment | SA-OSM-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-11 |
| Authority | DD-OSM-001 Article 10 |
| Supersedes | `docs/implementation/osm_intelligence_plan_v1.md` (in full) |
| Governs | OSM tile service selection, ODbL attribution, and OSM integration boundaries |
| Applies to | All NC surfaces displaying map tiles |
| Exemptions | Earthrise (no map tiles) |

---

## I. Purpose

DD-OSM-001 classified OSM as an Infrastructure Reference — the produced-works tile path is authorized for visual display; all OSM data ingestion into NC canonical tables is permanently prohibited. This standard:

1. Selects the governing tile service for NC production
2. Defines ODbL attribution implementation per surface
3. Formally supersedes the OSM Intelligence Plan v1, which was drafted before DD-OSM-001 and contains provisions that violate DD-OSM-001 Invariants OS-1 through OS-5
4. Defines the permitted OSM integration model going forward

---

## II. Tile Service Selection

### II.1 Primary: Mapbox GL JS

**Ratified tile service: Mapbox GL JS**

| Property | Value |
|---|---|
| Service | Mapbox GL JS |
| Tile type | Vector tiles (MVT), raster tiles (PNG/WebP) |
| Styling | Mapbox Studio — custom NC style required |
| API key | Required — managed as a secret in NC infrastructure |
| ODbL compliance | Mapbox maintains ODbL attribution in tile metadata; NC must surface it per §III |
| Commercial use | Permitted under Mapbox ToS |
| Rate limits | Governed by NC Mapbox account tier |

Mapbox is selected because it provides the richest vector tile styling capabilities, enabling NC place maps to reflect the visual language of the platform (natural heritage, cultural layer, minimal UI chrome) rather than generic navigation.

### II.2 Fallback: Protomaps (self-hosted PMTiles)

When Mapbox is unavailable (outage, account issue, cost constraint), the fallback is self-hosted Protomaps using the PMTiles v3 format.

| Property | Value |
|---|---|
| Service | Protomaps self-hosted |
| Tile source | Protomaps daily planet extracts (ODbL-licensed OSM data) |
| Hosting | NC infrastructure (CDN-served) |
| ODbL compliance | NC directly responsible for attribution; §III applies |
| Cost | Bandwidth-only (no per-tile fee) |

### II.3 Prohibited tile services

The OSM tile CDN (`tile.openstreetmap.org`) is **prohibited for NC production use**. OSM's tile usage policy explicitly forbids heavy use, commercial deployment, and applications without prior agreement. Using OSM's own CDN for commercial NC traffic would violate OSM tile policy and is not authorized.

---

## III. ODbL Attribution Requirements

### III.1 Canonical Attribution Text

```
© OpenStreetMap contributors
```

This text is **exact and immutable**. "OpenStreetMap contributors" must hyperlink to `https://www.openstreetmap.org/copyright` on any web surface where hyperlinking is possible.

For Mapbox-served tiles, the full attribution chain must read:

```
© OpenStreetMap contributors   |   Map data provided by Mapbox
```

The OSM attribution must always appear first and must never be smaller than the Mapbox attribution in any rendered form.

### III.2 Per-Surface Placement Rules

| Surface | Required form | Placement |
|---|---|---|
| Place page map | "© OpenStreetMap contributors" + hyperlink | Map overlay, bottom-right corner (standard cartographic convention) |
| Interactive discovery map | "© OpenStreetMap contributors" + hyperlink | Map overlay, always visible |
| Product listing (if map shown) | Attribution inline with map | Below or overlaid on map image |
| Static map export / print | Full text in map image or caption | Not removable via export |
| Mobile app map view | Attribution chip | Bottom corner, always visible |

### III.3 What does NOT require OSM attribution

- Place pages with no map tile display (text-only, illustration-only)
- Earthrise page (no map tiles)
- Product listings showing only asset images, no map

---

## IV. Permitted OSM Integration Model

This section replaces all provisions of the OSM Intelligence Plan v1. The following describes the ONLY authorized way NC may use OSM.

### IV.1 Authorized: Produced-Works Tile Rendering

NC may render OSM-sourced tiles as produced works (visual images, map displays) via the selected tile service. The following use cases are authorized as **visual rendering only**:

| Intelligence Plan vector | Authorized rendered equivalent |
|---|---|
| `highway=path` trails | Trail layer rendered on tile; no path geometry stored in NC tables |
| `access=restricted` restrictions | Restriction zone rendered on tile; no access tags stored in NC |
| `tourism=viewpoint` viewpoints | Viewpoint markers rendered on tile; no coordinates stored in NC (use GeoNames for NC-anchor coordinates) |
| `amenity=visitor_centre` infrastructure | Infrastructure layer rendered on tile; no building data stored in NC |
| `waterway=canal`, `route=ferry` (Venice) | Canal/ferry layer rendered on tile; no waterway geometry stored in NC |
| `admin_level=8` boundaries | Boundary rendered on tile; no boundary polygon stored in NC |

The rendered map is a produced work under ODbL §4.3. It is not subject to ODbL share-alike.

### IV.2 Prohibited: Data Ingestion and Storage

The following are permanently prohibited under DD-OSM-001 Invariants OS-1–OS-5:

| Prohibited action | Invariant violated |
|---|---|
| Storing any OSM relation ID in any NC table | OS-4 |
| Storing any OSM tag value (highway, access, amenity, etc.) in any NC table | OS-1 |
| Using OSM tags as scoring inputs to the CI Constitution | OS-3 |
| Querying Overpass API and writing results to NC database | OS-1, OS-2 |
| Using any OSM feature as an identity anchor for places | OS-2 (GeoNames is the identity authority) |
| Storing Wikidata P402 (OSM relation ID) values in any NC field | OS-4, DD-WIKIDATA-001 §X.1 |

### IV.3 Overpass API Usage

The Overpass API may be used solely to configure tile rendering parameters (e.g., to determine bounding box for a place's tile extent). Results must not be persisted in any NC database, cache with a TTL beyond the tile render session, or used as inputs to scoring or identity functions.

---

## V. Formal Supersession of OSM Intelligence Plan v1

`docs/implementation/osm_intelligence_plan_v1.md` is **formally superseded** by this standard.

The following provisions of the OSM Intelligence Plan v1 are rescinded:

| OSM Intelligence Plan v1 provision | Reason for rescission |
|---|---|
| "OSM as primary Access & Infrastructure Authority" | DD-OSM-001 classifies OSM as Infrastructure Reference only. No data authority role. |
| OSM Relation IDs listed by place (163151, 183377, 2533338, 44118, 6411191) | Prohibited by Invariant OS-4. These IDs must not be stored in any NC table. |
| "Operational Truth" framing with data integration vectors | No OSM data enters the NC pipeline. Tiles only. |
| Trails & Navigation vector (`highway=path` ingestion) | Tile rendering only; no geometry storage. |
| Access & Governance vector (`access=*` ingestion) | Tile rendering only; no tag storage. |
| Infrastructure & Amenities vector (`amenity=*` ingestion) | Tile rendering only; no building data. |
| Tourism Intelligence vector (`tourism=viewpoint` ingestion) | Tile rendering only; no coordinate storage (GeoNames governs place coordinates). |
| Integration Use Case #1 (Trail-to-Taxon Intersection with stored path data) | Prohibited; tile-based visual overlay is permitted. |
| Integration Use Case #4 (Access-Aware Recommendations filtering on `access=restricted`) | Prohibited as a data-driven filter. Tile display of restricted zones is permitted. |
| Integration Use Case #5 (Infrastructure Proximity scoring within 1km of `amenity=visitor_centre`) | Prohibited. OSM data may not be a CI Constitution scoring input (Invariant OS-3). |
| Overpass API Integration as a "service" with persistent data | Prohibited. Overpass may be used for tile configuration only; no persistence. |
| Tag-to-Concept Mapping to Canonical Vocabulary | Prohibited. OSM tags must not be ingested into the NC concept vocabulary. |

The OSM Intelligence Plan v1 may be retained as a historical document with a supersession notice prepended. It must not be referenced as an active implementation guide.

---

## VI. Implementation Gate

No NC map tile display may go live until:

| Gate item | Check |
|---|---|
| Mapbox account provisioned and API key stored as secret | ☐ |
| NC Mapbox style created (not default "streets" style) | ☐ |
| "© OpenStreetMap contributors" attribution rendered on all map tiles at correct placement | ☐ |
| Hyperlink from "OpenStreetMap contributors" to openstreetmap.org/copyright confirmed working | ☐ |
| No OSM Relation IDs present in any NC database table | ☐ |
| Protomaps fallback tested and confirmed operational | ☐ |

This gate is required for Attribution Launch Gate B-2. It is a pre-condition for the two-human activation sign-off (Launch Gate E).

---

## VII. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Standards Amendment | ☑ DRAFT | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*SA-OSM-001 — drafted 2026-06-11*  
*Required by: DD-OSM-001 Art. 10 · Supersedes: osm_intelligence_plan_v1.md · Clears: NC-PILOT-001-FGR Condition C-3 · Attribution Gate B-2*
