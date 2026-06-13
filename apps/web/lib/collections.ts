export type CollectionPathway = {
  title: string;
  theme: string;
  copy: string;
};

export type CollectionWork = {
  title: string;
  label: string;
  copy: string;
  imageSrc: string;
  imageAlt: string;
  imageTreatment: "earth" | "horizon" | "folio";
};

export type ProvenanceGlanceItem = {
  label: string;
  value: string;
};

export type NextJourney = {
  title: string;
  eyebrow: string;
  copy: string;
  href: string;
};

export type CollectionStatus = "live";

export type CollectionMetadata = {
  slug: string;
  title: string;
  shortTitle: string;
  status: CollectionStatus;
  badge: string;
  authority: string;
  imageSrc: string;
  imageAlt: string;
  summary: string;
  seoTitle: string;
  seoDescription: string;
  curatorStatement: string;
  narrativeTitle: string;
  narrative: [string, string];
  provenanceGlance: ProvenanceGlanceItem[];
  pathways: CollectionPathway[];
  works: CollectionWork[];
  nextJourneys: NextJourney[];
  ctaTitle: string;
  ctaCopy: string;
  primaryCta: {
    label: string;
    href: string;
  };
  secondaryCta?: {
    label: string;
    href: string;
  };
  credit: string;
};

const earthriseImage = "/images/earthrise-as08-14-2383.jpg";
const earthriseMasterworkImage = "/images/earthrise-work-masterwork.jpg";
const earthriseHorizonImage = "/images/earthrise-work-horizon.jpg";
const earthriseFolioImage = "/images/earthrise-work-folio.jpg";

const earthriseProvenance: ProvenanceGlanceItem[] = [
  { label: "Source", value: "NASA" },
  { label: "Mission", value: "Apollo 8" },
  { label: "Date", value: "December 24, 1968" },
  { label: "Frame", value: "AS08-14-2383" },
  { label: "Rights", value: "Public Domain, 17 U.S.C. § 105" }
];

export const earthriseCollection: CollectionMetadata = {
  slug: "earthrise",
  title: "Earthrise: The Oasis Collection",
  shortTitle: "Earthrise",
  status: "live",
  badge: "MASTERWORK COLLECTION",
  authority: "NASA / Apollo 8",
  imageSrc: earthriseImage,
  imageAlt: "Earth rising above the lunar horizon during Apollo 8",
  summary:
    "The moment humanity found home: a focused archival collection around Apollo 8, planetary awareness, and the photograph that changed the meaning of exploration.",
  seoTitle: "Earthrise: The Oasis Collection",
  seoDescription:
    "Explore the Earthrise collection: Apollo 8, William Anders, the Overview Effect, featured works, provenance, and public-domain editions.",
  curatorStatement:
    "We went to the Moon to discover the Moon. Instead, we found ourselves. Earthrise is the moment our species gained a planetary mirror, transforming a cold race for orbit into a profound awareness of our shared isolation and beauty.",
  narrativeTitle: "The oasis in the desert.",
  narrative: [
    "In the silence of the lunar far side, Apollo 8 emerged from darkness to witness a blue world rising over a cratered horizon. The subject was no longer only the Moon. It was Earth: vibrant, fragile, and suspended in an infinite void.",
    "The Earthrise Collection maps the cognitive shift from conquering space to protecting home. It returns to the primary NASA frame as a cultural artifact, a scientific record, and the visual baseline for the modern idea of planetary stewardship."
  ],
  provenanceGlance: earthriseProvenance,
  pathways: [
    {
      title: "The Thin Blue Line",
      theme: "Atmospheric Science & Fragility",
      copy:
        "Discover the protective shield that sustains life: a delicate, luminous boundary visible at planetary scale."
    },
    {
      title: "The Lunar Cradle",
      theme: "Orbital Mechanics & Exploration",
      copy:
        "Stand at the edge of the Moon and follow Apollo 8 as Earth emerges from the lunar limb."
    },
    {
      title: "The Movement Icon",
      theme: "Cultural Heritage & Conservation",
      copy:
        "Trace how an unplanned photograph became an icon of environmental consciousness and planetary identity."
    }
  ],
  works: [
    {
      title: "Earthrise Heritage Edition",
      label: "The Masterwork",
      copy:
        "The definitive high-resolution presentation of NASA AS08-14-2383, preserving the contrast between lunar surface, deep space, and cloud-streaked Earth.",
      imageSrc: earthriseMasterworkImage,
      imageAlt: "Earthrise Heritage Edition",
      imageTreatment: "earth"
    },
    {
      title: "The Lunar Horizon",
      label: "Detail Study",
      copy:
        "A focused reading of the lunar foreground: the ancient cratered landscape that became the cradle for humanity's first orbital view of home.",
      imageSrc: earthriseHorizonImage,
      imageAlt: "The Lunar Horizon detail study",
      imageTreatment: "horizon"
    },
    {
      title: "The Overview Folio",
      label: "Intellectual Record",
      copy:
        "A curated study path joining image, mission context, and the idea of the Overview Effect into one educational collection thread.",
      imageSrc: earthriseFolioImage,
      imageAlt: "The Overview Folio",
      imageTreatment: "folio"
    }
  ],
  nextJourneys: [
    {
      title: "Read the Earthrise story",
      eyebrow: "Story",
      copy:
        "Move from collection overview into the narrative of Apollo 8, the lunar horizon, and the image's cultural afterlife.",
      href: "/stories/earthrise"
    },
    {
      title: "Explore Earthrise editions",
      eyebrow: "Editions",
      copy: "Compare the Museum Print for display with the Digital Edition for close study.",
      href: "/products/earthrise"
    },
    {
      title: "See the collection index",
      eyebrow: "Collections",
      copy:
        "Return to the collection index when you are ready to explore the public catalog.",
      href: "/collections"
    }
  ],
  ctaTitle: "Continue from collection to edition.",
  ctaCopy:
    "Explore the Museum Print for display or the Digital Edition for close study, both tied to the same NASA source record.",
  primaryCta: {
    label: "Explore Earthrise editions",
    href: "/products/earthrise"
  },
  secondaryCta: {
    label: "Read the full story",
    href: "/stories/earthrise"
  },
  credit: "NASA · Apollo 8 · William Anders · Public Domain"
};


