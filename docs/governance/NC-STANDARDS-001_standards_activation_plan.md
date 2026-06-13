# NC-STANDARDS-001: Standards Activation Plan

| Field | Value |
|---|---|
| Document | NC-STANDARDS-001 |
| Version | 1.0 |
| Status | **DRAFT — pending ratification** |
| Date | 2026-06-13 |
| Authority | NC-TRUST-003 · NC-TRUST-002 · NC-TRUST-001 |
| Scope | Reviews each of the 5 NC standards against actual platform state. Determines what can activate immediately and what requires implementation. Issues sequenced activation plan. |

---

## Code Reality Assessment

A review of `apps/web/lib/trust.ts`, `apps/web/lib/collections.ts`, and all trust-related
pages reveals more infrastructure than expected — and a specific pattern of gaps that is
consistent across all five standards.

**What is already built:**

| System | Pages live | Data model | State |
|---|---|---|---|
| Certificate | `/certificate`, `/verify/[certificate]` | `certificateRecord` in trust.ts | Earthrise only, hardcoded |
| Edition Registry | `/registry`, `/verify/[certificate]` | `editionRegistry` in trust.ts | Earthrise only, no edition_size or status |
| Curators | `/curators`, `/curators/[slug]` | `trustCurators` in trust.ts | Anonymous desks, not named individuals |
| Institutions | `/institutions`, `/institutions/[slug]` | `trustInstitutions` in trust.ts | Wrong institutions listed |
| Provenance | Chain on `/verify/[certificate]` | `publicProvenanceChain` in trust.ts | Earthrise-specific 5-step format |
| Educational | Panel text in trust.ts only | `educationalUsePanel` | No page, no downloads, no resources |

**The consistent pattern:**
The structural skeleton is built for four of the five standards. The gaps are
specific, not architectural: wrong field values, missing fields, wrong institutions,
anonymous curators, static hardcoded data where queries should be, and no Earthrise-
scope extension to the signature collections.

**The single most impactful gap:**
The curator system has three institutional "desks" (Institutional Editorial Board,
Heritage Places Desk, Expedition & Ecology Desk) instead of named people. This is
not a data problem — it is a decision. Until a named individual replaces each desk,
no standard that references curator identity can claim conformance.

---

## Standard-by-Standard Activation Status

---

### NC-COAS — Certificate of Authenticity Standard

**Built:** `/certificate` page live. `certificateRecord` in trust.ts. `/verify/[certificate]`
live and functioning. One certificate (NC-COA-EARTHRISE-0001) fully verifiable.

**Current fields present:** certificateId, workTitle, collectionTitle, sourceInstitution,
sourceIdentifier, creator, mission, date, rights, attribution, nonendorsement,
verificationStatus, curatorStatement.

**Gaps against NC-COAS v1.0:**

| Gap | File | Specific fix |
|---|---|---|
| Rights string is not statutory-level | `governed-content.ts:8` | Current: `"Public domain — United States Government Work, 17 U.S.C. § 105"` → Required: full Class 2 language from NC-TRUST-003 Section 2 |
| No ISO conservation citations | `certificate/page.tsx` | Add conservation block to certificate page with ISO 9706, ISO 11798 citations |
| No permanence commitment | `certificate/page.tsx` | Add one paragraph: "Certificate records are permanent..." |
| No JSON schema published | None | Publish schema at `standards.nc.art/certificate/schema/v1.json` (static file) |
| Curator is anonymous desk | `trust.ts:130–163` | Replace `TrustCurator` records with named individuals |
| Certificate covers Earthrise only | `trust.ts:3–18` | Extend to 5 signature collections in Sprint 1 |
| No API endpoint | `services/api/routers/` | `GET /certificates/{id}` route required for NC-COAS conformance |

**Activation verdict: PARTIAL IMMEDIATE**

The Earthrise certificate can achieve NC-COAS partial conformance within 48 hours
with 3 targeted fixes: statutory rights language, ISO conservation block, and
permanence commitment — all in `trust.ts` and `certificate/page.tsx`. Full
conformance requires named curator + API endpoint.

**Blocking item for full conformance:** Named curator. Without a named individual
as the curator, the curatorStatement is institutional not personal, which fails the
NC-COAS curator field requirement.

