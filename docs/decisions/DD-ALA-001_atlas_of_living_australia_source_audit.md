# DD-ALA-001: Atlas of Living Australia — Source Audit Decision

**Type:** Decision Document — Institution Source Audit  
**Status:** DRAFT — Pending Ratification  
**Authority:** Institution Factory Constitution v1 (IFC-1–IFC-12), NC Strategic Directive, Illustration Opportunity Doctrine  
**Date Drafted:** 2026-06-10  
**Drafted By:** NC Principal Architect  

---

## DECISION

**DISQUALIFIED**

The Atlas of Living Australia (ALA) is disqualified as a production source for the NC commercial illustration pipeline. Three independent disqualifiers are each individually sufficient. The decision is not close. No reinstatement path exists under current NC doctrine.

---

## I. INSTITUTION PROFILE

**Institution:** Atlas of Living Australia  
**URL:** https://www.ala.org.au/  
**Type:** National biodiversity data aggregator / GBIF Australian node  
**Operator:** NCRIS (National Collaborative Research Infrastructure Strategy), hosted by CSIRO  
**Established:** 2010  
**Scale:** 100M+ occurrence records, 31M+ images, 153K+ species profiles  
**Geographic scope:** Primarily Australia; limited Pacific  

ALA is Australia's national biodiversity informatics infrastructure. It aggregates occurrence records, specimen data, species profiles, images, sounds, and environmental layers from museums, herbaria, government agencies, research institutions, and citizen scientists. ALA is the Australian node of GBIF (Global Biodiversity Information Facility) and shares ingestion pipeline infrastructure with GBIF.

---

## II. AUDIT FINDINGS

### II.1 Content Type Assessment (Primary Disqualifier)

**ALA is an occurrence database. It is not a historical illustration source.**

NC's Illustration Opportunity Doctrine defines the commercial object as a 1750–1900 golden-age natural history plate — Audubon, Gould, Merian, Redouté, Lear, Nodder, Haeckel, Wolf class content. ALA's holdings are:

| Category | Volume | Type |
|---|---|---|
| Field observations | ~72 million | GPS-tagged citizen-science sightings |
| Preserved specimens | ~13.5 million | Museum/herbarium specimen records |
| Machine observations | ~1.7 million | Sensor/acoustic data |
| eDNA records | ~1.17 million | Molecular occurrence data |
| Images | ~31 million | Citizen-science field photographs |

The image corpus is dominated by iNaturalist Australia (~24.9 million of 31 million images) — live-organism field photographs taken on mobile devices from 2010 onward. The Australian Plant Image Index (APII, ~28,000 images) is cited as a plant photograph collection, not a historical plate collection.

**No confirmed pre-1900 botanical illustration content.** ALA holds digitized specimen records dating to the late 17th century, and has transcribed ~800,000 specimen labels and ~124,000 pages of field notes. These are occurrence records and label images attached to preserved specimens — not stand-alone botanical illustration plates. No collection comparable to the Biodiversity Heritage Library, NHM Biodiversity Heritage Library content, BnF / Gallica natural history holdings, or any Audubon/Gould-class plate library was identified within ALA's scope.

**Verdict on content type: MISS.** ALA's content does not overlap with NC's Illustration Opportunity Doctrine. This disqualifier alone is sufficient and is doctrine-level, not configuration-level.

### II.2 Rights and Commercial Use (Second Disqualifier)

**Policy URL:** https://www.ala.org.au/terms-of-use/  
**Licensing documentation:** https://support.ala.org.au/support/solutions/articles/6000197133-what-licence-should-i-use-

ALA uses a per-record / per-dataset licensing framework. Three license types are accepted:

| License | Commercial Use | Volume (images) |
|---|---|---|
| CC0 | Permitted | Not separately quantified |
| CC BY 4.0 | Permitted (with attribution) | ~3.3 million images |
| CC BY-NC 4.0 | **Prohibited** | ~20.3 million images |
| CC BY-NC-SA 4.0 | **Prohibited** | ~1.5 million images |
| Unrecognized / unlabeled | Unknown | ~4.3 million images |

