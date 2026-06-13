import type { Metadata } from "next";
import {
  activationDashboardRows,
  activationDashboardSummary,
  activationReadinessCounts,
  type ActivationReadiness
} from "@/lib/place-activation-dashboard";

export const metadata: Metadata = {
  title: "Activation Dashboard",
  description: "Top place activation readiness across authority, collection, product, graph, and publishing."
};

const readinessClass: Record<ActivationReadiness, string> = {
  Ready: "ready",
  Review: "review",
  Hold: "hold"
};

const readinessGroups = [
  ["Authority readiness", activationReadinessCounts.authority],
  ["Collection readiness", activationReadinessCounts.collection],
  ["Product readiness", activationReadinessCounts.product],
  ["Graph readiness", activationReadinessCounts.graph],
  ["Publishing readiness", activationReadinessCounts.publishing]
] as const;

function labelFromKey(value: string) {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function readinessBadge(value: ActivationReadiness) {
  return <span className={`readiness ${readinessClass[value]}`}>{value}</span>;
}

export default function ActivationDashboardPage() {
  return (
    <section className="page activation-page">
      <p className="eyebrow">Activation Dashboard</p>
      <h1>Top 25 places</h1>
      <p className="lead">
        Candidate places are ranked for activation while authority remains source-observed.
        Publishing readiness stays in review or hold until authority, collection, product,
        and graph readiness align.
      </p>

      <div className="activation-metrics" aria-label="Activation summary">
        <div>
          <strong>{activationDashboardSummary.topPlaceCount}</strong>
          <span>top places</span>
        </div>
        <div>
          <strong>{activationDashboardSummary.totalCandidates}</strong>
          <span>candidate pool</span>
        </div>
        <div>
          <strong>{activationReadinessCounts.publishing.Review ?? 0}</strong>
          <span>publishing review</span>
        </div>
        <div>
          <strong>{activationReadinessCounts.publishing.Hold ?? 0}</strong>
          <span>publishing hold</span>
        </div>
      </div>

      <div className="activation-readiness-grid">
        {readinessGroups.map(([title, counts]) => (
          <section className="activation-panel" key={title}>
            <p className="eyebrow">{title}</p>
            <div className="activation-counts">
              {(["Ready", "Review", "Hold"] as ActivationReadiness[]).map((state) => (
                <div key={state}>
                  {readinessBadge(state)}
                  <strong>{counts[state] ?? 0}</strong>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>

      <div className="activation-table-wrap">
        <table className="activation-table">
          <thead>
            <tr>
              <th>Place</th>
              <th>Authority</th>
              <th>Collection</th>
              <th>Product</th>
              <th>Graph</th>
              <th>Publishing</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {activationDashboardRows.map((row) => (
              <tr key={row.placeSlug}>
                <td>
                  <strong>{row.place}</strong>
                  <span>{row.country} · {row.region} · {row.designationFamily}</span>
                  <span>{labelFromKey(row.collectionFamily)}</span>
                </td>
                <td>{readinessBadge(row.authorityReadiness)}</td>
                <td>{readinessBadge(row.collectionReadiness)}</td>
                <td>{readinessBadge(row.productReadiness)}</td>
                <td>{readinessBadge(row.graphReadiness)}</td>
                <td>{readinessBadge(row.publishingReadiness)}</td>
                <td><strong>{row.activationScore}</strong></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
