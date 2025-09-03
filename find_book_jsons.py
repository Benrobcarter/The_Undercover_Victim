import os
import json

# Define your base project directory
BASE_DIR = os.path.expanduser("~/Documents/the_undercover_victim")

# Define filename or folder keywords to look for
BOOK_KEYWORDS = [
    "BOOK", "quote_cards", "CROSSWALK_BOOK", "VEX_UNDERCOVER", "QUOTE_TO_CONTRADICTION", "TIMELINE_TO_CONTRADICTION",
    "MASTER_BOOK", "UNDERCOVER_VICTIM"
]

# Define content keys to look for inside JSON
BOOK_CONTENT_KEYS = {"chapter_title", "quote_id", "contradiction_id", "timeline_refs"}

# Storage for results
book_files = []

# Walk through the project and identify relevant .json files
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, BASE_DIR)

            # Quick keyword filter by name or location
            if any(keyword in file for keyword in BOOK_KEYWORDS) or "04_book" in rel_path or "07_meta" in rel_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # Match by content structure
                        flat_data = json.dumps(data)
                        if any(key in flat_data for key in BOOK_CONTENT_KEYS):
                            book_files.append({"filename": rel_path})
                except Exception as e:
                    print(f"⚠️ Failed to read {rel_path}: {e}")

# Output results
output_path = os.path.join(BASE_DIR, "BOOK_RELEVANT_FILES_INDEX_auto.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(book_files, f, indent=2)

print(f"\n✅ Found {len(book_files)} book-related JSON files.")
print(f"📄 Saved to: {output_path}")
