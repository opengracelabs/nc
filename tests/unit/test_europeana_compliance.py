import json
from pathlib import Path

from workers.europeana_adapter.store import write_record

_FIXTURE = Path("tests/fixtures/europeana/yellowstone_launch_metadata_v1_record.json")


class _Transaction:
    def __init__(self, conn: "ComplianceConn") -> None:
        self.conn = conn

    async def __aenter__(self) -> None:
        self.conn.events.append(("transaction_enter", None, "", ()))

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.conn.events.append(("transaction_exit", None, "", ()))


class ComplianceConn:
    def __init__(self) -> None:
        self.events = []
        self._count = 0

    def transaction(self) -> _Transaction:
        return _Transaction(self)

    async def fetchrow(self, sql: str, *args):
        self._count += 1
        table = _table_name(sql)
        self.events.append(("fetchrow", table, sql, args))
        return {"id": f"{table}-{self._count}"}

    async def execute(self, sql: str, *args):
        self.events.append(("execute", _table_name(sql), sql, args))
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


def _yellowstone_payload() -> dict:
    return json.loads(_FIXTURE.read_text())


def _event(conn: ComplianceConn, table: str, kind: str = "fetchrow"):
    return next(event for event in conn.events if event[0] == kind and event[1] == table)


async def test_v1_v3_media_rights_are_pending_human_verification() -> None:
    conn = ComplianceConn()

    await write_record(
        conn,
        _yellowstone_payload(),
        source_id="source-europeana",
        media_type_id="map",
    )

    _, _, sql, args = _event(conn, "media_rights")
    evidence = json.loads(args[2])
    compact_sql = " ".join(sql.split()).lower()
    assert "'pending_verification'" in compact_sql
    assert "verified_by" not in compact_sql
    assert "verified_at" not in compact_sql
    assert "true" not in compact_sql
    assert evidence["evidence_status"] == "pending_human_review"
    assert evidence["worker_classified_status"] == "verified_pd"
    assert "automated_allowlist" not in evidence


async def test_v2_v4_source_item_stays_proposed_with_governed_anchor_type() -> None:
    conn = ComplianceConn()

    await write_record(
        conn,
        _yellowstone_payload(),
        source_id="source-europeana",
        media_type_id="map",
    )

    _, _, insert_sql, _ = _event(conn, "source_item", kind="fetchrow")
    _, _, update_sql, _ = _event(conn, "source_item", kind="execute")
    assert "'mixed'" in insert_sql
    assert "europeana_record" not in insert_sql
    assert "activation_eligible" not in update_sql


async def test_v5_preservation_event_tracks_rights_verification() -> None:
    conn = ComplianceConn()

    await write_record(
        conn,
        _yellowstone_payload(),
        source_id="source-europeana",
        media_type_id="map",
    )

    _, _, _, args = _event(conn, "preservation_event")
    event_detail = json.loads(args[6])
    assert args[0] == "media_rights"
    assert args[1] == "media_rights-4"
    assert args[2] == "media_file-3"
    assert args[4] == "rights_verification"
    assert args[5] == "pending_human_review"
    assert args[7] == "europeana_adapter:sprint3"
    assert event_detail["decision"] == "ALLOWED"
    assert event_detail["rights_basis"] == "public_domain_mark"


async def test_v6_media_file_is_pending_retrieval_without_minio_or_checksum() -> None:
    conn = ComplianceConn()

    await write_record(
        conn,
        _yellowstone_payload(),
        source_id="source-europeana",
        media_type_id="map",
    )

    _, _, sql, args = _event(conn, "media_file")
    compact_sql = " ".join(sql.split()).lower()
    assert "'primary'" in compact_sql
    assert "'pending_retrieval'" in compact_sql
    assert "null, null, null" in compact_sql
    assert args[0] == "source_item-1"
    assert args[1] == "source_record-2"
    assert args[2] == "map"
    assert args[3] == "https://api.europeana.eu/thumbnail/v3/400/9200518/ark__12148_btv1b530248434"


async def test_v1_review_required_record_opens_rights_review_workflow() -> None:
    payload = _yellowstone_payload()
    payload["object"]["rights"] = ["https://rightsstatements.org/vocab/NKC/1.0/"]
    conn = ComplianceConn()

    result = await write_record(conn, payload, source_id="source-europeana", media_type_id="map")

    _, _, _, args = _event(conn, "workflow_items")
    context = json.loads(args[3])
    assert result["status"] == "written"
    assert result["workflow_item_id"] == "workflow_items-7"
    assert args[0] == "source_item-1"
    assert args[1] == "review_required_statement"
    assert args[2] == "europeana_adapter:sprint3"
    assert context["item_type"] == "rights_review"
    assert context["item_payload"]["matrix_classification"] == "review_required"
    assert context["item_payload"]["edm_rights_uri"] == "https://rightsstatements.org/vocab/NKC/1.0/"
