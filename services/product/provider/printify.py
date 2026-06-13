"""Printify POD adapter for Commerce Runtime v2."""

PRINTIFY_PRODUCT_MAP = {
    "fine_art_print": "poster",
    "framed_print": "framed_poster",
    "canvas": "canvas",
    "metal": "metal_print",
    "acrylic": "acrylic_print",
    "postcard": "postcard",
    "calendar": "calendar",
    "book": "book",
    "educational_pack": "digital_product",
    "digital_download": "digital_product",
}


def build_printify_payload(product: dict, collection: dict) -> dict:
    return {
        "provider": "printify",
        "adapter_version": "printify-commerce-runtime-v2",
        "title": product["title"],
        "description": collection["summary"],
        "blueprint_id": PRINTIFY_PRODUCT_MAP[product["product_type"]],
        "external": {"id": product["product_slug"], "handle": product["product_slug"]},
        "print_areas": [
            {
                "variant_ids": [product["variant"]],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [{"src": product["asset_url"], "x": 0.5, "y": 0.5, "scale": 1}],
                    }
                ],
            }
        ],
        "metadata": {
            "collection_slug": collection["slug"],
            "source_record_id": product["source_record_id"],
            "rights_statement_uri": product["rights_statement_uri"],
            "schema_org": product["schema_org"],
        },
    }
