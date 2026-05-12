from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_manifest(manifest: dict[str, Any]) -> str:
    payload = dict(manifest)
    payload.pop("signature", None)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def digest(data: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_manifest(data).encode("utf-8")).hexdigest()


def load_sigstore_bundle(path: str | Path) -> dict[str, Any] | str:
    raw = Path(path).read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def sign(manifest: dict[str, Any], key: str | None = None, sigstore_bundle: str | Path | None = None) -> dict[str, Any]:
    manifest_digest = digest(manifest)
    if sigstore_bundle is not None:
        return {
            **manifest,
            "signature": {
                "type": "sigstore-bundle",
                "digest": f"sha256:{manifest_digest}",
                "bundle": load_sigstore_bundle(sigstore_bundle),
            },
        }

    material = f"{key or 'unsigned'}:{manifest_digest}".encode("utf-8")
    return {
        **manifest,
        "signature": {
            "type": "local-digest",
            "digest": f"sha256:{manifest_digest}",
            "signature": hashlib.sha256(material).hexdigest(),
        },
    }
