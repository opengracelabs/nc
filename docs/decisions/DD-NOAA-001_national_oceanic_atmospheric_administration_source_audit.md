# DD-NOAA-001: National Oceanic and Atmospheric Administration — Source Audit

**Type:** Decision Document — Institution Source Audit  
**Status:** DRAFT — Pending Ratification  
**Authority:** Institution Factory Constitution v1 (IFC-1–IFC-12), 17 U.S.C. § 105, DD-NARA-001 (Rights Class 9 precedent), DD-GALLICA-003 (ToS disqualification precedent)  
**Institution Number:** #21  
**Date Drafted:** 2026-06-11  
**Drafted By:** NC Principal Architect  

---

## DECISION

**CONDITIONAL APPROVE**

The National Oceanic and Atmospheric Administration (NOAA) is CONDITIONALLY APPROVED as a production source for the NC commercial illustration pipeline. US federal government works produced by NOAA employees are in the public domain by operation of 17 U.S.C. § 105 — the same statutory basis as NARA (DD-NARA-001, Rights Class 9). No ToS commercial fee equivalent to the BnF/Gallica disqualifier (DD-GALLICA-003) exists. NOAA holds substantial marine life, fisheries, coral reef, and coastal natural history photography with clear NC commerce alignment, filling a marine bioregion gap no current NC institution addresses.

The conditional status arises from two unresolved connectivity questions that must be answered in Sprint 1:
1. The NOAA Photo Library (photolib.noaa.gov) has no documented public REST API. The only confirmed programmatic access path is NOAA's Flickr channel (@usoceangov), a third-party platform. The production access path — Flickr pilot or Photo Library direct (bulk download confirmation pending) — must be resolved before Sprint 2.
2. The rights gate field name and vocabulary vary by access path (Photo Library `credit` field vs. Flickr integer `license` field) and both require Sprint 1 confirmation.

Conditional status converts to full APPROVED upon ratification of SA-NOAA-001, SA-NOAA-002, and completion of Sprint 1 confirmation requirements (Article 11).

---

## I. INSTITUTION PROFILE

**Institution:** National Oceanic and Atmospheric Administration  
**Parent:** U.S. Department of Commerce  
**Founded:** 1970 (consolidating ESSA, US Coast and Geodetic Survey, US Weather Bureau, Bureau of Commercial Fisheries)  
**Photo Library:** https://photolib.noaa.gov/  
**Flickr:** https://www.flickr.com/photos/usoceangov/ (@usoceangov)  
**Fisheries Gallery:** https://www.fisheries.noaa.gov/gallery  
**Type:** US federal civilian science agency  
**Scale:** Photo Library: 30,000+ images across 25+ collections; Flickr @usoceangov: 25,000+ images; additional distributed galleries across NOAA divisions  
**Geographic scope:** Global — Atlantic, Pacific, Arctic, Gulf of Mexico, Caribbean; all US coastal and marine territories; international oceanographic expeditions  

NOAA is the authoritative US federal agency for oceans, marine life, fisheries, coasts, climate, weather, and atmospheric science. It is the direct institutional successor to the US Coast and Geodetic Survey (est. 1807), the US Weather Bureau (est. 1870), and the Bureau of Commercial Fisheries (est. 1871). NOAA operates the National Marine Fisheries Service (NMFS), the National Ocean Service (NOS), the Office of Oceanic and Atmospheric Research (OAR), and the National Weather Service (NWS). Its photographic holdings span marine species, coral reef ecosystems, oceanographic expeditions, coastal geography, and atmospheric phenomena. NOAA is the definitive U.S. government source for ocean and marine biodiversity imagery — a category no current NC institution holds.

---

## II. RIGHTS AND COMMERCIAL USE AUDIT (IFC-1 GATE)

### II.1 Legal Basis for Public Domain Status

**Statute:** 17 U.S.C. § 105 — "Copyright protection under this title is not available for any work of the United States Government."

**NOAA policy statement (standard disclaimer on NOAA media properties):** "Most NOAA photographs, video, and audio are not copyrighted and can be used freely." NOAA's stated position is consistent with § 105: works produced by federal employees in the scope of their employment carry no copyright. No commercial license fee for federally produced content is mentioned or confirmed.

This is the identical statutory basis as NARA (DD-NARA-001, Rights Class 9). Like NARA, the source of PD status is a congressional statute, not an institutional CC0 grant. Unlike Gallica (DD-GALLICA-003), NOAA does not impose a commercial reuse fee for federally produced works.

### II.2 The Contributed Image Exception

**NOAA's own disclaimer:** "However, some photos on this website are copyrighted, and NC should check for copyright restrictions before downloading."

