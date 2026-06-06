# Provider Routing Runtime v1

## Mission

Design the Provider Routing Runtime for Nature & Culture.

This document is architecture only. It does not implement migrations, workers,
routers, provider integrations, or tests.

Provider Routing maps approved internal `publication_candidates` to internal
provider capability decisions. It does not call provider APIs, create provider
products, publish storefront listings, reserve inventory, submit fulfillment, or
sync external state.

## Runtime Boundary

Provider Routing is a decision layer after Publication Intelligence.

```text
commerce_opportunities
  -> product_recommendations
  -> catalog_candidates
  -> catalog_variants
  -> publication_candidates
  -> provider_route_candidates
```

Allowed:

- Read approved or recommended publication candidates.
- Read catalog candidate and variant metadata.
- Read internal provider capability profiles.
- Decide which provider capability best fits the candidate.
- Store replayable route decisions in PostgreSQL.
- Mark route decisions stale when upstream data or policy changes.

Not allowed:

- No external API calls.
- No Shopify.
- No Etsy.
- No fulfillment execution.
- No provider product creation.
- No provider order creation.
- No external IDs as authoritative state.
- No provider webhook handling.

Provider names in this runtime are capability labels, not integrations.

## Design Goals

1. PostgreSQL is authoritative for all provider routing state.
2. Every route decision is deterministic and replayable.
3. Provider routing is policy-driven, not hardcoded in workers.
4. Provider capability profiles are governed records.
5. Provider route candidates never execute fulfillment.
6. Stale decisions are preserved for audit and cannot drive execution.
7. Future providers can be added through capability profiles and policy rules.

## Core Tables

### provider_routing_policy

`provider_routing_policy` is the versioned contract for mapping publication
candidates to provider capability profiles.

Recommended columns:

```sql
CREATE TABLE provider_routing_policy (
    id                         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version                    TEXT NOT NULL UNIQUE,
    status                     TEXT NOT NULL REFERENCES commerce_policy_status_vocabulary(value),
    effective_from             TIMESTAMPTZ,
    effective_until            TIMESTAMPTZ,
    authored_by                TEXT NOT NULL,
    approved_by                TEXT,
    approved_at                TIMESTAMPTZ,
    changelog                  TEXT NOT NULL,
    previous_version_id        UUID REFERENCES provider_routing_policy(id),
    max_route_age_days         INT NOT NULL DEFAULT 90 CHECK (max_route_age_days > 0),

    eligibility_gates          JSONB NOT NULL,
    provider_fit_rules         JSONB NOT NULL,
    capability_match_rules     JSONB NOT NULL,
    risk_rules                 JSONB NOT NULL,
    ranking_rules              JSONB NOT NULL,
    staleness_rules            JSONB NOT NULL,

    provenance                 JSONB NOT NULL DEFAULT '{}',
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                 TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Governance constraints:

- Only one active policy.
- Active policy requires `approved_by`, `approved_at`, and second-human approval.
- Policy is immutable after active, paused, or superseded status.
- Policy JSON must not contain executable integration configuration.

Do not store:

- API keys.
- endpoint URLs.
- webhook secrets.
- external product IDs.
- external variant IDs.
- order IDs.
- fulfillment IDs.

### provider_capability_profiles

`provider_capability_profiles` describe what a provider can support in theory.
They are internal capability records, not live integrations.

Recommended columns:

```sql
CREATE TABLE provider_capability_profiles (
    id                            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider_routing_policy_id     UUID NOT NULL REFERENCES provider_routing_policy(id),
    provider_key                   TEXT NOT NULL,
    provider_label                 TEXT NOT NULL,
    status                         TEXT NOT NULL DEFAULT 'draft',

    allowed_product_families       TEXT[] NOT NULL DEFAULT '{}',
    allowed_product_types          TEXT[] NOT NULL DEFAULT '{}',
    supported_variant_options      JSONB NOT NULL DEFAULT '{}',
    supported_asset_requirements   JSONB NOT NULL DEFAULT '{}',
    supported_price_bands          TEXT[] NOT NULL DEFAULT '{}',
    geographic_scope               JSONB NOT NULL DEFAULT '{}',
    operational_constraints        JSONB NOT NULL DEFAULT '{}',
    risk_profile                   JSONB NOT NULL DEFAULT '{}',

    priority                       INT NOT NULL DEFAULT 100,
    provenance                     JSONB NOT NULL DEFAULT '{}',
    created_at                     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (provider_routing_policy_id, provider_key)
);
```

Provider capability profile examples:

- `gelato_print_network`
- `lulu_book_printing`
- `direct_download`
- `future_provider_template`

These keys are internal routing labels. They do not authorize external calls.

### provider_route_candidates

`provider_route_candidates` are derived route decisions for publication
candidates.

Recommended columns:

```sql
CREATE TABLE provider_route_candidates (
    id                              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    publication_candidate_id         UUID NOT NULL REFERENCES publication_candidates(id),
    catalog_candidate_id             UUID NOT NULL REFERENCES catalog_candidates(id),
    catalog_variant_id               UUID NOT NULL REFERENCES catalog_variants(id),
    provider_routing_policy_id       UUID NOT NULL REFERENCES provider_routing_policy(id),
    provider_capability_profile_id   UUID NOT NULL REFERENCES provider_capability_profiles(id),

    provider_key                     TEXT NOT NULL,
    route_status                     TEXT NOT NULL DEFAULT 'draft',
    route_decision                   TEXT NOT NULL,
    route_priority                   TEXT NOT NULL,

    provider_fit_score               NUMERIC(4,3) NOT NULL CHECK (provider_fit_score BETWEEN 0 AND 1),
    capability_match_score           NUMERIC(4,3) NOT NULL CHECK (capability_match_score BETWEEN 0 AND 1),
    operational_risk_score           NUMERIC(4,3) NOT NULL CHECK (operational_risk_score BETWEEN 0 AND 1),
    route_score                      NUMERIC(4,3) NOT NULL CHECK (route_score BETWEEN 0 AND 1),

    route_basis                      JSONB NOT NULL DEFAULT '{}',
    input_snapshot                   JSONB NOT NULL DEFAULT '{}',
    staleness_status                 TEXT NOT NULL DEFAULT 'current',
    stale_reason                     TEXT,

    curator_decision                 TEXT NOT NULL DEFAULT 'pending'
                                      REFERENCES commerce_curator_decision_vocabulary(value),
    curator_reviewed_by              TEXT,
    curator_reviewed_at              TIMESTAMPTZ,
    provenance                       JSONB NOT NULL DEFAULT '{}',
    created_at                       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (publication_candidate_id, provider_capability_profile_id)
);
```

Route decisions:

- `recommend`
- `hold`
- `block`

Route statuses:

- `draft`
- `pending_curator_review`
- `approved_for_planning`
- `needs_revision`
- `blocked`
- `stale`
- `retired`
- `superseded`

`approved_for_planning` still does not execute fulfillment. It only says the
route is suitable for later execution-layer design.

## Provider Mapping Rules

### Gelato

Gelato maps to print-oriented catalog variants.

Use the internal capability profile key:

```text
gelato_print_network
```

Good fit:

- `wall_art`
- `museum_print`
- `card`
- `calendar`
- `puzzle`
- selected `home_decor`, if introduced later

Required capability signals:

- physical product family
- print-ready source image
- dimensions present
- price snapshot present
- rights snapshot present
- publication candidate decision is `recommend` or `hold`

Risk signals:

- low image width
- missing dimensions
- missing media requirements
- premium print without strong quality score
- stale catalog variant

Design rule:

Gelato may be recommended as a provider route, but the runtime must not create a
Gelato product, call Gelato APIs, store Gelato product UIDs, or submit orders.

### Lulu

Lulu maps to book and publication-oriented variants.

Use the internal capability profile key:

```text
lulu_book_printing
```

Good fit:

- `book`
- `educational`
- selected `institutional_license` support collateral, if represented as a book
  or document variant

Required capability signals:

- product type is book-like or educational material
- page/document structure exists or is planned
- title and description are complete
- rights snapshot exists
- price snapshot exists

Risk signals:

- single image with no editorial context
- missing page count or format specification
- weak publication readiness score
- stale catalog candidate

Design rule:

Lulu may be recommended as a route for planning only. The runtime must not create
Lulu projects, ISBN metadata, print jobs, external product IDs, or fulfillment
orders.

### Direct Download

Direct Download maps to internal digital delivery planning.

Use the internal capability profile key:

```text
direct_download
```

Good fit:

- `educational`
- `institutional_license`
- digital reference packs
- public-domain image downloads
- research or classroom material

Required capability signals:

- rights confidence high enough for digital access
- asset requirements satisfied
- digital format specification present or derivable
- price snapshot present for paid internal planning, or zero-price policy for
  free access if supported later

Risk signals:

- uncertain rights
- missing derivative format requirements
- missing attribution or provenance text
- content requiring curator notes before release

Design rule:

Direct Download is still a provider route candidate, not delivery execution. The
runtime must not generate download URLs, create access tokens, write CDN state,
or expose files publicly.

### Future Providers

Future providers are added by inserting new `provider_capability_profiles` under
an approved `provider_routing_policy`.

Required future provider profile fields:

- `provider_key`
- `allowed_product_families`
- `allowed_product_types`
- `supported_variant_options`
- `supported_asset_requirements`
- `supported_price_bands`
- `operational_constraints`
- `risk_profile`

Future provider policy must remain declarative. Execution-specific details are
out of scope for this runtime.

## Eligibility Gates

A publication candidate may enter provider routing only when:

```text
publication_candidates.publication_status IN ('draft', 'approved_for_planning')
publication_candidates.decision IN ('recommend', 'hold')
publication_candidates.staleness_status = 'current'
catalog_candidates.catalog_status IN ('draft', 'approved')
catalog_variants.variant_status IN ('draft', 'approved')
catalog_variants.price_snapshot exists
catalog_candidates.rights_snapshot exists
provider_routing_policy.status = 'active'
provider_capability_profiles.status IN ('draft', 'approved')
```

Blocked:

- stale publication candidates
- blocked publication decisions
- missing catalog variant
- missing price snapshot
- missing rights snapshot
- provider capability profile not governed by active policy

## Scoring Model

Provider route score is deterministic.

Recommended subscores:

```text
provider_fit_score
capability_match_score
operational_risk_score
route_score
```

Recommended formula:

```text
route_score =
  0.45 * provider_fit_score
