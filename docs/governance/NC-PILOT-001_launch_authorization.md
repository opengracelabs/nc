# NC-PILOT-001: Launch Authorization

| Field | Value |
|---|---|
| Document | NC-PILOT-001-LA |
| Version | 1.0 |
| Status | **DRAFT** — pending Principal Architect ratification |
| Date | 2026-06-11 |
| **Authorization** | **AUTHORIZED** |
| Documents reviewed | NC-PILOT-001 Governance Blueprint · NC-PILOT-001-FRR · SA-GEONAMES-001 · SA-OSM-001 · DD-WIKIDATA-001 · DD-GBIF-001 |
| Authorization scope | 7 pilot places · 16 confirmed product-safe assets · 5 governed source authorities |
| Gate E required | Yes — two-human sign-off before any asset goes live |

---

## I. Authorization Confirmation

### I.1 Document Review Findings

| Document | Status at review | Finding |
|---|---|---|
| NC-PILOT-001 Governance Blueprint | DRAFT — pending ratification | Authority chain complete; conditions met by SA-GEONAMES-001 + SA-OSM-001 |
| NC-PILOT-001-FRR (Final Readiness Review) | DRAFT — pending ratification | All 7 blocking conditions cleared; LAUNCH READY ruling confirmed |
| SA-GEONAMES-001 | DRAFT — pending ratification | CC BY 4.0 attribution standard defined; Attribution Gate B-1 implementable |
| SA-OSM-001 | DRAFT — pending ratification | Tile service selected (Mapbox); ODbL attribution standard defined; OSM Intelligence Plan formally superseded; Attribution Gate B-2 implementable |
| DD-WIKIDATA-001 | DRAFT — pending ratification | Identity and Evidence Authority confirmed; CC0 unconditional; evidence schemas and invariants W-1–W-8 confirmed |
| DD-GBIF-001 | **RATIFIED** | Identity and Evidence Authority confirmed; CC0 Backbone; occurrence evidence schema confirmed; SA-GBIF-001 active |

### I.2 Authorization Basis

**The pilot is authorized to proceed.** All governance blocking conditions are resolved. The six reviewed documents establish a complete and internally consistent governance architecture:

- **Rights path:** 17 U.S.C. § 105 (NASA, NOAA, NARA), pre-1928 PD (BHL), Rights Class 3B (MIA) — all governed by IFC-1
- **Identity authority:** GeoNames (place, S-3), Wikidata (entity QID), GBIF (biological anchor) — all governed, CC0 / CC BY 4.0
- **Commercial use:** Permitted for all 16 confirmed product-safe assets under the terms of their respective governing DDs
- **Attribution:** Fully governed by SA-GEONAMES-001 and SA-OSM-001; nonendorsement lines governed by DD-NASA-001 and DD-NOAA-001
- **Display layer:** OSM produced-works tile path authorized under DD-OSM-001; Mapbox GL JS selected as tile service

Authorization is **phased by place** per NC-PILOT-001 §VII.3. Earthrise Phase 1 authorization has the fewest pre-activation dependencies and may proceed immediately upon Gate E confirmation. Each subsequent phase activates independently as its Gate E items are confirmed.

---

## II. Final Attribution Matrix

Attribution obligations govern what NC must display, in what form, on which surfaces. All obligations are cumulative and independent. Meeting one does not satisfy another.

### II.1 Source Attribution Reference

