import type { Metadata } from "next";
import Link from "next/link";
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";
import {
  Breadcrumbs,
  FeaturedWorksGrid,
  NextJourneys,
  ProvenanceGlance
} from "@/components/CollectionExperience";
import { earthriseCollection as collection } from "@/lib/collections";
import { getCollectionTrustProfile } from "@/lib/trust";

export const metadata: Metadata = {
  title: collection.seoTitle,
  description: collection.seoDescription,
  alternates: {
    canonical: "/collections/earthrise"
  },
  openGraph: {
    title: collection.seoTitle,
    description: collection.seoDescription,
    type: "article",
    images: [collection.imageSrc]
  }
};

export default function EarthriseCollectionPage() {
  const trustProfile = getCollectionTrustProfile(collection.slug);

  return (
    <article className="collection-detail-page">
      <section className="collection-hero">
        <img className="collection-hero-image" src={collection.imageSrc} alt={collection.imageAlt} />
        <div className="collection-hero-copy">
          <Breadcrumbs
            items={[
              { href: "/", label: "Home" },
              { href: "/collections", label: "Collections" },
              { label: collection.shortTitle }
            ]}
          />
          <p className="eyebrow light-eyebrow">{collection.authority}</p>
          <span className="masterwork-badge">{collection.badge}</span>
          <h1>{collection.title}</h1>
          <p className="lead hero-lead">
            A curated suite of records documenting the moment humanity first saw its home from the
            cradle of the Moon.
          </p>
          {trustProfile ? (
            <div className="collection-trust-byline">
              <Link href={`/curators/${trustProfile.curator.slug}`}>
                {trustProfile.curator.byline}
              </Link>
              <Link href={`/institutions/${trustProfile.institution.slug}`}>
                Source institution: {trustProfile.institution.name}
              </Link>
            </div>
          ) : null}
        </div>
        <p className="hero-credit">{collection.credit}</p>
      </section>

      <ProvenanceGlance items={collection.provenanceGlance} />

      <section className="section curator-statement-section">
        <p className="eyebrow">Curator statement</p>
        <blockquote>{collection.curatorStatement}</blockquote>
      </section>

      <section className="section collection-narrative-section">
        <p className="eyebrow">Collection narrative</p>
        <h2>{collection.narrativeTitle}</h2>
        <div className="two-column-copy editorial-copy">
          <p>{collection.narrative[0]}</p>
          <p>{collection.narrative[1]}</p>
        </div>
      </section>

      <section className="section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">Discovery pathways</p>
          <h2>Three ways into the collection.</h2>
        </div>
        <div className="collection-pathway-grid">
          {collection.pathways.map((pathway) => (
            <article className="pathway-card" key={pathway.title}>
              <p className="eyebrow">{pathway.theme}</p>
              <h3>{pathway.title}</h3>
              <p>{pathway.copy}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section featured-works-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">Featured works</p>
          <h2>Records of the oasis moment.</h2>
        </div>
        <FeaturedWorksGrid collection={collection} works={collection.works} />
      </section>

      <NextJourneys journeys={collection.nextJourneys} />

      <section className="section collection-cta-section">
        <div>
          <p className="eyebrow">Continue</p>
          <h2>{collection.ctaTitle}</h2>
          <p className="lead">{collection.ctaCopy}</p>
          <div className="button-row">
            <Link className="button" href={collection.primaryCta.href}>
              {collection.primaryCta.label}
            </Link>
            {collection.secondaryCta ? (
              <Link className="button secondary-button" href={collection.secondaryCta.href}>
                {collection.secondaryCta.label}
              </Link>
            ) : null}
          </div>
        </div>
      </section>

      <section className="section attribution-section">
        <EarthriseAttributionBlock />
      </section>
    </article>
  );
}
