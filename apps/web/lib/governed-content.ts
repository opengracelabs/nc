export const NASA_EARTHRISE_CREDIT =
  "NASA: Photograph by William Anders, Apollo 8, December 24, 1968. § 105 — public domain.";

export const NASA_NONENDORSEMENT =
  "Image credit: NASA. NASA does not endorse this product.";

export const EARTHRISE_RIGHTS =
  "Public domain — United States Government Work, 17 U.S.C. § 105";

export type ProductStatus = "manual_purchase_available" | "coming_soon";

export type ProductSummary = {
  code: string;
  title: string;
  route: string;
  status: ProductStatus;
  phase: "Phase 0";
  description: string;
};

export const phaseZeroProducts: ProductSummary[] = [
  {
    code: "NC-PROD-001",
    title: "Earthrise Museum Giclee",
    route: "/products/earthrise",
    status: "manual_purchase_available",
    phase: "Phase 0",
    description:
      "Museum-grade print from the Apollo 8 Earthrise photograph, available through manual purchase."
  },
  {
    code: "NC-PROD-008",
    title: "Earthrise Digital Download",
    route: "/products/earthrise",
    status: "manual_purchase_available",
    phase: "Phase 0",
    description:
      "Governed digital edition from the same verified public-domain Earthrise source."
  }
];

export const placeTeasers = [
  {
    slug: "earthrise",
    title: "Earthrise",
    status: "Live Phase 0"
  },
  {
    slug: "yellowstone",
    title: "Yellowstone",
    status: "Coming soon"
  },
  {
    slug: "grand-canyon",
    title: "Grand Canyon",
    status: "Coming soon"
  },
  {
    slug: "great-barrier-reef",
    title: "Great Barrier Reef",
    status: "Coming soon"
  },
  {
    slug: "galapagos",
    title: "Galapagos",
    status: "Coming soon"
  }
];