| Source | Attribution required? | Legal basis | Canonical text | Surfaces |
|---|---|---|---|---|
| **NASA** | **Yes** | Federal nonendorsement doctrine | `Image credit: NASA. NASA does not endorse this product.` | Every product listing, product print label, and asset detail page showing a NASA-sourced image |
| **NOAA** | **Yes** | Federal nonendorsement doctrine | `Credit: NOAA/[Division]` (e.g., "NOAA/OAR", "NOAA/PIFSC") | Every asset detail page showing a NOAA-sourced image; not required on print products unless NOAA is named in product copy |
| **NARA** | Advisory | DD-NARA-001 §II.3 | `National Archives [catalog number]` | Provenance record; asset detail page; not required on product label |
| **GeoNames** | **Yes** | CC BY 4.0 (SA-GEONAMES-001 §II.1) | `Geographic data © GeoNames (geonames.org) — CC BY 4.0` | Place page footer (persistent); API `nc:geonames_attribution` field; IIIF `requiredStatement`; product pages where place-derived data is displayed |
| **OSM (tiles)** | **Yes** | ODbL 1.0 produced-works path (SA-OSM-001 §III.1) | `© OpenStreetMap contributors` (hyperlinked to openstreetmap.org/copyright) | Every page and display rendering OSM map tiles; map overlay, bottom-right corner |
| **Wikidata** | No | CC0 unconditional (DD-WIKIDATA-001 §III.1) | — | — |
| **GBIF** | No | CC0 unconditional (DD-GBIF-001 §III.2) | — | Bulk download citation advisory only; not consumer-facing |
| **BHL** | No | Pre-1928 PD / CC0 | — | — |
| **MIA** | Institutional credit | DD-MIA-001 | `Minneapolis Institute of Art` | Asset detail page; product metadata |

### II.2 Attribution Stacking by Place

The columns show which attribution obligations are simultaneously active on each place's public pages. Numbers in parentheses show total simultaneous attribution obligations.

| Place | GeoNames CC BY | NASA | NOAA | OSM | NARA (advisory) | Total binding |
|---|---|---|---|---|---|---|
| **Yellowstone** | ✓ footer | ✓ product | — | ✓ map | ✓ provenance | **3** |
| **Grand Canyon** | ✓ footer | ✓ product | — | ✓ map | ✓ provenance | **3** |
| **Great Barrier Reef** | ✓ footer | ✓ product | ✓ asset page | ✓ map | — | **4** |
| **Papahānaumokuākea** | ✓ footer | ✓ product | ✓ asset page | ✓ map | ✓ provenance | **4** |
| **Venice** | ✓ footer | ✓ product | — | ✓ map | — | **3** |
| **Galápagos** | ✓ footer | ✓ product | — | ✓ map | — | **3** |
| **Earthrise** | — (exempt) | ✓ product | — | — (no map) | — | **1** |

**Earthrise note:** No GeoNames attribution (S-3 cosmic anchor exception). No OSM tiles (no terrestrial boundary). NASA nonendorsement is the sole binding attribution obligation on the Earthrise place page and all Earthrise products.

### II.3 Attribution Ordering Rule

When multiple attributions are displayed simultaneously on a single surface, the governed ordering is:

```
1. Asset credit / source institution (NASA, NOAA, institutional)
2. Geographic data: "Geographic data © GeoNames (geonames.org) — CC BY 4.0"
3. Map tiles: "© OpenStreetMap contributors"
4. Additional institutional credits (NARA catalog number, MIA)
```

Federal nonendorsement lines must always appear proximate to the specific asset they govern. They must not be merged with GeoNames or OSM attribution.

### II.4 Attribution by Product Surface

| Surface | NASA | NOAA | GeoNames | OSM |
|---|---|---|---|---|
| Place page (web) | On NASA asset cards | On NOAA asset cards | Footer — persistent | Map overlay — always visible |
| Product listing (web) | Below product image | Below product image | Footer of place-anchored listing page | If map shown: map overlay |
| Product detail page | Prominent, below title | Prominent, below title | Footer | If map shown: map overlay |
| Physical print product | Label / back of print | Label / back of print | Not required on print (digital surface obligation only) | Not required unless map is printed |
| Digital download | Embedded metadata field | Embedded metadata field | `nc:geonames_attribution` in file metadata | Not required in file metadata |
| NC API response (place entity) | `attribution` field | `attribution` field | `nc:geonames_attribution` root field | Not required in API response |
| IIIF manifest | `requiredStatement` | `requiredStatement` | `requiredStatement` | Not required |

---

## III. Final Public-Facing Disclaimer Matrix

Disclaimers are what consumers and the public see on NC surfaces. They are distinct from internal provenance records. This matrix defines the exact disclaimer language for each governed situation.