---

### NC-ERS — Edition Registry Standard

**Built:** `/registry` page live. `editionRegistry` array in trust.ts. 2 editions
registered (museum giclee + digital download). Verify page shows editions correctly.

**Current fields present:** registryId, title, format, editionType, status, certificateId,
sourceIdentifier.

**Gaps against NC-ERS v1.0:**

| Gap | File | Specific fix |
|---|---|---|
| No `editionSize` field | `trust.ts:20–39` | Add `editionSize: number \| null` to each registry record |
| No `editionStatus` (open/closed/retired) | `trust.ts:20–39` | Add `editionStatus: "open" \| "closed" \| "retired"` |
| No permanence commitment | `registry/page.tsx` | Add one paragraph permanence statement |
| No public API (static data only) | `services/api/routers/` | `GET /editions/{id}` and `GET /editions/{id}/status` — Sprint 1 |
| Physical mark not documented on page | `registry/page.tsx` | Add "Physical editions carry pencil edition mark" note |
| No closure procedure published | None | Publish closure procedure — can be a section on registry page |
| Editions cover Earthrise only | `trust.ts:20–39` | Extend to 5 signature collections in Sprint 1 |

**Activation verdict: PARTIAL IMMEDIATE**

Two field additions to `trust.ts` (`editionSize` and `editionStatus`) and a
permanence paragraph on the registry page bring NC-ERS to partial conformance
within hours. The edition sizes for Earthrise products should be defined and locked
immediately — this is both an NC-ERS requirement and a commercial governance
requirement (edition sizes must be locked before any product goes on sale).

**Blocking item for full conformance:** API endpoint. The static trust.ts data
cannot serve as a compliant NC-ERS registry — it requires `GET /editions/{id}/verify`
as a persistent queryable endpoint.

---

### NC-PDPS — Public Domain Provenance Standard

**Built:** `publicProvenanceChain` (5 steps) in trust.ts, displayed on verify page.
`provenanceGlance` (5 label/value items) on collection pages. Rights string exists in
governed-content.ts.

**Current chain:** Source record → Rights basis → Collection record → Certificate record
→ Edition registry. This is a 5-step *display* chain, not the 6-link *documentation*
chain defined by NC-PDPS.

**Gaps against NC-PDPS v1.0:**

| Gap | File | Specific fix |
|---|---|---|
| Chain structure is display-oriented, not NC-PDPS 6-link | `trust.ts:196–222` | Restructure to: Creator → Creation Event → Custody History → Rights Status → Source Access → Commercial Activation |
| Rights string is not Class 2 statutory language | `governed-content.ts:7–8` | Current: `"Public domain — United States Government Work, 17 U.S.C. § 105"` → Required: full statute text from NC-PDPS Section 2 Class 2 |
| No ULAN IDs for creators | `trust.ts` | Earthrise: William Anders has no ULAN ID (photographer, not illustrator). N/A for Earthrise; required for Owen Jones, Roberts, Wilson, Cole in Sprint 1 |
| No custody history link (Link 3) | `trust.ts:196–222` | Add custody note: "Photograph taken by William Anders. Transferred to NASA archive immediately. No subsequent private ownership." |
| No Wayback Machine archive URL | `trust.ts` | Archive NASA source URL; add `sourceUrlArchived` field |
| No GeoNames place identifier | `trust.ts` | For Earthrise: "Lunar orbit" — GeoNames coverage limited; note in provenance |
| Provenance not on product pages | `products/earthrise/page.tsx` | Add collapsed provenance block to product page |
| Earthrise only | `trust.ts` | Extend to 5 signature collections in Sprint 1 |

**Activation verdict: REQUIRES RESTRUCTURE**

The Earthrise provenance chain needs to be rebuilt to NC-PDPS 6-link structure
(not just field additions — a structural change to `publicProvenanceChain` in
trust.ts). This is a content task (2–4 hours) not a development task for Earthrise.
The rights string upgrade is a one-line change to governed-content.ts. Wayback
archiving of the NASA source URL is a 5-minute task.

