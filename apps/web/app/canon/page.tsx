import type { Metadata } from "next";
import Link from "next/link";
import { canonRuntime, canonSeries } from "@/lib/canon";

export const metadata: Metadata = {
  title: "Canon",
  description: "Canon Runtime derived from the Masterpiece Registry."
};

export default function CanonPage() {
  return (
    <section className="page masterpieces-page canon-page">
      <p className="eyebrow">Masterpiece Registry</p>
      <h1>Canon Runtime</h1>
      <p className="lead">
        The Canon Runtime presents registry works as editorial series for activation, review,
        and public collection planning.
      </p>

      <div className="masterpiece-metrics" aria-label="Canon Runtime summary">
        <div><strong>{canonRuntime.totalCanonRecords}</strong><span>canon records</span></div>
        <div><strong>{canonRuntime.top100Count}</strong><span>top-100 records</span></div>
        <div><strong>{canonRuntime.seriesCount}</strong><span>canon series</span></div>
        <div><strong>{canonRuntime.sourceRuntimeVersion}</strong><span>source registry</span></div>
      </div>

      <section className="masterpiece-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">{canonRuntime.runtimeVersion}</p>
          <h2>Canon views.</h2>
        </div>
        <div className="grid">
          <article className="card">
            <h3>Top 100</h3>
            <p>Ranked registry works as the public canon index.</p>
            <Link href="/canon/top-100">View top 100</Link>
          </article>
          {canonSeries.map((series) => (
            <article className="card" key={series.slug}>
              <h3>{series.title}</h3>
              <p>{series.description}</p>
              <Link href={`/canon/${series.slug}`}>View {series.slug}</Link>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
