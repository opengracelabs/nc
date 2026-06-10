"""Getty ActivityStreams and Linked Art client helpers for Sprint 1.

Sprint 1 is intentionally read-only: it harvests ActivityStreams pages, resolves
Linked Art object records, filters Open Content CC0 candidates, discovers IIIF
manifests, and extracts IIIF image services. It does not write to the NC store.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import httpx

from .config import RIGHTS_POLICY_ID, SOURCE_SLUG, settings

CC0_URI = "https://creativecommons.org/publicdomain/zero/1.0/"
GETTY_OBJECT_PATH = "/museum/collection/object/"


@dataclass(frozen=True)
class GettyRightsEvidence:
    """Extracted Sprint 1 Getty rights decision data."""

    decision: str
    rights_statement_uri: str | None
    rights_basis: str
    rights_policy_id: str = RIGHTS_POLICY_ID

    @property
    def allowed(self) -> bool:
        return self.decision == "ALLOWED"


@dataclass(frozen=True)
class GettyOpenContentCandidate:
    """Read-only Open Content candidate with IIIF evidence."""

    object_uri: str
    rights_uri: str
    iiif_manifest: str
    iiif_image_service: str
    source_slug: str = SOURCE_SLUG


def _base_url() -> str:
    return settings.getty_collection_base_url.rstrip("/")


def _clean(value: Any) -> str:
    return str(value).strip()


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _id_value(node: dict[str, Any]) -> str:
    return _clean(node.get("id") or node.get("@id") or "")


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in params.items()
        if value is not None and value != ""
    }
    return dict(sorted(cleaned.items()))


def build_activity_stream_page_url(page: int | str) -> str:
    """Build an official Getty ActivityStreams page URL."""
    cleaned = _clean(page).strip("/")
    if not cleaned:
        raise ValueError("missing_activity_stream_page")
    if cleaned.startswith("http"):
        return cleaned
    if not cleaned.isdigit():
        raise ValueError("invalid_activity_stream_page")
    return f"{_base_url()}/activity-stream/page/{cleaned}"


def build_object_url(identifier_or_uri: str) -> str:
    """Build an official Getty Linked Art object URL."""
    cleaned = identifier_or_uri.strip()
    if not cleaned:
        raise ValueError("missing_object_id")
    if cleaned.startswith("http"):
        if GETTY_OBJECT_PATH not in cleaned:
            raise ValueError("not_getty_object_uri")
        return cleaned
    return f"{_base_url()}/object/{cleaned.strip('/')}"


async def _get_json(
    path_or_url: str,
    *,
    params: dict[str, Any] | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    if path_or_url.startswith("http"):
        url = path_or_url
    else:
        url = urljoin(f"{_base_url()}/", path_or_url.lstrip("/"))
    headers = {"User-Agent": settings.getty_user_agent}
    request_params = canonical_request_params(params or {})
    request_params_or_none = request_params or None

    if http_client is not None:
        response = await http_client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(timeout=settings.getty_fetch_timeout_seconds) as client:
        response = await client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()


async def fetch_activity_stream_page(
    page_or_url: int | str = 1,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one Getty ActivityStreams ordered collection page."""
    url = build_activity_stream_page_url(page_or_url)
    return await _get_json(url, http_client=http_client)


