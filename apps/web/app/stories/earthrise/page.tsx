import type { Metadata } from "next";
import Link from "next/link";
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";

export const metadata: Metadata = {
  title: "Earthrise Story",
  description: "The Apollo 8 Earthrise photograph with governed NASA attribution."
};

export default function EarthriseStoryPage() {
  return (
    <article className="page">
      <p className="eyebrow">Story</p>
      <h1>Earthrise</h1>
      <div className="hero-media" role="img" aria-label="Earthrise story visual" />
      <EarthriseAttributionBlock />

      <div className="story-body">
        <p>
          Earthrise was photographed during Apollo 8 on December 24, 1968. The image became a
          cultural reference point for seeing Earth as a shared, fragile world.
        </p>
        <p>
          Nature & Culture presents the image as a verified public-domain work with source,
          rights, and attribution visible beside the experience.
        </p>
      </div>

      <section className="section">
        <h2>Own Earthrise</h2>
        <p>Shop the Phase 0 Earthrise product family through manual purchase.</p>
        <Link className="button" href="/products/earthrise">
          View Earthrise products
        </Link>
      </section>
    </article>
  );
}
