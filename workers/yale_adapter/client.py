"""Yale LUX Linked Art client helpers for Sprint 1.

Sprint 1 is intentionally read-only: it fetches LUX JSON-LD, extracts Linked Art
rights evidence, derives or discovers IIIF Presentation v3 manifests, and parses
manifest image services. It does not write to the NC store.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import httpx

from .config import settings

YCBA_SOURCE_SLUG = "ycba"
YUAG_SOURCE_SLUG = "yuag"

YCBA_LABEL = "Yale Center for British Art"
YUAG_LABEL = "Yale University Art Gallery"

CC0_URI = "https://creativecommons.org/publicdomain/zero/1.0/"
NOC_US_URI = "http://rightsstatements.org/vocab/NoC-US/1.0/"

ALLOWED_RIGHTS_URIS = frozenset({CC0_URI, NOC_US_URI})
INSTITUTION_LABELS = {
    YCBA_SOURCE_SLUG: YCBA_LABEL,
    YUAG_SOURCE_SLUG: YUAG_LABEL,
}


@dataclass(frozen=True)
class YaleRightsEvidence:
    """Extracted Sprint 1 rights decision data."""

    decision: str
    rights_statement_uri: str | None
    rights_basis: str
    source_slug: str | None
    rights_policy_id: str = "yale_rights_matrix_v1"

    @property
    def allowed(self) -> bool:
        return self.decision == "ALLOWED"


@dataclass(frozen=True)
class YaleManifestCandidate:
    """Manifest URL plus provenance for the derivation/discovery path."""

    url: str
    source_slug: str
    object_id: str
    source: str


def _base_url() -> str:
    return settings.yale_lux_base_url.rstrip("/")


def _manifest_base_url() -> str:
    return settings.yale_manifest_base_url.rstrip("/")


def _clean(value: Any) -> str:
    return str(value).strip()


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _label(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("_label", "label", "content", "name"):
            text = _clean(value.get(key, ""))
            if text:
                return text
    return ""


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in params.items()
        if value is not None and value != ""
    }
    return dict(sorted(cleaned.items()))


def build_data_url(entity_type: str, identifier: str) -> str:
    """Build a concrete LUX `/data/...` URL."""
    cleaned_entity = entity_type.strip().strip("/")
    cleaned_identifier = identifier.strip().strip("/")
    if not cleaned_entity:
        raise ValueError("missing_entity_type")
    if not cleaned_identifier:
        raise ValueError("missing_identifier")
    if cleaned_identifier.startswith("http"):
        return cleaned_identifier
    return f"{_base_url()}/data/{cleaned_entity}/{cleaned_identifier}"


def build_search_url(entity_type: str = "item") -> str:
    """Build a LUX search API URL for an entity type."""
    cleaned = entity_type.strip().strip("/")
    if not cleaned:
        raise ValueError("missing_entity_type")
    return f"{_base_url()}/api/search/{cleaned}"


def build_manifest_url(source_slug: str, object_id: int | str, *, version: int = 3) -> str:
    """Build a Yale IIIF Presentation manifest URL."""
    slug = source_slug.strip().lower()
    if slug not in INSTITUTION_LABELS:
        raise ValueError("unsupported_yale_source")
    cleaned_id = _clean(object_id)
    if not cleaned_id:
        raise ValueError("missing_object_id")
    if version == 3:
        return f"{_manifest_base_url()}/{slug}/obj/{cleaned_id}"
    if version == 2:
        return f"{_manifest_base_url()}/v2/{slug}/obj/{cleaned_id}"
    raise ValueError("unsupported_iiif_version")


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
    headers = {"User-Agent": settings.yale_user_agent}
    request_params = canonical_request_params(params or {})
    request_params_or_none = request_params or None

    if http_client is not None:
        response = await http_client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(timeout=settings.yale_fetch_timeout_seconds) as client:
        response = await client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()


async def fetch_env(*, http_client: httpx.AsyncClient | None = None) -> dict[str, Any]:
    """Fetch the public LUX frontend environment config."""
    return await _get_json("/env", http_client=http_client)


async def fetch_advanced_search_config(
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch LUX advanced-search configuration."""
    return await _get_json("/api/advanced-search-config", http_client=http_client)


