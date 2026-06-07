"""Contracts shared by institution media adapters."""
from __future__ import annotations

from typing import Any

type NormalizedMediaRecord = dict[str, Any]

REQUIRED_NORMALIZED_FIELDS = (
    "record_id",
    "title",
    "description",
    "date",
    "creator",
    "subject_terms",
    "rights_uri",
    "provider",
    "dataProvider",
    "edm_type",
    "source_url",
    "representative_media_url",
    "preview_urls",
    "width_px",
    "height_px",
    "raw_payload_hash",
    "rights_decision",
    "rights_allowed",
)

OPTIONAL_NORMALIZED_FIELDS = (
    "set_specs",
    "language",
    "license_label",
    "collection_id",
    "source_object_number",
    "iiif_manifest_url",
    "iiif_image_service_url",
    "place_refs",
    "agent_refs",
    "concept_refs",
)


def mandatory_field_warnings(normalized: NormalizedMediaRecord) -> list[str]:
    """Return warnings for normalized fields required by the M36 substrate gate."""
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

