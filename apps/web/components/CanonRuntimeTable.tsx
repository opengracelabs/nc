import Link from "next/link";
import { getCanonRecordSeries } from "@/lib/canon";
import type { MasterpieceRecord } from "@/lib/masterpieces";

export function CanonRuntimeTable({ records }: { records: MasterpieceRecord[] }) {
  return (
    <div className="masterpiece-table-wrap">
      <table className="masterpiece-table canon-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Work</th>
            <th>Institution</th>
            <th>Collection</th>
            <th>Series</th>
            <th>Rights</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {records.map((record, index) => (
            <tr key={record.slug}>
              <td>{index + 1}</td>
              <td>
                <Link href={`/masterpieces/${record.slug}`}>{record.title}</Link>
                <span>{record.subtitle}</span>
              </td>
              <td>{record.sourceSystem}</td>
              <td>{record.primaryCollection}</td>
              <td>{getCanonRecordSeries(record).map((series) => series.title).join(", ") || "Unassigned"}</td>
              <td>{record.rightsStatus}</td>
              <td><strong>{record.masterpieceScore}</strong></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
