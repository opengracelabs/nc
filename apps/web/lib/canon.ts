import { masterpieceRegistry, masterpieceRuntime, top100Masterpieces, type MasterpieceRecord } from "@/lib/masterpieces";

export type CanonSeriesSlug = "extinction" | "exploration" | "planetary";

export type CanonSeries = {
  slug: CanonSeriesSlug;
  title: string;
  subtitle: string;
  description: string;
  recordSlugs: string[];
};

export const canonSeries: CanonSeries[] = [
  {
    slug: "extinction",
    title: "Extinction Archive",
    subtitle: "Loss, recovery, and evidence",
    description: "Canon works that carry extinction, near-extinction, or conservation recovery value.",
    recordSlugs: ["bison-bison-range-plate"]
  },
  {
    slug: "exploration",
    title: "Exploration",
    subtitle: "Field records and discovery chains",
    description: "Canon works connected to expeditions, discovery places, and source-led natural history.",
    recordSlugs: ["acanthaster-planci-plate", "bison-bison-range-plate"]
  },
  {
    slug: "planetary",
    title: "Planetary",
    subtitle: "Earth seen as a single subject",
    description: "Canon works that frame planetary stewardship, space observation, and global ecological meaning.",
    recordSlugs: ["earthrise", "acanthaster-planci-plate"]
  }
];

export const canonRuntime = {
  runtimeName: "Canon Runtime",
  runtimeVersion: "NC-CANON-001-v1",
  sourceRuntimeVersion: masterpieceRuntime.runtimeVersion,
  totalCanonRecords: masterpieceRegistry.length,
  top100Count: top100Masterpieces.length,
  seriesCount: canonSeries.length
};

export function getCanonSeries(slug: CanonSeriesSlug) {
  return canonSeries.find((series) => series.slug === slug);
}

export function getCanonRecordsForSeries(series: CanonSeries): MasterpieceRecord[] {
  const slugs = new Set(series.recordSlugs);
  return masterpieceRegistry.filter((record) => slugs.has(record.slug));
}

export function getCanonRecordSeries(record: MasterpieceRecord) {
  return canonSeries.filter((series) => series.recordSlugs.includes(record.slug));
}
