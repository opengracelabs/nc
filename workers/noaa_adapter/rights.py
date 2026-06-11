"""NOAA Rights Matrix v1 classification."""
from __future__ import annotations

import re
from typing import Any

from workers.shared_media_adapter.rights import NOC_US_URI, PDM_URI, RightsDecision

from .config import RIGHTS_POLICY_ID

NO_COPYRIGHT_US_URI = NOC_US_URI
PUBLIC_DOMAIN_MARK_URI = PDM_URI

FEDERAL_CREDIT_PATTERNS = (
    "NOAA",
    "NOAA/NMFS",
    "NOAA/NOS",
    "NOAA/OAR",
    "NOAA/NWS",
    "NOAA/NESDIS",
    "NOAA Fisheries",
    "NOAA Ocean Service",
    "NOAA Research",
    "National Oceanic and Atmospheric Administration",
    "ESSA",
    "Weather Bureau",
    "US Weather Bureau",
    "U.S. Weather Bureau",
    "USCGS",
    "U.S. Coast and Geodetic Survey",
    "Bureau of Commercial Fisheries",
    "NASA",
    "USGS",
    "U.S. Geological Survey",
    "United States Geological Survey",
    "USFWS",
    "U.S. Fish and Wildlife Service",
    "NPS",
    "National Park Service",
    "EPA",
    "Environmental Protection Agency",
    "NSF",
    "National Science Foundation",
    "USACE",
    "U.S. Army Corps of Engineers",
    "NIST",
    "National Institute of Standards and Technology",
)
NOAA_FEDERAL_CREDIT_PATTERNS = FEDERAL_CREDIT_PATTERNS
REVIEW_PARTNER_MARKERS = (
    "NASA/ESA",
    "ESA",
    "European Space Agency",
    "JAXA",
    "Japan Aerospace Exploration Agency",
    "CSA",
    "Canadian Space Agency",
    "foreign partner",
    "foreign agency",
    "International",
    "University",
    "College",
    "Institute",
    "NGO",
    "Foundation",
    "Conservancy",
    "Society",
    "AURA",
    "STScI",
    "MBARI",
    "Schmidt Ocean Institute",
    "contractor",
    "contract",
)
BLOCKED_MARKERS = ("Getty", "Reuters", "AP", "Maxar", "DigitalGlobe", "Planet", "GeoEye")


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _haystack(record: dict[str, Any]) -> str:
    values: list[str] = []
    for key in (
        "title",
        "description",
        "creator",
        "credit",
        "owner_name",
        "license_label",
        "tags",
        "source_url",
    ):
        value = record.get(key)
        if isinstance(value, list):
            values.extend(str(item) for item in value)
        elif value is not None:
            values.append(str(value))
    return " | ".join(values)


