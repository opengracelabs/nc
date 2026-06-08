# DD-GALLICA-001 — BnF Gallica Source Audit and Activation Framework

| Field | Value |
|---|---|
| **Decision ID** | DD-GALLICA-001 |
| **Type** | Source Audit + Activation Framework |
| **Status** | Draft — Pending Ratification |
| **Repository** | opengracelabs/nc |
| **Branch** | v0.4.0-collection-000001 |
| **Drafted** | 2026-06-08 |
| **Ratified** | — |
| **Director** | opengracelabs |
| **Second-Human Approval** | — |
| **Supersedes** | Nothing — first BnF Gallica governance document |
| **Governing Documents** | Institution Coverage Audit v1.0 · Europeana Rights Matrix v1.0 · MSC v1.2 · Standards Constitution v1.0 · Institution Factory Constitution v1.0 · FM Constitution v1.0 |

---

## Background

The Bibliothèque nationale de France (BnF) and its digital library Gallica constitute
the most important unactivated institution in NC's current portfolio. The Institution
Coverage Audit v1.0 (Article 11, MA-2) rated BnF Gallica a **Must Add** institution:
the single source that most directly fills NC's French and Francophone world geographic
gaps while simultaneously providing access to some of the most commercially compelling
pre-1900 natural history illustrations in existence — Buffon, Lacépède, Audebert,
Vieillot — held in a national library with generous public access policy.

This Decision is an **audit and activation framework**, not a simple production
authorization. Gallica presents five governance complexities absent from prior DDs:

1. **Rights field heterogeneity in French and URI form** — Gallica's OAI-PMH `dc:rights`
   field uses French-language text, generic phrases, and URIs interchangeably. The
   Europeana Rights Matrix applies to URI-form statements; Gallica requires a bespoke
   rights addendum for its institutional vocabulary.

2. **IIIF version gap** — Standards Constitution v1.0 Article 10 targets IIIF Presentation
   API 3.0 and Image API 3.0. Gallica provides IIIF Image API 2.1 (with Presentation
   API 2.1 manifests). A bridging specification is required.

3. **Public domain authority doctrine** — BnF's historical claim of reproduction rights
   over digitized PD works was partially addressed by EU Directive 2019/790 Article 14
   (France: transposed 2023). NC requires a formal public domain authority doctrine
   governing the extent of its reliance on this instrument and on the US Bridgeman rule.

4. **Audio and video collections** — Gallica holds approximately 300,000 phonorecord
   items and significant early film. These are Phase 3 media types under MSC v1.2
   Article 5.8. Their governance cannot proceed until Phase 2 is complete and Amendment
   P3-1 is ratified. This DD formally maps the Phase 3 landscape without authorizing it.

5. **No API key required** — Unlike Europeana and DPLA, Gallica's SRU and IIIF APIs
   are publicly accessible without authentication. This creates no activation barrier
   but removes the API-key-acquired precondition that bounded prior activations.

BnF Gallica is not registered in the NC `sources` table as of the date of this Decision.
This Decision, if ratified, authorizes an INSERT. No prior governance document has
authorized Gallica ingestion into the NC pipeline.

---

## Part I — Source Classification Audit

**F-1. Direct content institution.** BnF holds, digitizes, and serves its own collections
through first-party infrastructure. Gallica is BnF's public digital library — not a
third-party aggregator, not a discovery portal. All provenance chains terminate at BnF.
This is a one-tier provenance model: BnF → NC. The aggregator-source designation applied
to Europeana and DPLA does not apply here. Gallica is a **direct content institution**,
the same category as Rijksmuseum.

**F-2. Institutional scale and depth.** BnF holds 14 million digitized items on Gallica.
The commercially relevant subset for NC Phase 1 (image, map, photography, illustration)
is estimated at several hundred thousand PD-eligible items. The Buffon natural history
collection alone contains tens of thousands of plates from "Histoire Naturelle, générale
et particulière" (1749-1804) — 36 volumes, roughly 3,200 hand-colored plates. No other
institution in NC's portfolio provides access to Buffon at this scale.

**F-3. Priority illustrator coverage.** Gallica holds primary publication-quality
material for illustrators on NC's Priority Illustrator Registry. The BnF's direct
institutional relationship to the French natural history tradition is unmatched:

| Priority Illustrator | Gallica holding | Coverage quality |
|---|---|---|
| Pierre-Joseph Redouté | "Les Roses" (1817–1824), "Les Liliacées" (1802–1816) | Definitive — original plates |
| Maria Sibylla Merian | Editions of "Metamorphosis Insectorum" via BnF | Good — period editions |
| Pierre Sonnerat | "Voyage à la Nouvelle Guinée" (1776), "Voyage aux Indes" (1782) | Strong — covers Madagascar/Indian Ocean |
| Georges-Louis Buffon | "Histoire Naturelle" (1749–1804) — 36 volumes | Definitive — full run |
| Nicolas Robert | Botanical illustrations for Louis XIV — primary national collection | Strong |

Redouté and Buffon are NC priority or near-priority illustrators whose primary
institutional home is the BnF. No other NC-accessible source provides this coverage.

**F-4. Classification ruling.** BnF Gallica is classified as a **Tier 1 Core direct
content institution** (Institution Coverage Audit v1.0 Article 11 MA-2). It is a
Wave 3 onboarding target. Its institutional category is identical to Rijksmuseum,
not to Europeana or DPLA.

---

## Part II — Rights Strategy Audit

**F-5. Gallica rights field structure.** Gallica exposes rights data via three surfaces:

- **OAI-PMH `dc:rights`**: Free text (French or English) or Rights Statement URI.
  The primary rights metadata surface for bulk metadata harvest. Values are
  heterogeneous and not standardized across the collection.

- **IIIF Presentation API 2.1 manifest `@metadata`**: A key-value array in the JSON
  manifest. The `rights` field in IIIF 2.1 is `license` (a string URI). Present and
  reliable for most IIIF-served Gallica items.

