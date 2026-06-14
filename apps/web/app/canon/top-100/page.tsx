import type { Metadata } from "next";
import { CanonRuntimeTable } from "@/components/CanonRuntimeTable";
import { canonRuntime } from "@/lib/canon";
import { top100Masterpieces } from "@/lib/masterpieces";

export const metadata: Metadata = {
  title: "Canon Top 100",
  description: "Top 100 Canon Runtime entries derived from the Masterpiece Registry."
};

export default function CanonTop100Page() {
  return (
    <section className="page masterpieces-page canon-page">
      <p className="eyebrow">Canon Runtime</p>
      <h1>Canon Top 100</h1>
      <p className="lead">
        Ranked directly from the Masterpiece Registry, preserving source, rights, collection,
        and score fields.
      </p>
      <div className="masterpiece-metrics" aria-label="Canon Top 100 summary">
        <div><strong>{canonRuntime.top100Count}</strong><span>Top 100</span></div>
        <div><strong>{canonRuntime.totalCanonRecords}</strong><span>registry records</span></div>
        <div><strong>{canonRuntime.seriesCount}</strong><span>series overlays</span></div>
      </div>
      <CanonRuntimeTable records={top100Masterpieces} />
    </section>
  );
}
