import type { Metadata } from "next";
import Link from "next/link";
import { standards } from "@/lib/standards";

export const metadata: Metadata = {
  title: "Public Standards",
  description: "Nature & Culture public documentation, examples, and schemas for provenance, certificates, and edition registries."
};

export default function StandardsPage() {
  return (
    <section className="page standards-page">
      <div className="standards-hero">
        <p className="eyebrow">Institutional standards</p>
        <h1>Public standards for source-traceable collections.</h1>
        <p className="lead">
          NC-PDPS v1, NC-COAS v1, and NC-ERS v1 make provenance, certificates, and
          edition records visible to visitors before they encounter commerce.
        </p>
      </div>

      <div className="standards-grid" aria-label="Public standards">
        {standards.map((standard) => (
          <Link className="standard-card" href={standard.publicRoute} key={standard.slug}>
            <span>{standard.title}</span>
            <h2>{standard.shortTitle}</h2>
            <p>{standard.purpose}</p>
            <strong>Read schema and example</strong>
          </Link>
        ))}
      </div>

      <section className="standards-principles" aria-label="Standards principles">
        <article>
          <p className="eyebrow">Public documentation</p>
          <h2>Readable by visitors</h2>
          <p>Each standard explains what Nature & Culture displays publicly and what the record does not imply.</p>
        </article>
        <article>
          <p className="eyebrow">Public examples</p>
          <h2>Grounded in Earthrise</h2>
          <p>Examples use the live certificate, provenance chain, and edition registry already visible on the site.</p>
        </article>
        <article>
          <p className="eyebrow">Public schemas</p>
          <h2>Stable field contracts</h2>
          <p>Field names, required status, and public meanings are documented before new collection families scale.</p>
        </article>
      </section>
    </section>
  );
}
