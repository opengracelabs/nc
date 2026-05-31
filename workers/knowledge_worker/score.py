from typing import Any

_SOURCE_SCORES: dict[str, float] = {
    "unesco_whc": 0.95,
    "wikidata": 0.80,
    "manual": 0.70,
}


def score_fact(source: str, asset_id: Any = None, corroborated: bool = False) -> float:
    """Return a confidence score in [0, 1] for a fact from the given source."""
    s = _SOURCE_SCORES.get(source, 0.60)
    if asset_id is not None:
        s = min(1.0, s + 0.05)
    if corroborated:
        s = min(1.0, s + 0.05)
    return round(s, 4)
