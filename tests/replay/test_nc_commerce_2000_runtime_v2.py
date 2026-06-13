"""NC-COMMERCE-2000 replay coverage for Commerce Runtime v2."""

from services.product.commerce_runtime_v2 import build_commerce_runtime_v2


def test_nc_commerce_2000_runtime_v2_builds_collection_products_and_provider_payloads() -> None:
    runtime = build_commerce_runtime_v2()

    assert runtime["runtime_version"] == "NC-COMMERCE-2000-v2"
    assert runtime["collection"]["factory"] == "collection_factory"
    assert {product["factory"] for product in runtime["products"]} == {"product_factory"}
    assert runtime["summary"]["products"] == 10
    assert runtime["summary"]["pod_payloads"] == 30


def test_nc_commerce_2000_runtime_v2_payloads_cover_gelato_printful_printify() -> None:
    runtime = build_commerce_runtime_v2()
    providers = {
        provider
        for provider_payloads in runtime["pod_payloads"].values()
        for provider in provider_payloads
    }

    assert providers == {"gelato", "printful", "printify"}
    assert all(set(payloads) == providers for payloads in runtime["pod_payloads"].values())
