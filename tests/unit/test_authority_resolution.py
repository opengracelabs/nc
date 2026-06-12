import pytest

from services.data.authority_resolution import (
    AUTHORITY_RECORDS_BY_ANCHOR,
    AuthorityRecord,
    AuthorityResolutionError,
    get_authority_records,
    is_ratified_anchor,
    resolve_canonical_identity,
    resolve_identity,
    resolve_supported_identities,
    resolve_yellowstone_identity,
)


@pytest.mark.parametrize(
    ("anchor_slug", "canonical_place_id", "geonames_id", "wikidata_qid", "gbif_key"),
    [
        (
            "yellowstone",
            "geonames:5843591",
            "5843591",
            "Q351",
            "yellowstone-place-validation",
        ),
        (
            "grand-canyon",
            "geonames:5296401",
            "5296401",
            "Q220289",
            "grand-canyon-place-validation",
        ),
        (
            "great-barrier-reef",
            "geonames:2164628",
            "2164628",
            "Q7343",
            "great-barrier-reef-place-validation",
        ),
    ],
)
def test_ratified_places_resolve_to_one_canonical_place_id(
    anchor_slug: str,
    canonical_place_id: str,
    geonames_id: str,
    wikidata_qid: str,
    gbif_key: str,
) -> None:
    identity = resolve_identity(anchor_slug)

    assert identity.anchor_slug == anchor_slug
    assert identity.canonical_place_id == canonical_place_id
    assert identity.geonames_id == geonames_id
    assert identity.wikidata_qid == wikidata_qid
    assert identity.gbif_place_key == gbif_key
    assert sum(
        record.authority_role == "canonical_place_id"
        for record in identity.authority_records
    ) == 1


def test_yellowstone_resolves_to_one_canonical_place_id() -> None:
    identity = resolve_yellowstone_identity()

    assert identity.anchor_slug == "yellowstone"
    assert identity.canonical_place_id == "geonames:5843591"
    assert identity.geonames_id == "5843591"
    assert identity.wikidata_qid == "Q351"
    assert identity.gbif_place_key == "yellowstone-place-validation"


def test_supported_authority_records_keep_gbif_noncanonical() -> None:
    for records in AUTHORITY_RECORDS_BY_ANCHOR.values():
        roles = {
            record.authority: record.authority_role
            for record in records
        }

        assert roles["gbif"] == "validation_only"


def test_resolve_supported_identities_returns_ratified_only() -> None:
    identities = resolve_supported_identities()

    assert {identity.anchor_slug for identity in identities} == {
        "yellowstone",
        "grand-canyon",
        "great-barrier-reef",
    }


@pytest.mark.parametrize("anchor_slug", ["galapagos", "venice", "papahanaumokuakea"])
def test_unfixture_backed_places_are_registered_but_not_ratified(anchor_slug: str) -> None:
    records = get_authority_records(anchor_slug)

    assert not is_ratified_anchor(anchor_slug)
    assert records
    assert all(record.authority_role != "canonical_place_id" for record in records)
    with pytest.raises(AuthorityResolutionError, match="not ratified"):
        resolve_identity(anchor_slug)


def test_papahanaumokuakea_has_no_provisional_promotion() -> None:
    records = AUTHORITY_RECORDS_BY_ANCHOR["papahanaumokuakea"]
    roles = {record.authority: record.authority_role for record in records}
    geonames = next(record for record in records if record.authority == "geonames")
    wikidata = next(record for record in records if record.authority == "wikidata")

    assert roles == {
        "wikidata": "cross_reference",
        "geonames": "cross_reference",
        "gbif": "validation_only",
    }
    assert geonames.evidence["resolution_note"].startswith("Candidate only")
    assert wikidata.evidence["geonames_status"] == "unconfirmed"
    assert wikidata.evidence["ratification_status"] == "blocked_missing_fixture"
    assert "No provisional promotion" in wikidata.evidence["resolution_note"]


def test_resolution_rejects_multiple_canonical_place_ids() -> None:
    records = (
        AuthorityRecord("geonames", "5843591", "canonical_place_id", 1.0, {"name": "A"}),
        AuthorityRecord("geonames", "5844046", "canonical_place_id", 0.8, {"name": "B"}),
    )

    with pytest.raises(AuthorityResolutionError):
        resolve_canonical_identity("yellowstone", records)


def test_resolution_rejects_missing_canonical_place_id() -> None:
    records = (
        AuthorityRecord("wikidata", "Q351", "cross_reference", 0.9, {"label": "Yellowstone"}),
    )

    with pytest.raises(AuthorityResolutionError):
        resolve_canonical_identity("yellowstone", records)


def test_resolution_rejects_gbif_canonical_place_id() -> None:
    records = (
        AuthorityRecord("gbif", "bad-gbif-id", "canonical_place_id", 0.9, {"label": "Bad"}),
    )

    with pytest.raises(AuthorityResolutionError):
        resolve_canonical_identity("bad-place", records)


def test_resolution_rejects_unsupported_anchor_slug() -> None:
    with pytest.raises(AuthorityResolutionError):
        resolve_identity("not-a-pilot-place")
