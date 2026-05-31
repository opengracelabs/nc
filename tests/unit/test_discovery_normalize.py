from workers.discovery_worker.normalize import normalize_wikidata
from workers.discovery_worker.sources.base import RawRecord


def binding(value: str) -> dict:
    return {"value": value}


def test_wikidata_normalization_keeps_qid_as_source_id() -> None:
    record = RawRecord(
        source_id="Q123",
        payload={
            "siteLabel": binding("Example Site"),
            "whc_id": binding("31"),
            "countryCode": binding("au"),
            "lat": binding("-33.8"),
            "lon": binding("151.2"),
            "inscriptionYear": binding("1981"),
        },
    )

    normalized = normalize_wikidata(record)

    assert normalized["source_id"] == "Q123"
    assert normalized["wikidata_qid"] == "Q123"
    assert normalized["external_ids"] == {"whc_id": "31"}
    assert normalized["country_codes"] == ["AU"]
    assert normalized["centroid"] == {"type": "Point", "coordinates": [151.2, -33.8]}
