-- Performance indexes for the MILESTONE-002 knowledge worker and API.
-- These are additive and keep PostgreSQL as the authority for knowledge facts
-- and relationships.

-- Queue claim path:
--   WHERE status='active' AND knowledge_extracting=false
--   ORDER BY last_knowledge_extracted_at NULLS FIRST, created_at
CREATE INDEX IF NOT EXISTS idx_places_knowledge_claim_active
    ON places(last_knowledge_extracted_at NULLS FIRST, created_at, id)
    WHERE status = 'active' AND knowledge_extracting = FALSE;

-- Fact supersede/reactivation path in workers.knowledge_worker.store.upsert_facts.
CREATE INDEX IF NOT EXISTS idx_facts_active_slot_value
    ON facts(place_id, predicate, COALESCE(language, ''), (value::text))
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_facts_superseded_slot_value
    ON facts(place_id, predicate, COALESCE(language, ''), (value::text))
    WHERE status = 'superseded';

-- Relationship replay and API lookups by place.
CREATE INDEX IF NOT EXISTS idx_relationships_active_subject_predicate
    ON relationships(subject_id, subject_type, predicate, created_at DESC)
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_relationships_active_object_predicate
    ON relationships(object_id, object_type, predicate, created_at DESC)
    WHERE status = 'active';

-- Co-inscribed relationship build joins active inscription_year facts by
-- source/value and emits place pairs.
CREATE INDEX IF NOT EXISTS idx_facts_active_inscription_source_value_place
    ON facts(source, value, place_id)
    WHERE status = 'active' AND predicate = 'inscription_year';

-- Knowledge API filters.
CREATE INDEX IF NOT EXISTS idx_facts_active_place_predicate
    ON facts(place_id, predicate, language, created_at DESC)
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_facts_active_predicate_source
    ON facts(predicate, source, created_at DESC)
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_facts_active_predicate_created_at
    ON facts(predicate, created_at DESC)
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_relationships_active_place_co_inscribed
    ON relationships(subject_id, created_at DESC)
    WHERE status = 'active'
      AND subject_type = 'place'
      AND predicate = 'co_inscribed_with';


-- Search API filters and ordering. Existing indexes cover status, heritage_type,
-- country_codes, ouv_criteria, and name trigram search; these complete the
-- measured /places and /places/search query shapes.
CREATE INDEX IF NOT EXISTS idx_places_updated_at_desc
    ON places(updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_places_active_updated_at_desc
    ON places(updated_at DESC)
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_places_description_trgm
    ON places USING GIN((description::TEXT) gin_trgm_ops);
