from eval_run_manifest.validate import validate

def test_manifest_valid():
    assert not validate({"run_id":"r","timestamp":"t","code_sha":"s","env":{},"rubric_ref":"r","judge_card_ref":"j","contamination_report_ref":"c","dataset_card_refs":[],"results_digest":"d"})
