# eval-run-manifest

A JSON envelope for eval run provenance, environment, code SHA, judge card, contamination report, dataset cards, result digest, and optional signatures.

## Quickstart

```bash
pip install eval-run-manifest
eval-run-manifest build examples
eval-run-manifest validate examples/judge_bench_manifest.json
```

## What This Is Not

Signing is optional and this package does not require AuraOne services. Examples are synthetic.
