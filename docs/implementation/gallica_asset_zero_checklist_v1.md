# Gallica Asset Zero Checklist v1.0

| Field | Value |
|---|---|
| **Version** | 1.0 |
| **Status** | Operative — effective upon DD-GALLICA-002 ratification |
| **Scope** | BnF Gallica Madagascar pilot Asset Zero validation |
| **Governing Decision** | DD-GALLICA-002 Article 7 |
| **Target** | Gate 4 of the DD-GALLICA-002 governance gate sequence |
| **Required output** | Asset Zero ARK identifier, confirmed rights classification, confirmed IIIF delivery, second-human activation approval |

---

## Purpose

Asset Zero is the first asset ingested into the NC pipeline from a new content
institution. For Gallica, it simultaneously validates the IIIF 2.1 → 3.0 bridging
adapter in production, confirms the Gallica Rights Addendum v1 text-path classification
logic, and demonstrates end-to-end pipeline completion for a real Gallica asset.

Asset Zero must be completed and activated (second-human approval received) before any
pilot batch runs. It is Gate 4 of the DD-GALLICA-002 governance sequence.

---

## Phase 0 — Pre-Flight Checks

Before beginning the candidate search, confirm all of the following. If any item fails,
halt and resolve before proceeding.

| # | Pre-flight check | Result |
|---|---|---|
| 0.1 | Gates 0, 1, 2, 3 of DD-GALLICA-002 are closed | ☐ |
| 0.2 | IIIF 2.1 → 3.0 bridging adapter is deployed | ☐ |
| 0.3 | OAI-PMH worker is deployed with Gallica Rights Addendum v1 text-path logic | ☐ |
| 0.4 | Rate limiter is active: ≤ 2 req/s against Gallica endpoints | ☐ |
| 0.5 | French-language rights reviewer is available for this session | ☐ |
| 0.6 | `source_id = 'bnf_gallica'` is in sources table with `governance_state = 'active'` | ☐ |
| 0.7 | FM exclusion is confirmed in Gallica pipeline for this session | ☐ |

---

## Phase 1 — Candidate Identification

### Step 1.1 — Priority source publications

Attempt the following SRU queries in priority order. Stop at the first query that
returns ≥ 1 clean candidate.

**Priority 1 — Buffon "Histoire Naturelle" lemur plates:**

```
SRU endpoint: https://gallica.bnf.fr/SRU
Query: dc.creator all "Buffon" AND dc.subject any "maki" 
       AND dc.type = "image" AND dc.date < "1805"
Maximum records: 20
Record schema: dc
```

Expected results: plates from Buffon's "Histoire Naturelle" supplements (ca. 1774–1789).
Look for "maki", "maki vari", "maki mongoz", "maki vari" in dc:title.

**Priority 2 — Sonnerat "Voyage aux Indes" Madagascar illustrations:**

```
SRU endpoint: https://gallica.bnf.fr/SRU
Query: dc.creator all "Sonnerat" AND dc.subject any "Madagascar" 
       AND dc.type = "image" AND dc.date < "1785"
Maximum records: 20
Record schema: dc
```

Expected results: plates from Sonnerat's "Voyage aux Indes orientales et à la Chine"
(1782). Madagascar birds, mammals, and plants.

**Priority 3 — Broader Madagascar pre-1800 natural history:**

```
SRU endpoint: https://gallica.bnf.fr/SRU
Query: dc.subject any "Madagascar" AND dc.type = "image" 
       AND dc.date < "1800" AND dc.subject any "naturelle"
Maximum records: 20
Record schema: dc
```

**Priority 4 — Audebert/Vieillot Madagascar birds (marginally post-1800):**

```
SRU endpoint: https://gallica.bnf.fr/SRU
Query: dc.creator any "Audebert Vieillot" AND dc.subject any "Madagascar"
       AND dc.type = "image" AND dc.date < "1810"
Maximum records: 20
Record schema: dc
```

### Step 1.2 — Candidate shortlist

From the query results, build a shortlist of up to 5 candidates. Populate the following
table for each candidate:

| # | ARK identifier | dc:title | dc:creator | dc:date | dc:subject | dc:rights |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

### Step 1.3 — OAI-PMH metadata fetch for shortlisted candidates

For each shortlisted candidate, fetch the OAI-PMH Dublin Core record:

