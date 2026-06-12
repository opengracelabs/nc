-- NC-AI-001 Sprint 1 runtime.
-- Graph and source evidence are authoritative.
-- LLM output is advisory until grounded, audited, and human reviewed.
-- No external model calls are made by this schema.

CREATE TABLE IF NOT EXISTS ai_model_registry (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider            TEXT NOT NULL,
    model_name          TEXT NOT NULL,
    model_family        TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'stub' CHECK (
        status IN ('stub','available','disabled','retired')
    ),
    external_calls_allowed BOOLEAN NOT NULL DEFAULT FALSE,
    capabilities        TEXT[] NOT NULL DEFAULT '{}',
    policy              JSONB NOT NULL DEFAULT '{}',
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (provider, model_name),
    CONSTRAINT chk_ai_model_no_paid_calls CHECK (external_calls_allowed = FALSE)
);

CREATE TABLE IF NOT EXISTS ai_task_policy (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_type           TEXT NOT NULL UNIQUE,
    provider_policy     TEXT NOT NULL,
    default_model_provider TEXT NOT NULL,
    human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
    grounding_required  BOOLEAN NOT NULL DEFAULT TRUE,
    publication_allowed_by_default BOOLEAN NOT NULL DEFAULT FALSE,
    cite_sources_required BOOLEAN NOT NULL DEFAULT TRUE,
    policy              JSONB NOT NULL DEFAULT '{}',
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_ai_task_no_autopublish CHECK (publication_allowed_by_default = FALSE),
    CONSTRAINT chk_ai_task_grounded_public CHECK (
        NOT (task_type IN ('place_story','product_copy','education_module','public_website_copy','user_assistant'))
        OR (grounding_required = TRUE AND cite_sources_required = TRUE)
    )
);

CREATE TABLE IF NOT EXISTS ai_prompt_template (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    template_key        TEXT NOT NULL,
    template_version    TEXT NOT NULL,
    task_type           TEXT NOT NULL REFERENCES ai_task_policy(task_type),
    body                TEXT NOT NULL,
    template_sha256     TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'active' CHECK (
        status IN ('draft','active','retired')
    ),
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (template_key, template_version),
    CONSTRAINT chk_ai_prompt_hash CHECK (template_sha256 ~ '^[0-9a-f]{64}$')
);

CREATE TABLE IF NOT EXISTS ai_generation_request (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_type           TEXT NOT NULL REFERENCES ai_task_policy(task_type),
    prompt_template_id  UUID REFERENCES ai_prompt_template(id),
    requested_by        TEXT NOT NULL,
    request_payload     JSONB NOT NULL DEFAULT '{}',
    grounding_required  BOOLEAN NOT NULL DEFAULT TRUE,
    human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
    status              TEXT NOT NULL DEFAULT 'received' CHECK (
        status IN ('received','rejected','generated','reviewed','retracted')
    ),
    rejection_reason    TEXT,
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_ai_request_actor CHECK (length(requested_by) > 0),
    CONSTRAINT chk_ai_request_no_autopublish CHECK (human_review_required = TRUE)
);

