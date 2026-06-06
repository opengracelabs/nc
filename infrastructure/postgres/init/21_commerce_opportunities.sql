-- v0.5.0 Phase 1 / Migration 21.
-- Commerce Intelligence opportunity runtime table.
--
-- No scoring worker activation.
-- No product generation.
-- No Shopify integration.
--
-- Migration 22 will add score_audit_log and the deferred COS audit trigger.

CREATE TABLE IF NOT EXISTS commerce_opportunities (
    id                                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id                      UUID NOT NULL UNIQUE REFERENCES illustration_opportunities(id),
    policy_version_id                   UUID NOT NULL REFERENCES commerce_policy(id),
    computed_at                         TIMESTAMPTZ NOT NULL,
    computed_by                         TEXT NOT NULL,
    computation_trigger                 TEXT NOT NULL REFERENCES commerce_computation_trigger_vocabulary(value),
    policy_stale                        BOOLEAN NOT NULL DEFAULT FALSE,
    last_scored_at                      TIMESTAMPTZ,

    hard_gate_status                    TEXT NOT NULL REFERENCES commerce_hard_gate_status_vocabulary(value),

    rights_confidence                   NUMERIC(4,3) CHECK (rights_confidence BETWEEN 0 AND 1),
    golden_age_factor                   NUMERIC(4,3) CHECK (golden_age_factor BETWEEN 0 AND 1),
    institutional_credit                NUMERIC(4,3) CHECK (institutional_credit BETWEEN 0 AND 1),
    provenance_completeness             NUMERIC(4,3) CHECK (provenance_completeness BETWEEN 0 AND 1),
    resolution_tier_score               NUMERIC(4,3) CHECK (resolution_tier_score BETWEEN 0 AND 1),
    place_relevance_score               NUMERIC(4,3) CHECK (place_relevance_score BETWEEN 0 AND 1),
    place_tier_score                    NUMERIC(4,3) CHECK (place_tier_score BETWEEN 0 AND 1),

    illustrator_prestige                NUMERIC(4,3) CHECK (illustrator_prestige BETWEEN 0 AND 1),
    taxon_commercial_tier               TEXT,
    taxon_commercial_tier_score         NUMERIC(4,3) CHECK (taxon_commercial_tier_score BETWEEN 0 AND 1),
    taxon_place_iconic                  NUMERIC(4,3) CHECK (taxon_place_iconic BETWEEN 0 AND 1),

    image_quality_score                 NUMERIC(4,3) CHECK (image_quality_score BETWEEN 0 AND 1),
    image_quality_reviewed_by           TEXT,
    image_quality_reviewed_at           TIMESTAMPTZ,
    composition_fit                     NUMERIC(4,3) CHECK (composition_fit BETWEEN 0 AND 1),
    identification_confidence           NUMERIC(4,3) CHECK (identification_confidence BETWEEN 0 AND 1),
    color_profile                       TEXT REFERENCES commerce_color_profile_vocabulary(value),
    color_score                         NUMERIC(4,3) CHECK (color_score BETWEEN 0 AND 1),

    image_width_px                      INT CHECK (image_width_px IS NULL OR image_width_px >= 0),
    resolution_tier                     TEXT REFERENCES commerce_resolution_tier_vocabulary(value),

    museum_score                        NUMERIC(4,3) CHECK (museum_score BETWEEN 0 AND 1),
    retail_score                        NUMERIC(4,3) CHECK (retail_score BETWEEN 0 AND 1),
    publishing_score                    NUMERIC(4,3) CHECK (publishing_score BETWEEN 0 AND 1),
    tourism_score                       NUMERIC(4,3) CHECK (tourism_score BETWEEN 0 AND 1),
    reference_score                     NUMERIC(4,3) CHECK (reference_score BETWEEN 0 AND 1),

    commerce_opportunity_score          NUMERIC(4,3) CHECK (commerce_opportunity_score BETWEEN 0 AND 1),
    commerce_tier                       TEXT REFERENCES commerce_tier_vocabulary(value),

    csm_score                           NUMERIC(4,3) CHECK (csm_score BETWEEN 0 AND 1),
    csm_tier                            TEXT REFERENCES commerce_csm_tier_vocabulary(value),

    eligible_wall_art_premium           BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_wall_art_standard          BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_calendar                   BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_puzzle                     BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_card                       BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_book_illustration          BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_educational                BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_museum_print               BOOLEAN NOT NULL DEFAULT FALSE,
    eligible_institutional_license      BOOLEAN NOT NULL DEFAULT FALSE,

    requires_curator_review             BOOLEAN NOT NULL DEFAULT FALSE,
    curator_review_reason               TEXT REFERENCES commerce_curator_review_reason_vocabulary(value),
    curator_decision                    TEXT NOT NULL DEFAULT 'pending' REFERENCES commerce_curator_decision_vocabulary(value),
    curator_reviewed_by                 TEXT,
    curator_reviewed_at                 TIMESTAMPTZ,
    curator_notes                       TEXT,

    score_inputs                        JSONB NOT NULL DEFAULT '{}',
    input_hash_sha256                   TEXT NOT NULL,

    status                              TEXT NOT NULL DEFAULT 'pending_review',
    provenance                          JSONB NOT NULL DEFAULT '{}',
    created_at                          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_commerce_opportunities_input_hash CHECK (input_hash_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_commerce_opportunities_computed_by CHECK (length(computed_by) > 0),
    CONSTRAINT chk_commerce_opportunities_review_identity CHECK (
        curator_decision = 'pending'
        OR curator_reviewed_by IS NOT NULL
    ),
    CONSTRAINT chk_commerce_opportunities_status CHECK (
        status IN ('pending_review','active','blocked','stale','superseded','retired','archived','integrity_suspect')
    )
);

-- Director Decision H-2:
-- Legacy fit/value score columns are intentionally absent.

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_policy_score
    ON commerce_opportunities(policy_version_id, commerce_opportunity_score DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_tier_score
    ON commerce_opportunities(commerce_tier, commerce_opportunity_score DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_csm_tier
    ON commerce_opportunities(csm_tier, csm_score DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_gate
    ON commerce_opportunities(hard_gate_status, computed_at DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_curator
    ON commerce_opportunities(curator_decision, requires_curator_review, computed_at DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_stale
    ON commerce_opportunities(policy_stale, last_scored_at DESC)
    WHERE policy_stale = TRUE;

CREATE INDEX IF NOT EXISTS idx_commerce_opportunities_last_scored
    ON commerce_opportunities(last_scored_at)
    WHERE status NOT IN ('blocked','archived');

DROP TRIGGER IF EXISTS trg_commerce_opportunities_updated_at ON commerce_opportunities;
CREATE TRIGGER trg_commerce_opportunities_updated_at
    BEFORE UPDATE ON commerce_opportunities
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_active_taxon_commercial_tier()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.taxon_commercial_tier IS NOT NULL
       AND NOT EXISTS (
           SELECT 1
           FROM taxon_commercial_tier_vocabulary v
           WHERE v.value = NEW.taxon_commercial_tier
             AND v.status = 'active'
       )
    THEN
        RAISE EXCEPTION 'commerce opportunity references missing or inactive taxon commercial tier: %',
            NEW.taxon_commercial_tier;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_commerce_opportunities_active_taxon_tier ON commerce_opportunities;
CREATE TRIGGER trg_commerce_opportunities_active_taxon_tier
    BEFORE INSERT OR UPDATE OF taxon_commercial_tier ON commerce_opportunities
    FOR EACH ROW EXECUTE FUNCTION enforce_active_taxon_commercial_tier();

CREATE OR REPLACE FUNCTION enforce_commerce_opportunity_gate_eligibility()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.hard_gate_status <> 'passed'
       AND (
           NEW.eligible_wall_art_premium
           OR NEW.eligible_wall_art_standard
           OR NEW.eligible_calendar
           OR NEW.eligible_puzzle
           OR NEW.eligible_card
           OR NEW.eligible_book_illustration
           OR NEW.eligible_educational
           OR NEW.eligible_museum_print
           OR NEW.eligible_institutional_license
       )
    THEN
        RAISE EXCEPTION 'commerce opportunity hard gate % cannot have eligible product surfaces',
            NEW.hard_gate_status;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_commerce_opportunities_gate_eligibility ON commerce_opportunities;
CREATE TRIGGER trg_commerce_opportunities_gate_eligibility
    BEFORE INSERT OR UPDATE OF
        hard_gate_status,
        eligible_wall_art_premium,
        eligible_wall_art_standard,
        eligible_calendar,
        eligible_puzzle,
        eligible_card,
        eligible_book_illustration,
        eligible_educational,
        eligible_museum_print,
        eligible_institutional_license
    ON commerce_opportunities
    FOR EACH ROW EXECUTE FUNCTION enforce_commerce_opportunity_gate_eligibility();

-- Migration 22 requirement:
-- Add enforce_commerce_opportunity_audit_exists after score_audit_log exists.

-- ---------------------------------------------------------------------------
-- Benchmark fixture bridge
-- ---------------------------------------------------------------------------
-- This guarded insert proves benchmark fixtures can be inserted when a matching
-- approved illustration opportunity exists. It is a no-op on databases without
-- source_record_id = 'commerce_benchmark_fixture_v1'.

INSERT INTO commerce_opportunities (
    opportunity_id,
    policy_version_id,
    computed_at,
    computed_by,
    computation_trigger,
    policy_stale,
    last_scored_at,
    hard_gate_status,
    rights_confidence,
    golden_age_factor,
    institutional_credit,
    provenance_completeness,
    resolution_tier_score,
    place_relevance_score,
    place_tier_score,
    illustrator_prestige,
    image_quality_score,
    composition_fit,
    identification_confidence,
    color_profile,
    color_score,
    image_width_px,
    resolution_tier,
    museum_score,
    retail_score,
    publishing_score,
    tourism_score,
    reference_score,
    commerce_opportunity_score,
    commerce_tier,
    csm_score,
    csm_tier,
    eligible_wall_art_standard,
    requires_curator_review,
    curator_review_reason,
    score_inputs,
    input_hash_sha256,
    status,
    provenance
)
SELECT
    io.id,
    cp.id,
    NOW(),
    'commerce_benchmark_fixture_v1',
    'initial',
    FALSE,
    NOW(),
    'passed',
    1.000,
    1.000,
    0.900,
    0.900,
    0.700,
    COALESCE(MAX(iop.relevance_score), 0.750),
    0.850,
    1.000,
    0.800,
    0.700,
    0.900,
    'chromolithograph',
    0.900,
    2400,
    'standard',
    0.820,
    0.780,
    0.760,
    0.740,
    0.800,
    0.784,
    'tier_2',
    0.900,
    'MASTERWORK',
    TRUE,
    TRUE,
    'boundary_case',
    '{"fixture": "commerce_benchmark_fixture_v1", "benchmark fixture": true}',
    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    'pending_review',
    '{"seeded_for": "commerce_benchmark_fixture_v1"}'
FROM illustration_opportunities io
JOIN commerce_policy cp ON cp.version = '1.0.0'
LEFT JOIN illustration_opportunity_places iop ON iop.opportunity_id = io.id
WHERE io.source_record_id = 'commerce_benchmark_fixture_v1'
  AND io.status = 'approved'
GROUP BY io.id, cp.id
ON CONFLICT (opportunity_id) DO UPDATE SET
    policy_version_id = EXCLUDED.policy_version_id,
    computed_at = EXCLUDED.computed_at,
    computed_by = EXCLUDED.computed_by,
    computation_trigger = EXCLUDED.computation_trigger,
    policy_stale = FALSE,
    last_scored_at = EXCLUDED.last_scored_at,
    hard_gate_status = EXCLUDED.hard_gate_status,
    commerce_opportunity_score = EXCLUDED.commerce_opportunity_score,
    commerce_tier = EXCLUDED.commerce_tier,
    csm_score = EXCLUDED.csm_score,
    csm_tier = EXCLUDED.csm_tier,
    score_inputs = EXCLUDED.score_inputs,
    input_hash_sha256 = EXCLUDED.input_hash_sha256,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();
