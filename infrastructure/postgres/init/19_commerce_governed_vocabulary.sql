-- v0.5.0 Phase 1 / Migration 19.
-- Commerce Intelligence governed vocabulary and LOC source amendment.
--
-- No scoring worker activation.
-- No product generation.
-- No Shopify integration.

-- ---------------------------------------------------------------------------
-- 1. Director Decision B-3: allow BHL and LOC illustration opportunities
-- ---------------------------------------------------------------------------

ALTER TABLE illustration_opportunities
    DROP CONSTRAINT IF EXISTS chk_illustration_opportunity_source;

ALTER TABLE illustration_opportunities
    ADD CONSTRAINT chk_illustration_opportunity_source CHECK (source IN ('bhl','loc'));

-- ---------------------------------------------------------------------------
-- 2. Core Commerce Intelligence vocabularies
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS commerce_policy_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_policy_status_vocabulary (value, description, sort_order)
VALUES
    ('draft', 'Policy is editable and not approved.', 10),
    ('pending_approval', 'Policy is authored and awaiting second-human approval.', 20),
    ('active', 'Policy is active and governs scoring.', 30),
    ('paused', 'Policy is temporarily paused but immutable.', 40),
    ('superseded', 'Policy has been replaced by a newer version.', 50),
    ('retired', 'Policy is retained for audit but no longer used.', 60)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_tier_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_tier_vocabulary (value, description, sort_order)
VALUES
    ('tier_1', 'Premium commercial opportunity.', 10),
    ('tier_2', 'Standard retail commercial opportunity.', 20),
    ('tier_3', 'Reference or educational opportunity.', 30),
    ('blocked', 'No commercial routing.', 40)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_csm_tier_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_csm_tier_vocabulary (value, description, sort_order)
VALUES
    ('MASTERWORK', 'CSM score 0.90 to 1.00; premium anchor.', 10),
    ('FLAGSHIP', 'CSM score 0.75 to 0.89; core catalog asset.', 20),
    ('STANDARD', 'CSM score 0.60 to 0.74; long-tail commercial asset.', 30),
    ('REFERENCE', 'CSM score 0.40 to 0.59; education or reference only.', 40),
    ('BLOCKED', 'CSM score below 0.40 or blocked by gate.', 50)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_hard_gate_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_hard_gate_status_vocabulary (value, description, sort_order)
VALUES
    ('passed', 'All hard gates passed.', 10),
    ('blocked_rights', 'Rights gate blocked scoring or routing.', 20),
    ('blocked_resolution', 'Resolution gate blocked scoring or routing.', 30),
    ('blocked_quality', 'Quality gate blocked scoring or routing.', 40),
    ('blocked_legal', 'Legal gate blocked scoring or routing.', 50),
    ('not_evaluated', 'Hard gates have not been evaluated.', 60)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_computation_trigger_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_computation_trigger_vocabulary (value, description, sort_order)
VALUES
    ('initial', 'Initial computation.', 10),
    ('policy_version_change', 'Computation caused by policy version change.', 20),
    ('signal_correction', 'Computation caused by signal correction.', 30),
    ('manual_recompute', 'Computation manually requested.', 40),
    ('rights_update', 'Computation caused by rights update.', 50)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_curator_decision_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_curator_decision_vocabulary (value, description, sort_order)
VALUES
    ('approved', 'Curator approved.', 10),
    ('rejected', 'Curator rejected.', 20),
    ('pending', 'Curator decision is pending.', 30),
    ('escalated', 'Curator escalated for further review.', 40)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_curator_review_reason_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_curator_review_reason_vocabulary (value, description, sort_order)
VALUES
    ('priority_illustrator', 'Priority illustrator requires review.', 10),
    ('boundary_case', 'Score or routing boundary case.', 20),
    ('manual_flag', 'Manually flagged for review.', 30),
    ('rights_anomaly', 'Rights signal requires review.', 40),
    ('none', 'No special review reason.', 50)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_recommendation_status_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_recommendation_status_vocabulary (value, description, sort_order)
VALUES
    ('pending_curator_review', 'Recommendation awaits curator review.', 10),
    ('curator_approved', 'Recommendation approved by curator.', 20),
    ('curator_rejected', 'Recommendation rejected by curator.', 30),
    ('assigned', 'Recommendation assigned to downstream planning.', 40),
    ('retired', 'Recommendation retired.', 50)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_collection_gap_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_collection_gap_type_vocabulary (value, description, sort_order)
