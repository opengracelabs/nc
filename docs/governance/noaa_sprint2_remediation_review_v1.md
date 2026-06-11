# NOAA Sprint 2 Remediation Review v1

| Field | Value |
|---|---|
| Version | 1.0 |
| Status | DRAFT — Pending Ratification |
| Review Authority | NC Governance |
| Sprint | Sprint 2 exit gate / Sprint 3 planning authorization |
| Governing Documents | DD-NOAA-001 · SA-NOAA-001 · SA-NOAA-002 · NOAA Governance Review v1 · NOAA Sprint 2 Governance Review v1 |
| Tests Reviewed | `tests/unit/test_noaa_rights.py` · `tests/unit/test_noaa_sprint2_rights.py` · `tests/replay/test_noaa_adapter_sprint2.py` |
| Date | 2026-06-11 |

---

## DECISION

**APPROVE WITH CONDITIONS**

Two of four required Sprint 2 corrections are complete. Two remain open. Neither open item is an IFC-1 violation: no non-PD record reaches `rights_status: "allowed"`, and no store.py exists. Sprint 3 planning is authorized on that basis.

Sprint 3 implementation is not authorized until the three carry-over conditions in Section IX are resolved. Specifically: the M36 write path may not open until Corrections 1 and 4 are addressed.

---

## I. Correction 2 — Federal Agency Expansion

**COMPLETE.**

`FEDERAL_CREDIT_PATTERNS` now covers all eight required agencies:

| Agency | Pattern(s) Present |
|---|---|
| NASA | `"NASA"` ✓ |
| USGS | `"USGS"`, `"U.S. Geological Survey"`, `"United States Geological Survey"` ✓ |
| USFWS | `"USFWS"`, `"U.S. Fish and Wildlife Service"` ✓ |
| NPS | `"NPS"`, `"National Park Service"` ✓ |
| EPA | `"EPA"`, `"Environmental Protection Agency"` ✓ |
| NSF | `"NSF"`, `"National Science Foundation"` ✓ |
| USACE | `"USACE"`, `"U.S. Army Corps of Engineers"` ✓ |
| NIST | `"NIST"`, `"National Institute of Standards and Technology"` ✓ |

All eight acronyms are in the allow-set as exact-match entries. Slash-prefix matching generalizes from these (e.g., `"NASA/GSFC"` matches via `startswith("nasa/")`). The backward-compat alias `NOAA_FEDERAL_CREDIT_PATTERNS = FEDERAL_CREDIT_PATTERNS` is present.

`test_noaa_rights_sprint2_allows_federal_agency_credits` confirms ALLOWED for all eight acronyms at the unit level. Test coverage is adequate.

**Gate 2 is CLEARED.**

---

## II. Correction 3 — NOAA Prefix Strategy

**PARTIAL — Carry-over condition for Sprint 3.**

The `FEDERAL_CREDIT_PATTERNS` list includes three NOAA space-separated division names from Sprint 1: `"NOAA Fisheries"`, `"NOAA Ocean Service"`, `"NOAA Research"`. No new space-separated NOAA names were added in the Sprint 2 remediation and no generic `startswith("noaa ")` logic was added to `_is_noaa_federal_credit`.

**Coverage assessment:**

| Credit string | Status |
|---|---|
| `"NOAA"` | ALLOWED (exact match) ✓ |
| `"NOAA/OMAO"` | ALLOWED (slash-prefix on "NOAA") ✓ |
| `"NOAA Fisheries"` | ALLOWED (exact match) ✓ |
| `"NOAA Ocean Service"` | ALLOWED (exact match) ✓ |
| `"NOAA Research"` | ALLOWED (exact match) ✓ |
| `"NOAA Coral Reef Watch"` | NOT COVERED — falls through to BLOCKED |
| `"NOAA Fisheries Service"` | NOT COVERED — "noaa fisheries service" not in exact set; does not start with "noaa fisheries/" |
| `"NOAA Great Lakes Environmental Research Laboratory"` | NOT COVERED |
| `"NOAA Pacific Marine Environmental Laboratory"` | NOT COVERED |

**Impact:** For Flickr Path A, this gap is low risk. A NOAA Coral Reef Watch image with `license_id == "8"` is ALLOWED regardless of credit (license gate precedes credit gate). The gap only activates for Flickr records with license 7/9/10 where the credit confirmation is required, and for all Photo Library (Path B) records. For Path B, any NOAA division name not enumerated or slash-prefixed would be BLOCKED (missing_rights_evidence).

This gap must be resolved before Path B activation. For Sprint 3 planning, it is a non-blocking carry-over.

