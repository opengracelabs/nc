import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { collections } from "@/lib/collections";
import {
  certificateRecord,
  editionRegistry,
  foundingCurator,
  getTrustInstitution,
  publicProvenanceChain,
  trustInstitutions
} from "@/lib/trust";

type PageProps = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return trustInstitutions.map((institution) => ({ slug: institution.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const institution = getTrustInstitution(slug);
  return {
    title: institution ? institution.name : "Institution",
    description: institution?.summary ?? "Institution profile"
  };
}

export default async function InstitutionProfilePage({ params }: PageProps) {
  const { slug } = await params;
  const institution = getTrustInstitution(slug);
  if (!institution) {
    notFound();
  }
  const ownedCollections = collections.filter((collection) =>
    institution.collections.includes(collection.slug)
  );

  return (
    <section className="page trust-profile-page">
      <p className="eyebrow">Institution profile</p>
      <h1>{institution.name}</h1>
      <p className="lead">{institution.profile}</p>

      <div className="trust-profile-facts">
        <div><span>Type</span><strong>{institution.type}</strong></div>
        <div><span>Role</span><strong>{institution.role}</strong></div>
        <div><span>Source display</span><strong>{institution.sourceDisplay}</strong></div>
      </div>

      <section className="trust-ownership-section">
        <p className="eyebrow">Collection ownership</p>
        <h2>Collections connected to this institution.</h2>
        <div className="trust-ownership-list">
          {ownedCollections.map((collection) => (
            <Link href={`/collections/${collection.slug}`} key={collection.slug}>
              <strong>{collection.title}</strong>
              <span>{collection.authority}</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="trust-ownership-section">
        <p className="eyebrow">Founding Curator</p>
        <h2>Curator reference resolves to the public profile.</h2>
        <div className="trust-ownership-list">
          <Link href={`/curators/${foundingCurator.slug}`}>
            <strong>{foundingCurator.name}</strong>
            <span>{foundingCurator.title}</span>
          </Link>
        </div>
      </section>

      <section className="verify-provenance-section">
        <p className="eyebrow">Public provenance chain</p>
        <h2>How trust is made visible.</h2>
        <div className="provenance-chain">
          {publicProvenanceChain.map((item) => (
            <article key={item.step}>
              <span>{item.step}</span>
              <h3>{item.title}</h3>
              <p>{item.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="verify-edition-section">
        <p className="eyebrow">Public edition verification</p>
        <h2>Edition records connected to institutional source display.</h2>
        <div className="verify-edition-grid">
          {editionRegistry.map((edition) => (
            <article key={edition.registryId}>
              <p className="eyebrow">{edition.registryId}</p>
              <h3>{edition.title}</h3>
              <p>{edition.certificateId}</p>
              <Link href={`/verify/${certificateRecord.certificateId}`}>Verify edition</Link>
            </article>
          ))}
        </div>
      </section>

      <section className="trust-panel education-panel">
        <p className="eyebrow">Educational Use Panel</p>
        <h2>Use this profile to teach institutional roles.</h2>
        <p>
          This profile separates collection ownership, source institution display, certificate
          verification, and public-domain rights context so visitors can audit the trust chain.
        </p>
      </section>
    </section>
  );
}
