"""Printful POD adapter for Commerce Runtime v2."""

PRINTFUL_PRODUCT_MAP = {
    "fine_art_print": "enhanced_matte_paper_poster",
    "framed_print": "framed_poster",
    "canvas": "canvas",
    "metal": "metal_print",
    "acrylic": "acrylic_print",
    "postcard": "postcard",
    "calendar": "calendar",
    "book": "softcover_book",
    "educational_pack": "downloadable_file",
    "digital_download": "downloadable_file",
}


def build_printful_payload(product: dict, collection: dict) -> dict:
    return {
        "provider": "printful",
        "adapter_version": "printful-commerce-runtime-v2",
        "sync_product": {
            "external_id": product["product_slug"],
            "name": product["title"],
            "thumbnail": product["asset_url"],
        },
        "sync_variants": [
            {
                "external_id": f"{product['product_slug']}-default",
                "variant_id": PRINTFUL_PRODUCT_MAP[product["product_type"]],
                "retail_price": "0.00",
                "files": [{"type": "default", "url": product["asset_url"]}],
            }
        ],
        "metadata": {
            "collection_slug": collection["slug"],
            "source_record_id": product["source_record_id"],
            "rights_statement_uri": product["rights_statement_uri"],
            "requires_shipping": product["requires_shipping"],
        },
    }
