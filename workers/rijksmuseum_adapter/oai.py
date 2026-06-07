"""Rijksmuseum OAI-PMH client."""
from __future__ import annotations

from typing import Any

import httpx

from .config import settings

EDM_METADATA_PREFIX = "edm"
OAI_DC_METADATA_PREFIX = "oai_dc"


def _drop_none(params: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in params.items() if value is not None}


async def _get_oai(params: dict[str, Any], http_client: httpx.AsyncClient | None = None) -> str:
    if http_client is not None:
        response = await http_client.get(settings.rijksmuseum_oai_base_url, params=params)
        response.raise_for_status()
        return response.text

    async with httpx.AsyncClient(timeout=settings.rijksmuseum_fetch_timeout_seconds) as client:
        response = await client.get(settings.rijksmuseum_oai_base_url, params=params)
        response.raise_for_status()
        return response.text


async def identify(*, http_client: httpx.AsyncClient | None = None) -> str:
    """Run OAI-PMH Identify."""
    return await _get_oai({"verb": "Identify"}, http_client=http_client)


async def list_metadata_formats(*, http_client: httpx.AsyncClient | None = None) -> str:
    """Run OAI-PMH ListMetadataFormats."""
    return await _get_oai({"verb": "ListMetadataFormats"}, http_client=http_client)


async def list_sets(*, http_client: httpx.AsyncClient | None = None) -> str:
    """Run OAI-PMH ListSets."""
    return await _get_oai({"verb": "ListSets"}, http_client=http_client)


async def list_identifiers(
    *,
    metadata_prefix: str = EDM_METADATA_PREFIX,
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
    metadata_prefix: str = EDM_METADATA_PREFIX,
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
    metadata_prefix: str = EDM_METADATA_PREFIX,
    http_client: httpx.AsyncClient | None = None,
) -> str:
    """Run OAI-PMH GetRecord for one Rijksmuseum LOD identifier."""
    params = {
        "verb": "GetRecord",
        "metadataPrefix": metadata_prefix,
        "identifier": identifier,
    }
    return await _get_oai(params, http_client=http_client)