```
OAI-PMH endpoint: https://gallica.bnf.fr/services/OAIRecord
Parameters: identifier=oai:bnf.fr:gallica/{ark_id}  (substitute ark_id = last segment)
            metadataPrefix=oai_dc
```

Capture:
- Full `dc:rights` text (all instances if multiple)
- Full `dc:date` (publication year)
- `dc:type` values
- `dc:description` (may contain additional rights or condition text)
- `dc:identifier` (confirm ARK)

Record findings per candidate.

---

## Phase 2 — Candidate Evaluation and Selection

### Step 2.1 — Date confirmation

For each candidate, confirm the publication date is within acceptable range:

| Criterion | Requirement |
|---|---|
| Buffon "Histoire Naturelle" plates | dc:date ≤ 1804 (Imprimerie Royale editions) |
| Sonnerat "Voyage aux Indes" | dc:date = 1782 |
| Other pre-1800 | dc:date ≤ 1799 |
| Audebert/Vieillot (emergency fallback) | dc:date ≤ 1802; note the post-1800 date |

If `dc:date` is absent, check `dc:description` for date information. If date is
ambiguous, request HR-GA-1 (date confirmation review) before proceeding.

### Step 2.2 — Subject qualification

Confirm the illustration subject is an endemic Madagascar species. Qualifying subjects:

| Subject | Species | Notes |
|---|---|---|
| "maki" | *Lemur catta* (ring-tailed lemur) | Buffon's primary lemur taxon; best commercial candidate |
| "maki vari" / "maki vari blanc et noir" | *Varecia variegata* (ruffed lemur) | Buffon supplements; also excellent |
| "maki mongoz" | *Eulemur mongoz* (mongoose lemur) | Acceptable |
| "aye-aye" | *Daubentonia madagascariensis* | Sonnerat; exceptional rarity |
| "fossa" | *Cryptoprocta ferox* | Madagascar-endemic carnivore |
| Madagascar endemic birds | Various Coua, Vanga, etc. | Acceptable (Sonnerat/Vieillot) |

Reject candidates showing non-endemic species even if "Madagascar" appears in subject
(e.g., illustrations of introduced livestock, European-range birds photographed in
Madagascar context).

### Step 2.3 — Primary candidate selection

Select one candidate from the shortlist based on:
1. Subject (lemur > bird > other endemic)
2. Source publication (Buffon > Sonnerat > other)
3. Date (earlier is better — pre-1785 preferred)
4. Rights field clarity ("domaine public" text preferred over "libre de réutilisation")

Record the selected candidate:

| Field | Value |
|---|---|
| **Selected ARK** | |
| **dc:title** | |
| **dc:creator** | |
| **dc:date** | |
| **dc:rights** (full text) | |
| **dc:subject** (relevant) | |
| **Source publication** | |
| **Selection rationale** | |

---

## Phase 3 — Rights Classification

### Step 3.1 — IIIF manifest rights check

Fetch the IIIF 2.1 manifest from Gallica:

```
URL: https://gallica.bnf.fr/iiif/ark:/12148/{ark_id}/manifest.json
```

Check the `license` field in the manifest:

| If manifest `license` field | Classification | Action |
|---|---|---|
| Contains CC0 URI | `verified_cc0` | Proceed |
| Contains PDM URI | `verified_pd` | Proceed |
| Contains NoC-US URI | `verified_pd` (with NoC-US evidence) | Proceed (preferred for Asset Zero) |
| Contains REVIEW REQUIRED URI | `review_required` | Do NOT use as Asset Zero — pick another candidate |
| Contains BLOCKED URI | `ineligible` | Do NOT use as Asset Zero — pick another candidate |
| Field absent | Continue to dc:rights URI check | |

IIIF manifest `license` field result: ___________________

### Step 3.2 — OAI-PMH dc:rights URI check

If the IIIF `license` field is absent, check `dc:rights` for a URI:

Does `dc:rights` contain a rightsstatements.org or creativecommons.org URI?
☐ Yes — classify per Europeana Rights Matrix v1.0 (same rules as IIIF URI path)
☐ No — proceed to text-path classification (Step 3.3)

dc:rights URI (if present): ___________________
Classification (if URI path used): ___________________

### Step 3.3 — Gallica Rights Addendum v1 text-path classification

If no valid URI is found in IIIF `license` or `dc:rights`, classify the `dc:rights`
text using Table GA-1A:

| dc:rights text (normalized, lowercased) | Classification |
|---|---|
| "domaine public" (anywhere in text) | `verified_pd` — proceed to HR-GA-1 confirmation |
| "public domain" | `verified_pd` — proceed to HR-GA-1 confirmation |
| "libre de réutilisation" | `verified_pd` — proceed to HR-GA-2 scope confirmation |
| "usage commercial autorisé" | `verified_pd` — proceed to HR-GA-1 confirmation |
| "domaine public revisité" | REVIEW REQUIRED — **do NOT use as Asset Zero** |
| "usage non-commercial uniquement" | BLOCKED — do NOT use |
| "droits réservés" / "tous droits réservés" | BLOCKED — do NOT use |
| "under copyright" / "all rights reserved" | BLOCKED — do NOT use |
| None of the above | REVIEW REQUIRED — **do NOT use as Asset Zero** |
| dc:rights absent AND IIIF license absent | BLOCKED — do NOT use |

**For Asset Zero: only ALLOWED (verified_pd or verified_cc0) classifications proceed.**
If the candidate has any other classification, select a different candidate.

dc:rights text (full, verbatim): ___________________
Text-path classification result: ___________________

### Step 3.4 — HR-GA-1 date confirmation (if text-path used)

If Step 3.3 produced a `verified_pd` via text-path, complete HR-GA-1 date confirmation:

- Publication date confirmed from dc:date: _____________________
- Date is ≤ 1800 (preferred) or ≤ 1904 (minimum for PD in France): ☐ Yes / ☐ No
- BnF Tier 1 PD authority applies (per DD-GALLICA-001 Article 3.3): ☐ Yes
- Date confirmation completed by (French-language reviewer): _____________________

### Step 3.5 — Rights classification record

| Field | Value |
|---|---|
| **Final rights_status** | |
| **Rights evidence source** | IIIF URI path / dc:rights URI path / text path |
| **Rights evidence text/URI** | |
| **HR review type completed** | HR-GA-1 / HR-GA-2 / none (URI path only) |
| **HR reviewer** | |
| **Classification date** | |

---

## Phase 4 — IIIF Delivery Validation

### Step 4.1 — Full-resolution image check

Construct the IIIF Image API full-resolution URL:

```
URL: https://gallica.bnf.fr/iiif/ark:/12148/{ark_id}/f1/full/full/0/native.jpg
```

Fetch the image and verify:

| Check | Result |
|---|---|
| HTTP status code = 200 | ☐ Pass / ☐ Fail |
| Content-Type = image/jpeg or image/png | ☐ Pass / ☐ Fail |
| Image width ≥ 400px | _____ px |
| Image height ≥ 400px | _____ px |
| Image is watermark-free (visual inspection) | ☐ Pass / ☐ Fail |
| Image is hand-colored illustration (not photographic reproduction) | ☐ Yes / ☐ No |
| Recommended: shortest side ≥ 2000px for MASTERWORK tier | ☐ Yes / ☐ No |

If any check fails, select a different candidate.

### Step 4.2 — IIIF 2.1 manifest fetch and inspection

Fetch the raw IIIF 2.1 manifest:

```
URL: https://gallica.bnf.fr/iiif/ark:/12148/{ark_id}/manifest.json
```

Confirm the following IIIF 2.1 structure is present (these are inputs to the bridging
adapter — they should be present to be transformed, not absent):

| IIIF 2.1 field | Expected | Present? |
|---|---|---|
| `@context` containing "presentation/2" | String URL | ☐ |
| `@id` at manifest root | ARK-based URI | ☐ |
| `@type: "sc:Manifest"` | String | ☐ |
| `sequences` array with at least 1 sequence | Array | ☐ |
| `sequences[0].canvases` array | Array | ☐ |
| `metadata` array with label-value pairs | Array | ☐ |
| `label` (manifest title) | String or object | ☐ |
| `thumbnail` (manifest level, optional but common) | Object | ☐ or N/A |
| `license` field (rights URI, may be absent) | String URI or absent | ☐ / absent |

If `sequences[0].canvases` is absent, the bridging adapter cannot produce a valid
IIIF 3.0 manifest — select a different candidate.

### Step 4.3 — IIIF 2.1 → 3.0 bridging adapter test

Run the candidate ARK through the bridging adapter (per docs/standards/gallica_iiif_bridge_v1.md):

```
Input: raw IIIF 2.1 manifest (fetched in Step 4.2)
Output: IIIF 3.0 manifest
```

