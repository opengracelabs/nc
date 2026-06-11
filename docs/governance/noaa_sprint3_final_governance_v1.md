# NOAA Sprint 3 Final Governance Confirmation v1

| Field | Value |
|---|---|
| Version | 1.0 |
| Status | RATIFIED |
| Review Authority | NC Governance |
| Supersedes | NOAA Sprint 3 Governance Review v1 (Section IV — REVIEW_REQUIRED path) |
| Governing Documents | DD-NOAA-001 · SA-NOAA-001 · SA-NOAA-002 · IFC-1 |
| Date | 2026-06-11 |

---

## DECISION

**APPROVE**

REVIEW_REQUIRED records are excluded from the Sprint 3 pilot.

Option B (pilot exclusion) is both the preferred and constitutionally correct choice for Sprint 3. The workflow_item path (Option A) is architecturally sound but premature: it belongs in Sprint 4, not a 50-asset pilot. NOAA follows the NASA model. This ruling amends Section II and Section IV of NOAA Sprint 3 Governance Review v1. All other provisions of that document stand.

---

## I. The Architectural Precedent

NASA is the governing precedent. It is not merely analogous — it is the same institution class:

- Rights Class 9 (both institutions)
- 17 U.S.C. § 105 (same statutory basis)
- Federal government works with contributed-image exceptions
- Mixed-rights collection requiring per-record classification
- Sprint 3 M36 write path implementation

NASA's `store.py` contains this constant:

```python
REVIEW_REQUIRED_PILOT_EXCLUSION = "review_required_pilot_exclusion"
```

And this gate:

```python
if rights.get("decision") == "REVIEW_REQUIRED":
    return _rejected_result(record)  # reason = REVIEW_REQUIRED_PILOT_EXCLUSION
```

NASA explicitly named the constant to signal that pilot exclusion is a temporary policy, not a permanent architectural decision. NOAA adopts the same constant and the same gate.

---

## II. Why Option B is Constitutionally Correct for Sprint 3

### II.1 The pilot's purpose

A 50-asset pilot exists to validate one thing: that confirmed federal works (ALLOWED) traverse the M36 write path correctly — source_item, source_record, media_file, media_rights, preservation_event, technical_metadata, provenance pin — with `rights_status: 'pending_verification'` and the full NOAA evidence extension.

REVIEW_REQUIRED records do not contribute to this validation. They test a different code path (the workflow_item creation path), a different URI mapping (NKC/1.0/), and a different operational process (a human review queue). Including them in a 50-asset pilot adds surface area without adding signal.

### II.2 The operational reality

A workflow_item written during the pilot creates a `workflow_items` row with `status: 'pending'` and `capability: 'rights_review'`. That row will remain pending indefinitely unless a reviewer is assigned to process it. During a 50-asset pilot, there is no operational review process. Pending workflow_items accumulate as false-positive artifacts that must later be cleaned up. This is not a test of the workflow_item path; it is a test of whether those artifacts can be ignored.

Option A during the pilot would produce correct code but incorrect operations. Option B produces correct code and correct operations.

### II.3 IFC-1 is satisfied by either option

Both options satisfy IFC-1. REVIEW_REQUIRED records with `rights_status: 'pending_verification'` are not written as PD records under Option A. Under Option B they are not written at all. IFC-1 is not the deciding factor.

The deciding factor is pilot integrity. A pilot should contain only records that have been through the complete governed path. REVIEW_REQUIRED records have not been confirmed as § 105 works. They do not belong in the pilot store alongside confirmed federal works.

### II.4 The Mia model is inapplicable

Mia has no REVIEW_REQUIRED category. Mia's rights gate is binary: `mia_rights_type in {"Public Domain", "No Copyright–United States"}` — pass, or reject. Records that do not meet the binary gate are rejected immediately. There is no ambiguous middle class in Mia's rights matrix.

NOAA has three distinct REVIEW_REQUIRED sub-types (foreign agency, partner institution, PD-no-credit) that are genuinely ambiguous about § 105 status. Mia's binary model cannot be applied to this structure. The Mia model is not a reference for NOAA.

---

## III. Revised Write-Path Decision Matrix

This table replaces Table II in NOAA Sprint 3 Governance Review v1.

| NOAA Decision | Rights Basis | Sprint 3 Writes | Sprint 3 Reason | Sprint 4 Target |
|---|---|---|---|---|
| ALLOWED | `flickr_us_government_work` | 7 | — | 7 writes (unchanged) |
| ALLOWED | `noaa_federal_credit` | 7 | — | 7 writes (unchanged) |
| REVIEW_REQUIRED | `partner_or_contributor_marker` | **0** | `review_required_pilot_exclusion` | 8 writes (workflow_item) |
| REVIEW_REQUIRED | `public_domain_license_without_federal_credit` | **0** | `review_required_pilot_exclusion` | 8 writes (workflow_item) |
| REVIEW_REQUIRED | `personal_name_noaa_credit` | **0** | `contributed_image_exception` | 0 writes (permanent hard block) |
| BLOCKED | `blocked_partner_marker` | 0 | `blocked_partner_marker` | 0 writes (unchanged) |
| BLOCKED | `flickr_all_rights_reserved` | 0 | `flickr_all_rights_reserved` | 0 writes (unchanged) |
| BLOCKED | `unsupported_flickr_license` | 0 | `unsupported_flickr_license` | 0 writes (unchanged) |
| BLOCKED | `missing_rights_evidence` | 0 | `missing_rights_evidence` | 0 writes (unchanged) |

The personal name case (`personal_name_noaa_credit`) remains a permanent hard block in all sprints. It is not subject to Sprint 4 workflow_item activation. The `review_required_pilot_exclusion` reason code applies only to the genuinely ambiguous REVIEW_REQUIRED sub-types.

