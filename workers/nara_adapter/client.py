"""NARA Catalog API v2 client helpers for Sprint 1.

Sprint 1 is intentionally read-only: it searches archival descriptions, looks up
records by `naId`, extracts still-image digital objects, and captures access/use
restriction evidence. It does not write to the NC store.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import httpx

from .config import RIGHTS_POLICY_ID, SOURCE_SLUG, get_api_key, settings

PUBLIC_DOMAIN_MARK_URI = "https://creativecommons.org/publicdomain/mark/1.0/"
IMAGE_OBJECT_TYPES = frozenset(
    {
        "Image (JPG)",
        "Image (JPEG)",
        "Image (PNG)",
        "Image (GIF)",
        "Image (TIFF)",
        "Image (TIF)",
        "Image (JP2)",
    }
)


@dataclass(frozen=True)
class NaraRestrictionEvidence:
    """Sprint 1 access/use restriction evidence."""

    decision: str
    use_restriction_status: str | None
    access_restriction_status: str | None
    rights_basis: str
    rights_statement_uri: str | None = None
    rights_policy_id: str = RIGHTS_POLICY_ID

    @property
    def allowed(self) -> bool:
        return self.decision == "ALLOWED"


@dataclass(frozen=True)
class NaraDigitalObject:
    """NARA still-image digital object candidate."""

    na_id: str
    object_id: str
    object_url: str
    object_type: str
    object_filename: str | None
    object_description: str | None
    object_file_size: int | None
    source_slug: str = SOURCE_SLUG


@dataclass(frozen=True)
class NaraPublicDomainCandidate:
    """Evidence-only public-domain candidate for Sprint 1."""

    na_id: str
    title: str
    digital_object: NaraDigitalObject
    rights: NaraRestrictionEvidence
    source_slug: str = SOURCE_SLUG


def _base_url() -> str:
    return settings.nara_api_base_url.rstrip("/")


def _clean(value: Any) -> str:
    return str(value).strip()


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def canonical_request_params(params: dict[str, Any]) -> dict[str, str]:
    """Return replay-stable request params with empty values removed."""
    cleaned = {
        str(key): str(value)
        for key, value in params.items()
        if value is not None and value != ""
    }
    return dict(sorted(cleaned.items()))


def build_search_url() -> str:
    """Build the official NARA Catalog v2 records search URL."""
    return f"{_base_url()}/records/search"


def build_catalog_record_url(na_id: str | int) -> str:
    """Build the public NARA Catalog record URL."""
    cleaned = _clean(na_id)
    if not cleaned:
        raise ValueError("missing_na_id")
    return f"https://catalog.archives.gov/id/{cleaned}"


def build_search_params(
    *,
    query: str | None = None,
    na_id: str | int | None = None,
    page: int = 1,
    limit: int | None = None,
    available_online: bool | None = True,
    object_type: str | None = None,
    source_includes: str | None = None,
    search_after: str | None = None,
) -> dict[str, str]:
    """Build deterministic NARA search query parameters."""
    if page < 1:
        raise ValueError("invalid_page")
    resolved_limit = settings.nara_page_limit if limit is None else limit
    if resolved_limit < 1:
        raise ValueError("invalid_limit")

    params: dict[str, Any] = {
        "availableOnline": str(available_online).lower()
        if available_online is not None
        else None,
        "limit": resolved_limit,
        "naId_is": na_id,
        "objectType": object_type,
        "page": page,
        "q": query,
        "searchAfter": search_after,
        "sourceIncludes": source_includes,
    }
    return canonical_request_params(params)


def build_record_lookup_params(na_id: str | int) -> dict[str, str]:
    """Build a records search request for one exact `naId`."""
    cleaned = _clean(na_id)
    if not cleaned:
        raise ValueError("missing_na_id")
    return build_search_params(
        na_id=cleaned,
        limit=1,
        available_online=None,
        source_includes=(
            "naId,title,useRestriction,accessRestriction,digitalObjects,"
            "generalRecordsTypes,levelOfDescription"
        ),
    )


def build_headers() -> dict[str, str]:
    """Build NARA request headers from environment configuration."""
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("missing_nara_api_key")
    return {
        "Content-Type": "application/json",
        "User-Agent": settings.nara_user_agent,
        "x-api-key": api_key,
    }


async def _get_json(
    path_or_url: str,
    *,
    params: dict[str, Any] | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    if path_or_url.startswith("http"):
        url = path_or_url
    else:
        url = urljoin(f"{_base_url()}/", path_or_url.lstrip("/"))

    request_params = canonical_request_params(params or {})
    request_params_or_none = request_params or None
    headers = build_headers()

    if http_client is not None:
        response = await http_client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(timeout=settings.nara_fetch_timeout_seconds) as client:
        response = await client.get(url, params=request_params_or_none, headers=headers)
        response.raise_for_status()
        return response.json()


async def search_records(
    *,
    query: str | None = None,
    page: int = 1,
    limit: int | None = None,
    available_online: bool | None = True,
    object_type: str | None = None,
    source_includes: str | None = None,
    search_after: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Search NARA Catalog records through the official v2 endpoint."""
    params = build_search_params(
        query=query,
        page=page,
        limit=limit,
        available_online=available_online,
        object_type=object_type,
        source_includes=source_includes,
        search_after=search_after,
    )
    return await _get_json(build_search_url(), params=params, http_client=http_client)


