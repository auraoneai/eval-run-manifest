from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import os


def _digest_tree(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        h.update(str(path.relative_to(root)).encode("utf-8"))
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def _first_existing(root: Path, names: list[str], fallback: str) -> str:
    for name in names:
        if (root / name).exists():
            return name
    return fallback


def build(run_dir: str | Path) -> dict:
    root = Path(run_dir)
    dataset_cards = sorted(str(path.relative_to(root)) for path in root.glob("*dataset*card*.json"))
    return {
        "run_id": root.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_sha": os.environ.get("GITHUB_SHA", "local"),
        "env": {"python": f"{os.sys.version_info.major}.{os.sys.version_info.minor}"},
        "rubric_ref": _first_existing(root, ["rubric.json", "rubric-spec.json"], "rubric.json"),
        "judge_card_ref": _first_existing(root, ["judge-card.json", "judge_card.json", "card.json"], "judge-card.json"),
        "contamination_report_ref": _first_existing(root, ["contamination.json", "contamination-report.json"], "contamination.json"),
        "dataset_card_refs": dataset_cards,
        "results_digest": _digest_tree(root),
        "signature": None,
    }
