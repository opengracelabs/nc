"""Gallica OAI/DC and IIIF normalization for substrate intake."""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .client import build_iiif_image_url, extract_arks_from_xml, normalize_ark
from .rights import classify_rights

_TAG_RE_TEMPLATE = r"<(?:[A-Za-z0-9_]+:)?{tag}[^>]*>(.*?)</(?:[A-Za-z0-9_]+:)?{tag}>"
_TAG_RE_FLAGS = re.DOTALL | re.IGNORECASE


def _tag_values(xml_text: str, tag: str) -> list[str]:
    pattern = re.compile(_TAG_RE_TEMPLATE.format(tag=re.escape(tag)), _TAG_RE_FLAGS)
    values = []
    for match in pattern.finditer(xml_text):
        value = re.sub(r"<[^>]+>", " ", match.group(1))
        compact = " ".join(value.split())
        if compact:
            values.append(compact)
    return values


def _first(values: list[str]) -> str | None:
    return values[0] if values else None


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash a raw Gallica payload for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def extract_record_id(raw: dict[str, Any]) -> str | None:
    """Extract a stable Gallica record identifier from raw adapter payload."""
    explicit = raw.get("ark") or raw.get("record_id")
    if explicit:
        return normalize_ark(str(explicit))

    xml_text = str(raw.get("oai_record_xml") or "")
    arks = extract_arks_from_xml(xml_text)
    return arks[0] if arks else None


def _iiif_rights(raw: dict[str, Any]) -> str | None:
    manifest = raw.get("iiif_manifest")
    if isinstance(manifest, dict):
        rights = manifest.get("rights") or manifest.get("license")
        if rights:
            return str(rights)
    return None


def _dc_rights(xml_text: str) -> str | None:
    return _first(_tag_values(xml_text, "rights"))


def _source_url(record_id: str | None, raw: dict[str, Any], xml_text: str) -> str | None:
    explicit = raw.get("source_url")
    if explicit:
        return str(explicit)
    identifiers = _tag_values(xml_text, "identifier")
    for identifier in identifiers:
        if "gallica.bnf.fr" in identifier:
            return identifier
    if record_id:
        return f"https://gallica.bnf.fr/{record_id}"
    return None


def _representative_media_url(record_id: str | None, raw: dict[str, Any]) -> str | None:
    explicit = raw.get("representative_media_url")
    if explicit:
        return str(explicit)
    if not record_id:
        return None
    page = raw.get("selected_page") or raw.get("page") or 1
    region = str(raw.get("iiif_region") or "full")
    return build_iiif_image_url(record_id, page, region=region)


def _iiif_image_service_url(record_id: str | None, raw: dict[str, Any]) -> str | None:
    explicit = raw.get("iiif_image_service_url")
    if explicit:
        return str(explicit)
    if not record_id:
        return None
    page = raw.get("selected_page") or raw.get("page") or 1
    return f"https://gallica.bnf.fr/iiif/{record_id}/f{page}"


def normalize_edm_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize Gallica OAI/DC, IIIF, and rights fields for Sprint 2."""
    xml_text = str(raw.get("oai_record_xml") or "")
    record_id = extract_record_id(raw)
    rights_raw = _iiif_rights(raw) or _dc_rights(xml_text)
    rights = classify_rights(rights_raw)
    iiif_info = raw.get("iiif_info") if isinstance(raw.get("iiif_info"), dict) else {}

    return {
        "record_id": record_id,
        "title": _first(_tag_values(xml_text, "title")) or raw.get("title"),
        "description": _first(_tag_values(xml_text, "description")) or raw.get("description"),
        "date": _first(_tag_values(xml_text, "date")) or raw.get("date"),
        "creator": _first(_tag_values(xml_text, "creator")) or raw.get("creator"),
        "subject_terms": _tag_values(xml_text, "subject"),
        "rights_uri": rights["rights_statement_uri"],
        "provider": raw.get("provider") or "Bibliotheque nationale de France",
        "dataProvider": raw.get("dataProvider") or raw.get("data_provider") or "Gallica",
        "edm_type": _first(_tag_values(xml_text, "type")) or raw.get("edm_type"),
        "source_url": _source_url(record_id, raw, xml_text),
        "representative_media_url": _representative_media_url(record_id, raw),
        "preview_urls": [str(url) for url in raw.get("preview_urls", [])],
        "width_px": raw.get("width_px") or iiif_info.get("width"),
        "height_px": raw.get("height_px") or iiif_info.get("height"),
        "raw_payload_hash": canonical_json_hash(raw),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "gallica_rights_raw": rights_raw,
        "gallica_rights_basis": rights["rights_basis"],
        "gallica_rights_source": rights["rights_source"],
        "iiif_manifest_url": raw.get("iiif_manifest_url"),
        "iiif_image_service_url": _iiif_image_service_url(record_id, raw),
        "pagination_pages": raw.get("pagination_pages"),
        "selected_page": raw.get("selected_page") or raw.get("page") or 1,
        "iiif_region": raw.get("iiif_region") or "full",
    }


def mandatory_field_warnings(normalized: dict[str, Any]) -> list[str]:
    """Return warnings for fields required by the Gallica substrate gate."""
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
