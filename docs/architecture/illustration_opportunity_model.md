# Nature & Culture Illustration Opportunity Doctrine

Nature & Culture is a **place-centered, public-domain illustration discovery and commerce platform**. It is not a biodiversity inventory, a taxonomic database, or an art gallery for its own sake. It is a system designed to identify, preserve, and commercialize the "Golden Age" of natural history illustration by grounding it in geographic context.

---

## 1. THE COMMERCIAL OBJECT: THE OPPORTUNITY
The primary unit of value in the system is the **Illustration Opportunity**.

*   **NOT a Species:** We do not care about species for the sake of biological completeness.
*   **NOT an Occurrence:** We do not care about raw counts of individuals.
*   **NOT a Taxon:** Taxa are merely **metadata anchors**—semantic search handles used to find the art.
*   **THE OPPORTUNITY:** A specific, high-quality, public-domain illustration (`E36 Visual Item`) that can be reliably linked to a biological concept (`E55 Type`) and then routed to every relevant place (`E53 Place`).

---

## 2. THE PIPELINE
1.  **PLACE:** A defined geography (e.g., UNESCO World Heritage Site).
2.  **TAXONOMIC CONTEXT:** Identify high-value "Illustratable" taxa (Birds, Butterflies, Orchids) historically associated with the Place.
3.  **ILLUSTRATION OPPORTUNITY DISCOVERY:** Interrogate BHL for specific plates/illustrations of those taxa.
4.  **PUBLIC-DOMAIN ASSET:** Verify rights (PD/CC0) and ingest high-resolution TIFF/JPEG into MinIO.
5.  **COLLECTION:** Group assets by Place-centered themes (e.g., "Flora of the Great Barrier Reef").
6.  **PRODUCT:** Deploy assets onto Wall Art, Calendars, Puzzles, and Books.

---

## 3. CORE PRINCIPLES
*   **Assets belong to Concepts:** One illustration of *Chelonia mydas* is stored once.
*   **Places connect to Concepts:** Many places (Galapagos, GBR, Caribbean) link to the same *Chelonia mydas* concept.
*   **Place-Centered:** The user discovery experience always begins with the **Place**. The illustration is the "gift" the place provides.

---

## 4. SELECTION & SCORING (IPS: Illustration Potential Score)
The system optimizes for **Value**, not **Frequency**. A rare endemic with a 1848 Gould plate is prioritized over a common sparrow with 50,000 GBIF records and no usable art.

### Priority 1: The Golden Age (1750–1900)
This era produces the highest quality hand-colored lithographs and copperplate engravings, with zero copyright ambiguity.

### Priority 2: Master Illustrators
*   **Aves:** Audubon, Gould, Lear, Wolf.
*   **Entomology:** Merian, Nodder.
*   **Botany:** Redouté.
*   **General:** Haeckel, Shaw.

### Priority 3: Commercial Viability
*   **High Value:** Birds, Butterflies, Marine Life, Orchids, Large Mammals.
*   **Low Value:** Microorganisms, non-distinctive fungi, plain invertebrates.

---

## 5. GOVERNANCE (FASTAPI & HUMAN-IN-THE-LOOP)
*   **Commercial Rule:** No asset enters the pipeline unless rights are explicitly verified as **Public Domain** or **CC0**.
*   **AI Role:** Advisory (Discovery, Scoring, Restoration suggestions).
*   **Human Role:** Final Approval (Aesthetic quality, "Print-Ready" verification).
*   **Authority:** PostgreSQL tracks the state of every Opportunity.
*   **Evidence:** MinIO stores the high-resolution files.

---

## 6. STANDARDS MAPPING
*   **Darwin Core (DwC):** For taxonomic anchors (`dwc:Taxon`).
*   **CIDOC CRM:** For event-centric provenance (`E36 Visual Item` -> `P62 depicts` -> `E55 Type`).
*   **SKOS:** For hierarchical concept management.
*   **Audubon Core (AC):** For image metadata and rights management (`ac:rights`).

---

## 7. ROADMAP
1.  **Migration 16:** Database update to support the `IllustrationOpportunity` entity.
2.  **Discovery:** Execute BHL searches against the prioritized UNESCO taxa hit-list.
3.  **Ingestion:** Harvest high-res assets from BHL for approved opportunities.
4.  **Collection Build:** Route assets to Place-centered commercial collections.
5.  **Product Deployment:** Launch the first "Nature & Culture" print-on-demand offerings.
