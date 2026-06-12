import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, test } from "vitest";
import RootLayout from "@/app/layout";
import HomePage from "@/app/page";
import CollectionsPage from "@/app/collections/page";
import EarthriseCollectionPage, { metadata as earthriseCollectionMetadata } from "@/app/collections/earthrise/page";
import ProductsPage from "@/app/products/page";
import EarthriseStoryPage from "@/app/stories/earthrise/page";
import EarthriseProductPage from "@/app/products/earthrise/page";
import { NASA_EARTHRISE_CREDIT, NASA_NONENDORSEMENT } from "@/lib/governed-content";

describe("NC-WEB-001 public pages", () => {
  test("Earthrise page contains NASA credit and nonendorsement", () => {
    const html = renderToStaticMarkup(<EarthriseProductPage />);

    expect(html).toContain(NASA_EARTHRISE_CREDIT);
    expect(html).toContain(NASA_NONENDORSEMENT);
  });

  test("Earthrise page does not contain prohibited attribution or endorsement language", () => {
    const html = renderToStaticMarkup(<EarthriseProductPage />);

    expect(html).not.toContain("NARA");
    expect(html).not.toContain("Verified by NASA");
  });

  test("Products page only shows public Earthrise editions", async () => {
    const page = await ProductsPage();
    const html = renderToStaticMarkup(page);

    expect(html).toContain("Earthrise Museum Giclee");
    expect(html).toContain("Earthrise Digital Download");
    expect(html).not.toContain("Yellowstone from Orbit");
    expect(html).not.toContain("Grand Canyon");
    expect(html).not.toContain("Smithsonian");
  });

  test("Visitor pages do not render internal labels", async () => {
    const home = await HomePage();
    const products = await ProductsPage();
    const homeHtml = renderToStaticMarkup(home);
    const productsHtml = renderToStaticMarkup(products);
    const productHtml = renderToStaticMarkup(<EarthriseProductPage />);

    for (const html of [homeHtml, productsHtml, productHtml]) {
      expect(html).not.toContain("Phase 0");
      expect(html).not.toContain("NC-PROD");
      expect(html).not.toContain("Governed");
      expect(html).not.toContain("governed");
    }
  });

  test("Premium sprint elements render", async () => {
    const home = await HomePage();
    const homeHtml = renderToStaticMarkup(home);
    const productHtml = renderToStaticMarkup(<EarthriseProductPage />);
    const layoutHtml = renderToStaticMarkup(<RootLayout><main /></RootLayout>);

    expect(homeHtml).toContain("full-bleed-hero");
    expect(homeHtml).toContain("collection-card image-card");
    expect(homeHtml).toContain("MASTERWORK");
    expect(productHtml).toContain("View full provenance");
    expect(productHtml).toContain("provenance-panel");
    expect(layoutHtml).toContain("Collections");
    expect(layoutHtml).toContain("Discover");
  });

  test("Collection pages render Earthrise as a collection experience", () => {
    const indexHtml = renderToStaticMarkup(<CollectionsPage />);
    const detailHtml = renderToStaticMarkup(<EarthriseCollectionPage />);

    expect(indexHtml).toContain("Earthrise: The Oasis Collection");
    expect(indexHtml).toContain("Explore the collection");
    expect(indexHtml).not.toContain("Yellowstone: Fire and Water Collection");
    expect(indexHtml).not.toContain("Grand Canyon: Deep Time Collection");
    expect(indexHtml).not.toContain("Great Barrier Reef: Living Reef Collection");
    expect(detailHtml).toContain("Curator statement");
    expect(detailHtml).toContain("Discovery pathways");
    expect(detailHtml).toContain("Featured works");
    expect(detailHtml).toContain("The oasis in the desert");
    expect(detailHtml).toContain("Explore Earthrise editions");
    expect(detailHtml).toContain("Provenance glance");
    expect(detailHtml).toContain("Next journeys");
    expect(detailHtml).toContain("work-treatment-earth");
    expect(detailHtml).toContain("work-treatment-horizon");
    expect(detailHtml).toContain("work-treatment-folio");
    expect(detailHtml).toContain("/images/earthrise-work-masterwork.jpg");
    expect(detailHtml).toContain("/images/earthrise-work-horizon.jpg");
    expect(detailHtml).toContain("/images/earthrise-work-folio.jpg");
    expect(detailHtml).toContain("Breadcrumb");
  });

  test("Earthrise collection exposes collection-specific SEO metadata", () => {
    expect(earthriseCollectionMetadata.title).toBe("Earthrise: The Oasis Collection");
    expect(earthriseCollectionMetadata.description).toContain("Overview Effect");
    expect(earthriseCollectionMetadata.alternates).toEqual({ canonical: "/collections/earthrise" });
  });

  test("Availability CTA renders", () => {
    const html = renderToStaticMarkup(<EarthriseProductPage />);

    expect(html).toContain("Contact for availability");
    expect(html).toContain("Contact us");
    expect(html).toContain("availability, payment, and fulfillment details");
    expect(html).not.toContain("Request purchase");
  });

  test("Earthrise story falls back to static editorial copy", async () => {
    const page = await EarthriseStoryPage();
    const html = renderToStaticMarkup(page);

    expect(html).toContain("Earthrise was photographed during Apollo 8");
    expect(html).toContain(NASA_NONENDORSEMENT);
    expect(html).not.toContain("NARA");
    expect(html).not.toContain("Verified by NASA");
  });
});