Full NC-PDPS conformance for the 5 signature collections (Owen Jones, Roberts, Wilson,
Cole, Rakuchū-rakugai-zu) requires ULAN research, custody history documentation, and
institution URL archiving — a Sprint 1 content and research task.

---

### NC-ITS — Institutional Transparency Standard

**Built:** `/institutions` and `/institutions/[slug]` pages live. `trustInstitutions`
array in trust.ts. Per-institution display pages working.

**Current institutions listed:**
1. Nature & Culture (publishing institution)
2. NASA (source institution for Earthrise)
3. UNESCO World Heritage Centre (designation authority)
4. South Georgia Heritage Sources (vague — "expedition context")

**Gaps against NC-ITS v1.0:**

| Gap | File / Action | Specific fix |
|---|---|---|
| Wrong institutions listed | `trust.ts:78–127` | Replace with actual content institutions: NHM, NGA, Walters, CMA, Met, Europeana + retain NASA |
| No tier classification | `trust.ts` | Add `displayTier: 1 \| 2 \| 3` field to `TrustInstitution` type |
| No notification status | `trust.ts` | Add `notificationStatus: "notified" \| "not_notified" \| "pending"` field |
| No ROR IDs | `trust.ts` | Add `rorId: string \| null` field; populate from ror.org |
| No annual disclosure report | None | Draft as a static page or document; publish at `/institutions/disclosure` |
| No notification emails sent | Email task | Draft and send to NHM, NGA, Walters, CMA, Met, Europeana (NC-ITS Section 3 format) |
| No `/about/open-content` page | None | New static page — a 2-hour content task |
| "South Georgia Heritage Sources" is vague | `trust.ts:115–127` | Replace with "Natural History Museum, London" (the actual institution) |

**Activation verdict: HIGH IMMEDIATE POTENTIAL**

The institution data all exists — in NC governance documents (rights matrices, DD-*
documents). The trustInstitutions data model already has the right fields structure
(slug, name, type, role, summary, profile, collections). The fix is replacing the
wrong 4 entries with the correct 6+ entries.

This is a 2–4 hour data task: look up ROR IDs for each institution, draft institution
profile text (2 sentences each), assign tier, set notification status to
"not_notified" initially, then send emails.

**The `/about/open-content` page** is a 2-hour content task. NC-TRUST-003 defines
exactly what it should contain. No new development required.

**First annual disclosure report** can be a static markdown-rendered page covering
all current institutions, rights bases, and notification status.

---

### NC-EDRS — Educational Reuse Standard

**Built:** `educationalUsePanel` in trust.ts (title + copy + 4 use tags). Educational
panels on certificate page and verify page (display only, no downloads, no resources).

**Gaps against NC-EDRS v1.0:**

| Gap | Action | Effort |
|---|---|---|
| No educators page | Build `/educators` page | 4–6 hours development |
| No free educational download path | Add download links to educators page | 2 hours (static files) |
| No WCAG audit or accessibility statement | Commission audit; publish interim statement at `/accessibility` | 1 hour for interim statement; audit = contracted |
| No context guides | Write 5 context guides (6-section format) | 6–10 hours content work |
| No curriculum alignment | Add curriculum section to context guides | 2 hours per guide |
| No educational license application | Add 3-field form to educators page | 2 hours development |
| Educational panel text is informational, not actionable | Update panels to include download link | 1 hour |
| `educationalUsePanel.uses` are descriptions, not downloads | Replace with actual links | 1 hour |

**Activation verdict: REQUIRES DEVELOPMENT + CONTENT**

NC-EDRS is the only standard with nothing buildable today without development work.
The structural skeleton does not exist. Two parallel tracks:

Track A (content): Write 5 context guides. Can start immediately; no development dependency.
Track B (development): Build `/educators` page, add download path, publish accessibility
statement. 1-day development task.

NC-EDRS reaches minimum viable conformance when `/educators` page is live with at
least educational resolution downloads and the accessibility statement is published.

---

## Activation Tiers

Four tiers. Tier 1 can be done today. Each subsequent tier adds what the previous
tier does not yet deliver.

---

### Tier 1 — Today (hours, no new development)

Three standards reach partial conformance from existing infrastructure with targeted
data and content fixes.

