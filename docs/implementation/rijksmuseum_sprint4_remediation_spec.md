# Rijksmuseum Sprint 4 Remediation Specification

**Authority:** Sprint 3 Compliance Audit — V1, V2, V3
**Scope:** `workers/rijksmuseum_adapter/store.py`
**Governing documents:** DD-RIJKSMUSEUM-001 + A1 Articles 3(d), 4.2, 5.4; A1 Article 3(f)
**No redesign. Compliance only.**

---

## V1 — Absent `edm:rights` routes to REVIEW_REQUIRED instead of BLOCKED

**File:** `workers/rijksmuseum_adapter/store.py`
**Function:** `write_record()` — lines 337–344

### Required behavior

An OAI-PMH EDM record where `edm:rights` is absent (i.e. `normalize_oai_edm_record()` returns
`rights_uri = None`) must be rejected at pre-ingestion with zero database writes.
Rejection reason must be `"missing_rights_uri"`.

The rejection must occur before any call to `conn.fetchrow()` or `conn.execute()`.
It must occur before the BLOCKED URI token check and before `build_technical_metadata()`.

### Prohibited behavior

- Any DB write for a record where `normalized.get("rights_uri")` is `None` or falsy.
- Routing absent `edm:rights` to the REVIEW_REQUIRED workflow pipeline.
- Relying on `classify_rights(None)` → `REVIEW_REQUIRED` as the gate for absent rights.

### Minimum compliant fix

Add the following check as the **first guard** in `write_record()`, before
`classify_rights()` is inspected for BLOCKED:

```python
async def write_record(
    conn: Any,
    search_response: dict[str, Any],
    oai_xml: str,
    *,
    source_id: str,
    media_type_id: str,
    anchor_type: str = "cultural",      # added for V2 — see below
) -> dict[str, Any]:
    normalized = normalize_search_getrecord(search_response, oai_xml)
    rights = classify_rights(normalized.get("rights_uri"))

    if not normalized.get("rights_uri"):                      # V1 fix
        return {
            "status": "rejected",
            "reason": "missing_rights_uri",
            "record_id": normalized.get("record_id"),
            "writes": 0,
        }

    if rights["decision"] == RightsDecision.BLOCKED:
        ...
```

The existing BLOCKED check at line 338 is unchanged. The null guard fires first.

---

## V2 — `anchor_type` hardcoded `'mixed'`

**File:** `workers/rijksmuseum_adapter/store.py`
**Function:** `upsert_source_item()` — line 63; `write_record()` — signature

### Required behavior

`anchor_type` must be accepted as a parameter by both `upsert_source_item()` and
`write_record()`. The default value in both functions must be `"cultural"`.

For the pilot (OAI-PMH set 261222), the caller must pass `anchor_type="biological"`.
This is enforced at the call site (worker/main), not in `store.py` — `store.py`'s
responsibility is to accept and forward the value.

The SKOS governed vocabulary constraint (`biological | geographic | cultural | mixed`)
is enforced by the database CHECK constraint on `source_item.anchor_type`. No
application-level validation of vocabulary membership is required in `store.py`.

The `ON CONFLICT` UPDATE clause must **not** update `anchor_type`. Existing
`source_item` rows retain their `anchor_type` on re-ingestion.

### Prohibited behavior

- Hardcoding any `anchor_type` value (including `'mixed'` or `'cultural'`) in the SQL
  literal. The value must come from the function parameter.
- Updating `anchor_type` in the `ON CONFLICT DO UPDATE` clause.
- Defaulting to `'mixed'` at any level.

### Minimum compliant fix

**`upsert_source_item()` — reorder SQL parameters, replace literal with `$6`:**

```python
async def upsert_source_item(
    conn: Any,
    *,
    source_id: str,
    normalized: dict[str, Any],
    media_type_id: str,
    anchor_type: str = "cultural",
) -> Any:
    row = await conn.fetchrow(
        """
        INSERT INTO source_item (
            source_id, source_identifier, media_type_id, canonical_source_url,
            title, status, anchor_type, provenance, created_at, updated_at
        ) VALUES (
            $1, $2, $3, $4, $5, 'proposed', $6, $7::jsonb, NOW(), NOW()
        )
        ON CONFLICT (source_id, source_identifier)
        DO UPDATE SET
            media_type_id = EXCLUDED.media_type_id,
            canonical_source_url = EXCLUDED.canonical_source_url,
            title = EXCLUDED.title,
            updated_at = NOW()
        RETURNING id
        """,
        source_id,
        normalized["record_id"],
        media_type_id,
        normalized.get("source_url"),
        normalized.get("title"),
        anchor_type,
        _json(build_provenance(normalized)),
    )
    return row["id"]
```