async def fetch_record(
    na_id: str | int,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch one NARA record by exact `naId` through records search."""
    return await _get_json(
        build_search_url(),
        params=build_record_lookup_params(na_id),
        http_client=http_client,
    )


def extract_hits(response: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract raw hit objects from a NARA search response."""
    hits = response.get("body", {}).get("hits", {}).get("hits", [])
    return [hit for hit in hits if isinstance(hit, dict)]


def extract_total(response: dict[str, Any]) -> int:
    """Extract the total hit count from a NARA search response."""
    total = response.get("body", {}).get("hits", {}).get("total", {})
    if isinstance(total, dict):
        value = total.get("value")
    else:
        value = total
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def extract_record(hit_or_response: dict[str, Any]) -> dict[str, Any]:
    """Extract `_source.record` from a hit or from the first hit in a response."""
    if "body" in hit_or_response:
        hits = extract_hits(hit_or_response)
        if not hits:
            return {}
        hit_or_response = hits[0]
    record = hit_or_response.get("_source", {}).get("record", {})
    return record if isinstance(record, dict) else {}


def extract_na_id(record: dict[str, Any]) -> str | None:
    """Extract a stable string `naId` from a record."""
    value = record.get("naId")
    cleaned = _clean(value) if value is not None else ""
    return cleaned or None


def extract_next_search_after(response: dict[str, Any]) -> str | None:
    """Return the last hit sort token for future deep pagination."""
    hits = extract_hits(response)
    if not hits:
        return None
    sort_values = hits[-1].get("sort")
    if isinstance(sort_values, list) and sort_values:
        return ",".join(_clean(value) for value in sort_values)
    return None


def extract_use_restriction(record: dict[str, Any]) -> str | None:
    """Extract the record use-restriction status."""
    value = record.get("useRestriction")
    if isinstance(value, dict):
        status = value.get("status") or value.get("note")
    else:
        status = value
    cleaned = _clean(status) if status is not None else ""
    return cleaned or None


def extract_access_restriction(record: dict[str, Any]) -> str | None:
    """Extract the record access-restriction status."""
    value = record.get("accessRestriction")
    if isinstance(value, dict):
        status = value.get("status") or value.get("note")
    else:
        status = value
    cleaned = _clean(status) if status is not None else ""
    return cleaned or None


def extract_restriction_evidence(record: dict[str, Any]) -> NaraRestrictionEvidence:
    """Classify Sprint 1 public-domain candidate evidence from restriction fields."""
    if not record:
        return NaraRestrictionEvidence(
            decision="BLOCKED",
            use_restriction_status=None,
            access_restriction_status=None,
            rights_basis="missing_record",
        )

    use_status = extract_use_restriction(record)
    access_status = extract_access_restriction(record)
    if use_status == "Unrestricted" and (access_status in (None, "Unrestricted")):
        return NaraRestrictionEvidence(
            decision="ALLOWED",
            use_restriction_status=use_status,
            access_restriction_status=access_status,
            rights_basis="nara_unrestricted",
            rights_statement_uri=PUBLIC_DOMAIN_MARK_URI,
        )

    if use_status is None:
        basis = "missing_use_restriction"
    elif use_status != "Unrestricted":
        basis = "restricted_use"
    else:
        basis = "restricted_access"

    return NaraRestrictionEvidence(
        decision="BLOCKED",
        use_restriction_status=use_status,
        access_restriction_status=access_status,
        rights_basis=basis,
    )


def is_still_image_object(digital_object: dict[str, Any]) -> bool:
    """Return true for Sprint 1 still-image digital objects."""
    object_type = _clean(digital_object.get("objectType"))
    object_url = _clean(digital_object.get("objectUrl"))
    return bool(object_url) and object_type in IMAGE_OBJECT_TYPES


def extract_digital_objects(record: dict[str, Any]) -> list[NaraDigitalObject]:
    """Extract still-image digital object candidates from a NARA record."""
    na_id = extract_na_id(record)
    if not na_id:
        return []

    objects: list[NaraDigitalObject] = []
    for item in _as_list(record.get("digitalObjects")):
        if not isinstance(item, dict) or not is_still_image_object(item):
            continue
        object_id = _clean(item.get("objectId") or item.get("objectUrl"))
        object_url = _clean(item.get("objectUrl"))
        object_type = _clean(item.get("objectType"))
        if not object_id or not object_url:
            continue
        file_size = item.get("objectFileSize")
        objects.append(
            NaraDigitalObject(
                na_id=na_id,
                object_id=object_id,
                object_url=object_url,
                object_type=object_type,
                object_filename=_clean(item.get("objectFilename")) or None,
                object_description=_clean(item.get("objectDescription")) or None,
                object_file_size=int(file_size) if isinstance(file_size, int) else None,
            )
        )
    return objects


def build_public_domain_candidates(record: dict[str, Any]) -> list[NaraPublicDomainCandidate]:
    """Build evidence-only Sprint 1 candidates for unrestricted still-image records."""
    rights = extract_restriction_evidence(record)
    if not rights.allowed:
        return []

    na_id = extract_na_id(record)
    title = _clean(record.get("title"))
    if not na_id or not title:
        return []

    return [
        NaraPublicDomainCandidate(
            na_id=na_id,
            title=title,
            digital_object=digital_object,
            rights=rights,
        )
        for digital_object in extract_digital_objects(record)
    ]

