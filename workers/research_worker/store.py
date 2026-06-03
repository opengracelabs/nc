"""Database operations for the research worker."""
import json
import logging
from typing import Any

import asyncpg

from .config import settings

log = logging.getLogger("research_worker")

_PLACE_COLS = """
    id, source_id, source, unesco_ref_id, name, description, statement_of_ouv,
    heritage_type, ouv_criteria, country_codes, inscription_year, status,
    confidence_score, provenance, agent_notes, created_at, updated_at
"""

_FACT_COLS = """
    id, place_id, predicate, value, value_type, language,
    concept_id, asset_id, source, confidence_score,
    status, provenance, agent_notes, created_at, updated_at
"""

_REL_COLS = """
    id, subject_id, subject_type, predicate, object_id, object_type,
    confidence_score, status, asset_id, provenance, agent_notes,
    created_at, updated_at
"""

_JSON_FIELDS = {"name", "description", "statement_of_ouv", "value", "provenance", "agent_notes"}


def _decode(row: Any) -> dict[str, Any]:
    item = dict(row)
    for field in _JSON_FIELDS:
        if isinstance(item.get(field), str):
            item[field] = json.loads(item[field])
    return item


async def claim_places_for_research(
    conn: asyncpg.Connection,
    batch_size: int,
) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        f"""
        SELECT {_PLACE_COLS}
        FROM places p
        WHERE p.status = 'active'
          AND EXISTS (
              SELECT 1 FROM facts f
              WHERE f.place_id = p.id AND f.status = 'active'
          )
          AND EXISTS (
              SELECT 1 FROM relationships r
              WHERE r.status = 'active'
                AND ((r.subject_id = p.id AND r.subject_type = 'place')
                  OR (r.object_id = p.id AND r.object_type = 'place'))
          )
          AND NOT EXISTS (
              SELECT 1 FROM research_outputs ro
              WHERE ro.place_id = p.id
                AND ro.output_type = $1
                AND ro.output_version = $2
                AND ro.status IN ('pending_review','approved','published')
          )
        ORDER BY p.updated_at, p.created_at
        LIMIT $3
        """,  # noqa: S608
        settings.research_output_type,
        settings.research_version,
        batch_size,
    )
    return [_decode(r) for r in rows]


async def fetch_research_inputs(
    conn: asyncpg.Connection,
    place_id: Any,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    place = await conn.fetchrow(
        f"SELECT {_PLACE_COLS} FROM places WHERE id = $1",  # noqa: S608
        place_id,
    )
    if not place:
        raise ValueError(f"place not found: {place_id}")
    facts = await conn.fetch(
        f"""
        SELECT {_FACT_COLS}
        FROM facts
        WHERE place_id = $1 AND status = 'active'
        ORDER BY predicate, language, created_at
        """,  # noqa: S608
        place_id,
    )
    relationships = await conn.fetch(
        f"""
        SELECT {_REL_COLS} FROM relationships
        WHERE status = 'active'
          AND ((subject_id = $1 AND subject_type = 'place')
            OR (object_id = $1 AND object_type = 'place'))
        ORDER BY predicate, created_at
        """,  # noqa: S608
        place_id,
    )
    return _decode(place), [_decode(f) for f in facts], [_decode(r) for r in relationships]


async def upsert_research_output(conn: asyncpg.Connection, output: dict[str, Any]) -> Any:
    async with conn.transaction():
        row = await conn.fetchrow(
            """
            INSERT INTO research_outputs
                (place_id, output_type, output_version, title, summary, status,
                 confidence_score, provenance)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb)
            ON CONFLICT (place_id, output_type, output_version)
            DO UPDATE SET
                title = EXCLUDED.title,
                summary = EXCLUDED.summary,
                status = EXCLUDED.status,
                confidence_score = EXCLUDED.confidence_score,
                provenance = EXCLUDED.provenance,
                updated_at = NOW()
            WHERE research_outputs.status IN ('pending_review','rejected','disputed','retracted')
            RETURNING id
            """,
            output["place_id"],
            output["output_type"],
            output["output_version"],
            output["title"],
            output.get("summary"),
            output["status"],
            output["confidence_score"],
            json.dumps(output["provenance"], sort_keys=True),
        )
        if not row:
            return None

        output_id = row["id"]
        await conn.execute("DELETE FROM research_statements WHERE output_id = $1", output_id)
        for statement in output["statements"]:
            statement_row = await conn.fetchrow(
                """
                INSERT INTO research_statements
                    (output_id, place_id, sequence, statement_type, body, status,
                     confidence_score, provenance)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb)
                RETURNING id
                """,
                output_id,
                output["place_id"],
                statement["sequence"],
                statement["statement_type"],
                statement["body"],
                statement["status"],
                statement["confidence_score"],
                json.dumps(statement["provenance"], sort_keys=True),
            )
            statement_id = statement_row["id"]
            for evidence in statement["evidence"]:
                await conn.execute(
                    """
                    INSERT INTO research_statement_evidence
                        (statement_id, asset_id, fact_id, relationship_id,
                         evidence_role, provenance)
                    VALUES ($1, $2, $3, $4, $5, $6::jsonb)
                    """,
                    statement_id,
                    evidence["asset_id"],
                    evidence["fact_id"],
                    evidence["relationship_id"],
                    evidence.get("evidence_role", "supporting"),
                    json.dumps(evidence.get("provenance", {}), sort_keys=True),
                )
        return output_id
