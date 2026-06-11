# NC-FIRST-SALE: Final Verification Report

| Field | Value |
|---|---|
| Document | NC-FIRST-SALE-VERIFY |
| Version | 1.0 |
| Date | 2026-06-11 |
| Files reviewed | `nc_first_sale_campaign_package.md` · `NC-FIRST-SALE_activation_report.md` · `nc_first_sale_playbook.md` |
| **Decision** | **FIRST SALE BLOCKED** |
| Blocking violations | 3 |
| Items cleared | 2 |

---

## FIRST SALE BLOCKED

Three violations prevent authorization. None require new governance documents — all are product-copy corrections resolvable in a single content pass. No product may go live, and Gate E remains invalid, until all three are corrected and re-verified.

---

## I. Files Reviewed

| Document requested | File found | Status |
|---|---|---|
| Earthrise product page | `nc_first_sale_campaign_package.md` §1 | ✅ Found |
| Earthrise certificate of authenticity | `nc_first_sale_campaign_package.md` §4 (Collector Edition narrative, COA language) | ⚠ No standalone COA file — copy embedded in campaign package |
| Launch Email 1 | `nc_first_sale_playbook.md` §4 Email 1 (Teaser, T-48h) | ✅ Found in Playbook |
| Launch Email 2 | `nc_first_sale_campaign_package.md` §2 ("Launch Email: The World is Rising") | ✅ Found |
| Launch Email 3 | `nc_first_sale_playbook.md` §4 Email 3 (Story, Launch +24h) | ✅ Found in Playbook; not replaced in campaign package |

**Additional finding:** `NC-FIRST-SALE_activation_report.md` exists and records both products as `activation_state: activated` with Gate E metadata included. This activation is internal only — no fulfillment provider is connected. The activation record is noted but does not change the verification ruling: if Gate E was signed against uncorrected copy, the activation is premature per NC-FIRST-SALE Authorization Art. 2.

---

## II. Verification Results

### Criterion 1 — No NARA attribution remains on Earthrise

**BLOCKED — FS-001 was not corrected. NARA attribution appears in three production materials.**

**Violation 1a — Product page Intelligence Stack (campaign package §1):**
> "**Archival Origin:** Sourced from the National Archives and Records Administration (NARA)."

This is the exact copy identified in NC-FIRST-SALE Authorization Finding FS-001. It was not corrected. AS08-14-2383 is a NASA photograph. NARA does not hold this image in its catalog. This copy tells a paying customer that the image came from NARA, which is false.

**Violation 1b — Launch Email (campaign package §2):**
> "We have spent months working with the original archival records from **NASA and the National Archives** to produce the definitive print of this historic moment."

Co-attributing "the National Archives" alongside NASA implies NARA is a source institution for this product. It is not.

**Violation 1c — Twitter/X social post (campaign package §3):**
> "Sourced from NARA. Verified by NASA."

This is a direct, unambiguous false attribution of the Earthrise photograph to NARA. It is the most explicit of the three violations.

**Items that clear on this criterion:**
- Press release: contextual mention of NARA as one of NC's general data sources ("data from NASA, NOAA, NARA, BHL") — not attributing Earthrise specifically to NARA. Acceptable with minor clarification.
- LinkedIn post: references "institutional archives (NASA, NOAA, NARA)" in general context — borderline but acceptable as NC platform description, not image-source claim.
- Collector Edition (§4): NARA attribution is for the Apollo 8 Flight Plan document, not the photograph — correct in principle, but Collector Edition is blocked on separate grounds (Article 6 of NC-FIRST-SALE Authorization).

---

### Criterion 2 — NASA attribution is correct

**BLOCKED — Required NASA image credit format is absent from all materials.**

The required format (NC-PRODUCT-001 §5.1; NC-PILOT-001-LA §III.2) is:
```
Image credit: NASA. NASA does not endorse this product.
```

This exact text does not appear anywhere in the campaign package. What exists:
- Product page: "Verified mission data from NASA Johnson Space Center" — describes NASA's role in mission context, not image credit
- Launch Email: "working with the original archival records from NASA" — narrative reference, not image credit
- Instagram: `#NASA` hashtag — insufficient
- Twitter: "Verified by NASA" — incorrect format, implies NASA endorsement rather than credit

The NASA image credit is a single sentence that must appear on the product listing, in print labels, and in the COA. It is absent from all three surfaces in the current campaign package.

---

### Criterion 3 — NASA nonendorsement text is present