**NC-COAS — 3 fixes, ~2 hours:**
1. `governed-content.ts:7–8` — Upgrade `EARTHRISE_RIGHTS` to full NC-PDPS Class 2
   statutory language:
   ```
   "This work was created by an officer or employee of the United States federal
   government as part of that person's official duties. It is not subject to
   copyright protection under 17 U.S.C. § 105 and is in the public domain."
   ```
2. `apps/web/app/certificate/page.tsx` — Add ISO conservation block before the
   rights panel: paper standard (ISO 9706), ink longevity (ISO 11798), storage
   guidance (45–55% RH, 15–20°C, UV glazing).
3. `apps/web/app/certificate/page.tsx` — Add permanence paragraph:
   *"Certificate records at Nature & Culture are permanent. In the event that this
   platform ceases operation, all certificate and edition records will be transferred
   to the Internet Archive within 90 days."*

**NC-ERS — 2 data changes + 1 page addition, ~1 hour:**
1. `apps/web/lib/trust.ts:20–39` — Add `editionSize` and `editionStatus` to each
   edition record. Museum Giclee: `editionSize: 100, editionStatus: "open"`.
   Digital Download: `editionSize: null, editionStatus: "open"` (Open Edition).
2. `apps/web/app/registry/page.tsx` — Add edition size and status to table display.
   Add permanence paragraph (same text as NC-COAS fix above).
3. Lock edition size for NC-PROD-001 at 100 prints. This decision must be ratified
   before Tier 1 is complete — edition size cannot change after the first certificate
   is issued.

**NC-ITS — Institution data replacement, ~3 hours:**
1. `apps/web/lib/trust.ts:78–127` — Replace `trustInstitutions` array content.
   Remove: UNESCO placeholder, South Georgia Heritage Sources.
   Add: NHM London (Tier 1, CC0), NGA Washington (Tier 1, CC0), Walters Art Museum
   (Tier 1, CC0), CMA Cleveland (Tier 1, CC0), Met Museum (Tier 1, CC0),
   Europeana (Tier 2, aggregator). Retain: NASA (Tier 1, US gov), NC itself.
2. Add `displayTier`, `notificationStatus`, `rorId` fields to `TrustInstitution` type.
3. Draft notification emails for all Tier 1 institutions (NC-ITS Section 3 format).
   Send within 24 hours of Tier 1 completion.

**Tier 1 gate:** The three standards reach partial conformance. Edition size is locked.
Institutional notifications are sent. The curator decision is flagged as a blocker for
Tier 2 and above.

---

### Tier 2 — This week (content tasks, no new development)

**NC-PDPS — Earthrise chain restructure, ~3 hours:**
1. `apps/web/lib/trust.ts:196–222` — Rebuild `publicProvenanceChain` from 5 display
   steps to 6 NC-PDPS links (Creator → Creation Event → Custody History → Rights
   Status → Source Access → Commercial Activation).
2. `apps/web/lib/governed-content.ts` — Upgrade all rights strings to statutory level.
3. Archive NASA source URL via Wayback Machine. Add `sourceUrlArchived` field to
   provenance chain.
4. `apps/web/app/products/earthrise/page.tsx` — Add collapsed provenance block
   matching the verify page chain.

**NC-ITS — Open content page, ~2 hours:**
1. Create `apps/web/app/about/open-content/page.tsx` — static page naming all
   source institutions, rights bases, and NC's attribution commitments. Content
   defined in NC-TRUST-003 Section for NC-ITS.

**Named curator decision (critical):**
The anonymous "desks" in `trustCurators` must be replaced with a named individual
before any standard can claim full conformance. The decision: who is the named
curator? The founder is the appropriate choice until there are others. Update
`trustCurators` in trust.ts to replace desk names with a real name, real title, and
real curatorial statement. Add ORCID if available.

**Tier 2 gate:** Named curator live on `/curators`. Earthrise provenance chain is
NC-PDPS compliant. Open content page live. All Tier 1 institution notifications sent
and status updated in trust.ts.

---

### Tier 3 — Sprint 1 (3 months, development + research)

