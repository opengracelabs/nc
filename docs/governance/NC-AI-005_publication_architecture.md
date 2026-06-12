# NC-AI-005: Publication Architecture

| Field | Value |
|---|---|
| Document | NC-AI-005 |
| Version | 1.0 |
| Status | **DRAFT** — pending ratification |
| Date | 2026-06-12 |
| Authority | NC-AI-004 · NC-AI-001 · Foundation Model Constitution v1.0 |
| Governs | AI-generated page copy lifecycle: generation → review → approval → publication → rollback → version history |
| Stack | PostgreSQL + FastAPI (no external state stores) |
| **Decision** | **APPROVE WITH CONDITIONS** |

---

## I. Purpose

NC-AI-004 defined governance rules for five page families and specified the lifecycle stages a generated copy candidate must pass through before reaching a public surface. NC-AI-005 translates those rules into a concrete, implementable architecture: the exact state machine, database schema extensions, API endpoint specifications, and service-layer contracts that make the lifecycle operational.

**Current state after NC-AI-004 implementation:** The generation pipeline writes to `ai_page_generation` and `ai_page_generation_snapshot` (migration 44). But:
- No endpoint exists to submit a review decision on a snapshot
- `publication_allowed` is hardcoded `FALSE` in all INSERTs with no write path to `TRUE`
- No reviewer queue exists
- No two-human gate is wired for MASTERWORK tier
- No rollback trigger or endpoint exists
- No version history endpoint exists
- `chk_ai_page_snapshot_attribution` enforces NASA nonendorsement on all snapshots regardless of page — a constraint bug for non-NASA pages (§II.3)

NC-AI-005 fills these gaps.

---

## II. Pre-Architecture Findings (from codebase review)

### II.1 Publication blocked at database layer

`ai_page_generation_snapshot` has:
```sql
CONSTRAINT chk_ai_page_snapshot_review CHECK (
    publication_allowed = FALSE OR review_status = 'approved'
)
```

This correctly requires `review_status = 'approved'` before `publication_allowed = TRUE` can be set. However, no application path sets `publication_allowed = TRUE` after review approval. The pipeline terminates at `pending`. NC-AI-005 must wire the approval-to-publication transition.

### II.2 Missing review endpoints

The router (`services/ai/router.py`) has:
- `POST /ai/page-generation` — generates and persists snapshot (works)
- `GET /ai/page-generation/{page_type}/{anchor_slug}` — retrieves published copy (works as read, but returns 404 always since nothing is ever approved)

Missing:
- `GET /ai/review-queue` — list snapshots pending review
- `POST /ai/page-generation/{snapshot_id}/review` — submit a review decision
- `POST /ai/page-generation/{snapshot_id}/publish` — promote approved snapshot to live
- `POST /ai/page-generation/{snapshot_id}/rollback` — roll back to a previous version
- `GET /ai/page-generation/{page_type}/{anchor_slug}/history` — version history

### II.3 Constraint bug: `chk_ai_page_snapshot_attribution`

Migration 44 contains:
```sql
CONSTRAINT chk_ai_page_snapshot_attribution CHECK (
    attribution_block LIKE '%Image credit: NASA. NASA does not endorse this product.%'
)
```

This constraint fires on **every** snapshot insert, regardless of page type. A Walters illuminated manuscript page or an SMK Danish art page has no NASA attribution and will always fail this check. This is a Tier 1 schema defect.

**Fix (§IX migration spec):** Replace the global attribution constraint with a conditional check that only applies when `source_references` contains a NASA source type.

### II.4 State machine gap

`services/product/state_machine.py` models product activation state. No equivalent exists for page copy versions. NC-AI-005 defines `PageCopyStateMachine` following the same pattern.

---

## III. Page Copy State Machine

### III.1 States

```
generated ──► pending_review ──► approved ──► published
                    │                │
                    ▼                ▼
               rejected        changes_requested ──► pending_review (re-review)
                                     │
                                     ▼
                               [new generation]

published ──► archived (superseded by newer version)
published ──► rolled_back (active rollback triggered)
```

| State | Meaning |
|---|---|
| `generated` | Snapshot written; pre-review validation passed; no human has seen it |
| `pending_review` | In the reviewer queue; `publication_allowed = FALSE` |
| `approved` | Human reviewer approved; eligible for publication; `publication_allowed` may be set TRUE |
| `published` | Live on public surface; `publication_allowed = TRUE`; version is active |
| `archived` | Superseded by a newer `published` version; retained for audit and rollback |
| `rolled_back` | Was published; forcibly superseded; content is offline; retained for audit |
| `rejected` | Reviewer rejected; must not be published; retained for audit |
| `changes_requested` | Reviewer requested changes; sent back for re-generation |

### III.2 Allowed Transitions

