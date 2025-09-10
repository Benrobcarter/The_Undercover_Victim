#!/usr/bin/env python3
import json, sys
from pathlib import Path

def load_json(p):
    p = Path(p)
    if not p.exists():
        return None
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Failed to load {p}: {e}")
        return None

def write_json(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    with Path(p).open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def main():
    if len(sys.argv) < 4:
        print("Usage: consolidate_shards.py <atlas.json> <working_state.json> <out_dir>")
        sys.exit(1)

    atlas_path = Path(sys.argv[1]).resolve()
    working_state_path = Path(sys.argv[2]).resolve()
    out_dir = Path(sys.argv[3]).resolve()

    project_root = atlas_path.parent.parent  # atlas lives in 07_meta/
    atlas = load_json(atlas_path)
    if not atlas:
        print(f"[ERR] Could not load atlas: {atlas_path}")
        sys.exit(2)

    consolidated = {
        "contradictions": [],
        "contradictions_vex": [],
        "timelines": [],
        "evidence_vex": [],
        "manifest_meta": [],
        "working_state": load_json(working_state_path) or {"version":"1.0","notes":"No working_state found"},
        "overlays": {}
    }

    # Load shard contents
    for s in atlas.get("shards", []):
        rel = s.get("path")
        if not rel: 
            continue
        data = load_json(project_root / rel)
        name = s.get("name","")
        if data is None:
            print(f"[WARN] Missing shard: {rel}")
            continue
        # naive routing by shard name
        key = None
        if "contradictions" in name and "vex" not in name:
            key = "contradictions"
        elif "timelines" in name:
            key = "timelines"
        elif "evidence_vex" in name or "evidence" in name:
            key = "evidence_vex"
        elif "manifest_meta" in name:
            key = "manifest_meta"
        elif "contradictions_vex" in name:
            key = "contradictions_vex"
        if key:
            consolidated[key] = data

    # Load overlays (meta helpers)
    overlays_out = {}
    for o in atlas.get("overlays", []):
        rel = o.get("path")
        if not rel: 
            continue
        data = load_json(project_root / rel)
        overlays_out[o.get("name","overlay")] = data
    consolidated["overlays"] = overlays_out

    # Write per-file outputs for dashboard compatibility
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "consolidated_master.json", consolidated)
    write_json(out_dir / "contradictions.json", consolidated.get("contradictions", []))
    write_json(out_dir / "contradictions_vex.json", consolidated.get("contradictions_vex", []))
    write_json(out_dir / "timelines.json", consolidated.get("timelines", []))
    write_json(out_dir / "evidence_vex.json", consolidated.get("evidence_vex", []))
    write_json(out_dir / "manifest_meta.json", consolidated.get("manifest_meta", []))
    print("[OK] Wrote merged outputs to", out_dir)

if __name__ == "__main__":
    main()
