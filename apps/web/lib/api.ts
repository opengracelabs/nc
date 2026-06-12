import { phaseZeroProducts, placeTeasers, type ProductSummary } from "./governed-content";

const apiBaseUrl = process.env.NC_API_BASE_URL;

async function getJson<T>(path: string): Promise<T | null> {
  if (!apiBaseUrl) {
    return null;
  }

  try {
    const response = await fetch(`${apiBaseUrl}${path}`, {
      headers: { accept: "application/json" },
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

export async function getPhaseZeroProducts(): Promise<ProductSummary[]> {
  const packages = await getJson<Array<{ product_code?: string; production_status?: string }>>(
    "/products/production-packages"
  );

  if (!packages) {
    return phaseZeroProducts;
  }

  const approvedCodes = new Set(
    packages
      .filter((item) => item.product_code === "NC-PROD-001" || item.product_code === "NC-PROD-008")
      .map((item) => item.product_code)
  );

  const filtered = phaseZeroProducts.filter((product) => approvedCodes.has(product.code));
  return filtered.length > 0 ? filtered : phaseZeroProducts;
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