VALUES
    ('fills_gap', 'Opportunity fills a collection gap.', 10),
    ('reinforces_strength', 'Opportunity reinforces a collection strength.', 20),
    ('expands_coverage', 'Opportunity expands place or concept coverage.', 30),
    ('flagship_anchor', 'Opportunity can anchor a flagship collection.', 40),
    ('none', 'No collection gap identified.', 50)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_audit_event_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_audit_event_type_vocabulary (value, description, sort_order)
VALUES
    ('score_computed', 'Score computed or recomputed.', 10),
    ('signal_updated', 'Signal updated by authorized actor.', 20),
    ('hard_gate_blocked', 'Hard gate blocked scoring or routing.', 30),
    ('hard_gate_passed', 'Hard gate passed.', 40),
    ('curator_reviewed', 'Curator reviewed record.', 50),
    ('tier_assigned', 'Tier assigned or changed.', 60),
    ('policy_applied', 'Policy applied to record.', 70),
    ('eligibility_updated', 'Product eligibility updated.', 80),
    ('score_archived', 'Score archived.', 90),
    ('replay_verified', 'Replay verified.', 100),
    ('replay_failure', 'Replay failed.', 110)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_actor_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_actor_type_vocabulary (value, description, sort_order)
VALUES
    ('system_worker', 'System worker actor.', 10),
    ('curator', 'Curator actor.', 20),
    ('policy_approver', 'Policy approver actor.', 30),
    ('administrator', 'Administrator actor.', 40)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

-- ---------------------------------------------------------------------------
-- 3. Governed signal vocabularies with independent lifecycle
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS taxon_commercial_tier_vocabulary (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    value          TEXT NOT NULL UNIQUE,
    description    TEXT NOT NULL,
    score          NUMERIC(4,3) NOT NULL CHECK (score BETWEEN 0 AND 1),
    status         TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by    TEXT NOT NULL,
    approved_by    TEXT,
    approved_at    TIMESTAMPTZ,
    provenance     JSONB NOT NULL DEFAULT '{}',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_taxon_commercial_tier_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    )
);

