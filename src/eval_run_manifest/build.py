from pathlib import Path
from datetime import datetime, timezone
import hashlib, os

def build(run_dir):
    root=Path(run_dir); h=hashlib.sha256()
    for p in sorted(x for x in root.rglob('*') if x.is_file()): h.update(p.read_bytes())
    return {"run_id": root.name, "timestamp": datetime.now(timezone.utc).isoformat(), "code_sha": os.environ.get('GITHUB_SHA','local'), "env": {"python":"3"}, "rubric_ref": "rubric.json", "judge_card_ref": "judge-card.json", "contamination_report_ref": "contamination.json", "dataset_card_refs": [], "results_digest": h.hexdigest(), "signature": None}
