# Catalog Validation Dataset v1.0

This dataset provides canonical catalog objects for the core Nature & Culture asset fixtures. These objects serve as the "Gold Standard" for validating the **Catalog Sync Service** and **Product Generation Metadata**.

---

## 1. Catalog Object Schema

Each benchmark fixture follows this canonical structure:

*   **NC_ID:** Internal Nature & Culture Identifier.
*   **Title:** Canonical storefront title.
*   **Slug:** URL-friendly SEO slug.
*   **Classification:** MASTERWORK | FLAGSHIP | STANDARD.
*   **Product_Family:** Primary routing (e.g., Museum Print).
*   **Variants:** Nested list of Media, Size, and Price.
*   **Curator_Note:** The 2-3 sentence "Story" (SSS).
*   **Product_Description:** Full marketing and technical copy.
*   **SEO_Metadata:** Meta title, description, and tags.

---

## 2. Benchmark Catalog Objects

### 2.1 Thomas Moran: *The Grand Canyon of the Yellowstone*
*   **NC_ID:** `ASSET_000001`
*   **Title:** The Grand Canyon of the Yellowstone (1872) — Thomas Moran — Museum Print
*   **Slug:** `thomas-moran-grand-canyon-yellowstone-museum-print`
*   **Classification:** MASTERWORK
*   **Product_Family:** Museum Print
*   **Variants:**
    *   Archival Linen | 24x36" | $450.00
    *   Archival Linen | 36x48" | $850.00
    *   Archival Linen | 40x60" | $1,200.00
*   **Curator_Note:** Painted after the 1871 Hayden Survey, this masterwork was instrumental in convincing the U.S. Congress to establish Yellowstone as the world's first National Park. Moran’s use of color and scale captured the "unbelievable" beauty of the American West for a skeptical Eastern public.
*   **Product_Description:** 
    Experience the foundational vision of the American wilderness. Thomas Moran’s 1872 masterpiece, "The Grand Canyon of the Yellowstone," is more than a landscape; it is a document of conservation history. 
    
    **Provenance:** From the collections of the Smithsonian American Art Museum.
    **Restoration:** Digitally restored for modern display while preserving the original hand-painted textures and historic patina.
    **Rights:** Public Domain / CC0.
*   **SEO_Metadata:**
    *   **Meta Title:** Thomas Moran Yellowstone Print | Museum Grade Archival Art
    *   **Meta Description:** Own the iconic 1872 Thomas Moran painting that created Yellowstone National Park. Premium archival linen prints available in grand scale sizes.
    *   **Tags:** `place:yellowstone`, `artist:thomas-moran`, `classification:masterwork`, `style:hudson-river-school`, `media:archival-linen`

### 2.2 1871 Hayden Survey Map
*   **NC_ID:** `ASSET_000002`
*   **Title:** Map of the Yellowstone National Park (1871) — Hayden Survey — Wall Art
*   **Slug:** `hayden-survey-yellowstone-map-1871-wall-art`
*   **Classification:** MASTERWORK
*   **Product_Family:** Wall Art
*   **Variants:**
    *   Premium Matte Paper | 24x36" | $120.00
    *   Framed Canvas | 24x36" | $280.00
    *   Archival Paper | 40x60" | $450.00
*   **Curator_Note:** The "Blueprint of Wilderness." This was the first definitive map of the Yellowstone region, produced by Ferdinand V. Hayden’s 1871 expedition. It provided the scientific proof required to move the park's wonders from frontier legend into political fact.
*   **Product_Description:** 
    Trace the original boundaries of discovery. The 1871 Hayden Survey Map is the foundational document of the National Park movement, featuring the first precise topographic records of Old Faithful and Yellowstone Lake.
    
    **Provenance:** From the Geography and Map Division of the Library of Congress.
    **Restoration:** Digitally restored for high-fidelity technical clarity while preserving the original survey marks and historic patina.
    **Rights:** Public Domain / CC0.
*   **SEO_Metadata:**
    *   **Meta Title:** 1871 Hayden Yellowstone Map | Historical Cartography Wall Art
    *   **Meta Description:** The first map of Yellowstone National Park. High-resolution historical cartography from the 1871 Hayden Survey. Perfect for home and office decor.
    *   **Tags:** `place:yellowstone`, `category:cartography`, `classification:masterwork`, `style:historical-map`, `source:loc-gmd`

### 2.3 William Henry Jackson: *Old Faithful Geyser*
*   **NC_ID:** `ASSET_000003`
*   **Title:** Old Faithful Geyser (1872) — William Henry Jackson — Heritage Poster
*   **Slug:** `william-henry-jackson-old-faithful-heritage-poster`
*   **Classification:** FLAGSHIP
*   **Product_Family:** Wall Art
*   **Variants:**
    *   Standard Poster | 11x14" | $35.00
    *   Premium Matte | 18x24" | $65.00
    *   Framed Print | 18x24" | $145.00
*   **Curator_Note:** William Henry Jackson was the first to capture the geothermal wonders of Yellowstone on film. This 1872 image of Old Faithful provided the visual proof that the "tall tales" of mountain men were, in fact, a magnificent reality.
*   **Product_Description:** 
    Witness the birth of outdoor photography. This iconic albumen print by William Henry Jackson captures Old Faithful in its pristine, 19th-century state, serving as a testament to the enduring power of nature.
    
    **Provenance:** From the collections of the Smithsonian Institution.
    **Restoration:** Digitally enhanced for high-contrast B&W clarity while maintaining the authentic grain and atmosphere of early expeditionary photography.
    **Rights:** Public Domain / CC0.
