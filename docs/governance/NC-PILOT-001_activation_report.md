# NC-PILOT-001 Activation Report

**Authority:** NC-PILOT-001  
**Status:** Activation sprint implemented  
**Date:** June 11, 2026

## Activation Scope

Implemented only activation metadata and verification surfaces:

1. Pilot launch configuration
2. Attribution assembly verification
3. Publication snapshot verification
4. Pilot monitoring endpoints
5. Pilot health checks
6. Launch-report generation

No new sources were onboarded. No media ingestion, source-item creation, or M36 writes were added.

## Runtime Additions

- `pilot_launch_config` stores the activation configuration for `nc_pilot_001_activation`.
- Required launch gates are bound to the existing publication checklist keys.
- Snapshot policy requires a stable snapshot hash and assembled attribution.
- Monitoring remains metadata-only and reads ingest run, evidence, snapshot, and stale recovery counts.

## API Activation Surfaces

- `/pilot/anchors/{anchor_slug}/launch-config`
- `/pilot/anchors/{anchor_slug}/verify-attribution`
- `/pilot/anchors/{anchor_slug}/verify-publication-snapshot`
- `/pilot/anchors/{anchor_slug}/monitoring`
- `/pilot/anchors/{anchor_slug}/health`
- `/pilot/anchors/{anchor_slug}/launch-report`

## Verification Coverage

- Launch gates: activation config must be enabled and required gates must exist in the publication checklist.
- Attribution: GeoNames, OSM, NASA, and NOAA notices are verified from anchor requirements and evidence sources.
- Idempotency: launch report records the existing unique/upsert constraints for anchors, ingest runs, evidence, and snapshots.
- Recovery: health and launch report fail recovery when stale recoverable ingest runs remain.
- Publication snapshots: verification checks snapshot body presence, deterministic SHA-256, attribution presence, and creator metadata.

## Activation Status

NC-PILOT-001 activation surfaces are implemented for pilot API validation. Final launch readiness still depends on the live database state for each anchor: current evidence, completed checklist gates, no stale recoverable ingest runs, and a valid publication snapshot.