---

## IV. NOAA `store.py` Pre-Gate

NOAA's `write_record` implements the following pre-gate, in precedence order:

```
1. classify_rights(record) → decision
2. REVIEW_REQUIRED, basis == "personal_name_noaa_credit"
   → rejected: "contributed_image_exception", writes: 0  (permanent)
3. REVIEW_REQUIRED, any other basis
   → rejected: "review_required_pilot_exclusion", writes: 0  (Sprint 3 pilot)
4. BLOCKED, any basis
   → rejected: <rights_basis>, writes: 0
5. ALLOWED, normalized candidates empty
   → rejected: "missing_media_candidate", writes: 0
6. ALLOWED, validation_status != "valid"
   → rejected: "invalid_technical_metadata", writes: 0
7. ALLOWED, valid
   → write_normalized_record(runtime=_runtime(), ...), writes: 7
```

Steps 2 and 3 are explicit. Step 3 is removed in Sprint 4 when the workflow_item path is activated. Step 2 is never removed.

The `REVIEW_REQUIRED_PILOT_EXCLUSION = "review_required_pilot_exclusion"` constant must appear in NOAA `store.py` at module level, matching the NASA pattern, to signal the post-pilot activation intent.

---

## V. Sprint 4 Workflow Item Path (Design Target, Not Sprint 3 Scope)

The Option A architecture from NOAA Sprint 3 Governance Review v1 (Section IV) is preserved as the Sprint 4 design target. When Sprint 4 activates the workflow_item path:

- Step 3 in Section IV above is removed
- REVIEW_REQUIRED records with basis `partner_or_contributor_marker` → `rights_uri = NKC/1.0/` → shared REVIEW_REQUIRED → 8 writes (workflow_item)
- REVIEW_REQUIRED records with basis `public_domain_license_without_federal_credit` → same path
- Workflow_item `context.item_payload` carries the noaa_partner_markers, noaa_rights_basis, noaa_original_rights_uri fields per NOAA Sprint 3 Governance Review v1 Section IV
- Sprint 4 requires: review queue operational process, reviewer assignment protocol, and promotion/rejection workflow documented before activation

Sprint 4 workflow_item activation is not a code-only change. It requires a governance document (DD-NOAA-Sprint4 or equivalent) that confirms the review queue is staffed and the promotion criteria are defined.

---

## VI. Revised Replay Tests

Tests T1, T3, T5, T6, T7 from NOAA Sprint 3 Governance Review v1 are unchanged.

**T2 — REVISED: REVIEW_REQUIRED records produce 0 writes with pilot exclusion reason**

Fixture: `flickr_photo_nasa_esa_review.json` (partner_or_contributor_marker)

Assertions:
- `result["status"] == "rejected"`
- `result["writes"] == 0`
- `result["reason"] == "review_required_pilot_exclusion"`

**T4 — CONFIRMED: Personal name produces 0 writes permanently**

Fixture: `flickr_photo_personal_noaa_review.json`

Assertions:
- `result["status"] == "rejected"`
- `result["writes"] == 0`
- `result["reason"] == "contributed_image_exception"`

T4 reason is `contributed_image_exception`, not `review_required_pilot_exclusion`. The distinction is permanent vs. temporary exclusion. Tests must assert the specific reason string.

**T2 Sprint-4 variant (not active in Sprint 3, must be in a skipped or annotated test block):**

Fixture: `flickr_photo_nasa_esa_review.json`

Post-Sprint-4 assertions:
- `result["status"] == "written"`
- `result["writes"] == 8`
- `result["workflow_item_id"] is not None`

This test must exist as a documented Sprint 4 target so the architecture is not forgotten when Sprint 4 begins.

---

## VII. SA-NOAA-001 v1.1 Amendment Required

SA-NOAA-001 v1.1 must be amended to reflect this ruling:

1. **Part IX (store-layer behavior):** Add a new section documenting pilot exclusion as Sprint 3 behavior. Specify `REVIEW_REQUIRED_PILOT_EXCLUSION` as the reason code. Note that this is a Sprint 3 pilot decision, not a permanent rights classification outcome.

2. **Part IX (Sprint 4 activation criteria):** Document the three conditions required before workflow_item path activates: operational review queue, reviewer assignment protocol, promotion criteria.

3. **Part V (personal name):** Confirm that `contributed_image_exception` is permanent in all sprints (no Sprint 4 reversal).

---

## VIII. Final Sprint 3 Write-Path Summary

Sprint 3 writes exactly one class of records to M36: confirmed NOAA federal works that passed the rights gate with `decision == "ALLOWED"`.

Every other record — REVIEW_REQUIRED (all sub-types), BLOCKED (all sub-types), missing required fields — produces 0 writes, 0 workflow_items, reason code only.

The pilot store is clean: every record in it is a confirmed § 105 federal work with `rights_status: 'pending_verification'` awaiting human promotion. No ambiguous records. No pending review queue. Clear audit trail.

---

## IX. Ratification

This document supersedes NOAA Sprint 3 Governance Review v1 Section IV and Table II. All other provisions of NOAA Sprint 3 Governance Review v1 remain in force.

| Role | Ratified | Date |
|---|---|---|
| Governance Review | ☑ RATIFIED | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*NOAA Sprint 3 Final Governance Confirmation v1 — drafted 2026-06-11*  
*Precedent: `workers/nasa_adapter/store.py` (REVIEW_REQUIRED_PILOT_EXCLUSION pattern)*  
*Authority: DD-NOAA-001 · SA-NOAA-001 · SA-NOAA-002 · IFC-1*  
*Decision: Option B (pilot exclusion) · Model: NASA · Sprint 4 target: Option A (workflow_item)*
