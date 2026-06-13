import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  getLaunchCollectionFamily,
  launchCollectionFamilies
} from "@/lib/launch-collections";
import type { ActivationReadiness } from "@/lib/place-activation-dashboard";

type PageProps = {
  params: Promise<{ family: string }>;
};

const readinessClass: Record<ActivationReadiness, string> = {
  Ready: "ready",
  Review: "review",
  Hold: "hold"
};

export function generateStaticParams() {
  return launchCollectionFamilies.map((family) => ({ family: family.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { family: familySlug } = await params;
  const family = getLaunchCollectionFamily(familySlug);
  if (!family) {
    return { title: "Collection family" };
  }
  return {
    title: family.label,
    description: `${family.label} activation candidates and collection readiness.`
  };
}

export default async function CollectionFamilyPage({ params }: PageProps) {
  const { family: familySlug } = await params;
  const family = getLaunchCollectionFamily(familySlug);
  if (!family) {
    notFound();
  }

  return (
    <section className="page collection-family-page">
      <p className="eyebrow">Collection family</p>
      <h1>{family.label}</h1>
      <p className="lead">
        Activation-ranked candidates in this family, held with readiness indicators until
        authority review and publishing readiness are complete.
      </p>

      <div className="family-readiness-summary" aria-label="Collection family readiness summary">
        {(["Ready", "Review", "Hold"] as ActivationReadiness[]).map((state) => (
          <div key={state}>
            <span className={`readiness ${readinessClass[state]}`}>{state}</span>
            <strong>{family.readinessCounts[state]}</strong>
          </div>
        ))}
      </div>

      <div className="family-collection-list">
        {family.collections.map((collection) => (
          <article className="family-collection-row" key={collection.slug}>
            <div>
              <p className="eyebrow">{collection.designationFamily}</p>
              <h2>{collection.title}</h2>
              <p>
                {collection.country} · {collection.region} · Activation score {collection.activationScore}
              </p>
            </div>
            <div className="family-row-readiness">
              <span className={`readiness ${readinessClass[collection.authorityReadiness]}`}>
                Authority {collection.authorityReadiness}
              </span>
              <span className={`readiness ${readinessClass[collection.collectionReadiness]}`}>
                Collection {collection.collectionReadiness}
              </span>
              <span className={`readiness ${readinessClass[collection.publishingReadiness]}`}>
                Publishing {collection.publishingReadiness}
              </span>
            </div>
          </article>
        ))}
      </div>

      <Link className="button secondary-button" href="/collections">
        Back to collections
      </Link>
    </section>
  );
}
