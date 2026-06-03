"""Database writes for taxon discovery outputs."""
import json
from typing import Any

import asyncpg


async def upsert_taxon_discovery_run(
    conn: asyncpg.Connection,
    place_id: Any,
    ranked_taxa: list[dict[str, Any]],
    *,
    discovery_version: str = "1",
    parameters: dict[str, Any] | None = None,
) -> Any:
    async with conn.transaction():
        run = await conn.fetchrow(
            """
            INSERT INTO taxon_discovery_runs
                (place_id, discovery_version, status, parameters, provenance)
            VALUES ($1, $2, 'completed', $3::jsonb, $4::jsonb)
            ON CONFLICT (place_id, discovery_version)
            DO UPDATE SET
                status = 'completed',
                parameters = EXCLUDED.parameters,
                provenance = EXCLUDED.provenance,
                updated_at = NOW()
            RETURNING id
            """,
            place_id,
            discovery_version,
            json.dumps(parameters or {}, sort_keys=True),
            json.dumps({"prov:wasGeneratedBy": "taxon_discovery_worker:v1"}, sort_keys=True),
        )
        run_id = run["id"]
        await conn.execute("DELETE FROM taxon_candidates WHERE run_id = $1", run_id)
        for item in ranked_taxa:
            candidate = await conn.fetchrow(
                """
                INSERT INTO taxon_candidates
                    (run_id, place_id, scientific_name, canonical_name, taxon_rank,
                     gbif_taxon_key, wikidata_qid, common_names,
                     place_relevance_score, source_agreement_score,
                     illustration_likelihood_score, public_domain_path_score,
                     commercial_value_score, searchability_score, total_score,
                     score_components, provenance)
                VALUES
                    ($1, $2, $3, $4, $5, $6, $7, $8::text[],
                     $9, $10, $11, $12, $13, $14, $15, $16::jsonb, $17::jsonb)
                RETURNING id
                """,
                run_id,
                place_id,
                item["scientific_name"],
                item.get("canonical_name"),
                item["taxon_rank"],
                item.get("gbif_taxon_key"),
                item.get("wikidata_qid"),
                item.get("common_names", []),
                item["place_relevance_score"],
                item["source_agreement_score"],
                item["illustration_likelihood_score"],
                item["public_domain_path_score"],
                item["commercial_value_score"],
                item["searchability_score"],
                item["total_score"],
                json.dumps(item["score_components"], sort_keys=True),
                json.dumps(item["provenance"], sort_keys=True),
            )
            candidate_id = candidate["id"]
            for evidence in item.get("evidence", []):
                await conn.execute(
                    """
                    INSERT INTO taxon_candidate_evidence
                        (candidate_id, source, evidence_type, source_record_id,
                         source_url, payload, provenance)
                    VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7::jsonb)
                    """,
                    candidate_id,
                    evidence["source"],
                    evidence["evidence_type"],
                    evidence.get("source_record_id"),
                    evidence.get("source_url"),
                    json.dumps(evidence.get("payload", {}), sort_keys=True),
                    json.dumps(evidence.get("provenance", {}), sort_keys=True),
                )
            for target in item["bhl_search_targets"]:
                await conn.execute(
                    """
                    INSERT INTO bhl_search_targets
                        (candidate_id, sequence, query, target_type, provenance)
                    VALUES ($1, $2, $3, $4, $5::jsonb)
                    """,
                    candidate_id,
                    target["sequence"],
                    target["query"],
                    target["target_type"],
                    json.dumps(target.get("provenance", {}), sort_keys=True),
                )
        return run_id
