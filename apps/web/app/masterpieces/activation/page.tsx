import type { Metadata } from "next";
import {
  masterpieceActivationReadinessCounts,
  masterpieceActivationRows,
  masterpieceActivationSummary,
  type MasterpieceActivationReadiness
} from "@/lib/masterpiece-activation";

export const metadata: Metadata = {
  title: "Masterpiece Activation Dashboard",
  description: "Top 25 masterpiece activation readiness by institution, collection, rights, and commerce."
};

const readinessClass: Record<MasterpieceActivationReadiness, string> = {
  Ready: "ready",
  Review: "review",
  Hold: "hold"
};

function readinessBadge(value: MasterpieceActivationReadiness) {
  return <span className={`readiness ${readinessClass[value]}`}>{value}</span>;
}

export default function MasterpieceActivationPage() {
  return (
    <section className="page activation-page masterpiece-activation-page">
      <p className="eyebrow">NC-MASTERPIECES-002</p>
      <h1>Masterpiece Dashboard</h1>
      <p className="lead">
        Top 25 activation candidates ranked by cultural significance, public-domain confidence,
        collection value, and commercial deployment path.
      </p>

      <div className="activation-metrics" aria-label="Masterpiece activation summary">
        <div>
          <strong>{masterpieceActivationSummary.top25Count}</strong>
          <span>Top 25</span>
        </div>
        <div>
          <strong>{masterpieceActivationSummary.immediateLaunchCount}</strong>
          <span>ready now</span>
        </div>
        <div>
          <strong>{masterpieceActivationSummary.wave2Count}</strong>
          <span>DD ratification</span>
        </div>
        <div>
          <strong>{masterpieceActivationSummary.wave3BlockedCount}</strong>
          <span>blocked</span>
        </div>
      </div>

      <div className="activation-readiness-grid">
        {(["Ready", "Review", "Hold"] as MasterpieceActivationReadiness[]).map((state) => (
          <section className="activation-panel" key={state}>
            <p className="eyebrow">{state} readiness</p>
            <div className="masterpiece-readiness-total">
              {readinessBadge(state)}
              <strong>{masterpieceActivationReadinessCounts[state]}</strong>
            </div>
          </section>
        ))}
      </div>

      <div className="activation-table-wrap">
        <table className="activation-table masterpiece-activation-table">
          <thead>
            <tr>
              <th>Top 25</th>
              <th>Readiness</th>
              <th>Institution</th>
              <th>Collection</th>
              <th>Rights</th>
              <th>Commerce</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {masterpieceActivationRows.map((row) => (
              <tr key={row.ncId}>
                <td>
                  <strong>{String(row.rank).padStart(2, "0")}. {row.title}</strong>
                  <span>{row.illustrator} · {row.year} · {row.ncId}</span>
                  <span>{row.wave} · {row.blockingAction}</span>
                </td>
                <td>{readinessBadge(row.readiness)}</td>
                <td>{row.institution}</td>
                <td>{row.collection}</td>
                <td>{row.rights}</td>
                <td>
                  <strong>{row.revenueTier}</strong>
                  <span>{row.commerce}</span>
                </td>
                <td><strong>{row.score}</strong></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