+ 0.40 * capability_match_score
+ 0.15 * (1 - operational_risk_score)
```

Decision thresholds:

```text
recommend >= 0.750 and operational_risk_score <= risk_tolerance
hold      >= 0.500
block     <  0.500 or hard gate failed
```

Priority thresholds:

```text
high   >= 0.850
medium >= 0.650
low    >= 0.000
```

## Worker Design

### provider_routing_worker

Responsibilities:

1. Load active `provider_routing_policy`.
2. Load active provider capability profiles.
3. Claim eligible `publication_candidates`.
4. Join each candidate to catalog candidate and catalog variant snapshots.
5. Evaluate provider capability fit.
6. Write append-only audit entry first.
7. Insert `provider_route_candidates`.
8. Never call external APIs.
9. Never create fulfillment state.

Claim query shape:

```sql
SELECT pc.*, cc.*, cv.*
FROM publication_candidates pc
JOIN catalog_candidates cc ON cc.id = pc.catalog_candidate_id
JOIN catalog_variants cv ON cv.id = pc.catalog_variant_id
WHERE pc.publication_status IN ('draft','approved_for_planning')
  AND pc.decision IN ('recommend','hold')
  AND pc.staleness_status = 'current'
  AND cc.catalog_status IN ('draft','approved')
  AND cv.variant_status IN ('draft','approved')
  AND NOT EXISTS (
      SELECT 1
      FROM provider_route_candidates prc
      WHERE prc.publication_candidate_id = pc.id
        AND prc.route_status NOT IN ('retired','superseded','stale')
  )