| From | Action | To | Authority |
|---|---|---|---|
| `generated` | `queue` | `pending_review` | Automatic on successful generation |
| `pending_review` | `approve` | `approved` | Reviewer (single or two-human per §IV.2) |
| `pending_review` | `reject` | `rejected` | Reviewer |
| `pending_review` | `request_changes` | `changes_requested` | Reviewer |
| `approved` | `publish` | `published` | Reviewer (or PA for MASTERWORK) |
| `approved` | `reject` | `rejected` | PA override |
| `changes_requested` | `requeue` | `pending_review` | After new generation cycle |
| `published` | `supersede` | `archived` | Automatic when newer version is published |
| `published` | `rollback` | `rolled_back` | PA-initiated rollback trigger |
| `archived` | `restore` | `published` | Rollback to previous version |
| `rolled_back` | `restore` | `published` | PA re-publishes after correction |

### III.3 Terminal States (no further transitions)

`rejected` — terminal. A rejected snapshot may not be re-queued. A new generation is required.

`rolled_back` — non-terminal only via `restore`. A PA may re-publish a rolled-back version after root cause is resolved.

### III.4 Implementation: `PageCopyStateMachine`

File: `services/ai/page_copy_state_machine.py`

```python
TRANSITIONS = {
    "generated":          {"queue": "pending_review"},
    "pending_review":     {"approve": "approved",
                           "reject": "rejected",
                           "request_changes": "changes_requested"},
    "approved":           {"publish": "published",
                           "reject": "rejected"},
    "changes_requested":  {"requeue": "pending_review"},
    "published":          {"supersede": "archived",
                           "rollback": "rolled_back"},
    "archived":           {"restore": "published"},
    "rolled_back":        {"restore": "published"},
    "rejected":           {},
}
```

Mirrors `services/product/state_machine.py` exactly in structure. Single source of transitions; no ad-hoc state logic in endpoints.

---

## IV. Review Workflow

### IV.1 Reviewer Queue

**Endpoint:** `GET /ai/review-queue`

**Auth:** Reviewer role required (curator or PA per page family)

**Query parameters:**
| Parameter | Values | Default |
|---|---|---|
| `page_family` | homepage / story / product / educational / tourism | all |
| `quality_tier` | MASTERWORK / FLAGSHIP / STANDARD / REFERENCE | all |
| `anchor_slug` | e.g., `earthrise`, `yellowstone` | all |
| `status` | `pending_review` (default) / `changes_requested` | `pending_review` |
| `limit` | 1–50 | 20 |

**Response shape:**
```json
{
  "queue": [
    {
      "snapshot_id": "uuid",
      "page_generation_id": "uuid",
      "page_type": "product",
      "anchor_slug": "earthrise",
      "quality_tier": "MASTERWORK",
      "generation_purpose": "product_description_v1",
      "review_status": "pending_review",
      "requires_two_human_gate": true,
      "second_reviewer_required_role": "pa",
      "generated_at": "2026-06-12T10:00:00Z",
      "snapshot_version": "nc-ai-004-v1",
      "copy_preview": {
        "hero_text": "Earthrise",
        "story_text": "..."
      },
      "attribution_block": "NASA: Photograph by William Anders...\nImage credit: NASA. NASA does not endorse this product.",
      "source_references": [
        {"source_type": "nasa", "source_record_id": "AS08-14-2383", ...}
      ],
      "prohibited_phrase_check_passed": true,
      "pre_publication_checks": {
        "rights_verified": true,
        "attribution_present": true,
        "no_deferred_assets": true,
        "no_prohibited_phrases": true
      }
    }
  ],
  "total_pending": 1,
  "masterwork_pending": 1
}
```

**Database query:** `ai_page_generation_snapshot` JOIN `ai_page_generation` WHERE `review_status = 'pending_review'` ordered by `quality_tier DESC, created_at ASC` (MASTERWORK surfaced first).

---

### IV.2 Review Decision Endpoint

**Endpoint:** `POST /ai/page-generation/{snapshot_id}/review`

**Auth:** Curator or PA role

**Request body:**
```json
{
  "decision": "approved | rejected | changes_requested",
  "reviewer_id": "string (non-empty)",
  "reviewer_role": "curator | pa",
  "review_notes": "optional string",
  "pa_override": false
}
```

**State machine enforcement:**
```
allowed_transition = PageCopyStateMachine.transition(current_status, decision_map[decision])
```

Where `decision_map` is:
| `decision` value | State machine action |
|---|---|
| `"approved"` | `"approve"` |
| `"rejected"` | `"reject"` |
| `"changes_requested"` | `"request_changes"` |

**Two-human gate logic (MASTERWORK tier):**

For `page_type = 'product'` and `quality_tier = 'MASTERWORK'` (NC-PROD-001 Earthrise Giclée):

1. First reviewer submits `decision = "approved"` → snapshot moves to `approved_pending_pa`  
   (intermediate state: approved by curator, waiting for PA second signature)
2. PA reviewer submits `decision = "approved"` → snapshot moves to `approved`
3. If PA submits `decision = "rejected"` → snapshot moves to `rejected` regardless of curator approval
4. Same reviewer may not provide both signatures (`reviewer_id` uniqueness constraint per snapshot)

