"""Fixture acquisition inventory helpers for authority evidence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class FixtureAcquisitionError(ValueError):
    """Raised when an acquired fixture bundle is incomplete or unsafe."""


@dataclass(frozen=True)
class FixtureCapture:
    provider: str
    kind: str
    path: Path
    payload: dict[str, Any]


@dataclass(frozen=True)
class FixtureInventory:
    anchor_slug: str
    provider: str
    fixture_dir: Path
    captures: tuple[FixtureCapture, ...]
    canonical_assignment: bool

    @property
    def capture_kinds(self) -> tuple[str, ...]:
        return tuple(capture.kind for capture in self.captures)


def fixture_dir_name(anchor_slug: str) -> str:
    """Convert an anchor slug to the fixture directory naming convention."""
    return anchor_slug.replace("-", "_")


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise FixtureAcquisitionError(f"fixture is not a JSON object: {path}")
    return data


def load_fixture_inventory(fixture_dir: Path | str) -> FixtureInventory:
    """Load one provider fixture directory and verify its manifest inventory."""
    directory = Path(fixture_dir)
    manifest_path = directory / "manifest.json"
    if not manifest_path.exists():
        raise FixtureAcquisitionError(f"missing fixture manifest: {manifest_path}")

    manifest = _read_json(manifest_path)
    if manifest.get("canonical_assignment") is not False:
        raise FixtureAcquisitionError("fixture acquisition must not assign a canonical ID")

    captures: list[FixtureCapture] = []
    for item in manifest.get("captures", []):
        if not isinstance(item, dict):
            raise FixtureAcquisitionError("invalid capture manifest entry")
        kind = str(item.get("kind") or "").strip()
        filename = str(item.get("file") or "").strip()
        if not kind or not filename:
            raise FixtureAcquisitionError("capture entries require kind and file")
        path = directory / filename
        if not path.exists():
            raise FixtureAcquisitionError(f"missing fixture capture: {path}")
        captures.append(
            FixtureCapture(
                provider=str(manifest.get("provider") or ""),
                kind=kind,
                path=path,
                payload=_read_json(path),
            )
        )

    if not captures:
        raise FixtureAcquisitionError("fixture manifest has no captures")

    return FixtureInventory(
        anchor_slug=str(manifest.get("anchor_slug") or ""),
        provider=str(manifest.get("provider") or ""),
        fixture_dir=directory,
        captures=tuple(captures),
        canonical_assignment=False,
    )


def load_place_fixture_inventories(
    anchor_slug: str,
    fixtures_root: Path | str = Path("tests/fixtures"),
) -> tuple[FixtureInventory, FixtureInventory]:
    """Load GeoNames and Wikidata acquisition bundles for one place anchor."""
    root = Path(fixtures_root)
    directory = fixture_dir_name(anchor_slug)
    return (
        load_fixture_inventory(root / "geonames" / directory),
        load_fixture_inventory(root / "wikidata" / directory),
    )


def has_fixture_backed_evidence(
    anchor_slug: str,
    fixtures_root: Path | str = Path("tests/fixtures"),
) -> bool:
    """Return true only when required acquisition captures exist for ratification."""
    try:
        geonames, wikidata = load_place_fixture_inventories(anchor_slug, fixtures_root)
    except FixtureAcquisitionError:
        return False
    return (
        geonames.anchor_slug == anchor_slug
        and geonames.provider == "geonames"
        and {"direct", "search", "hierarchy"}.issubset(geonames.capture_kinds)
        and wikidata.anchor_slug == anchor_slug
        and wikidata.provider == "wikidata"
        and {"search", "entity"}.issubset(wikidata.capture_kinds)
    )


def load_grand_canyon_fixture_inventory(
    fixtures_root: Path | str = Path("tests/fixtures"),
) -> tuple[FixtureInventory, FixtureInventory]:
    """Load the NC-DATA-003 Grand Canyon GeoNames and Wikidata fixture bundles."""
    return load_place_fixture_inventories("grand-canyon", fixtures_root)