Validate the output manifest against IIIF Presentation API 3.0:

| Validation check | Expected | Result |
|---|---|---|
| `@context` = "http://iiif.io/api/presentation/3/context.json" | Exact string | |
| `id` present at manifest root (not `@id`) | URI | |
| `type: "Manifest"` | Exact string | |
| `items` array present (not `sequences`) | Array | |
| Each canvas has `type: "Canvas"` | String | |
| Each canvas has `items` (annotation pages) | Array | |
| `rights` field present if `license` was in source manifest | String URI | |
| `thumbnail` is an array | Array | |
| `metadata` array preserved with all entries | Array (same count) | |
| NC IIIF Commerce Extension properties present (`nc:activation_target_id`, etc.) | Object | |

**Overall manifest validity:** ☐ Pass / ☐ Fail

If any check fails, debug the bridging adapter against the specific failure mode.
Do not proceed to Phase 5 with an invalid manifest. Gate 4 is blocked until this
check passes.

---

## Phase 5 — Commerce Scoring

### Step 5.1 — Illustration Opportunity assessment

Evaluate the candidate against NC's Illustration Opportunity Doctrine for an initial
commerce tier estimate. This is a qualitative pre-scoring assessment, not the final
COS/CSM score (which is computed by the pipeline).

| Factor | Assessment |
|---|---|
| **Illustrator tier** | Is the creator a Priority Illustrator? (Buffon plates = Hired Artist / Daubenton; Sonnerat = Sonnerat) |
| **Subject specificity** | Is the subject uniquely identifiable as a specific Madagascar endemic taxon? |
| **Golden Age date** | Is the publication date within 1750–1900 (preferred Golden Age)? |
| **Rarity** | Is this illustration uncommon in the public domain landscape? |
| **Commercial context** | Nature print / scientific illustration / hand-colored plate? |
| **Resolution** | Is the image high-resolution (≥ 2000px) for premium product output? |

Expected commerce tier for a pre-1800 Buffon hand-colored lemur plate:
**MASTERWORK** (the highest NC CSM tier). If the pipeline scores this below FLAGSHIP,
flag for commerce formula review before proceeding with the pilot.

---

## Phase 6 — Asset Zero Activation

### Step 6.1 — Source record creation

Create the source_record for the Asset Zero candidate:

```sql
INSERT INTO source_records (
  source,
  external_id,
  external_url,
  raw_metadata,
  rights_status,
  created_at,
  updated_at
) VALUES (
  'bnf_gallica',
  'ark:/12148/{ark_id}',
  'https://gallica.bnf.fr/ark:/12148/{ark_id}',
  '{... raw OAI-PMH DC metadata ...}',
  'pending_verification',
  NOW(),
  NOW()
)
RETURNING id;
```

Record the `source_record.id`: _____________________

### Step 6.2 — Rights verification record

Create or update the media_rights record with the verified rights classification:

```sql
UPDATE media_rights
SET
  rights_status = 'verified_pd',   -- or 'verified_cc0'
  rights_evidence = '{
    "rights_source": "gallica_text_path",   -- or "iiif_uri_path" / "dc_rights_uri_path"
    "text_path_input": "{dc:rights text}",
    "text_path_match": "domaine public",
    "publication_date": "{dc:date}",
    "hr_review_type": "HR-GA-1",
    "hr_reviewer": "{reviewer name}",
    "hr_review_date": "{date}",
    "bnf_pd_authority_tier": 1,
    "eu_article_14_applicable": true,
    "bridgeman_doctrine_applicable": true,
    "governing_addendum": "gallica_rights_addendum_v1",
    "governing_decision": "DD-GALLICA-002"
  }',
  updated_at = NOW()
WHERE source_item_id = {source_item_id};
```

### Step 6.3 — Activation eligible promotion

After rights verification is recorded, promote the asset to `activation_eligible`:

```sql
UPDATE media_rights
SET
  rights_status = 'activation_eligible',
  updated_at = NOW()
WHERE source_item_id = {source_item_id}
  AND rights_status = 'verified_pd';
```

### Step 6.4 — Second-human review

Request second-human review of the Asset Zero candidate. The reviewer must:

1. Confirm the rights evidence in Step 6.2 is correct and complete
2. Visually confirm the image is a valid NC illustration opportunity (not a photograph,
   not a reproduction of a copyrighted work, not a map mistakenly classified as image)
