import type { Metadata } from "next";
import { CollectionDetailTemplate } from "@/components/CollectionDetailTemplate";
import { versaillesCollection as collection } from "@/lib/collections";

export const metadata: Metadata = {
  title: collection.seoTitle,
  description: collection.seoDescription,
  alternates: {
    canonical: "/collections/versailles"
  },
  openGraph: {
    title: collection.seoTitle,
    description: collection.seoDescription,
    type: "article",
    images: [collection.imageSrc]
  }
};

export default function CollectionPage() {
  return <CollectionDetailTemplate collection={collection} />;
}