This carve-out is the governing risk of this DD. NOAA's Photo Library, Flickr channel, and division galleries contain images from multiple contributor classes, not all of which qualify as § 105 federal works:

| Contributor Class | Rights Status | Detection Signal |
|---|---|---|
| NOAA federal employee (scope of employment) | PD — 17 U.S.C. § 105 | Credit: "NOAA", "NOAA/[Division]", "NOAA/OAR", "NOAA/NMFS", "NOAA/NOS" |
| NOAA federal contractor (producing creative work) | Copyright with contractor unless assignment obtained | Credit: "[Name]/NOAA" or "[Contractor]" |
| Third-party contributed (non-employee photographer) | Copyright with photographer | Credit: "[Photographer Name]/NOAA" or "[Org]/NOAA" |
| International partner (joint expedition) | Copyright under contributor's national law | Credit: "[Foreign Institution]/NOAA" or "[Country] agency" |
| Licensed commercial satellite imagery | Copyright with satellite operator | DigitalGlobe, Maxar, Planet Labs credits |
| University/NGO contributed | Copyright with institution unless CC0/licensed | "[University]/NOAA" or "Courtesy of [X]" |
| Predecessor agency (pre-1970 federal work) | PD — federal employee, statutory basis | "ESSA", "USCGS", "Weather Bureau", "Bureau of Commercial Fisheries" credits |

### II.3 IFC-1 Gate Analysis

**For confirmed federal-employee images (NOAA-only credit, no third-party indicator):** IFC-1 PASSED. Work of a U.S. Government employee in scope of employment. 17 U.S.C. § 105 applies. No copyright, no fee, no commercial restriction.

**For contributed images with third-party credit indicators:** IFC-1 BLOCKED. Copyright subsists with the contributor. NOAA's hosting of contributed content does not transfer or waive third-party rights. The NC NOAA adapter MUST block any image whose metadata indicates a third-party contributor.

**IFC-1 rights gate requirement:** The NOAA adapter MUST implement a credit-field check (Photo Library path) or license-integer check (Flickr path) as the IFC-1 equivalent. No image may be written without passing this gate. Gate logic is specified per access path in Section V.

### II.4 Commercial Use

**Permitted:** Yes, for confirmed § 105 federal works. NOAA imposes no commercial license fee on federally produced imagery. NOAA does not claim reproduction copyright over digital scans of government works (consistent with *Bridgeman Art Library v. Corel Corp*, SDNY 1999).

**Attribution:** Not legally required for § 105 works. NOAA requests attribution where practical: "NOAA" or "Credit: NOAA/[Division]". NC will include NOAA attribution in rights evidence; attribution is voluntary, not contractual.

**ToS commercial restriction:** None confirmed. NOAA does not operate a commercial picture library equivalent to BnF/NHM Images. No license fee is required for commercial use of § 105 government works. IFC-1 passes for the confirmed federal-work subset.

### II.5 No-Endorsement Restriction

**Statutory basis:** 5 U.S.C. § 3110 (federal employees may not endorse private enterprises); Commerce Department and NOAA non-endorsement policy.

**NOAA policy:** Use of NOAA imagery on commercial products does not imply NOAA endorsement of any company, product, or service. NOAA's name, logo, and seal may not be used in a manner that implies official federal endorsement.

**NC compliance requirement:** NC products incorporating NOAA imagery MUST NOT:
- Claim "Official NOAA", "NOAA Approved", "NOAA Partner", or equivalent
- Display the NOAA "weather satellite" logo or circular seal
- Suggest government backing or recommendation

Standard source attribution (e.g., "Image: NOAA") is acceptable. This restriction is identical in character to NASA's equivalent policy. NC's existing attribution framework is compliant as long as NOAA attribution does not accompany any endorsement claim.

---

## III. CONNECTIVITY AND API AUDIT

### III.1 NOAA Photo Library (photolib.noaa.gov)

**Type:** Web-based searchable image gallery  
**Collections:** 30,000+ images across 25+ thematic collections (Ships, Fish, Marine Life, Coral Reefs, Fisheries, Weather, Coasts, Historic, etc.)  
**Public REST API:** **NOT CONFIRMED.** No documented public REST or GraphQL API has been identified for the NOAA Photo Library. The gallery is browsable via HTML interface.  
**Authentication:** N/A (no API to authenticate against)  
**Bulk download:** Not documented; individual image downloads available via browser  
**Metadata format:** HTML-embedded, per-image caption/credit fields  
**Rights field:** `credit` field per image (text string; values include "NOAA", "NOAA/NMFS", "[Photographer]/NOAA", "Courtesy of [X]")

