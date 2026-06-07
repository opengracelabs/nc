# Europeana Sprint 3 Remediation Specification

**Authority:** Sprint 3 Audit (V1–V6)
**Governing documents:** MSC v1.2, Europeana Rights Matrix v1.0, DD-EUR-001, M36 Engineering Specification v2
**Affected files:** `workers/europeana_adapter/store.py`, `workers/europeana_adapter/rights.py`
**Scope:** Compliance only. No redesign. No new features.

---

## V1 — Machine Verification

**Files:** `store.py` lines 129–130; `rights.py` lines 27, 58–80

### Required behavior

- `media_rights.verified_by` and `media_rights.verified_at` are `NULL` when the row is created by the worker.
- `media_rights.rights_status` is always `'pending_verification'` when written by the worker.
- Terminal statuses (`'verified_pd'`, `'verified_cc0'`) are set only by a human actor via a subsequent update.
- REVIEW REQUIRED rights (NoC-CR, NoC-OKLR, NKC) are classified as `REVIEW_REQUIRED`, not `BLOCKED`.
- REVIEW REQUIRED assets do not return `"status": "rejected"` from `write_record()`. They enter the pipeline with `rights_status = 'pending_verification'` and a `workflow_item` of `item_type = 'rights_review'`.
- `write_record()` rejects on `decision == BLOCKED` only.

### Prohibited behavior

- Worker may not write `verified_by = WORKER_ID`.
- Worker may not write any terminal `rights_status` (`verified_pd`, `verified_cc0`, `blocked`-as-terminal).
- NoC-OKLR must not appear in `_BLOCKED_TOKENS`.
- REVIEW REQUIRED return may not carry `rights_status: 'blocked'`.
- `write_record()` may not gate on `not rights["allowed"]` — that rejects REVIEW REQUIRED assets before pipeline entry.

### Minimum compliant fix

**`rights.py`** — three changes:

1. Remove `/NoC-OKLR/` from `_BLOCKED_TOKENS`.

2. Add REVIEW REQUIRED URI constants and a lookup set before `_BLOCKED_TOKENS`:

```python
NOC_CR_URI   = "https://rightsstatements.org/vocab/NoC-CR/1.0/"
NOC_OKLR_URI = "https://rightsstatements.org/vocab/NoC-OKLR/1.0/"
NKC_URI      = "https://rightsstatements.org/vocab/NKC/1.0/"

_REVIEW_REQUIRED_URIS = {NOC_CR_URI, NOC_OKLR_URI, NKC_URI}
```

3. In `classify_rights()`, insert the REVIEW REQUIRED check between the ALLOWED lookup and the blocked-token scan, and change all `REVIEW_REQUIRED` returns to use `rights_status: 'pending_verification'`:

```python
def classify_rights(value: str | None) -> dict[str, str | bool | None]:
    uri = normalize_rights_uri(value)
    if uri in _ALLOWED_RIGHTS:
        return {
            "decision": RightsDecision.ALLOWED.value,
            "allowed": True,
            "rights_statement_uri": uri,
            **_ALLOWED_RIGHTS[uri],
        }

    if uri is None:
        return {
            "decision": RightsDecision.REVIEW_REQUIRED.value,
            "allowed": False,
            "rights_statement_uri": None,
            "rights_status": "pending_verification",
            "rights_basis": "missing_rights",
        }

    if uri in _REVIEW_REQUIRED_URIS:
        return {
            "decision": RightsDecision.REVIEW_REQUIRED.value,
            "allowed": False,
            "rights_statement_uri": uri,
            "rights_status": "pending_verification",
            "rights_basis": "review_required_statement",
        }

    if any(token.lower() in uri.lower() for token in _BLOCKED_TOKENS):
        return {
            "decision": RightsDecision.BLOCKED.value,
            "allowed": False,
            "rights_statement_uri": uri,
            "rights_status": "blocked",
            "rights_basis": "blocked_rights_statement",
        }

    return {
        "decision": RightsDecision.REVIEW_REQUIRED.value,
        "allowed": False,
        "rights_statement_uri": uri,
        "rights_status": "pending_verification",
        "rights_basis": "unknown_rights_statement",
    }
```

**`store.py`** — two changes:

1. In `insert_media_rights()`, set `rights_status = 'pending_verification'` unconditionally and remove `verified_by`/`verified_at` from the INSERT. Store the worker's classification in evidence as `worker_classified_status` for the human reviewer:

