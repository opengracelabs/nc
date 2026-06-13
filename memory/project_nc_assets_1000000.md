---
name: project-nc-assets-1000000
description: "NC-ASSETS-1000000 Asset Factory Blueprint. Architecture for scaling from thousands to 1M assets. 9-stage pipeline, 9 adapter classes, 10 rights classes + general engine, 4 asset tiers, BHL illustration extraction (500K+ from 60M pages), AI content governance, graph at 1M nodes/15M edges, 12 invariants. DD-BHL-001 = critical gap."
metadata:
  type: project
---

NC-ASSETS-1000000 Asset Factory Blueprint — DRAFT 2026-06-13, pending ratification.
File: `docs/architecture/NC-ASSETS-1000000_asset_factory_blueprint.md`

**Scale:** 1M total assets → ~100K-200K commerce-ready IOs → ~300-400K editorial → ~500-700K discovery. Pilot (20) → Sprint 1 (5K) → Sprint 2 (50K) → Sprint 3 (200K) → Sprint 4 (500K) → Target (1M).

**Source institutions and estimated contribution:**
- BHL (NEW — DD-BHL-001 REQUIRED): 500,000+ (largest single source, all pre-1928 PD)
- Europeana (DD-EUR-001): 200,000+
- Smithsonian Open Access (DD-SMITHSONIAN pending): 100,000+
- Getty (DD-GETTY-001): 88,000
- Met (DD-MET-001): 50,000+
- NHM (DD-NHM-001): 50,000+
- Mia (DD-MIA-001): 64,000+
- All others: +200,000

**9-stage pipeline:** Harvest (AC-1 to AC-9) → Normalise → Rights Screen → Illustration Filter → Quality Screen → IO Candidate Generation → M36 Write → Graph Integration → Product Routing.

**4 asset tiers:**
- Tier 1: Commerce-ready IO (ULAN + GeoNames + rights confidence ≥ 0.85)
- Tier 2: Editorial asset (rights confirmed + one anchor)
- Tier 3: Discovery asset (rights confirmed, no anchors)
- Tier 4: Reference/context (failed illustration filter or below quality threshold)

**9 adapter classes:** AC-1 OAI-PMH · AC-2 REST cursor · AC-3 CSV bulk · AC-4 Linked Art · AC-5 ActivityStreams · AC-6 CKAN Datastore · AC-7 Flickr API · AC-8 BHL Page API · AC-9 DPLA two-tier.

**General rights engine:** Decision tree → ALLOWED/REVIEW/BLOCKED + confidence score. ALLOWED_URIS + REVIEW_URIS + BLOCKED_URIS registries. Date rules: pre-1928 US = NoC-US (0.95), life+100 = life_plus_100 (0.85), pre-1800 = pre_1800_pd (0.90). Bridgeman doctrine applies; ToS is separate gate.

**BHL illustration extraction pipeline (most novel piece):**
BHL PageType filter → 500K candidate pages from 60M → image classifier → OCR caption → ULAN/GeoNames/GBIF resolution → rights assignment (pre-1928 = NoC-US) → IO candidate.
BHL-GBIF bridge: BHL Name Usage service already extracted GBIF taxon keys — inherit directly.
DD-BHL-001 required before commercial activation.

**AI content governance (NC-AI-001 extends to 1M):**
AI does: classify illustration type, resolve ULAN/GeoNames/GBIF, draft collection copy (3 candidates). AI never: publish without curator approval, write signed statements, make rights determinations, activate products, modify gate records, use Qwen/DeepSeek off-local.

**Graph at 1M:** ~1.13M nodes / ~15M edges. 7 bounded discovery journey queries. 3 new collection types only possible at scale: cross-place illustrator collection, designation-family meta-collection, era-and-expedition collection.

**Trust preservation at scale:** Confidence scoring per field (ulan/geonames/rights/date/image). Public confidence display on verify page. gate_events table (append-only audit, named humans). NC-PDPS L6 (Commercial Activation) always human; L1-L5 automatable.

**12 invariants AF-1–AF-12:** Rights gate first · confidence public · human verdicts immutable · AI drafts never published · Gate E always two humans · CE allocation governed · BHL requires DD-BHL-001 · Bridgeman+ToS separate gates · GBIF media prohibited · IFC-1 unconditional · L6 always human · Qwen/DeepSeek local only.

**12 open actions:** OA-1 DD-BHL-001 (CRITICAL) · OA-2 SA-BHL-001 · OA-3 illustration classifier ML model · OA-4 ULAN fuzzy lookup service · OA-5 M36 schema extension · OA-6 gate_events table · OA-7 collection_candidates table · OA-8 AC-8 BHL adapter · OA-9 rights verification engine · OA-10 AI content queue · OA-11 graph schema migration · OA-12 DD-SMITHSONIAN-001.

See also: [[project-nc-commerce-2000]] [[project-nc-graph-002]] [[project-nc-ai-001]] [[project-nc-trust-003]] [[project-nhm-audit]] [[project-nga-audit]]
