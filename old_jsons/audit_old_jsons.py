folder = "/Users/bencarter/Documents/The_Undercover_Victim/old_jsons"
import os
import json

folder = "."
print(f"\n🔍 Auditing JSON files in: {os.path.abspath(folder)}\n")

for fname in os.listdir(folder):
    if fname.endswith(".json"):
        path = os.path.join(folder, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"✅ {fname} is valid.")
        except Exception as e:
            print(f"❌ {fname} is broken: {e}")

