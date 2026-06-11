# NC-COMMERCE-002: First Revenue Authorization

| Field | Value |
|---|---|
| Document | NC-COMMERCE-002 |
| Version | 1.0 |
| Status | **DRAFT** — Pending Principal Architect Ratification |
| Date | 2026-06-11 |
| **Authorization** | **REVENUE AUTHORIZED — PHASE 1 IMMEDIATE · PHASES 2–4 CONDITIONAL** |
| Documents Reviewed | NC-COMMERCE-001 (First 10 Products) · NC-PRODUCT-001 · NC-PILOT-001-LA |
| First 3 products | NC-PROD-001 · NC-PROD-008 · NC-PROD-005 |
| Gate E required | Yes — per activation event |

---

## I. Review Findings

### I.1 NC-COMMERCE-001 (First 10 Products)

Three revenue-relevant findings:

**Finding R-001-1: Earthrise has zero external blocking conditions.**
NC-PROD-001 and NC-PROD-008 carry a single attribution obligation (NASA nonendorsement), no GeoNames ID dependency, no OSM tile dependency, and no SA ratification prerequisite. The only gate remaining is the internal curator + PA sign-off. These are the only two products in the catalog that can generate revenue before any Standards Amendment is ratified.

**Finding R-001-2: DD-NASA-001 is not formally filed.**
The NASA Decision Document does not exist at `docs/decisions/DD-NASA-001_*.md`. Five of the first 10 products (NC-PROD-001, 002, 007, 008, 010) are NASA-sourced. Their rights basis (17 U.S.C. § 105) is statutory and does not depend on a filed DD. Their attribution requirements are fully governed through NC-PILOT-001-LA and NC-PRODUCT-001. Phase 1 revenue (Earthrise) is not blocked. However, DD-NASA-001 must be formally filed before Phase 2 to close the governance gap for new NASA product type additions.