- **Gallica item page `dc:rights`**: HTML metadata and JSON-LD structured data at the
  item page. Cross-check surface for verification.

**F-6. Gallica rights vocabulary.** BnF uses the following rights designations in
`dc:rights`. These are not governed by the Europeana Rights Matrix v1.0 (which governs
URI-form statements only). A Gallica Rights Addendum is required:

| Gallica rights value (case-insensitive) | NC classification | Basis |
|---|---|---|
| `"domaine public"` | ALLOWED → PD | BnF institutional PD declaration; treated as PDM-equivalent |
| `"public domain"` | ALLOWED → PD | Same |
| `"libre de réutilisation"` | ALLOWED → PD/CC0 | BnF free reuse declaration; commercial use included |
| `"usage commercial autorisé"` | ALLOWED → PD | Explicit commercial permission on PD work |
| CC0 URI | ALLOWED → CC0 | Europeana Rights Matrix Table 1A rule 1 |
| PDM URI | ALLOWED → PD | Europeana Rights Matrix Table 1A rule 2 |
| NoC-US URI | ALLOWED → PD | Europeana Rights Matrix Table 1A rule 3 |
| `"usage non-commercial uniquement"` | BLOCKED | Non-commercial restriction; NC hard gate |
| `"usage non commercial"` | BLOCKED | Same; alternate French spelling |
| `"droits réservés"` | BLOCKED | Active copyright or institutional restriction |
| `"tous droits réservés"` | BLOCKED | Active copyright |
| `"domaine public revisité"` | BLOCKED | Obsolete BnF reproduction rights claim; see F-8 |
| Any InC / NoC-NC URI | BLOCKED | Europeana Rights Matrix Part II |
| Missing / absent `dc:rights` | BLOCKED | No rights determination possible |
| Unrecognized French text | BLOCKED (pending review) | Cannot classify; treat as absent |

The `IIIF license` field URI, when present, supersedes the `dc:rights` text value.
If a IIIF manifest provides a classifiable URI, the URI path (Europeana Rights Matrix
v1.0) applies. `dc:rights` text is the fallback when the IIIF `license` field is absent.

**F-7. BnF metadata rights separation.** BnF asserts CC-BY licensing on BnF-created
metadata (catalog records, finding aids, indexing terms). This CC-BY assertion applies
to the metadata, not to the image. The metadata CC-BY requirement means NC must
attribute BnF in metadata displays. It does not affect the rights status of the
underlying image. The two layers must not be confused:

```
BnF catalog record  →  CC-BY (metadata attribution required)
Digitized image      →  Governed by dc:rights / IIIF license field (separate determination)
```

**F-8. The "domaine public revisité" problem.** BnF historically claimed that its
photographic reproductions of 2D PD artworks constituted new copyrightable works
("domaine public revisité"). This claim has been invalidated in the EU by Directive
2019/790 Article 14 (faithful 2D reproductions of PD works are not copyrightable)
and in the US by *Bridgeman Art Library v. Corel Corp* (SDNY/EDNY 1999). Gallica
items still bearing "domaine public revisité" rights text are therefore governed by
the Article 14 / Bridgeman doctrine (see F-10 and F-11). This DD formally classifies
"domaine public revisité" as BLOCKED at the pre-ingestion filter pending individual
item review — not because the claim is valid, but because the pre-ingestion worker
cannot deterministically resolve it without human review. The Gallica Rights Addendum
(Article 2) defines the resolution path.

**F-9. Pre-1928 date-based analysis.** For items where `dc:rights` is absent or
unclassifiable, a date-based PD analysis is available if the publication date is
determinable from `dc:date`. Works published before 1 January 1928 in the US
(or published outside the US without compliance with US formalities before the Berne
retroactivity date) are in the public domain under US copyright law regardless of
French law. This date-based path may only be used as a secondary confirmation mechanism
for items that have already passed a `dc:rights` classification. It may not substitute
for a rights determination on items with BLOCKED rights text.

---

## Part III — Public Domain Authority Audit

**F-10. EU Directive 2019/790 Article 14 reliance.** EU Directive 2019/790 ("Digital
Single Market Copyright Directive") Article 14 provides: works of visual art that are
in the public domain may not generate new copyright or related rights protection from
acts of reproduction, unless the reproduced material is an original creative work in
its own right. France transposed this directive into national law effective 2023.

For NC's purposes, Article 14 establishes that BnF cannot claim new copyright over
faithful 2D reproductions (scans, photographs) of PD works in its collection. The
Gallica digitized images of PD plates, prints, illustrations, and photographs are
therefore not copyrighted by BnF regardless of historical "domaine public revisité"
practice.

NC formally relies on Article 14 as a negative rights clearance instrument for all
Gallica-sourced digitized reproductions of 2D PD works. This reliance is subject to
two conditions:

- The underlying work must be PD (pre-1928 under US law, or life+70 confirmed)
- The reproduction must be a faithful scan / photograph of the 2D original (not a
  creative editorial transformation that would itself constitute original expression)

**F-11. Bridgeman doctrine (US commerce jurisdiction).** *Bridgeman Art Library v.
Corel Corp*, 36 F.Supp.2d 191 (SDNY 1999), affirmed on reconsideration 25 F.Supp.2d
421 (SDNY 1998): faithful photographic reproductions of two-dimensional public domain
artworks are not independently copyrightable under US copyright law, because they
lack originality. NC's primary commerce jurisdiction is the United States. The Bridgeman
doctrine applies as the US-law equivalent of Article 14.

NC's reliance on Bridgeman is not new — it is implicit in NC's broader PD commerce
posture. This DD makes it explicit for Gallica specifically, because BnF is the
institution most associated with the "domaine public revisité" claim.

**F-12. BnF as public domain authority.** BnF's institutional PD declarations
("domaine public", "libre de réutilisation") are treated as the French equivalent of
the Public Domain Mark (PDM) under NC's rights framework, with the following conditions:

- The work's publication date must be consistent with a PD determination (generally
  pre-1928 for US commerce purposes)