**CC BY-NC is the majority license.** Approximately 66%+ of ALA images carry a non-commercial restriction. The unrecognized subset (14%) is indeterminate. Only the CC BY 4.0 subset (~10%) is confirmed commercially usable.

**Default grant is non-commercial.** The ALA ToS provides that contributors who do not designate an explicit license grant ALA a non-exclusive worldwide license for *non-commercial purposes*. There is no confirmed default-to-CC0 policy for unlicensed records.

**GBIF channel does not change this.** GBIF does not impose a CC0 mandate on published datasets (this mandate applies only to BID/BIFA-funded programme datasets, which ALA is not). CC BY-NC ALA records remain CC BY-NC when accessed via GBIF. The GBIF-ALA shared pipeline infrastructure does not alter per-record license designations.

**IFC-1 analysis:** Even if NC were to filter aggressively for only CC BY 4.0 records, the usable fraction (~10%) consists of modern citizen-science photographs (not golden-age illustration content), contains no confirmed IIIF delivery, and yields no NC-aligned commercial illustration product. IFC-1 would formally pass for that subset, but the content would fail the Illustration Opportunity Doctrine independently.

**Verdict on commercial use: BLOCKED for majority. Usable minority is wrong content type.**

### II.3 IIIF and Image Delivery (Third Disqualifier)

**IIIF support: Not confirmed.**

