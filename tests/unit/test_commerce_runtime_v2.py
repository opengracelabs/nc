from services.api.main import app
from services.product.commerce_runtime_v2 import (
    PRODUCT_TYPES,
    PROVIDER_NAMES,
    REFERENCE_MODELS,
    REFERENCE_STANDARDS,
    build_collection_factory,
    build_commerce_runtime_v2,
    build_pod_payload,
    build_product_factory,
)


def test_commerce_runtime_v2_router_is_registered() -> None:
    paths = {route.path for route in app.routes}

    assert "/products/commerce-runtime-v2" in paths
    assert "/products/commerce-runtime-v2/{collection_slug}" in paths


def test_collection_factory_references_requested_standards_and_models() -> None:
    runtime = build_commerce_runtime_v2()
    collection = runtime["collection"]

    for standard in ("IIIF", "CIDOC CRM", "Darwin Core", "Schema.org", "RightsStatements.org", "OpenAPI"):
        assert standard in runtime["reference_standards"]
        assert standard in REFERENCE_STANDARDS

    for model in ("Rijksmuseum", "Smithsonian", "Europeana", "Gelato", "Printful", "Printify"):
        assert model in runtime["reference_models"]

    assert collection["metadata_crosswalk"]["iiif"]["manifest"]
    assert collection["metadata_crosswalk"]["cidoc_crm"]["identified_by"] == "AS08-14-2383"
    assert collection["metadata_crosswalk"]["rightsstatements_org"]["rights_status"] == "verified_pd"


def test_product_factory_generates_all_requested_product_types() -> None:
    runtime = build_commerce_runtime_v2()
    products = runtime["products"]

    assert len(products) == 10
    assert {product["product_type"] for product in products} == set(PRODUCT_TYPES)
    for expected in (
        "fine_art_print",
        "framed_print",
        "canvas",
        "metal",
        "acrylic",
        "postcard",
        "calendar",
        "book",
        "educational_pack",
        "digital_download",
    ):
        assert expected in {product["product_type"] for product in products}


def test_collection_to_products_to_pod_payloads_is_deterministic() -> None:
    first = build_commerce_runtime_v2()
    second = build_commerce_runtime_v2()

    assert first == second
    assert first["summary"] == {
        "collections": 1,
        "products": 10,
        "providers": 3,
        "pod_payloads": 30,
    }
    assert len(first["runtime_hash"]) == 64


def test_provider_adapters_generate_payload_for_every_product() -> None:
    runtime = build_commerce_runtime_v2()
    collection = runtime["collection"]

    for product in runtime["products"]:
        for provider in PROVIDER_NAMES:
            payload = build_pod_payload(product, collection, provider)
            assert payload["provider"] == provider
            assert payload["payload_hash"]
            assert product["source_record_id"] in str(payload)
            assert product["rights_statement_uri"] in str(payload)


def test_collection_and_product_factories_accept_custom_source() -> None:
    source = {
        "slug": "smithsonian-botany-study",
        "title": "Smithsonian Botany Study Collection",
        "short_title": "Botany Study",
        "source_institution": "Smithsonian",
        "source_record_id": "NMNH-BOT-001",
        "source_url": "https://example.org/smithsonian/botany",
        "asset_url": "https://example.org/iiif/botany/full/full/0/default.jpg",
        "iiif_manifest_url": "https://example.org/iiif/botany/manifest",
        "rights_statement_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "rights_status": "verified_cc0",
        "rights_basis": "CC0",
        "schema_org_type": "VisualArtwork",
        "cidoc_type": "E22_Human-Made_Object",
        "darwin_core_basis": "PreservedSpecimen",
        "reference_model": "Smithsonian",
        "collection_summary": "A specimen-backed public-domain study collection.",
    }

    collection = build_collection_factory(source)
    products = build_product_factory(collection)

    assert collection["slug"] == "smithsonian-botany-study"
    assert collection["metadata_crosswalk"]["darwin_core"]["basisOfRecord"] == "PreservedSpecimen"
    assert len(products) == len(PRODUCT_TYPES)
    assert products[0]["collection_slug"] == collection["slug"]