- The NC human reviewer must confirm the BnF PD declaration is not a generic label
  applied to a work with contested publication history
- BnF is a recognized NC public domain authority for the purposes of confirmation
  (HR-4 equivalent): a BnF "domaine public" declaration on a pre-1928 work with a
  named author reduces the human verification burden to date confirmation only

This authority status is conditional on the work's publication date. A BnF "domaine
public" declaration on a post-1927 work does not constitute adequate rights evidence.

---

## Part IV — IIIF Governance Audit

**F-13. Gallica IIIF infrastructure.** Gallica provides:

- **IIIF Image API 2.1** via `https://gallica.bnf.fr/iiif/ark:/12148/{id}/f{n}/` — full
  resolution available at `/full/full/0/native.jpg`. Image tile service available.
  High resolution (frequently 3000+ px on longest side) confirmed for most digitized items.

- **IIIF Presentation API 2.1 manifest** via
  `https://gallica.bnf.fr/iiif/ark:/12148/{id}/manifest.json` — available for multi-page
  documents (books, albums). Single-image items may not have a Presentation API manifest;
  they use only the Image API.

**F-14. IIIF version gap.** Standards Constitution v1.0 Article 10 governs IIIF
Presentation API 3.0 and Image API 3.0 as the NC delivery target. Gallica provides
IIIF 2.1. The practical differences for NC's Phase 1 image pipeline are limited:

| Capability | IIIF 2.1 (Gallica) | IIIF 3.0 (NC target) | Impact |
|---|---|---|---|
| Image tile URL structure | `/iiif/{id}/f{n}/{region}/{size}/{rotation}/{quality}.{format}` | Identical | None |
| `info.json` structure | 2.1 schema | 3.0 schema (minor diffs) | Adapter field mapping |
| Manifest `@context` | `http://iiif.io/api/presentation/2/context.json` | `http://iiif.io/api/presentation/3/context.json` | Bridging adapter |
| Rights field in manifest | `license` (string URI) | `rights` (string URI) | Field rename only |
| `metadata` array | Key-value pairs | Same structure | None |
| `thumbnail` | Object reference | Array of objects | Minor bridging |
| Compliance levels | Level 0/1/2 | Level 0/1/2 | None |

For NC's primary use (image delivery via Image API, rights extraction from `license`
field), the 2.1 → 3.0 gap is a field-name bridging issue, not a capability gap. The
image URL structure is identical. Full-resolution delivery (`/full/full/`) works
identically across both versions. Standards Amendment SA-3 (Coverage Audit, Article 16)
or a dedicated IIIF bridging specification must address this before the IIIF manifest
surface is used for `source_record.schema_standard = 'gallica_iiif_2.1'`.

**F-15. Watermark policy.** Gallica provides watermark-free images through the IIIF
Image API at full resolution. Watermarks (if any) appear only on Gallica's own website
at reduced resolution. For NC's print product pipeline, the IIIF `/full/full/0/native.jpg`
endpoint must be confirmed to be watermark-free during Asset Zero validation. This is
a non-blocking pre-activation check, not a governance barrier.

---

## Part V — Audio and Video Governance Audit

**F-16. Gallica audio collections.** Gallica holds approximately 300,000 audio items
including:

- **Cylinder phonorecords** (~1890–1910): wax cylinder recordings from early commercial
  recording era. Extremely early; many are ethnographic field recordings.
- **78rpm shellac records** (~1900–1950): commercial recordings including French popular
  music, classical performances, opera.
- **Early LPs and radio recordings** (~1950–1970): predominantly in copyright under
  French law and protected in the US under the Music Modernization Act (MMA, 2018).

**Rights under US law for sound recordings (MMA analysis):**
The Music Modernization Act (17 U.S.C. §1401) governs pre-1972 sound recordings. Key
provisions relevant to Gallica:

| Recording era | US protection status | NC eligibility |
|---|---|---|
| Published in US before 1923 | PD as of January 1, 2022 | Potentially eligible — but few Gallica items qualify |
| Published anywhere before 1923 (non-US) | Protected until 2067 under MMA §1401(a)(2) | BLOCKED for NC commerce |
| Published anywhere 1923–1946 | Protected until 100 years after publication | BLOCKED for most (would require 2046+ clearance) |
| Published 1947–1956 | Protected until 110 years after publication | BLOCKED |

The practical impact: virtually all Gallica phonorecord holdings are BLOCKED for NC
Phase 3 commerce under current US law. Pre-1923 US publications are a narrow exception.
French phonorecords published in France (not the US) before 1923 receive US protection
until 2067 under the MMA.

**F-17. Gallica film and video collections.** Gallica holds early cinema and documentary
film including:

- **Lumière Brothers films** (~1895–1905): among the earliest motion pictures. Rights
  complex: some arguably PD under US law (published before 1928 abroad, but US
  formalities compliance is contested).
- **Early silent films** (~1905–1930): French and international productions.
- **Documentary and educational films** (~1930–1960): predominantly in copyright.

Film rights are even more complex than sound recording rights because film involves
multiple rights layers: screenplay, musical score, performance, and the film itself.
Silent films from before 1928 may qualify as PD under US law, but each requires
individual rights analysis.

**F-18. Phase 3 constitutional gate.** MSC v1.2 Article 5.8 governs the activation
sequence. Audio (Phase 3) requires:

```
Phase 1 complete (image, map, photography, poster all active with activated source_items)
  → Amendment P2-1 ratified
    → book AND ebook active with activated source_items
      → audiobook active with at least one activated source_item
        → Amendment P3-1 ratified
          → audio MAY be activated
            → [then film follows audio]
```

NC has not completed Phase 1. Activating any Phase 3 audio or film type from Gallica
before this prerequisite chain is satisfied would be a constitutional violation under
MSC v1.2 Article 5.8. This DD formally records the Phase 3 landscape for planning
purposes but cannot and does not authorize Phase 3 ingestion.

---

## Decision

### Article 1 — Source Classification Authorization

