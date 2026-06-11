"""GBIF Darwin Core evidence normalization helpers."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .config import SCHEMA_STANDARD, SOURCE_SLUG

DARWIN_CORE_TAXON_MAPPING = {
    "gbif_taxon_key": "dwc:taxonID",
    "scientific_name": "dwc:scientificName",
    "accepted_scientific_name": "dwc:acceptedNameUsage",
    "taxon_rank": "dwc:taxonRank",
    "kingdom": "dwc:kingdom",
    "phylum": "dwc:phylum",
    "class": "dwc:class",
    "order": "dwc:order",
    "family": "dwc:family",
    "genus": "dwc:genus",
    "species": "dwc:specificEpithet",
}

DARWIN_CORE_OCCURRENCE_MAPPING = {
    "gbif_occurrence_key": "dwc:occurrenceID",
    "gbif_taxon_key": "dwc:taxonID",
    "scientific_name": "dwc:scientificName",
    "basis_of_record": "dwc:basisOfRecord",
    "country_code": "dwc:countryCode",
    "state_province": "dwc:stateProvince",
    "locality": "dwc:locality",
    "decimal_latitude": "dwc:decimalLatitude",
    "decimal_longitude": "dwc:decimalLongitude",
    "coordinate_uncertainty_meters": "dwc:coordinateUncertaintyInMeters",
    "event_date": "dwc:eventDate",
    "recorded_by": "dwc:recordedBy",
    "identified_by": "dwc:identifiedBy",
}


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def canonical_json_hash(payload: Any) -> str:
    """Hash GBIF payloads for replay-stable provenance."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def build_source_url(path: str, identifier: str | int | None) -> str | None:
    """Build a public GBIF source URL for evidence records."""
    if identifier is None or identifier == "":
        return None
    return f"https://www.gbif.org/{path.strip('/')}/{identifier}"


def normalize_taxon_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize one GBIF species/match payload as identity evidence."""
    data = payload if isinstance(payload, dict) else {}
    taxon_key = _string(data.get("usageKey") or data.get("key"))
    accepted_taxon_key = _string(data.get("acceptedUsageKey") or data.get("acceptedKey"))
    evidence = {
        "source_slug": SOURCE_SLUG,
        "schema_standard": SCHEMA_STANDARD,
        "gbif_taxon_key": taxon_key,
        "scientific_name": _string(data.get("scientificName")),
        "canonical_name": _string(data.get("canonicalName")),
        "accepted_taxon_key": accepted_taxon_key or taxon_key,
        "accepted_scientific_name": _string(
            data.get("accepted")
            or data.get("acceptedScientificName")
            or data.get("scientificName")
        ),
        "taxon_rank": _string(data.get("rank")),
        "taxonomic_status": _string(data.get("status")),
        "match_type": _string(data.get("matchType")),
        "confidence": _int(data.get("confidence")),
        "synonym": bool(data.get("synonym")) or _string(data.get("status")) == "SYNONYM",
        "kingdom": _string(data.get("kingdom")),
        "phylum": _string(data.get("phylum")),
        "class": _string(data.get("class")),
        "order": _string(data.get("order")),
        "family": _string(data.get("family")),
        "genus": _string(data.get("genus")),
        "species": _string(data.get("species")),
        "source_url": build_source_url("species", accepted_taxon_key or taxon_key),
        "darwin_core_mapping": DARWIN_CORE_TAXON_MAPPING,
        "raw_payload_hash": canonical_json_hash(data),
    }
    evidence["record_id"] = evidence["accepted_taxon_key"] or evidence["gbif_taxon_key"]
    return evidence


def normalize_occurrence_payload(
    payload: dict[str, Any] | None,
    *,
    rights: dict[str, Any],
) -> dict[str, Any]:
    """Normalize one GBIF occurrence payload as Darwin Core evidence."""
    data = payload if isinstance(payload, dict) else {}
    occurrence_key = _string(data.get("key") or data.get("gbifID"))
    citation = _string(data.get("citation"))
    dataset_key = _string(data.get("datasetKey"))
    doi = _string(data.get("datasetDOI") or data.get("doi"))
    evidence = {
        "source_slug": SOURCE_SLUG,
        "schema_standard": SCHEMA_STANDARD,
        "record_id": occurrence_key,
        "gbif_occurrence_key": occurrence_key,
        "gbif_taxon_key": _string(data.get("taxonKey")),
        "accepted_taxon_key": _string(data.get("acceptedTaxonKey")),
        "scientific_name": _string(data.get("scientificName")),
        "taxon_rank": _string(data.get("taxonRank")),
        "basis_of_record": _string(data.get("basisOfRecord")),
        "dataset_key": dataset_key,
        "dataset_title": _string(data.get("datasetName")),
        "dataset_doi": doi,
        "publishing_org_key": _string(data.get("publishingOrgKey")),
        "publisher": _string(data.get("publisher")),
        "citation": citation,
        "license": _string(data.get("license")),
        "rights_holder": _string(data.get("rightsHolder")),
        "recorded_by": _string(data.get("recordedBy")),
        "identified_by": _string(data.get("identifiedBy")),
        "country_code": _string(data.get("countryCode")),
        "state_province": _string(data.get("stateProvince")),
        "locality": _string(data.get("locality")),
        "decimal_latitude": _float(data.get("decimalLatitude")),
        "decimal_longitude": _float(data.get("decimalLongitude")),
        "coordinate_uncertainty_meters": _float(data.get("coordinateUncertaintyInMeters")),
        "event_date": _string(data.get("eventDate")),
        "year": _int(data.get("year")),
        "month": _int(data.get("month")),
        "day": _int(data.get("day")),
        "issues": [str(issue) for issue in _as_list(data.get("issues"))],
        "media": _as_list(data.get("media")),
        "source_url": build_source_url("occurrence", occurrence_key),
        "dataset_url": build_source_url("dataset", dataset_key),
        "download_doi": doi,
        "darwin_core_mapping": DARWIN_CORE_OCCURRENCE_MAPPING,
        "rights_decision": rights["decision"],
        "rights_basis": rights["rights_basis"],
        "rights_policy_id": rights["rights_policy_id"],
        "license_uri": rights["license_uri"],
        "attribution_required": rights["attribution_required"],
        "commercial_media_allowed": False,
        "raw_payload_hash": canonical_json_hash(data),
    }
    if not evidence["citation"]:
        evidence["citation"] = _string(data.get("publisherTitle") or data.get("datasetName"))
    return evidence

