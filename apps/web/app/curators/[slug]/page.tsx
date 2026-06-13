import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { collections } from "@/lib/collections";
import { getTrustCurator, trustCurators } from "@/lib/trust";

type PageProps = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return trustCurators.map((curator) => ({ slug: curator.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const curator = getTrustCurator(slug);
  return {
    title: curator ? curator.name : "Curator",
    description: curator?.summary ?? "Curator profile"
  };
}

export default async function CuratorProfilePage({ params }: PageProps) {
  const { slug } = await params;
  const curator = getTrustCurator(slug);
  if (!curator) {
    notFound();
  }
  const curatedCollections = collections.filter((collection) =>
    curator.collections.includes(collection.slug)
  );

  return (
    <section className="page trust-profile-page">
      <p className="eyebrow">Curator profile</p>
      <h1>{curator.name}</h1>
      <p className="lead">{curator.profile}</p>

      <div className="trust-profile-facts">
        <div><span>Title</span><strong>{curator.title}</strong></div>
        <div><span>Byline</span><strong>{curator.byline}</strong></div>
        <div><span>Certificate signatory</span><strong>{curator.signatoryLabel}</strong></div>
      </div>

      <section className="trust-ownership-section curator-biography-section">
        <p className="eyebrow">Curator biography</p>
        <h2>Named responsibility for public collection records.</h2>
        <p>{curator.biography}</p>
      </section>

      <section className="trust-ownership-section">
        <p className="eyebrow">Collection bylines</p>
        <h2>Collections curated by {curator.name}.</h2>
        <div className="trust-ownership-list">
          {curatedCollections.map((collection) => (
            <Link href={`/collections/${collection.slug}`} key={collection.slug}>
              <strong>{collection.title}</strong>
              <span>{collection.summary}</span>
            </Link>
          ))}
        </div>
      </section>
    </section>
  );
}