BnF Gallica is classified as a **Tier 1 Core direct content institution** in NC's
institutional taxonomy. This is the first and authoritative governance classification
for Gallica as a NC source.

**(a)** Gallica is not an aggregator. The aggregator-source designation of Europeana
(DD-EUR-001) and DPLA (DD-DPLA-001) does not apply. The provenance model is one-tier:
BnF → NC.

**(b)** This Decision authorizes an INSERT into the `sources` table creating a new
record for `source_id = 'bnf_gallica'`. The `governance_state = 'active'` designation
is authorized.

**(c)** Gallica is a Wave 3 institution per Institution Coverage Audit v1.0 Article 17.
This DD initiates Wave 3 onboarding for Gallica.

---

### Article 2 — Gallica Rights Strategy and Rights Addendum

The **Europeana Rights Matrix v1.0** governs all URI-form rights statements encountered
in Gallica metadata. This DD additionally defines the **Gallica Rights Addendum v1**,
which extends the Matrix to cover Gallica's institutional text vocabulary and the
French law instruments applicable to BnF materials.

#### 2.1 URI Path (Primary)

When a Gallica item's IIIF manifest `license` field or `dc:rights` field contains a
URI classifiable under the Europeana Rights Matrix v1.0, that Matrix applies without
modification. The IIIF manifest `license` field URI supersedes `dc:rights` text when
both are present.

#### 2.2 Gallica Rights Addendum v1 — Institutional Text Path

When no classifiable URI is present, the following table governs classification of
Gallica `dc:rights` text values:

**Table GA-1A — ALLOWED (Institutional Text)**

| Gallica text pattern (case-insensitive) | NC rights_status target | Human review rule | Notes |
|---|---|---|---|
| `"domaine public"` | `verified_pd` (after confirmation) | HR-GA-1: date confirmation | PDM-equivalent. Confirm pub date pre-1928 |
| `"public domain"` | `verified_pd` (after confirmation) | HR-GA-1 | Same |
| `"libre de réutilisation"` | `verified_pd` or `verified_cc0` | HR-GA-2: scope confirmation | Free reuse including commercial; treat as PDM or CC0 |
| `"usage commercial autorisé"` | `verified_pd` (after confirmation) | HR-GA-1 | Explicit commercial permission; confirm pub date |

**Table GA-1B — REVIEW REQUIRED (Institutional Text)**

| Gallica text pattern | NC classification | Review rule |
|---|---|---|
| `"domaine public revisité"` | REVIEW REQUIRED | HR-GA-3: Article 14 / Bridgeman assessment |
| Unrecognized French PD-adjacent text | REVIEW REQUIRED | HR-GA-4: manual classification |

"Domaine public revisité" items in the review queue must be assessed against:
(i) Is the work a faithful 2D reproduction of a pre-1928 PD work?
(ii) Does EU Directive 2019/790 Article 14 apply (transposed France 2023)?
(iii) Does *Bridgeman Art Library v. Corel Corp* (SDNY 1999) apply?
If (i) through (iii) all resolve affirmatively: set `rights_status = 'verified_pd'`.
If any fails: set `rights_status = 'ineligible'`.

**Table GA-2 — BLOCKED (Institutional Text)**

| Gallica text pattern | Block reason |
|---|---|
| `"usage non-commercial uniquement"` | NC commercial restriction — permanent block |
| `"usage non commercial"` | Same |
| `"droits réservés"` | Active rights reservation |
| `"tous droits réservés"` | All rights reserved — active copyright |
| `"under copyright"` / `"en cours de droits"` | Active copyright |
| Missing / absent `dc:rights` AND absent IIIF `license` | No rights determination possible |
| Unrecognized text not matching Table GA-1A or GA-1B | Unknown status → BLOCKED pending classification |

**Table GA-3 — Metadata Rights Separation**

BnF's CC-BY assertion on catalog metadata does not affect image rights. All Gallica
ingestion workers must treat metadata rights and image rights as independent fields.
A CC-BY `dc:rights` value on a metadata record does not constitute image rights evidence.
The image rights field is determined separately from the metadata rights field.

#### 2.3 Combined Rights Determination Priority

```
1. IIIF manifest `license` field (URI)
   → If present and classifiable: apply Europeana Rights Matrix v1.0 (URI path)
   → If present but BLOCKED: reject at pre-ingestion filter

2. dc:rights URI (from OAI-PMH)
   → If present and classifiable: apply Europeana Rights Matrix v1.0 (URI path)

3. dc:rights text (from OAI-PMH)
   → Apply Gallica Rights Addendum v1 Table GA-1A, GA-1B, or GA-2

4. Both fields absent
   → BLOCKED (Table GA-2 last row)
```

#### 2.4 FM Exclusion (Permanent)

FM-4 applies permanently to all Gallica rights determinations. No FM output may
influence any `media_rights` record for any Gallica-sourced asset. This is permanent
and cannot be modified by this Decision or any amendment.

---

### Article 3 — Public Domain Authority Doctrine

#### 3.1 EU Directive 2019/790 Article 14 Reliance

NC formally relies on EU Directive 2019/790 Article 14, as transposed into French law
(effective 2023), as a negative rights clearance instrument for Gallica-sourced
digitized reproductions of 2D PD works.

This reliance means: for a faithful scan or photographic reproduction of a 2D work
that is itself in the public domain, NC does not recognize any BnF reproduction rights
claim as a bar to NC commerce.

This reliance applies only when both of the following are confirmed:
- (a) The underlying original work is in the public domain under US copyright law
- (b) The Gallica image is a faithful reproduction of the 2D original — not a
  creative editorial transformation (cropping, colorization, composite) that would
  constitute original expression

If condition (b) cannot be confirmed from the available metadata and image, the asset
must receive a REVIEW REQUIRED designation and enter the HR-GA-3 workflow.

#### 3.2 Bridgeman Doctrine Reliance (US Commerce Jurisdiction)