const PLACE_COLLECTION_IMAGES = {
  alhambra:
    "https://commons.wikimedia.org/wiki/Special:FilePath/Alhambra%20evening%20panorama%20Mirador%20San%20Nicolas%20sRGB-1.jpg",
  southGeorgia:
    "https://commons.wikimedia.org/wiki/Special:FilePath/South%20Georgia%20Island%20view.jpg",
  versailles:
    "https://commons.wikimedia.org/wiki/Special:FilePath/Chateau%20de%20Versailles%201668%20Pierre%20Patel.jpg",
  chichenItza:
    "https://commons.wikimedia.org/wiki/Special:FilePath/Chichen%20Itza%203.jpg",
  petra:
    "https://commons.wikimedia.org/wiki/Special:FilePath/Al%20Khazneh%2C%20Petra%2C%20Jordan8.jpg"
};

const PLACE_WORK_IMAGES = {
  map:
    "https://commons.wikimedia.org/wiki/Special:FilePath/Ortelius%20World%20Map%201570.jpg",
  archive:
    "https://commons.wikimedia.org/wiki/Special:FilePath/Great%20Gallery%20of%20the%20Louvre%20-%20Samuel%20F.%20B.%20Morse%20-%20Terra%20Foundation.jpg",
  field:
    "https://commons.wikimedia.org/wiki/Special:FilePath/Natural%20History%20Museum%20London%20Jan%202006.jpg"
};

function placeCollection({
  slug,
  title,
  shortTitle,
  authority,
  imageSrc,
  imageAlt,
  summary,
  curatorStatement,
  narrativeTitle,
  narrative,
  pathways,
  works,
  nextJourneys,
  ctaTitle,
  ctaCopy,
  credit
}: Omit<CollectionMetadata, "status" | "badge" | "seoTitle" | "seoDescription" | "provenanceGlance" | "primaryCta" | "secondaryCta">): CollectionMetadata {
  return {
    slug,
    title,
    shortTitle,
    status: "live",
    badge: "FLAGSHIP COLLECTION",
    authority,
    imageSrc,
    imageAlt,
    summary,
    seoTitle: title,
    seoDescription: summary,
    curatorStatement,
    narrativeTitle,
    narrative,
    provenanceGlance: [
      { label: "Authority", value: authority },
      { label: "Collection", value: "Activation-ranked flagship" },
      { label: "Readiness", value: "Collection ready, publishing review" },
      { label: "Source posture", value: "Candidate-first, authority review pending" }
    ],
    pathways,
    works,
    nextJourneys,
    ctaTitle,
    ctaCopy,
    primaryCta: {
      label: "View related products",
      href: "/products"
    },
    secondaryCta: {
      label: "Return to collections",
      href: "/collections"
    },
    credit
  };
}