3. Confirm the subject is an endemic Madagascar species per Phase 2
4. Sign off on activation_target promotion

Second-human reviewer sign-off:  
Name: _____________________  
Date: _____________________  
Signature: _____________________

### Step 6.5 — Activation target promotion

After second-human sign-off:

```sql
UPDATE activation_targets
SET
  status = 'activation_target',
  approved_by = '{second_human_name}',
  approved_at = NOW(),
  updated_at = NOW()
WHERE source_item_id = {source_item_id};
```

### Step 6.6 — Asset Zero ARK recording

Record the Asset Zero ARK in the source record's provenance:

```sql
UPDATE sources SET
  provenance = jsonb_set(
    jsonb_set(
      jsonb_set(provenance,
        '{asset_zero_ark}', to_jsonb('ark:/12148/{ark_id}'::text)),
      '{asset_zero_title}', to_jsonb('{dc:title}'::text)),
    '{asset_zero_date}', to_jsonb(NOW()::text)),
  updated_at = NOW()
WHERE source_id = 'bnf_gallica';
```

---

## Phase 7 — Gate 4 Closure

All items below must be checked before Gate 4 is declared closed and Gate 5
(Pilot Authorization) may open.

| # | Gate 4 closure requirement | Status |
|---|---|---|
| 7.1 | Phase 0 pre-flight all passed | ☐ |
| 7.2 | Asset Zero candidate identified and ARK documented | ☐ |
| 7.3 | Rights classification completed (ALLOWED result only) | ☐ |
| 7.4 | HR review completed (type and reviewer documented) | ☐ |
| 7.5 | Full-resolution image delivery confirmed (≥ 400px, watermark-free) | ☐ |
| 7.6 | IIIF 2.1 manifest fetched successfully | ☐ |
| 7.7 | IIIF 3.0 manifest produced by bridging adapter and validated | ☐ |
| 7.8 | Source record created in database | ☐ |
| 7.9 | Rights evidence recorded in media_rights | ☐ |
| 7.10 | Asset promoted to `activation_eligible` | ☐ |
| 7.11 | Second-human approval received (signed) | ☐ |
| 7.12 | Asset promoted to `activation_target` | ☐ |
| 7.13 | Asset Zero ARK recorded in source provenance | ☐ |

**Gate 4 closed by:**  
Name: _____________________  
Date: _____________________

**Asset Zero summary:**

| Field | Value |
|---|---|
| ARK identifier | |
| Title | |
| Creator | |
| Publication date | |
| Subject (species) | |
| Rights classification | |
| Rights evidence source | |
| IIIF 3.0 manifest valid | |
| Watermark-free confirmed | |
| Image dimensions | |
| Commerce tier estimate | |
| Second-human approver | |
| Gate 4 closed date | |

---

## Appendix A — Common ARK URL Patterns

```
# OAI-PMH record fetch
https://gallica.bnf.fr/services/OAIRecord?identifier=oai:bnf.fr:gallica/{id}&metadataPrefix=oai_dc

# IIIF manifest (2.1)
https://gallica.bnf.fr/iiif/ark:/12148/{id}/manifest.json

# IIIF full image
https://gallica.bnf.fr/iiif/ark:/12148/{id}/f1/full/full/0/native.jpg

# IIIF thumbnail (256px)
https://gallica.bnf.fr/iiif/ark:/12148/{id}/f1/256,/0/native.jpg

# Gallica item page
https://gallica.bnf.fr/ark:/12148/{id}

# SRU search
https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2&query={CQL}&maximumRecords=20&recordSchema=dc
```

## Appendix B — Known Buffon "Histoire Naturelle" ARK Patterns

Buffon's "Histoire Naturelle" volumes are typically catalogued at the volume level with
individual plate folios as sub-identifiers. The SRU query in Phase 1 Step 1.1 will
return specific ARKs. Do not attempt to construct ARKs manually — use the SRU query
results.

Typical structure:
- Work-level ARK: `ark:/12148/bpt6b{id}` (bibliothèque patrimoniale texte)
- Image-level ARK: `ark:/12148/btv1b{id}` (bibliothèque patrimoniale visuel)

For Asset Zero, prefer `btv1b` ARKs (image-level) over `bpt6b` ARKs (text/volume level)
as they map directly to individual illustration plates.

---

*Gallica Asset Zero Checklist v1.0 — 2026-06-08*
*Governing Decision: DD-GALLICA-002 Article 7 / Gate 4*
