from enum import StrEnum
from typing import Any

from pydantic import Field

from .base import NCBase, NCRecord


class HeritageType(StrEnum):
    CULTURAL = "cultural"
    NATURAL = "natural"
    MIXED = "mixed"


class PlaceStatus(StrEnum):
    CANDIDATE = "candidate"       # approved discovery candidate, not yet fully ingested
    ACTIVE = "active"             # ingested and published
    ENDANGERED = "endangered"     # on UNESCO danger list
    DELISTED = "delisted"         # removed from inscription
    DEPRECATED = "deprecated"     # internal — superseded by a merged record


class Place(NCRecord):
    """Canonical record for a cultural or ecological place."""

    # Identity
    wikidata_qid: str | None = None
    geonames_id: str | None = None
    osm_relation_id: int | None = None
    source_id: str | None = None           # originating source's own identifier
    source: str | None = None              # e.g. "unesco_whc"
    unesco_ref_id: str | None = None       # e.g. "123bis"

    # Names and descriptions — {ISO 639-1 lang: value}
    name: dict[str, str] = Field(default_factory=dict)
    description: dict[str, str] = Field(default_factory=dict)
    statement_of_ouv: dict[str, str] = Field(default_factory=dict)
    justification: dict[str, str] = Field(default_factory=dict)

    # Classification
    heritage_type: HeritageType | None = None
    ouv_criteria: list[str] = Field(default_factory=list)   # ["i", "ii", "vii"]
    category_skos: list[str] = Field(default_factory=list)  # SKOS concept URIs
    transboundary: bool = False

    # Geography
    country_codes: list[str] = Field(default_factory=list)  # ISO 3166-1 alpha-2
    continent: str | None = None
    centroid: dict[str, Any] | None = None      # GeoJSON Point
    boundary: dict[str, Any] | None = None      # GeoJSON Polygon / MultiPolygon
    area_ha: float | None = None
    core_area_ha: float | None = None
    buffer_area_ha: float | None = None
    spatial_precision: str | None = None        # 'approximate', 'surveyed'

    # Inscription
    inscription_year: int | None = None
    inscription_date: str | None = None         # ISO 8601
    endangered_since: str | None = None         # ISO 8601

    # Status
    status: PlaceStatus = PlaceStatus.CANDIDATE

    # Enrichment
    confidence_score: float | None = None       # 0.0–1.0
    agent_notes: dict[str, Any] = Field(default_factory=dict)


class PlaceCreate(NCBase):  # NCBase, no auto-id
    name: dict[str, str]
    source: str
    source_id: str


class PlacePatch(NCBase):
    name: dict[str, str] | None = None
    description: dict[str, str] | None = None
    heritage_type: HeritageType | None = None
    ouv_criteria: list[str] | None = None
    country_codes: list[str] | None = None
    centroid: dict[str, Any] | None = None
    boundary: dict[str, Any] | None = None
    inscription_year: int | None = None
    status: PlaceStatus | None = None
    wikidata_qid: str | None = None
    geonames_id: str | None = None
    osm_relation_id: int | None = None
