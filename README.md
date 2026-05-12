# eval-run-manifest

A JSON envelope for eval run provenance, environment, code SHA, judge card, contamination report, dataset cards, result digest, and optional signatures.

## Quickstart

```bash
pip install eval-run-manifest
eval-run-manifest build examples --out manifest.json
eval-run-manifest sign manifest.json --out manifest.signed.json
eval-run-manifest validate examples/judge_bench_manifest.json
```

Reference manifests are included for synthetic `judge-bench` and `eval-adapter` runs. Signing is optional; for Sigstore, create a bundle with your normal Sigstore workflow and attach it with `eval-run-manifest sign manifest.json --sigstore-bundle bundle.json --out manifest.signed.json`.

## What This Is Not

Signing is optional and this package does not require AuraOne services. Examples are synthetic.
