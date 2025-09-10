#!/usr/bin/env python3
import json, hashlib, os, sys

if len(sys.argv) != 2:
    print("Usage: python3 hash_audio.py <vex_json_file>")
    sys.exit(1)

json_path = os.path.abspath(sys.argv[1])
with open(json_path, "r") as f:
    data = json.load(f)

audio_rel = data.get("links", {}).get("audio_local_path")
if not audio_rel:
    print("No links.audio_local_path in JSON")
    sys.exit(1)

# Project root = two levels up from the VEX JSON (…/01_evidence/vex/… -> root)
project_root = os.path.abspath(os.path.join(os.path.dirname(json_path), "..", ".."))
audio_path = audio_rel if os.path.isabs(audio_rel) else os.path.join(project_root, audio_rel)

if not os.path.isfile(audio_path):
    print(f"Audio file not found: {audio_path}")
    sys.exit(1)

sha256 = hashlib.sha256(open(audio_path, "rb").read()).hexdigest()
print("SHA-256:", sha256)

data.setdefault("links", {})["audio_sha256"] = sha256
with open(json_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"Updated {json_path} with audio_sha256.")
