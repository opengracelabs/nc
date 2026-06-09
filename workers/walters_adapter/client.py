"""Deterministic CSV client for the official Walters Open Data files."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from .config import settings

ART_CSV = "art.csv"
MEDIA_CSV = "media.csv"
CREATORS_CSV = "creators.csv"

REQUIRED_CSV_FILES = (
    ART_CSV,
    MEDIA_CSV,
    CREATORS_CSV,
)


@dataclass(frozen=True)
class WaltersDataset:
    """Loaded Walters CSV rows and deterministic indexes for Sprint 1 operations."""

    art: list[dict[str, str]]
    media: list[dict[str, str]]
    creators: list[dict[str, str]]

    def __post_init__(self) -> None:
        object.__setattr__(self, "objects_by_id", _index_unique(self.art, "ObjectID"))
        object.__setattr__(self, "media_by_object_id", _index_many(self.media, "ObjectID"))
        object.__setattr__(self, "creators_by_id", _index_unique(self.creators, "id"))


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


def split_pipe_values(value: Any) -> list[str]:
    """Split Walters pipe-delimited CSV fields while dropping blank values."""
    return [part.strip() for part in _clean_key(value).split("|") if part.strip()]


def csv_url(filename: str) -> str:
    """Build the official raw GitHub URL for one Walters Open Data CSV."""
    cleaned = filename.strip()
    if cleaned not in REQUIRED_CSV_FILES:
        raise ValueError("unsupported_walters_csv")
    return f"{settings.walters_opendata_base_url}/{cleaned}"


def load_csv_text(text: str) -> list[dict[str, str]]:
    """Parse CSV text into deterministic dictionaries."""
    reader = csv.DictReader(text.splitlines())
    if reader.fieldnames is None:
        return []
    return [dict(row) for row in reader]


def load_csv_file(path: Path | str) -> list[dict[str, str]]:
    """Load one UTF-8 Walters CSV file from disk."""
    return load_csv_text(Path(path).read_text(encoding="utf-8-sig"))


async def fetch_csv(
    filename: str,
    *,
    http_client: httpx.AsyncClient | None = None,
) -> list[dict[str, str]]:
    """Fetch one official Walters CSV and parse it."""
    url = csv_url(filename)
    headers = {"User-Agent": settings.walters_user_agent}
    if http_client is not None:
        response = await http_client.get(url, headers=headers)
        response.raise_for_status()
        return load_csv_text(response.text)

    async with httpx.AsyncClient(timeout=settings.walters_fetch_timeout_seconds) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return load_csv_text(response.text)


def load_dataset(directory: Path | str) -> WaltersDataset:
    """Load the Sprint 1 required Walters CSV files from one directory."""
    root = Path(directory)
    missing = [name for name in REQUIRED_CSV_FILES if not (root / name).exists()]
    if missing:
        raise FileNotFoundError(f"missing_walters_csv:{','.join(missing)}")
    return WaltersDataset(
        art=load_csv_file(root / ART_CSV),
        media=load_csv_file(root / MEDIA_CSV),
        creators=load_csv_file(root / CREATORS_CSV),
    )


def get_object(dataset: WaltersDataset, object_id: int | str) -> dict[str, str] | None:
    """Return one Walters object row by ObjectID."""
    cleaned = _clean_key(object_id)
    if not cleaned:
        raise ValueError("missing_object_id")
    return dataset.objects_by_id.get(cleaned)


def is_image_media(row: dict[str, str]) -> bool:
    """Return true when a Walters media row is an image with a usable URL."""
    return (
        _clean_key(row.get("MediaType")).lower() == "image"
        and bool(_clean_key(row.get("ImageURL")))
    )


def is_primary_image(row: dict[str, str]) -> bool:
    """Return true when Walters marks a media row as primary."""
    return _clean_key(row.get("IsPrimary")) == "1"


def get_images_for_object(
    dataset: WaltersDataset,
    object_id: int | str,
) -> list[dict[str, str]]:
    """Return image media rows for one object in deterministic display order."""
    cleaned = _clean_key(object_id)
    if not cleaned:
        raise ValueError("missing_object_id")
    rows = [row for row in dataset.media_by_object_id.get(cleaned, []) if is_image_media(row)]
    return sorted(
        rows,
        key=lambda row: (
            0 if is_primary_image(row) else 1,
            _int_sort_value(row.get("Rank")),
            _int_sort_value(row.get("MediaXrefID")),
            _clean_key(row.get("Filename")),
        ),
    )


def select_primary_image(rows: list[dict[str, str]]) -> dict[str, str] | None:
    """Select the preferred Walters image row deterministically."""
    candidates = [row for row in rows if is_image_media(row)]
    if not candidates:
        return None
    return sorted(
        candidates,
        key=lambda row: (
            0 if is_primary_image(row) else 1,
            _int_sort_value(row.get("Rank")),
            _int_sort_value(row.get("MediaXrefID")),
            _clean_key(row.get("Filename")),
        ),
    )[0]


def get_primary_image(dataset: WaltersDataset, object_id: int | str) -> dict[str, str] | None:
    """Return the preferred image for one Walters object."""
    return select_primary_image(get_images_for_object(dataset, object_id))


def get_creators_for_object(
    dataset: WaltersDataset,
    object_id: int | str,
) -> list[dict[str, str]]:
    """Return creator rows associated with one object in art.Creators order."""
    object_row = get_object(dataset, object_id)
    if object_row is None:
        return []
    rows: list[dict[str, str]] = []
    for creator_id in split_pipe_values(object_row.get("Creators")):
        creator = dataset.creators_by_id.get(creator_id)
        if creator is not None:
            rows.append(creator)
    return rows


def search_objects(
    dataset: WaltersDataset,
    *,
    query: str | None = None,
    classification: str | None = None,
    has_image: bool | None = None,
    limit: int | None = None,
) -> list[dict[str, str]]:
    """Search loaded Walters objects with deterministic ordering by ObjectID."""
    if limit is not None and limit < 1:
        raise ValueError("invalid_limit")
    cleaned_query = query.strip().lower() if isinstance(query, str) and query.strip() else None
    cleaned_classification = (
        classification.strip().lower()
        if isinstance(classification, str) and classification.strip()
        else None
    )

    results: list[dict[str, str]] = []
    for row in sorted(dataset.art, key=lambda item: _int_sort_value(item.get("ObjectID"))):
        if cleaned_query:
            searchable = " ".join(
                _clean_key(row.get(key))
                for key in ("Title", "ObjectNumber", "ObjectName", "Culture", "Medium")
            ).lower()
            if cleaned_query not in searchable:
                continue
        if (
            cleaned_classification
            and _clean_key(row.get("Classification")).lower() != cleaned_classification
        ):
            continue
        if has_image is True and get_primary_image(dataset, row.get("ObjectID", "")) is None:
            continue
        results.append(row)
        if limit is not None and len(results) >= limit:
            break
    return results
