# SA-NOAA-001: NOAA Rights Matrix v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | DRAFT — Pending Ratification |
| SA Number | SA-NOAA-001 |
| Repository | opengracelabs/nc |
| Drafted | 2026-06-11 |
| Authority | DD-NOAA-001 · Institution Factory Constitution v1 (IFC-1) · 17 U.S.C. § 105 · NOAA Governance Review v1 |
| Rights Class | 9 (reuse — same as NARA, DD-NARA-001) |
| Source Slug | `noaa` |
| `rights_policy_id` | `"noaa_rights_matrix_v1"` |
| Blocks | NOAA Sprint 1 (required before adapter implementation) |

---

## Governing Principle

NOAA is a US federal civilian agency. Works produced by NOAA employees within the scope of their federal employment are works of the United States Government and are not eligible for copyright protection under 17 U.S.C. § 105.

This matrix governs how the NOAA adapter distinguishes federal government works (§ 105, PD, ALLOWED) from contributed or licensed works (third-party copyright, BLOCKED) within NOAA's mixed-rights image collections.

**The IFC-1 hard gate applies without exception.** No record may be written unless it passes the gate logic in Part I or Part II. No REVIEW_REQUIRED workflow exists for NOAA — ambiguous attribution is BLOCKED. This is the same hard gate as NARA (DD-NARA-001).

**Rights Class 9 dual-path note:** NOAA is the first Rights Class 9 institution with two distinct access paths presenting different rights gate fields. Path A (Flickr) uses an integer `license` field as the primary gate. Path B (Photo Library) uses a `credit` free-text string as the primary gate. Both paths apply the same secondary validation rules (Sections III–V). The rights class is the same; the field vocabulary differs by path.

---

## Part I — Path A: Flickr API Gate (Sprint 1 Pilot Path)

Path A governs records ingested via the Flickr API from NOAA's official Flickr accounts (@usoceangov, @noaafisheries, and any other confirmed NOAA federal accounts).

### I.1 Primary Gate — Flickr License Integer

The Flickr `license` field on each photo is the primary IFC-1 gate for Path A.

| Flickr License ID | License Name | NC Decision | Basis |
|---|---|---|---|
| 8 | United States Government Work | ALLOWED (subject to II.1) | Explicit § 105 assertion by uploader |
| 7 | No known copyright restrictions | ALLOWED (subject to II.1) | PD assertion consistent with § 105 |
| 9 | Public Domain Dedication (CC0) | ALLOWED (subject to II.1) | Explicit CC0 waiver |
| 10 | Public Domain Mark | ALLOWED (subject to II.1) | PD declaration |
| 0 | All Rights Reserved | BLOCKED | `copyright_retained` |
| 1 | CC BY-NC-SA 2.0 | BLOCKED | `non_commercial_restriction` |
| 2 | CC BY-NC 2.0 | BLOCKED | `non_commercial_restriction` |
| 3 | CC BY-NC-ND 2.0 | BLOCKED | `non_commercial_restriction` |
| 4 | CC BY 2.0 | BLOCKED | `doctrine_requires_pd_not_cc` |
| 5 | CC BY-SA 2.0 | BLOCKED | `doctrine_requires_pd_not_cc` |
| 6 | CC BY-ND 2.0 | BLOCKED | `derivative_restriction` |
| Missing / unrecognized | — | BLOCKED | `missing_license_field` |

**Note on licenses 4–6 (CC BY variants):** These are commercially usable but retain copyright. NC's Illustration Opportunity Doctrine requires PD or CC0; CC BY is not sufficient. These are BLOCKED pending a doctrine amendment. Block reason: `doctrine_requires_pd_not_cc`.

**Note on license 8 scope:** Flickr License 8 carries this statement: "This work, identified by [URL], has been cleared by the rights holder as a United States Government Work. As a Work of the United States Government, it is not subject to copyright." This is a self-reported § 105 assertion by the uploader. For NOAA's official government accounts, this assertion is trusted as primary evidence. The secondary validation in Part II provides the backstop for mislabelled records.

### I.2 Scope Restriction — NOAA Official Accounts Only