*   **SEO_Metadata:**
    *   **Meta Title:** Vintage Old Faithful Photo | William Henry Jackson Yellowstone Poster
    *   **Meta Description:** Authentic 1872 photograph of Old Faithful Geyser by William Henry Jackson. A classic piece of National Park heritage and American history.
    *   **Tags:** `place:yellowstone`, `artist:william-henry-jackson`, `classification:flagship`, `style:early-photography`, `category:heritage-poster`

### 2.4 John James Audubon: *American Bison*
*   **NC_ID:** `ASSET_000004`
*   **Title:** American Bison (1845) — John James Audubon — Giclée Print
*   **Slug:** `audubon-american-bison-giclee-print`
*   **Classification:** MASTERWORK
*   **Product_Family:** Wall Art
*   **Variants:**
    *   Premium Matte | 16x20" | $65.00
    *   Premium Matte | 24x36" | $140.00
    *   Framed Canvas | 24x36" | $320.00
*   **Curator_Note:** From Audubon’s final great work, *The Viviparous Quadrupeds of North America*, this plate remains the most iconic portrayal of the American buffalo. It captures the raw power and majesty of the species before its near-extinction.
*   **Product_Description:** 
    Own a masterpiece of natural history. John James Audubon’s "American Bison" is a cornerstone of 19th-century wildlife illustration, blending scientific precision with dramatic, hand-colored artistry.
    
    **Provenance:** From the collections of the Smithsonian Institution.
    **Restoration:** Digitally restored to recover the vibrant original hand-colored hues while preserving the authentic lithographic texture.
    **Rights:** Public Domain / CC0.
*   **SEO_Metadata:**
    *   **Meta Title:** Audubon Bison Print | Vintage Buffalo Wildlife Art
    *   **Meta Description:** High-quality Giclée print of John James Audubon's 1845 American Bison. A classic of North American natural history and home decor.
    *   **Tags:** `place:yellowstone`, `artist:john-james-audubon`, `classification:masterwork`, `style:natural-history`, `taxon:bison-bison`

### 2.5 John James Audubon: *Common American Wolf*
*   **NC_ID:** `ASSET_000005`
*   **Title:** Common American Wolf (1847) — John James Audubon — Giclée Print
*   **Slug:** `audubon-american-wolf-giclee-print`
*   **Classification:** MASTERWORK
*   **Product_Family:** Wall Art
*   **Variants:**
    *   Premium Matte | 16x20" | $65.00
    *   Premium Matte | 24x36" | $140.00
    *   Framed Canvas | 24x36" | $320.00
*   **Curator_Note:** A haunting and powerful depiction of the Grey Wolf, Audubon’s "Common American Wolf" reflects the wild spirit of the frontier. It remains a definitive reference for North American predator ecology and 19th-century art.
*   **Product_Description:** 
    Evoke the spirit of the wild. This 1847 lithograph by John James Audubon captures the intensity and grace of the American wolf, rendered with the unparalleled detail of the "Golden Age" of natural history.
    
    **Provenance:** From the collections of the Smithsonian Institution.
    **Restoration:** Digitally restored for maximum visual impact, ensuring the fine-line detail of the fur and landscape is preserved for modern display.
    **Rights:** Public Domain / CC0.
*   **SEO_Metadata:**
    *   **Meta Title:** Audubon Wolf Print | Vintage Grey Wolf Wildlife Art
    *   **Meta Description:** Premium Giclée print of John James Audubon's 1847 American Wolf. Dramatic 19th-century natural history illustration for modern interiors.
    *   **Tags:** `place:yellowstone`, `artist:john-james-audubon`, `classification:masterwork`, `style:natural-history`, `taxon:canis-lupus`

### 2.6 Ernst Haeckel: *Circogonia*
*   **NC_ID:** `ASSET_000006`
*   **Title:** Circogonia (Kunstformen der Natur) — Ernst Haeckel — Art Print
*   **Slug:** `haeckel-circogonia-art-print`
*   **Classification:** MASTERWORK
*   **Product_Family:** Wall Art
*   **Variants:**
    *   Premium Matte | 11x14" | $45.00
    *   Premium Matte | 18x24" | $75.00
    *   Premium Matte | 24x36" | $110.00
*   **Curator_Note:** Haeckel’s *Kunstformen der Natur* (Art Forms in Nature) bridged the gap between biology and art. "Circogonia" demonstrates the incredible geometric symmetry found in microscopic marine life, influencing the Art Nouveau movement.
*   **Product_Description:** 
    Discover the geometry of life. Ernst Haeckel’s "Circogonia" is a masterpiece of scientific art, revealing the intricate, symmetrical structures of Radiolaria with stunning precision and aesthetic grace.
    
    **Provenance:** From the collections of the Biodiversity Heritage Library (BHL).
    **Restoration:** Digitally restored to enhance the vibrant scientific colors while preserving the original 19th-century lithographic line work.
    **Rights:** Public Domain / CC0.
*   **SEO_Metadata:**
    *   **Meta Title:** Ernst Haeckel Circogonia Print | Scientific Art Decor
    *   **Meta Description:** High-quality art print of Ernst Haeckel's Circogonia from Art Forms in Nature. Beautiful geometric symmetry for modern and scientific decor.
    *   **Tags:** `place:global`, `artist:ernst-haeckel`, `classification:masterwork`, `style:scientific-illustration`, `category:geometric-art`
