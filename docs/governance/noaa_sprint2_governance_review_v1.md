# NOAA Sprint 2 Governance Review v1

| Field | Value |
|---|---|
| Version | 1.0 |
| Status | DRAFT — Pending Ratification |
| Review Authority | NC Governance |
| Sprint | Sprint 2 entry gate |
| Governing Documents | DD-NOAA-001 · SA-NOAA-001 · SA-NOAA-002 · NOAA Governance Review v1 |
| Sprint 1 Status | Complete — 20 tests passing |
| Date | 2026-06-11 |
| Implementation Reviewed | `workers/noaa_adapter/rights.py` · `workers/noaa_adapter/client.py` · `workers/noaa_adapter/normalize.py` |

---

## DECISION

**APPROVE WITH CONDITIONS**

SA-NOAA-001 is RATIFIED. SA-NOAA-002 is RATIFIED. The Sprint 1 implementation is substantially correct on its core compliance obligations: IFC-1 hard gate structure is sound, commercial operator blocking (Getty, Reuters, AP, Maxar, DigitalGlobe, Planet, GeoEye) is present and tested, FM-4 is respected, no store writes exist, and the Flickr API client is replay-stable.

Two compliance violations require correction before Sprint 2 work begins:

**Violation 1 (Hard):** Personal name/NOAA credits are routed to `REVIEW_REQUIRED`. Governance Review v1 Section V explicitly ruled these must be `BLOCKED`. This is an unambiguous implementation error.

**Violation 2 (Hard):** Other US federal agency credits (NASA, USGS, USFWS, NPS, EPA, NSF, USACE, NIST) are absent from the allow-list. Images from these agencies hosted in NOAA's collection would fall to `BLOCKED (missing_rights_evidence)` instead of `ALLOWED`. SA-NOAA-001 Part VI.3 requires these.

Two additional corrections are required before Sprint 2 to prevent latent issues from entering production:

**Correction 3:** `url_m` (~500px) must be removed from the `choose_image_url` hierarchy. SA-NOAA-002 Section I.6 sets 640px (`url_z`) as the minimum acceptable resolution. `url_m` is below that floor.

**Correction 4:** NOAA credit prefix-match must cover space-separated division names ("NOAA Coral Reef Watch", "NOAA Fisheries Service") in addition to slash-separated ones. The current code handles "NOAA/" correctly but silently falls through on "NOAA " (space) patterns.

Sprint 2 is authorized to begin after all four corrections are in code and the five Sprint 2 gates in Section IX are met.

---

## I. SA-NOAA-001 Ratification

**RATIFIED** — with implementation correction conditions binding on Sprint 2.

SA-NOAA-001 as drafted is correct. The rights matrix's structure, governing principle, invariants, block reason code registry, and rights evidence field specification are sound and constitute a complete Rights Class 9 governance document for NOAA. The five issues noted below are implementation deviations from the ratified SA, not errors in the SA itself. The SA does not require amendment; the implementation does.

**Ratification finding — dual-path scope:** SA-NOAA-001 correctly scopes both Path A (Flickr) and Path B (Photo Library) and correctly designates Path A as Sprint 1 only. This is confirmed in the implementation (`photolib_record_to_discovery_payload` exists and is fixture-tested, establishing the structural foundation for Path B without activating it for production). SA-NOAA-001's dual-path architecture is properly anticipated in the Sprint 1 code.

**Ratification finding — block reason code registry:** The registry in SA-NOAA-001 Part VIII uses reason codes that do not all appear in the implementation. The implementation uses `rights_basis` strings rather than structured `reason` codes. This is a naming difference, not a structural problem — the mapping is traceable. SA-NOAA-001 v1.1 should align terminology with the implementation's `rights_basis` vocabulary. Not a ratification blocker.

**SA-NOAA-001 Status: RATIFIED as of 2026-06-11.**

---

## II. SA-NOAA-002 Ratification

**RATIFIED** — with implementation correction conditions binding on Sprint 2.

SA-NOAA-002 as drafted is correct. The delivery protocol, URL hierarchy, Platform Dependency Statement (Part IV), Sprint 1 scope limitation, halt conditions, and path-promotion decision gate (Gate 2A / Gate 2B) are complete and implementable. Correction 3 (`url_m` removal) is an implementation deviation from the ratified SA.

