export type DiscoveryPlace = {
  slug: string;
  title: string;
  region: string;
  category: string;
  status: "Live" | "Coming soon";
  summary: string;
  works: number;
  journeys: number;
  nearby: Array<{ title: string; distance: string; reason: string }>;
  mapPosition: { x: number; y: number };
};

export type DiscoveryRecommendation = {
  title: string;
  eyebrow: string;
  summary: string;
  href: string;
  imageSrc: string;
  imageAlt: string;
  reasons: string[];
};

export type RelatedJourney = {
  title: string;
  eyebrow: string;
  summary: string;
  href: string;
};

export type CollectionGraphNode = {
  id: string;
  label: string;
  type: "collection" | "work" | "place" | "story" | "edition";
  x: number;
  y: number;
};

export type CollectionGraphEdge = {
  from: string;
  to: string;
  label: string;
};

export const discoveryPlaces: DiscoveryPlace[] = [
  {
    slug: "earthrise",
    title: "Earthrise",
    region: "Lunar orbit",
    category: "Planetary view",
    status: "Live",
    summary: "The Apollo 8 photograph that made Earth the subject of exploration.",
    works: 3,
    journeys: 3,
    nearby: [
      { title: "Blue Marble", distance: "Apollo archive", reason: "Whole-Earth iconography" },
      { title: "Moon limb studies", distance: "Same mission", reason: "Shared lunar horizon" }
    ],
    mapPosition: { x: 66, y: 28 }
  },
  {
    slug: "yellowstone",
    title: "Yellowstone",
    region: "Wyoming, United States",
    category: "National park",
    status: "Coming soon",
    summary: "Expedition art, geology, wildlife, and the visual argument for preservation.",
    works: 8,
    journeys: 4,
    nearby: [
      { title: "Grand Teton", distance: "85 km", reason: "Greater Yellowstone ecosystem" },
      { title: "Grand Canyon", distance: "900 km", reason: "Survey-era landscape record" }
    ],
    mapPosition: { x: 22, y: 42 }
  },
  {
    slug: "grand-canyon",
    title: "Grand Canyon",
    region: "Arizona, United States",
    category: "Geologic landscape",
    status: "Coming soon",
    summary: "Deep-time geology, survey cartography, and public-domain landscape records.",
    works: 5,
    journeys: 3,
    nearby: [
      { title: "Yellowstone", distance: "900 km", reason: "USGS survey lineage" },
      { title: "Yosemite", distance: "700 km", reason: "Western preservation arc" }
    ],
    mapPosition: { x: 20, y: 50 }
  },
  {
    slug: "great-barrier-reef",
    title: "Great Barrier Reef",
    region: "Queensland, Australia",
    category: "Marine ecosystem",
    status: "Coming soon",
    summary: "Reef systems, coral records, navigation, biodiversity, and conservation evidence.",
    works: 4,
    journeys: 4,
    nearby: [
      { title: "Daintree Rainforest", distance: "110 km", reason: "Reef-to-rainforest corridor" },
      { title: "Coral Sea", distance: "220 km", reason: "Shared marine bioregion" }
    ],
    mapPosition: { x: 82, y: 68 }
  },
  {
    slug: "galapagos",
    title: "Galapagos",
    region: "Ecuador",
    category: "Island ecosystem",
    status: "Coming soon",
    summary: "Evolutionary field records, species distribution, and voyage-based discovery.",
    works: 6,
    journeys: 3,
    nearby: [
      { title: "HMS Beagle route", distance: "Voyage thread", reason: "Expedition relationship" },
      { title: "Pacific island systems", distance: "Bioregion", reason: "Island biodiversity" }
    ],
    mapPosition: { x: 34, y: 61 }
  }
];

export const featuredRecommendation: DiscoveryRecommendation = {
  title: "Begin with Earthrise",
  eyebrow: "Recommended now",
  summary:
    "Start with the live collection: a single source image connected to story, editions, provenance, and the next planetary journeys.",
  href: "/collections/earthrise",
  imageSrc: "/images/earthrise-work-masterwork.jpg",
  imageAlt: "Earthrise masterwork crop from Apollo 8",
  reasons: [
    "Live collection with visible provenance",
    "Connects story, product, and place",
    "Strong bridge to future planetary journeys"
  ]
};

export const relatedJourneys: RelatedJourney[] = [
  {
    title: "The Overview Effect",
    eyebrow: "Story path",
    summary: "Move from the Apollo 8 image into planetary awareness and environmental memory.",
    href: "/stories/earthrise"
  },
  {
    title: "The Lunar Horizon",
    eyebrow: "Work path",
    summary: "Read the photograph through the Moon foreground that frames the Earth.",
    href: "/collections/earthrise"
  },
  {
    title: "Museum Print to Digital Edition",
    eyebrow: "Edition path",
    summary: "Compare the display and study formats derived from the same NASA record.",
    href: "/products/earthrise"
  }
];

export const collectionGraph = {
  nodes: [
    { id: "collection", label: "Earthrise Collection", type: "collection", x: 50, y: 50 },
    { id: "work", label: "NASA AS08-14-2383", type: "work", x: 22, y: 30 },
    { id: "story", label: "Overview story", type: "story", x: 78, y: 30 },
    { id: "place", label: "Lunar orbit", type: "place", x: 24, y: 74 },
    { id: "edition", label: "Museum + digital editions", type: "edition", x: 78, y: 74 }
  ] satisfies CollectionGraphNode[],
  edges: [
    { from: "collection", to: "work", label: "contains" },
    { from: "collection", to: "story", label: "explains" },
    { from: "collection", to: "place", label: "anchored at" },
    { from: "collection", to: "edition", label: "publishes" }
  ] satisfies CollectionGraphEdge[]
};
