# NOAA Onboarding Architecture — Governance Review v1

| Field | Value |
|---|---|
| Version | 1.0 |
| Status | DRAFT — Pending Ratification |
| Review Authority | NC Governance |
| Governing Document | DD-NOAA-001 |
| Authorities | IFC-1–IFC-12, 17 U.S.C. § 105, SA-NOAA-001, SA-NOAA-002 |
| Date | 2026-06-11 |
| Reviewer | NC Governance Review |

---

## DECISION

**APPROVE WITH CONDITIONS**

DD-NOAA-001's CONDITIONAL APPROVE is confirmed and advanced to APPROVE WITH CONDITIONS. The rights basis is sound. The contributor detection model is structurally correct but requires three refinements. The commercial imagery block list requires expansion (Getty, Reuters, AP not present in DD-NOAA-001). The Flickr path is acceptable for Sprint 1 pilot only; it is not acceptable as the permanent production path without a Platform Dependency Governance Review. Conditions are binding on SA-NOAA-001 and SA-NOAA-002 ratification.

The five conditions are stated in Section X.

---

## I. Scope of Review

This review assesses DD-NOAA-001 across eight dimensions specified in the governance mandate:

1. Rights Class 9 reuse validity
2. Contributor detection model completeness and precision
3. NOAA-only credit ALLOWED classification
4. Personal-name/NOAA credit classification (BLOCKED vs. REVIEW_REQUIRED)
5. Commercial imagery detection — specified operator list: Getty, Reuters, AP, Maxar, DigitalGlobe, Planet, GeoEye
6. Endorsement restriction compliance
7. Flickr platform dependency risk
8. Flickr path acceptability for Sprint 1

Each dimension receives a CONFIRMED, AMENDED, or REJECTED verdict with rationale. Governance findings are binding on SA-NOAA-001 and SA-NOAA-002.

---

## II. Rights Class 9 Reuse

**Verdict: CONFIRMED**

Rights Class 9 is defined by DD-NARA-001 as: "Per-record indicator discriminating U.S. federal government works from contributed/copyrighted works, statutory basis 17 U.S.C. § 105." NOAA satisfies both genus-level criteria:

- Legal basis: 17 U.S.C. § 105 — identical to NARA
- Structural pattern: per-record indicator within a mixed-rights collection — identical to NARA

The field vocabulary differs: NARA uses `useRestriction.status` (enum string); NOAA uses Flickr `license` (integer) and Photo Library `credit` (free text). This distinction is a species-level difference, not a genus-level difference. It does not warrant a new Rights Class. Rights Classes are defined by legal-structural type; field vocabulary is handled within the institution-specific Rights Matrix. This is architecturally identical to Getty and Yale both occupying Rights Class 7 under different field implementations.

**Governance finding — dual-path novelty:** NOAA is the first Rights Class 9 institution with dual access paths presenting different rights gate fields (Flickr integer vs. Photo Library credit string). NARA has a single field. SA-NOAA-001 must explicitly scope both paths and must declare which is primary for Sprint 1 (Flickr) and which is the production target (Photo Library). The SA must not treat the two paths as interchangeable — each path has a distinct gate implementation. This is a new pattern within Rights Class 9.

---

## III. Contributor Detection Model

**Verdict: AMENDED**

The DD-NOAA-001 contributor detection model is structurally correct: it identifies the seven contributor classes, establishes credit-line matching as the detection mechanism, and specifies a federal division allow-list. Three amendments are required.

### Amendment 1 — Allow-list strategy: prefix-match, not enumeration

The DD provides an enumerated allow-list of six NOAA divisions: NOAA, NOAA/NMFS, NOAA/NOS, NOAA/OAR, NOAA/NWS, NOAA/NESDIS. NOAA operates dozens of sub-offices, programs, and centers whose credits may appear in image metadata: NOAA/PMEL (Pacific Marine Environmental Laboratory), NOAA/GLERL (Great Lakes Environmental Research Laboratory), NOAA/AOML (Atlantic Oceanographic and Meteorological Laboratory), NOAA Coral Reef Watch, NOAA/GOES Program, NOAA/AVHRR, NOAA/ERDDAP, and others. An enumerated allow-list of six divisions will over-block legitimate federal work from unlisted sub-offices.

