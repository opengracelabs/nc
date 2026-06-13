# NC-TRUST-003: Level 4 Trust Blueprint

| Field | Value |
|---|---|
| Document | NC-TRUST-003 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | NC-TRUST-002 · NC-TRUST-001 · NC-INSTITUTION-001 |
| Scope | Designs Level 4 trust across 5 standards: PD Provenance, Certificate, Edition Registry, Institutional Transparency, Educational Reuse. |

---

## The Level 4 Premise

Level 3 means NC does institutional work at world-class quality.
Level 4 means NC publishes that work as open standards that the sector adopts.

The Rijksmuseum became the certificate standard-setter by doing it first, doing it well,
and doing it visibly. The Getty became the provenance standard-setter by publishing the
Provenance Index as a public resource. National Geographic became the editorial
standard-setter by printing the byline on every page for 136 years. None of these
institutions reached Level 4 by keeping their methods internal.

NC's path to Level 4 is the same: publish the standards you have already built.
NC-TRUST-001 and NC-TRUST-002 define systems for NC's internal use. NC-TRUST-003
turns those systems into citable, versioned, openly licensed standards that other
PD illustration platforms, digital archives, and commerce platforms can adopt.

**The gap these standards fill:**
There is no published professional standard for provenance documentation of PD
illustration in digital commerce. No published certificate standard for PD print
sales. No published edition registry API. No published institutional transparency
standard for PD commerce platforms. No published educational reuse standard for
PD illustration archives. These gaps are real and felt by every institution in this
space. NC is in a position to fill all five simultaneously — because NC has already
done the underlying work.

**Publishing model:**
All five standards are published under Creative Commons Zero (CC0) at
`standards.nc.art`. Any platform may adopt, fork, or extend them. Platforms that
conform to a standard may display "Conforms to NC [Standard Name] v[N]." NC
maintains the canonical version. Version history is public. Amendments are proposed
publicly and ratified after a stated comment period.

**The five standards:**

| Standard | Code | Domain |
|---|---|---|
| NC Public Domain Provenance Standard | NC-PDPS | Curator Identity + Provenance |
| NC Certificate of Authenticity Standard | NC-COAS | Certificates |
| NC Edition Registry Standard | NC-ERS | Editions |
| NC Institutional Transparency Standard | NC-ITS | Institutions |
| NC Educational Reuse Standard | NC-EDRS | Educational Reuse |

---

## Standard 1: NC Public Domain Provenance Standard (NC-PDPS)

**Version:** 1.0 · **License:** CC0 · **Published at:** `standards.nc.art/provenance`

### Purpose

The NC-PDPS defines the minimum requirements for provenance documentation of
public domain illustration works used in digital commerce. It addresses a specific
chain: original illustration (1750–1900) → institutional custody → digital release
(CC0 or copyright expiry) → commercial activation. This chain is structurally
different from the provenance of oil paintings with centuries of sale history.
No existing standard (Getty Provenance Index, SPECTRUM, CIDOC-CRM) addresses it
directly. NC-PDPS fills that gap.

### Why NC can write this standard

NC's PD chains are shorter and cleaner than those of any traditional museum:
typically one institutional custodian, one rights release, one commercial activator.
This simplicity is an advantage in standard design — the standard can be precise
because the chain is defined. A standard designed for NC's chain is useful for
every PD digital archive, not just NC.

### Section 1: Chain Structure

A compliant provenance record must contain all six links. No commercial activation
is permitted until all six links are documented.

