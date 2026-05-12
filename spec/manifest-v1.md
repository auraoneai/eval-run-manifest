# Eval Run Manifest v1

Fields: `run_id`, `timestamp`, `code_sha`, `env`, `rubric_ref`, `judge_card_ref`, `contamination_report_ref`, `dataset_card_refs`, `results_digest`, and optional `signature`.

`signature` may be `null`, a local deterministic digest object, or an attached Sigstore bundle object. Sigstore remains optional: generate a bundle with the Sigstore CLI for a canonical manifest artifact, then attach it with `eval-run-manifest sign --sigstore-bundle bundle.json`.