export const alhambraCollection = placeCollection({
  slug: "alhambra",
  title: "Alhambra: Water, Geometry, Garden",
  shortTitle: "Alhambra",
  authority: "UNESCO World Heritage / Granada",
  imageSrc: PLACE_COLLECTION_IMAGES.alhambra,
  imageAlt: "The Alhambra palace complex above Granada at dusk",
  summary:
    "A collection journey through Nasrid architecture, courtly water systems, carved geometry, and the garden landscapes of Granada.",
  curatorStatement:
    "The Alhambra is a study in restraint and abundance at once: water becomes architecture, plaster becomes light, and inscriptions turn walls into a living archive of place.",
  narrativeTitle: "A palace written in water and light.",
  narrative: [
    "The Alhambra gathers fortress, palace, garden, and city into one continuous cultural landscape. Its courts shape sound and shade as carefully as stone, turning movement through space into a sequence of revelations.",
    "This collection follows the ways craft, mathematics, botany, and power meet in Granada: the mirrored pools, muqarnas ceilings, tiled geometries, and hillside gardens that made the site a reference point for global heritage imagination."
  ],
  pathways: [
    {
      title: "Court of Water",
      theme: "Architecture & Atmosphere",
      copy: "Follow channels, fountains, and reflecting pools as structural elements rather than ornament."
    },
    {
      title: "Geometry as Memory",
      theme: "Craft & Pattern",
      copy: "Read tilework, plaster, and inscription as a visual system for transmitting culture."
    },
    {
      title: "The Garden City",
      theme: "Landscape & Power",
      copy: "Move from palace interiors to the Generalife and the cultivated hill above Granada."
    }
  ],
  works: [
    {
      title: "Nasrid Geometry Study",
      label: "Pattern Study",
      copy: "A visual reading of repeating geometry, surface rhythm, and architectural proportion.",
      imageSrc: PLACE_WORK_IMAGES.archive,
      imageAlt: "Historic gallery study representing archival visual analysis",
      imageTreatment: "folio"
    },
    {
      title: "Water Court Sequence",
      label: "Journey Map",
      copy: "A guided route through courts, thresholds, and the acoustics of moving water.",
      imageSrc: PLACE_WORK_IMAGES.map,
      imageAlt: "Historic world map used as a cartographic study image",
      imageTreatment: "horizon"
    },
    {
      title: "Garden Archive Folio",
      label: "Landscape Record",
      copy: "Botanical and spatial notes connecting palace gardens to Granada's wider terrain.",
      imageSrc: PLACE_WORK_IMAGES.field,
      imageAlt: "Natural history archive hall representing study collections",
      imageTreatment: "earth"
    }
  ],
  nextJourneys: [
    {
      title: "Versailles: Garden and State",
      eyebrow: "Related collection",
      copy: "Compare court landscapes, controlled vistas, and the political language of gardens.",
      href: "/collections/versailles"
    },
    {
      title: "Petra: Stone and Caravan",
      eyebrow: "Related collection",
      copy: "Continue from carved surfaces to an entire city shaped from geology and trade.",
      href: "/collections/petra"
    }
  ],
  ctaTitle: "Products for close study.",
  ctaCopy: "Prepare print, map, and study-folio products after authority review and image clearance.",
  credit: "UNESCO World Heritage · Granada · Candidate collection"
});

