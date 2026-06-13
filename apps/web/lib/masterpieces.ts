export type MasterpieceRecord = {
  slug: string;
  title: string;
  subtitle: string;
  sourceSystem: string;
  sourceRecordId: string;
  registryStatus: "published" | "candidate";
  masterpieceScore: number;
  collections: string[];
  primaryCollection: string;
  placeSlug: string;
  taxonName: string;
  rightsStatus: string;
  readinessState: "ready" | "review" | "hold";
  sourceUrl: string;
  imageSrc: string;
  imageAlt: string;
  narrative: string;
  candidateOnly: boolean;
};

export const masterpieceRuntime = {
  runtimeVersion: "NC-MASTERPIECES-001-v1",
  ioRuntimeVersion: "NC-IO-001-v1",
  totalMasterpieces: 3,
  top100Count: 3,
  collectionCount: 7,
  candidateCount: 2,
  publishedCount: 1
};

export const masterpieceRegistry: MasterpieceRecord[] = [
  {
    slug: "earthrise",
    title: "Earthrise",
    subtitle: "Apollo 8 frame AS08-14-2383",
    sourceSystem: "NASA",
    sourceRecordId: "AS08-14-2383",
    registryStatus: "published",
    masterpieceScore: 98,
    collections: ["earthrise", "space-earth-observation", "planetary-stewardship"],
    primaryCollection: "earthrise",
    placeSlug: "earthrise",
    taxonName: "",
    rightsStatus: "public_domain",
    readinessState: "ready",
    sourceUrl: "https://www.nasa.gov/image-article/apollo-8-earthrise/",
    imageSrc: "/images/earthrise-as08-14-2383.jpg",
    imageAlt: "Earth rising above the lunar horizon during Apollo 8",
    narrative: "A planetary image with unusually high cultural, educational, collection, and edition value.",
    candidateOnly: false
  },
  {
    slug: "acanthaster-planci-plate",
    title: "Acanthaster planci plate",
    subtitle: "BHL illustration candidate for Great Barrier Reef discovery",
    sourceSystem: "BHL",
    sourceRecordId: "bhl-item-1001:page:page-2001",
    registryStatus: "candidate",
    masterpieceScore: 84,
    collections: ["biodiversity-library", "bhl-illustration", "great-barrier-reef", "historic-natural-history", "marine-life"],
    primaryCollection: "biodiversity-library",
    placeSlug: "great-barrier-reef",
    taxonName: "Acanthaster planci",
    rightsStatus: "verified_pd",
    readinessState: "ready",
    sourceUrl: "https://www.biodiversitylibrary.org/page/2001",
    imageSrc: "https://www.biodiversitylibrary.org/pageimage/2001",
    imageAlt: "Historic BHL plate of Acanthaster planci",
    narrative: "A species-linked public-domain illustration candidate connecting taxonomy, reef collections, and educational products.",
    candidateOnly: true
  },
  {
    slug: "bison-bison-range-plate",
    title: "Bison bison range plate",
    subtitle: "BHL illustration candidate for Yellowstone discovery",
    sourceSystem: "BHL",
    sourceRecordId: "bhl-item-1002:page:page-2002",
    registryStatus: "candidate",
    masterpieceScore: 84,
    collections: ["bhl-illustration", "biodiversity-library", "historic-natural-history", "mammals", "yellowstone"],
    primaryCollection: "bhl-illustration",
    placeSlug: "yellowstone",
    taxonName: "Bison bison",
    rightsStatus: "verified_pd",
    readinessState: "ready",
    sourceUrl: "https://www.biodiversitylibrary.org/page/2002",
    imageSrc: "https://www.biodiversitylibrary.org/pageimage/2002",
    imageAlt: "Historic BHL plate of Bison bison",
    narrative: "A Yellowstone-linked public-domain natural history candidate with strong collection and product mapping.",
    candidateOnly: true
  }
];

export const masterpieceScore = Object.fromEntries(
  masterpieceRegistry.map((record) => [record.slug, record.masterpieceScore])
) as Record<string, number>;

export const masterpieceCollections = masterpieceRegistry.reduce<Record<string, MasterpieceRecord[]>>(
  (groups, record) => {
    for (const collection of record.collections) {
      groups[collection] = [...(groups[collection] ?? []), record];
    }
    return groups;
  },
  {}
);

export function getMasterpiece(slug: string) {
  return masterpieceRegistry.find((record) => record.slug === slug);
}

export const top100Masterpieces = masterpieceRegistry.slice(0, 100);
