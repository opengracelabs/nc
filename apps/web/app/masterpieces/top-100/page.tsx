import type { Metadata } from "next";
import Link from "next/link";
import { top100Masterpieces } from "@/lib/masterpieces";

export const metadata: Metadata = {
  title: "Top 100 Masterpieces",
  description: "The top 100 ranked entries in the Masterpiece Registry."
};

export default function Top100MasterpiecesPage() {
  return (
    <section className="page masterpieces-page">
      <p className="eyebrow">Top 100</p>
      <h1>Top 100 Masterpieces.</h1>
      <p className="lead">
        Ranked by masterpiece_score across publication readiness, collection fit, source evidence,
        rights posture, and product potential.
      </p>
      <div className="masterpiece-table-wrap">
        <table className="masterpiece-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Work</th>
              <th>Source</th>
              <th>Status</th>
              <th>Collections</th>
              <th>masterpiece_score</th>
            </tr>
          </thead>
          <tbody>
            {top100Masterpieces.map((record, index) => (
              <tr key={record.slug}>
                <td>{index + 1}</td>
                <td><Link href={`/masterpieces/${record.slug}`}>{record.title}</Link></td>
                <td>{record.sourceSystem}</td>
                <td>{record.registryStatus}</td>
                <td>{record.collections.slice(0, 3).join(", ")}</td>
                <td>{record.masterpieceScore}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
