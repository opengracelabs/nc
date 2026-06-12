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

export const collections: CollectionMetadata[] = [earthriseCollection];

export function getCollectionBySlug(slug: string) {
  return collections.find((collection) => collection.slug === slug);
}