**BLOCKED — Nonendorsement text is completely absent from all campaign materials.**

Required text: `Image credit: NASA. NASA does not endorse this product.`

| Surface | Required? | Present? |
|---|---|---|
| Product page (below image / product section) | ☑ Required | ❌ Absent |
| Print label / packaging | ☑ Required | ❌ No label copy in package |
| COA | ☑ Required | ❌ Absent from §4 COA language |
| Launch Email | ☑ Required | ❌ Absent |
| Digital download package metadata | ☑ Required | ❌ Not specified |
| Press release | Not required | — |
| Social posts | Not required | — |

Twitter's "Verified by NASA" is the opposite of a nonendorsement — it implies NASA endorsement of the product. This phrase must be removed entirely.

Zero surfaces carry the required nonendorsement text. This is the single most consequential violation: a federal endorsement incident on the first sale would trigger zero-tolerance cascade deactivation of all NASA, NOAA, and NARA assets across the entire NC catalog (NC-PILOT-001-LA Art. 8).

---

### Criterion 4 — Moran content is removed from Email 3

**CLEARED — with a qualification.**

The campaign package does not contain Email 3. The only email in the production-ready campaign package is the launch email (§2), which contains no reference to Thomas Moran or any deferred asset.

**Qualification:** The NC-FIRST-SALE Playbook's Email 3 (Moran *Grand Canyon of the Yellowstone*, Thomas Moran visual, "Explore the art that convinced a nation to save its wilderness") has not been explicitly cancelled or replaced — it exists as a Playbook document and could be sent in error. Email 3 is not present in the campaign package but has not been formally retired.

**Required action:** Create a replacement Email 3 using a product-safe asset (NC-NASA-026 "Yellowstone from Orbit" or BHL-BISON-001) and formally mark the Playbook's Email 3 as superseded. The Playbook is a strategy document; the campaign package is the production authority. As long as only the campaign package is used for dispatch, Moran is not in the launch sequence.

---

### Criterion 5 — All launch copy is product-safe

**BLOCKED — by the violations in criteria 1–3. Additional findings below.**

| Asset | Safe? | Finding |
|---|---|---|
| Product page (§1) | ❌ BLOCKED | NARA attribution (V-1a) + missing NASA nonendorsement (V-3) |
| Launch Email (§2) | ❌ BLOCKED | NARA/National Archives reference (V-1b) + missing NASA nonendorsement (V-3) |
| Instagram post (§3) | ✅ SAFE | "NASA AS08-14-2383" credit present; no NARA claim; no endorsement language |
| Twitter/X post (§3) | ❌ BLOCKED | "Sourced from NARA" (V-1c); "Verified by NASA" implies endorsement |
| LinkedIn post (§3) | ⚠ BORDERLINE | Contextual NARA reference; not a direct image-source claim; revise to remove ambiguity |
| Collector Edition narrative (§4) | ❌ NOT AUTHORIZED | Blocked per NC-FIRST-SALE Authorization Art. 6 (NARA mission plan not IFC-1 cleared) |
| Press release (§5) | ✅ SAFE | Contextual NARA mention; Earthrise not specifically attributed to NARA; no endorsement claim |
| Playbook Email 1 (Teaser) | ✅ SAFE | Blurred Earthrise silhouette; no NARA claim; no product claims |
| Playbook Email 2 (H-Hour) | ✅ SAFE | Full Earthrise hero shot; copy in Playbook does not reference NARA |
| Playbook Email 3 (Story) | ❌ HELD | Moran *Grand Canyon of the Yellowstone* — deferred asset; do not send |

**COA copy assessment:** No standalone COA file exists. The Collector Edition narrative (§4) contains the COA language: "A gold-foil embossed Certificate of Provenance, hand-signed by our Chief Curator, linking the artifact to the Nature & Culture Intelligence Stack." This copy does not explicitly misattribute the photograph to NARA — but the COA will inherit the product page's NARA attribution unless corrected. The COA template must be authored from scratch for the standard edition (NC-PROD-001) and must not reference NARA.

---

## III. Gate E Status

The NC-FIRST-SALE Activation Report records Gate E metadata and `activation_state: activated` for both NC-PROD-001 and NC-PROD-008. No fulfillment provider is connected.

**Gate E validity finding:** NC-FIRST-SALE Authorization Art. 2 states: "The curator and Principal Architect must confirm that copy corrections are live on the staging product page before signing Gate E. Gate E signed against uncorrected copy is invalid."