export const southGeorgiaCollection = placeCollection({
  slug: "south-georgia",
  title: "South Georgia: Ice, Expedition, Recovery",
  shortTitle: "South Georgia",
  authority: "Subantarctic island / Expedition heritage",
  imageSrc: PLACE_COLLECTION_IMAGES.southGeorgia,
  imageAlt: "Mountain and coastal landscape on South Georgia Island",
  summary:
    "A subantarctic collection connecting polar exploration, whale-era archives, seabird colonies, and ecological recovery.",
  curatorStatement:
    "South Georgia compresses extremes: heroic expedition, industrial extraction, and one of the great conservation reversals of the Southern Ocean.",
  narrativeTitle: "At the edge of the Southern Ocean.",
  narrative: [
    "South Georgia sits far from continental certainty, a steep island of glaciers, wind, and living abundance. It is a place where expedition history and ecological history cannot be separated.",
    "The collection moves from Shackleton's route and whaling stations to albatross, penguins, seals, and restoration work, treating the island as both archive and living system."
  ],
  pathways: [
    {
      title: "Expedition Shore",
      theme: "Exploration History",
      copy: "Trace landing points, survival narratives, and the geography of polar navigation."
    },
    {
      title: "Whale Station Ledger",
      theme: "Industrial Archive",
      copy: "Read extraction history through stations, ships, and the records of ocean commerce."
    },
    {
      title: "Return of Wildlife",
      theme: "Ecology & Recovery",
      copy: "Follow seabird and marine mammal recovery across beaches, cliffs, and open water."
    }
  ],
  works: [
    {
      title: "Expedition Route Folio",
      label: "Journey Record",
      copy: "A study product linking route, weather, and survival geography.",
      imageSrc: PLACE_WORK_IMAGES.map,
      imageAlt: "Historic map used for expedition-route study",
      imageTreatment: "horizon"
    },
    {
      title: "Subantarctic Wildlife Study",
      label: "Field Record",
      copy: "A conservation-facing work around colonies, migration, and recovery signals.",
      imageSrc: PLACE_WORK_IMAGES.field,
      imageAlt: "Natural history archive used for field record study",
      imageTreatment: "earth"
    },
    {
      title: "Whaling Archive Reader",
      label: "Archive Folio",
      copy: "A sober reader connecting industrial records to present ecological restoration.",
      imageSrc: PLACE_WORK_IMAGES.archive,
      imageAlt: "Archive hall representing historical document study",
      imageTreatment: "folio"
    }
  ],
  nextJourneys: [
    {
      title: "Earthrise: The Oasis Collection",
      eyebrow: "Related collection",
      copy: "Move from a remote island system to a planetary view of fragile home.",
      href: "/collections/earthrise"
    },
    {
      title: "Petra: Stone and Caravan",
      eyebrow: "Related collection",
      copy: "Contrast polar isolation with desert routes, trade, and built survival systems.",
      href: "/collections/petra"
    }
  ],
  ctaTitle: "Products for expedition and ecology.",
  ctaCopy: "Prepare route maps, wildlife studies, and archive readers after rights and source review.",
  credit: "South Georgia · Expedition heritage · Candidate collection"
});