INSERT INTO taxon_commercial_tier_vocabulary (
    value, description, score, status, authored_by, provenance
)
VALUES
    ('high', 'High commercial tier taxon.', 1.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('moderate', 'Moderate commercial tier taxon.', 0.650, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('low', 'Low commercial tier taxon.', 0.300, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('none', 'No taxon commercial tier.', 0.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}')
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    score = EXCLUDED.score,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

CREATE TABLE IF NOT EXISTS priority_illustrators_vocabulary (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    canonical_name TEXT NOT NULL UNIQUE,
    display_name   TEXT NOT NULL,
    prestige_score NUMERIC(4,3) NOT NULL CHECK (prestige_score BETWEEN 0 AND 1),
    status         TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by    TEXT NOT NULL,
    approved_by    TEXT,
    approved_at    TIMESTAMPTZ,
    provenance     JSONB NOT NULL DEFAULT '{}',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_priority_illustrator_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    )
);

INSERT INTO priority_illustrators_vocabulary (
    canonical_name, display_name, prestige_score, status, authored_by, provenance
)
VALUES
    ('audubon', 'Audubon', 1.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('gould', 'Gould', 1.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('merian', 'Merian', 1.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('redoute', 'Redoute', 1.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('lear', 'Lear', 1.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('nodder', 'Nodder', 1.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('haeckel', 'Haeckel', 1.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}'),
    ('wolf', 'Wolf', 1.000, 'proposed', 'commerce_migration_19', '{"seeded_for": "commerce_benchmark_fixture_v1"}')
ON CONFLICT (canonical_name) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    prestige_score = EXCLUDED.prestige_score,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();

CREATE TABLE IF NOT EXISTS commerce_place_tier_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    score       NUMERIC(4,3) NOT NULL CHECK (score BETWEEN 0 AND 1),
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_place_tier_vocabulary (value, description, score, sort_order)
VALUES
    ('unesco_flagship', 'UNESCO flagship place.', 1.000, 10),
    ('national_park', 'National park place.', 0.850, 20),
    ('regional', 'Regional place.', 0.550, 30),
    ('local', 'Local place.', 0.350, 40),
    ('none', 'No place tier.', 0.000, 50)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    score = EXCLUDED.score,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS place_iconic_taxa_vocabulary (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id        UUID NOT NULL REFERENCES places(id),
    concept_id      UUID REFERENCES concepts(id),
    scientific_name TEXT NOT NULL,
    common_name     TEXT,
    iconic_score    NUMERIC(4,3) NOT NULL CHECK (iconic_score BETWEEN 0 AND 1),
    status          TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by     TEXT NOT NULL,
    approved_by     TEXT,
    approved_at     TIMESTAMPTZ,
    provenance      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_place_iconic_taxa_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    ),
    UNIQUE (place_id, scientific_name)
);

CREATE TABLE IF NOT EXISTS commerce_color_profile_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    score       NUMERIC(4,3) NOT NULL CHECK (score BETWEEN 0 AND 1),
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_color_profile_vocabulary (value, description, score, sort_order)
VALUES
    ('hand_colored', 'Hand-colored image.', 1.000, 10),
    ('chromolithograph', 'Chromolithograph image.', 0.900, 20),
    ('bw_engraving', 'Black-and-white engraving.', 0.650, 30),
    ('photographic', 'Photographic image.', 0.600, 40),
    ('unknown', 'Unknown color profile.', 0.300, 50)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    score = EXCLUDED.score,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_resolution_tier_vocabulary (
    value        TEXT PRIMARY KEY,
    description  TEXT NOT NULL,
    min_width_px INT,
    score        NUMERIC(4,3) NOT NULL CHECK (score BETWEEN 0 AND 1),
    sort_order   INT NOT NULL UNIQUE
);

INSERT INTO commerce_resolution_tier_vocabulary (value, description, min_width_px, score, sort_order)
VALUES
    ('premium', 'Premium print resolution.', 4000, 1.000, 10),
    ('standard', 'Standard print resolution.', 2000, 0.700, 20),
    ('marginal', 'Marginal print resolution.', 1200, 0.350, 30),
    ('blocked', 'Blocked by resolution.', NULL, 0.000, 40)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    min_width_px = EXCLUDED.min_width_px,
    score = EXCLUDED.score,
    sort_order = EXCLUDED.sort_order;

CREATE TABLE IF NOT EXISTS commerce_anchor_type_vocabulary (
    value       TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    sort_order  INT NOT NULL UNIQUE
);

INSERT INTO commerce_anchor_type_vocabulary (value, description, sort_order)
VALUES
    ('biological', 'Biological anchor.', 10),
    ('geographic', 'Geographic anchor.', 20),
    ('cultural', 'Cultural anchor.', 30)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;

-- ---------------------------------------------------------------------------
-- 4. Indexes and updated_at triggers
-- ---------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_taxon_commercial_tier_status
    ON taxon_commercial_tier_vocabulary(status, value);

CREATE INDEX IF NOT EXISTS idx_priority_illustrators_status
    ON priority_illustrators_vocabulary(status, canonical_name);

CREATE INDEX IF NOT EXISTS idx_place_iconic_taxa_place_status
    ON place_iconic_taxa_vocabulary(place_id, status, iconic_score DESC);

CREATE INDEX IF NOT EXISTS idx_place_iconic_taxa_concept
    ON place_iconic_taxa_vocabulary(concept_id)
    WHERE concept_id IS NOT NULL;

DROP TRIGGER IF EXISTS trg_taxon_commercial_tier_updated_at ON taxon_commercial_tier_vocabulary;
CREATE TRIGGER trg_taxon_commercial_tier_updated_at
    BEFORE UPDATE ON taxon_commercial_tier_vocabulary
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_priority_illustrators_updated_at ON priority_illustrators_vocabulary;
CREATE TRIGGER trg_priority_illustrators_updated_at
    BEFORE UPDATE ON priority_illustrators_vocabulary
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_place_iconic_taxa_updated_at ON place_iconic_taxa_vocabulary;
CREATE TRIGGER trg_place_iconic_taxa_updated_at
    BEFORE UPDATE ON place_iconic_taxa_vocabulary
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
