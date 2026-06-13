import type { Metadata } from "next";
import {
  placeFactoryDashboardRows,
  placeFactoryDashboardSummary
} from "@/lib/place-factory-dashboard";

export const metadata: Metadata = {
  title: "Place Factory Dashboard v2",
  description: "Scale-ready place factory readiness dashboard."
};

const readinessClass = {
  Ready: "ready",
  Review: "review",
  Hold: "hold"
} as const;

export default function PlaceFactoryDashboardPage() {
  return (
    <section className="page factory-page">
      <p className="eyebrow">Place Factory Dashboard v2</p>
      <h1>Scale-ready place infrastructure</h1>
      <p className="lead">
        Batch candidates are grouped by authority family, collection family, discovery family,
        and readiness state before any canonical identity or product path is created.
      </p>

      <div className="factory-metrics" aria-label="Place factory scale summary">
        <div>
          <strong>{placeFactoryDashboardSummary.scaleTarget}</strong>
          <span>prepared scale target</span>
        </div>
        <div>
          <strong>{placeFactoryDashboardSummary.supportedFamilies.length}</strong>
          <span>designation systems</span>
        </div>
        <div>
          <strong>{placeFactoryDashboardSummary.rows}</strong>
          <span>dashboard sample rows</span>
        </div>
      </div>

      <div className="factory-family-strip" aria-label="Supported designation systems">
        {placeFactoryDashboardSummary.supportedFamilies.map((family) => (
          <span key={family}>{family}</span>
        ))}
      </div>

      <div className="factory-table-wrap">
        <table className="factory-table">
          <thead>
            <tr>
              <th>Place</th>
              <th>Authority</th>
              <th>Collection Family</th>
              <th>Discovery Family</th>
              <th>Commerce Readiness</th>
            </tr>
          </thead>
          <tbody>
            {placeFactoryDashboardRows.map((row) => (
              <tr key={row.place}>
                <td>
                  <strong>{row.place}</strong>
                  <span>{row.designationFamily}</span>
                </td>
                <td>{row.authority}</td>
                <td>{row.collectionFamily}</td>
                <td>
                  {row.discoveryFamily}
                  <span>{row.graphReadiness} graph</span>
                </td>
                <td>
                  <span className={`readiness ${readinessClass[row.commerceReadiness]}`}>
                    {row.commerceReadiness}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
