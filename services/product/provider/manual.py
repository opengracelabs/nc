"""Manual export provider for NC-PRODUCT-001 Sprint 1."""

from services.product.export import stable_json_hash


def build_manual_export_manifest(publication: dict) -> dict:
    snapshot = publication.get("snapshot") or {}
    manifest = {
        "provider": "manual",
        "publication_id": str(publication.get("id")),
        "publication_version": publication.get("publication_version"),
        "snapshot_sha256": publication.get("snapshot_sha256"),
        "candidate_key": snapshot.get("candidate_key"),
        "title": snapshot.get("title"),
        "attribution": snapshot.get("assembled_attribution") or [],
        "files": [],
    }
    manifest["manifest_sha256"] = stable_json_hash(manifest)
    return manifest


def build_manual_export_package(publication: dict) -> dict:
    manifest = build_manual_export_manifest(publication)
    snapshot = publication.get("snapshot") or {}
    attribution = snapshot.get("assembled_attribution") or []
    package = {
        "provider": "manual",
        "publication_id": str(publication.get("id")),
        "publication_version": publication.get("publication_version"),
        "candidate_key": snapshot.get("candidate_key"),
        "title": snapshot.get("title"),
        "manifest": manifest,
        "files": [
            {
                "path": "snapshot.json",
                "media_type": "application/json",
                "sha256": stable_json_hash(snapshot),
            },
            {
                "path": "attribution.json",
                "media_type": "application/json",
                "sha256": stable_json_hash({"attribution": attribution}),
            },
            {
                "path": "README.txt",
                "media_type": "text/plain",
                "sha256": stable_json_hash(
                    {"readme": "Manual export package for Nature & Culture product publication"}
                ),
            },
        ],
    }
    package["package_sha256"] = stable_json_hash(package)
    return package
