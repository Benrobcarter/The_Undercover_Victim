import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "consolidated_master.json"

silos = [
    "contradictions.json",
    "contradictions_vex.json",
    "timelines.json",
    "evidence_vex.json",
    "manifest_meta.json"
]

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def main():
    merged = {}
    for silo in silos:
        path = DATA_DIR / silo
        if not path.exists():
            print(f"[warn] Missing: {silo}")
            continue
        try:
            data = load_json(path)
            key = silo.replace(".json", "")
            merged[key] = data.get("items", [])
            print(f"[ok] Loaded: {silo}")
        except Exception as e:
            print(f"[error] Failed to load {silo}: {e}")
    write_json(OUTPUT_FILE, merged)
    print(f"✅ Rebuilt: {OUTPUT_FILE.name}")

if __name__ == "__main__":
    main()