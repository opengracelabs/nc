import type { Metadata } from "next";
import Link from "next/link";
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";
import { ManualPurchaseCTA } from "@/components/ManualPurchaseCTA";
import { getEarthriseProducts } from "@/lib/api";

export const metadata: Metadata = {
  title: "Products",
  description: "Earthrise editions from a verified public-domain NASA source."
};

export default async function ProductsPage() {
  const products = await getEarthriseProducts();

  return (
    <section className="page product-index">
      <p className="eyebrow">Editions</p>
      <h1>Earthrise editions</h1>
      <p className="lead">
        Two ways to own or study the Apollo 8 image: a museum-grade print for the wall, and a
        digital edition for close viewing and personal archival use.
      </p>

      <div className="grid edition-grid">
        {products.map((product) => (
          <article className="card product-card" key={product.code}>
            <h2>{product.title}</h2>
            <div className="badge-row">
              <span className="badge">Public domain source</span>
              <span className="badge">NASA credit included</span>
            </div>
            <p>{product.description}</p>
            <Link href={product.route}>Compare editions</Link>
          </article>
        ))}
      </div>

      <ManualPurchaseCTA productName="Earthrise" />
      <EarthriseAttributionBlock />
    </section>
  );
}