**Governance ruling:** SA-NOAA-001 MUST implement a prefix-match strategy, not an enumerated division list:

```
ALLOWED if: credit starts with "NOAA" (case-insensitive)
            AND does not contain a personal name pattern
            AND does not contain a commercial operator term
```

The allow-list MAY retain specific division names as positive confirmation examples, but the primary gate logic is prefix-based: any credit beginning with "NOAA" that does not trigger the personal-name or commercial-operator block patterns is ALLOWED.

### Amendment 2 — Other US federal agency credits: ALLOWED

The DD's allow-list is restricted to NOAA credits and NOAA predecessor agencies. It does not address the case where NOAA hosts an image produced by another US federal agency — NASA, USGS, USFWS (US Fish and Wildlife Service), EPA, NPS, USACE (US Army Corps of Engineers), or NIST. These images are still § 105 works; the copyright analysis is identical. Blocking them from NOAA's collection because their credit says "NASA" or "USGS" would over-block legitimate federal PD content.

**Governance ruling:** SA-NOAA-001 MUST include other US federal agency names in the ALLOWED pattern set. The following names, when appearing as the sole credit entry without a personal name or commercial operator, MUST produce ALLOWED:

- `NASA` / `National Aeronautics and Space Administration`
- `USGS` / `U.S. Geological Survey`
- `USFWS` / `US Fish and Wildlife Service` / `USFWS`
- `NPS` / `National Park Service`
- `EPA` / `U.S. Environmental Protection Agency`
- `NSF` / `National Science Foundation`
- `USACE` / `U.S. Army Corps of Engineers`
- `NIST` / `National Institute of Standards and Technology`
- Any `U.S. [Agency Name]` pattern where the agency is a confirmed federal department

These credits establish the same § 105 basis as NOAA-origin credits. The source slug remains `noaa` (from the ingestion path); the rights basis is still § 105.

### Amendment 3 — Credit precedence rule: personal name takes priority

The DD describes the contributed image detection as a credit-line check but does not specify the precedence logic when multiple signals are present in one credit string. The rule must be explicit:

**Governance ruling:** If a credit string contains ANY personal name pattern — regardless of whether it also contains "NOAA" — the personal-name gate takes precedence and the record MUST be blocked with `reason: "contributed_image_exception"`. Examples:

| Credit String | Ruling |
|---|---|
| `"NOAA"` | ALLOWED |
| `"NOAA/NMFS"` | ALLOWED |
| `"NOAA Fisheries"` | ALLOWED |
| `"John Smith/NOAA"` | BLOCKED — personal name precedes NOAA |
| `"NOAA/John Smith Photography"` | BLOCKED — personal name follows NOAA |
| `"Dr. Jane Doe, NOAA Research"` | BLOCKED — personal name present |
| `"Courtesy of NOAA"` | ALLOWED — Courtesy of a federal agency is fine |
| `"Courtesy of Schmidt Ocean Institute"` | BLOCKED — non-federal |
| `"NASA/JPL-Caltech"` | ALLOWED — confirmed federal agency |
| `"NASA/Bill Ingalls"` | BLOCKED — personal name present |

The personal-name detection pattern must use a heuristic: any sequence of "Firstname Lastname" (two capitalized words) or "[Initial]. [Lastname]" not matching a known federal division abbreviation triggers the block. SA-NOAA-001 specifies the exact pattern.

---

## IV. NOAA-Only Credits — ALLOWED Verification

**Verdict: CONFIRMED WITH AMENDMENTS**

"NOAA" and "NOAA/[federal division]" credits are correctly classified as ALLOWED under 17 U.S.C. § 105. The governing logic — credits from the US federal government source entity carry no copyright by operation of § 105 — is sound. 

