import { earthriseProducts, placeTeasers, type ProductSummary } from "./governed-content";
import { fallbackGraphJourney, type GraphJourney } from "./graph";

const apiBaseUrl = process.env.NC_API_BASE_URL;
const apiToken = process.env.NC_API_TOKEN;

export type ReviewedPageGeneration = {
  hero_text: string;
  story_text: string;
  product_text: string;
  education_text: string;
  tourism_text: string;
  attribution_block: string;
  source_references: Array<{ source_record_id?: string; title?: string }>;
  review_status: string;
  publication_allowed: boolean;
};

async function getJson<T>(path: string): Promise<T | null> {
  if (!apiBaseUrl) {
    return null;
  }

  try {
    const response = await fetch(`${apiBaseUrl}${path}`, {
      headers: {
        accept: "application/json",
        ...(apiToken ? { authorization: "Bearer " + apiToken } : {})
      },
      next: { revalidate: 120 }
    });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

export async function getEarthriseProducts(): Promise<ProductSummary[]> {
  const packages = await getJson<Array<{ product_code?: string; production_status?: string }>>(
    "/products/production-packages"
  );

  if (!packages) {
    return earthriseProducts;
  }

  const approvedCodes = new Set(
    packages
      .filter((item) => item.product_code === "NC-PROD-001" || item.product_code === "NC-PROD-008")
      .map((item) => item.product_code)
  );

  const filtered = earthriseProducts.filter((product) => approvedCodes.has(product.code));
  return filtered.length > 0 ? filtered : earthriseProducts;
}

export async function getPlaceTeasers() {
  const anchors = await getJson<Array<{ slug: string; title: string; status?: string }>>(
    "/pilot/anchors"
  );

  if (!anchors) {
    return placeTeasers;
  }

  const allowed = new Set(placeTeasers.map((place) => place.slug));
  const mapped = anchors
    .filter((anchor) => allowed.has(anchor.slug))
    .map((anchor) => ({
      slug: anchor.slug,
      title: anchor.title,
      status: anchor.status === "live" ? "Live" : "Coming soon"
    }));

  return mapped.length > 0 ? mapped : placeTeasers;
}

export async function getReviewedPageGeneration(
  pageType: string,
  anchorSlug: string
): Promise<ReviewedPageGeneration | null> {
  const page = await getJson<ReviewedPageGeneration>(
    `/ai/page-generation/${pageType}/${anchorSlug}`
  );

  if (!page || page.publication_allowed !== true || page.review_status !== "approved") {
    return null;
  }
  return page;
}

export async function getGraphJourney(slug: string): Promise<GraphJourney> {
  const journey = await getJson<GraphJourney>(`/graph/journey/${slug}`);
  return journey ?? fallbackGraphJourney;
}