**Ratification finding — method name:** SA-NOAA-002 Section I.2 specifies `flickr.people.getPhotos`. The implementation uses `flickr.people.getPublicPhotos`. For NOAA's public government accounts, these are functionally equivalent without authentication. `getPublicPhotos` is the correct unauthenticated method for public albums; `getPhotos` requires authentication for private accounts. The implementation's choice is acceptable and preferable for Sprint 1. SA-NOAA-002 v1.1 will update the method name to `getPublicPhotos` to match the implementation. Not a ratification blocker.

**Ratification finding — license pre-filter absent:** SA-NOAA-002 Section I.3 specifies `license=7,8,9,10` as a request parameter. The implementation does not pass this parameter. All public photos are returned and rights-gated in Python. This is safe — no compliant records are incorrectly admitted — but produces more API traffic than necessary. SA-NOAA-002 v1.1 will note this as a Sprint 2 efficiency optimization. Not a ratification blocker.

**Ratification finding — NSID resolution:** SA-NOAA-002 Section I.5 requires confirmed NSIDs for @usoceangov and @noaafisheries. The implementation uses usernames as the default (`DEFAULT_FLICKR_USER_ID = "usoceangov"`). Usernames can change; NSIDs are stable. Sprint 1 was expected to confirm NSIDs; this is a Sprint 2 gate item (Section IX, Gate 5).

**Ratification finding — Platform Dependency Statement:** SA-NOAA-002 Part IV is present and complete. The Sprint 1 scope cap, halt conditions, and Gate 2A / 2B path-promotion decision are all specified. The Sprint 2 gate requiring Photo Library evaluation finding (Gate 6, Section IX) is the implementation of SA-NOAA-002 Section IV.4.

**SA-NOAA-002 Status: RATIFIED as of 2026-06-11.**

---

## III. Rights Class 9 Reuse Verification

**CONFIRMED — implementation compliant.**

The implementation correctly reuses Rights Class 9 without introducing a new class:
- `RIGHTS_POLICY_ID = "noaa_rights_matrix_v1"` — distinct from NARA's `nara_rights_matrix_v1`
- `rights["rights_status"]` written as `"pending_verification"` throughout — FM-4 compliant
- No `"verified_pd"` or `"classified_pd"` written by any adapter worker function
- `"rights_class": 9` present in the SA-NOAA-001 rights evidence schema
- The `rights_statement_uri` maps to `NO_COPYRIGHT_US_URI` (the `NoC-US/1.0/` Rights Statements URI) — correct for 17 U.S.C. § 105

Rights Class 9 dual-path novelty is correctly implemented: `access_path` and `primary_gate_field` are distinct per path in the `build_rights_evidence` output, though these fields are not explicitly set in the current `normalize.py` implementation. Sprint 2 must add `access_path` and `primary_gate_field` to the evidence envelope per SA-NOAA-001 Part VII. Minor Sprint 2 item.

---

## IV. Contributor Detection Precedence Review

The implementation's precedence order in `classify_rights` is:

```
1. missing/empty record          → BLOCKED
2. blocked_markers (commercial)  → BLOCKED
3. license_id == "0"             → BLOCKED
4. partner_markers               → REVIEW_REQUIRED
5. contributor_markers           → REVIEW_REQUIRED     ← VIOLATION
6. license_id == "8"             → ALLOWED
7. _is_noaa_federal_credit       → ALLOWED
8. license_id in {7, 9, 10}      → REVIEW_REQUIRED
9. license_id in {1–6}           → BLOCKED
10. fallback                     → BLOCKED
```

**Compliance assessment of each step:**

**Steps 1–3 (BLOCKED):** COMPLIANT. Missing record, commercial operator, and license 0 are all correctly blocked before any allow logic.

**Step 4 (partner_markers → REVIEW_REQUIRED):** ACCEPTABLE DIVERGENCE. SA-NOAA-001 Part II.1 specifies `"Courtesy of [non-federal]"` → BLOCKED. The implementation routes University, NGO, Foundation, and similar markers to REVIEW_REQUIRED. This is more permissive than the SA in that it routes these to review rather than immediate block, but it is not a hard compliance violation: REVIEW_REQUIRED means `rights_status: "pending_verification"` — no production write until human review. This creates a human review queue for partner-institution imagery that may carry permissive CC licensing. Governance accepts this divergence for Sprint 2. SA-NOAA-001 v1.1 will document REVIEW_REQUIRED as the partner-institution handling path.

