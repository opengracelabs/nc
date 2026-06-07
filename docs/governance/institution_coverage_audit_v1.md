# Institution Coverage Audit v1

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Ratified — Director Decision required for Must Add institutions |
| Repository | opengracelabs/nc |
| Drafted | 2026-06-07 |
| Ratified | 2026-06-07 |
| Role | Principal Architect |

---

## Executive Summary

The current 14-institution target portfolio is **insufficient** to support NC's long-term
mission as the world's place-centered public domain heritage commerce platform.

**The core problem is geographic.** NC's mission is place-centered, but the current
portfolio covers roughly 35% of the world's geography by land mass and approximately
20% of the world's most commercially significant tourism destinations. The entire
African continent, the Asia-Pacific region, Latin America, and the Pacific have no
direct institutional source coverage. A place-centered platform cannot build
compelling place pages — and therefore cannot build commerce — for the majority of
the world's UNESCO World Heritage Sites.

**Three structural problems in the current portfolio:**

1. **Three institutions are misclassified as content sources.** Wikidata, Europeana,
   and DPLA are not content institutions — they are an identity authority, an
   aggregator, and an aggregator, respectively. Treating them as content sources
   obscures real gaps.

2. **The natural history tier has a critical hole.** The Natural History Museum London
   (NHM) — one of the two or three most important natural history collections in the
   world — is absent. Without NHM, NC cannot adequately cover pre-1900 natural history
   illustration for Africa, Asia, Australia, and the Pacific.

3. **The text/book pipeline has no preservation infrastructure.** HathiTrust is the
   dominant PD-determination infrastructure for digitized books. Its absence means
   NC has no scalable Phase 2 (book, ebook) pipeline.

**Verdict by gap type:**

| Gap type | Severity | Primary missing institutions |
|---|---|---|
| Geographic | Critical | NHM London, BnF/Gallica, Trove, MNHN Paris |
| Natural Heritage | Critical | NHM London, Wellcome, Naturalis |
| Cultural Heritage | Moderate | V&A, Paris Musées, Prado |
| Media | Moderate | V&A (poster), HathiTrust (books) |
| Standards | Minor | EAD (NARA), MODS (extended LOC use) |
| Preservation | Moderate | HathiTrust, NHM |

**Recommended additions:** 5 Must Add, 6 Should Add, 7 Nice to Have.

---

## Part I — Current Portfolio Assessment

### Article 1 — Structural Classification

Before assessing individual institutions, the portfolio must be divided into three
constitutional categories. Conflating them obscures real coverage gaps.

**Content Institutions** — primary sources of PD/CC0 illustrations, maps, photography,
and books that NC ingests, scores, and commercializes. These require full pipeline
adapters (source_record → media_rights → activation).

**Aggregator References** — discovery portals that aggregate content from many member
institutions. NC uses these for institution discovery and collection scoping, then
ingests directly from the member institution. They do not replace direct institutional
sources.

**Identity and Reference Authorities** — systems that provide entity identity (place IDs,
taxon IDs, person QIDs), geographic data, or classification frameworks. These are already
governed by the Standards Constitution v1.0 and the seeds in `03_seed.sql`.

**Reclassification of current portfolio:**

| Institution | Current classification | Constitutional classification |
|---|---|---|
| BHL | Content | Content Institution |
| Library of Congress | Content | Content Institution |
| Smithsonian Open Access | Content | Content Institution |
| NARA | Content | Content Institution |
| **Europeana** | Content | **Aggregator Reference — reclassify** |
| Rijksmuseum | Content | Content Institution |
| British Library | Content | Content Institution |
| NYPL | Content | Content Institution |
| **DPLA** | Content | **Aggregator Reference — reclassify** |
| Getty Open Content | Content | Content Institution |
| Met Open Access | Content | Content Institution |
| Royal Botanic Gardens Kew | Content | Content Institution |
| Internet Archive | Content | Content Institution |
| **Wikidata** | Content | **Identity Authority — already in Standards Constitution** |

After reclassification: **11 content institutions, 2 aggregator references, 1 identity
authority.**

### Article 2 — Content Institution Ratings

Each institution rated against five dimensions:

| Dimension | Key |
|---|---|
| Rights | How clean is PD/CC0 determination? A = clear, B = needs work, C = complex |
| Volume | Commercially usable PD assets for NC's mission |
| API | Quality of programmatic access |
| IIIF | IIIF Image/Presentation API support |
| Geographic reach | Which world regions does this institution cover? |

| Institution | Rights | Volume | API | IIIF | Geographic reach | NC mission fit |
|---|---|---|---|---|---|---|
| **BHL** | A | Very High | Good | Partial | Global (expeditions) | Core — primary natural history source |
| **LOC** | A | Very High | Excellent | Yes | North America + colonial | Core — maps, photography, prints |
| **Smithsonian** | A (CC0) | High | Excellent | Yes | Global (research missions) | Core — natural history + cultural |
| **NARA** | A | High | Good | Partial | North America (US government) | Important — photography, documents |
| **Rijksmuseum** | A (CC0) | High | Excellent | Yes | Netherlands + Dutch colonial | Core — Dutch Golden Age art, prints |
| **British Library** | B (mixed) | Very High | Good | Partial | Global (British Empire) | Important — complex rights management |
| **NYPL** | A | High | Good | Yes | North America + global | Important — maps, photographs, prints |
| **Getty Open Content** | A (CC0) | High | Good | Yes | Global (acquisitions) | Core — provenance-rich photography |
| **Met Open Access** | A (CC0) | Very High | Good | Yes | Global (acquisitions) | Core — art + decorative arts |
| **Kew** | B | High | Good | Partial | Global botany | Core — botanical illustration authority |
| **Internet Archive** | B | Very High | Good | No | Global | Important — books, Phase 2 pipeline |

### Article 3 — Aggregator Reference Assessment

