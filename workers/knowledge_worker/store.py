"""Database operations for the knowledge worker.

Claim pattern mirrors preservation_worker: claim (commit) → process → release.
Facts use content-addressable uniqueness: (place_id, predicate, language, value::text).
Value changes produce a supersede+insert pair — never an in-place update.
"""
import json
import logging
from typing import Any

import asyncpg
from asyncpg.exceptions import UniqueViolationError

from .config import settings

log = logging.getLogger("knowledge_worker")

_PLACE_COLS = """
    id, source, name, description, statement_of_ouv,
    heritage_type, ouv_criteria, country_codes,
    inscription_year, core_area_ha, buffer_area_ha,
    transboundary, spatial_precision, status
"""


async def reset_stale_extracting(conn: asyncpg.Connection) -> int:
    result = await conn.execute(
        """
        UPDATE places
        SET knowledge_extracting = FALSE, updated_at = NOW()
        WHERE knowledge_extracting = TRUE
          AND updated_at < NOW() - ($1::int * interval '1 second')
        """,
        settings.extraction_timeout_seconds,
    )
    count = int(result.rsplit(" ", 1)[-1])
    if count:
        log.info("Reset %d stale extracting places", count)
    return count


async def claim_places_for_extraction(
    conn: asyncpg.Connection,
    batch_size: int,
) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        f"""
        WITH next_places AS (
            SELECT id FROM places
            WHERE status = 'active'
              AND knowledge_extracting = FALSE
              AND (
                  last_knowledge_extracted_at IS NULL
                  OR last_knowledge_extracted_at < NOW() - ($1 * interval '1 day')
              )
            ORDER BY last_knowledge_extracted_at NULLS FIRST, created_at
            LIMIT $2
            FOR UPDATE SKIP LOCKED
        )
        UPDATE places AS p
        SET knowledge_extracting = TRUE, updated_at = NOW()
        FROM next_places
        WHERE p.id = next_places.id
        RETURNING {_PLACE_COLS}
        """,
        settings.rescore_interval_days,
        batch_size,
    )
    return [dict(r) for r in rows]


async def release_place(conn: asyncpg.Connection, place_id: Any) -> None:
    await conn.execute(
        """
        UPDATE places
        SET knowledge_extracting = FALSE,
            last_knowledge_extracted_at = NOW(),
            updated_at = NOW()
        WHERE id = $1
        """,
        place_id,
    )


async def resolve_concept_id(conn: asyncpg.Connection, uri: str) -> Any:
    row = await conn.fetchrow("SELECT id FROM concepts WHERE uri = $1", uri)
    return row["id"] if row else None


async def upsert_facts(
    conn: asyncpg.Connection,
    facts: list[dict[str, Any]],
) -> tuple[int, int]:
    """Write facts. Returns (written, superseded).

    Supersede flow: if an active fact exists with the same (place, predicate, language)
    but a DIFFERENT value, mark it superseded and insert the new value.
    If the exact same (place, predicate, language, value) was previously superseded,
    reactivate it rather than inserting a duplicate.
    """
    written = 0
    superseded = 0

    for f in facts:
        concept_id = None
        if uri := f.get("concept_uri"):
            concept_id = await resolve_concept_id(conn, uri)

        value_json = json.dumps(f["value"], ensure_ascii=False, sort_keys=True)
        language = f.get("language")

        # Supersede active facts for this slot that have a different value
        sup = await conn.execute(
            """
            UPDATE facts
            SET status = 'superseded', updated_at = NOW()
            WHERE place_id = $1
              AND predicate = $2
              AND COALESCE(language, '') = COALESCE($3, '')
              AND value::text != $4
              AND status = 'active'
            """,
            f["place_id"], f["predicate"], language, value_json,
        )
        superseded += int(sup.rsplit(" ", 1)[-1])

        # Reactivate if this exact value was previously superseded
        reactivated = await conn.execute(
            """
            UPDATE facts
            SET status = 'active', updated_at = NOW()
            WHERE place_id = $1
              AND predicate = $2
              AND COALESCE(language, '') = COALESCE($3, '')
              AND value::text = $4
              AND status = 'superseded'
            """,
            f["place_id"], f["predicate"], language, value_json,
        )
        if int(reactivated.rsplit(" ", 1)[-1]) > 0:
            written += 1
            continue

        # Insert new active fact; unique index prevents exact duplicates
        try:
            await conn.execute(
                """
                INSERT INTO facts
                    (place_id, predicate, value, value_type, language, concept_id,
                     asset_id, source, confidence_score, status, provenance)
                VALUES ($1, $2, $3::jsonb, $4, $5, $6, $7, $8, $9, 'active', $10::jsonb)
                """,
                f["place_id"], f["predicate"], value_json, f["value_type"],
                language, concept_id, f.get("asset_id"),
                f["source"], f["confidence_score"],
                json.dumps(f["provenance"]),
            )
            written += 1
        except UniqueViolationError:
            pass  # identical fact already active — nothing to do

    return written, superseded


async def upsert_relationships(
    conn: asyncpg.Connection,
    relationships: list[dict[str, Any]],
) -> int:
    written = 0
    for r in relationships:
        object_id = r.get("object_id")
        if object_id is None and (uri := r.get("concept_uri")):
            object_id = await resolve_concept_id(conn, uri)
        if object_id is None:
            log.warning("Skipping relationship: concept_uri=%s not in concepts table",
                        r.get("concept_uri"))
            continue

        try:
            await conn.execute(
                """
                INSERT INTO relationships
                    (subject_id, subject_type, predicate, object_id, object_type,
                     confidence_score, status, asset_id, provenance)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9::jsonb)
                ON CONFLICT (subject_id, subject_type, predicate, object_id, object_type)
                DO NOTHING
                """,
                r["subject_id"], r["subject_type"], r["predicate"],
                object_id, r["object_type"],
                r["confidence_score"], r.get("status", "active"),
                r.get("asset_id"), json.dumps(r["provenance"]),
            )
            written += 1
        except Exception as exc:
            log.warning("Relationship write error: %s", exc)

    return written


async def build_co_inscribed_relationships(conn: asyncpg.Connection) -> int:
    """Create co_inscribed_with for pairs of places sharing inscription year + source."""
    result = await conn.execute(
        """
        INSERT INTO relationships
            (subject_id, subject_type, predicate, object_id, object_type,
             confidence_score, status, provenance)
        SELECT
            a.place_id,
            'place',
            'co_inscribed_with',
            b.place_id,
            'place',
            0.85,
            'active',
            jsonb_build_object(
                'prov:wasGeneratedBy', 'knowledge_worker:v0.2.0',
                'extraction_method', 'join_query',
                'extraction_version', $1,
                'prov:generatedAtTime',
                    to_char(NOW(), 'YYYY-MM-DD"T"HH24:MI:SS"Z"')
            )
        FROM facts a
        JOIN facts b
          ON a.place_id    < b.place_id
         AND a.predicate   = 'inscription_year'
         AND b.predicate   = 'inscription_year'
         AND a.value       = b.value
         AND a.source      = b.source
         AND a.status      = 'active'
         AND b.status      = 'active'
        ON CONFLICT (subject_id, subject_type, predicate, object_id, object_type)
        DO NOTHING
        """,
        settings.extraction_version,
    )
    return int(result.rsplit(" ", 1)[-1])