Path A applies ONLY to images from confirmed NOAA federal Flickr accounts. An account is confirmed NOAA federal if it is operated by a NOAA organizational unit and was verified as such in the Sprint 1 account audit.

Confirmed accounts (Sprint 1 to verify and expand):
- `@usoceangov` — NOAA Ocean Service
- `@noaafisheries` — NOAA Fisheries (National Marine Fisheries Service)

Any additional NOAA Flickr account must be explicitly confirmed and added to the account list before its images may be ingested. Images from non-NOAA accounts, even if tagged License 8, are outside this matrix's scope.

---

## Part II — Path B: Photo Library Gate (Sprint 1 Evaluation; Production Target)

Path B governs records ingested directly from the NOAA Photo Library (photolib.noaa.gov) if a documented bulk download or API path is confirmed during Sprint 1 evaluation.

**Status:** Path B is NOT active for Sprint 1. Sprint 1 must complete a Photo Library access path evaluation (DD-NOAA-001 Article 11, SA-NOAA-002 Platform Dependency Statement). If confirmed viable, Path B becomes the production standard in Sprint 2 and Flickr (Path A) is demoted to fallback.

### II.1 Primary Gate — Credit Field

The `credit` text field on each Photo Library image is the primary IFC-1 gate for Path B.

**Decision logic (evaluated in priority order):**

1. If `credit` is missing or empty → BLOCKED (`missing_credit_field`)
2. If `credit` contains any `COMMERCIAL_OPERATOR_BLOCK_PATTERNS` term (Part IV) → BLOCKED (`licensed_commercial_imagery`)
3. If `credit` contains any `PERSONAL_NAME_PATTERNS` match (Part V) → BLOCKED (`contributed_image_exception`)
4. If `credit` starts with `"NOAA"` (case-insensitive) → ALLOWED candidate (proceed to Part III)
5. If `credit` matches any `FEDERAL_AGENCY_ALLOW_PATTERNS` (Part VI) → ALLOWED candidate (proceed to Part III)
6. If `credit` starts with `"Courtesy of"` followed by a federal agency name → ALLOWED candidate
7. If `credit` starts with `"Courtesy of"` followed by any non-federal name → BLOCKED (`donated_content`)
8. All other credit values → BLOCKED (`unrecognized_credit`)

---

## Part III — Secondary Validation (Both Paths)

Secondary validation applies to all records that passed the primary gate in Part I or Part II. It examines the full text of the available metadata fields (Flickr description/title or Photo Library caption/credit) for contributor-class signals that the primary gate may have missed.

### III.1 Personal Name Detection

Scan the `credit`, `description`, and `title` fields for patterns matching `PERSONAL_NAME_PATTERNS`:

**PERSONAL_NAME_PATTERNS** — any of the following:
- Two or more consecutive capitalized words where neither word matches a known federal division abbreviation or agency name (heuristic for "Firstname Lastname")
- Pattern: `[A-Z][a-z]+ [A-Z][a-z]+` not in the federal allow-list
- Pattern: `[A-Z]\. [A-Z][a-z]+` (initial + last name)
- Pattern: `Dr\.`, `Prof\.`, `Mr\.`, `Ms\.`, `Mrs\.` followed by a name

If any PERSONAL_NAME_PATTERNS match is found in credit/description: BLOCKED (`contributed_image_exception`).

**Exceptions from personal name blocking:**
- "New Hampshire", "New Mexico", "New Zealand" — geographic names, not personal names
- Federal division abbreviations that match the pattern incidentally (e.g., "NOS" is not "N.O.S.")
- Verified federal employee names added to the named_federal_employee_registry (future DD-NOAA-002 scope)

### III.2 "Courtesy of" Pattern

`"Courtesy of [non-federal source]"` → BLOCKED (`donated_content`).
`"Courtesy of [federal agency]"` → ALLOWED (passes to rights evidence with federal agency noted as source).
`"Courtesy of NOAA"` → ALLOWED (NOAA-origin confirmed even via third-party hosting).

### III.3 Missing Image Evidence