**Implementation note:** The two-human gate uses a `review_signatures` JSONB field on `ai_page_generation_snapshot` (§IX schema extension) rather than a separate table — each signature is appended to the array. The transition to `approved` is only permitted when `jsonb_array_length(review_signatures) >= required_signature_count`.

For MASTERWORK: `required_signature_count = 2`, distinct `reviewer_id` values required.
For all other tiers: `required_signature_count = 1`.

**Write path on approval:**
```sql
UPDATE ai_page_generation_snapshot
SET review_status = 'approved',
    review_signatures = review_signatures || $signature_jsonb::jsonb,
    updated_at = NOW()
WHERE id = $snapshot_id
  AND review_status = 'pending_review'
```

`publication_allowed` is NOT set to `TRUE` here — it is set only in the separate publish step (§V). This separation is intentional: approval authorizes publication but does not enact it.

**Response:**
```json
{
  "snapshot_id": "uuid",
  "previous_status": "pending_review",
  "new_status": "approved",
  "reviewer_id": "curator-001",
  "two_human_gate_complete": false,
  "second_signature_required": true,
  "audit_event_id": "uuid"
}
```

**Audit event written:** `event_type = 'page_copy_review_decision'` in `ai_audit_event`.

---

## V. Approval and Publication Workflow

### V.1 Publish Endpoint

**Endpoint:** `POST /ai/page-generation/{snapshot_id}/publish`

**Auth:** PA role (all page families) or Curator role (STANDARD/FLAGSHIP/REFERENCE tiers only)

**Preconditions (all must pass; 422 if any fail):**
1. `review_status = 'approved'` on the snapshot
2. `publication_allowed = FALSE` (not already published)
3. Two-human gate complete (if MASTERWORK)
4. `rights_status = 'verified_pd'` and `human_verified = TRUE` on all source records in `source_references` — live re-check at publish time, not cached from generation time
5. No prohibited phrases in `page_copy` (re-run validator at publish time)
6. SA-GEONAMES-001 and SA-OSM-001 ratification status confirmed for Phase 1+ pages
7. For NOAA-source pages: NOAA write cap not exceeded

**Transaction (atomic):**
```sql
BEGIN;

-- 1. Check and lock the snapshot
SELECT ... FOR UPDATE WHERE id = $snapshot_id;

-- 2. Promote previous 'published' snapshot to 'archived'
UPDATE ai_page_generation_snapshot
SET review_status = 'archived', updated_at = NOW()
WHERE id = (
    SELECT id FROM ai_page_generation_snapshot s
    JOIN ai_page_generation g ON g.id = s.page_generation_id
    WHERE g.page_type = $page_type
      AND g.anchor_slug = $anchor_slug
      AND s.review_status = 'published'
    ORDER BY s.created_at DESC
    LIMIT 1
)
RETURNING id AS archived_snapshot_id;

-- 3. Promote target snapshot to 'published'
UPDATE ai_page_generation_snapshot
SET review_status = 'published',
    publication_allowed = TRUE,
    published_at = NOW(),
    published_by = $actor,
    updated_at = NOW()
WHERE id = $snapshot_id
  AND review_status = 'approved';

-- 4. Write publication audit event
INSERT INTO ai_audit_event (...) VALUES (...);

COMMIT;
```

The transaction guarantees only one snapshot per (page_type, anchor_slug) is `published` at any time. This is the single-active-version invariant.

**Response:**
```json
{
  "snapshot_id": "uuid",
  "previous_status": "approved",
  "new_status": "published",
  "archived_snapshot_id": "uuid | null",
  "page_type": "product",
  "anchor_slug": "earthrise",
  "published_at": "2026-06-12T12:00:00Z",
  "published_by": "pa-001",
  "live_url": "/products/earthrise",
  "audit_event_id": "uuid"
}
```

### V.2 Live Copy Retrieval

**Endpoint:** `GET /ai/page-generation/{page_type}/{anchor_slug}` (existing, but fix required)

**Current state:** The existing endpoint queries `review_status = 'approved' AND publication_allowed = TRUE`. After NC-AI-005 is implemented, `review_status` for live copy is `'published'` (not `'approved'`). The query must be updated:

```sql
-- Before (NC-AI-004, incorrect state for live copy):
AND s.review_status = 'approved' AND s.publication_allowed = TRUE

-- After (NC-AI-005, correct):
AND s.review_status = 'published' AND s.publication_allowed = TRUE
```

**The web layer (`apps/web`) fetches this endpoint** at build time (SSG) or at request time (ISR/SSR) depending on phase:
- Phase 0: SSG — page is statically generated from approved copy at build time
- Phase 1+: ISR with 5-minute TTL — AI-generated copy is refreshed on approval; previous build is served until new build completes

---

## VI. Rollback Workflow

### VI.1 Rollback Triggers

A rollback is initiated when any of the following are confirmed:

| Trigger | Source | Urgency |
|---|---|---|
| Rights record correction (`rights_status` changed from `verified_pd`) | Automated monitor on `media_rights` | Immediate (15 min) |
| `human_verified` set to FALSE on source record | Automated monitor | Immediate |
| Prohibited phrase confirmed in published copy | PA review finding | Immediate |
| Federal endorsement phrase confirmed | Automated output scan + PA | Immediate + cascade |
| NARA attribution confirmed for Earthrise | Automated scan + PA | Immediate |
| Deferred asset appearing in published product context | Automated scan + PA | Immediate |
| Source record retracted by institution | PA manual action | Immediate |
| PA override (any reason) | PA manual action | Immediate |

### VI.2 Rollback Endpoint

**Endpoint:** `POST /ai/page-generation/{snapshot_id}/rollback`

**Auth:** PA role only

**Request body:**
```json
{
  "reason": "string (required, min 20 chars)",
  "trigger_type": "rights_correction | prohibited_phrase | endorsement_language | nara_attribution | deferred_asset | source_retraction | pa_override",
  "cascade": false,
  "actor": "pa-001"
}
```

**`cascade: true`** — only set when `trigger_type = "endorsement_language"`. Triggers cascade deactivation of all federal-source pages (see §VI.4).

**Transaction (atomic):**
```sql
BEGIN;

-- 1. Move current published snapshot to rolled_back
UPDATE ai_page_generation_snapshot
SET review_status = 'rolled_back',
    publication_allowed = FALSE,
    rolled_back_at = NOW(),
    rolled_back_by = $actor,
    rollback_reason = $reason,
    updated_at = NOW()
WHERE id = $snapshot_id
  AND review_status = 'published';

-- 2. Identify the most recent 'archived' snapshot (previous live version)
-- If found: restore it to 'published'
-- If not found: insert a static placeholder record

UPDATE ai_page_generation_snapshot
SET review_status = 'published',
    publication_allowed = TRUE,
    restored_at = NOW(),
    restored_by = $actor,
    updated_at = NOW()
WHERE id = (
    SELECT id FROM ai_page_generation_snapshot s
    JOIN ai_page_generation g ON g.id = s.page_generation_id
    WHERE g.page_type = $page_type
      AND g.anchor_slug = $anchor_slug
      AND s.review_status = 'archived'
    ORDER BY s.created_at DESC
    LIMIT 1
);

-- 3. Write rollback audit event
INSERT INTO ai_audit_event (event_type, ...) VALUES ('page_copy_rollback_executed', ...);

COMMIT;
```

**If no archived version exists:** The page enters a `placeholder` state — the web layer falls back to a static governed placeholder template ("This page is temporarily unavailable while we review content"). The placeholder is not AI-generated; it is a governed static component.

**Response:**
```json
{
  "rolled_back_snapshot_id": "uuid",
  "restored_snapshot_id": "uuid | null",
  "restored_from_archive": true,
  "page_type": "product",
  "anchor_slug": "earthrise",
  "rolled_back_at": "2026-06-12T14:00:00Z",
  "rolled_back_by": "pa-001",
  "reason": "...",
  "cascade_triggered": false,
  "audit_event_id": "uuid"
}
```

### VI.3 Automated Rights Monitor

The rights monitor is a background service that polls `media_rights` for changes and auto-initiates rollback.

**Implementation approach (Sprint 1: manual PA)**

For Sprint 1: no automated monitor. PA manually triggers rollback via the endpoint when a rights correction is detected.

**Phase 1+ (automated):** A PostgreSQL `NOTIFY`/`LISTEN` trigger on `media_rights` fires when `rights_status` changes from `verified_pd` or `human_verified` changes to `FALSE`. A FastAPI background task receives the `NOTIFY` and calls the rollback endpoint internally with `trigger_type = 'rights_correction'` and `actor = 'system-monitor'`.

```sql
CREATE OR REPLACE FUNCTION notify_rights_change()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF (OLD.rights_status IS DISTINCT FROM NEW.rights_status)
       OR (OLD.human_verified IS DISTINCT FROM NEW.human_verified)
    THEN
        PERFORM pg_notify(
            'rights_monitor',
            json_build_object(
                'source_record_id', NEW.source_record_id,
                'old_rights_status', OLD.rights_status,
                'new_rights_status', NEW.rights_status,
                'old_human_verified', OLD.human_verified,
                'new_human_verified', NEW.human_verified,
                'changed_at', NOW()
            )::text
        );
    END IF;
    RETURN NEW;
END;
$$;
```

### VI.4 Cascade Rollback (Endorsement Language Trigger)

When `trigger_type = "endorsement_language"` and `cascade = true`:

1. Find all `ai_page_generation_snapshot` records with `review_status = 'published'` where `source_references` contains a federal source type (`nasa`, `noaa`, `nara`)
2. Roll back each one using the standard rollback transaction
3. Write a single `cascade_rollback_event` audit record listing all affected snapshot IDs
4. Set `generation_pipeline_suspended = TRUE` in a system config table (blocks new `POST /ai/page-generation` for `product_copy` and `public_website_copy` task types)
5. Notify PA via `ai_audit_event` (and future: email/Slack notification)
6. PA reviews each page independently before re-publication
7. PA sets `generation_pipeline_suspended = FALSE` after review

This is the NC-PRODUCT-001 §IV cascade deactivation, implemented at the page copy layer.

---

## VII. Version History

### VII.1 Version History Endpoint

**Endpoint:** `GET /ai/page-generation/{page_type}/{anchor_slug}/history`

**Auth:** Curator or PA role

**Query parameters:**
| Parameter | Default |
|---|---|
| `limit` | 20 |
| `include_rejected` | false |
| `include_rolled_back` | true |

**Response:**
```json
{
  "page_type": "product",
  "anchor_slug": "earthrise",
  "active_snapshot_id": "uuid",
  "history": [
    {
      "snapshot_id": "uuid",
      "snapshot_version": "nc-ai-004-v1",
      "review_status": "published",
      "is_active": true,
      "generation_purpose": "product_description_v1",
      "generated_at": "2026-06-12T12:00:00Z",
      "approved_at": "2026-06-12T12:30:00Z",
      "published_at": "2026-06-12T12:45:00Z",
      "published_by": "pa-001",
      "page_copy_sha256": "abc123...",
      "source_record_ids": ["AS08-14-2383"],
      "review_signatures": [
        {"reviewer_id": "curator-001", "role": "curator", "signed_at": "..."},
        {"reviewer_id": "pa-001", "role": "pa", "signed_at": "..."}
      ]
    },
    {
      "snapshot_id": "uuid",
      "review_status": "archived",
      "is_active": false,
      "published_at": "2026-06-12T10:00:00Z",
      "archived_at": "2026-06-12T12:45:00Z",
      "archive_reason": "superseded_by_newer_version",
      "page_copy_sha256": "def456..."
    },
    {
      "snapshot_id": "uuid",
      "review_status": "rolled_back",
      "is_active": false,
      "rolled_back_at": "2026-06-12T09:00:00Z",
      "rolled_back_by": "pa-001",
      "rollback_reason": "prohibited phrase found post-publication",
      "trigger_type": "prohibited_phrase"
    }
  ],
  "total": 3
}
```

**Database query:**
```sql
SELECT s.id, s.snapshot_version, s.review_status, s.page_copy_sha256,
       s.created_at, s.published_at, s.published_by, s.rolled_back_at,
       s.rolled_back_by, s.rollback_reason, s.restored_at, s.review_signatures,
       s.generation_purpose,
       (s.review_status = 'published') AS is_active
  FROM ai_page_generation_snapshot s
  JOIN ai_page_generation g ON g.id = s.page_generation_id
 WHERE g.page_type = $page_type
   AND g.anchor_slug = $anchor_slug
   AND ($include_rejected OR s.review_status <> 'rejected')
 ORDER BY s.created_at DESC
 LIMIT $limit
```

### VII.2 Snapshot Diff Endpoint

**Endpoint:** `GET /ai/page-generation/{page_type}/{anchor_slug}/diff?from={snapshot_id_a}&to={snapshot_id_b}`

**Auth:** Curator or PA role

**Purpose:** Show text diff between two snapshots before deciding whether to publish a new version or restore an archived one.

**Response:** Side-by-side comparison of `page_copy` JSONB fields between two snapshots, highlighting changed zones (hero_text, story_text, product_text, attribution_block).

---

## VIII. Complete API Endpoint Registry

| Method | Path | Auth | Purpose | Exists? |
|---|---|---|---|---|
| `POST` | `/ai/page-generation` | Reviewer | Generate and queue snapshot | ✅ exists (migration 44) |
| `GET` | `/ai/review-queue` | Curator / PA | List snapshots pending review | ❌ missing |
| `POST` | `/ai/page-generation/{snapshot_id}/review` | Curator / PA | Submit review decision | ❌ missing |
| `POST` | `/ai/page-generation/{snapshot_id}/publish` | PA / Curator | Publish approved snapshot | ❌ missing |
| `GET` | `/ai/page-generation/{page_type}/{anchor_slug}` | Public | Get live copy | ✅ exists (fix query — §V.2) |
| `GET` | `/ai/page-generation/{page_type}/{anchor_slug}/history` | Curator / PA | Version history | ❌ missing |
| `GET` | `/ai/page-generation/{page_type}/{anchor_slug}/diff` | Curator / PA | Diff two snapshots | ❌ missing |
| `POST` | `/ai/page-generation/{snapshot_id}/rollback` | PA | Rollback live snapshot | ❌ missing |
| `POST` | `/ai/page-generation/{snapshot_id}/restore` | PA | Restore archived snapshot | ❌ missing |
| `GET` | `/ai/audit-events` | PA | List AI audit events | ✅ exists |

