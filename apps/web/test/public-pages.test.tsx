import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, test } from "vitest";
import ProductsPage from "@/app/products/page";
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

  test("Products page only shows approved Phase 0 products", async () => {
    const page = await ProductsPage();
    const html = renderToStaticMarkup(page);

    expect(html).toContain("Earthrise Museum Giclee");
    expect(html).toContain("Earthrise Digital Download");
    expect(html).not.toContain("Yellowstone from Orbit");
    expect(html).not.toContain("Grand Canyon");
    expect(html).not.toContain("Smithsonian");
  });

  test("Manual purchase CTA renders", () => {
    const html = renderToStaticMarkup(<EarthriseProductPage />);

    expect(html).toContain("Request purchase");
    expect(html).toContain("manual invoice");
  });
});
