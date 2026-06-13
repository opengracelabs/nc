import { EARTHRISE_RIGHTS, NASA_EARTHRISE_CREDIT, NASA_NONENDORSEMENT } from "@/lib/governed-content";

export const foundingCurator = {
  slug: "founding-curator",
  name: "Nathan Holderhead",
  title: "Founding Curator",
  credentials: "Nature & Culture founding curator for public-domain collections, source literacy, and edition governance.",
  biography:
    "Nathan Holderhead leads Nature & Culture's public collection program, connecting source records, institutional context, visitor journeys, and edition governance. His curatorial work focuses on public-domain cultural memory, place-based collections, and transparent source attribution.",
  philosophy:
    "A collection should make its evidence visible. The visitor should be able to see the source, understand the rights basis, follow the editorial path, and know who is accountable for the final publication.",
  signature: "Nathan Holderhead, Founding Curator"
};

export const certificateRecord = {
  certificateId: "NC-COA-EARTHRISE-0001",
  workTitle: "Earthrise",
  collectionTitle: "Earthrise: The Oasis Collection",
  sourceInstitution: "NASA",
  sourceIdentifier: "AS08-14-2383",
  creator: "William Anders",
  mission: "Apollo 8",
  date: "December 24, 1968",
  rights: EARTHRISE_RIGHTS,
  attribution: NASA_EARTHRISE_CREDIT,
  nonendorsement: NASA_NONENDORSEMENT,
  verificationStatus: "Source verified",
  signatoryName: foundingCurator.name,
  signatoryTitle: foundingCurator.title,
  signatorySlug: foundingCurator.slug,
  curatorStatement:
    "This certificate links the edition to the public NASA source record and preserves the difference between source attribution, institutional custody, and product publication."
};

export const editionRegistry = [
  {
    registryId: "NC-REG-EARTHRISE-MP-0001",
    title: "Earthrise Museum Giclee",
    format: "24 x 20 inch archival print",
    editionType: "Physical museum edition",
    status: "Manual purchase available",
    certificateId: certificateRecord.certificateId,
    sourceIdentifier: certificateRecord.sourceIdentifier
  },
  {
    registryId: "NC-REG-EARTHRISE-DD-0001",
    title: "Earthrise Digital Download",
    format: "High-resolution digital edition",
    editionType: "Digital study edition",
    status: "Manual purchase available",
    certificateId: certificateRecord.certificateId,
    sourceIdentifier: certificateRecord.sourceIdentifier
  }
];

export const educationalUsePanel = {
  title: "Educational Use Panel",
  copy:
    "Educators may use the source notes, attribution text, and rights basis to discuss Apollo 8, public-domain government works, visual culture, and environmental memory.",
  uses: ["Classroom projection", "Lecture reference", "Source literacy", "Collection study"]
};

export const sourceInstitutionPanel = {
  title: "Source Institution Panel",
  institution: "NASA",
  copy:
    "Nature & Culture attributes the image to NASA as the source institution. NASA does not endorse this product or publication.",
  sourceUrl: "https://www.nasa.gov/image-article/apollo-8-earthrise/"
};


export type TrustInstitution = {
  slug: string;
  name: string;
  type: string;
  role: string;
  summary: string;
  profile: string;
  collections: string[];
  sourceDisplay: string;
};

export type TrustCurator = {
  slug: string;
  name: string;
  title: string;
  summary: string;
  profile: string;
  biography: string;
  collections: string[];
  byline: string;
  signatoryLabel: string;
  isFoundingCurator?: boolean;
};