async def fetch_linked_art_record(
    identifier_or_uri: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one Getty Linked Art object record by UUID or full URI."""
    url = build_object_url(identifier_or_uri)
    return await _get_json(url, http_client=http_client)


async def fetch_object(
    identifier_or_uri: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one Getty Linked Art object record by UUID or full URI."""
    return await fetch_linked_art_record(identifier_or_uri, http_client=http_client)


async def fetch_iiif_manifest(
    manifest_or_record: str | dict[str, Any],
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch a Getty IIIF manifest by URL or Linked Art record."""
    if isinstance(manifest_or_record, dict):
        url = extract_manifest_url(manifest_or_record)
        if not url:
            raise ValueError("no_iiif_manifest")
    else:
        url = manifest_or_record.strip()
        if not url:
            raise ValueError("missing_manifest_url")
    return await _get_json(url, http_client=http_client)


def next_activity_stream_page(page: dict[str, Any]) -> str | None:
    """Return the next ActivityStreams page URL when present."""
    next_value = page.get("next")
    if isinstance(next_value, str):
        return next_value.strip() or None
    if isinstance(next_value, dict):
        return _id_value(next_value) or None
    return None


def _activity_object_uri(activity: dict[str, Any]) -> str | None:
    obj = activity.get("object")
    if isinstance(obj, str):
        uri = obj.strip()
    elif isinstance(obj, dict):
        uri = _id_value(obj)
    else:
        uri = _id_value(activity)

    if uri and GETTY_OBJECT_PATH in uri:
        return uri
    return None


def extract_activity_record_uris(
    page: dict[str, Any],
    *,
    include_types: tuple[str, ...] = ("Create", "Update"),
) -> list[str]:
    """Extract Getty object URIs from ActivityStreams ordered items."""
    include = {item.lower() for item in include_types}
    uris: list[str] = []
    for item in _as_list(page.get("orderedItems")):
        if not isinstance(item, dict):
            continue
        item_type = _clean(item.get("type", "")).lower()
        if item_type not in include:
            continue
        uri = _activity_object_uri(item)
        if uri:
            uris.append(uri)
    return list(dict.fromkeys(uris))


def extract_rights_uris(record: dict[str, Any]) -> list[str]:
    """Extract Getty Linked Art rights URIs from `referred_to_by[].subject_to[]`."""
    uris: list[str] = []
    for statement in _as_list(record.get("referred_to_by")):
        if not isinstance(statement, dict):
            continue
        for subject_to in _as_list(statement.get("subject_to")):
            if not isinstance(subject_to, dict):
                continue
            direct_uri = _id_value(subject_to)
            if direct_uri:
                uris.append(direct_uri)
            for classification in _as_list(subject_to.get("classified_as")):
                if not isinstance(classification, dict):
                    continue
                classified_uri = _id_value(classification)
                if classified_uri:
                    uris.append(classified_uri)
    return list(dict.fromkeys(uris))


def extract_rights(record: dict[str, Any]) -> GettyRightsEvidence:
    """Classify Sprint 1 Getty Open Content rights evidence."""
    if not isinstance(record, dict) or not record:
        return GettyRightsEvidence("BLOCKED", None, "missing_object")
    if "referred_to_by" not in record:
        return GettyRightsEvidence("BLOCKED", None, "missing_subject_to")

    rights_uris = extract_rights_uris(record)
    if not rights_uris:
        return GettyRightsEvidence("BLOCKED", None, "no_rights_statement")
    if CC0_URI in rights_uris:
        return GettyRightsEvidence("ALLOWED", CC0_URI, "getty_cc0")
    return GettyRightsEvidence("BLOCKED", rights_uris[0], "rights_not_allowed")


def is_open_content_candidate(record: dict[str, Any]) -> bool:
    """Return true only for Getty CC0 Open Content candidate records."""
    return extract_rights(record).allowed


def _find_manifest_in_node(node: Any) -> str | None:
    if isinstance(node, dict):
        node_id = _id_value(node)
        node_type = _clean(node.get("type", "")).lower()
        node_label = _clean(node.get("_label") or node.get("label") or "").lower()
        if node_id and (
            "iiif/manifest" in node_id.lower()
            or "manifest" in node_id.lower()
            or "manifest" in node_label
            or node_type == "manifest"
        ):
            return node_id
        for value in node.values():
            found = _find_manifest_in_node(value)
            if found:
                return found
    elif isinstance(node, list):
        for value in node:
            found = _find_manifest_in_node(value)
            if found:
                return found
    return None


def extract_manifest_url(record: dict[str, Any]) -> str | None:
    """Return a Getty IIIF manifest URL discovered in a Linked Art record."""
    for key in ("subject_of", "representation", "digitally_shown_by", "digitally_carried_by"):
        found = _find_manifest_in_node(record.get(key))
        if found:
            return found
    return None


def extract_iiif_image_services(manifest: dict[str, Any]) -> list[str]:
    """Extract IIIF Image API service IDs from Getty Presentation v2/v3 manifests."""
    services: list[str] = []

    for sequence in _as_list(manifest.get("sequences")):
        if not isinstance(sequence, dict):
            continue
        for canvas in _as_list(sequence.get("canvases")):
            if not isinstance(canvas, dict):
                continue
            for image in _as_list(canvas.get("images")):
                if not isinstance(image, dict):
                    continue
                resource = image.get("resource")
                if not isinstance(resource, dict):
                    continue
                for service in _as_list(resource.get("service")):
                    if not isinstance(service, dict):
                        continue
                    service_id = _id_value(service)
                    if service_id:
                        services.append(service_id.rstrip("/"))

    for canvas in _as_list(manifest.get("items")):
        if not isinstance(canvas, dict):
            continue
        for annotation_page in _as_list(canvas.get("items")):
            if not isinstance(annotation_page, dict):
                continue
            for annotation in _as_list(annotation_page.get("items")):
                if not isinstance(annotation, dict):
                    continue
                for body in _as_list(annotation.get("body")):
                    if not isinstance(body, dict):
                        continue
                    for service in _as_list(body.get("service")):
                        if not isinstance(service, dict):
                            continue
                        service_id = _id_value(service)
                        if service_id:
                            services.append(service_id.rstrip("/"))

    return list(dict.fromkeys(services))


def extract_iiif_image_service(manifest: dict[str, Any]) -> str | None:
    """Return the first deterministic IIIF image service from a manifest."""
    services = extract_iiif_image_services(manifest)
    return services[0] if services else None


def build_open_content_candidate(
    record: dict[str, Any],
    manifest: dict[str, Any],
) -> GettyOpenContentCandidate | None:
    """Build a read-only candidate when rights and IIIF evidence are present."""
    rights = extract_rights(record)
    manifest_url = extract_manifest_url(record)
    image_service = extract_iiif_image_service(manifest)
    object_uri = _id_value(record)
    if not rights.allowed or not manifest_url or not image_service or not object_uri:
        return None
    return GettyOpenContentCandidate(
        object_uri=object_uri,
        rights_uri=rights.rights_statement_uri or "",
        iiif_manifest=manifest_url,
        iiif_image_service=image_service,
    )

