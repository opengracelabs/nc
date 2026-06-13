import type { Metadata } from "next";
import Link from "next/link";
import { signatureCollections } from "@/lib/collections";

export const metadata: Metadata = {
  title: "Institution",
  description: "Nature & Culture mission, collections, discovery, education, conservation, and commerce."
};

const institutionalPillars = [
  {
    title: "Collections",
    eyebrow: "Public catalog",
    copy:
      "Source-led collections organize places, works, stories, and products into coherent visitor journeys.",
    href: "/collections"
  },
  {
    title: "Discovery",
    eyebrow: "Journey system",
    copy:
      "Discovery paths connect related places, nearby contexts, recommendations, and collection graphs.",
    href: "/discover"
  },
  {
    title: "Education",
    eyebrow: "Learning use",
    copy:
      "Each collection is structured for close looking, classroom reference, and independent study.",
    href: "/signature"
  },
  {
    title: "Conservation",
    eyebrow: "Stewardship frame",
    copy:
      "Natural and cultural heritage are treated together, with attention to provenance, ecology, and public memory.",
    href: "/collections/south-georgia"
  },
  {
    title: "Commerce",
    eyebrow: "Source-backed editions",
    copy:
      "Commerce supports the collection system through clearly attributed, rights-reviewed editions.",
    href: "/products"
  }
];

export default function InstitutionHubPage() {
  return (
    <article className="institution-page">
      <section className="institution-hero">
        <div>
          <p className="eyebrow">Institution</p>
          <h1>Nature & Culture is a public collection institution.</h1>
          <p className="lead">
            We build source-traceable collections that connect cultural heritage, natural history,
            discovery journeys, educational use, conservation context, and responsible commerce.
          </p>
          <div className="button-row">
            <Link className="button" href="/signature">Explore signature collections</Link>
            <Link className="button secondary-button" href="/collections">View collection catalog</Link>
          </div>
        </div>
      </section>

      <section className="section institution-mission-section">
        <p className="eyebrow">Mission</p>
        <h2>Make public-domain heritage legible, beautiful, and useful.</h2>
        <div className="two-column-copy editorial-copy">
          <p>
            Nature & Culture treats every collection as an institutional record: where it comes
            from, why it matters, how it connects to adjacent places, and what a visitor can do next.
          </p>
          <p>
            The work is not only publication. It is stewardship through context: source visibility,
            rights discipline, collection design, educational structure, and commerce that points
            back to the public record.
          </p>
        </div>
      </section>

      <section className="section institution-collections-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">Collections</p>
          <h2>Five signature collections anchor the institution.</h2>
        </div>
        <div className="institution-collection-strip">
          {signatureCollections.map((collection) => (
            <Link href={`/collections/${collection.slug}`} key={collection.slug}>
              <img src={collection.imageSrc} alt={collection.imageAlt} />
              <span>{collection.shortTitle}</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="section institution-pillars-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">Institutional work</p>
          <h2>Discovery, education, conservation, and commerce share one collection spine.</h2>
        </div>
        <div className="institution-pillar-grid">
          {institutionalPillars.map((pillar) => (
            <article key={pillar.title}>
              <p className="eyebrow">{pillar.eyebrow}</p>
              <h3>{pillar.title}</h3>
              <p>{pillar.copy}</p>
              <Link href={pillar.href}>Open {pillar.title}</Link>
            </article>
          ))}
        </div>
      </section>

      <section className="section institution-standards-section">
        <p className="eyebrow">Institutional standards</p>
        <h2>What makes this an institution.</h2>
        <div className="institution-standards-grid">
          <div>
            <strong>Source traceability</strong>
            <span>Every public experience points back to origin, rights, and context.</span>
          </div>
          <div>
            <strong>Collection continuity</strong>
            <span>Places become collections, collections become journeys, journeys become editions.</span>
          </div>
          <div>
            <strong>Visitor trust</strong>
            <span>Commercial paths are visible, restrained, and secondary to the public record.</span>
          </div>
        </div>
      </section>
    </article>
  );
}
