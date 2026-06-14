import type { Metadata } from "next";
import {
  collection_activation,
  collection_candidates,
  collection_family_registry,
  collection_readiness,
  collectionFactoryDashboardSummary,
  collectionFactoryRuntime,
  type CollectionReadiness
} from "@/lib/collection-factory";

export const metadata: Metadata = {
  title: "Collection Factory v2",
  description: "Reference-driven collection factory runtime for NC-SCALE-001."
};

const readinessClass: Record<CollectionReadiness, string> = {
  Ready: "ready",
  Review: "review",
  Hold: "hold"
};

function readinessBadge(value: CollectionReadiness) {
  return <span className={`readiness ${readinessClass[value]}`}>{value}</span>;
}

export default function CollectionFactoryPage() {
  return (
    <section className="page factory-page collection-factory-page">
      <p className="eyebrow">NC-SCALE-001</p>
      <h1>Collection Factory v2</h1>
      <p className="lead">
        Collection Factory Runtime turns reference-driven source systems into candidate collection
        registries before canonical publication or product activation.
      </p>

      <div className="factory-metrics" aria-label="Collection Factory Runtime">
        <div><strong>{collectionFactoryDashboardSummary.places}</strong><span>places</span></div>
        <div><strong>{collectionFactoryDashboardSummary.institutions}</strong><span>institutions</span></div>
        <div><strong>{collectionFactoryDashboardSummary.assets}</strong><span>assets</span></div>
        <div><strong>{collectionFactoryDashboardSummary.taxa}</strong><span>taxa</span></div>
        <div><strong>{collectionFactoryDashboardSummary.collections}</strong><span>collections</span></div>
        <div><strong>{collectionFactoryDashboardSummary.masterpieces}</strong><span>masterpieces</span></div>
      </div>

      <div className="factory-family-strip" aria-label="Reference sources">
        {collectionFactoryRuntime.referenceSources.map((source) => (
          <span key={source}>{source}</span>
        ))}
      </div>

      <section className="collection-factory-scale" aria-label="Scale targets">
        <article>
          <strong>{collectionFactoryRuntime.scaleTargets.places.toLocaleString()}</strong>
          <span>places</span>
        </article>
        <article>
          <strong>{collectionFactoryRuntime.scaleTargets.collections.toLocaleString()}</strong>
          <span>collections</span>
        </article>
        <article>
          <strong>{collectionFactoryRuntime.scaleTargets.assets.toLocaleString()}</strong>
          <span>assets</span>
        </article>
        <article>
          <strong>{collectionFactoryRuntime.scaleTargets.illustrationOpportunities.toLocaleString()}</strong>
          <span>illustration opportunities</span>
        </article>
      </section>

      <section className="masterpiece-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">collection_family_registry</p>
          <h2>Reference-driven collection families.</h2>
        </div>
        <div className="launch-collection-grid">
          {collection_family_registry.map((family) => (
            <article className="launch-collection-card" key={family.familySlug}>
              <div className="launch-collection-visual" aria-hidden="true">
                <span>{family.scaleTarget.toLocaleString()}</span>
              </div>
              <div className="launch-collection-body">
                <p className="eyebrow">{family.familySlug}</p>
                <h3>{family.label}</h3>
                <p>{family.description}</p>
                <div className="masterpiece-chip-list">
                  {family.referenceSources.map((source) => (
                    <span key={source}>{source}</span>
                  ))}
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="masterpiece-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">collection_candidates</p>
          <h2>Candidate collections.</h2>
        </div>
        <div className="factory-table-wrap">
          <table className="factory-table collection-factory-table">
            <thead>
              <tr>
                <th>Collection</th>
                <th>Place</th>
                <th>Institution</th>
                <th>Assets</th>
                <th>Taxa</th>
                <th>Masterpieces</th>
                <th>Readiness</th>
              </tr>
            </thead>
            <tbody>
              {collection_candidates.map((candidate) => (
                <tr key={candidate.collectionSlug}>
                  <td>
                    <strong>{candidate.title}</strong>
                    <span>{candidate.familyLabel}</span>
                  </td>
                  <td>{candidate.place}</td>
                  <td>{candidate.institution}</td>
                  <td>{candidate.assetCount}</td>
                  <td>{candidate.taxaCount}</td>
                  <td>{candidate.masterpieceCount}</td>
                  <td>{readinessBadge(candidate.readiness)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="activation-readiness-grid" aria-label="collection_readiness">
        {(["Ready", "Review", "Hold"] as CollectionReadiness[]).map((state) => (
          <article className="activation-panel" key={state}>
            <p className="eyebrow">collection_readiness</p>
            <div className="masterpiece-readiness-total">
              {readinessBadge(state)}
              <strong>{collection_readiness[state]}</strong>
            </div>
          </article>
        ))}
      </section>

      <section className="masterpiece-section">
        <div className="section-heading wide-heading">
          <p className="eyebrow">collection_activation</p>
          <h2>Activation registry.</h2>
        </div>
        <div className="factory-table-wrap">
          <table className="factory-table collection-factory-table">
            <thead>
              <tr>
                <th>Collection</th>
                <th>State</th>
                <th>Score</th>
                <th>Path</th>
                <th>Blocking action</th>
              </tr>
            </thead>
            <tbody>
              {collection_activation.map((activation) => (
                <tr key={activation.collectionSlug}>
                  <td>
                    <strong>{activation.title}</strong>
                    <span>{activation.familySlug}</span>
                  </td>
                  <td>{readinessBadge(activation.activationState)}</td>
                  <td>{activation.activationScore}</td>
                  <td>{activation.activationPath}</td>
                  <td>{activation.blockingAction}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </section>
  );
}