CREATE TABLE IF NOT EXISTS ai_generation_result (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    generation_request_id UUID NOT NULL REFERENCES ai_generation_request(id) ON DELETE CASCADE,
    provider            TEXT NOT NULL,
    model_name          TEXT NOT NULL,
    prompt_sha256       TEXT NOT NULL,
    output              JSONB NOT NULL DEFAULT '{}',
    output_sha256       TEXT NOT NULL,
    source_references   JSONB NOT NULL DEFAULT '[]',
    attribution_requirements JSONB NOT NULL DEFAULT '[]',
    publication_allowed BOOLEAN NOT NULL DEFAULT FALSE,
    human_review_required BOOLEAN NOT NULL DEFAULT TRUE,
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (generation_request_id),
    CONSTRAINT chk_ai_result_prompt_hash CHECK (prompt_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_ai_result_output_hash CHECK (output_sha256 ~ '^[0-9a-f]{64}$'),
    CONSTRAINT chk_ai_result_no_autopublish CHECK (
        publication_allowed = FALSE AND human_review_required = TRUE
    )
);

CREATE TABLE IF NOT EXISTS ai_grounding_source (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    generation_request_id UUID NOT NULL REFERENCES ai_generation_request(id) ON DELETE CASCADE,
    source_type         TEXT NOT NULL,
    source_id           TEXT NOT NULL,
    source_record_id    TEXT NOT NULL,
    title               TEXT NOT NULL,
    url                 TEXT,
    rights_status       TEXT,
    attribution         JSONB NOT NULL DEFAULT '{}',
    evidence            JSONB NOT NULL DEFAULT '{}',
    allowed_use         TEXT NOT NULL DEFAULT 'grounding' CHECK (
        allowed_use IN ('grounding','display_reference','product_safe')
    ),
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_ai_grounding_evidence CHECK (evidence <> '{}'::jsonb),
    CONSTRAINT chk_ai_grounding_attribution CHECK (attribution <> '{}'::jsonb),
    CONSTRAINT chk_ai_grounding_no_gbif_media CHECK (
        NOT (source_type = 'gbif' AND evidence::text ~* '(media|image|identifier)')
    ),
    CONSTRAINT chk_ai_grounding_no_wikidata_commons_product_safe CHECK (
        NOT (
            source_type = 'wikidata'
            AND allowed_use = 'product_safe'
            AND evidence::text ~* '(commons|wikimedia)'
        )
    ),
    CONSTRAINT chk_ai_grounding_osm_display_only CHECK (
        source_type <> 'osm' OR allowed_use = 'display_reference'
    )
);

CREATE TABLE IF NOT EXISTS ai_model_route_decision (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    generation_request_id UUID REFERENCES ai_generation_request(id) ON DELETE CASCADE,
    task_type           TEXT NOT NULL,
    selected_provider   TEXT NOT NULL,
    selected_model      TEXT NOT NULL,
    execution_provider  TEXT NOT NULL DEFAULT 'local',
    decision            JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ai_human_review (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    generation_result_id UUID NOT NULL REFERENCES ai_generation_result(id) ON DELETE CASCADE,
    review_status       TEXT NOT NULL DEFAULT 'pending' CHECK (
        review_status IN ('pending','approved','rejected','changes_requested')
    ),
    reviewed_by         TEXT,
    reviewed_at         TIMESTAMPTZ,
    notes               TEXT,
    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ai_audit_event (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    generation_request_id UUID REFERENCES ai_generation_request(id) ON DELETE CASCADE,
    generation_result_id UUID REFERENCES ai_generation_result(id) ON DELETE CASCADE,
    event_type          TEXT NOT NULL,
    actor               TEXT NOT NULL,
    event               JSONB NOT NULL DEFAULT '{}',
    event_sha256        TEXT NOT NULL UNIQUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_ai_audit_hash CHECK (event_sha256 ~ '^[0-9a-f]{64}$')
);

CREATE INDEX IF NOT EXISTS idx_ai_generation_request_task_status
    ON ai_generation_request(task_type, status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_generation_result_request
    ON ai_generation_result(generation_request_id);
CREATE INDEX IF NOT EXISTS idx_ai_grounding_source_request
    ON ai_grounding_source(generation_request_id);
CREATE INDEX IF NOT EXISTS idx_ai_audit_event_created
    ON ai_audit_event(created_at DESC);

DROP TRIGGER IF EXISTS trg_ai_model_registry_updated_at ON ai_model_registry;
CREATE TRIGGER trg_ai_model_registry_updated_at BEFORE UPDATE ON ai_model_registry FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_ai_task_policy_updated_at ON ai_task_policy;
CREATE TRIGGER trg_ai_task_policy_updated_at BEFORE UPDATE ON ai_task_policy FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_ai_prompt_template_updated_at ON ai_prompt_template;
CREATE TRIGGER trg_ai_prompt_template_updated_at BEFORE UPDATE ON ai_prompt_template FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_ai_generation_request_updated_at ON ai_generation_request;
CREATE TRIGGER trg_ai_generation_request_updated_at BEFORE UPDATE ON ai_generation_request FOR EACH ROW EXECUTE FUNCTION set_updated_at();
DROP TRIGGER IF EXISTS trg_ai_human_review_updated_at ON ai_human_review;
CREATE TRIGGER trg_ai_human_review_updated_at BEFORE UPDATE ON ai_human_review FOR EACH ROW EXECUTE FUNCTION set_updated_at();

INSERT INTO ai_model_registry (
    provider, model_name, model_family, status, external_calls_allowed, capabilities, policy, provenance
)
VALUES
    ('claude', 'claude-policy-stub', 'governance', 'stub', FALSE, ARRAY['rights','governance'], '{"sprint_1_stub":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('gemini', 'gemini-narrative-stub', 'narrative', 'stub', FALSE, ARRAY['story','education'], '{"sprint_1_stub":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('openai', 'gpt-copy-stub', 'narrative', 'stub', FALSE, ARRAY['copy','assistant'], '{"sprint_1_stub":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('codex', 'codex-policy-stub', 'code', 'stub', FALSE, ARRAY['code'], '{"sprint_1_stub":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('local', 'deterministic-mock-v1', 'mock', 'available', FALSE, ARRAY['deterministic_mock'], '{"external_calls":false}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb)
ON CONFLICT (provider, model_name) DO UPDATE SET
    status = EXCLUDED.status,
    external_calls_allowed = FALSE,
    capabilities = EXCLUDED.capabilities,
    policy = ai_model_registry.policy || EXCLUDED.policy,
    provenance = ai_model_registry.provenance || EXCLUDED.provenance,
    updated_at = NOW();

INSERT INTO ai_task_policy (
    task_type, provider_policy, default_model_provider, human_review_required,
    grounding_required, publication_allowed_by_default, cite_sources_required, policy, provenance
)
VALUES
    ('rights_governance', 'claude_policy', 'claude', TRUE, TRUE, FALSE, TRUE, '{"no_auto_publish":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('place_story', 'narrative_policy', 'gemini', TRUE, TRUE, FALSE, TRUE, '{"public_website_copy":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('product_copy', 'narrative_policy', 'openai', TRUE, TRUE, FALSE, TRUE, '{"public_website_copy":true,"product_safe":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('education_module', 'narrative_policy', 'gemini', TRUE, TRUE, FALSE, TRUE, '{"education":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('code_generation', 'codex_policy', 'codex', TRUE, FALSE, FALSE, FALSE, '{"operational_review_required":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('public_website_copy', 'narrative_policy', 'openai', TRUE, TRUE, FALSE, TRUE, '{"publication_review_required":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb),
    ('user_assistant', 'assistant_policy', 'openai', TRUE, TRUE, FALSE, TRUE, '{"cite_source_records":true}'::jsonb, '{"authority":"NC-AI-001"}'::jsonb)
ON CONFLICT (task_type) DO UPDATE SET
    provider_policy = EXCLUDED.provider_policy,
    default_model_provider = EXCLUDED.default_model_provider,
    human_review_required = TRUE,
    grounding_required = EXCLUDED.grounding_required,
    publication_allowed_by_default = FALSE,
    cite_sources_required = EXCLUDED.cite_sources_required,
    policy = ai_task_policy.policy || EXCLUDED.policy,
    provenance = ai_task_policy.provenance || EXCLUDED.provenance,
    updated_at = NOW();