Parameter mapping after fix: `$1`=source_id, `$2`=source_identifier, `$3`=media_type_id,
`$4`=source_url, `$5`=title, `$6`=anchor_type, `$7`=provenance.

**`write_record()` — add parameter, forward to `upsert_source_item()`:**

```python
async def write_record(
    conn: Any,
    search_response: dict[str, Any],
    oai_xml: str,
    *,
    source_id: str,
    media_type_id: str,
    anchor_type: str = "cultural",
) -> dict[str, Any]:
    ...
    source_item_id = await upsert_source_item(
        conn,
        source_id=source_id,
        normalized=normalized,
        media_type_id=media_type_id,
        anchor_type=anchor_type,
    )
```

No other changes to `write_record()` body.

---

## V3 — Evidence dict incomplete per A1 Article 3(f)

**File:** `workers/rijksmuseum_adapter/store.py`
**Function:** `insert_media_rights()` — lines 159–168

### Required behavior

The evidence dict written to `media_rights.rights_evidence` must include all nine
fields specified in A1 Article 3(f):

| Field | Value |
|---|---|
| `source` | `"rijksmuseum"` |
| `source_record_id` | `source_record_id` (UUID string) |
| `edm_rights_uri` | `rights["rights_statement_uri"]` |
| `rights_matrix_classification` | `rights["decision"].lower()` — `"allowed"`, `"review_required"`, or `"blocked"` |
| `applying_policy` | `"europeana_rights_matrix_v1.0"` (static string) |
| `oai_pmh_identifier` | `normalized.get("record_id")` — the `https://id.rijksmuseum.nl/{id}` URI |
| `raw_payload_hash` | `normalized["raw_payload_hash"]` |
| `worker_classified_status` | `rights["rights_status"]` — e.g. `"verified_pd"`, `"pending_verification"` |
| `evidence_status` | `"pending_human_review"` (static string) |

Existing fields not in the A1 spec (`schema_standard`, `rights_basis`,
`rights_statement_uri`) may be retained. They are not prohibited. The fix is additive.

### Prohibited behavior

- Omitting any of the nine required fields.
- Using the key name `"rights_statement_uri"` as the sole reference to the rights URI
  in place of `"edm_rights_uri"`. Both may coexist; `"edm_rights_uri"` must be present.
- Using a non-lowercase value for `rights_matrix_classification`.

### Minimum compliant fix

Add the four missing fields to the evidence dict without removing anything:

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
        "edm_rights_uri": rights["rights_statement_uri"],               # V3 — added
        "rights_matrix_classification": rights["decision"].lower(),     # V3 — added
        "applying_policy": "europeana_rights_matrix_v1.0",             # V3 — added
        "oai_pmh_identifier": normalized.get("record_id"),             # V3 — added
        "rights_basis": rights["rights_basis"],
        "rights_statement_uri": rights["rights_statement_uri"],
        "raw_payload_hash": normalized["raw_payload_hash"],
        "worker_classified_status": rights["rights_status"],
        "evidence_status": "pending_human_review",
    }
```

`insert_media_rights()` SQL is unchanged. Only the `evidence` dict changes.

---

## Required Unit Tests

**File:** `tests/unit/test_rijksmuseum_store.py`

Add the following tests. Do not modify existing tests.

### V1 — Absent `edm:rights` blocked before database writes

```python
async def test_write_record_rejects_absent_rights_before_database_writes() -> None:
    # Remove edm:rights element from fixture
    xml = _xml().replace(
        '<edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/" />',
        "",
    )
    conn = FakeConn()

    result = await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result == {
        "status": "rejected",
        "reason": "missing_rights_uri",
        "record_id": "https://id.rijksmuseum.nl/200343467",
        "writes": 0,
    }
    assert conn.events == []


async def test_write_record_absent_rights_is_rejected_before_blocked_token_check() -> None:
    """Null guard fires before BLOCKED token check — no BLOCKED classification needed."""
    xml = _xml().replace(
        '<edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/" />',
        "",
    )
    conn = FakeConn()

    result = await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result["reason"] == "missing_rights_uri"
    assert result["status"] == "rejected"
    # Confirm it is NOT being misrouted as REVIEW_REQUIRED
    assert result.get("workflow_item_id") is None
    assert conn.events == []
```

### V2 — `anchor_type` parameter wired through

```python
async def test_write_record_passes_anchor_type_biological_to_source_item() -> None:
    conn = FakeConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
        anchor_type="biological",
    )

    source_item_args = next(
        args
        for kind, table, args in conn.events
        if kind == "fetchrow" and table == "source_item"
    )
    # anchor_type is $6 — index 5 in zero-based args tuple
    assert source_item_args[5] == "biological"


