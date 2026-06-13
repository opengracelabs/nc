import { certificateRecord, editionRegistry, publicProvenanceChain } from "@/lib/trust";

export type StandardSlug = "pdps" | "coas" | "ers";

export type StandardField = {
  name: string;
  type: string;
  required: boolean;
  description: string;
};

export type StandardExample = {
  title: string;
  code: Record<string, unknown>;
};

export type NatureCultureStandard = {
  slug: StandardSlug;
  code: "NC-PDPS" | "NC-COAS" | "NC-ERS";
  version: "v1";
  title: string;
  shortTitle: string;
  purpose: string;
  publicRoute: string;
  schemaUrl: string;
  documentation: string[];
  schema: StandardField[];
  example: StandardExample;
};

const registryIds = editionRegistry.map((edition) => edition.registryId);

export const standards: NatureCultureStandard[] = [
  {
    slug: "pdps",
    code: "NC-PDPS",
    version: "v1",
    title: "NC-PDPS v1",
    shortTitle: "Public Domain Provenance Standard",
    purpose:
      "Defines the minimum public record required before Nature & Culture presents a public-domain source as collection, education, or product material.",
    publicRoute: "/standards/pdps",
    schemaUrl: "/standards/nc-pdps-v1.schema.json",
    documentation: [
      "Every public-domain work must retain a visible source institution, source identifier, rights basis, attribution text, and nonendorsement posture when applicable.",
      "PDPS records distinguish source custody from Nature & Culture publication. The source institution is credited without implying verification, partnership, sponsorship, or product endorsement.",
      "The provenance chain must be readable by a visitor without requiring internal tools, staff notes, or private authority decisions."
    ],
    schema: [
      { name: "standard", type: "string", required: true, description: "Fixed value NC-PDPS." },
      { name: "version", type: "string", required: true, description: "Published schema version, currently v1." },
      { name: "source_institution", type: "string", required: true, description: "Institution, archive, agency, or source context displayed to the public." },
      { name: "source_identifier", type: "string", required: true, description: "Stable public source reference, accession number, mission frame, URL slug, or equivalent identifier." },
      { name: "rights_basis", type: "string", required: true, description: "Plain-language basis for public-domain or permitted source use." },
      { name: "attribution_text", type: "string", required: true, description: "Exact attribution text presented near the work or edition." },
      { name: "nonendorsement_notice", type: "string", required: false, description: "Notice separating source attribution from endorsement when the source institution requires or benefits from it." },
      { name: "provenance_chain", type: "array<object>", required: true, description: "Public steps from source record through collection, certificate, and edition registry." }
    ],
    example: {
      title: "Earthrise public-domain provenance record",
      code: {
        standard: "NC-PDPS",
        version: "v1",
        source_institution: certificateRecord.sourceInstitution,
        source_identifier: certificateRecord.sourceIdentifier,
        rights_basis: certificateRecord.rights,
        attribution_text: certificateRecord.attribution,
        nonendorsement_notice: certificateRecord.nonendorsement,
        provenance_chain: publicProvenanceChain.map((step) => ({
          step: step.step,
          title: step.title,
          detail: step.detail
        }))
      }
    }
  },
  {
    slug: "coas",
    code: "NC-COAS",
    version: "v1",
    title: "NC-COAS v1",
    shortTitle: "Certificate of Authenticity Standard",
    purpose:
      "Defines the public certificate record that connects a Nature & Culture work to source provenance, curatorial context, and registered editions.",
    publicRoute: "/standards/coas",
    schemaUrl: "/standards/nc-coas-v1.schema.json",
    documentation: [
      "A certificate is a public verification surface for Nature & Culture publication records. It does not transfer ownership over an underlying public-domain source.",
      "COAS records must expose the work title, collection title, source identifier, rights basis, curator statement, source institution display, and linked registry records.",
      "The certificate page must be understandable on its own and must provide a route into the public edition registry."
    ],
    schema: [
      { name: "standard", type: "string", required: true, description: "Fixed value NC-COAS." },
      { name: "version", type: "string", required: true, description: "Published schema version, currently v1." },
      { name: "certificate_id", type: "string", required: true, description: "Public certificate identifier used by verification routes." },
      { name: "work_title", type: "string", required: true, description: "Title of the work or source-backed publication item." },
      { name: "collection_title", type: "string", required: true, description: "Nature & Culture collection connected to the certificate." },
      { name: "source_identifier", type: "string", required: true, description: "Source reference inherited from the PDPS record." },
      { name: "verification_status", type: "string", required: true, description: "Public verification state displayed to visitors." },
      { name: "signatory_name", type: "string", required: true, description: "Named curator who signs or governs the certificate record." },
      { name: "signatory_title", type: "string", required: true, description: "Public role of the certificate signatory." },
      { name: "curator_statement", type: "string", required: true, description: "Curatorial explanation of what the certificate verifies and what it does not imply." },
      { name: "edition_registry_ids", type: "array<string>", required: true, description: "Registry IDs linked to this certificate." }
    ],
    example: {
      title: "Earthrise certificate record",
      code: {
        standard: "NC-COAS",
        version: "v1",
        certificate_id: certificateRecord.certificateId,
        work_title: certificateRecord.workTitle,
        collection_title: certificateRecord.collectionTitle,
        source_institution: certificateRecord.sourceInstitution,
        source_identifier: certificateRecord.sourceIdentifier,
        rights_basis: certificateRecord.rights,
        verification_status: certificateRecord.verificationStatus,
        signatory_name: certificateRecord.signatoryName,
        signatory_title: certificateRecord.signatoryTitle,
        curator_statement: certificateRecord.curatorStatement,
        edition_registry_ids: registryIds
      }
    }
  },
  {
    slug: "ers",
    code: "NC-ERS",
    version: "v1",
    title: "NC-ERS v1",
    shortTitle: "Edition Registry Standard",
    purpose:
      "Defines how Nature & Culture lists public edition records, certificate links, formats, and availability states.",
    publicRoute: "/standards/ers",
    schemaUrl: "/standards/nc-ers-v1.schema.json",
    documentation: [
      "The edition registry identifies Nature & Culture editions while preserving the public-domain status of the underlying source material.",
      "ERS records must link every edition to a certificate and source identifier, then expose the format, edition type, and current availability status.",
      "Registry records are public trust surfaces. They should support verification, education, and purchaser due diligence without private staff intervention."
    ],
    schema: [
      { name: "standard", type: "string", required: true, description: "Fixed value NC-ERS." },
      { name: "version", type: "string", required: true, description: "Published schema version, currently v1." },
      { name: "registry_id", type: "string", required: true, description: "Public edition registry identifier." },
      { name: "certificate_id", type: "string", required: true, description: "Certificate that governs the edition record." },
      { name: "edition_title", type: "string", required: true, description: "Public title for the edition." },
      { name: "edition_type", type: "string", required: true, description: "Edition category, such as physical museum edition or digital study edition." },
      { name: "format", type: "string", required: true, description: "Size, file, print, or delivery format displayed to visitors." },
      { name: "status", type: "string", required: true, description: "Public availability or fulfillment state." },
      { name: "source_identifier", type: "string", required: true, description: "Source reference inherited from certificate and provenance records." }
    ],
    example: {
      title: "Earthrise edition registry records",
      code: {
        standard: "NC-ERS",
        version: "v1",
        editions: editionRegistry.map((edition) => ({
          registry_id: edition.registryId,
          certificate_id: edition.certificateId,
          edition_title: edition.title,
          edition_type: edition.editionType,
          format: edition.format,
          status: edition.status,
          source_identifier: edition.sourceIdentifier
        }))
      }
    }
  }
];

export function getStandard(slug: string) {
  return standards.find((standard) => standard.slug === slug);
}
