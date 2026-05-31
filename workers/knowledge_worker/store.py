"""Database operations for the knowledge worker.

Claim pattern mirrors preservation_worker: claim (commit) → process → release.
Facts use content-addressable uniqueness: (place_id, predicate, language, value::text).
Value changes produce a supersede+insert pair — never an in-place update.
"""
import json
import logging
from typing import Any

import asyncpg

from .config import settings
from .extract import _WORKER_ID

log = logging.getLogger("knowledge_worker")

_MULTI_VALUE_PREDICATES = {"country_code", "ouv_criterion"}


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
        """
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
        RETURNING
            p.id, p.source, p.name, p.description, p.statement_of_ouv,
            p.heritage_type, p.ouv_criteria, p.country_codes,
            p.inscription_year, p.core_area_ha, p.buffer_area_ha,
            p.transboundary, p.spatial_precision, p.status
        """,
        settings.rescore_interval_days,
        batch_size,
    )
    return [dict(r) for r in rows]


async def release_place(conn: asyncpg.Connection, place_id: Any) -> None:
    await conn.execute(
        """
        UPDATE places
        SET knowledge_extracting        = FALSE,
            last_knowledge_extracted_at = NOW(),
            knowledge_score = (
                SELECT AVG(confidence_score)
                FROM facts
                WHERE place_id = $1 AND status = 'active'
            ),
            updated_at = NOW()
        WHERE id = $1
        """,
        place_id,
    )


async def release_places(conn: asyncpg.Connection, place_ids: list[Any]) -> None:
    if not place_ids:
        return
    await conn.execute(
        """
        UPDATE places p
        SET knowledge_extracting        = FALSE,
            last_knowledge_extracted_at = NOW(),
            knowledge_score = (
                SELECT AVG(f.confidence_score)
                FROM facts f
                WHERE f.place_id = p.id AND f.status = 'active'
            ),
            updated_at = NOW()
        WHERE p.id = ANY($1::uuid[])
        """,
        place_ids,
    )


async def resolve_concept_id(conn: asyncpg.Connection, uri: str) -> Any:
    row = await conn.fetchrow("SELECT id FROM concepts WHERE uri = $1", uri)
    return row["id"] if row else None


async def upsert_facts(
    conn: asyncpg.Connection,
    facts: list[dict[str, Any]],
) -> tuple[int, int]:
    """Write facts in set-based batches. Returns (written, superseded).

    Single-value predicates supersede older active values in the same
    (place, predicate, language) slot. Multi-value predicates preserve sibling
    values, relying on content-addressable uniqueness to skip exact duplicates.
    """
    if not facts:
        return 0, 0

    payload = json.dumps(
        [
            {
                "place_id": str(f["place_id"]),
                "predicate": f["predicate"],
                "value": f["value"],
                "value_type": f["value_type"],
                "language": f.get("language"),
                "concept_uri": f.get("concept_uri"),
                "asset_id": str(f["asset_id"]) if f.get("asset_id") else None,
                "source": f["source"],
                "confidence_score": float(f["confidence_score"]),
                "provenance": f["provenance"],
            }
            for f in facts
        ],
        ensure_ascii=False,
        sort_keys=True,
    )

    superseded = await conn.fetchval(
        """
        WITH incoming AS (
            SELECT DISTINCT place_id, predicate, COALESCE(language, '') AS language_key, value
            FROM jsonb_to_recordset($1::jsonb) AS x(
                place_id uuid, predicate text, value jsonb, language text
            )
            WHERE predicate <> ALL($2::text[])
        ), updated AS (
            UPDATE facts f
            SET status = 'superseded', updated_at = NOW()
            FROM incoming i
            WHERE f.place_id = i.place_id
              AND f.predicate = i.predicate
              AND COALESCE(f.language, '') = i.language_key
              AND f.value::text != i.value::text
              AND f.status = 'active'
            RETURNING f.id
        )
        SELECT count(*)::int FROM updated
        """,
        payload,
        list(_MULTI_VALUE_PREDICATES),
    )

    reactivated = await conn.fetchval(
        """
        WITH incoming AS (
            SELECT place_id, predicate, value, language
            FROM jsonb_to_recordset($1::jsonb) AS x(
                place_id uuid, predicate text, value jsonb, language text
            )
        ), updated AS (
            UPDATE facts f
            SET status = 'active', updated_at = NOW()
            FROM incoming i
            WHERE f.place_id = i.place_id
              AND f.predicate = i.predicate
              AND COALESCE(f.language, '') = COALESCE(i.language, '')
              AND f.value::text = i.value::text
              AND f.status = 'superseded'
            RETURNING f.id
        )
        SELECT count(*)::int FROM updated
        """,
        payload,
    )

    inserted = await conn.fetchval(
        """
        WITH incoming AS (
            SELECT *
            FROM jsonb_to_recordset($1::jsonb) AS x(
                place_id uuid,
                predicate text,
                value jsonb,
                value_type text,
                language text,
                concept_uri text,
                asset_id uuid,
                source text,
                confidence_score numeric,
                provenance jsonb
            )
        ), inserted AS (
            INSERT INTO facts
                (place_id, predicate, value, value_type, language, concept_id,
                 asset_id, source, confidence_score, status, provenance)
            SELECT
                i.place_id, i.predicate, i.value, i.value_type, i.language, c.id,
                i.asset_id, i.source, i.confidence_score, 'active', i.provenance
            FROM incoming i
            LEFT JOIN concepts c ON c.uri = i.concept_uri
            ON CONFLICT (place_id, predicate, COALESCE(language, ''), (value::text))
            DO NOTHING
            RETURNING id
        )
        SELECT count(*)::int FROM inserted
        """,
        payload,
    )

    return int(inserted or 0) + int(reactivated or 0), int(superseded or 0)