def _detect_markers(text: str, markers: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    for marker in markers:
        pattern = rf"(?<![A-Za-z0-9]){re.escape(marker)}(?![A-Za-z0-9])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append(marker)
    return found


def _detect_personal_name_noaa(text: str) -> list[str]:
    patterns = (
        r"\b[A-Z][a-z]+(?:\s+[A-Z]\.)?\s+[A-Z][a-z]+/NOAA\b",
        r"\b[A-Z][a-z]+(?:\s+[A-Z]\.)?\s+[A-Z][a-z]+,?\s+NOAA\b",
        r"\bPhoto(?:graph)?\s+by\s+[A-Z][a-z]+(?:\s+[A-Z]\.)?\s+[A-Z][a-z]+\b",
    )
    matches: list[str] = []
    for pattern in patterns:
        matches.extend(match.group(0) for match in re.finditer(pattern, text))
    return sorted(set(matches))


def _is_noaa_federal_credit(credit: str | None) -> bool:
    if not credit:
        return False
    cleaned = " ".join(credit.strip().strip(".").split())
    lowered = cleaned.lower()
    if _detect_personal_name_noaa(cleaned):
        return False
    allowed = {pattern.lower() for pattern in NOAA_FEDERAL_CREDIT_PATTERNS}
    if lowered.startswith("noaa") or lowered.startswith("noaa "):
        return True
    if lowered in allowed:
        return True
    return any(
        lowered.startswith(f"{pattern.lower()}/")
        for pattern in NOAA_FEDERAL_CREDIT_PATTERNS
    )


def _result(
    *,
    decision: RightsDecision,
    allowed: bool,
    rights_statement_uri: str | None,
    rights_status: str,
    rights_basis: str,
    partner_markers: list[str] | None = None,
    contributor_markers: list[str] | None = None,
    blocked_markers: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "decision": decision.value,
        "allowed": allowed,
        "rights_statement_uri": rights_statement_uri,
        "rights_status": rights_status,
        "rights_basis": rights_basis,
        "rights_policy_id": RIGHTS_POLICY_ID,
        "partner_markers": partner_markers or [],
        "contributor_markers": contributor_markers or [],
        "blocked_markers": blocked_markers or [],
    }


def classify_rights(record: dict[str, Any] | None) -> dict[str, Any]:
    """Classify one NOAA discovery record under NOAA Rights Matrix v1."""
    data = _as_dict(record)
    if not data:
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="missing_object",
        )

    text = _haystack(data)
    license_id = _string(data.get("license_id") or data.get("license"))
    credit = _string(data.get("credit"))
    blocked_markers = _detect_markers(text, BLOCKED_MARKERS)
    partner_markers = _detect_markers(text, REVIEW_PARTNER_MARKERS)
    contributor_markers = _detect_personal_name_noaa(text)

    if blocked_markers:
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="blocked_partner_marker",
            partner_markers=partner_markers,
            contributor_markers=contributor_markers,
            blocked_markers=blocked_markers,
        )

    if license_id == "0":
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="flickr_all_rights_reserved",
            partner_markers=partner_markers,
            contributor_markers=contributor_markers,
        )

    if partner_markers:
        return _result(
            decision=RightsDecision.REVIEW_REQUIRED,
            allowed=False,
            rights_statement_uri=NO_COPYRIGHT_US_URI,
            rights_status="pending_verification",
            rights_basis="partner_or_contributor_marker",
            partner_markers=partner_markers,
            contributor_markers=contributor_markers,
        )

    if contributor_markers:
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="personal_name_noaa_credit",
            partner_markers=partner_markers,
            contributor_markers=contributor_markers,
        )

    if license_id == "8":
        return _result(
            decision=RightsDecision.ALLOWED,
            allowed=True,
            rights_statement_uri=NO_COPYRIGHT_US_URI,
            rights_status="pending_verification",
            rights_basis="flickr_us_government_work",
        )

    if _is_noaa_federal_credit(credit):
        return _result(
            decision=RightsDecision.ALLOWED,
            allowed=True,
            rights_statement_uri=NO_COPYRIGHT_US_URI,
            rights_status="pending_verification",
            rights_basis="noaa_federal_credit",
        )

    if license_id in {"7", "9", "10"}:
        return _result(
            decision=RightsDecision.REVIEW_REQUIRED,
            allowed=False,
            rights_statement_uri=PUBLIC_DOMAIN_MARK_URI,
            rights_status="pending_verification",
            rights_basis="public_domain_license_without_federal_credit",
        )

    if license_id in {"1", "2", "3", "4", "5", "6"}:
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="unsupported_flickr_license",
        )

    return _result(
        decision=RightsDecision.BLOCKED,
        allowed=False,
        rights_statement_uri=None,
        rights_status="blocked",
        rights_basis="missing_rights_evidence",
        partner_markers=partner_markers,
        contributor_markers=contributor_markers,
    )


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when NOAA Rights Matrix v1 permits discovery candidates."""
    return bool(classify_rights(record)["allowed"])

