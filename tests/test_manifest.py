import json

from eval_run_manifest.build import build
from eval_run_manifest.cli import main
from eval_run_manifest.sign import sign
from eval_run_manifest.validate import validate

def test_manifest_valid():
    assert not validate({"run_id":"r","timestamp":"t","code_sha":"s","env":{},"rubric_ref":"r","judge_card_ref":"j","contamination_report_ref":"c","dataset_card_refs":[],"results_digest":"d"})


def test_cli_validate_example():
    assert main(["validate", "examples/judge_bench_manifest.json"]) == 0


def test_eval_adapter_example_valid():
    assert main(["validate", "examples/eval_adapter_manifest.json"]) == 0


def test_build_manifest_from_run_dir(tmp_path):
    (tmp_path / "rubric-spec.json").write_text("{}", encoding="utf-8")
    (tmp_path / "judge-card.json").write_text("{}", encoding="utf-8")
    (tmp_path / "contamination-report.json").write_text("{}", encoding="utf-8")
    (tmp_path / "tutorial-dataset-card.json").write_text("{}", encoding="utf-8")
    manifest = build(tmp_path)
    assert not validate(manifest)
    assert manifest["rubric_ref"] == "rubric-spec.json"
    assert manifest["dataset_card_refs"] == ["tutorial-dataset-card.json"]


def test_cli_build_and_sign(tmp_path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "results.json").write_text('{"ok": true}', encoding="utf-8")
    manifest_path = tmp_path / "manifest.json"
    signed_path = tmp_path / "manifest.signed.json"
    assert main(["build", str(run_dir), "--out", str(manifest_path)]) == 0
    assert main(["sign", str(manifest_path), "--key", "test-key", "--out", str(signed_path)]) == 0
    signed = json.loads(signed_path.read_text(encoding="utf-8"))
    assert signed["signature"]["type"] == "local-digest"
    assert signed["signature"]["digest"].startswith("sha256:")


def test_attach_sigstore_bundle(tmp_path):
    bundle = tmp_path / "bundle.json"
    bundle.write_text('{"mediaType": "application/vnd.dev.sigstore.bundle+json"}', encoding="utf-8")
    signed = sign(
        {"run_id":"r","timestamp":"t","code_sha":"s","env":{},"rubric_ref":"r","judge_card_ref":"j","contamination_report_ref":"c","dataset_card_refs":[],"results_digest":"d"},
        sigstore_bundle=bundle,
    )
    assert signed["signature"]["type"] == "sigstore-bundle"