```
Link 1 — Creator
  creator_name:         string (full legal name as recorded historically)
  creator_ulan:         string|null (Getty ULAN ID where available)
  creator_viaf:         string|null (VIAF ID, used if ULAN absent)
  creator_dates:        string (YYYY–YYYY; "c. YYYY" for approximate)
  creator_nationality:  string (ISO 3166-1 alpha-2)
  creator_role:         string (e.g., "Physician and naturalist, Discovery Expedition")

Link 2 — Creation Event
  creation_date:        string (YYYY or YYYY–YYYY)
  creation_context:     string (commission, expedition, publication, survey)
  creation_location:    string (place name + GeoNames ID)
  creation_medium:      string (AAT vocabulary term preferred)
  source_publication:   string|null (if from a published work: title, year, plate/page)

Link 3 — Custody History
  custody_transfers: [
    {
      from:    string (creator | institution name | "unknown")
      to:      string (institution name | "unknown")
      date:    string (YYYY or "c. YYYY" or "unknown")
      method:  enum (bequest | purchase | founding_collection | transfer | unknown)
      evidence: string|null (source of this transfer record)
    }
  ]
  current_holder:       string (institution name)
  current_holder_ror:   string|null (ROR ID of holding institution)
  accession_record_url: string (stable permalink to institutional record)

Link 4 — Rights Status
  rights_class:         enum (1=copyright_expiry | 2=us_gov | 3=cc0 | 4=pre_date | 5=pd_dedication)
  rights_statement:     string (statutory language — see Section 2)
  expiry_date:          string|null (YYYY — for Class 1)
  expiry_statute:       string|null (full statute name and section — for Class 1)
  expiry_jurisdiction:  string|null (ISO 3166-1 alpha-2 — for Class 1)
  release_institution:  string|null (for Class 3: who released as CC0)
  release_date:         string|null (for Class 3: YYYY)
  release_url:          string|null (for Class 3: link to CC0 statement)

Link 5 — Source Access
  access_method:        enum (iiif | direct_download | api | physical_scan | aggregator)
  access_url:           string (URL used to obtain the file)
  access_url_archived:  string (Wayback Machine archive URL)
  access_date:          date (when NC obtained the file)
  file_format:          string (TIFF | JPEG | PNG)
  resolution_dpi:       integer
  color_profile:        string (sRGB | AdobeRGB | ProPhoto)

Link 6 — Commercial Activation
  curator_name:         string
  curator_id:           string (ORCID preferred)
  authority_reviewer:   string (name of second person who confirmed rights)
  curation_date:        date
  nc_collection:        string (collection slug)
  nc_product:           string (product code)
  authority_notes:      string|null (GeoNames ID, Wikidata QID, other authority refs)
```

### Section 2: Rights Statement Language

Compliant rights statements by class. The statement on the certificate and product
page must use language at this level of specificity.

**Class 1 — Copyright Expiry:**
```
"Copyright in the original work by [Creator] ([dates]) expired on [date] under
[Full Statute Name], [Section], which provides for copyright protection of
[N] years from the death of the author. [Creator] died [year]; copyright
expired [year]. This work is in the public domain in [jurisdiction]."
```

**Class 2 — US Government Work:**
```
"This work was created by an officer or employee of the United States federal
government as part of that person's official duties. It is not subject to
copyright protection under 17 U.S.C. § 105 and is in the public domain
in the United States."
```

**Class 3 — CC0 Voluntary Release:**
```
"The [Institution] released this digital reproduction under Creative Commons
Zero (CC0) on [date], waiving all copyright and related rights worldwide to
the fullest extent permitted by law. The original work is additionally in the
public domain: copyright expired [date] under [statute]. This work may be used
for any purpose without restriction or attribution requirement."
```

**Class 4 — Pre-Publication Date:**
```
"This work was first published in [country] before [threshold date]. Works
published before this date are in the public domain under [jurisdiction] law
([statute reference])."
```

### Section 3: Stability and Archiving

1. `accession_record_url` must be a stable institutional permalink (accession-number
   based, not a search result).
2. All source URLs must be archived via the Internet Archive Wayback Machine at time
   of curation. The archive URL is stored in `access_url_archived`.
3. URL health monitoring: all `accession_record_url` values must be checked quarterly.
   Broken links must be flagged within 30 days and remediated within 90 days.
   Broken link status is recorded in the provenance version history.
4. Provenance records are version-controlled. All edits are logged with date, editor
   name, and reason. Previous versions are retained permanently.

### Section 4: Metadata Authorities

| Field | Authority |
|---|---|
| creator_ulan | Getty Union List of Artist Names (vocab.getty.edu/page/ulan/) |
| creator_viaf | Virtual International Authority File (viaf.org) |
| creation_location | GeoNames numeric ID (geonames.org) |
| creation_medium | Getty Art & Architecture Thesaurus (vocab.getty.edu/aat/) |
| current_holder_ror | Research Organization Registry (ror.org) |

### Level 4 Gate for Provenance

