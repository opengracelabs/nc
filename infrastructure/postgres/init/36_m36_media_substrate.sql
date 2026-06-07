-- M36 Universal Media Substrate
-- Authority: MSC v1.2, DD-EUR-001 Article 4, M36 Engineering Specification v2
--
-- Implements (in sequence):
--   M36-002  media_type_registry
--   M36-003  media_type_registry seed (11 types; Phase 1 active, Phase 2-4 pending)
--   M36-004  source_item (nullable current FKs; constraints added in M36-008)
--   M36-005  source_record
--   M36-006  media_rights
--   M36-007  media_technical_metadata
--   M36-008  source_item current FK constraints (ALTER TABLE)
--   M36-009  media_file                          — closes S-1
--   M36-011  preservation_event                 — closes S-2 (M36-010 deferred)
--   M36-012  media_file.ingestion_event_id FK   (ALTER TABLE)
--   M36-016  Trigger suite (immutability + pending-type ingestion block)
--   M36-017  Index suite
--
-- Deferred (not required for first production ingestion):
--   M36-001  Separate vocabulary tables (absorbed as CHECK constraints below)
--   M36-010  media_derivative
--   M36-013  asset_delivery_manifest
--   M36-014  activation_target
--   M36-015  activation_target_downstream_link
--   M36-018  Compatibility views

-- ---------------------------------------------------------------------------
-- M36-002: media_type_registry
-- ---------------------------------------------------------------------------