**Required fix:** Add `lowered.startswith("noaa ")` as a prefix-match condition in `_is_noaa_federal_credit`, with the existing personal-name guard applied after:

```python
if lowered.startswith("noaa "):
    if _detect_personal_name_noaa(cleaned):
        return False
    return True
```

**Gate 3 is PARTIAL — Carry-over condition SPC-3-1 (see Section IX).**

---

## III. Correction 4 — url_z Minimum Delivery Tier

**NOT DONE — Carry-over condition for Sprint 3.**

`client.py` line 167 is unchanged from Sprint 1:

```python
for key in ("url_o", "url_l", "url_c", "url_z", "url_m"):
```

`url_m` (~500px) remains in the URL hierarchy. SA-NOAA-002 Section I.6 specifies `url_z` (640px) as the minimum; any record below this must be excluded with `reason: "insufficient_resolution"`.

**Impact:** A record with only `url_m` available returns a 500px URL as `image_url`. In Sprint 2 (read-only, no store writes, `noaa_dry_run: True`), this is contained. Once the M36 write path opens in Sprint 3, a sub-640px `representative_media_url` could be written to storage. This must be corrected before any store write is enabled.

**Required fix:** Remove `"url_m"` from the iteration, with `None` returned for records that have no URL at or above `url_z`. Callers must treat `None` as `missing_image_evidence` and exclude the record from normalization output.

**Gate 4 is NOT CLEARED — Carry-over condition SPC-3-2 (see Section IX).**

---

## IV. Correction 1 — Personal Name/NOAA Credits: BLOCKED vs REVIEW_REQUIRED

**NOT DONE — Carry-over condition for Sprint 3, with doctrine clarification required.**

`rights.py` lines 223–232 are unchanged:

```python
if contributor_markers:
    return _result(
        decision=RightsDecision.REVIEW_REQUIRED,
        allowed=False,
        rights_statement_uri=NO_COPYRIGHT_US_URI,
        rights_status="pending_verification",
        rights_basis="personal_name_noaa_credit",
        ...
    )
```

Both `test_noaa_rights.py` (Sprint 1) and `test_noaa_adapter_sprint2.py` (Sprint 2) explicitly assert `REVIEW_REQUIRED` for the personal name fixture. The Sprint 2 implementation treats this as the accepted behavior.

**IFC-1 status:** COMPLIANT. `rights_status: "pending_verification"` on the REVIEW_REQUIRED path means no production write proceeds without human review. IFC-1 requires that no non-PD record is written; REVIEW_REQUIRED satisfies this constraint. This is not an IFC-1 violation.

**SA-NOAA-001 status:** NON-COMPLIANT. NOAA Governance Review v1 Section V ruled "BLOCKED — not REVIEW_REQUIRED" for personal name/NOAA credits, with explicit rationale: federal employment status cannot be verified from public metadata at scale, making a human review queue operationally untenable. The implementation contradicts this ruling.

**Governance finding for Sprint 3:** The Sprint 2 implementation has taken a documented position that REVIEW_REQUIRED is more appropriate than BLOCKED for this case — specifically because REVIEW_REQUIRED is safe in the direction of caution (creates a human review queue that will reject; does not admit non-PD records). This position has been codified in two test files. It conflicts with SA-NOAA-001.

**Resolution required before Sprint 3 M36 write path opens:** SA-NOAA-001 v1.1 must reconcile this explicitly. The options are:

- **Option A — Align implementation to SA:** Change `contributor_markers` branch to `BLOCKED (contributed_image_exception)`. Remove personal-name records from human review queue entirely. Update both affected tests.
- **Option B — Align SA to implementation:** SA-NOAA-001 v1.1 formally adopts REVIEW_REQUIRED for personal name/NOAA credits, with explicit rationale that the human review queue is the appropriate safety mechanism, and that BLOCKED would discard potentially valid federal employee photos. The original "operationally untenable" concern becomes a queue-volume acceptance.

**Governance recommendation: Option A.** The original rationale holds. NC cannot determine federal employment status from a "Photo by [Name]/NOAA" credit line — this pattern covers contractors, visiting scientists, and non-federal staff as commonly as employees. The conservative rule is to BLOCK and accept false negatives (legitimate employee photos discarded) rather than create a review queue that is operationally equivalent to BLOCK anyway. This keeps the human review queue reserved for cases where there is genuine ambiguity (partner institutions, joint-mission work), not for cases where the contributed-image determination is reliable.

**Gate 1 is NOT CLEARED — Carry-over condition SPC-3-3 (see Section IX).**

---

## V. Rights Class 9 Verification

**CONFIRMED — Rights Class 9 is valid and correctly implemented.**

`normalize.py` line 135: `"noaa_rights_class": "rights_class_9"` — present and correct.