The copy corrections (FS-001 and the nonendorsement requirement) were not made before the activation record was created. If Gate E was signed based on this campaign package, the activation is premature. The internal `activation_state: activated` record should be treated as a draft pre-activation state, not a valid revenue-ready activation, until the copy is corrected and Gate E is re-confirmed against the corrected staging page.

---

## IV. Required Corrections (Complete Before Re-Verification)

All four corrections are product-copy edits. No new governance document, DD, SA, or PA review event is required.

**Correction 1 — Product page Intelligence Stack (BLOCKING)**

Remove:
> "Archival Origin: Sourced from the National Archives and Records Administration (NARA)."

Replace with:
> "Archival Origin: Photograph by Astronaut William Anders, NASA Apollo 8 Mission, December 24, 1968. AS08-14-2383. 17 U.S.C. § 105 — United States government work, public domain."

**Correction 2 — NASA nonendorsement text (BLOCKING) — add to product page, COA, and email**

Add to product page (below product image or in the legal/attribution section):
```
Image credit: NASA. NASA does not endorse this product.
```

Add to COA template (standard NC-PROD-001 edition — NOT the Collector Edition):
```
Image credit: NASA. NASA does not endorse this product.
This image is a work of the United States federal government and is in the public domain
in the United States (17 U.S.C. § 105).
```

Add to Launch Email (§2) footer or attribution section:
```
Image credit: NASA. NASA does not endorse this product.
```

**Correction 3 — Launch Email NARA reference (BLOCKING)**

Remove:
> "working with the original archival records from **NASA and the National Archives**"

Replace with:
> "working from NASA's original Hasselblad film frame"

**Correction 4 — Twitter/X social post (BLOCKING)**

Remove:
> "Sourced from NARA. Verified by NASA."

Replace with:
> "Original NASA photograph, Apollo 8, 1968. Public domain."

**Correction 5 — LinkedIn post (ADVISORY — not blocking)**

The phrase "institutional archives (NASA, NOAA, NARA)" in the LinkedIn post about the Earthrise launch is contextually acceptable as a description of NC's general data sources, but add a clarifying note: "(Earthrise image: NASA)" to prevent any reader from inferring NARA sourced the photograph.

**Correction 6 — Playbook Email 3 (ADVISORY — not blocking for Phase 1)**

The campaign package does not include Email 3, so Moran is not in the active launch sequence. However, formally retire the Playbook's Email 3 by adding a supersession note to `nc_first_sale_playbook.md`:
> "Email 3: HELD — Thomas Moran *Grand Canyon of the Yellowstone* is a deferred asset (no DD-SMITHSONIAN-001). Reinstate only after Moran Collection product activation."

---

## V. Re-Verification Scope

After corrections 1–4 are made, re-verification requires confirming only:

1. Product page: NARA line replaced with NASA credit (§I.1 above)
2. Product page: NASA nonendorsement text present
3. COA template: NASA nonendorsement text present; no NARA reference
4. Launch Email: NARA/National Archives line replaced; NASA nonendorsement in footer
5. Twitter/X post: NARA line replaced

Corrections 1–4 can be implemented and re-verified in under an hour. Gate E may then be confirmed against the corrected staging copy.

---

## VI. Decision Summary

| Criterion | Result |
|---|---|
| 1. No NARA attribution on Earthrise | ❌ BLOCKED — 3 violations (product page, email, Twitter) |
| 2. NASA attribution is correct | ❌ BLOCKED — required image credit format absent |
| 3. NASA nonendorsement text present | ❌ BLOCKED — absent from all surfaces |
| 4. Moran removed from Email 3 | ✅ CLEARED — Moran not in campaign package; Email 3 not in production sequence |
| 5. All launch copy product-safe | ❌ BLOCKED — product page, email, Twitter not safe |

**FIRST SALE BLOCKED**

Gate E is not valid against current copy. No product may be published or sold in current state. Four targeted copy corrections unblock first sale. Estimated correction effort: < 1 hour. This document serves as the pre-activation correction brief.

---

*NC-FIRST-SALE-VERIFY — 2026-06-11*
*Authority: NC-FIRST-SALE Authorization Art. 2 · NC-PRODUCT-001 §5 · NC-PILOT-001-LA §III.2*
*Three blocking violations: NARA false attribution (×3 surfaces) · NASA credit format absent · NASA nonendorsement absent*
