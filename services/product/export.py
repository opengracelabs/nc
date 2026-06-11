"""Publication snapshot helpers for the manual product runtime."""

import hashlib
import json

from .catalog import PRODUCT_RUNTIME_VERSION
from .rights_gate import verify_candidate_gates


def stable_json_hash(value: dict) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def build_publication_snapshot(candidate: dict, template: dict) -> dict:
    gates = verify_candidate_gates(candidate, template)
    snapshot = {
        "runtime_version": PRODUCT_RUNTIME_VERSION,
        "candidate_key": candidate["candidate_key"],
        "title": candidate["title"],
        "template_slug": template["slug"],
        "manual_provider_only": True,
        "assembled_attribution": candidate.get("assembled_attribution") or [],
        "gate_result": gates,
    }
    return {"snapshot": snapshot, "snapshot_sha256": stable_json_hash(snapshot)}


def build_product_snapshot_export(publication: dict) -> dict:
    snapshot = publication.get("snapshot") or {}
    candidate_key = snapshot.get("candidate_key") or "product-publication"
    return {
        "filename": f"{candidate_key}-snapshot.json",
        "media_type": "application/json",
        "snapshot": snapshot,
        "snapshot_sha256": stable_json_hash(snapshot),
    }
