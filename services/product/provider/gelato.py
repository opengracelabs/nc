"""Gelato POD adapter for Commerce Runtime v2."""

GELATO_PRODUCT_MAP = {
    "fine_art_print": "poster",
    "framed_print": "framed_poster",
    "canvas": "canvas",
    "metal": "aluminum_print",
    "acrylic": "acrylic_print",
    "postcard": "cards",
    "calendar": "calendar",
    "book": "photo_book",
    "educational_pack": "document_print",
    "digital_download": "digital_file",
}


def build_gelato_payload(product: dict, collection: dict) -> dict:
    return {
        "provider": "gelato",
        "adapter_version": "gelato-commerce-runtime-v2",
        "external_id": product["product_slug"],
        "productUid": GELATO_PRODUCT_MAP[product["product_type"]],
        "title": product["title"],
        "files": [{"type": "default", "url": product["asset_url"]}],
        "metadata": {
            "collection_slug": collection["slug"],
            "source_record_id": product["source_record_id"],
            "rights_statement_uri": product["rights_statement_uri"],
            "schema_org": product["schema_org"],
        },
        "shipping": {"required": product["requires_shipping"]},
    }
