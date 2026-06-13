import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getMasterpiece, masterpieceRegistry } from "@/lib/masterpieces";

type PageProps = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return masterpieceRegistry.map((record) => ({ slug: record.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const record = getMasterpiece(slug);
  return {
    title: record ? record.title : "Masterpiece",
    description: record?.narrative ?? "Masterpiece Registry detail"
  };
}

export default async function MasterpieceDetailPage({ params }: PageProps) {
  const { slug } = await params;
  const record = getMasterpiece(slug);
  if (!record) {
    notFound();
  }

  return (
    <article className="page masterpiece-detail-page">
      <div className="masterpiece-detail-hero">
        <img src={record.imageSrc} alt={record.imageAlt} />
        <div>
          <p className="eyebrow">Masterpiece Registry</p>
          <h1>{record.title}</h1>
          <p className="lead">{record.subtitle}</p>
          <div className="masterpiece-score-block">
            <span>masterpiece_score</span>
            <strong>{record.masterpieceScore}</strong>
          </div>
        </div>
      </div>

      <section className="masterpiece-facts" aria-label="Masterpiece registry facts">
        <div><span>Source</span><strong>{record.sourceSystem}</strong></div>
        <div><span>Status</span><strong>{record.registryStatus}</strong></div>
        <div><span>Readiness</span><strong>{record.readinessState}</strong></div>
        <div><span>Rights</span><strong>{record.rightsStatus}</strong></div>
      </section>

      <section className="masterpiece-section">
        <p className="eyebrow">masterpiece_collections</p>
        <h2>Collection links.</h2>
        <div className="masterpiece-chip-list">
          {record.collections.map((collection) => <span key={collection}>{collection}</span>)}
        </div>
      </section>

      <section className="masterpiece-section">
        <p className="eyebrow">Registry narrative</p>
        <h2>{record.candidateOnly ? "Candidate masterpiece." : "Published masterwork."}</h2>
        <p>{record.narrative}</p>
        <p>
          Source record <code>{record.sourceRecordId}</code>
          {record.taxonName ? <> · Taxon <code>{record.taxonName}</code></> : null}
        </p>
        <div className="button-row">
          <a className="button" href={record.sourceUrl}>View source</a>
          <Link className="button secondary-button" href="/masterpieces/top-100">Back to top 100</Link>
        </div>
      </section>
    </article>
  );
}