**Stage 3 assessment: BLOCKED (direct API path).** The Photo Library does not provide a documented programmatic API for systematic harvest. It cannot be used as the Sprint 1 access path without documentation of a bulk download mechanism or undocumented API endpoint. Sprint 1 must investigate: (a) hidden API endpoints (inspect network requests in browser); (b) RSS/OAI-PMH availability; (c) bulk download package availability via request.

### III.2 NOAA Flickr Channel (@usoceangov)

**URL:** https://www.flickr.com/photos/usoceangov/  
**Platform:** Flickr (owned by SmugMug Inc.)  
**Scale:** 25,000+ images  
**Additional NOAA Flickr accounts:** @noaafisheries (NOAA Fisheries Service); other division accounts may exist  
**Flickr API:** `https://api.flickr.com/services/rest/` — well-documented, paginated JSON  
**Authentication:** Flickr API key required (free, public access tier; no OAuth required for read-only public photos)  
**Pagination:** `flickr.people.getPhotos` method; `per_page` + `page` parameters; `total` count in response  
**Rights field:** `license` integer per photo  

**NOAA Flickr license values:**

| Flickr License ID | Name | NC Decision | Basis |
|---|---|---|---|
| 7 | No known copyright restrictions | ALLOWED | PD assertion, consistent with § 105 |
| 8 | United States Government Work | ALLOWED | Explicit § 105 assertion |
| 1–6 | Various Creative Commons + All Rights Reserved | BLOCKED | Contributed or copyrighted image |
| 9–10 | Public Domain Dedication / Public Domain Mark | ALLOWED | Additional PD indicators |
| 0 | All Rights Reserved | BLOCKED | Copyright retained |

NOAA primarily tags its federal imagery as License 8. Images tagged License 8 carry Flickr's statement: "This work, identified by [URL], has been cleared by the rights holder as a United States Government Work... not subject to copyright." This is a per-record PD assertion directly equivalent to § 105.

**Caveat:** Flickr's license tag is self-reported by the uploader. NOAA's account is official and trusted, but the Flickr tag is not a legal determination. NC must treat License 8 as the IFC-1 gate, not as a legal guarantee. Images where the caption or credit indicates a third-party contributor MUST be blocked even if tagged License 8 — the credit line is the secondary validation gate.

**Stage 3 assessment: CLEARED for pilot** — Flickr API provides confirmed programmatic access, pagination, rights field, and JSON output. This is the Sprint 1 access path. The platform dependency on Flickr/SmugMug is a production-scale risk documented in the Risk Register (R-3).

### III.3 NOAA Data API (api.noaa.gov)

**Coverage:** National Weather Service forecast/alert data, Climate Data Online (CDO) historical observations, National Buoy Center ocean conditions  
**Image content:** None. This API serves structured weather, climate, and oceanographic observational data — not photographs or illustrations.  
**NC relevance:** None for the illustration pipeline. Noted to prevent confusion with the image access path.

### III.4 IIIF Status

**IIIF in production: NOT AVAILABLE.** Neither the NOAA Photo Library nor the Flickr channel provides IIIF Image API or Presentation API endpoints. NOAA is not a IIIF Consortium member. Image delivery for NC is via direct JPEG/PNG URLs from the Flickr API response (`url_o` or `url_l` for original/large) or direct file links from the Photo Library.

This is consistent with the NARA pattern (DD-NARA-001, Rights Class 9, no IIIF, direct URL delivery).

---

## IV. COPYRIGHT TRAPS AND RISK INVENTORY

### IV.1 Contributed Image Trap (Primary)

The single highest-risk copyright trap in the NOAA collection is the contributed image — a photograph taken by a non-federal employee and hosted in the Photo Library or Flickr under a NOAA account. NOAA's own disclaimer acknowledges these exist. The NC adapter MUST treat any non-"NOAA"-only credit line as a contributed image and block it at the IFC-1 gate. Detection signals are documented in Section II.2.

### IV.2 Federal Contractor Trap

Photographs taken by private contractors working for NOAA on a services contract do NOT automatically become U.S. government works under § 105. The © status depends on whether the contract included a copyright assignment to the United States. NOAA does not systematically label contractor-produced imagery distinctly from federal-employee imagery in public-facing metadata. The NC adapter MUST apply a conservative rule: any credit line containing a personal name not associated with a recognized NOAA division MUST be blocked.

### IV.3 Licensed Commercial Satellite Imagery Trap

NOAA acquires and redistributes commercial satellite imagery (DigitalGlobe/Maxar, Planet Labs, and prior operators) for disaster response, ocean monitoring, and coastal assessments. This imagery is licensed from commercial operators, not produced by federal employees. NOAA has use rights but typically does not have sublicensing rights for commercial reuse. Indicators: credit lines containing "DigitalGlobe", "Maxar", "Planet Labs", "GeoEye", or similar commercial satellite operators. These MUST be blocked. Flickr License 0 ("All Rights Reserved") is the expected tag for these, but the credit line check is the authoritative gate.