---

## IX. Schema Extensions (Migration 45)

Migration 45 must address the constraint bug (§II.3) and add the fields required by the publication workflow.

### IX.1 Fix `chk_ai_page_snapshot_attribution` (critical)

**Bug:** NASA nonendorsement is required in ALL snapshots. For non-NASA pages (Walters, SMK, NGA) this will always fail.

**Fix:**
```sql
-- Drop the broken constraint
ALTER TABLE ai_page_generation_snapshot
DROP CONSTRAINT IF EXISTS chk_ai_page_snapshot_attribution;

-- Replace with a conditional constraint
ALTER TABLE ai_page_generation_snapshot
ADD CONSTRAINT chk_ai_page_snapshot_attribution_conditional CHECK (
    -- Only enforce NASA nonendorsement when source_references contains a NASA source
    NOT (source_references::text ~* '"source_type":\s*"nasa"')
    OR attribution_block LIKE '%Image credit: NASA. NASA does not endorse this product.%'
);
```

### IX.2 New columns on `ai_page_generation_snapshot`

```sql
ALTER TABLE ai_page_generation_snapshot
ADD COLUMN IF NOT EXISTS page_family        TEXT,
ADD COLUMN IF NOT EXISTS quality_tier       TEXT CHECK (quality_tier IN ('MASTERWORK','FLAGSHIP','STANDARD','REFERENCE')),
ADD COLUMN IF NOT EXISTS published_at       TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS published_by       TEXT,
ADD COLUMN IF NOT EXISTS archived_at        TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS archive_reason     TEXT,
ADD COLUMN IF NOT EXISTS rolled_back_at     TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS rolled_back_by     TEXT,
ADD COLUMN IF NOT EXISTS rollback_reason    TEXT,
ADD COLUMN IF NOT EXISTS trigger_type       TEXT,
ADD COLUMN IF NOT EXISTS restored_at        TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS restored_by        TEXT,
ADD COLUMN IF NOT EXISTS review_signatures  JSONB NOT NULL DEFAULT '[]',
ADD COLUMN IF NOT EXISTS required_signatures INT NOT NULL DEFAULT 1,
ADD COLUMN IF NOT EXISTS generation_purpose TEXT;
```

### IX.3 New constraints on `ai_page_generation_snapshot`

```sql
-- Single active version per (page_type, anchor_slug)
CREATE UNIQUE INDEX IF NOT EXISTS uniq_ai_page_snapshot_one_published
    ON ai_page_generation_snapshot(page_generation_id)
    WHERE review_status = 'published';

-- publication_allowed can only be TRUE when published or restored
ALTER TABLE ai_page_generation_snapshot
ADD CONSTRAINT chk_ai_page_snapshot_publish_gate CHECK (
    publication_allowed = FALSE
    OR review_status IN ('published')
);

-- Two-human gate: MASTERWORK requires 2 signatures
ALTER TABLE ai_page_generation_snapshot
ADD CONSTRAINT chk_ai_page_snapshot_masterwork_gate CHECK (
    quality_tier <> 'MASTERWORK'
    OR (
        jsonb_array_length(review_signatures) >= required_signatures
        AND required_signatures >= 2
    )
    OR review_status NOT IN ('published')
);

-- Rollback fields populated together
ALTER TABLE ai_page_generation_snapshot
ADD CONSTRAINT chk_ai_page_snapshot_rollback_fields CHECK (
    (rolled_back_at IS NULL) = (rolled_back_by IS NULL)
);
```

### IX.4 New table: `ai_page_copy_audit_event`

This extends `ai_audit_event` with page-copy-specific event types, keeping the general AI audit log clean.

```sql
CREATE TABLE IF NOT EXISTS ai_page_copy_audit_event (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    snapshot_id             UUID NOT NULL REFERENCES ai_page_generation_snapshot(id),
    page_generation_id      UUID NOT NULL REFERENCES ai_page_generation(id),
    event_type              TEXT NOT NULL CHECK (event_type IN (
        'snapshot_generated',
        'snapshot_queued_for_review',
        'review_decision_submitted',
        'review_approved',
        'review_rejected',
        'review_changes_requested',
        'pa_second_signature',
        'snapshot_published',
        'snapshot_archived',
        'snapshot_rolled_back',
        'snapshot_restored',
        'cascade_rollback_triggered',
        'generation_pipeline_suspended',
        'generation_pipeline_resumed',
        'rights_monitor_triggered',
        'prohibited_phrase_detected'
    )),
    actor                   TEXT NOT NULL,
    actor_role              TEXT NOT NULL CHECK (actor_role IN ('curator','pa','system','system-monitor')),
    previous_status         TEXT,
    new_status              TEXT,
    event_detail            JSONB NOT NULL DEFAULT '{}',
    event_sha256            TEXT NOT NULL UNIQUE,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_ai_page_copy_audit_hash CHECK (event_sha256 ~ '^[0-9a-f]{64}$')
);

-- Append-only: no UPDATE, no DELETE
CREATE OR REPLACE RULE ai_page_copy_audit_no_update AS
    ON UPDATE TO ai_page_copy_audit_event DO INSTEAD NOTHING;
CREATE OR REPLACE RULE ai_page_copy_audit_no_delete AS
    ON DELETE TO ai_page_copy_audit_event DO INSTEAD NOTHING;

CREATE INDEX IF NOT EXISTS idx_ai_page_copy_audit_snapshot
    ON ai_page_copy_audit_event(snapshot_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_page_copy_audit_event_type
    ON ai_page_copy_audit_event(event_type, created_at DESC);
```

