import Link from "next/link";
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";
import { getPhaseZeroProducts, getPlaceTeasers } from "@/lib/api";

export default async function HomePage() {
  const [products, places] = await Promise.all([getPhaseZeroProducts(), getPlaceTeasers()]);

  return (
    <>
      <section className="hero">
        <div>
          <p className="eyebrow">Phase 0 public launch</p>
          <h1>Earthrise, with provenance visible.</h1>
          <p className="lead">
            Nature & Culture publishes public-domain heritage stories and products only after
            rights, source, and attribution checks are visible on the page.
          </p>
          <Link className="button" href="/products/earthrise">
            Shop Earthrise
          </Link>
        </div>
        <div className="hero-media" role="img" aria-label="Earthrise inspired public-domain visual" />
      </section>

      <section className="section">
        <h2>Phase 0 products</h2>
        <div className="grid">
          {products.map((product) => (
            <article className="card" key={product.code}>
              <p className="eyebrow">{product.code}</p>
              <h2>{product.title}</h2>
              <p>{product.description}</p>
              <Link href={product.route}>View product</Link>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Places</h2>
        <div className="grid">
          {places.map((place) => (
            <article className="card" key={place.slug}>
              <h2>{place.title}</h2>
              <p>{place.status}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <EarthriseAttributionBlock />
      </section>
    </>
  );
}
