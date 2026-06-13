import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { StandardDocument } from "@/components/StandardDocument";
import { getStandard } from "@/lib/standards";

export const metadata: Metadata = {
  title: "NC-ERS v1",
  description: "Nature & Culture Edition Registry Standard public documentation, examples, and schema."
};

export default function ERSStandardPage() {
  const standard = getStandard("ers");

  if (!standard) {
    notFound();
  }

  return <StandardDocument standard={standard} />;
}
