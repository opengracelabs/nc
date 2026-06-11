# DD-OSM-001: OpenStreetMap — Governance Review

| Field | Value |
|---|---|
| Document | DD-OSM-001 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-11 |
| Institution Number | **Not Assigned** — Infrastructure Reference; not a content institution, not an Identity/Evidence Authority |
| Decision | APPROVE WITH CONDITIONS |
| Conditions | OSM data may never enter NC canonical PostgreSQL tables. Consumption restricted to produced-works path (tile rendering services). SA-OSM-001 required to govern attribution and tile service policy. |
| Prior Rulings | IFC v1 Article 1.2 · DD-GEONAMES-001 Article 10 + OQ-1 (2026-06-11) · Standards Constitution v1.0 Article 17 (Invariant S-3) |

---

## I. Institution Overview

**OpenStreetMap (OSM)**
- Operator: OpenStreetMap Foundation (OSMF), United Kingdom
- URL: https://www.openstreetmap.org
- Governance: Community-contributed open geographic database; copyright held by OpenStreetMap contributors; licensed by OSMF under ODbL 1.0
- Core product: Collaborative global map database — vector geometry (points, lines, polygons, relations), tags (key-value attributes), place names, road networks, building footprints, administrative boundaries, natural features

OSM is the world's foremost open geographic database. Contributors map physical reality — roads, buildings, coastlines, administrative boundaries, land use polygons, natural areas — using GPS traces, aerial imagery, and local knowledge. OSM provides polygon boundary geometry that GeoNames does not supply: park boundaries, island outlines, reef extents, administrative boundary polygons.

OSM does not hold illustrations, photographs, artworks, or media in the NC commercial sense. OSM is a geographic vector database.

---

## II. ODbL Analysis

### II.1 The License

OSM data is licensed under **Open Database License 1.0 (ODbL 1.0)**, published by the Open Data Commons project. ODbL was specifically designed for databases and is fundamentally different from any Creative Commons license. Understanding ODbL requires understanding four distinct objects it governs:

| ODbL object | Definition | Share-alike applies? |
|---|---|---|
| **Database** | A collection of data arranged systematically or methodically | Yes — share-alike applies to derivative databases |
| **Derivative Database** | A database based upon the whole or a substantial part of the OSM database | Yes — must be released under ODbL |
| **Produced Work** | A work produced from the database, not itself a database (e.g., a rendered map image, a printed map, a report, a spatial visualization) | No — produced works are NOT governed by ODbL share-alike |
| **Collective Database** | A database that includes OSM as a distinct component without integration | Potentially exempt if OSM is kept fully isolated |

### II.2 Share-Alike Obligation (Section 4.2b)

ODbL's share-alike clause (§4.2b) states:

> "If You Publicly Use any Derivative Database, You must also offer that Derivative Database under the terms of this License."

This is the critical clause. Its implications:

**What triggers share-alike:**
- Storing OSM vector data (coordinates, geometry, tags) in NC's PostgreSQL tables
- Transforming OSM geometry to a different format and storing it in NC tables
- Selecting a subset of OSM features (e.g., national park boundaries) and storing them in `places`
- Joining OSM data with NC's own data to produce a new table

Any of these operations produces a **Derivative Database** and triggers the share-alike obligation.

**What does share-alike mean in practice for NC:**
- NC would be required to publish its Derivative Database (the tables containing OSM data) under ODbL
- ODbL requires the published database to be available to anyone without restriction
- "Publicly Use" under ODbL §1.0(c) means making the database available or using it to produce distributed works — this includes operating a commercial web service that queries the database to serve place page content

### II.3 The Share-Alike / Commercial Doctrine Conflict

Share-alike applied to NC's `places` table would require NC to publish that table under ODbL. The `places` table contains or connects to:
- `places.geonames_id` — place identity
- `places.population` — TAS scoring input
- `places.feature_code` — CI Constitution routing input
- `illustration_opportunity_places.relevance_score` — commercial scoring
- Links to `commerce_opportunities` records

Even if OSM geometry were isolated to a separate column or table, the ODbL share-alike obligation follows the data: if OSM geometry is used to derive NC's scoring outputs — if park boundary polygons inform which illustration opportunities are tagged to Yellowstone — then those scoring outputs trace to OSM geometry as a source, and the database containing them may constitute a Derivative Database.