NC formally relies on *Bridgeman Art Library v. Corel Corp*, 36 F.Supp.2d 191 (SDNY
1999), as the US copyright law authority for the same principle: faithful photographic
reproductions of 2D PD works are not independently copyrightable in the US.

NC's primary commerce jurisdiction is the United States. The Bridgeman doctrine is
the operative legal basis for NC's treatment of Gallica reproductions as PD without
independent BnF copyright. Bridgeman doctrine reliance is not conditional on any
French law instrument — it applies as US law independently.

#### 3.3 BnF Public Domain Authority Status

BnF is recognized as a **Tier 1 NC public domain authority** for pre-1928 works in
its collection, with the following governance parameters:

**(a)** A BnF "domaine public" declaration on a work with a confirmed publication date
before 1 January 1928 reduces the human reviewer's confirmation burden to date
verification only. Independent copyright analysis is not required for such items.

**(b)** A BnF "domaine public" declaration on a work where the publication date is
absent, uncertain, or post-1927 does NOT reduce the verification burden. An independent
PD analysis per Europeana Rights Matrix Rule HR-2c is required.

**(c)** BnF's authority status may be suspended by Director Decision if evidence
emerges that BnF is systematically misapplying "domaine public" to works that are not
PD under US law. This DD does not establish unconditional trust.

---

### Article 4 — IIIF Governance

#### 4.1 IIIF 2.1 Bridging Authorization

NC authorizes the use of Gallica's IIIF Image API 2.1 and Presentation API 2.1 for
the pilot ingestion, subject to a bridging adapter that maps 2.1 manifest fields to
NC's IIIF 3.0 target:

| IIIF 2.1 field | IIIF 3.0 target field | Bridging rule |
|---|---|---|
| `@context` (2.1 URL) | `@context` (3.0 URL) | Replace context URL; preserve content |
| `license` (string URI) | `rights` (string URI) | Field rename |
| `@id` | `id` | Field rename |
| `@type: sc:Manifest` | `type: Manifest` | Remove `@`, remove `sc:` prefix |
| `sequences[0].canvases` | `items` (Canvases) | Structural uplift |
| `thumbnail` (object) | `thumbnail` (array of objects) | Wrap in array |
| `metadata` (key-value array) | `metadata` (label-value array) | Same structure |

The Gallica IIIF 2.1 → 3.0 bridging adapter must be implemented before the first
ingestion run. The adapter specification must be documented as a governed artifact in
`docs/standards/gallica_iiif_bridge_v1.md` before Gate 3 of Article 12.

#### 4.2 Image API Delivery Standard

The Gallica IIIF Image API 2.1 endpoint is authorized as the primary image delivery
mechanism. The full-resolution request format is:

```
https://gallica.bnf.fr/iiif/ark:/12148/{ark_id}/f{page}/full/full/0/native.jpg
```

Or equivalently:
```
https://gallica.bnf.fr/iiif/ark:/12148/{ark_id}/f{page}/full/!{maxdim},{maxdim}/0/native.jpg
```

For single-image items (not paginated books), `f1` is the page identifier.
The target format is `native.jpg` or `native.tif` where available. Watermark-free
delivery at full resolution must be confirmed during Asset Zero validation.

MSC v1.2 Article 29.2(d) minimum dimension (400px on shortest side) applies.

#### 4.3 Manifest Coverage

Not all Gallica items have IIIF Presentation API 2.1 manifests. Items without a
manifest may still be ingested using the Image API only. The absence of a Presentation
API manifest does not block ingestion — it means `media_file.iiif_manifest_url` is
null for that item. The image delivery URL remains available.

---

### Article 5 — Audio and Video Exclusion

**(a)** This Decision authorizes **Phase 1 media types only**: image, map, photography,
illustration. Audio and film (Phase 3 under MSC v1.2 Article 5.8) are formally excluded
from this DD's activation scope.

**(b)** The constitutional gate for Phase 3 (audio, film) activation from any source
requires completion of Phase 1, Amendment P2-1 ratification, book/ebook activation,
audiobook activation, and Amendment P3-1 ratification. NC has not completed Phase 1.
No Phase 3 activation can proceed under this DD or any amendment to it.

**(c)** The phonorecord landscape documented in F-16 is formally recorded for
pre-planning. The Music Modernization Act analysis in F-16 establishes that most
Gallica phonorecords are BLOCKED for NC commerce under current US law. This finding
informs future Phase 3 governance without authorizing any Phase 3 action now.

**(d)** Film holdings documented in F-17 are likewise recorded for pre-planning.
Early silent film rights analysis may proceed as an FM advisory research task
(`film_rights_landscape_advisory` use case) without connecting to any `media_rights`
or pipeline record.

**(e)** This exclusion may not be lifted by Director Decision alone. Lifting it requires
completion of the full MSC v1.2 Phase 3 prerequisite chain and ratification of
Amendment P3-1 as a constitutional amendment.

---

### Article 6 — API Surface Authorization

The following Gallica API surfaces are authorized for the pilot ingestion:

| Surface | Endpoint | Use | Status |
|---|---|---|---|
| OAI-PMH | `https://gallica.bnf.fr/services/OAIRecord` | Metadata harvest (DC format) | Authorized |
| IIIF Image API 2.1 | `https://gallica.bnf.fr/iiif/ark:/12148/{id}/f{n}/` | Image delivery | Authorized (with bridging) |
| IIIF Presentation API 2.1 | `https://gallica.bnf.fr/iiif/ark:/12148/{id}/manifest.json` | Manifest for paginated works | Authorized (with bridging) |
| SRU Search | `https://gallica.bnf.fr/SRU` | Collection search and scoping | Authorized (scoping only during pilot) |

The following surfaces are **not authorized** under this Decision:

| Surface | Reason |
|---|---|
| Gallica bulk export / data dumps | Not evaluated; requires separate Director Decision |
| IIIF Content Search API | Not evaluated; requires separate Decision |
| BnF catalogue BnF JSON API | Not evaluated; requires separate Decision |
| INA (Institut national de l'audiovisuel) feeds | Phase 3; excluded per Article 5 |
| BnF UNIMARC direct | OAI-PMH DC is the authorized metadata path; UNIMARC requires SA-3 mapping |

Authentication: No API key is required for Gallica SRU, OAI-PMH, or IIIF. NC does not
need to register an API key as a precondition for production ingestion.

---

### Article 7 — Gallica Metadata Field Mapping

The Gallica adapter maps OAI-PMH Dublin Core fields to NC's `source_record` layer:

| OAI-PMH / IIIF field | NC field | Notes |
|---|---|---|
| `dc:identifier` (ARK URI) | `source_item.provider_item_id` | ARK format `ark:/12148/{id}` |
| `dc:title` | `source_record.title` | First value if multiple |
| `dc:creator` | `source_record.creator` | Array; join with "; " |
| `dc:date` | `source_record.date_display` | Raw date string |
| `dc:description` | `source_record.description` | First value if multiple |
| `dc:subject` | `source_record.subjects` | Array |
| `dc:type` | `source_record.media_type_raw` | Normalize to NC media type |
| `dc:format` | `source_record.format_raw` | MIME type or format string |
| `dc:rights` | `source_record.rights_raw` + rights classification | Full text pre-classification |
| `dc:publisher` | `source_record.publisher` | BnF for most items |
| `dc:source` | `source_record.source_provenance` | Originating collection |
| `dc:language` | `source_record.language` | ISO 639-1 if determinable |
| `dc:coverage` | `source_record.geographic_coverage` | Geographic scope text |
| `dc:relation` | `source_record.relation` | Part-of, version, etc. |
| `oai:identifier` | `source_record.oai_identifier` | OAI-PMH record ID |
| IIIF `license` | `media_rights.rights_statement_uri` | URI path primary |
| IIIF Image API URL | `media_file.source_url` | Full resolution target |
| IIIF Manifest URL | `media_file.iiif_manifest_url` | Null if absent |

The ARK identifier scheme (`ark:/12148/`) is NC's canonical item identifier for Gallica.
The `source_item.provider_item_id` format is `ark:/12148/{id}` (full ARK, not abbreviated).
This identifier format enables direct URL construction for both IIIF and item page retrieval.

---

### Article 8 — Source Registry Authorization

BnF Gallica is not currently registered in the `sources` table. This Decision authorizes
an **INSERT** to create a new record. The INSERT must be executed as a single authorized
statement.

| Amendment | Field | Value |
|---|---|---|
| GAL-SR-1 | `source_id` | `'bnf_gallica'` |
| GAL-SR-2 | `name` | `'Gallica — Bibliothèque nationale de France'` |
| GAL-SR-3 | `institution` | `'Bibliothèque nationale de France'` |
| GAL-SR-4 | `base_url` | `'https://gallica.bnf.fr'` |
| GAL-SR-5 | `fetch_strategy` | `'api'` |
| GAL-SR-6 | `auth_type` | `'none'` |
| GAL-SR-7 | `priority` | `7` |
| GAL-SR-8 | `entity_types` | `ARRAY['image', 'map', 'photography', 'illustration']` |
| GAL-SR-9 | `standards` | `ARRAY['dc', 'oai_pmh', 'iiif_2.1']` |
| GAL-SR-10 | `governance_state` | `'active'` |
| GAL-SR-11 | `operational_status` | `'unavailable'` |
| GAL-SR-12 | `status` | `'active'` |
| GAL-SR-13 | `config` | See target JSON below |

The `sources.config` target state at INSERT:

```json
{
  "sru_endpoint": "https://gallica.bnf.fr/SRU",
  "oai_endpoint": "https://gallica.bnf.fr/services/OAIRecord",
  "iiif_image_base": "https://gallica.bnf.fr/iiif",
  "iiif_version": "2.1",
  "iiif_bridging_required": true,
  "auth_type": "none",
  "identifier_scheme": "ark",
  "identifier_prefix": "ark:/12148/",
  "rate_limit": {
    "requests_per_second": 2,
    "burst": 5,
    "timeout_seconds": 45
  },
  "rights_strategy": "gallica_rights_addendum_v1",
  "rights_field_iiif": "manifest.license",
  "rights_field_oai": "dc:rights",
  "rights_determination_priority": ["iiif_license_uri", "dc_rights_uri", "dc_rights_text"],
  "source_role": "direct_institution",
  "aggregation_tier": "one_tier",
  "metadata_standard": "dc_via_oai_pmh",
  "phase_1_only": true,
  "audio_video_excluded": true,
  "eu_article_14_reliance": true,
  "bridgeman_doctrine_reliance": true,
  "bnf_pd_authority_tier": 1,
  "completeness_required_fields": [
    "dc:title", "dc:identifier", "dc:date", "dc:rights"
  ],
  "rights_filter": {
    "mode": "pre_ingestion",
    "primary_authority": "europeana_rights_matrix_v1",
    "secondary_authority": "gallica_rights_addendum_v1",
    "allowed_text_patterns": [
      "domaine public",
      "public domain",
      "libre de réutilisation",
      "usage commercial autorisé"
    ],
    "review_required_patterns": [
      "domaine public revisité"
    ],
    "blocked_text_patterns": [
      "usage non-commercial",
      "usage non commercial",
      "droits réservés",
      "tous droits réservés",
      "under copyright",
      "en cours de droits"
    ],
    "filter_mode": "strict"
  }
}
```

---

### Article 9 — Pilot Scope

This Decision authorizes a **scoped pilot** for Madagascar only.

**(a) Rationale for Madagascar.** Madagascar represents three simultaneous NC priorities:

1. **Africa geographic gap closure.** Madagascar is the highest-tourism, highest-UNESCO
   value African location for which NC currently has zero source content. With five UNESCO
   World Heritage Sites (Tsingy de Bemaraha, Rainforests of Atsinanana, and three others),
   Madagascar is a commercially significant place NC cannot serve from its current portfolio.

2. **BnF collection strength.** The French colonial-era scientific relationship with
   Madagascar is exceptionally well-documented in BnF. Commerson (Banks-voyage botanist),
   Sonthonnax, Audebert, and Vieillot produced natural history illustrations of Madagascar's
   endemic fauna directly held in BnF. Buffon's "Histoire Naturelle" covers lemurs, fossas,
   and aye-ayes. BnF maps from the French colonial administration cover the island's
   coastline, interior regions, and expedition routes in detail unavailable elsewhere.

3. **Priority illustrator activation.** The Madagascar pilot validates the Buffon and
   Redouté collection pipelines — two Priority Illustrator Registry entries — in a
   geographically meaningful context.

**(b) Place association.** All assets ingested under this Decision must be associated
with Madagascar (`places.geonames_id = 1062947`, Wikidata Q1019). Assets returned by
queries that cannot be associated with Madagascar must be discarded, not queued for a
different place. Place expansion requires DD-GALLICA-002.

**(c) Pilot batch size.** The first ingestion batch is capped at **50 assets**. This
is the most conservative pilot cap to date, reflecting:
- Higher rights validation burden (bilingual text classification + Article 14 / Bridgeman
  assessment for any "domaine public revisité" items)
- IIIF 2.1 bridging adapter to be confirmed in production for the first time
- Asset Zero validation of watermark-free delivery at full resolution
- New OAI-PMH harvest pathway untested in NC pipeline

**(d) Query scope.** The pilot SRU queries:

```
Primary (natural history):
  https://gallica.bnf.fr/SRU
  ?operation=searchRetrieve
  &query=gallica.subject all "Madagascar" AND gallica.typedoc all "image"
  &recordSchema=oai_dc
  &maximumRecords=50

Secondary (cartographic):
  query=gallica.subject all "Madagascar" AND gallica.typedoc all "carte"
  &maximumRecords=20
```

Both queries are subject to pre-ingestion rights classification. Only assets with
ALLOWED or REVIEW REQUIRED rights proceed to `source_record` creation.

**(e) Rights path breakdown.** Within the 50-asset cap:
- URI ALLOWED (CC0, PDM, NoC-US): proceed with standard confirmation
- Text ALLOWED ("domaine public" + date confirmation): proceed with HR-GA-1 check
- URI REVIEW REQUIRED (NoC-CR, NoC-OKLR, NKC): sub-cap 10
- Text REVIEW REQUIRED ("domaine public revisité" + Article 14 / Bridgeman): sub-cap 5
- BLOCKED: rejected, logged, not counted

---

### Article 10 — Asset Zero Requirements

Asset Zero for Gallica must satisfy the following criteria:

**(a) Subject.** The Asset Zero candidate must be a natural history illustration of a
Madagascar endemic species — lemur, aye-aye, fossa, or equivalent — from a pre-1800
French natural history publication. The ring-tailed lemur ("maki", *Lemur catta*) and
ruffed lemur ("maki vari", *Varecia variegata*) from Buffon's "Histoire Naturelle
(Suppléments)" are the priority candidates.

**(b) Source publication.** Candidate publications:
- Buffon, "Histoire Naturelle, générale et particulière" (1749–1804, with supplements)
  — lemurs, fossas, and other Madagascar megafauna
- Sonnerat, "Voyage aux Indes orientales et à la Chine" (1782) — natural history of
  Madagascar and Indian Ocean
- Audebert and Vieillot, "Oiseaux Dorés" (1802) — Madagascar endemic birds

**(c) Rights profile.** Asset Zero must carry:
- A publication date of 1800 or earlier (comfortably pre-1928 under any US copyright rule)
- A rights designation of "domaine public" (text path) or PDM URI (URI path)
- No "domaine public revisité" text (the pilot's first validated asset should be clean)

**(d) IIIF delivery confirmation.** Asset Zero must validate:
- Full-resolution IIIF Image API access at the `/full/full/0/native.jpg` endpoint
- Image dimensions ≥ 400px on shortest side (MSC v1.2 Article 29.2(d) minimum)
- Watermark-free delivery at full resolution
- IIIF 2.1 → 3.0 bridging adapter producing a valid IIIF 3.0 manifest

**(e) Commerce eligibility.** Asset Zero must reach `activation_eligible` status with
a COS calculated and CSM tier assigned before the pilot is considered validated.

**(f) Asset Zero is not production.** Asset Zero is a governance validation exercise.
It does not constitute a production ingestion run. The 50-asset pilot cap begins with
the first production ingestion batch, not with the Asset Zero validation.

---

### Article 11 — Standards Constitution Amendments Required

The following Standards Constitution amendments are required before or concurrent with
the first production ingestion run:

**SA-3 (Coverage Audit, previously called for):** BnF Gallica API Profile as Extension
to Standards Constitution v1.0. This amendment must formally register:
- OAI-PMH Dublin Core → NC `source_record` field mapping
- IIIF 2.1 → 3.0 bridging specification
- ARK identifier scheme as a governed `provider_item_id` format
- BnF-specific rights vocabulary (Gallica Rights Addendum v1) as a governed extension
  to the Europeana Rights Matrix

**SA-4 (DD-RIJKSMUSEUM-001):** IIIF Presentation API standards amendment. If SA-4 has
been ratified before this DD, SA-3 may be narrowed to cover only the Gallica-specific
elements (OAI-PMH, ARK, rights addendum). If SA-4 has not been ratified, SA-3 must
cover both the IIIF version bridging and the Gallica-specific elements.

**UNIMARC acknowledgment (SA-6):** BnF's native catalog format is UNIMARC. NC does not
adopt UNIMARC internally — OAI-PMH DC is the production metadata path. However, the
Standards Constitution's covered-standards list (Article 1.2) should acknowledge
UNIMARC as a recognized source standard for BnF, even if NC maps from it only via the
DC export layer. SA-6 adds UNIMARC to the Acknowledged Standards list with Posture: Map
(via DC) and explicit exclusion from internal model adoption.

---

### Article 12 — Activation Prerequisites

The following must be complete before the first production ingestion run begins.

| # | Action | Gate |
|---|---|---|
| 12.1 | DD-GALLICA-001 ratified (Director signature + second-human approval) | Gate 1 |
| 12.2 | Source registry INSERT (GAL-SR-1 through GAL-SR-13) executed as single authorized statement | Gate 2 |
| 12.3 | Standards Constitution Amendment SA-3 ratified (BnF Gallica API profile) | Gate 2 |
| 12.4 | Gallica IIIF 2.1 → 3.0 bridging adapter implemented and documented in `docs/standards/gallica_iiif_bridge_v1.md` | Gate 3 |
| 12.5 | OAI-PMH ingestion worker implemented: Gallica Rights Addendum v1 classification logic (Article 2 tables GA-1A, GA-1B, GA-2) | Gate 3 |
| 12.6 | Asset Zero validated: full-resolution watermark-free IIIF delivery confirmed | Gate 3 |
| 12.7 | Asset Zero validated: IIIF 2.1 → 3.0 bridging adapter produces valid IIIF 3.0 manifest | Gate 3 |
| 12.8 | At least one human reviewer authorized for `item_type = 'rights_review'` workflow items (Gallica source, including French-language text classification) | Gate 3 |
| 12.9 | FM exclusion confirmed in writing — no FM system has access to rights workflow | Gate 3 |
| 12.10 | Rate limit confirmed at or below 2 req/s against Gallica production endpoints | Gate 3 |

No partial completion is acceptable.

---

## Part VI — Unique Risk Register

Risks specific to Gallica relative to prior activated sources (Europeana, DPLA, Rijksmuseum).

| Risk ID | Risk | Severity | Prior DD equivalent | Mitigation |
|---|---|---|---|---|
| **R-1** | Bilingual rights text (`dc:rights` in French) not covered by URI-based Matrix | High | DPLA free-text R-1, but different language | Gallica Rights Addendum v1 (Article 2.2 tables) |
| **R-2** | "Domaine public revisité" items require Article 14 / Bridgeman assessment per item | Medium | No equivalent in prior DDs | HR-GA-3 review rule; pilot sub-cap of 5 items |
| **R-3** | IIIF version gap (2.1 vs 3.0 target) — bridging adapter unproven in NC pipeline | Medium | Partial: DD-RIJKSMUSEUM-001 F-5 (SA-4) | Article 4.1 bridging specification; Asset Zero validation gate (12.6–12.7) |
| **R-4** | BnF metadata CC-BY assertion may be confused with image rights | Medium | No equivalent | Article 2.3 metadata rights separation rule |
| **R-5** | OAI-PMH `dc:date` format inconsistent; publication year parsing unreliable | Medium | No equivalent | Date parsing tolerance: accept year-only, decade ranges, "ca." prefixes as `date_confidence = 'approximate'`; fail-safe to `absent` rather than error |
| **R-6** | Audio/video Phase 3 exclusion must not be breached by overly broad SRU queries | Low | No equivalent | Article 5(e): Phase 3 constitutional gate; `phase_1_only = true` in config |
| **R-7** | SRU query returning results outside Madagascar scope despite `subject all "Madagascar"` filter | Low | Europeana pilot place association (Article 6c) | Article 9(b): place association required; non-Madagascar assets discarded at ingestion |
| **R-8** | Watermarks on some Gallica images at full resolution | Low-Medium | No equivalent | Article 10(d): watermark-free delivery confirmed in Asset Zero before pilot cap begins |
| **R-9** | UNIMARC metadata richer than OAI-PMH DC export; some fields lost in DC export path | Low | No equivalent | Noted; SA-6 registers UNIMARC as an Acknowledged Standard; production may evaluate UNIMARC direct path in DD-GALLICA-002 |
| **R-10** | Post-1927 publication dates incorrectly declared as "domaine public" by BnF | Medium | DPLA R-5 (small institution NoC-US) | Article 3.3(b): BnF authority status conditional; reviewer must confirm pub date regardless of BnF declaration |

---

### Article 13 — Subsequent Decisions

| ID | Trigger | Scope |
|---|---|---|
| **SA-3** | Required before Gate 2 | BnF Gallica API Profile → Standards Constitution v1.1 |
| **SA-6** | Concurrent with SA-3 | UNIMARC acknowledged standard → Standards Constitution v1.1 |
| **DD-GALLICA-002** | Pilot success (all criteria met at 50 assets) | Gallica scope expansion beyond Madagascar; pilot cap removal; additional place queries |
| **DD-GALLICA-003** | When MSC P3-1 amendment is ratified | Phase 3 audio/film assessment for Gallica; phonorecord rights framework under MMA |
| **DD-IIIF-SA-4** | If not yet ratified concurrent with SA-3 | IIIF Presentation API standards amendment to Standards Constitution |

DD-GALLICA-002 is not automatically triggered by pilot success. It requires a Director
review of pilot results, a Principal Architect recommendation, and a new Decision.
The IIIF 2.1 bridging performance and OAI-PMH metadata quality observations from the
pilot are primary inputs to the DD-GALLICA-002 scope decision.

DD-GALLICA-003 is a long-term planning decision. The phonorecord rights framework
under the Music Modernization Act analysis (F-16) establishes that most Gallica audio
is BLOCKED. DD-GALLICA-003 is unlikely to yield significant commercial activation
even when the Phase 3 constitutional gate is satisfied. The Director should review this
assessment at Phase 3 activation time.

---

## Ratification

This Decision requires:

1. **Director signature** — opengracelabs (the Director)
2. **Second-human approval** — a second person with authority over NC governance decisions

Neither the Director's signature nor the second-human approval has been recorded.
This document is a Draft until both signatures are present.

| Role | Name | Date |
|---|---|---|
| Director | — | — |
| Second Human Approver | — | — |

---

*DD-GALLICA-001 Draft — 2026-06-08*
*Drafted by: Principal Architect (Claude Sonnet 4.6)*
*Pending ratification by: Director (opengracelabs)*
