-- MILESTONE-003 concept-owned commercial assets.
-- Assets belong to concepts; legacy place anchoring remains nullable for UNESCO compatibility.

ALTER TABLE assets
    ADD COLUMN IF NOT EXISTS concept_id UUID REFERENCES concepts(id);

ALTER TABLE assets
    ALTER COLUMN place_id DROP NOT NULL;

ALTER TABLE assets
    DROP CONSTRAINT IF EXISTS chk_assets_anchor;

ALTER TABLE assets
    ADD CONSTRAINT chk_assets_anchor CHECK (
        concept_id IS NOT NULL OR place_id IS NOT NULL
    );

CREATE INDEX IF NOT EXISTS idx_assets_concept
    ON assets(concept_id);

CREATE TABLE asset_rights (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id            UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    rights_status       TEXT NOT NULL,
    rights_source_url   TEXT,
    rights_statement    TEXT,
    verified_by         TEXT NOT NULL,
    verified_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_asset_rights_status CHECK (rights_status IN (
        'Public Domain','CC0'
    )),
    UNIQUE (asset_id)
);

CREATE INDEX idx_asset_rights_status
    ON asset_rights(rights_status);

CREATE TRIGGER trg_asset_rights_updated_at
    BEFORE UPDATE ON asset_rights
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION check_commercial_asset_rights_verified()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.asset_type = 'bhl_illustration'
       AND NEW.status = 'active'
       AND NOT EXISTS (
           SELECT 1
           FROM asset_rights r
           WHERE r.asset_id = NEW.id
             AND r.rights_status IN ('Public Domain','CC0')
       )
    THEN
        RAISE EXCEPTION 'commercial asset % has no explicit Public Domain or CC0 rights verification',
            NEW.id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE CONSTRAINT TRIGGER trg_commercial_asset_rights_verified
    AFTER INSERT OR UPDATE OF asset_type, status ON assets
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_commercial_asset_rights_verified();

-- MILESTONE-003 Taxon discovery.
-- Place -> GBIF/Wikidata -> ranked taxa -> BHL search targets.
-- This stage does not ingest BHL assets and does not verify asset rights.

CREATE TABLE taxon_discovery_runs (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id         UUID NOT NULL REFERENCES places(id),
    discovery_version TEXT NOT NULL DEFAULT '1',
    status           TEXT NOT NULL DEFAULT 'completed',
    parameters       JSONB NOT NULL DEFAULT '{}',
    provenance       JSONB NOT NULL DEFAULT '{}',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_taxon_discovery_run_status CHECK (status IN (
        'completed','superseded','rejected'
    )),
    UNIQUE (place_id, discovery_version)
);

CREATE TABLE taxon_candidates (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id           UUID NOT NULL REFERENCES taxon_discovery_runs(id) ON DELETE CASCADE,
    place_id         UUID NOT NULL REFERENCES places(id),
    concept_id       UUID REFERENCES concepts(id),
    scientific_name  TEXT NOT NULL,
    canonical_name   TEXT,
    taxon_rank       TEXT NOT NULL,
    gbif_taxon_key   TEXT,
    wikidata_qid     TEXT,
    common_names     TEXT[] NOT NULL DEFAULT '{}',
    status           TEXT NOT NULL DEFAULT 'candidate',

    place_relevance_score          NUMERIC(4,3) NOT NULL CHECK (place_relevance_score BETWEEN 0 AND 1),
    source_agreement_score         NUMERIC(4,3) NOT NULL CHECK (source_agreement_score BETWEEN 0 AND 1),
    illustration_likelihood_score  NUMERIC(4,3) NOT NULL CHECK (illustration_likelihood_score BETWEEN 0 AND 1),
    public_domain_path_score       NUMERIC(4,3) NOT NULL CHECK (public_domain_path_score BETWEEN 0 AND 1),
    commercial_value_score         NUMERIC(4,3) NOT NULL CHECK (commercial_value_score BETWEEN 0 AND 1),
    searchability_score            NUMERIC(4,3) NOT NULL CHECK (searchability_score BETWEEN 0 AND 1),
    total_score                    NUMERIC(4,3) NOT NULL CHECK (total_score BETWEEN 0 AND 1),

    score_components JSONB NOT NULL DEFAULT '{}',
    provenance       JSONB NOT NULL DEFAULT '{}',
    agent_notes      JSONB NOT NULL DEFAULT '{}',
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_taxon_candidate_rank CHECK (taxon_rank IN (
        'species','subspecies','genus','family'
    )),
    CONSTRAINT chk_taxon_candidate_status CHECK (status IN (
        'candidate','approved','rejected','disputed','retracted'
    )),
    CONSTRAINT chk_taxon_candidate_source CHECK (
        gbif_taxon_key IS NOT NULL OR wikidata_qid IS NOT NULL
    )
);