Amendments from Section III apply: the allow-list must use prefix-match strategy (Amendment 1) and must include other US federal agency names (Amendment 2). With those amendments applied, the NOAA-only credit classification is correct.

**Predecessor agency credits:** ESSA, USCGS, US Weather Bureau, and Bureau of Commercial Fisheries credits are correctly ALLOWED. These are confirmed federal agencies whose employees' works qualify as § 105 equivalents (works of US government employees, though the precise statutory basis differs slightly for pre-1978 works). Pre-1978, US government works were not protected under common law copyright. The practical effect is the same: these are public domain. ALLOWED confirmed.

---

## V. Personal-Name/NOAA Credits — BLOCKED vs. REVIEW_REQUIRED

**Verdict: BLOCKED — not REVIEW_REQUIRED**

The DD-NOAA-001 classifies `[Name]/NOAA` credits as BLOCKED with `reason: "contributed_image_exception"`. This is the correct governance ruling.

**Rationale against REVIEW_REQUIRED classification:**

IFC-1 is a hard gate under the Institution Factory Constitution. The Illustration Opportunity Doctrine permits only PD or CC0 works. A `[Name]/NOAA` credit indicates that a named individual — not a federal agency — is the attributed creator. This individual may be:
- A private contractor whose copyright was not assigned to the US government
- A third-party contributor (volunteer, researcher, academic)
- A federal employee photographer (whose work WOULD be § 105)

NC cannot determine which without access to NOAA's employment and contract records, which are not available in the public metadata. Placing these records in a REVIEW_REQUIRED queue would create operational overhead without a clear resolution path, since the review would require verifying federal employment status for individual image credits at scale.

The conservative rule is correct: BLOCKED at the adapter level. A future DD-NOAA-002 may establish a named federal employee photographer registry allowing certain `[Name]/NOAA` credits to be elevated from BLOCKED to ALLOWED via a documented exception process. That mechanism requires a separate governance decision and is outside Sprint 1 scope.

**Classification:**

| Credit Pattern | Rights Decision | Reason Code |
|---|---|---|
| `[PersonName]/NOAA` | BLOCKED | `contributed_image_exception` |
| `NOAA/[PersonName]` | BLOCKED | `contributed_image_exception` |
| `[PersonName], NOAA` | BLOCKED | `contributed_image_exception` |
| Any credit with personal name format | BLOCKED | `contributed_image_exception` |

**No REVIEW_REQUIRED status for NOAA.** The REVIEW_REQUIRED workflow (as defined in the Europeana Rights Matrix) is for rights statements that are ambiguous by their standard meaning. The `[Name]/NOAA` credit is not rights-statement ambiguity — it is unresolvable federal-vs-private attribution at the adapter level. The correct IFC-1 response is BLOCKED.

---

## VI. Commercial Imagery Detection

**Verdict: AMENDED — Expanded Block List Required**

DD-NOAA-001 identifies DigitalGlobe, Maxar, Planet Labs, and GeoEye as commercial satellite operators requiring blocking. The governance mandate adds: Getty, Reuters, AP. All seven plus additional operators are confirmed for the SA-NOAA-001 block list.

### VI.1 Rationale for News Agency Addition

Getty Images, Reuters, and the Associated Press are commercial news and photography licensing agencies. US government agencies routinely license imagery from these providers for official communications, press releases, and public affairs materials. These licensed images may appear in NOAA's Photo Library or Flickr channel with NOAA publication provenance but retain third-party copyright held by the licensing agency. NOAA's hosting does not transfer or waive that copyright.

- **Getty Images** licenses editorial photography, commercial stock, and scientific imagery. Licenses to government clients do not sublicense for commercial third-party use. NOAA may have used Getty images in official publications uploaded to their channels.
- **Reuters** licenses news photography. Government agencies use Reuters wire photos in press materials. Same analysis as Getty.
- **AP / Associated Press** licenses photojournalism. Same analysis. AP images are often credited as "AP Photo/[Photographer Name]" — the AP credit pattern must be detected even when the credit structure differs from simple commercial operator names.

