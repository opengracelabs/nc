"""Database operations for illustration opportunity discovery."""
import json
from typing import Any

import asyncpg

_TARGET_COLS = """
    t.id, t.candidate_id, t.query, t.target_type,
    c.place_id, c.concept_id, c.scientific_name, c.gbif_taxon_key, c.wikidata_qid,
    c.place_relevance_score
"""


def _decode(row: Any) -> dict[str, Any]:
    return dict(row)


async def claim_bhl_search_targets(
    conn: asyncpg.Connection,
    batch_size: int,
) -> list[dict[str, Any]]:
    rows = await conn.fetch(
        f"""
        SELECT {_TARGET_COLS}
        FROM bhl_search_targets t
        JOIN taxon_candidates c ON c.id = t.candidate_id
        WHERE t.status = 'pending'
          AND c.concept_id IS NOT NULL
          AND c.status IN ('candidate','approved')
        ORDER BY c.total_score DESC, t.sequence
        LIMIT $1
        """,  # noqa: S608
        batch_size,
    )
    return [_decode(row) for row in rows]


async def mark_target_searched(conn: asyncpg.Connection, target_id: Any) -> None:
    await conn.execute(
        "UPDATE bhl_search_targets SET status = 'searched' WHERE id = $1",
        target_id,
    )


async def upsert_illustration_opportunity(
    conn: asyncpg.Connection,
    opportunity: dict[str, Any],
) -> Any:
    async with conn.transaction():
        row = await conn.fetchrow(
            """
            INSERT INTO illustration_opportunities
                (concept_id, source, source_record_id, source_url,
                 bhl_item_id, bhl_page_id, taxon_name, title, publication_title,
                 illustrator, publication_year, rights_status, rights_source_url,
                 rights_verified_by, illustration_quality_score,
                 historical_significance_score, commercial_value_score,
                 provenance_score, opportunity_score, score_components, provenance)
            VALUES
                ($1, 'bhl', $2, $3, $4, $5, $6, $7, $8, $9, $10,
                 $11, $12, $13, $14, $15, $16, $17, $18, $19::jsonb, $20::jsonb)
            ON CONFLICT (source, bhl_page_id)
            DO UPDATE SET
                concept_id = EXCLUDED.concept_id,
                source_url = EXCLUDED.source_url,
                taxon_name = EXCLUDED.taxon_name,
                title = EXCLUDED.title,
                publication_title = EXCLUDED.publication_title,
                illustrator = EXCLUDED.illustrator,
                publication_year = EXCLUDED.publication_year,
                rights_status = EXCLUDED.rights_status,
                rights_source_url = EXCLUDED.rights_source_url,
                rights_verified_by = EXCLUDED.rights_verified_by,
                illustration_quality_score = EXCLUDED.illustration_quality_score,
                historical_significance_score = EXCLUDED.historical_significance_score,
                commercial_value_score = EXCLUDED.commercial_value_score,
                provenance_score = EXCLUDED.provenance_score,
                opportunity_score = EXCLUDED.opportunity_score,
                score_components = EXCLUDED.score_components,
                provenance = EXCLUDED.provenance,
                updated_at = NOW()
            RETURNING id
            """,
            opportunity["concept_id"],
            opportunity["source_record_id"],
            opportunity.get("source_url"),
            opportunity["bhl_item_id"],
            opportunity["bhl_page_id"],
            opportunity["taxon_name"],
            opportunity.get("title"),
            opportunity["publication_title"],
            opportunity.get("illustrator"),
            opportunity.get("publication_year"),
            opportunity["rights_status"],
            opportunity.get("rights_source_url"),
            opportunity["rights_verified_by"],
            opportunity["illustration_quality_score"],
            opportunity["historical_significance_score"],
            opportunity["commercial_value_score"],
            opportunity["provenance_score"],
            opportunity["opportunity_score"],
            json.dumps(opportunity.get("score_components", {}), sort_keys=True),
            json.dumps(opportunity["provenance"], sort_keys=True),
        )
        opportunity_id = row["id"]
        link = opportunity["place_link"]
        await conn.execute(
            """
            INSERT INTO illustration_opportunity_places
                (opportunity_id, place_id, relevance_score, evidence_summary, provenance)
            VALUES ($1, $2, $3, $4, $5::jsonb)
            ON CONFLICT (opportunity_id, place_id)
            DO UPDATE SET
                relevance_score = EXCLUDED.relevance_score,
                evidence_summary = EXCLUDED.evidence_summary,
                provenance = EXCLUDED.provenance
            """,
            opportunity_id,
            link["place_id"],
            link["relevance_score"],
            link["evidence_summary"],
            json.dumps(link.get("provenance", {}), sort_keys=True),
        )
        await conn.execute(
            "DELETE FROM illustration_opportunity_evidence WHERE opportunity_id = $1",
            opportunity_id,
        )
        for evidence in opportunity["evidence"]:
            await conn.execute(
                """
                INSERT INTO illustration_opportunity_evidence
                    (opportunity_id, evidence_type, source, source_url, payload, provenance)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6::jsonb)
                """,
                opportunity_id,
                evidence["evidence_type"],
                evidence["source"],
                evidence.get("source_url"),
                json.dumps(evidence.get("payload", {}), sort_keys=True),
                json.dumps(evidence.get("provenance", {}), sort_keys=True),
            )
        return opportunity_id
