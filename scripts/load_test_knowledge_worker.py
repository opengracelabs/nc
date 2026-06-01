"""Load test the knowledge worker against PostgreSQL.

The harness seeds synthetic active UNESCO-like places, runs the same extraction
and storage functions used by workers.knowledge_worker, then reports extraction,
write, relationship, and query timings.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import asyncpg

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workers.knowledge_worker.config import settings  # noqa: E402
from workers.knowledge_worker.extract import (  # noqa: E402
    build_place_concept_relationships,
    extract_facts,
)
from workers.knowledge_worker.store import (  # noqa: E402
    build_co_inscribed_relationships,
    upsert_facts,
    upsert_relationships,
)

LOAD_SOURCE = "unesco_load_test"
LOAD_PREFIX = "loadtest-unesco-"
COUNTRIES = ["AU", "BR", "CA", "CN", "EG", "FR", "IN", "IT", "JP", "MX", "PE", "ZA"]
CRITERIA = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
HERITAGE_TYPES = ["cultural", "natural", "mixed"]


@dataclass(frozen=True)
class Timing:
    label: str
    seconds: float

    @property
    def ms(self) -> float:
        return self.seconds * 1000


async def timed(label: str, fn: Callable[[], Awaitable[Any]]) -> tuple[Any, Timing]:
    start = time.perf_counter()
    result = await fn()
    return result, Timing(label, time.perf_counter() - start)


def make_place(index: int) -> dict[str, Any]:
    ref_id = f"{LOAD_PREFIX}{index:05d}"
    country = COUNTRIES[index % len(COUNTRIES)]
    second_country = COUNTRIES[(index + 5) % len(COUNTRIES)]
    heritage_type = HERITAGE_TYPES[index % len(HERITAGE_TYPES)]
    criteria = [CRITERIA[index % len(CRITERIA)]]
    if index % 4 == 0:
        criteria.append(CRITERIA[(index + 3) % len(CRITERIA)])

    return {
        "source_id": ref_id,
        "source": LOAD_SOURCE,
        "unesco_ref_id": f"LT-{index:05d}",
        "wikidata_qid": f"Q{900000000 + index}",
        "name": {"en": f"UNESCO Load Test Site {index:05d}"},
        "description": {
            "en": (
                "Synthetic UNESCO World Heritage load-test record for knowledge "
                f"extraction benchmark {index:05d}."
            )
        },
        "statement_of_ouv": {
            "en": (
                "Generated evidence text used to validate traceable fact "
                f"extraction for synthetic place {index:05d}."
            )
        },
        "heritage_type": heritage_type,
        "ouv_criteria": criteria,
        "country_codes": [country, second_country] if index % 13 == 0 else [country],
        "transboundary": index % 13 == 0,
        "inscription_year": 1978 + (index % 47),
        "core_area_ha": float(1000 + index),
        "buffer_area_ha": float(200 + (index % 500)),
        "spatial_precision": "centroid",
        "status": "active",
        "provenance": {
            "source": LOAD_SOURCE,
            "source_id": ref_id,
            "evidence": {
                "minio_bucket": "nc-raw",
                "minio_object": f"load-test/unesco/{index:05d}.json",
                "checksum_sha256": f"{index:064x}"[-64:],
            },
        },
    }


async def assert_schema(conn: asyncpg.Connection) -> None:
    required = {
        "concepts": {"id", "uri", "type", "status"},
        "facts": {"id", "place_id", "predicate", "value", "value_type", "source", "status"},
        "relationships": {"id", "subject_id", "predicate", "object_id", "status"},
        "places": {
            "id",
            "source",
            "source_id",
            "knowledge_extracting",
            "last_knowledge_extracted_at",
        },
    }
    for table, columns in required.items():
        rows = await conn.fetch(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = $1
            """,
            table,
        )
        present = {row["column_name"] for row in rows}
        missing = sorted(columns - present)
        if missing:
            raise RuntimeError(f"{table} is missing required columns: {', '.join(missing)}")


async def reset_load_rows(conn: asyncpg.Connection) -> None:
    rows = await conn.fetch(
        "SELECT id FROM places WHERE source = $1 OR source_id LIKE $2",
        LOAD_SOURCE,
        f"{LOAD_PREFIX}%",
    )
    place_ids = [row["id"] for row in rows]
    if place_ids:
        await conn.execute(
            "DELETE FROM relationships WHERE subject_id = ANY($1::uuid[])",
            place_ids,
        )
        await conn.execute(
            "DELETE FROM relationships WHERE object_id = ANY($1::uuid[])",
            place_ids,
        )
        await conn.execute("DELETE FROM facts WHERE place_id = ANY($1::uuid[])", place_ids)
        await conn.execute("DELETE FROM places WHERE id = ANY($1::uuid[])", place_ids)


