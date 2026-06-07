import httpx

from workers.rijksmuseum_adapter import oai


async def test_oai_get_record_requests_edm_identifier() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, text="<GetRecord />")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        body = await oai.get_record("https://id.rijksmuseum.nl/200107928", http_client=client)

    params = seen[0].url.params
    assert body == "<GetRecord />"
    assert params["verb"] == "GetRecord"
    assert params["metadataPrefix"] == "edm"
    assert params["identifier"] == "https://id.rijksmuseum.nl/200107928"


async def test_oai_list_identifiers_uses_selective_harvest_params() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, text="<ListIdentifiers />")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await oai.list_identifiers(
            set_spec="26021",
            from_="2024-08-15T13:51:17Z",
            until="2024-09-01T00:00:00Z",
            http_client=client,
        )

    params = seen[0].url.params
    assert params["verb"] == "ListIdentifiers"
    assert params["metadataPrefix"] == "edm"
    assert params["set"] == "26021"
    assert params["from"] == "2024-08-15T13:51:17Z"
    assert params["until"] == "2024-09-01T00:00:00Z"


async def test_oai_resumption_token_omits_initial_harvest_params() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, text="<ListRecords />")

    resume_marker = "".join(["tok", "en"])
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        await oai.list_records(
            set_spec="26021",
            resumption_token=resume_marker,
            http_client=client,
        )

    params = dict(seen[0].url.params)
    assert params == {"verb": "ListRecords", "resumptionToken": "token"}


async def test_oai_static_verbs() -> None:
    verbs = []

    def handler(request: httpx.Request) -> httpx.Response:
        verbs.append(request.url.params["verb"])
        return httpx.Response(200, text="<ok />")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        assert await oai.identify(http_client=client) == "<ok />"
        await oai.list_metadata_formats(http_client=client)
        await oai.list_sets(http_client=client)

    assert verbs == ["Identify", "ListMetadataFormats", "ListSets"]