### IV.4 International Collaboration Trap

NOAA conducts joint oceanographic expeditions with foreign research institutions (Schmidt Ocean Institute, IODP, MBARI, foreign national hydrographic offices). Photographs taken by non-US-government researchers on joint cruises are not § 105 works. Credit lines containing foreign institution names, international researchers, or "Courtesy of [foreign org]" MUST be blocked.

### IV.5 Predecessor Agency Provenance Trap

NOAA's pre-1970 archive includes images from the US Coast and Geodetic Survey, US Weather Bureau, Bureau of Commercial Fisheries, and ESSA. These are generally § 105 equivalents (works of US federal employees). However, some historical images in the NOAA archive were received as donations or gifts from private individuals or organizations, and their federal-work status is not assured. The credit line check covers this: any pre-NOAA image with a non-federal credit must be blocked.

### IV.6 Endorsement/Logo Trap

NOAA logo, seal, and name cannot be used in a manner implying government endorsement of NC products. Standard attribution ("Image: NOAA") is acceptable. Any NC product title, description, or marketing copy cannot contain phrases suggesting official NOAA affiliation.

### IV.7 Weather Map Composite Trap

Certain NOAA weather and satellite composite visualizations incorporate data from ECMWF (European Centre for Medium-Range Weather Forecasts), WMO member organizations, and commercial weather services. These composite products may be mixed-license works. The NC adapter should scope away from NWS-produced forecast graphics and atmospheric model outputs — these are outside NC's natural history illustration commerce focus in any case.

---

## V. RIGHTS MODEL CLASSIFICATION

### V.1 Rights Class Assignment

**Rights class: Rights Class 9 (REUSE — no new class required).**

Rights Class 9 was established for NARA (DD-NARA-001) as: "Per-record indicator discriminating U.S. federal government works from contributed/copyrighted works, statutory basis 17 U.S.C. § 105." NOAA satisfies all definitional criteria of Rights Class 9:

- Legal basis: identical (17 U.S.C. § 105)
- Structural logic: identical (per-record check discriminating within a mixed-rights collection)
- Governing standard: identical (17 U.S.C. § 105, not a CC license grant)

The field name and vocabulary differ by access path — this distinction is handled within the NOAA Rights Matrix (SA-NOAA-001), not by creating a new class. This is directly analogous to Getty and Yale both being Rights Class 7 (Linked Art `subject_to` URI) under different institution-specific rights matrices.

**Architecture justification for reuse vs. new class:** Rights Classes are defined by their legal-structural type (the genus), not by field-level vocabulary (the species). Rights Class 9's defining characteristic is: "statutory PD under § 105, gated by a per-record indicator of federal vs. contributed origin." NOAA satisfies both genus-level criteria. A new Rights Class would only be warranted if NOAA's legal basis differed from § 105 (it does not) or if the structural pattern differed categorically (it does not).

### V.2 NOAA Rights Matrix v1 (SA-NOAA-001 Scope)

The NOAA Rights Matrix v1 must specify gate logic for each confirmed access path:

**Path A — Flickr API (Sprint 1 pilot path):**

| Condition | Decision | Basis |
|---|---|---|
| `license` == 8 ("United States Government Work") AND credit line is NOAA-only | ALLOWED | 17 U.S.C. § 105 |
| `license` == 7 ("No known copyright restrictions") AND credit line is NOAA-only | ALLOWED | PD assertion, NOAA-confirmed |
| `license` == 9 ("Public Domain Dedication") | ALLOWED | Explicit PD |
| `license` == 10 ("Public Domain Mark") | ALLOWED | Explicit PD |
| `license` == 8 BUT credit line contains non-NOAA personal name or organization | BLOCKED | `contributed_image_exception` |
| `license` == 0 ("All Rights Reserved") | BLOCKED | `copyright_retained` |
| `license` == 1–6 (any Creative Commons) | BLOCKED | `not_federal_work` |
| `license` missing or unrecognized | BLOCKED | `missing_license_field` |

**Path B — Photo Library (Sprint 1 evaluation; production target):**

| Condition | Decision | Basis |
|---|---|---|
| `credit` == "NOAA" only | ALLOWED | 17 U.S.C. § 105 |
| `credit` matches pattern "NOAA/[Division]" where division is federal | ALLOWED | 17 U.S.C. § 105 |
| `credit` contains "[Name]/NOAA" (person before slash) | BLOCKED | `contributed_image_exception` |
| `credit` contains "Courtesy of" | BLOCKED | `donated_or_licensed_content` |
| `credit` contains commercial satellite operator name | BLOCKED | `licensed_commercial_satellite` |
| `credit` contains foreign institution | BLOCKED | `international_collaboration` |
| `credit` is missing | BLOCKED | `missing_credit_field` |

