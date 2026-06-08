from pathlib import Path

import httpx

from workers.gallica_adapter.client import (
    ark_id,
    build_iiif_image_url,
    build_iiif_info_url,
    build_iiif_manifest_url,
    extract_arks_from_xml,
    extract_oai_identifier,
    extract_resumption_token,
    fetch_iiif_info,
    fetch_iiif_manifest,
    fetch_oai_record,
    fetch_pagination,
    get_record,
    identify,
    list_identifiers,
    list_metadata_formats,
    list_records,
    list_sets,
    normalize_ark,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "gallica"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_normalize_ark_accepts_bare_ark_url_and_oai_identifier() -> None:
    assert normalize_ark("btv1b53066668g") == "ark:/12148/btv1b53066668g"
    assert normalize_ark("ark:/12148/btv1b53066668g") == "ark:/12148/btv1b53066668g"
    assert (
        normalize_ark("https://gallica.bnf.fr/ark:/12148/btv1b53066668g/f1")
        == "ark:/12148/btv1b53066668g"
    )
    assert (
        normalize_ark("oai:bnf.fr:gallica/ark:/12148/btv1b53066668g")
        == "ark:/12148/btv1b53066668g"
    )
    assert ark_id("ark:/12148/btv1b53066668g") == "btv1b53066668g"


def test_build_iiif_urls_are_deterministic() -> None:
    ark = "ark:/12148/btv1b53066668g"

    assert build_iiif_info_url(ark, 1) == (
        "https://gallica.bnf.fr/iiif/ark:/12148/btv1b53066668g/f1/info.json"
    )
    assert build_iiif_manifest_url(ark) == (
        "https://gallica.bnf.fr/iiif/ark:/12148/btv1b53066668g/manifest.json"
    )
    assert build_iiif_image_url(ark, 12, region="349,272,923,1346") == (
        "https://gallica.bnf.fr/iiif/ark:/12148/btv1b53066668g/f12/"
        "349,272,923,1346/full/0/native.jpg"
    )


async def test_fetch_oai_record_requests_document_api_oairecord() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, text=fixture("oairecord_image.xml"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        body = await fetch_oai_record("btv1b53066668g", http_client=client)

    assert seen[0].url.path == "/services/OAIRecord"
    assert seen[0].url.params["ark"] == "ark:/12148/btv1b53066668g"
    assert "Carte de test Gallica" in body


async def test_fetch_pagination_requests_document_api_pagination() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, text=fixture("pagination.xml"))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        body = await fetch_pagination("ark:/12148/btv1b53066668g", http_client=client)

    assert seen[0].url.path == "/services/Pagination"
    assert seen[0].url.params["ark"] == "ark:/12148/btv1b53066668g"
    assert "<nbVueImages>2</nbVueImages>" in body


async def test_fetch_iiif_info_and_manifest_parse_json() -> None:
    paths = []

    def handler(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        if request.url.path.endswith("/info.json"):
            return httpx.Response(200, json={"width": 1200, "height": 900})
        return httpx.Response(200, json={"id": str(request.url), "type": "Manifest"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        info = await fetch_iiif_info("btv1b53066668g", 1, http_client=client)
        manifest = await fetch_iiif_manifest("btv1b53066668g", http_client=client)

    assert paths == [
        "/iiif/ark:/12148/btv1b53066668g/f1/info.json",
        "/iiif/ark:/12148/btv1b53066668g/manifest.json",
    ]
    assert info == {"width": 1200, "height": 900}
    assert manifest["type"] == "Manifest"


def test_xml_extractors_support_replay_fixtures() -> None:
    oairecord = fixture("oairecord_image.xml")
    resumption = fixture("oai_resumption.xml")

    assert extract_arks_from_xml(oairecord) == ["ark:/12148/btv1b53066668g"]
    assert (
        extract_oai_identifier(oairecord)
        == "oai:bnf.fr:gallica/ark:/12148/btv1b53066668g"
    )
    assert extract_resumption_token(resumption) == "next-token"


async def test_oai_harvest_verbs_and_resumption_token_requests() -> None:
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, text="<ok />")

    record_page_token = "-".join(["next", "token"])

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await identify(http_client=client)
        await list_metadata_formats(http_client=client)
        await list_sets(http_client=client)
        await list_identifiers(
            set_spec="gallica:typedoc:images",
            from_="2025-01-01",
            until="2025-02-01",
            http_client=client,
        )
        await list_records(resumption_token=record_page_token, http_client=client)
        await get_record(
            "oai:bnf.fr:gallica/ark:/12148/btv1b53066668g",
            http_client=client,
        )

    params = [request.url.params for request in requests]
    assert params[0]["verb"] == "Identify"
    assert params[1]["verb"] == "ListMetadataFormats"
    assert params[2]["verb"] == "ListSets"
    assert params[3]["verb"] == "ListIdentifiers"
    assert params[3]["metadataPrefix"] == "oai_dc"
    assert params[3]["set"] == "gallica:typedoc:images"
    assert params[3]["from"] == "2025-01-01"
    assert params[3]["until"] == "2025-02-01"
    assert dict(params[4]) == {"verb": "ListRecords", "resumptionToken": "next-token"}
    assert params[5]["verb"] == "GetRecord"
    assert params[5]["identifier"] == "oai:bnf.fr:gallica/ark:/12148/btv1b53066668g"
