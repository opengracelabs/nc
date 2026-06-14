import { institutionFactoryRecords } from "@/lib/institution-factory";
import { masterpieceRegistry } from "@/lib/masterpieces";
import { placeFactoryDashboardRows } from "@/lib/place-factory-dashboard";

export type CollectionReadiness = "Ready" | "Review" | "Hold";

export type CollectionFamilyRecord = {
  familySlug: string;
  label: string;
  referenceSources: string[];
  scaleTarget: number;
  description: string;
};

export type CollectionRegistryRecord = {
  collectionSlug: string;
  title: string;
  familySlug: string;
  place: string;
  institution: string;
  assetCount: number;
  taxaCount: number;
  masterpieceCount: number;
  readiness: CollectionReadiness;
};

export type CollectionActivationRecord = {
  collectionSlug: string;
  activationScore: number;
  activationState: CollectionReadiness;
  activationPath: string;
  blockingAction: string;
};

export const collectionFactoryRuntime = {
  runtimeName: "Collection Factory Runtime",
  runtimeVersion: "NC-SCALE-001-v1",
  scaleTargets: {
    places: 2000,
    collections: 10000,
    assets: 1000000,
    illustrationOpportunities: 100000
  },
  referenceSources: [
    "Smithsonian Open Access",
    "Europeana",
    "Google Arts & Culture",
    "GBIF",
    "BHL"
  ]
};

export const collection_family_registry: CollectionFamilyRecord[] = [
  {
    familySlug: "world-heritage",
    label: "World Heritage Collection",
    referenceSources: ["Europeana", "Google Arts & Culture", "Smithsonian Open Access"],
    scaleTarget: 2200,
    description: "Place-led cultural and natural heritage collections with institution-backed assets."
  },
  {
    familySlug: "biodiversity-library",
    label: "Biodiversity Library Collection",
    referenceSources: ["BHL", "GBIF"],
    scaleTarget: 2800,
    description: "Taxon-led illustration collections sourced from public-domain natural history literature."
  },
  {
    familySlug: "open-access-masterworks",
    label: "Open Access Masterworks",
    referenceSources: ["Smithsonian Open Access", "Europeana", "Google Arts & Culture"],
    scaleTarget: 2500,
    description: "Institutional open-access masterworks routed into collection and commerce readiness."
  },
  {
    familySlug: "planetary-observation",
    label: "Planetary Observation Collection",
    referenceSources: ["Smithsonian Open Access", "Google Arts & Culture"],
    scaleTarget: 1200,
    description: "Planetary-scale images and records organized around place, stewardship, and education."
  },
  {
    familySlug: "extinction-archive",
    label: "Extinction Archive",
    referenceSources: ["BHL", "GBIF", "Smithsonian Open Access"],
    scaleTarget: 1300,
    description: "Lost and threatened species collections linked to taxa, places, and conservation narratives."
  }
];

export const collection_registry: CollectionRegistryRecord[] = [
  {
    collectionSlug: "earthrise",
    title: "Earthrise: The Oasis Collection",
    familySlug: "planetary-observation",
    place: "Earthrise",
    institution: "NASA",
    assetCount: 3,
    taxaCount: 0,
    masterpieceCount: 1,
    readiness: "Ready"
  },
  {
    collectionSlug: "yellowstone-natural-history",
    title: "Yellowstone Natural History Collection",
    familySlug: "world-heritage",
    place: "Yellowstone",
    institution: "Smithsonian / BHL",
    assetCount: 2,
    taxaCount: 1,
    masterpieceCount: 1,
    readiness: "Review"
  },
  {
    collectionSlug: "great-barrier-reef-biodiversity",
    title: "Great Barrier Reef Biodiversity Collection",
    familySlug: "biodiversity-library",
    place: "Great Barrier Reef",
    institution: "BHL / GBIF",
    assetCount: 2,
    taxaCount: 1,
    masterpieceCount: 1,
    readiness: "Review"
  },
  {
    collectionSlug: "alhambra-ornament",
    title: "Alhambra Ornament Collection",
    familySlug: "open-access-masterworks",
    place: "Alhambra",
    institution: "Europeana",
    assetCount: 1,
    taxaCount: 0,
    masterpieceCount: 0,
    readiness: "Ready"
  },
  {
    collectionSlug: "extinction-archive",
    title: "Extinction Archive Collection",
    familySlug: "extinction-archive",
    place: "Eastern North America",
    institution: "BHL / Smithsonian",
    assetCount: 4,
    taxaCount: 4,
    masterpieceCount: 0,
    readiness: "Hold"
  }
];

export const collection_activation_registry: CollectionActivationRecord[] = [
  {
    collectionSlug: "earthrise",
    activationScore: 96,
    activationState: "Ready",
    activationPath: "Published collection plus product route",
    blockingAction: "None"
  },
  {
    collectionSlug: "yellowstone-natural-history",
    activationScore: 88,
    activationState: "Review",
    activationPath: "Place page plus BHL and Smithsonian asset confirmation",
    blockingAction: "Resolve Smithsonian high-resolution upgrade"
  },
  {
    collectionSlug: "great-barrier-reef-biodiversity",
    activationScore: 84,
    activationState: "Review",
    activationPath: "GBIF taxon validation plus BHL illustration source",
    blockingAction: "Complete source image verification"
  },
  {
    collectionSlug: "alhambra-ornament",
    activationScore: 82,
    activationState: "Ready",
    activationPath: "Europeana public-domain source mapped to signature collection",
    blockingAction: "None"
  },
  {
    collectionSlug: "extinction-archive",
    activationScore: 79,
    activationState: "Hold",
    activationPath: "BHL first release, Smithsonian Open Access upgrade later",
    blockingAction: "Confirm rights and resolution for paired portfolio"
  }
];

export const masterpiece_registry = masterpieceRegistry.map((record) => ({
  masterpieceSlug: record.slug,
  title: record.title,
  collectionSlug: record.primaryCollection,
  sourceSystem: record.sourceSystem,
  score: record.masterpieceScore,
  readiness: record.readinessState
}));

export const collection_candidates = collection_registry.map((record) => {
  const family = collection_family_registry.find((item) => item.familySlug === record.familySlug);
  return {
    ...record,
    familyLabel: family?.label ?? record.familySlug,
    referenceSources: family?.referenceSources ?? []
  };
});

export const collection_readiness = collection_registry.reduce<Record<CollectionReadiness, number>>(
  (counts, record) => {
    counts[record.readiness] += 1;
    return counts;
  },
  { Ready: 0, Review: 0, Hold: 0 }
);

export const collection_activation = collection_activation_registry.map((activation) => {
  const collection = collection_registry.find((record) => record.collectionSlug === activation.collectionSlug);
  return {
    ...activation,
    title: collection?.title ?? activation.collectionSlug,
    familySlug: collection?.familySlug ?? "unknown"
  };
});

export const collectionFactoryDashboardSummary = {
  places: placeFactoryDashboardRows.length,
  institutions: institutionFactoryRecords.length,
  assets: collection_registry.reduce((total, record) => total + record.assetCount, 0),
  taxa: collection_registry.reduce((total, record) => total + record.taxaCount, 0),
  collections: collection_registry.length,
  masterpieces: masterpiece_registry.length
};
