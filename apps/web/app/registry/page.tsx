import type { Metadata } from "next";
import Link from "next/link";
import { certificateRecord, editionRegistry } from "@/lib/trust";

export const metadata: Metadata = {
  title: "Edition Registry",
  description: "Public edition registry for Nature & Culture source-backed editions."
};

export default function RegistryPage() {
  return (
    <section className="page trust-page registry-page">
      <p className="eyebrow">Edition Registry</p>
      <h1>Registered source-backed editions.</h1>
      <p className="lead">
        The registry lists public Nature & Culture editions, their certificate connection, source
        identifier, format, and current availability status.
      </p>

      <div className="registry-summary" aria-label="Registry summary">
        <div><strong>{editionRegistry.length}</strong><span>registered editions</span></div>
        <div><strong>1</strong><span>certificate record</span></div>
        <div><strong>{certificateRecord.sourceInstitution}</strong><span>source institution</span></div>
      </div>

      <div className="registry-table-wrap">
        <table className="registry-table">
          <thead>
            <tr>
              <th>Registry ID</th>
              <th>Edition</th>
              <th>Format</th>
              <th>Certificate</th>
              <th>Source</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {editionRegistry.map((edition) => (
              <tr key={edition.registryId}>
                <td><strong>{edition.registryId}</strong></td>
                <td>
                  <strong>{edition.title}</strong>
                  <span>{edition.editionType}</span>
                </td>
                <td>{edition.format}</td>
                <td>{edition.certificateId}</td>
                <td>{edition.sourceIdentifier}</td>
                <td><span className="readiness ready">{edition.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <section className="trust-rights-panel">
        <p className="eyebrow">Registry note</p>
        <h2>Public-domain source, private edition record.</h2>
        <p>
          The registry identifies Nature & Culture editions and their certificate records. The
          underlying Earthrise image remains public domain under the stated rights basis.
        </p>
        <div className="button-row">
          <Link className="button" href="/certificate">View Certificate</Link>
          <Link className="button secondary-button" href="/products/earthrise">View Earthrise editions</Link>
        </div>
      </section>
    </section>
  );
}