CREATE TABLE taxon_candidate_evidence (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id    UUID NOT NULL REFERENCES taxon_candidates(id) ON DELETE CASCADE,
    source          TEXT NOT NULL REFERENCES sources(source_id),
    evidence_type   TEXT NOT NULL,
    source_record_id TEXT,
    source_url      TEXT,
    payload         JSONB NOT NULL DEFAULT '{}',
    provenance      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_taxon_candidate_evidence_source CHECK (source IN ('gbif','wikidata')),
    CONSTRAINT chk_taxon_candidate_evidence_type CHECK (evidence_type IN (
        'occurrence_summary','taxon_identity','place_statement','name_mapping'
    ))
);

CREATE TABLE bhl_search_targets (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id    UUID NOT NULL REFERENCES taxon_candidates(id) ON DELETE CASCADE,
    sequence        INT NOT NULL CHECK (sequence > 0),
    query           TEXT NOT NULL,
    target_type     TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',
    provenance      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_bhl_search_target_type CHECK (target_type IN (
        'scientific_name','canonical_name','historic_synonym','common_name','genus'
    )),
    CONSTRAINT chk_bhl_search_target_status CHECK (status IN (
        'pending','searched','rejected'
    )),
    UNIQUE (candidate_id, query)
);

CREATE UNIQUE INDEX uniq_taxon_candidates_run_scientific_source
    ON taxon_candidates(
        run_id,
        scientific_name,
        COALESCE(gbif_taxon_key, ''),
        COALESCE(wikidata_qid, '')
    );
CREATE INDEX idx_taxon_candidates_place_score
    ON taxon_candidates(place_id, total_score DESC, scientific_name);
CREATE INDEX idx_taxon_candidates_gbif
    ON taxon_candidates(gbif_taxon_key) WHERE gbif_taxon_key IS NOT NULL;
CREATE INDEX idx_taxon_candidates_wikidata
    ON taxon_candidates(wikidata_qid) WHERE wikidata_qid IS NOT NULL;
CREATE INDEX idx_taxon_evidence_candidate_source
    ON taxon_candidate_evidence(candidate_id, source);
CREATE INDEX idx_bhl_search_targets_candidate_sequence
    ON bhl_search_targets(candidate_id, sequence);

CREATE TRIGGER trg_taxon_discovery_runs_updated_at
    BEFORE UPDATE ON taxon_discovery_runs
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_taxon_candidates_updated_at
    BEFORE UPDATE ON taxon_candidates
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION check_taxon_candidate_supported()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM taxon_candidate_evidence e
        WHERE e.candidate_id = NEW.id
          AND e.source IN ('gbif','wikidata')
    ) THEN
        RAISE EXCEPTION 'taxon candidate % has no GBIF or Wikidata evidence', NEW.id;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM bhl_search_targets t
        WHERE t.candidate_id = NEW.id
    ) THEN
        RAISE EXCEPTION 'taxon candidate % has no BHL search targets', NEW.id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE CONSTRAINT TRIGGER trg_taxon_candidate_supported
    AFTER INSERT OR UPDATE ON taxon_candidates
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_taxon_candidate_supported();

-- MILESTONE-003 Illustration opportunities.
-- Output is Illustration Opportunity, not Species.
-- Illustration opportunities are concept-owned and place-linked.

