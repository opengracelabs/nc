# NC-FIRST-SALE: First Sale Authorization

| Field | Value |
|---|---|
| Document | NC-FIRST-SALE-AUTH |
| Version | 1.0 |
| Status | **DRAFT** — Pending Principal Architect Ratification |
| Date | 2026-06-11 |
| **Authorization** | **FIRST SALE AUTHORIZED — with two mandatory corrections** |
| Documents Reviewed | NC-COMMERCE-001 · NC-COMMERCE-002 · NC-FIRST-SALE Playbook |
| First sale products | NC-PROD-008 (digital) then NC-PROD-001 (print) — concurrent Gate E |
| Collector Edition | NOT READY — NARA mission plan asset not cleared |

---

## I. Review Findings

### I.1 Blocking Issue: NARA Attribution on an NASA-Sourced Image

**Finding FS-001 — CRITICAL (must correct before first sale):**

The NC-FIRST-SALE Playbook (Zone 2, Intelligence Stack) lists:
> "NARA: Verified archival source."

AS08-14-2383 is a **NASA** photograph. Its source is the NASA Image and Video Library. NARA holds administrative records of federal agencies including NASA, but the Earthrise image is not a NARA-catalogued item — it is a NASA-originating work. Presenting "NARA: Verified archival source" to a paying customer on the product page incorrectly represents the source of the image.

The COA copy ("linking the physical artifact to its digital record in the **National Archives**") compounds this: Earthrise has no `naId` in the NARA catalog. The digital provenance record is NASA's, not NARA's.

**This copy must be corrected before the first sale.** The Intelligence Stack must read:
```
NASA: Photograph by Astronaut William Anders, Apollo 8, December 24, 1968.
      17 U.S.C. § 105 — US government work, public domain.
```

The NARA entry must be removed entirely from the Earthrise product page. NARA attribution is correct for NARA-sourced assets (Hayden Map, Strata Series, etc.) — it is not correct here.

### I.2 Blocking Issue: Email 3 Uses a Deferred Asset

**Finding FS-002 — CRITICAL (must hold before launch):**

The NC-FIRST-SALE Playbook Email 3 (Launch + 24 Hours):
> Visual: Thomas Moran's *Grand Canyon of the Yellowstone*
> Copy: "Explore the art that convinced a nation to save its wilderness."

Thomas Moran's Yellowstone paintings are **deferred assets** (Smithsonian, no DD-SMITHSONIAN-001). They are not in any NC product catalog and may not be presented to paying customers as part of an NC product or campaign. Using this image in a launch email implies NC sells or endorses this work, which is a product-safety violation.

**Email 3 must be held.** A replacement Email 3 using product-safe assets (NC-NASA-026 Yellowstone from Orbit, or BHL Bison bison illustration) may be substituted. Email 3 may be reinstated using the Moran image only after DD-SMITHSONIAN-001 is ratified and the Moran Collection product is activated.

### I.3 Collector Edition: NOT READY

**Finding FS-003 — Phase 1b gate:**

The Collector Edition ("Earthrise: The Lunar Gate") specifies:
> "Includes a physical **1968 Apollo 8 Mission Plan reproduction (NARA)**"

This is a second asset — a distinct NARA document — that has not been identified, located, or IFC-1 cleared. It requires:
- Sprint 1 NARA API search to confirm the Apollo 8 Mission Plan `naId`
- `useRestriction.status == "Unrestricted"` confirmed per record
- Separate Gate E covering both assets (Earthrise photograph + mission plan document)
- SA-22 / SA-23 ratification OR manual Sprint 1 verification path per NC-COMMERCE-001 Art. 4

The Collector Edition cannot ship until the mission plan document is individually cleared. The standard museum giclée (NC-PROD-001) and digital download (NC-PROD-008) do not share this dependency — they are Earthrise photograph only.

### I.4 Everything Else Clears

With FS-001 and FS-002 corrected, and the Collector Edition deferred to Phase 1b:

- Rights: NC-NASA-002 is § 105, statutory PD, unconditional
- Attribution: NASA nonendorsement text is one sentence; placement is defined
- GeoNames: Not required (S-3 cosmic anchor exception)
- OSM: Not required (no map tiles on Earthrise page)
- SA ratification: Not required for Earthrise
- Sprint 1: Not required for NC-PROD-001 / NC-PROD-008
- NOAA write cap: Not consumed by Earthrise products
- External providers: No fulfillment constraint governed here (operational, not governance)

---

## II. Exact Earthrise Products to Activate

### Product A — NC-PROD-001: *Earthrise* Museum Giclée Print

| Field | Value |
|---|---|
| Asset | NC-NASA-002 (AS08-14-2383, Apollo 8, December 24, 1968) |
| Source | NASA Image and Video Library — not NARA |
| Rights | 17 U.S.C. § 105 — statutory public domain |
| Routing | `museum_print` → `museum_giclée` |
| CSM tier | MASTERWORK |
| Format | Archival giclée on 310gsm Hahnemühle Photo Rag, pigment inks |
| Print label | `Image credit: NASA. NASA does not endorse this product.` |
| COA | Required — see §III for compliant COA language |
| Edition | Standard open edition (not limited) unless Collector Edition is separately activated |
| Curator | Required — `museum_print` always + MASTERWORK tier |
| PA sign-off | Required — separate person from curator |
| GeoNames | Exempt — `geonames_exemption: "cosmic_anchor_S3_provisional"` |
| OSM | Not required |
| Gate E | Required — two-human, per this activation event |

### Product B — NC-PROD-008: *Earthrise* Digital Download

| Field | Value |
|---|---|
| Asset | NC-NASA-002 |
| Rights | 17 U.S.C. § 105 |
| Routing | `institutional_license` → `digital_license` |
| CSM tier | MASTERWORK |
| Delivery | High-resolution digital file (TIFF or lossless JPEG) |
| Package | Includes `nc:nasa_attribution` JSON metadata, consumer use rights notice, NASA nonendorsement text |
| Curator | Required — `institutional_license` always |
| PA sign-off | Required (fold into NC-PROD-001 Gate E session) |
| Gate E | Required — same session as NC-PROD-001 |

### Product C — Collector Edition: NOT READY

| Field | Value |
|---|---|
| Asset | NC-NASA-002 + NARA Apollo 8 Mission Plan (uncleared) |
| Status | **BLOCKED** — NARA mission plan `naId` not confirmed |
| Activation path | NARA Sprint 1 API lookup → `useRestriction.status == "Unrestricted"` → manual rights verification → separate Gate E |
| Expected phase | Phase 1b — after NARA Sprint 1 completes |
| Price point | $850 / 50 units — requires edition tracking system operational |

---

## III. Final Launch Checklist

All items must be confirmed before Gate E is signed. Items marked ⚠ are newly required by this review (not in prior checklists).

### A — Copy Corrections (NEW — from this review)

| # | Item | Authority | Status |
|---|---|---|---|
| A-1 | ⚠ Remove "NARA: Verified archival source" from Earthrise product page Zone 2 | FS-001 | ☐ REQUIRED |
| A-2 | ⚠ Update Intelligence Stack: `NASA: Photograph by William Anders, Apollo 8, December 24, 1968. § 105 — public domain.` | FS-001 | ☐ REQUIRED |
| A-3 | ⚠ Update COA: remove reference to "National Archives"; reference NASA as source | FS-001 | ☐ REQUIRED |
| A-4 | ⚠ Hold Email 3 (Moran *Grand Canyon of the Yellowstone*) — deferred asset; replace with product-safe visual | FS-002 | ☐ REQUIRED |

### B — Rights (IFC-1)

| # | Item | Authority | Status |
|---|---|---|---|
| B-1 | NC-NASA-002 `rights_status = 'verified_pd'` | IFC-1 | ☐ |
| B-2 | NC-NASA-002 `human_verified = TRUE` | IFC-1, FM-4 | ☐ |
| B-3 | `hard_gate_status = 'passed'` on commerce_opportunity for NC-NASA-002 | PRG-1 | ☐ |
| B-4 | `activation_target.status = 'activated'` set in same transaction as Gate E | IFC-11 | ☐ |

### C — Attribution