NC reaches Level 4 in provenance when:
- All NC products carry a compliant NC-PDPS chain
- The standard is published at `standards.nc.art/provenance`
- At least one other platform cites or adopts the standard
- NC presents or publishes the standard methodology in a peer-accessible forum
  (conference, open publication, or institutional communication)

---

## Standard 2: NC Certificate of Authenticity Standard (NC-COAS)

**Version:** 1.0 · **License:** CC0 · **Published at:** `standards.nc.art/certificate`

### Purpose

NC-COAS defines the format, fields, language, and verification requirements for a
certificate of authenticity for a public domain illustration print. No existing
certificate standard applies specifically to PD illustration commerce. Christie's
and Sotheby's use certificate conventions that assume a living artist or an estate
licensor. Rijksmuseum's certificate is excellent but internal. NC-COAS makes the
standard explicit, public, and adoptable.

### Section 1: Certificate Schema

The canonical machine-readable representation of an NC-COAS certificate.
Published at `standards.nc.art/certificate/schema/v1.json`.

```json
{
  "$schema": "https://standards.nc.art/certificate/v1",
  "standard": "NC-COAS-1.0",
  "certificate_id": {
    "type": "string",
    "description": "Platform-specific. Must be unique, permanent, and queryable.",
    "example": "NC-COL001-PROD001-042-2026"
  },
  "work": {
    "title": "string",
    "creator_name": "string",
    "creator_ulan": "string|null",
    "creator_dates": "string",
    "creation_date": "string",
    "creation_context": "string",
    "provenance_standard": "NC-PDPS-1.0",
    "provenance_url": "string (permalink to full provenance record)"
  },
  "institution": {
    "name": "string",
    "location": "string",
    "record_url": "string",
    "rights_class": "integer (1–5)",
    "rights_statement": "string (NC-PDPS Section 2 language)"
  },
  "edition": {
    "type": "enum: collector|open|digital",
    "number": "integer|null",
    "size": "integer|null",
    "status": "enum: open|closed|retired",
    "registry_url": "string (NC-ERS verify endpoint)"
  },
  "production": {
    "paper_brand": "string",
    "paper_gsm": "integer",
    "paper_archival_standard": "string (ISO citation)",
    "print_process": "string",
    "ink_archival_rating": "string (ISO citation)",
    "studio_name": "string",
    "studio_location": "string"
  },
  "conservation": {
    "note": "string",
    "humidity_max_pct": "integer",
    "temperature_max_c": "integer",
    "glazing_recommendation": "string",
    "storage_recommendation": "string"
  },
  "curation": {
    "curator_name": "string",
    "curator_orcid": "string|null",
    "institution": "string",
    "selection_date": "string (YYYY)"
  },
  "document": {
    "issued_date": "date",
    "issuing_institution": "string",
    "verification_url": "string",
    "certificate_standard": "NC-COAS-1.0"
  }
}
```

### Section 2: Physical Certificate Requirements

A physically printed certificate must meet the following minimum requirements:

| Requirement | Specification |
|---|---|
| Size | A5 minimum (148 × 210mm) |
| Paper weight | 270gsm minimum, uncoated |
| Paper standard | Acid-free |
| Required fields | All schema fields except null-permitted optional fields |
| Institution mark | Issuing institution name and contact (logo if permitted) |
| Source institution | Named with record URL (printed as short URL or QR code) |
| Verification | URL or QR code linking to public verification endpoint |
| Conservation note | Conservation section complete with ISO citations |
| Edition mark | Physical mark reference ("See edition mark on print margin") |
| Language | Rights statement at NC-PDPS Section 2 statutory level |

### Section 3: Conservation Language Standard

Conservation notes must cite specific published standards, not marketing claims.

**Minimum required citations:**
- Paper permanence: ISO 9706 (permanent paper) or ANSI/NISO Z39.48
- Ink longevity: ISO 11798 (accelerated ageing) with rated year figure
- Display guidance: reference to AAM (American Alliance of Museums) light guidelines
  or equivalent (max 50 lux for works on paper)
- Humidity: 45–55% RH for paper (ISO 11799 storage standard)
- Temperature: 15–20°C for long-term storage