`classify_rights` never writes `rights_status: "verified_pd"` or `rights_status: "classified_pd"` — FM-4 satisfied throughout.

`config.py` centralizes `RIGHTS_POLICY_ID = "noaa_rights_matrix_v1"` — all modules import from config; no hardcoded strings diverge.

`technical.py` is discovery-only; `store.py` does not exist; `noaa_dry_run: bool = True` is present in `config.py`. The Sprint 2 boundary is intact.

Rights Class 9 anchor in `rights.py` via `NO_COPYRIGHT_US_URI = NOC_US_URI` (maps to `NoC-US/1.0/` Rights Statements URI) — the correct § 105 basis.

---

## VI. Personal-Name Precedence Verification

**PRECEDENCE CORRECTLY ORDERED — outcome non-compliant with SA.**

The `classify_rights` precedence chain is:

```
1. missing/empty         → BLOCKED
2. blocked_markers       → BLOCKED       (Getty, Reuters, AP, Maxar, DigitalGlobe, Planet, GeoEye)
3. license_id == "0"     → BLOCKED
4. partner_markers       → REVIEW_REQUIRED
5. contributor_markers   → REVIEW_REQUIRED   ← personal name check, step 5 of 10
6. license_id == "8"     → ALLOWED
7. federal_credit        → ALLOWED
8. license {7,9,10}      → REVIEW_REQUIRED
9. license {1–6}         → BLOCKED
10. fallback              → BLOCKED
```

Personal names are checked at step 5, before the license-8 ALLOWED gate at step 6. A `"Photo by John Smith/NOAA"` record with `license_id == "8"` correctly reaches REVIEW_REQUIRED (step 5) rather than ALLOWED (step 6). The precedence order enforces that personal-name detection intercepts before any allow path. This ordering is correct and would not change under either Option A or Option B above — only the outcome code (`BLOCKED` vs `REVIEW_REQUIRED`) would change.

---

## VII. Commercial Operator Blocking

**FULLY COMPLIANT — tested with new Sprint 2 fixtures.**

`BLOCKED_MARKERS = ("Getty", "Reuters", "AP", "Maxar", "DigitalGlobe", "Planet", "GeoEye")`

Sprint 1 fixtures (Getty, Reuters, AP, satellite combined) and Sprint 2 fixtures (Maxar standalone, Planet standalone) all confirm BLOCKED. The word-boundary regex in `_detect_markers` prevents "AP" from matching substrings. SA-NOAA-001 OQ-2 is closed.

`test_noaa_sprint2_rights.py` adds individual Maxar and Planet fixture coverage. Commercial operator gate is fully tested.

---

## VIII. Foreign Agency REVIEW_REQUIRED Verification

**IMPROVED AND COMPLIANT.**

`REVIEW_PARTNER_MARKERS` now includes:

```python
"NASA/ESA",                         # joint-mission sentinel (new, Step 4 priority)
"ESA",
"European Space Agency",            # new
"JAXA",
"Japan Aerospace Exploration Agency",  # new
"CSA",
"Canadian Space Agency",            # new
"foreign partner",                  # new
"foreign agency",                   # new
"International",                    # new
```

The `flickr_photo_nasa_esa_review.json` fixture (credit: `"NASA/ESA"`, license: `"8"`) produces REVIEW_REQUIRED correctly: the partner_markers check at step 4 fires before the license-8 ALLOWED gate at step 6. `"NASA/ESA"` in `REVIEW_PARTNER_MARKERS` resolves the joint-mission ambiguity that was identified in the Sprint 2 governance review.

Solo NASA credit (`"NASA"` alone) does NOT appear in REVIEW_PARTNER_MARKERS and correctly routes to ALLOWED via `_is_noaa_federal_credit("NASA")` at step 7. This distinction is correct and properly tested.

`test_noaa_sprint2_rights.py` confirms `"NASA/ESA"` → REVIEW_REQUIRED with `"NASA/ESA"` in `partner_markers`.

---

## IX. Sprint 3 Carry-Over Conditions

Three conditions carry forward from the Sprint 2 gate. Sprint 3 **planning** is authorized. Sprint 3 **implementation** (M36 write path, catalog harvest, Path B activation) requires the conditions to be resolved in the order specified.

### SPC-3-1 — NOAA Space-Prefix (Non-blocking for Sprint 3 planning)

Add `lowered.startswith("noaa ")` prefix-match logic to `_is_noaa_federal_credit`, with the personal-name guard applied after. This must be in place before:
- Path B (Photo Library) activation
- Any Sprint 3 credit-gated catalog harvest

