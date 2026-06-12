import type { Metadata } from "next";
import Link from "next/link";
import { collections } from "@/lib/collections";

export const metadata: Metadata = {
  title: "Collections",
  description: "Curated public-domain collections from Nature & Culture."
};

export default function CollectionsPage() {
  return (
    <section className="page collections-index-page">
      <p className="eyebrow">Collections</p>
      <h1>Source-led collections.</h1>
      <p className="lead">
        Curated records that connect public-domain works to stories, discovery pathways, and
        editions.
      </p>

      <div className="collection-card-grid collection-index-grid">
        {collections.map((collection) => {
          const isLive = collection.status === "live";
          const href = isLive ? "/collections/" + collection.slug : "/places";

          return (
            <article className="collection-card image-card" key={collection.slug}>
              <img src={collection.imageSrc} alt={collection.imageAlt} />
              <div>
                <span className="masterwork-badge">{collection.badge}</span>
                <h2>{collection.title}</h2>
                <p>{collection.summary}</p>
                <Link href={href}>{isLive ? "Explore the collection" : "Preview the place"}</Link>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