**Standard conservation block:**
```
Conservation
Paper: [Brand] [gsm]gsm. Acid-free, OBA-free. Conforms to ISO 9706
(permanent paper).
Inks: Archival pigment. Rated [N]+ years per ISO 11798 accelerated ageing.
Display: Avoid direct sunlight. Maximum 50 lux for displayed works on paper.
Frame with UV-protective glazing (UV-filter glass or acrylic, ≥97% UV block).
Storage: 45–55% relative humidity. 15–20°C. Store flat or rolled in
acid-free tissue.
```

### Section 4: Verification Protocol

A platform implementing NC-COAS must provide a public verification endpoint.

**Endpoint specification:**
```
GET /certificates/{certificate_id}
→ 200: {
    "certificate_id": "string",
    "work_title": "string",
    "creator": "string",
    "edition_type": "string",
    "edition_number": "integer|null",
    "edition_size": "integer|null",
    "edition_status": "string",
    "curator": "string",
    "issued_date": "date",
    "valid": true
  }
→ 404: { "error": "Certificate not found" }
→ No authentication required
→ Uptime SLA: 99.5% (stated public commitment)
→ Permanence: data retained permanently (see Section 5)
```

### Section 5: Permanence Commitment

A platform implementing NC-COAS must publish the following commitment:

*"Certificates issued under NC-COAS are permanent records. In the event that
[Platform] ceases commercial operation, all certificate records will be transferred
to the Internet Archive within 90 days and made publicly queryable in perpetuity
at no charge."*

This is the condition under which a collector can rationally trust a digital
certificate. Without the permanence commitment, the certificate is only as durable
as the platform.

### Level 4 Gate for Certificates

NC reaches Level 4 in certificates when:
- All NC products carry NC-COAS-compliant certificates
- NC-COAS is published at `standards.nc.art/certificate`
- The verification endpoint is public and has a stated uptime SLA
- The permanence commitment is published on the NC website
- At least one other platform adopts or publicly references NC-COAS

---

## Standard 3: NC Edition Registry Standard (NC-ERS)

**Version:** 1.0 · **License:** CC0 · **Published at:** `standards.nc.art/editions`

### Purpose

NC-ERS defines the architecture, API, and operational procedures for a public edition
registry for limited edition prints. It addresses the gap between "limited edition"
as a marketing claim and "limited edition" as a verifiable fact. The standard is
designed so that auction houses, insurers, resellers, and collectors can verify any
registered edition without contacting the issuing platform.

### Section 1: Edition Type Definitions

**Collector's Edition (CE):**
A fixed-count edition. Before the first print is sold, the edition size is defined
and locked. Edition numbers are assigned sequentially (1, 2, 3 … N). When N prints
have been sold, the edition closes automatically. The production file may not be
reused for a new CE of the same work without opening a distinctly named second
edition (e.g., "Second Collector's Edition") with a new edition ID.

**Open Edition (OE):**
An unlimited edition. No edition number. A certificate of authenticity is still
issued for every print. The certificate edition type field reads "Open Edition."
The product page must display "Open Edition" prominently. An OE may be retired
(production discontinued) without closure — the platform may stop selling it at
any time.

**Digital Download (DD):**
A file licence, not a print. No edition concept applies. A purchase confirmation
is issued. The confirmation records: work title, creator, rights statement, file
format, resolution, intended use licence, and date of download. Not governed by
NC-ERS beyond the digital record.

### Section 2: Registry API Specification

All NC-ERS compliant registries must implement the following public endpoints.
No authentication required for read operations. HTTPS mandatory.

```
GET /editions/{edition_id}
Response: {
  "edition_id": "string",
  "product_name": "string",
  "work_title": "string",
  "creator": "string",
  "edition_type": "CE|OE|DD",
  "edition_size": "integer|null",
  "edition_current": "integer",
  "edition_status": "open|closed|retired",
  "opened_date": "date",
  "closed_date": "date|null",
  "curator": "string"
}

GET /certificates/{certificate_id}/verify
Response: {
  "certificate_id": "string",
  "valid": true|false,
  "edition_type": "string",
  "edition_number": "integer|null",
  "edition_size": "integer|null",
  "edition_status": "string",
  "produced_date": "date",
  "work_title": "string",
  "curator": "string"
}

GET /editions/{edition_id}/status
Response: {
  "edition_id": "string",
  "edition_status": "open|closed|retired",
  "prints_issued": "integer",
  "prints_remaining": "integer|null",
  "closed_date": "date|null"
}
```

