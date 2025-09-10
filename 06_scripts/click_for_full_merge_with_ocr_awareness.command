import os
import json
import hashlib
import sys

def hash_file(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def process_entry(entry, json_path):
    try:
        audio_rel = entry.get("links", {}).get("audio_local_path")
        if not audio_rel:
            return False

        audio_path = os.path.join(os.path.dirname(json_path), audio_rel)
        if not os.path.exists(audio_path):
            print(f"[⚠️] Audio file not found: {audio_path}")
            return False

        sha = hash_file(audio_path)
        entry["links"]["audio_sha256"] = sha
        print(f"[✅] Hashed {audio_rel} → {sha}")
        return True

    except Exception as e:
        print(f"[❌] Error processing audio: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: hash_audio.py <path_to_vex_json>")
        return

    json_path = sys.argv[1]
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = False

    try:
        if isinstance(data, list):
            for entry in data:
                updated |= process_entry(entry, json_path)
        elif isinstance(data, dict):
            updated |= process_entry(data, json_path)
        else:
            print(f"[⚠️] Unexpected JSON structure: {type(data)}")

        if updated:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"[💾] Updated file saved: {json_path}")
        else:
            print(f"[ℹ️] No audio hashes added in: {json_path}")

    except Exception as e:
        print(f"[❌] Fatal error: {e}")

if __name__ == "__main__":
    main()

