"""Europeana EDM normalization for substrate intake."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .rights import classify_rights, normalize_rights_uri


def _first(value: Any) -> Any:
    if isinstance(value, list):
        return _first(value[0]) if value else None
    if isinstance(value, dict):
        for key in ("def", "en", "nl"):
            if key in value:
                return _first(value[key])
        return _first(next(iter(value.values()))) if value else None
    return value


def _list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, dict):
        value = _first(value)
    if isinstance(value, list):
        return value
    return [value]


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash a raw Europeana payload for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _record_object(raw: dict[str, Any]) -> dict[str, Any]:
    obj = raw.get("object")
    if isinstance(obj, dict):
        return obj
    return raw


def _first_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, list):
        return next((item for item in value if isinstance(item, dict)), {})
    if isinstance(value, dict):
        return value
    return {}


def _provider_proxy(item: dict[str, Any]) -> dict[str, Any]:
    proxies = item.get("proxies")
    if not isinstance(proxies, list):
        return {}
    for proxy in proxies:
        if isinstance(proxy, dict) and proxy.get("europeanaProxy") is False:
            return proxy
    return _first_dict(proxies)


def _provider_aggregation(item: dict[str, Any]) -> dict[str, Any]:
    return _first_dict(item.get("aggregations"))


def _europeana_aggregation(item: dict[str, Any]) -> dict[str, Any]:
    return _first_dict(item.get("europeanaAggregation"))


def _image_web_resource(aggregation: dict[str, Any]) -> dict[str, Any]:
    web_resources = aggregation.get("webResources")
    if not isinstance(web_resources, list):
        return {}
    for resource in web_resources:
        if not isinstance(resource, dict):
            continue
        mime_type = str(resource.get("ebucoreHasMimeType") or "").lower()
        if mime_type.startswith("image/"):
            return resource
    return _first_dict(web_resources)


def _organization_label(item: dict[str, Any], organization_uri: Any) -> str | None:
    uri = _first(organization_uri)
    organizations = item.get("organizations")
    if isinstance(organizations, list):
        for organization in organizations:
            if isinstance(organization, dict) and organization.get("about") == uri:
                return _first(organization.get("prefLabel"))
    return str(uri) if uri else None


def extract_record_id(raw: dict[str, Any]) -> str | None:
    """Extract the stable Europeana record identifier."""
    item = _record_object(raw)
    value = item.get("id") or item.get("about") or raw.get("id")
    return str(value).strip() if value else None


def normalize_edm_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize EDM fields used by rights, technical metadata, and substrate gates."""
    item = _record_object(raw)
    provider_proxy = _provider_proxy(item)
    provider_aggregation = _provider_aggregation(item)
    europeana_aggregation = _europeana_aggregation(item)
    image_resource = _image_web_resource(provider_aggregation)

    rights_uri = normalize_rights_uri(
        _first(
            item.get("rights")
            or item.get("edmRights")
            or provider_aggregation.get("edmRights")
            or europeana_aggregation.get("edmRights")
            or image_resource.get("webResourceEdmRights")
        )
    )
    rights = classify_rights(rights_uri)
    representative_url = _first(
        item.get("isShownBy")
        or item.get("object")
        or provider_aggregation.get("edmIsShownBy")
        or provider_aggregation.get("edmObject")
        or image_resource.get("about")
    )
    provider = _first(item.get("provider")) or _organization_label(
        item, provider_aggregation.get("edmProvider")
    )
    data_provider = _first(item.get("dataProvider")) or _organization_label(
        item, provider_aggregation.get("edmDataProvider")
    )

    return {
        "record_id": extract_record_id(raw),
        "title": _first(item.get("title") or item.get("dcTitle") or provider_proxy.get("dcTitle")),
        "description": _first(
            item.get("description")
            or item.get("dcDescription")
            or provider_proxy.get("dcDescription")
            or image_resource.get("textAttributionSnippet")
        ),
        "date": _first(
            item.get("date")
            or item.get("dcDate")
            or provider_proxy.get("dctermsCreated")
            or provider_proxy.get("year")
        ),
        "creator": _first(
            item.get("creator") or item.get("dcCreator") or provider_proxy.get("dcCreator")
        ),
        "subject_terms": _list(
            item.get("subject") or item.get("dcSubject") or provider_proxy.get("dcSubject")
        ),
        "rights_uri": rights_uri,
        "provider": provider,
        "dataProvider": data_provider,
        "edm_type": _first(
            item.get("type") or item.get("edmType") or provider_proxy.get("edmType")
        ),
        "source_url": _first(
            item.get("isShownAt")
            or item.get("guid")
            or provider_aggregation.get("edmIsShownAt")
            or europeana_aggregation.get("edmLandingPage")
        ),
        "representative_media_url": representative_url,
        "preview_urls": _list(
            europeana_aggregation.get("edmPreview") or item.get("edmPreview") or item.get("preview")
        ),
        "width_px": _first(
            item.get("width") or item.get("width_px") or image_resource.get("ebucoreWidth")
        ),
        "height_px": _first(
            item.get("height") or item.get("height_px") or image_resource.get("ebucoreHeight")
        ),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "raw_payload_hash": canonical_json_hash(raw),
    }


def mandatory_field_warnings(normalized: dict[str, Any]) -> list[str]:
    """Return warnings for fields required by the Europeana substrate gate."""
    warnings: list[str] = []
    if not normalized.get("record_id"):
        warnings.append("missing_record_id")
    if not normalized.get("title"):
        warnings.append("missing_title")
    if not normalized.get("rights_uri"):
        warnings.append("missing_rights_uri")
    if not normalized.get("description"):
        warnings.append("missing_description")
    if not normalized.get("date"):
        warnings.append("missing_date")
    if not normalized.get("provider"):
        warnings.append("missing_provider")
    if not normalized.get("dataProvider"):
        warnings.append("missing_data_provider")
    return warnings