**Rate limits:** 1,000 requests/hour per IP, unauthenticated. No rate limit for
verified institutional API partners (auction houses, insurance platforms).

**Error codes:** Standard HTTP. 404 for unknown IDs. 410 Gone for retired editions
where records have been transferred to archive.

### Section 3: Physical Edition Mark Specification

Every Collector's Edition print must carry a physical authentication mark applied
before packaging. The mark is the second authentication factor alongside the
certificate.

**Specification:**
- Location: lower-left margin, 5–10mm below the image edge
- Content: `{edition_number}/{edition_size}` in pencil
  Example: `42/100`
- Medium: acid-free graphite pencil (HB or 2H). Not ballpoint, marker, or ink.
  Reason: graphite is stable, conservator-accepted, and cannot be chemically
  removed without visible damage to the paper.
- Initialling: curator initials in pencil, lower-right margin, same level
- Applied by: named curator or explicitly authorised designee
- Applied when: after print quality check, before packaging

This mark is the Senefelder convention for limited edition lithographs, adapted for
giclée. It is immediately recognisable to print collectors and auction specialists.

### Section 4: Edition Closure Procedure

When a Collector's Edition reaches its defined size limit, the following procedure
must be completed within 5 business days:

```
Step 1: Registry update
  edition_status → "closed"
  closed_date → today

Step 2: Product page update
  Display: "This edition is now closed. [N] prints were issued."
  Remove "Add to cart" or equivalent purchase mechanism
  Retain product page permanently (provenance reference for existing holders)

Step 3: Production file archive
  The high-resolution production file is archived with a closure record
  File metadata includes: closure date, final edition number, curator ID
  The file may not be re-exported for new CE prints of this edition
  A second edition requires a new production file audit and a new edition_id

Step 4: Final print annotation
  The certificate issued for print number N carries the notation:
  "Final print of [Edition Name]. Edition closed [date]."

Step 5: Registry closure record (public)
  Published at: GET /editions/{edition_id}/closure
  Content: {closed_date, final_edition_number, closure_confirmed_by}
```

### Section 5: Archive Commitment

Registries implementing NC-ERS must publish:

*"Edition records are permanent. If [Platform] ceases operation, all edition registry
data — including all certificate records, edition histories, and closure records —
will be transferred to the Internet Archive within 90 days and maintained as a
permanent public queryable archive. API access will be preserved at
archive.org/nc-ers/ with identical endpoint structure."*

This commitment must appear on the platform's terms of service or standards page.

### Level 4 Gate for Editions

NC reaches Level 4 in editions when:
- All CE products are registered in a compliant NC-ERS registry
- The API is public, documented, and has a stated uptime commitment
- Physical marks have been applied to all CE prints sold
- At least one closed edition has completed the closure procedure
- NC-ERS is published at `standards.nc.art/editions`
- At least one resale transaction references the NC-ERS registry for verification

---

## Standard 4: NC Institutional Transparency Standard (NC-ITS)

**Version:** 1.0 · **License:** CC0 · **Published at:** `standards.nc.art/institutions`

### Purpose

NC-ITS defines the minimum disclosure requirements for a commercial platform using
content sourced from cultural institutions. It addresses the specific case of PD
illustration commerce: a platform uses digitised works held by museums, libraries,
and archives — often CC0 released — and must disclose that use adequately to
collectors, scholars, journalists, and the institutions themselves.

No existing standard covers this. IFLA and CIDOC provide museum documentation
standards. Creative Commons provides attribution guidance. Neither defines what
"adequate disclosure" means for a PD illustration commerce platform. NC-ITS fills
this gap.

### Section 1: Required Disclosures

A platform that uses content from a cultural institution must disclose, publicly and
permanently, the following information per institution:

```
institution_disclosure {
  institution_name:       string
  institution_location:   string (city, country)
  institution_founded:    integer (year)
  institution_ror:        string|null (ROR ID)
  institution_url:        string (official website)
  collection_url:         string|null (digital collection URL)

  rights_basis:           enum (cc0 | copyright_expiry | us_gov | other)
  rights_statement_url:   string|null (institution's published rights statement)

  notification_status:    enum (notified | not_notified | not_applicable)
  notification_date:      date|null
  institutional_response: enum (acknowledged | no_response | not_applicable)
  institutional_contact:  string|null (name of contact, if any — not email)

  works_in_use:           integer (count, updated dynamically)
  content_types:          string[] (e.g., ["botanical illustration", "natural history"])

  display_tier:           enum (1=cc0_partner | 2=pd_source | 3=aggregator_source)
  logo_permitted:         boolean
  logo_permission_date:   date|null
}
```

### Section 2: Tier Definitions

**Tier 1 — CC0 Partner:**
Institution has been notified of commercial use. Institution has responded
(acknowledged, no objection, or actively endorsed). Logo display is appropriate
where permission is granted in writing. Full institution page on platform.

**Tier 2 — PD Source:**
Content is used on PD/copyright expiry basis. Institution may or may not have
been notified. No CC0 release by the institution. Institution name and link
displayed; logo not displayed without specific written permission.

**Tier 3 — Aggregator Source:**
Content accessed via an aggregator (Europeana, DPLA). The aggregator and the
original holding institution are both disclosed. Attribution format: "From
[Holding Institution] via [Aggregator]."

### Section 3: Notification Protocol

Before any work goes on sale commercially, the following notification must be sent
to the holding institution:

**Minimum notification content:**
1. Platform name and URL
2. Description of commercial use (what is being sold)
3. Works being used (list or representative count by type)
4. Rights basis claimed (specific statute or CC0 reference)
5. Attribution format used on product pages and certificates
6. Contact email for institutional response

Notification must be sent via the institution's stated digital collections or rights
contact. Non-response is logged and does not block sale. Non-response is distinguished
from refusal. Refusal blocks sale.

### Section 4: Annual Institutional Disclosure Report

A compliant platform must publish an annual institutional disclosure report.
Published publicly, linked from the platform's about section.

**Required content:**
1. All institutions with tier classification (Tier 1 / 2 / 3)
2. Works count per institution in active commercial use
3. Rights basis per institution
4. Notification status per institution (sent / responded / pending / not applicable)
5. Changes since previous report (institutions added, removed, reclassified)
6. Logo permissions held (institutions, granted date)
7. Total works in active commercial use across all institutions

**First report:** Published when the platform goes to public launch.
**Subsequent reports:** Annual, within 90 days of the platform's founding anniversary.

### Section 5: Attribution Standards

Published attribution formats for all use contexts. These formats are part of the
platform's public standards page so that users (teachers, journalists, bloggers) know
how to attribute NC content in their own work.

**Product page (short form):**
`From the collection of [Institution Name]`

**Certificate (long form):**
`From the collection of [Institution Name], [Location]. [Rights statement].
View the original record: [URL]`

**Educational use:**
`[Work Title] · [Creator] ([dates]) · [Institution Name] (CC0 / Public domain) ·
Via [Platform Name] ([URL])`

**Academic citation:**
`[Creator]. [Work Title]. [Date]. [Institution Name], [Location]. Public domain.
Accessed via [Platform Name], [URL], [access date].`

### Level 4 Gate for Institutions

NC reaches Level 4 in institutional transparency when:
- All Tier 1 institutions have been notified and responses are documented
- The first annual institutional disclosure report is published
- At least 3 Tier 1 institutions have granted logo permission in writing
- NC-ITS is published at `standards.nc.art/institutions`
- At least one external party (journalist, academic, institution) references NC-ITS

---

## Standard 5: NC Educational Reuse Standard (NC-EDRS)

**Version:** 1.0 · **License:** CC0 · **Published at:** `standards.nc.art/education`

### Purpose

NC-EDRS defines the minimum requirements for a public domain digital archive to be
genuinely useful in educational settings. It addresses access, attribution, curriculum
support, accessibility, and teacher resources as a unified standard. The standard is
designed for adoption by any PD digital archive — not just NC — and is grounded in
the structural fact that PD content requires no licence for educational use.

### Section 1: Access Requirements

**Minimum free educational access:**
- All PD works must be downloadable at educational resolution without account creation,
  payment, or licence agreement
