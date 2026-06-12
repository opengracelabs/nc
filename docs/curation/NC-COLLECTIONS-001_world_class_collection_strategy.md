# NC-COLLECTIONS-001: World-Class Collection Strategy

| Field | Value |
|---|---|
| Document | NC-COLLECTIONS-001 |
| Title | World-Class Collection Strategy |
| Date | 2026-06-12 |
| Status | **DRAFT** |
| Authority | NC-PLATFORM-001 · NC-AI-001 · NC-PRODUCT-001 · NC-WEB-001 |
| Reference Models | National Geographic Store, Smithsonian Store, MoMA Store, Rijksmuseum Shop, Patagonia |

---

## 1. Goal

Design the most desirable public-domain collection business possible. 

The strategy is built on the transformation of "raw" public-domain assets (NASA, NOAA, GBIF, BHL, NARA) into "governed" high-end lifestyle, educational, and collector products. We move beyond generic "merch" by grounding every product in deep storytelling, scientific authority, and archival provenance.

---

## 2. Infrastructure: The Three Pillars

To scale desirability and authority, the strategy utilizes three core infrastructure components:

### 2.1 Grounded AI
AI is the instrument of scale for storytelling. It generates "Grounded" content (product copy, educational modules, place-based stories) that is strictly cited and constrained by canonical facts.
- **Rule:** AI never determines rights or provenance; it only synthesizes advisory copy from the Authority Registry.
- **Output:** National Geographic-quality editorial modules for every product.

### 2.2 Authority Registry
The canonical truth source for the ecosystem. It stores verified identities for Places (GeoNames), Taxa (GBIF), and Institutions (Wikidata).
- **Rule:** Every product is "anchored" to a registry record.
- **Value:** Provides the "Archival Trust" required to compete with the Smithsonian or Rijksmuseum stores.

### 2.3 Product Engine (Product Runtime)
The automation layer that maps governed assets to physical and digital product families.
- **Logic:** `Asset + Place + Story + Rights -> Product Profile -> Shopify Listing`.
- **Fulfillment:** Automated routing to Gelato (prints), Lulu (books), and digital delivery systems.

---

## 3. Scaling Strategy

### 3.1 100 Products: The Flagship Tier (Manual + Grounded AI)
Focus on the "Masterwork" assets of Earthrise, Yellowstone, and Grand Canyon.
- **Approach:** Hand-curated selection of the top 100 "Asset Zero" images.
- **Copy:** High-touch human-reviewed Grounded AI stories.
- **Goal:** Establish the brand aesthetic (Apple/Nat Geo vibe).

### 3.2 1,000 Products: The Regional Tier (Semi-Automated)
Expansion to GBR, Galápagos, Venice, and Papahānaumokuākea.
- **Approach:** Authority-led batching. Use the Authority Registry to identify all high-relevance assets for a place (e.g., all 19th-century Haeckel corals for GBR).
- **Copy:** Template-driven Grounded AI with batch human QA.
- **Goal:** Create "Long-Tail" desirability across diverse scientific and cultural niches.

### 3.3 10,000 Products: The Ecosystem Tier (Product Engine Automation)
The "Airbnb of Public Domain."
- **Approach:** Full Product Engine automation. Use relationship paths (Recursive CTEs) to link every taxon in the GBIF registry to historical illustrations in the BHL.
- **Copy:** Fully automated, self-validating Grounded AI modules.
- **Goal:** Comprehensive coverage of the natural and cultural world.

---

## 4. Product Tiers (Per Collection)

For every collection, we maintain a consistent hierarchy of desirability:

| Tier | Description | Example |
|---|---|---|
| **Hero** | Masterwork items, high-premium, signed/numbered. | "Heritage Edition" framed archival Earthrise print. |
| **Entry** | Accessible "Discovery" items. | Postcards, stickers, digital "Overview Effect" packs. |
| **Premium** | High-end materials and archival focus. | Linen-bound field guides or museum-grade canvas. |
| **Collector** | Curated sets for deep enthusiasts. | "The Darwin Forge" folio (Galápagos). |
| **Educational** | Focus on knowledge and scientific evidence. | Annotated species posters (GBIF/Haeckel). |
| **Tourism** | Place-native Waypoint guides. | "Grand Canyon: The Geology of Time" trail map. |
| **Conservation** | Products linked to active conservation stories. | "Reef Witness" series (GBR Bleaching documentation). |

---

## 5. Collection Deep Dives

### 5.1 Earthrise Collection (Cosmic Anchor)
- **Story:** The Overview Effect. Humanity's first view of its fragile home.
- **Hero:** Heritage Edition Print (NASA Ektachrome Remaster).
- **Educational:** "Planetary Nature" module for schools.
- **Conservation:** Overview Effect awareness program.

### 5.2 Yellowstone Collection (Geothermal Power)
- **Story:** The world's first National Park. Fire, ice, and ancient geology.
- **Hero:** "The Fire Hole" large-scale archival print.
- **Tourism:** Waypoint guide to the Geyser Basins.
- **Educational:** Volcanology and thermal biology posters.

### 5.3 Grand Canyon Collection (The Library of Time)
- **Story:** Two billion years of Earth's history exposed in stone.
- **Hero:** Panoramic "Greatest Earth Work" print.
- **Entry:** "Layers of Time" postcard set.
- **Collector:** High-resolution USGS historical map folio.

### 5.4 Great Barrier Reef Collection (The Marine Mosaic)
- **Story:** The largest living structure. A miracle of regeneration and a witness to climate change.
- **Hero:** Haeckel's "Hexacoralla" Masterwork series.
- **Conservation:** "Climate Witness" prints (bleaching event documentation).
- **Educational:** Coral anatomy and reef biodiversity posters.

### 5.5 Galápagos Collection (The Darwinian Forge)
- **Story:** Evolution in action. The bridge between the Old World and modern science.
- **Hero:** Seba's "Giant Tortoise" (1734) archival print.
- **Collector:** The "Evolutionary Record" box set (Tortoises, Finches, Iguanas).
- **Educational:** "How Science Works" module for students.

### 5.6 Venice Collection (The Cultural Waterfront)
- **Story:** Human heritage and the rising sea. The Golden Age of Venice.
- **Hero:** Canaletto's "Grand Canal" hyper-realistic print.
- **Tourism:** "The Sun of Venice" historical walking map.
- **Conservation:** "The Future of Heritage" climate-waterfront series.

### 5.7 Papahānaumokuākea Collection (The Remote Frontier)
- **Story:** The world's largest protected area. Pristine sea and spiritual connection.
- **Hero:** "The Albatross Vista" panoramic print.
- **Educational:** Marine sanctuary and ocean conservation posters.
- **Tourism:** Digital-only "Remote Waypoint" discovery journey.

---

## 6. Execution acceptance Criteria

1. Every product is grounded in a verified Authority Registry ID.
2. AI-generated copy passes the "Prohibited Phrases" and "Attribution Verification" gates (NC-AI-001).
3. Product pricing reflects the "MoMA Store" premium quality, not a generic print-on-demand store.
4. The Product Engine can generate a draft Shopify listing with NC IDs preserved in metafields.

---
*NC-COLLECTIONS-001 v1.0 — drafted 2026-06-12.*