| # | Item | Authority | Status |
|---|---|---|---|
| C-1 | NASA nonendorsement on product listing: `Image credit: NASA. NASA does not endorse this product.` | DD-NASA-001; NC-PRODUCT-001 §5.1 | ☐ |
| C-2 | NASA nonendorsement on physical print label / packaging | NC-PRODUCT-001 §4.1 | ☐ |
| C-3 | NASA nonendorsement on COA | NC-PRODUCT-001 §4.3 | ☐ |
| C-4 | No NASA insignia, meatball logo, or endorsement language anywhere in product copy, COA, or email | NC-PILOT-001-LA §III.2 | ☐ |
| C-5 | Consumer use rights notice present on product detail page | NC-PILOT-001-LA §III.5 | ☐ |
| C-6 | Digital download package: `nc:nasa_attribution` JSON field populated; consumer notice in package | NC-PRODUCT-001 §4.2 | ☐ |
| C-7 | Earthrise page: no GeoNames attribution (correctly exempt); `geonames_exemption` field populated | SA-GEONAMES-001 §V.3 | ☐ |

### D — Gate E (Two-Human Activation)

| # | Item | Authority | Status |
|---|---|---|---|
| D-1 | Curator review completed for NC-PROD-001 (name + date) | NC-PRODUCT-001 Art. 11, Gate 7 | ☐ [name / date] |
| D-2 | Curator review completed for NC-PROD-008 (may be same session as D-1) | NC-PRODUCT-001 Art. 11, Gate 7 | ☐ [name / date] |
| D-3 | Principal Architect sign-off for NC-PROD-001 — must be distinct person from curator | IFC-11; NC-PRODUCT-001 Art. 11, Gate 8 | ☐ [name / date] |
| D-4 | Principal Architect sign-off for NC-PROD-008 | IFC-11 | ☐ [name / date] |

### E — Operational (not governance-gated, but required for first transaction)

| # | Item | Status |
|---|---|---|
| E-1 | Product page live and accessible (correct URL, no staging flags) | ☐ |
| E-2 | Payment processor active; test transaction completed | ☐ |
| E-3 | Print fulfillment partner confirmed; Hahnemühle Photo Rag stock confirmed | ☐ |
| E-4 | Digital download delivery mechanism tested (file accessible post-purchase) | ☐ |
| E-5 | Edition tracking system operational (for Collector Edition Phase 1b — not blocking Phase 1a) | ☐ |
| E-6 | T+30 rights audit calendar entry set (30 days from first sale date) | ☐ |
| E-7 | Earthrise 60-day cosmic anchor deadline calendar entry set | ☐ |

---

## IV. Activation Order

**Step 1 — Correct copy (A-1 through A-4).** Non-negotiable; no product may go live until FS-001 and FS-002 are resolved. Estimated effort: single content pass, < 1 hour.

**Step 2 — Gate E session (B + C + D).** Single curator + PA session covering both NC-PROD-001 and NC-PROD-008. Confirm rights fields in the database, verify all attribution text live on the staging product page, sign off. Estimated effort: < 2 hours.

**Step 3 — Activate NC-PROD-008 first (digital download).**
Activate the digital download before the physical print. Rationale: zero physical production dependency; validates the payment and attribution pipeline with the lowest operational risk before a physical print order is committed to production. If any attribution issue is discovered post-sale, a digital transaction is far easier to manage than a physical print in production.

**Step 4 — Activate NC-PROD-001 (museum giclée) immediately after.**
Once the digital download is confirmed live and correctly attributed, activate the print. Both products share the same Gate E — the print activation requires no additional governance action.

**Step 5 — Confirm Email 1 (Teaser) and Email 2 (Launch) only.**
Email 1 (blurred Earthrise silhouette) and Email 2 (full Earthrise hero shot) are product-safe and may be sent on schedule. Email 3 is held.

**Step 6 — NARA Sprint 1 for Collector Edition (Phase 1b).**
After Phase 1 is live, begin the NARA API Sprint 1 lookup for the Apollo 8 Mission Plan document. Confirm `naId` + `useRestriction.status == "Unrestricted"`. Run a separate Gate E for the Collector Edition. Activate when cleared.

---

## V. Revenue Readiness

