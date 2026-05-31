# MinIO Bucket Layout

## Buckets

| Bucket | Purpose | Who writes | Who reads |
|---|---|---|---|
| `nc-raw` | Untouched source artifacts as fetched | workers | workers, api |
| `nc-normalized` | Canonical-schema artifacts after normalization | workers | workers, api |
| `nc-curated` | Human-reviewed, publication-ready exports | api | api, public (scoped) |

## Path Conventions

```
nc-raw/
├── ingestion/{place_id}/{ingest_id}/{artifact_name}
├── ingestion/{place_id}/{ingest_id}/{artifact_name}.headers.json
├── discovery/{source}/{run_id}/{response_name}
└── quarantine/{place_id}/{ingest_id}/{artifact_name}

nc-normalized/
├── ingestion/{place_id}/{ingest_id}/record.json
├── ingestion/{place_id}/{ingest_id}/geometry.geojson
├── ingestion/{place_id}/{ingest_id}/entity_links.json
└── ingestion/{place_id}/{ingest_id}/occurrences.jsonl

nc-curated/
├── sites/{place_id}/latest.json
├── sites/{place_id}/{version}.json
└── exports/temp/{export_id}.zip
```

## Policies

- `policies/worker_policy.json` — read/write on `nc-raw` and `nc-normalized`; read-only on `nc-curated`
- `policies/api_policy.json` — read-only on `nc-raw` and `nc-normalized`; read/write on `nc-curated`

## Lifecycle

- `quarantine/` artifacts expire after 90 days.
- `raw/ingestion/` artifacts transition to cold storage after 365 days.
- `exports/temp/` artifacts expire after 7 days.
