import argparse
import json
from pathlib import Path

from .build import build
from .validate import validate

def main(argv=None):
    p=argparse.ArgumentParser(prog="eval-run-manifest")
    sub=p.add_subparsers(dest="cmd", required=True)
    b=sub.add_parser("build")
    b.add_argument("run_dir")
    v=sub.add_parser("validate")
    v.add_argument("path")
    args=p.parse_args(argv)
    if args.cmd == "validate":
        manifest=json.loads(Path(args.path).read_text(encoding="utf-8"))
        errors=validate(manifest)
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
        return 0 if not errors else 1
    manifest=build(args.run_dir)
    errors=validate(manifest)
    print(json.dumps({"manifest": manifest, "errors": errors}, indent=2))
    return 0 if not errors else 1
if __name__ == '__main__': raise SystemExit(main())
