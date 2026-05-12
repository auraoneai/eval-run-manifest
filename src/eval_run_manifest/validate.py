REQUIRED=["run_id","timestamp","code_sha","env","rubric_ref","judge_card_ref","contamination_report_ref","dataset_card_refs","results_digest"]
def validate(manifest): return [f"missing {f}" for f in REQUIRED if f not in manifest]
