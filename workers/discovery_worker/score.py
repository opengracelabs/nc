from typing import Any

# Weight of each field toward the 0.0–1.0 confidence score.
_WEIGHTS: list[tuple[str, float]] = [
    ("name",             0.20),
    ("country_codes",    0.15),
    ("heritage_type",    0.15),
    ("ouv_criteria",     0.15),
    ("inscription_year", 0.10),
    ("centroid",         0.15),
    ("wikidata_qid",     0.10),
]


def score(record: dict[str, Any]) -> float:
    total = 0.0
    for field, weight in _WEIGHTS:
        value = record.get(field)
        if value is None:
            continue
        if isinstance(value, dict) and not value:
            continue
        if isinstance(value, list) and not value:
            continue
        total += weight
    return round(min(total, 1.0), 4)
