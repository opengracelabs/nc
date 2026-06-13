# NC-GRAPH-003A: Neo4j Implementation Code Review

| Field | Value |
|---|---|
| Document | NC-GRAPH-003A |
| Version | 1.0 |
| Status | **DRAFT** |
| Date | 2026-06-13 |
| Scope | Implemented Neo4j code only |
| Files reviewed | `services/api/graph_runtime.py` · `graph/loaders/load_seed.py` · `graph/seed.py` · `graph/schema/constraints.cypher` · `graph/sync/sync_seed.py` |

---

## Implementation State

The graph layer is seed-based. There are no PostgreSQL triggers, no change queue, and no
projection workers. All three NC-GRAPH-003 findings (RI-1, RI-2, GV-1) were written against
the NC-GRAPH-002 blueprint. This review maps each to the actual code and provides exact fixes
for what is implemented.

---

## RI-1: Commerce signal served from graph without PostgreSQL recheck

**NC-GRAPH-003 finding:** Dual `rights` fields on node + SOURCED_FROM relationship diverge
during sync window.

**In the implemented code:** No `rights` field and no `SOURCED_FROM` relationship exist yet.
The equivalent active issue is `status` on `Product` nodes being returned directly from the
graph to API consumers.

### Finding 1a — `_serialize_node` returns `status` for all labels including Product

**File:** `services/api/graph_runtime.py`, lines 27–36

```python
def _serialize_node(record: Any) -> dict:
    node = record if isinstance(record, dict) else dict(record)
    return {
        "id": node.get("id"),
        "slug": node.get("slug"),
        "label": node.get("label") or next(iter(getattr(record, "labels", [])), None),
        "name": node.get("name"),
        "summary": node.get("summary"),
        "status": node.get("status"),   # ← problem: returns "live" for Product nodes
    }
```

`status: "live"` on a Product node is a commerce gate. Two seed Products have this value:
`product:earthrise-print` and `product:earthrise-digital`. Both appear in recommendation
results from `get_graph_recommendations`. Any caller reading `status` from this response
and using it to gate a "Buy" button or cart action is bypassing PostgreSQL authority.

**Exact fix:**

```python
# Labels whose status field has commerce meaning and must not be served from graph
_COMMERCE_LABELS = {"Product"}


def _serialize_node(record: Any) -> dict:
    node = record if isinstance(record, dict) else dict(record)
    label = node.get("label") or next(iter(getattr(record, "labels", [])), None)
    result: dict = {
        "id": node.get("id"),
        "slug": node.get("slug"),
        "label": label,
        "name": node.get("name"),
        "summary": node.get("summary"),
    }
    # status is a display hint for Place/Collection ("coming_soon") but a commerce
    # gate for Product. Strip it for commerce labels — callers must fetch from PostgreSQL.
    if label not in _COMMERCE_LABELS:
        result["status"] = node.get("status")
    return result
```

### Finding 1b — Recommendations query returns Product nodes with no rights guard

**File:** `services/api/graph_runtime.py`, lines 139–156

```python
result = session.run(
    """
    MATCH (subject {slug: $slug})
    OPTIONAL MATCH (subject)-[r:RECOMMENDS]->(target)
    RETURN subject, collect({
      node: target,
      relationship: {
        source: subject.id,
        target: target.id,
        type: type(r),
        reason: r.reason,
        weight: r.weight
      }
    }) AS recommendations
    """,
    slug=slug,
)
```

This query returns any node that is a `RECOMMENDS` target — including Product nodes — with no
label restriction and no rights or status filter on the target. The seed has:

```python
{"source": "collection:earthrise", "target": "product:earthrise-print",
 "type": "RECOMMENDS", "reason": "The museum print is the primary live edition.", "weight": 0.92}
```

A Product node with `status: "live"` (or any status) can appear in results regardless of
whether it is active in PostgreSQL.

**Exact fix:** Restrict RECOMMENDS targets to non-commerce labels in the query, or add an
explicit exclusion for Product nodes and document that product availability is determined by
PostgreSQL:

```python
result = session.run(
    """
    MATCH (subject {slug: $slug})
    OPTIONAL MATCH (subject)-[r:RECOMMENDS]->(target)
    WHERE NOT 'Product' IN labels(target)
       OR target.status IS NOT NULL  -- Product targets returned for discovery only;
                                     -- callers must recheck status from PostgreSQL
    RETURN subject, collect({
      node: target,
      relationship: {
        source: subject.id,
        target: target.id,
        type: type(r),
        reason: r.reason,
        weight: r.weight
      }
    }) AS recommendations
    """,
    slug=slug,
)
```