async def seed_source(conn: asyncpg.Connection) -> None:
    await conn.execute(
        """
        INSERT INTO sources (source_id, name, base_url, fetch_strategy, entity_types, standards)
        VALUES ($1, 'UNESCO load test', 'https://whc.unesco.org/', 'file',
                ARRAY['place'], ARRAY['UNESCO World Heritage'])
        ON CONFLICT (source_id) DO UPDATE
        SET name = EXCLUDED.name,
            base_url = EXCLUDED.base_url,
            updated_at = NOW()
        """,
        LOAD_SOURCE,
    )


async def seed_places(conn: asyncpg.Connection, count: int) -> list[dict[str, Any]]:
    places = [make_place(i) for i in range(count)]
    rows = await conn.fetch(
        """
        INSERT INTO places (
            source_id, source, unesco_ref_id, wikidata_qid, name, description,
            statement_of_ouv, heritage_type, ouv_criteria, country_codes,
            transboundary, inscription_year, core_area_ha, buffer_area_ha,
            spatial_precision, status, provenance, knowledge_extracting,
            last_knowledge_extracted_at
        )
        SELECT
            p.source_id, p.source, p.unesco_ref_id, p.wikidata_qid,
            p.name::jsonb, p.description::jsonb, p.statement_of_ouv::jsonb,
            p.heritage_type, p.ouv_criteria::text[], p.country_codes::text[],
            p.transboundary, p.inscription_year, p.core_area_ha, p.buffer_area_ha,
            p.spatial_precision, p.status, p.provenance::jsonb, FALSE, NULL
        FROM jsonb_to_recordset($1::jsonb) AS p(
            source_id text,
            source text,
            unesco_ref_id text,
            wikidata_qid text,
            name jsonb,
            description jsonb,
            statement_of_ouv jsonb,
            heritage_type text,
            ouv_criteria text[],
            country_codes text[],
            transboundary boolean,
            inscription_year int,
            core_area_ha double precision,
            buffer_area_ha double precision,
            spatial_precision text,
            status text,
            provenance jsonb
        )
        RETURNING
            id, source, name, description, statement_of_ouv, heritage_type,
            ouv_criteria, country_codes, inscription_year, core_area_ha,
            buffer_area_ha, transboundary, spatial_precision, status
        """,
        json.dumps(places),
    )
    return [dict(row) for row in rows]