LIMIT $1;
```

### provider_replay_worker

Responsibilities:

1. Read pinned provider routing policy.
2. Read pinned capability profile.
3. Read original publication candidate, catalog candidate, and variant snapshots.
4. Recompute provider fit, capability match, risk, route score, decision, and
   priority.
5. Compare against stored `provider_route_candidates`.
6. Emit replay verdict.

Replay passes only if:

- same policy version
- same capability profile version/snapshot
- same input snapshot hash
- same subscores after policy rounding
- same route decision
- same route priority
- no external execution state is present

## Append-Only Audit

Implementation should use a provider-specific append-only log, e.g.
`provider_routing_audit_log`.

Events:

- `provider_route_candidate_created`
- `provider_route_decision_computed`
- `provider_route_stale`
- `provider_replay_verified`
- `provider_replay_failed`

Audit entry fields:

- route candidate ID
- publication candidate ID
- provider routing policy ID
- provider capability profile ID
- event type
- event timestamp
- actor type and actor ID
- input snapshot
- output snapshot
- previous state
- new state
- entry checksum
- previous entry checksum
- generated by

Audit must prohibit update and delete.

## Staleness Handling

A provider route candidate becomes stale when:

- source publication candidate becomes stale
- source publication candidate decision changes
- catalog candidate changes status to blocked, retired, superseded, or stale
- catalog variant changes status to blocked, retired, superseded, or stale
- price snapshot changes
- rights snapshot changes
- provider capability profile changes
- provider routing policy major version changes

Stale action:

```text
route_status = 'stale'
staleness_status = 'stale'
stale_reason = policy-defined reason
append provider_route_stale audit event
```

Do not delete stale routes.
Do not silently mutate route scores.
Regeneration creates a new route candidate or supersedes the old one under a new
policy decision.

## API Design

No external provider APIs are called.

Internal FastAPI endpoints, if later implemented, should be read/governance only:

```text
GET  /provider-routing/policies
GET  /provider-routing/policies/{id}
GET  /provider-routing/capability-profiles
GET  /provider-routing/route-candidates
GET  /provider-routing/route-candidates/{id}
POST /provider-routing/route-candidates/{id}/review
POST /provider-routing/replay/{route_candidate_id}
```

These endpoints must not publish, sync, fulfill, or call providers.

## Replay Test Plan

Required tests for implementation:

1. Gelato-capable wall art publication candidate creates a route candidate.
2. Lulu-capable book publication candidate creates a route candidate.
3. Direct Download educational candidate creates a route candidate.
4. Future provider profile can match without code changes.
5. Route score is deterministic.
6. Replay worker reproduces identical scores and decision.
7. Staleness handling marks route stale without deletion.
8. Audit chain works and is append-only.
9. No external API fields or execution state exist.

## Answer: Mapping Publication Candidates to Providers

A publication candidate maps to providers through governed capability matching:

- Gelato: match physical print variants such as wall art, museum prints, cards,
  calendars, and puzzles to `gelato_print_network` capability profiles.
- Lulu: match book-like and educational variants to `lulu_book_printing`
  capability profiles.
- Direct Download: match digital, educational, institutional, or reference
  variants to `direct_download` capability profiles.
- Future providers: add new capability profiles under an approved routing policy;
  the worker evaluates them using the same policy-defined fit, capability, and
  risk rules.

The output is only a `provider_route_candidate`. It is not a provider product,
not a publication action, and not a fulfillment instruction.
