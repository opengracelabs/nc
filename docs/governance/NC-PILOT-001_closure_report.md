# NC-PILOT-001 Closure Report

**Authority:** NC-PILOT-001  
**Status:** Closure sprint implemented  
**Date:** June 11, 2026

## Closure Outcomes

1. **GeoNames ID conflicts resolved**
   - Yellowstone: `5843642`
   - Grand Canyon National Park: `5296401`
   - Great Barrier Reef: `2164628`
   - Venice: `3164603`
   - Galápagos Islands: `3658931`
   - Papahānaumokuākea: GeoNames unconfirmed, no canonical GeoNames ID written
   - Earthrise: exempt; asset anchor, no place identity required

2. **Attribution assembly tests implemented**
   - GeoNames attribution is emitted when GeoNames identity is required.
   - OSM attribution is emitted when OSM tiles are displayed.
   - NASA and NOAA nonendorsement notices are emitted for NASA/NOAA evidence.

3. **Publication checklist built**
   - Checklist registry is seeded in `pilot_publication_checklist`.
   - Pilot API exposes `/pilot/anchors/{anchor_slug}/publication-checklist`.
   - Gates cover rights, human verification, source authority, nonendorsement copy, GeoNames attribution, OSM attribution, GeoNames ID write, and two-human sign-off.

4. **ESA-only Venice asset removed from launch set**
   - The Venice Sentinel/Copernicus launch asset is no longer listed as a launch asset.
   - The pilot registry records it as an excluded asset pending ESA source authority.

5. **Venice partial-launch status marked**
   - Venice is `partial_launch`.
   - Provenance states editorial-only publication until rights and source-authority gates pass.

6. **Governance assertions added**
   - GeoNames: `Geographic data © GeoNames (geonames.org) — CC BY 4.0`
   - OSM: `© OpenStreetMap contributors`
   - NASA: `Image credit: NASA. NASA does not endorse this product.`
   - NOAA: `Image: NOAA. NOAA does not endorse this product.`

## Operational Constraints Preserved

- No new source onboarding.
- No media ingestion.
- No source item creation.
- No M36 writes.
- HTTP remains outside DB transactions.
- Runtime writes use `ON CONFLICT` upserts for duplicate protection.
- Ingest run stale-state recovery remains available through pilot APIs.

## Closure Status

NC-PILOT-001 is closure-ready for pilot API validation, subject to normal database migration execution in the target environment and final human governance sign-off.
