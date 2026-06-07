# Europeana Production Readiness Closure Plan

**Authority:** Sprint 4 Compliance Verdict (V1–V6 resolved)
**Blockers in scope:** S-1, S-2, S-3, G-1, G-2
**Out of scope (human actions, no code path):** G-3, G-4, G-5

---

## Execution Overview

Three parallel tracks. Tracks A, B, and C may all start simultaneously.
Within Track C, G-2 must follow G-1.

```
Track A (Schema)  ──────── M36-002→003→004→005→006→007→008→009→011→012→016→017
Track B (Data)    ──────── S-3 Yellowstone INSERT (independent, no deps)
Track C (Gov)     ──────── G-1 DD-EUR-001 ratification → G-2 source registry SQL
                                          ↑
                                  G-2 blocked until G-1
```

All five blockers must be closed before the first ingestion run.
G-3, G-4, and G-5 (authorized reviewer, FM exclusion confirmation, NKC deadline)
must also be closed per DD-EUR-001 Article 9 — they are human actions not
addressed by this plan.

---

## Track A — Schema

### Why S-1 and S-2 require the full M36 substrate

`media_file` (S-1) and `preservation_event` (S-2) are not standalone tables.
`media_file` has FK columns to `source_item`, `source_record`, and
`media_type_registry`. `preservation_event` has a FK column to `media_file`.
None of those tables exist. The minimum action for S-1 and S-2 is the full
M36 media substrate DDL sequence.

### Minimum migration sequence

M36-010 (media_derivative), M36-013 (asset_delivery_manifest),
M36-014 (activation_target), M36-015 (activation_target_downstream_link),
and M36-018 (compatibility views) are deferred. They are not required for
the first production ingestion.

| Step | M36 sub-migration | Action | Closes |
|------|-------------------|--------|--------|
| 1 | M36-002 | Create `media_type_registry` | — |
| 2 | M36-003 | Seed 11 `media_type_registry` rows | — |
| 3 | M36-004 | Create `source_item` (nullable current FKs) | — |
| 4 | M36-005 | Create `source_record` | — |
| 5 | M36-006 | Create `media_rights` | — |
| 6 | M36-007 | Create `media_technical_metadata` | — |
| 7 | M36-008 | `ALTER TABLE source_item` — add current FK constraints | — |
| 8 | M36-009 | Create `media_file` | **S-1** |
| 9 | M36-011 | Create `preservation_event` (M36-010 skipped) | **S-2** |
| 10 | M36-012 | `ALTER TABLE media_file` — add `ingestion_event_id` FK | — |
| 11 | M36-016 | Install trigger suite | — |
| 12 | M36-017 | Install index suite | — |

### Minimum action

The migration file is already written:

```
infrastructure/postgres/init/36_m36_media_substrate.sql
```

Apply it in a single transaction against the target database.

**Pre-application check** — confirm none of the tables exist yet:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'media_type_registry', 'source_item', 'source_record',
    'media_rights', 'media_technical_metadata',
    'media_file', 'preservation_event'
  );
-- Expected: 0 rows
```

**Apply:**

```
psql -d <database> -f infrastructure/postgres/init/36_m36_media_substrate.sql
```

**Post-application verification:**

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'media_type_registry', 'source_item', 'source_record',
    'media_rights', 'media_technical_metadata',
    'media_file', 'preservation_event'
  )
ORDER BY table_name;
-- Expected: 7 rows

SELECT media_type_id, status FROM media_type_registry ORDER BY expansion_phase, media_type_id;
-- Expected: image/map/photography/poster → active; others → pending

SELECT COUNT(*) FROM media_type_registry;
-- Expected: 11
```

S-1 closed when `\d media_file` succeeds.
S-2 closed when `\d preservation_event` succeeds.

---

## Track B — Data (S-3)

### Dependency

None. The `places` table exists (01_tables.sql). This INSERT may be executed
before or after Track A. It does not depend on the M36 substrate.

### Minimum action

```sql
INSERT INTO places (
    wikidata_qid,
    geonames_id,
    name,
    description,
    heritage_type,
    country_codes,
    continent,
    status,
    provenance,
    created_at,
    updated_at
) VALUES (
    'Q351',
    '5843591',
    '{"en": "Yellowstone National Park"}'::jsonb,
    '{"en": "First United States national park, established 1872. Located primarily in Wyoming."}'::jsonb,
    'natural',
    ARRAY['US'],
    'North America',
    'active',
    '{"nc:source": "manual", "nc:authority": "DD-EUR-001 Article 6(c)", "nc:applied_by": "<name>", "nc:applied_at": "<timestamp>"}'::jsonb,
    NOW(),
    NOW()
)
ON CONFLICT (wikidata_qid) DO NOTHING;
```

Record applier name and timestamp in the `provenance` field before executing.

**Verification:**

```sql
SELECT id, wikidata_qid, geonames_id, name->>'en' AS name, status
FROM places
WHERE geonames_id = '5843591';
-- Expected: 1 row, name = 'Yellowstone National Park', status = 'active'
```

