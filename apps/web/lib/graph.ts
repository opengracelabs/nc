export type GraphNode = {
  id: string;
  slug: string;
  label: string;
  name: string;
  summary: string;
  status: string;
};

export type GraphRelationship = {
  source: string;
  target: string;
  type: string;
  reason: string;
  weight: number;
};

export type GraphJourney = {
  subject: GraphNode;
  nodes: GraphNode[];
  relationships: GraphRelationship[];
  source: string;
};

export const fallbackGraphJourney: GraphJourney = {
  source: "seed",
  subject: {
    id: "collection:earthrise",
    slug: "earthrise-collection",
    label: "Collection",
    name: "Earthrise: The Oasis Collection",
    summary: "A source-traceable collection around NASA AS08-14-2383 and the overview effect.",
    status: "live"
  },
  nodes: [
    {
      id: "collection:earthrise",
      slug: "earthrise-collection",
      label: "Collection",
      name: "Earthrise: The Oasis Collection",
      summary: "A source-traceable collection around NASA AS08-14-2383 and the overview effect.",
      status: "live"
    },
    {
      id: "asset:earthrise-as08-14-2383",
      slug: "as08-14-2383",
      label: "Asset",
      name: "NASA AS08-14-2383",
      summary: "The Apollo 8 Earthrise source frame photographed by William Anders.",
      status: "live"
    },
    {
      id: "place:earthrise",
      slug: "earthrise",
      label: "Place",
      name: "Earthrise",
      summary: "Apollo 8 lunar-orbit viewpoint where Earth became the subject.",
      status: "live"
    },
    {
      id: "person:william-anders",
      slug: "william-anders",
      label: "Person",
      name: "William Anders",
      summary: "Apollo 8 astronaut who photographed Earthrise.",
      status: "source_credit"
    },
    {
      id: "institution:nasa",
      slug: "nasa",
      label: "Institution",
      name: "NASA",
      summary: "Source institution for Apollo 8 Earthrise public-domain material.",
      status: "active"
    },
    {
      id: "theme:overview-effect",
      slug: "overview-effect",
      label: "Theme",
      name: "Overview Effect",
      summary: "Planetary awareness created by seeing Earth from space.",
      status: "active"
    },
    {
      id: "product:earthrise-print",
      slug: "earthrise-museum-print",
      label: "Product",
      name: "Earthrise Museum Giclee",
      summary: "Museum-grade print derived from the source image.",
      status: "live"
    },
    {
      id: "collection:great-barrier-reef",
      slug: "great-barrier-reef-collection",
      label: "Collection",
      name: "Great Barrier Reef Living Reef Collection",
      summary: "A reserved marine systems journey recommended from Earthrise.",
      status: "coming_soon"
    },
    {
      id: "collection:yellowstone",
      slug: "yellowstone-collection",
      label: "Collection",
      name: "Yellowstone Discovery Collection",
      summary: "A reserved preservation landscape journey recommended from Earthrise.",
      status: "coming_soon"
    }
  ],
  relationships: [
    { source: "collection:earthrise", target: "asset:earthrise-as08-14-2383", type: "FEATURES", reason: "The source image anchors the live collection.", weight: 1 },
    { source: "asset:earthrise-as08-14-2383", target: "institution:nasa", type: "PART_OF", reason: "NASA is the source institution for the asset.", weight: 1 },
    { source: "asset:earthrise-as08-14-2383", target: "person:william-anders", type: "DISCOVERED_BY", reason: "William Anders photographed the Earthrise frame during Apollo 8.", weight: 0.95 },
    { source: "asset:earthrise-as08-14-2383", target: "place:earthrise", type: "LOCATED_IN", reason: "The viewpoint is Apollo 8 lunar orbit.", weight: 1 },
    { source: "collection:earthrise", target: "product:earthrise-print", type: "RECOMMENDS", reason: "The museum print is the primary live edition.", weight: 0.92 },
    { source: "collection:earthrise", target: "theme:overview-effect", type: "INSPIRED", reason: "Earthrise is a canonical overview-effect artifact.", weight: 1 },
    { source: "collection:earthrise", target: "collection:great-barrier-reef", type: "RECOMMENDS", reason: "Continue from planetary awareness to marine planetary systems.", weight: 0.68 },
    { source: "collection:earthrise", target: "collection:yellowstone", type: "RECOMMENDS", reason: "Continue from planetary stewardship to preservation landscapes.", weight: 0.64 }
  ]
};
