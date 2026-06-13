import type { Metadata } from "next";
import Link from "next/link";
import { collections } from "@/lib/collections";
import { flagshipCollections } from "@/lib/launch-collections";

export const metadata: Metadata = {
  title: "Collections",
  description: "Curated public-domain collections from Nature & Culture."
};

const readinessClass = {
  Ready: "ready",
  Review: "review",
  Hold: "hold"
} as const;

export default function CollectionsPage() {
  return (
    <section className="page collections-index-page">
      <p className="eyebrow">Collections</p>
      <h1>Source-led collections.</h1>
      <p className="lead">
        Curated records that connect public-domain works to stories, discovery pathways, and
        editions. Launch candidates are ranked from activation readiness before publication.
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

      <section className="launch-collections-section" aria-labelledby="launch-collections-title">
        <div className="section-heading wide-heading">
          <p className="eyebrow" id="launch-collections-title">Flagship launch queue</p>
          <h2>First 10 activation-ranked collections.</h2>
        </div>
        <div className="launch-collection-grid">
          {flagshipCollections.map((collection, index) => (
            <article className="launch-collection-card" key={collection.slug}>
              <div className="launch-collection-visual" aria-hidden="true">
                <span>{String(index + 1).padStart(2, "0")}</span>
              </div>
              <div className="launch-collection-body">
                <p className="eyebrow">{collection.collectionFamilyLabel}</p>
                <h3>{collection.title}</h3>
                <p>
                  {collection.country} · {collection.region} · {collection.designationFamily}
                </p>
                <div className="launch-readiness-grid" aria-label="Collection readiness indicators">
                  <span className={`readiness ${readinessClass[collection.authorityReadiness]}`}>
                    Authority {collection.authorityReadiness}
                  </span>
                  <span className={`readiness ${readinessClass[collection.collectionReadiness]}`}>
                    Collection {collection.collectionReadiness}
                  </span>
                  <span className={`readiness ${readinessClass[collection.productReadiness]}`}>
                    Product {collection.productReadiness}
                  </span>
                  <span className={`readiness ${readinessClass[collection.graphReadiness]}`}>
                    Graph {collection.graphReadiness}
                  </span>
                </div>
                <div className="launch-card-footer">
                  <span>Activation score {collection.activationScore}</span>
                  <Link href={`/collections/family/${collection.collectionFamilySlug}`}>
                    View family
                  </Link>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