Europeana and DPLA serve as discovery routing layers, not direct sources. Their role
in NC's architecture is:

1. **Europeana:** Use to discover which European member institutions have NC-relevant
   content. Then negotiate and ingest directly from the member institution. Europeana
   API is useful for scoping; direct institution API is the production path.
   Europeana is a Tier 1 reference institution (Media Substrate Constitution v1.2,
   Article 28) — this designation governs NC's data standards alignment, not the
   ingestion path.

2. **DPLA:** Same role — discovery routing for US content outside of the major named
   institutions. Many DPLA member institutions (state libraries, local historical
   societies) have NC-relevant PD content that NC would otherwise miss. DPLA is the
   discovery layer; the member institution is the source.

**Both aggregators remain in scope as discovery routing tools.** Neither should be
treated as a direct content source in the production ingestion pipeline.

---

## Part II — Gap Analysis

### Article 4 — Geographic Gap Analysis

NC's place-centered mission requires source content for every major place category.
The current portfolio's geographic coverage is concentrated in North America and
Western Europe. The coverage holes map directly to empty place pages.

**Current coverage by region:**

| Region | Coverage quality | Primary sources | Commercially significant places lacking coverage |
|---|---|---|---|
| North America | Strong | LOC, BHL, Smithsonian, NARA, NYPL, Getty, Met | Most covered |
| Western Europe (NL, UK, US) | Good | Rijksmuseum, British Library, NYPL | Most covered |
| France + Francophone world | Weak | Europeana (indirect only) | French Polynesia, French Guiana, Sub-Saharan Francophone |
| Iberian Peninsula + Latin America | Weak | Met/Getty acquisitions only | Amazon, Andes, Patagonia, Iberian coastline |
| Northern Europe (Scandinavia) | Thin | BHL (expedition literature) | Norwegian fjords, Lapland, Iceland |
| Sub-Saharan Africa | **None** | None | Serengeti, Okavango, Victoria Falls, Congo Basin, Cape Floristic Region |
| North Africa | Thin | BHL (expedition literature) | Sahara, Atlas Mountains, Nile Valley |
| South Asia | Thin | British Library (colonial-era) | Himalayas, Western Ghats, Sundarbans |
| Southeast Asia | **None** | None | Komodo, Raja Ampat, Mekong, Borneo, Bali |
| East Asia | **None** | None | Mount Fuji, Yangtze, Li River, Korean coastline, Mongolian steppe |
| Australia + Oceania | **None** | None | Great Barrier Reef, Blue Mountains, New Zealand fjords, Polynesia |
| Arctic + Antarctic | Thin | BHL (polar expedition literature) | Svalbard, Ross Ice Shelf (polar tourism growth area) |
| Pacific Islands | **None** | None | Galápagos, Hawaii (cultural), Fiji, Palau |
| Middle East | Thin | BHL, Getty (acquisitions) | Dead Sea, Wadi Rum, Hajar Mountains |
| Russia + Central Asia | Thin | BHL (expeditions) | Lake Baikal, Kamchatka, Altai Mountains, Caucasus |

**The geographic gap is NC's largest commercial risk.** A place page for the Serengeti,
the Great Barrier Reef, Machu Picchu, or Mount Fuji cannot be built without source
content from institutions that hold PD material for those regions.

**Top commercially significant places with zero current source coverage:**

| Place | UNESCO WHS | Tourism significance | Missing institution |
|---|---|---|---|
| Serengeti National Park (Tanzania) | Yes | Very High | NHM London, Wellcome |
| Great Barrier Reef (Australia) | Yes | Very High | Trove (NLA) |
| Galápagos Islands (Ecuador) | Yes | High | BHL has Darwin; Trove, MNHN fill gaps |
| Machu Picchu (Peru) | Yes | Very High | BnF Gallica, Biblioteca Nacional España |
| Mount Fuji (Japan) | Yes | Very High | No Japanese institution in current list |
| Angkor Wat (Cambodia) | Yes | High | BnF Gallica (French Indochina), MNHN |
| Okavango Delta (Botswana) | Yes | High | NHM London, Wellcome |
| Fiordland / New Zealand | Yes | High | Trove, NLA |
| Borneo Rainforest (Malaysia) | Yes | High | Naturalis (Dutch colonial), NHM |
| Komodo National Park (Indonesia) | Yes | High | Naturalis, NHM, BnF |

### Article 5 — Natural Heritage Gap Analysis

NC's natural heritage mission requires illustrations, maps, and photography for:
- Biodiversity hotspots
- Natural Wonder places (canyons, waterfalls, geothermal)
- Terrestrial ecosystems (tropical rainforest, savanna, alpine, polar)
- Marine environments (coral reefs, ocean, coastal)
- Geological features

**Critical missing institution: Natural History Museum London (NHM)**

The NHM is arguably the single most important missing institution. It holds:
- 80 million specimens with associated illustration records
- The Rothschild Collection (tropical birds, insects — exceptional Golden Age illustrations)
- The Walter Collection (Papuan fauna — extraordinary PD illustrations)
- Historical expeditions covering Africa, Southeast Asia, Pacific, South America
- Strong IIIF API and open licensing (CC0 on images)

BHL covers European natural history literature. Kew covers botany. The NHM fills the
non-botanical natural history gap for the tropics and southern hemisphere — the same
regions where NC has geographic gaps.

**Missing natural heritage institutions by domain:**