export const versaillesCollection = placeCollection({
  slug: "versailles",
  title: "Versailles: Garden, State, Spectacle",
  shortTitle: "Versailles",
  authority: "UNESCO World Heritage / France",
  imageSrc: PLACE_COLLECTION_IMAGES.versailles,
  imageAlt: "Historic depiction of the Palace of Versailles and formal gardens",
  summary:
    "A court landscape collection about architecture, power, hydraulics, performance, and the designed horizon of the French state.",
  curatorStatement:
    "Versailles turns landscape into ceremony. Every axis, basin, facade, and room participates in a visual grammar of authority.",
  narrativeTitle: "The state as a garden machine.",
  narrative: [
    "Versailles is not only a palace. It is an engineered landscape of approach, spectacle, water, symmetry, and controlled perspective built to choreograph attention.",
    "This collection treats the estate as a system: palace rooms, garden axes, hydraulic ambition, court performance, and the images that carried Versailles across Europe."
  ],
  pathways: [
    {
      title: "Axis and Horizon",
      theme: "Landscape Design",
      copy: "Follow the long sightlines that turn movement through the grounds into political theater."
    },
    {
      title: "Water as Power",
      theme: "Engineering & Display",
      copy: "Study fountains, basins, and hydraulic systems as symbols of command over nature."
    },
    {
      title: "Rooms of Ceremony",
      theme: "Court Culture",
      copy: "Move inside to the spaces where daily life became performance."
    }
  ],
  works: [
    {
      title: "Grand Axis Print",
      label: "Landscape Study",
      copy: "A formal reading of vista, canal, basin, and approach.",
      imageSrc: PLACE_COLLECTION_IMAGES.versailles,
      imageAlt: "Historic Versailles landscape view",
      imageTreatment: "earth"
    },
    {
      title: "Court Ceremony Reader",
      label: "Archive Folio",
      copy: "A compact guide to rooms, rituals, and the public life of monarchy.",
      imageSrc: PLACE_WORK_IMAGES.archive,
      imageAlt: "Historic gallery archive study",
      imageTreatment: "folio"
    },
    {
      title: "Hydraulic Garden Map",
      label: "System Map",
      copy: "A study of fountains, water movement, and infrastructure behind spectacle.",
      imageSrc: PLACE_WORK_IMAGES.map,
      imageAlt: "Historic map used for garden-system study",
      imageTreatment: "horizon"
    }
  ],
  nextJourneys: [
    {
      title: "Alhambra: Water, Geometry, Garden",
      eyebrow: "Related collection",
      copy: "Compare two palace landscapes where water shapes power and perception.",
      href: "/collections/alhambra"
    },
    {
      title: "Chichen Itza: Calendar, City, Cenote",
      eyebrow: "Related collection",
      copy: "Move from court spectacle to astronomy, ritual space, and civic landscape.",
      href: "/collections/chichen-itza"
    }
  ],
  ctaTitle: "Products for rooms and gardens.",
  ctaCopy: "Prepare garden prints, system maps, and court-culture folios for launch review.",
  credit: "UNESCO World Heritage · Versailles · Candidate collection"
});

export const chichenItzaCollection = placeCollection({
  slug: "chichen-itza",
  title: "Chichen Itza: Calendar, City, Cenote",
  shortTitle: "Chichen Itza",
  authority: "UNESCO World Heritage / Yucatán",
  imageSrc: PLACE_COLLECTION_IMAGES.chichenItza,
  imageAlt: "El Castillo pyramid at Chichen Itza",
  summary:
    "A collection about Maya and Itza urban space, astronomical alignment, ritual landscapes, and the long life of Yucatán knowledge systems.",
  curatorStatement:
    "Chichen Itza is a city of alignments: stone, sky, water, movement, and memory meet in a landscape built for civic and ceremonial time.",
  narrativeTitle: "A city tuned to sky and water.",
  narrative: [
    "Chichen Itza gathers pyramid, ball court, observatory, sacbe, and cenote into a dense civic landscape. Its forms point beyond monumentality toward systems of time, governance, ritual, and exchange.",
    "This collection follows the site as a knowledge landscape: astronomy in architecture, water in limestone, public ceremony in urban space, and the continuing cultural presence of Yucatán."
  ],
  pathways: [
    {
      title: "Calendar Architecture",
      theme: "Astronomy & Time",
      copy: "Read El Castillo and nearby structures through alignment, shadow, and seasonal rhythm."
    },
    {
      title: "Cenote and City",
      theme: "Water & Ritual",
      copy: "Connect limestone geology, sacred water, and civic life."
    },
    {
      title: "Ball Court Soundscape",
      theme: "Public Ceremony",
      copy: "Study scale, acoustics, and ritual performance in the Great Ball Court."
    }
  ],
  works: [
    {
      title: "Calendar Pyramid Study",
      label: "Architecture Print",
      copy: "A focused study product around stepped form, shadow, and seasonal reading.",
      imageSrc: PLACE_COLLECTION_IMAGES.chichenItza,
      imageAlt: "Chichen Itza pyramid study",
      imageTreatment: "earth"
    },
    {
      title: "Yucatán Water Map",
      label: "Landscape Map",
      copy: "A map-led view of cenotes, limestone, and civic settlement.",
      imageSrc: PLACE_WORK_IMAGES.map,
      imageAlt: "Historic map used for Yucatan landscape study",
      imageTreatment: "horizon"
    },
    {
      title: "City of Ceremony Folio",
      label: "Study Folio",
      copy: "A reader joining ball court, observatory, pyramid, and processional space.",
      imageSrc: PLACE_WORK_IMAGES.archive,
      imageAlt: "Archive study image for ceremonial city folio",
      imageTreatment: "folio"
    }
  ],
  nextJourneys: [
    {
      title: "Petra: Stone and Caravan",
      eyebrow: "Related collection",
      copy: "Continue to another city where geology, water, and movement shape architecture.",
      href: "/collections/petra"
    },
    {
      title: "Versailles: Garden and State",
      eyebrow: "Related collection",
      copy: "Compare ceremonial landscapes across radically different political worlds.",
      href: "/collections/versailles"
    }
  ],
  ctaTitle: "Products for time and landscape.",
  ctaCopy: "Prepare architectural studies, landscape maps, and educational folios for review.",
  credit: "UNESCO World Heritage · Yucatán · Candidate collection"
});

