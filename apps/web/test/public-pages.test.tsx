import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, test } from "vitest";
import RootLayout from "@/app/layout";
import CertificatePage from "@/app/certificate/page";
import CuratorProfilePage from "@/app/curators/[slug]/page";
import CuratorsPage from "@/app/curators/page";
import InstitutionHubPage from "@/app/institution/page";
import InstitutionFactoryPage from "@/app/institutions/factory/page";
import MasterpieceDetailPage from "@/app/masterpieces/[slug]/page";
import MasterpiecesPage from "@/app/masterpieces/page";
import Top100MasterpiecesPage from "@/app/masterpieces/top-100/page";
import InstitutionProfilePage from "@/app/institutions/[slug]/page";
import InstitutionsPage from "@/app/institutions/page";
import SignatureCollectionHubPage from "@/app/signature/page";
import HomePage from "@/app/page";
import CollectionsPage from "@/app/collections/page";
import DiscoverPage from "@/app/discover/page";
import DiscoverGraphPage from "@/app/discover/graph/page";
import PlaceFactoryDashboardPage from "@/app/place-factory/page";
import PlaceFactoryCoverageDashboardPage from "@/app/place-factory/coverage/page";
import ActivationDashboardPage from "@/app/place-factory/activation/page";
import AlhambraCollectionPage from "@/app/collections/alhambra/page";
import ChichenItzaCollectionPage from "@/app/collections/chichen-itza/page";
import CollectionFamilyPage from "@/app/collections/family/[family]/page";
import PetraCollectionPage from "@/app/collections/petra/page";
import SouthGeorgiaCollectionPage from "@/app/collections/south-georgia/page";
import VersaillesCollectionPage from "@/app/collections/versailles/page";
import EarthriseCollectionPage, { metadata as earthriseCollectionMetadata } from "@/app/collections/earthrise/page";
import ProductsPage from "@/app/products/page";
import RegistryPage from "@/app/registry/page";
import CoasStandardPage from "@/app/standards/coas/page";
import ErsStandardPage from "@/app/standards/ers/page";
import PdpsStandardPage from "@/app/standards/pdps/page";
import StandardsPage from "@/app/standards/page";
import VerifyCertificatePage from "@/app/verify/[certificate]/page";
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
    expect(layoutHtml).toContain("Masterpieces");
    expect(layoutHtml).toContain("Signature");
    expect(layoutHtml).toContain("Institution");
    expect(layoutHtml).toContain("Institutions");
    expect(layoutHtml).toContain("Curators");
    expect(layoutHtml).toContain("Standards");
    expect(layoutHtml).toContain("Discover");
  });

  test("Discover page renders journey-first graph surfaces", () => {
    const html = renderToStaticMarkup(<DiscoverPage />);

    expect(html).toContain("Start with a journey");
    expect(html).toContain("Recommended now");
    expect(html).toContain("Related journeys");
    expect(html).toContain("Nearby places");
    expect(html).toContain("Collection graph");
    expect(html).toContain("Earthrise Collection");
    expect(html).toContain("Great Barrier Reef");
  });

  test("Place Factory Dashboard v2 renders readiness columns", () => {
    const html = renderToStaticMarkup(<PlaceFactoryDashboardPage />);

    expect(html).toContain("Place Factory Dashboard v2");
    expect(html).toContain("10,000 places");
    expect(html).toContain("Authority");
    expect(html).toContain("Collection Family");
    expect(html).toContain("Discovery Family");
    expect(html).toContain("Commerce Readiness");
    expect(html).toContain("UNESCO");
    expect(html).toContain("Biosphere");
    expect(html).toContain("Geopark");
    expect(html).toContain("Ramsar");
    expect(html).toContain("ICH");
  });


  test("Place Factory Coverage Dashboard renders source coverage gaps", () => {
    const html = renderToStaticMarkup(<PlaceFactoryCoverageDashboardPage />);

    expect(html).toContain("Place Factory Coverage Dashboard");
    expect(html).toContain("World map");
    expect(html).toContain("Regions");
    expect(html).toContain("Designation counts");
    expect(html).toContain("Authority gaps");
    expect(html).toContain("Collection family gaps");
    expect(html).toContain("218");
    expect(html).toContain("Source-observed only");
    expect(html).toContain("Dark Sky Collection");
    expect(html).toContain("Marine Collection");
  });


  test("Activation Dashboard renders top places and readiness columns", () => {
    const html = renderToStaticMarkup(<ActivationDashboardPage />);

    expect(html).toContain("Activation Dashboard");
    expect(html).toContain("Top 25 places");
    expect(html).toContain("Authority readiness");
    expect(html).toContain("Collection readiness");
    expect(html).toContain("Product readiness");
    expect(html).toContain("Graph readiness");
    expect(html).toContain("Publishing readiness");
    expect(html).toContain("candidate pool");
  });


  test("Signature Collection Hub renders the five flagship collections", () => {
    const html = renderToStaticMarkup(<SignatureCollectionHubPage />);

    expect(html).toContain("Signature Collection Hub");
    expect(html).toContain("Five collections for deep looking");
    expect(html).toContain("Alhambra: Water, Geometry, Garden");
    expect(html).toContain("South Georgia: Ice, Expedition, Recovery");
    expect(html).toContain("Versailles: Garden, State, Spectacle");
    expect(html).toContain("Chichen Itza: Calendar, City, Cenote");
    expect(html).toContain("Petra: Stone, Water, Caravan");
    expect(html).toContain("Visitor paths");
  });


  test("Institution Hub renders mission and institutional work areas", () => {
    const html = renderToStaticMarkup(<InstitutionHubPage />);

    expect(html).toContain("Nature &amp; Culture is a public collection institution");
    expect(html).toContain("Mission");
    expect(html).toContain("Collections");
    expect(html).toContain("Discovery");
    expect(html).toContain("Education");
    expect(html).toContain("Conservation");
    expect(html).toContain("Commerce");
    expect(html).toContain("Institutional standards");
  });


  test("Trust pages render certificate and registry panels", () => {
    const certificateHtml = renderToStaticMarkup(<CertificatePage />);
    const registryHtml = renderToStaticMarkup(<RegistryPage />);

    expect(certificateHtml).toContain("Certificate of Authenticity");
    expect(certificateHtml).toContain("Curator Panel");
    expect(certificateHtml).toContain("Source Institution Panel");
    expect(certificateHtml).toContain("Educational Use Panel");
    expect(certificateHtml).toContain("NC-COA-EARTHRISE-0001");
    expect(certificateHtml).toContain("Certificate signatory");
    expect(certificateHtml).toContain("Nathan Holderhead");
    expect(certificateHtml).toContain("Founding Curator page");
    expect(registryHtml).toContain("Edition Registry");
    expect(registryHtml).toContain("Earthrise Museum Giclee");
    expect(registryHtml).toContain("Earthrise Digital Download");
    expect(registryHtml).toContain("NC-REG-EARTHRISE-MP-0001");
  });


  test("Institution and curator trust directories render profiles", async () => {
    const institutionsHtml = renderToStaticMarkup(<InstitutionsPage />);
    const curatorsHtml = renderToStaticMarkup(<CuratorsPage />);
    const nasaPage = await InstitutionProfilePage({
      params: Promise.resolve({ slug: "nasa" })
    });
    const curatorPage = await CuratorProfilePage({
      params: Promise.resolve({ slug: "founding-curator" })
    });
    const nasaHtml = renderToStaticMarkup(nasaPage);
    const curatorHtml = renderToStaticMarkup(curatorPage);

    expect(institutionsHtml).toContain("Institutional trust network");
    expect(institutionsHtml).toContain("NASA");
    expect(institutionsHtml).toContain("UNESCO World Heritage Centre");
    expect(curatorsHtml).toContain("Named curator support");
    expect(curatorsHtml).toContain("Nathan Holderhead");
    expect(curatorsHtml).toContain("Founding Curator page");
    expect(nasaHtml).toContain("Institution profile");
    expect(nasaHtml).toContain("Earthrise: The Oasis Collection");
    expect(nasaHtml).toContain("Nathan Holderhead");
    expect(nasaHtml).toContain("/curators/founding-curator");
    expect(nasaHtml).toContain("Public provenance chain");
    expect(nasaHtml).toContain("Public edition verification");
    expect(nasaHtml).toContain("Educational Use Panel");
    expect(curatorHtml).toContain("Curator profile");
    expect(curatorHtml).toContain("Curator biography");
    expect(curatorHtml).toContain("Certificate signatory");
    expect(curatorHtml).toContain("Alhambra: Water, Geometry, Garden");
  });


  test("Masterpiece Registry renders ranked routes", async () => {
    const indexHtml = renderToStaticMarkup(<MasterpiecesPage />);
    const topHtml = renderToStaticMarkup(<Top100MasterpiecesPage />);
    const detail = await MasterpieceDetailPage({
      params: Promise.resolve({ slug: "earthrise" })
    });
    const detailHtml = renderToStaticMarkup(detail);

    expect(indexHtml).toContain("Masterpiece Registry");
    expect(indexHtml).toContain("masterpiece_registry");
    expect(indexHtml).toContain("Earthrise");
    expect(indexHtml).toContain("Acanthaster planci plate");
    expect(topHtml).toContain("Top 100 Masterpieces");
    expect(topHtml).toContain("masterpiece_score");
    expect(topHtml).toContain("Bison bison range plate");
    expect(detailHtml).toContain("masterpiece_score");
    expect(detailHtml).toContain("masterpiece_collections");
    expect(detailHtml).toContain("Published masterwork");
  });


  test("Institution Factory dashboard renders candidate-only institution runtime", () => {
    const html = renderToStaticMarkup(<InstitutionFactoryPage />);

    expect(html).toContain("Institution Factory Runtime");
    expect(html).toContain("institution_registry");
    expect(html).toContain("institution_readiness");
    expect(html).toContain("institution_asset_counts");
    expect(html).toContain("institution_collection_counts");
    expect(html).toContain("Biodiversity Heritage Library");
    expect(html).toContain("Rijksmuseum");
    expect(html).toContain("National Archives and Records Administration");
    expect(html).toContain("No canonical publication");
  });


  test("Verify certificate page renders provenance chain and edition verification", async () => {
    const page = await VerifyCertificatePage({
      params: Promise.resolve({ certificate: "NC-COA-EARTHRISE-0001" })
    });
    const html = renderToStaticMarkup(page);

    expect(html).toContain("Certificate verified");
    expect(html).toContain("Public provenance chain");
    expect(html).toContain("Public edition verification");
    expect(html).toContain("Educational Use Panel");
    expect(html).toContain("Earthrise Museum Giclee");
    expect(html).toContain("NC-REG-EARTHRISE-DD-0001");
  });


  test("Standards pages render public documentation examples and schemas", () => {
    const indexHtml = renderToStaticMarkup(<StandardsPage />);
    const pdpsHtml = renderToStaticMarkup(<PdpsStandardPage />);
    const coasHtml = renderToStaticMarkup(<CoasStandardPage />);
    const ersHtml = renderToStaticMarkup(<ErsStandardPage />);

    expect(indexHtml).toContain("NC-PDPS v1");
    expect(indexHtml).toContain("NC-COAS v1");
    expect(indexHtml).toContain("NC-ERS v1");

    for (const html of [pdpsHtml, coasHtml, ersHtml]) {
      expect(html).toContain("Public documentation");
      expect(html).toContain("Public schema");
      expect(html).toContain("Public example");
    }

    expect(pdpsHtml).toContain("source_institution");
    expect(pdpsHtml).toContain("provenance_chain");
    expect(coasHtml).toContain("certificate_id");
    expect(coasHtml).toContain("signatory_name");
    expect(coasHtml).toContain("edition_registry_ids");
    expect(ersHtml).toContain("registry_id");
    expect(ersHtml).toContain("edition_title");
  });

  test("Discover graph page renders Neo4j graph runtime", async () => {
    const page = await DiscoverGraphPage();
    const html = renderToStaticMarkup(page);

    expect(html).toContain("Discovery graph runtime");
    expect(html).toContain("Neo4j graph");
    expect(html).toContain("Earthrise: The Oasis Collection");
    expect(html).toContain("RECOMMENDS");
    expect(html).toContain("Great Barrier Reef");
  });

  test("Collections page renders first 10 activation flagship collections", () => {
    const indexHtml = renderToStaticMarkup(<CollectionsPage />);

    expect(indexHtml).toContain("Earthrise: The Oasis Collection");
    expect(indexHtml).toContain("Flagship launch queue");
    expect(indexHtml).toContain("First 10 activation-ranked collections");
    expect(indexHtml).toContain("pont Saint-Bénézet: World Heritage Collection");
    expect(indexHtml).toContain("iSimangaliso Wetland Park: World Heritage Collection");
    expect(indexHtml).toContain("Authority Review");
    expect(indexHtml).toContain("Collection Ready");
    expect(indexHtml).toContain("Product Review");
    expect(indexHtml).toContain("Graph Ready");
  });

  test("Collection family page renders readiness indicators", async () => {
    const page = await CollectionFamilyPage({
      params: Promise.resolve({ family: "world-heritage" })
    });
    const html = renderToStaticMarkup(page);

    expect(html).toContain("World Heritage Collection");
    expect(html).toContain("Collection family");
    expect(html).toContain("Publishing Review");
    expect(html).toContain("Back to collections");
  });


  test("new flagship collection pages render required collection sections", () => {
    const pages = [
      renderToStaticMarkup(<AlhambraCollectionPage />),
      renderToStaticMarkup(<SouthGeorgiaCollectionPage />),
      renderToStaticMarkup(<VersaillesCollectionPage />),
      renderToStaticMarkup(<ChichenItzaCollectionPage />),
      renderToStaticMarkup(<PetraCollectionPage />)
    ];

    for (const html of pages) {
      expect(html).toContain("Collection narrative");
      expect(html).toContain("Discovery journey");
      expect(html).toContain("Featured works");
      expect(html).toContain("Products");
      expect(html).toContain("Next journeys");
      expect(html).toContain("Provenance glance");
      expect(html).toContain("FLAGSHIP COLLECTION");
      expect(html).toContain("Curated by Nathan Holderhead");
      expect(html).toContain("Source institution:");
    }

    expect(pages[0]).toContain("Alhambra: Water, Geometry, Garden");
    expect(pages[1]).toContain("South Georgia: Ice, Expedition, Recovery");
    expect(pages[2]).toContain("Versailles: Garden, State, Spectacle");
    expect(pages[3]).toContain("Chichen Itza: Calendar, City, Cenote");
    expect(pages[4]).toContain("Petra: Stone, Water, Caravan");
  });

  test("Earthrise collection detail renders as a collection experience", () => {
    const detailHtml = renderToStaticMarkup(<EarthriseCollectionPage />);

    expect(detailHtml).toContain("Curated by Nathan Holderhead");
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