**Step 5 (contributor_markers → REVIEW_REQUIRED):** **NON-COMPLIANT — Violation 1.** SA-NOAA-001 Part V explicitly states personal name/NOAA credits must produce `BLOCKED (contributed_image_exception)`. Governance Review v1 Section V ruled: "BLOCKED — not REVIEW_REQUIRED" with explicit rationale (NC cannot verify federal employment status from public metadata at scale; conservative block rule is correct). The implementation contradicts this ruling. Must be corrected before Sprint 2. See Section V.

**Step 6 (license_id == "8" → ALLOWED):** COMPLIANT. Flickr License 8 is the primary IFC-1 gate for Path A. Correct.

**Note on steps 4–6 ordering:** The current order means a license=8 record with a partner institution mention in its description is routed to REVIEW_REQUIRED (step 4) before reaching the license=8 gate (step 6). This is more conservative than the SA intends (license 8 is the primary gate; secondary validation is a backstop for mislabelled records). However, for Sprint 2 this conservative ordering is acceptable — routing a genuine government photo to REVIEW_REQUIRED is a false negative that a human can correct; routing a contributed image to ALLOWED would be a false positive that violates IFC-1. Conservatism in the safe direction is acceptable for Sprint 2.

**Step 7 (_is_noaa_federal_credit → ALLOWED):** PARTIAL COMPLIANT. See Section V (credit detection gap).

**Steps 8–10:** COMPLIANT for their respective decisions.

---

## V. Route Verification

### V.1 NOAA Prefix → ALLOWED

**PARTIAL COMPLIANT — Correction 4 required.**

The `_is_noaa_federal_credit` function handles two cases:
1. Exact match against enumerated `NOAA_FEDERAL_CREDIT_PATTERNS` → ALLOWED
2. `credit.lower().startswith(f"{pattern.lower()}/")` for any pattern in the list → ALLOWED

Since "NOAA" is in the pattern list, any credit starting with "NOAA/" (slash-delimited) is correctly handled:
- "NOAA/NMFS" ✓
- "NOAA/PMEL" ✓ (covered by "NOAA" + "/" prefix logic)
- "NOAA/Coral Reef Watch" ✓ (covered)

**Gap:** Credits starting with "NOAA " (space, not slash) are NOT covered:
- "NOAA Coral Reef Watch" — lowered = "noaa coral reef watch" — not in exact list, not matched by `startswith("noaa/")` → falls to BLOCKED
- "NOAA Fisheries Service" — same gap
- "National Ocean Service" — also not in list (only "NOAA Ocean Service" is)

This gap affects Photo Library (Path B) more than Flickr (Path A), since Flickr images pass the license-8 gate before reaching the credit check. But for Path B production and for any Flickr record with license 7/9/10, space-separated NOAA names would be incorrectly blocked.

**Required correction:** Add `credit.lower().startswith("noaa ")` to the prefix-match logic, and add `"National Oceanic and Atmospheric Administration"` to exact-match. These are safe additions under the personal-name guard (step 3 in `_is_noaa_federal_credit` already checks for personal names).

### V.2 Personal Name/NOAA → BLOCKED

**NON-COMPLIANT — Violation 1 — Sprint 2 blocking item.**

The implementation routes personal name/NOAA credits to `REVIEW_REQUIRED` with `rights_basis: "personal_name_noaa_credit"`. Tests confirm this:

```
flickr_photo_personal_noaa_review.json → REVIEW_REQUIRED
```

Governance Review v1 Section V ruled explicitly: "BLOCKED — not REVIEW_REQUIRED." The implementation contradicts this ruling. The rationale stands: NC cannot verify federal employment status from public metadata at scale; a human review queue for contributor attribution is operationally untenable. The IFC-1 conservative rule is BLOCKED.

**Required correction:**
In `rights.py`, the `contributor_markers` branch must be changed from:
```python
if contributor_markers:
    return _result(
        decision=RightsDecision.REVIEW_REQUIRED,
        ...
        rights_basis="personal_name_noaa_credit",
    )
```
To:
```python
if contributor_markers:
    return _result(
        decision=RightsDecision.BLOCKED,
        allowed=False,
        rights_statement_uri=None,
        rights_status="blocked",
        rights_basis="contributed_image_exception",
        contributor_markers=contributor_markers,
    )
```

The corresponding test `test_noaa_rights_reviews_contributor_and_partner_markers` must be updated to assert `BLOCKED` (not `REVIEW_REQUIRED`) for the personal name fixture case.

### V.3 Foreign Agency → REVIEW_REQUIRED

**COMPLIANT for the joint-mission case. Acceptable for solo foreign credits.**

