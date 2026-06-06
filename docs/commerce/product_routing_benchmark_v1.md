# Product Routing Benchmark v1.0

This benchmark provides the expected commercial routing for the core Nature & Culture asset fixtures. It defines which **Product Families** are the primary, secondary, and tertiary targets for each asset type.

---

## 1. Product Family Definitions

*   **Museum Print:** Premium archival media (Linen, Heavyweight Rag), custom sizes, individual numbering.
*   **Book:** Coffee table books, field guides, and educational folios.
*   **Calendar:** Seasonal curated sets (e.g., "Yellowstone Heritage").
*   **Puzzle:** High-complexity (1,000+ pieces) or thematic sets.
*   **Wall Art:** Standard framed prints, canvases, and posters.
*   **Cards:** High-quality stationery, postcards, and gift card sets.

---

## 2. Routing Matrix

| Asset | Museum Print | Book | Calendar | Puzzle | Wall Art | Cards | Primary Route |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Thomas Moran** | **HERO** | **HERO** | STRONG | STRONG | **HERO** | VIABLE | Museum Print |
| **Hayden Map** | **HERO** | **HERO** | VIABLE | VIABLE | **HERO** | WEAK | Museum Print |
| **W.H. Jackson** | WEAK | VIABLE | **HERO** | STRONG | STRONG | **HERO** | Calendar |
| **Audubon** | STRONG | STRONG | **HERO** | **HERO** | **HERO** | STRONG | Wall Art |
| **Haeckel** | **HERO** | STRONG | VIABLE | **HERO** | **HERO** | STRONG | Wall Art |

---

## 3. Detailed Benchmark Routing

### 3.1 Thomas Moran: *The Grand Canyon of the Yellowstone*
*   **Strategy:** "The Masterwork Anchor." Focus on the highest possible print quality.
*   **Expected Route:** Museum Print (98) > Wall Art (95) > Book (92).

### 3.2 1871 Hayden Survey Map (Yellowstone)
*   **Strategy:** "The Cartographic Foundation." Focus on scale and technical fidelity.
*   **Expected Route:** Museum Print (96) > Wall Art (92) > Book (90).

### 3.3 William Henry Jackson: *Old Faithful Geyser*
*   **Strategy:** "The Heritage Keepsake." Focus on nostalgia and historical proof.
*   **Expected Route:** Calendar (92) > Cards (88) > Wall Art (84).

### 3.4 John James Audubon: *Wildlife Series*
*   **Strategy:** "The Universal Collection." Focus on high-velocity marketplace products.
*   **Expected Route:** Wall Art (94) > Calendar (90) > Puzzle (90).

### 3.5 Ernst Haeckel: *Scientific Art Series*
*   **Strategy:** "The Geometric Aesthetic." Focus on complexity and modern decor.
*   **Expected Route:** Wall Art (95) > Puzzle (94) > Museum Print (92).

---

## 4. Routing Failure Controls (Negative Benchmarks)

*   **Asset:** *Blurred Field Note Scan (Common Sparrow)*
*   **Expected Routing:** **REJECTED** for all families.
*   **Logic:** Failure of Visual Authority (VAS) and Product Versatility (PVS) hard gates.
