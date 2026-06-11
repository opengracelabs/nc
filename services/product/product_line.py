"""Product line normalization helpers."""


def public_line_summary(row: dict) -> dict:
    return {
        "slug": row["slug"],
        "title": row["title"],
        "status": row["status"],
        "anchor_slug": row.get("anchor_slug"),
        "commercial_allowed": row.get("commercial_allowed"),
    }