### III.1 Public Domain Declaration

Every product and product listing must carry a PD status declaration appropriate to its rights basis:

| Rights basis | Consumer-facing PD declaration |
|---|---|
| 17 U.S.C. § 105 (NASA, NOAA, NARA) | `This image is a work of the United States federal government and is in the public domain in the United States.` |
| Pre-1928 publication (BHL) | `This image is in the public domain due to its age (published before 1928).` |
| Rights Class 3B (MIA, verified PD) | `This image has been verified as in the public domain by the Minneapolis Institute of Art.` |

### III.2 Federal Nonendorsement Disclaimer

Required on all products and pages that display, sell, or reference imagery from NASA, NOAA, or NARA.

| Agency | Exact disclaimer text | Where displayed |
|---|---|---|
| **NASA** | `Image credit: NASA. NASA does not endorse this product.` | Below each NASA-sourced product image; on product listing; in print product label |
| **NOAA** | `Credit: NOAA/[Division]. NOAA does not endorse this product.` | Below each NOAA-sourced image on asset detail pages |
| **NARA** | `Image from the National Archives (Record Group [number], Catalog ID [number]).` | Asset detail page; provenance display |

**Prohibited in all NC product copy:**
- "Official NASA", "NASA Approved", "NOAA Certified", "Official National Archives"
- Any federal seal, insignia, meatball logo, or NOAA circular seal
- Any claim that NC is affiliated with, sponsored by, or endorsed by a US government agency

### III.3 Geographic Attribution Disclaimer

Required on all place pages and any page displaying GeoNames-sourced geographic data.

```
Geographic data © GeoNames (geonames.org) — CC BY 4.0
```

This line must be present in the visible footer of every terrestrial place page. It must hyperlink to `https://www.geonames.org` on web surfaces. On mobile: compact form ("© GeoNames — CC BY 4.0") is permitted if full form cannot fit.

### III.4 Map Tile Disclaimer

Required on every page rendering OSM-based map tiles.

```
© OpenStreetMap contributors
```

Displayed as a map overlay, bottom-right corner, always visible. Must hyperlink to `https://www.openstreetmap.org/copyright`. Must not be smaller than any other map attribution (Mapbox branding, if displayed).

Full map attribution chain when using Mapbox:
```
© OpenStreetMap contributors   |   Map data provided by Mapbox
```

OSM attribution must appear first.

### III.5 Consumer Use Rights Notice

Every product detail page must carry a consumer use rights notice clarifying what the consumer can do with a purchased NC product:

```
The underlying image in this product is in the public domain. NC's commercial product 
(print, download, or licensed design file) is sold under NC's Terms of Service. The 
public domain status of the source image is not affected by this purchase.
```

