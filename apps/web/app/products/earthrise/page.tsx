import type { Metadata } from "next";
import Link from "next/link";
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";
import { ManualPurchaseCTA } from "@/components/ManualPurchaseCTA";
import { EARTHRISE_RIGHTS, NASA_EARTHRISE_CREDIT, NASA_NONENDORSEMENT } from "@/lib/governed-content";

export const metadata: Metadata = {
  title: "Earthrise",
  description: "Earthrise Museum Giclee and Digital Edition with NASA-only attribution."
};

export default function EarthriseProductPage() {
  return (
    <section className="page product-page premium-product-page">
      <div className="product-layout premium-product-layout">
        <div>
          <Link className="text-link" href="/collections/earthrise">
            Back to Earthrise Collection
          </Link>
          <p className="eyebrow">Apollo 8 · William Anders</p>
          <h1>Earthrise</h1>
          <p className="lead">
            A MASTERWORK source image offered in two distinct editions: a physical Museum Print for
            display and a Digital Edition for close study.
          </p>
          <div className="badge-row">
            <span className="masterwork-badge">MASTERWORK</span>
            <span className="badge">Public domain</span>
            <span className="badge">17 U.S.C. § 105</span>
          </div>
          <figure className="earthrise-frame product-image-frame premium-product-image">
            <img
              className="earthrise-image"
              src="/images/earthrise-as08-14-2383.jpg"
              alt="Earth rising above the lunar horizon during Apollo 8"
            />
            <figcaption>NASA · Apollo 8 · William Anders · Public Domain</figcaption>
          </figure>

          <section className="section compact-section edition-comparison-section">
            <p className="eyebrow">Choose an edition</p>
            <h2>Two editions, two jobs.</h2>
            <div className="edition-comparison-grid">
              <article className="edition-panel museum-edition">
                <span className="edition-kicker">For display</span>
                <h3>Museum Print</h3>
                <p>
                  A physical edition for rooms where the image should hold the wall: quiet, large,
                  source-backed, and ready for framed presentation.
                </p>
                <dl>
                  <div><dt>Format</dt><dd>24 x 20 inch archival print</dd></div>
                  <div><dt>Best for</dt><dd>Collectors, gifts, offices, and gallery-style display</dd></div>
                  <div><dt>Included</dt><dd>Certificate of Authenticity and NASA attribution</dd></div>
                </dl>
              </article>
              <article className="edition-panel digital-edition">
                <span className="edition-kicker">For study</span>
                <h3>Digital Edition</h3>
                <p>
                  A high-resolution file for close reading of the frame, teaching, presentation, and
                  personal archival use.
                </p>
                <dl>
                  <div><dt>Format</dt><dd>Digital image edition</dd></div>
                  <div><dt>Best for</dt><dd>Classrooms, lectures, reference, and personal study</dd></div>
                  <div><dt>Included</dt><dd>Source and attribution notes for responsible reuse</dd></div>
                </dl>
              </article>
            </div>
          </section>

          <section className="section compact-section provenance-section">
            <p className="eyebrow">Provenance</p>
            <h2>Source record at a glance.</h2>
            <div className="provenance-glance">
              <span>NASA</span>
              <span>Apollo 8</span>
              <span>December 24, 1968</span>
              <span>Public Domain</span>
            </div>
            <details className="provenance-panel">
              <summary>View full provenance</summary>
              <div className="provenance-detail-grid">
                <div>
                  <strong>Attribution</strong>
                  <p>{NASA_EARTHRISE_CREDIT}</p>
                </div>
                <div>
                  <strong>Rights basis</strong>
                  <p>{EARTHRISE_RIGHTS}</p>
                </div>
                <div>
                  <strong>Source identifier</strong>
                  <p>AS08-14-2383</p>
                </div>
                <div>
                  <strong>Nonendorsement</strong>
                  <p>{NASA_NONENDORSEMENT}</p>
                </div>
              </div>
            </details>
          </section>

          <section className="section compact-section">
            <p className="eyebrow">Why it matters</p>
            <h2>A new portrait of home.</h2>
            <p>
              Earthrise compressed distance, exploration, and environmental memory into one frame.
              It showed a living planet above the lunar surface and turned a mission of outward
              exploration into an image of shared home.
            </p>
            <Link href="/stories/earthrise">Read the Earthrise story</Link>
          </section>
        </div>

        <aside className="purchase-stack">
          <ManualPurchaseCTA productName="Earthrise" />
          <EarthriseAttributionBlock />
        </aside>
      </div>
    </section>
  );
}