**NOAA federal division allow-list for credit line matching:**

Confirmed federal NOAA divisions (credit lines containing these are ALLOWED where no external name precedes them):
- NOAA, NOAA/NMFS, NOAA/NOS, NOAA/OAR, NOAA/NWS, NOAA/NESDIS
- NOAA Fisheries, NOAA Ocean Service, NOAA Research
- ESSA, USCGS, US Weather Bureau, Bureau of Commercial Fisheries (predecessor agencies)

`rights_policy_id`: `"noaa_rights_matrix_v1"`  
Source slug: `"noaa"` (single institution; no dual-institution routing required)

---

## VI. CONTENT TYPE ASSESSMENT

### VI.1 Marine Life and Natural History

NOAA's Photo Library is one of the most significant publicly accessible repositories of marine species photography in the world. NC-relevant collections:

| Collection | NC Relevance | Examples |
|---|---|---|
| Fish species (NMFS) | HIGH — species photography | Pacific salmon, Atlantic cod, rockfish, tuna |
| Marine mammals | HIGH — flagship species | Humpback whales, dolphins, sea lions, manatees |
| Sea turtles | HIGH — conservation narrative | Loggerhead, green, leatherback |
| Seabirds | HIGH — natural history | Albatross, puffins, pelicans |
| Coral reefs | HIGH — place anchor | Florida Keys, Hawaii, Pacific atolls, Caribbean |
| Invertebrates | MEDIUM — niche commerce | Sea stars, jellyfish, anemones |
| Deep sea | MEDIUM — discovery narrative | ROV footage/stills, bioluminescent species |
| Tide pools / intertidal | MEDIUM | Oregon coast, California, Maine |

### VI.2 Geographic Coverage

NOAA fills the marine geography gap that no current NC institution addresses:

| Region | NOAA Coverage | NC Gap Filled |
|---|---|---|
| Florida Keys / Caribbean | CONFIRMED — major collections | First Caribbean marine content |
| Hawaii / Hawaiian Islands | CONFIRMED — NMFS Hawaii collections | First Hawaii marine content |
| Pacific Northwest coasts | CONFIRMED — Pacific salmon, orca | Pacific Northwest marine gap |
| Gulf of Mexico | CONFIRMED — coral, fisheries | Gulf marine gap |
| Arctic / Alaska | CONFIRMED — walrus, polar bears, ice | Arctic ecology gap |
| Atlantic coast / NEUS | CONFIRMED — historic fisheries | Atlantic fisheries history |
| Pacific Ocean / open ocean | CONFIRMED — tuna, pelagic species | Pelagic gap |

**Note:** NOAA has minimal coverage of tropical Indian Ocean and Southeast Asian waters — regions better served by other future institutions. NOAA fills US territorial marine geography with depth.

### VI.3 Content Type Exclusions

The following NOAA content types are **outside NC's illustration commerce scope** and MUST be excluded from the adapter scope:

- **Numerical weather data visualizations** — forecast maps, NWS alert graphics, model outputs. These are scientific products, not illustration commerce material.
- **Satellite data composites incorporating licensed imagery** — potential mixed-license (IV.7 trap).
- **Climate graphs and charts** — data visualizations without commercial illustration value.
- **Building / facility photography** — ships, research stations, equipment. Low NC commerce value; not natural history.

The adapter scope MUST be restricted to NOAA Photo Library collections and Flickr albums that contain natural history subjects (marine life, coasts, coastal ecosystems). Weather, atmospheric, and administrative photography should be excluded from pilot scope.

### VI.4 NC Strategic Value Assessment

NOAA is an entirely non-redundant source for NC. It provides:
1. **Marine bioregion coverage** — no current NC institution holds marine species or ocean ecosystem imagery
2. **Species photography** (not illustration) — distinct from the golden-age botanical/zoological illustration focus; fills the modern natural history photography tier
3. **U.S. coastal geography** — Florida Keys, Hawaii, Pacific Northwest, Gulf Coast — all high-commerce NC places
4. **Federal government work** — clean rights basis, no ToS commercial restriction

NOAA does not compete with any current NC institution. NASA covers space and Earth-from-orbit; NOAA covers oceans and marine ecology at the surface.

---

## VII. ASSET ZERO

**Recommended: Coral reef panorama or NOAA marine flagship species — Hawaiian Islands or Florida Keys**

Candidates (to be confirmed by naId/flickrId in Sprint 1):