```python
async def insert_media_rights(
    conn: Any,
    *,
    source_item_id: str,
    source_record_id: str,
    normalized: dict[str, Any],
) -> Any:
    rights = classify_rights(normalized.get("rights_uri"))
    evidence = {
        "source": SOURCE_SLUG,
        "schema_standard": SCHEMA_STANDARD,
        "source_record_id": source_record_id,
        "rights_basis": rights["rights_basis"],
        "rights_statement_uri": rights["rights_statement_uri"],
        "raw_payload_hash": normalized["raw_payload_hash"],
        "worker_classified_status": rights["rights_status"],
        "evidence_status": "pending_human_review",
    }
    row = await conn.fetchrow(
        """
        INSERT INTO media_rights (
            source_item_id, rights_status, rights_statement_uri, rights_evidence,
            commercial_reuse_permitted, modification_permitted,
            authored_by, provenance, created_at, updated_at
        ) VALUES (
            $1, 'pending_verification', $2, $3::jsonb, FALSE, FALSE,
            $4, $5::jsonb, NOW(), NOW()
        )
        RETURNING id
        """,
        source_item_id,
        rights["rights_statement_uri"],
        _json(evidence),
        WORKER_ID,
        _json(build_provenance(normalized)),
    )
    return row["id"]
```

Note: `commercial_reuse_permitted` and `modification_permitted` are `FALSE` until a human verifies.

2. In `write_record()`, change the rejection gate and add the REVIEW REQUIRED pipeline branch:

```python
rights = classify_rights(normalized.get("rights_uri"))
if rights["decision"] == RightsDecision.BLOCKED:
    return {
        "status": "rejected",
        "reason": rights["rights_basis"],
        "record_id": normalized.get("record_id"),
        "writes": 0,
    }
```

Add `from .rights import RightsDecision` to the import at the top of `store.py`. After the main transaction completes, add the REVIEW REQUIRED workflow branch:

```python
if rights["decision"] == RightsDecision.REVIEW_REQUIRED:
    await insert_workflow_item(
        conn,
        source_item_id=source_item_id,
        source_record_id=source_record_id,
        media_rights_id=media_rights_id,
        item_type="rights_review",
        rights_basis=rights["rights_basis"],
    )
```

---

## V2 — Premature activation_eligible

**File:** `store.py` lines 185–199

### Required behavior

M36 status flow: `proposed → acquired → rights_verified → activation_eligible → activated`

- `acquired` requires: `media_file` row present with binary stored in MinIO.
- `rights_verified` requires: human has set `media_rights.rights_status` to a terminal status.
- `activation_eligible` requires: both `acquired` and `rights_verified`.
- After `write_record()` completes, `source_item.status` remains `'proposed'` because neither condition is satisfied.

### Prohibited behavior

- Worker may not set `status = 'activation_eligible'` in any step of the write transaction.
- Worker may not set any status beyond `'proposed'` in a transaction that does not include binary MinIO storage and human rights verification.

### Minimum compliant fix

In `pin_current_substrate_records()`, remove the `status = 'activation_eligible'` line entirely:

```python
async def pin_current_substrate_records(
    conn: Any,
    *,
    source_item_id: str,
    source_record_id: str,
    media_rights_id: str,
    technical_metadata_id: str,
) -> None:
    await conn.execute(
        """
        UPDATE source_item
        SET current_source_record_id = $2,
            current_media_rights_id = $3,
            current_technical_metadata_id = $4,
            updated_at = NOW()
        WHERE id = $1
        """,
        source_item_id,
        source_record_id,
        media_rights_id,
        technical_metadata_id,
    )
```

The `upsert_source_item()` INSERT already sets `status = 'proposed'`. On conflict (update path), `status` is not touched. The item remains `'proposed'` until the binary retrieval step sets it to `'acquired'`.

---

## V3 — Automated Evidence

**File:** `store.py` lines 114–122

### Required behavior

- Evidence dict must not assert or imply machine clearance.
- Evidence must carry `evidence_status: 'pending_human_review'`.
- Evidence must include `worker_classified_status` so the human reviewer knows the worker's determination.
- Evidence must not include `automated_allowlist`.
- `commercial_reuse_permitted` and `modification_permitted` must be `FALSE` until human verification (see V1 fix — these are set correctly in the V1 minimum compliant fix).

### Prohibited behavior

- `automated_allowlist` key is prohibited in any evidence dict written to `media_rights.rights_evidence`.
- Evidence may not carry any key or value that a human reviewer could interpret as prior machine clearance.
- Evidence may not omit `evidence_status`.

### Minimum compliant fix

The V1 minimum compliant fix satisfies V3. The evidence dict in the corrected `insert_media_rights()` is:

```python
evidence = {
    "source": SOURCE_SLUG,
    "schema_standard": SCHEMA_STANDARD,
    "source_record_id": source_record_id,
    "rights_basis": rights["rights_basis"],
    "rights_statement_uri": rights["rights_statement_uri"],
    "raw_payload_hash": normalized["raw_payload_hash"],
    "worker_classified_status": rights["rights_status"],
    "evidence_status": "pending_human_review",
}
```

No additional changes beyond the V1 fix.

---

## V4 — Ungoverned anchor_type