If a record passes the rights gate but has no valid image URL (no Flickr photo URL or no Photo Library file URL available) → BLOCKED (`missing_image_evidence`). This is independent of the rights gate and applies to both paths.

---

## Part IV — Commercial Operator Block Patterns

The following terms, when found anywhere in the `credit`, `description`, or `title` fields, trigger BLOCKED (`licensed_commercial_imagery`). Pattern matching is case-insensitive. Check `credit` field first; check description/title if credit is absent or ambiguous.

**Commercial operator block takes priority over the federal agency allow.** If both a federal agency name AND a commercial operator term appear in the same credit string, the commercial operator takes precedence.

### IV.1 News and Photography Agencies

| Operator | Patterns |
|---|---|
| Getty Images | `"Getty Images"`, `"Getty"`, `"iStock"`, `"iStockphoto"`, `"iStock by Getty"` |
| Reuters | `"Reuters"`, `"Thomson Reuters"` |
| AP / Associated Press | `"Associated Press"`, `"AP Photo"`, `"AP/Wide World"` |
| Shutterstock | `"Shutterstock"` |
| Alamy | `"Alamy"` |

**Note on `"AP"` alone:** Standalone `"AP"` is ambiguous (may appear in many contexts). Apply only when `"AP"` appears in the `credit` field and is followed by `"Photo"`, `/`, or is the full credit value. Do not block on `"AP"` appearing in general description text.

### IV.2 Commercial Satellite Operators

| Operator | Patterns |
|---|---|
| Maxar Technologies | `"Maxar"`, `"Maxar Technologies"` |
| DigitalGlobe (legacy Maxar) | `"DigitalGlobe"` |
| Planet Labs | `"Planet Labs"`, `"Planet.com"`, `"Planet"` (credit field only) |
| GeoEye (acquired by Maxar) | `"GeoEye"` |
| Airbus Defence & Space | `"Airbus"`, `"SPOT Image"`, `"SPOT Satellite"` |
| BlackSky | `"BlackSky"` |
| Satellogic | `"Satellogic"` |

### IV.3 Foreign Space Agencies (Not § 105)

These agencies produce federally analogous work under their own national frameworks but are not US government entities. Their works are not covered by 17 U.S.C. § 105 and are not in the US public domain by statute. When appearing as the primary credit (not accompanied by a US federal agency credit), BLOCKED (`not_us_federal_work`).

| Agency | Patterns |
|---|---|
| ESA | `"ESA"`, `"European Space Agency"` |
| JAXA | `"JAXA"`, `"Japan Aerospace"` |
| CNES | `"CNES"` |
| DLR | `"DLR"`, `"Deutsches Zentrum"` |
| CSA (Canadian Space Agency) | `"CSA"`, `"Canadian Space Agency"` |

**Exception:** If a foreign space agency credit appears TOGETHER WITH a US federal agency credit (e.g., "NASA/ESA"), the image is the result of a joint mission. In such cases, apply the REVIEW_REQUIRED exception: create a `workflow_item` of type `joint_mission_rights_review`. This is the only REVIEW_REQUIRED pathway for NOAA. Most joint mission images will resolve BLOCKED, but the reviewing human may confirm US-origin elements if documentation supports it.

---

## Part V — Personal Name Block Patterns

In addition to the heuristic described in Section III.1, the following explicit patterns BLOCK a record regardless of other credit content:

- Any credit matching `[PersonName]/NOAA` (name precedes slash and "NOAA")
- Any credit matching `NOAA/[PersonName Photography|PersonName Images|PersonName Studio]`
- Any credit containing `"photo by"`, `"photograph by"`, `"image by"`, `"©"` (copyright symbol) followed by a name
- Any credit containing `"photographer:"` followed by a name not in the federal-employee-registry

Block reason: `contributed_image_exception`

---

## Part VI — Federal Agency Allow Patterns

The following US federal agency names or prefixes, when appearing as the primary credit without a personal name or commercial operator, establish § 105 PD status and produce ALLOWED:

### VI.1 NOAA and Divisions (Prefix-Match)

