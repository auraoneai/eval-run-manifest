import argparse,json
from .build import build
from .validate import validate

def main(argv=None):
    p=argparse.ArgumentParser(prog="eval-run-manifest"); sub=p.add_subparsers(dest="cmd", required=True); b=sub.add_parser('build'); b.add_argument('run_dir')
    args=p.parse_args(argv); manifest=build(args.run_dir); print(json.dumps({"manifest": manifest, "errors": validate(manifest)}, indent=2)); return 0
if __name__ == '__main__': raise SystemExit(main())