The simpler and cleaner fix: exclude Product nodes from RECOMMENDS results entirely. If the
frontend needs to show a "buy this" panel, it fetches product availability from PostgreSQL
after the graph returns a collection or asset slug:

```python
result = session.run(
    """
    MATCH (subject {slug: $slug})
    OPTIONAL MATCH (subject)-[r:RECOMMENDS]->(target)
    WHERE NOT 'Product' IN labels(target)
    RETURN subject, collect({
      node: target,
      relationship: {
        source: subject.id,
        target: target.id,
        type: type(r),
        reason: r.reason,
        weight: r.weight
      }
    }) AS recommendations
    """,
    slug=slug,
)
```

This removes Products from graph-driven recommendations. Products are surfaced by the PostgreSQL
commerce layer, not the discovery graph.

---

## RI-2: Unsafe parameter expansion in loader

**NC-GRAPH-003 finding:** `shopify_variant_id` on Product node creates G-5 violation pathway.

**In the implemented code:** No `shopify_variant_id` in any node — that finding is preventive.
The active issue is `**node` and `**rel` expanding all dict fields as Neo4j driver parameters,
and f-string interpolation of label/rel_type into Cypher.

### Finding 2a — `_merge_node` uses f-string for label and `**node` parameter expansion

**File:** `graph/loaders/load_seed.py`, lines 48–63

```python
def _merge_node(tx, node: dict) -> None:
    label = node["label"]
    if label not in LABELS:
        raise ValueError(f"Unsupported graph label: {label}")
    tx.run(
        f"""
        MERGE (n:{label} {{id: $id}})
        SET n.label = $label,
            n.slug = $slug,
            n.name = $name,
            n.summary = $summary,
            n.status = $status,
            n.graph_version = 'NC-GRAPH-003'
        """,
        **node,               # ← expands ALL node fields as driver parameters
    )
```

Two problems:

1. **f-string interpolation**: `f"MERGE (n:{label} ..."` builds Cypher at runtime from
   `label`. The LABELS check before it is the only guard. If that check is ever refactored
   away, this is a Cypher injection point. Labels in Cypher cannot be parameterized natively,
   but the safe pattern is to pre-build queries from a trusted constant set at import time —
   never at call time from a runtime value.

2. **`**node` expansion**: passes every field in `node` to the driver as named parameters.
   The driver silently ignores unbound parameters. If `GraphNode` gains a field (e.g., a
   future `rights`, `shopify_variant_id`, or `price_usd`), it is silently passed to the
   driver in every node write call. This is not currently exploitable but creates a pattern
   where adding a field to `GraphNode` automatically passes it into graph write operations.

**Exact fix — pre-build queries from constants, explicit parameters:**

```python
# Build queries at import time from the trusted LABELS constant.
# f-strings run once here against a known-safe set — not at query time.
_NODE_MERGE: dict[str, str] = {
    lbl: (
        f"MERGE (n:{lbl} {{id: $id}})"
        " SET n.label = $label,"
        "     n.slug = $slug,"
        "     n.name = $name,"
        "     n.summary = $summary,"
        "     n.status = $status,"
        "     n.graph_version = $graph_version"
    )
    for lbl in LABELS
}


def _merge_node(tx, node: dict) -> None:
    label = node["label"]
    if label not in _NODE_MERGE:          # guard is now on the query map
        raise ValueError(f"Unsupported graph label: {label}")
    tx.run(
        _NODE_MERGE[label],
        id=node["id"],                    # explicit parameters — no **node
        label=node["label"],
        slug=node["slug"],
        name=node["name"],
        summary=node["summary"],
        status=node["status"],
        graph_version="NC-GRAPH-003",
    )
```

### Finding 2b — `_merge_relationship` has the same f-string and `**rel` issues

**File:** `graph/loaders/load_seed.py`, lines 66–80

```python
def _merge_relationship(tx, rel: dict) -> None:
    rel_type = rel["type"]
    if rel_type not in REL_TYPES:
        raise ValueError(f"Unsupported graph relationship: {rel_type}")
    tx.run(
        f"""
        MATCH (source {{id: $source}})
        MATCH (target {{id: $target}})
        MERGE (source)-[r:{rel_type}]->(target)
        SET r.reason = $reason,
            r.weight = $weight,
            r.graph_version = 'NC-GRAPH-003'
        """,
        **rel,               # ← passes rel["type"] as unused parameter $type
    )
```