Any credit that begins with `"NOAA"` (case-insensitive) and does not trigger Part IV or Part V → ALLOWED.

This covers all NOAA divisions, sub-offices, and programs without enumeration:
- NOAA/NMFS, NOAA/NOS, NOAA/OAR, NOAA/NWS, NOAA/NESDIS (named for documentation; not the exhaustive list)
- NOAA Coral Reef Watch, NOAA/PMEL, NOAA/GLERL, NOAA/AOML, NOAA Fisheries, NOAA Ocean Service, NOAA Research, etc. — all covered by prefix-match

### VI.2 NOAA Predecessor Agencies

The following predecessor agency names establish § 105-equivalent PD status for images produced by their federal employees:

| Predecessor Agency | Patterns |
|---|---|
| Environmental Science Services Administration | `"ESSA"` |
| US Coast and Geodetic Survey | `"USCGS"`, `"US Coast and Geodetic Survey"`, `"Coast and Geodetic Survey"` |
| US Weather Bureau | `"US Weather Bureau"`, `"Weather Bureau"` |
| Bureau of Commercial Fisheries | `"Bureau of Commercial Fisheries"` |

### VI.3 Other US Federal Agencies

Works by employees of the following agencies, when hosted in NOAA's channels, are § 105 works. Source slug remains `noaa` (from ingestion path); rights basis is § 105.

| Agency | Patterns |
|---|---|
| NASA | `"NASA"` (prefix-match: any credit beginning with "NASA" not triggering Part IV) |
| USGS | `"USGS"`, `"U.S. Geological Survey"`, `"US Geological Survey"` |
| USFWS | `"USFWS"`, `"US Fish and Wildlife Service"`, `"U.S. Fish and Wildlife Service"` |
| NPS | `"NPS"`, `"National Park Service"` |
| EPA | `"EPA"`, `"U.S. Environmental Protection Agency"` |
| NSF | `"NSF"`, `"National Science Foundation"` |
| USACE | `"USACE"`, `"U.S. Army Corps of Engineers"` |
| NIST | `"NIST"`, `"National Institute of Standards and Technology"` |
| NOAA/NASA joint | `"NOAA/NASA"`, `"NASA/NOAA"` — both are federal; ALLOWED |

**Note:** Personal-name precedence applies equally to other federal agency credits. `"NASA/Bill Ingalls"` → BLOCKED (`contributed_image_exception`). `"NASA"` alone → ALLOWED.

---

## Part VII — Rights Evidence Fields

Every NOAA record that passes the IFC-1 gate MUST include the following fields in `media_rights.rights_evidence`:

```json
{
  "rights_policy_id": "noaa_rights_matrix_v1",
  "rights_class": 9,
  "legal_basis": "17 U.S.C. § 105 — Work of the United States Government",
  "access_path": "flickr_api" | "photo_library",
  "primary_gate_field": "flickr_license" | "credit",
  "primary_gate_value": <exact field value as received from API or metadata>,
  "federal_source_confirmed": true,
  "credit_line": <exact credit string from source, or null if absent>,
  "commercial_operator_scan": "passed",
  "personal_name_scan": "passed",
  "endorsement_restrictions": "noaa_nonendorsement_policy",
  "endorsement_restriction_basis": "5 U.S.C. § 3110; NOAA non-endorsement policy",
  "permitted_attribution": "Image: NOAA | Credit: NOAA/[Division]",
  "prohibited_use": "NOAA name/logo to imply government endorsement"
}
```

**FM-4 invariant:** `media_rights.rights_status` MUST be written as `"pending_verification"` by the adapter worker. Reclassification to `"classified_pd"` occurs in `build_rights_evidence` via SA-9 slug remap. The adapter worker MUST NOT write `"verified_pd"` or `"classified_pd"`.

---

## Part VIII — Block Reason Code Registry

