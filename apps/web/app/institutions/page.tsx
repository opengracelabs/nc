import type { Metadata } from "next";
import Link from "next/link";
import { trustInstitutions } from "@/lib/trust";

export const metadata: Metadata = {
  title: "Institutions",
  description: "Institution cards, source displays, and collection ownership for Nature & Culture."
};

export default function InstitutionsPage() {
  return (
    <section className="page trust-directory-page">
      <p className="eyebrow">Institutions</p>
      <h1>Institutional trust network.</h1>
      <p className="lead">
        Source institutions, designation authorities, and publication ownership are shown alongside
        collection responsibilities so visitors can see who holds what role.
      </p>

      <div className="trust-directory-grid">
        {trustInstitutions.map((institution) => (
          <Link className="trust-directory-card" href={`/institutions/${institution.slug}`} key={institution.slug}>
            <p className="eyebrow">{institution.type}</p>
            <h2>{institution.name}</h2>
            <p>{institution.summary}</p>
            <span>{institution.collections.length} collection links</span>
          </Link>
        ))}
      </div>
    </section>
  );
}