async def explain_ms(conn: asyncpg.Connection, sql: str, *args: Any) -> float:
    row = await conn.fetchval(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {sql}", *args)
    plan = json.loads(row) if isinstance(row, str) else row
    return float(plan[0]["Execution Time"])


async def query_benchmarks(conn: asyncpg.Connection, place_id: Any) -> dict[str, float]:
    return {
        "facts_by_place_ms": await explain_ms(
            conn,
            """
            SELECT id, predicate, value
            FROM facts
            WHERE place_id = $1 AND status = 'active'
            ORDER BY predicate, language
            LIMIT 200
            """,
            place_id,
        ),
        "facts_by_predicate_ms": await explain_ms(
            conn,
            """
            SELECT id, place_id, value
            FROM facts
            WHERE predicate = 'heritage_type' AND status = 'active'
            ORDER BY created_at DESC
            LIMIT 200
            """,
        ),
        "relationships_by_place_ms": await explain_ms(
            conn,
            """
            SELECT id, predicate, object_id
            FROM relationships
            WHERE subject_id = $1 AND subject_type = 'place' AND status = 'active'
            ORDER BY predicate
            LIMIT 200
            """,
            place_id,
        ),
        "co_inscribed_lookup_ms": await explain_ms(
            conn,
            """
            SELECT id, object_id
            FROM relationships
            WHERE subject_id = $1
              AND subject_type = 'place'
              AND predicate = 'co_inscribed_with'
              AND status = 'active'
            ORDER BY created_at DESC
            LIMIT 200
            """,
            place_id,
        ),
        "places_search_ms": await explain_ms(
            conn,
            """
            SELECT id
            FROM places
            WHERE name::text ILIKE '%UNESCO%' OR description::text ILIKE '%UNESCO%'
            ORDER BY updated_at DESC
            LIMIT 50
            """,
        ),
        "places_country_filter_ms": await explain_ms(
            conn,
            """
            SELECT id
            FROM places
            WHERE 'AU' = ANY(country_codes)
            ORDER BY updated_at DESC
            LIMIT 50
            """,
        ),
        "places_heritage_type_filter_ms": await explain_ms(
            conn,
            """
            SELECT id
            FROM places
            WHERE heritage_type = 'natural'
            ORDER BY updated_at DESC
            LIMIT 50
            """,
        ),
        "places_criterion_filter_ms": await explain_ms(
            conn,
            """
            SELECT id
            FROM places
            WHERE 'vii' = ANY(ouv_criteria)
            ORDER BY updated_at DESC
            LIMIT 50
            """,
        ),
    }


async def run_load_test(count: int) -> dict[str, Any]:
    pool = await asyncpg.create_pool(dsn=settings.postgres_dsn, min_size=1, max_size=5)
    try:
        async with pool.acquire() as conn:
            await assert_schema(conn)
            await reset_load_rows(conn)
            await seed_source(conn)
            places, seed_timing = await timed("seed_places", lambda: seed_places(conn, count))

        facts_by_place: list[list[dict[str, Any]]] = []
        rels_by_place: list[list[dict[str, Any]]] = []

        start = time.perf_counter()
        for place in places:
            facts_by_place.append(extract_facts(place))
        fact_extract = Timing("fact_generation", time.perf_counter() - start)

        start = time.perf_counter()
        for place, facts in zip(places, facts_by_place, strict=True):
            rels_by_place.append(
                build_place_concept_relationships(place["id"], facts, place["source"])
            )
        rel_extract = Timing("relationship_generation", time.perf_counter() - start)

        all_facts = [fact for facts in facts_by_place for fact in facts]
        all_rels = [rel for rels in rels_by_place for rel in rels]

        async with pool.acquire() as conn:
            (facts_written, facts_superseded), fact_write = await timed(
                "upsert_facts",
                lambda: upsert_facts(conn, all_facts),
            )
            rels_written, rel_write = await timed(
                "upsert_relationships",
                lambda: upsert_relationships(conn, all_rels),
            )
            co_written, co_timing = await timed(
                "co_inscribed_generation",
                lambda: build_co_inscribed_relationships(conn, [place["id"] for place in places]),
            )
            await conn.execute("ANALYZE facts")
            await conn.execute("ANALYZE relationships")
            await conn.execute(
                """
                UPDATE places
                SET last_knowledge_extracted_at = NOW(), knowledge_extracting = FALSE
                WHERE source = $1
                """,
                LOAD_SOURCE,
            )
            queries = await query_benchmarks(conn, places[0]["id"])

        fact_count = sum(len(facts) for facts in facts_by_place)
        rel_count = sum(len(rels) for rels in rels_by_place)
        fact_write_total = fact_write.seconds
        rel_write_total = rel_write.seconds
        total_seconds = (
            seed_timing.seconds
            + fact_extract.seconds
            + rel_extract.seconds
            + fact_write_total
            + rel_write_total
            + co_timing.seconds
        )

        return {
            "sites": count,
            "facts_extracted": fact_count,
            "relationships_extracted": rel_count,
            "facts_written": facts_written,
            "facts_superseded": facts_superseded,
            "relationships_written": rels_written,
            "co_inscribed_relationships_written": co_written,
            "timings_ms": {
                seed_timing.label: round(seed_timing.ms, 3),
                fact_extract.label: round(fact_extract.ms, 3),
                rel_extract.label: round(rel_extract.ms, 3),
                "fact_writes_total": round(fact_write_total * 1000, 3),
                "relationship_writes_total": round(rel_write_total * 1000, 3),
                co_timing.label: round(co_timing.ms, 3),
                "total_measured": round(total_seconds * 1000, 3),
            },
            "rates_per_second": {
                "fact_generation": round(fact_count / fact_extract.seconds, 2)
                if fact_extract.seconds
                else None,
                "relationship_generation": round(rel_count / rel_extract.seconds, 2)
                if rel_extract.seconds
                else None,
                "fact_writes": round(facts_written / fact_write_total, 2)
                if fact_write_total
                else None,
                "relationship_writes": round(rels_written / rel_write_total, 2)
                if rel_write_total
                else None,
            },
            "batch_write_ms": {
                "facts": round(fact_write.ms, 3),
                "relationships": round(rel_write.ms, 3),
            },
            "query_execution_ms": {k: round(v, 3) for k, v in queries.items()},
        }
    finally:
        await pool.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sites", type=int, required=True, choices=(500, 5000, 10000))
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    result = await run_load_test(args.sites)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    asyncio.run(main())
