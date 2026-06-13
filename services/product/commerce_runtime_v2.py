"""Commerce Runtime v2 collection/product/POD factories.

The runtime is deterministic and network-free. Provider adapters build outbound payloads
that can be inspected, tested, and queued before any provider API call is attempted.
"""

from __future__ import annotations

from copy import deepcopy

from services.product.export import stable_json_hash

COMMERCE_RUNTIME_V2 = "NC-COMMERCE-2000-v2"

REFERENCE_STANDARDS = (
    "IIIF",
    "CIDOC CRM",
    "Darwin Core",
    "Schema.org",
    "RightsStatements.org",
    "OpenAPI",
)

REFERENCE_MODELS = (
    "Rijksmuseum",
    "Smithsonian",
    "Europeana",
    "Gelato",
    "Printful",
)

PROVIDER_NAMES = ("gelato", "printful", "printify")

PRODUCT_TYPES = (
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
)

PRODUCT_TYPE_LABELS = {
    "fine_art_print": "Fine Art Print",
    "framed_print": "Framed Print",
    "canvas": "Canvas",
    "metal": "Metal",
    "acrylic": "Acrylic",
    "postcard": "Postcard",
    "calendar": "Calendar",
    "book": "Book",
    "educational_pack": "Educational Pack",
    "digital_download": "Digital Download",
}

PRODUCT_SPECS = {
    "fine_art_print": {"surface": "archival matte paper", "variant": "18x24", "requires_shipping": True},
    "framed_print": {"surface": "framed archival print", "variant": "20x28 black frame", "requires_shipping": True},
    "canvas": {"surface": "stretched canvas", "variant": "24x30", "requires_shipping": True},
    "metal": {"surface": "aluminum metal print", "variant": "16x20", "requires_shipping": True},
    "acrylic": {"surface": "acrylic face mount", "variant": "16x20", "requires_shipping": True},
    "postcard": {"surface": "postcard stock", "variant": "set of 8", "requires_shipping": True},
    "calendar": {"surface": "wall calendar", "variant": "12 month", "requires_shipping": True},
    "book": {"surface": "softcover book", "variant": "48 page", "requires_shipping": True},
    "educational_pack": {"surface": "classroom PDF plus source notes", "variant": "teacher pack", "requires_shipping": False},
    "digital_download": {"surface": "high resolution digital file", "variant": "download", "requires_shipping": False},
}

SEED_COLLECTION_SOURCES = {
    "earthrise": {
        "slug": "earthrise",
        "title": "Earthrise: The Oasis Collection",
        "short_title": "Earthrise",
        "source_institution": "NASA",
        "source_record_id": "AS08-14-2383",
        "source_url": "https://www.nasa.gov/image-article/apollo-8-earthrise/",
        "asset_url": "/images/earthrise-as08-14-2383.jpg",
        "iiif_manifest_url": "https://images-assets.nasa.gov/image/AS08-14-2383/manifest.json",
        "rights_statement_uri": "https://rightsstatements.org/vocab/NoC-US/1.0/",
        "rights_status": "verified_pd",
        "rights_basis": "United States Government Work, 17 U.S.C. 105",
        "schema_org_type": "VisualArtwork",
        "cidoc_type": "E22_Human-Made_Object",
        "darwin_core_basis": None,
        "reference_model": "Smithsonian",
        "collection_summary": "Apollo 8 image record prepared for collection, education, and edition publishing.",
    }
}


def _slug(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace("&", "and")
        .replace("/", "-")
        .replace(" ", "-")
        .replace("--", "-")
    )


def standard_crosswalk(source: dict) -> dict:
    """Build public metadata crosswalk across requested standards."""

    return {
        "iiif": {
            "manifest": source.get("iiif_manifest_url"),
            "image_service": source.get("asset_url"),
        },
        "cidoc_crm": {
            "entity_type": source.get("cidoc_type") or "E78_Curated_Holding",
            "identified_by": source.get("source_record_id"),
            "current_keeper": source.get("source_institution"),
        },
        "darwin_core": {
            "basisOfRecord": source.get("darwin_core_basis") or "HumanObservation",
            "associatedMedia": source.get("asset_url"),
        },
        "schema_org": {
            "@type": source.get("schema_org_type") or "CreativeWork",
            "name": source.get("title"),
            "isBasedOn": source.get("source_url"),
        },
        "rightsstatements_org": {
            "rights_statement_uri": source.get("rights_statement_uri"),
            "rights_status": source.get("rights_status"),
            "rights_basis": source.get("rights_basis"),
        },
        "openapi": {
            "operationId": "generateCommerceRuntimeV2",
            "request_model": "CollectionFactoryInput",
            "response_model": "CommerceRuntimeV2",
        },
    }