The implementation routes ESA, JAXA, CSA, MBARI, and Schmidt Ocean Institute credits to REVIEW_REQUIRED via `REVIEW_PARTNER_MARKERS`. Tests confirm:

```
flickr_photo_foreign_agency_review.json → REVIEW_REQUIRED (partner_or_contributor_marker)
```

SA-NOAA-001 Part IV.3 specifies a distinction between solo foreign agency credits (BLOCKED, `not_us_federal_work`) and joint-mission credits (REVIEW_REQUIRED). The implementation does not make this distinction — it routes all foreign agency credits to REVIEW_REQUIRED regardless of whether a US federal co-credit is present. 

**Governance ruling:** This is an acceptable deviation for Sprint 2. REVIEW_REQUIRED for solo foreign agency credits is more permissive than the SA intends in theory, but safe in practice: no production write proceeds without human review. The SA's "BLOCKED for solo foreign" rule avoids creating unnecessary review queue load; the implementation's REVIEW_REQUIRED creates a human review queue that will mostly reject anyway. The conservative-in-the-right-direction argument applies here as it does to step 4 ordering.

SA-NOAA-001 v1.1 will align the specification to REVIEW_REQUIRED for all foreign agency credits (removing the solo/joint distinction as an implementation concern, since the human review queue handles both cases correctly).

**No correction required for Sprint 2 on this item.**

### V.4 Getty / AP / Reuters → BLOCKED

**COMPLIANT — fully tested.**

All three commercial news agencies are present in `BLOCKED_MARKERS`:
```python
BLOCKED_MARKERS = ("Getty", "Reuters", "AP", "Maxar", "DigitalGlobe", "Planet", "GeoEye")
```

Tests confirm all three block correctly:
```
flickr_photo_getty_blocked.json   → BLOCKED (Getty in blocked_markers)
flickr_photo_reuters_blocked.json → BLOCKED (Reuters in blocked_markers)
flickr_photo_ap_blocked.json      → BLOCKED (AP in blocked_markers)
```

The `"AP"` pattern uses word-boundary matching (`rf"(?<![A-Za-z0-9]){re.escape(marker)}(?![A-Za-z0-9])"`) which correctly prevents false positives from "AP" appearing as a substring (e.g., "NOAA/PMEL" or "Capped Petrel" are not matched). The word-boundary regex in `_detect_markers` resolves the "AP" ambiguity concern from SA-NOAA-001 OQ-2 in a clean, generalizable way.

**SA-NOAA-001 OQ-2 is closed.** The word-boundary regex is the correct implementation.

---

## VI. Compliance Issue Detail: Other US Federal Agencies (Violation 2)

**NON-COMPLIANT — Violation 2 — Sprint 2 blocking item.**

SA-NOAA-001 Part VI.3 requires the following US federal agency names to produce ALLOWED when appearing as the primary credit (without personal name or commercial operator):

NASA, USGS, USFWS, NPS, EPA, NSF, USACE, NIST

None of these appear in `NOAA_FEDERAL_CREDIT_PATTERNS`. A NOAA-hosted NASA image (e.g., credit "NASA/GSFC") would pass the BLOCKED_MARKERS check, pass the partner_markers check, fail the license_id=="8" gate (if tagged 7 or 0), fail `_is_noaa_federal_credit` (no "NOAA" prefix), and fall to BLOCKED (`missing_rights_evidence`). This incorrectly blocks legitimate § 105 federal works.

**Required correction:** Add these patterns to `NOAA_FEDERAL_CREDIT_PATTERNS` (or a new `FEDERAL_AGENCY_ALLOW_PATTERNS` constant):

```python
FEDERAL_AGENCY_ALLOW_PATTERNS = (
    "NASA",
    "USGS",
    "U.S. Geological Survey",
    "US Geological Survey",
    "USFWS",
    "US Fish and Wildlife Service",
    "U.S. Fish and Wildlife Service",
    "NPS",
    "National Park Service",
    "EPA",
    "U.S. Environmental Protection Agency",
    "NSF",
    "National Science Foundation",
    "USACE",
    "U.S. Army Corps of Engineers",
    "NIST",
    "National Institute of Standards and Technology",
)
```

Apply the same prefix-match and personal-name-guard logic as `_is_noaa_federal_credit`. A NASA image with credit "NASA/Bill Ingalls" must still be BLOCKED (personal name guard); "NASA" alone or "NASA/GSFC" must be ALLOWED.

---