**NC-COAS + NC-ERS — API endpoints:**
1. `services/api/routers/` — Add new `trust.py` router:
   - `GET /certificates/{certificate_id}` → certificate public record
   - `GET /editions/{edition_id}` → edition metadata
   - `GET /editions/{edition_id}/status` → open/closed/remaining count
   - `GET /certificates/{certificate_id}/verify` → boolean + edition details
2. Migrate certificate and edition data from static trust.ts to database-backed
   records. `services/api/database.py` — add `certificates` and `editions` tables.
3. Extend certificate and edition systems to 5 signature collections (Owen Jones,
   Roberts, Wilson, Cole, CMA folding screen). One certificate per product.

**NC-PDPS — Signature collection chains:**
1. Research ULAN IDs for 5 priority illustrators:
   - Owen Jones: ULAN 500010851 (confirmed)
   - David Roberts: ULAN 500028453 (confirmed)
   - Edward Wilson: research required (naturalist, may have VIAF not ULAN)
   - Thomas Cole: ULAN 500010471 (confirmed)
   - CMA: work-level provenance, not creator ULAN
2. Document custody history for each signature collection (creator → institution
   acquisition record — typically 1–2 transfers).
3. Build `provenanceChain` data structure in trust.ts for all 5 collections.
4. Archive all 5 institutional source URLs via Wayback Machine.

**NC-ITS — Annual disclosure report:**
1. Draft first annual disclosure report as a static page at `/institutions/disclosure`.
   Content: all institutions, tier, rights basis, notification sent/responded,
   works count, changes since launch. Publish within 90 days of public launch.

**NC-EDRS — Build educators infrastructure:**
1. `apps/web/app/educators/page.tsx` — Educators page with: PD explainer, free
   download links, context guide links, educational license application form.
2. Serve educational resolution JPEGs (1920px, 150dpi) at static URLs under
   `/edu/[collection-slug]-[work-slug]-edu-2026.jpg`.
3. Write context guides for 5 signature collections (6-section format, NC-EDRS
   Section 4). These can begin as static pages.
4. Commission WCAG 2.1 AA audit. Publish interim accessibility statement at
   `/accessibility` immediately (do not wait for audit completion).

**Tier 3 gate:** All 5 standards have API-backed data (not static hardcoded). NC-PDPS
6-link chains exist for 5 signature collections. Educators page live with free
downloads. WCAG audit commissioned. Named curator on all 5 collections.

---

### Tier 4 — Sprint 2 (6 months, standards publication + institutional)

**Publish standards at `standards.nc.art`:**
All five NC-TRUST-003 standard documents published as versioned static pages.
JSON schemas published (NC-COAS schema v1.0). API specifications documented.

**NC-ERS — Physical mark operations:**
Pencil edition numbering and curator initials applied to all Collector's Edition
prints before dispatch. This requires operational workflow documentation for the
print studio. No development required — a physical process.

**NC-EDRS — WCAG remediation:**
Complete remediation of all WCAG critical and serious failures from the Sprint 1
audit. Re-audit confirmation. Publish full WCAG conformance statement.

**NC-ITS — Logo permissions:**
Request written logo permission from NHM, NGA, Walters, CMA, Met. Display logos
for all that grant permission.

**NC-PDPS — Full corpus extension:**
Extend 6-link chains to all active products (beyond 5 signature collections).
URL health monitoring active (quarterly checks).

**NC-EDRS — Educational partnerships:**
Minimum 3 named educational institutions listed as NC Educational Partners.
Curriculum alignment documented for all 5 signature collections.

---

## Activation Summary

| Standard | Today | This week | Sprint 1 | Sprint 2 |
|---|---|---|---|---|
| **NC-COAS** | Partial (Earthrise, 3 fixes) | Named curator | API + 5 collections | Standards published |
| **NC-ERS** | Partial (Earthrise, 2 fixes) | Named curator | API + 5 collections | Physical marks |
| **NC-PDPS** | Blocked (chain restructure needed) | Earthrise restructure | 5 collections + ULAN | Full corpus |
| **NC-ITS** | Partial (institutions data replace) | Open content page + notifications | Annual report | Logo permissions |
| **NC-EDRS** | Not started | — | Educators page + downloads + WCAG | WCAG conformance + partners |