`**rel` passes `type` (e.g., `"RECOMMENDS"`) as a parameter named `$type` that the Cypher
does not bind. The driver ignores it. But `type` is used in the f-string to build the query,
not as a parameter — which is the correct role for it. The `**rel` expansion also passes
`source` and `target` which ARE bound (`$source`, `$target`). This works but the pattern
allows future `GraphRelationship` fields to silently enter the driver call.

**Exact fix:**

```python
_REL_MERGE: dict[str, str] = {
    rt: (
        f"MATCH (source {{id: $source}})"
        f" MATCH (target {{id: $target}})"
        f" MERGE (source)-[r:{rt}]->(target)"
        f" SET r.reason = $reason,"
        f"     r.weight = $weight,"
        f"     r.graph_version = $graph_version"
    )
    for rt in REL_TYPES
}


def _merge_relationship(tx, rel: dict) -> None:
    rel_type = rel["type"]
    if rel_type not in _REL_MERGE:
        raise ValueError(f"Unsupported graph relationship: {rel_type}")
    tx.run(
        _REL_MERGE[rel_type],
        source=rel["source"],             # explicit parameters — no **rel
        target=rel["target"],
        reason=rel["reason"],
        weight=rel["weight"],
        graph_version="NC-GRAPH-003",
    )
```

---

## GV-1: Trigger function with hardcoded entity ID column

**NC-GRAPH-003 finding:** `COALESCE(NEW.place_id, OLD.place_id)` used in a single trigger
function applied to all entity tables.

**In the implemented code:** No PostgreSQL triggers exist. No `nc_graph_change_queue` table.
The sync is `graph/sync/sync_seed.py`, which is:

```python
from graph.loaders.load_seed import load_seed

if __name__ == "__main__":
    load_seed()
```

GV-1 as specified does not exist in the current codebase. The finding applies to future
trigger infrastructure.

**One actual code-level GV-1 analog exists in `_merge_node`:** the entity identity key is
hardcoded as `id` in the MERGE clause (`MERGE (n:{label} {{id: $id}})`). When trigger-based
sync is implemented, each entity table has a different PK column name. The MERGE key must
match the PostgreSQL PK. If the trigger infrastructure is built on top of the current loader
pattern, the hardcoded `id` will conflict with PostgreSQL PK columns (`place_id`,
`illustration_id`, `artist_id`, etc.) unless a translation layer is added.

**No code fix required now.** Document for the trigger implementation:

```
When building trigger infrastructure:
  - nc_graph_change_queue.entity_id is always UUID
  - Each trigger function must extract the correct PK column per table:
      nc_places          → OLD/NEW.place_id
      nc_illustrations   → OLD/NEW.illustration_id
      nc_artists         → OLD/NEW.artist_id
      nc_taxa            → OLD/NEW.taxon_id
  - The graph node always uses {id: $entity_id} as the MERGE key
  - The change queue stores entity_id as UUID regardless of source column name
  - One trigger function per table — no shared function with COALESCE(NEW.place_id, ...)
```

---

## Summary of exact fixes

Three files require changes. No new files.

### `services/api/graph_runtime.py`

**Change 1:** Add `_COMMERCE_LABELS` constant and update `_serialize_node` to strip `status`
for commerce labels (lines 15 and 27–36).

**Change 2:** Remove Product nodes from `RECOMMENDS` query targets (lines 139–156).

### `graph/loaders/load_seed.py`

**Change 3:** Replace `_merge_node` f-string + `**node` with pre-built query map and explicit
parameters (lines 48–63).

**Change 4:** Replace `_merge_relationship` f-string + `**rel` with pre-built query map and
explicit parameters (lines 66–80).

### No changes required

- `graph/seed.py` — no rights or commerce fields on nodes; no SOURCED_FROM relationships
- `graph/schema/constraints.cypher` — correct; no rights fields
- `graph/sync/sync_seed.py` — calls load_seed; GV-1 trigger infrastructure is future work
- `tests/unit/test_graph_api.py` — tests check slug and label only; unaffected by status removal

---

*NC-GRAPH-003A · v1.0 · 2026-06-13 · DRAFT*