export const petraCollection = placeCollection({
  slug: "petra",
  title: "Petra: Stone, Water, Caravan",
  shortTitle: "Petra",
  authority: "UNESCO World Heritage / Jordan",
  imageSrc: PLACE_COLLECTION_IMAGES.petra,
  imageAlt: "The Treasury facade carved into sandstone at Petra",
  summary:
    "A collection about Nabataean architecture, desert water systems, caravan exchange, and a city carved from living geology.",
  curatorStatement:
    "Petra is not simply carved stone. It is a desert technology of movement, water, trade, and memory made monumental.",
  narrativeTitle: "A city cut from route and rock.",
  narrative: [
    "Petra rises from sandstone and corridor. The Siq compresses arrival into revelation, while tomb facades, water channels, and high places reveal a city built from geology and exchange.",
    "This collection follows Nabataean ingenuity through carved architecture, hydraulic infrastructure, caravan routes, and the long afterlife of Petra as archaeological site and cultural symbol."
  ],
  pathways: [
    {
      title: "The Siq Approach",
      theme: "Journey & Threshold",
      copy: "Move through the narrow geological corridor toward the staged reveal of the Treasury."
    },
    {
      title: "Desert Hydraulics",
      theme: "Water Engineering",
      copy: "Trace channels, cisterns, and water control in an arid urban landscape."
    },
    {
      title: "Caravan City",
      theme: "Trade & Cultural Exchange",
      copy: "Connect facades and routes to incense, commerce, and regional networks."
    }
  ],
  works: [
    {
      title: "Treasury Facade Study",
      label: "Architecture Print",
      copy: "A focused visual study of carved stone, scale, and theatrical arrival.",
      imageSrc: PLACE_COLLECTION_IMAGES.petra,
      imageAlt: "Petra Treasury facade study",
      imageTreatment: "earth"
    },
    {
      title: "Caravan Route Map",
      label: "Route Map",
      copy: "A map-led view of exchange routes, desert passage, and regional connection.",
      imageSrc: PLACE_WORK_IMAGES.map,
      imageAlt: "Historic map used for caravan-route study",
      imageTreatment: "horizon"
    },
    {
      title: "Water in Sandstone Folio",
      label: "Engineering Folio",
      copy: "A study reader on cisterns, channels, and the design of desert resilience.",
      imageSrc: PLACE_WORK_IMAGES.archive,
      imageAlt: "Archive study image for Petra engineering folio",
      imageTreatment: "folio"
    }
  ],
  nextJourneys: [
    {
      title: "Alhambra: Water, Geometry, Garden",
      eyebrow: "Related collection",
      copy: "Compare water as architecture across desert and palace landscapes.",
      href: "/collections/alhambra"
    },
    {
      title: "Chichen Itza: Calendar, City, Cenote",
      eyebrow: "Related collection",
      copy: "Continue through cities where geology and water structure civic space.",
      href: "/collections/chichen-itza"
    }
  ],
  ctaTitle: "Products for stone and route.",
  ctaCopy: "Prepare facade studies, route maps, and engineering folios for launch review.",
  credit: "UNESCO World Heritage · Jordan · Candidate collection"
});

export const collections: CollectionMetadata[] = [
  earthriseCollection,
  alhambraCollection,
  southGeorgiaCollection,
  versaillesCollection,
  chichenItzaCollection,
  petraCollection
];

export const signatureCollections: CollectionMetadata[] = [
  alhambraCollection,
  southGeorgiaCollection,
  versaillesCollection,
  chichenItzaCollection,
  petraCollection
];

export function getCollectionBySlug(slug: string) {
  return collections.find((collection) => collection.slug === slug);
}