def build_collection_factory(source: dict) -> dict:
    """Normalize a source-backed collection into a commerce-ready collection record."""

    collection = {
        "runtime_version": COMMERCE_RUNTIME_V2,
        "factory": "collection_factory",
        "slug": source["slug"],
        "title": source["title"],
        "short_title": source.get("short_title") or source["title"],
        "source_institution": source["source_institution"],
        "source_record_id": source["source_record_id"],
        "source_url": source["source_url"],
        "asset_url": source["asset_url"],
        "rights_status": source["rights_status"],
        "rights_statement_uri": source["rights_statement_uri"],
        "summary": source.get("collection_summary") or source["title"],
        "reference_standards": list(REFERENCE_STANDARDS),
        "reference_models": [source.get("reference_model") or "Europeana", "Rijksmuseum", "Smithsonian"],
        "metadata_crosswalk": standard_crosswalk(source),
    }
    collection["collection_hash"] = stable_json_hash(collection)
    return collection


def build_product_factory(collection: dict) -> list[dict]:
    """Generate supported products from one collection record."""

    products = []
    for product_type in PRODUCT_TYPES:
        spec = PRODUCT_SPECS[product_type]
        product = {
            "runtime_version": COMMERCE_RUNTIME_V2,
            "factory": "product_factory",
            "collection_slug": collection["slug"],
            "product_slug": f"{collection['slug']}-{product_type.replace('_', '-')}",
            "product_type": product_type,
            "product_label": PRODUCT_TYPE_LABELS[product_type],
            "title": f"{collection['short_title']} {PRODUCT_TYPE_LABELS[product_type]}",
            "source_record_id": collection["source_record_id"],
            "asset_url": collection["asset_url"],
            "rights_statement_uri": collection["rights_statement_uri"],
            "rights_status": collection["rights_status"],
            "surface": spec["surface"],
            "variant": spec["variant"],
            "requires_shipping": spec["requires_shipping"],
            "schema_org": {
                "@type": "Product",
                "name": f"{collection['short_title']} {PRODUCT_TYPE_LABELS[product_type]}",
                "isBasedOn": collection["source_url"],
                "category": PRODUCT_TYPE_LABELS[product_type],
            },
            "standards": collection["metadata_crosswalk"],
            "provider_targets": list(PROVIDER_NAMES),
        }
        product["product_hash"] = stable_json_hash(product)
        products.append(product)
    return products


def _load_provider_builder(provider: str):
    if provider == "gelato":
        from services.product.provider.gelato import build_gelato_payload

        return build_gelato_payload
    if provider == "printful":
        from services.product.provider.printful import build_printful_payload

        return build_printful_payload
    if provider == "printify":
        from services.product.provider.printify import build_printify_payload

        return build_printify_payload
    raise ValueError(f"Unsupported provider: {provider}")


def build_pod_payload(product: dict, collection: dict, provider: str) -> dict:
    """Translate one generated product into one provider POD payload."""

    builder = _load_provider_builder(provider)
    payload = builder(product, collection)
    payload["payload_hash"] = stable_json_hash(payload)
    return payload


def build_provider_payloads(collection: dict, products: list[dict]) -> dict:
    payloads: dict[str, dict[str, dict]] = {}
    for product in products:
        payloads[product["product_slug"]] = {
            provider: build_pod_payload(product, collection, provider) for provider in PROVIDER_NAMES
        }
    return payloads


def build_commerce_runtime_v2(source: dict | None = None) -> dict:
    """Generate collection -> products -> POD payloads for Commerce Runtime v2."""

    source_record = deepcopy(source or SEED_COLLECTION_SOURCES["earthrise"])
    collection = build_collection_factory(source_record)
    products = build_product_factory(collection)
    runtime = {
        "runtime_version": COMMERCE_RUNTIME_V2,
        "reference_standards": list(REFERENCE_STANDARDS),
        "reference_models": list(REFERENCE_MODELS) + ["Printify"],
        "collection": collection,
        "products": products,
        "pod_payloads": build_provider_payloads(collection, products),
        "summary": {
            "collections": 1,
            "products": len(products),
            "providers": len(PROVIDER_NAMES),
            "pod_payloads": len(products) * len(PROVIDER_NAMES),
        },
    }
    runtime["runtime_hash"] = stable_json_hash(runtime)
    return runtime
