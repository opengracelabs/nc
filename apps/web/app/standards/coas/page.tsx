import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { StandardDocument } from "@/components/StandardDocument";
import { getStandard } from "@/lib/standards";

export const metadata: Metadata = {
  title: "NC-COAS v1",
  description: "Nature & Culture Certificate of Authenticity Standard public documentation, examples, and schema."
};

export default function COASStandardPage() {
  const standard = getStandard("coas");

  if (!standard) {
    notFound();
  }

  return <StandardDocument standard={standard} />;
}
