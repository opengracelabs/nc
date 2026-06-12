"""Authority resolution registry helpers for NC-DATA authority records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class AuthorityResolutionError(ValueError):
    """Raised when authority records cannot resolve to one canonical identity."""


@dataclass(frozen=True)
class AuthorityRecord:
    authority: str
    authority_record_id: str
    authority_role: str
    confidence: float
    evidence: dict[str, Any]


@dataclass(frozen=True)
class CanonicalIdentity:
    canonical_place_id: str
    anchor_slug: str
    label: str
    geonames_id: str | None
    wikidata_qid: str | None
    gbif_place_key: str | None
    authority_records: tuple[AuthorityRecord, ...]


def _record(
    authority: str,
    authority_record_id: str,
    authority_role: str,
    confidence: float,
    **evidence: Any,
) -> AuthorityRecord:
    return AuthorityRecord(
        authority=authority,
        authority_record_id=authority_record_id,
        authority_role=authority_role,
        confidence=confidence,
        evidence=evidence,
    )


AUTHORITY_RECORDS_BY_ANCHOR: dict[str, tuple[AuthorityRecord, ...]] = {
    "yellowstone": (
        _record(
            "geonames",
            "5843591",
            "canonical_place_id",
            1.0,
            name="Yellowstone National Park",
            feature_code="PRKA",
            source_url="https://www.geonames.org/5843591",
        ),
        _record(
            "wikidata",
            "Q351",
            "cross_reference",
            0.92,
            label="Yellowstone National Park",
            geonames_id_claim="5844046",
            source_url="https://www.wikidata.org/wiki/Q351",
            resolution_note="Wikidata is identity evidence, not canonical place ID.",
        ),
        _record(
            "gbif",
            "yellowstone-place-validation",
            "validation_only",
            0.75,
            source_role="validation_only",
            media_allowed=False,
            resolution_note="GBIF evidence validates biodiversity relevance only.",
        ),
    ),
    "grand-canyon": (
        _record(
            "geonames",
            "5296401",
            "canonical_place_id",
            1.0,
            name="Grand Canyon National Park",
            feature_code="PRK",
            source_url="https://www.geonames.org/5296401",
        ),
        _record(
            "wikidata",
            "Q220289",
            "cross_reference",
            0.97,
            label="Grand Canyon National Park",
            geonames_id_claim="5296401",
            source_url="https://www.wikidata.org/wiki/Q220289",
        ),
        _record(
            "gbif",
            "grand-canyon-place-validation",
            "validation_only",
            0.7,
            source_role="validation_only",
            media_allowed=False,
        ),
    ),
    "great-barrier-reef": (
        _record(
            "geonames",
            "2164628",
            "canonical_place_id",
            1.0,
            name="Great Barrier Reef",
            feature_code="RF",
            source_url="https://www.geonames.org/2164628",
        ),
        _record(
            "wikidata",
            "Q7343",
            "cross_reference",
            0.97,
            label="Great Barrier Reef",
            geonames_id_claim="2164628",
            source_url="https://www.wikidata.org/wiki/Q7343",
        ),
        _record(
            "gbif",
            "great-barrier-reef-place-validation",
            "validation_only",
            0.7,
            source_role="validation_only",
            media_allowed=False,
        ),
    ),
    "galapagos": (
        _record(
            "geonames",
            "3658931",
            "cross_reference",
            0.82,
            name="Galapagos Islands",
            feature_code="ISLS",
            source_url="https://www.geonames.org/3658931",
            ratification_status="blocked_missing_fixture",
        ),
        _record(
            "wikidata",
            "Q38095",
            "cross_reference",
            0.97,
            label="Galapagos Islands",
            geonames_id_claim="3658931",
            source_url="https://www.wikidata.org/wiki/Q38095",
        ),
        _record(
            "gbif",
            "galapagos-place-validation",
            "validation_only",
            0.7,
            source_role="validation_only",
            media_allowed=False,
        ),
    ),
    "venice": (
        _record(
            "geonames",
            "3164603",
            "cross_reference",
            0.82,
            name="Venice",
            feature_code="PPLA",
            source_url="https://www.geonames.org/3164603",
            ratification_status="blocked_missing_fixture",
        ),
        _record(
            "wikidata",
            "Q641",
            "cross_reference",
            0.97,
            label="Venice",
            geonames_id_claim="3164603",
            source_url="https://www.wikidata.org/wiki/Q641",
        ),
        _record(
            "gbif",
            "venice-place-validation",
            "validation_only",
            0.55,
            source_role="validation_only",
            media_allowed=False,
        ),
    ),
    "papahanaumokuakea": (
        _record(
            "wikidata",
            "Q787425",
            "cross_reference",
            0.72,
            name="Papahanaumokuakea Marine National Monument",
            label="Papahanaumokuakea Marine National Monument",
            diacritics="Papahānaumokuākea",
            geonames_status="unconfirmed",
            ratification_status="blocked_missing_fixture",
            resolution_note=(
                "No provisional promotion; requires fixture-backed evidence before "
                "ratification."
            ),
            source_url="https://www.wikidata.org/wiki/Q787425",
        ),
        _record(
            "geonames",
            "11854341",
            "cross_reference",
            0.35,
            name="Papahanaumokuakea candidate",
            source_url="https://www.geonames.org/11854341",
            resolution_note=(
                "Candidate only; not canonical until confirmed by NC GeoNames account lookup."
            ),
        ),
        _record(
            "gbif",
            "papahanaumokuakea-place-validation",
            "validation_only",
            0.7,
            source_role="validation_only",
            media_allowed=False,
        ),
    ),
}

RATIFIED_ANCHOR_SLUGS = frozenset({"yellowstone", "grand-canyon", "great-barrier-reef"})

YELLOWSTONE_AUTHORITY_RECORDS = AUTHORITY_RECORDS_BY_ANCHOR["yellowstone"]


def get_authority_records(anchor_slug: str) -> tuple[AuthorityRecord, ...]:
    try:
        return AUTHORITY_RECORDS_BY_ANCHOR[anchor_slug]
    except KeyError as exc:
        raise AuthorityResolutionError(f"unsupported anchor slug: {anchor_slug}") from exc


def is_ratified_anchor(anchor_slug: str) -> bool:
    return anchor_slug in RATIFIED_ANCHOR_SLUGS


def resolve_canonical_identity(
    anchor_slug: str,
    records: tuple[AuthorityRecord, ...],
) -> CanonicalIdentity:
    canonical = [
        record for record in records if record.authority_role == "canonical_place_id"
    ]
    if len(canonical) != 1:
        raise AuthorityResolutionError("exactly one canonical place ID is required")

    canonical_record = canonical[0]
    if canonical_record.authority == "gbif":
        raise AuthorityResolutionError("GBIF records cannot be canonical place IDs")
    if canonical_record.authority not in {"geonames", "wikidata"}:
        raise AuthorityResolutionError("unsupported canonical authority")

    wikidata = next((record for record in records if record.authority == "wikidata"), None)
    gbif = next((record for record in records if record.authority == "gbif"), None)
    label = (
        canonical_record.evidence.get("name")
        or canonical_record.evidence.get("label")
        or anchor_slug
    )
    return CanonicalIdentity(
        canonical_place_id=(
            f"{canonical_record.authority}:{canonical_record.authority_record_id}"
        ),
        anchor_slug=anchor_slug,
        label=str(label),
        geonames_id=(
            canonical_record.authority_record_id
            if canonical_record.authority == "geonames"
            else None
        ),
        wikidata_qid=wikidata.authority_record_id if wikidata else None,
        gbif_place_key=gbif.authority_record_id if gbif else None,
        authority_records=records,
    )


def resolve_identity(anchor_slug: str) -> CanonicalIdentity:
    records = get_authority_records(anchor_slug)
    if not is_ratified_anchor(anchor_slug):
        raise AuthorityResolutionError(
            f"anchor is not ratified with fixture-backed evidence: {anchor_slug}"
        )
    return resolve_canonical_identity(anchor_slug, records)


def resolve_supported_identities() -> tuple[CanonicalIdentity, ...]:
    return tuple(resolve_identity(slug) for slug in RATIFIED_ANCHOR_SLUGS)


def resolve_yellowstone_identity() -> CanonicalIdentity:
    return resolve_identity("yellowstone")
