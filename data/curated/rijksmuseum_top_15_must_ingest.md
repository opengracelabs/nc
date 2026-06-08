# Rijksmuseum Top 15 "Must Ingest" Collection

**Role:** Chief Curator  
**Objective:** Finalize the 15 highest-priority assets from the Rijksmuseum for immediate ingestion into the Nature & Culture platform.

---

## 1. The Rijksmuseum "Prime" Assets

| Rank | ID | Title | Creator | Flagship | Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Asset 0** | **RM-001** | *Kinkaku-ji in Snow* | Hiroshige | **Kyoto** | **Atmospheric Genesis.** Defines "Sacred Stillness." |
| **Asset 1** | **RM-006** | *Giant Tortoise (Thesaurus)* | Albertus Seba | **Galápagos** | **Scientific Authority.** Bridges Old World & Darwin. |
| **Asset 2** | **RM-004** | *Stone Garden, Kyoto* | Saitō Kiyoshi | **Kyoto** | **Modern Aesthetic.** Validates Minimalist UI. |
| **4** | **RM-005** | *Bison Americanus* | Aert Schouman | **Yellowstone** | **Biological Soul.** Anchors 19th C fauna. |
| **5** | **RM-007** | *Coral Reef Mosaic* | Albertus Seba | **G.B. Reef** | **Marine Architecture.** Foundational reef record. |
| **6** | **RM-002** | *Kiyomizu-dera (Kyoto)* | Hiroshige | **Kyoto** | **Architectural Anchor.** Essential site discovery. |
| **7** | **RM-009** | *Metamorphosis Plate* | Maria Merian | **General** | **Scientific Proof.** Validates observation layers. |
| **8** | **RM-010** | *Map of the West Indies* | Johannes Blaeu | **General** | **Cartographic Base.** Navigational trust. |
| **9** | **RM-003** | *Arashiyama: Cherry Blossoms* | Hiroshige | **Kyoto** | **Seasonal Fluidity.** Defines Sakura theme. |
| **10** | **RM-012** | *Japanese Iris (Siebold)* | Kawahara Keiga | **Kyoto** | **Botanical Authority.** Dejima-era precision. |
| **11** | **RM-008** | *Tropical Fish Collection* | Albertus Seba | **G.B. Reef** | **Vibrant Detail.** Color-health benchmark. |
| **12** | **RM-011** | *Bear Study (Natural History)* | Seba / Schouman | **Yellowstone** | **Fauna Depth.** Grizzly narrative anchor. |
| **13** | **RM-015** | *Ryoan-ji: The Sand Garden* | Saitō Kiyoshi | **Kyoto** | **Zen Texture.** Infinite Zoom test case. |
| **14** | **RM-013** | *Machu Picchu Region (VOC)* | Anonymous | **M. Picchu** | **Discovery Base.** 18th C Andean cartography. |
| **15** | **RM-014** | *Half Dome / Sierra Proxy* | Early Exploration | **Yosemite** | **Perspective Bridge.** European views of Yosemite. |

---

## 2. Rationale for Asset Zero, One, and Two

### Asset Zero: RM-001 (*Kinkaku-ji in Snow*)
**Why First:** The Rijksmuseum's Japanese collection is its most unique contribution to the Nature & Culture vision. This masterpiece establishes the **Kyoto Flagship** with immediate atmospheric impact. It validates the "Zen Motion" UI theme and the shift from natural history (BHL) to cultural-natural intersections.

### Asset One: RM-006 (*Giant Tortoise*)
**Why Second:** This asset establishes **Scientific Trust**. By using an 18th-century Dutch record to describe a Galápagos icon, we prove that Nature & Culture is an archive of global exploration history, not just local observation. It is the primary test case for linking 1734 metadata to modern Darwin Core IDs.

### Asset Two: RM-004 (*Stone Garden, Kyoto*)
**Why Third:** This asset validates **Modern Aesthetic Fidelity**. Saitō Kiyoshi’s 1955 woodcut uses texture and negative space to define a new type of digital luxury. It is the perfect asset to test "Zero-UI" transitions and high-contrast atmospheric luminescence.

---

## 3. Launch Ingestion Rule
The **Rijksmuseum Ingestion Worker** is directed to target these 15 IDs as the first production set. All must be fetched in high-resolution (TIFF/JP2) via the RijksStudio API and mapped to the `nc:must_ingest` status in PostgreSQL.

---

**Next Steps:**
- Initiate ingestion for **Asset Zero (RM-001)**.
- Verify the **CC0 1.0 Universal** license for the entire Top 15.
- Generate the **IIIF Manifest for Asset Zero** to test the Kyoto Sacred Garden experience.
