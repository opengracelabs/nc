import type { CSSProperties } from "react";
import type { Metadata } from "next";
import {
  coverageCollectionFamilies,
  coverageCollectionReviewGaps,
  coverageDesignationCounts,
  coverageMapPoints,
  coverageMissingCollectionFamilies,
  coverageRegions,
  coverageSummary
} from "@/lib/place-factory-coverage";

export const metadata: Metadata = {
  title: "Place Factory Coverage Dashboard",
  description: "Candidate source coverage, authority, map, and collection family gaps."
};

const designationClass: Record<string, string> = {
  UNESCO: "heritage",
  Biosphere: "biosphere",
  Geopark: "geopark",
  Ramsar: "ramsar",
  ICH: "ich"
};

function mapPointStyle(latitude: number, longitude: number): CSSProperties {
  return {
    left: `${((longitude + 180) / 360) * 100}%`,
    top: `${((90 - latitude) / 180) * 100}%`
  };
}

function labelFromKey(value: string) {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default function PlaceFactoryCoverageDashboardPage() {
  return (
    <section className="page coverage-page">
      <p className="eyebrow">Place Factory Coverage Dashboard</p>
      <h1>Source ingestion coverage</h1>
      <p className="lead">
        Candidate places from priority source ingestion are mapped, counted, and held at
        source-observed authority until canonical identity review is ready.
      </p>

      <div className="coverage-metrics" aria-label="Coverage summary">
        <div>
          <strong>{coverageSummary.totalCandidates}</strong>
          <span>candidate places</span>
        </div>
        <div>
          <strong>{coverageSummary.mappedCandidates}</strong>
          <span>mapped candidates</span>
        </div>
        <div>
          <strong>{coverageSummary.missingCoordinateCandidates}</strong>
          <span>coordinate gaps</span>
        </div>
        <div>
          <strong>{coverageSummary.sourceObservedOnly}</strong>
          <span>source-observed only</span>
        </div>
      </div>

      <section className="coverage-band" aria-labelledby="coverage-map-title">
        <div className="coverage-section-heading">
          <p className="eyebrow" id="coverage-map-title">World map</p>
          <h2>Candidate distribution</h2>
        </div>
        <div className="coverage-map" role="img" aria-label="World map of candidate places">
          <div className="coverage-map-grid" />
          {coverageMapPoints.map((point) => (
            <span
              className={`coverage-map-point ${designationClass[point.designationFamily] ?? "other"}`}
              key={point.placeSlug}
              style={mapPointStyle(point.latitude, point.longitude)}
              title={`${point.displayName} - ${point.designationFamily}`}
            />
          ))}
        </div>
      </section>

      <div className="coverage-grid">
        <section className="coverage-panel" aria-labelledby="coverage-regions-title">
          <p className="eyebrow" id="coverage-regions-title">Regions</p>
          <h2>Regional coverage</h2>
          <div className="coverage-bars">
            {coverageRegions.map((region) => (
              <div className="coverage-bar-row" key={region.region}>
                <span>{region.region}</span>
                <div>
                  <i style={{ width: `${Math.max(8, region.count)}%` }} />
                </div>
                <strong>{region.count}</strong>
              </div>
            ))}
          </div>
        </section>

        <section className="coverage-panel" aria-labelledby="coverage-designations-title">
          <p className="eyebrow" id="coverage-designations-title">Designation counts</p>
          <h2>Source families</h2>
          <div className="coverage-count-list">
            {coverageDesignationCounts.map((item) => (
              <div key={item.designation}>
                <span>{item.designation}</span>
                <strong>{item.count}</strong>
              </div>
            ))}
          </div>
        </section>

        <section className="coverage-panel" aria-labelledby="coverage-authority-title">
          <p className="eyebrow" id="coverage-authority-title">Authority gaps</p>
          <h2>Review queue</h2>
          <div className="coverage-count-list">
            <div>
              <span>Source-observed only</span>
              <strong>{coverageSummary.sourceObservedOnly}</strong>
            </div>
            <div>
              <span>Unverified</span>
              <strong>{coverageSummary.unverified}</strong>
            </div>
            <div>
              <span>Needs review</span>
              <strong>{coverageSummary.needsReview}</strong>
            </div>
            <div>
              <span>Missing coordinates</span>
              <strong>{coverageSummary.missingCoordinateCandidates}</strong>
            </div>
          </div>
        </section>

        <section className="coverage-panel" aria-labelledby="coverage-collection-title">
          <p className="eyebrow" id="coverage-collection-title">Collection family gaps</p>
          <h2>Readiness gaps</h2>
          <div className="coverage-count-list">
            {coverageCollectionReviewGaps.map((gap) => (
              <div key={gap.family}>
                <span>{labelFromKey(gap.family)}</span>
                <strong>{gap.count}</strong>
              </div>
            ))}
          </div>
          <div className="coverage-gap-strip" aria-label="Missing expected collection families">
            {coverageMissingCollectionFamilies.map((family) => (
              <span key={family}>{labelFromKey(family)}</span>
            ))}
          </div>
        </section>
      </div>

      <section className="coverage-band" aria-labelledby="coverage-families-title">
        <div className="coverage-section-heading">
          <p className="eyebrow" id="coverage-families-title">Collection families</p>
          <h2>Candidate inventory</h2>
        </div>
        <div className="coverage-family-grid">
          {coverageCollectionFamilies.map((family) => (
            <div key={family.family}>
              <span>{labelFromKey(family.family)}</span>
              <strong>{family.count}</strong>
            </div>
          ))}
        </div>
      </section>
    </section>
  );
}