### VI.2 Confirmed Commercial Operator Block List

SA-NOAA-001 MUST include the following in the `COMMERCIAL_OPERATOR_BLOCK_PATTERNS` set:

**News/Photography Agencies:**

| Operator | Credit Patterns to Block |
|---|---|
| Getty Images | `"Getty Images"`, `"Getty"`, `"iStock"`, `"iStock by Getty"`, `"iStockphoto"` |
| Reuters | `"Reuters"`, `"Thomson Reuters"`, `"Reuters/"` |
| AP / Associated Press | `"AP"`, `"Associated Press"`, `"AP Photo"`, `"AP/Wide World"` |

**Commercial Satellite Operators:**

| Operator | Credit Patterns to Block |
|---|---|
| Maxar Technologies | `"Maxar"`, `"Maxar Technologies"` |
| DigitalGlobe (legacy Maxar) | `"DigitalGlobe"` |
| Planet Labs | `"Planet"`, `"Planet Labs"`, `"Planet.com"` |
| GeoEye (acquired by Maxar) | `"GeoEye"` |

**Additional commercial satellite operators (extend block list):**

| Operator | Credit Patterns to Block |
|---|---|
| Airbus Defence & Space | `"Airbus"`, `"SPOT Image"`, `"SPOT Satellite"` |
| BlackSky | `"BlackSky"` |
| Satellogic | `"Satellogic"` |

**Foreign space agencies (not § 105 — block as non-US-government):**

| Agency | Credit Patterns to Block |
|---|---|
| ESA (European Space Agency) | `"ESA"` (when not preceded by NOAA) |
| JAXA | `"JAXA"`, `"Japan Aerospace"` |
| CNES | `"CNES"` |
| DLR | `"DLR"`, `"Deutsches Zentrum"` |

**Note on "AP" ambiguity:** The pattern `"AP"` is a short string that may appear in non-photo-credit contexts. SA-NOAA-001 must specify that the block pattern applies to the credit field specifically, not to general text fields. The full pattern `"AP Photo"` is unambiguous; standalone `"AP"` must be checked for credit-field context.

### VI.3 Block Precedence

The commercial operator block takes priority over the federal agency allow logic. If a credit contains both "NOAA" and a commercial operator term (e.g., "NOAA/DigitalGlobe"), the commercial operator takes precedence: BLOCKED with `reason: "licensed_commercial_imagery"`.

---

## VII. Endorsement Restrictions

**Verdict: CONFIRMED**

DD-NOAA-001's endorsement restriction analysis is correct and complete. The statutory basis (5 U.S.C. § 3110, Commerce Department non-endorsement policy) is properly cited. The NOAA-specific requirements are correctly identified.

**Governance confirmation of required compliance items:**

| Requirement | Status | Implementation |
|---|---|---|
| No NOAA name to imply endorsement | CONFIRMED | Operational policy |
| No NOAA circular seal/logo in products | CONFIRMED | Design-time restriction |
| No division logos (NWS, NMFS, NOS) | CONFIRMED | Design-time restriction |
| Standard attribution format | CONFIRMED | "Image: NOAA" acceptable |
| `endorsement_restrictions` field in rights evidence | CONFIRMED | Required in all NOAA records |

**Rights evidence field format (confirmed):**

```json
{
  "endorsement_restrictions": "noaa_nonendorsement_policy",
  "endorsement_restriction_basis": "5 U.S.C. § 3110; NOAA non-endorsement policy",
  "permitted_attribution": "Image: NOAA | Credit: NOAA/[Division]",
  "prohibited_use": "NOAA name/logo to imply government endorsement of NC products"
}
```