export const trustInstitutions: TrustInstitution[] = [
  {
    slug: "nature-culture",
    name: "Nature & Culture",
    type: "Publishing institution",
    role: "Collection owner and publisher",
    summary:
      "Owns the collection experience, curatorial framing, edition records, and visitor pathways.",
    profile:
      "Nature & Culture publishes source-traceable collections that connect public-domain works, place narratives, education, conservation context, and carefully governed commerce.",
    collections: ["earthrise", "alhambra", "south-georgia", "versailles", "chichen-itza", "petra"],
    sourceDisplay: "Collection owner"
  },
  {
    slug: "nasa",
    name: "NASA",
    type: "Source institution",
    role: "Earthrise source institution",
    summary:
      "Source institution for the Apollo 8 Earthrise photograph and source attribution record.",
    profile:
      "NASA is presented as the source institution for Earthrise. Nature & Culture displays NASA attribution and nonendorsement language wherever the Earthrise source record is used.",
    collections: ["earthrise"],
    sourceDisplay: "NASA / Apollo 8 source"
  },
  {
    slug: "unesco-world-heritage",
    name: "UNESCO World Heritage Centre",
    type: "Source authority",
    role: "World Heritage designation context",
    summary:
      "Designation context for Alhambra, Versailles, Chichen Itza, and Petra collection records.",
    profile:
      "UNESCO World Heritage designation is used as contextual authority for place collections. The collection pages remain Nature & Culture publications and do not imply source endorsement.",
    collections: ["alhambra", "versailles", "chichen-itza", "petra"],
    sourceDisplay: "UNESCO World Heritage designation"
  },
  {
    slug: "south-georgia-heritage",
    name: "South Georgia Heritage Sources",
    type: "Source context",
    role: "Expedition and conservation context",
    summary:
      "Source context for South Georgia expedition, ecological recovery, and conservation storytelling.",
    profile:
      "South Georgia institutional trust is presented through expedition heritage, conservation context, and careful separation of source context from Nature & Culture publication ownership.",
    collections: ["south-georgia"],
    sourceDisplay: "Expedition and conservation source context"
  }
];

export const trustCurators: TrustCurator[] = [
  {
    slug: foundingCurator.slug,
    name: foundingCurator.name,
    title: foundingCurator.title,
    summary:
      "Named curator responsible for Nature & Culture collection bylines, certificate signatory records, and public source posture.",
    profile: foundingCurator.philosophy,
    biography: foundingCurator.biography,
    collections: ["earthrise", "alhambra", "south-georgia", "versailles", "chichen-itza", "petra"],
    byline: `Curated by ${foundingCurator.name}`,
    signatoryLabel: foundingCurator.signature,
    isFoundingCurator: true
  }
];

export const collectionTrustProfiles: Record<string, { institutionSlug: string; curatorSlug: string }> = {
  earthrise: { institutionSlug: "nasa", curatorSlug: foundingCurator.slug },
  alhambra: { institutionSlug: "unesco-world-heritage", curatorSlug: foundingCurator.slug },
  "south-georgia": { institutionSlug: "south-georgia-heritage", curatorSlug: foundingCurator.slug },
  versailles: { institutionSlug: "unesco-world-heritage", curatorSlug: foundingCurator.slug },
  "chichen-itza": { institutionSlug: "unesco-world-heritage", curatorSlug: foundingCurator.slug },
  petra: { institutionSlug: "unesco-world-heritage", curatorSlug: foundingCurator.slug }
};

export function getTrustInstitution(slug: string) {
  return trustInstitutions.find((institution) => institution.slug === slug);
}

export function getTrustCurator(slug: string) {
  return trustCurators.find((curator) => curator.slug === slug);
}

export function getCollectionTrustProfile(collectionSlug: string) {
  const profile = collectionTrustProfiles[collectionSlug];
  if (!profile) {
    return undefined;
  }
  const institution = getTrustInstitution(profile.institutionSlug);
  const curator = getTrustCurator(profile.curatorSlug);
  if (!institution || !curator) {
    return undefined;
  }
  return { institution, curator };
}


export const publicProvenanceChain = [
  {
    step: "Source record",
    title: "NASA Apollo 8 image record",
    detail: "Earthrise frame AS08-14-2383, photographed by William Anders on December 24, 1968."
  },
  {
    step: "Rights basis",
    title: "United States Government Work",
    detail: EARTHRISE_RIGHTS
  },
  {
    step: "Collection record",
    title: "Earthrise: The Oasis Collection",
    detail: "Nature & Culture collection context, story, educational framing, and edition pathways."
  },
  {
    step: "Certificate record",
    title: certificateRecord.certificateId,
    detail: "Certificate links source, attribution, curator statement, nonendorsement, and edition registry."
  },
  {
    step: "Edition registry",
    title: "Public edition verification",
    detail: "Registered editions inherit the same public-domain source record and certificate link."
  }
];

export function normalizeCertificateSlug(certificate: string) {
  return certificate.trim().toUpperCase();
}

export function getCertificateRecord(certificate: string) {
  return normalizeCertificateSlug(certificate) === certificateRecord.certificateId
    ? certificateRecord
    : undefined;
}

export function getEditionsForCertificate(certificate: string) {
  const normalized = normalizeCertificateSlug(certificate);
  return editionRegistry.filter((edition) => edition.certificateId === normalized);
}

export function isCertificateVerified(certificate: string) {
  return Boolean(getCertificateRecord(certificate));
}