## VII. Compliance Issue Detail: `url_m` Below Minimum Resolution (Correction 3)

**NON-COMPLIANT — Correction 3 required before Sprint 2.**

`choose_image_url` in `client.py`:

```python
for key in ("url_o", "url_l", "url_c", "url_z", "url_m"):
```

SA-NOAA-002 Section I.6 specifies the minimum acceptable resolution as `url_z` (640px longest side). Any record that falls through `url_o → url_l → url_c → url_z` to `url_m` (~500px) must be BLOCKED with `reason: "insufficient_resolution"`, not silently accepted at 500px.

**Required correction:**

```python
for key in ("url_o", "url_l", "url_c", "url_z"):
    value = _string(data.get(key))
    if value:
        return value
return None  # caller blocks with missing_image_evidence
```

Remove `"url_m"` from the hierarchy. Any record that has only `url_m` available has no image at the SA minimum and must be blocked.

---

## VIII. Additional Observations (Non-Blocking)

These items are noted for SA-NOAA-001/002 v1.1 and Sprint 2 awareness but do not block Sprint 2 authorization.

**OB-1 — Method name alignment:** SA-NOAA-002 specifies `flickr.people.getPhotos`; implementation uses `flickr.people.getPublicPhotos`. `getPublicPhotos` is the correct unauthenticated method and is preferable. SA-NOAA-002 v1.1 will update the specified method name to match. No correction required.

**OB-2 — License pre-filter absent:** SA-NOAA-002 Section I.3 specifies `license=7,8,9,10` as a request parameter for efficiency. The implementation omits this; all licenses are returned and rights-gated in Python. Safe but inefficient. Sprint 2 should add the pre-filter as an optimization. No blocking issue.

**OB-3 — access_path and primary_gate_field missing from evidence:** SA-NOAA-001 Part VII specifies `access_path` and `primary_gate_field` in the rights evidence envelope. The `build_rights_evidence` function in `normalize.py` does not write these fields. Sprint 2 must add them to complete the evidence schema. Non-blocking for Sprint 1 replay tests.

**OB-4 — SA-NOAA-001 OQ-2 closed:** The "AP standalone" ambiguity is resolved by the word-boundary regex in `_detect_markers`. No SA amendment needed.

**OB-5 — SA-NOAA-001 OQ-4 closed for Flickr path:** The Flickr `description` field carries "Credit:" prefixed lines that `extract_credit` parses correctly (confirmed in `test_noaa_client_extracts_flickr_records_and_credit`). The "Photo Library credit field name" question remains open for Path B, pending Sprint 1 evaluation finding.

---

## IX. Sprint 2 Approval Gates

All six gates must be met before Sprint 2 M36 integration work begins. Gates 1–4 are code corrections from this review. Gates 5–6 are SA-NOAA-002 path-promotion requirements.

### Gate 1 — Personal Name Credits: BLOCKED (not REVIEW_REQUIRED)

`rights.py` must be corrected so `contributor_markers` returns `BLOCKED` with `rights_basis: "contributed_image_exception"`. The corresponding test must assert `BLOCKED`. No Sprint 2 code may be written while `contributor_markers` routes to `REVIEW_REQUIRED`.

**Verification:** `test_noaa_rights_reviews_contributor_and_partner_markers` for the `flickr_photo_personal_noaa_review.json` case must assert `rights["decision"] == "BLOCKED"`.

### Gate 2 — Other US Federal Agency Allow Patterns

`FEDERAL_AGENCY_ALLOW_PATTERNS` (or equivalent) must be added to `rights.py` and integrated into `classify_rights`. At minimum: NASA, USGS, USFWS, NPS, EPA. NIST, NSF, USACE are lower priority but should be included.

**Verification:** A new unit test `test_noaa_rights_allows_other_federal_agency_credits` must pass, covering at minimum "NASA", "USGS", "NASA/GSFC", "USGS/WRD".

### Gate 3 — `url_m` Removed from URL Hierarchy

`choose_image_url` in `client.py` must iterate only `("url_o", "url_l", "url_c", "url_z")`. `url_m` must be removed.

**Verification:** A unit test `test_noaa_client_rejects_url_m_only_record` must confirm that a record with only `url_m` returns `None` from `choose_image_url` and is excluded from `normalize_record` output.

### Gate 4 — NOAA Space-Prefix Coverage

`_is_noaa_federal_credit` must handle space-separated NOAA names ("NOAA Coral Reef Watch", "NOAA Fisheries Service") by adding `credit.lower().startswith("noaa ")` to the prefix-match logic.