| Domain | Current coverage | Gap | Filling institution |
|---|---|---|---|
| Tropical bird illustration | BHL (some), Smithsonian | Pre-1900 tropical species | NHM London |
| Tropical insect illustration | BHL (some) | Golden Age entomology | NHM London, Naturalis |
| Marine/coral illustration | BHL (some) | Ernst Haeckel's Kunstformen der Natur (in current portfolio via BHL) — but tropical marine broadly | NHM, Wellcome |
| African megafauna illustration | None | Golden Age African natural history | NHM London, Wellcome |
| Southeast Asian flora | Kew (partial) | Dutch-era botanical surveys | Naturalis Biodiversity Center |
| Australian flora/fauna | None | 19th century Australian natural history | Trove (NLA), NHM |
| Geological/mineralogical illustration | BHL (some), Smithsonian | Systematic geology illustration | NHM London |
| Ethnobotany (traditional plant use) | Kew (partial) | Colonial-era ethnobotanical records | Wellcome Collection, NHM |
| Medical/scientific illustration | None | Wellcome-type material | Wellcome Collection |

**Wellcome Collection** deserves special attention. The Wellcome Library is not a natural
history institution in the traditional sense, but its CC4.0 open access collection spans:
natural history, medicine, anthropology, and social history — with extraordinary pre-1900
illustration quality. It has one of the best IIIF implementations of any institution
globally. Its material is commercially underexploited and directly relevant to NC.

### Article 6 — Cultural Heritage Gap Analysis

NC's cultural heritage mission covers: art, artifacts, architectural documentation,
ethnographic material, and printed cultural objects (posters, broadsides, ephemera).

**Gaps in the current portfolio:**

| Cultural heritage category | Current coverage | Gap | Missing institution |
|---|---|---|---|
| French fine art + Impressionism | Getty (some), Met (some) | Musée d'Orsay, Louvre holdings | Paris Musées Open Data |
| Poster art / graphic design | None specifically | Alphonse Mucha, art nouveau, travel posters | Victoria and Albert Museum |
| Decorative arts + design | Met (some), Getty (some) | Systematic decorative arts | V&A |
| Iberian / Spanish colonial art | Met (some) | Velázquez, El Greco, colonial Americas | Museo Nacional del Prado |
| Dutch colonial material (Southeast Asia) | Rijksmuseum (some) | Tropenmuseum material | Nationaal Museum van Wereldculturen |
| Japanese art + ukiyo-e | Met (some), Getty (some) | Institutional Japanese sources | No direct institution |
| Islamic geometric art + manuscripts | British Library (partial), BnF (via Europeana) | Direct institutional source | BnF/Gallica |
| Pre-Columbian and Andean heritage | Met (some), Smithsonian (some) | Latin American cultural institutions | Biblioteca Nacional de España |
| Scandinavian cultural heritage | None | Norse, Viking, Sami cultural material | No specific institution |
| Russian / Slavic cultural heritage | None | Imperial Russia artistic production | No institution |

