#!/usr/bin/env python3
import json, os, sys, datetime, shutil

PROJECT = os.path.expanduser("~/Documents/the_undercover_victim")
BOOK_MASTER = os.path.join(PROJECT, "04_book/BOOK_MASTER_MERGED_POC_2025-08-27_v5.2.json")
CROSSWALK = os.path.join(PROJECT, "07_meta/CROSSWALK_BOOK_SHARD_TIMELINE_2025-08-31.json")
QUOTES = os.path.join(PROJECT, "05_public/quote_cards.json")
QUOTE_LINKS = os.path.join(PROJECT, "07_meta/CONTRA_QUOTE_LINKS_PATCH.json")
INSERTS_GLOBS = [
    os.path.join(PROJECT, "07_meta/UPDATED_BOOK_SECTION_3X_PALMER_INSERT_v2.json"),
    os.path.join(PROJECT, "07_meta/BOOK_SECTION_3X_VERITAS_INSERT_PALMER.json"),
]

OUT_DIR = os.path.join(PROJECT, "04_book/exports_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
os.makedirs(OUT_DIR, exist_ok=True)

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_copy(src, dst):
    shutil.copy2(src, dst)

# 1) Load sources (book master is required)
book = load_json(BOOK_MASTER)

# Extract meta and chapters
meta = book.get("meta", {})
chapters = book.get("chapters", book.get("sections", []))  # fallback if schema is 'sections'

# Basic selection helpers
def by_prefix(prefixes):
    picked, rest = [], []
    for ch in chapters:
        cid = ch.get("chapter_id") or ch.get("id") or ""
        if any(cid.startswith(p) for p in prefixes):
            picked.append(ch)
        else:
            rest.append(ch)
    return picked, rest

# 2) Split: Section 2 core (sec2_*)
sec2_chaps, remainder = by_prefix(["sec2_"])

# Foreword/Intro etc (everything else becomes 'core_sec1_and_intro' for now)
core1 = remainder

# 3) Write core shards
def write_json(name, obj):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path

# book_core_sec2.json
path_sec2 = write_json("book_core_sec2.json", {
    "meta_ref": "book_meta.json",
    "type": "book_core",
    "section": "sec2",
    "chapters": sec2_chaps
})

# book_core_sec1_and_intro.json
path_core1 = write_json("book_core_sec1_and_intro.json", {
    "meta_ref": "book_meta.json",
    "type": "book_core",
    "section": "intro_and_other",
    "chapters": core1
})

# 4) Inserts shard (if any exist)
inserts_payload = []
for p in INSERTS_GLOBS:
    if os.path.exists(p):
        inserts_payload.append(load_json(p))

path_inserts = None
if inserts_payload:
    path_inserts = write_json("book_inserts.json", {
        "type": "book_inserts",
        "inserts": inserts_payload
    })

# 5) Crosswalk shard (verbatim copy)
if os.path.exists(CROSSWALK):
    safe_copy(CROSSWALK, os.path.join(OUT_DIR, "book_crosswalk.json"))

# 6) Quotes shard (quotes + tether links merged under one top-level)
quotes_obj = load_json(QUOTES) if os.path.exists(QUOTES) else []
links_obj = load_json(QUOTE_LINKS) if os.path.exists(QUOTE_LINKS) else {}
path_quotes = write_json("book_quotes.json", {
    "type": "book_quotes",
    "quote_cards": quotes_obj,
    "contradiction_links_patch": links_obj
})

# 7) Meta shard: carry global book meta + a file_index pointing to these shards
file_index = [
    {"name": "book_core_sec2.json"},
    {"name": "book_core_sec1_and_intro.json"},
    {"name": "book_inserts.json"} if path_inserts else {"name": None},
    {"name": "book_crosswalk.json"},
    {"name": "book_quotes.json"},
    {"name": "book_overlays.json"},  # will be written next
]
file_index = [x for x in file_index if x["name"]]

meta_out = {
    "type": "book_meta",
    "generated_at": datetime.datetime.now().isoformat(),
    "source_master": os.path.relpath(BOOK_MASTER, PROJECT),
    "meta": meta,
    "file_index": file_index
}
write_json("book_meta.json", meta_out)

# 8) Overlays shard (room for future dashboard/labels; keep minimal for now)
write_json("book_overlays.json", {
    "type": "book_overlays",
    "notes": "Place overlay/labelling/json that the book references.",
    "version": "1.0.0"
})

print("Wrote shards to:", OUT_DIR)

