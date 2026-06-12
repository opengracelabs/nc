import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About",
  description: "Nature & Culture source, rights, and attribution commitments."
};

export default function AboutPage() {
  return (
    <section className="page">
      <p className="eyebrow">About</p>
      <h1>Public-domain works, source-traceable editions.</h1>
      <p className="lead">
        Nature & Culture publishes stories and editions from public-domain works with clear source, rights, and attribution records.
      </p>
      <div className="grid">
        <article className="card">
          <h2>Public domain first</h2>
          <p>Products are limited to verified public-domain or CC0 works.</p>
        </article>
        <article className="card">
          <h2>Rights verification</h2>
          <p>Every asset is reviewed against source and rights records before launch.</p>
        </article>
        <article className="card">
          <h2>Attribution visible</h2>
          <p>Source credits and nonendorsement notices are rendered on the relevant page.</p>
        </article>
      </div>
    </section>
  );
}
