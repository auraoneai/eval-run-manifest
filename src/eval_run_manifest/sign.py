import hashlib,json
def digest(data): return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
def sign(manifest, key=None): return {**manifest, "signature": "unsigned:" + digest(manifest)}