async def upsert_relationships(
    conn: asyncpg.Connection,
    relationships: list[dict[str, Any]],
) -> int:
    """Write relationships in one set-based insert."""
    if not relationships:
        return 0

    payload = json.dumps(
        [
            {
                "subject_id": str(r["subject_id"]),
                "subject_type": r["subject_type"],
                "predicate": r["predicate"],
                "object_id": str(r["object_id"]) if r.get("object_id") else None,
                "object_type": r["object_type"],
                "concept_uri": r.get("concept_uri"),
                "confidence_score": float(r["confidence_score"]),
                "status": r.get("status", "active"),
                "asset_id": str(r["asset_id"]) if r.get("asset_id") else None,
                "provenance": r["provenance"],
            }
            for r in relationships
        ],
        ensure_ascii=False,
        sort_keys=True,
    )

    written = await conn.fetchval(
        """
        WITH incoming AS (
            SELECT *
            FROM jsonb_to_recordset($1::jsonb) AS x(
                subject_id uuid,
                subject_type text,
                predicate text,
                object_id uuid,
                object_type text,
                concept_uri text,
                confidence_score numeric,
                status text,
                asset_id uuid,
                provenance jsonb
            )
        ), resolved AS (
            SELECT
                i.subject_id, i.subject_type, i.predicate,
                COALESCE(i.object_id, c.id) AS object_id,
                i.object_type, i.confidence_score, i.status, i.asset_id, i.provenance
            FROM incoming i
            LEFT JOIN concepts c ON c.uri = i.concept_uri
        ), inserted AS (
            INSERT INTO relationships
                (subject_id, subject_type, predicate, object_id, object_type,
                 confidence_score, status, asset_id, provenance)
            SELECT
                subject_id, subject_type, predicate, object_id, object_type,
                confidence_score, status, asset_id, provenance
            FROM resolved
            WHERE object_id IS NOT NULL
            ON CONFLICT (subject_id, subject_type, predicate, object_id, object_type)
            DO NOTHING
            RETURNING id
        )
        SELECT count(*)::int FROM inserted
        """,
        payload,
    )
    return int(written or 0)


async def build_co_inscribed_relationships(
    conn: asyncpg.Connection,
    place_ids: list[Any],
) -> int:
    """Create co_inscribed_with pairs for the given batch of place_ids.

    Restricts the driving side (a) to the current batch so the join does not
    become a global cross-product. LEAST/GREATEST ensures canonical subject/object
    ordering so ON CONFLICT correctly deduplicates when both sides are in the batch.
    """
    if not place_ids:
        return 0
    result = await conn.execute(
        """
        INSERT INTO relationships
            (subject_id, subject_type, predicate, object_id, object_type,
             confidence_score, status, provenance)
        SELECT
            LEAST(a.place_id, b.place_id),
            'place',
            'co_inscribed_with',
            GREATEST(a.place_id, b.place_id),
            'place',
            0.85,
            'active',
            jsonb_build_object(
                'prov:wasGeneratedBy', $1::text,
                'extraction_method',  'join_query',
                'extraction_version', $2::text,
                'prov:generatedAtTime',
                    to_char(NOW(), 'YYYY-MM-DD"T"HH24:MI:SS"Z"')
            )
        FROM facts a
        JOIN facts b
          ON a.value     = b.value
         AND a.source    = b.source
         AND a.predicate = 'inscription_year'
         AND b.predicate = 'inscription_year'
         AND a.place_id != b.place_id
         AND a.status    = 'active'
         AND b.status    = 'active'
        WHERE a.place_id = ANY($3::uuid[])
        ON CONFLICT (subject_id, subject_type, predicate, object_id, object_type)
        DO NOTHING
        """,
        _WORKER_ID,
        settings.extraction_version,
        place_ids,
    )
    return int(result.rsplit(" ", 1)[-1])
