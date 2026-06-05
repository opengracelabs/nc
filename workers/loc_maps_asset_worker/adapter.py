"""Library of Congress maps asset adapter.

Scope is intentionally narrow: LOC maps only, with the 1871 Hayden Survey map
as the proof target for Migration 18.
"""
from __future__ import annotations

from typing import Any

ADAPTER_ID = "loc_maps_asset_adapter_v1"
RIGHTS_EXTRACTOR_ID = "loc_maps_rights_extractor_v1"
SOURCE_ID = "loc"
SOURCE_PROFILE_ID = "loc_maps"

HAYDEN_ITEM_ID = "97683567"
HAYDEN_RESOURCE_ID = "g4262y.ye000023"
HAYDEN_SOURCE_RECORD_ID = f"loc:{HAYDEN_ITEM_ID}"
HAYDEN_SOURCE_URL = f"https://www.loc.gov/item/{HAYDEN_ITEM_ID}/"
HAYDEN_RESOURCE_URL = f"https://www.loc.gov/resource/{HAYDEN_RESOURCE_ID}/"
HAYDEN_IIIF_SERVICE = (
    "https://tile.loc.gov/image-services/iiif/"
    "service:gmd:gmd426:g4262:g4262y:ye000023"
)


def adapter_inputs(
    *,
    place_id: str,
    ingest_id: str = "loc_maps:97683567",
    fetched_at: str = "runtime_iso8601",
) -> dict[str, Any]:
    return {
        "adapter_id": ADAPTER_ID,
        "adapter_version": "1",
        "source_profile_id": SOURCE_PROFILE_ID,
        "source_id": SOURCE_ID,
        "target": {
            "loc_item_id": HAYDEN_ITEM_ID,
            "loc_item_url": HAYDEN_SOURCE_URL,
            "loc_resource_id": HAYDEN_RESOURCE_ID,
            "loc_resource_url": HAYDEN_RESOURCE_URL,
        },
        "place_context": {
            "place_id": place_id,
            "place_label": "Yellowstone National Park",
            "expected_terms": ["Yellowstone National Park", "Wyoming", "Parks"],
        },
        "run": {
            "ingest_id": ingest_id,
            "fetched_at": fetched_at,
        },
        "policy": {
            "preserve_master_media": True,
            "commercial_eligibility_mode": "review_required",
            "allowed_asset_classes": ["map"],
        },
    }


def loc_maps_raw_paths(ingest_id: str, item_id: str = HAYDEN_ITEM_ID) -> dict[str, str]:
    base = f"raw/loc/maps/{ingest_id}/{item_id}"
    return {
        "raw_payload_path": f"{base}/item.json",
        "iiif_info_path": f"{base}/iiif-info.json",
        "media_raw_path": f"{base}/ye000023.tif",
        "normalized_path": (
            f"normalized/loc/maps/{ingest_id}/{item_id}/canonical_asset_record.json"
        ),
    }


def extract_loc_map_rights(item_json: dict[str, Any]) -> dict[str, Any]:
    item = item_json.get("item", item_json)
    date = str(item.get("date") or "")
    rights = item.get("rights") or []
    rights_statement = " ".join(str(value) for value in rights).strip()
    lowered_rights = rights_statement.lower()
    has_adverse_advisory = (
        "no known restrictions" not in lowered_rights
        and any(
            token in lowered_rights
            for token in (
                "access restricted",
                "permission required",
                "may be restricted",
                "known restrictions apply",
            )
        )
    )
    pre_1928 = date.isdigit() and int(date) < 1928

    if has_adverse_advisory:
        status = "blocked"
        reuse = "blocked"
        confidence = 0.2
    elif pre_1928:
        status = "Public Domain"
        reuse = "allowed"
        confidence = 0.72
    else:
        status = "review_required"
        reuse = "review_required"
        confidence = 0.5

    return {
        "rights_extractor_id": RIGHTS_EXTRACTOR_ID,
        "source_record_id": HAYDEN_SOURCE_RECORD_ID,
        "normalized_rights_status": status,
        "commercial_reuse": reuse,
        "rights_source_url": HAYDEN_SOURCE_URL,
        "rights_statement": rights_statement,
        "confidence_score": confidence,
        "evidence": [
            {
                "field": "item.rights",
                "source_url": HAYDEN_SOURCE_URL,
                "value": rights_statement,
            },
            {
                "field": "item.date",
                "value": date,
                "interpretation": "Pre-1928 date supports public-domain analysis."
                if pre_1928
                else "Date does not independently establish public-domain status.",
            },
        ],
        "requires_human_review": True,
    }


