#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 - <<'PY'
import json, pathlib
p = pathlib.Path("07_meta/atlas_FINAL_2025-09-01.json")
a = json.load(open(p, encoding="utf-8"))
root = p.parent.parent
missing=[]
for s in a.get("shards", []):
    path = root / s["path"]
    print(f"[CHECK] {s['name']:>24} -> {path} | {'OK' if path.exists() else 'MISSING'}")
    if not path.exists(): missing.append(str(path))
if missing:
    print("\n[FAIL] Missing shards:\n  " + "\n  ".join(missing))
    raise SystemExit(2)
PY
python3 consolidate_shards.py 07_meta/atlas_FINAL_2025-09-01.json 07_meta/working_state.json 08_audit/
echo "[OK] Merge complete → 08_audit/"