CREATE TABLE media_type_registry (
    media_type_id               TEXT PRIMARY KEY,
    display_name                TEXT NOT NULL,
    expansion_phase             INT  NOT NULL CHECK (expansion_phase IN (1, 2, 3, 4)),
    anchor_types_allowed        TEXT[] NOT NULL DEFAULT '{}',
    delivery_protocol           TEXT,
    archival_format             TEXT,
    delivery_format             TEXT,
    requires_file_manifest      BOOLEAN NOT NULL DEFAULT FALSE,
    content_spec_schema         TEXT,
    content_spec_schema_version TEXT,
    status                      TEXT NOT NULL DEFAULT 'pending'
                                    CHECK (status IN ('active', 'pending', 'deprecated')),
    constitutional_ref          TEXT,
    authored_by                 TEXT,
    approved_by                 TEXT,
    approved_at                 TIMESTAMPTZ,
    provenance                  JSONB NOT NULL DEFAULT '{}',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- M36-003: media_type_registry seed
-- Phase 1 (active): image, map, photography, poster  — MSC v1.2 Article 5.1
-- Phase 2 (pending): book, ebook
-- Phase 3 (pending): audiobook, audio, film
-- Phase 4 (pending): 3d, dataset
-- ---------------------------------------------------------------------------

INSERT INTO media_type_registry (
    media_type_id, display_name, expansion_phase,
    anchor_types_allowed, delivery_protocol, archival_format, delivery_format,
    requires_file_manifest, status, constitutional_ref, authored_by,
    approved_by, approved_at, provenance
) VALUES
    ('image',       'Image',        1,
     ARRAY['biological','geographic','cultural','mixed'],
     'iiif', 'tiff', 'jpeg', TRUE, 'active', 'MSC v1.2 Article 5.1', 'system',
     'msc_v1.2', '2026-06-07'::timestamptz, '{}'),

    ('map',         'Map',          1,
     ARRAY['geographic','mixed'],
     'iiif', 'tiff', 'jpeg', TRUE, 'active', 'MSC v1.2 Article 5.1', 'system',
     'msc_v1.2', '2026-06-07'::timestamptz, '{}'),

    ('photography', 'Photography',  1,
     ARRAY['biological','geographic','cultural','mixed'],
     'iiif', 'tiff', 'jpeg', TRUE, 'active', 'MSC v1.2 Article 5.1', 'system',
     'msc_v1.2', '2026-06-07'::timestamptz, '{}'),

    ('poster',      'Poster',       1,
     ARRAY['biological','geographic','cultural','mixed'],
     'iiif', 'tiff', 'jpeg', TRUE, 'active', 'MSC v1.2 Article 5.1', 'system',
     'msc_v1.2', '2026-06-07'::timestamptz, '{}'),

    ('book',        'Book',         2,
     ARRAY['cultural','mixed'],
     'epub', 'epub', 'epub', FALSE, 'pending', 'MSC v1.2 Article 5.2', 'system',
     NULL, NULL, '{}'),

    ('ebook',       'Ebook',        2,
     ARRAY['cultural','mixed'],
     'epub', 'epub', 'epub', FALSE, 'pending', 'MSC v1.2 Article 5.2', 'system',
     NULL, NULL, '{}'),

    ('audiobook',   'Audiobook',    3,
     ARRAY['cultural','mixed'],
     'hls', 'wav', 'aac', FALSE, 'pending', 'MSC v1.2 Article 5.3', 'system',
     NULL, NULL, '{}'),

    ('audio',       'Audio',        3,
     ARRAY['cultural','mixed'],
     'hls', 'wav', 'aac', FALSE, 'pending', 'MSC v1.2 Article 5.3', 'system',
     NULL, NULL, '{}'),

    ('film',        'Film',         3,
     ARRAY['cultural','mixed'],
     'hls', 'mkv', 'mp4', FALSE, 'pending', 'MSC v1.2 Article 5.3', 'system',
     NULL, NULL, '{}'),

    ('3d',          '3D Model',     4,
     ARRAY['cultural','mixed'],
     'gltf', 'gltf', 'gltf', FALSE, 'pending', 'MSC v1.2 Article 5.4', 'system',
     NULL, NULL, '{}'),

    ('dataset',     'Dataset',      4,
     ARRAY['cultural','mixed'],
     'csv', 'csv', 'csv', FALSE, 'pending', 'MSC v1.2 Article 5.4', 'system',
     NULL, NULL, '{}');

-- ---------------------------------------------------------------------------
-- M36-004: source_item
-- Nullable current FKs — constraints added in M36-008 after downstream tables exist.
-- ---------------------------------------------------------------------------

CREATE TABLE source_item (
    id                              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source_id                       TEXT NOT NULL REFERENCES sources(source_id),
    source_identifier               TEXT NOT NULL,
    media_type_id                   TEXT NOT NULL REFERENCES media_type_registry(media_type_id),
    canonical_source_url            TEXT,
    title                           TEXT,

    status                          TEXT NOT NULL DEFAULT 'proposed'
                                        CHECK (status IN (
                                            'proposed', 'acquired', 'rights_verified',
                                            'activation_eligible', 'activated'
                                        )),
    anchor_type                     TEXT NOT NULL
                                        CHECK (anchor_type IN (
                                            'biological', 'geographic', 'cultural', 'mixed'
                                        )),

    -- Current pointers — nullable until first substrate records are pinned.
    -- FK constraints added in M36-008.
    current_source_record_id        UUID,
    current_media_rights_id         UUID,
    current_technical_metadata_id   UUID,

    provenance                      JSONB NOT NULL DEFAULT '{}',
    created_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (source_id, source_identifier)
);

-- ---------------------------------------------------------------------------
-- M36-005: source_record
-- Raw payload is immutable after insert. Refetch creates a new row.
-- ---------------------------------------------------------------------------

CREATE TABLE source_record (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source_item_id      UUID NOT NULL REFERENCES source_item(id),
    institution_id      TEXT,
    source_identifier   TEXT NOT NULL,
    schema_standard     TEXT NOT NULL,

    raw_payload         JSONB NOT NULL,
    raw_payload_hash    TEXT NOT NULL,
    normalized_payload  JSONB NOT NULL,

    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fetched_by          TEXT NOT NULL,

    superseded_by       UUID REFERENCES source_record(id),

    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- M36-006: media_rights
-- verified_by / verified_at are NULL until human verification.
-- Terminal statuses (verified_pd, verified_cc0) require human actor.
-- ---------------------------------------------------------------------------

CREATE TABLE media_rights (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source_item_id              UUID NOT NULL REFERENCES source_item(id),
    rights_status               TEXT NOT NULL
                                    CHECK (rights_status IN (
                                        'pending_verification', 'verified_pd',
                                        'verified_cc0', 'blocked'
                                    )),
    rights_statement_uri        TEXT,
    rights_evidence             JSONB NOT NULL DEFAULT '{}',

    commercial_reuse_permitted  BOOLEAN NOT NULL DEFAULT FALSE,
    modification_permitted      BOOLEAN NOT NULL DEFAULT FALSE,

    -- NULL until human verification completes.
    verified_by                 TEXT,
    verified_at                 TIMESTAMPTZ,
    authored_by                 TEXT,

    superseded_by               UUID REFERENCES media_rights(id),

    provenance                  JSONB NOT NULL DEFAULT '{}',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- M36-007: media_technical_metadata
-- ---------------------------------------------------------------------------

CREATE TABLE media_technical_metadata (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source_item_id      UUID NOT NULL REFERENCES source_item(id),
    media_type_id       TEXT NOT NULL REFERENCES media_type_registry(media_type_id),
    schema_version      TEXT NOT NULL,

    content             JSONB NOT NULL,
    validation_status   TEXT NOT NULL DEFAULT 'valid'
                            CHECK (validation_status IN ('valid', 'invalid', 'warnings')),
    validated_by        TEXT,
    validated_at        TIMESTAMPTZ,
    validator_name      TEXT,
    validator_version   TEXT,
    content_hash        TEXT NOT NULL,

    superseded_by       UUID REFERENCES media_technical_metadata(id),

    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- M36-008: Add current FK constraints to source_item
-- These could not be added in M36-004 because the referenced tables did not
-- exist yet. All three FKs are nullable — source_item exists before its
-- substrate records are written.
-- ---------------------------------------------------------------------------

ALTER TABLE source_item
    ADD CONSTRAINT source_item_current_source_record_fk
        FOREIGN KEY (current_source_record_id)
        REFERENCES source_record(id) DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT source_item_current_media_rights_fk
        FOREIGN KEY (current_media_rights_id)
        REFERENCES media_rights(id) DEFERRABLE INITIALLY DEFERRED,
    ADD CONSTRAINT source_item_current_technical_metadata_fk
        FOREIGN KEY (current_technical_metadata_id)
        REFERENCES media_technical_metadata(id) DEFERRABLE INITIALLY DEFERRED;

-- ---------------------------------------------------------------------------
-- M36-009: media_file                                              CLOSES S-1
-- EDM WebResource layer. Binary is not required at row creation.
-- ingestion_event_id FK added in M36-012 after preservation_event exists.
-- ---------------------------------------------------------------------------

CREATE TABLE media_file (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source_item_id      UUID NOT NULL REFERENCES source_item(id),
    source_record_id    UUID NOT NULL REFERENCES source_record(id),
    media_type_id       TEXT NOT NULL REFERENCES media_type_registry(media_type_id),

    file_role           TEXT NOT NULL DEFAULT 'primary'
                            CHECK (file_role IN ('primary', 'supplementary', 'thumbnail')),
    sequence_position   INT  NOT NULL DEFAULT 1,

    source_url          TEXT,
    original_filename   TEXT,

    -- NULL until binary is retrieved and stored in MinIO.
    minio_bucket        TEXT,
    minio_key           TEXT,
    mime_type           TEXT,
    byte_size           BIGINT,
    checksum_sha256     TEXT,

    preservation_status TEXT NOT NULL DEFAULT 'pending_retrieval'
                            CHECK (preservation_status IN (
                                'pending_retrieval', 'retrieved',
                                'verified', 'worm_committed'
                            )),

    -- FK to preservation_event added in M36-012.
    ingestion_event_id  UUID,

    provenance          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- M36-011: preservation_event                                      CLOSES S-2
-- Append-only. No UPDATE or DELETE permitted (enforced by triggers in M36-016).
-- M36-010 (media_derivative) is deferred; media_derivative_id is untyped UUID.
-- ---------------------------------------------------------------------------

CREATE TABLE preservation_event (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    subject_type        TEXT NOT NULL,
    subject_id          UUID NOT NULL,

    -- media_file FK navigates the event back to the file it describes.
    -- NULL for rights_verification events (subject is media_rights, not a file).
    media_file_id       UUID REFERENCES media_file(id),

    -- Untyped until M36-010 creates media_derivative.
    media_derivative_id UUID,

    event_type          TEXT NOT NULL,
    event_datetime      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_outcome       TEXT NOT NULL,
    event_detail        JSONB NOT NULL DEFAULT '{}',

    agent_type          TEXT NOT NULL CHECK (agent_type IN ('worker', 'human')),
    agent_id            TEXT NOT NULL,

    -- No updated_at: preservation_event is append-only.
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- M36-012: file-event FK integrity
-- ingestion_event_id left NULL in Sprint 3 (binary not yet retrieved).
-- FK is deferred so the event can be inserted in the same transaction as the
-- media_file row that references it, if needed in future sprints.
-- ---------------------------------------------------------------------------

ALTER TABLE media_file
    ADD CONSTRAINT media_file_ingestion_event_fk
        FOREIGN KEY (ingestion_event_id)
        REFERENCES preservation_event(id) DEFERRABLE INITIALLY DEFERRED;

-- ---------------------------------------------------------------------------
-- M36-016: Trigger suite
-- Minimum set required for constitutional compliance at ingestion time.
-- ---------------------------------------------------------------------------

-- Prevent DELETE on source_item (no-DELETE invariant: identity is permanent).
CREATE OR REPLACE FUNCTION _trg_source_item_no_delete()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'source_item rows are permanent: DELETE is not permitted (M36-016).';
END;
$$;
CREATE TRIGGER trg_source_item_no_delete
    BEFORE DELETE ON source_item
    FOR EACH ROW EXECUTE FUNCTION _trg_source_item_no_delete();

-- Prevent DELETE on source_record (raw payload immutability).
CREATE OR REPLACE FUNCTION _trg_source_record_no_delete()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'source_record rows are immutable: DELETE is not permitted (M36-016).';
END;
$$;
CREATE TRIGGER trg_source_record_no_delete
    BEFORE DELETE ON source_record
    FOR EACH ROW EXECUTE FUNCTION _trg_source_record_no_delete();

-- Prevent DELETE and UPDATE on preservation_event (append-only, PREMIS invariant).
CREATE OR REPLACE FUNCTION _trg_preservation_event_immutable()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION
        'preservation_event is append-only: % is not permitted (M36-016, RM-6).',
        TG_OP;
END;
$$;
CREATE TRIGGER trg_preservation_event_no_delete
    BEFORE DELETE ON preservation_event
    FOR EACH ROW EXECUTE FUNCTION _trg_preservation_event_immutable();
CREATE TRIGGER trg_preservation_event_no_update
    BEFORE UPDATE ON preservation_event
    FOR EACH ROW EXECUTE FUNCTION _trg_preservation_event_immutable();

-- Block ingestion of pending media types (Phase 2-4 gate).
CREATE OR REPLACE FUNCTION _trg_source_item_media_type_gate()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE
    v_status TEXT;
BEGIN
    SELECT status INTO v_status
    FROM media_type_registry
    WHERE media_type_id = NEW.media_type_id;

    IF v_status IS DISTINCT FROM 'active' THEN
        RAISE EXCEPTION
            'Ingestion blocked: media_type_id=% has status=% — only active types may ingest (MSC v1.2 Phase gate).',
            NEW.media_type_id, COALESCE(v_status, 'not_found');
    END IF;
    RETURN NEW;
END;
$$;
CREATE TRIGGER trg_source_item_media_type_gate
    BEFORE INSERT ON source_item
    FOR EACH ROW EXECUTE FUNCTION _trg_source_item_media_type_gate();

-- Prevent raw_payload mutation on source_record (immutability invariant).
CREATE OR REPLACE FUNCTION _trg_source_record_raw_payload_immutable()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.raw_payload IS DISTINCT FROM OLD.raw_payload
    OR NEW.raw_payload_hash IS DISTINCT FROM OLD.raw_payload_hash THEN
        RAISE EXCEPTION
            'source_record.raw_payload is immutable after insert (M36-016).';
    END IF;
    RETURN NEW;
END;
$$;
CREATE TRIGGER trg_source_record_raw_payload_immutable
    BEFORE UPDATE ON source_record
    FOR EACH ROW EXECUTE FUNCTION _trg_source_record_raw_payload_immutable();

-- ---------------------------------------------------------------------------
-- M36-017: Index suite
-- ---------------------------------------------------------------------------

-- source_item lookup by source + external identifier (replay anchor)
CREATE INDEX idx_source_item_source_id    ON source_item(source_id);
CREATE UNIQUE INDEX idx_source_item_identity
    ON source_item(source_id, source_identifier);
CREATE INDEX idx_source_item_status       ON source_item(status);
CREATE INDEX idx_source_item_media_type   ON source_item(media_type_id);

-- source_record lookup
CREATE INDEX idx_source_record_item       ON source_record(source_item_id);
CREATE INDEX idx_source_record_hash       ON source_record(raw_payload_hash);

-- media_rights lookup
CREATE INDEX idx_media_rights_item        ON media_rights(source_item_id);
CREATE INDEX idx_media_rights_status      ON media_rights(rights_status);

-- media_technical_metadata lookup
CREATE INDEX idx_media_technical_item     ON media_technical_metadata(source_item_id);
CREATE INDEX idx_media_technical_hash     ON media_technical_metadata(content_hash);

-- media_file lookup
CREATE INDEX idx_media_file_item          ON media_file(source_item_id);
CREATE INDEX idx_media_file_record        ON media_file(source_record_id);
CREATE INDEX idx_media_file_preservation  ON media_file(preservation_status);

-- preservation_event lookup (audit trail)
CREATE INDEX idx_preservation_event_subject
    ON preservation_event(subject_type, subject_id);
CREATE INDEX idx_preservation_event_type
    ON preservation_event(event_type);
CREATE INDEX idx_preservation_event_media_file
    ON preservation_event(media_file_id)
    WHERE media_file_id IS NOT NULL;
CREATE INDEX idx_preservation_event_outcome
    ON preservation_event(event_outcome);
