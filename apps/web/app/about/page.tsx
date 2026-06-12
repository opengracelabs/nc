import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About",
  description: "Nature & Culture source, rights, and attribution commitments."
};

export default function AboutPage() {
  return (
    <section className="page">
      <p className="eyebrow">About</p>
      <h1>Public-domain commerce with visible provenance.</h1>
      <p className="lead">
        Nature & Culture sells and publishes works only when source, rights, and attribution checks
        can be shown clearly to the public.
      </p>
      <div className="grid">
        <article className="card">
          <h2>Public domain first</h2>
          <p>Products are limited to verified public-domain or CC0 works.</p>
        </article>
        <article className="card">
          <h2>Rights verification</h2>
          <p>Every asset is reviewed against governed source and rights records before launch.</p>
        </article>
        <article className="card">
          <h2>Attribution visible</h2>
          <p>Source credits and nonendorsement notices are rendered on the relevant page.</p>
        </article>
      </div>
    </section>
  );
}