| Reason Code | Trigger |
|---|---|
| `copyright_retained` | Flickr license 0 (All Rights Reserved) |
| `non_commercial_restriction` | Flickr license 1–3 (CC NC variants) |
| `derivative_restriction` | Flickr license 6 (CC ND) |
| `doctrine_requires_pd_not_cc` | Flickr license 4–5 (CC BY variants) |
| `missing_license_field` | Flickr license missing or unrecognized |
| `licensed_commercial_imagery` | Commercial operator term in credit |
| `contributed_image_exception` | Personal name in credit |
| `donated_content` | "Courtesy of [non-federal]" in credit |
| `international_collaboration` | Foreign agency credit (non-US-government) |
| `not_us_federal_work` | Foreign space agency credit without US federal co-credit |
| `missing_credit_field` | Credit field absent (Photo Library path) |
| `unrecognized_credit` | Credit present but matches no allow or block pattern |
| `missing_image_evidence` | No valid image URL in record |

---

## Part IX — Invariants

**RM-I-1 — IFC-1 Hard Gate.** BLOCKED classifications cannot be overridden by human review, Director Decision, or matrix amendment alone. Lifting a BLOCKED classification for a specific contributor class requires a doctrine amendment (permitting non-PD works) AND a new version of this matrix.

**RM-I-2 — FM Exclusion (Permanent).** Foundation Model output may not influence any rights determination. This is inherited from FM Constitution v1.0 Invariant FM-4 and is permanent. The `rights_analysis_advisory` FM use case produces output in `fm_candidate_record` only and has no connection to this matrix's decision pipeline.

**RM-I-3 — Commercial Operator Priority.** The commercial operator block (Part IV) takes precedence over all allow patterns. If a credit contains both a federal agency name and a commercial operator term, the commercial operator rule applies and the record is BLOCKED.

**RM-I-4 — Personal Name Priority.** Personal name detection (Part V) takes precedence over the federal-prefix allow rule. If a credit starts with "NOAA" but also contains a personal name, the personal name rule applies and the record is BLOCKED.

**RM-I-5 — No REVIEW_REQUIRED except Joint Mission.** The only REVIEW_REQUIRED pathway in this matrix is the joint-mission exception (Part IV, Section IV.3). All other ambiguous cases are BLOCKED. There is no general human-review queue for contributor attribution ambiguity.

**RM-I-6 — Source Slug Immutability.** All records ingested via the NOAA adapter, regardless of which other federal agency produced the image (NASA, USGS, etc.), carry source slug `"noaa"`. The originating agency is recorded in rights evidence but does not change the source slug.

---

## Part X — Open Questions

**OQ-1 — Named Federal Employee Registry.** A future DD-NOAA-002 may establish a registry of known NOAA federal employee photographers whose `[Name]/NOAA` credits can be elevated from BLOCKED to ALLOWED. This would require NOAA employment verification and a formal exception process. Currently out of scope.

**OQ-2 — "AP" Standalone Pattern.** The standalone pattern `"AP"` in a credit field is ambiguous. Sprint 1 must determine whether NOAA-hosted images ever carry standalone `"AP"` as a full credit value (which would be unambiguously AP wire photo) vs. `"AP"` as a partial substring. SA-NOAA-001 v1.1 may refine this pattern after Sprint 1 credit field survey.

**OQ-3 — Joint Mission REVIEW_REQUIRED Volume.** If NASA/ESA, NASA/JAXA, or other joint-mission credits appear frequently in NOAA's Flickr collection, the REVIEW_REQUIRED queue volume may exceed operational capacity. Revisit after Sprint 1 credit survey.

**OQ-4 — Photo Library Credit Field Name.** The `credit` field name in the Photo Library's metadata structure has not been confirmed. Sprint 1 must confirm the exact field name and provide it to SA-NOAA-001 v1.1 if it differs from `"credit"`.

---

*SA-NOAA-001 v1.0.0 — drafted 2026-06-11*  
*Authority: DD-NOAA-001 · IFC-1 · 17 U.S.C. § 105 · NOAA Governance Review v1*  
*Precedent: SA-22 (NARA Rights Matrix v1) — same Rights Class 9 basis, different field vocabulary*  
*Next version trigger: Named federal employee registry (OQ-1), Photo Library credit field confirmation (OQ-4), joint mission volume assessment (OQ-3)*
