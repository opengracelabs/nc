import type { Metadata } from "next";
import { CanonRuntimeTable } from "@/components/CanonRuntimeTable";
import { getCanonRecordsForSeries, getCanonSeries } from "@/lib/canon";

export const metadata: Metadata = {
  title: "Canon Extinction",
  description: "Extinction Archive Canon Runtime view."
};

export default function CanonExtinctionPage() {
  const series = getCanonSeries("extinction")!;
  const records = getCanonRecordsForSeries(series);

  return (
    <section className="page masterpieces-page canon-page">
      <p className="eyebrow">Canon Runtime</p>
      <h1>{series.title}</h1>
      <p className="lead">{series.description}</p>
      <div className="masterpiece-metrics" aria-label="Extinction Canon Runtime summary">
        <div><strong>{records.length}</strong><span>series records</span></div>
        <div><strong>{series.subtitle}</strong><span>series posture</span></div>
      </div>
      <CanonRuntimeTable records={records} />
    </section>
  );
}