**The single action that unblocks the most:**

Naming a curator. It unblocks NC-COAS (curator field), NC-PDPS (Link 6 curator ID),
and the editorial credibility layer across all standards. It is not a development
task. It is a decision. Everything else in Tier 1 and Tier 2 is implementation.

---

## Open Actions

| # | Action | Standard | Tier | Effort |
|---|---|---|---|---|
| OA-1 | **Name a curator.** Update trustCurators in trust.ts with a real name. | All | T2 decision | 0 dev / decision only |
| OA-2 | Upgrade EARTHRISE_RIGHTS to full Class 2 statutory language | NC-COAS, NC-PDPS | T1 | 15 min |
| OA-3 | Add ISO conservation block to `/certificate` page | NC-COAS | T1 | 30 min |
| OA-4 | Add permanence paragraph to `/certificate` and `/registry` | NC-COAS, NC-ERS | T1 | 30 min |
| OA-5 | Add `editionSize` and `editionStatus` to trust.ts editionRegistry | NC-ERS | T1 | 30 min |
| OA-6 | **Lock NC-PROD-001 edition size at 100.** Governance decision. | NC-ERS | T1 | Decision only |
| OA-7 | Replace trustInstitutions with NHM, NGA, Walters, CMA, Met, Europeana, NASA | NC-ITS | T1 | 3 hrs |
| OA-8 | Add displayTier, notificationStatus, rorId to TrustInstitution type | NC-ITS | T1 | 1 hr |
| OA-9 | Draft and send institutional notifications to all Tier 1 institutions | NC-ITS | T1 | 2 hrs |
| OA-10 | Rebuild publicProvenanceChain to NC-PDPS 6-link structure | NC-PDPS | T2 | 3 hrs |
| OA-11 | Archive NASA source URL via Wayback Machine | NC-PDPS | T2 | 15 min |
| OA-12 | Add collapsed provenance block to `/products/earthrise` | NC-PDPS | T2 | 1 hr |
| OA-13 | Build `/about/open-content` page | NC-ITS | T2 | 2 hrs |
| OA-14 | Add trust.py router to API (4 endpoints) | NC-COAS, NC-ERS | T3 | 1 day |
| OA-15 | Research ULAN IDs for Wilson, Cole; confirm Owen Jones/Roberts | NC-PDPS | T3 | 2 hrs |
| OA-16 | Document custody history for 5 signature collections | NC-PDPS | T3 | 4 hrs |
| OA-17 | Build `/educators` page with PD explainer + free downloads | NC-EDRS | T3 | 1 day |
| OA-18 | Commission WCAG 2.1 AA audit + publish interim `/accessibility` statement | NC-EDRS | T3 | 1 hr interim |
| OA-19 | Write 5 context guides (6-section format) | NC-EDRS | T3 | 8 hrs |
| OA-20 | Publish all 5 standards at standards.nc.art | All | T4 | 1 day |

---

## The Critical Path

```
Decision: Name a curator  ──────────────────────────────────────────────────┐
                                                                             │
OA-2/3/4 (certificate fixes) ──────────────────────────────────────────────┤
OA-5/6 (edition size + lock) ────────────┐                                  │
OA-7/8/9 (institutions replace + notify) ┤                                  │
                                         │                                  ▼
OA-10/11/12 (provenance restructure) ────┤ ─────── Tier 2 complete ─── NC-COAS partial
OA-13 (open content page) ───────────────┘         NC-ERS partial          │
                                                    NC-PDPS partial     Named
OA-14 (API trust router) ─────────────────┐        NC-ITS partial     curator
OA-15/16 (ULAN + custody history) ────────┤                                │
OA-17/18/19 (educators page + guides) ────┤ ─────── Tier 3 complete ──────-┘
OA-20 (publish standards) ─────────────── ┘        All 5 standards
                                                    partial→full
```

The critical path is not technical. The first two gating items — naming a curator
and locking NC-PROD-001's edition size — are decisions, not implementation tasks.
Both can be made today. Every technical item in Tier 1 and Tier 2 can ship within
the same week those decisions are made.

---

*NC-STANDARDS-001 · v1.0 · 2026-06-13 · DRAFT — pending ratification*
