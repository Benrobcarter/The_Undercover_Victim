
import json, sys, os
from pathlib import Path

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def main(atlas_path: str, working_state_path: str, out_dir: str):
    atlas = load_json(atlas_path)
    root = Path(atlas_path).resolve().parent
    # load shards
    shards = {}
    for s in atlas["shards"]:
        sp = (root.parent / s["path"]).resolve()
        shards[s["name"]] = load_json(sp)
    # merge
    merged = {"contradictions": [], "contradictions_vex": [], "timelines": [], "evidence_vex": [], "manifest_meta": []}
    mapping = {
        "shard_contradictions_core": "contradictions",
        "shard_contradictions_vex": "contradictions_vex",
        "shard_timelines_core": "timelines",
        "shard_evidence_vex": "evidence_vex",
        "shard_manifest_meta": "manifest_meta"
    }
    for name, shard in shards.items():
        key = mapping.get(name)
        if not key:
            continue
        merged[key].extend(shard.get("items", []))
    # add working state
    try:
        working = load_json(working_state_path)
        merged["working_state"] = working
    except Exception as e:
        merged["working_state_error"] = str(e)
    # write monolith
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "consolidated_master.json", merged)
    # also write per-silo monoliths
    for k in ["contradictions", "contradictions_vex", "timelines", "evidence_vex", "manifest_meta"]:
        write_json(out_dir / f"{k}.json", {"items": merged[k]})
    print(f"Wrote consolidated files to: {out_dir}")

if __name__ == "__main__":
    atlas_path = sys.argv[1] if len(sys.argv) > 1 else "PROJECT_SHARDED_2025-08-26_v5/atlas.json"
    working_state_path = sys.argv[2] if len(sys.argv) > 2 else "PROJECT_SHARDED_2025-08-26_v5/working_state.json"
    out_dir = sys.argv[3] if len(sys.argv) > 3 else "PROJECT_SHARDED_2025-08-26_v5/_consolidated"
    main(atlas_path, working_state_path, out_dir)
