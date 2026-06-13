import type { Metadata } from "next";
import Link from "next/link";
import {
  certificateRecord,
  educationalUsePanel,
  sourceInstitutionPanel
} from "@/lib/trust";

export const metadata: Metadata = {
  title: "Certificate of Authenticity",
  description: "Certificate, curator, source institution, and educational use panels for Earthrise."
};

export default function CertificatePage() {
  return (
    <section className="page trust-page certificate-page">
      <p className="eyebrow">Certificate of Authenticity</p>
      <h1>{certificateRecord.workTitle}</h1>
      <p className="lead">
        A source-traceable certificate connecting the edition to its public-domain source record,
        attribution text, rights basis, and institutional context.
      </p>

      <section className="certificate-sheet" aria-label="Certificate of Authenticity">
        <div className="certificate-mark">N&C</div>
        <div>
          <p className="eyebrow">Certificate ID</p>
          <h2>{certificateRecord.certificateId}</h2>
          <p>{certificateRecord.collectionTitle}</p>
        </div>
        <dl className="certificate-facts">
          <div><dt>Certificate signatory</dt><dd>{certificateRecord.signatoryName}</dd></div>
          <div><dt>Signatory role</dt><dd>{certificateRecord.signatoryTitle}</dd></div>
          <div><dt>Source institution</dt><dd>{certificateRecord.sourceInstitution}</dd></div>
          <div><dt>Source identifier</dt><dd>{certificateRecord.sourceIdentifier}</dd></div>
          <div><dt>Creator</dt><dd>{certificateRecord.creator}</dd></div>
          <div><dt>Mission</dt><dd>{certificateRecord.mission}</dd></div>
          <div><dt>Date</dt><dd>{certificateRecord.date}</dd></div>
          <div><dt>Status</dt><dd>{certificateRecord.verificationStatus}</dd></div>
        </dl>
      </section>

      <div className="trust-panel-grid">
        <article className="trust-panel curator-panel">
          <p className="eyebrow">Curator Panel</p>
          <h2>{certificateRecord.signatoryName}</h2>
          <p>{certificateRecord.curatorStatement}</p>
          <p className="trust-small">Signed by {certificateRecord.signatoryName}, {certificateRecord.signatoryTitle}</p>
          <div className="button-row compact-button-row">
            <Link href={`/curators/${certificateRecord.signatorySlug}`}>Founding Curator page</Link>
            <Link href="/collections/earthrise">Open collection</Link>
          </div>
        </article>

        <article className="trust-panel source-panel">
          <p className="eyebrow">Source Institution Panel</p>
          <h2>{sourceInstitutionPanel.institution}</h2>
          <p>{sourceInstitutionPanel.copy}</p>
          <p className="trust-small">{certificateRecord.attribution}</p>
          <p className="trust-small">{certificateRecord.nonendorsement}</p>
        </article>

        <article className="trust-panel education-panel">
          <p className="eyebrow">{educationalUsePanel.title}</p>
          <h2>For teaching and source literacy</h2>
          <p>{educationalUsePanel.copy}</p>
          <div className="trust-chip-row">
            {educationalUsePanel.uses.map((use) => <span key={use}>{use}</span>)}
          </div>
        </article>
      </div>

      <section className="trust-rights-panel">
        <p className="eyebrow">Rights basis</p>
        <h2>{certificateRecord.rights}</h2>
        <p>
          This certificate records source and rights context. It is not an endorsement by the source
          institution and does not create private ownership over the underlying public-domain image.
        </p>
        <Link className="button" href="/registry">View Edition Registry</Link>
      </section>
    </section>
  );
}
