"""NASA Image and Video Library Rights Class 10."""
from __future__ import annotations

import re
from typing import Any

from workers.shared_media_adapter.rights import NOC_US_URI, RightsDecision

from .config import RIGHTS_POLICY_ID

NASA_RIGHTS_POLICY_ID = RIGHTS_POLICY_ID
NO_COPYRIGHT_US_URI = NOC_US_URI

CENTER_ALLOWLIST = frozenset(
    {
        "ARC",
        "AFRC",
        "GRC",
        "GSFC",
        "HQ",
        "JSC",
        "KSC",
        "LaRC",
        "MSFC",
        "SSC",
        "WFF",
    }
)
REVIEW_CENTERS = frozenset({"JPL"})
REVIEW_PARTNER_MARKERS = ("ESA", "CSA", "JAXA", "STScI", "AURA")
BLOCKED_PARTNER_MARKERS = ("Getty", "AP", "Reuters")
COPYRIGHT_MARKERS = ("copyright", "all rights reserved", "used with permission")
PUBLICITY_RISK_MARKERS = (
    "commercial use",
    "endorsement",
    "personality rights",
    "privacy",
    "publicity",
    "trademark",
)


def _string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _haystack(record: dict[str, Any]) -> str:
    values: list[str] = []
    for key in (
        "title",
        "description",
        "description_508",
        "center",
        "photographer",
        "secondary_creator",
        "copyright",
        "rights",
        "rights_summary",
        "use_restrictions",
    ):
        value = record.get(key)
        if isinstance(value, str):
            values.append(value)
    for key in ("keywords", "album"):
        values.extend(str(value) for value in _as_list(record.get(key)))
    return " | ".join(values)


def detect_markers(record: dict[str, Any], markers: tuple[str, ...]) -> list[str]:
    """Return markers found in NASA metadata as standalone tokens."""
    haystack = _haystack(record)
    found: list[str] = []
    for marker in markers:
        pattern = rf"(?<![A-Za-z0-9]){re.escape(marker)}(?![A-Za-z0-9])"
        if re.search(pattern, haystack, flags=re.IGNORECASE):
            found.append(marker)
    return found


def _result(
    *,
    decision: RightsDecision,
    allowed: bool,
    rights_statement_uri: str | None,
    rights_status: str,
    rights_basis: str,
    partner_markers: list[str] | None = None,
    copyright_markers: list[str] | None = None,
    publicity_risk_markers: list[str] | None = None,
) -> dict[str, str | bool | None | list[str]]:
    return {
        "decision": decision.value,
        "allowed": allowed,
        "rights_statement_uri": rights_statement_uri,
        "rights_status": rights_status,
        "rights_basis": rights_basis,
        "rights_policy_id": NASA_RIGHTS_POLICY_ID,
        "partner_markers": partner_markers or [],
        "copyright_markers": copyright_markers or [],
        "publicity_risk_markers": publicity_risk_markers or [],
    }


def classify_rights(record: dict[str, Any] | None) -> dict[str, str | bool | None | list[str]]:
    """Classify one NASA Image Library metadata record under Rights Class 10."""
    if not isinstance(record, dict) or not record:
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="missing_object",
        )

    if not _string(record.get("nasa_id")):
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="missing_nasa_id",
        )

    if _string(record.get("media_type")) != "image":
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="unsupported_media_type",
        )

    center = _string(record.get("center"))
    blocked_markers = detect_markers(record, BLOCKED_PARTNER_MARKERS)
    review_markers = detect_markers(record, REVIEW_PARTNER_MARKERS)
    copyright_markers = detect_markers(record, COPYRIGHT_MARKERS)
    publicity_risk_markers = detect_markers(record, PUBLICITY_RISK_MARKERS)

    if blocked_markers:
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="blocked_partner_marker",
            partner_markers=blocked_markers,
            copyright_markers=copyright_markers,
            publicity_risk_markers=publicity_risk_markers,
        )

    if copyright_markers or _string(record.get("copyright")):
        return _result(
            decision=RightsDecision.BLOCKED,
            allowed=False,
            rights_statement_uri=None,
            rights_status="blocked",
            rights_basis="copyright_detected",
            partner_markers=review_markers,
            copyright_markers=copyright_markers or ["copyright"],
            publicity_risk_markers=publicity_risk_markers,
        )

    if center in REVIEW_CENTERS:
        return _result(
            decision=RightsDecision.REVIEW_REQUIRED,
            allowed=False,
            rights_statement_uri=NO_COPYRIGHT_US_URI,
            rights_status="pending_verification",
            rights_basis="review_center_jpl",
            partner_markers=review_markers,
            publicity_risk_markers=publicity_risk_markers,
        )

    if review_markers:
        return _result(
            decision=RightsDecision.REVIEW_REQUIRED,
            allowed=False,
            rights_statement_uri=NO_COPYRIGHT_US_URI,
            rights_status="pending_verification",
            rights_basis="review_partner_marker",
            partner_markers=review_markers,
            publicity_risk_markers=publicity_risk_markers,
        )

    if publicity_risk_markers:
        return _result(
            decision=RightsDecision.REVIEW_REQUIRED,
            allowed=False,
            rights_statement_uri=NO_COPYRIGHT_US_URI,
            rights_status="pending_verification",
            rights_basis="publicity_risk_detected",
            publicity_risk_markers=publicity_risk_markers,
        )

    if center in CENTER_ALLOWLIST:
        return _result(
            decision=RightsDecision.ALLOWED,
            allowed=True,
            rights_statement_uri=NO_COPYRIGHT_US_URI,
            rights_status="pending_verification",
            rights_basis="federal_center_clean_rights",
        )

    return _result(
        decision=RightsDecision.REVIEW_REQUIRED,
        allowed=False,
        rights_statement_uri=NO_COPYRIGHT_US_URI,
        rights_status="pending_verification",
        rights_basis="center_not_allowlisted",
    )


def is_allowed_rights(record: dict[str, Any] | None) -> bool:
    """Return true only when NASA Rights Class 10 permits candidate expansion."""
    return bool(classify_rights(record)["allowed"])
