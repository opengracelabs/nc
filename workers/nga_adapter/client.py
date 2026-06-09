"""Deterministic CSV client for the official NGA Open Data dataset."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from .config import settings

OBJECTS_CSV = "objects.csv"
PUBLISHED_IMAGES_CSV = "published_images.csv"
OBJECTS_CONSTITUENTS_CSV = "objects_constituents.csv"
CONSTITUENTS_CSV = "constituents.csv"
OBJECTS_TERMS_CSV = "objects_terms.csv"

REQUIRED_CSV_FILES = (
    OBJECTS_CSV,
    PUBLISHED_IMAGES_CSV,
    OBJECTS_CONSTITUENTS_CSV,
    CONSTITUENTS_CSV,
    OBJECTS_TERMS_CSV,
)


@dataclass(frozen=True)
class NgaDataset:
    """Loaded NGA CSV rows and deterministic indexes for Sprint 1 operations."""

    objects: list[dict[str, str]]
    published_images: list[dict[str, str]]
    objects_constituents: list[dict[str, str]]
    constituents: list[dict[str, str]]
    objects_terms: list[dict[str, str]]

    def __post_init__(self) -> None:
        object.__setattr__(self, "objects_by_id", _index_unique(self.objects, "objectid"))
        object.__setattr__(
            self,
            "images_by_object_id",
            _index_many(self.published_images, "depictstmsobjectid"),
        )
        object.__setattr__(
            self,
            "terms_by_object_id",
            _index_many(self.objects_terms, "objectid"),
        )
        object.__setattr__(
            self,
            "object_constituents_by_object_id",
            _index_many(self.objects_constituents, "objectid"),
        )
        object.__setattr__(
            self,
            "constituents_by_id",
            _index_unique(self.constituents, "constituentid"),
        )


def _clean_key(value: Any) -> str:
    return str(value).strip()


def _index_unique(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        value = _clean_key(row.get(key, ""))
        if value and value not in indexed:
            indexed[value] = row
    return indexed


def _index_many(rows: list[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    indexed: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        value = _clean_key(row.get(key, ""))
        if value:
            indexed.setdefault(value, []).append(row)
    return indexed


def _int_sort_value(value: Any) -> tuple[int, int | str]:
    cleaned = _clean_key(value)
    if not cleaned:
        return (1, "")
    try:
        return (0, int(cleaned))
    except ValueError:
        return (0, cleaned)


def csv_url(filename: str) -> str:
    """Build the official raw GitHub URL for one NGA Open Data CSV."""
    cleaned = filename.strip()
    if cleaned not in REQUIRED_CSV_FILES:
        raise ValueError("unsupported_nga_csv")
    return f"{settings.nga_opendata_base_url}/{cleaned}"


def load_csv_text(text: str) -> list[dict[str, str]]:
    """Parse CSV text into deterministic dictionaries."""
    reader = csv.DictReader(text.splitlines())
    if reader.fieldnames is None:
        return []
    return [dict(row) for row in reader]


def load_csv_file(path: Path | str) -> list[dict[str, str]]:
    """Load one UTF-8 NGA CSV file from disk."""
    return load_csv_text(Path(path).read_text(encoding="utf-8-sig"))


async def fetch_csv(
    filename: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> list[dict[str, str]]:
    """Fetch one official NGA CSV and parse it."""
    url = csv_url(filename)
    headers = {"User-Agent": settings.nga_user_agent}
    if http_client is not None:
        response = await http_client.get(url, headers=headers)
        response.raise_for_status()
        return load_csv_text(response.text)

    async with httpx.AsyncClient(timeout=settings.nga_fetch_timeout_seconds) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return load_csv_text(response.text)


def load_dataset(directory: Path | str) -> NgaDataset:
    """Load the Sprint 1 required NGA CSV files from one directory."""
    root = Path(directory)
    missing = [name for name in REQUIRED_CSV_FILES if not (root / name).exists()]
    if missing:
        raise FileNotFoundError(f"missing_nga_csv:{','.join(missing)}")
    return NgaDataset(
        objects=load_csv_file(root / OBJECTS_CSV),
        published_images=load_csv_file(root / PUBLISHED_IMAGES_CSV),
        objects_constituents=load_csv_file(root / OBJECTS_CONSTITUENTS_CSV),
        constituents=load_csv_file(root / CONSTITUENTS_CSV),
        objects_terms=load_csv_file(root / OBJECTS_TERMS_CSV),
    )


def get_object(dataset: NgaDataset, object_id: int | str) -> dict[str, str] | None:
    """Return one NGA object row by objectid."""
    cleaned = _clean_key(object_id)
    if not cleaned:
        raise ValueError("missing_object_id")
    return dataset.objects_by_id.get(cleaned)


def get_images_for_object(dataset: NgaDataset, object_id: int | str) -> list[dict[str, str]]:
    """Return all published image rows for one object in deterministic order."""
    cleaned = _clean_key(object_id)
    if not cleaned:
        raise ValueError("missing_object_id")
    rows = list(dataset.images_by_object_id.get(cleaned, []))
    return sorted(
        rows,
        key=lambda row: (
            _int_sort_value(row.get("sequence")),
            _clean_key(row.get("viewtype")),
            _clean_key(row.get("uuid")),
        ),
    )


def is_openaccess_image(row: dict[str, str]) -> bool:
    """Return true when an NGA published image is open access with a IIIF URL."""
    return _clean_key(row.get("openaccess")) == "1" and bool(_clean_key(row.get("iiifurl")))


def select_primary_image(rows: list[dict[str, str]]) -> dict[str, str] | None:
    """Select the preferred open-access image row deterministically."""
    candidates = [row for row in rows if is_openaccess_image(row)]
    if not candidates:
        return None
    return sorted(
        candidates,
        key=lambda row: (
            0 if _clean_key(row.get("viewtype")).lower() == "primary" else 1,
            _int_sort_value(row.get("sequence")),
            _clean_key(row.get("uuid")),
        ),
    )[0]


def get_primary_image(dataset: NgaDataset, object_id: int | str) -> dict[str, str] | None:
    """Return the preferred open-access published image for one object."""
    return select_primary_image(get_images_for_object(dataset, object_id))


def get_terms_for_object(dataset: NgaDataset, object_id: int | str) -> list[dict[str, str]]:
    """Return NGA object term rows in deterministic termtype/term order."""
    cleaned = _clean_key(object_id)
    if not cleaned:
        raise ValueError("missing_object_id")
    return sorted(
        dataset.terms_by_object_id.get(cleaned, []),
        key=lambda row: (_clean_key(row.get("termtype")), _clean_key(row.get("term"))),
    )


def get_constituents_for_object(dataset: NgaDataset, object_id: int | str) -> list[dict[str, str]]:
    """Return constituent rows associated with one object in display order."""
    cleaned = _clean_key(object_id)
    if not cleaned:
        raise ValueError("missing_object_id")
    links = sorted(
        dataset.object_constituents_by_object_id.get(cleaned, []),
        key=lambda row: _int_sort_value(row.get("displayorder")),
    )
    rows: list[dict[str, str]] = []
    for link in links:
        constituent = dataset.constituents_by_id.get(_clean_key(link.get("constituentid")))
        if constituent is not None:
            rows.append({**constituent, "object_role": link.get("role", "")})
    return rows


def search_objects(
    dataset: NgaDataset,
    *,
    query: str | None = None,
    classification: str | None = None,
    openaccess: bool | None = None,
    limit: int | None = None,
) -> list[dict[str, str]]:
    """Search loaded NGA objects with deterministic ordering by objectid."""
    if limit is not None and limit < 1:
        raise ValueError("invalid_limit")
    cleaned_query = query.strip().lower() if isinstance(query, str) and query.strip() else None
    cleaned_classification = (
        classification.strip().lower()
        if isinstance(classification, str) and classification.strip()
        else None
    )

    results: list[dict[str, str]] = []
    for row in sorted(dataset.objects, key=lambda item: _int_sort_value(item.get("objectid"))):
        if cleaned_query:
            searchable = " ".join(
                _clean_key(row.get(key))
                for key in ("title", "attribution", "accessionnum", "medium")
            ).lower()
            if cleaned_query not in searchable:
                continue
        if (
            cleaned_classification
            and _clean_key(row.get("classification")).lower() != cleaned_classification
        ):
            continue
        if openaccess is True and get_primary_image(dataset, row.get("objectid", "")) is None:
            continue
        results.append(row)
        if limit is not None and len(results) >= limit:
            break
    return results