**File:** `store.py` line 55

### Required behavior

`source_item.anchor_type` must be a value from the SKOS Anchor Type Scheme governed vocabulary: `biological`, `geographic`, `cultural`, `mixed`.

`'europeana_record'` is not a governed value. It is a provenance descriptor, not a content classification.

For Sprint 3 (Yellowstone pilot), content spans biological, geographic, and cultural subject matter. Classification has not been performed. `'mixed'` is the correct conservative default until a classification step is added to the pipeline.

### Prohibited behavior

- `'europeana_record'` may not be written to `anchor_type`.
- Any value outside the four governed terms (`biological`, `geographic`, `cultural`, `mixed`) is prohibited.

### Minimum compliant fix

In `upsert_source_item()`, change the anchor_type literal:

```python
# Before
'proposed', 'europeana_record', $6::jsonb, NOW(), NOW()

# After
'proposed', 'mixed', $6::jsonb, NOW(), NOW()
```

One character change. `'mixed'` is the honest default: the content has not been classified and may span multiple anchor categories.

---

## V5 — No Preservation Events

**File:** `store.py` — `write_record()` and all sub-functions

### Required behavior

Rights Matrix RM-6 and M36-011: Every rights determination must be recorded as an append-only `preservation_event` with `event_type = 'rights_verification'`.

Required columns (M36 Engineering Specification v2):

| Column | Value |
|--------|-------|
| `subject_type` | `'media_rights'` |
| `subject_id` | the new `media_rights_id` |
| `media_file_id` | `NULL` (binary not yet retrieved) |
| `media_derivative_id` | `NULL` |
| `event_type` | `'rights_verification'` |
| `event_datetime` | `NOW()` |
| `event_outcome` | `'pending_human_review'` |
| `event_detail` | JSON: `rights_basis`, `rights_statement_uri`, `decision`, `raw_payload_hash` |
| `agent_type` | `'worker'` |
| `agent_id` | `WORKER_ID` |

### Prohibited behavior

- A `media_rights` row may not be created without a corresponding `preservation_event` of `event_type = 'rights_verification'`.
- Preservation events are append-only. No UPDATE or DELETE on `preservation_event` rows.

### Minimum compliant fix

Add `insert_preservation_event()` to `store.py` and call it inside the write transaction immediately after `insert_media_rights()`:

```python
async def insert_preservation_event(
    conn: Any,
    *,
    subject_type: str,
    subject_id: str,
    event_type: str,
    event_outcome: str,
    event_detail: dict[str, Any],
    agent_id: str,
    media_file_id: str | None = None,
    media_derivative_id: str | None = None,
) -> Any:
    row = await conn.fetchrow(
        """
        INSERT INTO preservation_event (
            subject_type, subject_id, media_file_id, media_derivative_id,
            event_type, event_datetime, event_outcome, event_detail,
            agent_type, agent_id, created_at
        ) VALUES (
            $1, $2, $3, $4, $5, NOW(), $6, $7::jsonb, 'worker', $8, NOW()
        )
        RETURNING id
        """,
        subject_type,
        subject_id,
        media_file_id,
        media_derivative_id,
        event_type,
        event_outcome,
        _json(event_detail),
        agent_id,
    )
    return row["id"]
```

In `write_record()`, call it after `insert_media_rights()` inside the transaction:

```python
media_rights_id = await insert_media_rights(
    conn,
    source_item_id=source_item_id,
    source_record_id=source_record_id,
    normalized=normalized,
)
await insert_preservation_event(
    conn,
    subject_type="media_rights",
    subject_id=media_rights_id,
    event_type="rights_verification",
    event_outcome="pending_human_review",
    event_detail={
        "rights_basis": rights["rights_basis"],
        "rights_statement_uri": rights["rights_statement_uri"],
        "decision": rights["decision"],
        "raw_payload_hash": normalized["raw_payload_hash"],
        "worker_id": WORKER_ID,
    },
    agent_id=WORKER_ID,
)
```

Update the `"writes"` return value in `write_record()`: `5 → 7` (adds media_file and preservation_event rows — see V6).

---

## V6 — No media_file

**File:** `store.py` — `write_record()` and `pin_current_substrate_records()`

### Required behavior

DD-EUR-001 Article 4 mandates the EDM tripartite mapping:

- `ore:Aggregation → source_record`
- `edm:ProvidedCHO → source_item`
- `edm:WebResource → media_file`

A `media_file` row must be created for every record written. Sprint 3 ingests metadata; the binary is not retrieved during this transaction. The row is created with `preservation_status = 'pending_retrieval'`. MinIO fields (`minio_bucket`, `minio_key`, `checksum_sha256`) are `NULL` until binary retrieval completes.

Required columns (M36 Engineering Specification v2):