Verification: unit test `test_noaa_rights_sprint3_covers_noaa_space_prefix_credits` covering "NOAA Coral Reef Watch", "NOAA Fisheries Service", "NOAA Great Lakes Environmental Research Laboratory".

Priority: **Medium — Path B blocker, Sprint 3 harvest risk if credit-gating is primary path.**

### SPC-3-2 — url_m Removal (Blocking for M36 write path)

Remove `"url_m"` from `choose_image_url` hierarchy. Must be resolved before any Sprint 3 M36 write path opens. A record with only `url_m` must return `None` and be excluded from `normalize_record` output.

Verification: unit test `test_noaa_client_rejects_url_m_only_record` confirming `choose_image_url` returns `None` when only `url_m` is available.

Priority: **High — Blocks Sprint 3 M36 write path.**

### SPC-3-3 — Personal Name: BLOCKED or SA-NOAA-001 v1.1 (Blocking for M36 write path)

SA-NOAA-001 v1.1 must formally resolve the Option A / Option B ruling. Under **Option A** (recommendation): change the `contributor_markers` branch in `rights.py` to `BLOCKED (contributed_image_exception)`. Under **Option B**: SA-NOAA-001 v1.1 explicitly adopts REVIEW_REQUIRED with documented rationale and queue-volume acceptance. Either way, the governing document and implementation must be aligned before the M36 write path opens.

This condition is not about IFC-1 safety — it is about governance coherence. The SA and the implementation cannot permanently diverge.

Priority: **Medium — Does not block Sprint 3 planning; blocks M36 write path until resolved.**

---

## X. Sprint 3 Scope Authorization

**Sprint 3 planning: AUTHORIZED.**

**Sprint 3 implementation conditions:**

| Gate | Description | Status |
|---|---|---|
| SPC-3-1 | NOAA space-prefix | Must resolve before Path B or credit-gated harvest |
| SPC-3-2 | url_m removal | Must resolve before any M36 write path |
| SPC-3-3 | Personal name doctrine alignment | Must resolve before M36 write path |
| Gate 5 | Confirmed NSIDs for @usoceangov and @noaafisheries | Carries forward from Sprint 2 |
| Gate 6 | Photo Library evaluation finding (Gate 2A / 2B) | Carries forward from Sprint 2 |

Gates 5 and 6 from the Sprint 2 Governance Review are also open. Neither blocks Sprint 3 planning but Gate 6 determines whether Sprint 3 includes a Path B implementation scope.

---

## XI. Additional Observations

**OB-1 — config.py is architecturally sound.** Centralizing `RIGHTS_POLICY_ID`, `SOURCE_SLUG`, `SCHEMA_STANDARD` in config.py with `pydantic_settings.BaseSettings` is the correct pattern. `noaa_dry_run: bool = True` provides a governance-visible dry-run gate. No issues.

**OB-2 — technical.py is discovery-only and correct.** FM-4 is respected throughout. `"media_type_id" not in content` asserted in Sprint 2 replay test, confirming M36 write fields are absent. `store.py` still absent. Discovery boundary intact.

**OB-3 — normalize_record correctly gates on `rights["allowed"]`.** REVIEW_REQUIRED records (`allowed=False`) return `[]` from `normalize_record`. Blocked records return `[]`. Only ALLOWED records proceed to normalization output. This is correct regardless of whether Correction 1 routes to BLOCKED or REVIEW_REQUIRED: either way, personal name records produce no normalized output.

**OB-4 — SA-NOAA-001/002 v1.1 drafts required.** Sprint 3 planning authorization presupposes that SA-NOAA-001 v1.1 and SA-NOAA-002 v1.1 are drafted in Sprint 3, incorporating the resolutions for SPC-3-1, SPC-3-2, SPC-3-3, Gate 5, Gate 6. These are Sprint 3 entry deliverables alongside code corrections.

---

## XII. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Governance Review | ☐ PENDING | — |
| Principal Architect | ☐ PENDING | — |

---

*NOAA Sprint 2 Remediation Review v1 — drafted 2026-06-11*  
*Implementation reviewed: `workers/noaa_adapter/rights.py`, `client.py`, `normalize.py`, `technical.py`, `config.py`*  
*Test suites reviewed: `test_noaa_rights.py`, `test_noaa_sprint2_rights.py`, `test_noaa_adapter_sprint2.py`*  
*Authority: DD-NOAA-001 · SA-NOAA-001 · SA-NOAA-002 · NOAA Governance Review v1 · NOAA Sprint 2 Governance Review v1*  
*Sprint 3 planning: AUTHORIZED · Sprint 3 M36 write path: CONDITIONAL on SPC-3-2, SPC-3-3 · Path B: CONDITIONAL on SPC-3-1, Gate 6*
