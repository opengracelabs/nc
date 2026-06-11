"""Audit helpers for NC-COMMERCE-002 product activation."""

from .export import stable_json_hash


def build_audit_event(
    *,
    entity_type: str,
    entity_id: str,
    event_type: str,
    actor: str,
    previous_state: dict | None = None,
    new_state: dict | None = None,
    event: dict | None = None,
) -> dict:
    body = {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "event_type": event_type,
        "actor": actor,
        "previous_state": previous_state or {},
        "new_state": new_state or {},
        "event": event or {},
    }
    body["event_sha256"] = stable_json_hash(body)
    return body
