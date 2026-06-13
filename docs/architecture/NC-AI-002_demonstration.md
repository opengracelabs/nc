# NC-AI-002 Demonstration

NC-AI-002 demonstrates the first grounded generation flow for Earthrise using the
`deterministic-mock-v1` interface only. No external APIs are called.

## Input

- NASA source record: `AS08-14-2383`
- Product metadata: `NC-PROD-001`, `NC-PROD-008`, manual purchase only, Phase 0
- Attribution: `NASA: Photograph by William Anders, Apollo 8, December 24, 1968. § 105 — public domain.`
- Nonendorsement: `Image credit: NASA. NASA does not endorse this product.`

## Workflow

```text
retrieval
  -> NASA source record
  -> Earthrise product metadata
grounding
  -> source record AS08-14-2383
  -> rights_status verified_pd
  -> NASA attribution and nonendorsement
generation
  -> product description
  -> story variant
  -> educational summary
review
  -> pending human review
  -> approved_for_demo_not_publication
  -> publication_allowed remains false
```

## Generated Outputs

The deterministic mock emits task-specific advisory drafts:

1. Product description:
   `Earthrise is a manually fulfilled Nature & Culture product grounded in NASA source record AS08-14-2383. The work is treated as public domain under 17 U.S.C. § 105; source credit and nonendorsement must remain visible wherever the product copy appears.`

2. Story variant:
   `Story variant: Earthrise, photographed during Apollo 8, is presented here through NASA source record AS08-14-2383. The draft may discuss the image's historical and cultural importance, but it remains advisory copy pending human review and cannot imply agency endorsement.`

3. Educational summary:
   `Educational summary: Earthrise is a NASA Apollo 8 photograph associated with source record AS08-14-2383. Learners should understand the image, its public-domain basis under 17 U.S.C. § 105, and the requirement to preserve NASA credit and nonendorsement.`

Every result preserves source references and attribution requirements. The demonstration does not
publish content automatically.
