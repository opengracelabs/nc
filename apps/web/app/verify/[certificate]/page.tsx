import type { Metadata } from "next";
import Link from "next/link";
import {
  certificateRecord,
  getCertificateRecord,
  getEditionsForCertificate,
  normalizeCertificateSlug,
  publicProvenanceChain
} from "@/lib/trust";

type PageProps = {
  params: Promise<{ certificate: string }>;
};

export function generateStaticParams() {
  return [{ certificate: certificateRecord.certificateId }];
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { certificate } = await params;
  const normalized = normalizeCertificateSlug(certificate);
  return {
    title: `Verify ${normalized}`,
    description: "Public certificate, provenance chain, and edition verification."
  };
}

export default async function VerifyCertificatePage({ params }: PageProps) {
  const { certificate } = await params;
  const normalized = normalizeCertificateSlug(certificate);
  const record = getCertificateRecord(normalized);
  const editions = getEditionsForCertificate(normalized);
  const verified = Boolean(record);

  return (
    <section className="page verify-page">
      <p className="eyebrow">Public edition verification</p>
      <h1>{verified ? "Certificate verified." : "Certificate not found."}</h1>
      <p className="lead">
        {verified
          ? "This public page verifies the certificate, source record, provenance chain, and registered editions connected to this Nature & Culture publication."
          : "No public Nature & Culture certificate record matches this identifier."}
      </p>

      <section className={`verify-status-panel ${verified ? "verified" : "unverified"}`}>
        <div>
          <span>Certificate</span>
          <strong>{normalized}</strong>
        </div>
        <div>
          <span>Status</span>
          <strong>{verified ? record?.verificationStatus : "No public record"}</strong>
        </div>
        <div>
          <span>Source</span>
          <strong>{record?.sourceIdentifier ?? "Unavailable"}</strong>
        </div>
      </section>

      {verified && record ? (
        <>
          <section className="verify-provenance-section">
            <p className="eyebrow">Public provenance chain</p>
            <h2>From source record to edition registry.</h2>
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
            <h2>Registered editions using this certificate.</h2>
            <div className="verify-edition-grid">
              {editions.map((edition) => (
                <article key={edition.registryId}>
                  <p className="eyebrow">{edition.registryId}</p>
                  <h3>{edition.title}</h3>
                  <p>{edition.format}</p>
                  <span className="readiness ready">{edition.status}</span>
                </article>
              ))}
            </div>
          </section>

          <section className="trust-panel education-panel">
            <p className="eyebrow">Educational Use Panel</p>
            <h2>Use this page to teach source verification.</h2>
            <p>
              The verification page shows how an edition connects to source institution, rights
              basis, certificate record, and registry entry without implying endorsement by the
              source institution.
            </p>
          </section>
        </>
      ) : null}

      <div className="button-row">
        <Link className="button" href="/certificate">View Certificate</Link>
        <Link className="button secondary-button" href="/registry">View Registry</Link>
      </div>
    </section>
  );
}