### IX.5 System config table (pipeline suspension)

```sql
CREATE TABLE IF NOT EXISTS ai_pipeline_config (
    key             TEXT PRIMARY KEY,
    value           TEXT NOT NULL,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by      TEXT NOT NULL
);

INSERT INTO ai_pipeline_config (key, value, updated_at, updated_by)
VALUES ('generation_pipeline_suspended', 'false', NOW(), 'migration-45')
ON CONFLICT (key) DO NOTHING;
```

---

## X. Service Layer: `services/ai/publication.py`

This module implements the publication workflow logic. It is called by the router endpoints and is not invoked directly by other services.

```python
"""NC-AI-005 publication workflow."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from services.ai.page_copy_state_machine import PageCopyStateMachine
from services.ai.page_generation import PROHIBITED_PHRASES, validate_prohibited_phrases
from services.ai.prompts import stable_hash


@dataclass(frozen=True)
class ReviewDecision:
    snapshot_id: str
    decision: str          # "approved" | "rejected" | "changes_requested"
    reviewer_id: str
    reviewer_role: str     # "curator" | "pa"
    review_notes: str = ""


@dataclass(frozen=True)
class PublishDecision:
    snapshot_id: str
    actor: str
    actor_role: str


@dataclass(frozen=True)
class RollbackDecision:
    snapshot_id: str
    actor: str
    reason: str
    trigger_type: str
    cascade: bool = False


def validate_review_decision(decision: ReviewDecision) -> None:
    action_map = {
        "approved": "approve",
        "rejected": "reject",
        "changes_requested": "request_changes",
    }
    if decision.decision not in action_map:
        raise ValueError(f"Unknown review decision: {decision.decision}")
    if not decision.reviewer_id:
        raise ValueError("reviewer_id is required")
    if decision.reviewer_role not in ("curator", "pa"):
        raise ValueError("reviewer_role must be 'curator' or 'pa'")


def validate_publish_preconditions(
    snapshot: dict[str, Any],
    source_rights_records: list[dict[str, Any]],
) -> None:
    if snapshot["review_status"] != "approved":
        raise ValueError("Snapshot must be approved before publication")
    if snapshot["publication_allowed"]:
        raise ValueError("Snapshot is already published")
    for right in source_rights_records:
        if right.get("rights_status") != "verified_pd":
            raise ValueError(
                f"Source {right['source_record_id']} has unverified rights at publish time"
            )
        if not right.get("human_verified"):
            raise ValueError(
                f"Source {right['source_record_id']} is not human_verified at publish time"
            )
    page_copy = snapshot.get("page_copy") or {}
    if isinstance(page_copy, str):
        import json
        page_copy = json.loads(page_copy)
    validate_prohibited_phrases(page_copy)


def build_review_signature(decision: ReviewDecision, signed_at: str) -> dict[str, Any]:
    sig = {
        "reviewer_id": decision.reviewer_id,
        "role": decision.reviewer_role,
        "decision": decision.decision,
        "notes": decision.review_notes,
        "signed_at": signed_at,
    }
    sig["signature_sha256"] = stable_hash(sig)
    return sig
```

---

## XI. Web Layer Integration

### XI.1 Page Copy Delivery

The Next.js web layer fetches AI-generated copy at build or revalidation time:

```typescript
// apps/web/lib/ai-page-copy.ts

import { phaseZeroProducts } from "@/lib/governed-content";

export type PageCopyResult = {
  hero_text: string;
  story_text: string;
  product_text: string;
  attribution_block: string;
  review_status: "published";
  publication_allowed: true;
} | null;

export async function getPublishedPageCopy(
  pageType: string,
  anchorSlug: string,
): Promise<PageCopyResult> {
  const apiBase = process.env.NC_API_BASE_URL;
  if (!apiBase) return null; // Fall back to static governed content

  const res = await fetch(
    `${apiBase}/ai/page-generation/${pageType}/${anchorSlug}`,
    { next: { revalidate: 300 } } // 5-minute ISR for Phase 1+
  );
  if (!res.ok) return null;
  return res.json();
}
```

**Fallback:** If `NC_API_BASE_URL` is unset or the endpoint returns non-200, the page uses static governed content from `governed-content.ts`. This is Phase 0 behavior. AI-generated copy augments but never gates the page.

### XI.2 Attribution Block Rendering

