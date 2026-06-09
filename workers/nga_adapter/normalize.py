"""National Gallery of Art Open Data normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .client import (
    NgaDataset,
    get_constituents_for_object,
    get_images_for_object,
    get_primary_image,
    get_terms_for_object,
)
from .rights import classify_rights

NGA_PROVIDER = "National Gallery of Art"
NGA_COLLECTION_BASE_URL = "https://www.nga.gov/collection/art-object-page"


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _int(value: Any) -> int | None:
    cleaned = _string(value)
    if cleaned is None:
        return None
    try:
        return int(cleaned)
    except ValueError:
        return None


def _string_list(values: list[Any]) -> list[str]:
    return [str(value).strip() for value in values if str(value).strip()]


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash normalized NGA source rows for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def build_collection_url(object_id: str | None) -> str | None:
    """Build the public NGA collection page URL for one object id."""
    cleaned = _string(object_id)
    if cleaned is None:
        return None
    return f"{NGA_COLLECTION_BASE_URL}.{cleaned}.html"


def representative_media_url(image_row: dict[str, Any] | None) -> str | None:
    """Build a usable IIIF image URL from an NGA iiifurl service base."""
    iiif_url = _string(image_row.get("iiifurl")) if isinstance(image_row, dict) else None
    if iiif_url is None:
        return None
    return f"{iiif_url.rstrip('/')}/full/!1024,1024/0/default.jpg"


def _creator(constituents: list[dict[str, str]], object_row: dict[str, str]) -> str | None:
    names = [
        _string(row.get("forwarddisplayname") or row.get("preferreddisplayname"))
        for row in constituents
    ]
    cleaned = [name for name in names if name]
    if cleaned:
        return "; ".join(cleaned)
    return _string(object_row.get("attribution"))


def _term_value(terms: list[dict[str, str]], term_type: str) -> str | None:
    expected = term_type.strip().lower()
    for row in terms:
        termtype = _string(row.get("termtype"))
        if termtype and termtype.lower() == expected:
            return _string(row.get("term"))
    return None


def _constituent_value(constituents: list[dict[str, str]], key: str) -> str | None:
    values = [_string(row.get(key)) for row in constituents]
    cleaned = [value for value in values if value]
    return "; ".join(cleaned) if cleaned else None


def _blocked_normalized_record(raw_payload: dict[str, Any], basis: str) -> dict[str, Any]:
    return {
        "record_id": None,
        "title": None,
        "description": None,
        "date": None,
        "creator": None,
        "subject_terms": [],
        "rights_uri": None,
        "provider": NGA_PROVIDER,
        "dataProvider": NGA_PROVIDER,
        "edm_type": None,
        "source_url": None,
        "representative_media_url": None,
        "preview_urls": [],
        "width_px": None,
        "height_px": None,
        "raw_payload_hash": canonical_json_hash(raw_payload),
        "rights_decision": "BLOCKED",
        "rights_allowed": False,
        "nga_rights_basis": basis,
        "nga_rights_policy_id": "nga_rights_matrix_v1",
        "nga_openaccess": None,
        "nga_image_uuid": None,
        "nga_iiifurl": None,
        "nga_iiif_thumb_url": None,
        "nga_viewtype": None,
        "nga_objectid": None,
        "nga_accessionnum": None,
        "accession_number": None,
        "classification": None,
        "subclassification": None,
        "department_abbr": None,
        "wikidataid": None,
        "is_virtual": None,
        "parent_id": None,
        "school": None,
        "place_executed": None,
        "creator_nationality": None,
        "source_object": (
            raw_payload.get("object") if isinstance(raw_payload.get("object"), dict) else {}
        ),
        "images": raw_payload.get("images") or [],
        "terms": raw_payload.get("terms") or [],
        "constituents": raw_payload.get("constituents") or [],
    }


def normalize_record(
    object_row: dict[str, str],
    image_row: dict[str, str] | None,
    *,
    terms: list[dict[str, str]] | None = None,
    constituents: list[dict[str, str]] | None = None,
    all_images: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Normalize one NGA object row plus selected image row."""
    terms = terms or []
    constituents = constituents or []
    all_images = all_images or ([] if image_row is None else [image_row])
    if not isinstance(object_row, dict):
        raw_payload = {
            "object": object_row,
            "selected_image": image_row,
            "images": all_images,
            "terms": terms,
            "constituents": constituents,
        }
        return _blocked_normalized_record(raw_payload, "missing_object_record")

    rights = classify_rights(image_row)
    object_id = _string(object_row.get("objectid"))
    accession_num = _string(object_row.get("accessionnum"))
    school = _term_value(terms, "school")
    place_executed = _term_value(terms, "place executed")
    creator_nationality = _constituent_value(constituents, "nationality")
    rep_url = representative_media_url(image_row)
    thumb_url = _string(image_row.get("iiifthumburl")) if isinstance(image_row, dict) else None

    raw_payload = {
        "object": object_row,
        "selected_image": image_row,
        "images": all_images,
        "terms": terms,
        "constituents": constituents,
    }

    return {
        "record_id": object_id,
        "title": _string(object_row.get("title")),
        "description": _string(object_row.get("provenancetext") or object_row.get("medium")),
        "date": _string(object_row.get("displaydate")),
        "creator": _creator(constituents, object_row),
        "subject_terms": _string_list([row.get("term") for row in terms]),
        "rights_uri": rights["rights_statement_uri"],
        "provider": NGA_PROVIDER,
        "dataProvider": NGA_PROVIDER,
        "edm_type": _string(object_row.get("classification")),
        "source_url": build_collection_url(object_id),
        "representative_media_url": rep_url,
        "preview_urls": [url for url in [rep_url, thumb_url] if url],
        "width_px": _int(image_row.get("width")) if isinstance(image_row, dict) else None,
        "height_px": _int(image_row.get("height")) if isinstance(image_row, dict) else None,
        "raw_payload_hash": canonical_json_hash(raw_payload),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "nga_rights_basis": rights["rights_basis"],
        "nga_rights_policy_id": rights["rights_policy_id"],
        "nga_openaccess": (
            _string(image_row.get("openaccess")) if isinstance(image_row, dict) else None
        ),
        "nga_image_uuid": _string(image_row.get("uuid")) if isinstance(image_row, dict) else None,
        "nga_iiifurl": _string(image_row.get("iiifurl")) if isinstance(image_row, dict) else None,
        "nga_iiif_thumb_url": thumb_url,
        "nga_viewtype": _string(image_row.get("viewtype")) if isinstance(image_row, dict) else None,
        "nga_objectid": object_id,
        "nga_accessionnum": accession_num,
        "accession_number": accession_num,
        "classification": _string(object_row.get("classification")),
        "subclassification": _string(object_row.get("subclassification")),
        "department_abbr": _string(object_row.get("departmentabbr")),
        "wikidataid": _string(object_row.get("wikidataid")),
        "is_virtual": _string(object_row.get("isvirtual")),
        "parent_id": _string(object_row.get("parentid")),
        "school": school,
        "place_executed": place_executed,
        "creator_nationality": creator_nationality,
        "source_object": object_row,
        "images": all_images,
        "terms": terms,
        "constituents": constituents,
    }


def normalize_dataset_record(dataset: NgaDataset, object_id: int | str) -> dict[str, Any]:
    """Normalize one object from a loaded NGA dataset."""
    cleaned = _string(object_id)
    if cleaned is None:
        raise ValueError("missing_object_id")
    object_row = dataset.objects_by_id.get(cleaned)
    if object_row is None:
        raise KeyError(f"missing_nga_object:{cleaned}")
    all_images = get_images_for_object(dataset, cleaned)
    return normalize_record(
        object_row,
        get_primary_image(dataset, cleaned),
        terms=get_terms_for_object(dataset, cleaned),
        constituents=get_constituents_for_object(dataset, cleaned),
        all_images=all_images,
    )


def mandatory_field_warnings(normalized: dict[str, Any]) -> list[str]:
    """Return warnings for fields required by the shared media contract."""
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
    if not normalized.get("representative_media_url"):
        warnings.append("missing_representative_media_url")
    return warnings
