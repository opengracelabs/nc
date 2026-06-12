-- NC-AI-004 dynamic grounded page generation.
-- Generated page copy is advisory by default and never auto-published.

CREATE TABLE IF NOT EXISTS ai_page_generation (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page_type             TEXT NOT NULL,
    anchor_slug           TEXT NOT NULL,
    generation_purpose    TEXT NOT NULL,
    retrieval_package     JSONB NOT NULL DEFAULT '{}',
    source_references     JSONB NOT NULL DEFAULT '[]',
    provider              TEXT NOT NULL DEFAULT 'deterministic-mock-v1',
    review_status         TEXT NOT NULL DEFAULT 'pending' CHECK (
        review_status IN ('pending','approved','rejected','changes_requested')
    ),
    publication_allowed   BOOLEAN NOT NULL DEFAULT FALSE,
    human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_ai_page_generation_retrieval CHECK (retrieval_package <> '{}'::jsonb),
    CONSTRAINT chk_ai_page_generation_sources CHECK (jsonb_array_length(source_references) > 0),
    CONSTRAINT chk_ai_page_generation_review CHECK (
        publication_allowed = FALSE OR review_status = 'approved'
    ),
    CONSTRAINT chk_ai_page_generation_human_review CHECK (human_review_required = TRUE)
);

CREATE TABLE IF NOT EXISTS ai_page_generation_snapshot (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page_generation_id    UUID NOT NULL REFERENCES ai_page_generation(id) ON DELETE CASCADE,
    snapshot_version      TEXT NOT NULL,
    page_copy             JSONB NOT NULL DEFAULT '{}',
    page_copy_sha256      TEXT NOT NULL,
    attribution_block     TEXT NOT NULL,
    source_references     JSONB NOT NULL DEFAULT '[]',
    review_status         TEXT NOT NULL DEFAULT 'pending' CHECK (
        review_status IN ('pending','approved','rejected','changes_requested')
    ),
    publication_allowed   BOOLEAN NOT NULL DEFAULT FALSE,
    human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
    generated_by          TEXT NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (page_generation_id, snapshot_version),
    CONSTRAINT chk_ai_page_snapshot_copy CHECK (page_copy <> '{}'::jsonb),
    CONSTRAINT chk_ai_page_snapshot_hash CHECK (page_copy_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_ai_page_snapshot_sources CHECK (jsonb_array_length(source_references) > 0),
    CONSTRAINT chk_ai_page_snapshot_attribution CHECK (
        attribution_block LIKE '%Image credit: NASA. NASA does not endorse this product.%'
    ),
    CONSTRAINT chk_ai_page_snapshot_no_nara_earthrise CHECK (
        NOT (page_copy::text ~* '(NARA|National Archives|Verified by NASA|Moran|Smithsonian)')
    ),
    CONSTRAINT chk_ai_page_snapshot_review CHECK (
        publication_allowed = FALSE OR review_status = 'approved'
    ),
    CONSTRAINT chk_ai_page_snapshot_human_review CHECK (human_review_required = TRUE)
);

CREATE INDEX IF NOT EXISTS idx_ai_page_generation_lookup
    ON ai_page_generation(page_type, anchor_slug, review_status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_page_generation_snapshot_lookup
    ON ai_page_generation_snapshot(page_generation_id, review_status, created_at DESC);

DROP TRIGGER IF EXISTS trg_ai_page_generation_updated_at ON ai_page_generation;
CREATE TRIGGER trg_ai_page_generation_updated_at BEFORE UPDATE ON ai_page_generation
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
