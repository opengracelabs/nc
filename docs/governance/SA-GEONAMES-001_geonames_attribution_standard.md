# SA-GEONAMES-001: GeoNames CC BY 4.0 Attribution Standard

| Field | Value |
|---|---|
| Amendment | SA-GEONAMES-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-11 |
| Authority | DD-GEONAMES-001 Article 13 |
| Governs | CC BY 4.0 attribution for all GeoNames data used by NC |
| Applies to | All NC surfaces displaying place-derived data from GeoNames |
| Exemptions | Earthrise (S-3 cosmic anchor exception — no GeoNames ID) |

---

## I. Purpose

GeoNames is NC's sole Identity and Evidence Authority for place data. Under DD-GEONAMES-001, GeoNames is licensed CC BY 4.0 — the only NC authority source that requires attribution. This standard defines the exact attribution texts, placement rules, API field specifications, and implementation gates that satisfy the CC BY 4.0 obligation.

Non-compliance with this standard is a rights violation under DD-GEONAMES-001 Invariant GN-4 and constitutes a failure of Attribution Launch Gate B-1 (NC-PILOT-001 §VII).

---

## II. Canonical Attribution Text

### II.1 Full Attribution (required on place pages and product listings)

```
Geographic data © GeoNames (geonames.org) — CC BY 4.0
```

This text is **exact and immutable**. It may not be shortened, reordered, or substituted. "GeoNames" must hyperlink to `https://www.geonames.org` on any web surface where hyperlinking is possible.

### II.2 Compact Attribution (permitted in space-constrained surfaces)

```
© GeoNames — CC BY 4.0
```

The compact form is permitted only when the full form cannot fit due to layout constraints. It may never appear on place pages or product listings where the full form is feasible.

### II.3 Machine-Readable Attribution

In all NC API responses for place entities, include the following field at the root level of the place object:

```json
"nc:geonames_attribution": {
  "text": "Geographic data © GeoNames (geonames.org) — CC BY 4.0",
  "url": "https://www.geonames.org",
  "license": "https://creativecommons.org/licenses/by/4.0/"
}
```

---

## III. Per-Surface Placement Rules

| Surface | Required form | Placement | Required when? |
|---|---|---|---|
| Place page | Full | Footer, visible without scroll on desktop | Always, for all terrestrial places |
| Product listing | Full | Below asset attribution, above purchase CTA | Always, when asset is geo-anchored to a place |
| NC API JSON (place entity) | Machine-readable (§II.3) | Root-level field on place object | Always |
| IIIF manifest (if applicable) | Full | `requiredStatement.value` field | When IIIF manifest includes place-derived metadata |
| Email / print / download PDF | Full | Footer or credits section | When document includes place-derived data |
| Map tile display | Not required separately | OSM tile attribution satisfies map layer; GeoNames attribution covers place data | See SA-OSM-001 for map-layer rules |
| Mobile app | Full or compact | Page footer or dedicated credits screen | Always |

### III.1 Co-attribution ordering (when multiple attributions are present)

When a place page carries multiple attribution obligations (e.g., NASA nonendorsement + GeoNames CC BY 4.0 + OSM ODbL), display in this order:

1. Asset credit (NASA, NOAA, institution)
2. Geographic data: GeoNames CC BY 4.0
3. Map tiles: OSM ODbL (if tiles present)
4. Any additional institutional credit

The federal nonendorsement line (NASA/NOAA) must always appear closest to the asset it governs and must not be merged with GeoNames attribution.

---

## IV. Implementation Gate

No NC place page may be made publicly visible until the following have been confirmed:

| Gate item | Check |
|---|---|
| GeoNames full attribution text present in place page footer | ☐ |
| `nc:geonames_attribution` field populated on place API endpoint | ☐ |
| "GeoNames" hyperlinked to geonames.org on web surfaces | ☐ |
| Earthrise page: attribution NOT required (exemption logged in Technical Plan) | ☐ |

This gate is required for Attribution Launch Gate B-1. It is a pre-condition for the two-human activation sign-off (Launch Gate E).

---

## V. Scope and Exclusions

### V.1 What this standard governs

- All place entity records in the NC `places` table that carry a `geonames_id`
- All NC web pages, API responses, and documents that expose GeoNames-derived data (coordinates, feature names, feature codes, administrative hierarchy)
- Place-anchored product listings

### V.2 What this standard does NOT govern

- Wikidata attribution (CC0 — no attribution required; governed by DD-WIKIDATA-001)
- GBIF attribution (CC0 — no attribution required; governed by SA-GBIF-001)
- OSM tile attribution (ODbL — governed by SA-OSM-001)
- NASA / NOAA nonendorsement (governed by DD-NASA-001, DD-NOAA-001)
- Media file copyright attribution (governed per institution DD)

### V.3 Earthrise exemption

The Earthrise place anchor is subject to an S-3 provisional exception (NC-PILOT-001 §IX.1). No GeoNames ID exists for the Earthrise vantage point; therefore, no GeoNames attribution is required on the Earthrise place page. The exemption must be noted in the Technical Plan and in the Earthrise place record (`geonames_exemption: "cosmic_anchor_S3_provisional"`).

The 60-day deadline for Standards Constitution amendment or proxy-place resolution is unchanged.

---

## VI. Feature Code Routing (CI Constitution Pointer)

GeoNames `fcode` values govern which CI Constitution formula is applied to place-anchored assets. This routing must not be overridden. Operators must not substitute alternative feature codes from other authorities (OSM tags, Wikidata types) when GeoNames `fcode` is available. This rule is governed by DD-GEONAMES-001 Invariant GN-5 and the CI Constitution v1.2; it is not re-litigated here.

---

## VII. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Standards Amendment | ☑ DRAFT | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*SA-GEONAMES-001 — drafted 2026-06-11*  
*Required by: DD-GEONAMES-001 Art. 13 · Clears: NC-PILOT-001-FGR Condition C-2 · Attribution Gate B-1*
