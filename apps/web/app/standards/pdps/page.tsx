import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { StandardDocument } from "@/components/StandardDocument";
import { getStandard } from "@/lib/standards";

export const metadata: Metadata = {
  title: "NC-PDPS v1",
  description: "Nature & Culture Public Domain Provenance Standard public documentation, examples, and schema."
};

export default function PDPSStandardPage() {
  const standard = getStandard("pdps");

  if (!standard) {
    notFound();
  }

  return <StandardDocument standard={standard} />;
}