**Verification:** Unit tests covering "NOAA Coral Reef Watch" → ALLOWED and "NOAA Fisheries Service" → ALLOWED via credit gate.

### Gate 5 — Confirmed Flickr NSIDs

The NSIDs for @usoceangov and @noaafisheries must be confirmed and committed to configuration. `DEFAULT_FLICKR_USER_ID` or the config layer must use NSIDs, not usernames, as the stable production identifier.

**Verification:** Config documentation showing the confirmed NSIDs; the adapter uses them in the Sprint 2 harvest configuration.

### Gate 6 — Photo Library Evaluation Finding

The Sprint 1 Photo Library evaluation deliverable (SA-NOAA-002 Part II.1) must be completed and documented. The finding must explicitly record one of three outcomes:

- **Gate 2A:** Photo Library API/bulk path confirmed viable → SA-NOAA-002 v1.1 drafted; Path B becomes production standard for Sprint 2; Flickr path demoted to fallback.
- **Gate 2B:** Photo Library confirmed non-viable → Platform Dependency Governance Review opened (per SA-NOAA-002 Section IV.4). Sprint 2 Flickr harvest authorized only after that review produces a decision document.
- **Partial:** Scraping-only path found → DD-NOAA-002 scope required; Sprint 2 Flickr harvest conditional.

**No Sprint 2 Flickr harvest beyond the pilot scope may proceed until Gate 6 outcome is documented and Gate 2A or 2B is formally recorded.**

---

## X. Sprint 2 Scope Authorization

Upon meeting all six gates in Section IX, Sprint 2 is authorized to proceed with:

1. **M36 write integration** — source_record and media_rights writes for records passing the rights gate. Store writes require FM-4 compliance: `rights_status: "pending_verification"` only.
2. **SA-9 extension** — add `"noaa"` slug to `build_rights_evidence` source slug remap (13th slug). This is the Sprint 3 prerequisite per DD-NOAA-001 Article 13.
3. **rights_evidence completion** — add `access_path`, `primary_gate_field`, `endorsement_restrictions` fields to the evidence envelope per SA-NOAA-001 Part VII.
4. **License pre-filter** — add `license=7,8,9,10` parameter to Flickr API requests per SA-NOAA-002 OB-2.
5. **Path B activation** (contingent on Gate 6 outcome) — if Gate 2A, implement Photo Library adapter per SA-NOAA-002 Part II specification.

Sprint 2 scope is NOT authorized for:
- Full catalog harvest (50-asset pilot cap remains until Gate 2A or Gate 2B formally lifts it per SA-NOAA-002 Section IV.4)
- Any use of `url_m` for image delivery
- Any write path that does not respect M36 write order

---

## XI. SA Amendment Schedule

| Amendment | Trigger | Priority |
|---|---|---|
| SA-NOAA-001 v1.1 | Align block reason code vocabulary with `rights_basis` strings; document REVIEW_REQUIRED for foreign agencies; close OQ-2 | Sprint 2 |
| SA-NOAA-002 v1.1 | Update method name to `getPublicPhotos`; record confirmed NSIDs; update Path B per Gate 6 finding | Sprint 2 |

---

## XII. Ratification Table

| Role | SA-NOAA-001 | SA-NOAA-002 | Sprint 2 Auth | Date |
|---|---|---|---|---|
| Governance Review | ☐ PENDING | ☐ PENDING | ☐ PENDING (after Gates 1–6) | — |
| Principal Architect | ☐ PENDING | ☐ PENDING | ☐ PENDING | — |

**Ratification conditions:**
1. SA-NOAA-001 ratification: unconditional — SA is correct as drafted
2. SA-NOAA-002 ratification: unconditional — SA is correct as drafted
3. Sprint 2 authorization: contingent on all six gates in Section IX

---

*NOAA Sprint 2 Governance Review v1 — drafted 2026-06-11*  
*Implementation reviewed: `workers/noaa_adapter/rights.py`, `client.py`, `normalize.py`, `tests/unit/test_noaa_rights.py`, `tests/replay/test_noaa_adapter_sprint1.py`*  
*Authority: DD-NOAA-001 · SA-NOAA-001 · SA-NOAA-002 · NOAA Governance Review v1 · IFC-1*  
*SA-NOAA-001: RATIFIED · SA-NOAA-002: RATIFIED · Sprint 2: CONDITIONAL on Gates 1–6*