CREATE TABLE illustration_opportunities (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    concept_id          UUID NOT NULL REFERENCES concepts(id),
    source              TEXT NOT NULL REFERENCES sources(source_id),
    source_record_id    TEXT NOT NULL,
    source_url          TEXT,
    bhl_item_id         TEXT NOT NULL,
    bhl_page_id         TEXT NOT NULL,

    taxon_name          TEXT NOT NULL,
    title               TEXT,
    publication_title   TEXT NOT NULL,
    illustrator         TEXT,
    publication_year    INT CHECK (publication_year BETWEEN 1400 AND 2100),

    rights_status       TEXT NOT NULL,
    rights_source_url   TEXT,
    rights_verified_by  TEXT NOT NULL,
    rights_verified_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    illustration_quality_score NUMERIC(4,3) NOT NULL CHECK (illustration_quality_score BETWEEN 0 AND 1),
    historical_significance_score NUMERIC(4,3) NOT NULL CHECK (historical_significance_score BETWEEN 0 AND 1),
    commercial_value_score NUMERIC(4,3) NOT NULL CHECK (commercial_value_score BETWEEN 0 AND 1),
    provenance_score    NUMERIC(4,3) NOT NULL CHECK (provenance_score BETWEEN 0 AND 1),
    opportunity_score   NUMERIC(4,3) NOT NULL CHECK (opportunity_score BETWEEN 0 AND 1),

    status              TEXT NOT NULL DEFAULT 'candidate',
    reviewed_by         TEXT,
    reviewed_at         TIMESTAMPTZ,
    rejection_reason    TEXT,
    score_components    JSONB NOT NULL DEFAULT '{}',
    provenance          JSONB NOT NULL DEFAULT '{}',
    agent_notes         JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_illustration_opportunity_source CHECK (source = 'bhl'),
    CONSTRAINT chk_illustration_opportunity_rights CHECK (rights_status IN (
        'Public Domain','CC0'
    )),
    CONSTRAINT chk_illustration_opportunity_status CHECK (status IN (
        'candidate','approved','rejected','disputed','retracted'
    )),
    UNIQUE (source, source_record_id),
    UNIQUE (source, bhl_page_id)
);

CREATE TABLE illustration_opportunity_places (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id      UUID NOT NULL REFERENCES illustration_opportunities(id) ON DELETE CASCADE,
    place_id            UUID NOT NULL REFERENCES places(id),
    relevance_score     NUMERIC(4,3) NOT NULL CHECK (relevance_score BETWEEN 0 AND 1),
    evidence_summary    TEXT NOT NULL,
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (opportunity_id, place_id)
);

CREATE TABLE illustration_opportunity_evidence (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id      UUID NOT NULL REFERENCES illustration_opportunities(id) ON DELETE CASCADE,
    evidence_type       TEXT NOT NULL,
    source              TEXT NOT NULL REFERENCES sources(source_id),
    source_url          TEXT,
    payload             JSONB NOT NULL DEFAULT '{}',
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_illustration_opportunity_evidence_type CHECK (evidence_type IN (
        'rights','publication','illustration','taxonomic_context','place_relevance'
    )),
    CONSTRAINT chk_illustration_opportunity_evidence_source CHECK (source IN (
        'bhl','gbif','wikidata'
    ))
);

CREATE TABLE illustration_opportunity_assets (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id      UUID NOT NULL REFERENCES illustration_opportunities(id) ON DELETE CASCADE,
    asset_id            UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    link_type           TEXT NOT NULL DEFAULT 'source_asset',
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_illustration_opportunity_asset_link_type CHECK (link_type IN (
        'source_asset'
    )),
    UNIQUE (opportunity_id, asset_id),
    UNIQUE (opportunity_id, link_type),
    UNIQUE (asset_id)
);

CREATE INDEX idx_illustration_opportunities_concept_score
    ON illustration_opportunities(concept_id, opportunity_score DESC);
CREATE INDEX idx_illustration_opportunities_status_score
    ON illustration_opportunities(status, opportunity_score DESC);
CREATE INDEX idx_illustration_opportunity_places_place
    ON illustration_opportunity_places(place_id, relevance_score DESC);
CREATE INDEX idx_illustration_opportunity_evidence_opportunity
    ON illustration_opportunity_evidence(opportunity_id, evidence_type);
CREATE INDEX idx_illustration_opportunity_assets_opportunity
    ON illustration_opportunity_assets(opportunity_id);

CREATE TRIGGER trg_illustration_opportunities_updated_at
    BEFORE UPDATE ON illustration_opportunities
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION check_illustration_opportunity_supported()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM illustration_opportunity_evidence e
        WHERE e.opportunity_id = NEW.id
          AND e.evidence_type = 'rights'
    ) THEN
        RAISE EXCEPTION 'illustration opportunity % has no explicit rights evidence', NEW.id;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM illustration_opportunity_evidence e
        WHERE e.opportunity_id = NEW.id
          AND e.evidence_type = 'illustration'
    ) THEN
        RAISE EXCEPTION 'illustration opportunity % has no illustration evidence', NEW.id;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM illustration_opportunity_places p
        WHERE p.opportunity_id = NEW.id
    ) THEN
        RAISE EXCEPTION 'illustration opportunity % is not connected to any place', NEW.id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE CONSTRAINT TRIGGER trg_illustration_opportunity_supported
    AFTER INSERT OR UPDATE ON illustration_opportunities
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_illustration_opportunity_supported();