def build_canonical_asset_record(
    *,
    item_json: dict[str, Any],
    place_id: str,
    ingest_id: str = "loc_maps:97683567",
    fetched_at: str = "runtime_iso8601",
) -> dict[str, Any]:
    item = item_json.get("item", item_json)
    nested = item.get("item") or {}
    paths = loc_maps_raw_paths(ingest_id)
    rights = extract_loc_map_rights(item_json)

    title = item.get("title") or nested.get("title") or "Yellowstone National Park : 1871"
    contributors = item.get("contributor_names") or nested.get("contributors") or []
    subjects = item.get("subject_headings") or nested.get("subjects") or []
    language = item.get("language") or nested.get("language") or ["english"]
    normalized_language = ["en" if str(value).lower() == "english" else str(value) for value in language]

    return {
        "canonical_record_type": "CanonicalAssetRecord",
        "canonical_record_version": "1",
        "asset_class": "map",
        "asset_subclass": "historic_map",
        "legacy_asset_type": "unknown",
        "source_id": SOURCE_ID,
        "source_profile_id": SOURCE_PROFILE_ID,
        "source_adapter_id": ADAPTER_ID,
        "source_record_id": HAYDEN_SOURCE_RECORD_ID,
        "source_native_ids": {
            "loc_lccn": item.get("library_of_congress_control_number") or HAYDEN_ITEM_ID,
            "loc_digital_id": _first(item.get("digital_id")) or (
                "http://hdl.loc.gov/loc.gmd/g4262y.ye000023"
            ),
            "loc_resource_id": HAYDEN_RESOURCE_ID,
            "loc_call_number": _first(item.get("call_number")) or item.get("shelf_id"),
        },
        "source_url": HAYDEN_SOURCE_URL,
        "resource_url": HAYDEN_RESOURCE_URL,
        "title": {"en": title},
        "description": {
            "en": _first(item.get("description"))
            or "1871 LOC Geography and Map Division raster map associated with the Hayden survey context."
        },
        "dates": {
            "created": str(item.get("date") or nested.get("date") or "1871"),
            "published_display": _first(item.get("created_published")) or "[S.l.], 1871.",
            "normalized_start_year": int(item.get("date") or 1871),
            "normalized_end_year": int(item.get("date") or 1871),
        },
        "creators": [
            {"name": contributor, "role": _creator_role(contributor)}
            for contributor in contributors
        ],
        "language": normalized_language,
        "subjects": [
            {"label": subject, "scheme": "loc_subject"}
            for subject in subjects
        ],
        "places": [
            {
                "place_id": place_id,
                "relationship": "depicts_or_covers",
                "relevance_score": 0.98,
                "evidence": (
                    "Title, location, and subject headings identify "
                    "Yellowstone National Park, Wyoming."
                ),
            }
        ],
        "media": {
            "primary_mime_type": "image/tiff",
            "iiif_image_service": HAYDEN_IIIF_SERVICE,
            "iiif_info_json": f"{HAYDEN_IIIF_SERVICE}/info.json",
            "files": [
                {
                    "role": "preservation_master",
                    "url": (
                        "https://tile.loc.gov/storage-services/master/gmd/gmd426/"
                        "g4262/g4262y/ye000023.tif"
                    ),
                    "mime_type": "image/tiff",
                    "size_bytes": 47811644,
                },
                {
                    "role": "service_jp2",
                    "url": (
                        "https://tile.loc.gov/storage-services/service/gmd/gmd426/"
                        "g4262/g4262y/ye000023.jp2"
                    ),
                    "mime_type": "image/jp2",
                    "width": 3696,
                    "height": 4312,
                    "size_bytes": 2816581,
                },
                {
                    "role": "web_derivative",
                    "url": f"{HAYDEN_IIIF_SERVICE}/full/pct:25/0/default.jpg",
                    "mime_type": "image/jpeg",
                    "width": 924,
                    "height": 1078,
                },
            ],
        },
        "rights": {
            "normalized_rights_status": rights["normalized_rights_status"],
            "commercial_reuse": rights["commercial_reuse"],
            "rights_source_url": HAYDEN_SOURCE_URL,
            "credit_line": "Library of Congress, Geography and Map Division.",
            "rights_extractor_id": RIGHTS_EXTRACTOR_ID,
            "requires_human_review": True,
        },
        "preservation": {
            "raw_payload_path": paths["raw_payload_path"],
            "raw_payload_checksum_sha256": "computed_at_fetch",
            "media_raw_path": paths["media_raw_path"],
            "media_checksum_sha256": "computed_after_media_fetch",
            "premis_object_id": "loc:maps:97683567",
            "fetched_at": fetched_at,
        },
        "status": "candidate",
        "provenance": {
            "prov:wasGeneratedBy": ADAPTER_ID,
            "prov:wasAttributedTo": "source:loc",
            "prov:used": [
                "source_profile:loc_maps",
                f"rights_extractor:{RIGHTS_EXTRACTOR_ID}",
                f"{HAYDEN_SOURCE_URL}?fo=json",
            ],
        },
    }


def _first(value: Any) -> str | None:
    if isinstance(value, list) and value:
        return str(value[0])
    if value:
        return str(value)
    return None


def _creator_role(name: str) -> str:
    lowered = name.lower()
    if "department of the interior" in lowered:
        return "issuing_body"
    if "hergesheimer" in lowered:
        return "cartographer_or_compiler"
    if "bien" in lowered:
        return "lithographer_or_printer"
    if "geological survey" in lowered:
        return "associated_body"
    return "contributor"
