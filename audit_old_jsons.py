import os, json
from pathlib import Path

SOURCE_DIR = Path.home() / "Documents" / "old-jsons"
DEST_DIRS = {
    "contradiction": "07_meta/shard_contradictions_core.json",
    "evidence": "07_meta/shard_evidence_vex.json",
    "timeline": "07_meta/shard_timelines_core.json",
}

# Load existing shards
def load_shard(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# Save updated shard
def save_shard(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Classify file type
def classify(obj):
    if "contradiction_id" in obj:
        return "contradiction"
    if "vex_id" in obj or "evidence_id" in obj:
        return "evidence"
    if "event_id" in obj or "timeline_id" in obj:
        return "timeline"
    return None

# Main merge loop
def main():
    for file in SOURCE_DIR.glob("*.json"):
        try:
            obj = json.load(open(file, "r", encoding="utf-8"))
        except Exception as e:
            print(f"[❌] Broken JSON: {file.name} → {e}")
            continue

        kind = classify(obj)
        if not kind:
            print(f"[❓] Unrecognized file: {file.name}")
            continue

        shard_path = Path(DEST_DIRS[kind])
        shard = load_shard(shard_path)

        if any(item.get("id") == obj.get("id") for item in shard):
            print(f"[⚠️] Duplicate (already in shard): {file.name}")
        else:
            shard.append(obj)
            save_shard(shard_path, shard)
            print(f"[✅] Imported → {kind}: {file.name}")
    
    print("\n🎉 Done. You can now run: python3 consolidate_shards.py")

if __name__ == "__main__":
    main()