**This conflict is structural.** NC cannot publish its commercial intelligence layer (scoring, routing, opportunity records) under ODbL. Doing so would:
- Destroy the competitive moat of NC's scored catalog
- Require NC to release its place-relevance and COS scores to any party under ODbL terms
- Violate NC's Strategic Directive ("the scores, the tiers, the anchor classifications, the commerce routing — are unmistakably NC's own")

There is no legal workaround that simultaneously stores OSM geometry in NC's PostgreSQL database AND protects NC's commercial intelligence layer from ODbL share-alike obligations.

### II.4 The Produced Works Exception (Section 4.3)

ODbL §4.3 provides the key safe harbor:

> "A Produced Work does not require you to release it under ODbL, provided that the Produced Work is not itself a database."

**A rendered map tile, a boundary image, or a polygon displayed in a browser is a Produced Work, not a database.** It is the visual output of OSM data, not a re-publication of the OSM database itself.

**Safe paths under the Produced Works exception:**
- Displaying OSM-based map tiles on NC place pages via a tile rendering service (Mapbox, CARTO, OpenLayers with OSM tiles, Stamen)
- Displaying boundary outlines as rendered SVG or canvas graphics (the graphic is the produced work; the underlying OSM geometry never enters NC's database)
- Consuming a third-party geocoding API that uses OSM data internally — the API response is a Produced Work

**Unsafe paths regardless of produced works framing:**
- Storing the API-returned coordinates in `places.geom` — at that point NC has created a derivative database
- Caching OSM geometry polygons in NC's database for repeated use — caching constitutes derivative database creation
- Deriving `places.boundary_polygon` from OSM and storing it — same issue

**The critical line:** OSM data may cross the NC boundary as a visual rendering. It may not cross the NC boundary as structured data in NC's canonical store.

### II.5 The Collective Database Path — Analyzed and Rejected

ODbL §10.4 provides a Collective Database path: a database that merely aggregates OSM with other datasets without integration may not trigger share-alike if OSM remains distinct.

Arguments that NC could use the Collective Database path:
- Store OSM boundary data in a separate, isolated schema (`osm_boundaries` table, not `places`)
- Never join OSM data with NC's scoring tables
- Make `osm_boundaries` publicly available under ODbL independently

**Rejected for three reasons:**

**Reason 1 — Functional dependency.** The reason NC wants OSM boundary geometry is to display boundaries on place pages alongside NC's scored illustration catalog. That display creates a functional dependency: OSM boundary data is queried in the context of serving NC's commercial place pages. OSMF's legal interpretation guidance indicates that serving a commercial product that queries a Collective Database OSM component likely triggers "Publicly Use" under §1.0(c), pulling the database — including the NC-commercial components — into ODbL scope.

**Reason 2 — Operational complexity.** Maintaining a strict, never-integrated OSM partition alongside NC's commercial intelligence layer is operationally fragile. A single JOIN in a query, a single foreign key, a single derived field that reads from `osm_boundaries` to populate a `places` column transforms the Collective Database into a Derivative Database. The governance risk of maintaining this boundary at the code level (across all workers, all queries, all schema migrations) is untenable.

**Reason 3 — Materiality.** Even if the Collective Database argument succeeded legally, it would require NC to publicly publish a subset of the OSM database under ODbL as a standalone dataset. This creates data publication obligations for a company whose strategic directive is to own and protect its commercial intelligence. The cure introduces an operational cost greater than the problem solved.

### II.6 Attribution Obligations

Regardless of whether NC uses OSM data directly or via produced works (tile services), ODbL §4.2a requires attribution:

> "You must include a notice associated with the Database reasonably calculated to make any Person that uses, makes available, or redistributes the Database or a Derivative Database aware that Database has been used in the making of the Produced Work."

For tile-service produced works, the standard form is:
```
© OpenStreetMap contributors
```
Displayed on any page, product, or output that renders OSM-based tiles or boundary graphics.

---

## III. Governance Classification Ruling

### III.1 The Three Governance Options

**Option 1 — Identity and Evidence Authority (parallel to GBIF, Wikidata, GeoNames).** OSM as a data source whose structured content enters NC's canonical PostgreSQL tables. Requires ODbL compliance — triggers share-alike for the `places` table and connected NC commercial intelligence. **The ODbL conflict analysis in §II makes this option incompatible with NC's commercial doctrine.**

**Option 2 — Infrastructure Reference.** OSM consumed only via the produced-works path — tile rendering services, boundary visualization, geocoding APIs — as a display and navigation layer. OSM geometry never enters NC's canonical data layer. NC's commercial intelligence is never exposed to ODbL share-alike.

**Option 3 — Complete Rejection.** OSM not used in any capacity. Place boundary visualization deferred until an ODbL-clean alternative is available.

### III.2 Option 1 (Identity/Evidence Authority): REJECTED

The ODbL share-alike conflict is structural and unresolvable under NC's commercial doctrine. Option 1 is rejected on three independent grounds:

**Ground 1 — Derivative database obligation.** Storing OSM geometry in `places` creates a Derivative Database subject to ODbL §4.2b share-alike. NC cannot comply with this obligation without exposing its commercial intelligence layer under ODbL. This is categorically incompatible with the Strategic Directive's protection of NC's scoring and routing as proprietary.

**Ground 2 — No superseding identity need.** GeoNames already satisfies NC's place identity requirements (Invariant S-3, Standards Constitution v1.0 Article 17). OSM would add geometry depth, not identity authority. There is no governance gap in place identity that OSM must fill. GeoNames is constitutionally sufficient for place identity. Adding OSM as an Identity Authority would require overriding S-3 without resolving the ODbL conflict — a double violation.

**Ground 3 — IFC v1 Article 1.2 pre-classification.** IFC v1 Article 1.2 lists OSM as an "Identity and Reference Authority" governed by Standards Constitution v1.0. The pre-classification was a preliminary designation, not a formal governance ruling. DD-OSM-001 is the first formal governance analysis of OSM for NC. That analysis reveals that the Identity Authority classification — which implies structured data storage in NC canonical tables — is incompatible with ODbL. The IFC v1 pre-classification is therefore revised by this DD: OSM is reclassified from "Identity and Reference Authority" to "Infrastructure Reference."

### III.3 Option 3 (Complete Rejection): REJECTED

OSM is not strictly necessary at current NC scope. GeoNames centroid coordinates and the Wireframe Constitution's current place page designs do not require polygon boundary geometry. However, Option 3 forecloses future place boundary visualization and is unnecessarily absolute.

The produced-works path (Option 2) is legally sound, operationally clean, and preserves future boundary visualization capability. Complete rejection is unwarranted given that a compliant use path exists.

### III.4 Option 2 (Infrastructure Reference): RATIFIED

**OSM is ratified as an Infrastructure Reference under the produced-works path.**

This is a new governance classification not held by any other NC data source. It differs from Identity/Evidence Authority in a fundamental way:

| Classification | Data enters NC canonical tables? | ODbL share-alike applies? |
|---|---|---|
| Identity Authority (GBIF, Wikidata, GeoNames) | Yes | N/A (CC0 or CC BY, no share-alike) |
| Evidence Authority | Yes (evidence payloads) | N/A |
| **Infrastructure Reference (OSM)** | **No — permanently prohibited** | **Not triggered (produced works only)** |

An Infrastructure Reference is a system whose outputs NC consumes for display, navigation, or user experience — not for data storage, scoring, or commercial routing. OSM tile services render maps on NC place pages. The tiles are a visual layer, not a data layer.

This classification also governs how third-party services that use OSM internally (Mapbox, CARTO, Stamen) relate to NC's licensing posture: NC's contract is with the third-party service, not with OSMF. The third-party service's ODbL compliance is its own obligation; NC's produced-works consumption of the rendered output does not inherit ODbL share-alike obligations.

---

## IV. Identity Authority Analysis

### IV.1 Ruling: OSM is Not an Identity Authority for NC

GeoNames is NC's place identity authority (Standards Constitution v1.0 Article 17, Invariant S-3). OSM is not a name authority — it is a geometry database. OSM feature IDs (numeric `osm_id` values) are not stable global name authorities; they change when features are merged, split, or re-tagged by contributors. OSM has no equivalent of GeoNames' stable integer `geonameId` as a persistent cross-system identifier.

**Even if ODbL were not an issue, OSM would not qualify as NC's place identity authority** because:
- OSM feature IDs are mutable (contributors can delete and recreate features)
- OSM has no formal identity authority governance (no OSMF commitment to ID stability)
- GeoNames already provides stable identity anchors mapped to every feature NC will ever need

### IV.2 No `osm_id` Column in NC Schema

No OSM feature ID (`osm_id`, `osm_type`, or equivalent) may be stored in any NC canonical table. Adding an `osm_id` to `places` would:
1. Constitute storage of OSM-derived data — triggering derivative database analysis
2. Create a dependency on an unstable identifier that OSMF does not guarantee
3. Imply an identity authority role that this DD explicitly rejects

---

## V. Place Authority Analysis

### V.1 Ruling: OSM is Not NC's Place Data Authority

GeoNames is NC's place data authority. OSM's potential contribution — polygon boundary geometry — is a display enhancement, not a data authority function. The distinction:

| Function | Authority | NC table |
|---|---|---|
| Place identity (what place is this?) | GeoNames (geonames_id) | `places.geonames_id` |
| Place type (what kind of place?) | GeoNames (feature_code) | `places.feature_code` |
| Place coordinates (where is it?) | GeoNames (lat/lng) | `places.geom` |
| Place population | GeoNames | `places.population` |
| Place name authority | GeoNames (alternateNames) | `places.alternate_names` |
| **Place boundary polygon (visual display)** | **OSM (tile service only)** | **Not stored in NC** |

Boundary polygon display is an Infrastructure Reference function. It is not a data authority function. The polygon is rendered by a tile service and displayed in a user's browser; it does not change any NC data record.

### V.2 When Boundary Geometry Is Needed

The only governed NC use case for OSM boundary geometry is visual display of place boundaries on Wireframe Constitution place pages. This use case:
- Does not require storing OSM polygons in NC's database
- Can be served by Mapbox, OpenLayers + OSM tiles, CARTO, or equivalent tile services
- Requires ODbL attribution ("© OpenStreetMap contributors") on any page that renders OSM-based tiles

No future expansion of this use case to include NC database storage of OSM geometry is authorized by this DD. Such expansion would require DD-OSM-002.

---

## VI. Infrastructure Reference Governance

### VI.1 Permitted Uses (Produced Works Path)

The following OSM-derived uses are governed and permitted:

| Use | Form | ODbL status | NC storage? |
|---|---|---|---|
| Map tile display on place pages | Raster tiles via tile service (Mapbox, CARTO, OSM tile CDN) | Produced work — no share-alike | No |
| Place boundary outline on place pages | Rendered boundary via tile/vector tile service | Produced work — no share-alike | No |
| Geocoding lookups via OSM-based service (Nominatim, Mapbox Geocoding API) | API response used for display only | Produced work — API response is a produced work | No |
| Administrative boundary outlines on collection/atlas pages | Rendered via tile service | Produced work | No |

### VI.2 Prohibited Uses (All Permanent)

**OS-1 — No OSM data in canonical tables.** No OSM-sourced data may be stored in any NC canonical PostgreSQL table, including but not limited to: `places`, `collections`, `source_item`, `media_file`, `media_rights`, `illustration_opportunities`, `commerce_opportunities`. This prohibition is permanent. It applies to:
- OSM geometry (points, lines, polygons, relations)
- OSM tags (key-value attributes)
- OSM feature IDs (`osm_id`, `osm_type`)
- Derived data whose derivation trace includes OSM vectors as a source

**OS-2 — No OSM-sourced schema fields.** No NC database migration may add a column that stores OSM-derived data. This applies to any table, not just `places`. A migration that adds `places.boundary_polygon` and populates it from OSM vectors violates OS-1.

**OS-3 — No OSM scoring input.** OSM geometry may not be used as an input to any NC scoring formula (COS, TAS, place_relevance_score, or any CI Constitution formula). Using a park polygon area from OSM to compute a TAS score would create a derivation trace from OSM to a scored NC record — potentially triggering derivative database obligations for the scored record.

**OS-4 — No osm_id storage.** No OSM feature identifier may be stored in any NC table as a crosswalk, foreign key, or advisory field.

**OS-5 — No caching of OSM geometry.** NC infrastructure (workers, caches, message queues, S3 buckets, Redis) may not cache OSM vector geometry payloads. Caching constitutes storage and would create a derivative database. Tile service response caching (raster tiles, vector tile images) is permitted — cached images are produced works, not cached data.

**OS-6 — Attribution required.** Any NC page, product, or API response that renders OSM-based tiles or boundary graphics must display "© OpenStreetMap contributors" in a visible location per ODbL §4.2a. This attribution must survive across all environments (staging, production, partner embeds).

### VI.3 Tile Service Governance

NC must consume OSM through a governed tile service, not directly from the OSM database or OSM tile CDN at scale. Governed tile services:

| Service | License model | ODbL compliance | NC use permitted? |
|---|---|---|---|
| Mapbox (Standard/Atlas plan) | Commercial SaaS | Mapbox handles ODbL compliance for its tile products | Yes — subject to Mapbox TOS + OSM attribution |
| CARTO | Commercial SaaS | CARTO handles ODbL compliance | Yes — subject to CARTO TOS + OSM attribution |
| OSM Tile CDN (tile.openstreetmap.org) | Free; usage policy applies | NC is responsible for attribution | Yes — limited by OSMF fair-use policy; not for heavy production traffic |
| Self-hosted (Mapnik, OpenMapTiles, Protomaps) | Self-operated | NC is responsible for ODbL compliance | Permitted under Produced Works path if vectors are never stored in NC canonical tables |

**Recommended:** A commercial tile service (Mapbox or equivalent) is preferred for production. Commercial tile services contractually assume ODbL compliance responsibilities for their tile products, reducing NC's direct ODbL exposure. Self-hosted tile rendering using downloaded OSM PBF files is permitted but requires explicit confirmation that rendered tiles, not OSM vectors, are the output — and that PBF files are processed ephemerally (not stored in NC canonical infrastructure).

---

## VII. M36 Implications

### VII.1 No M36 Writes — by Definition

OSM is an Infrastructure Reference. It contributes no data to NC's M36 canonical store. There are no M36 writes to govern, authorize, or prohibit in the active sense — the prohibition is unconditional and absolute (Invariants OS-1 through OS-5).

The M36 write prohibition for OSM is stronger than for GBIF (which prohibits content writes but permits evidence payload writes) and stronger than for Wikidata (which permits identity field writes to `places` and `creator_authority_registry`). OSM is the only NC data source for which **all M36 writes without exception are permanently prohibited**.

### VII.2 No Source Slug

OSM has no M36 source slug. `build_rights_evidence(source_slug="osm")` is not valid and must never be called. SA-9 does not apply.

### VII.3 No Institution Factory Stages

IFC v1 Article 1.2 pre-classifies OSM as outside the Institution Factory. This DD confirms the exclusion. OSM receives no institution number, no adapter module, no rights matrix, no pilot plan.

---

## VIII. Commercial Compatibility

### VIII.1 Ruling: Compatible via Produced Works Path; Incompatible via Database Path

| Use path | ODbL share-alike triggered? | Commercially compatible? |
|---|---|---|
| OSM geometry stored in NC PostgreSQL | Yes — Derivative Database | No — share-alike requires publishing NC commercial intelligence |
| OSM tile service for visual display | No — Produced Work | Yes — no share-alike, attribution only |

**NC's commercial pipeline is compatible with OSM only via the produced-works tile service path.** This path is legally clean, operationally sound, and supports the visual use case (boundary display) without triggering share-alike.

### VIII.2 CC BY vs. ODbL — Why OSM Cannot Be Used Like GeoNames

GeoNames (CC BY 4.0) and OSM (ODbL 1.0) are both attribution-requiring licenses, but they govern fundamentally different obligations:

| License | Share-alike? | Attribution? | Database restriction? |
|---|---|---|---|
| CC BY 4.0 (GeoNames) | No | Yes | No — database may be incorporated into commercial database without share-alike |
| ODbL 1.0 (OSM) | **Yes** | Yes | **Yes — Derivative Databases must be released under ODbL** |

This is why GeoNames data can enter NC's `places` table (with CC BY attribution) but OSM data cannot. The CC BY license permits database incorporation; ODbL's share-alike clause prohibits it for NC's commercial use case.

---

## IX. Relationship to GeoNames

### IX.1 Complementary, Non-Overlapping

GeoNames and OSM serve different functions with no authority overlap:

| Dimension | GeoNames | OSM |
|---|---|---|
| Place identity | Authoritative (S-3) | Not used |
| Feature classification | Authoritative (fcode) | Not used |
| Canonical coordinates | Authoritative (WGS 84 centroid) | Not used |
| Administrative hierarchy | Authoritative | Not used |
| Boundary polygon geometry | Not provided | Display only (tile service) |
| Database in NC schema | Yes (`places` table) | No (never) |
| Attribution | CC BY 4.0 | ODbL attribution on rendered output |

### IX.2 No Conflict

GeoNames and OSM do not compete for the same governance role in NC. GeoNames owns the data layer; OSM contributes to the display layer. A place page for Yellowstone National Park uses GeoNames for its canonical `geonames_id`, feature code, coordinates, and population; it uses an OSM tile service to render the park's boundary polygon on the page's map. These are separate layers with separate governance; neither overrides the other.

---

## X. Relationship to Wikidata

### X.1 No OSM QID Storage via Wikidata

Wikidata items for geographic features often carry OSM relation IDs (Wikidata `P402` = OpenStreetMap Relation identifier). NC must not follow Wikidata `P402` as a pathway to store OSM relation IDs in NC tables. Storing an OSM relation ID — even if sourced from Wikidata — constitutes storage of an OSM identifier and violates Invariant OS-4.

Wikidata's `P402` property may be used for display purposes only (e.g., linking from a Wikidata Q-item to the corresponding OSM relation for external reference), but it may not be stored in any NC canonical field.

### X.2 Wikidata Does Not Grant OSM Rights

Wikidata's CC0 license does not extend to OSM data accessible via Wikidata properties. `P402` on a Wikidata item does not convert the referenced OSM relation to CC0. The OSM relation retains its ODbL licensing regardless of how it is accessed.

---

## XI. Governance Implications Summary

| Question | Ruling |
|---|---|
| Governance classification | Infrastructure Reference (not Content Institution, not Identity Authority, not Evidence Authority) |
| Identity Authority? | No — GeoNames owns place identity (S-3) |
| Place Data Authority? | No — GeoNames owns place data layer |
| Infrastructure layer? | Yes — tile rendering and boundary display only |
| Institution Factory applicable? | No — IFC v1 Article 1.2 confirms exclusion; classification revised to Infrastructure Reference |
| Institution number | Not assigned |
| Adapter module | None — not created |
| Rights Matrix | None |
| M36 writes (any) | Prohibited — permanently and unconditionally |
| OSM data in canonical tables | Prohibited — Invariant OS-1, permanent |
| osm_id storage | Prohibited — Invariant OS-4 |
| OSM as scoring input | Prohibited — Invariant OS-3 |
| SA-9 applicability | Not applicable |
| Media ingestion | Prohibited — no media exists |
| Commercial compatibility | Yes — via produced-works tile service path only |
| ODbL share-alike triggered by tile service use | No — produced works are exempt |
| Attribution required | Yes — "© OpenStreetMap contributors" on any page rendering OSM-based tiles |
| Tile service governance | Required — governed tile service list in §VI.3; self-hosted permitted with constraints |
| SA-OSM-001 | Required — tile service selection, attribution implementation, Wikidata P402 prohibition |
| Reclassification | IFC v1 Article 1.2 "Identity and Reference Authority" pre-classification revised to "Infrastructure Reference" |

---

## XII. Open Questions

**OQ-1 — Tile service selection.** NC has not formally selected a tile service provider for place page maps. Mapbox is the recommended production option (commercial SaaS, ODbL-compliant, vector tile support). SA-OSM-001 should govern the tile service selection, SLA requirements, and fallback policy.

**OQ-2 — Self-hosted tile rendering feasibility.** For cost or performance reasons, NC may evaluate self-hosted tile rendering using OpenMapTiles or Protomaps (static PMTiles files served from S3). Self-hosted rendering is permitted under the produced-works path only if: (a) OSM PBF source files are processed ephemerally; (b) rendered tile images, not vector data, are served and cached in NC infrastructure; (c) ODbL attribution is maintained. SA-OSM-001 should evaluate this option.

**OQ-3 — OSM Overture Maps alternative.** The Overture Maps Foundation (Microsoft, Meta, AWS, TomTom) releases geographic data under CC BY 4.0 (not ODbL). Overture Maps derives significantly from OSM but its license is CC BY — the same license as GeoNames, without share-alike. If Overture Maps' polygon geometry coverage is sufficient, it would be a commercially cleaner alternative to OSM tiles for boundary display. Overture Maps is an open question for future evaluation and would require its own DD (DD-OVERTURE-001). If DD-OVERTURE-001 approves Overture Maps as a Place Geometry Authority (CC BY 4.0, no share-alike), polygon storage in `places` would become feasible under a licensing model analogous to GeoNames. This OQ is the most commercially significant of the four.

**OQ-4 — Wikidata P402 display use.** Wikidata items carry OSM relation IDs (`P402`). NC's Wikidata evidence policy (DD-WIKIDATA-001 §VI.3) does not currently enumerate `P402` as a stored field. This DD confirms it must never be stored (Invariant OS-4). Whether NC should display an external link to the OSM relation page from a place's detail view (display only, not stored) is a UX question deferred to the Wireframe Constitution.

---

## XIII. Decision Articles

**Article 1 — Governance Classification.** OSM is classified as an Infrastructure Reference under NC governance. This is a new classification, distinct from Identity and Evidence Authority. It means OSM outputs are consumed for display and navigation purposes only; OSM data never enters NC's canonical data layer. IFC v1 Article 1.2's preliminary designation of OSM as "Identity and Reference Authority" is formally revised by this ruling.

**Article 2 — ODbL Derivative Database Prohibition.** Storing OSM geometry, tags, feature IDs, or any OSM-sourced field in any NC canonical PostgreSQL table is permanently prohibited. This prohibition is unconditional. It applies regardless of the specific OSM feature, the specific NC table, or the purpose of the storage. Violation triggers ODbL §4.2b share-alike obligations over NC's commercial intelligence layer, which is incompatible with NC's Strategic Directive.

**Article 3 — Produced Works Authorization.** OSM data consumed via tile rendering services — raster tiles, vector tile graphics, boundary outline images — is governed as a Produced Work under ODbL §4.3. This use is authorized. Produced works are not subject to ODbL share-alike. NC's commercial intelligence is not exposed to ODbL by this use.

**Article 4 — Identity Authority Rejection.** OSM is not NC's place identity authority. GeoNames is (Standards Constitution v1.0 Article 17, Invariant S-3). OSM feature IDs are not stable global identifiers. No `osm_id` column may be added to any NC table.

**Article 5 — No Scoring Input.** OSM geometry may not be used as an input to any NC scoring formula. This prohibition protects NC from derivative database obligations that would arise from scored records tracing to OSM vectors.

**Article 6 — Tile Service Governance.** OSM consumption requires a governed tile service. Commercial tile services (Mapbox, CARTO) are preferred for production. Self-hosted tile rendering is permitted under the produced-works path with the constraints defined in §VI.3.

**Article 7 — Attribution Obligation.** "© OpenStreetMap contributors" must be displayed on any NC page or product that renders OSM-based tiles or boundary graphics. This attribution is required by ODbL §4.2a and is a compliance obligation, not a styling choice. Attribution omission on a production surface is a licensing violation.

**Article 8 — Wikidata P402 Prohibition.** OSM relation IDs accessed via Wikidata `P402` may not be stored in any NC canonical field. Wikidata's CC0 license does not convert OSM data to CC0. This prohibition is an extension of Invariant OS-4 to the Wikidata-access pathway.

**Article 9 — Overture Maps OQ.** OQ-3 (Overture Maps Foundation as a CC BY 4.0 place geometry alternative) is the highest-priority open question from this review. If Overture Maps' polygon coverage is sufficient for NC's place boundary needs, it would resolve the ODbL conflict entirely by providing polygon geometry under CC BY 4.0 — the same license as GeoNames — without share-alike. DD-OVERTURE-001 is recommended as the next governance action for place geometry.

**Article 10 — Standards Amendment Required.** SA-OSM-001 must formalize: tile service selection and SLA requirements, attribution implementation standard, OS-1 through OS-6 invariants in Standards Constitution form, Wikidata P402 prohibition, and self-hosted tile rendering constraints. SA-OSM-001 is a prerequisite for production deployment of place page map display.

---

## XIV. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Governance Review | ☑ APPROVE WITH CONDITIONS | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*DD-OSM-001 — drafted 2026-06-11*  
*Prior rulings: IFC v1 Article 1.2 (pre-classification) · DD-GEONAMES-001 Article 10 + OQ-1 · Standards Constitution v1.0 Article 17 (Invariant S-3) · DD-WIKIDATA-001 §VI.3*  
*Governing standards: ODbL 1.0 (Open Data Commons) · Standards Constitution v1.0 · Institution Factory Constitution v1.0 Article 1.2 · Strategic Directive*  
*Decision: APPROVE WITH CONDITIONS — Infrastructure Reference only — OSM data permanently prohibited from NC canonical tables — produced-works tile path authorized*
