-- NC-AI-005 review queue, publication snapshots, page version history.
-- AI page output remains unpublished until explicit human approval.

CREATE TABLE IF NOT EXISTS ai_page_review_queue (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page_generation_id    UUID NOT NULL REFERENCES ai_page_generation(id) ON DELETE CASCADE,
    snapshot_id           UUID NOT NULL REFERENCES ai_page_generation_snapshot(id) ON DELETE CASCADE,
    review_status         TEXT NOT NULL DEFAULT 'pending' CHECK (
        review_status IN ('pending','approved','rejected','changes_requested','completed')
    ),
    assigned_to           TEXT,
    reviewed_by           TEXT,
    reviewed_at           TIMESTAMPTZ,
    notes                 TEXT,
    publication_allowed   BOOLEAN NOT NULL DEFAULT FALSE,
    human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
    queue_item_sha256     TEXT NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (page_generation_id, snapshot_id),
    CONSTRAINT chk_ai_page_review_queue_hash CHECK (queue_item_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_ai_page_review_queue_human CHECK (human_review_required = TRUE),
    CONSTRAINT chk_ai_page_review_queue_publication CHECK (
        publication_allowed = FALSE OR review_status IN ('approved','completed')
    )
);

CREATE TABLE IF NOT EXISTS ai_page_publication_snapshot (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page_generation_id    UUID NOT NULL REFERENCES ai_page_generation(id) ON DELETE CASCADE,
    source_snapshot_id    UUID NOT NULL REFERENCES ai_page_generation_snapshot(id) ON DELETE RESTRICT,
    publication_version   TEXT NOT NULL,
    page_copy             JSONB NOT NULL DEFAULT '{}',
    page_copy_sha256      TEXT NOT NULL,
    attribution_block     TEXT NOT NULL,
    source_references     JSONB NOT NULL DEFAULT '[]',
    publication_status    TEXT NOT NULL DEFAULT 'active' CHECK (
        publication_status IN ('active','superseded','rolled_back','retracted')
    ),
    approved_by           TEXT NOT NULL,
    approval_event_sha256 TEXT NOT NULL,
    rollback_of_publication_snapshot_id UUID REFERENCES ai_page_publication_snapshot(id),
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (page_generation_id, publication_version),
    CONSTRAINT chk_ai_page_publication_copy CHECK (page_copy <> '{}'::jsonb),
    CONSTRAINT chk_ai_page_publication_hash CHECK (page_copy_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_ai_page_publication_sources CHECK (jsonb_array_length(source_references) > 0),
    CONSTRAINT chk_ai_page_publication_attribution CHECK (
        attribution_block LIKE '%Image credit: NASA. NASA does not endorse this product.%'
    ),
    CONSTRAINT chk_ai_page_publication_no_prohibited CHECK (
        NOT (page_copy::text ~* '(NARA|National Archives|Verified by NASA|Moran|Smithsonian)')
    ),
    CONSTRAINT chk_ai_page_publication_event_hash CHECK (
        approval_event_sha256 ~ '^[0-9a-f]{64}$'
    )
);

CREATE TABLE IF NOT EXISTS ai_page_version_history (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page_generation_id    UUID NOT NULL REFERENCES ai_page_generation(id) ON DELETE CASCADE,
    snapshot_id           UUID REFERENCES ai_page_generation_snapshot(id) ON DELETE SET NULL,
    publication_snapshot_id UUID REFERENCES ai_page_publication_snapshot(id) ON DELETE SET NULL,
    event_type            TEXT NOT NULL CHECK (
        event_type IN ('queued_generation','approved_generation','rollback_generation','rejected_generation')
    ),
    actor                 TEXT NOT NULL,
    event                 JSONB NOT NULL DEFAULT '{}',
    event_sha256          TEXT NOT NULL UNIQUE,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_ai_page_version_event_hash CHECK (event_sha256 ~ '^[0-9a-f]{64}$')
);

CREATE INDEX IF NOT EXISTS idx_ai_page_review_queue_status
    ON ai_page_review_queue(review_status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_page_publication_active
    ON ai_page_publication_snapshot(page_generation_id, publication_status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_page_version_history_generation
    ON ai_page_version_history(page_generation_id, created_at DESC);

DROP TRIGGER IF EXISTS trg_ai_page_review_queue_updated_at ON ai_page_review_queue;
CREATE TRIGGER trg_ai_page_review_queue_updated_at BEFORE UPDATE ON ai_page_review_queue
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