- Educational resolution: minimum 1920px long edge, minimum 150dpi
- Format: JPEG or TIFF with embedded XMP/IPTC metadata
- Metadata fields embedded in every file: work title, creator, institution,
  rights class (NC-PDPS), attribution text, source URL, download date

**The no-friction principle:**
The path from the product page or educators page to a free educational download must
contain zero commerce friction: no cart, no checkout, no payment step, no login
requirement. Any download path that routes through a commerce flow before offering
free access fails this standard.

**Download file naming convention:**
`[platform]-[collection-slug]-[work-slug]-edu-[year].jpg`
Example: `nc-south-georgia-wilson-penguin-edu-2026.jpg`

### Section 2: Attribution Standard for Education

A compliant platform must publish, prominently on its educators page, the
recommended attribution format for educational materials.

**Standard educational attribution:**
`[Work Title] · [Creator] ([dates]) · [Institution Name] · Public domain ·
Via [Platform Name] ([URL])`

**The key disclosure:**
The platform must publish the following statement alongside the attribution format:

*"These works are in the public domain. Public domain means copyright has expired
or been waived. No permission is required to reproduce, display, or distribute
public domain works, including for educational purposes. Attribution to [Platform]
is appreciated but not legally required."*

This statement answers the question every teacher has: "Do I need permission?"
A compliant platform answers it clearly, on the educators page, without requiring
the teacher to ask.

### Section 3: Accessibility Requirements

A compliant platform must:

1. Publish a WCAG 2.1 AA accessibility audit, conducted by a person or service
   distinct from the platform's own staff, with results publicly available at
   `/accessibility`
2. Publish a remediation timeline for all identified failures within 30 days of
   the audit
3. Complete remediation of critical (Level A) failures within 60 days of audit
4. Complete remediation of serious (Level AA) failures within 120 days of audit
5. Name a contact for accessibility concerns and provide a stated response time
   (maximum 10 business days)
6. Include meaningful alt text on all images — not decorative description but
   educational context description suitable for a visually impaired student

**Alt text standard for PD illustration:**
Alt text must include: what is depicted, by whom, and when. Sufficient for a student
who cannot see the image to understand its historical and educational significance.

*Example:* `"Watercolour painting of an adult king penguin and chick, with detailed
feather colouring. Painted by Edward Wilson during the British National Antarctic
Expedition of 1901–04. The only visual record of this species made by a scientific
observer before photography reached sub-Antarctic waters."`

### Section 4: Curriculum Support Standard

For any collection with an "educational designation," the following resources must
be published and maintained:

**Context guide (6-section format):**
```
Section 1: THE PLACE (3 sentences)
  What is this place, why does it matter, what is it like today.

Section 2: THE ILLUSTRATOR (3 sentences)
  Who made these images, when, and why they were making them.

Section 3: THE WORKS (3 sentences)
  What the images show, what makes them significant, what they record.

Section 4: THE HISTORICAL MOMENT (3 sentences)
  What was happening in the world when these images were made.
  Why that context matters for understanding the images.

Section 5: DISCUSSION QUESTIONS (minimum 3)
  Q1: Close-looking question about the image itself
  Q2: Contextual question connecting the image to history, science, or geography
  Q3: Critical question about knowledge, representation, or public domain

Section 6: CURRICULUM CONNECTIONS
  [Subject]: [Specific topic] · [Year group / age range] · [Standard reference]
  Minimum 2 subjects. At least one from: history, biology, geography, art/design.
  Standard reference must be a named, publicly verifiable curriculum document.
```

