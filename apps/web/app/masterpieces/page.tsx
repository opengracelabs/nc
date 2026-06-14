import type { Metadata } from "next";
import Link from "next/link";
import { masterpieceRegistry, masterpieceRuntime } from "@/lib/masterpieces";

export const metadata: Metadata = {
  title: "Masterpieces",
  description: "Masterpiece Registry ranked by collection, source, readiness, and product potential."
};

export default function MasterpiecesPage() {
  const lead = masterpieceRegistry[0];

  return (
    <section className="page masterpieces-page">
      <div className="masterpieces-hero">
        <div>
          <p className="eyebrow">Masterpiece Registry</p>
          <h1>Ranked works with collection gravity.</h1>
          <p className="lead">
            The registry scores published works and candidate illustrations by source strength,
            readiness, collection fit, and edition potential.
          </p>
          <div className="button-row">
            <Link className="button" href="/masterpieces/activation">Activation dashboard</Link>
            <Link className="button" href="/masterpieces/top-100">View top 100</Link>
            <Link className="button secondary-button" href={`/masterpieces/${lead.slug}`}>Top masterpiece</Link>
          </div>
        </div>
        <img src={lead.imageSrc} alt={lead.imageAlt} />
      </div>

      <div className="masterpiece-metrics" aria-label="Masterpiece Runtime summary">
        <div><strong>{masterpieceRuntime.totalMasterpieces}</strong><span>registry records</span></div>
        <div><strong>{masterpieceRuntime.top100Count}</strong><span>top-100 entries</span></div>
        <div><strong>{masterpieceRuntime.collectionCount}</strong><span>collection links</span></div>
        <div><strong>{masterpieceRuntime.candidateCount}</strong><span>candidate works</span></div>
      </div>

      <section className="masterpiece-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">masterpiece_registry</p>
          <h2>Current ranked registry.</h2>
        </div>
        <div className="masterpiece-list">
          {masterpieceRegistry.map((record, index) => (
            <Link className="masterpiece-row" href={`/masterpieces/${record.slug}`} key={record.slug}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <strong>{record.title}</strong>
              <em>{record.sourceSystem} · {record.registryStatus}</em>
              <b>{record.masterpieceScore}</b>
            </Link>
          ))}
        </div>
      </section>
    </section>
  );
}