async def fetch_data_uri(
    uri: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one concrete LUX JSON-LD record."""
    cleaned = uri.strip()
    if not cleaned:
        raise ValueError("missing_data_uri")
    if "/view/" in cleaned:
        raise ValueError("view_routes_are_not_data_uris")
    return await _get_json(cleaned, http_client=http_client)


async def fetch_object(
    identifier_or_uri: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch a LUX object by UUID-like identifier or full data URI."""
    return await fetch_data_uri(
        build_data_url("object", identifier_or_uri),
        http_client=http_client,
    )


async def search_items(
    *,
    responsible_unit: str,
    page: int = 1,
    page_length: int | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search LUX item records by responsible unit name."""
    if page < 1:
        raise ValueError("invalid_page")
    limit = page_length or settings.yale_page_length
    if limit < 1:
        raise ValueError("invalid_page_length")
    unit = responsible_unit.strip()
    if not unit:
        raise ValueError("missing_responsible_unit")
    query = f'{{"AND":[{{"responsibleUnits":{{"name":"{unit}"}}}}]}}'
    return await _get_json(
        build_search_url("item"),
        params={"q": query, "page": page, "pageLength": limit},
        http_client=http_client,
    )


async def search_ycba_items(
    *,
    page: int = 1,
    page_length: int | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search YCBA item records."""
    return await search_items(
        responsible_unit=YCBA_LABEL,
        page=page,
        page_length=page_length,
        http_client=http_client,
    )


async def search_yuag_items(
    *,
    page: int = 1,
    page_length: int | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search YUAG item records."""
    return await search_items(
        responsible_unit=YUAG_LABEL,
        page=page,
        page_length=page_length,
        http_client=http_client,
    )


async def fetch_manifest(
    manifest_or_record: str | dict[str, Any],
    *,
    source_slug: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch a Yale IIIF manifest by URL or by a LUX record."""
    if isinstance(manifest_or_record, dict):
        candidate = derive_manifest_candidate(manifest_or_record, source_slug=source_slug)
        if candidate is None:
            raise ValueError("no_iiif_manifest")
        url = candidate.url
    else:
        url = manifest_or_record.strip()
        if not url:
            raise ValueError("missing_manifest_url")
    return await _get_json(url, http_client=http_client)


def extract_record_id(record: dict[str, Any]) -> str:
    """Return the LUX record URI from a Linked Art record."""
    return _clean(record.get("id", ""))


def detect_source_slug(record: dict[str, Any]) -> str | None:
    """Detect YCBA/YUAG from member fields, labels, IDs, and source URLs."""
    haystack_parts = [extract_record_id(record)]
    for key in ("member_of", "part_of", "classified_as"):
        for entry in _as_list(record.get(key)):
            if isinstance(entry, dict):
                haystack_parts.extend(
                    _clean(entry.get(subkey, ""))
                    for subkey in ("id", "_label", "label", "content")
                )
            else:
                haystack_parts.append(_clean(entry))
    haystack = " ".join(part for part in haystack_parts if part).lower()

    if "ycba" in haystack or "yale center for british art" in haystack:
        return YCBA_SOURCE_SLUG
    if "yuag" in haystack or "yale university art gallery" in haystack:
        return YUAG_SOURCE_SLUG
    return None


def extract_subject_to_uris(record: dict[str, Any]) -> list[str]:
    """Extract Linked Art `subject_to[].id` rights URIs in source order."""
    uris: list[str] = []
    for entry in _as_list(record.get("subject_to")):
        if not isinstance(entry, dict):
            continue
        uri = _clean(entry.get("id", ""))
        if uri:
            uris.append(uri)
    return uris


def extract_rights(record: dict[str, Any]) -> YaleRightsEvidence:
    """Classify Sprint 1 Yale rights evidence from Linked Art `subject_to`."""
    if not isinstance(record, dict) or "subject_to" not in record:
        return YaleRightsEvidence("BLOCKED", None, "missing_subject_to", None)

    rights_uris = extract_subject_to_uris(record)
    if not rights_uris:
        return YaleRightsEvidence(
            "BLOCKED",
            None,
            "no_rights_statement",
            detect_source_slug(record),
        )

    matched = next((uri for uri in rights_uris if uri in ALLOWED_RIGHTS_URIS), None)
    if matched is None:
        return YaleRightsEvidence(
            "BLOCKED",
            rights_uris[0],
            "rights_not_allowed",
            detect_source_slug(record),
        )

    source_slug = detect_source_slug(record)
    if matched == CC0_URI:
        return YaleRightsEvidence("ALLOWED", matched, "ycba_cc0", source_slug)
    return YaleRightsEvidence("ALLOWED", matched, "yuag_noc_us", source_slug)


def has_representation(record: dict[str, Any]) -> bool:
    """Return true when the record has at least one Linked Art representation."""
    return bool(_as_list(record.get("representation")))


def extract_object_id(record: dict[str, Any]) -> str | None:
    """Extract a Yale numeric object ID from common LUX/Linked Art fields."""
    for key in ("object_id", "ycba_object_id", "yuag_object_id"):
        cleaned = _clean(record.get(key, ""))
        if cleaned and cleaned.isdigit():
            return cleaned

    for entry in _as_list(record.get("identified_by")):
        if not isinstance(entry, dict):
            continue
        label = " ".join(
            _clean(entry.get(key, ""))
            for key in ("type", "_label", "label", "classified_as")
        ).lower()
        content = _clean(entry.get("content", ""))
        if content.isdigit() and ("object" in label or "lux" in label):
            return content
        if _clean(entry.get("id", "")).rstrip("/").split("/")[-1].isdigit():
            return _clean(entry.get("id", "")).rstrip("/").split("/")[-1]

    for entry in _as_list(record.get("representation")):
        if not isinstance(entry, dict):
            continue
        candidate = _clean(entry.get("id", "")).rstrip("/").split("/")[-1]
        if candidate.isdigit():
            return candidate

    return None


def _find_manifest_in_node(node: Any) -> str | None:
    if isinstance(node, dict):
        node_type = _clean(node.get("type", "")).lower()
        node_id = _clean(node.get("id", ""))
        node_label = _label(node).lower()
        if node_id and (
            "manifest" in node_id.lower()
            or "iiif" in node_id.lower()
            or "manifest" in node_label
            or "iiif" in node_label
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
    """Return a source IIIF manifest URL discovered in the LUX record."""
    for key in ("subject_of", "representation", "digitally_shown_by", "digitally_carried_by"):
        found = _find_manifest_in_node(record.get(key))
        if found:
            return found
    return None


def derive_manifest_candidate(
    record: dict[str, Any],
    *,
    source_slug: str | None = None,
) -> YaleManifestCandidate | None:
    """Discover or derive the v3 IIIF manifest URL for a LUX record."""
    discovered = extract_manifest_url(record)
    slug = source_slug or detect_source_slug(record)
    object_id = extract_object_id(record)

    if discovered and slug and object_id:
        return YaleManifestCandidate(discovered, slug, object_id, "record")
    if discovered and slug:
        return YaleManifestCandidate(discovered, slug, "", "record")
    if slug and object_id:
        return YaleManifestCandidate(
            build_manifest_url(slug, object_id),
            slug,
            object_id,
            "derived",
        )
    return None


def extract_manifest_rights(manifest: dict[str, Any]) -> str | None:
    """Extract IIIF Presentation v3 manifest rights URI."""
    rights = _clean(manifest.get("rights", ""))
    return rights or None


def extract_iiif_image_services(manifest: dict[str, Any]) -> list[str]:
    """Extract IIIF Image API service IDs from a Presentation v3 manifest."""
    services: list[str] = []
    canvases = _as_list(manifest.get("items"))
    for canvas in canvases:
        if not isinstance(canvas, dict):
            continue
        for annotation_page in _as_list(canvas.get("items")):
            if not isinstance(annotation_page, dict):
                continue
            for annotation in _as_list(annotation_page.get("items")):
                if not isinstance(annotation, dict):
                    continue
                body = annotation.get("body")
                bodies = body if isinstance(body, list) else [body]
                for body_entry in bodies:
                    if not isinstance(body_entry, dict):
                        continue
                    for service in _as_list(body_entry.get("service")):
                        if not isinstance(service, dict):
                            continue
                        service_id = _clean(service.get("id", ""))
                        if service_id:
                            services.append(service_id.rstrip("/"))
    return list(dict.fromkeys(services))


def build_iiif_image_url(
    service_id: str,
    *,
    size: str = "!1024,1024",
) -> str:
    """Build a IIIF Image API URL from a service base."""
    cleaned = service_id.strip().rstrip("/")
    if not cleaned:
        raise ValueError("missing_iiif_service")
    cleaned_size = size.strip() or "!1024,1024"
    return f"{cleaned}/full/{cleaned_size}/0/default.jpg"


def extract_object_uris_from_search(response: dict[str, Any]) -> list[str]:
    """Extract LUX object URIs from common LUX search response shapes."""
    candidates = response.get("orderedItems")
    if not isinstance(candidates, list):
        candidates = response.get("data")
    if not isinstance(candidates, list):
        candidates = response.get("items")
    if not isinstance(candidates, list):
        return []

    uris: list[str] = []
    for item in candidates:
        if isinstance(item, str):
            uri = item.strip()
        elif isinstance(item, dict):
            uri = _clean(item.get("id") or item.get("@id") or item.get("uri") or "")
        else:
            uri = ""
        if uri:
            uris.append(uri)
    return uris