**Finding R-001-3: BHL scan quality is unconfirmed per record.**
NC-PROD-005 (Darwin's Finches), NC-PROD-006 (Haeckel *Hexacoralla*), NC-PROD-009 (Galápagos Education Pack), and NC-PROD-010 (calendar BHL months) depend on BHL scan resolution meeting the NC-PRODUCT-001 Article 13 thresholds. Gould's *Zoology of the Voyage of H.M.S. Beagle* (1841) and Haeckel's *Kunstformen der Natur* (1904) are large-format zoological plates and are expected to exceed thresholds — but per-record pixel dimension confirmation is required at Gate 6 before revenue activation.

### I.2 NC-PRODUCT-001 Review

**Finding R-001-4: The calendar (NC-PROD-010) is the highest-attribution-complexity product in the first 10.**
NC-PROD-010 mixes BHL (pre-1928 PD) and NASA (§ 105) source assets across calendar months. The NASA nonendorsement line is required per-month, not per-product. This means 12 individual month panels must each be audited for correct attribution placement. The calendar is revenue-safe in rights but operationally complex. It should activate last in Phase 2, after simpler products are live.

**Finding R-001-5: The institutional_license curator gate applies to NC-PROD-008 (Earthrise Digital Download).**
NC-PRODUCT-001 Article 11 (Gate 7) requires curator review for all `institutional_license` products. NC-PROD-008 is Phase 1 but carries this gate. It can activate concurrently with NC-PROD-001 in a single curator review session covering both Earthrise products.

### I.3 NC-PILOT-001-LA Review

**Finding R-001-6: Revenue and activation are not the same event.**
NC-PILOT-001-LA authorizes activation per Gate E. Revenue authorization (this document) is a higher-level decision confirming that the product is not only governance-cleared but commercially appropriate for a paying customer transaction. The distinction matters for two products:
- NC-PROD-006 (Haeckel *Hexacoralla* archival print): governance-cleared but BHL scan quality must be confirmed at 6000px before a museum-grade product goes on sale at a premium price point
- NC-PROD-009 (Galápagos Education Pack): governance-cleared but the education pack design must be confirmed complete (3-asset pack, PDF layout) before revenue activation

---

## II. First 3 Products to Activate

### Product 1: NC-PROD-001 — *Earthrise* Museum Giclée Print

**Revenue authorization: IMMEDIATE upon Gate E.**

| Dimension | Assessment |
|---|---|
| Rights confidence | Maximum — 17 U.S.C. § 105, statutory PD, no exceptions possible |
| Attribution complexity | Minimum — NASA nonendorsement only; no GeoNames; no OSM |
| External dependencies | None — no SA ratification required; no Sprint required; no GeoNames ID |
| Quality certainty | Maximum — NASA original exceeds 6000px / 300 DPI unconditionally |
| Gate friction | Curator + PA sign-off (internal); two-human Gate E (internal) |
| Commercial position | MASTERWORK tier — highest CSM score in catalog; leads with the strongest asset |
| Revenue risk | LOWEST in catalog |

**Revenue gate checklist:**
- [ ] `rights_status = 'verified_pd'` AND `human_verified = TRUE` for NC-NASA-002
- [ ] NASA nonendorsement text present: `Image credit: NASA. NASA does not endorse this product.`
- [ ] No NASA insignia, seal, or endorsement language in product copy
- [ ] Consumer use rights notice present on product detail page
- [ ] `activation_target.status = 'activated'` set after Gate E
- [ ] Curator review signed (curator name + date)
- [ ] Principal Architect sign-off (separate person from curator)

---

### Product 2: NC-PROD-008 — *Earthrise* Digital Download

**Revenue authorization: IMMEDIATE upon Gate E. Activate concurrent with NC-PROD-001.**

| Dimension | Assessment |
|---|---|
| Rights confidence | Maximum — same asset (NC-NASA-002), same § 105 basis |
| Attribution complexity | Minimum — NASA nonendorsement in download package metadata |
| External dependencies | None |
| Digital delivery | No physical production risk; immediate fulfillment on purchase |
| Gate friction | Curator review required (institutional_license) — fold into NC-PROD-001 session |
| Revenue risk | LOWEST in catalog; broadest market access point (lower price point) |

**Additional requirement:** Digital download package must include `nc:nasa_attribution` JSON metadata field and consumer use rights notice in the file or accompanying README. Rights statement URI must link to § 105 explanation.

---

### Product 3: NC-PROD-005 — *Darwin's Finches Portfolio* Archival Print

**Revenue authorization: CONDITIONAL — upon SA-GEONAMES-001 + SA-OSM-001 ratification and BHL scan quality confirmation.**

| Dimension | Assessment |
|---|---|
| Rights confidence | Very high — Gould *Zoology of the Voyage of H.M.S. Beagle* (1841); Gould d. 1881; pre-1928 by >80 years |
| Attribution complexity | Low — GeoNames CC BY 4.0 + OSM ODbL; no federal agency; no nonendorsement |
| External dependencies | SA-GEONAMES-001 ratification + SA-OSM-001 ratification |
| Quality certainty | Expected high (large-format zoological plate); BHL per-record pixel dimension confirmation required at Gate 6 |
| Gate friction | Standard routing; no curator required (FLAGSHIP, not MASTERWORK) |
| Commercial position | FLAGSHIP tier; Galápagos is the strongest natural history place in the catalog; Darwin brand recognition is universal |
| Revenue risk | LOW |

NC-PROD-005 is the strongest BHL product in the catalog. It carries no federal nonendorsement requirement, no curator-always gate, and no NARA Sprint verification dependency. It is blocked only by SA ratification and scan confirmation — both internal governance actions. Once SAs are ratified, this product has the fastest path to revenue of any non-Earthrise product.

---

## III. Revenue-Safe Launch Sequence

All 10 products ranked by revenue risk. Tier assignment reflects the number and type of blocking conditions remaining.

### Tier 1 — Revenue-ready now (Gate E only)

| # | Product | Rights | Attribution | External deps | Revenue gate |
|---|---|---|---|---|---|
| 1 | NC-PROD-001 Earthrise Giclée | § 105 | NASA only | None | Curator + PA Gate E |
| 2 | NC-PROD-008 Earthrise Digital | § 105 | NASA only | None | Curator Gate E |

**Rationale:** These are the only two products with zero external platform dependencies. Revenue is gated solely on internal governance actions. Activate these before any SA is ratified, before any place page is live, before any NARA Sprint begins.

---

### Tier 2 — Revenue-ready upon SA ratification (no Sprint required)

| # | Product | Additional condition | Attribution |
|---|---|---|---|
| 3 | NC-PROD-005 Darwin's Finches Print | BHL scan ≥3600px confirmed | GeoNames + OSM |
| 4 | NC-PROD-009 Galápagos Education Pack | 3 BHL scans confirmed; PDF layout complete | GeoNames + OSM |
| 5 | NC-PROD-002 Yellowstone from Orbit Framed | GeoNames ID 5843642 written to `places` | GeoNames + OSM + NASA |
| 6 | NC-PROD-007 GBR Whitsundays Framed | GeoNames ID 2164628 written to `places` | GeoNames + OSM + NASA |

NC-PROD-005 and NC-PROD-009 are Tier 2 frontrunners because they carry no NASA nonendorsement requirement — one fewer obligation than the NASA-sourced wall art products. NC-PROD-002 and NC-PROD-007 are equally ready on SA ratification but add the NASA obligation.

---

### Tier 3 — Revenue-ready upon SA ratification + Sprint 1 completion

| # | Product | Sprint 1 requirement | Additional |
|---|---|---|---|
| 7 | NC-PROD-003 Hayden Map Print | NARA `naId` confirmed; Unrestricted verified | GeoNames + OSM + NARA credit |
| 8 | NC-PROD-004 Grand Canyon Strata Print | NARA `naId` confirmed; Unrestricted verified | GeoNames + OSM + NARA credit |

NARA products are slightly higher-friction than BHL or NASA because they require per-record API verification. The rights are clear (§ 105), but the individual record confirmation adds an operational step that is not required for NASA or BHL assets.

---

### Tier 4 — Revenue-ready upon SA ratification + quality confirmation + curator/PA

| # | Product | Additional condition | Revenue risk note |
|---|---|---|---|
| 9 | NC-PROD-006 Haeckel Hexacoralla Archival | BHL scan ≥6000px confirmed; curator + PA sign-off | MASTERWORK museum_print — higher scrutiny appropriate before revenue |
| 10 | NC-PROD-010 Yellowstone Wildlife Calendar | BHL scan confirmed; 12-month per-panel NASA attribution audit | Mixed-source attribution; seasonal product — time-sensitive |

NC-PROD-010 (calendar) has the most complex per-unit attribution requirement (NASA nonendorsement on each NASA-sourced month) and is time-sensitive (print calendars have a market window). It should activate before the seasonal window closes — but not before all 12 panels are attribution-audited.

---

### Revenue Launch Sequence Summary

```
PHASE 1 (immediate):
  NC-PROD-001 Earthrise Giclée       ──► Gate E ──► REVENUE
  NC-PROD-008 Earthrise Digital      ──► Gate E ──► REVENUE  (concurrent)

PHASE 2 (upon SA ratification + GeoNames IDs written):
  NC-PROD-005 Darwin's Finches       ──► BHL scan confirmed ──► Gate E ──► REVENUE
  NC-PROD-009 Galápagos Edu Pack     ──► BHL confirmed + PDF complete ──► Gate E ──► REVENUE
  NC-PROD-002 YNP Framed Print       ──► Gate E ──► REVENUE
  NC-PROD-007 GBR Satellite Print    ──► Gate E ──► REVENUE

PHASE 3 (upon Phase 2 + NARA Sprint 1):
  NC-PROD-003 Hayden Map Print       ──► naId confirmed ──► Gate E ──► REVENUE
  NC-PROD-004 GC Strata Print        ──► naId confirmed ──► Gate E ──► REVENUE

PHASE 4 (upon Phase 2 + BHL quality + curator/PA):
  NC-PROD-006 Haeckel Archival       ──► scan confirmed ──► curator+PA ──► Gate E ──► REVENUE
  NC-PROD-010 YNP Calendar           ──► 12-panel attribution audit ──► Gate E ──► REVENUE
```

---

## IV. Lowest-Risk Commercial Products

Risk scoring on four dimensions: rights confidence (R), attribution complexity (A), external dependency count (D), quality certainty (Q). Lower score = lower risk.

| Product | R | A | D | Q | Risk score | Verdict |
|---|---|---|---|---|---|---|
| NC-PROD-001 Earthrise Giclée | 1 | 1 | 0 | 1 | **3** | LOWEST — first to revenue |
| NC-PROD-008 Earthrise Digital | 1 | 1 | 0 | 1 | **3** | LOWEST — first to revenue |
| NC-PROD-005 Darwin's Finches | 1 | 2 | 1 | 2 | **6** | LOW — third to revenue |
| NC-PROD-002 YNP Framed | 1 | 3 | 2 | 1 | **7** | LOW |
| NC-PROD-007 GBR Satellite | 1 | 3 | 2 | 1 | **7** | LOW |
| NC-PROD-009 Galápagos Edu Pack | 1 | 2 | 1 | 2 | **6** | LOW (lower revenue per unit) |
| NC-PROD-003 Hayden Map | 2 | 3 | 3 | 1 | **9** | MEDIUM |
| NC-PROD-004 GC Strata | 2 | 3 | 3 | 1 | **9** | MEDIUM |
| NC-PROD-006 Haeckel Archival | 1 | 2 | 1 | 3 | **7** | LOW-MEDIUM (quality dependency) |
| NC-PROD-010 YNP Calendar | 2 | 4 | 2 | 2 | **10** | MEDIUM (attribution complexity) |

**Score key:** R: 1=statutory PD, 2=pre-1928 PD/Rights Class 9; A: 1=1 obligation, 2=2 obligations, 3=3 obligations, 4=4+ obligations; D: count of external blocking conditions; Q: 1=confirmed exceeds threshold, 2=expected but unconfirmed, 3=must confirm per record.

**Structural insight:** The two Earthrise products are in a class of their own (score 3). The nearest competitor is Darwin's Finches (score 6) — but it sits behind an SA ratification gate that Earthrise does not share. Any product that requires SA-GEONAMES-001 ratification is structurally one governance event away from revenue, regardless of how clean its rights are.

---

## V. Products Needing Additional DDs

### V.1 Within the First 10 Products

No product in the first 10 requires a new DD that does not already exist in drafted form. However, three products carry unratified DD dependencies that should be tracked:

| Product | DD dependency | Status | Revenue impact |
|---|---|---|---|
| NC-PROD-001, 002, 007, 008, 010 (NASA) | DD-NASA-001 (not filed) | File not found at expected path | Phase 1 revenue NOT blocked (rights are statutory; existing governance sufficient). New NASA product types blocked until filed (NC-PRODUCT-001 Condition C-3). |
| NC-PROD-003, 004 (NARA) | DD-NARA-001 | Drafted, pending ratification; SA-22 + SA-23 pending | Phase 3 revenue gated on Sprint 1 manual verification. Bulk ingestion blocked until SA-22/SA-23 ratified. |
| NC-PROD-007 (NOAA — actually NASA) | — | NC-PROD-007 is NC-NASA-029 (NASA, not NOAA) | No NOAA dependency on this product |

**DD-NASA-001 filing is a governance debt.** The document does not exist at `docs/decisions/DD-NASA-001_*.md`. All Phase 1 and Phase 2 NASA products operate on institutional knowledge rather than a filed and ratified DD. This is acceptable for the pilot under NC-PRODUCT-001 Condition C-3 (no new NASA product types added until filed), but the gap must be closed. **DD-NASA-001 should be filed as the second priority after DD-SMITHSONIAN-001.**

### V.2 Beyond the First 10 — DD Requirements for Next Revenue Wave

The following products cannot generate revenue regardless of SA ratification status because their source institution DDs are not filed, not drafted, or disqualified:

| Product category | Source | DD required | Priority |
|---|---|---|---|
| Moran Collection (Yellowstone hero tier) | Smithsonian | DD-SMITHSONIAN-001 | **CRITICAL** — highest commercial impact blocked |
| Venice museum art products | Met, AIC, CMA | DD-MET-001 ratification (drafted) | HIGH — unblocks Venice entirely |
| MIA natural history prints | Minneapolis Institute of Art | DD-MIA-001 ratification + SA-MIA-RIGHTS-001 + SA-MIA-DELIVERY-001 | MEDIUM — 64,416 PD images ready when ratified |
| HMS Beagle Galápagos chart | UKHO | DD-TNA-001 or DD-UKHO-001 (not drafted) | MEDIUM — strong Galápagos commercial asset |
| NHM Nodder/Parkinson/Haeckel prints | NHM London | DD-NHM-001 ratification + SA-20 + SA-21 | MEDIUM — fills Priority Illustrator gap |
| ESA/Copernicus imagery | ESA | DD-ESA-001 (not drafted) | LOW for pilot; unblocks Venice satellite layer |
| Canaletto / Venetian art | Museo Correr | DD-MUSEOCORRER-001 (not drafted) | LOW until Venice full-launch DDs clear |

**Revenue gap summary:** With the first 10 products, NC has a complete revenue capability for natural-history illustration, NASA/NOAA/NARA documentary images, and BHL botanical/zoological plates. The major revenue gap is Yellowstone's hero cultural tier (Moran) — the most commercially compelling product in the Playbook — which is entirely blocked on DD-SMITHSONIAN-001.

---

## VI. Revenue Authorization

### VI.1 Authorization

**NC-COMMERCE-002 REVENUE AUTHORIZED.**

Phase 1 revenue (NC-PROD-001 and NC-PROD-008) is authorized with immediate effect upon Gate E completion. Phases 2–4 are conditionally authorized per the sequence in §III.

### VI.2 Decision Articles

**Article 1 — Phase 1 Revenue Authorization.**
NC-PROD-001 (*Earthrise* Museum Giclée Print) and NC-PROD-008 (*Earthrise* Digital Download) are authorized to generate revenue immediately upon Gate E completion. No Standards Amendment ratification, no Sprint completion, and no GeoNames lookup is required. The sole blocking conditions are the internal curator + Principal Architect sign-offs, which are entirely within NC's control.

**Article 2 — Phase 2–4 Revenue Authorization.**
NC-PROD-002 through NC-PROD-010 (excluding NC-PROD-001 and NC-PROD-008) are conditionally authorized. Each product's revenue gate is defined in §III. No product in Phase 2–4 may generate revenue before Phase 1 is live and its own tier conditions are met.

**Article 3 — Darwin's Finches Is the Third Product.**
NC-PROD-005 (*Darwin's Finches Portfolio* Archival Print) is authorized as the third revenue-generating product upon: (a) SA-GEONAMES-001 ratification, (b) SA-OSM-001 ratification, and (c) BHL-GOULD-FINCHES scan confirmed at ≥3600px per Gate 6. No other condition applies. This product does not require curator review, NARA Sprint, or NOAA gate check.

**Article 4 — DD-NASA-001 Filing Required Before Phase 3.**
DD-NASA-001 must be formally filed at `docs/decisions/DD-NASA-001_*.md` and ratified before any new NASA product types beyond the current first 10 are added to the product catalog. Phase 1 and Phase 2 NASA products (NC-PROD-001, 002, 007, 008, 010) are exempt from this gate — they are covered by existing governance. Phase 3 and beyond: no new NASA product types without the filed DD.

**Article 5 — Calendar Activates Last in Phase 2.**
NC-PROD-010 (*Yellowstone Wildlife Calendar*) is the last product to activate in Phase 2. Its 12-panel mixed-source attribution (NASA nonendorsement per NASA-sourced month) must be individually audited before revenue activation. Activating the calendar before simpler Phase 2 products are live introduces unnecessary operational risk. Sequence: NC-PROD-002 → NC-PROD-005 → NC-PROD-010.

**Article 6 — Haeckel Quality Gate is Blocking.**
NC-PROD-006 (*Haeckel Hexacoralla* Archival Print) is a MASTERWORK museum_print priced at a premium. Revenue activation requires BHL scan confirmation at ≥6000px. If BHL's *Kunstformen der Natur* scan does not meet this threshold, NC-PROD-006 must be downgraded to `wall_art` → `print_premium` (not `museum_print` → `archival_print`) or held until a higher-resolution source is identified. Do not activate this product at museum_print tier without confirming the pixel dimension.

**Article 7 — DD-SMITHSONIAN-001 Is the Revenue Gap.**
The Moran Collection is the highest-value deferred product in the catalog. It cannot be added to the NC product pipeline by any internal governance action — it requires DD-SMITHSONIAN-001, which is not yet drafted. The gap between the first 10 products and the Playbook's full commercial vision is almost entirely explained by this single missing DD. DD-SMITHSONIAN-001 should be the next governance sprint priority after the Phase 1 launch is live.

**Article 8 — NOAA Write Cap Tracking Is Operational.**
The NOAA Sprint 3 write cap (max 7 NOAA writes) is an operational tracking requirement, not a DB constraint. Operations must maintain a running log. The NOAA Bathymetric Map (Papahānaumokuākea) is not in the first 10 products — it activates in Phase 5. When it does, it counts as write #1. The first 10 products consume 0 NOAA writes.

**Article 9 — Revenue Does Not Modify Rights.**
The consumer use rights notice required on every product detail page must clearly state that the purchase of an NC product does not affect the public domain status of the underlying image. Revenue generation is permitted because NC's curation, color correction, and product design may carry separate IP — not because NC holds copyright over the PD image. This distinction must be present in product copy and ToS. It is not a new condition but is restated here as it applies to the first moment of actual customer transaction.

**Article 10 — Gate E Applies Per Transaction Event, Not Per Launch.**
Gate E (two-human activation sign-off) is confirmed per activation event — not once for the whole product line. When NC-PROD-001 activates, Gate E is signed for that specific asset at that specific product type. If NC-PROD-001 is later re-activated after suspension, Gate E is required again. The authorization in Article 1 enables the Gate E process to begin; it does not substitute for it.

---

## VII. Ratification Table

| Role | Decision | Date |
|---|---|---|
| Revenue Authorization Review | ☑ AUTHORIZED | 2026-06-11 |
| Principal Architect | ☐ PENDING | — |

---

*NC-COMMERCE-002 — drafted 2026-06-11*
*Reviews: NC-COMMERCE-001 · NC-PRODUCT-001 · NC-PILOT-001-LA*
*Phase 1 revenue: NC-PROD-001 + NC-PROD-008 · Phase 1 unblocked immediately · DD-SMITHSONIAN-001 = revenue gap*