The `attribution_block` from the AI copy payload is **not rendered as raw HTML or as generated text in the story body**. It is passed to the `EarthriseAttributionBlock` (or equivalent per page type) template component, which renders it in the governed attribution zone separate from the generated copy body.

```tsx
// apps/web/components/PageCopyBlock.tsx
import { EarthriseAttributionBlock } from "@/components/AttributionBlock";

type PageCopyBlockProps = {
  pageCopy: PageCopyResult | null;
  fallbackContent: React.ReactNode;
};

export function PageCopyBlock({ pageCopy, fallbackContent }: PageCopyBlockProps) {
  if (!pageCopy) return <>{fallbackContent}</>;
  return (
    <>
      <p className="hero-text">{pageCopy.hero_text}</p>
      <p className="story-text">{pageCopy.story_text}</p>
      {/* Attribution is ALWAYS from governed constants, not from AI copy body */}
      <EarthriseAttributionBlock />
    </>
  );
}
```

The `attribution_block` field in the API response is used by the reviewer to confirm attribution is correct — it is not rendered directly on the page. The page always renders attribution from governed template components.

---

## XII. Conditions

**C-1 (Migration 45 — critical):** Fix `chk_ai_page_snapshot_attribution` constraint before any non-NASA page copy is generated. The current constraint blocks all non-NASA pages at the database level. This is a Tier 1 schema defect.

**C-2 (Review endpoints):** Implement the 5 missing endpoints (review queue, review decision, publish, rollback, history) before the review workflow is operational. Sprint 1 may mock these; they must be real before any human review is requested.

**C-3 (`PageCopyStateMachine`):** Implement `services/ai/page_copy_state_machine.py` following the product state machine pattern. All state transitions in review/publish/rollback endpoints must use this machine — no ad-hoc transition logic.

**C-4 (Publication service layer):** Implement `services/ai/publication.py` with `validate_publish_preconditions()` and `validate_review_decision()`. These must be called by the router, not inlined in endpoint handlers.

**C-5 (Rights re-check at publish time):** The publish endpoint must re-verify `rights_status = 'verified_pd'` and `human_verified = TRUE` on all source records at the moment of publication, not rely on cached generation-time values. This is separate from the pre-generation IFC-1 check.

**C-6 (Web layer fallback):** `getPublishedPageCopy()` in `apps/web/lib/ai-page-copy.ts` must have a clean fallback to static governed content when the API is unavailable. AI-generated copy is an enhancement; the governed static content is the ground truth.

**C-7 (Attribution block separation):** The `attribution_block` field from the AI copy payload must never be rendered as raw content on the page. Attribution is always rendered by governed template components (`EarthriseAttributionBlock`, etc.). This rule must be enforced in code review.

**C-8 (Audit log append-only):** `ai_page_copy_audit_event` must be append-only (no UPDATE, no DELETE). Migration 45 must include the Rules that enforce this.

---

## XIII. Decision

**APPROVE WITH CONDITIONS**

The NC-AI-005 Publication Architecture defines the complete lifecycle from generation through publication and rollback. The design is grounded in the existing PostgreSQL schema (migrations 43–44) and follows the established state machine pattern from the product activation pipeline.

**What is structural and correct in the existing implementation:**
- `ai_page_generation` and `ai_page_generation_snapshot` tables are correctly structured
- `publication_allowed = FALSE` hardcoded in generation INSERT — correct
- `chk_ai_page_snapshot_review` constraint (publication_allowed requires approved status) — correct
- `chk_ai_page_snapshot_no_nara_earthrise` CHECK constraint — correct (this enforcement belongs at the DB layer)

**What must be fixed before any human review is requested:**
- C-1: `chk_ai_page_snapshot_attribution` constraint bug (blocks all non-NASA pages)
- C-3: `PageCopyStateMachine` must exist before review endpoints are built

**What must be built before the review workflow is operational:**
- C-2: 5 missing endpoints
- C-4: Publication service layer
- C-5: Rights re-check at publish time
- C-8: Audit log append-only enforcement

**What must be in place before web layer uses AI copy:**
- C-6: Web layer fallback
- C-7: Attribution block rendering separation

**Priority:**

1. C-1 (constraint bug) — run migration 45 before any new page generation
2. C-3 (state machine) — before any endpoint is built
3. C-2 (endpoints) — review workflow unblocked
4. C-4 + C-5 (service layer + rights re-check) — alongside C-2
5. C-8 (audit log) — alongside migration 45
6. C-6 + C-7 (web layer) — before Phase 0 AI copy goes live

---

*NC-AI-005 v1.0 — drafted 2026-06-12. Pending ratification.*
*Reference models: NC-AI-004 · NC-AI-001 · Foundation Model Constitution v1.0*
*Grounded in: migrations 29–44, services/product/state_machine.py, services/ai/router.py*
*Conditions: 8 (C-1 through C-8). C-1 is a Tier 1 schema defect requiring immediate migration.*