This is consistent with the NASA equivalent (DD-NASA-001, Institution #20). The field is required on every NOAA `media_rights` record regardless of which access path produced the record.

---

## VIII. Flickr Dependency Risk

**Verdict: MEDIUM risk — acceptable for Sprint 1 pilot only; NOT acceptable as permanent production path without Platform Dependency Governance Review**

### VIII.1 Risk Quantification

| Risk Dimension | Assessment | Severity | Probability |
|---|---|---|---|
| Platform ownership change | SmugMug acquired Flickr 2018. SmugMug is profitable and stable but is a private company. Further sale or restructuring possible. | HIGH impact | LOW probability |
| API term change | Flickr has changed API terms historically (2018 storage limits, 2019 free account cap). Rate limits could tighten. | MEDIUM impact | MEDIUM probability |
| Government account continuity | NOAA's @usoceangov account is large (25K+ photos) and established. Suspension risk low. | LOW impact | VERY LOW probability |
| Content completeness | Flickr is a SUBSET of NOAA's holdings. Photo Library is the canonical archive. Production at Flickr-only scope permanently limits NC's NOAA content universe. | MEDIUM impact | CERTAIN (it's a fact) |
| License tag reliability | Tags are self-reported. NOAA's account is official. Secondary credit check provides backstop. | LOW impact | VERY LOW probability |
| Full-resolution availability | `url_o` access may be rate-limited or require Pro account. `url_l` (large, ~1024px) is confirmed available. | MEDIUM impact | LOW probability |

### VIII.2 Structural Concern: Third-Party Platform Dependency

NOAA is the first proposed NC institution whose primary confirmed API access path runs through a private third-party platform (Flickr/SmugMug), not a government-operated or institutional API endpoint. All prior NC institutions use their own infrastructure:
- REST APIs on institution-owned domains
- CSV/bulk downloads from institution-owned GitHub or S3
- CKAN DataStore on the institution's domain
- ActivityStreams on institution-owned endpoints

Flickr is not NOAA's infrastructure. NOAA uses Flickr as a social media distribution channel. NC would be ingesting from NOAA via a social media platform, not from NOAA's authoritative data systems.

**This creates a category difference from all prior NC institutions.** The Institution Factory Constitution does not currently address the case of a third-party platform path. SA-NOAA-002 must establish the constitutional basis for accepting this path, including the conditions under which NC would halt Flickr ingestion and the process for migrating to a direct path.

### VIII.3 Acceptability Ruling

The Flickr path is ACCEPTABLE for Sprint 1 (50-asset pilot, 90 days) under three conditions:
1. Sprint 1 is formally designated as a path-confirmation exercise as well as a content pilot
2. Photo Library direct path evaluation is a Sprint 1 deliverable — not Sprint 2
3. SA-NOAA-002 formally limits the Flickr path to Sprint 1/pilot scope and specifies the decision gate for Sprint 2 access path promotion

The Flickr path is NOT acceptable as the permanent production path without a Platform Dependency Governance Review that documents the long-term access path architecture. SA-NOAA-002 must specify the trigger conditions for that review.

---

## IX. Flickr Sprint 1 Acceptability

**Verdict: ACCEPTABLE — with three binding conditions**

Based on Section VIII analysis:

**Condition 1:** Sprint 1 scope is capped at 50 assets and 90 days as specified in DD-NOAA-001. Sprint 1 does not authorize a full catalog harvest from Flickr.

**Condition 2:** Photo Library evaluation is a Sprint 1 deliverable (not Sprint 2). Before Sprint 1 is closed, the team must document: (a) whether the Photo Library has an undocumented API endpoint discoverable via network inspection; (b) whether a bulk download package is available via institutional request; (c) whether an OAI-PMH or RSS feed exists. This evaluation must produce a documented finding that either clears or blocks the Photo Library direct path for Sprint 2.

**Condition 3:** SA-NOAA-002 must include a Platform Dependency Statement (PDS) that formally classifies the Flickr path as `platform_type: third_party_social_media`, documents the known risks, and specifies the Sprint 2 path-promotion decision gate. Without the PDS in SA-NOAA-002, the Flickr path is not ratified for any sprint.

---

## X. Governance Findings Summary and Conditions of Approval

### Findings

| # | Area | Finding |
|---|---|---|
| GF-1 | Rights Class 9 | CONFIRMED. Dual-path novelty documented; SA-NOAA-001 must scope both paths explicitly. |
| GF-2 | Contributor detection | AMENDED. Three amendments required: prefix-match strategy, other federal agency allow-list, personal-name precedence rule. |
| GF-3 | NOAA-only credits ALLOWED | CONFIRMED WITH AMENDMENTS. Prefix-match strategy (GF-2 Amendment 1) and federal agency expansion (GF-2 Amendment 2) apply. |
| GF-4 | [Name]/NOAA credits | BLOCKED confirmed. No REVIEW_REQUIRED pathway for contributor attribution. |
| GF-5 | Commercial block list | AMENDED. Getty, Reuters, AP added. Foreign space agencies added. Precedence rule stated. |
| GF-6 | Endorsement restrictions | CONFIRMED. `endorsement_restrictions` field required in all NOAA rights evidence records. |
| GF-7 | Flickr dependency risk | MEDIUM. Third-party platform dependency is a new architectural category for NC. SA-NOAA-002 must include Platform Dependency Statement. |
| GF-8 | Flickr Sprint 1 | ACCEPTABLE with three binding conditions (Section IX). |

### Conditions of Approval

The following five conditions are binding. SA-NOAA-001 and SA-NOAA-002 are not ratified until all five are satisfied.

**Condition 1 — SA-NOAA-001: Prefix-match allow strategy**  
SA-NOAA-001 MUST implement prefix-match logic for the NOAA credit allow-list. The allow gate is: credit starts with "NOAA" (case-insensitive) AND no personal name AND no commercial operator. Division enumeration is advisory, not the gate logic.

**Condition 2 — SA-NOAA-001: Other US federal agency credits ALLOWED**  
SA-NOAA-001 MUST include confirmed US federal agency names (NASA, USGS, USFWS, NPS, EPA, NSF, USACE, NIST) in the ALLOWED pattern set. These are § 105 works appearing in NOAA's channels. Rights basis is unchanged.

**Condition 3 — SA-NOAA-001: Expanded commercial operator block list**  
SA-NOAA-001 MUST include Getty Images, Reuters, and AP in the `COMMERCIAL_OPERATOR_BLOCK_PATTERNS` set, in addition to the satellite operators already listed in DD-NOAA-001. Foreign space agencies (ESA, JAXA, CNES, DLR) must also be blocked as non-§ 105 entities.

**Condition 4 — SA-NOAA-002: Platform Dependency Statement**  
SA-NOAA-002 MUST include a formal Platform Dependency Statement classifying the Flickr path as `platform_type: third_party_social_media`, documenting the known risks, and specifying: (a) the Sprint 1 scope limitation; (b) the Photo Library evaluation deliverable; (c) the Sprint 2 path-promotion decision gate; (d) the conditions under which NOAA ingestion pauses (API term change, account inaccessibility).

**Condition 5 — SA-NOAA-002: Flickr path explicitly scoped to Sprint 1**  
SA-NOAA-002 MUST state that the Flickr path is authorized for Sprint 1 only (50-asset pilot). Sprint 2 and beyond require either: (a) Photo Library direct path confirmed viable, OR (b) a separate Platform Dependency Governance Review formally authorizing Flickr as production path. No Sprint 2 Flickr harvest proceeds without one of these two gates being met.

---

## XI. Ratification Table

| Role | Approval | Date |
|---|---|---|
| Governance Review | ☐ PENDING | — |
| Principal Architect | ☐ PENDING | — |

**For full ratification of DD-NOAA-001:**  
All five conditions in Section X must be satisfied, SA-NOAA-001 and SA-NOAA-002 must be ratified, and DD-NOAA-001's ratification table must be countersigned.

---

*NOAA Governance Review v1 — drafted 2026-06-11*  
*Authority: DD-NOAA-001, IFC-1–IFC-12, 17 U.S.C. § 105*  
*Precedents consulted: DD-NARA-001 (Rights Class 9), DD-GALLICA-003 (IFC-1 hard gate), Europeana Rights Matrix v1 (REVIEW_REQUIRED doctrine)*