async def test_write_record_defaults_anchor_type_to_cultural() -> None:
    conn = FakeConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    source_item_args = next(
        args
        for kind, table, args in conn.events
        if kind == "fetchrow" and table == "source_item"
    )
    assert source_item_args[5] == "cultural"


async def test_write_record_anchor_type_mixed_is_not_the_default() -> None:
    conn = FakeConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    source_item_args = next(
        args
        for kind, table, args in conn.events
        if kind == "fetchrow" and table == "source_item"
    )
    assert source_item_args[5] != "mixed"
```

### V3 — Evidence dict contains all A1 Article 3(f) required fields

```python
async def test_media_rights_evidence_contains_all_required_a1_fields() -> None:
    conn = FakeConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    media_rights_args = next(
        args
        for kind, table, args in conn.events
        if kind == "fetchrow" and table == "media_rights"
    )
    evidence = json.loads(media_rights_args[2])

    # All nine A1 Article 3(f) required fields must be present
    required_fields = {
        "source",
        "source_record_id",
        "edm_rights_uri",
        "rights_matrix_classification",
        "applying_policy",
        "oai_pmh_identifier",
        "raw_payload_hash",
        "worker_classified_status",
        "evidence_status",
    }
    assert required_fields.issubset(evidence.keys())


async def test_media_rights_evidence_edm_rights_uri_key_is_present() -> None:
    conn = FakeConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    media_rights_args = next(
        args
        for kind, table, args in conn.events
        if kind == "fetchrow" and table == "media_rights"
    )
    evidence = json.loads(media_rights_args[2])

    assert "edm_rights_uri" in evidence
    assert evidence["edm_rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"


async def test_media_rights_evidence_rights_matrix_classification_is_lowercase() -> None:
    conn = FakeConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    media_rights_args = next(
        args
        for kind, table, args in conn.events
        if kind == "fetchrow" and table == "media_rights"
    )
    evidence = json.loads(media_rights_args[2])

    assert evidence["rights_matrix_classification"] == "allowed"
    assert evidence["applying_policy"] == "europeana_rights_matrix_v1.0"
    assert evidence["oai_pmh_identifier"] == "https://id.rijksmuseum.nl/200343467"


async def test_media_rights_evidence_classification_is_review_required_for_noc_oklr() -> None:
    xml = _xml().replace(
        "http://creativecommons.org/publicdomain/mark/1.0/",
        "https://rightsstatements.org/vocab/NoC-OKLR/1.0/",
    )
    conn = FakeConn()

    await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    media_rights_args = next(
        args
        for kind, table, args in conn.events
        if kind == "fetchrow" and table == "media_rights"
    )
    evidence = json.loads(media_rights_args[2])

    assert evidence["rights_matrix_classification"] == "review_required"
    assert evidence["applying_policy"] == "europeana_rights_matrix_v1.0"
```

---

## Required Replay Tests

**File:** `tests/replay/test_rijksmuseum_adapter_sprint4.py` (new file)

```python
"""Sprint 4 remediation replay tests — V1, V2, V3."""
import json
from pathlib import Path

from workers.rijksmuseum_adapter.store import write_record

_FIXTURE = Path("tests/fixtures/rijksmuseum/yellowstone_getrecord_edm.xml")


class _Transaction:
    def __init__(self, conn: "ReplayConn") -> None:
        self.conn = conn

    async def __aenter__(self) -> None:
        self.conn.sql_order.append("BEGIN")

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.conn.sql_order.append("COMMIT")


class ReplayConn:
    def __init__(self) -> None:
        self.sql_order = []
        self._count = 0
        self.args_by_table: dict[str, tuple] = {}

    def transaction(self) -> _Transaction:
        return _Transaction(self)

    async def fetchrow(self, sql: str, *args):
        self._count += 1
        table = _table_name(sql)
        self.sql_order.append(table)
        self.args_by_table[table] = args
        return {"id": f"{table}-{self._count}"}

    async def execute(self, sql: str, *args):
        table = _table_name(sql)
        self.sql_order.append(table)
        self.args_by_table[f"execute:{table}"] = args
        return "UPDATE 1"


def _table_name(sql: str) -> str:
    compact = " ".join(sql.split()).lower()
    for table in (
        "workflow_items",
        "preservation_event",
        "media_technical_metadata",
        "media_rights",
        "media_file",
        "source_record",
        "source_item",
    ):
        if f"insert into {table}" in compact or f"update {table}" in compact:
            return table
    return "unknown"


def _search_response() -> dict:
    return {
        "orderedItems": [
            {"id": "https://id.rijksmuseum.nl/200343467", "title": "Yellowstone National Park"}
        ]
    }


def _xml() -> str:
    return _FIXTURE.read_text()


# V1 ──────────────────────────────────────────────────────────────────────────

async def test_sprint4_v1_absent_rights_blocked_without_source_record() -> None:
    """V1: absent edm:rights must be rejected before any DB write."""
    xml = _xml().replace(
        '<edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/" />',
        "",
    )
    conn = ReplayConn()

    result = await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    assert result["status"] == "rejected"
    assert result["reason"] == "missing_rights_uri"
    assert result["writes"] == 0
    assert conn.sql_order == []


async def test_sprint4_v1_absent_rights_rejection_is_deterministic() -> None:
    """Same payload with absent rights produces same rejection result on both runs."""
    xml = _xml().replace(
        '<edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/" />',
        "",
    )
    left = ReplayConn()
    right = ReplayConn()

    left_result = await write_record(
        left, _search_response(), xml,
        source_id="source-rijksmuseum", media_type_id="image",
    )
    right_result = await write_record(
        right, _search_response(), xml,
        source_id="source-rijksmuseum", media_type_id="image",
    )

    assert left_result == right_result
    assert left.sql_order == right.sql_order == []


# V2 ──────────────────────────────────────────────────────────────────────────

async def test_sprint4_v2_biological_anchor_type_written_for_set_261222() -> None:
    """V2: passing anchor_type=biological writes 'biological' to source_item."""
    conn = ReplayConn()

    result = await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
        anchor_type="biological",
    )

    assert result["status"] == "written"
    # anchor_type is the 6th positional arg ($6) to source_item INSERT
    source_item_args = conn.args_by_table["source_item"]
    assert source_item_args[5] == "biological"


