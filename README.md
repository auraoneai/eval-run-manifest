# eval-run-manifest

Build a portable JSON record of an evaluation run's provenance and directory digest.

`eval-run-manifest` is for evaluation engineers, release reviewers, and reproducibility owners who need to archive which run directory, code SHA, Python version, rubric, judge card, contamination report, dataset cards, and result bytes were associated with an evaluation. Its differentiator is a deterministic digest over relative paths and file bytes alongside explicit artifact references, without claiming cryptographic signing.

## Inspectable Output

`build` writes a JSON manifest containing:

- `run_id`, UTC `timestamp`, `code_sha`, and Python major/minor version.
- Heuristic references to rubric, Judge Card, contamination report, and matching dataset-card files.
- A SHA-256 `results_digest` over every relative file path and file byte in the run directory.
- An optional `signature` field.

`validate` emits JSON with `ok` and missing required keys. It does not verify field types, referenced files, the directory digest, or attached signatures.

## Signature Semantics

The default `sign` path creates a deterministic `local-digest` marker. Even with `--key`, it hashes the literal key string with the manifest digest; it is not asymmetric signing and has no built-in verification command. `--sigstore-bundle` attaches an existing bundle and digest to the manifest but does not create or verify the Sigstore bundle.

Use your normal signing and verification system when cryptographic provenance is required.

## Runtime Boundary

All package operations are local and make no network requests. `build` reads every file under the supplied run directory to calculate the digest, so run it only where that complete local read is appropriate. A separate Sigstore workflow may use network services, but this package only attaches the resulting bundle.

## Install

```bash
python -m pip install eval-run-manifest==0.1.2
```

For development from a clone:

```bash
python -m pip install -e .
```

## Quickstart

From a repository checkout:

```bash
eval-run-manifest build examples --out manifest.json
eval-run-manifest validate manifest.json
eval-run-manifest sign manifest.json --out manifest.local-digest.json
```

See [`spec/manifest-v1.md`](spec/manifest-v1.md), [`spec/manifest-v1.json`](spec/manifest-v1.json), and the synthetic examples under [`examples/`](examples/).

## Release Status

Registry status verified July 13, 2026: version `0.1.2` is published on PyPI and tagged `v0.1.2` in the public repository. The project is alpha software. No provenance-certification or adoption claim is made.

## Limits

The manifest is an envelope and integrity input, not an attestation service. File references are inferred by name, validation is presence-only, and the local digest marker is not a cryptographic identity signature.

## Next Action

Build a manifest from the exact run directory, inspect every inferred reference and the directory digest, archive both together, and use an external signing and verification workflow when cryptographic provenance is required.