**The poster art gap** is directly relevant to NC's Phase 1 media types (`media_type_id
= 'poster'`). The Victoria and Albert Museum has the largest and best-documented poster
collection in the world, including: travel posters, art nouveau, Art Deco, British
railway posters (pre-1928 = PD). This is a direct commercial opportunity NC cannot
access without the V&A.

### Article 7 — Media Type Gap Analysis

Assessed against the Media Substrate Constitution v1.2 Phase 1–4 framework:

**Phase 1 (image, map, photography, poster):**

| Media type | Coverage | Gap |
|---|---|---|
| Natural history illustration (image) | Good: BHL, Smithsonian, Kew, NHM (missing) | NHM London critical for tropics |
| Historic maps | Good: LOC, British Library, NYPL | BnF Gallica for French colonial maps |
| Historic photography | Good: LOC, NARA, Smithsonian, NYPL, Getty | Geographic gaps, not institution gaps |
| Poster art | **None** | V&A is the dominant PD poster institution globally |

**Phase 2 (book, ebook, audiobook):**

| Media type | Coverage | Gap |
|---|---|---|
| Digitized books | Internet Archive, British Library, BHL | **HathiTrust missing** — largest PD book aggregator |
| PD ebooks | Internet Archive | HathiTrust fills this systematically |
| Audiobooks | None | Phase 2; not urgent |

**Phase 3 (audio, film):**

| Media type | Coverage | Gap |
|---|---|---|
| Ethnographic audio | None | LOC American Folklife Center (already in portfolio via LOC) |
| Historical film | Internet Archive | LOC Motion Picture Division |
| Nature documentary | None | Phase 3; no current institution needed |

**Phase 4 (dataset, 3D):**

| Media type | Coverage | Gap |
|---|---|---|
| 3D models | Smithsonian X 3D (in portfolio) | Covered for now |
| Scientific datasets | GBIF (in seeds; biodiversity data) | Phase 4; low urgency |

**The critical Phase 1 gap is poster art.** The V&A is not just "nice to have" — it is
the institutional source for a constitutionally defined Phase 1 media type that the
current portfolio cannot support.

**The critical Phase 2 gap is HathiTrust.** Internet Archive is the current text source,
but HathiTrust has a far more systematic PD determination framework, better metadata
quality, and deeper institutional provenance for digitized books. When NC activates Phase
2, Internet Archive alone is insufficient.

### Article 8 — Standards Gap Analysis

Assessed against the Standards Constitution v1.0 governed vocabulary and the ingestion
requirements of current + recommended institutions:

| Standard | Currently in NC? | Institution requiring it | Priority |
|---|---|---|---|
| **EAD (Encoded Archival Description)** | No | NARA (finding aids), British Library (manuscripts) | Medium — needed for NARA production ingestion |
| **MODS (Metadata Object Description Schema)** | No (DC covers most) | LOC extended metadata, HathiTrust | Medium — LOC uses both DC and MODS |
| **MARC 21** | No | British Library, BnF, HathiTrust, Library of Congress | Low — DC/DCTERMS covers export layer |
| **LIDO (Lightweight Information Describing Objects)** | No | Rijksmuseum API (uses JSON), V&A, some Europeana contributors | Low — Rijksmuseum uses JSON API already |
| **VRA Core (Visual Resources Association)** | No | Some art museum collections management | Low — DC + Schema.org covers the need |
| **EML (Ecological Metadata Language)** | No | GBIF dataset downloads, DataONE | Phase 4 only — low urgency |
| **Spectrum (Collections Management Standard UK)** | No | NHM London, V&A, UK museums | Low — V&A/NHM export as DC/IIIF |
| **BnF/Gallica specific XML** | No | BnF Gallica API uses its own XML dialect + IIIF | Medium — IIIF covers image layer; BnF XML needs mapping |
| **Trove API (NLA-specific format)** | No | Trove uses Dublin Core + custom JSON | Low — DC covers it; need adapter |

**Standards additions required for Must Add institutions:**

- **EAD:** Required for NARA at production scale (finding aids for photo/document collections).
  Recommend adding EAD to the Standards Constitution as a Mapped standard.
- **MODS:** LOC production ingestion benefits from MODS for richer bibliographic metadata
  than DC allows. Recommend adding MODS as a Mapped standard.
- **BnF API profile:** BnF Gallica uses IIIF (Image API) + OAI-PMH + a proprietary JSON
  structure. The IIIF layer is already covered; need an NC adapter profile for the BnF
  metadata format.

These are three Standards Constitution amendments, not new constitutions.

### Article 9 — Preservation Gap Analysis

NC's provenance and replayability doctrine requires that source institutions have
adequate preservation infrastructure. A source institution whose digital archive is
at preservation risk creates replay risk for NC.

| Institution | Preservation status | Risk to NC |
|---|---|---|
| LOC | Excellent — NDNP, digital preservation infrastructure | Low |
| Smithsonian | Excellent — dedicated digital preservation | Low |
| NHM London (to add) | Good — national institution, UK law deposit | Low |
| British Library | Excellent — UK legal deposit library | Low |
| Rijksmuseum | Good — Dutch government backed | Low |
| BHL | Good — distributed across member institutions | Low-Medium |
| NYPL | Good — endowed institution | Low |
| **Internet Archive** | **Moderate — some infrastructure concerns, non-profit** | **Medium — watch** |
| **HathiTrust (to add)** | **Excellent — university consortium, LOCKSS** | **Low** |
| BnF/Gallica (to add) | Excellent — national library, French law deposit | Low |
| Trove/NLA (to add) | Good — Australian government backed | Low |
| Wellcome (to add) | Good — major endowed foundation | Low |
| Kew | Good — UK government backed | Low |
| **NARA** | **Good but access concerns — US government funding** | **Medium — political risk** |

**Key preservation observations:**

1. **Internet Archive:** The Internet Archive's recent legal challenges (Authors Guild v.
   Internet Archive, 2023) and financial constraints create moderate preservation risk.
   NC should not rely on Internet Archive as the sole source for any critical asset type.
   HathiTrust provides a more stable institutional preservation home for the same content.

2. **NARA:** US government funding creates political risk for long-term access to NARA
   digital collections. NC should prioritize ingesting NARA content (photography,
   government maps) while access is stable.

3. **HathiTrust:** HathiTrust's university consortium model (13 founding partners) and
   use of LOCKSS (Lots of Copies Keep Stuff Safe) makes it one of the most preservation-
   stable sources NC can access. Strongly supports the Must Add recommendation.

---

## Part III — Institution Recommendations

### Article 10 — Classification Criteria

| Classification | Criteria |
|---|---|
| **Must Add** | Fills a critical coverage gap (geographic, natural heritage, or media type gap that blocks core NC mission capabilities). Has good API access and clear PD/CC rights. Commercial upside is significant and near-term. |
| **Should Add** | Fills an important gap without which NC's mission is meaningful incomplete. Good API and rights. May require more adaptation work. |
| **Nice to Have** | Incremental improvement to existing coverage. Geographic or domain specificity. Higher adaptation cost relative to benefit. |

### Article 11 — Must Add (5 institutions)

---

**MA-1: Natural History Museum London (NHM)**

| Attribute | Value |
|---|---|
| URL | https://data.nhm.ac.uk / https://www.nhm.ac.uk/open-data |
| API | NHM Data Portal API (JSON), IIIF image service |
| Rights | CC0 on most digitized specimens and illustrations |
| Standards | Dublin Core, IIIF, Darwin Core (specimens), JSON-LD |
| Content volume | 80+ million specimens; 500,000+ illustration images in PD |

**Why Must Add:**
The NHM is the most important missing institution in NC's portfolio. It fills three
simultaneous gaps:

1. **Geographic gap:** The NHM holds the most significant collections from Africa,
   Southeast Asia, the Pacific, and Australia from the Golden Age (1750–1900) — exactly
   the regions where NC has no source coverage. Alfred Russel Wallace collections
   (Malay Archipelago), Philip Sclater collections (African birds), Richard Bowdler Sharpe
   collections (global ornithology).

2. **Natural heritage gap:** The NHM holds exceptional pre-1900 zoological illustrations
   for tropical species that BHL does not have — particularly birds, insects, reptiles,
   and marine life from the Indo-Pacific and Africa.

3. **Priority illustrator overlap:** The NHM holds original works and the primary
   institutional context for John Gould (birds) and Edward Lear (parrots) — both on
   NC's Priority Illustrator Registry. The NHM's Gould collection is the definitive
   institutional source.

**Commercial upside:** Tropical wildlife illustration from the NHM fills NC's most
commercially demanded place gap. Serengeti, Borneo, Great Barrier Reef, and New Zealand
place pages require NHM material.

---

**MA-2: Bibliothèque nationale de France / Gallica**

| Attribute | Value |
|---|---|
| URL | https://gallica.bnf.fr / https://api.bnf.fr |
| API | Gallica API (SRU/OAI-PMH + IIIF), OAI-PMH |
| Rights | PD for pre-1928 materials; CC-BY for BnF-created metadata |
| Standards | Dublin Core, IIIF Image API, OAI-PMH, UNIMARC, EAD |
| Content volume | 15+ million documents digitized; millions of PD images |

**Why Must Add:**
BnF Gallica is the single institution that most directly fills NC's French and
Francophone world geographic gaps, while simultaneously providing content for the
entire French colonial world: North Africa, West Africa, Indochina, the Caribbean,
South America (French Guiana), and the Pacific (French Polynesia).

1. **Natural history:** BnF holds the Buffon collections (Histoire Naturelle, 1749–1804
   — some of the most commercially desirable pre-Linnaean natural history illustration),
   the Lacépède fish illustrations, and de Humboldt expedition materials covering
   South and Central America.

2. **Maps:** BnF has exceptional cartographic collections covering French colonial
   territories globally — filling the mapping gap for North Africa, Indochina, West
   Africa, and the Pacific that LOC does not cover.

3. **Cultural heritage:** BnF holds Gothic and Renaissance illuminated manuscripts,
   French royal court portraiture, and Orientalist painting records — all relevant
   to NC's cultural heritage mission.

**Commercial upside:** French Polynesia (Bora Bora, Moorea), Morocco, Vietnam, and
Madagascar are major tourism destinations with zero NC source content today.

---

**MA-3: Wellcome Collection**

| Attribute | Value |
|---|---|
| URL | https://wellcomecollection.org / https://developers.wellcomecollection.org |
| API | Wellcome Catalogue API (excellent documentation, JSON/IIIF) |
| Rights | CC4.0 on most digitized content; some CC0 |
| Standards | IIIF Presentation API 3.0, Dublin Core, CALM (archives), JSON-LD |
| Content volume | 750,000+ digitized images; significant PD illustration library |

**Why Must Add:**
The Wellcome Collection is constitutionally ideal for NC: excellent API, best-in-class
IIIF implementation, generous rights (CC4.0 allows commercial use), and a collection
that spans natural history, anthropology, and cultural heritage in a way no other
single institution does.

1. **Cross-domain content:** The Wellcome holds natural history illustrations from
   global scientific expeditions, ethnographic photography from Africa and Asia, and
   social history material that connects to NC's tourism and education mission.

2. **Underexploited commercially:** The Wellcome's digitized collection is enormous
   but relatively underserved in the print-on-demand market. This creates commercial
   opportunity for NC.

3. **Rights model:** CC4.0 (Creative Commons Attribution 4.0) requires attribution
   but permits commercial use without restrictions. This is the cleanest rights
   model outside CC0. NC's pipeline handles attribution requirements.

4. **IIIF quality:** The Wellcome's IIIF implementation is among the best globally —
   high-resolution tiles, reliable manifests, strong metadata. Low technical integration
   risk.

**Commercial upside:** Wellcome's tropical medicine expedition photography (Africa,
India, Southeast Asia) and natural history illustration fills geographic gaps. High
commercial demand for Victorian natural history illustration.

---

**MA-4: Trove (National Library of Australia)**

| Attribute | Value |
|---|---|
| URL | https://trove.nla.gov.au / https://api.trove.nla.gov.au |
| API | Trove API v3 (JSON, Dublin Core), IIIF image delivery |
| Rights | PD for pre-1955 Australian materials; mixed for contributed content |
| Standards | Dublin Core, IIIF (partial), OAI-PMH, Australian MARC |
| Content volume | 400+ million items; significant digitized PD content |

**Why Must Add:**
Australia and the Pacific are the most commercially significant geographic gaps in NC's
current portfolio. Trove fills this for:

1. **Australian natural heritage:** 19th century Australian natural history expeditions
   produced extraordinary illustration material — John Gould's Birds of Australia (BHL
   has it), but also colonial-era surveys of Australian flora (Banks-Solander from Cook
   voyages, available via Trove and NHM) and landscape photography.

2. **Pacific:** Trove holds material from the Pacific — New Zealand, Melanesia, Polynesia —
   from British, French, and Australian expeditions.

3. **New Zealand content:** Te Papa Tongarewa (New Zealand national museum) contributes
   content to Trove. New Zealand's unique natural heritage (kiwi, tuatara, kauri forests)
   is a distinct commercial opportunity.

4. **Cook voyage material:** James Cook's three voyages (1768–1779) covered the Pacific,
   New Zealand, Australia, and Hawaii. The illustrations from these expeditions are PD
   and some of the most commercially compelling natural history art ever produced.
   Trove holds Australian access to this material; NHM holds UK access.

**Commercial upside:** Great Barrier Reef, Uluru, Fiordland (NZ), and Galápagos
(partial — Cook material) are globally iconic places that NC cannot currently build.

---

**MA-5: HathiTrust**

| Attribute | Value |
|---|---|
| URL | https://www.hathitrust.org / https://www.hathitrust.org/data |
| API | HathiTrust Data API, Bibliographic API |
| Rights | Systematic PD determination framework (copyright renewal records) |
| Standards | MARC, Dublin Core, IIIF (developing), JSON-LD |
| Content volume | 17+ million volumes; 7+ million PD volumes |

**Why Must Add:**
HathiTrust is not primarily a content source — it is an infrastructure institution.
Its importance to NC is specifically for Phase 2 (book, ebook) pipeline readiness.

1. **PD determination infrastructure:** HathiTrust has the most systematic US copyright
   renewal lookup infrastructure in existence. They've processed millions of copyright
   renewals to determine PD status for digitized books. NC's rights pipeline for Phase 2
   books benefits enormously from HathiTrust's existing PD determinations.

2. **Phase 2 volume:** When NC activates Phase 2, HathiTrust provides 7+ million PD
   volumes vs. Internet Archive's less systematic PD determination. For NC's
   commerce pipeline, a HathiTrust PD determination is higher confidence than an
   Internet Archive PD claim.

3. **BHL partnership:** HathiTrust and BHL share a close institutional relationship.
   Many BHL items also appear in HathiTrust. The combined coverage is essential for
   the natural history book tier.

4. **Preservation stability:** HathiTrust's university consortium model (including Michigan,
   California, Harvard, Cornell) and LOCKSS-based preservation infrastructure is among
   the most stable in the world.

**Commercial upside:** Primarily a Phase 2 infrastructure unlock. Phase 2 books and
ebooks are not in the current prototype but are constitutionally planned.

---

### Article 12 — Should Add (6 institutions)

---

**SA-1: Victoria and Albert Museum (V&A)**

| Gap filled | Phase 1 poster art; decorative arts; design |
|---|---|
| URL | https://collections.vam.ac.uk / https://api.vam.ac.uk |
| Rights | CC0 on most digitized objects |
| Priority | HIGH — fills Phase 1 media type gap (poster) |

The V&A holds the world's most important poster collection: travel posters, art nouveau
prints, Art Deco design, and British graphic arts, most of which are pre-1928 (PD) or
CC0. This fills NC's poster media type gap directly. No other institution in the current
portfolio covers this.

Secondary value: V&A decorative arts and design holdings (wallpaper, textiles, furniture
design prints) create a product category NC currently cannot serve.

---

**SA-2: Paris Musées (Paris Open Data)**

| Gap filled | French fine art; cultural heritage; Impressionism |
|---|---|
| URL | https://opendata.paris.fr/explore/dataset/musees-collections/ |
| Rights | CC0 on 300,000+ images from 14 Paris museums |
| Priority | HIGH — Musée d'Orsay, Musée Carnavalet, Petit Palais |

Paris Musées Open Collections gives CC0 access to works from the Musée d'Orsay
(Impressionism), Musée Carnavalet (Paris history), Petit Palais (classical/romantic art),
and 11 other Paris museums. These are among the most commercially demanded fine art
images in the world. The Impressionist works (Monet, Renoir, Degas) are post-1750,
many pre-1900, placing them squarely in NC's Golden Age priority range.

---

**SA-3: Naturalis Biodiversity Center (Netherlands)**

| Gap filled | Southeast Asian natural history; Dutch colonial-era illustration |
|---|---|
| URL | https://data.biodiversitydata.nl |
| Rights | CC0 on most digitized material |
| Priority | HIGH — Borneo, Indonesia, Malaysia, Papua natural history |

Naturalis in Leiden has one of the world's largest natural history collections,
including extraordinary Southeast Asian material from Dutch colonial-era expeditions
(VOC-era illustration, Rumphius herbarium, 18th century Moluccan natural history).
This fills the Borneo/Indonesia/Malaysia/Papua New Guinea natural heritage gap that
no current institution covers.

---

**SA-4: MNHN Paris (Muséum national d'Histoire naturelle)**

| Gap filled | French colonial natural history; pre-Linnaean illustration; global tropics |
|---|---|
| URL | https://www.mnhn.fr/en/digital-collections / Recolnat consortium |
| Rights | PD for pre-1928; CC licenses on MNHN-created images |
| Priority | MEDIUM-HIGH — strongest for West Africa, Indochina, Amazonia natural history |

MNHN holds the collections of Buffon, Cuvier, Lamarck, and Saint-Hilaire — four of
the most important natural history illustrators of the 18th-19th century. These are
the scientific contemporaries of NC's Priority Illustrators (Redouté was MNHN-
affiliated; Haeckel visited MNHN). MNHN also holds exceptional collections from
French colonial-era expeditions to West Africa, Madagascar, Indochina, and the
Caribbean — complementing BnF Gallica's cartographic and documentary material.

---

**SA-5: Museo Nacional del Prado**

| Gap filled | Iberian fine art; Spanish colonial-era cultural heritage |
|---|---|
| URL | https://www.museodelprado.es/en/the-collection/online-gallery |
| Rights | CC license on high-quality reproductions; many works PD |
| Priority | MEDIUM — specific to Iberian and Latin American cultural content |

The Prado's CC license (CC BY-NC-ND on most reproductions, some CC BY-SA) is more
restrictive than CC0. However, for pre-1928 works, the underlying painting is PD
regardless of reproduction rights — and the Prado does release CC0/CC-BY images for
many medieval and Renaissance works. The Prado fills the significant gap in Iberian
cultural heritage, and via the Spanish colonial connection, Latin American cultural
heritage content.

**Note:** Confirm CC0 or CC-BY rights for each item before production ingestion.
The Prado's rights model requires careful per-item verification.

---

**SA-6: Library and Archives Canada (LAC)**

| Gap filled | Canadian geographic content; Francophone North America; Arctic |
|---|---|
| URL | https://www.bac-lac.gc.ca/eng/discover/Pages/discover.aspx |
| Rights | PD for pre-1949 under Canadian copyright; some CC0 |
| Priority | MEDIUM — fills Canadian and Arctic geographic gaps |

LAC holds: surveying and expedition maps of Canada's national parks (Banff, Jasper,
Pacific Rim), early 20th century photography of the Canadian West, and Francophone
material for Quebec and New France. The Canadian Rockies, Niagara Falls (Canadian
side), and the Arctic represent commercially significant places NC cannot currently
build. LAC fills this alongside Trove's Pacific coverage.

---

### Article 13 — Nice to Have (7 institutions)

These institutions provide incremental improvement to existing coverage areas.
Each requires director evaluation before being added to the roadmap.

| # | Institution | Gap filled | Notes |
|---|---|---|---|
| NTH-1 | **Field Museum (Chicago)** | Anthropology + natural history supplement | Limited open access; primarily for ethnographic/cultural gaps |
| NTH-2 | **Biblioteca Nacional de España** | Spanish colonial maps + natural history | Strong for Americas colonial-era material; rights complex |
| NTH-3 | **Te Papa Tongarewa (New Zealand)** | Pacific and Māori cultural heritage | IIIF support; CC licensing; strong Pacific cultural content |
| NTH-4 | **Staatsbibliothek Berlin (SBB / Deutsche Fotothek)** | Central European photography + maps | Fills Germanic/Central European gap; Deutsche Fotothek has PD photography |
| NTH-5 | **Nationaal Museum van Wereldculturen (Tropenmuseum)** | Dutch colonial Southeast Asia + Africa | Colonial-era ethnographic material; complements Naturalis |
| NTH-6 | **New York Botanical Garden** | New World botany; supplements Kew | Strong for North American and Neotropical botany |
| NTH-7 | **Koninklijke Bibliotheek (National Library Netherlands)** | Dutch colonial history + Golden Age documents | Complements Rijksmuseum; primarily text/document material |

---

## Part IV — Target End-State Portfolio

### Article 14 — Proposed End-State Architecture

The target end-state divides the institutional portfolio into three tiers based on
commercial priority and mission centrality.

#### Tier 1 — Core Institutions (non-negotiable for long-term mission)

These institutions are the backbone of NC's content pipeline. Without them, NC cannot
serve its core mission scope.

| Institution | Currently targeted? | Status | Primary contribution |
|---|---|---|---|
| BHL | Yes | Seeded (active) | Natural history illustration — primary discovery source |
| Library of Congress | Yes | Seeded (proposed) | Maps, photography, prints — North America |
| Smithsonian Open Access | Yes | Not yet seeded | Natural + cultural — global research missions |
| Rijksmuseum | Yes | Not yet seeded | Dutch Golden Age — best museum API globally |
| British Library | Yes | Not yet seeded | Books, maps, manuscripts — British Empire global scope |
| Metropolitan Museum | Yes | Not yet seeded | Art + decorative arts — CC0 |
| Getty Open Content | Yes | Not yet seeded | Photography + provenance-rich art — CC0 |
| Royal Botanic Gardens Kew | Yes | Not yet seeded | Botanical illustration — global botany authority |
| **Natural History Museum London** | **No — Must Add** | **Recommended** | **Tropical natural history — Africa, Asia-Pacific, Americas** |
| **Bibliothèque nationale de France** | **No — Must Add** | **Recommended** | **French colonial world — maps + natural history** |
| **Wellcome Collection** | **No — Must Add** | **Recommended** | **Cross-domain — natural history + anthropology + social history** |
| **Trove (NLA)** | **No — Must Add** | **Recommended** | **Australia + Pacific — unique biodiversity + geography** |
| **HathiTrust** | **No — Must Add** | **Recommended** | **Phase 2 book pipeline infrastructure** |

#### Tier 2 — Important Institutions (complete the mission picture)

| Institution | Currently targeted? | Status | Primary contribution |
|---|---|---|---|
| NARA | Yes | Not yet seeded | US government photography, documents, maps |
| NYPL | Yes | Not yet seeded | Prints, photography, maps — North America |
| Internet Archive | Yes | Not yet seeded | Books, text, Phase 2/3 pipeline |
| **Victoria and Albert Museum** | **No — Should Add** | **Recommended** | **Poster art — Phase 1 media type gap** |
| **Paris Musées** | **No — Should Add** | **Recommended** | **French fine art — CC0 on Impressionism** |
| **Naturalis Biodiversity Center** | **No — Should Add** | **Recommended** | **Southeast Asian natural history** |
| **MNHN Paris** | **No — Should Add** | **Recommended** | **French colonial natural history + pre-Linnaean illustration** |
| **Museo Nacional del Prado** | **No — Should Add** | **Recommended** | **Iberian + Latin American cultural heritage** |
| **Library and Archives Canada** | **No — Should Add** | **Recommended** | **Canada + Arctic geographic coverage** |

#### Tier 3 — Strategic Institutions (geographic + domain expansion)

These are activated as NC expands into specific place categories. Not needed for the
current prototype or early commercial phases.

| Institution | Gap filled | Activation trigger |
|---|---|---|
| Field Museum | Anthropology + ethnography | When cultural anchor type is commercially active |
| Biblioteca Nacional de España | Spanish colonial Americas | When Latin America places are targeted |
| Te Papa Tongarewa | Pacific + Māori cultural heritage | When Pacific place pages are targeted |
| Staatsbibliothek Berlin | Central European photography | When Germanic place pages are targeted |
| Nationaal Museum van Wereldculturen | SE Asian colonial material | When Borneo / Indonesia / Pacific are targeted |
| New York Botanical Garden | New World botany | When North American botanical content is needed |
| Koninklijke Bibliotheek NL | Dutch history documents | When Dutch colonial places are targeted |

#### Aggregator References (reclassified — not content sources)

| Institution | Role | Production ingestion path |
|---|---|---|
| Europeana | Discovery routing for European member institutions | Ingest directly from member institutions |
| DPLA | Discovery routing for US regional institutions | Ingest directly from member institutions |

#### Identity and Reference Authorities (governed by Standards Constitution v1.0)

| System | Role |
|---|---|
| Wikidata | Entity identity (QIDs for places, creators, taxa, institutions) |
| GeoNames | Place identity and classification |
| GBIF | Taxon identity and occurrence evidence (biological anchor) |
| UNESCO WHC/ICH | Place classification and heritage designation |

### Article 15 — Portfolio Summary Count

| Category | Current | After Must Add | After Should Add | End-state (with Tier 3) |
|---|---|---|---|---|
| Tier 1 Core | 8 | 13 | 13 | 13 |
| Tier 2 Important | 3 | 3 | 9 | 9 |
| Tier 3 Strategic | 0 | 0 | 0 | 7 |
| Aggregator References | 2 | 2 | 2 | 2 |
| Identity Authorities | 1 | 1 | 1 | 1 |
| **Total content institutions** | **11** | **16** | **22** | **29** |

---

## Part V — Standards Additions Required

### Article 16 — Standards Constitution Amendments

Three amendments to the Standards Constitution v1.0 are required to support Must Add
and Should Add institutions:

**Standards Amendment SA-1: Add EAD (Encoded Archival Description) as Mapped**

Required for: NARA (archival finding aids), British Library (manuscript series),
NHM London (collection series descriptions).
Mapping target: NARA EAD finding aids → `source_record.raw_payload` + structured
`series_path` in `media_technical_metadata.content`.
Posture: **Map** (NC does not adopt EAD as internal model; maps EAD to DC/JSON-LD for
the governed source_record structure).

**Standards Amendment SA-2: Add MODS (Metadata Object Description Schema) as Mapped**

Required for: LOC production ingestion (LOC uses MODS for richer bibliographic data
than DC), HathiTrust (MODS catalog records).
Mapping target: MODS `titleInfo`, `name`, `subject`, `originInfo` → DCTERMS fields.
MODS gives NC richer creator and subject metadata than DC15 for LOC records.
Posture: **Map**.

**Standards Amendment SA-3: Add BnF Gallica API Profile as Extension**

Required for: BnF/Gallica institution adapter.
BnF Gallica uses: IIIF Image API 2.1 (minor version difference from NC's 3.0 adoption),
OAI-PMH for metadata, and a proprietary JSON API for item-level data.
NC needs an adapter profile that: (a) bridges IIIF 2.1 → 3.0 for manifests; (b) maps
BnF's OAI-PMH Dublin Core output to NC's `source_record` format; (c) governs BnF's
notice field as the provenance text.
Posture: Extend (existing IIIF adoption; new adapter profile for BnF metadata format).

---

## Part VI — Implementation Sequencing

### Article 17 — Recommended Onboarding Sequence

Institution onboarding is gated by two factors: (1) whether it fills the Yellowstone
prototype gap (near-term) or a future place gap (medium-term); and (2) adapter
complexity.

| Wave | Institution | Reason for this wave | Adapter complexity |
|---|---|---|---|
| **Wave 1** (current — Prototype) | LOC (governance activate), Smithsonian | Prototype required; existing M18 foundation | Low-Medium |
| **Wave 2** (post-prototype) | NHM London, Wellcome Collection | Natural heritage + geographic gap; excellent APIs | Medium |
| **Wave 3** | BnF/Gallica, NARA, Rijksmuseum, NYPL | Geographic expansion + cultural heritage | Medium-High |
| **Wave 4** | Met, Getty, British Library, Kew | Enrich existing North America + botanical pipeline | Medium |
| **Wave 5** | Trove, V&A, Paris Musées | Pacific geographic + poster/decorative arts media | Medium |
| **Wave 6** | Naturalis, MNHN, Library and Archives Canada | Domain depth + geographic expansion | Medium |
| **Wave 7** | Prado, HathiTrust, Internet Archive | Phase 2 pipeline preparation + Latin America | Medium-High |
| **Wave 8+** | Tier 3 institutions as place categories are targeted | As needed by place expansion roadmap | Variable |

---

## Open Questions

| OQ | Question | Recommended resolution |
|---|---|---|
| OQ-1 | Should Wikimedia Commons be upgraded from its current infrastructure-source role (seeded in `03_seed.sql`) to a content institution? | Recommended: Yes for specific collections. Wikimedia Commons has high-quality PD reproductions of institution collections (mirrored from Met, Rijksmuseum, etc.) plus unique content (user-contributed historical photography). The quality is variable. A Wikimedia Commons content profile that filters by: (a) institution-sourced CC0 images; (b) photographic metadata quality threshold; would make it a valuable supplemental source. The current seed treats it as a file source — this should remain, but a content profile should be added. |
| OQ-2 | The British Museum (London) is absent from this audit. Is it intentional? | Yes, intentional. The British Museum uses CC-BY-NC-SA licensing on most images, which prohibits commercial use. NC's pipeline requires PD or commercial-use CC licenses. The British Museum's non-commercial restriction makes it unsuitable as a NC content source. Exception: specific items in the British Museum's collection that are explicitly CC0 (some objects photographed under the Open Content policy) could be individually ingested. Recommend maintaining a watch list but not a full adapter. |
| OQ-3 | Should GBIF be reclassified from an occurrence/identity source to a potential illustration source via its integration with BHL? | No. GBIF's core value to NC is as a biological taxon identity and evidence validation source. GBIF does surface some BHL illustrations via the species pages, but these are already accessible via BHL directly. Dual-sourcing from both GBIF and BHL would create provenance complexity without adding content. Keep GBIF as an identity/validation source only. |
| OQ-4 | Japanese institutions (National Diet Library, Tokyo National Museum) are absent from all tiers. Is this the right call? | The absence is deliberate for Wave 1–4, but Japan is a top-5 tourism destination globally (Mount Fuji, Kyoto, Nara) and NC cannot build compelling place pages without Japanese institutional sources. The barrier is API accessibility (Japanese institutions often have Japanese-language APIs only) and rights complexity (Japanese copyright law differs from US). Recommend adding a Japan-specific institutional scoping project at Wave 5. Primary target: National Diet Library Digital Collections (NDL Digital), which has a JSON API and significant PD material. |
| OQ-5 | Should NC target the Pan-African Heritage World Book (PAHWB) or other African heritage initiatives for the Sub-Saharan Africa gap? | The African institutional landscape for digitized PD heritage content is thinner than other regions. The most practical near-term paths are: (1) NHM London for African natural history illustration (via British colonial expeditions — fills NC's commercial need); (2) BnF Gallica for French colonial North and West Africa; (3) The Smithsonian National Museum of African Art (already in portfolio via Smithsonian Open Access). A dedicated African institutional partner is a longer-term aspiration; the 1750-1900 Golden Age content for Africa is primarily in European institutional collections due to colonial-era collecting. |