| Product | Revenue-ready? | Condition |
|---|---|---|
| NC-PROD-008 Earthrise Digital Download | **YES** — upon copy corrections + Gate E | Steps 1–2 above |
| NC-PROD-001 Earthrise Museum Giclée | **YES** — upon copy corrections + Gate E | Steps 1–4 above |
| Collector Edition | **NO** | NARA Sprint 1 required |
| Any Phase 2+ product | **NO** | SA-GEONAMES-001 + SA-OSM-001 ratification required |

**The governance chain is complete for Phase 1.** IFC-1 is satisfiable. FM-4 is satisfiable. Gate E is executable. Attribution is defined and one-sentence simple. The two copy corrections (FS-001, FS-002) are product-page edits, not governance documents. They do not require a new DD, SA, or PA review event — they require a content fix.

**First sale is one Gate E session away.**

---

## VI. Authorization

### VI.1 Decision

**FIRST SALE AUTHORIZED**

for NC-PROD-001 (*Earthrise* Museum Giclée Print) and NC-PROD-008 (*Earthrise* Digital Download), subject to the two mandatory copy corrections identified in §I (FS-001 and FS-002) and completion of Gate E.

The Collector Edition is NOT AUTHORIZED for Phase 1. It is authorized to proceed through NARA Sprint 1 as a Phase 1b activation.

### VI.2 Decision Articles

**Article 1 — First Sale Authorization.**
NC-PROD-001 and NC-PROD-008 are authorized to generate revenue. The governance architecture is complete: rights are statutory (§ 105), attribution is one obligation (NASA nonendorsement), no SA ratification is required, no Sprint is required, no GeoNames or OSM dependency exists. The two mandatory corrections (FS-001, FS-002) are product-copy edits within NC's immediate control.

**Article 2 — Mandatory Corrections Are Pre-Gate.**
Items A-1 through A-4 in the Final Launch Checklist are pre-conditions for Gate E. The curator and Principal Architect must confirm that copy corrections are live on the staging product page before signing Gate E. Gate E signed against uncorrected copy is invalid.

**Article 3 — Earthrise Is NASA, Not NARA.**
For all current Earthrise products, the source is NASA and the attribution is NASA. NARA is not a source for NC-NASA-002. No Earthrise product copy, COA, certificate, email, or listing may reference NARA as the image source. NARA attribution (Record Group + naId format) is reserved for NARA-sourced assets (Hayden Map, Strata Series, Mission Plan document pending Sprint 1).

**Article 4 — Moran Is Held.**
Email 3 and any other marketing material referencing Thomas Moran's Yellowstone paintings is held. No launch communication may present a deferred asset as an NC product or imply its commercial availability.

**Article 5 — Digital Before Print.**
NC-PROD-008 activates before NC-PROD-001 in the operational sequence. Both share the same Gate E. The digital activation validates the payment and attribution pipeline before any physical print production is committed.

**Article 6 — Collector Edition Phase 1b.**
The Collector Edition is commercially promising ($850, 50 units, waitlist model) but requires a NARA asset that is not yet IFC-1 cleared. It is held for Phase 1b. Once the Apollo 8 Mission Plan `naId` is confirmed and `useRestriction.status == "Unrestricted"` is verified per DD-NARA-001, a separate Gate E activates the Collector Edition.

**Article 7 — 60-Day Clock Starts at First Sale.**
The Earthrise cosmic anchor 60-day deadline (Standards Constitution amendment or proxy-place GeoNames ID) begins on the date of first sale, not the date of this authorization. The options remain: (a) Standards Constitution amendment adding `cosmic_anchor` place type, or (b) Pacific Ocean proxy GeoNames ID assignment. The first sale may proceed without resolution — Earthrise products are commercial regardless of place governance status.

---

## VII. Ratification Table

| Role | Decision | Date |
|---|---|---|
| First Sale Authorization Review | ☑ AUTHORIZED | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*NC-FIRST-SALE-AUTH — drafted 2026-06-11*
*Reviews: NC-COMMERCE-001 · NC-COMMERCE-002 · NC-FIRST-SALE Playbook*
*First sale: NC-PROD-008 (digital) then NC-PROD-001 (print) · Two mandatory copy corrections required · Collector Edition Phase 1b*
