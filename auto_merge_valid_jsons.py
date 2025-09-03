import os, json, shutil
from datetime import datetime

SOURCE = os.path.expanduser("~/Documents/The_Undercover_Victim/old_jsons")
DEST_ROOT = os.path.expanduser("~/Documents/The_Undercover_Victim/07_meta")
LOG_PATH = os.path.expanduser("~/Documents/The_Undercover_Victim/08_audit/OLD_JSONS_MERGE_LOG.txt")

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
log = []

def log_line(msg):
    print(msg)
    log.append(msg)

def classify_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "vex_id" in data.get("meta", {}):
            return "vex"
        elif "timeline_id" in data.get("meta", {}) or "timeline" in data.get("type", ""):
            return "timeline"
        elif "contradiction" in data.get("type", "").lower() or "contradiction" in data.get("meta", {}).get("title", "").lower():
            return "contradiction"
        else:
            return "unknown"
    except Exception as e:
        log_line(f"❌ Could not read {os.path.basename(path)}: {e}")
        return "error"

# Mapping
DEST_FILES = {
    "vex": "shard_evidence_vex.json",
    "timeline": "shard_timelines_core.json",
    "contradiction": "shard_contradictions_core.json"
}

log_line(f"\n🧠 Auto Merging Old JSONs — {datetime.now()}\n")

for fname in os.listdir(SOURCE):
    if not fname.endswith(".json"):
        continue

    fpath = os.path.join(SOURCE, fname)
    classification = classify_json(fpath)

    if classification in DEST_FILES:
        dest_file = DEST_FILES[classification]
        dest_path = os.path.join(DEST_ROOT, dest_file)
        backup_path = dest_path.replace(".json", f"_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")

        shutil.copy2(dest_path, backup_path)  # backup
        with open(dest_path, "r+", encoding="utf-8") as f:
            existing = json.load(f)
            if isinstance(existing, list):
                existing.append(json.load(open(fpath)))
                f.seek(0)
                json.dump(existing, f, indent=2)
                f.truncate()
                log_line(f"✅ Merged {fname} → {dest_file}")
 import os, json, shutil
from datetime import datetime

SOURCE = os.path.expanduser("~/Documents/The_Undercover_Victim/old_jsons")
DEST_ROOT = os.path.expanduser("~/Documents/The_Undercover_Victim/07_meta")
LOG_PATH = os.path.expanduser("~/Documents/The_Undercover_Victim/08_audit/OLD_JSONS_MERGE_LOG.txt")

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
log = []

def log_line(msg):
    print(msg)
    log.append(msg)

def classify_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "vex_id" in data.get("meta", {}):
            return "vex"
        elif "timeline_id" in data.get("meta", {}) or "timeline" in data.get("type", ""):
            return "timeline"
        elif "contradiction" in data.get("type", "").lower() or "contradiction" in data.get("meta", {}).get("title", "").lower():
            return "contradiction"
        else:
            return "unknown"
    except Exception as e:
        log_line(f"❌ Could not read {os.path.basename(path)}: {e}")
        return "error"

# Mapping
DEST_FILES = {
    "vex": "shard_evidence_vex.json",
    "timeline": "shard_timelines_core.json",
    "contradiction": "shard_contradictions_core.json"
}

log_line(f"\n🧠 Auto Merging Old JSONs — {datetime.now()}\n")

for fname in os.listdir(SOURCE):
    if not fname.endswith(".json"):
        continue

    fpath = os.path.join(SOURCE, fname)
    classification = classify_json(fpath)

    if classification in DEST_FILES:
        dest_file = DEST_FILES[classification]
        dest_path = os.path.join(DEST_ROOT, dest_file)
        backup_path = dest_path.replace(".json", f"_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")

        shutil.copy2(dest_path, backup_path)  # backup
        with open(dest_path, "r+", encoding="utf-8") as f:
            existing = json.load(f)
            if isinstance(existing, list):
                existing.append(json.load(open(fpath)))
                f.seek(0)
                json.dump(existing, f, indent=2)
                f.truncate()
                log_line(f"✅ Merged {fname} → {dest_file}")
            elif isinstance(existing, dict) and "items" in existing:
                existing["items"].append(json.load(open(fpath)))
                f.seek(0)
                json.dump(existing, f, indent=2)
                f.truncate()
                log_line(f"✅ Injected {fname} into {dest_file} (dict format)")
            else:
                log_line(f"⚠️ Unknown format in {dest_file}, skipped {fname}")
    elif classification == "unknown":
        log_line(f"❓ Skipped (unknown type): {fname}")
    else:
        log_line(f"❌ Error reading {fname}")

with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")

log_line(f"\n📜 Merge log written to {LOG_PATH}")
