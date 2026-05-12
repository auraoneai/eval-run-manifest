import argparse
import json
from pathlib import Path

from .build import build
from .sign import sign
from .validate import validate

def main(argv=None):
    p=argparse.ArgumentParser(prog="eval-run-manifest")
    sub=p.add_subparsers(dest="cmd", required=True)
    b=sub.add_parser("build")
    b.add_argument("run_dir")
    b.add_argument("--out")
    v=sub.add_parser("validate")
    v.add_argument("path")
    s=sub.add_parser("sign")
    s.add_argument("path")
    s.add_argument("--out", required=True)
    s.add_argument("--key")
    s.add_argument("--sigstore-bundle")
    args=p.parse_args(argv)
    if args.cmd == "validate":
        manifest=json.loads(Path(args.path).read_text(encoding="utf-8"))
        errors=validate(manifest)
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
        return 0 if not errors else 1
    if args.cmd == "sign":
        manifest=json.loads(Path(args.path).read_text(encoding="utf-8"))
        signed=sign(manifest, key=args.key, sigstore_bundle=args.sigstore_bundle)
        errors=validate(signed)
        Path(args.out).write_text(json.dumps(signed, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"ok": not errors, "path": args.out, "errors": errors}, indent=2))
        return 0 if not errors else 1
    manifest=build(args.run_dir)
    errors=validate(manifest)
    if args.out:
        Path(args.out).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": manifest, "errors": errors}, indent=2))
    return 0 if not errors else 1
if __name__ == '__main__': raise SystemExit(main())
