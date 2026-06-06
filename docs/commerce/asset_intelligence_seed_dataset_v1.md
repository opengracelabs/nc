# Asset Intelligence Seed Dataset v1

| Field | Value |
|---|---|
| Version | v1.0.0 |
| Status | Approved — Authority Seed |
| Role | Chief Curator |
| Date | 2026-06-06 |

---

## 1. Creator Prestige and Authority Tiers

This section defines the ranking of key creators across multiple dimensions. These values seed the `commerce_policy` logic for **Visual Authority (VAS)** and **Story Strength (SSS)**.

### 1.1 Natural History

| Creator | Prestige | Authority | Comm | Edu | Tour | Place Associations |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **John James Audubon** | Tier 1 | Tier 1 | 10 | 10 | 9 | US (Upper Missouri, Florida, Northeast) |
| **John Gould** | Tier 1 | Tier 1 | 9 | 10 | 8 | Australia, UK, Galápagos (Darwin's Finches) |
| **Ernst Haeckel** | Tier 1 | Tier 2 | 10 | 9 | 7 | Marine (Global), Germany |
| **Pierre-Joseph Redouté** | Tier 1 | Tier 2 | 10 | 9 | 8 | France, Botanical Gardens |
| **Maria Sibylla Merian** | Tier 1 | Tier 1 | 9 | 10 | 7 | Suriname, Europe |
| **Joseph Wolf** | Tier 2 | Tier 1 | 8 | 10 | 7 | UK, Zoological illustrations |

### 1.2 Fine Art

| Creator | Prestige | Authority | Comm | Edu | Tour | Place Associations |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Thomas Moran** | Tier 1 | Tier 1 | 9 | 9 | 10 | Yellowstone, Grand Canyon |
| **Albert Bierstadt** | Tier 1 | Tier 2 | 9 | 8 | 10 | Yosemite, Rocky Mountains |
| **Frederic Edwin Church** | Tier 1 | Tier 1 | 9 | 8 | 9 | South America (Andes), North America |
| **J.M.W. Turner** | Tier 1 | Tier 3 | 10 | 9 | 9 | UK, Europe, Maritime |

### 1.3 Photography

| Creator | Prestige | Authority | Comm | Edu | Tour | Place Associations |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **William Henry Jackson** | Tier 1 | Tier 1 | 8 | 10 | 10 | Yellowstone, Colorado |
| **Carleton Watkins** | Tier 1 | Tier 1 | 9 | 9 | 10 | Yosemite |
| **Edward S. Curtis** | Tier 1 | Tier 1 | 10 | 10 | 9 | US West (Indigenous Cultures) |

### 1.4 Maps

| Creator | Prestige | Authority | Comm | Edu | Tour | Place Associations |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Hayden Survey** | Tier 2 | Tier 1 | 8 | 10 | 10 | Yellowstone, Wyoming, Montana |
| **Joan Blaeu** | Tier 1 | Tier 1 | 10 | 9 | 8 | Global (Atlas Maior), Europe |
| **John Tallis** | Tier 1 | Tier 3 | 10 | 8 | 7 | British Empire, Global Vignettes |
| **Aaron Arrowsmith** | Tier 2 | Tier 1 | 8 | 10 | 8 | Arctic, Hydrography |

---

## 2. Place Iconic Taxa Seeds

These taxa represent the highest-value "Illustration Opportunities" for their respective flagship places. Discovery workers should prioritize finding public-domain assets depicting these species for these places.

### 2.1 Yellowstone National Park
- **Bison bison** (American Bison)
- **Ursus arctos horribilis** (Grizzly Bear)
- **Canis lupus** (Gray Wolf)
- **Cervus canadensis** (American Elk / Wapiti)
- **Oncorhynchus clarkii bouvieri** (Yellowstone Cutthroat Trout)

### 2.2 Yosemite National Park
- **Sequoiadendron giganteum** (Giant Sequoia)
- **Ursus americanus** (American Black Bear)
- **Falco peregrinus** (Peregrine Falcon)
- **Cyanocitta stelleri** (Steller's Jay)
- **Odocoileus hemionus** (Mule Deer)

### 2.3 Grand Canyon National Park
- **Gymnogyps californianus** (California Condor)
- **Ovis canadensis nelsoni** (Desert Bighorn Sheep)
- **Puma concolor** (Mountain Lion)
- **Crotalus abyssus** (Grand Canyon Pink Rattlesnake)
- **Haliaeetus leucocephalus** (Bald Eagle)

### 2.4 Everglades National Park
- **Alligator mississippiensis** (American Alligator)
- **Puma concolor coryi** (Florida Panther)
- **Platalea ajaja** (Roseate Spoonbill)
- **Trichechus manatus** (West Indian Manatee)
- **Mycteria americana** (Wood Stork)

### 2.5 Galápagos Islands
- **Chelonoidis niger** (Galápagos Giant Tortoise)
- **Amblyrhynchus cristatus** (Marine Iguana)
- **Sula nebouxii** (Blue-footed Booby)
- **Geospizinae** (Darwin's Finches - General)
- **Spheniscus mendiculus** (Galápagos Penguin)

---

## 3. Anchor Type Validation Rules

When evaluating an "Illustration Opportunity", the `anchor_type` must be validated against the following hierarchy:

1.  **Direct Depiction:** Asset title or metadata explicitly names the iconic taxon. (Confidence: 1.000)
2.  **Contextual Association:** Asset depicts a habitat or related species known to be an iconic associate (e.g., *Sequoiadendron* landscape for Yosemite). (Confidence: 0.850)
3.  **Place-Illustrator Lock:** Asset by a Tier 1 Creator historically bound to the Place (e.g., Moran + Yellowstone Falls) even if the specific taxon is secondary. (Confidence: 0.950)
4.  **Generic Range Match:** Asset depicts a taxon found in the Place but not identified as "Iconic". (Confidence: 0.600)
