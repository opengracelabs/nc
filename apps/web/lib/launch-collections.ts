import {
  activationDashboardRows,
  type ActivationDashboardRow,
  type ActivationReadiness
} from "@/lib/place-activation-dashboard";

export type LaunchCollectionCard = {
  slug: string;
  title: string;
  place: string;
  country: string;
  region: string;
  designationFamily: string;
  collectionFamily: string;
  collectionFamilyLabel: string;
  collectionFamilySlug: string;
  authorityReadiness: ActivationReadiness;
  collectionReadiness: ActivationReadiness;
  productReadiness: ActivationReadiness;
  graphReadiness: ActivationReadiness;
  publishingReadiness: ActivationReadiness;
  activationScore: number;
};

export type LaunchCollectionFamily = {
  slug: string;
  label: string;
  collectionFamily: string;
  collections: LaunchCollectionCard[];
  readinessCounts: Record<ActivationReadiness, number>;
};

const FAMILY_LABELS: Record<string, string> = {
  world_heritage_collection: "World Heritage Collection",
  biosphere_collection: "Biosphere Collection",
  geopark_collection: "Geopark Collection",
  wetland_collection: "Wetland Collection",
  ich_collection: "ICH Collection",
  dark_sky_collection: "Dark Sky Collection",
  marine_collection: "Marine Collection"
};

function titleCase(value: string) {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function familyLabel(collectionFamily: string) {
  return FAMILY_LABELS[collectionFamily] ?? titleCase(collectionFamily);
}

function familySlug(collectionFamily: string) {
  return collectionFamily.replace(/_collection$/, "").replaceAll("_", "-");
}

function cardFromActivation(row: ActivationDashboardRow): LaunchCollectionCard {
  const label = familyLabel(row.collectionFamily);
  return {
    slug: row.placeSlug,
    title: `${row.place}: ${label}`,
    place: row.place,
    country: row.country,
    region: row.region,
    designationFamily: row.designationFamily,
    collectionFamily: row.collectionFamily,
    collectionFamilyLabel: label,
    collectionFamilySlug: familySlug(row.collectionFamily),
    authorityReadiness: row.authorityReadiness,
    collectionReadiness: row.collectionReadiness,
    productReadiness: row.productReadiness,
    graphReadiness: row.graphReadiness,
    publishingReadiness: row.publishingReadiness,
    activationScore: row.activationScore
  };
}

export const flagshipCollections: LaunchCollectionCard[] = activationDashboardRows
  .slice(0, 10)
  .map(cardFromActivation);

export const launchCollectionFamilies: LaunchCollectionFamily[] = Object.values(
  activationDashboardRows.reduce<Record<string, LaunchCollectionFamily>>((families, row) => {
    const card = cardFromActivation(row);
    const existing = families[card.collectionFamilySlug] ?? {
      slug: card.collectionFamilySlug,
      label: card.collectionFamilyLabel,
      collectionFamily: card.collectionFamily,
      collections: [],
      readinessCounts: { Ready: 0, Review: 0, Hold: 0 }
    };
    existing.collections.push(card);
    existing.readinessCounts[card.collectionReadiness] += 1;
    families[card.collectionFamilySlug] = existing;
    return families;
  }, {})
).map((family) => ({
  ...family,
  collections: family.collections.slice(0, 25)
}));

export function getLaunchCollectionFamily(slug: string) {
  return launchCollectionFamilies.find((family) => family.slug === slug);
}