async def test_sprint4_v2_cultural_default_anchor_type_is_stable_across_runs() -> None:
    """V2: default anchor_type 'cultural' is deterministic."""
    left = ReplayConn()
    right = ReplayConn()

    await write_record(
        left, _search_response(), _xml(),
        source_id="source-rijksmuseum", media_type_id="image",
    )
    await write_record(
        right, _search_response(), _xml(),
        source_id="source-rijksmuseum", media_type_id="image",
    )

    assert left.args_by_table["source_item"][5] == "cultural"
    assert right.args_by_table["source_item"][5] == "cultural"
    assert left.sql_order == right.sql_order


# V3 ──────────────────────────────────────────────────────────────────────────

async def test_sprint4_v3_evidence_contains_all_required_fields_for_pdm_record() -> None:
    """V3: complete evidence dict for an ALLOWED PDM record."""
    conn = ReplayConn()

    await write_record(
        conn,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["source"] == "rijksmuseum"
    assert evidence["edm_rights_uri"] == "https://creativecommons.org/publicdomain/mark/1.0/"
    assert evidence["rights_matrix_classification"] == "allowed"
    assert evidence["applying_policy"] == "europeana_rights_matrix_v1.0"
    assert evidence["oai_pmh_identifier"] == "https://id.rijksmuseum.nl/200343467"
    assert evidence["worker_classified_status"] == "verified_pd"
    assert evidence["evidence_status"] == "pending_human_review"
    assert len(evidence["raw_payload_hash"]) == 64  # SHA-256 hex


async def test_sprint4_v3_evidence_is_stable_across_runs() -> None:
    """V3: evidence hash is deterministic for the same payload."""
    left = ReplayConn()
    right = ReplayConn()

    await write_record(
        left, _search_response(), _xml(),
        source_id="source-rijksmuseum", media_type_id="image",
    )
    await write_record(
        right, _search_response(), _xml(),
        source_id="source-rijksmuseum", media_type_id="image",
    )

    left_evidence = json.loads(left.args_by_table["media_rights"][2])
    right_evidence = json.loads(right.args_by_table["media_rights"][2])

    assert left_evidence == right_evidence


async def test_sprint4_v3_evidence_review_required_classification_for_noc_cr() -> None:
    """V3: rights_matrix_classification is 'review_required' for NoC-CR."""
    xml = _xml().replace(
        "http://creativecommons.org/publicdomain/mark/1.0/",
        "https://rightsstatements.org/vocab/NoC-CR/1.0/",
    )
    conn = ReplayConn()

    await write_record(
        conn,
        _search_response(),
        xml,
        source_id="source-rijksmuseum",
        media_type_id="image",
    )

    evidence = json.loads(conn.args_by_table["media_rights"][2])
    assert evidence["rights_matrix_classification"] == "review_required"
    assert evidence["edm_rights_uri"] == "https://rightsstatements.org/vocab/NoC-CR/1.0/"
    assert evidence["applying_policy"] == "europeana_rights_matrix_v1.0"


# Cross-violation ──────────────────────────────────────────────────────────────

async def test_sprint4_full_write_path_with_all_three_fixes_applied() -> None:
    """All three fixes coexist: absent-rights blocked, biological anchor, complete evidence."""
    # First: confirm absent rights still blocked even when anchor_type and evidence fixes applied
    xml_no_rights = _xml().replace(
        '<edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/" />',
        "",
    )
    conn_blocked = ReplayConn()
    blocked_result = await write_record(
        conn_blocked,
        _search_response(),
        xml_no_rights,
        source_id="source-rijksmuseum",
        media_type_id="image",
        anchor_type="biological",
    )
    assert blocked_result["status"] == "rejected"
    assert blocked_result["reason"] == "missing_rights_uri"
    assert conn_blocked.sql_order == []

    # Second: confirm full write path with biological anchor and complete evidence
    conn_written = ReplayConn()
    written_result = await write_record(
        conn_written,
        _search_response(),
        _xml(),
        source_id="source-rijksmuseum",
        media_type_id="image",
        anchor_type="biological",
    )
    assert written_result["status"] == "written"
    assert conn_written.args_by_table["source_item"][5] == "biological"
    evidence = json.loads(conn_written.args_by_table["media_rights"][2])
    assert "edm_rights_uri" in evidence
    assert "rights_matrix_classification" in evidence
    assert "applying_policy" in evidence
    assert "oai_pmh_identifier" in evidence
```

---

## Post-Remediation Invariants

All six invariants must hold after Sprint 4 remediation is applied.

| # | Invariant | Verification |
|---|---|---|
| I-1 | `write_record()` with absent `rights_uri` returns `{"status": "rejected", "reason": "missing_rights_uri", "writes": 0}` with zero DB calls | `test_sprint4_v1_absent_rights_blocked_without_source_record` |
| I-2 | `write_record()` with absent `rights_uri` does not call any DB function | `assert conn.sql_order == []` |
| I-3 | `write_record()` default `anchor_type` is `"cultural"`, not `"mixed"` | `test_sprint4_v2_cultural_default_anchor_type_is_stable_across_runs` |
| I-4 | `write_record(anchor_type="biological")` writes `"biological"` at position `source_item_args[5]` | `test_sprint4_v2_biological_anchor_type_written_for_set_261222` |
| I-5 | `media_rights.rights_evidence` contains all nine A1 Article 3(f) fields | `test_sprint4_v3_evidence_contains_all_required_fields_for_pdm_record` |
| I-6 | `evidence["rights_matrix_classification"]` is lowercase `"allowed"` for PDM, `"review_required"` for NoC-CR/NoC-OKLR/NKC | `test_sprint4_v3_evidence_review_required_classification_for_noc_cr` |

---

## Existing Test Impact

No existing tests require modification.

| Existing test | Impact |
|---|---|
| `test_write_record_creates_m36_substrate_write_path` | V2 default is `"cultural"` — no `anchor_type` arg passed, default applies. Table order unchanged. **Passes.** |
| `test_write_record_rejects_blocked_rights_before_database_writes` | CC license still reaches BLOCKED token check (rights_uri is non-null). **Passes.** |
| `test_write_record_rejects_invalid_technical_metadata_before_database_writes` | Rights URI present, not absent. Reaches `validation_status()` check. **Passes.** |
| `test_media_rights_payload_records_pending_human_review_evidence` | Asserts `rights_basis`, `source`, `evidence_status`, `worker_classified_status` — all still present. V3 adds fields; does not remove. **Passes.** |
| `test_review_required_rights_enter_pipeline_with_workflow_item` | NoC-OKLR has rights_uri present. Not caught by V1 null guard. **Passes.** |
| `test_write_record_serializes_database_uuid_ids_in_json_evidence` | `source_record_id` still in evidence. **Passes.** |
| `test_rijksmuseum_sprint3_replay_is_deterministic_for_same_getrecord_payload` | No `anchor_type` arg — default `"cultural"`. Hash determinism unaffected. **Passes.** |
| `test_rijksmuseum_sprint3_replay_blocks_uncleared_rights_without_source_record` | CC license has non-null rights_uri. V1 null guard does not fire. BLOCKED token check fires as before. **Passes.** |

---

*Rijksmuseum Sprint 4 Remediation Specification — 2026-06-07*
*Authority: Sprint 3 Compliance Audit*