**Curriculum alignment standard:**
Alignment must cite a specific, publicly verifiable national or international
curriculum. Accepted frameworks: UK National Curriculum, US Common Core / Next
Generation Science Standards, Australian Curriculum, IB Diploma Programme, IB MYP.
Alignment to a named document (e.g., "UK National Curriculum, History, Key Stage 3:
'Challenges for Britain, Europe and the wider world 1901 to the present day'") is
required at Level 3. General subject area only is accepted at Level 2.

### Section 5: Institutional Adoption Protocol

A compliant platform must provide a formal pathway for educational institutions
wishing to cite or formally adopt the platform as a curriculum resource.

**Minimum protocol requirements:**
- Application form: maximum 3 required fields (institution name, contact email,
  intended use)
- Response commitment: maximum 5 business days
- Free for all public educational institutions
- License issued: acknowledgment of right to use NC content in non-commercial
  educational materials with required attribution
- Annual renewal: email confirmation, no new application required
- Adopted institution listed as Educational Partner (opt-out available)

**Annual publication:**
The count of educational partners is published annually in the institutional
disclosure report (see NC-ITS Section 4) and on the educators page.

### Section 6: Open Licensing of the Standard

NC-EDRS is published under CC0. Any digital archive, library, museum education
department, or heritage platform may adopt, fork, or extend it for their own use.
Platforms that conform to all sections may display "Conforms to NC-EDRS v[N]."

The standard is specifically designed so that a small team or solo operator can
reach conformance. The goal is to raise the floor for PD educational access
across the sector — not to create a certification barrier.

### Level 4 Gate for Educational Reuse

NC reaches Level 4 in educational reuse when:
- WCAG 2.1 AA audit is complete, results are published, and critical/serious failures
  are remediated
- Context guides are published for all 5 signature collections
- Curriculum alignment cites a named standard for each collection
- At least 3 named educational institutions are listed as Educational Partners
- NC-EDRS is published at `standards.nc.art/education`
- At least one external educational authority references NC-EDRS

---

## The NC Standards Suite

The five standards together form the NC Standards Suite, published at
`standards.nc.art`. A platform that conforms to all five may display:

> **"Conforms to NC Standards Suite v1.0"**

This conformance mark signals: named curators, complete provenance chains, verified
edition registries, institutional transparency, and free educational access — all at
the level of specification required by scholars, collectors, teachers, and institutions.

### Suite conformance levels

| Mark | Requirements |
|---|---|
| NC-PDPS Conformant | Provenance standard only |
| NC-COAS Conformant | Certificate standard only |
| NC-ERS Conformant | Edition registry standard only |
| NC-ITS Conformant | Institutional transparency standard only |
| NC-EDRS Conformant | Educational reuse standard only |
| **NC Standards Suite Conformant** | All five standards |

Individual conformance marks allow other platforms to adopt one standard without
committing to all five. This is the adoption model: entry through any single standard,
path to full conformance available.

### Amendment Process

NC publishes amendments to any standard following a stated process:
1. Proposed amendment published publicly with 30-day comment period
2. Comments reviewed by NC; responses published
3. Amendment adopted or rejected with stated rationale
4. New version published; version history retained permanently

---

## Level 4 Maturity Gate Summary

NC reaches Level 4 when all five domain gates are confirmed.

| Domain | Gate confirmation event |
|---|---|
| Provenance | NC-PDPS published; at least one external citation or adoption |
| Certificates | NC-COAS published; permanence commitment published; verification endpoint live |
| Editions | NC-ERS published; at least one CE closed and closure procedure completed; registry API public |
| Institutions | NC-ITS published; first annual disclosure report published; 3+ logo permissions |
| Educational Reuse | NC-EDRS published; WCAG audit complete; 3+ educational partners named |

**The Level 4 signal:**
When all five gates are confirmed, NC publishes a Level 4 declaration at
`standards.nc.art` stating: "Nature & Culture operates at Level 4 institutional
trust across all five domains of the NC Trust Maturity Model. Methodology available
for independent review."

That declaration is the institutional signal. Not a claim that NC is world-class.
A published, verifiable, independently reviewable statement that NC has done the
work and is showing it.

---

## The Strategic Argument

The Smithsonian, Rijksmuseum, NatGeo, and Getty became sector authorities because
they published their methods. The Getty Provenance Index is not a competitive
advantage for Getty — it is a public resource that made Getty the reference point
for provenance research globally. The AAT, ULAN, and TGN are public. They are cited
in every museum management system. Getty is cited every time they are used.

NC's equivalent is not art historical data. It is commercial PD illustration
infrastructure. The provenance chain, the certificate format, the edition registry,
the institutional transparency protocol, the educational reuse framework — these are
the standards that the PD commerce space needs and that no one has published.

NC publishes them first. NC maintains them. NC becomes the reference point.

That is Level 4.

---

*NC-TRUST-003 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
