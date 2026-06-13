import type { Metadata } from "next";
import Link from "next/link";
import { institutionFactoryRecords, institutionFactorySummary } from "@/lib/institution-factory";

export const metadata: Metadata = {
  title: "Institution Factory",
  description: "Candidate-only institution registry, readiness, asset counts, and collection counts."
};

export default function InstitutionFactoryPage() {
  return (
    <section className="page institution-factory-page">
      <div className="institution-factory-hero">
        <p className="eyebrow">Institution Factory Runtime</p>
        <h1>Institution registry from candidate assets.</h1>
        <p className="lead">
          The factory groups Asset Factory candidates by source institution, then exposes readiness,
          asset counts, and collection counts without creating canonical institution records or
          canonical publication records.
        </p>
        <div className="button-row">
          <Link className="button" href="/institutions">Institution directory</Link>
          <Link className="button secondary-button" href="/curators/founding-curator">Founding Curator</Link>
        </div>
      </div>

      <div className="institution-factory-metrics" aria-label="Institution Factory summary">
        <div><strong>{institutionFactorySummary.institutionCount}</strong><span>institutions</span></div>
        <div><strong>{institutionFactorySummary.assetCount}</strong><span>asset candidates</span></div>
        <div><strong>{institutionFactorySummary.collectionMappingCount}</strong><span>collection mappings</span></div>
        <div><strong>0</strong><span>canonical publications</span></div>
      </div>

      <section className="institution-factory-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">institution_registry</p>
          <h2>Candidate institutions observed in asset sources.</h2>
        </div>
        <div className="institution-factory-table-wrap">
          <table className="institution-factory-table">
            <thead>
              <tr>
                <th>Institution</th>
                <th>Source systems</th>
                <th>Readiness</th>
                <th>Assets</th>
                <th>Collections</th>
                <th>Rights</th>
              </tr>
            </thead>
            <tbody>
              {institutionFactoryRecords.map((record) => (
                <tr key={record.institutionSlug}>
                  <td>
                    <strong>{record.displayName}</strong>
                    <span>{record.institutionSlug}</span>
                  </td>
                  <td>{record.sourceSystems.join(", ")}</td>
                  <td>
                    <span className={`readiness ${record.readiness}`}>{record.readiness}</span>
                    <small>{record.readinessScore}</small>
                  </td>
                  <td>{record.assetCount}</td>
                  <td>{record.collectionCount}</td>
                  <td><code>{record.rightsStatus}</code></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="institution-factory-grid">
        <article className="institution-factory-panel">
          <p className="eyebrow">institution_readiness</p>
          <h2>Readiness posture</h2>
          <div className="institution-factory-list">
            {institutionFactoryRecords.map((record) => (
              <div key={record.institutionSlug}>
                <span>{record.displayName}</span>
                <strong>{record.readiness}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="institution-factory-panel">
          <p className="eyebrow">institution_asset_counts</p>
          <h2>Candidate asset coverage</h2>
          <div className="institution-factory-list">
            {institutionFactoryRecords.map((record) => (
              <div key={record.institutionSlug}>
                <span>{record.displayName}</span>
                <strong>{record.assetCount}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="institution-factory-panel">
          <p className="eyebrow">institution_collection_counts</p>
          <h2>Collection mapping coverage</h2>
          <div className="institution-factory-list">
            {institutionFactoryRecords.map((record) => (
              <div key={record.institutionSlug}>
                <span>{record.displayName}</span>
                <strong>{record.collections.join(", ")}</strong>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="trust-rights-panel">
        <p className="eyebrow">Candidate-only contract</p>
        <h2>No canonical publication.</h2>
        <p>
          This dashboard is a factory view over candidate asset sources. It does not create canonical
          institution identities, product pages, certificates, edition registry records, or canonical
          publication records.
        </p>
      </section>
    </section>
  );
}