| Candidate | Place Anchor | Subject | Rights |
|---|---|---|---|
| Hawaiian Islands humpback whale | Hawaii | Marine mammal flagship | NOAA/NMFS — federal work |
| Florida Keys coral reef panorama | Florida Keys National Marine Sanctuary | Coral reef ecosystem | NOAA — federal work |
| Stellar sea lion (Steller's sea lion, Gulf of Alaska) | Alaska / Pacific | Marine mammal | NOAA/NMFS — federal work |
| Pacific salmon (Bristol Bay, Alaska) | Bristol Bay | Fisheries heritage | NOAA/NMFS — federal work |

**Primary recommendation:** Hawaiian green sea turtle or humpback whale from NOAA Fisheries Hawaii, @noaafisheries Flickr. Rationale: Hawaii is a high-commerce NC place anchor; humpback whale is an iconic NC-commercial species; NOAA/NMFS Hawaii is a confirmed federal division (§ 105 clear); Flickr API accessible for Sprint 1.

**Secondary recommendation:** Florida Keys National Marine Sanctuary coral reef image. Rationale: Florida Keys is a confirmed NC place; coral reef is the highest-commerce marine ecosystem type; Florida Keys Marine Sanctuary is a federally managed place with direct NOAA provenance.

Specific photo ID to be confirmed in Sprint 1 via Flickr API: `flickr.people.getPhotos` for @usoceangov or @noaafisheries, filtered to `license=8`, species or location tag matching. No specific image ID pre-confirmed in this DD.

---

## VIII. PILOT SCOPE

**Pilot:** Florida Keys National Marine Sanctuary and Hawaiian Marine Ecosystems  
**Target asset count:** 50  
**Duration:** 90 days  
**Access path:** Flickr API (primary confirmed path)  
**Rights gate:** Flickr `license` == 8 AND NOAA-only credit line  
**Primary anchor places:** Florida Keys, Hawaii  
**Content types:** Marine species photography (coral, fish, marine mammals); coral reef ecosystems  

**Rationale:** The Florida Keys and Hawaii pilots activate NC's first ocean/marine bioregion coverage. Both are NOAA-confirmed collection areas with high Flickr image volume. The Flickr API path is confirmed for Sprint 1. The 50-asset target (smaller than standard 75) reflects the connectivity uncertainty and the pilot's function as a path-confirmation exercise as much as a content harvest.

**Pilot success criteria:**
1. ≥50 records ingested with `rights_decision=ALLOWED` from `license==8` Flickr images
2. Zero IFC-1 violations (no contributed-image or copyrighted-content records written)
3. NOAA credit line validation gate confirmed operational
4. M36 write order preserved for 100% of records
5. Asset Zero (Hawaiian or Florida Keys marine flagship) written at MASTERWORK quality tier
6. Photo Library bulk download path evaluated and documented (blocker or cleared for Sprint 2)

---

## IX. DECISION ARTICLES

**Article 1 — Conditional Production Authorization**  
NOAA is CONDITIONALLY APPROVED as a production source. US federal government employee works are in the public domain under 17 U.S.C. § 105. No ToS commercial restriction equivalent to DD-GALLICA-003 exists. Conditional status is governed by the Sprint 1 requirements in Article 11. Conditional status converts to full APPROVED upon SA-NOAA-001 and SA-NOAA-002 ratification and Sprint 1 completion.

**Article 2 — Institution Number**  
NOAA is assigned Institution #21 in the NC institution registry.

**Article 3 — Source Slug**  
Source slug: `noaa`. Single institution, no dual-institution routing.

**Article 4 — Rights Class Assignment**  
NOAA is classified under Rights Class 9 (reuse — same class as NARA, DD-NARA-001). Rights Class 9 is defined by: per-record indicator discriminating U.S. federal government works from contributed/copyrighted works, statutory basis 17 U.S.C. § 105. SA-NOAA-001 (NOAA Rights Matrix v1) governs the field-level vocabulary and gate logic for each access path.

**Article 5 — IFC-1 Hard Gate**  
The NOAA adapter MUST block any image that does not pass the IFC-1 rights gate as specified in the NOAA Rights Matrix v1 (SA-NOAA-001). For the Flickr path: `license` must be 7, 8, 9, or 10 AND the caption/credit must not indicate a third-party contributor. For the Photo Library path: `credit` must match the confirmed federal division allow-list and must not contain a third-party name prefix. Any record failing this gate MUST produce zero writes. This gate is unconditionally permanent per IFC-1.

**Article 6 — Contributed Image Secondary Validation**  
Even where the primary rights field (Flickr `license` or Photo Library credit) passes the IFC-1 gate, the NOAA adapter MUST perform a secondary caption/credit text scan. Any caption or credit containing a personal photographer name not associated with a confirmed federal NOAA division MUST block the record with `reason: "contributed_image_exception"`. The allow-list of NOAA federal division name patterns is maintained in SA-NOAA-001.

**Article 7 — No IIIF Condition**  
NOAA does not provide production IIIF endpoints. Image delivery is via direct JPEG/PNG URL from the Flickr API (`url_o` for original, `url_l` for large) or direct Photo Library link. Records with no valid image URL MUST be blocked with `reason: "missing_image_evidence"`. SA-NOAA-002 governs the delivery protocol for each access path.

**Article 8 — Flickr Platform Dependency Condition**  
The Flickr pilot path relies on a third-party platform (SmugMug Inc.). This creates a platform dependency risk not present in direct-API institutions. NC MUST evaluate the Photo Library direct access path before Sprint 2 and document findings. If the Photo Library provides a documented bulk download or API path in Sprint 1, the Flickr path is demoted to fallback and the Photo Library path becomes the production standard.

**Article 9 — Scope Restriction to Natural History Content**  
The NOAA adapter scope is restricted to natural history subjects (marine species, coral reefs, coastal ecosystems, marine mammals, seabirds). Weather maps, forecast visualizations, NWS graphics, satellite data composites, and administrative/facility photography are EXCLUDED from scope. The adapter MUST apply subject-matter filtering (collection name, tags, or album/set membership) to enforce scope restriction.

**Article 10 — Endorsement Restriction Compliance**  
NC products incorporating NOAA imagery MUST NOT use NOAA's name, logo, or seal in a manner implying government endorsement. The attribution format "Image: NOAA" or "Credit: NOAA/[Division]" is acceptable. No product title, description, or marketing copy may claim "official", "approved by", or "in partnership with" NOAA. The rights evidence record for each NOAA asset MUST include the field `endorsement_restrictions: "noaa_nonendorsement_policy"`.

**Article 11 — Sprint 1 Confirmation Requirements**  
Before Sprint 1 adapter implementation begins, the following must be confirmed:
1. Flickr API `license` field values present in @usoceangov and @noaafisheries photo response JSON
2. NOAA credit line format patterns in Flickr `description` or `title` fields — confirming the contributed-image secondary gate is implementable from API response alone
3. Photo Library: whether any undocumented API endpoint, RSS feed, or bulk download package exists (browser network inspection required)
4. Photo Library: `credit` field name in HTML/metadata, confirming SA-NOAA-001 Path B gate is implementable
5. Confirmed `url_o` (original) image URL availability for NOAA Flickr images (some accounts restrict full-resolution)

**Article 12 — FM-4 Invariant**  
FM-4 applies without exception. The NOAA adapter worker MUST write `"pending_verification"` to `media_rights.rights_status`, never `"verified_pd"`. Reclassification to `"classified_pd"` occurs in `build_rights_evidence` via slug remap in SA-9.

**Article 13 — SA-9 Extension**  
SA-9 (`build_rights_evidence` source slug remap) MUST be extended to include `"noaa"` before Sprint 3. SA-9 is critically overdue across multiple institutions. NOAA brings the required slug count to 13: met, aic, cma, smk, nga, walters, ycba, yuag, getty, nhm, nara, mia, **noaa**.

---

## X. ARCHITECTURAL COMPARISON

| Dimension | NOAA | NARA (Rights Class 9) | NHM (Rights Class 8) |
|---|---|---|---|
| Rights class | 9 (reuse) | 9 (origin) | 8 (dataset-level CC) |
| Legal basis | 17 U.S.C. § 105 | 17 U.S.C. § 105 | CC BY 4.0 |
| Rights gate field | Flickr `license` int / Photo Library `credit` string | `useRestriction.status` enum | CKAN `license_id` |
| Allowed value(s) | license==8/7/9/10 + NOAA-only credit | `"Unrestricted"` | `cc-by`, `cc-zero` |
| Mixed-rights collection | YES — contributed images | YES — donated/private records | YES — Tier A/B split |
| Ingestion protocol | Flickr API (new) or bulk download (pending) | REST API v2 + AWS S3 bulk | CKAN Datastore API |
| IIIF | No | No | Yes (v3) |
| Auth required | Flickr API key (free) | API key (rate limited) | No |
| Rate limits | Flickr: undocumented commercial tier | 10K/month default | Soft limit (suspend risk) |
| Bulk path | Photo Library (to be confirmed) | AWS S3 (biannual) | DwC-A bulk download |
| NC content type | Marine life, coral reefs, fisheries | Maps, expedition photos | Specimen specimens, Cook Voyages illustrations |
| Geographic gap filled | Ocean/marine bioregions, US coasts | US West federal cartography | Pacific, Australia/NZ |

---

## XI. RISK REGISTER

| ID | Risk | Severity | Probability | Mitigation |
|---|---|---|---|---|
| R-1 | Photo Library has no API path — Flickr remains the only production path indefinitely | High | Medium | Sprint 1 evaluates Photo Library HTML/network; Flickr as fallback if no path found |
| R-2 | Flickr platform dependency (SmugMug changes API terms or account access) | High | Low | Photo Library path must be qualified as production alternative; NODD S3 evaluated in Sprint 2 |
| R-3 | NOAA Flickr account contains contributed images tagged License 8 incorrectly | Medium | Low | Secondary credit/caption text gate (Article 6) provides backstop; SA-NOAA-001 must specify credit scan patterns |
| R-4 | NOAA Flickr full-resolution (`url_o`) restricted to Flickr Pro accounts | Medium | Low | Sprint 1 confirms `url_o` availability; `url_l` (large) is fallback at lower resolution |
| R-5 | Commercial satellite imagery (DigitalGlobe/Maxar) appears in NOAA collections tagged as federal work | Medium | Low | Credit line scan blocks by satellite operator name (Article 6); scope restriction to natural history content (Article 9) avoids satellite-heavy collections |
| R-6 | Federal contractor photographs not distinguishable from federal employee photographs by credit line alone | Medium | Medium | Conservative rule: personal names in credit trigger block; allow-list restricted to confirmed NOAA division strings |
| R-7 | SA-9 overdue — blocks Sprint 3 across NOAA + 12 other institutions | High | High | SA-9 must be resolved before any institution reaches Sprint 3 |
| R-8 | NOAA content lacks the Golden Age illustration aesthetic (1750–1900) — limited commerce opportunity vs. Met/Rijksmuseum | Low | High (it's true) | NOAA fills the modern natural history photography tier; not an illustration-commerce institution — framed as species/marine photography, not historical illustration |
| R-9 | International NOAA expeditions yield images with contested US-government-work status | Low | Low | Credit line check blocks international collaborator images; conservative allow-list |

---

## XII. STANDARDS AMENDMENTS REQUIRED

| SA | Title | Blocks | Status |
|---|---|---|---|
| SA-9 | `build_rights_evidence` source slug remap (add `noaa`, 13th slug) | NOAA Sprint 3 | CRITICALLY OVERDUE |
| SA-NOAA-001 | NOAA Rights Matrix v1 (Flickr integer gate + Photo Library credit gate) | NOAA Sprint 1 | REQUIRED |
| SA-NOAA-002 | NOAA Image Delivery Protocol (Flickr API direct URL extraction + Photo Library path specification) | NOAA Sprint 1 | REQUIRED |

**Note on new Flickr adapter class:** If the Photo Library direct path is confirmed non-viable after Sprint 1, SA-NOAA-002 will define the Flickr API as a new NC ingestion adapter class — the first third-party platform delivery path in the NC pipeline. This would require constitutional-level documentation of the platform dependency, its risks, and the conditions under which a platform-based adapter is acceptable. No prior NC institution uses a third-party platform as its primary access path.

---

## XIII. RATIFICATION TABLE

| Role | Approval | Date |
|---|---|---|
| Principal Architect | ☐ PENDING | — |
| Governance Review | ☐ PENDING | — |

**Conditions for ratification:**
1. SA-NOAA-001 scope accepted (NOAA Rights Matrix v1 with Flickr + Photo Library gate logic)
2. SA-NOAA-002 scope accepted (image delivery protocol for chosen access path)
3. Institution #21 recorded in NC institution registry
4. Scope restriction to natural history content (Article 9) acknowledged by governance
5. Flickr platform dependency risk (R-2) acknowledged and Photo Library evaluation accepted as Sprint 1 deliverable
6. Asset Zero designation accepted (Hawaiian or Florida Keys marine flagship, Sprint 1 confirmation required)

---

*DD-NOAA-001 drafted 2026-06-11 under authority of Institution Factory Constitution v1.*  
*Legal basis: 17 U.S.C. § 105 (federal works PD), Commerce Department non-endorsement policy.*  
*Rights Class precedent: DD-NARA-001 (Rights Class 9 — same § 105 statutory basis, reused without modification).*  
*Connectivity precedent: No prior NC institution uses a third-party platform (Flickr) as primary access path — SA-NOAA-002 must specify constitutional basis for Flickr-path acceptance.*  
*Disqualification precedent consulted: DD-GALLICA-003 (no equivalent ToS commercial fee — NOAA cleared); DD-ALA-001 (content type doctrine — NOAA passes, marine photography is natural history content).*
