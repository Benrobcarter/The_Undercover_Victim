#!/usr/bin/env python3
"""
Merge atlas shards into consolidated JSON files.

- Reads atlas.json with a list of shards (name + path)
- Loads each shard's JSON and maps it into buckets (contradictions, timelines, etc.)
- Writes:
    - consolidated_master.json (everything + working_state)
    - <bucket>.json files with {"items": [...]}
- Outputs to both the chosen out_dir and dashboard/data
- Extras:
    --dedupe           : remove duplicates by 'id' (stable)
    --fail-on-missing  : exit non-zero if any shard fails to load
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

# ------------------ Config ------------------

MAPPING: Dict[str, str] = {
    "shard_contradictions_core": "contradictions",
    "shard_contradictions_vex": "contradictions_vex",
    "shard_timelines_core": "timelines",
    "shard_evidence_vex": "evidence_vex",
    "shard_manifest_meta": "manifest_meta",
    "contradictions_holiday_alibi": "contradictions",
    "contradictions_veritas_chat": "contradictions",
    "contradictions_duncan_patch": "contradictions",
}

BUCKET_KEYS = [
    "contradictions",
    "contradictions_vex",
    "timelines",
    "evidence_vex",
    "manifest_meta",
]

# ------------------ IO helpers ------------------

def load_json(p: Path) -> Optional[Any]:
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n[❌ ERROR] Broken JSON in:\n    {p}\n    → {e}\n")
        return None
    except FileNotFoundError:
        print(f"[⚠️ WARN] File not found: {p}")
        return None
    except Exception as e:
        print(f"[❌ ERROR] Cannot read {p}: {e}")
        return None

def write_json(p: Path, obj: Any) -> bool:
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[❌ ERROR] Writing JSON failed: {p}\n→ {e}")
        return False

# ------------------ Types ------------------

@dataclass
class ShardRef:
    name: str
    path: Path

# ------------------ Core logic ------------------

def parse_shards(atlas_obj: dict, atlas_path: Path) -> List[ShardRef]:
    shard_refs: List[ShardRef] = []
    shards = atlas_obj.get("shards", [])
    if not isinstance(shards, list):
        print("[❌ ERROR] atlas.json must contain a 'shards' array.")
        return shard_refs

    root = atlas_path.resolve().parent

    for idx, s in enumerate(shards):
        if not isinstance(s, dict):
            print(f"[skip] Invalid shard entry at index {idx}: expected object.")
            continue
        name = s.get("name")
        rel_path = s.get("path")
        if not isinstance(name, str) or not isinstance(rel_path, str) or not name or not rel_path:
            print(f"[skip] Shard missing valid 'name' or 'path' at index {idx}")
            continue
        sp = (root.parent / rel_path).resolve()
        shard_refs.append(ShardRef(name=name, path=sp))
    return shard_refs

def load_all_shards(shard_refs: Iterable[ShardRef]) -> Dict[str, Any]:
    loaded: Dict[str, Any] = {}
    for ref in shard_refs:
        print(f"🔍 Loading shard: {ref.name} → {ref.path}")
        data = load_json(ref.path)
        if data is not None:
            loaded[ref.name] = data
        else:
            print(f"[⛔ Skipped] Could not load: {ref.name}")
    return loaded

def ensure_buckets() -> Dict[str, List[Any]]:
    return {k: [] for k in BUCKET_KEYS}

def merge_items(loaded_shards: Dict[str, Any]) -> Dict[str, List[Any]]:
    buckets = ensure_buckets()
    for name, shard in loaded_shards.items():
        key = MAPPING.get(name)
        if not key:
            print(f"[skip] No mapping for shard: {name}")
            continue
        items = shard.get("items", []) if isinstance(shard, dict) else []
        if not isinstance(items, list):
            print(f"[skip] Shard '{name}' has non-list 'items'; skipping")
            continue
        buckets[key].extend(items)
    return buckets

def dedupe_by_id(items: List[Any]) -> List[Any]:
    """
    De-duplicate list of dicts by 'id' (string or int). Stable: keeps first seen.
    If an item lacks 'id', it is kept as-is.
    """
    seen = set()
    out: List[Any] = []
    for it in items:
        if isinstance(it, dict) and "id" in it and isinstance(it["id"], (str, int)):
            k = it["id"]
            if k in seen:
                continue
            seen.add(k)
            out.append(it)
        else:
            out.append(it)
    return out

def build_output_payload(
    merged_buckets: Dict[str, List[Any]],
    working_state: Optional[Any],
    working_state_error: Optional[str],
    perform_dedupe: bool,
) -> Dict[str, Any]:
    merged: Dict[str, Any] = {k: merged_buckets.get(k, []) for k in BUCKET_KEYS}

    if perform_dedupe:
        for k in BUCKET_KEYS:
            before = len(merged[k])
            merged[k] = dedupe_by_id(merged[k])
            after = len(merged[k])
            if after != before:
                print(f"[ℹ️ dedupe] {k}: {before} → {after}")

    if working_state is not None:
        merged["working_state"] = working_state
    if working_state_error:
        merged["working_state_error"] = working_state_error

    return merged

def write_outputs(out_dir: Path, merged: Dict[str, Any]) -> bool:
    ok = True
    targets = [out_dir, Path("dashboard/data")]
    for directory in targets:
        if not write_json(directory / "consolidated_master.json", merged):
            ok = False
        for k in BUCKET_KEYS:
            if not write_json(directory / f"{k}.json", {"items": merged[k]}):
                ok = False
    print(f"✅ Wrote consolidated files to: {[str(d) for d in targets]}")
    return ok

# ------------------ CLI ------------------

def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Merge atlas shards into consolidated JSON files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("atlas_path", nargs="?", default="07_meta/atlas.json", help="Path to atlas.json")
    p.add_argument("working_state_path", nargs="?", default="07_meta/working_state.json", help="Path to working_state.json")
    p.add_argument("out_dir", nargs="?", default="08_audit", help="Primary output directory")
    p.add_argument("--dedupe", action="store_true", help="De-duplicate items by 'id' field if present")
    p.add_argument("--fail-on-missing", action="store_true", help="Exit non-zero if any shard failed to load")
    return p.parse_args(argv)

def main(argv: List[str]) -> int:
    args = parse_args(argv)
    atlas_path = Path(args.atlas_path)
    working_state_path = Path(args.working_state_path)
    out_dir = Path(args.out_dir)

    atlas = load_json(atlas_path)
    if atlas is None:
        print("❌ Cannot continue: atlas.json is invalid or missing")
        return 2

    shard_refs = parse_shards(atlas if isinstance(atlas, dict) else {}, atlas_path)
    if not shard_refs:
        print("❌ No valid shards found in atlas.json")
        return 3

    loaded = load_all_shards(shard_refs)
    if args.fail_on_missing and len(loaded) != len(shard_refs):
        print("❌ One or more shards failed to load (per --fail-on-missing).")
        return 4

    merged_buckets = merge_items(loaded)

    ws = load_json(working_state_path)
    working_state_error = None
    if ws is None:
        if not working_state_path.exists():
            print(f"[ℹ️ info] working_state.json not found at {working_state_path}; proceeding with empty object")
            working_state = {}
        else:
            working_state = {}
            working_state_error = f"Failed to load working_state from {working_state_path}"
    else:
        working_state = ws

    payload = build_output_payload(
        merged_buckets, working_state, working_state_error, perform_dedupe=args.dedupe
    )

    ok = write_outputs(out_dir, payload)
    return 0 if ok else 5

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
