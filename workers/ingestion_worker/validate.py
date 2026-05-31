"""
Validate a discovery candidate before ingestion begins.
Returns a list of error strings. Empty list = valid.
"""
from typing import Any


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if not candidate.get("id"):
        errors.append("missing id")

    if not candidate.get("source"):
        errors.append("missing source")

    if not candidate.get("source_id"):
        errors.append("missing source_id")

    name = candidate.get("name") or {}
    if not any(name.values()):
        errors.append("name has no non-empty language values")

    if candidate.get("status") != "approved":
        errors.append(f"candidate status is '{candidate.get('status')}', expected 'approved'")

    country_codes = candidate.get("country_codes") or []
    for code in country_codes:
        if not isinstance(code, str) or len(code) != 2:
            errors.append(f"invalid country_code: {code!r}")

    centroid = candidate.get("centroid")
    if centroid is not None:
        coords = centroid.get("coordinates") if isinstance(centroid, dict) else None
        if not coords or len(coords) != 2:
            errors.append("centroid.coordinates must be [lon, lat]")
        else:
            lon, lat = coords
            if not (-180 <= lon <= 180):
                errors.append(f"centroid longitude out of range: {lon}")
            if not (-90 <= lat <= 90):
                errors.append(f"centroid latitude out of range: {lat}")

    ouv = candidate.get("ouv_criteria") or []
    valid_criteria = {"i","ii","iii","iv","v","vi","vii","viii","ix","x"}
    for c in ouv:
        if c.lower() not in valid_criteria:
            errors.append(f"unknown OUV criterion: {c!r}")

    return errors
