export type InstitutionFactoryRecord = {
  institutionSlug: string;
  displayName: string;
  sourceSystems: string[];
  readiness: "ready" | "review" | "hold";
  readinessScore: number;
  assetCount: number;
  collectionCount: number;
  collections: string[];
  rightsStatus: string;
};

export const institutionFactorySummary = {
  runtimeVersion: "NC-INSTITUTIONS-100-v1",
  assetFactoryVersion: "NC-ASSETS-1000000-v1",
  institutionCount: 8,
  assetCount: 8,
  collectionMappingCount: 9,
  candidateOnly: true,
  canonicalInstitutionCreated: false,
  canonicalPublicationCreated: false
};

export const institutionFactoryRecords: InstitutionFactoryRecord[] = [
  {
    institutionSlug: "biodiversity-heritage-library",
    displayName: "Biodiversity Heritage Library",
    sourceSystems: ["BHL"],
    readiness: "ready",
    readinessScore: 100.0,
    assetCount: 1,
    collectionCount: 2,
    collections: ["biodiversity-library", "yellowstone"],
    rightsStatus: "verified_pd"
  },
  {
    institutionSlug: "europeana",
    displayName: "Europeana",
    sourceSystems: ["Europeana"],
    readiness: "ready",
    readinessScore: 100.0,
    assetCount: 1,
    collectionCount: 1,
    collections: ["alhambra"],
    rightsStatus: "verified_pd"
  },
  {
    institutionSlug: "nasa",
    displayName: "NASA",
    sourceSystems: ["NASA"],
    readiness: "ready",
    readinessScore: 100.0,
    assetCount: 1,
    collectionCount: 1,
    collections: ["earthrise"],
    rightsStatus: "verified_pd"
  },
  {
    institutionSlug: "national-archives-and-records-administration",
    displayName: "National Archives and Records Administration",
    sourceSystems: ["NARA"],
    readiness: "review",
    readinessScore: 62.0,
    assetCount: 1,
    collectionCount: 1,
    collections: ["grand-canyon"],
    rightsStatus: "pending_verification"
  },
  {
    institutionSlug: "natural-history-museum",
    displayName: "Natural History Museum",
    sourceSystems: ["NHM"],
    readiness: "review",
    readinessScore: 62.0,
    assetCount: 1,
    collectionCount: 1,
    collections: ["natural-history"],
    rightsStatus: "verified_cc0"
  },
  {
    institutionSlug: "noaa",
    displayName: "NOAA",
    sourceSystems: ["NOAA"],
    readiness: "review",
    readinessScore: 62.0,
    assetCount: 1,
    collectionCount: 1,
    collections: ["great-barrier-reef"],
    rightsStatus: "source_observed"
  },
  {
    institutionSlug: "rijksmuseum",
    displayName: "Rijksmuseum",
    sourceSystems: ["Rijksmuseum"],
    readiness: "ready",
    readinessScore: 100.0,
    assetCount: 1,
    collectionCount: 1,
    collections: ["yosemite"],
    rightsStatus: "verified_pd"
  },
  {
    institutionSlug: "smithsonian",
    displayName: "Smithsonian",
    sourceSystems: ["Smithsonian"],
    readiness: "review",
    readinessScore: 100.0,
    assetCount: 1,
    collectionCount: 1,
    collections: ["yellowstone"],
    rightsStatus: "open_access"
  }
];