ALA images are served via the ALA Image Service (https://images.ala.org.au/) as direct JPEG URLs. No IIIF Image API endpoint and no IIIF Presentation API manifest delivery were identified in any ALA documentation reviewed.

NC's architecture requires IIIF Image API delivery for all image content entering the media pipeline. Every current and planned NC institution (Europeana, Rijksmuseum, Met, AIC, CMA, SMK, NGA, Yale, Getty) either provides IIIF natively or has a confirmed IIIF-adjacent delivery path. ALA has no equivalent.

Without IIIF, NC cannot build `representative_media_url` via the standard `{service}/full/!1024,1024/0/default.jpg` tile pattern, cannot serve tiled deep zoom for the product experience, and cannot build a standards-compliant technical metadata record (`media_technical_metadata`) for any ALA image.

**Verdict on IIIF: INCOMPATIBLE with NC architecture.**

### II.4 Additional Risk Factors (Informational)

**No-endorsement clause:** The ALA ToS explicitly states that links to ALA "should not suggest that your website, organisation or services/products are endorsed by the Atlas." This is a standard clause that would require care in any NC product page attribution wording. This is not a disqualifier but is a live constraint for any future reinstatement scenario.

**Indigenous data and CARE principles:** ALA is actively implementing Traditional Knowledge (TK) Labels in collaboration with Local Contexts and has adopted ICIP (Indigenous Cultural and Intellectual Property) protocols via Terri Janke & Company. Specific access restrictions or commercial prohibition language for TK-labeled records were not confirmed in publicly accessible ToS text as of this audit date. The program is in scoping/development phase. This is a **latent risk that would require assessment in any future reinstatement scenario** — TK-labeled records may carry consent-based commercial restrictions that do not map cleanly to standard CC license terms.

**Attribution and DOI requirements:** ALA auto-generates download DOIs and expects citation in derived works. Per-record attribution to data providers is required. This is consistent with CC BY practice and is not a disqualifier, but the per-provider attribution chain is more complex than single-institution attribution (e.g., Getty's simple "Digital image courtesy of Getty's Open Content Program").

---

## III. COMPARATIVE ANALYSIS

| Criterion | ALA | Getty (Approved) | Gallica (Disqualified) |
|---|---|---|---|
| Content type | Occurrence data / field photos | Historical paintings, manuscripts, botanical prints | Historical natural history prints, maps |
| Golden-age illustration content | None confirmed | Van Huysum, Merian holdings | Buffon, Lamarck, Réaumur holdings |
| Dominant license | CC BY-NC (~66%) | CC0 (per-record, 100% of open content) | PD (but ToS license fee) |
| IIIF | No | Yes (v2) | Yes (v2.1) |
| Commercial use permitted | No (majority) | Yes (all open content) | No (ToS commercial fee) |
| NC doctrine fit | Wrong content type | Correct content type | Correct content type |

ALA's disqualification differs structurally from Gallica's (DD-GALLICA-003). Gallica was disqualified solely on ToS commercial restriction — its content was correct type and high NC priority, and a reinstatement path exists if BnF grants a commercial licence. ALA is disqualified on content type alone, independent of any licensing consideration. Even if ALA were entirely CC0 and IIIF-enabled, it would not be a NC content source under current doctrine.

---

## IV. DISQUALIFICATION ARTICLES

**Article 1 — Disqualification**  
The Atlas of Living Australia is DISQUALIFIED as a production source for the NC commercial illustration pipeline. The disqualification is based on three independent findings, each individually sufficient.

**Article 2 — Content Type Disqualifier (Doctrine-Level)**  
ALA is a biodiversity occurrence aggregator. Its image holdings are predominantly citizen-science field photographs from 2010 onward (iNaturalist Australia). No confirmed pre-1900 botanical illustration content, natural history plate collection, or golden-age illustration holdings exist within ALA's scope. ALA does not produce Illustration Opportunities under NC's Illustration Opportunity Doctrine.

**Article 3 — Commercial License Disqualifier (IFC-1 Structural)**  
The majority of ALA's image corpus (~66%) carries CC BY-NC 4.0, which prohibits commercial use. The ALA default grant for unlicensed content is non-commercial. The GBIF channel does not alter per-record license designations. IFC-1 cannot be satisfied at scale.

**Article 4 — IIIF Disqualifier (Architecture-Level)**  
ALA does not provide IIIF Image API or Presentation API delivery. Direct JPEG URL delivery is incompatible with NC's technical architecture and media pipeline standards.

**Article 5 — No Reinstatement Path**  
Unlike Gallica (DD-GALLICA-003), there is no reinstatement condition that would bring ALA within NC's production scope. The content type disqualifier is not addressable — ALA would need to become a different institution. No reinstatement condition is established.

**Article 6 — GBIF Ruling**  
ALA records accessed via GBIF carry the same per-record license as the source record. GBIF access does not convert CC BY-NC records to CC0 or CC BY. GBIF is confirmed not viable as an ALA license-laundering channel.

**Article 7 — Indigenous Data Risk Note**  
ALA's development of Traditional Knowledge Labels and ICIP protocols introduces a latent commercial restriction risk for TK-labeled records. If NC were to reconsider ALA in a future audit under a substantially different doctrine, this risk would require formal assessment. This article does not affect the current disqualification.

**Article 8 — Future Biodiversity Data Sources**  
This disqualification is specific to ALA. Other biodiversity data sources that hold confirmed historical illustration content (e.g., Biodiversity Heritage Library, NHM Natural History Museum Biodiversity Heritage Library content, JSTOR Global Plants plate scans) are addressed by their own DD process and are not governed by this decision.

---

## V. RISK REGISTER

| ID | Risk | Notes |
|---|---|---|
| R-1 | Future ALA direction changes content scope | ALA could integrate BHL-class content. No evidence of this; not actionable. |
| R-2 | TK Labels evolve to restrict export of certain records | Relevant only in a future reinstatement scenario; latent only. |
| R-3 | iNaturalist Australia expands historical digitization scope | Not in current roadmap. Citizen-science scope will not produce golden-age plates. |

---

## VI. RATIFICATION TABLE

| Role | Approval | Date |
|---|---|---|
| Principal Architect | ☐ PENDING | — |
| Governance Review | ☐ PENDING | — |

---

*DD-ALA-001 drafted 2026-06-10 under authority of Institution Factory Constitution v1 and NC Illustration Opportunity Doctrine.*  
*Comparative precedent: DD-GALLICA-003 (ToS disqualification), DD-GETTY-001 (approved: correct content type + CC0).*
