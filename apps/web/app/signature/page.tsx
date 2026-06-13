import type { Metadata } from "next";
import Link from "next/link";
import { signatureCollections } from "@/lib/collections";

export const metadata: Metadata = {
  title: "Signature Collection Hub",
  description: "Five flagship Nature & Culture collections for museum-quality discovery."
};

const [heroCollection, ...supportingCollections] = signatureCollections;

export default function SignatureCollectionHubPage() {
  return (
    <article className="signature-page">
      <section className="signature-hero">
        <img src={heroCollection.imageSrc} alt={heroCollection.imageAlt} />
        <div className="signature-hero-copy">
          <p className="eyebrow light-eyebrow">Signature Collection Hub</p>
          <h1>Five collections for deep looking.</h1>
          <p className="lead hero-lead">
            A visitor path through architecture, expedition, landscape, astronomy, and carved
            stone. Each collection opens from a place into stories, works, products, and related
            journeys.
          </p>
          <div className="button-row">
            <Link className="button" href={`/collections/${heroCollection.slug}`}>
              Enter {heroCollection.shortTitle}
            </Link>
            <Link className="button secondary-button signature-secondary" href="/collections">
              View all collections
            </Link>
          </div>
        </div>
        <p className="hero-credit">{heroCollection.credit}</p>
      </section>

      <section className="section signature-intro-section">
        <p className="eyebrow">The flagship five</p>
        <h2>Designed as collection entrances, not catalog lists.</h2>
        <div className="two-column-copy editorial-copy">
          <p>
            The signature hub is built for visitors who want a clear first step into the collection
            system: a strong visual impression, a precise story proposition, and a visible path to
            related places.
          </p>
          <p>
            Each card leads to a complete collection page with hero, narrative, discovery journey,
            featured works, products, and related collections already in place.
          </p>
        </div>
      </section>

      <section className="section signature-gallery-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">Collections</p>
          <h2>Choose a first journey.</h2>
        </div>
        <div className="signature-gallery">
          {signatureCollections.map((collection, index) => (
            <Link
              className={index === 0 ? "signature-card signature-card-large" : "signature-card"}
              href={`/collections/${collection.slug}`}
              key={collection.slug}
            >
              <img src={collection.imageSrc} alt={collection.imageAlt} />
              <span className="signature-card-index">{String(index + 1).padStart(2, "0")}</span>
              <div>
                <p className="eyebrow light-eyebrow">{collection.authority}</p>
                <h3>{collection.title}</h3>
                <p>{collection.summary}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="section signature-pathway-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">Visitor paths</p>
          <h2>Move by atmosphere, evidence, or place.</h2>
        </div>
        <div className="signature-pathway-grid">
          <article>
            <span>01</span>
            <h3>Architecture and power</h3>
            <p>Alhambra and Versailles frame water, garden, geometry, and ceremony.</p>
          </article>
          <article>
            <span>02</span>
            <h3>Stone and time</h3>
            <p>Petra and Chichen Itza connect geology, movement, astronomy, and civic space.</p>
          </article>
          <article>
            <span>03</span>
            <h3>Expedition and recovery</h3>
            <p>South Georgia opens the polar archive through exploration and ecological return.</p>
          </article>
        </div>
      </section>

      <section className="section signature-related-section">
        <p className="eyebrow">Continue</p>
        <h2>From signature collections into the wider catalog.</h2>
        <div className="button-row">
          {supportingCollections.slice(0, 3).map((collection) => (
            <Link className="button secondary-button" href={`/collections/${collection.slug}`} key={collection.slug}>
              {collection.shortTitle}
            </Link>
          ))}
        </div>
      </section>
    </article>
  );
}