| Column | Sprint 3 value |
|--------|---------------|
| `source_item_id` | the `source_item_id` |
| `source_record_id` | the `source_record_id` |
| `media_type_id` | the `media_type_id` |
| `file_role` | `'primary'` |
| `sequence_position` | `1` |
| `source_url` | `normalized['representative_media_url']` |
| `original_filename` | `NULL` (not yet retrieved) |
| `minio_bucket` | `NULL` |
| `minio_key` | `NULL` |
| `mime_type` | `NULL` |
| `byte_size` | `NULL` |
| `checksum_sha256` | `NULL` |
| `preservation_status` | `'pending_retrieval'` |
| `ingestion_event_id` | `NULL` (set when binary is stored) |
| `provenance` | `build_provenance(normalized)` |

### Prohibited behavior

- `write_record()` may not complete successfully without creating at least one `media_file` row.
- `media_file.minio_key` and `media_file.checksum_sha256` may not be non-null unless the binary has been verified in MinIO.

### Minimum compliant fix

Add `insert_media_file()` to `store.py`:

```python
async def insert_media_file(
    conn: Any,
    *,
    source_item_id: str,
    source_record_id: str,
    media_type_id: str,
    normalized: dict[str, Any],
) -> Any:
    row = await conn.fetchrow(
        """
        INSERT INTO media_file (
            source_item_id, source_record_id, media_type_id,
            file_role, sequence_position, source_url,
            original_filename, minio_bucket, minio_key,
            mime_type, byte_size, checksum_sha256,
            preservation_status, ingestion_event_id,
            provenance, created_at, updated_at
        ) VALUES (
            $1, $2, $3,
            'primary', 1, $4,
            NULL, NULL, NULL,
            NULL, NULL, NULL,
            'pending_retrieval', NULL,
            $5::jsonb, NOW(), NOW()
        )
        RETURNING id
        """,
        source_item_id,
        source_record_id,
        media_type_id,
        normalized.get("representative_media_url"),
        _json(build_provenance(normalized)),
    )
    return row["id"]
```

In `write_record()`, call it inside the transaction after `insert_source_record()`:

```python
source_record_id = await insert_source_record(...)
media_file_id = await insert_media_file(
    conn,
    source_item_id=source_item_id,
    source_record_id=source_record_id,
    media_type_id=media_type_id,
    normalized=normalized,
)
```

Pass `media_file_id` to `insert_preservation_event()` for the `rights_verification` event (V5 fix). Update `write_record()` return to include `media_file_id` and change `"writes": 5` to `"writes": 7`:

```python
return {
    "status": "written",
    "record_id": normalized["record_id"],
    "source_item_id": source_item_id,
    "source_record_id": source_record_id,
    "media_file_id": media_file_id,
    "media_rights_id": media_rights_id,
    "technical_metadata_id": technical_metadata_id,
    "raw_payload_hash": normalized["raw_payload_hash"],
    "technical_content_hash": content["content_hash"],
    "writes": 7,
}
```

---

## Affected Files Summary

| File | Violations | Changes |
|------|-----------|---------|
| `rights.py` | V1 | Remove `/NoC-OKLR/` from `_BLOCKED_TOKENS`. Add `NOC_CR_URI`, `NOC_OKLR_URI`, `NKC_URI` constants. Add `_REVIEW_REQUIRED_URIS` set. Update `classify_rights()` for REVIEW REQUIRED branch and `pending_verification` status. |
| `store.py` | V1–V6 | `insert_media_rights()`: remove `verified_by`/`verified_at`, set `rights_status = 'pending_verification'`, fix evidence. `pin_current_substrate_records()`: remove `status = 'activation_eligible'`. `upsert_source_item()`: change `'europeana_record'` → `'mixed'`. Add `insert_media_file()`. Add `insert_preservation_event()`. Update `write_record()` gate to `decision == BLOCKED`, add REVIEW REQUIRED branch, call new functions, update return. |

---

## Invariants

These must hold after remediation. Verify with integration tests before marking Sprint 3 complete.

**I-1.** No `media_rights` row may have `rights_status` of `'verified_pd'` or `'verified_cc0'` with `verified_by = WORKER_ID`.

**I-2.** Every `media_rights` row created by `write_record()` must have a corresponding `preservation_event` row with `event_type = 'rights_verification'` in the same transaction.

**I-3.** No `source_item` row may have `status = 'activation_eligible'` immediately after `write_record()` completes.

**I-4.** Every `source_record` row created by `write_record()` must have a corresponding `media_file` row with `source_record_id` matching.

**I-5.** No `anchor_type` value outside `{'biological', 'geographic', 'cultural', 'mixed'}` may appear in `source_item`.

**I-6.** BLOCKED assets (decision = BLOCKED) produce zero writes. REVIEW REQUIRED and ALLOWED assets both enter the pipeline; REVIEW REQUIRED additionally receives a `workflow_item`.
