import type { Metadata } from "next";
import Link from "next/link";
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";
import { ManualPurchaseCTA } from "@/components/ManualPurchaseCTA";
import { getPhaseZeroProducts } from "@/lib/api";

export const metadata: Metadata = {
  title: "Products",
  description: "Phase 0 products from verified public-domain sources."
};

export default async function ProductsPage() {
  const products = await getPhaseZeroProducts();

  return (
    <section className="page">
      <p className="eyebrow">Products</p>
      <h1>Phase 0 products</h1>
      <p className="lead">
        Earthrise is the only public product family in Phase 0. Manual purchase is enabled after
        governed verification.
      </p>

      <div className="grid">
        {products.map((product) => (
          <article className="card" key={product.code}>
            <p className="eyebrow">{product.phase}</p>
            <h2>{product.title}</h2>
            <div className="badge-row">
              <span className="badge">Public domain</span>
              <span className="badge">Manual purchase</span>
            </div>
            <p>{product.description}</p>
            <Link href={product.route}>View Earthrise</Link>
          </article>
        ))}
      </div>

      <ManualPurchaseCTA productName="Earthrise" />
      <EarthriseAttributionBlock />
    </section>
  );
}
