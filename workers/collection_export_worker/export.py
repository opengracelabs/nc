"""Deterministic collection export manifests."""
from __future__ import annotations

import hashlib
import json
from typing import Any

_EXPORTER_ID = "collection_export_worker:v0.4.0"


def _json_default(value: Any) -> str:
    return str(value)


def _sort_key(item: dict[str, Any]) -> tuple[int, str]:
    sequence = item.get("sequence")
    if sequence is None:
        sequence = 999_999
    return int(sequence), str(item.get("asset_id") or item.get("id") or "")


def build_collection_export_manifest(
    collection: dict[str, Any],
    assets: list[dict[str, Any]],
    places: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a stable public export manifest for a governed collection."""
    ordered_assets = sorted(assets, key=_sort_key)
    manifest_assets = [
        {
            "asset_id": str(asset.get("asset_id") or asset["id"]),
            "sequence": asset.get("sequence"),
            "role": asset.get("role", "primary"),
            "title": asset.get("title"),
            "caption": asset.get("caption"),
            "credit_line": asset.get("credit_line"),
            "rights_status": asset.get("rights_status"),
            "rights_source_url": asset.get("rights_source_url"),
            "raw_path": asset.get("raw_path"),
            "normalized_path": asset.get("normalized_path"),
            "checksum_sha256": asset.get("checksum_sha256"),
            "source_url": asset.get("source_url"),
            "bhl_page_id": asset.get("bhl_page_id"),
        }
        for asset in ordered_assets
    ]
    manifest = {
        "collection_id": str(collection["id"]),
        "slug": collection["slug"],
        "title": collection["title"],
        "collection_type": collection["collection_type"],
        "status": collection["status"],
        "summary": collection.get("summary"),
        "places": [
            {
                "place_id": str(place.get("place_id") or place["id"]),
                "name": place.get("name"),
                "role": place.get("role", "primary"),
            }
            for place in sorted(places or [], key=lambda p: str(p.get("place_id") or p.get("id")))
        ],
        "assets": manifest_assets,
        "asset_count": len(manifest_assets),
        "provenance": {
            "prov:wasGeneratedBy": _EXPORTER_ID,
            "export_format": "collection_manifest_v1",
        },
    }
    encoded = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
        default=_json_default,
    ).encode("utf-8")
    manifest["checksum_sha256"] = hashlib.sha256(encoded).hexdigest()
    return manifest