This notice is NC's standard consumer notice; it is not a new governance requirement per this authorization. It is included here as a reminder that the existence of a PD image does not mean NC has no IP in its products — NC's creative additions (curation, color correction, framing, product design) may carry their own rights. The consumer notice distinguishes between the underlying image (PD) and the NC product (governed by NC's ToS).

### III.6 Disclaimer Matrix by Place

| Place | PD declaration | Federal nonendorsement | GeoNames | OSM | Consumer use |
|---|---|---|---|---|---|
| Yellowstone | § 105 + pre-1928 | NASA (products) | ✓ | ✓ | ✓ |
| Grand Canyon | § 105 + pre-1928 | NASA (products) | ✓ | ✓ | ✓ |
| Great Barrier Reef | § 105 | NASA + NOAA | ✓ | ✓ | ✓ |
| Papahānaumokuākea | § 105 + pre-1928 | NASA + NOAA | ✓ | ✓ | ✓ |
| Venice | § 105 | NASA (contextual) | ✓ | ✓ | ✓ |
| Galápagos | § 105 + pre-1928 | NASA (products) | ✓ | ✓ | ✓ |
| Earthrise | § 105 | NASA (product) | — (exempt) | — | ✓ |

---

## IV. Launch Governance Checklist

This checklist must be confirmed in full before any place page or product is made publicly visible. It covers governance, infrastructure, rights, and attribution. Items are organized in dependency order — complete earlier sections before moving to later ones.

### Section A — Document Ratification

All governing documents must be ratified before public launch. Draft status is sufficient for staging operations.

| # | Item | Document | Status |
|---|---|---|---|
| A-1 | NC-PILOT-001 Governance Blueprint ratified | NC-PILOT-001 | ☐ |
| A-2 | NC-PILOT-001-FRR ratified | NC-PILOT-001-FRR | ☐ |
| A-3 | NC-PILOT-001-LA (this document) ratified | NC-PILOT-001-LA | ☐ |
| A-4 | SA-GEONAMES-001 ratified | SA-GEONAMES-001 | ☐ |
| A-5 | SA-OSM-001 ratified | SA-OSM-001 | ☐ |
| A-6 | DD-WIKIDATA-001 ratified | DD-WIKIDATA-001 | ☐ |
| A-7 | SA-NOAA-001 ratified | SA-NOAA-001 | ☑ RATIFIED |
| A-8 | SA-NOAA-002 ratified | SA-NOAA-002 | ☑ RATIFIED |
| A-9 | SA-GBIF-001 ratified | SA-GBIF-001 | ☑ RATIFIED |

**Note:** DD-GBIF-001 carries RATIFIED status. All other DDs in the authority chain (DD-NASA-001, DD-NOAA-001, DD-NARA-001, DD-MIA-001, DD-GEONAMES-001, DD-OSM-001) must also carry ratified status before public launch. Confirm ratification status for all DDs in the authority chain.

### Section B — Infrastructure

| # | Item | Authority | Status |
|---|---|---|---|
| B-1 | GeoNames NC application account provisioned (not demo) | SA-GEONAMES-001 §IV | ☐ |
| B-2 | Mapbox account provisioned; API key stored as secret in NC infrastructure | SA-OSM-001 §VI | ☐ |
| B-3 | NC Mapbox map style created (custom — not default Mapbox Streets) | SA-OSM-001 §II.1 | ☐ |
| B-4 | Protomaps self-hosted fallback configured and tested | SA-OSM-001 §II.2 | ☐ |
| B-5 | Wikidata API User-Agent header configured to identify NC application | DD-WIKIDATA-001 §VI.7 | ☐ |

### Section C — Identity Layer (per place)

Complete for each place before that place's Gate E. Confirmed GeoNames IDs from NC-PILOT-001-FRR §III.

| # | Place | Canonical GeoNames ID | Wikidata QID | fcode | Written to `places` table? |
|---|---|---|---|---|---|
| C-1 | Yellowstone NP | ~~5843642~~ **5843591** (NC-DATA-001) | Q351 | PRKA (H.PRKA) | ☐ |
| C-2 | Grand Canyon NP | **5296401** (NC-DATA-003) | Q220289 | PRK (L.PRK) | ☐ |
| C-3 | Great Barrier Reef | **2164628** | Q7343 | RF (H.RF) | ☐ |
| C-4 | Papahānaumokuākea | **TBD** — NC GeoNames lookup required | Q787425 | MAR (expected) | ☐ |
| C-5 | Venice | **3164603** | Q641 | PPLA | ☐ |
| C-6 | Galápagos Islands | **3658931** | Q38095 | ISLS | ☐ |
| C-7 | Earthrise | **exempt** (S-3 exception) | Q1163059 | — | ☐ |

**Note on Wikidata QIDs:** The Governance Blueprint carried draft QIDs that were not confirmed via P1566 cross-validation. The QIDs in this table are the FRR-confirmed QIDs derived from the Wikidata P1566 lookup (2026-06-11). These are the canonical values for `places.wikidata_qid`. The `wikidata_conflict` field should flag any discrepancy with the Blueprint's draft QIDs until those are resolved.

**Papahānaumokuākea GeoNames ID:** Run `curl "https://secure.geonames.org/searchJSON?q=Papahanaumokuakea&country=US&username=<NC_GEONAMES_ACCOUNT>"` to confirm. Do not activate the Papahānaumokuākea place page until the ID is confirmed and written. This does not block any other phase.

### Section D — Asset Zero Rights Clearance (per place)

| # | Place | Asset Zero | Source | Rights gate | IFC-1 confirmed? |
|---|---|---|---|---|---|
| D-1 | Earthrise | AS08-14-2383 (NC-NASA-002) | NASA | § 105 — federal work; verify NASA attribution record | ☐ |
| D-2 | Yellowstone | NC-NASA-026 "Yellowstone from Orbit" | NASA | § 105 | ☐ |
| D-3 | Yellowstone | Hayden Survey map 1871 | NARA | `useRestriction.status == "Unrestricted"` | ☐ |
| D-4 | Grand Canyon | NC-NASA-027 "Grand Canyon Depth" | NASA | § 105 | ☐ |
| D-5 | Grand Canyon | Powell Survey map 1869 | NARA | `useRestriction.status == "Unrestricted"` | ☐ |
| D-6 | Great Barrier Reef | NC-NASA-029 "GBR Whitsundays" | NASA | § 105 | ☐ |
| D-7 | Great Barrier Reef | NOAA coral reef image (PIFSC or OAR) | NOAA | SA-NOAA-001: license ∈ {7, 8}; credit field = institutional (no personal name) | ☐ |
| D-8 | Papahānaumokuākea | NC-NASA (Pacific atoll) | NASA | § 105 | ☐ |
| D-9 | Papahānaumokuākea | NOAA PIFSC marine image | NOAA | SA-NOAA-001 gate | ☐ |
| D-10 | Venice | NC-NASA Mediterranean contextual | NASA | § 105 | ☐ |
| D-11 | Galápagos | NC-NASA-042 "Galápagos Islands" | NASA | § 105 | ☐ |
| D-12 | Galápagos | Gould *Darwin's Finches* plate | BHL | Pre-1928 PD (Gould died 1881) | ☐ |

For each Asset Zero: `media_rights.rights_status = 'verified_pd'` AND `media_rights.human_verified = TRUE` must be confirmed before activation.

### Section E — Attribution Implementation Verification

| # | Check | Authority | Status |
|---|---|---|---|
| E-1 | GeoNames attribution string present and visible in footer of all 6 terrestrial place pages | SA-GEONAMES-001 §III | ☐ |
| E-2 | "GeoNames" hyperlinks to geonames.org on all web surfaces | SA-GEONAMES-001 §II.1 | ☐ |
| E-3 | `nc:geonames_attribution` field populated in all place API responses | SA-GEONAMES-001 §II.3 | ☐ |
| E-4 | "© OpenStreetMap contributors" visible and hyperlinked on all map tile displays | SA-OSM-001 §III.1 | ☐ |
| E-5 | OSM attribution appears first when co-displayed with Mapbox attribution | SA-OSM-001 §III.1 | ☐ |
| E-6 | NASA nonendorsement line present on all NASA-sourced product listings | DD-NASA-001; NC-PILOT-001 §IV.3 ATT-3 | ☐ |
| E-7 | NOAA nonendorsement line present on all NOAA-sourced asset detail pages | DD-NOAA-001; NC-PILOT-001 §IV.3 ATT-4 | ☐ |
| E-8 | No OSM Relation IDs present in any NC database table | SA-OSM-001 §IV.2; DD-OSM-001 OS-4 | ☐ |
| E-9 | PD declaration present on every product listing | §III.1 of this document | ☐ |
| E-10 | Consumer use rights notice present on every product detail page | §III.5 of this document | ☐ |
| E-11 | Earthrise page: no GeoNames attribution (correctly exempt); `geonames_exemption` field populated | SA-GEONAMES-001 §V.3 | ☐ |

### Section F — Disclaimer and Copy Review

| # | Check | Authority | Status |
|---|---|---|---|
| F-1 | All product copy reviewed: no "Official NASA", "NASA Approved", "NOAA Certified", or equivalent | DD-NASA-001; DD-NOAA-001 | ☐ |
| F-2 | No NASA insignia, meatball logo, or NOAA circular seal on any product or page | DD-NASA-001; DD-NOAA-001 | ☐ |
| F-3 | No claim that NC is affiliated with, sponsored by, or endorsed by any federal agency | DD-NASA-001; DD-NOAA-001; DD-NARA-001 | ☐ |
| F-4 | Venice place page: `content_status: 'partial'` operational notation recorded | NC-PILOT-001 §IX.2; NC-PILOT-001-FRR §C-6 | ☐ |
| F-5 | Earthrise: `geonames_exemption: "cosmic_anchor_S3_provisional"` recorded; 60-day amendment timer started | NC-PILOT-001 §IX.1 | ☐ |
| F-6 | NOAA pilot restriction documented in operations log: ALLOWED → max 7 writes; REVIEW_REQUIRED → 0 writes | DD-NOAA-001 Sprint 3 authorization | ☐ |

### Section G — Gate E: Two-Human Activation Sign-Off

Gate E is required for every individual activation event (place page + product launch pair). It is not a single one-time sign-off — it is confirmed per activation.

| # | Check | Authority | Sign-off |
|---|---|---|---|
| G-1 | Rights Verifier #1: confirms IFC-1 compliance for this Asset Zero activation event (Sections D + E above) | IFC v1 | ☐ [Verifier 1 name + date] |
| G-2 | Principal Architect: confirms activation authorization for this place + asset combination | IFC v1; NC-PILOT-001-LA ratification | ☐ [Principal Architect signature + date] |

**Gate E is non-delegable.** Both sign-offs must be from different individuals. A single person cannot satisfy both G-1 and G-2.

---

## V. Post-Launch Review Schedule

The pilot is governed by a defined review schedule. Reviews are not optional — they are governance events with defined decision outputs.

### V.1 T+30 Days: Initial Compliance Review

**Date:** 30 days after first place page goes live.  
**Trigger:** Mandatory; not based on commercial performance.

| Review item | Target | Decision output |
|---|---|---|
| Rights audit | 100% of activated assets: `rights_status = 'verified_pd'` and `human_verified = TRUE` | Pass / Fail. Fail = immediate escalation to Principal Architect; affected assets deactivated |
| FM-4 audit | 0 assets with FM-only rights determination | Pass / Fail |
| NOAA gate audit | 0 REVIEW_REQUIRED records in any activated product | Pass / Fail |
| NARA gate audit | 0 non-Unrestricted records in any activated product | Pass / Fail |
| Attribution spot check | GeoNames footer present on all live place pages; OSM attribution on all map displays; NASA nonendorsement on all NASA products | Pass / Fail. Fail = attribution component fix within 48 hours |
| Federal endorsement scan | 0 endorsement claims in all product copy, marketing, and UI | Pass / Fail |
| First commerce review | Commercial performance baseline established (page views, conversion) | Data only — no pass/fail at T+30 |

**T+30 governance output:** "Pilot rights and attribution compliance confirmed" or "Pilot compliance escalation — [findings]."

### V.2 T+60 Days: Earthrise Cosmic Anchor Deadline

**Date:** 60 days after Earthrise place page goes live.  
**Trigger:** Mandatory, tied to NC-PILOT-001 §IX.1 provisional exception.

| Decision required | Options | Consequence of non-decision |
|---|---|---|
| Earthrise cosmic anchor resolution | (a) Standards Constitution amendment adding `cosmic_anchor` place type; OR (b) Proxy-place assignment (e.g., Pacific Ocean GeoNames ID) | Earthrise demoted from canonical place to standalone product page; no place page until resolved |

**T+60 governance output:** Standards Constitution Amendment drafted (option a), OR place record updated with proxy GeoNames ID (option b), OR Earthrise demotion executed.

### V.3 T+90 Days: Full Pilot Assessment

**Date:** 90 days after first public launch.  
**Trigger:** Mandatory.

| Category | Metrics reviewed | Decision threshold |
|---|---|---|
| **Rights compliance** | All zero-tolerance metrics from NC-PILOT-001 §VIII.1 | 100% required for scale authorization |
| **Attribution compliance** | All attribution metrics from §VIII.2 | 100% required for scale authorization |
| **Commercial performance** | Activated assets ≥7; product listings ≥7; ≥1 transaction; Earthrise revenue baseline | No hard threshold — establishes data for v0.5.0 decision |
| **GBIF evidence coverage** | ≥80% of pilot place-taxon pairs have `gbif_taxon_key` resolved | SA-GBIF-001 evidence policy |
| **Governance health** | SA-GEONAMES-001 ratified; SA-OSM-001 ratified; Earthrise amendment/proxy complete | All three required for scale authorization |
| **Venice upgrade** | ≥1 art museum DD (DD-MET-001 / DD-AIC-001 / DD-CMA-001) ratified or in progress | Determines Venice Phase 6 timeline |

**T+90 governance output:** SCALE AUTHORIZED or SCALE DEFERRED (with specific remediation conditions).

### V.4 T+180 Days: Scale Authorization Review

**Date:** 180 days after first public launch.  
**Trigger:** If scale was authorized at T+90, this is the first expansion checkpoint.

| Review item | Content |
|---|---|
| New institution DDs | Progress on DD-SMITHSONIAN-001, DD-MET-001 ratification, DD-TNA-001/UKHO-001 |
| Deferred asset reinstatement | Status of the 9 deferred assets (are their institution DDs now ratified?) |
| Venice full-launch status | Is at least one museum DD ratified? If yes: trigger Venice Phase 6 |
| Additional place candidates | Is there a governance case for adding a new place to the pilot? |
| NOAA Sprint 4 readiness | DD-NOAA-001 Sprint 1 Photo Library path evaluation status |
| SA-WIKIDATA-001 | Drafted and on path to ratification? |
| DD-OVERTURE-001 | Commissioned? Would unblock polygon geometry for places table |

**T+180 governance output:** Expansion plan or "hold at current scope" ruling.

### V.5 T+365 Days: Annual Governance Review

**Date:** 12 months after first public launch.  
**Trigger:** Annual; recurring.

| Annual governance check | Authority |
|---|---|
| GBIF Backbone Taxonomy synchronization audit | DD-GBIF-001 §VI.2 Addition 3 |
| Wikidata QID redirect check (entity merges) | DD-WIKIDATA-001 OQ-2 |
| GBIF multimedia license distribution monitoring | DD-GBIF-001 OQ-3 |
| NOAA path B evaluation (Photo Library access) | DD-NOAA-001 Article 11 |
| NARA rate limit review (10K/month default tier) | DD-NARA-001 §IV.1 |
| Rights audit: all activated assets | IFC-1 annual audit |
| SA-WIKIDATA-001 status | Required before catalog harvest scale |
| Institution factory pipeline review | How many of the 5 outstanding target institutions (NHM, Wellcome, Trove, HathiTrust, plus 3 geographic gap candidates) are in active onboarding? |

---

## VI. Authority Chain and Precedence

This authorization document is issued at the base of NC's authority chain. It does not override any higher-authority document. Conflicts are resolved in favor of the higher authority:

```
Strategic Directive + Illustration Opportunity Doctrine
        ↓
Institution Factory Constitution v1 (IFC-1–IFC-12)
        ↓
Standards Constitution v1.0
        ↓
Commerce Intelligence Constitution v1.2
        ↓
Foundation Model Constitution v1.0
        ↓
Director Decisions (DD-NASA-001 through DD-OSM-001)
        ↓
Standards Amendments (SA-NOAA-001, SA-NOAA-002, SA-GBIF-001, SA-GEONAMES-001, SA-OSM-001)
        ↓
NC-PILOT-001 Governance Blueprint
        ↓
NC-PILOT-001-FRR · NC-PILOT-001-LA (this document) [co-equal]
```

**IFC-1 and FM-4 are unconditional across this entire chain.** No provision in this document, the Governance Blueprint, or any SA grants an exception to IFC-1 or FM-4. Any code change that would allow an asset into the commercial pipeline without `rights_status = 'verified_pd'` and `human_verified = TRUE` is a constitutional violation, regardless of authorization status at this layer.

---

## VII. Decision Articles

**Article 1 — Launch Authorization.** The NC-PILOT-001 commercial pilot is authorized to proceed. All seven governance blocking conditions identified in NC-PILOT-001-FGR have been resolved. The pilot may activate per the phased launch sequence: Earthrise → Yellowstone + Grand Canyon → Galápagos → Great Barrier Reef + Papahānaumokuākea → Venice (partial) → Venice (full, post-museum DD).

**Article 2 — Gate E Non-Waivable.** Gate E (two-human activation sign-off) is required for every individual activation event. It is not a single pre-launch authorization — it is confirmed per place page + product launch pair. The authorization in Article 1 enables operations to begin the Gate E process; it does not substitute for Gate E.

**Article 3 — SA Ratification Required Before Public Launch.** SA-GEONAMES-001 and SA-OSM-001 must reach ratified status (Principal Architect sign-off) before any place page is made publicly visible. Draft status is sufficient for staging operations and Gate E preparation.

**Article 4 — Attribution Is Non-Negotiable.** All attribution obligations in §II are binding. SA-GEONAMES-001 and SA-OSM-001 define the implementation standard; that standard is not met by approximate or conditional attribution. Attribution must be present on every surface governed by §II.4 before Gate E is confirmed.

**Article 5 — 16 Confirmed Assets Only.** The 9 deferred assets (NC-PILOT-001-FRR §C-5) are excluded from the launch inventory. No deferred asset may enter any NC pipeline — staging, testing, or production — until the governing institution DD is ratified. Reinstatement requires a Principal Architect authorization event, not just DD ratification.

**Article 6 — Papahānaumokuākea GeoNames ID.** The Papahānaumokuākea GeoNames ID is unconfirmed. The Papahānaumokuākea place page must not be activated until the ID is confirmed via NC's GeoNames application account and written to the `places` table. Phases 1–3 (Earthrise, Yellowstone, Grand Canyon, Galápagos) may proceed independently.

**Article 7 — Post-Launch Reviews Are Governance Events.** The T+30, T+60, T+90, T+180, and T+365 reviews in §V are governance commitments, not optional reports. The T+60 Earthrise deadline is time-critical: failure to resolve the cosmic anchor within 60 days of Earthrise launch requires demotion of the Earthrise place page per NC-PILOT-001 §IX.1.

**Article 8 — Federal Endorsement Zero-Tolerance.** A single confirmed federal endorsement claim in any NC product copy, marketing material, or UI is sufficient grounds for immediate deactivation of all federal-sourced assets (NASA, NOAA, NARA) pending a compliance review. This is not a proportionate remedy — it is the required response to federal nonendorsement doctrine violation.

**Article 9 — Venice Patience.** Venice's content-thin status at launch is not a failure condition. Venice is authorized to launch with an editorial place page (no products) and to upgrade automatically upon the first art museum DD ratification. The Venice place page shall not carry any notice to consumers that content is "coming soon" unless specifically approved — the standard place page experience is the correct initial state.

**Article 10 — OSM Intelligence Plan Is Dead.** The OSM Intelligence Plan v1 (`docs/implementation/osm_intelligence_plan_v1.md`) is formally superseded by SA-OSM-001. No engineer, product manager, or analyst may treat the OSM Intelligence Plan as an active implementation reference. SA-OSM-001 §V is the governing OSM integration specification.

---

## VIII. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Launch Authorization Review | ☑ AUTHORIZED | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*NC-PILOT-001-LA — drafted 2026-06-11*  
*Documents reviewed: NC-PILOT-001 · NC-PILOT-001-FRR · SA-GEONAMES-001 · SA-OSM-001 · DD-WIKIDATA-001 · DD-GBIF-001*  
*Authorization: AUTHORIZED — Gate E required per activation · SA-GEONAMES-001 + SA-OSM-001 ratification required before public launch*
