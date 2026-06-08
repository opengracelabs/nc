"""Gallica Document API and IIIF connectivity helpers."""
from __future__ import annotations

import re
from typing import Any
from urllib.parse import quote

import httpx

from .config import settings

_ARK_RE = re.compile(r"ark:/[0-9]+/[A-Za-z0-9]+")
_OAI_IDENTIFIER_RE = re.compile(
    r"<(?:[A-Za-z0-9_]+:)?identifier[^>]*>(.*?)</(?:[A-Za-z0-9_]+:)?identifier>",
    re.DOTALL,
)
_RESUMPTION_TOKEN_RE = re.compile(
    r"<(?:[A-Za-z0-9_]+:)?resumptionToken[^>]*>(.*?)</(?:[A-Za-z0-9_]+:)?resumptionToken>",
    re.DOTALL,
)


def _drop_none(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


def normalize_ark(value: str) -> str:
    """Return the canonical Gallica ARK from an ARK, URL, OAI id, or bare id."""
    raw = value.strip()
    if not raw:
        raise ValueError("missing_ark")

    match = _ARK_RE.search(raw)
    if match:
        return match.group(0)

    bare = raw.split("?", 1)[0].split("#", 1)[0].strip("/")
    if "/" in bare:
        bare = bare.rsplit("/", 1)[-1]
    if not bare:
        raise ValueError("missing_ark")
    return f"ark:/12148/{bare}"


def ark_id(value: str) -> str:
    """Return the terminal ARK identifier used by OCR request parameters."""
    return normalize_ark(value).rsplit("/", 1)[-1]


def quote_ark(value: str) -> str:
    """Quote an ARK for safe use inside path segments while preserving ARK separators."""
    return quote(normalize_ark(value), safe="/:")


async def _get_text(
    path: str,
    *,
    params: dict[str, Any] | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> str:
    url = f"{settings.gallica_base_url}{path}"
    if http_client is not None:
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        return response.text

    async with httpx.AsyncClient(timeout=settings.gallica_fetch_timeout_seconds) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.text


async def _get_oai(
    params: dict[str, Any],
    *,
    http_client: httpx.AsyncClient | None = None,
) -> str:
    if http_client is not None:
        response = await http_client.get(settings.gallica_oai_base_url, params=params)
        response.raise_for_status()
        return response.text

    async with httpx.AsyncClient(timeout=settings.gallica_fetch_timeout_seconds) as client:
        response = await client.get(settings.gallica_oai_base_url, params=params)
        response.raise_for_status()
        return response.text


async def fetch_oai_record(
    ark: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> str:
    """Fetch one Gallica document record using the Document API OAIRecord verb."""
    return await _get_text(
        "/services/OAIRecord",
        params={"ark": normalize_ark(ark)},
        http_client=http_client,
    )


async def fetch_pagination(
    ark: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> str:
    """Fetch page and folio information for one Gallica document."""
    return await _get_text(
        "/services/Pagination",
        params={"ark": normalize_ark(ark)},
        http_client=http_client,
    )


async def fetch_iiif_info(
    ark: str,
    page: int | str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch Gallica IIIF Image API info.json for a page."""
    response_text = await _get_text(
        f"/iiif/{quote_ark(ark)}/f{page}/info.json",
        http_client=http_client,
    )
    return httpx.Response(200, content=response_text.encode("utf-8")).json()


async def fetch_iiif_manifest(
    ark: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Fetch Gallica IIIF Presentation manifest for a document."""
    response_text = await _get_text(
        f"/iiif/{quote_ark(ark)}/manifest.json",
        http_client=http_client,
    )
    return httpx.Response(200, content=response_text.encode("utf-8")).json()


def build_iiif_info_url(ark: str, page: int | str) -> str:
    """Build a Gallica IIIF info.json URL."""
    return f"{settings.gallica_base_url}/iiif/{quote_ark(ark)}/f{page}/info.json"


def build_iiif_manifest_url(ark: str) -> str:
    """Build a Gallica IIIF Presentation manifest URL."""
    return f"{settings.gallica_base_url}/iiif/{quote_ark(ark)}/manifest.json"


def build_iiif_image_url(
    ark: str,
    page: int | str,
    *,
    region: str = "full",
    size: str = "full",
    rotation: str = "0",
    quality: str = "native.jpg",
) -> str:
    """Build a Gallica IIIF image URL for a page or region."""
    return (
        f"{settings.gallica_base_url}/iiif/{quote_ark(ark)}/f{page}/"
        f"{region}/{size}/{rotation}/{quality}"
    )


def extract_arks_from_xml(xml_text: str) -> list[str]:
    """Extract canonical Gallica ARKs from XML text in stable encounter order."""
    arks: list[str] = []
    seen: set[str] = set()
    for match in _ARK_RE.finditer(xml_text):
        ark = normalize_ark(match.group(0))
        if ark not in seen:
            arks.append(ark)
            seen.add(ark)
    return arks


def extract_oai_identifier(xml_text: str) -> str | None:
    """Extract the first OAI header identifier from an OAIRecord response."""
    match = _OAI_IDENTIFIER_RE.search(xml_text)
    if not match:
        return None
    identifier = match.group(1).strip()
    return identifier or None


def extract_resumption_token(xml_text: str) -> str | None:
    """Extract an OAI-PMH resumption token from ListIdentifiers/ListRecords XML."""
    match = _RESUMPTION_TOKEN_RE.search(xml_text)
    if not match:
        return None
    token = match.group(1).strip()
    return token or None


async def identify(*, http_client: httpx.AsyncClient | None = None) -> str:
    """Run OAI-PMH Identify against the Gallica OAI repository."""
    return await _get_oai({"verb": "Identify"}, http_client=http_client)


async def list_metadata_formats(*, http_client: httpx.AsyncClient | None = None) -> str:
    """Run OAI-PMH ListMetadataFormats."""
    return await _get_oai({"verb": "ListMetadataFormats"}, http_client=http_client)


async def list_sets(*, http_client: httpx.AsyncClient | None = None) -> str:
    """Run OAI-PMH ListSets."""
    return await _get_oai({"verb": "ListSets"}, http_client=http_client)


async def list_identifiers(
    *,
    metadata_prefix: str = "oai_dc",
    set_spec: str | None = None,
    from_: str | None = None,
    until: str | None = None,
    resumption_token: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> str:
    """Run OAI-PMH ListIdentifiers with selective harvest support."""
    if resumption_token:
        params = {"verb": "ListIdentifiers", "resumptionToken": resumption_token}
    else:
        params = _drop_none(
            {
                "verb": "ListIdentifiers",
                "metadataPrefix": metadata_prefix,
                "set": set_spec,
                "from": from_,
                "until": until,
            }
        )
    return await _get_oai(params, http_client=http_client)


async def list_records(
    *,
    metadata_prefix: str = "oai_dc",
    set_spec: str | None = None,
    from_: str | None = None,
    until: str | None = None,
    resumption_token: str | None = None,
    http_client: httpx.AsyncClient | None = None,
) -> str:
    """Run OAI-PMH ListRecords with selective harvest support."""
    if resumption_token:
        params = {"verb": "ListRecords", "resumptionToken": resumption_token}
    else:
        params = _drop_none(
            {
                "verb": "ListRecords",
                "metadataPrefix": metadata_prefix,
                "set": set_spec,
                "from": from_,
                "until": until,
            }
        )
    return await _get_oai(params, http_client=http_client)


async def get_record(
    identifier: str,
    *,
    metadata_prefix: str = "oai_dc",
    http_client: httpx.AsyncClient | None = None,
) -> str:
    """Run OAI-PMH GetRecord for one Gallica OAI identifier."""
    params = {
        "verb": "GetRecord",
        "metadataPrefix": metadata_prefix,
        "identifier": identifier,
    }
    return await _get_oai(params, http_client=http_client)
