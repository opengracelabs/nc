"""Walters Art Museum Open Data normalization for Sprint 2."""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .client import (
    WaltersDataset,
    get_creators_for_object,
    get_images_for_object,
    get_primary_image,
    split_pipe_values,
)
from .rights import WALTERS_RIGHTS_POLICY_ID, classify_rights

WALTERS_PROVIDER = "Walters Art Museum"
WALTERS_COLLECTION_PURL = "https://purl.thewalters.org/art"


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


def _text_from_html(value: Any) -> str | None:
    cleaned = _string(value)
    if cleaned is None:
        return None
    text = re.sub(r"<[^>]+>", " ", cleaned)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def _join_values(values: list[Any]) -> str | None:
    cleaned = [text for text in (_string(value) for value in values) if text]
    return "; ".join(cleaned) if cleaned else None


def canonical_json_hash(payload: dict[str, Any]) -> str:
    """Hash normalized Walters source rows for replay checks."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def representative_media_url(image_row: dict[str, Any] | None) -> str | None:
    """Return the direct Walters image URL from a selected media row."""
    return _string(image_row.get("ImageURL")) if isinstance(image_row, dict) else None


def build_collection_url(object_number: str | None) -> str | None:
    """Build PURL for one Walters object. Fallback: caller supplies ResourceURL."""
    cleaned = _string(object_number)
    if cleaned is None:
        return None
    return f"{WALTERS_COLLECTION_PURL}/{cleaned}"


def _collection_names(object_row: dict[str, Any]) -> list[str]:
    return split_pipe_values(object_row.get("CollectionName"))


def _blocked_normalized_record(raw_payload: dict[str, Any], basis: str) -> dict[str, Any]:
    object_row = raw_payload.get("object")
    image_row = raw_payload.get("selected_image")
    object_dict = object_row if isinstance(object_row, dict) else {}
    image_dict = image_row if isinstance(image_row, dict) else {}
    collection_ids = split_pipe_values(object_dict.get("CollectionID"))
    collection_names = _collection_names(object_dict)
    return {
        "record_id": _string(object_dict.get("ObjectID")),
        "title": _string(object_dict.get("Title")),
        "description": _text_from_html(object_dict.get("Description")),
        "date": _string(object_dict.get("DateText")),
        "creator": None,
        "subject_terms": [],
        "rights_uri": None,
        "provider": WALTERS_PROVIDER,
        "dataProvider": WALTERS_PROVIDER,
        "edm_type": _string(object_dict.get("Classification")),
        "source_url": build_collection_url(object_dict.get("ObjectNumber"))
        or _string(object_dict.get("ResourceURL")),
        "representative_media_url": representative_media_url(image_dict),
        "preview_urls": [],
        "width_px": None,
        "height_px": None,
        "raw_payload_hash": canonical_json_hash(raw_payload),
        "rights_decision": "BLOCKED",
        "rights_allowed": False,
        "walters_rights_basis": basis,
        "walters_rights_policy_id": WALTERS_RIGHTS_POLICY_ID,
        "walters_object_id": _string(object_dict.get("ObjectID")),
        "walters_object_number": _string(object_dict.get("ObjectNumber")),
        "walters_image_url": representative_media_url(image_dict),
        "walters_media_xref_id": _string(image_dict.get("MediaXrefID")),
        "walters_is_primary": _string(image_dict.get("IsPrimary")),
        "walters_collection_ids": collection_ids,
        "walters_collection_names": collection_names,
        "accession_number": _string(object_dict.get("ObjectNumber")),
        "object_name": _string(object_dict.get("ObjectName")),
        "classification": _string(object_dict.get("Classification")),
        "medium": _string(object_dict.get("Medium")),
        "culture": _string(object_dict.get("Culture")),
        "style": _string(object_dict.get("Style")),
        "dynasty": _string(object_dict.get("Dynasty")),
        "credit_line": _string(object_dict.get("CreditLine")),
        "provenance": _string(object_dict.get("Provenance")),
        "date_start": _int(object_dict.get("DateBeginYear")),
        "date_end": _int(object_dict.get("DateEndYear")),
        "creator_nationality": None,
        "source_object": object_dict,
        "images": raw_payload.get("images") or [],
        "creators": raw_payload.get("creators") or [],
    }


def normalize_record(
    object_row: dict[str, str],
    image_row: dict[str, str] | None,
    *,
    creators: list[dict[str, str]] | None = None,
    all_images: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Normalize one Walters object row plus selected media row."""
    creators = creators or []
    all_images = all_images or ([] if image_row is None else [image_row])
    raw_payload = {
        "object": object_row,
        "selected_image": image_row,
        "images": all_images,
        "creators": creators,
    }
    rights = classify_rights(object_row, image_row)
    if rights["decision"] == "BLOCKED":
        return _blocked_normalized_record(raw_payload, str(rights["rights_basis"]))

    object_id = _string(object_row.get("ObjectID"))
    object_number = _string(object_row.get("ObjectNumber"))
    image_url = representative_media_url(image_row)
    collection_ids = split_pipe_values(object_row.get("CollectionID"))
    collection_names = _collection_names(object_row)
    creator = _join_values([row.get("name") for row in creators])
    creator_nationality = _join_values([row.get("nationality") for row in creators])
    preview_urls = []
    for row in all_images:
        url = representative_media_url(row)
        if url and url not in preview_urls:
            preview_urls.append(url)

    return {
        "record_id": object_id,
        "title": _string(object_row.get("Title")),
        "description": _text_from_html(object_row.get("Description"))
        or _string(object_row.get("Medium")),
        "date": _string(object_row.get("DateText")),
        "creator": creator,
        "subject_terms": [
            value
            for value in [
                _string(object_row.get("ObjectName")),
                _string(object_row.get("Culture")),
                _string(object_row.get("Style")),
                *collection_names,
            ]
            if value
        ],
        "rights_uri": rights["rights_statement_uri"],
        "provider": WALTERS_PROVIDER,
        "dataProvider": WALTERS_PROVIDER,
        "edm_type": _string(object_row.get("Classification")),
        "source_url": build_collection_url(object_number)
        or _string(object_row.get("ResourceURL")),
        "representative_media_url": image_url,
        "preview_urls": preview_urls,
        "width_px": None,
        "height_px": None,
        "raw_payload_hash": canonical_json_hash(raw_payload),
        "rights_decision": rights["decision"],
        "rights_allowed": rights["allowed"],
        "walters_rights_basis": rights["rights_basis"],
        "walters_rights_policy_id": rights["rights_policy_id"],
        "walters_object_id": object_id,
        "walters_object_number": object_number,
        "walters_image_url": image_url,
        "walters_media_xref_id": _string(image_row.get("MediaXrefID"))
        if isinstance(image_row, dict)
        else None,
        "walters_is_primary": _string(image_row.get("IsPrimary"))
        if isinstance(image_row, dict)
        else None,
        "walters_collection_ids": collection_ids,
        "walters_collection_names": collection_names,
        "accession_number": object_number,
        "object_name": _string(object_row.get("ObjectName")),
        "classification": _string(object_row.get("Classification")),
        "medium": _string(object_row.get("Medium")),
        "culture": _string(object_row.get("Culture")),
        "style": _string(object_row.get("Style")),
        "dynasty": _string(object_row.get("Dynasty")),
        "credit_line": _string(object_row.get("CreditLine")),
        "provenance": _string(object_row.get("Provenance")),
        "date_start": _int(object_row.get("DateBeginYear")),
        "date_end": _int(object_row.get("DateEndYear")),
        "creator_nationality": creator_nationality,
        "source_object": object_row,
        "images": all_images,
        "creators": creators,
    }


def normalize_dataset_record(dataset: WaltersDataset, object_id: int | str) -> dict[str, Any]:
    """Normalize one object from a loaded Walters dataset."""
    cleaned = _string(object_id)
    if cleaned is None:
        raise ValueError("missing_object_id")
    object_row = dataset.objects_by_id.get(cleaned)
    if object_row is None:
        raise KeyError(f"missing_walters_object:{cleaned}")
    return normalize_record(
        object_row,
        get_primary_image(dataset, cleaned),
        creators=get_creators_for_object(dataset, cleaned),
        all_images=get_images_for_object(dataset, cleaned),
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
