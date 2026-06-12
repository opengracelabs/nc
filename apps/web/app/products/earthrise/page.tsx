import type { Metadata } from "next";
import Link from "next/link";
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";
import { ManualPurchaseCTA } from "@/components/ManualPurchaseCTA";
import { EARTHRISE_RIGHTS } from "@/lib/governed-content";

export const metadata: Metadata = {
  title: "Earthrise",
  description: "Earthrise Museum Giclee and digital edition with NASA-only attribution."
};

export default function EarthriseProductPage() {
  return (
    <section className="page">
      <div className="product-layout">
        <div>
          <p className="eyebrow">NC-PROD-001 / NC-PROD-008</p>
          <h1>Earthrise</h1>
          <div className="badge-row">
            <span className="badge">Public domain</span>
            <span className="badge">17 U.S.C. § 105</span>
            <span className="badge">Certificate of Authenticity</span>
          </div>
          <div className="hero-media" role="img" aria-label="Earthrise product preview" />
          <EarthriseAttributionBlock />

          <section className="section">
            <h2>Available variants</h2>
            <div className="grid">
              <article className="card">
                <p className="eyebrow">NC-PROD-001</p>
                <h2>Earthrise Museum Giclee</h2>
                <p>24 x 20 inch museum-grade print with governed source and rights record.</p>
              </article>
              <article className="card">
                <p className="eyebrow">NC-PROD-008</p>
                <h2>Earthrise Digital Download</h2>
                <p>Digital edition delivered through a manual fulfillment path.</p>
              </article>
            </div>
          </section>

          <section className="section">
            <h2>Rights details</h2>
            <p>{EARTHRISE_RIGHTS}</p>
            <p>Source: NASA. Asset ID: AS08-14-2383. Human verified: yes.</p>
            <Link href="/stories/earthrise">Read the Earthrise story</Link>
          </section>
        </div>

        <ManualPurchaseCTA productName="Earthrise" />
      </div>
    </section>
  );
}
