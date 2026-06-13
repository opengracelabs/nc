import type { Metadata } from "next";
import Link from "next/link";
import { trustCurators } from "@/lib/trust";

export const metadata: Metadata = {
  title: "Curators",
  description: "Curator bylines and public profiles for Nature & Culture collections."
};

export default function CuratorsPage() {
  return (
    <section className="page trust-directory-page">
      <p className="eyebrow">Curators</p>
      <h1>Named curator support.</h1>
      <p className="lead">
        Collection pages show named bylines so visitors can see the person responsible for
        collection narrative, source posture, educational framing, and certificate signatory records.
      </p>

      <div className="trust-directory-grid">
        {trustCurators.map((curator) => (
          <Link className="trust-directory-card" href={`/curators/${curator.slug}`} key={curator.slug}>
            <p className="eyebrow">{curator.title}</p>
            <h2>{curator.name}</h2>
            <p>{curator.summary}</p>
            <span>{curator.isFoundingCurator ? "Founding Curator page" : `${curator.collections.length} collection bylines`}</span>
          </Link>
        ))}
      </div>
    </section>
  );
}
