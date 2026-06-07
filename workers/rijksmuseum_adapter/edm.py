"""Rijksmuseum OAI-PMH EDM normalization."""
from __future__ import annotations

import hashlib
import json
from typing import Any
from xml.etree import ElementTree as ET

from .rights import classify_rights, normalize_rights_uri

OAI_NS = "http://www.openarchives.org/OAI/2.0/"
RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
DC_NS = "http://purl.org/dc/elements/1.1/"
DCTERMS_NS = "http://purl.org/dc/terms/"
EDM_NS = "http://www.europeana.eu/schemas/edm/"
ORE_NS = "http://www.openarchives.org/ore/terms/"
EBCORE_NS = "http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#"

NS = {
    "oai": OAI_NS,
    "rdf": RDF_NS,
    "dc": DC_NS,
    "dcterms": DCTERMS_NS,
    "edm": EDM_NS,
    "ore": ORE_NS,
    "ebucore": EBCORE_NS,
}


def canonical_xml_hash(payload: str) -> str:
    """Hash raw OAI XML exactly as fetched for replay checks."""
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash a normalized search/OAI payload for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _text(element: ET.Element | None) -> str | None:
    if element is None or element.text is None:
        return None
    value = element.text.strip()
    return value or None


def _resource(element: ET.Element | None) -> str | None:
    if element is None:
        return None
    value = element.attrib.get(f"{{{RDF_NS}}}resource") or element.attrib.get("resource")
    if value:
        return value.strip()
    return _text(element)


def _first_text(root: ET.Element, paths: tuple[str, ...]) -> str | None:
    for path in paths:
        value = _text(root.find(path, NS))
        if value:
            return value
    return None


def _all_text(root: ET.Element, paths: tuple[str, ...]) -> list[str]:
    values: list[str] = []
    for path in paths:
        for element in root.findall(path, NS):
            value = _text(element)
            if value and value not in values:
                values.append(value)
    return values


def _first_resource(root: ET.Element, paths: tuple[str, ...]) -> str | None:
    for path in paths:
        value = _resource(root.find(path, NS))
        if value:
            return value
    return None


def _all_resources(root: ET.Element, paths: tuple[str, ...]) -> list[str]:
    values: list[str] = []
    for path in paths:
        for element in root.findall(path, NS):
            value = _resource(element)
            if value and value not in values:
                values.append(value)
    return values


def _first_int(root: ET.Element, paths: tuple[str, ...]) -> int | None:
    for path in paths:
        value = _text(root.find(path, NS))
        if value is None:
            continue
        try:
            return int(value)
        except ValueError:
            continue
    return None


def _record_root(oai_xml: str) -> ET.Element:
    try:
        root = ET.fromstring(oai_xml)  # noqa: S314
    except ET.ParseError as exc:
        raise ValueError("invalid_oai_xml") from exc
    error = root.find(".//oai:error", NS)
    if error is not None:
        code = error.attrib.get("code") or "unknown"
        raise ValueError(f"oai_error:{code}")
    return root


def extract_oai_identifier(oai_xml: str) -> str | None:
    """Extract the OAI-PMH record identifier from a GetRecord/ListRecords payload."""
    root = _record_root(oai_xml)
    return _first_text(root, (".//oai:header/oai:identifier",))


def first_search_identifier(search_response: dict[str, Any]) -> str | None:
    """Return the first Rijksmuseum Search LOD ID suitable for OAI GetRecord."""
    for item in search_response.get("orderedItems", []):
        if isinstance(item, dict) and item.get("id"):
            return str(item["id"])
    return None


def _search_item(search_response: dict[str, Any], identifier: str | None) -> dict[str, Any]:
    for item in search_response.get("orderedItems", []):
        if isinstance(item, dict) and item.get("id") == identifier:
            return item
    return {}


def normalize_oai_edm_record(
    oai_xml: str,
    *,
    search_item: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize Rijksmuseum OAI EDM into the shared substrate contract."""
    root = _record_root(oai_xml)
    identifier = _first_text(root, (".//oai:header/oai:identifier",))
    provided_cho = root.find(".//edm:ProvidedCHO", NS)
    aggregation = root.find(".//ore:Aggregation", NS)
    web_resource = root.find(".//edm:WebResource", NS)
    source = search_item or {}

    source_id = identifier or _resource(provided_cho) or source.get("id")
    rights_uri = normalize_rights_uri(
        _first_resource(
            root,
            (
                ".//ore:Aggregation/edm:rights",
                ".//edm:WebResource/edm:rights",
                ".//dc:rights",
            ),
        )
    )
    rights = classify_rights(rights_uri)
    title = _first_text(root, (".//edm:ProvidedCHO/dc:title", ".//dc:title")) or source.get("title")
    description = _first_text(
        root,
        (
            ".//edm:ProvidedCHO/dc:description",
            ".//dc:description",
            ".//edm:WebResource/dc:description",
        ),
    ) or source.get("summary")
    date = _first_text(
        root,
        (".//edm:ProvidedCHO/dcterms:created", ".//edm:ProvidedCHO/dc:date", ".//dc:date"),
    ) or source.get("creationDate")

    return {
        "record_id": str(source_id).strip() if source_id else None,
        "title": title,
        "description": description,
        "date": date,
        "creator": _first_text(root, (".//edm:ProvidedCHO/dc:creator", ".//dc:creator"))
        or source.get("creator"),
        "subject_terms": _all_text(root, (".//edm:ProvidedCHO/dc:subject", ".//dc:subject")),
        "rights_uri": rights_uri,
        "provider": _first_text(root, (".//ore:Aggregation/edm:provider",)) or "Rijksmuseum",
        "dataProvider": _first_text(root, (".//ore:Aggregation/edm:dataProvider",))
        or "Rijksmuseum",
        "edm_type": _first_text(root, (".//edm:ProvidedCHO/edm:type", ".//edm:type"))
        or source.get("type"),
        "source_url": _first_resource(root, (".//ore:Aggregation/edm:isShownAt",))
        or _resource(aggregation),
        "representative_media_url": _first_resource(
            root,
            (
                ".//ore:Aggregation/edm:isShownBy",
                ".//ore:Aggregation/edm:object",
                ".//edm:WebResource",
            ),
        )
        or _resource(web_resource),
        "preview_urls": _all_resources(root, (".//ore:Aggregation/edm:preview",)),
        "width_px": _first_int(root, (".//edm:WebResource/ebucore:width",)),
        "height_px": _first_int(root, (".//edm:WebResource/ebucore:height",)),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "raw_payload_hash": canonical_xml_hash(oai_xml),
    }


def normalize_search_getrecord(
    search_response: dict[str, Any],
    oai_xml: str,
) -> dict[str, Any]:
    """Normalize the Search -> OAI GetRecord workflow result."""
    identifier = extract_oai_identifier(oai_xml) or first_search_identifier(search_response)
    return normalize_oai_edm_record(oai_xml, search_item=_search_item(search_response, identifier))


def mandatory_field_warnings(normalized: dict[str, Any]) -> list[str]:
    """Return warnings for fields required by the Rijksmuseum substrate gate."""
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