S-3 closed when this query returns one row.

---

## Track C — Governance

### G-1 — DD-EUR-001 Ratification

**Dependency:** None. Can start immediately.

**Minimum action:**

Two humans must sign. Both signatures must be recorded in the decision document
before G-2 may proceed.

**Step 1 — Director review and signature:**

Document: `docs/decisions/DD-EUR-001_ratification_package.md`

1. Complete Section 1 pre-ratification checklist (all items checked).
2. Read Section 2 Director Approval Statement in full.
3. Record ratification date and Director signature in Section 2.

**Step 2 — Second human review and approval:**

1. Read DD-EUR-001 independently.
2. Read Section 3 Second-Human Approval Statement.
3. Record approval date, name, and role in Section 3.

**Step 3 — Update DD-EUR-001 header:**

In `docs/decisions/DD-EUR-001_europeana_production_activation.md`:

- Line 11: Change `**Ratified** | —` to `**Ratified** | <date>`
- Line 13: Change `**Second-Human Approval** | —` to `**Second-Human Approval** | <name>`
- Final table: Record both signatures and dates.

**Verification:**

Both signature lines in the ratification table are non-empty.
Status field reads `Ratified` (not `Draft — Pending Ratification`).

G-1 closed when both signatures are recorded.

---

### G-2 — Source Registry Amendments EU-SR-1 through EU-SR-7

**Dependency:** G-1 must be closed first. The SQL is authorized by DD-EUR-001;
executing it before ratification is unauthorized.

**Minimum action:**

Run the pre-amendment verification query first:

```sql
SELECT
    source_id,
    entity_types,
    standards,
    config,
    governance_state,
    operational_status
FROM sources
WHERE source_id = 'europeana';
```

Confirm the output matches the expected pre-amendment state documented in
DD-EUR-001 Ratification Package Section 4. If it does not match, investigate
before proceeding.

Execute the amendment (from DD-EUR-001 Ratification Package Section 4):

```sql
BEGIN;

UPDATE sources
SET
    standards    = ARRAY['cidoc_crm', 'skos', 'prov_o', 'premis', 'edm'],
    entity_types = ARRAY['cultural_object', 'image', 'photography', 'map', 'illustration'],
    config       = '{
        "api_endpoint":      "https://api.europeana.eu/record/v2",
        "auth_key_env":      "EUROPEANA_API_KEY",
        "rate_limit":        {"requests_per_second": 2, "burst": 10},
        "rights_strategy":   "rights_matrix_filtered",
        "source_role":       "aggregator",
        "completeness_minimum": 4,
        "edm_tripartite":    true,
        "rights_filter": {
            "mode":      "pre_ingestion",
            "authority": "europeana_rights_matrix_v1",
            "allowed_uris": [
                "http://creativecommons.org/publicdomain/zero/1.0/",
                "http://creativecommons.org/publicdomain/mark/1.0/",
                "http://rightsstatements.org/vocab/NoC-US/1.0/"
            ],
            "review_required_uris": [
                "http://rightsstatements.org/vocab/NoC-CR/1.0/",
                "http://rightsstatements.org/vocab/NoC-OKLR/1.0/",
                "http://rightsstatements.org/vocab/NKC/1.0/"
            ],
            "filter_mode": "strict"
        }
    }'::jsonb,
    updated_at   = NOW()
WHERE source_id = 'europeana';

COMMIT;
```

Run the post-amendment verification query (from Ratification Package Section 4).
All seven rows must return `applied = true`:

```sql
SELECT 'EU-SR-1' AS amendment, config->>'rights_strategy' = 'rights_matrix_filtered' AS applied FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-2', config->>'source_role' = 'aggregator' FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-3', (config->>'completeness_minimum')::int = 4 FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-4', config->'rights_filter' IS NOT NULL FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-5', 'edm' = ANY(standards) FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-6', 'photography' = ANY(entity_types) FROM sources WHERE source_id = 'europeana'
UNION ALL
SELECT 'EU-SR-7', (config->>'edm_tripartite')::boolean = true FROM sources WHERE source_id = 'europeana';
```

Record applier name and timestamp in DD-EUR-001 Ratification Package Section 4.

G-2 closed when all seven verification rows return `applied = true`.

---

## Completion Gate

All five blockers are closed when:

| Blocker | Verification query / action | Expected |
|---------|----------------------------|---------|
| S-1 | `\d media_file` | Table exists |
| S-2 | `\d preservation_event` | Table exists |
| S-3 | `SELECT id FROM places WHERE geonames_id = '5843591'` | 1 row |
| G-1 | Both signature lines non-empty in DD-EUR-001 | Signed |
| G-2 | 7-row EU-SR verification query | All `applied = true` |

When all five are closed and G-3 (authorized reviewer), G-4 (FM exclusion
confirmation), and G-5 (NKC deadline) are also confirmed, the Article 9 gate
is satisfied and the first production ingestion run may begin.
